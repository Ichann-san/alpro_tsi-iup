# Module 6 — Recursion and Dictionaries

> **Course:** Algorithms and Programming  
> **Programming language:** Python  
> **Supported runtime:** Python 3.10 or later  
> **Resource type:** Technical learning module  
> **Practical notebook:** Deferred to `../Practice/Modul_4-6.ipynb`  
> **Estimated study time:** 4 hours

## 1. Module scope

Recursion defines a result in terms of smaller instances of the same problem. A correct recursive function requires terminating base cases, progress toward them, and a valid composition rule. Dictionaries implement key-based mappings and are frequently used to store recursive subproblem results, represent sparse relationships, and index structured data.

This module covers call-stack reasoning, recurrence relations, recursive structure traversal, dictionary contracts, key requirements, views, and memoization.

<!-- TODO(media): Add an animation showing recursive calls expanding into stack frames and then returning values in reverse order. Suggested path: ../Assets/Module-6/recursion-call-stack.mp4 -->

## 2. Learning outcomes

After completing this module, a student should be able to:

1. **Specify** recursive base cases, recursive cases, and a decreasing problem measure.
2. **Trace** call frames and return-value composition.
3. **Derive** simple time and space recurrences.
4. **Recognize** repeated-subproblem recursion and apply dictionary memoization.
5. **Construct** dictionaries and use key-based access, update, deletion, iteration, and views.
6. **Explain** hashability, key equality, insertion order, and missing-key behaviour.
7. **Traverse** nested dictionary structures recursively.
8. **Diagnose** missing base cases, non-progressing calls, mutable keys, and unintended dictionary insertion.

## 3. Recursion model

NIST defines recursion as an algorithmic technique in which a function calls itself on part of a task [1]. A recursive specification normally contains:

1. **base case:** solve a minimal instance directly;
2. **decomposition:** reduce the current instance to smaller instances;
3. **recursive call:** solve those instances;
4. **composition:** combine returned results; and
5. **progress measure:** prove that every call moves toward a base case.

### 3.1 Factorial

For non-negative integer `n`:

```text
0! = 1
n! = n × (n - 1)!    for n > 0
```

```python
def factorial(n):
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")
    if n == 0:
        return 1
    return n * factorial(n - 1)


print(factorial(5))
assert factorial(0) == 1
assert factorial(5) == 120
```

Expected output:

```text
120
```

The progress measure is `n`. Each recursive call reduces it by one, and it is bounded below by zero.

## 4. Call-stack trace

A function call creates a new execution frame containing its local bindings and return position [2].

For `factorial(4)`:

```text
factorial(4)
  4 * factorial(3)
        3 * factorial(2)
              2 * factorial(1)
                    1 * factorial(0)
                          return 1
                    return 1
              return 2
        return 6
  return 24
```

Expansion proceeds toward the base case. Composition proceeds as frames return.

Recursive auxiliary space is proportional to maximum active call depth. The factorial implementation uses `Θ(n)` active frames.

<!-- TODO(media): Add a synchronized animation of the factorial recursion tree, active call stack, local n values, and return multiplication. Suggested path: ../Assets/Module-6/factorial-stack.gif -->

## 5. Recursive correctness

A proof by induction matches recursive structure:

1. **Base:** show the function is correct for each base case.
2. **Inductive hypothesis:** assume recursive calls correctly solve smaller valid inputs.
3. **Step:** show decomposition and composition produce the correct result for the current input.
4. **Termination:** show a well-founded measure decreases on every recursive path.

Correct base output alone does not prove termination. Every recursive branch must make progress.

Incorrect:

```python
def countdown(n):
    if n == 0:
        return
    countdown(n)  # no progress
```

The function repeats the same state until Python raises `RecursionError`.

## 6. Structural recursion

Recursive data structures contain smaller instances of themselves. Nested lists and trees are natural inputs for structural recursion.

```python
def nested_sum(value):
    if isinstance(value, int):
        return value
    return sum(nested_sum(item) for item in value)


data = [1, [2, 3], [[4], 5]]
result = nested_sum(data)

print(result)
assert result == 15
```

