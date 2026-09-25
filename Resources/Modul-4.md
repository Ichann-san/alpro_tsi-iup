# Module 4: Decomposition, Abstraction, and Functions

**Course:** Algorithms and Programming

**Program:** TSI International Undergraduate Program

**Programming language:** Python 3.10 or later

**Prerequisites:** Modules 1-3

**Estimated study time:** 3 to 4 hours

## 1. Module scope

A function gives a name to a reusable computation. Functions allow a program to be divided into smaller responsibilities, with each part receiving input and producing a defined result.

This module begins with the basic `def` syntax and function calls. It then develops two design ideas:

- **decomposition:** divide one large problem into smaller problems;
- **abstraction:** use a component through its interface without depending on every implementation detail.

The assessed core uses ordinary parameters, return values, local variables, and simple docstrings. Advanced parameter syntax and higher-order functions are not required.

<!-- TODO(media): Add an animation that transforms one long production-cost program into four connected functions. Suggested path: ../Assets/Module-4/decomposition-flow.mp4 -->

## 2. Learning outcomes

After completing this module, a student should be able to:

1. define and call a Python function;
2. distinguish parameters from arguments;
3. return a value and store the returned result;
4. distinguish `print()` output from a return value;
5. trace local variables during a function call;
6. divide a calculation into functions with separate responsibilities;
7. write a simple function contract and docstring;
8. identify basic side effects involving mutable arguments.

## 3. Prerequisite check

Before continuing, confirm that you can:

- create variables and evaluate expressions;
- use `if`, `elif`, and `else`;
- process values with `for` and `while` loops;
- create lists and manipulate strings.

No previous experience defining custom functions is assumed.

### 3.1 Suggested study schedule

| Activity | Time |
| --- | ---: |
| Function syntax, calls, parameters, and returns | 55 minutes |
| Decomposition, abstraction, and contracts | 50 minutes |
| Scope, data flow, and side effects | 45 minutes |
| Production Cost Calculator study case | 35 minutes |
| Practice and knowledge check | 25 minutes |
| **Total** | **210 minutes** |

## 4. Why functions are needed

Consider two production calculations written without functions:

```python
morning_good_units = 520 - 18
afternoon_good_units = 490 - 12

print(morning_good_units)
print(afternoon_good_units)
```

The calculation `total units - defective units` is repeated. Repetition creates several risks:

- the same rule may be written differently in different places;
- a rule change must be applied in several locations;
- a long program becomes difficult to inspect;
- individual calculations cannot be tested independently.

A function defines the rule once:

```python
def calculate_good_units(total_units, defective_units):
    return total_units - defective_units


morning_good_units = calculate_good_units(520, 18)
afternoon_good_units = calculate_good_units(490, 12)

assert morning_good_units == 502
assert afternoon_good_units == 478
```

The function name states the purpose. Its parameters identify the required input. Its return value provides the result.

## 5. Defining a function

The basic structure is:

```python
def function_name(parameter_1, parameter_2):
    statement
    return result
```

Example:

```python
def calculate_area(length, width):
    area = length * width
    return area
```

Technical parts:

| Part | Meaning |
| --- | --- |
| `def` | Starts a function definition |
| `calculate_area` | Function name |
| `length, width` | Parameters |
| `:` | Ends the function header |
| Indented statements | Function body |
| `return area` | Sends a result to the caller |

Defining a function does not execute its body. The body runs when the function is called.

## 6. Calling a function

A call writes the function name followed by arguments in parentheses:

```python
def calculate_area(length, width):
    return length * width


floor_area = calculate_area(12, 8)
print(floor_area)

assert floor_area == 96
```

Expected output:

```text
96
```

Execution sequence:

1. Python evaluates the arguments `12` and `8`.
2. `length` refers to `12` and `width` refers to `8` for this call.
3. The function body calculates `96`.
4. `return` sends `96` to the call location.
5. `floor_area` refers to the returned value.

<!-- TODO(media): Add a call-frame animation showing argument binding, local calculation, return, and assignment. Suggested path: ../Assets/Module-4/function-call-frame.gif -->

## 7. Parameters and arguments

A **parameter** is a name in a function definition. An **argument** is a value or expression supplied in a function call.

```python
def calculate_utilization(actual_output, maximum_output):
    return actual_output / maximum_output * 100


utilization = calculate_utilization(450, 500)
assert utilization == 90.0
```

In this example:

- `actual_output` and `maximum_output` are parameters;
- `450` and `500` are arguments;
- `90.0` is the returned value.

Python normally matches arguments to parameters by position:

```python
def calculate_difference(actual, target):
    return actual - target


assert calculate_difference(520, 500) == 20
assert calculate_difference(500, 520) == -20
```

Changing argument order changes the calculation.

### 7.1 Keyword arguments

Parameter names can also be written in the call:

```python
difference = calculate_difference(actual=520, target=500)
assert difference == 20
```

Keyword arguments are useful when adjacent numeric values have different meanings.

## 8. Returning values

`return` ends the current function call and supplies a value to the caller.

```python
def classify_output(actual, target):
    if actual >= target:
        return "TARGET MET"
    return "BELOW TARGET"


status = classify_output(515, 500)
assert status == "TARGET MET"
```

Once a `return` statement executes, later statements in that function body are not executed.

```python
def example():
    return 10
    print("This statement cannot run")


assert example() == 10
```

### 8.1 A function without an explicit return

If execution reaches the end of a function without `return`, Python returns `None` [1].

```python
def display_line_name(line_name):
    print(f"Line: {line_name}")


result = display_line_name("Assembly A")
assert result is None
```

`None` represents the absence of a value. It is not the same as `0`, `False`, or an empty string.

## 9. `print()` versus `return`

`print()` displays text. `return` supplies data to the caller.

```python
def printed_total(first, second):
    print(first + second)


def returned_total(first, second):
    return first + second
```

The returned result can participate in another calculation:

```python
daily_total = returned_total(125, 140)
weekly_estimate = daily_total * 5

assert daily_total == 265
assert weekly_estimate == 1325
```

The printed version displays a value but returns `None`:

```python
printed_result = printed_total(125, 140)
assert printed_result is None
```

Use `return` for calculated domain data. Use `print()` at the output boundary when a person needs to see the result.

## 10. Decomposition

Decomposition separates a requirement into responsibilities. A useful function performs one coherent job.

Requirement:

> Calculate material cost, labor cost, and total production cost.

Possible decomposition:

```text
calculate_material_cost
calculate_labor_cost
calculate_total_cost
display_cost_report
```

Dependencies:

```text
quantity + material cost per unit -> material cost
hours + hourly labor cost         -> labor cost
material cost + labor cost        -> total cost
total cost                        -> displayed report
```

This structure makes data flow visible. A material-price rule can change without changing the labor calculation.

## 11. Abstraction

Abstraction separates **what a function provides** from **how it performs the work**.

```python
def calculate_material_cost(quantity, unit_cost):
    return quantity * unit_cost
```

A caller needs to know:

- which arguments are required;
- what each argument means;
- what value is returned;
- which input assumptions apply.

The caller does not need to repeat the multiplication or depend on the local variable names inside the function.

A function therefore has two useful views:

| View | Main concern |
| --- | --- |
| Interface | Function name, parameters, result, assumptions |
| Implementation | Statements that produce the result |

## 12. Function contracts

A function contract states the expected relationship between input and output.

```text
calculate_material_cost(quantity, unit_cost)

Inputs:
- quantity: non-negative number of units
- unit_cost: non-negative cost per unit

Returns:
- quantity multiplied by unit_cost

Side effects:
- none
```

The contract does not need to describe each Python statement. It describes what callers may rely on.

### 12.1 Preconditions and postconditions

A **precondition** must be true before a function is called. A **postcondition** must be true after a successful call.

For `calculate_material_cost`:

- precondition: `quantity >= 0` and `unit_cost >= 0`;
- postcondition: the returned value equals `quantity * unit_cost`;
- side effect: no caller-owned object is changed.

Validation and exception handling are developed in Module 7. In this module, examples state input assumptions explicitly.

## 13. Docstrings

A docstring is the first string literal inside a function body. It records the function's purpose and contract.

```python
def calculate_labor_cost(hours, hourly_rate):
    """Return labor cost for non-negative hours and hourly rate."""
    return hours * hourly_rate


assert calculate_labor_cost(8, 45_000) == 360_000
```

Useful docstrings state information that is not already obvious from the syntax, such as units, allowed ranges, and whether input is modified.

## 14. Local variables and scope

A variable created inside a function is normally local to that function call.

```python
def calculate_net_output(gross_output, defective_output):
    net_output = gross_output - defective_output
    return net_output


result = calculate_net_output(600, 25)
assert result == 575
```

