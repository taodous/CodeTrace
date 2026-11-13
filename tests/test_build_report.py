import datetime as dt
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("build_report", ROOT / "scripts" / "build_report.py")
br = importlib.util.module_from_spec(spec)
sys.modules["build_report"] = br
spec.loader.exec_module(br)

META = {
    "titre": "CodeTrace",
    "sous_titre": "Provenance",
    "type_document": "Rapport de recherche",
    "annee": "2026-2027",
    "equipe": "Équipe Data \\& IA",
    "ville": "Paris",
    "auteurs": ["A. Auteur", "B. Auteur"],
    "encadrants": ["E. Encadrant"],
}


def test_list_versions_ignores_other_dirs(tmp_path):
    for name in ["V1", "V10", "V2", "template", "Vx", "v3"]:
        (tmp_path / name).mkdir()
    (tmp_path / "V4").write_text("pas un dossier")
    assert br.list_versions(tmp_path) == [1, 2, 10]


def test_list_versions_missing_dir(tmp_path):
    assert br.list_versions(tmp_path / "absent") == []


def test_adapt_real_template_removes_tp_content(tmp_path):
    (tmp_path / "sections" / "annexes").mkdir(parents=True)
    for s in ["00-resume", "01-introduction", "02-etat-de-l-art"]:
        (tmp_path / "sections" / f"{s}.tex").write_text("")
    (tmp_path / "sections" / "annexes" / "A-decisions.tex").write_text("")
    template = br.TEMPLATE.read_text(encoding="utf-8")
    main = br.render_main(template, 3, META, tmp_path)
    # le style ECE est conservé
    assert r"\definecolor{ece}" in main and r"\usepackage{helvet}" in main
    assert r"\input{preamble-recherche}" in main
    assert "V3" in main
    # le contenu TP a disparu
    for tp in ["RAPPORT DE TP", "colorbox{yellow}", "elec.png", "binôme", "T1."]:
        assert tp not in main
    # ordre : résumé avant la table des matières, sections, bibliographie, annexes
    order = [
        r"\input{sections/00-resume}",
        r"\tableofcontents",
        r"\input{sections/01-introduction}",
        r"\input{sections/02-etat-de-l-art}",
        r"\printbibliography",
        r"\appendix",
        r"\input{sections/annexes/A-decisions}",
    ]
    positions = [main.index(x) for x in order]
    assert positions == sorted(positions)
    assert main.count(r"\begin{document}") == 1


def test_adapt_preamble_requires_header():
    with pytest.raises(ValueError):
        br.adapt_preamble(r"\documentclass{article}", 1, META)


def test_render_titlepage_fills_all_placeholders():
    asset = (br.ASSETS / "titlepage.tex").read_text(encoding="utf-8")
    out = br.render_titlepage(asset, 2, META, dt.date(2026, 11, 1))
    assert "{{" not in out
    assert r"\MakeUppercase{Rapport de recherche}" in out
    assert "1er novembre 2026" in out
    assert r"A. Auteur \\ B. Auteur" in out


def test_is_trivial(tmp_path):
    (tmp_path / "vide.py").write_text("\n")
    (tmp_path / "plein.py").write_text("x = 1\n")
    assert br.is_trivial("results/.gitkeep", tmp_path)
    assert br.is_trivial("vide.py", tmp_path)
    assert not br.is_trivial("plein.py", tmp_path)
    assert not br.is_trivial("supprime.py", tmp_path)  # fichier supprimé : on le garde


def test_strip_comments_keeps_escaped_percent():
    assert br.strip_comments(r"10\,\% de FPR % commentaire") == r"10\,\% de FPR "


def test_journal_entries_since():
    text = "# Journal\n## 2026-11-12\n- a\n## 2026-11-20\n- b\n"
    assert br.journal_entries_since(text, None) == ["2026-11-12", "2026-11-20"]
    assert br.journal_entries_since(text, dt.date(2026, 11, 13)) == ["2026-11-20"]


