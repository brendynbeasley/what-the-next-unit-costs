# Methods review: Hall (1988)

- **Paper:** Robert E. Hall, "The Relation between Price and Marginal Cost in U.S. Industry," *Journal of
  Political Economy* 96(5), October 1988, pp. 921–947. Earlier version: NBER Working Paper No. 1785, January 1986.
- **Statistical focus:** the instrumental-variables slope of the Solow residual on output growth for total
  manufacturing, 1949–1978 (0.385, implying price 1.63 times marginal labor cost), and the industry-by-industry
  rejections of price equal to marginal cost in Table 2.
- **Review standard:** current AEA Data and Code Availability Policy and standard reporting of estimates,
  uncertainty, instrument strength and sample construction; internal consistency of the derivation and the
  testability of its identifying assumption.
- **What was read:** the full text of NBER Working Paper 1785 (January 1986), from the NBER website, including
  Tables 1 and 2, equation 4.1, the specification-error section and the conclusions. For the published version
  only the bibliographic record and abstract (IDEAS/RePEc) were read. Basu and Fernald, Federal Reserve Board
  IFDP 546 (1996), was read for its abstract and its Appendix III, which tests the "Hall-Ramey instruments"
  (current and lagged growth of the world oil price and of real defense spending, and the President's party) and
  cites Hall (1990) for them; it does not by itself establish which instruments the 1988 article used. Everything
  below refers to the working paper unless stated otherwise; the published version may differ in data,
  instruments and estimates.

## Methods summary

### Research design

Observational time-series design, one regression per industry. The paper derives, under constant returns to
scale and a constant ratio of price to marginal cost, that the Solow residual equals $`\beta\,\Delta q + (1-\beta)\theta`$
(eq. 1.6), where $`\beta = 1 - MC/P`$. It estimates $`\beta`$ by regressing the residual on the growth of the
output-capital ratio, instrumenting output growth with the growth of real GNP. Identification rests on the
assumption that true productivity growth is uncorrelated with the instrument (section 1).

### Sampling strategy

Not a sample in the statistical sense. The unit is the industry-year for total manufacturing and 21 two-digit SIC
industries (19 manufacturing, plus communication and electric, gas and sanitary services), chosen from the
national income and product accounts. The paper does not say how the 21 industries were selected or why SIC 37
(transportation equipment) does not appear in Table 2.

### Sample size

Thirty annual observations per industry, 1949–1978 (Table 1 lists 30 years). The window is set by the availability
of NIPA hours by industry. For eight industries with a 1973 definitional break, the 1972–73 change is omitted, so
those regressions have 29 observations; the paper does not report per-industry N.

### Inclusion and exclusion criteria

Years limited to 1949–1978 by data availability; the 1972–73 change dropped for lumber, furniture, chemicals,
rubber, primary metals, fabricated metals, electrical machinery and instruments (section 3). No other exclusions
are described.

### Independent and dependent variables

Dependent: the Solow residual, growth of real value added per unit of capital minus labor's share of value added
times growth of hours per unit of capital. Independent (endogenous): growth of real value added per unit of
capital. Instrument: growth of real GNP. Data: real value added (NIPA), net real capital (BEA), implicit deflator
net of indirect business taxes, hours of all employees (NIPA), compensation per hour (section 3).

### Statistical methods

Instrumental variables with one instrument per industry. Reported: slope, its standard error, the regression
standard error and the Durbin-Watson statistic; OLS slopes are added in Table 2 when the IV standard error exceeds
0.150. Section 5 derives the sign and size of biases from wage smoothing, adjustment costs, price rigidity, labor
mismeasurement, shift aggregation and increasing returns, and adds capital growth to test returns to scale.

### Reported effect sizes

The slope $`\beta`$ and its transformation $`1/(1-\beta)`$, the price to marginal labor cost ratio; a gross-output
lower bound using the value-added share of sales.

### Confidence intervals

None reported. Standard errors are given, so approximate intervals can be computed by a reader.

### P-values, if applicable

None reported. Rejections are stated verbally ("overwhelmingly rejected," "soundly rejected"); the test level is
given only for the returns-to-scale check (95 percent).

### Missing data treatment

Not discussed beyond the dropped 1972–73 changes and the restriction of the period to years with NIPA hours.

### Stated limitations

The paper itself names measurement error in output (handled by the instrument), unmeasured hours or effort, wage
smoothing, adjustment costs, price rigidity, shift aggregation and increasing returns, and argues that only
unmeasured labor input could produce large spurious estimates, requiring implausibly large swings in hours or
effort (Figures 2 to 4). It notes that real GNP is a poor instrument where demand is idiosyncratic to the
industry, and that monopsony in input markets is an alternative interpretation.

## Statistics extraction table

| Statistic | Value and unit | Source location | What it measures | What it does not establish |
|---|---|---|---|---|
| Slope of Solow residual on output growth, total manufacturing | 0.385 (s.e. 0.070), dimensionless | Eq. 4.1, p. 16 | Lerner index in value-added terms, 1949–1978, IV real GNP | A gross-output markup; validity of the instrument; constant returns |
| Intercept, total manufacturing | −0.0071 per year | Eq. 4.1 | Average productivity growth term, scaled by (1 − beta) | Anything about markups |
| Regression standard error; Durbin-Watson | 2.2 percent; 1.40 | Below eq. 4.1 | Fit and first-order serial correlation of residuals | Whether standard errors are robust to serial correlation |
| Price to marginal labor cost | 1.63, ratio | p. 16 text | 1/(1 − 0.385) | Price over total marginal cost |
| Value added share of manufacturing sales | 56.9 percent | p. 16 text | Used to convert to gross output | That materials move one for one with output |
| Lower bound on price over total marginal cost | 1.28, ratio | p. 16 text | 1/(1 − 0.385 × 0.569) | An upper bound or a point estimate |
| Industries rejecting price = marginal cost | 16 of 21 | Introduction, p. 2; p. 18 | Count of IV slopes significantly above zero | Any joint or multiple-testing correction |
| Industries where beta exceeds 0.5 | 8 of 21 | p. 18 text | Price gap larger than marginal labor cost | Gross-output markups above 2 |
| IV slopes by industry | 0.059 (textiles) to 0.874 (electric, gas, sanitary) | Table 2 | Industry Lerner indexes in value-added terms | Comparability across industries with different materials shares |
| OLS slopes where IV imprecise | 0.275 (apparel) to 0.965 (utilities) | Table 2 | Uninstrumented slopes, biased up by output error | Valid estimates of beta |
| Implied demand elasticity | about 4 | Section 6, p. 38 | Reciprocal of the gross-output parameter beta* for a typical manufacturing firm under simple monopoly | Elasticities faced by oligopolists |
| Returns-to-scale coefficients | 0.377 (utilities), 0.328 (leather); 17 of 21 accept constant returns | Section 5, eq. 5.27, p. 36 | Coefficient on capital growth, (1 − beta)(returns − 1) | Returns to scale in gross output |
| Bias from wage smoothing, adjustment costs, price rigidity | −0.02, −0.11, about 0.004 | Section 5, eqs. 5.11, 5.16 and 5.20, pp. 24–27 | Illustrative size of bias under assumed parameters | Empirical estimates of those biases |

## Interpretation notes

- The paper is careful to say that the slope measures the price gap relative to value added, and it gives the
  conversion to gross output itself. Later readers often quoted the larger value-added ratio. Basu and Fernald
  (1997) showed that the value-added and gross-output estimates differ substantially when materials co-move with
  output, which is consistent with the paper's own lower-bound calculation.
- The identifying assumption, that true productivity growth is uncorrelated with real GNP growth, is the crux. If
  aggregate technology shocks drive GNP, the instrument is correlated with the error and the estimate is biased
  upward. The paper argues for the assumption on a priori grounds but does not test it.
- Instrument strength is not reported. With one aggregate instrument and 30 observations, the first-stage fit
  matters for both bias and inference; the rerun here finds a strong first stage for total manufacturing on the
  printed data (F about 186), but industry-level strength is unknown.
- No standard errors robust to serial correlation are reported; the Durbin-Watson statistics in Table 2 range from
  0.48 (utilities) to 2.66 (leather), so conventional standard errors may be off for some industries.
- These are reporting gaps, not documented errors. No published correction to the paper was found.
- The modern rerun in this repository uses different data (NBER-CES and BEA rather than 1980s NIPA vintages) and is
  not a reproduction. On Hall's printed Table 1 with today's real GNP it gives 0.375 (0.054), close to his 0.385.

## Unanswered questions

- How the 21 industries were chosen, and why transportation equipment (SIC 37) is absent from Table 2.
- The per-industry number of observations after the 1973 breaks, and the first-stage strength industry by
  industry.
- Whether the results hold with instruments other than real GNP. The published version is often described as
  using military spending, the oil price and the President's party, but that was not checked against the
  published text here.
- How sensitive the estimates are to the capital measure, since the regressions are written per unit of capital.

## Items requiring expert verification

- The exact data, instruments, sample period and estimates in the 1988 published version, which was not read in
  full; the numbers in this review come from the 1986 working paper.
- Whether the "Hall-Ramey instruments" analyzed in Basu and Fernald's appendix are the same variables, in the same
  form, as those in Hall (1988).
- The transcription of Tables 1 and 2 into `data/raw/hall1986_table1.csv` and `data/raw/hall1986_table2.csv`,
  made from a scanned PDF; the Table 1 residuals recompute to within 0.08 points of the printed values.
