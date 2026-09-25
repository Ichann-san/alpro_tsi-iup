# Module 6: Dictionaries and Recursion

**Course:** Algorithms and Programming

**Program:** TSI International Undergraduate Program

**Programming language:** Python 3.10 or later

**Prerequisite:** Module 5

**Estimated study time:** 4 to 5 hours

## 1. Module scope

A dictionary stores associations between keys and values. It is suitable when a program should access information by a meaningful identifier such as a product code rather than a numeric position.

Recursion is a problem-solving technique in which a function solves a problem by calling itself with a smaller version of the same problem. A correct recursive function needs a base case and guaranteed progress toward that base case.

This module teaches dictionaries before recursion. The concrete mapping model supports later recursive examples, including a multi-level bill of materials.

The assessed core covers basic dictionary operations and simple finite recursion. Formal recurrence analysis, mathematical induction, and performance optimization are deferred.

<!-- TODO(media): Add an animation that compares numeric list indexing with key-based dictionary lookup. Suggested path: ../Assets/Module-6/list-versus-dictionary.mp4 -->

## 2. Learning outcomes

After completing this module, a student should be able to:

1. create a dictionary from key-value pairs;
2. read, insert, and update dictionary entries;
3. test key membership and use `get()` for optional lookup;
4. iterate through keys, values, and items;
5. build a frequency or quantity dictionary;
6. identify the base case and recursive case of a function;
7. verify that recursive arguments progress toward termination;
8. trace recursive calls and returned results;
9. recursively process a small hierarchical structure.

## 3. Prerequisite check

Before continuing, confirm that you can:

- define and call functions;
- use parameters and return values;
- iterate through lists and tuples;
- unpack a two-element tuple;
- explain mutation and aliasing.

### 3.1 Suggested study schedule

| Activity | Time |
| --- | ---: |
| Dictionary construction and operations | 60 minutes |
| Dictionary iteration and accumulation | 45 minutes |
| Recursion model and call tracing | 65 minutes |
| Bill of Materials study case | 55 minutes |
| Practice and knowledge check | 35 minutes |
| **Total** | **260 minutes** |

## 4. Why dictionaries are needed

Suppose product quantities are stored in parallel lists:

```python
product_codes = ["PUMP", "VALVE", "SEAL"]
quantities = [12, 8, 25]
```

To find the quantity for `VALVE`, the program must first find its index and then use the same index in `quantities`.

A dictionary stores the association directly:

```python
inventory = {
    "PUMP": 12,
    "VALVE": 8,
    "SEAL": 25,
}

assert inventory["VALVE"] == 8
```

The key expresses the lookup meaning. The program no longer depends on synchronized positions in two lists.

## 5. Dictionary structure

A dictionary contains key-value pairs:

```python
inventory = {
    "PUMP": 12,
    "VALVE": 8,
}
```

In one pair:

```text
"PUMP": 12
   key   value
```

Properties:

- each key is unique within the dictionary;
- values may be repeated;
- a value may have any Python type;
- a dictionary is mutable;
- dictionaries preserve insertion order in modern Python [1].

An empty dictionary uses braces:

```python
inventory = {}
assert len(inventory) == 0
```

## 6. Reading values

Use square brackets with a key:

```python
inventory = {"PUMP": 12, "VALVE": 8}

pump_quantity = inventory["PUMP"]
assert pump_quantity == 12
```

If the key does not exist, subscription raises `KeyError` [1]:

```text
inventory["MOTOR"]
```

Exception handling is introduced in Module 7. For now, prevent an unexpected lookup by testing membership or using `get()`.

## 7. Inserting and updating entries

Assignment with a new key inserts a pair:

```python
inventory = {"PUMP": 12}
inventory["VALVE"] = 8

assert inventory == {"PUMP": 12, "VALVE": 8}
```

Assignment with an existing key replaces its value:

```python
inventory["PUMP"] = 15
assert inventory["PUMP"] == 15
```

To add to the current quantity:

```python
inventory["PUMP"] = inventory["PUMP"] + 4
assert inventory["PUMP"] == 19
```

The shorter augmented assignment is equivalent for this integer value:

```python
inventory["PUMP"] += 1
assert inventory["PUMP"] == 20
```

## 8. Membership and optional lookup

The `in` operator tests keys:

```python
inventory = {"PUMP": 12, "VALVE": 8}

assert "PUMP" in inventory
assert "MOTOR" not in inventory
```

