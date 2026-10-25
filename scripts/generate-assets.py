# Regenerates the animated SVGs in ./assets.  Usage: python3 scripts/generate-assets.py assets
import sys, os
from xml.sax.saxutils import escape

OUT = sys.argv[1]
MONO = "'JetBrains Mono','Fira Code','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
SANS = "'Segoe UI','Inter',-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif"

DEFS = """
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#071513"/>
    <stop offset="1" stop-color="#030908"/>
  </linearGradient>
  <linearGradient id="glass" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#16362f" stop-opacity=".85"/>
    <stop offset="1" stop-color="#0a1d19" stop-opacity=".85"/>
  </linearGradient>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#5ff2c0" stop-opacity=".7"/>
    <stop offset=".5" stop-color="#1f6f5b" stop-opacity=".25"/>
    <stop offset="1" stop-color="#5ff2c0" stop-opacity=".55"/>
  </linearGradient>
  <radialGradient id="aura" cx=".85" cy=".1" r=".8">
    <stop offset="0" stop-color="#2dd4a7" stop-opacity=".22"/>
    <stop offset="1" stop-color="#2dd4a7" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="aura2" cx=".05" cy="1" r=".7">
    <stop offset="0" stop-color="#14b88a" stop-opacity=".16"/>
    <stop offset="1" stop-color="#14b88a" stop-opacity="0"/>
  </radialGradient>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="3" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
    <path d="M28 0H0V28" fill="none" stroke="#1d4a40" stroke-opacity=".28" stroke-width="1"/>
  </pattern>
"""


def write(name, body):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(body)


