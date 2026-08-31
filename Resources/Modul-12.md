# Module 12 — Exploratory Data Analysis

> **Course:** Algorithms and Programming  
> **Programming language:** Python  
> **Supported runtime:** Python 3.10 or later  
> **Primary libraries:** pandas, NumPy, Matplotlib  
> **Resource type:** Technical learning module  
> **Practical notebook:** Deferred to `../Practice/Modul_12.ipynb`  
> **Estimated study time:** 5 hours

## 1. Module scope

Exploratory data analysis (EDA) is a structured investigation of a dataset's schema, quality, distributions, and relationships before formal modelling or decision-making. EDA combines computation with domain interpretation. A chart or statistic is evidence about the observed data and collection process; it is not automatically a causal conclusion.

This module introduces pandas `Series` and `DataFrame` objects, tabular ingestion, schema inspection, missing and duplicate data, selection, aggregation, NumPy arrays, and Matplotlib's object-oriented plotting interface.

<!-- TODO(media): Add an animation of the EDA workflow from raw table through schema validation, quality audit, transformation, aggregation, visualization, and documented findings. Suggested path: ../Assets/Module-12/eda-workflow.mp4 -->

## 2. Learning outcomes

After completing this module, a student should be able to:

1. **Load** a tabular dataset with explicit parsing assumptions.
2. **Inspect** shape, labels, data types, missingness, uniqueness, and representative rows.
3. **Distinguish** storage dtype from a variable's analytical meaning.
4. **Select and filter** rows and columns with `loc`, `iloc`, and Boolean masks.
5. **Apply** documented missing-value and duplicate policies.
6. **Compute** grouped summary statistics with pandas.
7. **Construct** and interpret NumPy arrays using shape, axes, dtype, vectorization, and broadcasting.
8. **Create** labelled plots with Matplotlib's Figure/Axes interface.
9. **Match** a visualization to variable types and analytical questions.
10. **Report** limitations, provenance, transformations, and non-causal boundaries.

## 3. Environment and compatibility

Module examples target this Python 3.10-compatible profile:

```text
Python      3.10+
pandas      2.3.x
NumPy       2.2.x
Matplotlib  3.10.x
```

Install into an isolated environment:

```console
python -m pip install "pandas>=2.3,<3" "numpy>=2.2,<2.3" "matplotlib>=3.10,<3.11"
```

Verify:

```python
import numpy as np
import pandas as pd

print(pd.__version__)
print(np.__version__)

assert tuple(int(part) for part in pd.__version__.split(".")[:2]) >= (2, 3)
assert tuple(int(part) for part in np.__version__.split(".")[:2]) >= (2, 2)
```

Patch versions may differ. Exact table display, inferred dtypes, and chart rendering can vary between compatible releases.

> **Plot verification status:** Matplotlib was not installed in the authoring environment. The plotting snippets follow Matplotlib's documented Figure/Axes interface [5] but remain locally unexecuted until the practical environment is prepared.

## 4. EDA contract

An EDA report should identify:

- data source and retrieval date;
- observational unit represented by one row;
- population and sampling mechanism;
- variable definitions, units, and valid ranges;
- parsing and transformation steps;
- missing-value and duplicate policies;
- descriptive results;
- anomalies requiring domain review;
- limits of inference; and
- code and dependency versions required to reproduce results.

Without an observational-unit definition, duplicate detection and aggregation can be conceptually wrong.

## 5. Tabular data model

In pandas:

- a `DataFrame` is a two-dimensional labelled table whose columns can use different dtypes; and
- a `Series` is a one-dimensional labelled array and commonly represents one DataFrame column [1].

```python
import pandas as pd

students = pd.DataFrame(
    {
        "student_id": ["S001", "S002", "S003"],
        "program": ["CS", "IS", "CS"],
        "score": [82.0, 75.5, 91.0],
    }
)

scores = students["score"]

print(students.shape)
print(type(scores).__name__)

assert students.shape == (3, 3)
assert isinstance(scores, pd.Series)
assert scores.mean() == 82.83333333333333
```

Expected output:

```text
(3, 3)
Series
```

The **index** labels rows; column labels identify variables. Labels and integer positions are different access systems.

## 6. Analytical variable types

Storage dtype does not fully define analytical meaning.

| Analytical type | Examples | Typical operations |
| --- | --- | --- |
| Identifier | Student ID, transaction code | equality, uniqueness, joins |
| Nominal category | Department, region | counts, proportions |
| Ordinal category | Low, medium, high | ordered comparison |
| Discrete numeric | Number of attempts | counts, integer summaries |
| Continuous numeric | Temperature, duration | distributions, numeric summaries |
| Temporal | Timestamp, date | ordering, intervals, resampling |
| Free text | Comment, description | length, tokens, domain parsing |

