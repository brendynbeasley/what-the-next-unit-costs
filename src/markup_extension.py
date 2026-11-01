"""Basu and Fernald's counter-test: count every input, not just labor.

Hall worked with value added because annual materials data did not exist for US industries. Basu
and Fernald (1997) showed that value-added regressions overstate the markup when materials move
with output, and that gross-output estimates are far smaller. This script reruns Hall's regression
on gross output, two ways:

  A. NBER-CES, 1959-2016: gross output with labor, materials-and-energy and capital, for total
     manufacturing, its 21 three-digit subsectors, and a set of named six-digit industries. Purchased
     services are not in the Census data, so these are still upper bounds.
  B. BEA GDP-by-industry KLEMS accounts, 1999-2025: 19 manufacturing industries with energy,
     materials AND purchased services, so the value-added and gross-output answers can be compared
     on one dataset with every input counted. Labor is full-time-equivalent employees times average
     weekly hours (BLS, via FRED).

Run src/hall_markup.py first: this script imports its helpers and reads results/industries_value_added.csv.

Usage (from the repository root):
    python src/markup_extension.py
"""

import sys
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import openpyxl
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))  # run with python -I as well
import hall_markup as h  # noqa: E402

BEA_FIRST, BEA_LAST = 1999, 2025       # FTE employees (NIPA 6.5D) start in 1998, so growth from 1999
COVID_YEARS = [2020, 2021]             # dropped in one robustness row

# Recognizable six-digit industries for the names table (2012 NAICS). Leading firms are named in the
# README from public knowledge; no firm data enters the estimates.
NAMED = ["311230", "311611", "311615", "312111", "312120", "312230", "322121", "324110", "325412",
         "327310", "331110", "334413", "336111", "336112", "336411", "326211", "327320", "321113"]

DURABLE = ["Wood products", "Nonmetallic mineral products", "Primary metals", "Fabricated metal products",
           "Machinery", "Computer and electronic products", "Electrical equipment, appliances, and components",
           "Motor vehicles, bodies and trailers, and parts", "Other transportation equipment",
           "Furniture and related products", "Miscellaneous manufacturing"]
NONDURABLE = ["Food and beverage and tobacco products", "Textile mills and textile product mills",
              "Apparel and leather and allied products", "Paper products", "Printing and related support activities",
              "Petroleum and coal products", "Chemical products", "Plastics and rubber products"]
BEA_INDUSTRIES = ["Manufacturing"] + DURABLE + NONDURABLE


# ----------------------------------------------------------------------------- Part A: NBER-CES

