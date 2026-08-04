# Statistics foundations I: distributions, sampling, and uncertainty

<!-- Instructor draft for Mark: the notation below is deliberately compact and matches the
Thursday application notebooks. Change symbols, examples, or theory depth here first; the
code-object map at the end identifies the corresponding notebook names. -->

## The durable idea

A dataset contains observations. A statistic summarizes those observations. An uncertainty
interval describes how the estimate could vary under a stated sampling or resampling model. These
are three different things.

By the end of this session, you should be able to:

- distinguish a population, sample, observation, random variable, distribution, statistic, and
  estimator;
- interpret center, spread, and quantiles with their units;
- distinguish the spread of observations from uncertainty in an estimated mean;
- explain the logic of a sampling distribution, standard error, and confidence interval; and
- identify the resampling unit and the independence assumption in a climate-data example.

## 1. Population, sample, and observation

Suppose the scientific target is the typical June–August surface-minus-bottom temperature
difference at Scripps Pier over many possible years.

| Idea | Symbol | Pier example |
|---|---:|---|
| Population or process | — | All relevant summers, including years not observed |
| Observation | $x_i$ | One paired daily surface-minus-bottom difference |
| Sample | $x_1,\ldots,x_n$ | The usable paired days in the acquired archive |
| Population quantity | $\mu$ | The unknown process mean for the target population |
| Sample statistic | $\bar{x}$ | The mean calculated from the selected data |
| Estimator | rule $\bar{X}$ | The procedure “take the sample mean” before seeing a sample |
| Estimate | observed $\bar{x}$ | The number produced for this particular sample |

The rows in a file are not automatically a random or representative sample. How, when, where, and
why observations were collected remains part of the analysis.

## 2. A distribution needs center and spread

For $n$ observations $x_1,\ldots,x_n$, the sample mean is

$$
\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i.
$$

The median is the middle ordered value (or the mean of the two middle values). Quantiles divide the
ordered observations by proportion; the interquartile range is

$$
\mathrm{IQR} = Q_{0.75} - Q_{0.25}.
$$

The sample variance and standard deviation are

$$
s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})^2,
\qquad
s = \sqrt{s^2}.
$$

The $n-1$ denominator makes $s^2$ an unbiased estimator of population variance under the usual iid
sampling model. That fact does not make the data iid.

### Units check

If temperature differences are measured in °C:

- mean, median, quantiles, IQR, and standard deviation have units °C;
- variance has units °C²; and
- a count has no physical unit.

An answer with impossible units is evidence of a wrong calculation or interpretation.

### Worked example

For the four values $1,2,3,4$ °C:

$$
\bar{x}=2.5\ ^\circ\mathrm{C},
\quad
\sum(x_i-\bar{x})^2=5\ ^\circ\mathrm{C}^2,
\quad
s=\sqrt{5/3}\approx1.29\ ^\circ\mathrm{C}.
$$

The mean reports center. The standard deviation reports how far individual observations typically
vary around that center. Neither number shows skewness, multiple modes, gaps, or time ordering, so
we also inspect a distribution and time plot.

## 3. Observation spread is not estimate uncertainty

The standard deviation $s$ describes variation among observations. The standard error describes
variation of an estimator across hypothetical repeated samples.

Under an independent, identically distributed model, the estimated standard error of a sample mean
is

$$
\widehat{\mathrm{SE}}(\bar{x}) = \frac{s}{\sqrt{n}}.
$$

These quantities answer different questions:

| Quantity | Question |
|---|---|
| $s$ | How variable are the observed daily differences? |
| $\widehat{\mathrm{SE}}(\bar{x})$ | How much would the estimated mean vary across repeated iid samples of size $n$? |

More observations can reduce uncertainty about a mean without making the observations themselves
less variable.

## 4. Sampling distributions and intervals

A **sampling distribution** is the distribution of a statistic across hypothetical repeated
samples produced by the same sampling process. It is not the histogram of the observations in one
sample.

A familiar approximate confidence interval is

$$
\bar{x} \pm t^*\widehat{\mathrm{SE}}(\bar{x}),
$$

where the multiplier $t^*$ depends on the confidence level and degrees of freedom. Its coverage
claim depends on the model and sampling assumptions.

