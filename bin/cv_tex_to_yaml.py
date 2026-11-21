#!/usr/bin/env python3
"""Generate _data/cv.yml (the web CV on /cv/) from my-cv, my Awesome-CV LaTeX CV.

my-cv is the source of truth; _data/cv.yml is generated. Run bin/sync-cv rather than
this file: it also rebuilds the public PDF.

    cv_tex_to_yaml.py MY_CV_DIR > _data/cv.yml
    cv_tex_to_yaml.py --check-pdf PDF ROOT_TEX   # exit 1 if the phone number is in PDF

LaTeX -> RenderCV-style YAML read by al_folio_cv:
    header (\\name \\position \\address \\email)    -> cv.name / label / address / website / email
    \\mobile                                       -> never read: the site is public
    Summary (cvparagraph)                         -> cv.summary
    Experience, Education (\\cventry)               -> sections.Experience / Education
    Publications (\\cvhonor under \\cvsubsection)    -> sections.Publications, except the
                                                     "Submitted" subsection -> "Manuscripts Under Review"
    Patents (\\cvhonor)                             -> sections.Patents (bullets)
    Honors & Awards (\\cvhonor)                     -> sections."Honors and Awards"
    Skills (\\cvskill)                              -> sections.Skills (with icons)
    Research Interests and other \\cvskill lists    -> "label: details" lines
Sections follow the \\input order in root_cv.tex (al_folio_cv always shows Experience first).
"""

import json
import re
import subprocess
import sys
from pathlib import Path

KOREAN_NAME = "양건모"  # web-only: shown next to the name on /cv/
SKILL_ICONS = {
    "Programming": "fa-solid fa-code",
    "Firmware": "fa-solid fa-microchip",
    "Interfaces": "fa-solid fa-plug",
    "Hardware": "fa-solid fa-screwdriver-wrench",
    "DevOps": "fa-solid fa-server",
    "Languages": "fa-solid fa-language",
}
DEFAULT_SKILL_ICON = "fa-solid fa-circle-check"
ICONS = {
    "faTrophy": '<i class="fa-solid fa-trophy"></i>',
    "faStar": '<i class="fa-solid fa-star"></i>',
    "faYoutubePlay": '<i class="fa-brands fa-youtube"></i>',
}
MONTHS = {m: i for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split(), 1)}
MONTHS["sept"] = 9


# --------------------------------------------------------------------------- parsing
def strip_comments(text):
    return "\n".join(re.sub(r"(?<!\\)%.*", "", line) for line in text.splitlines())


def read_group(s, i):
    """s[i] is '{'; return (content, index after the matching '}')."""
    depth, j = 0, i
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1 : j], j + 1
        j += 1
    raise ValueError("unbalanced braces near: " + s[i : i + 80])


def macro_args(s, i, n):
    args = []
    for _ in range(n):
        while i < len(s) and s[i].isspace():
            i += 1
        if i >= len(s) or s[i] != "{":
            raise ValueError("expected {argument} near: " + s[i : i + 80])
        arg, i = read_group(s, i)
        args.append(arg)
    return args, i


def calls(s, name, n):
    """[(position, [arg1..argn]), ...] for every \\name{...}...{...} in s."""
    found = []
    for m in re.finditer(r"\\" + name + r"(?![A-Za-z])", s):
        args, _ = macro_args(s, m.end(), n)
        found.append((m.start(), args))
    return found


def sub_macro(s, name, n, fn):
    """Replace every \\name{...}x n in s with fn(args)."""
    out, i = [], 0
    pat = re.compile(r"\\" + name + r"(?![A-Za-z])")
    while True:
        m = pat.search(s, i)
        if not m:
            out.append(s[i:])
            return "".join(out)
        args, end = macro_args(s, m.end(), n)
        out += [s[i : m.start()], fn(args)]
        i = end


