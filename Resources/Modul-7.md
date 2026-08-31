# Module 7 — Testing, Debugging, and Exceptions

> **Course:** Algorithms and Programming  
> **Programming language:** Python  
> **Supported runtime:** Python 3.10 or later  
> **Resource type:** Technical learning module  
> **Practical notebook:** Deferred to `../Practice/Modul_7.ipynb`  
> **Estimated study time:** 4 hours

## 1. Module scope

Testing supplies evidence that software satisfies specified behaviour for selected cases. Debugging localizes and explains an observed failure. Exceptions provide structured propagation of abnormal conditions. These activities are related but not interchangeable:

- a test detects a mismatch;
- debugging identifies its cause; and
- exception handling defines runtime failure semantics.

This module covers test design, assertions, `unittest`, tracebacks, controlled debugging, exception hierarchies, cleanup, propagation, chaining, and custom exceptions.

<!-- TODO(media): Add an animation of the failure lifecycle: test input, assertion failure, traceback inspection, debugger state, root-cause correction, and regression test. Suggested path: ../Assets/Module-7/failure-lifecycle.mp4 -->

## 2. Learning outcomes

After completing this module, a student should be able to:

1. **Derive** test cases from a function contract and input partitions.
2. **Write** deterministic unit tests with setup, action, and assertions.
3. **Distinguish** test assertions from production input validation.
4. **Read** a traceback from exception type backward through call frames.
5. **Use** breakpoints, stepping, state inspection, and call-stack navigation.
6. **Handle** only exceptions that a layer can resolve or translate.
7. **Apply** `try`, `except`, `else`, `finally`, `raise`, and exception chaining.
8. **Design** a small domain-specific exception hierarchy.
9. **Prevent** swallowed failures, overbroad handlers, and cleanup defects.

## 3. Verification vocabulary

| Term | Meaning |
| --- | --- |
| Test case | Inputs, execution conditions, and expected observations |
| Test oracle | Rule that determines the expected result |
| Unit test | Test of a small component in controlled isolation |
| Integration test | Test of interactions between components or systems |
| Regression test | Test retained to prevent recurrence of a defect |
| Fixture | Controlled state established for a test |
| Failure | Observed result does not meet expectation |
| Error | Underlying defect or invalid state that may cause failure |
| Coverage | Structural measurement of code exercised by tests |

Coverage is not proof of correctness. A line can execute without its result being asserted, and unrepresented input classes can remain defective.

## 4. Designing tests from contracts

Given:

```python
def clamp(value, minimum, maximum):
    if minimum > maximum:
        raise ValueError("minimum cannot exceed maximum")
    return min(max(value, minimum), maximum)
```

Derive partitions:

| Partition | Representative input | Expected result |
| --- | --- | --- |
| Below range | `clamp(-2, 0, 10)` | `0` |
| At lower boundary | `clamp(0, 0, 10)` | `0` |
| Interior | `clamp(4, 0, 10)` | `4` |
| At upper boundary | `clamp(10, 0, 10)` | `10` |
| Above range | `clamp(12, 0, 10)` | `10` |
| Invalid bounds | `clamp(4, 10, 0)` | `ValueError` |

### 4.1 Selection techniques

- **Equivalence partitioning:** choose representatives expected to behave alike.
- **Boundary analysis:** test at, immediately below, and immediately above boundaries.
- **Decision-table testing:** cover meaningful combinations of conditions and actions.
- **State-transition testing:** exercise valid and invalid transitions.
- **Invariant testing:** assert properties that must hold across many cases.

### 4.2 Arrange, act, assert

```python
# Arrange
values = [3, 1, 2]

# Act
result = sorted(values)

# Assert
assert result == [1, 2, 3]
assert values == [3, 1, 2]
```

Keep the decisive behaviour visible. A test that reproduces the implementation line by line may repeat the same defect in its oracle.

## 5. Plain assertions

`assert condition, message` raises `AssertionError` when the condition is false.

Use assertions for:

- internal invariants;
- developer assumptions;
- examples and focused checks; and
- impossible states after validated boundaries.

Do not use assertions as the only validation for untrusted input. Python can remove assert statements when optimization is enabled.

```python
def midpoint(low, high):
    assert low <= high, "low must not exceed high"
    return low + (high - low) // 2


assert midpoint(2, 8) == 5
```

For a public API precondition, an explicit exception is normally clearer.

## 6. Unit testing with `unittest`

The standard-library `unittest` framework organizes tests as methods and supplies assertion APIs, fixtures, suites, and runners [1].

