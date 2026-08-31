# Module 5 — Tuples, Lists, and Aliasing

> **Course:** Algorithms and Programming  
> **Programming language:** Python  
> **Supported runtime:** Python 3.10 or later  
> **Resource type:** Technical learning module  
> **Practical notebook:** Deferred to `../Practice/Modul_4-6.ipynb`  
> **Estimated study time:** 3–4 hours

## 1. Module scope

Tuples and lists are ordered Python sequences with different mutation contracts. A tuple fixes its directly stored references after construction; a list permits insertion, replacement, and deletion. Both can participate in aliasing because variables and containers hold object references.

This module develops a precise object-graph model for assignment, slicing, shallow copying, and deep copying. The central question is not “Was a copy made?” but “Which objects are new, and which nested objects remain shared?”

<!-- TODO(media): Add an object-graph animation comparing tuple construction, list construction, alias assignment, shallow copy, and deep copy. Suggested path: ../Assets/Module-5/copying-object-graphs.mp4 -->

## 2. Learning outcomes

After completing this module, a student should be able to:

1. **Compare** tuple and list contracts, operations, and use cases.
2. **Apply** indexing, slicing, concatenation, repetition, and unpacking.
3. **Distinguish** value equality from object identity.
4. **Trace** aliases through nested mutable containers.
5. **Predict** the effects of assignment, shallow copying, and deep copying.
6. **Construct** list comprehensions without hidden mutation.
7. **Select** tuples or lists based on semantic stability rather than syntax preference.
8. **Diagnose** repeated-reference initialization, in-place return values, and accidental caller mutation.

## 3. Sequence contract

Python sequences provide ordered positional access. Common operations include [1]:

| Operation | Meaning |
| --- | --- |
| `len(s)` | Number of items |
| `s[i]` | Item at index `i` |
| `s[i:j:k]` | Slice |
| `x in s` | Membership test |
| `s + t` | Concatenation |
| `s * n` | Repetition |
| `min(s)` / `max(s)` | Extremum when items are comparable |
| `s.index(x)` | First matching position |
| `s.count(x)` | Number of matching items |

Indexing returns one stored object reference. Slicing constructs a new outer sequence containing references selected from the source.

## 4. Tuples

### 4.1 Construction

The comma creates a tuple; parentheses usually group the expression.

```python
empty = ()
singleton = (42,)
coordinates = 3, 5

print(empty)
print(singleton)
print(coordinates)

assert len(empty) == 0
assert singleton == (42,)
assert coordinates == (3, 5)
```

Expected output:

```text
()
(42,)
(3, 5)
```

`(42)` is the integer `42`. The trailing comma is required for a one-item tuple.

### 4.2 Packing and unpacking

```python
record = ("CS204", "Algorithms", 4)
code, title, credits = record

print(code, credits)
assert code == "CS204"
assert title == "Algorithms"
assert credits == 4
```

Unpacking requires the number of targets to match, unless one target uses starred collection:

```python
first, *middle, last = (10, 20, 30, 40, 50)

assert first == 10
assert middle == [20, 30, 40]
assert last == 50
```

The starred target receives a list.

### 4.3 Immutability boundary

A tuple's direct item references cannot be replaced, inserted, or deleted [1]. A referenced mutable object can still change:

```python
configuration = ("v1", ["read", "write"])
configuration[1].append("delete")

print(configuration)
assert configuration == ("v1", ["read", "write", "delete"])
```

The tuple still references the same two objects. Its nested list changed.

## 5. Lists

Lists are mutable sequences [1]. They support item and slice assignment, deletion, and methods including `append()`, `extend()`, `insert()`, `remove()`, `pop()`, `clear()`, `sort()`, and `reverse()` [2].

```python
queue = ["A", "B"]
queue.append("C")
queue.extend(["D", "E"])
removed = queue.pop(1)

print(queue)
print(removed)

assert queue == ["A", "C", "D", "E"]
assert removed == "B"
```

### 5.1 In-place methods

Methods that mutate a list, such as `append()` and `sort()`, normally return `None` [2].

Incorrect:

```python
values = [3, 1, 2]
result = values.sort()

assert values == [1, 2, 3]
assert result is None
```

Use `sorted(values)` when a new sorted list is required:

```python
source = [3, 1, 2]
ordered = sorted(source)

assert source == [3, 1, 2]
assert ordered == [1, 2, 3]
```

### 5.2 Slice assignment

Slice assignment can replace a region with a different number of items:

```python
values = [0, 1, 2, 3, 4]
values[1:4] = [10, 20]

print(values)
assert values == [0, 10, 20, 4]
```

This mutates the existing list; aliases observe the change.

