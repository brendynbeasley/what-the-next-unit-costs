# Hall (1988) on modern data: findings

## In plain English

Robert Hall showed in 1986 that the productivity of American manufacturing jumps in booms and sinks in
recessions, and argued that the swing means factories sell their output well above the cost of making one more
unit. This study reruns his test on 1959-2016 factory data and 1999-2025 industry accounts, then runs Basu and
Fernald's counter-test, which counts materials and services as inputs.

- **Hall's pattern is still there.** Run his way, on value added, US manufacturing looks like it prices at 2 to 3
  times marginal cost, more than the 1.63 he found for 1949-1978. Much of the increase comes from how value added
  is measured, not from a change in pricing.
- **Counting every input shrinks the markup to about 1.2.** With materials and purchased services in the
  calculation, the pooled markup across 19 manufacturing industries in 1999-2025 is 1.18 (95% interval 1.08 to
  1.29). That is close to the lower bound Hall himself computed (1.28) and to Basu and Fernald's view.
- **Cars, trucks, steel and tires sit near the average.** Light trucks (Ford, GM, Stellantis) 1.24, automobiles
  (Toyota, Honda, GM) 1.22, steel mills (Nucor, Cleveland-Cliffs) 1.27, tires (Goodyear, Michelin) 1.18. Cement
  (Holcim, Cemex) is high at 2.15. Pharmaceuticals (Pfizer, Merck) at 2.93 partly reflect uncounted research.
- **The test is blind where demand ignores the business cycle.** Breakfast cereal, cigarettes, meat packing,
  beer, soft drinks and refining have output that barely moves with GDP, so the instrument fails (first-stage F
  below 5) and the data say nothing about their markups.

A friendlier tour is in the [README](../README.md). The rest of this page is the technical detail.

**Key to the labels below.** *beta* = Hall's slope, the Lerner index (P - MC)/P. *markup_mu* = price / marginal
cost = 1/(1 - beta). *mu_ci_low, mu_ci_high* = 95% interval for the markup (unbounded when the beta interval
reaches 1). *se* = standard error of beta (Newey-West, 2 lags, for single series; clustered by year for pooled
panels). *first_stage_F* = strength of the instrument (below 10 is weak). *Value added* = Hall's method, labor the
only input subtracted. *Gross output* = materials (NBER-CES) or energy, materials and purchased services (BEA)
also subtracted. *IV real GDP growth* = instrument is growth of real GDP; *Hall-Ramey* = growth of real defense
spending, growth of the real oil price and a Democratic-President dummy; *OLS* = no instrument. *NBER-CES* =
Census-based manufacturing data, 1959-2016. *BEA* = national industry accounts, 1999-2025. *FE* = industry fixed
effects. *materials_share* = materials cost / shipments; *services_share* = purchased services / gross output.

## Summary of answers

| Question | Answer |
|---|---|
| Does Hall's test still find price above marginal cost? | Yes. Total manufacturing, value added, 1959-2016: markup 2.93 (2.37 to 3.82). |
| Does it survive Basu and Fernald's gross-output test? | Yes, but much smaller. NBER-CES gross output 1.45; BEA with all inputs 1.24 (total) and 1.18 (pooled). |
| Constant returns to scale? | Not rejected. Implied returns 1.15, capital coefficient 0.103 (s.e. 0.092). |
| Did markups rise? | Pooled gross output 1.30 for 1959-87 and 1.52 for 1988-2016, partly a measurement effect. |

## Hall's own regression, rerun from his Table 1

File: `hall_1949_78_check.csv`. Hall's printed estimate (NBER WP 1785, eq. 4.1) beside a rerun on the numbers in his Table 1 with today's vintage of real GNP from FRED.