```python
import io
import unittest


def normalize_code(value):
    cleaned = value.strip().upper()
    if not cleaned:
        raise ValueError("code cannot be empty")
    return cleaned


class NormalizeCodeTests(unittest.TestCase):
    def test_trims_and_uppercases(self):
        self.assertEqual(normalize_code(" cs204 "), "CS204")

    def test_rejects_whitespace_only(self):
        with self.assertRaises(ValueError):
            normalize_code("   ")


suite = unittest.defaultTestLoader.loadTestsFromTestCase(NormalizeCodeTests)
stream = io.StringIO()
result = unittest.TextTestRunner(stream=stream, verbosity=0).run(suite)

assert result.wasSuccessful(), stream.getvalue()
assert result.testsRun == 2
```

Common assertions:

| Assertion | Contract |
| --- | --- |
| `assertEqual(a, b)` | Values compare equal |
| `assertIs(a, b)` | Same object identity |
| `assertIsNone(value)` | Value is `None` |
| `assertTrue(condition)` | Condition is truthy |
| `assertIn(item, container)` | Membership holds |
| `assertRaises(Error)` | Block raises expected exception |
| `assertAlmostEqual(a, b)` | Numeric values agree to configured precision |

Prefer a specific assertion because its failure report contains more diagnostic information.

### 6.1 Test isolation

A unit test should not depend on:

- execution order;
- prior test mutations;
- uncontrolled clock time or randomness;
- the developer's current directory; or
- external network state unless explicitly an integration test.

Use `setUp()` and `tearDown()` for per-test fixtures only when direct local setup would be repetitive.

## 7. Test quality

### 7.1 Determinism

The same controlled state should produce the same result. Seed pseudo-random generators when randomness itself is not under test.

### 7.2 Focus

One test may contain several assertions about one behaviour. A test covering several unrelated behaviours produces ambiguous failures.

### 7.3 Failure messages

Test names and assertion diagnostics should identify the violated contract, not generic labels such as `test_1`.

### 7.4 Negative paths

Test invalid types, empty values, missing keys, and violated preconditions that the contract explicitly addresses.

### 7.5 Regression value

When a defect is found:

1. reproduce it with the smallest realistic input;
2. convert that reproduction into a failing test;
3. correct the narrow responsible layer; and
4. retain the test.

## 8. Exception model

An exception is an object representing abnormal control flow. Raising an exception stops ordinary execution of the current suite and searches outward for a compatible handler [2].

```python
def parse_positive_integer(text):
    value = int(text)
    if value <= 0:
        raise ValueError("value must be positive")
    return value


assert parse_positive_integer("12") == 12

for invalid in ("0", "-2", "abc"):
    try:
        parse_positive_integer(invalid)
    except ValueError:
        pass
    else:
        raise AssertionError(f"expected ValueError for {invalid!r}")
```

`int("abc")` and the explicit domain check both produce `ValueError`, but for different reasons. A public contract may translate lower-level parsing details into a domain exception.

## 9. `try` statement structure

```text
try:
    risky_operation()
except SpecificError:
    recover()
else:
    use_success_result()
finally:
    release_resource()
```

This is schematic and intentionally tagged as text rather than executable code.

### 9.1 `except`

Runs when a compatible exception escapes the `try` suite.

### 9.2 `else`

Runs only when the `try` suite completes without exception. Put success-path work here so exceptions from that work are not accidentally caught by handlers intended for the risky operation [2].

### 9.3 `finally`

Runs whether execution succeeds, raises, returns, or breaks. It is appropriate for mandatory cleanup. A context manager is usually clearer for resources that support `with`.

```python
events = []

try:
    events.append("try")
    value = int("42")
except ValueError:
    events.append("except")
else:
    events.append(f"else:{value}")
finally:
    events.append("finally")

print(events)
assert events == ["try", "else:42", "finally"]
```

<!-- TODO(media): Add a control-flow animation for try/except/else/finally across success and failure paths. Suggested path: ../Assets/Module-7/exception-flow.gif -->

## 10. Catch at the responsible boundary

Catch an exception only when the current layer can:

- recover with a valid alternative;
- add meaningful context;
- translate it into a domain-level failure;
- retry under a defined policy; or
- perform logging before re-raising.

Do not catch an exception merely to continue with invalid state.

Narrow the `try` suite and catch specific types:

```python
def ratio_from_text(numerator_text, denominator_text):
    try:
        numerator = float(numerator_text)
        denominator = float(denominator_text)
    except ValueError as error:
        raise ValueError("inputs must be numeric") from error

    if denominator == 0:
        raise ZeroDivisionError("denominator cannot be zero")

    return numerator / denominator


assert ratio_from_text("6", "3") == 2.0
```

Avoid `except Exception: pass`. It suppresses evidence, may leave partial state, and prevents upstream policy from running.

## 11. Raising and chaining

`raise` creates or re-raises an exception [2].

Explicit chaining:

```python
class ConfigurationError(Exception):
    """Raised when application configuration is invalid."""


def read_port(configuration):
    try:
        raw_port = configuration["port"]
    except KeyError as error:
        raise ConfigurationError("missing required setting: port") from error

    try:
        port = int(raw_port)
    except (TypeError, ValueError) as error:
        raise ConfigurationError("port must be an integer") from error

    if not 1 <= port <= 65535:
        raise ConfigurationError("port must be between 1 and 65535")
    return port


assert read_port({"port": "8080"}) == 8080

try:
    read_port({})
except ConfigurationError as error:
    assert isinstance(error.__cause__, KeyError)
```

`raise NewError(...) from original` preserves causal evidence. Use `from None` only when suppressing the original context is an intentional interface decision.

## 12. Custom exception hierarchies

Custom exceptions make domain failures catchable without parsing message text.

```python
class EnrollmentError(Exception):
    """Base class for enrollment failures."""


class CapacityExceededError(EnrollmentError):
    """Raised when a course has no available capacity."""


class PrerequisiteError(EnrollmentError):
    """Raised when required study has not been completed."""


def enroll(*, seats_remaining, prerequisite_met):
    if seats_remaining <= 0:
        raise CapacityExceededError("course is full")
    if not prerequisite_met:
        raise PrerequisiteError("prerequisite not satisfied")
    return "enrolled"


assert enroll(seats_remaining=1, prerequisite_met=True) == "enrolled"

try:
    enroll(seats_remaining=0, prerequisite_met=True)
except EnrollmentError as error:
    assert isinstance(error, CapacityExceededError)
```

Inherit application exceptions from `Exception`, not `BaseException`. The latter also covers interpreter-exit signals such as `KeyboardInterrupt` and `SystemExit`.

## 13. Traceback analysis

A traceback records the stack of active calls associated with an exception [3].

Read it in two directions:

1. **Bottom line:** exception type and message.
2. **Frames from bottom upward:** immediate failing operation, caller state, and propagation path.

Diagnostic questions:

- Which expression raised?
- Which actual values reached that expression?
- Which earlier assumption allowed the invalid state?
- Is the observed frame the root cause or only the detection point?

`traceback` utilities can format or inspect traceback information programmatically [3]. Do not expose full internal tracebacks to untrusted end users; they may reveal paths, configuration, or implementation details.

## 14. Systematic debugging

Use an evidence loop:

```text
reproduce
    -> minimize
    -> observe
    -> form one falsifiable hypothesis
    -> run a discriminating check
    -> correct cause
    -> run regression tests
```

### 14.1 Minimize

Remove irrelevant input and dependencies until the failure remains in the smallest useful case.

### 14.2 Observe state

Inspect values, types, identities, lengths, branch conditions, and call paths. Prefer targeted observations to large unstructured logs.

### 14.3 Change one variable

A debugging experiment should separate competing hypotheses. Multiple simultaneous code changes destroy causal evidence.

### 14.4 Verify the correction

Run:

- the new regression test;
- nearby unit tests;
- invalid-input tests; and
- an appropriate broader gate.

## 15. Debugging with `pdb`

Python's debugger supports breakpoints, stepping, stack inspection, and expression evaluation [4].

Start at a location:

```text
breakpoint()
```

Or run a script:

```console
python -m pdb program.py
```

Core commands:

| Command | Action |
| --- | --- |
| `l` | List source |
| `n` | Execute next line in current frame |
| `s` | Step into a call |
| `r` | Continue until current function returns |
| `c` | Continue execution |
| `p expression` | Evaluate and display expression |
| `pp expression` | Pretty-print expression |
| `w` | Show stack trace |
| `u` / `d` | Move up or down the stack |
| `b location` | Set breakpoint |
| `q` | Quit debugger |

Do not leave unconditional `breakpoint()` calls in submitted production paths.

<!-- TODO(media): Add a terminal recording of pdb reproducing an off-by-one error, moving through frames, inspecting values, and confirming the corrected state. Suggested path: ../Assets/Module-7/pdb-session.mp4 -->

