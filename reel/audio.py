"""Synthesize the reel soundtrack (120 BPM phonk-style beat + SFX) with numpy only. Writes audio.wav."""
import numpy as np, wave

SR = 44100
DUR = 24.0
N = int(SR * DUR)
BEAT = 0.5
rng = np.random.default_rng(3)

music = np.zeros((N, 2))
sfx = np.zeros((N, 2))


def tt(d):
    return np.arange(int(d * SR)) / SR


def add(buf, sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if sig.ndim == 1:
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        sig = np.stack([sig * l * 1.414, sig * r * 1.414], 1)
    j = min(N, i + len(sig))
    if j > i:
        buf[i:j] += sig[: j - i] * gain


def fft_filter(x, lo=None, hi=None):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    m = np.ones_like(f)
    if lo: m *= 1 / (1 + (lo / np.maximum(f, 1)) ** 4)
    if hi: m *= 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * m, len(x))


def sweep(x, fc_fn, bw=0.6, kind='band'):
    """Time-varying filter via windowed overlap-add. fc_fn(t)->Hz."""
    n, hop = 1024, 256
    win = np.hanning(n)
    out = np.zeros(len(x) + n)
    norm = np.zeros(len(x) + n)
    f = np.fft.rfftfreq(n, 1 / SR)
    for s in range(0, len(x), hop):
        seg = np.zeros(n); c = x[s:s + n]; seg[:len(c)] = c
        fc = fc_fn(s / SR)
        if kind == 'band':
            m = np.exp(-0.5 * (np.log2(np.maximum(f, 1) / fc) / bw) ** 2)
        else:  # lowpass
            m = 1 / (1 + (f / fc) ** 4)
        y = np.fft.irfft(np.fft.rfft(seg * win) * m, n)
        out[s:s + n] += y * win; norm[s:s + n] += win ** 2
    return (out / np.maximum(norm, 1e-3))[: len(x)]


def reverb(x, dur=1.6, mix=0.3, hp=300):
    ir_t = tt(dur)
    irs = []
    for ch in range(2):
        ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 6.5 / dur)
        irs.append(fft_filter(ir, lo=hp, hi=7000))
    L = len(x) + len(ir_t)
    out = np.zeros((L, 2))
    for ch in range(2):
        src = x[:, ch] if x.ndim == 2 else x
        y = np.fft.irfft(np.fft.rfft(src, L) * np.fft.rfft(irs[ch], L), L)
        out[:, ch] = y / (np.abs(irs[ch]).sum() ** 0.5 * 4)
    dry = np.zeros((L, 2)); dry[: len(x)] = x if x.ndim == 2 else np.stack([x, x], 1)
    return dry * (1 - mix) + out * mix * 3


# ---------- instruments ----------
def kick():
    t = tt(0.45)
    f = 45 + 110 * np.exp(-t * 35)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    s += rng.standard_normal(len(t)) * np.exp(-t * 300) * 0.4
    return np.tanh(s * 2.2) * 0.9


def b808(freq, dur):
    t = tt(dur)
    f = freq * (1 + 0.8 * np.exp(-t * 40))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR)
    env = np.minimum(1, t / 0.005) * np.exp(-t * 1.3)
    env[-int(0.03 * SR):] *= np.linspace(1, 0, int(0.03 * SR))
    return np.tanh(s * env * 3.0) * 0.55


def clap():
    t = tt(0.35)
    n = rng.standard_normal(len(t))
    env = np.zeros(len(t))
    for d in (0, 0.011, 0.022):
        env += (t >= d) * np.exp(-np.maximum(t - d, 0) * (90 if d < 0.02 else 18))
    return fft_filter(n * env, lo=900, hi=6000) * 0.8


def snare():
    t = tt(0.25)
    s = fft_filter(rng.standard_normal(len(t)), lo=1500, hi=9000) * np.exp(-t * 22)
    s += np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * 0.5
    return s * 0.7