def inline(s):
    """LaTeX fragment -> Markdown/HTML text (al_folio_cv markdownifies most fields)."""
    s = sub_macro(s, "href", 2, lambda a: f"[{inline(a[1])}]({a[0].strip()})")
    s = sub_macro(s, "underline", 1, lambda a: f"**{inline(a[0])}**")  # \underline marks me
    s = sub_macro(s, "textbf", 1, lambda a: f"**{inline(a[0])}**")
    s = sub_macro(s, "textit", 1, lambda a: f"_{inline(a[0])}_")
    s = sub_macro(s, "emph", 1, lambda a: f"_{inline(a[0])}_")
    s = sub_macro(s, "venue", 1, lambda a: inline(a[0]))
    s = sub_macro(s, "pubtag", 1, lambda a: "")  # read separately by pubtags()
    s = sub_macro(s, "color", 1, lambda a: "")
    s = re.sub(r"\$\^\{?\s*(?:\*|∗)\s*\}?\$|\$\s*∗\s*\$", "<sup>*</sup>", s)
    s = re.sub(r"\$\^\{?\s*\\dagger\s*\}?\$|\$\s*†\s*\$|\\dagger(?![A-Za-z])", "<sup>†</sup>", s)
    for macro, html in ICONS.items():
        s = re.sub(r"\\" + macro + r"(?![A-Za-z])", lambda _m, h=html: h, s)
    for pat, rep in [
        (r"\\newline|\\\\", " "),
        (r"\\&", "&"),
        (r"\\%", "%"),
        (r"\\_", "_"),
        (r"\\#", "#"),
        (r"\\cdotp|\\cdot", "·"),
        (r"\\textbar", "|"),
        (r"\\(?:enskip|quad|qquad|,|;)", " "),
        (r"~", " "),
        (r"---", "—"),
        (r"--", "–"),
    ]:
        s = re.sub(pat, rep, s)
    s = re.sub(r"\\[A-Za-z]+\*?", "", s)  # any other macro (\upshape, \faHome, ...)
    s = s.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", s).strip()


def unquote(s):
    return s.strip().strip("“”\"").strip()


def pubtags(s):
    return [inline(a[0]) for _, a in calls(s, "pubtag", 1)]


def items_of(desc):
    """The \\item texts of a cvitems block."""
    desc = re.sub(r"\\(?:begin|end)\{cvitems\}", "", desc)
    items = []
    for chunk in re.split(r"\\item(?![A-Za-z])", desc)[1:]:
        chunk = chunk.strip()
        text = read_group(chunk, 0)[0] if chunk.startswith("{") else chunk
        items.append(inline(text))
    return [i for i in items if i]


def iso(date):
    """'Mar. 2022' -> '2022-03', '2026' -> '2026', 'Present' -> 'Present', else None."""
    date = date.strip()
    m = re.fullmatch(r"([A-Za-z]{3,4})\.?\s+(\d{4})", date)
    if m and m.group(1).lower() in MONTHS:
        return f"{m.group(2)}-{MONTHS[m.group(1).lower()]:02d}"
    if re.fullmatch(r"\d{4}", date):
        return date
    if date.lower().startswith("present"):
        return "Present"
    return None


def date_range(text):
    """'Mar. 2022 – Aug. 2027 (Expected)' -> ('2022-03', '2027-08')."""
    parts = re.split(r"\s*(?:–|—|--)\s*", re.sub(r"\(.*?\)", "", text).strip(), maxsplit=1)
    start = iso(parts[0])
    end = iso(parts[1]) if len(parts) > 1 else None
    return start, end


def keywords_item(item):
    return re.sub(r"^Keywords:\s*", "**Keywords:** ", item)


# Line breaks: short fields wrap only between whole phrases, never inside one.
# .nobr (white-space: nowrap) is defined in _sass/_custom.scss.
def nobr(text):
    return f'<span class="nobr">{text}</span>'


def keep_parens(s):
    """Keep each short "(...)" group on one line: no "(Undergraduate Research / Intern)"."""
    return re.sub(r"\([^()]{1,40}\)", lambda m: nobr(m.group(0)), s)


def keep_place(s):
    """'Bucheon, Incheon, South Korea' can break only after a comma."""
    parts = [p.strip() for p in s.split(",")]
    return " ".join(nobr(p + ("," if i < len(parts) - 1 else "")) for i, p in enumerate(parts))


def keep_names(s):
    """'A Kim, B Lee' -> each name stays on one line."""
    return ", ".join(nobr(name) for name in s.split(", "))


