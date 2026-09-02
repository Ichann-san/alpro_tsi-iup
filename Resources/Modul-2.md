# Module 2: Basic Branching and Iteration

**Course:** Algorithms and Programming

**Program:** TSI International Undergraduate Program

**Programming language:** Python 3.10 or later

**Prerequisite:** Module 1

**Estimated study time:** 3 to 4 hours

## 1. Module scope

Module 1 introduced statements that execute from top to bottom. This module introduces **control flow**: rules that select which statements execute and how many times they execute.

The core tools are:

- `if`, `elif`, and `else` for decisions;
- `for` for processing items in a collection;
- `while` for repetition controlled by a condition;
- `break` and `continue` for simple loop control.

The examples use familiar Industrial Systems data such as daily production, quality inspection results, and targets.

<!-- TODO(media): Add a beginner animation showing a program moving through sequence, one if-else decision, and one repeated loop. Use the same production-target example throughout. Suggested path: ../Assets/Module-2/control-flow-basics.mp4 -->

## 2. Learning outcomes

After completing this module, a student should be able to:

1. construct Boolean conditions using comparison and logical operators;
2. select one or more actions with `if`, `elif`, and `else`;
3. use indentation to define a branch or loop body;
4. process every item in a list with a `for` loop;
5. generate a known sequence of integers with `range()`;
6. construct a terminating `while` loop;
7. apply counter and accumulator patterns;
8. use `break` for a sentinel and `continue` for an invalid item;
9. trace variable values across several iterations.

## 3. Prerequisite check

Before continuing, confirm that you can:

- assign numeric and string values to variables;
- calculate with `+`, `-`, `*`, and `/`;
- compare values with operators such as `==` and `>=`;
- create a list;
- display variables with an f-string.

Review Module 1 if any operation is unfamiliar.

### 3.1 Suggested study schedule

| Activity | Time |
| --- | ---: |
| Conditions and basic branches | 55 minutes |
| `for` loops and `range()` | 45 minutes |
| `while` loops and tracing | 40 minutes |
| `break`, `continue`, and sentinels | 25 minutes |
| Study case, practice, and knowledge check | 45 minutes |
| **Total** | **210 minutes** |

## 4. Sequential execution

Without a branch or loop, Python executes statements in order:

```python
planned_units = 500
actual_units = 475
difference = actual_units - planned_units

print(f"Planned: {planned_units}")
print(f"Actual: {actual_units}")
print(f"Difference: {difference}")
```

Every line runs once. Control flow changes this fixed path.

## 5. Boolean conditions

A condition is an expression that produces `True` or `False`.

```python
actual_units = 525
target_units = 500

print(actual_units >= target_units)
print(actual_units == target_units)
print(actual_units < target_units)
```

Output:

```text
True
False
False
```

Logical operators combine conditions:

| Operator | Result |
| --- | --- |
| `and` | `True` only when both operands are true |
| `or` | `True` when at least one operand is true |
| `not` | Reverses a Boolean value |

```python
temperature = 72
guard_closed = True

temperature_ok = temperature >= 60 and temperature <= 80
safe_to_run = temperature_ok and guard_closed

assert temperature_ok is True
assert safe_to_run is True
```

For a beginner, explicit comparisons are easier to audit than compact expressions.

## 6. The basic `if` statement

An `if` statement executes its indented body only when its condition is true [1].

```python
actual_units = 525
target_units = 500

if actual_units >= target_units:
    print("Target reached")
```

The colon starts a block. The four spaces before `print()` place that statement inside the branch.

If the condition is false, the body is skipped:

```python
actual_units = 480
target_units = 500

if actual_units >= target_units:
    print("Target reached")

print("Evaluation complete")
```

Output:

```text
Evaluation complete
```

## 7. Two alternatives with `if` and `else`

Use `else` when exactly one of two paths must execute:

```python
actual_units = 480
target_units = 500

if actual_units >= target_units:
    status = "REACHED"
else:
    status = "NOT REACHED"

print(f"Target status: {status}")
assert status == "NOT REACHED"
```

The `else` branch has no condition. It runs only when the corresponding `if` condition is false.

## 8. Several alternatives with `elif`

Use `elif` when one value must be classified into several mutually exclusive categories:

```python
utilization = 87

if utilization >= 90:
    category = "HIGH"
elif utilization >= 70:
    category = "NORMAL"
else:
    category = "LOW"

assert category == "NORMAL"
```

Conditions are checked from top to bottom. The first true branch executes, and the remaining branches are skipped [1].

Order matters. Put the most restrictive upper category first:

```text
if score >= 80:
    grade = "A"
elif score >= 60:
    grade = "B"
else:
    grade = "C"
```

If `score >= 60` appeared first, a score of `90` would incorrectly enter that broader branch.