def hat(open_=False):
    t = tt(0.25 if open_ else 0.06)
    s = fft_filter(rng.standard_normal(len(t)), lo=7000) * np.exp(-t * (14 if open_ else 80))
    return s * 0.35


def cowbell(freq, dur=0.32):
    t = tt(dur)
    sq = lambda f: np.sign(np.sin(2 * np.pi * f * t))
    s = (sq(freq) + sq(freq * 1.4815)) * 0.5
    s = fft_filter(s, lo=freq * 0.8, hi=freq * 4)
    env = np.exp(-t * 9) * 0.85 + np.exp(-t * 60) * 0.3
    return s * env * 0.5


def pad_chord(freqs, dur):
    t = tt(dur)
    s = np.zeros((len(t), 2))
    for i, f in enumerate(freqs):
        for d, ch in ((-0.12, 0), (0.12, 1)):
            ph = rng.uniform(0, 1)
            saw = 2 * ((f * (1 + d / 100) * t + ph) % 1) - 1
            s[:, ch] += saw
    env = np.minimum(1, t / 0.25) * np.minimum(1, (dur - t) / 0.25)
    s *= env[:, None] * 0.06
    return np.stack([fft_filter(s[:, 0], hi=1800), fft_filter(s[:, 1], hi=1800)], 1)


def riser(dur, f0=300, f1=6000):
    t = tt(dur)
    n = rng.standard_normal(len(t))
    s = sweep(n, lambda x: f0 * (f1 / f0) ** (x / dur), bw=0.5)
    tone = np.sin(2 * np.pi * np.cumsum(120 * (8 ** (t / dur))) / SR) * 0.25
    return (s + tone) * (t / dur) ** 2 * 0.7


def whoosh(dur=0.55, f0=400, f1=3500, peak=0.55):
    t = tt(dur)
    n = rng.standard_normal(len(t))
    s = sweep(n, lambda x: f0 * (f1 / f0) ** np.sin(np.pi * min(x / dur, 1) * 0.5) if x < dur * peak else f1 * (f0 / f1) ** ((x - dur * peak) / (dur * (1 - peak))), bw=0.7)
    env = np.where(t < dur * peak, (t / (dur * peak)) ** 2, ((dur - t) / (dur * (1 - peak))) ** 1.5)
    return s * env * 0.9


def impact(big=True):
    t = tt(2.5 if big else 1.0)
    f = 30 + 70 * np.exp(-t * 8)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * (1.6 if big else 4))
    s += fft_filter(rng.standard_normal(len(t)), hi=3000) * np.exp(-t * 14) * 0.6
    return np.tanh(s * 1.8) * 0.8


def clank():
    t = tt(1.2)
    s = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, a, d in
            ((523, 1, 5), (1307, 0.6, 7), (2149, 0.45, 9), (3371, 0.3, 12), (4410, 0.2, 16)))
    s += fft_filter(rng.standard_normal(len(t)), lo=2000) * np.exp(-t * 60) * 0.8
    s += np.sin(2 * np.pi * 85 * t) * np.exp(-t * 12) * 0.8
    return s * 0.35


def slice_():
    t = tt(0.35)
    n = rng.standard_normal(len(t))
    s = sweep(n, lambda x: 9000 * (0.3 ** (x / 0.35)), bw=0.35)
    return s * np.exp(-t * 7) * 0.8


def pop(f=700):
    t = tt(0.12)
    ff = f * (1 + 1.2 * np.minimum(t / 0.04, 1))
    return np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.exp(-t * 30) * 0.5


def tick(f=2500):
    t = tt(0.03)
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 200) * 0.35


def ding():
    t = tt(1.6)
    s = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, a, d in
            ((1318.5, 1, 2.5), (1318.5 * 2.76, 0.35, 5), (1318.5 * 5.4, 0.15, 8), (659.25, 0.4, 3)))
    return s * 0.35