def nberces_part(d, names):
    tot = h.build_panel(d, "total")
    p3 = h.build_panel(d, 3)
    va = dict(y="solow_va", x=["dq"])
    go = dict(y="solow_go", x=["dyk"])
    rows = [
        h.summarize(h.iv(tot, z=["d_gdp"], **va), "dq", "NBER-CES total manufacturing, value added (Hall)"),
        h.summarize(h.iv(tot, z=["d_gdp"], **go), "dyk", "NBER-CES total manufacturing, gross output, materials counted"),
    ]
    # Hall's returns-to-scale check (1986 WP eq. 5.27): add capital growth, treated as predetermined
    r = h.iv(tot, "solow_go", ["dyk", "dk"], ["d_gdp", "dk"])
    delta, beta = r["coef"]["dk"], r["coef"]["dyk"]
    rows.append(h.summarize(r, "dyk", "NBER-CES total manufacturing, gross output, capital growth added",
                            {"capital_coef": delta, "capital_se": r["se"]["dk"],
                             "returns_to_scale_gamma": 1 + delta / (1 - beta)}))
    total = pd.DataFrame(rows)

    pooled = pd.concat([h.pooled(p3, "solow_va", "dq", "NBER-CES value added"),
                        h.pooled(p3, "solow_go", "dyk", "NBER-CES gross output")], ignore_index=True)

    ind = []
    for code, x in p3.groupby("group"):
        a = h.iv(x, "solow_va", ["dq"], ["d_gdp"])
        b = h.iv(x, "solow_go", ["dyk"], ["d_gdp"])
        ind.append({"naics3": code, "industry": names.get(code, code),
                    "beta_va": a["coef"]["dq"], "se_va": a["se"]["dq"], "beta_go": b["coef"]["dyk"],
                    "se_go": b["se"]["dyk"], "first_stage_F_go": b["first_f"], "first_stage_F_va": a["first_f"],
                    "materials_share": x.s_m.mean(), "labor_share_of_sales": x.s_l.mean()})
    ind = pd.DataFrame(ind)
    ind["mu_va"] = 1 / (1 - ind.beta_va)
    ind["mu_go"] = 1 / (1 - ind.beta_go)
    ind["mu_go_ci_low"] = 1 / (1 - (ind.beta_go - 1.96 * ind.se_go))
    ind["mu_go_ci_high"] = np.where(ind.beta_go + 1.96 * ind.se_go < 1, 1 / (1 - (ind.beta_go + 1.96 * ind.se_go)), np.inf)
    ind["weak_instrument"] = ind.first_stage_F_go < h.WEAK_F
    # Basu-Fernald identity: value-added markup implied by the gross-output markup and materials share
    ind["mu_va_implied_by_go"] = ind.mu_go * (1 - ind.materials_share) / (1 - ind.mu_go * ind.materials_share)
    ind = ind.sort_values("mu_go", ascending=False)

    six = h.build_panel(d[d.naics.isin(NAMED)], 6)
    named = []
    for code, x in six.groupby("group"):
        a = h.iv(x, "solow_va", ["dq"], ["d_gdp"])
        b = h.iv(x, "solow_go", ["dyk"], ["d_gdp"])
        o = h.iv(x, "solow_go", ["dyk"], ["dyk"])
        named.append({"naics6": code, "industry": names.get(code, code), "years": len(x),
                      "shipments_2016_bn": x.loc[x.year == h.LAST_YEAR, "vship"].sum() / 1000,
                      "beta_va": a["coef"]["dq"], "beta_go": b["coef"]["dyk"], "se_go": b["se"]["dyk"],
                      "first_stage_F": b["first_f"], "beta_go_ols": o["coef"]["dyk"], "se_go_ols": o["se"]["dyk"],
                      "materials_share": x.s_m.mean(),
                      "output_volatility": x.dy.std(), "corr_output_gdp": x.dy.corr(x.d_gdp)})
    named = pd.DataFrame(named)
    named["mu_va"] = 1 / (1 - named.beta_va)
    named["mu_go"] = 1 / (1 - named.beta_go)
    named["mu_go_ols"] = 1 / (1 - named.beta_go_ols)
    named["weak_instrument"] = named.first_stage_F < h.WEAK_F
    named["mu_go_ci_low"] = 1 / (1 - (named.beta_go - 1.96 * named.se_go))
    named["mu_go_ci_high"] = np.where(named.beta_go + 1.96 * named.se_go < 1,
                                      1 / (1 - (named.beta_go + 1.96 * named.se_go)), np.inf)
    return total, pooled, ind, named.sort_values("shipments_2016_bn", ascending=False)


# ----------------------------------------------------------------------------- Part B: BEA KLEMS

def _num(v):
    """BEA cells hold numbers, or strings such as '.....' or '(D)' for suppressed values."""
    return float(v) if isinstance(v, (int, float)) else np.nan


def _sheet(wb, name):
    """Read a BEA table into {clean industry name: {year: value}} (first occurrence of each name)."""
    rows = list(wb[name].iter_rows(values_only=True))
    hdr = next(i for i, r in enumerate(rows) if r[0] == "Line")
    years = {j: int(v) for j, v in enumerate(rows[hdr]) if isinstance(v, str) and v.isdigit()}
    out = {}
    for r in rows[hdr + 1:]:
        if not r[1]:
            continue
        nm = str(r[1]).split("\\")[0].strip()
        if nm not in out:
            out[nm] = {y: _num(r[j]) for j, y in years.items()}
    return out


