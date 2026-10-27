const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const mode = process.argv[2] || 'test';
(async () => {
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('console', m => console.log('page:', m.text()));
  p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('http://localhost:8765/reel/reel.html');
  await p.waitForFunction(() => window.__ready, null, { timeout: 120000 });
  if (mode === 'test') {
    console.log(JSON.stringify(await p.evaluate(() => window.__info)));
    fs.mkdirSync('test', { recursive: true });
    const times = (process.argv[3] || '1,3,4.6,6.5,7.6,9,11.5,13,15,16.5,18.3,21,23').split(',').map(Number);
    for (const t of times) { await p.evaluate(t => window.renderAt(t), t); await p.screenshot({ path: `test/t${t}.jpg`, type: 'jpeg', quality: 80 }); }
  } else {
    const fps = 30, N = Math.round(24 * fps);
    const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', 'video.mp4'], { stdio: ['pipe', 'ignore', 'inherit'] });
    for (let i = 0; i < N; i++) {
      await p.evaluate(t => window.renderAt(t), i / fps);
      const buf = await p.screenshot({ type: 'jpeg', quality: 95 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 60 === 0) console.log('frame', i, '/', N);
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await b.close();
})();