def keep_segments(parts):
    """'A · B · C' that can break only after a dot (&nbsp; keeps the dot off a new line)."""
    return "&nbsp;· ".join(nobr(p) for p in parts if p)


# Applied to every displayed string just before the YAML is written (glue_all). URLs, ISO
# dates and icon names are left alone, and so is anything already inside a .nobr span, an
# HTML tag or a markdown link target.
MON = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.?"
DATE = rf"(?:{MON}\s+)?\d{{4}}"
DATE_RANGE = re.compile(rf"(?<![A-Za-z0-9.])(?:{DATE}|{MON})\s*[–—]\s*(?:{DATE}|Present)(?![A-Za-z0-9])")
MONTH_YEAR = re.compile(rf"(?<![A-Za-z])({MON})\s+(\d{{4}})(?![0-9])")
HYPHENATED = re.compile(r"(?<![A-Za-z0-9./+&#;-])[A-Za-z0-9][A-Za-z0-9./+]*(?:-[A-Za-z0-9./+]*[A-Za-z0-9])+")
NO_GLUE_KEYS = {"email", "website", "url", "start_date", "end_date", "releaseDate", "date", "icon"}


def _outside(s, fn):
    """Apply fn to the plain-text parts of s: not tags, not markdown link targets, not .nobr."""
    parts = re.split(r"(<[^>]+>|\]\([^)]*\))", s)
    out, stack = [], []
    for part in parts:
        if part.startswith("<"):
            if re.match(r"<span\b", part):
                stack.append('class="nobr"' in part)
            elif part.startswith("</span") and stack:
                stack.pop()
            out.append(part)
        elif part.startswith("]("):
            out.append(part)
        else:
            out.append(part if any(stack) else fn(part))
    return "".join(out)


def _glue_last_two(s):
    """Replace the last breakable space with &nbsp;, so no line ends up holding one word."""
    parts = re.split(r"(<[^>]+>|\]\([^)]*\))", s)
    depth = []
    spans = []  # (index, inside_nobr) for plain-text parts
    for i, part in enumerate(parts):
        if part.startswith("<"):
            if re.match(r"<span\b", part):
                depth.append('class="nobr"' in part)
            elif part.startswith("</span") and depth:
                depth.pop()
        elif not part.startswith("]("):
            spans.append((i, any(depth)))
    for i, inside in reversed(spans):
        if inside:
            continue
        # the space may also sit just before a tag ("· <i …></i>&nbsp;Spotlight")
        j = parts[i].rfind(" ") if i < len(parts) - 1 else parts[i].rstrip().rfind(" ")
        if j >= 0:
            parts[i] = parts[i][:j] + "&nbsp;" + parts[i][j + 1 :]
            break
    return "".join(parts)


def glue(s, last_two=True):
    """Line-break rules for one displayed string (see the comment above MON)."""
    if not isinstance(s, str) or s.startswith(("http://", "https://")):
        return s
    s = _outside(s, lambda t: DATE_RANGE.sub(lambda m: nobr(m.group(0)), t))
    s = _outside(s, lambda t: MONTH_YEAR.sub(r"\1&nbsp;\2", t))
    s = _outside(s, lambda t: HYPHENATED.sub(lambda m: nobr(m.group(0)), t))
    s = _outside(s, lambda t: t.replace(" · ", "&nbsp;· "))
    # "· ★ Spotlight": Chrome breaks around an inline-block icon even next to &nbsp;, so wrap it whole
    s = re.sub(r"&nbsp;·(?:&nbsp;| )(<i [^>]*></i>)(?:&nbsp;| )([A-Za-z]+)", r'&nbsp;<span class="nobr">· \1 \2</span>', s)
    if last_two and len(re.sub(r"<[^>]+>", "", s).split()) >= 4:
        s = _glue_last_two(s)
    return s