A numeric-looking identifier should not be averaged. A category encoded as `0` and `1` still requires semantic labels.

## 7. Loading tabular data

pandas supplies `read_*` functions such as `read_csv()` and corresponding `to_*` methods [2].

Self-contained CSV example:

```python
from io import StringIO

import pandas as pd

csv_text = """station,timestamp,temperature_c,humidity_pct
A,2026-08-01 08:00,21.0,50
A,2026-08-01 09:00,21.5,55
B,2026-08-01 08:00,,60
B,2026-08-01 08:00,,60
C,2026-08-01 08:00,35.0,45
"""

readings = pd.read_csv(
    StringIO(csv_text),
    dtype={"station": "string"},
    parse_dates=["timestamp"],
)

assert readings.shape == (5, 4)
assert str(readings["station"].dtype) == "string"
assert pd.api.types.is_datetime64_any_dtype(readings["timestamp"])
```

### 7.1 Ingestion decisions

Specify where relevant:

- delimiter and quoting;
- header row;
- text encoding;
- missing-value markers;
- selected columns;
- expected dtypes;
- date parsing;
- decimal and thousands separators;
- invalid-row policy; and
- chunking for large input.

Type inference is a convenience, not a substitute for schema validation.

## 8. First inspection

Immediately inspect:

```python
assert readings.shape == (5, 4)
assert readings.columns.tolist() == [
    "station",
    "timestamp",
    "temperature_c",
    "humidity_pct",
]

preview = readings.head(3)
missing = readings.isna().sum()
duplicates = readings.duplicated().sum()

print(missing.to_dict())
print(duplicates)

assert missing.to_dict() == {
    "station": 0,
    "timestamp": 0,
    "temperature_c": 2,
    "humidity_pct": 0,
}
assert duplicates == 1
```

Expected output:

```text
{'station': 0, 'timestamp': 0, 'temperature_c': 2, 'humidity_pct': 0}
1
```

Inspection checklist:

1. `shape`: row and column count;
2. `columns`: expected labels;
3. `head()` and `tail()`: parsing symptoms;
4. `dtypes`: storage interpretation;
5. `info()`: non-null counts and memory summary;
6. `isna().sum()`: missing counts;
7. `duplicated().sum()`: exact duplicates;
8. `nunique()`: cardinality;
9. `describe()`: numeric or categorical summaries; and
10. domain constraints: valid ranges and combinations.

Do not print an entire large table as a substitute for structured checks.

<!-- TODO(media): Add an annotated DataFrame visual explaining index, columns, dtype, shape, missing cells, and duplicate rows. Suggested path: ../Assets/Module-12/dataframe-anatomy.png -->

## 9. Missing data

pandas uses different missing sentinels according to dtype. Use `isna()` or `notna()` rather than equality comparisons [3].

Missingness policy is a domain decision:

- retain and report;
- remove affected rows or columns;
- impute from a documented rule;
- use a model capable of handling missingness;
- recover from an authoritative source; or
- create an explicit “unknown” category when semantically valid.

### 9.1 Imputation example

```python
temperature_median = readings["temperature_c"].median()

cleaned = readings.drop_duplicates().copy()
cleaned["temperature_c"] = cleaned["temperature_c"].fillna(
    temperature_median
)

print(cleaned.shape)
print(cleaned["temperature_c"].isna().sum())

assert cleaned.shape == (4, 4)
assert cleaned["temperature_c"].isna().sum() == 0
assert temperature_median == 21.5
```

Expected output:

```text
(4, 4)
0
```

Median imputation changes the distribution and reduces observed variability. It is used here as a mechanical example, not a universal recommendation. Record which rows were imputed if traceability matters.

## 10. Duplicate policy

`duplicated()` detects exact or subset-based repeated rows. A repeated row is not necessarily erroneous:

- several events can legitimately share values;
- repeated measurements may be distinct observations;
- a one-to-many table naturally repeats entity identifiers; and
- exact duplicates can result from ingestion duplication.

Define a candidate key from the observational unit:

```python
key_columns = ["station", "timestamp"]
duplicate_keys = readings.duplicated(subset=key_columns, keep=False)

flagged = readings.loc[duplicate_keys, key_columns]

assert len(flagged) == 2
```

Investigate before deletion. `drop_duplicates()` encodes a retention policy through `keep` and selected columns.

