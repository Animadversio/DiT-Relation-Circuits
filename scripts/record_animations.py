#!/usr/bin/env python3
"""Record the interactive Figure 6 circuit widget as GIFs.

For each target (widget id, mode), headless Chromium loads index.html,
steps the widget through every stage, screenshots after each step, then
PIL composes the frames into a looping GIF in media/.

Outputs land in media/ (gitignored by default).

Run:
    pip install playwright pillow
    playwright install chromium
    python scripts/record_animations.py
"""
import io
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parent.parent
INDEX = REPO / "index.html"
MEDIA = REPO / "media"
MEDIA.mkdir(exist_ok=True)

# (widget_id, mode | None, stage_count, output_filename)
TARGETS = [
    ("circuit-widget", "rte", 5, "circuit-rte.gif"),
    ("circuit-widget", "t5",  6, "circuit-t5.gif"),
    # Uncomment to also record Fig 3a / 3b:
    # ("synopsis-widget",  None, 5, "synopsis-widget.gif"),
    # ("screening-widget", None, 5, "screening-widget.gif"),
]

FRAME_MS     = 1500   # per-stage hold in the GIF
END_PAUSE_MS = 2000   # extra hold on the final frame so the result lingers
STEP_WAIT_MS = 700    # wall-clock pause after clicking Step (CSS transition is 0.5s)


def record(page, widget_id, mode, stage_count):
    """Reset to stage 0 (in the given mode) then capture stage 1..N."""
    if mode is not None:
        page.click(f'#{widget_id} .circuit-toggle button[data-mode="{mode}"]')
        page.wait_for_timeout(300)
    page.click(f'#{widget_id} .circuit-controls button[data-action="reset"]')
    page.wait_for_timeout(STEP_WAIT_MS)
    widget = page.query_selector(f"#{widget_id}")
    frames = [Image.open(io.BytesIO(widget.screenshot()))]
    for _ in range(stage_count):
        page.click(f'#{widget_id} .circuit-controls button[data-action="step"]')
        page.wait_for_timeout(STEP_WAIT_MS)
        frames.append(Image.open(io.BytesIO(widget.screenshot())))
    return frames


def make_gif(frames, path):
    """Quantize each frame and write a looping, optimized GIF."""
    # Adaptive 128-color palette per frame keeps gradients smooth at reasonable size
    pframes = [f.convert("P", palette=Image.ADAPTIVE, colors=128) for f in frames]
    durations = [FRAME_MS] * len(pframes)
    durations[-1] += END_PAUSE_MS
    pframes[0].save(
        path,
        save_all=True,
        append_images=pframes[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(f"  {path.name}: {len(pframes)} frames · {sum(durations)/1000:.1f}s · {path.stat().st_size/1024:.0f} KB")


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": 1400, "height": 1000},
            device_scale_factor=2,
        )
        page = ctx.new_page()
        page.goto(f"file://{INDEX}")
        page.wait_for_load_state("networkidle")
        for widget_id, mode, stages, fname in TARGETS:
            print(f"Recording {widget_id}{f' [{mode}]' if mode else ''}...")
            page.evaluate(
                f'document.getElementById("{widget_id}").scrollIntoView({{block: "center"}})'
            )
            page.wait_for_timeout(400)
            frames = record(page, widget_id, mode, stages)
            make_gif(frames, MEDIA / fname)
        browser.close()
    print("Done.")


if __name__ == "__main__":
    main()
