# Statistics foundations II: relationships, regression, and time dependence

<!-- Instructor draft for Mark: this note uses x for NASA global annual temperature anomaly and y
for annual mean Pier surface SST so the symbols map directly to Friday's application notebook.
Revise notation or theory depth here and update the code-object map at the end. -->

## The durable idea

Correlation and a fitted line summarize a selected relationship; they do not explain its cause. The
slope has physical units, residuals show what the line missed, and climate time series require
special caution because trend and persistence reduce the information in a simple scatterplot.

By the end of this session, you should be able to:

- interpret covariance and correlation;
- interpret slope, intercept, fitted value, and residual in physical units;
- recognize common residual patterns and influential observations;
- explain why shared trend, confounding, and autocorrelation limit a simple analysis; and
- describe what comparing levels with year-to-year changes can and cannot diagnose.

## 1. Covariance: do two quantities vary together?

For paired observations $(x_i,y_i)$, sample covariance is

$$
s_{xy}=\frac{1}{n-1}\sum_{i=1}^n(x_i-\bar{x})(y_i-\bar{y}).
$$

- Positive covariance: above-average $x$ tends to occur with above-average $y$.
- Negative covariance: above-average $x$ tends to occur with below-average $y$.
- Near-zero covariance: there is little **linear** co-variation; a nonlinear relationship may still
  exist.

If $x$ is annual global temperature anomaly in °C and $y$ is annual mean Pier SST in °C, covariance
has units °C². Its magnitude changes under unit conversion, so it is difficult to compare across
variable pairs.

## 2. Correlation standardizes covariance

Pearson correlation is

$$
r=\frac{s_{xy}}{s_xs_y}.
$$

It is unitless and lies between $-1$ and $1$ when both variables have nonzero variation.

Correlation describes the direction and strength of a **linear** association. It does not by itself
report slope, physical importance, prediction error, causation, or whether the pattern is stable
across periods.

### What changes under a unit conversion?

Converting Pier SST from degrees Celsius to degrees Fahrenheit multiplies its deviations by $9/5$.
The covariance and regression slope are multiplied by $9/5$; the intercept also changes because of
the 32 °F offset. Pearson correlation is unchanged under a positive linear transformation.

### Plot time before trusting $r$

Two unrelated quantities can have a high correlation when each rises smoothly with time. In a
climate analysis, calendar time is not merely a label: it can stand in for changing forcings,
instrumentation, sampling, circulation, and many omitted processes. Always inspect both time series
and show time in the scatterplot before compressing the sample to $r$.

## 3. A least-squares line

The simple linear model is written

$$
y_i=\beta_0+\beta_1x_i+\varepsilon_i.
$$

The fitted line uses estimated coefficients:

$$
\hat{y}_i=b_0+b_1x_i,
\qquad
e_i=y_i-\hat{y}_i.
$$

Least squares chooses $b_0$ and $b_1$ to minimize

$$
\mathrm{SSE}=\sum_i e_i^2.
$$

The fitted slope can be written

$$
b_1=\frac{s_{xy}}{s_x^2},
\qquad
b_0=\bar{y}-b_1\bar{x}.
$$

For global anomaly $x$ and Pier SST $y$, $b_1$ has units local °C per global-anomaly °C: the fitted
difference in local annual SST associated with a 1 °C higher global anomaly **within the selected
annual pairs**. That wording does not claim that directly changing the plotted global index would
cause an immediate $b_1$ change at the Pier.

### Hypothetical worked example

Suppose a fitted line is

$$
\widehat{\mathrm{PierSST}}=17.0\ ^\circ\mathrm{C} +
(0.70\ ^\circ\mathrm{C}/^\circ\mathrm{C})\,\mathrm{GISTEMP\ anomaly}.
$$

At a global anomaly of 0.8 °C, fitted Pier SST is 17.56 °C. If the observed annual Pier mean is
18.10 °C, the residual is $18.10-17.56=0.54$ °C. The residual is what the line failed to predict for
that year; it is not automatically measurement error.

An anomaly of 0 °C corresponds to NASA's 1951–1980 global baseline, so the intercept is more
interpretable here than an extrapolation to an impossible physical value. It is still a fitted
summary, not necessarily the observed Pier climatology for that exact period.

## 4. Residuals are a diagnostic view

Plot residuals against fitted values, the predictor, and time. Look for:

| Pattern | Possible concern |
|---|---|
| Curved center | A straight line misses nonlinearity |
| Funnel-shaped spread | Variance changes with the fitted level |
| A few distant years | Influential observations need investigation |
| Long runs above/below zero | Persistence, regime change, or an omitted process |
| Different early/late behavior | A single stationary relationship may be inappropriate |

A good residual plot does not prove every assumption. A patterned residual plot is evidence that the
simple line is incomplete.

## 5. Assumptions belong beside the result

The formulas used for familiar regression standard errors and tests commonly rely on:

- an appropriate linear mean relationship;
- errors centered near zero conditional on $x$;
- independent sampling/errors;
- roughly stable error variance for the simplest formulas; and
- no single observation dominating the result.

Normal error assumptions are mainly about exact small-sample inference, not a requirement that the
raw $x$ or $y$ values themselves be normally distributed.

Friday's core notebook emphasizes plots, units, residuals, and sensitivity comparisons rather than
treating a default p-value as a scientific verdict.

## 6. Shared trend and first differences

Define a first difference as

$$
\Delta y_t=y_t-y_{t-1}.
$$

Correlating $\Delta x_t$ with $\Delta y_t$ asks whether consecutive-year changes move together. It
removes much of a smooth trend, so comparing correlation in levels with correlation in first
differences can reveal how much the levels relationship depends on low-frequency change.

Differencing is not a magic repair:

- it changes the scientific question from levels to changes;
- it can amplify measurement noise;
- it discards the first value and must not bridge missing calendar years silently;
- it does not remove all autocorrelation or confounding; and
- a climate response may be lagged or distributed over many years.

Other trend-aware approaches include anomalies relative to a climatology, explicit time terms,
detrending, lagged models, and mechanistic climate models. Each represents additional assumptions.

## 7. Confounding, attribution, and causation

Pier SST responds to regional circulation, upwelling, winds, air–sea heat exchange, climate modes,
weather, local sampling, and long-term forcing. NASA global temperature is itself a response index,
not an experimentally assigned predictor.

Atmospheric CO₂ is a well-established climate forcing, but a regression of contemporaneous annual
Pier SST on Mauna Loa CO₂ is not an attribution model. Both series trend, CO₂ forcing acts through
the climate system, responses can lag, and many forcings and local processes are omitted.

A correlation supports a bounded statement about association in the selected sample. Establishing
cause or attribution requires physical theory, competing explanations, suitable design/models, and
additional evidence.

## 8. Autocorrelation and effective information

Annual climate values can still be persistent. Adjacent years are therefore not necessarily
independent replicates. Lag-one correlation for a series $z_t$ is the correlation between $z_t$ and
$z_{t-1}$, calculated on aligned consecutive pairs.

A nonzero lag-one residual correlation tells us the line leaves time structure. It does not by
itself select the correct time-series model. Introductory responses include aggregation,
trend/first-difference sensitivity checks, block methods, and dependence-aware models.

## 9. What a small model can and cannot say

A careful result sounds like:

> Across the selected matched years, annual mean Pier surface SST and NASA global temperature
> anomaly had a fitted association of [slope with units]. The residual plot showed [pattern], and
> the relationship [did/did not] remain similar for year-to-year changes. Shared trend, dependence,
> local processes, sampling, and the observational design limit causal or predictive claims.

Avoid:

- “global temperature causes exactly this local change” from one scatterplot;
- calling the Pier–CO₂ slope a direct CO₂ effect;
- reporting $r$ without plotting both series in time;
- ignoring the completeness rule used to make annual means;
- treating annual values as automatically independent; or
- interpreting a small p-value as a large or important physical effect.

## Notebook bridge: notation to code

| Theory | Friday code object |
|---|---|
| Predictor $x_i$ | `analysis["global_temp_anomaly_c"]` |
| Response $y_i$ | `analysis["pier_mean_sst_c"]` |
| Correlation $r$ | `correlation` |
| Slope/intercept $b_1,b_0$ | `slope_local_per_global`, `intercept_c` |
| Fitted value $\hat{y}_i$ | `analysis["fitted_pier_sst_c"]` |
| Residual $e_i$ | `analysis["residual_c"]` |
| Time-dependence check | `analysis["residual_c"].autocorr(lag=1)` |
| First differences | `changes` |

## Concept checks

1. If Pier SST is converted from °C to °F, what happens to $r$ and the slope?
2. Both plotted series rise through time, but their first-difference correlation is near zero. What
   did the levels correlation partly summarize?
3. A residual plot bends upward at low and high fitted values. What did the straight line miss?
4. Why does correlating annual Pier SST with Mauna Loa CO₂ not estimate a direct causal CO₂ effect?

<details>
<summary>Check your reasoning</summary>

1. $r$ is unchanged; the numerical slope is multiplied by $9/5$ and its response units become °F.
2. Shared low-frequency trend/calendar time, not necessarily year-to-year co-variation.
3. Nonlinearity or an omitted nonlinear term/process.
4. The data are observational and trending; responses can be lagged, and many global and local
   processes are omitted. Physical attribution needs more than this bivariate fit.

</details>

## Continuation: derive the least-squares slope

Differentiate $\sum_i[y_i-(b_0+b_1x_i)]^2$ with respect to $b_0$ and $b_1$, set both derivatives to
zero, and solve the normal equations. Centering $x$ and $y$ makes the slope result
$b_1=s_{xy}/s_x^2$ especially clear.