Contract:

- valid input is an integer or a finite list of valid inputs;
- integer is the base representation;
- list composition is summation; and
- cyclic lists are outside the contract.

A cyclic structure would not progress toward a leaf without explicit visited-state tracking.

## 7. Recurrence relations

A recurrence expresses cost in terms of smaller inputs.

For factorial:

```text
T(0) = Θ(1)
T(n) = T(n - 1) + Θ(1)
Therefore T(n) = Θ(n)
```

For a recursive function that makes two calls on size `n/2` and performs linear combination work:

```text
T(n) = 2T(n/2) + Θ(n)
```

Its solution is `Θ(n log n)`. Module 10 develops recurrence analysis in more detail.

### 7.1 Repeated subproblems

Naive Fibonacci recursion recomputes the same inputs:

```python
def fibonacci(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


assert fibonacci(10) == 55
```

The call tree grows exponentially because subproblems overlap. A dictionary can cache results.

## 8. Python recursion limits

Python exposes an interpreter recursion limit, which protects the underlying stack from unbounded recursion [3]. Deep valid inputs can still raise `RecursionError`.

```python
import sys

limit = sys.getrecursionlimit()
print(limit > 0)
assert isinstance(limit, int)
assert limit > 0
```

Expected output:

```text
True
```

Do not increase the limit as a routine fix. Prefer iteration or an explicit stack when depth can scale with uncontrolled input. Changing the limit is implementation-sensitive and can risk interpreter failure if set excessively high [3].

## 9. Dictionary contract

A dictionary is a mutable mapping from unique hashable keys to values [4].

Core operations:

| Operation | Behaviour |
| --- | --- |
| `d[key]` | Return value; raise `KeyError` if absent |
| `d[key] = value` | Insert or replace |
| `del d[key]` | Delete; raise `KeyError` if absent |
| `key in d` | Test key membership |
| `d.get(key, default)` | Return value or default without insertion |
| `d.setdefault(key, default)` | Return value; insert default if absent |
| `d.pop(key)` | Remove and return value |
| `d.keys()` / `values()` / `items()` | Return dynamic view objects |

```python
credits = {"Algorithms": 4, "Databases": 3}
credits["Networks"] = 3
credits["Algorithms"] = 5

print(credits["Algorithms"])
print("Networks" in credits)

assert credits == {"Algorithms": 5, "Databases": 3, "Networks": 3}
```

Python dictionaries preserve insertion order [2]. Replacing an existing key does not move it; deleting and reinserting places it at the end.

## 10. Keys and hashability

A dictionary uses a key's hash and equality behaviour. A key must be hashable, which normally requires an immutable equality-relevant state [2].

Valid common keys:

- strings;
- numbers;
- tuples whose items are hashable;
- frozen sets; and
- appropriately designed immutable user objects.

Lists and dictionaries are not valid keys.

```python
locations = {
    (0, 0): "origin",
    (2, 5): "checkpoint",
}

assert locations[(2, 5)] == "checkpoint"

try:
    locations[[2, 5]] = "invalid"
except TypeError as error:
    print(type(error).__name__)
```

Expected output:

```text
TypeError
```

Numeric keys that compare equal, such as `1` and `1.0`, identify the same dictionary entry [2].

## 11. Missing-key policies

Choose policy from domain semantics.

### 11.1 Required key

Use `d[key]` when absence is an error.

### 11.2 Optional read

Use `d.get(key)` or `d.get(key, default)` when absence is expected and does not require insertion.

### 11.3 Initialize on demand

`setdefault()` can initialize a mutable accumulator:

```python
groups = {}

for course, level in [("Algorithms", 2), ("Databases", 2), ("AI", 3)]:
    groups.setdefault(level, []).append(course)

print(groups)
assert groups == {2: ["Algorithms", "Databases"], 3: ["AI"]}
```

For frequent grouping, `collections.defaultdict` can make the initialization policy explicit.