## 6. Equality, identity, and aliasing

- `a == b` asks whether values compare equal.
- `a is b` asks whether names refer to the same object.
- **Aliasing** occurs when two references reach the same mutable object.

```python
original = ["red", "blue"]
alias = original
equal_copy = ["red", "blue"]

print(original == equal_copy)
print(original is alias)
print(original is equal_copy)

assert original == equal_copy
assert original is alias
assert original is not equal_copy
```

Assignment does not copy an object. It binds another name to the existing object [3].

### 6.1 Mutation through an alias

```python
primary = [1, 2]
secondary = primary

secondary.append(3)

assert primary == [1, 2, 3]
assert primary is secondary
```

Rebinding `secondary = [9]` would not change `primary`. Mutation changes an object; assignment changes a binding.

<!-- TODO(media): Add an animation contrasting mutation of a shared list with rebinding one alias to a new list. Suggested path: ../Assets/Module-5/mutation-vs-rebinding.gif -->

## 7. Shallow copies

A **shallow copy** creates a new outer container and reuses references to nested objects [4].

Common shallow-copy operations for a list:

- `source.copy()`;
- `list(source)`;
- `source[:]`; and
- `copy.copy(source)`.

```python
source = [["A"], ["B"]]
shallow = source.copy()

print(source is shallow)
print(source[0] is shallow[0])

shallow.append(["C"])
shallow[0].append("shared")

assert source is not shallow
assert len(source) == 2
assert len(shallow) == 3
assert source[0] == ["A", "shared"]
assert source[0] is shallow[0]
```

The outer append affects only `shallow`. Mutation of the nested list is visible through both outer containers.

## 8. Deep copies

`copy.deepcopy()` recursively copies reachable components while tracking objects already copied to handle cycles and preserve sharing relationships where appropriate [4].

```python
from copy import deepcopy

source = [["A"], ["B"]]
deep = deepcopy(source)

deep[0].append("independent")

assert source == [["A"], ["B"]]
assert deep == [["A", "independent"], ["B"]]
assert source is not deep
assert source[0] is not deep[0]
```

Deep copying is not automatically the correct policy:

- some resources cannot or should not be duplicated;
- copying a large graph is expensive;
- preserving shared identity may be semantically required; and
- custom classes can control copying behaviour.

Prefer constructing the exact new structure required by the operation.

## 9. Repetition and the shared-reference trap

Sequence repetition copies references, not nested objects.

```python
incorrect = [[]] * 3
incorrect[0].append("X")

print(incorrect)
assert incorrect == [["X"], ["X"], ["X"]]
assert incorrect[0] is incorrect[1]
```

Create independent inner lists with a comprehension:

```python
correct = [[] for _ in range(3)]
correct[0].append("X")

print(correct)
assert correct == [["X"], [], []]
assert correct[0] is not correct[1]
```

The same issue appears with `[[0] * columns] * rows`.

<!-- TODO(media): Add a memory-reference animation for [[]] * 3 versus a list comprehension, showing one shared inner list versus three independent lists. Suggested path: ../Assets/Module-5/repetition-aliasing.mp4 -->

## 10. List comprehensions

A list comprehension constructs a new list from an iterable:

```text
[expression for target in iterable if condition]
```

```python
readings = [3, -2, 7, 0, -1]
squares = [value * value for value in readings if value >= 0]

print(squares)
assert squares == [9, 49, 0]
```

The output expression should primarily compute a value. Avoid hidden mutation or I/O inside a comprehension; use a loop when the body performs several stateful operations.

Nested comprehensions follow nested-loop order but can become unreadable when they combine several conditions.

## 11. Tuples, hashability, and keys

An object is **hashable** when its hash value remains stable and it supports equality consistently. Hashable objects may be dictionary keys or set elements [1].

- a tuple is hashable only if all its elements are hashable;
- a list is not hashable because it is mutable; and
- tuple immutability alone does not make a tuple recursively immutable.

```python
valid_key = ("course", 204)
mapping = {valid_key: "Algorithms"}

assert mapping[("course", 204)] == "Algorithms"

invalid_key = ("course", [204])
try:
    hash(invalid_key)
except TypeError as error:
    print(type(error).__name__)
```

Expected output:

```text
TypeError
```

## 12. Function boundaries and ownership

A function receiving a list may:

1. read it without mutation;
2. mutate it by contract;
3. make a shallow copy;
4. make a deep copy; or
5. construct a transformed result.

Make ownership policy explicit.

```python
def without_negatives(values):
    """Return a new list containing only non-negative values."""
    return [value for value in values if value >= 0]


source = [2, -1, 5]
result = without_negatives(source)

assert source == [2, -1, 5]
assert result == [2, 5]
assert result is not source
```