`net_output` exists while the function call is active. The caller receives its value through `return`.

Different calls have separate local values:

```python
first_result = calculate_net_output(600, 25)
second_result = calculate_net_output(450, 10)

assert first_result == 575
assert second_result == 440
```

### 14.1 Local names can hide outer names

```python
rate = 10


def calculate(value):
    rate = 2
    return value * rate


assert calculate(5) == 10
assert rate == 10
```

Assignment inside the function creates the local `rate`. It does not change the outer `rate`.

For beginner programs, prefer parameters and returned values over changing global variables. Explicit data flow is easier to trace and test.

## 15. Calling one function from another

A larger function may coordinate smaller functions:

```python
def calculate_material_cost(quantity, unit_cost):
    return quantity * unit_cost


def calculate_labor_cost(hours, hourly_rate):
    return hours * hourly_rate


def calculate_total_cost(quantity, unit_cost, hours, hourly_rate):
    material = calculate_material_cost(quantity, unit_cost)
    labor = calculate_labor_cost(hours, hourly_rate)
    return material + labor


total = calculate_total_cost(120, 8_500, 8, 45_000)
assert total == 1_380_000
```

`calculate_total_cost` operates at a higher abstraction level. It coordinates two named calculations rather than repeating their arithmetic.

## 16. Side effects and mutable arguments

A side effect changes state outside the returned value. Printing is a side effect. Mutating a caller-owned list is another side effect.

```python
def add_measurement(measurements, value):
    measurements.append(value)


shift_output = [120, 125]
add_measurement(shift_output, 130)

assert shift_output == [120, 125, 130]
```

The parameter and caller can refer to the same list object. The mutation is therefore visible after the call.

A transformation can instead create and return a new list:

```python
def with_measurement(measurements, value):
    updated = measurements.copy()
    updated.append(value)
    return updated


original = [120, 125]
updated = with_measurement(original, 130)

assert original == [120, 125]
assert updated == [120, 125, 130]
```

Module 5 develops aliasing and copying in detail.

## 17. Technical extension: default parameters

A default parameter supplies a value when the caller omits that argument:

```python
def calculate_overtime_cost(hours, hourly_rate, multiplier=1.5):
    return hours * hourly_rate * multiplier


assert calculate_overtime_cost(2, 40_000) == 120_000
assert calculate_overtime_cost(2, 40_000, 2.0) == 160_000
```

Required parameters should normally appear before parameters with defaults.

Avoid a mutable object such as `[]` as a default value. Default values are created when the function definition is executed, so a mutable default can be shared across calls [1]. This rule is technical extension material and is not assessed in the Module 4 practicum.

## 18. Technical extension: type hints

Type hints document an intended interface:

```python
def calculate_defect_rate(defective: int, total: int) -> float:
    return defective / total * 100
```

Annotations do not automatically validate arguments at runtime [1]. They support readers, development tools, and static type checkers. Runtime validation remains a separate design decision.

## 19. Study case: Production Cost Calculator

### 19.1 Requirement

A production order contains:

- quantity;
- material cost per unit;
- labor hours;
- labor cost per hour;
- budget limit.

The program must calculate material cost, labor cost, total cost, and budget status.

### 19.2 Responsibility map

| Function | Input | Return |
| --- | --- | --- |
| `calculate_material_cost` | quantity, unit cost | material cost |
| `calculate_labor_cost` | hours, hourly cost | labor cost |
| `calculate_total_cost` | four cost inputs | combined cost |
| `classify_budget` | total cost, budget | status string |

### 19.3 Implementation

```python
def calculate_material_cost(quantity, unit_cost):
    """Return material cost for one production order."""
    return quantity * unit_cost


def calculate_labor_cost(hours, hourly_rate):
    """Return labor cost for one production order."""
    return hours * hourly_rate


def calculate_total_cost(quantity, unit_cost, hours, hourly_rate):
    """Return combined material and labor cost."""
    material = calculate_material_cost(quantity, unit_cost)
    labor = calculate_labor_cost(hours, hourly_rate)
    return material + labor


def classify_budget(total_cost, budget):
    """Return the order's budget classification."""
    if total_cost <= budget:
        return "WITHIN BUDGET"
    return "OVER BUDGET"


order_cost = calculate_total_cost(120, 8_500, 8, 45_000)
order_status = classify_budget(order_cost, 1_400_000)

print(f"Total cost: Rp{order_cost:,}")
print(f"Status: {order_status}")

assert order_cost == 1_380_000
assert order_status == "WITHIN BUDGET"
```