## 11. Row and column selection

### 11.1 Label-based `loc`

`df.loc[row_selector, column_selector]` uses labels and Boolean masks.

### 11.2 Position-based `iloc`

`df.iloc[row_positions, column_positions]` uses zero-based integer positions.

```python
hot = cleaned.loc[
    cleaned["temperature_c"] >= 25,
    ["station", "temperature_c"],
]

first_two_rows = cleaned.iloc[:2, :]

print(hot["station"].tolist())

assert hot["station"].tolist() == ["C"]
assert first_two_rows.shape == (2, 4)
```

Expected output:

```text
['C']
```

Parenthesize combined Boolean conditions:

```python
selected = cleaned.loc[
    (cleaned["humidity_pct"] >= 50)
    & (cleaned["temperature_c"] < 30)
]

assert len(selected) == 3
```

Use `&`, `|`, and `~` for element-wise pandas Boolean expressions, not scalar `and`, `or`, and `not`.

## 12. Derived columns

Vectorized column operations express data-parallel transformations:

```python
cleaned = cleaned.assign(
    temperature_f=cleaned["temperature_c"] * 9 / 5 + 32,
    humidity_fraction=cleaned["humidity_pct"] / 100,
)

assert cleaned["temperature_f"].round(1).tolist() == [
    69.8,
    70.7,
    70.7,
    95.0,
]
assert cleaned["humidity_fraction"].max() == 0.6
```

State units in column names or schema metadata. Derived columns should not overwrite raw measurements unless the transformation contract requires replacement.

## 13. Summary statistics

### 13.1 Univariate summaries

For numeric data, examine:

- count and missing count;
- minimum and maximum;
- mean and median;
- quantiles;
- standard deviation or robust spread;
- impossible values; and
- distribution shape.

The mean is sensitive to extreme values. A median can conceal multimodality. No one statistic characterizes every distribution.

### 13.2 Grouped summaries

`groupby` follows a split–apply–combine model.

```python
station_summary = (
    cleaned.groupby("station", as_index=False)
    .agg(
        observations=("temperature_c", "size"),
        mean_temperature_c=("temperature_c", "mean"),
        mean_humidity_pct=("humidity_pct", "mean"),
    )
    .sort_values("station")
    .reset_index(drop=True)
)

print(station_summary["station"].tolist())

assert station_summary["station"].tolist() == ["A", "B", "C"]
assert station_summary["observations"].tolist() == [2, 1, 1]
```

Expected output:

```text
['A', 'B', 'C']
```

Aggregation changes the observational unit. After grouping by station, each output row represents a station summary, not one sensor reading.

## 14. NumPy arrays

NumPy's central `ndarray` is a homogeneous N-dimensional array. Important attributes include `ndim`, `shape`, `size`, and `dtype` [4].

```python
import numpy as np

matrix = np.array(
    [
        [21.0, 50.0],
        [21.5, 55.0],
        [35.0, 45.0],
    ],
    dtype=np.float64,
)

print(matrix.shape)
print(matrix.ndim)

assert matrix.shape == (3, 2)
assert matrix.ndim == 2
assert matrix.size == 6
assert matrix.dtype == np.float64
```

Expected output:

```text
(3, 2)
2
```

An **axis** identifies a dimension:

- `axis=0` aggregates down rows, producing one result per column;
- `axis=1` aggregates across columns, producing one result per row.

```python
column_means = matrix.mean(axis=0)
row_means = matrix.mean(axis=1)

assert np.allclose(column_means, [25.8333333333, 50.0])
assert np.allclose(row_means, [35.5, 38.25, 40.0])
```

<!-- TODO(media): Add a NumPy axes animation showing a 3×2 array aggregated along axis 0 and axis 1. Suggested path: ../Assets/Module-12/numpy-axes.gif -->

## 15. Vectorization and broadcasting

Vectorization applies array operations without an explicit Python loop. Broadcasting permits compatible shapes to participate in element-wise operations [4].

```python
temperatures = np.array([20.0, 25.0, 30.0])
fahrenheit = temperatures * 9 / 5 + 32

measurements = np.array(
    [
        [20.0, 50.0],
        [25.0, 60.0],
    ]
)
offsets = np.array([1.0, -5.0])
adjusted = measurements + offsets

assert np.allclose(fahrenheit, [68.0, 77.0, 86.0])
assert np.allclose(adjusted, [[21.0, 45.0], [26.0, 55.0]])
```

Shapes are compatible from the trailing dimensions when each compared dimension is equal or one of them is `1`. Incompatible shapes raise `ValueError`.