def rumble(dur):
    t = tt(dur)
    b = np.cumsum(rng.standard_normal(len(t))); b -= np.convolve(b, np.ones(2000) / 2000, 'same')
    b = fft_filter(b, lo=25, hi=220); b /= np.abs(b).max()
    clack = np.zeros(len(t))
    for k in np.arange(0.12, dur, 0.27):
        i = int(k * SR); seg = tt(0.08)
        c = fft_filter(rng.standard_normal(len(seg)), lo=150, hi=1500) * np.exp(-seg * 60)
        clack[i:i + len(seg)] += c[: len(clack) - i] * (0.6 if int(k / 0.27) % 2 else 0.4)
    env = np.minimum(1, t / 0.8) * np.minimum(1, (dur - t) / 0.6)
    return (b * 0.9 + clack * 0.5) * env


# ---------- music arrangement ----------
A4 = 440.0
note = lambda semi: A4 * 2 ** (semi / 12)
chords = [[0, 3, 7], [-4, 0, 3], [-2, 2, 5], [-5, -2, 2]]       # Am F G Em (rel. A4)
roots = [55.0, 43.65, 49.0, 41.2]
mel = [[0, None, 3, 0, 7, None, 5, 3], [-4, None, 0, -4, 3, None, 0, -2],
       [-2, None, 2, -2, 5, None, 3, 2], [-5, None, -2, -5, 2, 3, 2, -2]]

KICKS = [0, 1.5, 2.25, 3.0]          # beats within a 4-beat bar (trap-ish)
bar_len = 4 * BEAT

def section(name, t):
    if t < 2.0: return 'intro'
    if 11.5 <= t < 12.0: return 'break'
    if 12.0 <= t < 15.5: return 'map'
    if 15.5 <= t < 16.0: return 'build'
    if t >= 23.5: return 'end'
    return 'full'

# pad through everything
pad = np.zeros((N, 2))
for b in range(12):
    c = pad_chord([note(s - 12) for s in chords[b % 4]], bar_len + 0.3)
    add(pad, c, b * bar_len)
pad_l = sweep(pad[:, 0], lambda x: 350 + 2500 * min(1, x / 2.0) if x < 2.0 else (2800 if x < 23.5 else 600), kind='lp')
pad_r = sweep(pad[:, 1], lambda x: 350 + 2500 * min(1, x / 2.0) if x < 2.0 else (2800 if x < 23.5 else 600), kind='lp')
music += np.stack([pad_l, pad_r], 1) * 0.9

cow = np.zeros((N, 2))
for b in range(12):
    t0 = b * bar_len
    # drums
    for kb in KICKS:
        tk = t0 + kb * BEAT
        if section('', tk) in ('full', 'map'):
            add(music, kick(), tk, 0.95)
    for cb in (1, 3):
        tc = t0 + cb * BEAT
        if section('', tc) == 'full':
            add(music, clap(), tc, 0.55); add(music, snare(), tc, 0.25)
    # hats: 8ths, with 16th/triplet rolls on last beat of every other bar
    for h in range(8):
        th = t0 + h * BEAT / 2
        if section('', th) in ('full', 'map'):
            add(music, hat(open_=(h == 7 and b % 2 == 0)), th, 0.6 if h % 2 == 0 else 0.4, pan=0.25)
    if b % 2 == 1:
        for r in range(6):
            th = t0 + 3 * BEAT + r * BEAT / 6
            if section('', th) == 'full':
                add(music, hat(), th, 0.25 + 0.05 * r, pan=0.25)
    # 808 on kicks, follows chord root
    for kb in KICKS:
        tk = t0 + kb * BEAT
        nxt = [x for x in KICKS if x > kb]
        d = ((nxt[0] if nxt else 4) - kb) * BEAT
        if section('', tk) in ('full', 'map'):
            f = roots[b % 4] * (2 if kb == 2.25 and b % 2 else 1)
            add(music, b808(f, d + 0.02), tk, 0.9)
    # cowbell melody
    for k, sm in enumerate(mel[b % 4]):
        if sm is None: continue
        tn = t0 + k * BEAT / 2
        if section('', tn) in ('full', 'intro'):
            add(cow, cowbell(note(sm)), tn, 0.8, pan=-0.2 if k % 2 else 0.2)