Use `get()` when a missing key has an expected default:

```python
seal_quantity = inventory.get("SEAL", 0)
assert seal_quantity == 0
```

`get()` does not insert the missing key:

```python
assert "SEAL" not in inventory
```

Choose based on the contract:

| Situation | Operation |
| --- | --- |
| Missing key is an error | `dictionary[key]` |
| Missing key should use a default | `dictionary.get(key, default)` |
| Program only needs to check existence | `key in dictionary` |

## 9. Removing entries

`del` removes a pair by key:

```python
inventory = {"PUMP": 12, "VALVE": 8}
del inventory["VALVE"]

assert inventory == {"PUMP": 12}
```

`pop()` removes a pair and returns its value:

```python
removed_quantity = inventory.pop("PUMP")

assert removed_quantity == 12
assert inventory == {}
```

Both operations need a valid key unless a default is supplied to `pop()`.

## 10. Iterating through a dictionary

Direct iteration visits keys:

```python
inventory = {"PUMP": 12, "VALVE": 8}
codes = []

for code in inventory:
    codes.append(code)

assert codes == ["PUMP", "VALVE"]
```

Use `.values()` when only values are needed:

```python
total_quantity = 0

for quantity in inventory.values():
    total_quantity += quantity

assert total_quantity == 20
```

Use `.items()` for both key and value:

```python
records = []

for code, quantity in inventory.items():
    records.append(f"{code}: {quantity}")

assert records == ["PUMP: 12", "VALVE: 8"]
```

Each item behaves like a two-element tuple and can be unpacked.

## 11. Building a quantity dictionary

A common pattern accumulates repeated records:

```python
receipts = [
    ("BOLT", 12),
    ("NUT", 8),
    ("BOLT", 7),
    ("NUT", 4),
]

inventory = {}

for item, quantity in receipts:
    inventory[item] = inventory.get(item, 0) + quantity

assert inventory == {"BOLT": 19, "NUT": 12}
```

Loop invariant:

> After processing the first `k` records, `inventory[item]` equals the sum of the processed quantities for that item.

The invariant explains why the algorithm is correct at each iteration, not only for the final example.

## 12. Dictionary keys

Dictionary keys must be hashable. For the current course level, use immutable key types such as:

- strings;
- integers;
- tuples containing immutable elements.

Lists and dictionaries cannot be keys because their contents can change.

```python
station_status = {
    ("Line A", 1): "ACTIVE",
    ("Line A", 2): "MAINTENANCE",
}

assert station_status[("Line A", 2)] == "MAINTENANCE"
```

Use keys with stable domain meaning. A product code is usually clearer than a temporary numeric position.

## 13. Nested dictionaries

A dictionary value can be another dictionary:

```python
production = {
    "Line A": {
        "good": 480,
        "defective": 12,
    },
    "Line B": {
        "good": 510,
        "defective": 8,
    },
}

assert production["Line B"]["good"] == 510
```

Nested mappings model hierarchical relationships. Each lookup moves one level deeper.

## 14. What recursion means

Recursion is a technique in which a function calls itself on a smaller instance of the same problem [2].

A correct recursive solution normally contains:

1. a **base case** that returns a result directly;
2. a **recursive case** that calls the function with a smaller problem;
3. a **progress measure** that moves toward the base case;
4. a **combination step** that forms the current result.

The objective is not repeated self-calling. The objective is reducing a problem until a directly solvable case is reached.

## 15. First recursive function

```python
def sum_from_one(number):
    """Return 1 + 2 + ... + number for a non-negative integer."""
    if number == 0:
        return 0
    return number + sum_from_one(number - 1)


assert sum_from_one(0) == 0
assert sum_from_one(4) == 10
```

Analysis:

| Part | Code |
| --- | --- |
| Base case | `if number == 0: return 0` |
| Recursive case | `sum_from_one(number - 1)` |
| Progress measure | `number` decreases by one |
| Combination | current `number` plus smaller result |

The precondition is that `number` is a non-negative integer.

## 16. Tracing recursive calls

For `sum_from_one(3)`:

```text
sum_from_one(3)
    -> 3 + sum_from_one(2)
           -> 2 + sum_from_one(1)
                  -> 1 + sum_from_one(0)
                         -> 0
                  <- 1 + 0 = 1
           <- 2 + 1 = 3
    <- 3 + 3 = 6
```

Calls expand until the base case. Returned values then combine in reverse order.

Each active call has its own local parameter value.