Vectorization can reduce Python interpreter overhead, but it may allocate large temporary arrays. Measure representative memory and runtime.

## 16. NumPy views and copies

NumPy slicing commonly returns a **view** sharing underlying data, unlike a Python list slice, which creates a new outer list.

```python
values = np.array([10, 20, 30, 40])
view = values[1:3]
view[0] = 99

assert values.tolist() == [10, 99, 30, 40]

independent = values[1:3].copy()
independent[0] = -1

assert values.tolist() == [10, 99, 30, 40]
```

Ownership and aliasing remain essential in numerical code.

## 17. Visualization model

Matplotlib's object-oriented interface uses:

- **Figure:** complete output container;
- **Axes:** plotting region with data coordinates;
- **Artist:** rendered element such as line, text, or bar.

Prefer:

```text
fig, ax = plt.subplots()
ax.plot(...)
```

over implicit global-state plotting in reusable code [5].

### 17.1 Chart selection

| Analytical question | Starting chart |
| --- | --- |
| Distribution of one numeric variable | Histogram, box plot, empirical distribution |
| Counts by category | Bar chart |
| Numeric value over ordered time | Line plot |
| Relationship between two numeric variables | Scatter plot |
| Distribution by category | Side-by-side box or violin plot |
| Matrix of values | Heatmap with interpretable scale |

Chart choice depends on variable semantics, sample size, overlap, and uncertainty.

### 17.2 Complete plot

The following snippet requires the Matplotlib profile from Section 3:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 4))

for station, group in cleaned.groupby("station"):
    ax.scatter(
        group["temperature_c"],
        group["humidity_pct"],
        label=station,
        s=60,
    )

ax.set(
    title="Humidity versus temperature by station",
    xlabel="Temperature (°C)",
    ylabel="Relative humidity (%)",
)
ax.legend(title="Station")
ax.grid(alpha=0.25)
fig.tight_layout()