## 9. Nested decisions

One decision may contain another decision:

```python
machine_active = True
defect_detected = False

if machine_active:
    if defect_detected:
        message = "Stop and inspect"
    else:
        message = "Continue production"
else:
    message = "Machine is inactive"

assert message == "Continue production"
```

Use nesting only when the second condition is meaningful after the first condition succeeds. Deep nesting becomes difficult to trace.

## 10. Repetition with a `for` loop

A `for` loop processes items from a sequence in their existing order [1].

```python
daily_output = [480, 510, 495, 525]

for units in daily_output:
    print(f"Recorded output: {units}")
```

The loop variable `units` receives one list item per iteration:

| Iteration | `units` |
| ---: | ---: |
| 1 | 480 |
| 2 | 510 |
| 3 | 495 |
| 4 | 525 |

The loop ends after the last item.

### 10.1 Counter pattern

A counter records how many times an event occurs:

```python
daily_output = [480, 510, 495, 525]
target = 500
successful_days = 0

for units in daily_output:
    if units >= target:
        successful_days += 1

assert successful_days == 2
```

Counter sequence:

```text
start at 0
    -> condition succeeds
    -> add 1
    -> final count
```

### 10.2 Accumulator pattern

An accumulator combines values across iterations:

```python
daily_output = [480, 510, 495, 525]
total_output = 0

for units in daily_output:
    total_output += units

assert total_output == 2010
```

`sum(daily_output)` is shorter, but the explicit loop exposes how accumulation works.

## 11. Numeric repetition with `range()`

`range(stop)` produces integer values from zero up to, but not including, `stop` [1].

```python
for period in range(4):
    print(period)
```

Output:

```text
0
1
2
3
```

Common forms:

| Expression | Values |
| --- | --- |
| `range(4)` | `0, 1, 2, 3` |
| `range(1, 5)` | `1, 2, 3, 4` |
| `range(2, 11, 2)` | `2, 4, 6, 8, 10` |

Use `range()` when the algorithm needs a controlled numeric sequence:

```python
total = 0

for value in range(1, 6):
    total += value

assert total == 15
```

## 12. Condition-controlled repetition with `while`

A `while` loop repeats while its condition remains true [2]:

```python
count = 1

while count <= 4:
    print(count)
    count += 1
```

Output:

```text
1
2
3
4
```

Trace:

| Condition check | `count` before body | Body runs? | `count` after body |
| ---: | ---: | --- | ---: |
| 1 | 1 | Yes | 2 |
| 2 | 2 | Yes | 3 |
| 3 | 3 | Yes | 4 |
| 4 | 4 | Yes | 5 |
| 5 | 5 | No | 5 |

The update `count += 1` moves the state toward `count > 4`. Without the update, the loop would not terminate.

<!-- TODO(media): Add a frame-by-frame animation of the previous while loop showing condition, output, update, and exit. Suggested path: ../Assets/Module-2/while-loop-trace.gif -->

## 13. Using `break`

`break` exits the nearest loop immediately [1].

A **sentinel** is a special value that indicates the end of useful input. In this example, `-1` is not a production measurement. It stops processing:

```python
measurements = [120, 135, 128, -1, 150]
total = 0

for units in measurements:
    if units == -1:
        break
    total += units

assert total == 383
```

The final value `150` is ignored because it appears after the sentinel.

## 14. Using `continue`

`continue` skips the rest of the current iteration and moves to the next item [1].

```python
measurements = [120, -5, 135, 0, 128]
valid_count = 0

for units in measurements:
    if units < 0:
        continue
    valid_count += 1

assert valid_count == 4
```

Here, negative measurements are invalid and skipped. Zero remains valid because the condition rejects only values below zero.

## 15. Choosing `for` or `while`

Use `for` when the program should process items from a known collection or numeric range.

Use `while` when repetition depends on a changing condition and the number of iterations is not known directly.

| Situation | Suitable loop |
| --- | --- |
| Process every daily output in a list | `for` |
| Print the integers from 1 through 10 | `for` with `range()` |
| Repeat until available stock reaches zero | `while` |
| Repeat until a valid menu choice is entered | `while` |

## 16. Study case: Production Target Tracker

### 16.1 Problem

A supervisor receives daily production values. The value `-1` indicates that no more days should be processed.

For every earlier value:

- reject negative values other than `-1`;
- classify output as `ABOVE TARGET`, `ON TARGET`, or `BELOW TARGET`;
- count processed days;
- count days that reached or exceeded the target;
- calculate total accepted output.

### 16.2 Implementation

