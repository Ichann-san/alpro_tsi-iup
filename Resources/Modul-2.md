# Module 2 — Branching and Iteration

> **Course:** Algorithms and Programming  
> **Programming language:** Python  
> **Supported runtime:** Python 3.10 or later  
> **Resource type:** Technical learning module  
> **Practical notebook:** Deferred to `../Practice/Modul_1-3.ipynb`  
> **Estimated study time:** 3–4 hours

## 1. Module scope

Control flow determines which statements execute, how often they execute, and when execution leaves a region of code. This module covers Boolean evaluation, conditional branching, pattern matching, definite and condition-controlled iteration, loop invariants, termination, and control-transfer statements.

The objective is not only to write syntactically valid loops. A correct control-flow design must make branch coverage, state transitions, boundary conditions, and termination arguments explicit.

<!-- TODO(media): Add an animation of a program counter moving through sequential, conditional, and repeated control-flow paths. Include captions and descriptive alt text. Suggested path: ../Assets/Module-2/control-flow-overview.mp4 -->

## 2. Learning outcomes

After completing this module, a student should be able to:

1. **Evaluate** Boolean expressions using precedence, short-circuiting, and Python truth-value rules.
2. **Construct** mutually exclusive and non-exclusive conditional branches.
3. **Trace** `for` and `while` loops by recording state before and after each iteration.
4. **Formulate** a loop invariant and a termination argument for a simple iterative algorithm.
5. **Use** `range()`, `enumerate()`, and `zip()` according to their contracts.
6. **Apply** `break`, `continue`, and loop `else` without changing intended behaviour.
7. **Diagnose** off-by-one errors, unreachable branches, non-termination, and unsafe collection mutation.

## 3. Prerequisites and environment

Required knowledge:

- Python variables, expressions, and basic container operations;
- the distinction between a value and its type; and
- the data-structure terminology introduced in Module 1.

All examples use the Python standard library and were designed for Python 3.10+.

## 4. Control-flow model

At the statement level, execution normally proceeds in source order. A control-flow statement changes that order.

| Construct | Decision basis | Possible effect |
| --- | --- | --- |
| `if` / `elif` / `else` | Truth value of expressions | Select one branch |
| `match` / `case` | Structural pattern match | Select first matching case |
| `for` | Items produced by an iterable | Repeat once per item |
| `while` | Repeated truth-value test | Repeat while condition is true |
| `break` | Explicit transfer | Exit innermost loop |
| `continue` | Explicit transfer | Start next iteration |
| `return` | Function result | Exit current function |
| Exception | Exceptional transfer | Search for a matching handler |

An algorithm's **control-flow graph** represents statements or basic blocks as nodes and possible transfers as directed edges. Branch coverage asks whether tests exercise each decision outcome; path coverage is stronger and may be infeasible when loops create many possible paths.

## 5. Boolean evaluation

### 5.1 Truth values

Python permits any object in a Boolean context. The following values are false:

- `False` and `None`;
- numeric zero values;
- empty strings and containers; and
- instances whose type defines `__bool__()` as false or `__len__()` as zero.

Other objects are normally true [2]. Use explicit comparisons when distinct states must remain distinguishable. For example, `if result:` treats `0`, `""`, `[]`, and `None` alike.

```python
values = [0, 1, "", "data", [], [0], None]
truth_table = [bool(value) for value in values]

print(truth_table)
assert truth_table == [False, True, False, True, False, True, False]
```

Expected output:

```text
[False, True, False, True, False, True, False]
```

### 5.2 Comparisons

Comparison operators include `<`, `<=`, `>`, `>=`, `==`, `!=`, `is`, `is not`, `in`, and `not in`. Equality compares values; `is` compares identity. Use `is None` and `is not None` for the singleton `None`.

Python supports comparison chaining:

```python
temperature = 24

acceptable = 18 <= temperature <= 27
equivalent = 18 <= temperature and temperature <= 27

print(acceptable)
assert acceptable is True
assert acceptable == equivalent
```

Expected output:

```text
True
```

In a chain, the middle expression is evaluated once [3]. Chaining communicates interval membership more directly than repeating the operand.