| specification | beta | se | markup_mu | mu_ci_low | mu_ci_high | intercept | ser | dw | first_stage_F | n |
|---|---|---|---|---|---|---|---|---|---|---|
| Hall (1986 WP), printed eq. 4.1, IV real GNP | 0.385 | 0.070 | 1.626 |  |  | -0.007 | 0.022 | 1.400 |  | 30 |
| Rerun on Hall's Table 1, IV real GNP (current FRED vintage) | 0.375 | 0.054 | 1.600 | 1.367 | 1.930 | -0.007 | 0.023 | 1.412 | 185.628 | 30 |
| Rerun on Hall's Table 1, OLS | 0.477 | 0.045 | 1.912 | 1.637 | 2.297 | -0.007 | 0.022 | 1.419 |  | 30 |

## Total manufacturing, value added (NBER-CES)

File: `total_mfg_estimates.csv`. *mean_labor_share_va* = labor compensation over Census value added; *mu_star_lower_bound* = Hall's conversion to a gross-output markup, 1/(1 - beta x value-added share of sales).

| specification | beta | se | markup_mu | mu_ci_low | mu_ci_high | first_stage_F | n | mean_labor_share_va | mu_star_lower_bound |
|---|---|---|---|---|---|---|---|---|---|
| IV real GDP growth, 1959-2016 | 0.658 | 0.041 | 2.926 | 2.369 | 3.825 | 58.249 | 58 | 0.444 | 1.414 |
| OLS, 1959-2016 | 0.711 | 0.037 | 3.465 | 2.772 | 4.618 |  | 58 | 0.444 | 1.463 |
| IV defense, oil, party (Hall-Ramey), 1959-2016 | 0.569 | 0.269 | 2.318 | 1.042 | unbounded | 0.848 | 58 | 0.444 | 1.339 |
| IV real GDP growth, 1959-1987 | 0.573 | 0.036 | 2.341 | 2.006 | 2.810 | 45.474 | 29 | 0.517 | 1.342 |
| IV real GDP growth, 1988-2016 | 0.767 | 0.049 | 4.292 | 3.030 | 7.353 | 21.165 | 29 | 0.371 | 1.518 |

## Pooled three-digit industries, value added (NBER-CES)

File: `pooled_value_added.csv`. 21 subsectors, industry fixed effects.

| specification | beta | se | markup_mu | mu_ci_low | mu_ci_high | first_stage_F | n |
|---|---|---|---|---|---|---|---|
| Value added, IV real GDP growth, 1959-2016, industry FE, SE clustered by year | 0.626 | 0.047 | 2.675 | 2.150 | 3.541 | 34.709 | 1218 |
| Value added, IV real GDP growth, 1959-1987, industry FE, SE clustered by year | 0.517 | 0.064 | 2.069 | 1.642 | 2.797 | 39.539 | 609 |
| Value added, IV real GDP growth, 1988-2016, industry FE, SE clustered by year | 0.728 | 0.059 | 3.670 | 2.572 | 6.403 | 16.014 | 609 |
| Value added, IV Hall-Ramey, 1959-2016, industry FE, SE clustered by year | 0.614 | 0.165 | 2.589 | 1.410 | 15.812 | 1.399 | 1218 |
| Value added, IV Hall-Ramey, 1959-1987, industry FE, SE clustered by year | 0.816 | 0.110 | 5.433 | 2.502 | unbounded | 1.643 | 609 |
| Value added, IV Hall-Ramey, 1988-2016, industry FE, SE clustered by year | 0.580 | 0.094 | 2.378 | 1.652 | 4.247 | 2.945 | 609 |
| Value added, OLS, 1959-2016, industry FE, SE clustered by year | 0.885 | 0.028 | 8.666 | 5.871 | 16.536 |  | 1218 |
| Value added, OLS, 1959-1987, industry FE, SE clustered by year | 0.800 | 0.038 | 4.999 | 3.639 | 7.979 |  | 609 |
| Value added, OLS, 1988-2016, industry FE, SE clustered by year | 0.928 | 0.031 | 13.875 | 7.528 | 88.461 |  | 609 |

