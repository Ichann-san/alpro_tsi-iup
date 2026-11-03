# Week 10: Testing, Debugging, Exceptions, and Assertions

**Course:** Algorithms and Programming

**Program:** TSI International Undergraduate Program

**Repository module:** Module 7

**Environment:** Python 3.10 or later, with no additional packages

**Prerequisites:** Variables, conditions, loops, lists, dictionaries, and functions

**Practical notebook:** [Week 10 practicum](../Practice/Modul_7.ipynb)

## 1. What you will learn

This week focuses on four questions:

| Subject | Question |
| --- | --- |
| Testing | Does the program produce the expected result? |
| Debugging | Why does the program produce an incorrect result? |
| Exceptions | How should the program respond when an operation fails? |
| Assertions | How can a program automatically check an expected condition? |

After this lesson, you should be able to choose simple test cases, fix a small logic error, handle invalid numeric text, raise `ValueError`, and check results with `assert`.

<!-- TODO(media): Add an animation showing input, expected output, observed failure, correction, and a passing test. Suggested path: ../Assets/Module-7/testing-debugging-cycle.mp4 -->

## 2. Testing: compare actual and expected results

A test case contains input and an expected result. Calculate the expected result independently before running the program.

Example requirement: production meets its target when actual output is greater than or equal to the target.

```python
def meets_target(actual, target):
    return actual >= target


print(meets_target(120, 100))
print(meets_target(99, 100))
print(meets_target(100, 100))
```

Expected output:

```text
True
False
True
```

Choose cases that exercise different decisions:

| Case | Input: actual, target | Expected |
| --- | --- | --- |
| Above target | `120, 100` | `True` |
| Just below target | `99, 100` | `False` |
| Exactly at target | `100, 100` | `True` |
| Zero output | `0, 100` | `False` |

The equality case detects the difference between `>` and `>=`. One successful case does not prove that a function works for every input.

## 3. Assertions: automate a check

An assertion checks a condition:

```text
assert condition, "message shown if the condition is false"
```

A true condition allows execution to continue. A false condition raises `AssertionError` [2].

Replace repeated manual inspection with checks:

```python
assert meets_target(120, 100) is True
assert meets_target(99, 100) is False
assert meets_target(100, 100) is True, "Output equal to target must pass."
assert meets_target(0, 100) is False

print("All target checks passed.")
```

Expected output:

```text
All target checks passed.
```

When an assertion fails, read its message and inspect the function and test expectation. Correct the cause before running later checks.

Use assertions for developer checks and test expectations. Required input validation should use an explicit condition and `raise`: Python can disable assertions when started with the `-O` option [2].

## 4. Recognizing errors

| Category | Example | Observation |
| --- | --- | --- |
| Syntax error | Missing `:` after an `if` condition | Python cannot parse the code |
| Runtime exception | `int("many")` | Execution raises an exception |
| Logic error | Using `>` when the requirement says `>=` | Code runs but returns the wrong result |

For a runtime failure, read the last line of the traceback first. It identifies the exception type and message. Then inspect the referenced line in your code [1].

Illustrative traceback:

```text
Traceback (most recent call last):
  File "example.py", line 1, in <module>
    quantity = int("many")
ValueError: invalid literal for int() with base 10: 'many'
```

The failing operation is numeric conversion. The actual input is text that does not represent an integer.

## 5. Debugging: reproduce, inspect, correct, retest

Use this sequence:

1. Find a small input that reproduces the problem.
2. Write down the expected result.
3. Inspect relevant variables with `print()`.
4. Correct the statement that causes the mismatch.
5. Run the original test and additional cases.

This function contains a deliberate logic error:

```python
def total_output_buggy(values):
    total = 0

    for index in range(len(values) - 1):
        print(f"index={index}, value={values[index]}")
        total += values[index]

    return total


observed = total_output_buggy([10, 8, 12])
print(f"Observed: {observed}; expected: 30")
```

Expected output from the buggy example:

```text
index=0, value=10
index=1, value=8
Observed: 18; expected: 30
```

The loop never visits the final element. A direct loop over the values removes the incorrect index boundary:

```python
def total_output(values):
    total = 0

    for value in values:
        total += value

    return total


assert total_output([10, 8, 12]) == 30
assert total_output([7]) == 7
assert total_output([]) == 0
```

Keep these checks after the correction. A retained check for a previous bug is a **regression test**.