### 5.3 Boolean operators and short-circuiting

Precedence from higher to lower is:

```text
comparisons
not
and
or
```

`and` returns its first false operand, or its last operand when all are true. `or` returns its first true operand, or its last operand when all are false [2]. They do not necessarily return `bool`.

```python
label = ""
display_label = label or "untitled"

records = ["A12"]
first_record = records and records[0]

print(display_label)
print(first_record)

assert display_label == "untitled"
assert first_record == "A12"
```

Expected output:

```text
untitled
A12
```

Short-circuiting prevents evaluation of later operands once the result is determined. It can guard an operation:

```python
denominator = 0
safe = denominator != 0 and 100 / denominator > 2

print(safe)
assert safe is False
```

The division is not evaluated. Do not hide significant side effects inside a Boolean expression; control flow becomes harder to audit.

## 6. Conditional branching

### 6.1 Mutually exclusive selection

An `if`–`elif`–`else` chain selects at most one suite. Conditions are tested from top to bottom, and evaluation stops at the first true condition [1].

```python
score = 78

if score >= 85:
    grade = "A"
elif score >= 70:
    grade = "B"
elif score >= 55:
    grade = "C"
else:
    grade = "D"

print(grade)
assert grade == "B"
```

Order is part of the algorithm. If `score >= 55` appeared first, every score of 55 or more would enter that branch and higher classifications would be unreachable.

### 6.2 Independent conditions

Separate `if` statements may execute multiple suites:

```python
value = 30
properties = []

if value % 2 == 0:
    properties.append("even")
if value % 3 == 0:
    properties.append("divisible by 3")
if value % 5 == 0:
    properties.append("divisible by 5")

print(properties)
assert properties == ["even", "divisible by 3", "divisible by 5"]
```

Choose a chain when outcomes exclude each other. Choose independent conditions when multiple properties may hold simultaneously.

### 6.3 Guard conditions

A **guard condition** rejects invalid or exceptional states before the main operation. Inside a function, an early `return` can keep the valid path shallow. Before Module 4 introduces full function design, apply the same principle by testing prerequisites before the operation they protect.

### 6.4 Conditional expressions

Python's conditional expression has the form:

```text
result_if_true if condition else result_if_false
```

Use it for one small value selection, not for multi-step branching:

```python
quantity = 0
status = "available" if quantity > 0 else "out of stock"
assert status == "out of stock"
```

## 7. Structural pattern matching

`match` compares a subject against `case` patterns. Only the first matching case executes [1]. Pattern matching is appropriate when the structure of the data determines the operation.

```python
command = ("move", 3, -1)

match command:
    case ("move", x, y):
        result = f"move by ({x}, {y})"
    case ("stop",):
        result = "stop"
    case _:
        result = "invalid command"

print(result)
assert result == "move by (3, -1)"
```

Technical distinctions:

- a literal pattern tests a value;
- a standalone name captures a value;
- `_` is a wildcard and does not bind a name;
- a guard such as `case value if value > 0:` adds a Boolean condition; and
- case order matters because matching stops after the first success.

A broad capture pattern placed early can make later cases unreachable.

<!-- TODO(media): Add an animation comparing an if–elif decision chain with first-match structural pattern matching. Show capture names and guard evaluation. Suggested path: ../Assets/Module-2/branch-selection.gif -->

## 8. Definite iteration with `for`

Python's `for` statement requests items from an iterable and assigns each item to the loop target [1]. It is item-driven rather than inherently counter-driven.

```python
readings = [4, 7, 2, 9]
total = 0

for reading in readings:
    total += reading

print(total)
assert total == 22
```

### 8.1 State trace

| Iteration | `reading` | `total` before | `total` after |
| ---: | ---: | ---: | ---: |
| 1 | 4 | 0 | 4 |
| 2 | 7 | 4 | 11 |
| 3 | 2 | 11 | 13 |
| 4 | 9 | 13 | 22 |

The trace exposes the accumulation invariant:

> Before each iteration, `total` equals the sum of the items already processed.

### 8.2 `range()`