def _composition(wb):
    """Composition of gross output (TKG105): nine lines per industry, in a fixed order."""
    rows = [r for r in wb["TKG105-A"].iter_rows(values_only=True)]
    hdr = next(i for i, r in enumerate(rows) if r[0] == "Line")
    years = {j: int(v) for j, v in enumerate(rows[hdr]) if isinstance(v, str) and v.isdigit()}
    body = [r for r in rows[hdr + 1:] if r[1]]
    parts = ["go", "va", "comp", "taxes", "gos", "ii", "energy", "materials", "services"]
    out = {}
    for i in range(len(body) - 8):
        if str(body[i + 1][1]).strip() == "Value added" and str(body[i + 8][1]).strip() == "Purchased-services inputs":
            nm = str(body[i][1]).split("\\")[0].strip()
            if nm not in out:
                out[nm] = {p: {y: _num(body[i + k][j]) for j, y in years.items()} for k, p in enumerate(parts)}
    return out


def load_bea():
    zf = zipfile.ZipFile(h.RAW / "bea_GdpByInd.zip")
    klems = openpyxl.load_workbook(zf.open("KLEMS.xlsx"), read_only=True)
    gout = openpyxl.load_workbook(zf.open("GrossOutput.xlsx"), read_only=True)
    vadd = openpyxl.load_workbook(zf.open("ValueAdded.xlsx"), read_only=True)
    fa = openpyxl.load_workbook(h.RAW / "bea_FixedAssets_Section3All.xlsx", read_only=True)
    nipa = openpyxl.load_workbook(h.RAW / "bea_NIPA_Section6All.xlsx", read_only=True)
    comp = _composition(klems)
    q = {"go": _sheet(gout, "TGO103-A"), "va": _sheet(vadd, "TVA103-A"), "e": _sheet(klems, "TKE103-A"),
         "m": _sheet(klems, "TKM103-A"), "s": _sheet(klems, "TKS103-A"), "k": _sheet(fa, "FAAt302ESI-A"),
         "fte": _sheet(nipa, "T60500D-A")}
    hours = {"dur": h.read_fred("CES3100000007"), "nondur": h.read_fred("CES3200000007"), "all": h.read_fred("AWHMAN")}
    rows = []
    for ind in BEA_INDUSTRIES:
        wk = hours["all"] if ind == "Manufacturing" else hours["dur"] if ind in DURABLE else hours["nondur"]
        for yr in range(BEA_FIRST - 1, BEA_LAST + 1):
            c = comp[ind]
            rows.append({"group": ind, "year": yr,
                         "go_nom": c["go"][yr], "va_nom": c["va"][yr], "comp": c["comp"][yr], "taxes": c["taxes"][yr],
                         "energy": c["energy"][yr], "materials": c["materials"][yr], "services": c["services"][yr],
                         "q_go": q["go"][ind][yr], "q_va": q["va"][ind][yr], "q_e": q["e"][ind][yr],
                         "q_m": q["m"][ind][yr], "q_s": q["s"][ind][yr],
                         "k_start": q["k"][ind].get(yr - 1),     # year-end stock of t-1 = start of t
                         "labor": q["fte"][ind][yr] * wk.get(yr)})
    b = pd.DataFrame(rows)
    print(f"BEA: {len(b)} industry-years for {b.group.nunique()} manufacturing lines, {BEA_FIRST - 1}-{BEA_LAST}; "
          f"missing values: {int(b.isna().sum().sum())}")
    return b


