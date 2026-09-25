# Module 5: Tuples, Lists, and Aliasing

**Course:** Algorithms and Programming

**Program:** TSI International Undergraduate Program

**Programming language:** Python 3.10 or later

**Prerequisite:** Module 4

**Estimated study time:** 3 to 4 hours

## 1. Module scope

Lists and tuples store ordered collections. They support similar reading operations, but they have different update rules:

- a list is mutable, so its elements can be changed;
- a tuple is immutable, so its stored element references cannot be replaced.

Variables do not contain independent copies automatically. Two names may refer to the same list. This relationship is called aliasing. A mutation performed through either name is visible through both names.

This module develops a practical model for sequences, mutation, aliases, and independent copies. The assessed core uses flat lists and tuples. Nested shallow-copy behavior appears as a technical extension.

<!-- TODO(media): Add an object-reference animation comparing list aliasing, a flat copy, and two independent mutations. Suggested path: ../Assets/Module-5/aliasing-and-copying.mp4 -->

## 2. Learning outcomes

After completing this module, a student should be able to:

1. create and access lists and tuples;
2. apply indexing, slicing, membership tests, and iteration;
3. pack and unpack tuple values;
4. modify a list with assignment and common methods;
5. explain why a tuple does not support element replacement;
6. distinguish equality from identity;
7. predict the effect of mutation through an alias;
8. create an independent flat-list copy;
9. design a function that either mutates input intentionally or returns a new collection.

## 3. Prerequisite check

Before continuing, confirm that you can:

- create and iterate through a list;
- define a function with parameters;
- return a result from a function;
- trace assignment statements.

### 3.1 Suggested study schedule

| Activity | Time |
| --- | ---: |
| Sequence operations and tuples | 45 minutes |
| List mutation and methods | 50 minutes |
| Identity, aliasing, and copies | 55 minutes |
| Shift Output Summary study case | 35 minutes |
| Practice and knowledge check | 25 minutes |
| **Total** | **210 minutes** |

## 4. Ordered sequences

Lists, tuples, and strings are ordered sequences. Position determines how an element is accessed.

```python
output_values = [120, 128, 125, 132]
shift_record = ("Shift A", 120, 8)

assert output_values[0] == 120
assert output_values[-1] == 132
assert shift_record[0] == "Shift A"
```

Indices begin at zero. A negative index counts from the end.

Common sequence operations:

| Operation | Result |
| --- | --- |
| `len(sequence)` | number of elements |
| `sequence[index]` | one element |
| `sequence[start:stop]` | a slice |
| `value in sequence` | membership test |
| `first + second` | concatenated sequence of the same type |
| `sequence * count` | repeated sequence |

## 5. Indexing and slicing

Indexing returns one stored element:

```python
measurements = [18.5, 19.0, 18.8, 19.3]

assert measurements[1] == 19.0
assert measurements[-2] == 18.8
```

Slicing returns a new sequence containing a selected range:

```python
first_half = measurements[:2]
second_half = measurements[2:]

assert first_half == [18.5, 19.0]
assert second_half == [18.8, 19.3]
```

The stop index is excluded. `measurements[1:3]` contains positions `1` and `2`.

## 6. Iterating through a sequence

A direct `for` loop is appropriate when the calculation needs each value:

```python
output_values = [120, 128, 125, 132]
total_output = 0

for output in output_values:
    total_output += output

assert total_output == 505
```

Use `range(len(sequence))` when the numeric position is required:

```python
labels = []

for index in range(len(output_values)):
    labels.append(f"Period {index + 1}: {output_values[index]}")

assert labels[0] == "Period 1: 120"
```

Prefer direct iteration when the index has no purpose.

## 7. Tuples

A tuple is an ordered immutable sequence. Parentheses commonly make tuple boundaries visible:

```python
shift_record = ("Shift A", 505, "TARGET MET")

assert len(shift_record) == 3
assert shift_record[1] == 505
```

Tuple elements may have different types because a tuple often represents one fixed record.

Examples:

