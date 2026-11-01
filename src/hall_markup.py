"""Hall (1988) on modern data: is price above marginal cost in US manufacturing?

Robert Hall's test: under constant returns and price equal to marginal cost, the Solow residual
(output growth minus labor's share times labor growth, all per unit of capital) is technical
progress and should not move with demand. If price is a markup mu over marginal cost, the residual
picks up a fraction beta = 1 - 1/mu of output growth. Regressing the residual on output growth,
with a demand variable as the instrument, recovers beta and so mu.

This script:
  1. Re-estimates Hall's own total-manufacturing regression (1949-78) from the numbers printed in
     Table 1 of his 1986 NBER working paper, with real GNP growth (FRED) as the instrument.
  2. Builds value added, hours and capital for total manufacturing and its 21 three-digit NAICS
     subsectors from the NBER-CES Manufacturing Industry Database (1958-2018), and runs Hall's
     value-added regression on 1959-2016, by industry and pooled.
  3. Writes CSVs and one figure to results/.

Usage (from the repository root):
    python src/hall_markup.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"

FIRST_YEAR, LAST_YEAR = 1959, 2016  # growth years; NBER-CES capital stops in 2016 (technical notes, sec. 4)
SPLIT_YEAR = 1987                   # last year of the first half, close to Hall's own sample end (1984-86)
HAC_LAGS = 2                        # Newey-West lags for annual time series
WEAK_F = 10                         # first-stage F below this is flagged as a weak instrument (Staiger-Stock rule)

# Hall's 1986 working paper, Table 2, matched to the nearest 2012 NAICS subsector (judgment; SIC 37
# is absent from Hall's table, and NAICS 312 joins beverages, which Hall kept with food, to tobacco).
HALL_SIC_FOR_NAICS = {
    "311": 20, "312": 21, "313": 22, "314": 22, "315": 23, "316": 31, "321": 24, "322": 26,
    "323": 27, "324": 29, "325": 28, "326": 30, "327": 32, "331": 33, "332": 34, "333": 35,
    "334": 36, "335": 36, "337": 25, "339": 39,
}


# ----------------------------------------------------------------------------- data

def read_fred(series):
    d = pd.read_csv(RAW / f"fred_{series}.csv")
    d.columns = ["date", "value"]
    d["year"] = pd.to_datetime(d.date).dt.year
    d["value"] = pd.to_numeric(d.value, errors="coerce")
    return d.groupby("year").value.mean()


def instruments():
    """Annual demand instruments: real GDP/GNP growth (Hall 1986) and the Hall-Ramey set."""
    z = pd.DataFrame({
        "gdp": read_fred("GDPCA"), "gnp": read_fred("GNPCA"),
        "defense": read_fred("B824RA3A086NBEA"), "deflator": read_fred("A191RD3A086NBEA"),
        "oil": read_fred("WTISPLC"),
    })
    out = pd.DataFrame(index=z.index)
    out["d_gdp"] = np.log(z.gdp).diff()
    out["d_gnp"] = np.log(z.gnp).diff()
    out["d_defense"] = np.log(z.defense).diff()
    out["d_oil"] = np.log(z.oil / z.deflator).diff()
    party = pd.read_csv(RAW / "presidents_party.csv")
    dem = {y: int(r.party == "D") for r in party.itertuples() for y in range(r.first_year, r.last_year + 1)}
    out["democrat"] = pd.Series(dem)
    return out


def fringe_factor():
    """Compensation / wages and salaries, all US employees (NIPA, via FRED). NBER-CES pay is payroll only."""
    return read_fred("A033RC1A027NBEA") / read_fred("A034RC1A027NBEA")


def industry_names():
    names = {}
    for line in (RAW / "naics_names_2012.txt").read_text(encoding="latin-1").splitlines()[1:]:
        parts = line.split("\t")
        if len(parts) >= 2 and parts[0].strip().isdigit():
            names[parts[0].strip()] = parts[1].strip().strip('"').strip()
    return names


def load_nberces():
    raw = pd.read_csv(RAW / "nberces5818v1_n2012.csv")
    print(f"NBER-CES: loaded {len(raw):,} industry-years, {raw.naics.nunique()} six-digit industries, "
          f"{raw.year.min()}-{raw.year.max()}")
    d = raw.copy()
    d["naics"] = d.naics.astype(str)
    d = d[(d.year >= FIRST_YEAR - 1) & (d.year <= LAST_YEAR)]
    need = ["vship", "matcost", "pay", "emp", "prode", "prodh", "cap", "piship", "pimat", "piinv"]
    ok = d[need].notna().all(axis=1) & (d[need] > 0).all(axis=1) & (d.vship > d.matcost)
    print(f"  kept {ok.sum():,} industry-years in {FIRST_YEAR - 1}-{LAST_YEAR} with positive output, "
          f"inputs and capital; dropped {(~ok).sum():,} (missing, zero, or materials above shipments)")
    d = d[ok].copy()
    d["comp"] = d.pay * d.year.map(fringe_factor())
    d["hours"] = d.prodh * d.emp / d.prode       # production hours scaled up to all employees
    d["y"] = np.log(d.vship / d.piship)          # real gross output
    d["m"] = np.log(d.matcost / d.pimat)         # real materials and energy
    d["k"] = np.log(d.cap)                       # real capital, start of year
    d["h"] = np.log(d.hours)
    d["kval"] = d.cap * d.piinv
    d["hpw"] = np.log(d.prodh / d.prode)         # hours per production worker (utilization proxy)
    return d


def build_panel(d, key):
    """Industry-year growth rates and shares for groups of six-digit industries.

    Real growth rates are Tornqvist aggregates of six-digit growth (weights: average nominal shares in
    t and t-1); hours are summed. Only industries observed in both t and t-1 enter a year's change.
    """
    d = d.sort_values(["naics", "year"]).copy()
    d["grp"] = d.naics.str[:key] if isinstance(key, int) else key
    g = d.groupby("naics")
    for v in ["y", "m", "k", "h", "hpw"]:
        d["d" + v] = d[v] - g[v].shift()
    for v in ["vship", "matcost", "kval", "comp", "hours", "pay"]:
        d[v + "_l"] = g[v].shift()
    d = d[d.year >= FIRST_YEAR].dropna(subset=["dy", "dm", "dk", "dh", "vship_l"])

    rows = []
    for (grp, yr), x in d.groupby(["grp", "year"]):
        w = lambda v: (x[v] / x[v].sum() + x[v + "_l"] / x[v + "_l"].sum()) / 2
        s = lambda a, b: (x[a].sum() / x[b].sum() + x[a + "_l"].sum() / x[b + "_l"].sum()) / 2
        va, va_l = (x.vship - x.matcost).sum(), (x.vship_l - x.matcost_l).sum()
        rows.append({
            "group": grp, "year": yr, "n_industries": len(x),
            "dy": (w("vship") * x.dy).sum(), "dm": (w("matcost") * x.dm).sum(),
            "dk": (w("kval") * x.dk).sum(), "dh": np.log(x.hours.sum() / x.hours_l.sum()),
            "dhpw": (w("hours") * x.dhpw).sum(),
            "s_m": s("matcost", "vship"), "s_l": s("comp", "vship"),
            "alpha": (x.comp.sum() / va + x.comp_l.sum() / va_l) / 2,
            "vship": x.vship.sum(), "va": va,
        })
    p = pd.DataFrame(rows)
    # Hall's value-added version (1986 WP eqs. 1.6, 2.2): Divisia real value added per unit of capital
    p["dv"] = (p.dy - p.s_m * p.dm) / (1 - p.s_m)
    p["dq"] = p.dv - p.dk
    p["dn"] = p.dh - p.dk
    p["solow_va"] = p.dq - p.alpha * p.dn
    # Gross-output version with materials (1986 WP eq. 2.1)
    p["dyk"] = p.dy - p.dk
    p["solow_go"] = p.dyk - p.s_l * (p.dh - p.dk) - p.s_m * (p.dm - p.dk)
    return p.join(instruments(), on="year")


# ----------------------------------------------------------------------------- estimation

def iv(data, y, x, z, exog=(), fe=None, cov="hac", cluster=None):
    """Two-stage least squares with HAC (Newey-West) or clustered standard errors.

    x: endogenous regressors; z: excluded instruments; exog: included exogenous regressors.
    fe: column for fixed effects (absorbed as dummies). With z == x this is OLS.
    Returns dict with coefficients, standard errors, first-stage F (robust Wald / q) and N.
    """
    cols = [y] + list(x) + list(z) + list(exog) + ([fe] if fe else []) + ([cluster] if cluster else [])
    d = data.dropna(subset=list(dict.fromkeys(cols))).sort_values(["year"] + ([fe] if fe else []))
    n = len(d)
    W = [np.ones(n)] if fe is None else []
    W += [d[c].values for c in exog]
    if fe is not None:
        W += [(d[fe] == v).values.astype(float) for v in sorted(d[fe].unique())]
    W = np.column_stack(W)
    X = np.column_stack([d[c].values for c in x] + [W])
    Z = np.column_stack([d[c].values for c in z] + [W])
    Y = d[y].values
    Pz = Z @ np.linalg.pinv(Z.T @ Z) @ Z.T
    Xh = Pz @ X
    A = np.linalg.pinv(Xh.T @ X)
    b = A @ (Xh.T @ Y)
    e = Y - X @ b
    V = A @ _meat(Xh, e, d, cov, cluster) @ A.T
    k = X.shape[1]
    if cov == "cluster":
        G = d[cluster].nunique()
        V *= G / (G - 1) * (n - 1) / (n - k)
    else:
        V *= n / (n - k)
    res = {"n": n, "coef": dict(zip(x, b[:len(x)])), "se": dict(zip(x, np.sqrt(np.diag(V))[:len(x)])),
           "const": b[len(x)] if fe is None else np.nan,
           "ser": float(np.sqrt(e @ e / (n - k))), "dw": float(np.sum(np.diff(e) ** 2) / (e @ e))}
    res["first_f"] = first_stage_f(d, x[0], z, W, cov, cluster) if list(z) != list(x) else np.nan
    return res


def _meat(Xh, e, d, cov, cluster):
    s = Xh * e[:, None]
    if cov == "cluster":
        g = d[cluster].values
        S = np.vstack([s[g == v].sum(axis=0) for v in np.unique(g)])
        return S.T @ S
    # Newey-West over the time index (for a single time series the rows are years)
    M = s.T @ s
    for lag in range(1, HAC_LAGS + 1):
        G = s[lag:].T @ s[:-lag]
        M += (1 - lag / (HAC_LAGS + 1)) * (G + G.T)
    return M


def first_stage_f(d, xcol, z, W, cov, cluster):
    Zf = np.column_stack([d[c].values for c in z] + [W])
    xv = d[xcol].values
    A = np.linalg.pinv(Zf.T @ Zf)
    g = A @ Zf.T @ xv
    u = xv - Zf @ g
    V = A @ _meat(Zf, u, d, cov, cluster) @ A
    q = len(z)
    gz, Vz = g[:q], V[:q, :q]
    return float(gz @ np.linalg.pinv(Vz) @ gz / q)


def summarize(res, xname, label, extra=None):
    b, se = res["coef"][xname], res["se"][xname]
    lo, hi = b - 1.96 * se, b + 1.96 * se
    mu = lambda v: 1 / (1 - v) if v < 1 else np.inf       # mu = 1/(1-beta) is monotone below beta = 1
    row = {"specification": label, "beta": b, "se": se, "ci_low": lo, "ci_high": hi,
           "markup_mu": 1 / (1 - b), "mu_ci_low": mu(lo), "mu_ci_high": mu(hi),
           "first_stage_F": res["first_f"], "n": res["n"],
           "intercept": res["const"], "ser": res["ser"], "dw": res["dw"]}
    row.update(extra or {})
    return row


# ----------------------------------------------------------------------------- analyses

def hall_check(z):
    """Hall's 1949-78 total-manufacturing regression from his printed Table 1."""
    t = pd.read_csv(RAW / "hall1986_table1.csv").set_index("year")
    t = t / 100
    t["solow_recomputed"] = t.output_growth - t.labor_share * t.hours_growth
    t = t.join(z[["d_gnp", "d_gdp"]])
    t = t.reset_index()
    gap = (t.solow_recomputed - t.solow_residual).abs().max()
    print(f"Hall Table 1: {len(t)} years; largest gap between printed and recomputed residual "
          f"{gap * 100:.2f} points (rounding)")
    rows = [{"specification": "Hall (1986 WP), printed eq. 4.1, IV real GNP", "beta": 0.385, "se": 0.070,
             "markup_mu": 1 / (1 - 0.385), "intercept": -0.0071, "ser": 0.022, "dw": 1.40, "n": 30}]
    rows.append(summarize(iv(t, "solow_residual", ["output_growth"], ["d_gnp"]), "output_growth",
                          "Rerun on Hall's Table 1, IV real GNP (current FRED vintage)"))
    rows.append(summarize(iv(t, "solow_residual", ["output_growth"], ["output_growth"]), "output_growth",
                          "Rerun on Hall's Table 1, OLS"))
    return pd.DataFrame(rows)