## Three-digit industries, value added (NBER-CES), beside Hall's Table 2

File: `industries_value_added.csv`. Hall's two-digit SIC industries are matched to the nearest 2012 NAICS subsector; the match is approximate (SIC 37, transportation equipment, is absent from his table). Rows with first-stage F below 10 are unreliable.

| naics3 | industry | beta | se | markup_mu | first_stage_F | beta_ols | hall_industry | hall_beta_iv | hall_se_iv |
|---|---|---|---|---|---|---|---|---|---|
| 311 | Food Manufacturing | 1.634 | 6.548 | -1.578 | 0.011 | 0.981 | Food and beverages | 0.683 | 0.198 |
| 312 | Beverage and Tobacco Product Manufacturing | 1.009 | 0.105 | -108.453 | 3.297 | 0.975 | Tobacco | 0.158 | 0.718 |
| 324 | Petroleum and Coal Products Manufacturing | 0.993 | 0.021 | 135.143 | 1.361 | 0.997 | Petroleum refining | 0.639 | 0.159 |
| 325 | Chemical Manufacturing | 0.920 | 0.019 | 12.465 | 24.037 | 0.957 | Chemicals | 0.831 | 0.052 |
| 322 | Paper Manufacturing | 0.732 | 0.067 | 3.733 | 12.112 | 0.831 | Paper | 0.661 | 0.044 |
| 334 | Computer and Electronic Product Manufacturing | 0.700 | 0.092 | 3.332 | 14.043 | 0.811 | Machinery (electrical) | 0.301 | 0.081 |
| 314 | Textile Product Mills | 0.681 | 0.055 | 3.131 | 18.362 | 0.796 | Textiles | 0.059 | 0.245 |
| 327 | Nonmetallic Mineral Product Manufacturing | 0.670 | 0.033 | 3.032 | 22.462 | 0.692 | Stone, clay, and glass | 0.536 | 0.048 |
| 339 | Miscellaneous Manufacturing | 0.646 | 0.071 | 2.822 | 23.405 | 0.763 | Miscellaneous | 0.485 | 0.098 |
| 323 | Printing and Related Support Activities | 0.644 | 0.144 | 2.808 | 5.057 | 0.497 | Printing and publishing | 0.383 | 0.233 |
| 333 | Machinery Manufacturing | 0.621 | 0.047 | 2.640 | 37.955 | 0.691 | Machinery (non-electrical) | 0.273 | 0.056 |
| 315 | Apparel Manufacturing | 0.615 | 0.112 | 2.601 | 4.378 | 0.704 | Apparel | 0.173 | 0.179 |
| 335 | Electrical Equipment, Appliance, and Component Manufacturing | 0.609 | 0.050 | 2.558 | 56.001 | 0.675 | Machinery (electrical) | 0.301 | 0.081 |
| 332 | Fabricated Metal Product Manufacturing | 0.600 | 0.040 | 2.500 | 28.105 | 0.663 | Fabricated metals | 0.291 | 0.066 |
| 326 | Plastics and Rubber Products Manufacturing | 0.592 | 0.045 | 2.454 | 22.805 | 0.662 | Rubber | 0.289 | 0.092 |
| 337 | Furniture and Related Product Manufacturing | 0.543 | 0.054 | 2.186 | 23.399 | 0.608 | Furniture | 0.271 | 0.085 |
| 331 | Primary Metal Manufacturing | 0.538 | 0.078 | 2.165 | 22.660 | 0.717 | Primary metals | 0.512 | 0.033 |
| 336 | Transportation Equipment Manufacturing | 0.527 | 0.044 | 2.115 | 67.272 | 0.699 |  |  |  |
| 313 | Textile Mills | 0.405 | 0.156 | 1.679 | 9.160 | 0.777 | Textiles | 0.059 | 0.245 |
| 321 | Wood Product Manufacturing | 0.307 | 0.086 | 1.443 | 13.797 | 0.590 | Lumber | 0.152 | 0.204 |
| 316 | Leather and Allied Product Manufacturing | -2.155 | 8.130 | 0.317 | 0.142 | 0.750 | Leather | 0.424 | 0.159 |