```python
daily_output = [480, 500, 525, -4, 510, -1, 600]
daily_target = 500

processed_days = 0
successful_days = 0
total_output = 0

for units in daily_output:
    if units == -1:
        break

    if units < 0:
        print(f"Ignored invalid value: {units}")
        continue

    processed_days += 1
    total_output += units

    if units > daily_target:
        classification = "ABOVE TARGET"
        successful_days += 1
    elif units == daily_target:
        classification = "ON TARGET"
        successful_days += 1
    else:
        classification = "BELOW TARGET"

    print(f"Day {processed_days}: {units} units - {classification}")

print(f"Processed days: {processed_days}")
print(f"Successful days: {successful_days}")
print(f"Total accepted output: {total_output}")

assert processed_days == 4
assert successful_days == 3
assert total_output == 2015
```

Output:

```text
Day 1: 480 units - BELOW TARGET
Day 2: 500 units - ON TARGET
Day 3: 525 units - ABOVE TARGET
Ignored invalid value: -4
Day 4: 510 units - ABOVE TARGET
Processed days: 4
Successful days: 3
Total accepted output: 2015
```

### 16.3 State trace

| Input | Action | Processed | Successful | Total |
| ---: | --- | ---: | ---: | ---: |
| 480 | Below target | 1 | 0 | 480 |
| 500 | On target | 2 | 1 | 980 |
| 525 | Above target | 3 | 2 | 1505 |
| -4 | Continue | 3 | 2 | 1505 |
| 510 | Above target | 4 | 3 | 2015 |
| -1 | Break | 4 | 3 | 2015 |

The trace separates input handling, state changes, and output classification.

## 17. Common beginner errors

### 17.1 Missing a colon

```text
if units >= target
    print("Reached")
```

Add a colon after the condition.

### 17.2 Incorrect indentation

```text
if units >= target:
print("Reached")
```

The branch body must be indented consistently.

### 17.3 Confusing assignment and comparison

```text
if units = target:
```

Use `==` to compare:

```text
if units == target:
```

### 17.4 Wrong branch order

Check a narrow or higher threshold before a broader lower threshold.

### 17.5 Infinite `while` loop

```text
count = 1
while count <= 4:
    print(count)
```

The condition remains true because `count` never changes.

### 17.6 Off-by-one with `range()`

`range(1, 5)` stops before `5`. It produces `1, 2, 3, 4`.

## 18. Guided practice

Complete the missing conditions:

```text
stock = 25
minimum_stock = 20

if __________________________:
    message = "REORDER"
else:
    message = "SUFFICIENT"
```

Expected message for the given values:

```text
SUFFICIENT
```

Then complete this loop:

```text
total = 0

for value in [10, 20, 30]:
    __________________________
```

Expected final value:

```text
60
```

## 19. Independent practice

### Task 1: Quality classification

Given a defect percentage:

- below `2` is `EXCELLENT`;
- from `2` through `5` is `ACCEPTABLE`;
- above `5` is `REVIEW`.

Write a branch that stores the correct classification.

### Task 2: Weekly target count

Given a list of seven production values and one daily target, count how many days reach the target.

### Task 3: Controlled countdown

Use a `while` loop to print values from `5` down to `1`. After the loop, print `START`.

### Task 4: Sentinel processing

Process values from a list until `0` appears. Ignore negative values and add positive values to a total.

## 20. Knowledge check

1. What type must an `if` condition produce?
2. When does `else` execute?
3. Why should a high threshold normally appear before a lower threshold?
4. Which loop is suitable for processing every item in a list?
5. What values does `range(3)` produce?
6. What state change makes `while count < 5` terminate?
7. What does `break` do?
8. What does `continue` do?
9. What is a sentinel?

<details>
<summary>Answer guide</summary>

1. A Boolean result interpreted as `True` or `False`.
2. When the corresponding `if` and `elif` conditions are false.
3. A broader lower threshold could capture values intended for the higher category.
4. A `for` loop.
5. `0, 1, 2`.
6. `count` must change until it is at least `5`.
7. It exits the nearest loop.
8. It skips the rest of the current iteration.
9. A special value that signals the end of useful input or processing.

</details>

## 21. Module synthesis

Basic control flow follows this progression:

```text
condition
    -> branch selection
    -> repeated processing
    -> state update
    -> termination
```

A correct loop needs both useful work and a clear end. Trace the variables that change to diagnose incorrect results or non-termination.

## References

1. Python Software Foundation. "More Control Flow Tools." *Python 3.14.7 Documentation*. Accessed 2 September 2026. https://docs.python.org/3/tutorial/controlflow.html
2. Python Software Foundation. "An Informal Introduction to Python." *Python 3.14.7 Documentation*. Accessed 2 September 2026. https://docs.python.org/3/tutorial/introduction.html

---

**Previous module:** Module 1: Python Fundamentals and Introduction to Data Structures

**Next module:** Module 3: Basic String Manipulation
