# Technical notes

This is the technical companion to the [README](README.md). Every table is reproduced in
[results/FINDINGS.md](results/FINDINGS.md), and every number below is in a CSV in `results/`.

## The original study

Robert E. Hall, "The Relation between Price and Marginal Cost in U.S. Industry," *Journal of Political Economy*
96(5), October 1988, pp. 921–947; earlier version NBER Working Paper 1785, January 1986. The figures quoted here
come from the working paper, which is freely available; the published version could not be read in full. Using
NIPA value added, hours and BEA capital for 1949–1978 and real GNP growth as the instrument, Hall regressed the
Solow residual on the growth of the output-capital ratio. For total manufacturing (eq. 4.1) he reported a slope of
0.385 (s.e. 0.070), a price to marginal labor cost ratio of 1.63, and, with value added at 56.9% of sales, a lower
bound of 1.28 for price over total marginal cost. Price equal to marginal cost was rejected in 16 of 21 two-digit
industries (Table 2).

## Headline results

| Specification | $`\hat\beta`$ (s.e.) | $`\hat\mu`$ | 95% interval for $`\mu`$ | First-stage F | N |
|---|---|---|---|---|---|
| Hall, total manufacturing 1949–78 (printed) | 0.385 (0.070) | 1.63 | | | 30 |
| Hall's Table 1 rerun, IV real GNP | 0.375 (0.054) | 1.60 | 1.37–1.93 | 185.6 | 30 |
| NBER-CES total manufacturing, value added, 1959–2016 | 0.658 (0.041) | 2.93 | 2.37–3.82 | 58.2 | 58 |
| NBER-CES total manufacturing, gross output | 0.311 (0.041) | 1.45 | 1.30–1.64 | 87.9 | 58 |
| NBER-CES 21 industries pooled, value added | 0.626 (0.047) | 2.68 | 2.15–3.54 | 34.7 | 1,218 |
| NBER-CES 21 industries pooled, gross output | 0.282 (0.028) | 1.39 | 1.30–1.51 | 57.1 | 1,218 |
| BEA total manufacturing, value added, 1999–2025 | 0.517 (0.083) | 2.07 | 1.55–3.13 | 50.5 | 27 |
| BEA total manufacturing, gross output, all inputs | 0.193 (0.051) | 1.24 | 1.10–1.41 | 24.5 | 27 |
| BEA 19 industries pooled, value added | 0.451 (0.064) | 1.82 | 1.48–2.36 | 28.9 | 513 |
| BEA 19 industries pooled, gross output, energy and materials | 0.181 (0.049) | 1.22 | 1.09–1.38 | 20.2 | 513 |
| BEA 19 industries pooled, gross output, all inputs | 0.149 (0.040) | 1.18 | 1.08–1.29 | 20.2 | 513 |

## Data

All files are in `data/raw/` and were downloaded on 1 November 2026.