# ---------------------------------------------------------------- terminal
def terminal():
    W, H = 880, 400
    x0, y0, lh = 40, 92, 27
    CW = 9.0  # approx monospace char width at 15px
    # (kind, text, extra) kinds: cmd (typed), out (fade in), raw svg
    script = [
        ("cmd", "whoami"),
        ("out", [("Christian Earl Siong", "#eafff7", True), ("  //  ", "#3b6b5f", False), ("Full Stack Developer", "#5ff2c0", True)]),
        ("cmd", "cat mission.txt"),
        ("out", [("Building modern web experiences — from idea to deployment.", "#a9c9bf", False)]),
        ("cmd", "ls ./stack"),
        ("out", [("next.js  ", "#eafff7", False), ("react  ", "#61dafb", False), ("node.js  ", "#8cc84b", False),
                 ("express  ", "#cfd8d5", False), ("mysql  ", "#4fa3d1", False), ("supabase", "#3ecf8e", False)]),
        ("cmd", "./deploy --prod"),
        ("out", [("✔ ", "#5ff2c0", True), ("build passed   ", "#a9c9bf", False), ("✔ ", "#5ff2c0", True),
                 ("db synced   ", "#a9c9bf", False), ("✔ ", "#5ff2c0", True), ("jwt secured   ", "#a9c9bf", False),
                 ("● ", "#5ff2c0", True), ("LIVE", "#5ff2c0", True)]),
    ]
    t = 0.6
    rows = []
    clips = []
    y = y0
    for i, (kind, payload) in enumerate(script):
        if kind == "cmd":
            n = len(payload)
            dur = max(0.35, n * 0.055)
            step = 0.055
            chars = "".join(
                f'<tspan opacity="0">{escape(ch) if ch != " " else "&#160;"}<animate attributeName="opacity" to="1" begin="{t + .25 + k * step:.2f}s" dur=".01s" fill="freeze"/></tspan>'
                for k, ch in enumerate(payload))
            rows.append(
                f'<g opacity="0"><animate attributeName="opacity" to="1" begin="{t:.2f}s" dur=".01s" fill="freeze"/>'
                f'<text x="{x0}" y="{y}" class="m"><tspan fill="#5ff2c0">christian</tspan><tspan fill="#3b6b5f">@</tspan>'
                f'<tspan fill="#2dd4a7">cs</tspan><tspan fill="#3b6b5f">:</tspan><tspan fill="#7fb8a8">~</tspan><tspan fill="#eafff7"> $&#160;</tspan>'
                f'<tspan fill="#eafff7">{chars}</tspan></text></g>')
            dur = n * step
            t += .25 + dur + .25
        else:
            spans = "".join(
                f'<tspan fill="{c}"{" font-weight=\"700\"" if b else ""}>{escape(s)}</tspan>' for s, c, b in payload)
            rows.append(
                f'<text x="{x0}" y="{y}" class="m" opacity="0">{spans}'
                f'<animate attributeName="opacity" to="1" begin="{t:.2f}s" dur=".35s" fill="freeze"/></text>')
            t += .45
            y += 10
        y += lh
    # final prompt + blinking cursor
    prompt_w = 15 * CW + 6
    rows.append(
        f'<g opacity="0"><animate attributeName="opacity" to="1" begin="{t:.2f}s" dur=".01s" fill="freeze"/>'
        f'<text x="{x0}" y="{y}" class="m"><tspan fill="#5ff2c0">christian</tspan><tspan fill="#3b6b5f">@</tspan>'
        f'<tspan fill="#2dd4a7">cs</tspan><tspan fill="#3b6b5f">:</tspan><tspan fill="#7fb8a8">~</tspan><tspan fill="#eafff7"> $&#160;</tspan>'
        f'<tspan fill="#5ff2c0">&#9608;<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" repeatCount="indefinite"/></tspan></text></g>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal: Christian Earl Siong, Full Stack Developer. Stack: Next.js, React, Node.js, Express, MySQL, Supabase.">
<defs>{DEFS}{"".join(clips)}</defs>
<style>.m{{font-family:{MONO};font-size:15px;}} .s{{font-family:{SANS};}}</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#bg)"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#grid)"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#aura)"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#aura2)"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="none" stroke="url(#edge)" stroke-width="1.5"/>
<path d="M17 1h{W - 34}a16 16 0 0 1 16 16v29H1V17A16 16 0 0 1 17 1z" fill="#0c211d" fill-opacity=".9"/>
<line x1="1" y1="46" x2="{W - 1}" y2="46" stroke="#1f4d42" stroke-opacity=".8"/>
<circle cx="26" cy="24" r="6" fill="#ff5f57"/><circle cx="46" cy="24" r="6" fill="#febc2e"/><circle cx="66" cy="24" r="6" fill="#28c840"/>
<text x="{W / 2}" y="29" text-anchor="middle" class="m" font-size="13" fill="#7fb8a8">christian@cs-dev — ~/portfolio — zsh</text>
<g transform="translate({W - 120},16)"><rect width="96" height="18" rx="9" fill="#5ff2c0" fill-opacity=".12" stroke="#5ff2c0" stroke-opacity=".5"/>
<circle cx="13" cy="9" r="3.5" fill="#5ff2c0"><animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>
<text x="56" y="13" text-anchor="middle" class="m" font-size="10.5" fill="#5ff2c0" letter-spacing="1.5">ONLINE</text></g>
{"".join(rows)}
<!-- scanline sweep -->
<linearGradient id="sweep" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5ff2c0" stop-opacity="0"/><stop offset=".5" stop-color="#5ff2c0" stop-opacity=".06"/><stop offset="1" stop-color="#5ff2c0" stop-opacity="0"/></linearGradient>
<rect x="2" y="48" width="{W - 4}" height="60" fill="url(#sweep)" opacity="0">
<animate attributeName="y" values="48;{H - 60};48" dur="7s" repeatCount="indefinite"/>
<animate attributeName="opacity" values="0;.5;0" dur="7s" repeatCount="indefinite"/></rect>
</svg>'''
    write("terminal.svg", svg)


# ---------------------------------------------------------------- architecture
def architecture():
    W, H = 880, 330
    cards = [
        ("FRONTEND", "the experience", ["Next.js", "React", "TypeScript", "Tailwind"], "#61dafb"),
        ("BACKEND", "the logic", ["Node.js", "Express", "REST APIs", "JWT Auth"], "#8cc84b"),
        ("DATABASE", "the memory", ["MySQL", "Supabase", "PostgreSQL", "Redis"], "#3ecf8e"),
    ]
    cw, ch, gap, top = 236, 176, 46, 40
    left = (W - (3 * cw + 2 * gap)) / 2
    parts = []
    for i, (title, sub, items, accent) in enumerate(cards):
        x = left + i * (cw + gap)
        d = .3 + i * .35
        lis = "".join(
            f'<g transform="translate(22,{82 + j * 22})"><rect width="6" height="6" y="-6" rx="1.5" fill="{accent}"/>'
            f'<text x="16" y="0" class="m" font-size="13.5" fill="#d7efe7">{escape(it)}</text></g>'
            for j, it in enumerate(items))
        parts.append(f'''<g transform="translate({x},{top})" opacity="0">
<animate attributeName="opacity" to="1" begin="{d:.2f}s" dur=".6s" fill="freeze"/>
<animateTransform attributeName="transform" type="translate" from="{x} {top + 14}" to="{x} {top}" begin="{d:.2f}s" dur=".6s" fill="freeze"/>
<rect width="{cw}" height="{ch}" rx="14" fill="url(#glass)"/>
<rect width="{cw}" height="{ch}" rx="14" fill="none" stroke="url(#edge)" stroke-width="1.2"/>
<rect x="22" y="0" width="44" height="2.5" rx="1" fill="{accent}" filter="url(#glow)"/>
<text x="22" y="38" class="s" font-size="15" font-weight="700" letter-spacing="3.5" fill="#eafff7">{title}</text>
<text x="22" y="57" class="m" font-size="11.5" fill="#5f9283">// {sub}</text>
{lis}
</g>''')
        if i < 2:
            px = x + cw + gap / 2
            py = top + ch / 2
            parts.append(f'''<g opacity="0"><animate attributeName="opacity" to="1" begin="{d + .3:.2f}s" dur=".5s" fill="freeze"/>
<line x1="{x + cw + 4}" y1="{py}" x2="{x + cw + gap - 4}" y2="{py}" stroke="#5ff2c0" stroke-opacity=".5" stroke-dasharray="3 5">
<animate attributeName="stroke-dashoffset" from="16" to="0" dur=".8s" repeatCount="indefinite"/></line>
<circle cx="{px}" cy="{py}" r="13" fill="#071513" stroke="#5ff2c0" stroke-opacity=".7"/>
<text x="{px}" y="{py + 5.5}" text-anchor="middle" class="s" font-size="17" font-weight="700" fill="#5ff2c0">+</text></g>''')

    # bottom bus line + result pill
    by = top + ch + 46
    xs = [left + i * (cw + gap) + cw / 2 for i in range(3)]
    bus = "".join(
        f'<path d="M{xx} {top + ch} V{by - 16} H{W / 2}" fill="none" stroke="#2dd4a7" stroke-opacity=".35" stroke-width="1.2"/>'
        for xx in xs)
    packets = "".join(
        f'<circle r="3" fill="#5ff2c0" filter="url(#glow)"><animateMotion dur="2.6s" begin="{1.6 + k * .45:.2f}s" repeatCount="indefinite" path="M{xx} {top + ch} V{by - 16} H{W / 2}"/></circle>'
        for k, xx in enumerate(xs))
    pill_w = 300
    result = f'''<g opacity="0"><animate attributeName="opacity" to="1" begin="1.5s" dur=".6s" fill="freeze"/>
{bus}{packets}
<rect x="{W / 2 - pill_w / 2}" y="{by - 16}" width="{pill_w}" height="44" rx="22" fill="#0c2a23" stroke="#5ff2c0" stroke-width="1.4" filter="url(#glow)"/>
<text x="{W / 2}" y="{by + 12}" text-anchor="middle" class="s" font-size="17" font-weight="700" letter-spacing="5" fill="#5ff2c0">= FULL STACK</text>
<rect x="{W / 2 - pill_w / 2}" y="{by - 16}" width="{pill_w}" height="44" rx="22" fill="none" stroke="#5ff2c0" stroke-opacity=".6">
<animate attributeName="stroke-opacity" values=".7;0;.7" dur="2.4s" repeatCount="indefinite"/></rect></g>'''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Frontend (Next.js, React, TypeScript, Tailwind) + Backend (Node.js, Express, REST APIs, JWT Auth) + Database (MySQL, Supabase, PostgreSQL, Redis) = Full Stack">
<defs>{DEFS}</defs>
<style>.m{{font-family:{MONO};}} .s{{font-family:{SANS};}}</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#bg)"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#grid)"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#aura)"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="none" stroke="url(#edge)" stroke-width="1.5"/>
{"".join(parts)}
{result}
</svg>'''
    write("architecture.svg", svg)


# ---------------------------------------------------------------- section headers
def header(name, label, index):
    W, H = 880, 64
    text = f"{index:02d} // {label}"
    tw = len(text) * 13.6
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(label)}">
<defs>{DEFS}
<linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="#5ff2c0" stop-opacity=".9"/><stop offset="1" stop-color="#5ff2c0" stop-opacity="0"/></linearGradient>
<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#eafff7" stop-opacity="0"/><stop offset=".5" stop-color="#eafff7" stop-opacity=".9"/><stop offset="1" stop-color="#eafff7" stop-opacity="0"/></linearGradient>
</defs>
<style>.m{{font-family:{MONO};}}</style>
<rect x="6" y="20" width="22" height="22" rx="5" fill="none" stroke="#5ff2c0" stroke-width="1.5" filter="url(#glow)"/>
<rect x="12" y="26" width="10" height="10" rx="2" fill="#5ff2c0"><animate attributeName="opacity" values="1;.3;1" dur="2s" repeatCount="indefinite"/></rect>
<text x="44" y="39" class="m" font-size="18" font-weight="700" letter-spacing="2.5" fill="#eafff7"><tspan fill="#5ff2c0">{index:02d}</tspan><tspan fill="#3b6b5f"> // </tspan>{escape(label.upper())}</text>
<rect x="{44 + tw + 18}" y="31.25" width="{W - 6 - (44 + tw + 18)}" height="1.5" fill="url(#ln)"/>
<rect x="{44 + tw + 18}" y="31" width="80" height="2.5" fill="url(#sh)">
<animate attributeName="x" from="{44 + tw + 18}" to="{W - 80}" dur="3.2s" repeatCount="indefinite"/></rect>
</svg>'''
    write(name, svg)


# ---------------------------------------------------------------- footer
def footer():
    W, H = 880, 120
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Thanks for visiting">
<defs>{DEFS}
<linearGradient id="wv" x1="0" x2="1"><stop offset="0" stop-color="#5ff2c0" stop-opacity="0"/><stop offset=".5" stop-color="#5ff2c0" stop-opacity=".9"/><stop offset="1" stop-color="#5ff2c0" stop-opacity="0"/></linearGradient>
</defs>
<style>.m{{font-family:{MONO};}}</style>
<path fill="none" stroke="url(#wv)" stroke-width="1.6" filter="url(#glow)">
<animate attributeName="d" dur="6s" repeatCount="indefinite"
values="M0 40 C 180 10, 300 70, 440 40 S 700 10, 880 40;M0 40 C 180 70, 300 10, 440 40 S 700 70, 880 40;M0 40 C 180 10, 300 70, 440 40 S 700 10, 880 40"/></path>
<path fill="none" stroke="url(#wv)" stroke-width="1" stroke-opacity=".45">
<animate attributeName="d" dur="8s" repeatCount="indefinite"
values="M0 46 C 200 76, 320 16, 440 46 S 680 76, 880 46;M0 46 C 200 16, 320 76, 440 46 S 680 16, 880 46;M0 46 C 200 76, 320 16, 440 46 S 680 76, 880 46"/></path>
<text x="{W / 2}" y="94" text-anchor="middle" class="m" font-size="14" letter-spacing="3" fill="#7fb8a8">
<tspan fill="#5ff2c0">&lt;/&gt;</tspan>  THANKS FOR STOPPING BY  <tspan fill="#3b6b5f">·</tspan>  LET'S BUILD SOMETHING  <tspan fill="#5ff2c0">_</tspan></text>
</svg>'''
    write("footer.svg", svg)


terminal()
architecture()
for i, (n, l) in enumerate([
    ("h-about.svg", "about me"),
    ("h-architecture.svg", "how i build"),
    ("h-toolbox.svg", "toolbox"),
    ("h-telemetry.svg", "github telemetry"),
    ("h-connect.svg", "connect"),
], 1):
    header(n, l, i)
footer()