A name such as `sort_in_place()` signals mutation better than a generic `process()`.

## 13. Selection guidance

Choose a tuple when:

- item positions have stable semantic roles;
- the collection itself should not grow or shrink;
- unpacking is part of the interface; or
- a hashable composite key is required and all elements are hashable.

Choose a list when:

- the collection grows, shrinks, or reorders;
- homogeneous repeated items are processed as a sequence;
- slice assignment or in-place operations are required; or
- a comprehension naturally produces the result.

Tuple use does not automatically guarantee deep immutability, validation, named fields, or domain invariants.

## 14. Common failure modes

### 14.1 Missing singleton comma

`(value)` is grouping; `(value,)` is a tuple.

### 14.2 Assigning an in-place result

`items = items.sort()` replaces the name with `None`.

### 14.3 Assuming slicing is deep

`nested[:]` copies only the outer list.

### 14.4 Repeating a mutable item

`[mutable] * n` creates `n` references to one object.

### 14.5 Mutating caller-owned data silently

State mutation in the function contract or return a new structure.

### 14.6 Using equality to test aliasing

Equal lists can be distinct objects. Use `is` only when identity is the question.

### 14.7 Deep-copying without a semantic reason

Deep copying may duplicate excessive state or violate resource identity.

## 15. Guided practice

### 15.1 Object graph

Draw names and objects after:

```python
from copy import deepcopy

a = [[1], [2]]
b = a
c = a.copy()
d = deepcopy(a)
```

Mark each true identity relationship between outer and inner lists.

### 15.2 Unpacking trace

Predict values:

```python
head, *body, tail = range(6)
```

### 15.3 Mutation policy

Review a function that calls `values.sort()`. Write two alternative contracts: one for in-place sorting and one for returning an independent sorted list.

## 16. Independent practice

### Exercise 1 — Matrix initialization

Create a `3 × 4` matrix of independent zeros. Set position `[0][0]` to `1`.

**Success criteria:** only one cell changes, and inner row identities are distinct.

### Exercise 2 — Shallow versus deep

Construct a nested list containing two shared references to the same inner list. Apply `copy()` and `deepcopy()`.

**Deliverable:** identity assertions explaining which sharing relationships remain.

### Exercise 3 — Immutable record

Represent a course record as a tuple containing code, title, and credits. Unpack it and use it as a dictionary key.

**Constraint:** every element must be hashable.

### Exercise 4 — Pure transformation

Implement `normalized_rows(rows)` that returns a new nested list with each numeric row divided by its sum.

**Requirements:** reject zero-sum rows with `ValueError` and do not mutate any input row.

## 17. Knowledge check

1. What syntactic element creates a one-item tuple?
2. What does a list slice copy?
3. How do equality and identity differ?
4. Why does `[[]] * 3` create coupled rows?
5. What remains shared after a shallow copy?
6. When is a tuple hashable?
7. Why do mutating list methods normally return `None`?
8. When is a deep copy inappropriate?

<details>
<summary>Answer key</summary>

1. A trailing comma.
2. The outer sequence and its selected references; nested objects are reused.
3. Equality compares values; identity asks whether references reach the same object.
4. Repetition duplicates the one inner-list reference.
5. Nested referenced objects.
6. When every contained element is hashable.
7. Their purpose is an in-place state change; returning `None` prevents confusion with a new collection.
8. When identity sharing is required, resources are not duplicable, or recursive duplication is unnecessarily expensive.

</details>

## 18. Module synthesis

Analyse sequence operations with an object graph:

```text
names
    -> outer container identities
    -> contained references
    -> nested mutable objects
```

Assignment adds a binding. Slicing and `copy()` create a shallow outer object. `deepcopy()` recursively constructs a new graph according to copy semantics. Select tuple or list from the mutation contract, then make ownership visible at every function boundary.

## References

1. Python Software Foundation. “Sequence Types — `list`, `tuple`, `range`.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range
2. Python Software Foundation. “Data Structures.” *The Python Tutorial*. Accessed 31 August 2026. https://docs.python.org/3/tutorial/datastructures.html
3. Python Software Foundation. “Data Model: Objects, Values and Types.” *Python Language Reference*. Accessed 31 August 2026. https://docs.python.org/3/reference/datamodel.html#objects-values-and-types
4. Python Software Foundation. “`copy` — Shallow and Deep Copy Operations.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/copy.html

---

**Previous module:** Module 4 — Decomposition, Abstraction, and Functions  
**Next module:** Module 6 — Recursion and Dictionaries