Do not use `get()` when stored `None` and absence must be distinguished; test membership or use a unique sentinel.

## 12. Dictionary views and iteration

`keys()`, `values()`, and `items()` return dynamic views that reflect later dictionary changes [4].

```python
scores = {"A": 80, "B": 90}
items_view = scores.items()

scores["C"] = 85

print(list(items_view))
assert list(items_view) == [("A", 80), ("B", 90), ("C", 85)]
```

Changing dictionary size during direct iteration can raise `RuntimeError`. Iterate over `list(d.items())` or build a new dictionary when structural mutation is required.

Dictionary comprehensions construct mappings:

```python
squares = {value: value * value for value in range(1, 5)}
assert squares == {1: 1, 2: 4, 3: 9, 4: 16}
```

If two generated items have equal keys, the later value replaces the earlier value.

## 13. Frequency indexing

```python
tokens = ["data", "code", "data", "test", "code", "data"]
frequency = {}

for token in tokens:
    frequency[token] = frequency.get(token, 0) + 1

print(frequency)
assert frequency == {"data": 3, "code": 2, "test": 1}
```

Invariant:

> After processing the first `k` tokens, `frequency[x]` equals the number of occurrences of `x` among those `k` tokens.

For production frequency counting, `collections.Counter` provides a specialized mapping. The explicit loop reveals the invariant.

## 14. Memoization

**Memoization** stores the result of a deterministic subproblem and reuses it when the same key appears again.

```python
def fibonacci_memoized(n, cache=None):
    if n < 0:
        raise ValueError("n must be non-negative")
    if cache is None:
        cache = {0: 0, 1: 1}
    if n not in cache:
        cache[n] = (
            fibonacci_memoized(n - 1, cache)
            + fibonacci_memoized(n - 2, cache)
        )
    return cache[n]


print(fibonacci_memoized(30))
assert fibonacci_memoized(30) == 832040
```

Each integer subproblem from `0` through `n` is computed once. Time becomes `Θ(n)` and cache space is `Θ(n)`, excluding call-stack space.

Memoization is valid only when the cache key captures every input that affects the result and external mutable state does not invalidate cached values.

<!-- TODO(media): Add a side-by-side call-tree animation for naive and memoized Fibonacci, highlighting cache hits and eliminated subtrees. Suggested path: ../Assets/Module-6/fibonacci-memoization.mp4 -->

## 15. Recursive dictionary traversal

Nested dictionaries can represent hierarchical configuration:

```python
def count_leaves(node):
    if not isinstance(node, dict):
        return 1
    return sum(count_leaves(value) for value in node.values())


configuration = {
    "service": {
        "host": "localhost",
        "ports": {"http": 80, "https": 443},
    },
    "debug": False,
}

print(count_leaves(configuration))
assert count_leaves(configuration) == 4
```

The dictionary case recursively visits child values. Every non-dictionary value is a leaf. This is a domain-specific definition; a list inside the structure would count as one leaf unless the contract is extended.

## 16. Recursion versus iteration

Prefer recursion when:

- the input is recursively defined;
- recursive decomposition mirrors the correctness argument;
- maximum depth is safely bounded; and
- composition is clearer than explicit stack management.

Prefer iteration or an explicit stack when:

- input depth may be large or adversarial;
- state progresses linearly;
- Python call overhead matters; or
- the iterative invariant is simpler.

Equivalent factorial:

```python
def factorial_iterative(n):
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")
    result = 1
    for value in range(2, n + 1):
        result *= value
    return result


assert factorial_iterative(5) == 120
```

This uses constant auxiliary space under the ordinary scalar-variable model.

## 17. Common failure modes

### 17.1 Missing or unreachable base case

Prove which inputs reach each base case.

### 17.2 Non-decreasing recursive argument

Every path must reduce a well-founded measure.

### 17.3 Exponential repeated work

Draw the call tree and identify repeated subproblem keys. Memoize only when results are stable.

### 17.4 Assuming recursion is unlimited

Python limits interpreter recursion depth [3].

### 17.5 Using a mutable key

