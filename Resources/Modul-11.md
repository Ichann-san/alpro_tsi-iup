# Module 11 — Searching Algorithms

> **Course:** Algorithms and Programming  
> **Programming language:** Python  
> **Supported runtime:** Python 3.10 or later  
> **Resource type:** Technical learning module  
> **Practical notebook:** Deferred to `../Practice/Modul_10-11.ipynb`  
> **Estimated study time:** 4 hours

## 1. Module scope

Searching locates an item or boundary within a data structure. Algorithm selection depends on representation, ordering, update frequency, duplicate policy, result contract, and query volume. Linear search works without ordering. Binary search reduces a sorted indexed interval by half. Hash-based mappings and sets provide a different key-membership trade-off.

This module derives search algorithms from invariants and specifies duplicate and absence semantics explicitly.

<!-- TODO(media): Add a side-by-side animation of linear search scanning items and binary search shrinking a half-open interval. Show comparison counts. Suggested path: ../Assets/Module-11/linear-vs-binary-search.mp4 -->

## 2. Learning outcomes

After completing this module, a student should be able to:

1. **Specify** a search contract including equality, duplicates, absence, and result form.
2. **Implement and trace** linear search.
3. **State and preserve** a half-open interval invariant for binary search.
4. **Implement** exact binary search without off-by-one errors.
5. **Use** `bisect_left()` and `bisect_right()` for insertion boundaries.
6. **Compare** linear, binary, and hash-based searching under stated workloads.
7. **Calculate** best-, worst-, and relevant average-case costs.
8. **Test** empty, singleton, boundary, absent, and duplicate cases.
9. **Diagnose** invalid sortedness assumptions and result-contract ambiguity.

## 3. Search contract

Before choosing an algorithm, define:

| Contract element | Example decision |
| --- | --- |
| Collection | Finite sequence of course codes |
| Target relation | String equality |
| Result | First matching index |
| Absence | `-1` |
| Duplicate policy | Return lowest index |
| Mutation | No mutation |
| Preconditions | None for linear search; non-decreasing order for binary search |

Other valid results include:

- Boolean membership;
- matching item;
- every matching position;
- insertion point;
- predecessor or successor; and
- raised exception on absence.

Two search functions with different duplicate policies are not interchangeable.

## 4. Linear search

Linear search examines items one at a time [1].

```python
def linear_search(values, target):
    """Return the first index equal to target, or -1 when absent."""
    for index, value in enumerate(values):
        if value == target:
            return index
    return -1


values = [8, 3, 5, 3, 9]

print(linear_search(values, 3))
assert linear_search(values, 3) == 1
assert linear_search(values, 9) == 4
assert linear_search(values, 7) == -1
assert linear_search([], 7) == -1
```

Expected output:

```text
1
```

### 4.1 Loop invariant

Before iteration at index `i`:

> No position in `values[0:i]` contains an item equal to `target`.

If `values[i] == target`, `i` is therefore the first matching position. If iteration ends, no position contains the target.

### 4.2 Cost

For `n` items:

- best case: `Θ(1)` when the first item matches;
- worst case: `Θ(n)` when absent or last;
- average successful case under a uniform target-position model: `Θ(n)`; and
- auxiliary space: `Θ(1)`.

The average model must be stated. It is not a property of syntax alone.

## 5. Binary-search precondition

Binary search operates on a sorted indexed sequence and repeatedly halves the candidate interval [2].

For ascending order:

```text
values[i] <= values[i + 1]    for every valid adjacent pair
```

If the precondition is false, binary search may return absence for an existing item. It does not normally detect unsorted input.

Sorting once costs approximately `Θ(n log n)` for comparison sorting. That preprocessing cost may be justified for many searches over stable data, but not necessarily for one query.

## 6. Exact binary search

Use a half-open interval `[low, high)`:

- `low` is included;
- `high` is excluded;
- initial interval is `[0, len(values))`; and
- empty interval is `low == high`.

```python
def binary_search(values, target):
    """Return an index equal to target, or -1 when absent.

    Precondition: values is sorted in non-decreasing order.
    Duplicate policy: any matching index may be returned.
    """
    low = 0
    high = len(values)

    while low < high:
        middle = low + (high - low) // 2
        candidate = values[middle]

        if candidate == target:
            return middle
        if candidate < target:
            low = middle + 1
        else:
            high = middle

    return -1


values = [2, 5, 8, 12, 16, 23, 38]

assert binary_search(values, 2) == 0
assert binary_search(values, 12) == 3
assert binary_search(values, 38) == 6
assert binary_search(values, 7) == -1
assert binary_search([], 7) == -1
```

### 6.1 Interval invariant

At loop start:

> If `target` occurs in the sequence and has not been returned, at least one matching position lies in `[low, high)`.

Transitions:

- if `values[middle] < target`, positions through `middle` cannot match, so set `low = middle + 1`;
- if `values[middle] > target`, positions from `middle` onward cannot match, so set `high = middle`.

