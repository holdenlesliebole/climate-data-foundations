# Statistics foundations II: relationships, regression, and time dependence

<!-- Instructor draft for Mark: this note uses x for peak period and y for significant wave height
so its symbols map directly to Friday's MOP notebook. Revise notation or theory depth here and then
update the code-object map at the end. -->

## The durable idea

Correlation and a fitted line summarize a relationship; they do not explain its cause. The slope has
physical units, residuals show what the line missed, and uncertainty claims require assumptions
about sampling and dependence.

By the end of this session, you should be able to:

- interpret covariance and correlation;
- interpret slope, intercept, fitted value, and residual in physical units;
- recognize common residual patterns and influential observations;
- explain why seasonality, confounding, and autocorrelation limit a simple analysis; and
- treat peak direction as circular rather than ordinary linear data.

## 1. Covariance: do two quantities vary together?

For paired observations $(x_i,y_i)$, sample covariance is

$$
s_{xy}=\frac{1}{n-1}\sum_{i=1}^n(x_i-\bar{x})(y_i-\bar{y}).
$$

- Positive covariance: above-average $x$ tends to occur with above-average $y$.
- Negative covariance: above-average $x$ tends to occur with below-average $y$.
- Near-zero covariance: there is little **linear** co-variation; a nonlinear relationship may still
  exist.

If $x$ is peak period in seconds and $y$ is wave height in meters, covariance has units m·s. Its
magnitude changes under unit conversion, so it is difficult to compare across variable pairs.

## 2. Correlation standardizes covariance

Pearson correlation is

$$
r=\frac{s_{xy}}{s_xs_y}.
$$

It is unitless and lies between $-1$ and $1$ when both variables have nonzero variation.

Correlation describes the direction and strength of a **linear** association. It does not by itself
report slope, physical importance, prediction error, causation, or whether the pattern is stable
across seasons.

### What changes under unit conversion?

Converting meters to centimeters multiplies covariance and the regression slope when wave height is
the response. It does not change Pearson correlation because the same positive scale factor appears
in numerator and denominator.

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

For peak period $x$ in seconds and wave height $y$ in meters, $b_1$ has units m s$^{-1}$: the fitted
change in wave height associated with a one-second increase in peak period **within this sample**.
That wording does not claim that changing period would cause height to change.

### Worked example

Suppose a fitted line is

$$
\widehat{\mathrm{waveHs}}=-0.40\ \mathrm{m} +
(0.12\ \mathrm{m\,s^{-1}})\,\mathrm{waveTp}.
$$

At 10 s, the fitted height is 0.80 m. If the observed height is 1.10 m, the residual is
$1.10-0.80=0.30$ m. The residual is what the line failed to predict for that observation; it is not
automatically measurement error.

The intercept corresponds to a peak period of 0 s, outside the physical range. It is needed to
position the line but may have no useful standalone interpretation.

## 4. Residuals are a diagnostic view

Plot residuals against fitted values, the predictor, and time. Look for:

| Pattern | Possible concern |
|---|---|
| Curved center | A straight line misses nonlinearity |
| Funnel-shaped spread | Variance changes with the fitted level |
| A few distant points | Outliers or influential observations need investigation |
| Long runs above/below zero | Time dependence or a missing time-varying process |
| Separate seasonal clouds | Seasonality or a grouping variable is omitted |

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

Friday's core notebook emphasizes plots, units, residuals, and a sensitivity comparison rather than
treating a default p-value as a scientific verdict.

## 6. Seasonality, confounding, and causation

Two variables can move together because both respond to another process. For waves, storms, swell
source, direction, bathymetry, and season can influence height and period. Pooling seasons may create,
hide, or reverse a relationship.

A correlation supports a bounded statement about association in the selected sample. Establishing
cause usually requires design, mechanistic reasoning, competing explanations, and additional
evidence.

## 7. Autocorrelation and effective information

Hourly wave conditions are persistent. Adjacent rows are therefore not equivalent to independent
replicates. Lag-one autocorrelation for a series $z_t$ is the correlation between $z_t$ and
$z_{t-1}$, calculated on aligned pairs.

A high lag-one residual autocorrelation tells us the line leaves time structure. It does not by
itself select the correct time-series model. Introductory responses include aggregation, event/block
sampling, dependence-aware models, and sensitivity checks.

## 8. Peak direction is circular

Directions wrap around: 1° and 359° are 2° apart, not 358° apart. Before interpretation, read the
metadata to determine whether direction is wave-from or wave-toward and whether degrees are relative
to true or magnetic north.

For a circular mean, convert angles $\theta_i$ to unit vectors:

$$
C=\frac{1}{n}\sum_i\cos\theta_i,
\qquad
S=\frac{1}{n}\sum_i\sin\theta_i,
\qquad
\bar{\theta}=\operatorname{atan2}(S,C).
$$

Friday's core path uses a polar histogram or directional bins. Circular summaries are a continuation
option because the metadata convention and concentration also need interpretation.

## 9. What a small model can and cannot say

A careful result sounds like:

> In the selected D0513 MOP model-output period, peak period and significant wave height had a
> positive/negative fitted association of [slope with units]. The residual plot showed [pattern], and
> the result [did/did not] change materially under [stated sensitivity check]. Hourly dependence,
> model-output status, seasonality, and omitted physical variables limit causal or long-term claims.

Avoid:

- “$x$ causes $y$” from one observational/model-output scatterplot;
- reporting $r$ without the plot;
- calling a small p-value a large or important effect;
- ignoring slope units;
- treating thousands of hourly rows as thousands of independent events; or
- averaging direction degrees as ordinary numbers across north.

## Notebook bridge: notation to code

| Theory | Friday code object |
|---|---|
| Predictor $x_i$ | `analysis["waveTp"]` |
| Response $y_i$ | `analysis["waveHs"]` |
| Correlation $r$ | `correlation` |
| Slope/intercept $b_1,b_0$ | `slope_m_per_s`, `intercept_m` |
| Fitted value $\hat{y}_i$ | `analysis["fitted_waveHs"]` |
| Residual $e_i$ | `analysis["residual_m"]` |
| Time dependence check | `analysis["residual_m"].autocorr(lag=1)` |

## Concept checks

1. If wave height is converted from meters to centimeters, what happens to $r$ and the slope?
2. A residual plot bends upward at low and high fitted values. What did the straight line miss?
3. A correlation based on 5,000 consecutive hourly rows is precise under an iid formula. What key
   assumption should you question first?
4. Why can the arithmetic mean of 1° and 359° be scientifically misleading?

<details>
<summary>Check your reasoning</summary>

1. $r$ is unchanged; the numerical slope is multiplied by 100 and its units become cm/s.
2. Nonlinearity or an omitted nonlinear term/process.
3. Independence: consecutive wave conditions are time-dependent.
4. It gives 180°, even though both directions are close to north; circular geometry is required.

</details>

## Continuation: derive the least-squares slope

Differentiate $\sum_i[y_i-(b_0+b_1x_i)]^2$ with respect to $b_0$ and $b_1$, set both derivatives to
zero, and solve the normal equations. Centering $x$ and $y$ makes the slope result
$b_1=s_{xy}/s_x^2$ especially clear.