<!-- TODO(media): Add a walkthrough highlighting the skipped final element, print-based inspection, and the corrected loop. Suggested path: ../Assets/Module-7/skipped-element-debugging.gif -->

## 6. Exceptions: handle an expected failure

An exception interrupts normal execution. A matching `except` block can handle it [1].

Common examples:

| Exception | Example cause |
| --- | --- |
| `ValueError` | `int("many")` |
| `ZeroDivisionError` | `10 / 0` |
| `IndexError` | Reading position 3 from a three-item list |
| `KeyError` | Reading a missing dictionary key |
| `TypeError` | Adding a string and an integer |

Start with one risky operation and one specific handler:

```python
raw_quantity = "many"

try:
    quantity = int(raw_quantity)
    print(f"Recorded: {quantity}")
except ValueError:
    print("Quantity must be an integer.")
```

Expected output:

```text
Quantity must be an integer.
```

If conversion succeeds, the handler is skipped. If conversion raises `ValueError`, the remaining statements inside `try` are skipped and the handler runs.

Catch an exception you expect and can respond to. An empty handler or a broad `except:` can hide a programming mistake.

## 7. Raising an exception for an invalid value

Conversion alone does not check every rule. For example, `int("-3")` succeeds, but a production quantity must not be negative.

Use `raise` to reject an invalid value:

```python
def parse_quantity(text):
    """Return a non-negative integer or raise ValueError."""
    quantity = int(text)

    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")

    return quantity


assert parse_quantity("12") == 12
assert parse_quantity(" 0 ") == 0

try:
    parse_quantity("-3")
except ValueError as error:
    print(error)
```

Expected output:

```text
Quantity cannot be negative.
```

The function raises `ValueError` for invalid numeric text or a negative integer. The caller decides how to respond.

To test an expected exception, record whether the handler runs:

```python
error_detected = False

try:
    parse_quantity("many")
except ValueError:
    error_detected = True

assert error_detected, "Invalid quantity text must raise ValueError."
```

## 8. Study case: reading production quantities

A daily log contains text values. Accept non-negative integer quantities, skip invalid records, and calculate the total.

Use `parse_quantity` from Section 7:

```python
raw_quantities = ["12", "8", "many", "-3", "0"]
accepted_quantities = []
rejected_count = 0

for text in raw_quantities:
    try:
        quantity = parse_quantity(text)
    except ValueError:
        rejected_count += 1
        continue

    accepted_quantities.append(quantity)

total_units = sum(accepted_quantities)

assert accepted_quantities == [12, 8, 0]
assert rejected_count == 2
assert total_units == 20

print(f"Total units: {total_units}")
print(f"Rejected records: {rejected_count}")
```

Expected output:

```text
Total units: 20
Rejected records: 2
```

The exception handler makes the invalid-record policy explicit. The assertions check whether the result follows that policy.

<!-- TODO(media): Add a flow animation of five quantity records, showing accepted values, rejected values, and the running total. Suggested path: ../Assets/Module-7/production-log-validation.mp4 -->

## 9. Practicum

Open [Modul_7.ipynb](../Practice/Modul_7.ipynb) and complete:

1. tests for a target-checking function;
2. a correction to a loop that skips the last item;
3. quantity validation with `raise ValueError`;
4. a Daily Production Checker that handles invalid records and reports totals.

Replace the marked starter code and keep the validation cells unchanged. Complete solutions are maintained separately for the instructor.

## 10. Knowledge check

Answer in your own words:

1. How do testing and debugging differ?
2. Why should a target test include a value exactly equal to the target?
3. What happens when an assertion condition is false?
4. Why does `int("-3")` need a separate production-quantity check?
5. Which exception handles `int("many")`?
6. Why is `raise ValueError` suitable for required input validation?
7. Which tests would reveal a loop that skips the last item?

## References

1. Python Software Foundation. "Errors and Exceptions." *The Python Tutorial*. Accessed 3 November 2026. https://docs.python.org/3.10/tutorial/errors.html
2. Python Software Foundation. "The assert statement." *Python Language Reference*. Accessed 3 November 2026. https://docs.python.org/3.10/reference/simple_stmts.html#the-assert-statement

---

**Previous module:** [Module 6: Dictionaries and Recursion](Modul-6.md)

**Next module:** [Module 8: Object-Oriented Programming](Modul-8.md)