def bea_panel(b):
    b = b.sort_values(["group", "year"]).copy()
    g = b.groupby("group")
    for v in ["q_go", "q_va", "q_e", "q_m", "q_s", "k_start", "labor"]:
        b["d_" + v] = np.log(b[v]) - np.log(g[v].shift())
    net = b.go_nom - b.taxes                       # Hall measures prices net of indirect taxes
    for p in ["comp", "energy", "materials", "services"]:
        sh = b[p] / net
        b["s_" + p] = (sh + sh.groupby(b.group).shift()) / 2
    a = b.comp / (b.va_nom - b.taxes)
    b["alpha"] = (a + a.groupby(b.group).shift()) / 2
    b = b[b.year >= BEA_FIRST].copy()
    dk, dl = b.d_k_start, b.d_labor
    b["dq"] = b.d_q_va - dk
    b["solow_va"] = b.dq - b.alpha * (dl - dk)
    b["dyk"] = b.d_q_go - dk
    em = b.s_energy * (b.d_q_e - dk) + b.s_materials * (b.d_q_m - dk)
    b["solow_go_em"] = b.dyk - b.s_comp * (dl - dk) - em
    b["solow_go_all"] = b.solow_go_em - b.s_services * (b.d_q_s - dk)
    b["s_intermediate"] = b.s_energy + b.s_materials + b.s_services
    return b.join(h.instruments(), on="year")


def bea_part(b):
    tot = b[b.group == "Manufacturing"]
    p = b[b.group != "Manufacturing"]
    specs = [("solow_va", "dq", "value added (Hall)"), ("solow_go_em", "dyk", "gross output, energy and materials counted"),
             ("solow_go_all", "dyk", "gross output, all intermediate inputs counted")]
    rows = []
    for y, x, lab in specs:
        rows.append(h.summarize(h.iv(tot, y, [x], ["d_gdp"]), x, f"BEA total manufacturing, {lab}"))
        for excl, tag in [([], ""), (COVID_YEARS, ", 2020-21 dropped")]:
            dd = p[~p.year.isin(excl)]
            r = h.iv(dd, y, [x], ["d_gdp"], fe="group", cov="cluster", cluster="year")
            rows.append(h.summarize(r, x, f"BEA 19 industries pooled, {lab}{tag}, industry FE, SE clustered by year"))
        r = h.iv(p, y, [x], [x], fe="group", cov="cluster", cluster="year")
        rows.append(h.summarize(r, x, f"BEA 19 industries pooled, {lab}, OLS"))
    summary = pd.DataFrame(rows)

    ind = []
    for nm, x in p.groupby("group"):
        res = {k: h.iv(x, y, [xx], ["d_gdp"]) for y, xx, k in [("solow_va", "dq", "va"), ("solow_go_em", "dyk", "go_em"),
                                                                ("solow_go_all", "dyk", "go_all")]}
        row = {"industry": nm, "first_stage_F": res["go_all"]["first_f"], "intermediate_share": x.s_intermediate.mean(),
               "services_share": x.s_services.mean(), "labor_share_va": x.alpha.mean()}
        for k, r in res.items():
            xx = "dq" if k == "va" else "dyk"
            row["beta_" + k] = r["coef"][xx]
            row["se_" + k] = r["se"][xx]
            row["mu_" + k] = 1 / (1 - r["coef"][xx])
            hi = r["coef"][xx] + 1.96 * r["se"][xx]
            row["mu_ci_low_" + k] = 1 / (1 - (r["coef"][xx] - 1.96 * r["se"][xx]))
            row["mu_ci_high_" + k] = 1 / (1 - hi) if hi < 1 else np.inf
        ind.append(row)
    ind = pd.DataFrame(ind).sort_values("mu_go_all", ascending=False)
    ind["weak_instrument"] = ind.first_stage_F < h.WEAK_F
    return summary, ind