Each transition strictly reduces `high - low`. This proves termination.

### 6.2 Trace

Search for `16` in `[2, 5, 8, 12, 16, 23, 38]`:

| Iteration | `low` | `high` | `middle` | candidate | Action |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 0 | 7 | 3 | 12 | `low = 4` |
| 2 | 4 | 7 | 5 | 23 | `high = 5` |
| 3 | 4 | 5 | 4 | 16 | return `4` |

<!-- TODO(media): Add an interval animation for the trace, clearly marking [low, high), discarded regions, and middle. Suggested path: ../Assets/Module-11/binary-search-interval.gif -->

## 7. Binary-search cost

After `k` unsuccessful reductions, interval length is at most approximately:

```text
n / 2ᵏ
```

The interval becomes empty when `2ᵏ > n`, so comparison count is `Θ(log n)`. Auxiliary space for the iterative implementation is `Θ(1)`.

This time bound relies on efficient indexed access. Applying the comparison strategy to a linked list can require linear traversal to locate each middle element.

## 8. Duplicate policy

Exact binary search can return any equal index. To find the first equal position, search for the left insertion boundary.

```python
def lower_bound(values, target):
    """Return first index i for which values[i] >= target."""
    low = 0
    high = len(values)

    while low < high:
        middle = low + (high - low) // 2
        if values[middle] < target:
            low = middle + 1
        else:
            high = middle

    return low


values = [1, 3, 3, 3, 8]

assert lower_bound(values, 3) == 1
assert lower_bound(values, 2) == 1
assert lower_bound(values, 9) == 5
```

Postcondition:

```text
all items before result are < target
all items at or after result are >= target
```

Exact first-match search:

```python
def binary_search_first(values, target):
    index = lower_bound(values, target)
    if index < len(values) and values[index] == target:
        return index
    return -1


assert binary_search_first([1, 3, 3, 3, 8], 3) == 1
assert binary_search_first([1, 3, 3, 3, 8], 4) == -1
```

## 9. Standard-library bisection

The `bisect` module maintains sorted order and returns insertion points [3].

```python
from bisect import bisect_left, bisect_right, insort

values = [1, 3, 3, 3, 8]

left = bisect_left(values, 3)
right = bisect_right(values, 3)

print(left, right)
assert (left, right) == (1, 4)
assert values[left:right] == [3, 3, 3]

insort(values, 5)
assert values == [1, 3, 3, 3, 5, 8]
```

Expected output:

```text
1 4
```

`bisect_left()` and `bisect_right()` perform logarithmic search for a position. Inserting into a Python list remains `O(n)` because references after the insertion point must move [3].

The bisection functions use ordering comparisons to find boundaries; they do not call `__eq__()` to locate an exact value [3].

## 10. Search with a key function

Python 3.10+ bisection functions accept `key=` for extracting comparison keys [3].

```python
from bisect import bisect_left

records = [
    {"id": 10, "name": "A"},
    {"id": 20, "name": "B"},
    {"id": 40, "name": "C"},
]

position = bisect_left(records, 20, key=lambda record: record["id"])

assert position == 1
assert records[position]["name"] == "B"
```

The target `x` is compared to extracted keys; the key function is not applied to `x` [3]. For expensive keys or repeated searches, precompute a parallel key sequence or cache key results.

## 11. Linear, binary, and hash search

| Strategy | Precondition | Typical query cost | Update consideration | Order queries |
| --- | --- | ---: | --- | --- |
| Linear scan | None | `Θ(n)` worst case | No index maintenance | Works on any iterable |
| Binary search | Sorted indexed sequence | `Θ(log n)` | Preserve or rebuild order | Supports bounds and ranges |
| Hash set/dictionary | Hashable key | Expected `Θ(1)` | Hash index maintained on update | Does not provide sorted neighbours |

Choose from the workload:

- one search on small unsorted data: linear search may be sufficient;
- many exact searches on stable ordered data: binary search;
- frequent exact key membership with no range requirement: set or dictionary;
- predecessor, successor, or range boundary: ordered sequence plus bisection.

## 12. Preprocessing economics

Suppose:

- linear query costs proportional to `n`;
- sorting costs proportional to `n log n`; and
- each binary query costs proportional to `log n`.

For `q` queries:

```text
linear total: Θ(qn)
sort + binary total: Θ(n log n + q log n)
```

This asymptotic comparison omits constants and update costs. If the data changes between queries, maintaining sorted order becomes part of the workload.

## 13. Searching derived data

Avoid repeated transformation inside a search loop:

```python
def find_case_insensitive(values, target):
    normalized_target = target.casefold()
    for index, value in enumerate(values):
        if value.casefold() == normalized_target:
            return index
    return -1


assert find_case_insensitive(["Alpha", "BETA"], "beta") == 1
```

For many queries, build a normalized index once, while defining collision policy when distinct originals normalize to the same key.

## 14. Search testing matrix

Test at least:

| Case | Purpose |
| --- | --- |
| Empty input | Initial interval and absence |
| Singleton match | Minimal success |
| Singleton absence | Minimal failure |
| First item | Lower boundary |
| Last item | Upper boundary |
| Interior item | Ordinary success |
| Below minimum | Lower absent boundary |
| Above maximum | Upper absent boundary |
| Between items | Interior absence |
| Duplicates | Defined duplicate policy |

```python
def verify_search(search):
    assert search([], 4) == -1
    assert search([4], 4) == 0
    assert search([4], 3) == -1
    assert search([1, 2, 3], 1) == 0
    assert search([1, 2, 3], 3) == 2
    assert search([1, 2, 3], 4) == -1


verify_search(linear_search)
verify_search(binary_search)
```

Shared contract tests help compare implementations. Add implementation-specific precondition tests separately.

## 15. Common failure modes

### 15.1 Binary search on unsorted data

The algorithm can silently return an incorrect absence result.

### 15.2 Mixed interval conventions

Combining inclusive `high` with half-open update rules creates skipped items or out-of-range access.

### 15.3 No strict interval reduction

Updates such as `low = middle` can repeat the same state when two positions remain.

### 15.4 Undefined duplicate result

“Find the item” does not specify first, last, any, or all.

### 15.5 Sorting for one small query

Preprocessing may cost more than a scan.

### 15.6 Ignoring insertion cost

`insort()` has logarithmic search but linear list insertion [3].

### 15.7 Returning inconsistent absence forms

Mixing `-1`, `None`, and exceptions complicates callers.

### 15.8 Expensive key recomputation

Repeated key extraction can dominate comparison cost.

## 16. Guided practice

### 16.1 Linear invariant

Trace linear search for absent target `7` in `[2, 4, 6, 8]`. State the invariant before each comparison.

### 16.2 Binary trace

Trace `binary_search([2, 5, 8, 12, 16, 23, 38], 7)` with `low`, `high`, `middle`, and discarded interval.

### 16.3 Boundary selection

Use `bisect_left` and `bisect_right` to count values equal to `5` without scanning.

## 17. Independent practice

### Exercise 1 — Last occurrence

Implement `binary_search_last(values, target)`.

**Contract:** return highest matching index or `-1`.  
**Required tests:** empty, absent, one match, and repeated values.

### Exercise 2 — Range query

Return the half-open interval containing all values `low <= value < high` in a sorted sequence.

**Constraint:** use bisection boundaries.

### Exercise 3 — Comparison counting

Instrument linear and binary search to return both result and comparison count.

**Deliverable:** counts for successful and unsuccessful searches across increasing powers of two.

### Exercise 4 — Workload recommendation

Choose a strategy for:

```text
2,000,000 stable records
500,000 exact-ID queries per day
100 range queries per day
one nightly bulk rebuild
```

**Deliverable:** representation, algorithms, preprocessing cost, query costs, and one operational limitation.

## 18. Knowledge check

1. What belongs in a search contract?
2. What invariant proves linear search returns the first match?
3. What precondition enables binary search?
4. Why does a half-open interval simplify empty-state handling?
5. What guarantees binary-search termination?
6. How do `bisect_left` and `bisect_right` differ?
7. Why is `insort()` not `O(log n)` overall on a list?
8. When can linear search be preferable?

<details>
<summary>Answer key</summary>

1. Collection, match relation, result form, absence, duplicate policy, mutation, and preconditions.
2. No earlier processed position matches the target.
3. A sorted sequence with efficient indexed access for logarithmic time.
4. `low == high` directly represents an empty interval, and `len(values)` is a valid excluded bound.
5. Every iteration strictly decreases `high - low`.
6. Left returns the first valid insertion position before equals; right returns the position after existing equals.
7. Moving list elements for insertion costs linear time.
8. For small data, one or few queries, unsorted input, or iterables without efficient indexing.

</details>

## 19. Module synthesis

Search selection:

```text
result contract
    -> representation and ordering
    -> query/update workload
    -> algorithm invariant
    -> boundary and duplicate tests
    -> cost including preprocessing
```

Binary search is short code with a strict proof obligation. Keep one interval convention, prove each discarded region cannot contain the target, and define duplicate behaviour before implementation.

## References

1. Black, P. E. “Linear Search.” *Dictionary of Algorithms and Data Structures*, National Institute of Standards and Technology, modified 21 April 2022. Accessed 31 August 2026. https://www.nist.gov/dads/HTML/linearSearch.html
2. Black, P. E. “Binary Search.” *Dictionary of Algorithms and Data Structures*, National Institute of Standards and Technology, modified 21 April 2022. Accessed 31 August 2026. https://www.nist.gov/dads/HTML/binarySearch.html
3. Python Software Foundation. “`bisect` — Array Bisection Algorithm.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/bisect.html

---

**Previous module:** Module 10 — Program Efficiency  
**Next module:** Module 12 — Exploratory Data Analysis