- `nberces5818v1_n2012.csv`: NBER-CES Manufacturing Industry Database, 1958–2018 release, 364 six-digit 2012
  NAICS industries (https://data.nber.org/nberces/nberces5818v1/nberces5818v1_n2012.csv). Capital is a
  start-of-year stock and ends in 2016. `naics_names_2012.txt` gives industry titles (same folder).
- `bea_GdpByInd.zip`: BEA GDP-by-industry accounts, the release posted on 1 November 2026
  (https://apps.bea.gov/industry/Release/ZIP/GdpByInd.zip; workbooks dated 28 September 2026). Tables TGO103 (gross output quantity index),
  TVA103 (value added quantity index), TKG105 (composition of gross output), TKE103, TKM103, TKS103 (energy,
  materials and purchased-services quantity indexes).
- `bea_FixedAssets_Section3All.xlsx`: Table 3.2ESI, chain-type quantity index of net private fixed assets by
  industry, year-end (https://apps.bea.gov/national/FixedAssets/Release/XLS/Section3All_xls.xlsx).
- `bea_NIPA_Section6All.xlsx`: NIPA Table 6.5D, full-time-equivalent employees by industry
  (https://apps.bea.gov/national/Release/XLS/Survey/Section6All_xls.xlsx).
- FRED (`https://fred.stlouisfed.org/graph/fredgraph.csv?id=...`): GDPCA, GNPCA (real GDP and GNP),
  B824RA3A086NBEA (real national defense spending), WTISPLC (WTI crude price), A191RD3A086NBEA (GDP deflator),
  A033RC1A027NBEA and A034RC1A027NBEA (compensation and wages of all employees), AWHMAN, CES3100000007,
  CES3200000007 (average weekly hours of production workers in manufacturing, durable and nondurable goods).
- `hall1986_table1.csv`, `hall1986_table2.csv`: Hall's Tables 1 and 2, transcribed from the working paper.
- `presidents_party.csv`: party of the President by calendar year, for the Hall-Ramey instrument set.

## Method

The estimating equation is Hall's, written for industry $`i`$ and year $`t`$.

```math
\begin{aligned}
r_{it} &\equiv \Delta q_{it} - \alpha_{it}\,\Delta n_{it} = \gamma_i + \beta\,\Delta q_{it} + \varepsilon_{it} \\
\Delta q_{it} &= \delta_i + \pi\,\Delta\ln \text{GDP}_t + v_{it}, \qquad \hat\mu = \frac{1}{1-\hat\beta}
\end{aligned}
```

The gross-output version replaces the left side with output growth net of every input's revenue-share-weighted
growth, all per unit of capital, and the regressor with $`\Delta y_{it} - \Delta k_{it}`$. The value-added and
gross-output markups are linked when materials are proportional to output.

```math
\mu_{\text{VA}} = \frac{\mu_{\text{GO}}(1-s_M)}{1-\mu_{\text{GO}}\,s_M}, \qquad \beta^{*} = \beta_{\text{VA}}\,(1 - s_M)
```

Rules fixed before estimation:

1. Sample. NBER-CES growth years 1959–2016; six-digit industry-years with missing or non-positive output,
   inputs or capital, or materials above shipments, are dropped (117 of 21,476). A six-digit industry enters a year's aggregate change
   only if it is observed in both that year and the year before. BEA growth years 1999–2025, 19
   manufacturing industries plus the manufacturing total.
2. Labor. NBER-CES hours are production-worker hours scaled by total over production employment; payroll is
   multiplied by the economy-wide compensation/wage ratio to add benefits. BEA hours are FTE employees times
   average weekly hours (durable or nondurable goods; all manufacturing for the total).
3. Output and inputs. NBER-CES real output is shipments over the shipments deflator; real materials (including
   energy) is materials cost over its deflator; real value added is the Divisia aggregate of Hall's eq. (2.2).
   Three-digit and total aggregates are Törnqvist indexes of six-digit growth rates. BEA quantities are the
   published chain-type indexes; capital at the start of year $`t`$ is the year-end stock of $`t-1`$.
4. Shares. Two-year averages (Törnqvist). BEA shares are of revenue net of taxes on production, as Hall used
   prices net of indirect taxes.
5. Instrument. Real GDP growth (Hall's working paper used real GNP). The Hall-Ramey set (growth of real defense
   spending, growth of the real oil price, a Democratic-President dummy, current-year values only; Basu and Fernald also use one lag) is reported as a
   robustness check.
6. Inference. Single series use Newey-West standard errors with 2 lags; pooled panels have industry fixed effects
   and standard errors clustered by year. First-stage F is a robust Wald statistic divided by the number of
   instruments; F below 10 is flagged as weak. Intervals for $`\mu`$ transform the endpoints of the $`\beta`$
   interval.

## Full test statistics

- Hall's Table 1 rerun: OLS slope 0.477 (0.045); IV intercept −0.007, regression standard error 0.023,
  Durbin-Watson 1.41 (Hall: −0.0071, 0.022, 1.40).
- NBER-CES total manufacturing, value added: OLS 0.711 (0.037); Hall-Ramey IV 0.569 (0.269), F = 0.85;
  1959–87 0.573 (0.036), F = 45.5; 1988–2016 0.767 (0.049), F = 21.2. Mean labor share of value added 0.517 and
  0.371 in the two halves. Hall's conversion gives $`\beta^* = 0.293`$ and $`\mu^* = 1.41`$.
- Returns to scale (gross output, capital growth added): capital coefficient 0.103 (0.092), implied
  returns to scale $`1 + 0.103/(1-0.304) = 1.15`$; constant returns not rejected.
- Pooled NBER-CES gross output by period: 1959–87 $`\mu`$ = 1.30 (1.23–1.38), 1988–2016 1.52 (1.33–1.76);
  Hall-Ramey IV 1.37, F = 2.09.
- Industries with first-stage F ≥ 10: 14 of 21 for value added (all 14 reject $`\mu = 1`$), 15 for gross output
  (14 reject; median $`\mu`$ 1.43). Basu-Fernald identity: median implied value-added markup 2.50 against a median
  direct estimate of 2.56. BEA, all inputs: 7 strong industries, 4 reject, median 1.27.
- BEA pooled, 2020–21 dropped: value added 1.88, all inputs 1.17. OLS, all inputs: 1.16.
- Labor share of manufacturing value added, 1999–2016: 0.342 (Census) against 0.544 (BEA).

## Reproducing the results

```bash
pip install -r requirements.txt
python src/hall_markup.py
python src/markup_extension.py
```

The first script writes the replication files and the scatter plot; the second, which imports the first, writes
the gross-output files, the named-industry table and the remaining two figures. Both run offline in under a minute.

## References

- Basu, S. & Fernald, J. G. (1997). Returns to scale in U.S. production: estimates and implications. *Journal of
  Political Economy* 105(2), 249–283. Federal Reserve Board IFDP 546 (1996).
- Becker, R., Gray, W. & Marvakov, J. NBER-CES Manufacturing Industry Database, 1958–2018 release, technical notes
  (March 2021).
- Hall, R. E. (1986). The relation between price and marginal cost in U.S. industry. NBER Working Paper 1785.
- Hall, R. E. (1988). *Journal of Political Economy* 96(5), 921–947.
- Hall, R. E. (2018). New evidence on the markup of prices over marginal costs and the role of mega-firms in the
  US economy. NBER Working Paper 24574.
- Solow, R. M. (1957). Technical change and the aggregate production function. *Review of Economics and
  Statistics* 39(3), 312–320.