def total_manufacturing(tot):
    rows = []
    base = dict(y="solow_va", x=["dq"])
    early, late = tot[tot.year <= SPLIT_YEAR], tot[tot.year > SPLIT_YEAR]
    info = lambda x: {"mean_labor_share_va": x.alpha.mean(), "mean_materials_share": x.s_m.mean()}
    rows.append(summarize(iv(tot, z=["d_gdp"], **base), "dq", "IV real GDP growth, 1959-2016", info(tot)))
    rows.append(summarize(iv(tot, z=["dq"], **base), "dq", "OLS, 1959-2016", info(tot)))
    rows.append(summarize(iv(tot, z=["d_defense", "d_oil", "democrat"], **base), "dq",
                          "IV defense, oil, party (Hall-Ramey), 1959-2016", info(tot)))
    rows.append(summarize(iv(early, z=["d_gdp"], **base), "dq", f"IV real GDP growth, 1959-{SPLIT_YEAR}", info(early)))
    rows.append(summarize(iv(late, z=["d_gdp"], **base), "dq", f"IV real GDP growth, {SPLIT_YEAR + 1}-2016", info(late)))
    out = pd.DataFrame(rows)
    sv = 1 - tot.s_m.mean()
    out["va_share_of_sales"] = sv
    out["beta_star_lower_bound"] = out.beta * sv            # Hall's conversion to gross output
    out["mu_star_lower_bound"] = 1 / (1 - out.beta_star_lower_bound)
    return out