## Total manufacturing, gross output (NBER-CES)

File: `extension_total_mfg.csv`. *capital_coef* = coefficient on capital growth (Hall's eq. 5.27 check); *returns_to_scale_gamma* = 1 + capital_coef / (1 - beta).

| specification | beta | se | markup_mu | mu_ci_low | mu_ci_high | first_stage_F | n | capital_coef | capital_se | returns_to_scale_gamma |
|---|---|---|---|---|---|---|---|---|---|---|
| NBER-CES total manufacturing, value added (Hall) | 0.658 | 0.041 | 2.926 | 2.369 | 3.825 | 58.249 | 58 |  |  |  |
| NBER-CES total manufacturing, gross output, materials counted | 0.311 | 0.041 | 1.451 | 1.300 | 1.642 | 87.869 | 58 |  |  |  |
| NBER-CES total manufacturing, gross output, capital growth added | 0.304 | 0.035 | 1.436 | 1.308 | 1.592 | 77.766 | 58 | 0.103 | 0.092 | 1.148 |

## Pooled three-digit industries, gross output (NBER-CES)

File: `extension_pooled_nberces.csv`. 

| specification | beta | se | markup_mu | mu_ci_low | mu_ci_high | first_stage_F | n |
|---|---|---|---|---|---|---|---|
| NBER-CES gross output, IV real GDP growth, 1959-2016, industry FE, SE clustered by year | 0.282 | 0.028 | 1.393 | 1.295 | 1.508 | 57.107 | 1218 |
| NBER-CES gross output, IV real GDP growth, 1959-1987, industry FE, SE clustered by year | 0.230 | 0.022 | 1.299 | 1.231 | 1.375 | 85.079 | 609 |
| NBER-CES gross output, IV real GDP growth, 1988-2016, industry FE, SE clustered by year | 0.340 | 0.047 | 1.515 | 1.329 | 1.764 | 17.987 | 609 |
| NBER-CES gross output, IV Hall-Ramey, 1959-2016, industry FE, SE clustered by year | 0.269 | 0.107 | 1.368 | 1.062 | 1.921 | 2.093 | 1218 |
| NBER-CES gross output, IV Hall-Ramey, 1959-1987, industry FE, SE clustered by year | 0.292 | 0.075 | 1.412 | 1.169 | 1.785 | 1.416 | 609 |
| NBER-CES gross output, IV Hall-Ramey, 1988-2016, industry FE, SE clustered by year | 0.276 | 0.056 | 1.382 | 1.201 | 1.628 | 5.683 | 609 |
| NBER-CES gross output, OLS, 1959-2016, industry FE, SE clustered by year | 0.329 | 0.020 | 1.490 | 1.407 | 1.583 |  | 1218 |
| NBER-CES gross output, OLS, 1959-1987, industry FE, SE clustered by year | 0.267 | 0.015 | 1.365 | 1.311 | 1.423 |  | 609 |
| NBER-CES gross output, OLS, 1988-2016, industry FE, SE clustered by year | 0.389 | 0.043 | 1.637 | 1.440 | 1.897 |  | 609 |

## Three-digit industries, value added against gross output (NBER-CES)

File: `industries_gross_output.csv`. *mu_va_implied_by_go* = mu_go (1 - s_M) / (1 - mu_go s_M), the Basu-Fernald identity.

| naics3 | industry | mu_va | mu_go | mu_go_ci_low | mu_go_ci_high | first_stage_F_go | materials_share | mu_va_implied_by_go |
|---|---|---|---|---|---|---|---|---|
| 312 | Beverage and Tobacco Product Manufacturing | -108.45 | 11.54 | 1.44 | unbounded | 3.33 | 0.47 | -1.40 |
| 324 | Petroleum and Coal Products Manufacturing | 135.14 | 2.27 | 0.72 | unbounded | 6.06 | 0.83 | -0.45 |
| 325 | Chemical Manufacturing | 12.47 | 1.81 | 1.48 | 2.34 | 62.85 | 0.48 | 7.42 |
| 322 | Paper Manufacturing | 3.73 | 1.55 | 1.27 | 1.99 | 19.11 | 0.55 | 4.72 |
| 327 | Nonmetallic Mineral Product Manufacturing | 3.03 | 1.55 | 1.42 | 1.71 | 24.91 | 0.45 | 2.77 |
| 323 | Printing and Related Support Activities | 2.81 | 1.54 | 1.24 | 2.06 | 6.01 | 0.40 | 2.45 |
| 339 | Miscellaneous Manufacturing | 2.82 | 1.54 | 1.29 | 1.93 | 31.69 | 0.41 | 2.50 |
| 334 | Computer and Electronic Product Manufacturing | 3.33 | 1.54 | 1.26 | 2.00 | 23.85 | 0.43 | 2.58 |
| 337 | Furniture and Related Product Manufacturing | 2.19 | 1.49 | 1.31 | 1.72 | 28.50 | 0.47 | 2.61 |
| 332 | Fabricated Metal Product Manufacturing | 2.50 | 1.48 | 1.32 | 1.68 | 51.76 | 0.47 | 2.56 |
| 333 | Machinery Manufacturing | 2.64 | 1.43 | 1.31 | 1.58 | 72.83 | 0.48 | 2.39 |
| 314 | Textile Product Mills | 3.13 | 1.42 | 1.22 | 1.69 | 37.18 | 0.61 | 4.06 |
| 335 | Electrical Equipment, Appliance, and Component Manufacturing | 2.56 | 1.39 | 1.27 | 1.54 | 67.40 | 0.49 | 2.26 |
| 326 | Plastics and Rubber Products Manufacturing | 2.45 | 1.37 | 1.26 | 1.50 | 30.55 | 0.50 | 2.19 |
| 315 | Apparel Manufacturing | 2.60 | 1.34 | 1.13 | 1.65 | 4.30 | 0.50 | 2.05 |
| 331 | Primary Metal Manufacturing | 2.17 | 1.23 | 1.09 | 1.40 | 47.70 | 0.62 | 1.97 |
| 336 | Transportation Equipment Manufacturing | 2.11 | 1.22 | 1.17 | 1.28 | 78.02 | 0.60 | 1.83 |
| 313 | Textile Mills | 1.68 | 1.20 | 0.97 | 1.58 | 11.62 | 0.59 | 1.69 |
| 321 | Wood Product Manufacturing | 1.44 | 1.13 | 1.04 | 1.24 | 17.70 | 0.60 | 1.40 |
| 316 | Leather and Allied Product Manufacturing | 0.32 | 0.81 | 0.52 | 1.87 | 4.14 | 0.52 | 0.67 |
| 311 | Food Manufacturing | -1.58 | 0.76 | 0.14 | unbounded | 0.08 | 0.66 | 0.51 |

## BEA industry accounts, 1999-2025

File: `bea_klems_estimates.csv`. 

| specification | beta | se | markup_mu | mu_ci_low | mu_ci_high | first_stage_F | n |
|---|---|---|---|---|---|---|---|
| BEA total manufacturing, value added (Hall) | 0.517 | 0.083 | 2.072 | 1.548 | 3.131 | 50.459 | 27 |
| BEA 19 industries pooled, value added (Hall), industry FE, SE clustered by year | 0.451 | 0.064 | 1.822 | 1.484 | 2.357 | 28.897 | 513 |
| BEA 19 industries pooled, value added (Hall), 2020-21 dropped, industry FE, SE clustered by year | 0.469 | 0.097 | 1.884 | 1.389 | 2.930 | 34.599 | 475 |
| BEA 19 industries pooled, value added (Hall), OLS | 0.794 | 0.055 | 4.859 | 3.180 | 10.295 |  | 513 |
| BEA total manufacturing, gross output, energy and materials counted | 0.216 | 0.043 | 1.275 | 1.152 | 1.429 | 24.457 | 27 |
| BEA 19 industries pooled, gross output, energy and materials counted, industry FE, SE clustered by year | 0.181 | 0.049 | 1.222 | 1.093 | 1.384 | 20.212 | 513 |
| BEA 19 industries pooled, gross output, energy and materials counted, 2020-21 dropped, industry FE, SE clustered by year | 0.172 | 0.061 | 1.207 | 1.055 | 1.410 | 24.966 | 475 |
| BEA 19 industries pooled, gross output, energy and materials counted, OLS | 0.268 | 0.041 | 1.366 | 1.230 | 1.536 |  | 513 |
| BEA total manufacturing, gross output, all intermediate inputs counted | 0.193 | 0.051 | 1.239 | 1.103 | 1.412 | 24.457 | 27 |
| BEA 19 industries pooled, gross output, all intermediate inputs counted, industry FE, SE clustered by year | 0.149 | 0.040 | 1.175 | 1.076 | 1.294 | 20.212 | 513 |
| BEA 19 industries pooled, gross output, all intermediate inputs counted, 2020-21 dropped, industry FE, SE clustered by year | 0.147 | 0.046 | 1.173 | 1.061 | 1.310 | 24.966 | 475 |
| BEA 19 industries pooled, gross output, all intermediate inputs counted, OLS | 0.141 | 0.020 | 1.164 | 1.114 | 1.219 |  | 513 |

## BEA industries, three ways

File: `bea_klems_industries.csv`. *mu_go_em* counts energy and materials; *mu_go_all* also counts purchased services.

| industry | mu_va | mu_go_em | mu_go_all | mu_ci_low_go_all | mu_ci_high_go_all | first_stage_F | services_share | labor_share_va |
|---|---|---|---|---|---|---|---|---|
| Other transportation equipment | 3.08 | 1.86 | 2.11 | 0.69 | unbounded | 1.42 | 0.12 | 0.61 |
| Petroleum and coal products | 33.04 | 1.62 | 1.65 | 1.27 | 2.34 | 7.09 | 0.04 | 0.16 |
| Motor vehicles, bodies and trailers, and parts | 3.16 | 1.34 | 1.45 | 1.15 | 1.99 | 23.90 | 0.07 | 0.56 |
| Printing and related support activities | 1.84 | 1.49 | 1.37 | 0.99 | 2.24 | 10.30 | 0.15 | 0.70 |
| Fabricated metal products | 2.05 | 1.33 | 1.37 | 1.26 | 1.50 | 7.45 | 0.14 | 0.68 |
| Machinery | 2.40 | 1.33 | 1.32 | 1.14 | 1.55 | 15.71 | 0.13 | 0.65 |
| Computer and electronic products | 3.03 | 1.44 | 1.28 | 0.95 | 1.95 | 6.29 | 0.13 | 0.63 |
| Textile mills and textile product mills | 2.09 | 1.36 | 1.27 | 1.08 | 1.54 | 16.83 | 0.11 | 0.76 |
| Electrical equipment, appliances, and components | 2.00 | 1.29 | 1.24 | 1.09 | 1.45 | 11.36 | 0.10 | 0.63 |
| Furniture and related products | 1.66 | 1.31 | 1.24 | 1.12 | 1.39 | 5.37 | 0.14 | 0.75 |
| Chemical products | 3.02 | 1.38 | 1.17 | 0.98 | 1.45 | 5.81 | 0.11 | 0.32 |
| Nonmetallic mineral products | 1.37 | 1.17 | 1.09 | 1.00 | 1.21 | 3.87 | 0.14 | 0.56 |
| Apparel and leather and allied products | 1.28 | 1.09 | 1.08 | 0.76 | 1.86 | 4.84 | 0.21 | 0.80 |
| Plastics and rubber products | 1.09 | 1.04 | 1.03 | 0.84 | 1.32 | 16.34 | 0.11 | 0.63 |
| Miscellaneous manufacturing | 0.94 | 1.08 | 1.00 | 0.73 | 1.59 | 12.99 | 0.17 | 0.62 |
| Primary metals | -0.23 | 0.93 | 0.86 | 0.71 | 1.08 | 7.82 | 0.10 | 0.58 |
| Wood products | 0.24 | 0.88 | 0.79 | 0.58 | 1.26 | 1.96 | 0.10 | 0.69 |
| Paper products | -0.49 | 0.75 | 0.75 | 0.51 | 1.40 | 9.79 | 0.10 | 0.56 |
| Food and beverage and tobacco products | 1.15 | -0.22 | 0.38 | 0.03 | unbounded | 0.02 | 0.08 | 0.48 |

## Named six-digit industries (NBER-CES, gross output)

File: `named_industries.csv`. *shipments_2016_bn* = value of shipments in 2016, billions of dollars; *corr_output_gdp* = correlation of the industry's output growth with real GDP growth. Weak-instrument rows (F below 10) should not be read as estimates.

| naics6 | industry | shipments_2016_bn | mu_va | mu_go | mu_go_ci_low | mu_go_ci_high | first_stage_F | mu_go_ols | corr_output_gdp |
|---|---|---|---|---|---|---|---|---|---|
| 324110 | Petroleum Refineries | 388.26 | -32.84 | 2.14 | 0.66 | unbounded | 4.13 | 2.18 | 0.01 |
| 336112 | Light Truck and Utility Vehicle Manufacturing | 187.52 | 3.28 | 1.24 | 1.14 | 1.36 | 54.70 | 1.35 | 0.66 |
| 325412 | Pharmaceutical Preparation Manufacturing | 165.19 | 8.46 | 2.93 | 1.47 | 531.01 | 15.07 | 4.68 | 0.41 |
| 336111 | Automobile Manufacturing | 130.00 | 2.80 | 1.22 | 1.13 | 1.31 | 56.36 | 1.26 | 0.68 |
| 336411 | Aircraft Manufacturing | 128.75 | 1.58 | 1.22 | 0.81 | 2.45 | 5.37 | 1.45 | 0.23 |
| 311611 | Animal (except Poultry) Slaughtering | 90.21 | -1.10 | 0.27 | 0.01 | unbounded | 0.00 | 1.44 | 0.03 |
| 331110 | Iron and Steel Mills and Ferroalloy Manufacturing | 79.61 | 2.44 | 1.27 | 1.10 | 1.49 | 24.75 | 1.27 | 0.64 |
| 311615 | Poultry Processing | 62.30 | 1.95 | 4.12 | 0.40 | unbounded | 0.12 | 1.84 | -0.06 |
| 334413 | Semiconductor and Related Device Manufacturing | 47.02 | 2.79 | 1.73 | 1.34 | 2.44 | 11.23 | 2.20 | 0.49 |
| 312230 | Tobacco Manufacturing | 42.62 | -4.34 | -0.27 | 0.03 | unbounded | 0.06 | 4.65 | 0.17 |
| 322121 | Paper (except Newsprint) Mills | 40.41 | 6.31 | 1.77 | 1.22 | 3.21 | 9.38 | 2.64 | 0.49 |
| 312111 | Soft Drink Manufacturing | 40.29 | 8.92 | 1.85 | 0.87 | unbounded | 3.99 | 2.01 | 0.33 |
| 312120 | Breweries | 31.23 | 3.34 | 1.74 | 0.51 | unbounded | 0.33 | 3.26 | -0.08 |
| 327320 | Ready-Mix Concrete Manufacturing | 29.82 | 4.26 | 1.49 | 1.34 | 1.68 | 9.20 | 1.52 | 0.67 |
| 321113 | Sawmills | 22.79 | 0.74 | 0.95 | 0.68 | 1.54 | 10.08 | 1.29 | 0.52 |
| 326211 | Tire Manufacturing (except Retreading) | 17.05 | 1.84 | 1.18 | 0.97 | 1.50 | 42.43 | 1.35 | 0.66 |
| 311230 | Breakfast Cereal Manufacturing | 9.44 | 20.92 | -8.94 | 1.39 | unbounded | 1.49 | 7.97 | 0.22 |
| 327310 | Cement Manufacturing | 8.70 | 6.99 | 2.15 | 1.69 | 2.97 | 10.59 | 2.05 | 0.67 |

## Headline counts

File: `headline_counts.csv`. 

| measure | value |
|---|---|
| NBER-CES value added: industries with first-stage F >= 10 | 14.000 |
| NBER-CES value added: of those, 95% CI excludes mu = 1 | 14.000 |
| NBER-CES value added: median mu among strong-instrument industries | 2.599 |
| NBER-CES gross output: industries with first-stage F >= 10 | 15.000 |
| NBER-CES gross output: of those, 95% CI excludes mu = 1 | 14.000 |
| NBER-CES gross output: median mu among strong-instrument industries | 1.434 |
| Basu-Fernald identity: median value-added mu implied by gross-output mu (strong industries) | 2.503 |
| Basu-Fernald identity: median directly estimated value-added mu (same industries) | 2.558 |
| BEA all inputs: industries with first-stage F >= 10 | 7.000 |
| BEA all inputs: of those, 95% CI excludes mu = 1 | 4.000 |
| BEA all inputs: median mu among strong-instrument industries | 1.269 |
| BEA value added: median mu among the same industries | 2.001 |

## Labor and input shares

File: `labor_share_comparison.csv`. 

| measure | value |
|---|---|
| NBER-CES (Census) labor share of value added, 1999-2016 mean | 0.342 |
| BEA (NIPA) labor share of value added net of taxes, 1999-2016 mean | 0.544 |
| BEA (NIPA) labor share of value added net of taxes, 1999-2025 mean | 0.531 |
| BEA purchased-services share of manufacturing gross output, 1999-2025 mean | 0.103 |
| BEA energy and materials share of manufacturing gross output, 1999-2025 mean | 0.540 |

## Markup ladder (figure data)

File: `markup_ladder.csv`. Data behind results/markup_ladder.png.

| label | beta | se | markup_mu | mu_ci_low | mu_ci_high | first_stage_F | n |
|---|---|---|---|---|---|---|---|
| NBER-CES 1959-2016: value added | 0.626 | 0.047 | 2.675 | 2.150 | 3.541 | 34.709 | 1218 |
| NBER-CES 1959-2016: gross output, materials | 0.282 | 0.028 | 1.393 | 1.295 | 1.508 | 57.107 | 1218 |
| BEA 1999-2025: value added | 0.451 | 0.064 | 1.822 | 1.484 | 2.357 | 28.897 | 513 |
| BEA 1999-2025: gross output, materials | 0.181 | 0.049 | 1.222 | 1.093 | 1.384 | 20.212 | 513 |
| BEA 1999-2025: gross output, all inputs | 0.149 | 0.040 | 1.175 | 1.076 | 1.294 | 20.212 | 513 |

## Figures

- `solow_residual_scatter.png`: Solow residual against growth of real value added per unit of capital, total
  manufacturing 1959-2016, with the IV line.
- `markup_ladder.png`: pooled markups as more inputs are counted, both datasets.
- `industries_va_vs_go.png`: value-added and gross-output markups for the three-digit industries with a strong
  instrument.

Year-by-year series are in `total_mfg_series.csv` (NBER-CES total manufacturing) and `bea_klems_series.csv`
(BEA industries).