plt.show()
```

Required plot elements:

- informative title;
- labelled axes with units;
- legend when encodings need explanation;
- readable scales;
- distinguishable markers or lines beyond colour alone; and
- caption or surrounding text stating dataset and transformation.

<!-- TODO(media): Add a narrated plot-construction animation showing Figure, Axes, data marks, labels, legend, scale, and final interpretation. Suggested path: ../Assets/Module-12/matplotlib-anatomy.mp4 -->

## 18. Visualization integrity

Avoid:

- truncated axes that exaggerate differences without disclosure;
- three-dimensional effects that distort magnitude;
- excessive categories or overlapping marks;
- colour-only distinctions inaccessible to some readers;
- unlabelled units;
- dual axes that imply unsupported comparability;
- smoothed lines that hide raw variation; and
- causal language for observational association.

Show uncertainty or sample size when it changes interpretation. Preserve raw or lightly transformed views alongside aggregates when aggregation can conceal variation.

## 19. EDA sequence

Use a repeatable order:

1. **Establish provenance and observational unit.**
2. **Load with explicit parsing assumptions.**
3. **Validate schema and keys.**
4. **Audit missingness, duplicates, ranges, and categories.**
5. **Record cleaning decisions without destroying raw input.**
6. **Calculate univariate summaries.**
7. **Compare groups and relationships.**
8. **Visualize with correct encodings and units.**
9. **Investigate anomalies against source data.**
10. **Report findings, limitations, and reproducibility metadata.**

EDA is iterative: an unexpected chart can trigger a schema check, and a data-quality finding can invalidate earlier summaries.

## 20. Common failure modes

### 20.1 Trusting inferred dtype

Identifiers can be parsed as numbers; dates can remain generic strings.

### 20.2 Comparing missing values with equality

Use `isna()` or `notna()` [3].

### 20.3 Removing duplicates without an observational key

Repeated rows may be legitimate observations.

### 20.4 Chained assignment

Ambiguous chained indexing can target a temporary object. Prefer one `loc` assignment.

### 20.5 Confusing labels and positions

Use `loc` for labels and `iloc` for integer positions.

### 20.6 Aggregating identifiers

Numeric storage does not imply quantitative meaning.

### 20.7 Data leakage

Do not derive cleaning or imputation parameters from evaluation data in a predictive workflow.

### 20.8 Treating correlation as causation

Observed association may reflect confounding, selection, measurement, or chance.

### 20.9 Unreproducible plot

Record source data, transformations, version profile, and plotting code.

## 21. Guided practice

### 21.1 Schema audit

For the `readings` table, write a schema containing variable name, analytical type, storage dtype, unit, missing policy, and valid range.

### 21.2 Missingness decision

Compare dropping, median imputation, and retaining missing temperatures. State how each choice changes the estimand.

### 21.3 Aggregation unit

Explain the observational unit before and after grouping by station.

### 21.4 Chart critique

Review a bar chart with a y-axis starting at 95 for values from 96 to 100. State whether truncation is defensible and what disclosure is required.

## 22. Independent practice

### Exercise 1 — Data quality report

Load a lecturer-provided CSV and report:

- shape and schema;
- candidate key;
- missing counts and proportions;
- duplicate counts;
- numeric ranges;
- category cardinalities; and
- at least three quality findings.

**Deliverable:** Markdown report plus reproducible code.

### Exercise 2 — Cleaning pipeline

Create a function that accepts a DataFrame and returns a cleaned copy.

**Requirements:** no input mutation, explicit duplicate key, documented missing policy, validation assertions, and before/after row counts.

### Exercise 3 — NumPy analysis

Convert selected numeric columns to a NumPy array.

**Deliverable:** shape, dtype, column means, standardized values, and an explanation of `axis`.

### Exercise 4 — Visualization set

Create:

1. one univariate distribution plot;
2. one category comparison;
3. one two-numeric-variable relationship plot.

Every chart must include units, descriptive labels, accessible encodings, and a two-sentence interpretation that avoids causal claims.

### Exercise 5 — EDA technical report

Write a 600–900 word report containing provenance, observational unit, quality decisions, three supported findings, two limitations, and environment versions.

## 23. Knowledge check

1. What does one DataFrame row represent?
2. Why can storage dtype differ from analytical type?
3. What should be checked immediately after `read_csv()`?
4. Why is missing-value handling a domain decision?
5. How do `loc` and `iloc` differ?
6. What does `axis=0` mean for a two-dimensional NumPy aggregation?
7. Why can a NumPy slice mutation affect its source?
8. What does grouped aggregation change?
9. What minimum metadata makes a plot interpretable?
10. Why does EDA not establish causality?

<details>
<summary>Answer key</summary>

1. The observational unit defined by the dataset contract.
2. Storage describes representation; analytical type describes variable meaning and valid operations.
3. Shape, labels, dtypes, representative rows, missingness, duplicates, and domain constraints.
4. The cause and meaning of absence determine whether removal, imputation, retention, or recovery is valid.
5. `loc` selects by labels and Boolean masks; `iloc` selects by integer position.
6. Aggregate down the rows, returning one value per column.
7. NumPy slicing commonly returns a view sharing underlying storage.
8. The observational unit becomes one row per grouping combination and aggregation result.
9. Title or caption, labelled axes, units, scale, encoding explanation, and data context.
10. Association in observed data does not rule out confounding, selection effects, measurement error, or reverse direction.

</details>

## 24. Module synthesis

Defensible EDA:

```text
provenance and observational unit
    -> explicit schema
    -> quality audit
    -> documented transformation
    -> numerical summary
    -> appropriate visualization
    -> qualified interpretation
```

pandas provides labelled tabular operations, NumPy provides homogeneous multidimensional computation, and Matplotlib provides explicit visual composition. Tool output becomes analysis only when assumptions, units, data quality, and inference boundaries are stated.

## References

1. pandas development team. “What Kind of Data Does pandas Handle?” *pandas 2.3.3 Documentation*. Accessed 31 August 2026. https://pandas.pydata.org/pandas-docs/version/2.3/getting_started/intro_tutorials/01_table_oriented.html
2. pandas development team. “How Do I Read and Write Tabular Data?” *pandas 2.3.3 Documentation*. Accessed 31 August 2026. https://pandas.pydata.org/pandas-docs/version/2.3/getting_started/intro_tutorials/02_read_write.html
3. pandas development team. “Working with Missing Data.” *pandas 2.3.3 Documentation*. Accessed 31 August 2026. https://pandas.pydata.org/pandas-docs/version/2.3/user_guide/missing_data.html
4. NumPy developers. “NumPy: The Absolute Basics for Beginners.” *NumPy 2.2 Manual*. Accessed 31 August 2026. https://numpy.org/doc/2.2/user/absolute_beginners.html
5. Matplotlib development team. “Quick Start Guide.” *Matplotlib Documentation*. Accessed 31 August 2026. https://matplotlib.org/stable/users/explain/quick_start.html

---

**Previous module:** Module 11 — Searching Algorithms  
**Next resource:** Practical notebooks (deferred)