```python
coordinate = (4, 7)
production_result = ("PUMP-01", 120, 3.5)
empty_tuple = ()
single_item_tuple = (120,)

assert len(single_item_tuple) == 1
```

The comma creates a one-element tuple. `(120)` is only the integer `120` inside parentheses.

### 7.1 Tuple packing and unpacking

Packing combines values into one tuple:

```python
result = 121, 135, 514
assert result == (121, 135, 514)
```

Unpacking assigns tuple elements to separate names:

```python
minimum_output, maximum_output, total_output = result

assert minimum_output == 121
assert maximum_output == 135
assert total_output == 514
```

The number of target names must match the number of elements.

### 7.2 Returning a tuple from a function

```python
def output_range(values):
    return min(values), max(values)


minimum, maximum = output_range([128, 121, 135, 130])

assert minimum == 121
assert maximum == 135
```

The function returns one tuple. Unpacking separates its elements at the call site.

### 7.3 Tuple immutability

This assignment is invalid:

```text
record = ("Shift A", 505)
record[1] = 510
```

Python raises `TypeError` because tuple elements cannot be replaced.

Immutability does not mean every referenced object is unchangeable. A tuple may contain a list:

```python
record = ("Shift A", [120, 125])
record[1].append(130)

assert record == ("Shift A", [120, 125, 130])
```

The tuple still refers to the same list. The list itself was mutated. This boundary is technical extension material.

## 8. Lists

A list is an ordered mutable sequence:

```python
measurements = [120, 125, 130]
measurements[1] = 128

assert measurements == [120, 128, 130]
```

Mutation changes the existing list object. This differs from string processing, where methods return new strings because strings are immutable.

### 8.1 Adding elements

```python
measurements = [120, 125]
measurements.append(130)
measurements.extend([128, 132])

assert measurements == [120, 125, 130, 128, 132]
```

- `append(value)` adds one element;
- `extend(sequence)` adds each element from another sequence;
- `insert(index, value)` inserts before a position.

```python
measurements.insert(1, 122)
assert measurements == [120, 122, 125, 130, 128, 132]
```

### 8.2 Removing elements

```python
values = [120, 125, 130, 125]

values.remove(125)
last_value = values.pop()
del values[0]

assert values == [130]
assert last_value == 125
```

- `remove(value)` deletes the first equal value;
- `pop()` removes and returns an element;
- `del` removes by index or slice.

### 8.3 Sorting and reversing

```python
values = [128, 121, 135, 130]
sorted_values = sorted(values)

assert values == [128, 121, 135, 130]
assert sorted_values == [121, 128, 130, 135]
```

`sorted(values)` returns a new list. `values.sort()` changes the existing list:

```python
values.sort()
assert values == [121, 128, 130, 135]
```

List methods such as `append()`, `extend()`, `sort()`, and `reverse()` modify the list and return `None`.

```python
values = [3, 1, 2]
result = values.sort()

assert values == [1, 2, 3]
assert result is None
```

## 9. Mutation and rebinding

Mutation changes an object. Rebinding makes a name refer to a different object.

```python
values = [120, 125]
values.append(130)       # mutation
values = [140, 145]      # rebinding
```

These operations have different effects when aliases exist.

## 10. Aliasing

Assignment does not automatically copy a list:

```python
original = [120, 125, 130]
alias = original

alias[0] = 118

assert original == [118, 125, 130]
assert alias == [118, 125, 130]
```

`original` and `alias` refer to the same list object. A mutation through either name changes that shared object.

<!-- TODO(media): Add a memory diagram with two names pointing to one list, followed by a mutation through one alias. Suggested path: ../Assets/Module-5/two-names-one-list.gif -->

### 10.1 Equality and identity

Equality asks whether values are equivalent. Identity asks whether two names refer to the same object.

```python
first = [1, 2, 3]
second = [1, 2, 3]
alias = first

assert first == second
assert first is not second
assert first is alias
```

Use `==` for ordinary value comparison. Use `is` for identity questions, especially comparisons with `None`.

## 11. Creating an independent flat copy

For a flat list, these forms create a new list object:

```python
source = [120, 125, 130]

copy_with_method = source.copy()
copy_with_slice = source[:]
copy_with_constructor = list(source)

copy_with_method[0] = 118

assert source == [120, 125, 130]
assert copy_with_method == [118, 125, 130]
assert copy_with_slice is not source
assert copy_with_constructor is not source
```

The new outer list can be changed without changing the source outer list.

### 11.1 Technical extension: shallow copies

`copy()`, slicing, and `list()` make shallow copies. The outer list is new, but nested objects remain shared.

```python
source = [[120, 125], [130, 135]]
copied = source.copy()

copied[0].append(128)

assert source == [[120, 125, 128], [130, 135]]
assert copied is not source
assert copied[0] is source[0]
```

The assessed practicum uses flat lists. For nested data, decide whether sharing nested objects is acceptable before choosing a copying method.

## 12. Function boundaries and list ownership

A function should make its mutation policy clear.

### 12.1 Function that mutates input

```python
def record_output(output_values, new_value):
    """Append new_value to output_values and return None."""
    output_values.append(new_value)


measurements = [120, 125]
record_output(measurements, 130)

assert measurements == [120, 125, 130]
```

### 12.2 Function that returns a new list

```python
def revised_output(output_values, index, new_value):
    """Return an updated copy without changing output_values."""
    revised = output_values.copy()
    revised[index] = new_value
    return revised


measurements = [120, 125, 130]
revised = revised_output(measurements, 1, 128)

assert measurements == [120, 125, 130]
assert revised == [120, 128, 130]
```

Neither design is universally correct. The contract must state which behavior is intended.

## 13. Safe iteration and mutation

Removing elements from the same list being iterated can skip values because element positions change.

Unsafe pattern:

```text
for value in values:
    if value < 0:
        values.remove(value)
```

Safer construction of a new result:

```python
values = [10, -1, -2, 12]
accepted = []

for value in values:
    if value >= 0:
        accepted.append(value)

assert values == [10, -1, -2, 12]
assert accepted == [10, 12]
```

Another valid approach is to iterate over a copy when mutation of the original is required. Constructing a new result is often easier to reason about.

## 14. Technical extension: list comprehensions

A list comprehension constructs a new list from an iterable:

```python
values = [10, -1, -2, 12]
accepted = [value for value in values if value >= 0]

assert accepted == [10, 12]
```

Use a comprehension for one clear transformation or filter. Use an ordinary loop when several state changes or branches need explanation.

## 15. Choosing a tuple or list

Use a tuple when:

- the number and meaning of positions are fixed;
- element replacement should not occur;
- a function returns a small fixed group of results.

Use a list when:

- the collection grows or shrinks;
- elements need replacement;
- the program processes a variable number of similar values.

Example design:

```python
shift_name = "Shift A"
measurements = [128, 121, 135, 130]
summary = (min(measurements), max(measurements), sum(measurements))
```

The measurements are a changeable collection. The summary is a fixed three-part result.

## 16. Study case: Shift Output Summary

### 16.1 Requirement

Given a list of shift outputs:

- preserve the original list;
- produce a sorted copy;
- calculate minimum, maximum, and total;
- return the numeric summary and sorted values.

### 16.2 Implementation

```python
def summarize_shift(output_values):
    """Return min, max, total, and a sorted copy of output_values."""
    sorted_output = output_values.copy()
    sorted_output.sort()

    minimum_output = sorted_output[0]
    maximum_output = sorted_output[-1]
    total_output = sum(sorted_output)

    return minimum_output, maximum_output, total_output, sorted_output


original_output = [128, 121, 135, 130]
summary = summarize_shift(original_output)

minimum, maximum, total, sorted_output = summary

assert original_output == [128, 121, 135, 130]
assert minimum == 121
assert maximum == 135
assert total == 514
assert sorted_output == [121, 128, 130, 135]
```

Reference relationships:

```text
original_output -> original list
sorted_output   -> new outer list
summary         -> tuple containing three numbers and sorted_output
```

