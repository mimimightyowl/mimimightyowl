"""Generate assets/header-{dark,light}.svg. Run: python3 scripts/gen_header.py assets"""
from pathlib import Path
import sys

out_dir = Path(sys.argv[1])
out_dir.mkdir(parents=True, exist_ok=True)

MONO = "ui-monospace, 'SF Mono', SFMono-Regular, Menlo, Consolas, 'Liberation Mono', 'DejaVu Sans Mono', monospace"
W, H = 808, 240
WX, WY, WW, WH, WR = 4, 14, 800, 212, 12
BAR_H = 36
X = 38

PALETTES = {
    "dark": dict(
        win_bg="#1a1b26", win_stroke="#2b2f44", bar_bg="#16161e",
        blob1="#7aa2f7", blob2="#bb9af7", blob_op="0.17",
        title="#565f89", prompt="#9ece6a", cmd="#c0caf5", cursor="#7aa2f7",
        name1="#7aa2f7", name2="#bb9af7", sub="#a9b1d6",
    ),
    "light": dict(
        win_bg="#e1e2e7", win_stroke="#c4c8da", bar_bg="#d5d6db",
        blob1="#2e7de9", blob2="#9854f1", blob_op="0.13",
        title="#848cb5", prompt="#587539", cmd="#3760bf", cursor="#2e7de9",
        name1="#2e7de9", name2="#9854f1", sub="#6172b0",
    ),
}

NAME = "Tracy"
SUBTITLE = "Software Engineer  ·  Tbilisi, Georgia"
TITLE = "tracy@tbilisi — zsh"
CMD = "whoami"


def typing_block(p):
    """One <text> per typing step, each visible for its slice of the timeline."""
    t, step, hold = 0.6, 0.12, 0.45

    def text(typed, cursor, begin, dur=None):
        cur = f'<tspan fill="{p["cursor"]}">█</tspan>' if cursor else ""
        if dur is None:
            anim = f'<set attributeName="visibility" to="visible" begin="{begin:.2f}s" fill="freeze"/>'
        else:
            anim = f'<set attributeName="visibility" to="visible" begin="{begin:.2f}s" dur="{dur:.2f}s"/>'
        return (f'  <text x="{X}" y="86" visibility="hidden" xml:space="preserve">'
                f'<tspan fill="{p["prompt"]}">~ $ </tspan>'
                f'<tspan fill="{p["cmd"]}">{typed}</tspan>{cur}{anim}</text>')

    lines = [text("", True, 0.0, t)]
    for i in range(1, len(CMD)):
        lines.append(text(CMD[:i], True, t + (i - 1) * step, step))
    t_full = t + (len(CMD) - 1) * step
    lines.append(text(CMD, True, t_full, hold))
    t_done = t_full + hold
    lines.append(text(CMD, False, t_done))
    return "\n".join(lines), t_done


def reveal(begin, inner):
    return (f'  <g opacity="0">\n'
            f'    <animate attributeName="opacity" from="0" to="1" dur="0.35s" begin="{begin:.2f}s" fill="freeze"/>\n'
            f'    <animateTransform attributeName="transform" type="translate" from="0 6" to="0 0" dur="0.35s" begin="{begin:.2f}s" fill="freeze"/>\n'
            f'{inner}\n  </g>')


def build(theme, p):
    typed, t_done = typing_block(p)
    t_name = t_done + 0.15
    t_sub = t_name + 0.25
    t_prompt = t_sub + 0.35
    i = theme[0]  # id prefix, keeps ids unique if both files ever share a page
    name = f'    <text x="{X}" y="140" font-size="40" font-weight="700" fill="url(#{i}-name)">{NAME}</text>'
    sub = f'    <text x="{X}" y="170" fill="{p["sub"]}" xml:space="preserve">{SUBTITLE}</text>'
    prompt = (f'    <text x="{X}" y="208" xml:space="preserve"><tspan fill="{p["prompt"]}">~ $ </tspan>'
              f'<tspan fill="{p["cursor"]}">█<animate attributeName="fill-opacity" values="1;1;0;0" '
              f'keyTimes="0;0.5;0.5;1" dur="1.1s" begin="{t_prompt:.2f}s" repeatCount="indefinite"/></tspan></text>')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="{i}-title">
<title id="{i}-title">{NAME} — Software Engineer, Tbilisi, Georgia</title>
<defs>
  <clipPath id="{i}-win"><rect x="{WX}" y="{WY}" width="{WW}" height="{WH}" rx="{WR}"/></clipPath>
  <linearGradient id="{i}-name" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{p["name1"]}"/><stop offset="1" stop-color="{p["name2"]}"/>
  </linearGradient>
  <radialGradient id="{i}-b1"><stop offset="0" stop-color="{p["blob1"]}" stop-opacity="{p["blob_op"]}"/><stop offset="1" stop-color="{p["blob1"]}" stop-opacity="0"/></radialGradient>
  <radialGradient id="{i}-b2"><stop offset="0" stop-color="{p["blob2"]}" stop-opacity="{p["blob_op"]}"/><stop offset="1" stop-color="{p["blob2"]}" stop-opacity="0"/></radialGradient>
</defs>
<rect x="{WX}" y="{WY}" width="{WW}" height="{WH}" rx="{WR}" fill="{p["win_bg"]}"/>
<g clip-path="url(#{i}-win)">
  <ellipse cx="140" cy="70" rx="380" ry="210" fill="url(#{i}-b1)"><animate attributeName="cx" values="140;210;140" dur="16s" repeatCount="indefinite"/></ellipse>
  <ellipse cx="700" cy="230" rx="360" ry="190" fill="url(#{i}-b2)"><animate attributeName="cx" values="700;630;700" dur="19s" repeatCount="indefinite"/></ellipse>
  <rect x="{WX}" y="{WY}" width="{WW}" height="{BAR_H}" fill="{p["bar_bg"]}"/>
</g>
<rect x="{WX}" y="{WY}" width="{WW}" height="{WH}" rx="{WR}" fill="none" stroke="{p["win_stroke"]}"/>
<circle cx="30" cy="32" r="6" fill="#ff5f57"/><circle cx="50" cy="32" r="6" fill="#febc2e"/><circle cx="70" cy="32" r="6" fill="#28c840"/>
<g font-family="{MONO}" font-size="17">
  <text x="{W / 2:.0f}" y="37" text-anchor="middle" font-size="13" fill="{p["title"]}">{TITLE}</text>
{typed}
{reveal(t_name, name)}
{reveal(t_sub, sub)}
{reveal(t_prompt, prompt)}
</g>
</svg>
'''


for theme, p in PALETTES.items():
    path = out_dir / f"header-{theme}.svg"
    path.write_text(build(theme, p), encoding="utf-8")
    print(f"wrote {path} ({path.stat().st_size} bytes)")
