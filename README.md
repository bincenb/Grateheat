# GrateHeat

Interactive website for our NYAS Junior Academy project, *Climatizing Infrastructure: Green Retrofit* (Fall 2026). GrateHeat recovers waste heat from NYC subway grates and sends it to nearby public schools.

The site has three parts:

1. **3D model.** The grate module, a street cutaway, and the fin test rig. You can rotate them, lift the grate, and cut the module open.
2. **School map.** The 179 school buildings within 150 m of an underground subway line, with the 19 we would start with.
3. **Calculator.** A simple version of our energy model. Change the grate air speed, grate size, and number of modules to see heat, CO2, and cost.

## How to publish it

1. Upload everything in this folder to the top level of a GitHub repository (not inside a subfolder).
2. Go to **Settings → Pages**. Under "Build and deployment," pick **Deploy from a branch**, then choose **main** and **/ (root)**, and save.
3. After a minute or two the site is live at `https://<your-username>.github.io/<repo-name>/`.

The site needs a web server to run, so opening `index.html` by double-clicking won't load the models. To test on your own computer, run `python3 -m http.server` in this folder and go to `http://localhost:8000`.

## What's inside

| Path | What it is |
|---|---|
| `index.html`, `app.js` | The page |
| `calc.js` | The energy model the calculator uses (fixed values are listed at the top) |
| `data/schools.json` | School buildings within 250 m of an underground line, from NYC Open Data, LL84 2024, and the NYS disadvantaged community map |
| `data/tunnels.json` | Underground lines, drawn as straight lines between stations |
| `models/` | STL files for the 3D viewer. The same files can be 3D printed. |
| `vendor/` | three.js (MIT) and Leaflet (BSD-2), included so the site works without outside links |
| `fonts/` | Space Grotesk and IBM Plex Sans (SIL Open Font License) |

Map tiles © OpenStreetMap contributors.
