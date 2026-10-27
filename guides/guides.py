"""Builds the employer guides (lead magnets) as HTML, in Arabic and English:
labour_law_eg, benefits_eg and labour_law_sa. Content lives in eg_labour.py, eg_benefits.py
and sa_labour.py; the layout in kit.py.

  python3 guides/guides.py   -> guides/out/<tool>-<lang>.html, then `node guides/render.js` prints the PDFs.
Re-check every figure against the law text and the year's decisions before each edition.
"""
import os
import kit, eg_labour, eg_benefits, sa_labour, compare_eg, elite_case

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
GUIDES = {"labour_law_eg": eg_labour.GUIDE, "benefits_eg": eg_benefits.GUIDE, "labour_law_sa": sa_labour.GUIDE,
          "compare_pdf": compare_eg.GUIDE, "elite_case_pdf": elite_case.GUIDE}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for tool, g in GUIDES.items():
        for lang in ("ar", "en"):
            with open(os.path.join(OUT, "%s-%s.html" % (tool, lang)), "w", encoding="utf-8") as f:
                f.write(kit.render(g, lang))
    print("ok")