`range(start, stop, step)` represents an arithmetic progression. `stop` is excluded [1].

```python
print(list(range(2, 9, 2)))
print(list(range(5, 0, -2)))

assert list(range(2, 9, 2)) == [2, 4, 6, 8]
assert list(range(5, 0, -2)) == [5, 3, 1]
```

Expected output:

```text
[2, 4, 6, 8]
[5, 3, 1]
```

A zero step raises `ValueError`. A step whose sign cannot approach the stop produces an empty range.

### 8.3 `enumerate()` and `zip()`

Use `enumerate(iterable, start=0)` when both position and item are required. Use `zip()` for lockstep iteration.

```python
codes = ["AX", "BY", "CZ"]
weights = [2.5, 3.0, 1.5]
rows = []

for position, (code, weight) in enumerate(zip(codes, weights), start=1):
    rows.append((position, code, weight))

print(rows)
assert rows == [(1, "AX", 2.5), (2, "BY", 3.0), (3, "CZ", 1.5)]
```

By default, `zip()` stops at the shortest input. In Python 3.10+, `zip(..., strict=True)` raises `ValueError` when lengths differ, which is useful when unequal lengths indicate corrupt data.

## 9. Condition-controlled iteration with `while`

A `while` loop repeats while its condition remains true. Correctness requires:

1. an initialized state;
2. a condition describing when more work remains;
3. a body that preserves the invariant; and
4. progress toward condition failure.

```python
value = 40
steps = 0

while value > 1:
    value //= 2
    steps += 1

print(value, steps)
assert (value, steps) == (1, 5)
```

### 9.1 Termination argument

For the example:

- variant: non-negative integer `value - 1`;
- each iteration with `value > 1` decreases `value` through floor division by 2; and
- the variant cannot decrease indefinitely below zero.

Therefore the loop terminates for every positive initial integer.

A loop may be intentionally unbounded, such as an event loop, but it still requires a documented external exit mechanism.

<!-- TODO(media): Add a loop-state animation showing initialization, condition test, body, update, invariant, and decreasing variant. Suggested path: ../Assets/Module-2/while-loop-invariant.mp4 -->

## 10. Loop control

### 10.1 `break`

`break` exits the innermost enclosing loop [1].

### 10.2 `continue`

`continue` skips the remainder of the current body and begins the next iteration. Ensure the skipped statements are not required for progress in a `while` loop.

### 10.3 Loop `else`

A loop's `else` suite executes only when the loop finishes without `break` [1].

```python
values = [14, 23, 35, 42]
target = 23

for index, value in enumerate(values):
    if value == target:
        found_at = index
        break
else:
    found_at = -1

print(found_at)
assert found_at == 1
```

Loop `else` represents “no early success or failure occurred,” not “the loop condition was false once.”

## 11. Nested iteration and cost

Nested loops do not automatically imply quadratic time. Cost depends on iteration counts.

```python
pair_count = 0

for left in range(4):
    for right in range(left + 1, 4):
        pair_count += 1

print(pair_count)
assert pair_count == 6
```

The exact count is:

```text
3 + 2 + 1 + 0 = 4(4 - 1) / 2 = 6
```

For general `n`, the count is `n(n - 1)/2`, which is `Θ(n²)`. Module 10 develops formal cost analysis.

## 12. Mutation during iteration

Changing the size or key set of a collection while iterating over it can skip items, duplicate work, or raise an exception. Python's tutorial recommends iterating over a copy or constructing a new collection when modification is required [1].

Preferred transformation:

```python
measurements = [3, -1, 5, -2, 7]
non_negative = []

for value in measurements:
    if value >= 0:
        non_negative.append(value)

assert non_negative == [3, 5, 7]
```

## 13. Common failure modes

### 13.1 Off-by-one boundaries

`range(n)` produces `0` through `n - 1`. State whether an interval is closed, open, or half-open before coding it.

### 13.2 Unreachable branch

Place more specific conditions before broader conditions in an exclusive chain.

### 13.3 Non-terminating `while` loop

Identify a variant that must move toward the stopping condition. Check every path, including `continue` paths, for progress.

### 13.4 Accidental truthiness