def by_industry(p3, names):
    rows = []
    hall = pd.read_csv(RAW / "hall1986_table2.csv").set_index("sic")
    for code, x in p3.groupby("group"):
        r_iv = iv(x, "solow_va", ["dq"], ["d_gdp"])
        r_ols = iv(x, "solow_va", ["dq"], ["dq"])
        sic = HALL_SIC_FOR_NAICS.get(code)
        rows.append(summarize(r_iv, "dq", "IV real GDP growth", {
            "naics3": code, "industry": names.get(code, code), "beta_ols": r_ols["coef"]["dq"],
            "se_ols": r_ols["se"]["dq"], "va_share_of_sales": 1 - x.s_m.mean(),
            "va_2016_bn": x.loc[x.year == LAST_YEAR, "va"].sum() / 1000,
            "hall_sic": sic, "hall_industry": hall.description.get(sic) if sic else None,
            "hall_beta_iv": hall.iv_slope.get(sic) if sic else np.nan,
            "hall_se_iv": hall.iv_se.get(sic) if sic else np.nan}))
    out = pd.DataFrame(rows)
    out["weak_instrument"] = out.first_stage_F < WEAK_F
    out["reject_mu_eq_1"] = out.ci_low > 0
    return out.sort_values("beta", ascending=False)


