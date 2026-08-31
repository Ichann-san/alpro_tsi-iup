# Module 4 — Decomposition, Abstraction, and Functions

> **Course:** Algorithms and Programming  
> **Programming language:** Python  
> **Supported runtime:** Python 3.10 or later  
> **Resource type:** Technical learning module  
> **Practical notebook:** Deferred to `../Practice/Modul_4-6.ipynb`  
> **Estimated study time:** 3–4 hours

## 1. Module scope

Decomposition separates a problem into components with limited responsibilities. Abstraction exposes the behaviour a client needs while suppressing representation details. Functions are Python's primary mechanism for expressing both ideas at the procedural level.

This module treats a function as a contract: accepted inputs, returned output, state effects, failure behaviour, and invariants. Syntax is secondary to interface quality.

<!-- TODO(media): Add an animation transforming a monolithic calculation into a call graph of cohesive functions with explicit inputs and outputs. Suggested path: ../Assets/Module-4/decomposition-call-graph.mp4 -->

## 2. Learning outcomes

After completing this module, a student should be able to:

1. **Decompose** a computational requirement into cohesive function responsibilities.
2. **Specify** function contracts with parameters, return values, preconditions, postconditions, and exceptions.
3. **Implement** positional, keyword, default, positional-only, and keyword-only parameters.
4. **Trace** local, enclosing, global, and built-in name resolution.
5. **Predict** mutation and rebinding effects when arguments reference mutable objects.
6. **Construct** pure transformations and isolate necessary side effects.
7. **Document and annotate** a public function without confusing type hints with runtime validation.
8. **Diagnose** shared mutable defaults, hidden dependencies, mixed abstraction levels, and missing returns.

## 3. Prerequisites

Students should be able to:

- use expressions, branching, and iteration;
- manipulate strings and basic containers; and
- state simple preconditions and invariants.

All examples use the standard library.

## 4. Decomposition criteria

A useful decomposition is based on responsibility and change boundaries.

### 4.1 Cohesion

A function is **cohesive** when its statements serve one defined purpose. “Read data, calculate statistics, format a report, and save a file” contains at least four responsibilities.

### 4.2 Coupling

**Coupling** is dependency between components. Explicit parameters and return values expose coupling. Global state, hidden file access, and mutation of caller-owned objects conceal it.

### 4.3 Information hiding

A client should depend on a stable contract rather than internal steps. If a calculation changes from iteration to a closed-form formula but the inputs and result remain the same, callers should not require modification.

### 4.4 Abstraction level

Statements within a function should operate at a compatible level. A high-level `generate_report()` should delegate byte decoding or numeric validation rather than mix those details with report orchestration.

## 5. Function contracts

A technical contract records:

| Element | Question |
| --- | --- |
| Purpose | What single result or state transition does the function provide? |
| Parameters | What values are accepted, and what does each mean? |
| Preconditions | What must callers establish? |
| Return | What value and type represent success? |
| Postconditions | What becomes true after success? |
| Side effects | What external or caller-visible state may change? |
| Failures | Which exceptions or sentinel values represent failure? |
| Complexity | How does cost grow when relevant? |

Example contract:

```text
mean(values)
Precondition: values is a non-empty sequence of real numbers.
Return: arithmetic mean as a float.
Side effects: none.
Failure: ValueError when values is empty.
```

## 6. Defining and calling functions

`def` creates a function object and binds it to a name [1], [2].

```python
def rectangle_area(width: float, height: float) -> float:
    """Return the area of a rectangle with non-negative dimensions."""
    if width < 0 or height < 0:
        raise ValueError("dimensions must be non-negative")
    return width * height


area = rectangle_area(3.5, 2.0)
print(area)
assert area == 7.0
```

Expected output:

```text
7.0
```

Terms:

- **parameter:** name in the function definition;
- **argument:** expression supplied by the caller;
- **signature:** parameter structure and return annotation;
- **body:** statements executed by a call;
- **return value:** object supplied to the caller by `return`.

Falling off the end of a function returns `None` [1]. Printing and returning are different operations.

## 7. Parameters and arguments

### 7.1 Positional and keyword arguments

```python
def scale(value, factor=1.0):
    return value * factor


assert scale(8, 0.5) == 4.0
assert scale(value=8, factor=0.5) == 4.0
assert scale(8) == 8.0
```

Keyword calls document meaning and reduce mistakes when several adjacent parameters have the same type.

### 7.2 Positional-only and keyword-only parameters

The markers `/` and `*` constrain the call interface [1]:

```python
def clamp(value, /, *, minimum=0, maximum=100):
    if minimum > maximum:
        raise ValueError("minimum cannot exceed maximum")
    return min(max(value, minimum), maximum)


assert clamp(120, maximum=90) == 90
assert clamp(-4, minimum=1) == 1
```

- parameters before `/` are positional-only;
- parameters after `*` are keyword-only; and
- parameters between them may be passed either way.

Keyword-only parameters are useful when several configuration values would be ambiguous by position.

### 7.3 Variable-length arguments

- `*args` collects extra positional arguments into a tuple.
- `**kwargs` collects extra keyword arguments into a dictionary.