def glue_all(obj, key=None):
    if isinstance(obj, dict):
        return {k: (v if k in NO_GLUE_KEYS else glue_all(v, k)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [glue_all(v, key) for v in obj]
    # the location sits in a 75px column: it must keep breaking after each comma
    return glue(obj, last_two=key != "location")


# --------------------------------------------------------------------------- sections
def experience(body):
    entries = []
    for _, (title, org, loc, date, desc) in calls(body, "cventry", 5):
        start, end = date_range(inline(date))
        entries.append(
            {
                "company": keep_parens(inline(org)),
                "position": keep_parens(inline(title)),
                "location": keep_place(inline(loc)),
                "start_date": start,
                "end_date": end or "Present",  # explicit: an empty end date renders as "2022 -"
                "summary": inline(date),  # the date column shows years only
                "highlights": [keywords_item(i) for i in items_of(desc)],
            }
        )
    return entries


def education(body):
    entries = []
    for _, (degree, inst, loc, date, desc) in calls(body, "cventry", 5):
        degree = inline(degree)
        m = re.fullmatch(r"(.+?)\s+in\s+(.+)", degree)
        start, end = date_range(inline(date))
        entries.append(
            {
                "institution": keep_parens(inline(inst)),
                "studyType": m.group(1) if m else degree,
                "area": m.group(2) if m else None,
                "location": keep_place(inline(loc)),
                "start_date": start,
                "end_date": end,
                "highlights": [inline(date)] + items_of(desc),  # months and "(Expected)"
            }
        )
    return entries


def publications(body):
    """-> (published entries, submitted bullets)."""
    subsections = [(pos, inline(a[0])) for pos, a in calls(body, "cvsubsection", 1)]
    published, submitted = [], []
    for pos, (title, authors, venue, date) in calls(body, "cvhonor", 4):
        kind = next((name for spos, name in reversed(subsections) if spos < pos), "")
        tags = pubtags(title)
        title = sub_macro(title, "pubtag", 1, lambda a: "")
        links = calls(title, "href", 2)
        url = links[0][1][0].strip() if links else None
        name = unquote(inline(links[0][1][1]) if links else inline(title))
        authors, venue, date = inline(authors), inline(venue), inline(date)
        if kind.lower() == "submitted":
            submitted.append({"bullet": f"**{name}** — {keep_names(authors)} · _{venue}_ · submitted {date}"})
            continue
        published.append(
            {
                "title": name,
                "publisher": keep_segments([kind, keep_parens(venue), date]),
                "releaseDate": iso(date),
                "url": url,
                "summary": " · ".join([keep_names(authors)] + tags),
            }
        )
    return published, submitted


def patents(body):
    return [
        {"bullet": f"**{unquote(inline(t))}** — {keep_names(inline(who))} · {inline(no)} · {inline(date)}"}
        for _, (t, who, no, date) in calls(body, "cvhonor", 4)
    ]


def honors(body):
    return [
        {
            "title": keep_parens(", ".join(x for x in (inline(award), inline(event)) if x)),
            "awarder": keep_parens(inline(where)),
            "date": iso(inline(date)),
        }
        for _, (award, event, where, date) in calls(body, "cvhonor", 4)
    ]


def skills(body):
    return [
        {
            "name": inline(cat),
            "icon": SKILL_ICONS.get(inline(cat), DEFAULT_SKILL_ICON),
            "keywords": inline(kw),
        }
        for _, (cat, kw) in calls(body, "cvskill", 2)
    ]


def labelled(body):
    return [{"label": inline(cat), "details": inline(kw)} for _, (cat, kw) in calls(body, "cvskill", 2)]


def generic(body):
    """Bullets for a section this script has no special mapping for."""
    out = [{"bullet": f"**{inline(t)}**, {inline(o)} ({inline(d)})"} for _, (t, o, _l, d, _x) in calls(body, "cventry", 5)]
    out += [{"bullet": " · ".join(x for x in map(inline, a) if x)} for _, a in calls(body, "cvhonor", 4)]
    out += labelled(body)
    for m in re.finditer(r"\\begin\{cvparagraph\}(.*?)\\end\{cvparagraph\}", body, re.S):
        out.append({"bullet": inline(m.group(1))})
    return out


# --------------------------------------------------------------------------- build
def build(mycv):
    root = strip_comments((mycv / "root_cv.tex").read_text(encoding="utf-8"))
    (first, last), = [a for _, a in calls(root, "name", 2)]
    address = calls(root, "address", 1)[0][1][0]
    links = calls(address, "href", 2)
    cv = {
        "name": f"{inline(first)} {inline(last).title()}" + (f" ({KOREAN_NAME})" if KOREAN_NAME else ""),
        "label": inline(calls(root, "position", 1)[0][1][0]),
        "email": inline(calls(root, "email", 1)[0][1][0]),
        "website": links[0][1][0].strip() if links else None,
    }
    place = inline(re.split(r"\\textbar", address)[0])
    if place:
        city, _, region = place.partition(",")
        cv["address"] = {"city": city.strip(), "region": region.strip() or None}

    sections = {}
    for rel in re.findall(r"\\input\{([^}]+)\}", root):
        path = mycv / (rel if rel.endswith(".tex") else rel + ".tex")
        body = strip_comments(path.read_text(encoding="utf-8"))
        heads = calls(body, "cvsection", 1)
        if not heads:
            continue
        title = inline(heads[0][1][0])
        key = title.lower()
        if key == "summary":
            m = re.search(r"\\begin\{cvparagraph\}(.*?)\\end\{cvparagraph\}", body, re.S)
            cv["summary"] = inline(m.group(1)) if m else None
        elif key == "experience":
            sections["Experience"] = experience(body)
        elif key == "education":
            sections["Education"] = education(body)
        elif key == "publications":
            published, submitted = publications(body)
            sections["Publications"] = published
            if submitted:
                sections["Manuscripts Under Review"] = submitted
        elif key == "patents":
            sections["Patents"] = patents(body)
        elif key in ("honors & awards", "honors and awards", "awards"):
            sections["Honors and Awards"] = honors(body)
        elif key == "skills":
            sections["Skills"] = skills(body)
        elif calls(body, "cvskill", 2) and not calls(body, "cventry", 5):
            sections[title] = labelled(body)  # e.g. Research Interests
        else:
            sections[title] = generic(body)
    cv["sections"] = sections
    return {"cv": cv}


# --------------------------------------------------------------------------- YAML out
def scalar(v):
    # Same quoting as Prettier, so `npm run lint:prettier` stays clean: single quotes when
    # the text has double quotes (HTML attributes), else a JSON string, which is also a
    # valid YAML double-quoted string.
    if isinstance(v, str) and '"' in v and "'" not in v and "\\" not in v and v.isprintable():
        return f"'{v}'"
    return json.dumps(v, ensure_ascii=False)


def emit(obj, level=0):
    pad, lines = "  " * level, []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if v in (None, "", [], {}):
                continue
            key = k if re.fullmatch(r"[A-Za-z][A-Za-z0-9 _-]*", k) else scalar(k)
            if isinstance(v, (dict, list)):
                lines.append(f"{pad}{key}:")
                lines += emit(v, level + 1)
            else:
                lines.append(f"{pad}{key}: {scalar(v)}")
    else:
        for item in obj:
            if isinstance(item, dict):
                sub = emit(item, level + 1)
                lines.append(f"{pad}- {sub[0].strip()}")
                lines += sub[1:]
            else:
                lines.append(f"{pad}- {scalar(item)}")
    return lines


HEADER = """\
# GENERATED by bin/sync-cv from my-cv (the Awesome-CV LaTeX CV) -- do not edit by hand.
# Edit ../my-cv/cv/*.tex, then run bin/sync-cv. The phone number is never copied.
"""


def check_pdf(pdf, root_tex):
    root = strip_comments(Path(root_tex).read_text(encoding="utf-8"))
    m = re.search(r"\\mobile\{([^}]*)\}", root)
    digits = re.sub(r"\D", "", m.group(1)) if m else ""
    text = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout
    if "Geonmo" not in text:
        sys.exit(f"check-pdf: {pdf} does not look like my CV")
    if digits and re.search(r"\D{0,3}".join(digits), text):
        sys.exit(f"check-pdf: the phone number is in {pdf}; not publishing it")
    print("check-pdf: OK (no phone number)")


def main(argv):
    if len(argv) == 4 and argv[1] == "--check-pdf":
        check_pdf(argv[2], argv[3])
        return
    if len(argv) != 2:
        sys.exit(__doc__)
    sys.stdout.write(HEADER + "\n".join(emit(glue_all(build(Path(argv[1]))))) + "\n")


if __name__ == "__main__":
    main(sys.argv)