## 16. Resource cleanup

Use context managers for files and other resources:

```python
from io import StringIO

buffer = StringIO("alpha\nbeta\n")

with buffer as stream:
    lines = [line.strip() for line in stream]

assert lines == ["alpha", "beta"]
assert buffer.closed
```

`with` expresses acquisition and release as one structured region. `finally` remains appropriate when no suitable context manager exists or several cleanup actions must be coordinated.

## 17. Common failure modes

### 17.1 Tests without an oracle

Executing code and observing no crash is not enough when a result contract exists.

### 17.2 Testing implementation details

Tests coupled to private intermediate steps fail during safe refactoring. Assert externally meaningful behaviour unless an internal invariant itself is the target.

### 17.3 Floating-point exact equality

Use tolerance-aware comparison when rounding is part of the numeric model.

### 17.4 Broad exception handling

Catch the narrow types a layer can resolve. Unexpected exceptions should remain visible.

### 17.5 Empty handler

`except ...: pass` destroys evidence and often permits corrupt continuation.

### 17.6 Oversized `try` suite

Unrelated operations can raise the same exception type and be misclassified.

### 17.7 Returning from `finally`

A `return` in `finally` can suppress an active exception or earlier return. Avoid it.

### 17.8 Debugging by random edits

Without a hypothesis and discriminating observation, a disappearing symptom does not prove the cause is fixed.

## 18. Guided practice

### 18.1 Test matrix

Produce partitions and boundary tests for:

```python
def valid_percentage(value):
    return 0 <= value <= 100
```

### 18.2 Traceback reading

Create a three-function call chain whose final function indexes an empty list. Identify detection point, propagation path, and correct validation boundary.

### 18.3 Handler audit

Rewrite:

```text
try:
    result = complex_operation()
except Exception:
    result = None
```

State the recoverable exception, fallback semantics, and logging or propagation policy.

## 19. Independent practice

### Exercise 1 — Contract-based unit tests

Write `unittest` cases for a median function.

**Required partitions:** odd length, even length, one item, duplicates, negative values, and empty-input exception.

### Exercise 2 — Domain translation

Implement `parse_student_id(text)` and a `StudentIdError`.

**Requirements:** preserve the original `ValueError` as `__cause__` when numeric conversion fails.

### Exercise 3 — Debugging report

Diagnose an off-by-one defect using:

1. minimal reproduction;
2. observed state;
3. ranked hypothesis;
4. debugger or trace evidence;
5. correction; and
6. regression test.

### Exercise 4 — Cleanup proof

Read data from a file-like object with `with`. Cause a deliberate parsing exception and prove the resource is closed afterward.

## 20. Knowledge check

1. How do testing and debugging differ?
2. What is a test oracle?
3. Why is code coverage not proof of correctness?
4. When should assertions not be used as the only validation?
5. What is the purpose of `else` on a `try` statement?
6. When should an exception be caught?
7. What does explicit exception chaining preserve?
8. Why should the smallest failing example be retained as a regression test?

<details>
<summary>Answer key</summary>

1. Testing detects contract mismatches for selected cases; debugging finds the cause of an observed mismatch.
2. A rule or source that determines the expected result.
3. Execution does not prove meaningful output was asserted or all input classes were represented.
4. For external or untrusted input and any requirement that must remain active under optimized execution.
5. It isolates success-path work from the code whose specific exceptions are handled.
6. When the current layer can recover, translate, enrich, retry, or perform necessary reporting before re-raising.
7. The causal relationship and original traceback.
8. It supplies direct evidence that the correction remains effective.

</details>

## 21. Module synthesis

Quality loop:

```text
contract
    -> representative and boundary tests
    -> observed failure
    -> traceback and state evidence
    -> root-cause correction
    -> regression verification
```

Exceptions are part of interface design. Handle them at the layer that owns recovery policy, preserve causal evidence, and keep cleanup independent from success.

## References

1. Python Software Foundation. “`unittest` — Unit Testing Framework.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/unittest.html
2. Python Software Foundation. “Errors and Exceptions.” *The Python Tutorial*. Accessed 31 August 2026. https://docs.python.org/3/tutorial/errors.html
3. Python Software Foundation. “`traceback` — Print or Retrieve a Stack Traceback.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/traceback.html
4. Python Software Foundation. “`pdb` — The Python Debugger.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/pdb.html

---

**Previous module:** Module 6 — Recursion and Dictionaries  
**Next module:** Module 8 — Object-Oriented Programming