<!-- TODO(media): Add an animation of recursive calls expanding and returned values collapsing for sum_from_one(3). Suggested path: ../Assets/Module-6/recursive-call-stack.gif -->

## 17. Recursion requires progress

This function does not progress:

```text
def broken_countdown(number):
    if number == 0:
        return
    broken_countdown(number)
```

The recursive argument is unchanged. The function does not reach its base case for a positive input.

Correct form:

```python
def countdown(number):
    if number == 0:
        return [0]
    return [number] + countdown(number - 1)


assert countdown(3) == [3, 2, 1, 0]
```

Before writing recursive code, answer:

- What input is directly solvable?
- What input becomes smaller?
- Why must every valid call eventually reach the base case?

## 18. Recursive package counting

Suppose one package holds at most `capacity` units. The number of packages can be calculated by repeatedly removing one full capacity.

```python
def count_packages(units, capacity):
    """Return packages needed for non-negative units and positive capacity."""
    if units == 0:
        return 0
    if units <= capacity:
        return 1
    return 1 + count_packages(units - capacity, capacity)


assert count_packages(0, 10) == 0
assert count_packages(10, 10) == 1
assert count_packages(11, 10) == 2
assert count_packages(27, 10) == 3
```

There are two base cases:

- zero units require zero packages;
- a positive quantity not exceeding capacity requires one package.

For larger quantities, each call removes one package capacity.

## 19. Recursion versus iteration

The same package calculation can use a loop:

```python
def count_packages_iterative(units, capacity):
    packages = 0

    while units > 0:
        packages += 1
        units -= capacity

    return packages


assert count_packages_iterative(27, 10) == 3
```

Prefer iteration when state changes in a simple linear process. Prefer recursion when the data or problem is naturally defined in smaller instances of itself.

Python limits interpreter recursion depth to protect the stack [3]. Recursion is therefore not appropriate for arbitrarily deep input.

## 20. Recursive structures

A hierarchical structure contains smaller structures of the same form. A bill of materials can represent an assembly as a list of component tuples:

```python
bill_of_materials = {
    "pump_unit": [
        ("motor_assembly", 1),
        ("housing", 1),
        ("seal", 2),
    ],
    "motor_assembly": [
        ("coil", 2),
        ("shaft", 1),
    ],
}
```

Interpretation:

- one `pump_unit` requires one `motor_assembly`, one `housing`, and two `seal` items;
- one `motor_assembly` requires two `coil` items and one `shaft`;
- a name absent from the dictionary is treated as a raw material.

This structure is recursive because an assembly can contain another assembly.

## 21. Recursive bill of materials expansion

```python
def expand_requirements(item, quantity, bill_of_materials):
    """Return raw-material quantities for an item and positive quantity."""
    if item not in bill_of_materials:
        return {item: quantity}

    totals = {}

    for component, amount_per_item in bill_of_materials[item]:
        component_quantity = quantity * amount_per_item
        component_totals = expand_requirements(
            component,
            component_quantity,
            bill_of_materials,
        )

        for material, amount in component_totals.items():
            totals[material] = totals.get(material, 0) + amount

    return totals


requirements = expand_requirements("pump_unit", 2, bill_of_materials)

assert requirements == {
    "coil": 4,
    "shaft": 2,
    "housing": 2,
    "seal": 4,
}
```

Base case:

```text
item is not an assembly key -> return the raw item and required quantity
```

Recursive case:

```text
item is an assembly -> expand every component and merge its raw-material totals
```

Progress depends on a finite acyclic bill of materials. Cycle detection is outside this module. A real production system must reject relationships such as assembly A requiring B while B requires A.

<!-- TODO(media): Add a tree animation that expands two pump units into raw-material totals. Suggested path: ../Assets/Module-6/bom-expansion.mp4 -->

## 22. Technical extension: memoization

Some recursive functions solve the same smaller input many times. Memoization stores a completed result in a dictionary and reuses it.

Conceptual pattern:

```python
def solve(problem, cache):
    if problem in cache:
        return cache[problem]

    result = solve_smaller_problem(problem)
    cache[problem] = result
    return result
```

Memoization is correct only when the cache key includes every input that affects the result. Performance analysis and memoized Fibonacci are developed in Module 10.

## 23. Common failure modes

### 23.1 Looking up a missing key

`dictionary[key]` raises `KeyError` if the key is absent. Test membership or use `get()` when absence is expected.

### 23.2 Testing values instead of keys

