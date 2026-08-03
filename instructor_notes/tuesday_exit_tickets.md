# Tuesday exit tickets

## Session 1

Name one failure your Copilot acceptance checks catch and one important failure they do not catch.

**Expected:** a concrete caught case such as unequal length, two-dimensional input, wrong freezing
conversion, or lost unit label; and an uncaught scientific issue such as wrong source values, time
zone, representativeness, bias, or causal interpretation. “It could be wrong” without a mechanism is
not yet a strong response.

If most students name only syntax errors, begin Tuesday 2 by showing a smooth, plausible unit-error
plot and requiring an attribute/known-range check.

## Session 2

What would another researcher need to repeat your MOP request after the rolling nowcast has changed?

**Expected:** provider/dataset/site, exact URL or parameterized request, requested variables and
flags, start/end/stride/format, access time, local filename, software/load step, and scientific
metadata. A checksum identifies the received bytes but cannot recreate a response after the service
changes; preserving the local raw file matters.

If students answer only “the URL,” revisit version/access time and local preservation before
Wednesday's reproducibility session.