cow_f = np.stack([sweep(cow[:, ch], lambda x: 600 + 1200 * (x / 2) if x < 2.0 else 9000, kind='lp') for ch in range(2)], 1)
music += reverb(cow_f, 1.2, 0.25)[:N]

# drum fills
for r in range(8):                                 # 11.5 -> 12 snare roll
    add(music, snare(), 11.5 + r * BEAT / 8, 0.2 + 0.06 * r)
for r in range(16):                                # 15.5 -> 16 build
    add(music, snare(), 15.5 + r * BEAT / 16, 0.15 + 0.04 * r)
# final hit
add(music, kick(), 23.5, 1.0); add(music, b808(55.0, 0.5), 23.5, 0.9)

# ---------- SFX (timed to the visuals) ----------
add(sfx, rumble(2.6), 0.0, 1.0)
add(sfx, riser(2.0, 200, 5000), 0.0, 0.6)
add(sfx, whoosh(0.5, 300, 4000, 0.85), 1.55, 0.55)
add(sfx, impact(True), 2.0, 0.9)
add(sfx, rumble(1.6), 2.3, 0.35); add(sfx, rumble(1.6), 3.9, 0.3)
add(sfx, whoosh(0.7, 500, 3000), 3.85, 0.45, pan=0.3)
add(sfx, whoosh(0.5), 5.3, 0.5, pan=-0.3)
add(sfx, clank(), 6.0, 0.9); add(sfx, impact(False), 6.0, 0.4)
add(sfx, slice_(), 7.0, 0.7)
add(sfx, whoosh(0.5), 7.8, 0.5, pan=0.3)
for i, at in enumerate((8.4, 9.4, 10.4)):
    add(sfx, pop(600 + 150 * i), at, 0.9)
add(sfx, pop(1100), 11.2, 0.6)
add(sfx, riser(0.5, 800, 8000), 11.5, 0.5)
add(sfx, impact(False), 12.0, 0.7)
for i in range(18):                                 # counter ticks while dots pop in
    add(sfx, tick(2200 + 80 * i), 12.5 + i * 0.095, 0.7, pan=np.sin(i))
add(sfx, ding(), 14.4, 0.8); add(sfx, impact(False), 14.4, 0.4)
add(sfx, riser(0.5, 600, 9000), 15.5, 0.6)
for at in (16, 17, 18, 19):
    add(sfx, impact(at == 16), at, 0.75); add(sfx, whoosh(0.3, 800, 5000, 0.3), at - 0.05, 0.25)
add(sfx, whoosh(0.5, 300, 4000, 0.85), 19.6, 0.5)
add(sfx, impact(True), 20.0, 0.8)
add(sfx, whoosh(0.4, 600, 5000), 20.15, 0.4)
add(sfx, clank(), 20.4, 0.55)
add(sfx, pop(900), 21.4, 0.5); add(sfx, pop(1200), 22.6, 0.5)
add(sfx, impact(True), 23.5, 0.6)

sfx = reverb(sfx, 1.4, 0.18)[:N]
mix = music * 0.8 + sfx * 0.9
# sidechain-ish duck of music under big impacts is implicit; gentle master: HPF + soft clip
mix = np.stack([fft_filter(mix[:, ch], lo=28) for ch in range(2)], 1)
mix = np.tanh(mix / np.percentile(np.abs(mix), 99.7) * 0.9) * 0.97
fade = int(0.35 * SR); mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
pcm = (mix * 32767).astype('<i2')
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', mix.shape, float(np.abs(mix).max()))