Use `value is None` when `None` has a different meaning from zero or an empty container.

### 13.5 Incorrect identity comparison

Use `==` for value comparison. Reserve `is` for identity, especially singleton checks.

### 13.6 Misplaced loop `else`

The `else` belongs to the loop whose indentation matches it. It runs when that loop completes without `break`.

### 13.7 Silent truncation by `zip()`

Use `strict=True` when input lengths are required to match.

## 14. Guided practice

### 14.1 Branch table

For the grade chain in Section 6, evaluate boundary inputs `54`, `55`, `69`, `70`, `84`, and `85`.

**Success criteria:** each boundary maps to exactly one expected grade, and the student identifies which comparison accepts it.

### 14.2 Loop trace

Trace:

```python
value = 11
count = 0

while value > 1:
    if value % 2 == 0:
        value //= 2
    else:
        value -= 1
    count += 1
```

**Deliverable:** table of `value` and `count` before and after every iteration.

### 14.3 Search outcome

Modify the loop-`else` example for an absent target. Explain why `found_at` becomes `-1`.

## 15. Independent practice

### Exercise 1 — Input classification

Write code that classifies an integer as:

- negative;
- zero;
- positive even; or
- positive odd.

**Constraints:** outcomes must be mutually exclusive; use one `if`–`elif`–`else` chain.

**Success criteria:** assertions pass for `-3`, `0`, `8`, and `9`.

### Exercise 2 — Validated accumulation

Given `values = [12, -4, 7, -1, 5]`, sum only non-negative values and count how many were excluded.

**Expected result:** sum `24` and excluded count `2`.

**Constraints:** one loop; no `sum()`.

### Exercise 3 — Terminating digit count

Use a `while` loop to count decimal digits in a non-negative integer.

**Required cases:** `0 -> 1`, `7 -> 1`, `4205 -> 4`.

**Deliverable:** code, state invariant, and termination argument.

### Exercise 4 — Pair generation

For `labels = ["A", "B", "C", "D"]`, produce each unordered pair exactly once.

**Expected count:** `6`.

**Success criteria:** no pair contains the same item twice, and reversed duplicates do not appear.

## 16. Knowledge check

1. Why can `and` or `or` return a non-Boolean object?
2. How does an `if` chain differ from multiple independent `if` statements?
3. What values does `range(2, 8, 2)` produce?
4. What must decrease or otherwise progress to prove `while` termination?
5. When does a loop `else` suite execute?
6. Why can `zip()` hide an input-length defect?
7. What is the difference between `==` and `is`?
8. Does a pair of nested loops always execute `n²` iterations?

<details>
<summary>Answer key</summary>

1. They return one of their operands after short-circuit evaluation; truth is tested, but conversion to `bool` is not automatic.
2. A chain selects at most one branch; independent statements may execute several suites.
3. `2, 4, 6`; the stop value `8` is excluded.
4. A well-founded variant must move toward its lower bound or another proven terminal state.
5. When the loop completes without executing `break`.
6. Default `zip()` stops when its shortest input is exhausted.
7. `==` compares values; `is` compares object identity.
8. No. The exact cost depends on each loop's bounds and whether iterations terminate early.

</details>

## 17. Module synthesis

A defensible iterative algorithm states:

```text
initial state
    -> branch or loop condition
    -> state transition
    -> preserved invariant
    -> termination or explicit transfer
```

Use branching to select valid behaviour and iteration to repeat a state transition. Verify boundaries, control transfers, and progress independently.

## References

1. Python Software Foundation. “More Control Flow Tools.” *The Python Tutorial*. Accessed 31 August 2026. https://docs.python.org/3/tutorial/controlflow.html
2. Python Software Foundation. “Built-in Types: Truth Value Testing and Boolean Operations.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/stdtypes.html#truth-value-testing
3. Python Software Foundation. “Expressions: Comparisons and Boolean Operations.” *Python Language Reference*. Accessed 31 August 2026. https://docs.python.org/3/reference/expressions.html#comparisons

---

**Previous module:** Module 1 — Introduction to Data Structures  
**Next module:** Module 3 — String Manipulation
