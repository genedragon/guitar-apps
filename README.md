# Guitar Practice Suite

Three browser-based guitar practice tools that run entirely on your device. No
accounts, no server-side code, and no audio ever leaves your browser.

- **Tuner** (`tuner.html`): listens through your mic, detects the pitch, and
  shows which way to turn the peg, with the string lit on a fretboard.
- **Fret Player** (`index.html`): a scrolling fretboard that shows you where to
  play. Fret-number bubbles flow toward a hit line; play each note as it
  arrives. Optional mic scoring lights notes green as you hit them. Tracks:
  a C-major scale, the Seven Nation Army riff, a C-Am-F-G chord drill, and a
  three-stage progressive chord trainer for "Nash dom" (Am-Dm, then four
  chords with a six-stroke strum, then the full verse). Backing is a metronome
  or a synthesized band (drums plus a bass that follows the chord changes),
  always with a one-bar count-in.
- **Chord Trainer** (`trainer.html`): shows a chord diagram and listens as you
  play, verifying the whole chord (FFT chroma detection), then auto-advances.
  A **Practice** selector switches between all chords and a song's chord order
  so you can drill the actual switches, with a "next chord" hint.

## Running it

Everything is static HTML plus vanilla JavaScript using the Web Audio API.
There is **no build step and no dependencies**.

**Local server (recommended).** A tiny standard-library Python server maps
extensionless paths (`/`, `/tuner`, `/trainer`) to the HTML files:

```bash
python3 serve.py                      # 127.0.0.1:8799
python3 serve.py --port 8080 --bind 127.0.0.1
```

Then open <http://127.0.0.1:8799/>. Microphone access needs a secure context
(`https://` or `localhost`), which this satisfies.

**Any static host.** The nav links are relative (`index.html`, `tuner.html`,
`trainer.html`), so the files work as-is on GitHub Pages (including under a
`/repo-name/` path), S3, Netlify and similar, or opened straight from disk.
`serve.py` additionally gives you the clean `/tuner` and `/trainer` URLs.

## How it works

- **Pitch detection** (tuner, fret player) uses time-domain autocorrelation to
  find the fundamental frequency. It is monophonic, so it suits single notes.
- **Chord detection** (chord trainer) maps the FFT spectrum into a 12-bin
  chroma vector with a rolling average, a noise-floor calibration, and a
  sensitivity setting. It checks that every tone of the chord is present.
- **Backing audio** is generated live with Web Audio oscillators (drums, bass,
  click). There are no audio samples.
- **Progress** (best scores, per-chord mastery) and settings are stored in
  `localStorage` on your device. Nothing is sent anywhere.
- The microphone is released whenever the page is hidden or closed, so the
  apps do not hold the mic against other apps on mobile.

Settings live behind a gear button (a side drawer on desktop, a bottom sheet on
mobile): string orientation, loop, backing on/off, audio sync, mic sync,
sensitivity and auto-advance.

## Notes and limitations

- **Bluetooth latency.** Bluetooth adds output and input delay. The Fret Player
  has *Audio sync* and *Mic sync* calibrations (tap or strum to a click) so the
  backing and the scoring line up with the visuals.
- **Speaker bleed.** The mic can hear the backing through the speaker.
  Headphones give the cleanest scoring.
- **Monophonic scoring in the Fret Player.** Its chord tracks require at least
  two distinct chord tones within the strum window, which rejects a single
  string but is not a full fingering check. For strict whole-chord
  verification use the Chord Trainer.
- **Song content.** The song stages use commonly published chord progressions
  and a standard strumming pattern for practice. They are not transcriptions of
  any particular tab or recording.
- Best in a reasonably quiet room with a clear pick attack. Tune first.

## Browser support

Any modern browser with the Web Audio API and `getUserMedia` (Chrome, Firefox,
Safari, Edge; desktop and mobile).

## License

MIT. See [LICENSE](LICENSE).