def headline_counts(ind, bind):
    """How many industries reject price = marginal cost, among those where the instrument is strong."""
    va = pd.read_csv(h.OUT / "industries_value_added.csv")
    strong_va = va[~va.weak_instrument]
    strong_go = ind[~ind.weak_instrument]
    strong_bea = bind[~bind.weak_instrument]
    return pd.DataFrame([
        {"measure": "NBER-CES value added: industries with first-stage F >= 10", "value": len(strong_va)},
        {"measure": "NBER-CES value added: of those, 95% CI excludes mu = 1", "value": int(strong_va.reject_mu_eq_1.sum())},
        {"measure": "NBER-CES value added: median mu among strong-instrument industries", "value": strong_va.markup_mu.median()},
        {"measure": "NBER-CES gross output: industries with first-stage F >= 10", "value": len(strong_go)},
        {"measure": "NBER-CES gross output: of those, 95% CI excludes mu = 1", "value": int((strong_go.mu_go_ci_low > 1).sum())},
        {"measure": "NBER-CES gross output: median mu among strong-instrument industries", "value": strong_go.mu_go.median()},
        {"measure": "Basu-Fernald identity: median value-added mu implied by gross-output mu (strong industries)",
         "value": strong_go.mu_va_implied_by_go.median()},
        {"measure": "Basu-Fernald identity: median directly estimated value-added mu (same industries)",
         "value": strong_go.mu_va.median()},
        {"measure": "BEA all inputs: industries with first-stage F >= 10", "value": len(strong_bea)},
        {"measure": "BEA all inputs: of those, 95% CI excludes mu = 1", "value": int((strong_bea.mu_ci_low_go_all > 1).sum())},
        {"measure": "BEA all inputs: median mu among strong-instrument industries", "value": strong_bea.mu_go_all.median()},
        {"measure": "BEA value added: median mu among the same industries", "value": strong_bea.mu_va.median()},
    ])


# ----------------------------------------------------------------------------- figures