For a 95% frequentist interval, the careful interpretation is:

> If the sampling procedure and interval method were repeated many times under the assumptions,
> about 95% of the resulting intervals would cover the target parameter.

After one interval has been calculated, the parameter is not randomly moving inside it. Avoid “there
is a 95% probability that the fixed parameter lies in this interval” unless using a method that
actually defines such a probability statement.

## 5. Bootstrap logic

A nonparametric bootstrap approximates a sampling distribution by resampling the observed units
with replacement:

1. Name the statistic and the unit that can plausibly be exchanged.
2. Draw $n$ units with replacement from the observed $n$ units.
3. Calculate the statistic for the resample.
4. Repeat many times.
5. Use the bootstrap distribution to estimate uncertainty, for example with percentile endpoints.

The computer can repeat step 2 quickly. It cannot decide whether a daily row, storm, month, season,
or year is the scientifically defensible resampling unit.

### Pier thought experiment

Daily temperatures on adjacent days tend to be similar. Resampling individual days treats them as
exchangeable independent units and may produce an interval that is too narrow. Thursday's notebook
first creates one summer mean per year and resamples years. This is still a model, but it keeps much
of the within-summer time dependence together.

## 6. Independence is an assumption

If $x_t$ is strongly related to $x_{t-1}$, 1,000 daily rows do not necessarily contain the same
information as 1,000 independent measurements. Dependence can arise from:

- persistence in the ocean or atmosphere;
- repeated measurements from one event;
- seasonal cycles;
- spatial neighbors; and
- shared instruments or processing.

Grouping, block resampling, explicit time-series models, and sensitivity analyses are possible
responses. None is automatic. The honest introductory move is to name the dependence, choose a
defensible unit, and report how the conclusion changes under another reasonable choice.

## 7. What the formulas do not guarantee

An interval does not repair:

- biased or unrepresentative sampling;
- an incorrect unit, sensor, or quality-flag interpretation;
- nonrandom missingness;
- an inappropriate target population;
- a data-processing error; or
- a causal claim unsupported by the design.

Uncertainty calculation comes after provenance, inspection, and a clear scientific target.

## Notebook bridge: notation to code

| Theory | Thursday code object |
|---|---|
| Daily observation $x_i$ | `seasonal["surface_minus_bottom_c"]` |
| Number of usable observations $n$ | `values.size` |
| Sample mean $\bar{x}$ | `values.mean()` |
| Sample standard deviation $s$ | `values.std(ddof=1)` |
| One summer/year as a resampling unit | `annual_means` |
| Bootstrap distribution | `bootstrap_means` inside the helper |
| Interval endpoints | `lower_c`, `upper_c` |

Before the application session, be able to finish this sentence:

> My estimate is ______; my resampling unit is ______; the interval assumes ______; and it does not
> address ______.

## Concept checks

1. A daily-difference histogram has standard deviation 1.4 °C. A reported standard error is 0.2 °C.
   Which number describes individual-day variability?
2. If every temperature is converted from °C to K, what happens to differences, standard deviation,
   and variance?
3. Why might resampling years produce a wider interval than resampling every daily row?
4. Does a narrow interval establish that the sensor is unbiased or the estimate is scientifically
   important?

<details>
<summary>Check your reasoning</summary>

1. The 1.4 °C standard deviation describes individual observations.
2. Temperature differences and standard deviation are unchanged numerically for °C versus K;
   variance is also unchanged because the conversion adds a constant. Absolute means shift by
   273.15.
3. Adjacent days are dependent, so counting each as independent can exaggerate effective sample
   size. Year-level resampling also has far fewer units.
4. No. Precision is not freedom from bias, validity, practical importance, or causation.

</details>

## Continuation: why the square-root rule appears

Under independent sampling with common variance $\sigma^2$,

$$
\mathrm{Var}(\bar{X})
= \mathrm{Var}\left(\frac{1}{n}\sum_i X_i\right)
= \frac{1}{n^2}\sum_i\mathrm{Var}(X_i)
= \frac{\sigma^2}{n}.
$$

Taking the square root gives $\mathrm{SD}(\bar{X})=\sigma/\sqrt{n}$. The step that removes covariance
terms is exactly where independence enters.