Use them when the interface is genuinely variadic, not to avoid designing named parameters.

## 8. Return design

### 8.1 Return values rather than display

```python
def summarize(values):
    return min(values), max(values), sum(values)


minimum, maximum, total = summarize([4, 1, 7])
print(minimum, maximum, total)

assert (minimum, maximum, total) == (1, 7, 12)
```

Returning data allows testing, composition, alternate formatting, and reuse. Output functions may print at the application boundary.

### 8.2 One logical return shape

Avoid returning a number on one branch and a string error message on another. Prefer:

- one stable result type;
- a documented optional result such as `int | None`; or
- an exception for a failed precondition or operation.

### 8.3 Multiple values

`return first, second` returns one tuple containing two references. Tuple unpacking at the call site is assignment syntax, not multiple independent return channels.

## 9. Name resolution and scope

Python resolves an ordinary name through:

```text
Local -> Enclosing -> Global -> Built-in
```

This is commonly called the LEGB rule.

```python
tax_rate = 0.11


def total_with_tax(subtotal):
    tax_rate = 0.10
    return subtotal * (1 + tax_rate)


result = total_with_tax(200)
print(result)

assert result == 220.00000000000003
assert tax_rate == 0.11
```

Assignment inside the function binds a local name unless declared `global` or `nonlocal`. Avoid exact equality for many floating-point calculations in production tests; this example exposes the binary floating-point result intentionally.

### 9.1 `global` and `nonlocal`

- `global name` makes assignment target a module-level binding.
- `nonlocal name` makes assignment target a binding in an enclosing function scope.

Both increase non-local state coupling. Prefer explicit state objects or returned values when practical.

<!-- TODO(media): Add a scope-frame animation showing local, enclosing, global, and built-in lookup plus local rebinding. Suggested path: ../Assets/Module-4/legb-scope.gif -->

## 10. Argument binding, rebinding, and mutation

Function arguments bind local parameter names to the same objects supplied by the caller [1].

```python
def append_marker(items):
    items.append("processed")


def replace_locally(items):
    items = ["replacement"]
    return items


records = ["raw"]
append_marker(records)
local_result = replace_locally(records)

print(records)
print(local_result)

assert records == ["raw", "processed"]
assert local_result == ["replacement"]
```

- `append_marker` mutates the shared list object.
- `replace_locally` rebinds only its local parameter name.

The call mechanism is often described as **call by sharing**: object references are passed by value, and mutation is visible through all aliases to the object.

## 11. Pure functions and side effects

A **pure function**:

- returns a result determined only by its arguments; and
- creates no externally observable side effects.

```python
def normalized_scores(scores, maximum):
    if maximum <= 0:
        raise ValueError("maximum must be positive")
    return [score / maximum for score in scores]


source = [20, 15, 10]
result = normalized_scores(source, 20)

assert result == [1.0, 0.75, 0.5]
assert source == [20, 15, 10]
```

Pure functions are easier to test and compose. Programs still need side effects for input, output, persistence, clocks, and randomness. Isolate those effects at explicit boundaries rather than pretending they do not exist.

## 12. Default argument evaluation

Default expressions are evaluated once when the `def` statement executes, not once per call [1].

Incorrect shared mutable default:

```python
def collect(value, bucket=[]):
    bucket.append(value)
    return bucket


first = collect("A")
second = collect("B")

assert first is second
assert second == ["A", "B"]
```

Correct independent default:

```python
def collect(value, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(value)
    return bucket


first = collect("A")
second = collect("B")

assert first == ["A"]
assert second == ["B"]
assert first is not second
```

An immutable default such as `None`, a number, or a string is normally safe.

## 13. Documentation and type annotations

### 13.1 Docstrings

The first string literal in a function body becomes its documentation string [1].

A concise public-function docstring should state:

- action and returned result;
- parameter meaning not obvious from names;
- required units or ranges;
- notable side effects; and
- intentionally raised exceptions.

Do not repeat the signature in prose.

### 13.2 Type hints

```python
def weighted_total(values: list[float], weight: float = 1.0) -> float:
    """Return the sum of values after applying one common weight."""
    return sum(value * weight for value in values)


assert weighted_total([1.0, 2.5], 2.0) == 7.0
```

Annotations are metadata and do not enforce types at runtime by themselves [3]. Static type checkers, IDEs, documentation tools, and frameworks may interpret them.

Type hints should express the supported interface, not overspecify one representation when any compatible abstraction is accepted.

## 14. Functions as objects

Functions are first-class objects: they can be assigned to names, stored in containers, passed as arguments, and returned.

```python
def square(value):
    return value * value


def apply_twice(operation, value):
    return operation(operation(value))


result = apply_twice(square, 2)
print(result)
assert result == 16
```

This supports strategy selection and higher-order abstraction. Use named functions when behaviour deserves a stable name, documentation, or independent testing.

## 15. Decomposition example

Requirement:

> Convert Celsius readings to Fahrenheit, discard readings outside a sensor's valid Celsius range, and report the mean converted value.

Decomposition:

```python
def is_valid_celsius(value, minimum=-80.0, maximum=80.0):
    return minimum <= value <= maximum


def celsius_to_fahrenheit(value):
    return value * 9 / 5 + 32


def mean(values):
    if not values:
        raise ValueError("mean requires at least one value")
    return sum(values) / len(values)


def mean_valid_fahrenheit(readings):
    converted = [
        celsius_to_fahrenheit(value)
        for value in readings
        if is_valid_celsius(value)
    ]
    return mean(converted)


result = mean_valid_fahrenheit([0.0, 20.0, 100.0])
print(result)
assert result == 50.0
```

Responsibilities remain separate:

- validation policy;
- unit conversion;
- aggregation contract; and
- workflow composition.

<!-- TODO(media): Add a data-flow animation for validation, conversion, and aggregation functions. Show the rejected 100 °C reading. Suggested path: ../Assets/Module-4/function-pipeline.mp4 -->

## 16. Common failure modes

### 16.1 Mixed responsibility

A function that parses input, mutates a database, calculates a result, and formats output has several reasons to change.

### 16.2 Hidden global dependency

A function that reads undeclared global configuration cannot be understood or tested from its signature alone.

### 16.3 Printing instead of returning

Printed text is difficult to compose into later calculations. Return domain data; format it at an output boundary.

### 16.4 Missing return

A path that reaches the end returns `None`. Trace every branch when callers require a value.

### 16.5 Shared mutable default

Mutable defaults retain state between calls. Use `None` and allocate inside.

### 16.6 Undocumented mutation

If a function changes a caller-owned object, state that side effect in its contract and name it clearly.

### 16.7 Boolean flag overload

Several flags can create many behaviour combinations. Separate strategies or functions may provide clearer contracts.

### 16.8 Catch-all parameters

Unnecessary `*args` and `**kwargs` hide spelling errors and supported options.

## 17. Guided practice

### 17.1 Contract completion

Write the missing precondition, postcondition, and failure rule for:

```python
def percentage(part, whole):
    return part / whole * 100
```

### 17.2 Mutation trace

Trace names and objects for:

```python
def add_one(values):
    values.append(1)
    values = [99]
    return values


source = [0]
result = add_one(source)
```

**Success criteria:** final `source` and `result` are correct, and rebinding is distinguished from mutation.

### 17.3 Responsibility split

Decompose “read a CSV file, validate rows, calculate totals, and print a report” into at least four functions. State each function's input and output.

## 18. Independent practice

### Exercise 1 — Numeric contract

Implement `safe_mean(values)`.

**Requirements:** return a float for non-empty numeric input; raise `ValueError` for empty input; do not mutate `values`.

### Exercise 2 — Keyword-only policy

Implement:

```text
convert_temperature(value, /, *, source, target)
```

Support Celsius and Fahrenheit in both directions. Reject unsupported unit codes with `ValueError`.

### Exercise 3 — Pure normalization

Implement a function that returns normalized, non-empty tags from a list of strings.

**Constraints:** trim whitespace, use `casefold()`, preserve input order, and do not mutate the input list.

### Exercise 4 — Decomposition review

Given a 30-line monolithic function from a previous exercise, produce:

1. a responsibility map;
2. proposed function contracts;
3. refactored code; and
4. assertions proving equivalent output for three inputs.

## 19. Knowledge check

1. How do decomposition and abstraction differ?
2. What is the difference between a parameter and an argument?
3. What does a function return when no `return` executes?
4. Why can mutation inside a function affect the caller?
5. Why does rebinding a parameter not rebind the caller's name?
6. When are default expressions evaluated?
7. Do type hints perform runtime validation automatically?
8. Why are pure functions generally easier to test?

<details>
<summary>Answer key</summary>

1. Decomposition divides responsibilities; abstraction defines a stable relevant interface while hiding detail.
2. A parameter is a definition-time local name; an argument is a call-time expression or value.
3. `None`.
4. Caller and parameter may reference the same mutable object.
5. Assignment changes the local binding, not another scope's binding.
6. Once, when the function definition executes.
7. No. They are metadata unless a separate tool or framework enforces them.
8. Their results depend only on arguments and they do not require external-state setup or side-effect inspection.

</details>

## 20. Module synthesis

Function design sequence:

```text
responsibility
    -> contract
    -> explicit dependencies
    -> implementation
    -> assertions or tests
    -> composition
```

Use parameters and returns to make data flow visible. Isolate mutation and external effects. A short function is not automatically cohesive, and a long function is not automatically incorrect; the decisive property is whether its contract expresses one stable responsibility.

## References

1. Python Software Foundation. “More on Defining Functions.” *The Python Tutorial*. Accessed 31 August 2026. https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions
2. Python Software Foundation. “Function Definitions.” *Python Language Reference*. Accessed 31 August 2026. https://docs.python.org/3/reference/compound_stmts.html#function-definitions
3. Python Software Foundation. “`typing` — Support for Type Hints.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/typing.html

---

**Previous module:** Module 3 — String Manipulation  
**Next module:** Module 5 — Tuples, Lists, and Aliasing