<!-- TODO(media): Add a step-by-step object diagram for the Shift Output Summary, including copy, sort, and tuple return. Suggested path: ../Assets/Module-5/shift-summary-objects.png -->

## 17. Common failure modes

### 17.1 Missing the singleton comma

`(5)` is an integer. `(5,)` is a one-element tuple.

### 17.2 Assigning an in-place method result

`values = values.sort()` binds `values` to `None`. Use `values.sort()` or `values = sorted(values)`.

### 17.3 Assuming assignment copies a list

`second = first` creates another reference to the same object.

### 17.4 Using `is` for value comparison

Use `==` to compare list contents. Identity is a different question.

### 17.5 Assuming a shallow copy duplicates nested lists

A shallow copy creates a new outer container while preserving references to nested objects.

### 17.6 Mutating during iteration

Removing elements from the iterated list can cause elements to be skipped.

### 17.7 Hiding mutation inside a function

Document whether a function changes a supplied list.

## 18. Guided practice

### 18.1 Tuple trace

Predict each result:

```python
record = ("A", 120, 4.5)
name, quantity, hours = record
```

### 18.2 Alias trace

Draw the names and objects after each statement:

```python
first = [10, 20]
second = first
second.append(30)
first = [99]
```

### 18.3 Copy selection

Modify this program so `original` remains unchanged:

```python
original = [128, 121, 135]
ordered = original
ordered.sort()
```

## 19. Independent practice

### Exercise 1: Fixed record

Represent a production record as `(product_code, quantity, line_name)`, unpack it, and display each field.

### Exercise 2: Independent revision

Write a function that returns a copy of a list with one corrected measurement. The source list must remain unchanged.

### Exercise 3: Summary tuple

Return minimum, maximum, and total as a tuple for a non-empty list of numbers.

### Exercise 4: Mutation audit

For five list operations, identify whether each operation mutates the list or returns a new object.

## 20. Knowledge check

1. What operations do lists and tuples share?
2. Why does `(5,)` require a comma?
3. What is tuple unpacking?
4. What is the difference between mutation and rebinding?
5. What is an alias?
6. How do `==` and `is` differ?
7. Name three ways to make a shallow list copy.
8. Why can a shallow copy still share nested lists?
9. Why does `values.sort()` return `None`?
10. Why is removing elements during direct iteration risky?

<details>
<summary>Answer key</summary>

1. Both support ordered access, indexing, slicing, iteration, membership, concatenation, and length.
2. The comma defines the tuple; parentheses alone only group an expression.
3. It assigns sequence elements to separate target names.
4. Mutation changes an object. Rebinding changes which object a name refers to.
5. It is another reference to the same object.
6. `==` compares values. `is` compares object identity.
7. `values.copy()`, `values[:]`, and `list(values)`.
8. Only the outer list is new; nested object references are reused.
9. It changes the existing list, and the `None` return discourages confusion with a new list.
10. Removing an element changes later positions while the loop continues its traversal.

</details>

## 21. Module synthesis

Use this reasoning sequence:

```text
choose the sequence type
    -> identify allowed mutations
    -> identify possible aliases
    -> choose shared or independent state
    -> test the original and result after each operation
```

The key question is not only what values a collection contains. Also ask which names refer to the same object and which operations modify that object.

## References

1. Python Software Foundation. "Data Structures." *The Python Tutorial*, Python 3.14.7 documentation. Accessed 25 September 2026. https://docs.python.org/3/tutorial/datastructures.html
2. Python Software Foundation. "Data Model: Objects, Values and Types." *Python Language Reference*, Python 3 documentation. Accessed 25 September 2026. https://docs.python.org/3/reference/datamodel.html
3. Bell, Ana. "Lecture 5: Tuples, Lists, Aliasing, Mutability, and Cloning." *MIT OpenCourseWare 6.0001: Introduction to Computer Science and Programming in Python*, Fall 2016. Accessed 25 September 2026. https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/resources/lecture-5-tuples-lists-aliasing-mutability-and-cloning/

---

**Previous module:** Module 4: Decomposition, Abstraction, and Functions

**Next module:** Module 6: Dictionaries and Recursion