Expected output:

```text
Total cost: Rp1,380,000
Status: WITHIN BUDGET
```

<!-- TODO(media): Add a data-flow diagram showing the four cost functions, their inputs, and their returned values. Suggested path: ../Assets/Module-4/production-cost-functions.png -->

## 20. Common failure modes

### 20.1 Defining but not calling

`def` creates a function. It does not run the function body.

### 20.2 Forgetting parentheses

`calculate_area` refers to the function object. `calculate_area(12, 8)` calls it.

### 20.3 Printing instead of returning

Printed output cannot directly participate in a later calculation. Return the value first, then print at the program boundary.

### 20.4 Missing a return path

If a branch reaches the end of the function, that path returns `None`.

### 20.5 Incorrect indentation

The function body must be indented consistently. Code aligned with `def` is outside the body.

### 20.6 Depending on global variables

A function that silently reads or changes global state is harder to reuse. Pass required data through parameters.

### 20.7 Mixing responsibilities

A function that reads input, calculates costs, modifies a list, and formats a report has several reasons to change. Separate these responsibilities.

### 20.8 Hidden mutation

If a function changes a supplied list, state that behavior in its contract. Prefer returning a new value when mutation is not required.

## 21. Guided practice

### 21.1 Trace a call

Trace this call and record the parameter values, local variable, and returned value:

```python
def calculate_reject_rate(rejected, inspected):
    percentage = rejected / inspected * 100
    return percentage


result = calculate_reject_rate(8, 200)
```

### 21.2 Convert printing to returning

Rewrite the following function so its result can be used in another calculation:

```python
def display_total(first, second):
    print(first + second)
```

### 21.3 Decompose a requirement

Create a responsibility map for this requirement:

> Calculate gross production, defective production, good production, and achievement percentage.

## 22. Independent practice

### Exercise 1: Unit conversion

Implement `minutes_to_hours(minutes)` and return a decimal number of hours.

### Exercise 2: Capacity calculation

Implement `calculate_utilization(actual_output, maximum_output)`. Assume maximum output is positive.

### Exercise 3: Function composition

Implement separate functions for material cost, labor cost, and total production cost. The total function must call the two smaller functions.

### Exercise 4: Contract review

For each function from Exercise 3, state its parameters, preconditions, return value, and side effects.

## 23. Knowledge check

1. What is the difference between defining and calling a function?
2. What is the difference between a parameter and an argument?
3. What does `return` do?
4. What value is produced when a function reaches its end without `return`?
5. Why is `print()` not a substitute for `return`?
6. What is decomposition?
7. What is abstraction?
8. Why are local variables useful?
9. How can a function change a caller-owned list?
10. Do type hints enforce types automatically?

<details>
<summary>Answer key</summary>

1. A definition creates and names a function. A call executes its body.
2. A parameter is a name in the definition. An argument is supplied by a call.
3. It ends the current call and provides a value to the caller.
4. `None`.
5. Printing displays data but does not provide the displayed value for later computation.
6. It divides a problem into smaller responsibilities.
7. It exposes the interface a caller needs while hiding unnecessary implementation detail.
8. They isolate the temporary state of each call.
9. The parameter and caller may refer to the same mutable object.
10. No. Type hints are metadata unless another tool performs checking.

</details>

## 24. Module synthesis

Use this sequence when designing a function:

```text
identify one responsibility
    -> define required input
    -> define returned result
    -> implement the calculation
    -> test representative calls
    -> combine the function with other functions
```

A function is useful when its name, inputs, result, and side effects form a clear contract. Function length alone does not determine quality. The important property is a coherent responsibility with explicit data flow.

## References

1. Python Software Foundation. "More Control Flow Tools." *The Python Tutorial*, Python 3.14.7 documentation. Accessed 25 September 2026. https://docs.python.org/3/tutorial/controlflow.html
2. Bell, Ana. "Lecture 4: Decomposition, Abstraction, and Functions." *MIT OpenCourseWare 6.0001: Introduction to Computer Science and Programming in Python*, Fall 2016. Accessed 25 September 2026. https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/resources/lecture-4-decomposition-abstraction-and-functions/

---

**Previous module:** Module 3: Basic String Manipulation

**Next module:** Module 5: Tuples, Lists, and Aliasing