Mutable value-based keys cannot provide a stable hash.

### 17.6 Confusing absent with stored `None`

Use membership or a unique sentinel when the distinction matters.

### 17.7 Mutating size during iteration

Iterate over a snapshot or construct a result mapping.

### 17.8 Cache key omits relevant state

An incomplete memoization key can return an incorrect stale result.

## 18. Guided practice

### 18.1 Recursion trace

Trace `factorial(4)` with one row per call frame. Record argument, pending operation, and returned value.

### 18.2 Nested structure

Trace `nested_sum([1, [2, [3]]])`. Identify every base case and composition.

### 18.3 Dictionary state

Starting from `{"A": 1}`, trace insertion, replacement, `setdefault()`, and deletion. Record key order after each step.

## 19. Independent practice

### Exercise 1 — Recursive power

Implement exponentiation by repeated squaring for non-negative integer exponents:

```text
x^(2k) = (x^k)^2
x^(2k+1) = x × (x^k)^2
```

**Deliverable:** code, base case, progress measure, and recurrence.

### Exercise 2 — Recursive maximum

Return the maximum integer in a non-empty list using recursion.

**Constraints:** no `max()`; define empty-input failure.

### Exercise 3 — Inverted index

Given document tokens, construct a dictionary mapping each token to a list of positions at which it occurs.

**Expected input:** `["a", "b", "a"]`.  
**Expected result:** `{"a": [0, 2], "b": [1]}`.

### Exercise 4 — Nested configuration paths

Recursively return leaf paths from a nested dictionary as tuples.

For `{"db": {"host": "localhost", "port": 5432}}`, include `("db", "host")` and `("db", "port")`.

### Exercise 5 — Memoization audit

Compare call counts for naive and memoized Fibonacci at `n = 20`. Count calls without relying on execution time.

## 20. Knowledge check

1. What are the required parts of a recursive solution?
2. Why does factorial recursion terminate for non-negative integers?
3. What resource grows with recursive call depth?
4. What makes a valid dictionary key?
5. How do `d[key]` and `d.get(key)` differ?
6. Are dictionary views snapshots?
7. What condition makes memoization semantically valid?
8. Why can nested recursive input require cycle detection?

<details>
<summary>Answer key</summary>

1. Base case, smaller recursive subproblem, recursive call, composition, and progress argument.
2. `n` decreases by one and is bounded below by zero.
3. Active call-stack space.
4. Stable hashability and equality compatible with the hash.
5. Subscription raises `KeyError` when absent; `get()` returns a default without insertion.
6. No. They dynamically reflect mapping changes.
7. The key captures all result-determining input and cached results remain valid.
8. A cycle may revisit the same object indefinitely instead of reaching a leaf.

</details>

## 21. Module synthesis

Recursive reasoning:

```text
base cases
    -> smaller subproblems
    -> recursive results
    -> composition
    -> termination and cost recurrence
```

Dictionary reasoning:

```text
key contract
    -> lookup/update policy
    -> missing-key policy
    -> iteration and mutation policy
```

Dictionaries complement recursion by indexing subproblems and representing nested or sparse relationships. They do not repair an invalid recurrence; prove correctness and cache validity separately.

## References

1. Black, P. E., and P. Rodgers. “Recursion.” *Dictionary of Algorithms and Data Structures*, National Institute of Standards and Technology, modified 30 September 2013. Accessed 31 August 2026. https://www.nist.gov/dads/HTML/recursion.html
2. Python Software Foundation. “Data Model: Objects, Values and Types.” *Python Language Reference*. Accessed 31 August 2026. https://docs.python.org/3/reference/datamodel.html
3. Python Software Foundation. “`sys.getrecursionlimit()`.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/sys.html#sys.getrecursionlimit
4. Python Software Foundation. “Mapping Types — `dict`.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/stdtypes.html#mapping-types-dict

---

**Previous module:** Module 5 — Tuples, Lists, and Aliasing  
**Next module:** Module 7 — Testing, Debugging, and Exceptions