def pooled(p3, ycol="solow_va", xcol="dq", label="Value added"):
    rows = []
    for z, zlab in [(["d_gdp"], "IV real GDP growth"), (["d_defense", "d_oil", "democrat"], "IV Hall-Ramey"),
                    ([xcol], "OLS")]:
        for lo, hi in [(FIRST_YEAR, LAST_YEAR), (FIRST_YEAR, SPLIT_YEAR), (SPLIT_YEAR + 1, LAST_YEAR)]:
            x = p3[(p3.year >= lo) & (p3.year <= hi)]
            r = iv(x, ycol, [xcol], z, fe="group", cov="cluster", cluster="year")
            rows.append(summarize(r, xcol, f"{label}, {zlab}, {lo}-{hi}, industry FE, SE clustered by year"))
    return pd.DataFrame(rows)


def scatter(tot, path):
    fig, ax = plt.subplots(figsize=(7, 5.2))
    rec = tot.year.isin([1961, 1970, 1974, 1975, 1980, 1982, 1991, 2001, 2008, 2009])
    ax.scatter(tot.dq[~rec] * 100, tot.solow_va[~rec] * 100, color="#4a6fa5", s=28, label="Other years")
    ax.scatter(tot.dq[rec] * 100, tot.solow_va[rec] * 100, color="#c8553d", s=28, label="Recession years")
    for yr in [1975, 1982, 2009, 2010, 1984, 1976]:
        r = tot[tot.year == yr].iloc[0]
        ax.annotate(str(yr), (r.dq * 100, r.solow_va * 100), fontsize=8, xytext=(4, 3),
                    textcoords="offset points")
    b = iv(tot, "solow_va", ["dq"], ["d_gdp"])
    xs = np.linspace(tot.dq.min(), tot.dq.max(), 10)
    ax.plot(xs * 100, (b["const"] + b["coef"]["dq"] * xs) * 100, color="black", lw=1,
            label=f"IV slope (real GDP growth) = {b['coef']['dq']:.2f}")
    ax.axhline(0, color="grey", lw=0.5)
    ax.axvline(0, color="grey", lw=0.5)
    ax.set_xlabel("Growth of real value added per unit of capital (%)")
    ax.set_ylabel("Solow residual (%)")
    ax.set_title("US manufacturing, 1959-2016: the Solow residual rises with output")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    z = instruments()
    names = industry_names()

    check = hall_check(z)
    check.to_csv(OUT / "hall_1949_78_check.csv", index=False)
    print(check[["specification", "beta", "se", "markup_mu"]].round(3).to_string(index=False))

    d = load_nberces()
    tot = build_panel(d, "total")
    p3 = build_panel(d, 3)
    print(f"Panels: total manufacturing {len(tot)} years; three-digit {len(p3)} industry-years, "
          f"{p3.group.nunique()} industries")

    keep = ["year", "n_industries", "dy", "dm", "dk", "dh", "dv", "dq", "dn", "alpha", "s_m", "s_l",
            "solow_va", "solow_go", "d_gdp", "d_defense", "d_oil", "democrat", "vship", "va"]
    series = tot[keep].copy()
    for v, lab in [("dy", "output"), ("dh", "hours"), ("dv", "value_added")]:
        series[lab + "_growth_pct"] = (np.exp(series[v]) - 1) * 100
    series.to_csv(OUT / "total_mfg_series.csv", index=False)

    t = total_manufacturing(tot)
    t.to_csv(OUT / "total_mfg_estimates.csv", index=False)
    print(t[["specification", "beta", "se", "markup_mu", "first_stage_F"]].round(3).to_string(index=False))

    ind = by_industry(p3, names)
    ind.to_csv(OUT / "industries_value_added.csv", index=False)
    print(ind[["naics3", "industry", "beta", "se", "markup_mu", "first_stage_F", "hall_beta_iv"]]
          .round(3).to_string(index=False))

    pv = pooled(p3)
    pv.to_csv(OUT / "pooled_value_added.csv", index=False)
    print(pv[["specification", "beta", "se", "markup_mu", "first_stage_F", "n"]].round(3).to_string(index=False))

    scatter(tot, OUT / "solow_residual_scatter.png")
    print("Wrote results/hall_1949_78_check.csv, total_mfg_series.csv, total_mfg_estimates.csv, "
          "industries_value_added.csv, pooled_value_added.csv, solow_residual_scatter.png")


if __name__ == "__main__":
    main()