def test_section_targets_specific_prefix_first():
    assert br.section_targets("notes/etat_de_l_art.md") == ["02-etat-de-l-art"]
    assert br.section_targets("src/codetrace/perturb/rename.py")[0] == "05-methodes"
    assert br.section_targets("results/2026-12-01_mink/metrics.json")[0] == "07-resultats"
    assert br.section_targets("inconnu.txt") == ["selon le contenu"]


def test_static_checks_detects_problems():
    files = {
        "sections/02.tex": "Texte — avec tiret. \\cite{carlini2021,absent2099}\n"
        "\\label{fig:a} \\label{tab:b} \\cref{tab:b} \\afaire{x}",
        "sections/07-resultats.tex": "AUC de 0,62 et \\res{run}{auc} % 0.99 en commentaire",
        "titlepage.tex": "\\colorbox{yellow}{X} À compléter",
    }
    rep = br.static_checks(files, "@misc{carlini2021,\n title={x}}\n")
    text = "\n".join(rep.errors)
    assert "tiret cadratin" in text
    assert "absent2099" in text and "carlini2021" not in text
    assert "0,62" in text and "0.99" not in text
    assert "colorbox{yellow}" in text
    warnings = "\n".join(rep.warnings)
    assert "fig:a" in warnings and "tab:b" not in warnings
    assert "À compléter" in warnings
    assert "\\afaire : 1" in rep.infos[0]


def test_static_checks_allows_triple_hyphen_free_text():
    rep = br.static_checks({"a.tex": "pages 10--12, -- tiret demi-cadratin ok"}, "")
    assert rep.errors == []


def test_parse_latex_log():
    log = (
        "LaTeX Warning: Reference `sec:x' on page 3 undefined on input line 12.\n"
        "LaTeX Warning: Citation `foo2020' on page 4 undefined on input line 20.\n"
        "Overfull \\hbox (12.5pt too wide) in paragraph at lines 30--31\n"
        "Overfull \\hbox (1.2pt too wide) in paragraph at lines 40--41\n"
        "Package codetrace Warning: Resultat inconnu: run/auc on input line 9.\n"
    )
    rep = br.parse_latex_log(log)
    assert len(rep.errors) == 3
    assert len(rep.warnings) == 1 and "12.5pt" in rep.warnings[0]


def test_metrics_to_tex_flattens_and_formats():
    tex = br.metrics_to_tex(
        "2026-12-01_mink",
        {"llama": {"auc": 0.62, "auc_ci": [0.58, 0.66]}, "n": 1000, "note": "a_b"},
        "results/x",
    )
    assert r"\defres{2026-12-01-mink}{llama.auc}{\num{0.62}}" in tex
    assert r"\defres{2026-12-01-mink}{llama.auc-ci}{[\num{0.58}~; \num{0.66}]}" in tex
    assert r"\defres{2026-12-01-mink}{n}{\num{1000}}" in tex
    assert r"{a\_b}" in tex


def test_csv_to_tex():
    tex = br.csv_to_tex([["Modèle", "AUC"], ["LLaMA_3", "0.62"]], "results/x/tables/t.csv")
    assert r"\toprule" in tex and r"\bottomrule" in tex
    assert r"LLaMA\_3 & \num{0.62} \\" in tex


def test_export_results(tmp_path):
    results = tmp_path / "results"
    run = results / "2026-12-01_mink"
    (run / "tables").mkdir(parents=True)
    (run / "figures").mkdir()
    (run / "metrics.json").write_text(json.dumps({"auc": 0.6}))
    (run / "tables" / "auc.csv").write_text("m,auc\nx,0.6\n", encoding="utf-8")
    (run / "figures" / "roc.pdf").write_bytes(b"%PDF")
    vdir = tmp_path / "V1"
    vdir.mkdir()
    log = br.export_results(vdir, results)
    assert len(log) == 3
    assert (vdir / "generated" / "res-2026-12-01-mink.tex").exists()
    assert (vdir / "generated" / "2026-12-01-mink" / "auc.tex").exists()
    assert (vdir / "figures" / "2026-12-01-mink" / "roc.pdf").exists()
    index = (vdir / "generated" / "resultats.tex").read_text(encoding="utf-8")
    assert r"\input{generated/res-2026-12-01-mink}" in index