`item in dictionary` checks keys, not values.

### 23.3 Replacing instead of accumulating

For repeated records, use the previous quantity plus the new quantity.

### 23.4 Mutating dictionary size during iteration

Adding or removing keys during direct iteration can fail. Build a separate result or iterate over a snapshot.

### 23.5 Missing a recursive base case

Every valid recursive path must reach a directly returned result.

### 23.6 Recursive call does not become smaller

Identify a progress measure and verify that it decreases on every recursive path.

### 23.7 Ignoring invalid recursive input

State preconditions. A recursion designed for non-negative integers may not terminate for negative values.

### 23.8 Cyclic hierarchical data

A cyclic structure can revisit the same item indefinitely. The bill of materials study case assumes no cycles.

## 24. Guided practice

### 24.1 Dictionary state trace

Record the dictionary after each statement:

```python
inventory = {}
inventory["BOLT"] = 10
inventory["NUT"] = 5
inventory["BOLT"] += 4
```

### 24.2 Quantity accumulator

Complete a loop that converts this list into `{"A": 7, "B": 3}`:

```python
records = [("A", 2), ("B", 3), ("A", 5)]
```

### 24.3 Recursive trace

Trace `count_packages(23, 10)`. Record the arguments of every call and the returned value.

### 24.4 Base-case design

State the base case, progress measure, and precondition for a recursive function that returns `1 + 2 + ... + n`.

## 25. Independent practice

### Exercise 1: Frequency dictionary

Create a function that counts how many times each machine code appears in a list.

### Exercise 2: Inventory accumulation

Create a function that converts `(item, quantity)` records into a quantity dictionary.

### Exercise 3: Recursive list total

Return the sum of a list recursively. The empty list returns zero.

### Exercise 4: Package planner

For each item in an inventory dictionary, calculate the number of packages required from a capacity dictionary.

### Exercise 5: Bill of materials trace

Trace the recursive expansion of one `pump_unit`. List every function call and the dictionary it returns.

## 26. Knowledge check

1. What relationship does a dictionary store?
2. What happens when a value is assigned to an existing key?
3. What does `key in dictionary` test?
4. How do subscription and `get()` differ for a missing key?
5. What does `.items()` provide during iteration?
6. What are the required parts of a recursive solution?
7. Why does `sum_from_one(number - 1)` make progress?
8. What is the base case in bill of materials expansion?
9. Why can a cycle prevent recursive termination?
10. When is iteration preferable to recursion in Python?

<details>
<summary>Answer key</summary>

1. It maps unique keys to values.
2. The previous value for that key is replaced.
3. Whether the key exists.
4. Subscription raises `KeyError`; `get()` returns `None` or a supplied default.
5. Key-value pairs that can be unpacked into two names.
6. A base case, smaller recursive input, progress toward termination, and result combination.
7. The non-negative integer decreases by one and approaches zero.
8. An item absent from the assembly dictionary is a raw material and returns directly.
9. A path may revisit the same item instead of reaching a raw material.
10. When state progresses linearly, depth may be large, or an explicit loop is clearer.

</details>

## 27. Module synthesis

Dictionary reasoning:

```text
choose meaningful keys
    -> define value meaning
    -> select missing-key behavior
    -> update or accumulate
    -> iterate without unsafe structural mutation
```

Recursive reasoning:

```text
define the base case
    -> define a smaller problem
    -> prove progress
    -> combine returned results
    -> trace representative and boundary inputs
```

Dictionaries organize relationships. Recursion processes self-similar problems. A hierarchical bill of materials uses both: the dictionary records assembly relationships, and recursion follows those relationships until raw materials are reached.

## References

1. Python Software Foundation. "Data Structures." *The Python Tutorial*, Python 3.14.7 documentation. Accessed 25 September 2026. https://docs.python.org/3/tutorial/datastructures.html
2. Grimson, Eric. "Lecture 6: Recursion and Dictionaries." *MIT OpenCourseWare 6.0001: Introduction to Computer Science and Programming in Python*, Fall 2016. Accessed 25 September 2026. https://live.ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/resources/lecture-6-recursion-and-dictionaries/
3. Python Software Foundation. "sys.getrecursionlimit()." *Python 3 Standard Library*. Accessed 25 September 2026. https://docs.python.org/3/library/sys.html#sys.getrecursionlimit

---

**Previous module:** Module 5: Tuples, Lists, and Aliasing

**Next module:** Module 7: Testing, Debugging, and Exceptions