def ladder_figure(rows, path):
    """Markup estimates as more inputs are counted, with 95% intervals."""
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    ys = np.arange(len(rows))[::-1]
    for yv, (_, r) in zip(ys, rows.iterrows()):
        hi = min(r.mu_ci_high, 4)
        ax.plot([r.mu_ci_low, hi], [yv, yv], color="#4a6fa5", lw=2)
        ax.scatter([r.markup_mu], [yv], color="#1d3557", zorder=3, s=36)
        ax.annotate(f"{r.markup_mu:.2f}", (r.markup_mu, yv), xytext=(0, 7), textcoords="offset points",
                    ha="center", fontsize=8)
    ax.axvline(1, color="#c8553d", lw=1, ls="--")
    ax.text(1.03, ys[0] + 0.3, "price = marginal cost", color="#c8553d", fontsize=8)
    ax.set_yticks(ys)
    ax.set_yticklabels(rows.label, fontsize=8)
    ax.set_xlim(0.8, 4)
    ax.set_ylim(ys[-1] - 0.6, ys[0] + 0.7)
    ax.set_xlabel("Price / marginal cost, pooled industries (instrument: real GDP growth)")
    ax.set_title("The markup shrinks as more of the inputs are counted")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def dumbbell_figure(ind, path):
    d = ind[~ind.weak_instrument].sort_values("mu_go")
    fig, ax = plt.subplots(figsize=(7.5, 6))
    y = np.arange(len(d))
    va = d.mu_va.clip(upper=6)
    ax.hlines(y, d.mu_go, va, color="#bbbbbb")
    ax.scatter(va, y, color="#c8553d", s=24, label="Value added (Hall's method)", zorder=3)
    ax.scatter(d.mu_go, y, color="#1d3557", s=24, label="Gross output (materials counted)", zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels([s.replace(" Manufacturing", "") for s in d.industry], fontsize=7)
    ax.axvline(1, color="grey", lw=0.6, ls="--")
    ax.set_xlabel("Price / marginal cost, 1959-2016 (value added capped at 6)")
    ax.set_title("Three-digit manufacturing industries, NBER-CES")
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main():
    h.OUT.mkdir(exist_ok=True)
    names = h.industry_names()
    d = h.load_nberces()
    total, pooled, ind, named = nberces_part(d, names)
    b = bea_panel(load_bea())
    print(f"BEA panel: {len(b)} industry-years, {BEA_FIRST}-{BEA_LAST}; rows with a missing growth rate: "
          f"{int(b[['solow_va', 'solow_go_all']].isna().any(axis=1).sum())}")
    bsum, bind = bea_part(b)

    total.to_csv(h.OUT / "extension_total_mfg.csv", index=False)
    pooled.to_csv(h.OUT / "extension_pooled_nberces.csv", index=False)
    ind.to_csv(h.OUT / "industries_gross_output.csv", index=False)
    named.to_csv(h.OUT / "named_industries.csv", index=False)
    bsum.to_csv(h.OUT / "bea_klems_estimates.csv", index=False)
    bind.to_csv(h.OUT / "bea_klems_industries.csv", index=False)
    b[["group", "year", "dq", "dyk", "alpha", "s_comp", "s_energy", "s_materials", "s_services",
       "solow_va", "solow_go_em", "solow_go_all", "d_gdp"]].to_csv(h.OUT / "bea_klems_series.csv", index=False)

    for df in [total, pooled, bsum]:
        print(df[["specification", "beta", "se", "markup_mu", "mu_ci_low", "mu_ci_high", "first_stage_F", "n"]]
              .round(3).to_string(index=False))
    print(ind[["naics3", "industry", "mu_va", "mu_go", "first_stage_F_go"]].round(2).to_string(index=False))
    print(named[["naics6", "industry", "mu_va", "mu_go", "se_go", "first_stage_F", "mu_go_ols"]].round(2).to_string(index=False))
    print(bind[["industry", "mu_va", "mu_go_em", "mu_go_all", "first_stage_F"]].round(2).to_string(index=False))

    # Labor's share of value added: Census value added (NBER-CES) vs NIPA value added (BEA), manufacturing
    census = h.build_panel(d, "total")
    bm = b[b.group == "Manufacturing"]
    shares = pd.DataFrame([
        {"measure": "NBER-CES (Census) labor share of value added, 1999-2016 mean", "value": census[census.year >= 1999].alpha.mean()},
        {"measure": "BEA (NIPA) labor share of value added net of taxes, 1999-2016 mean", "value": bm[bm.year <= 2016].alpha.mean()},
        {"measure": "BEA (NIPA) labor share of value added net of taxes, 1999-2025 mean", "value": bm.alpha.mean()},
        {"measure": "BEA purchased-services share of manufacturing gross output, 1999-2025 mean", "value": bm.s_services.mean()},
        {"measure": "BEA energy and materials share of manufacturing gross output, 1999-2025 mean",
         "value": (bm.s_energy + bm.s_materials).mean()},
    ])
    shares.to_csv(h.OUT / "labor_share_comparison.csv", index=False)
    print(shares.round(3).to_string(index=False))

    counts = headline_counts(ind, bind)
    counts.to_csv(h.OUT / "headline_counts.csv", index=False)
    print(counts.round(3).to_string(index=False))

    pick = lambda df, s: df[df.specification == s].iloc[0]
    lad = pd.DataFrame([
        pick(pooled, "NBER-CES value added, IV real GDP growth, 1959-2016, industry FE, SE clustered by year"),
        pick(pooled, "NBER-CES gross output, IV real GDP growth, 1959-2016, industry FE, SE clustered by year"),
        pick(bsum, "BEA 19 industries pooled, value added (Hall), industry FE, SE clustered by year"),
        pick(bsum, "BEA 19 industries pooled, gross output, energy and materials counted, industry FE, SE clustered by year"),
        pick(bsum, "BEA 19 industries pooled, gross output, all intermediate inputs counted, industry FE, SE clustered by year"),
    ])
    lad["label"] = ["NBER-CES 1959-2016: value added", "NBER-CES 1959-2016: gross output, materials",
                    "BEA 1999-2025: value added", "BEA 1999-2025: gross output, materials",
                    "BEA 1999-2025: gross output, all inputs"]
    lad.to_csv(h.OUT / "markup_ladder.csv", index=False)
    ladder_figure(lad, h.OUT / "markup_ladder.png")
    dumbbell_figure(ind, h.OUT / "industries_va_vs_go.png")
    print("Wrote results/extension_total_mfg.csv, extension_pooled_nberces.csv, industries_gross_output.csv, "
          "named_industries.csv, bea_klems_estimates.csv, bea_klems_industries.csv, bea_klems_series.csv, headline_counts.csv, labor_share_comparison.csv, "
          "markup_ladder.csv, markup_ladder.png, industries_va_vs_go.png")


if __name__ == "__main__":
    main()
