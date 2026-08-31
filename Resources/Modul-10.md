# Module 10 — Program Efficiency

> **Course:** Algorithms and Programming  
> **Programming language:** Python  
> **Supported runtime:** Python 3.10 or later  
> **Resource type:** Technical learning module  
> **Practical notebook:** Deferred to `../Practice/Modul_10-11.ipynb`  
> **Estimated study time:** 4 hours

## 1. Module scope

Efficiency analysis estimates how resource requirements grow with input size. It does not replace correctness, workload definition, or measurement. This module covers cost models, asymptotic bounds, case analysis, operation counting, recurrence reasoning, time–space trade-offs, Python benchmarking, profiling, and evidence-driven optimization.

The main discipline is to attach every efficiency claim to an operation, input-size definition, representation, and case.

<!-- TODO(media): Add an animated graph comparing constant, logarithmic, linear, n log n, quadratic, and exponential growth on the same axes. Include a non-logarithmic and logarithmic view. Suggested path: ../Assets/Module-10/growth-rates.mp4 -->

## 2. Learning outcomes

After completing this module, a student should be able to:

1. **Define** input size and a cost model for an algorithm.
2. **Distinguish** worst-case, average-case, best-case, and amortized analysis.
3. **Apply** `O`, `Ω`, and `Θ` notation correctly.
4. **Derive** costs for sequential, conditional, nested, and halving control flow.
5. **Formulate** and solve basic recurrences.
6. **Evaluate** time–space trade-offs and representation effects.
7. **Measure** small code fragments with `timeit` and whole-program call costs with `cProfile`.
8. **Interpret** timing and profiling evidence without overstating conclusions.
9. **Optimize** the dominant cost while preserving tested behaviour.

## 3. Cost model

An analysis must define:

- **input size:** such as number of elements `n`, vertices `|V|`, edges `|E|`, or text length;
- **basic operation:** comparison, assignment, arithmetic operation, hash lookup, byte transfer, or another relevant unit;
- **resource:** time, auxiliary memory, total memory, I/O, network requests, or energy;
- **case:** worst, average under a stated distribution, best, or amortized; and
- **representation assumptions:** array, linked structure, hash table, sorted input, and so on.

For a distributed service, network round trips may dominate local comparisons. For an in-memory search, comparison count may be a useful model.

## 4. Asymptotic bounds

Let `f(n)` be a non-negative cost and `g(n)` a comparison function.

### 4.1 Big O

`f(n) = O(g(n))` when fixed positive constants `c` and `n₀` exist such that:

```text
0 <= f(n) <= c g(n)    for every n >= n₀
```

Big O is an asymptotic upper bound [1].

### 4.2 Big Omega

`f(n) = Ω(g(n))` gives an asymptotic lower bound.

### 4.3 Big Theta

`f(n) = Θ(g(n))` when `g(n)` is both an asymptotic upper and lower bound for `f(n)` [2].

For:

```text
f(n) = 3n² + 5n + 8
```

the tight bound is `Θ(n²)`. It is also technically `O(n³)`, but that upper bound is not tight.

### 4.4 Growth order

```text
Θ(1)
Θ(log n)
Θ(n)
Θ(n log n)
Θ(n²)
Θ(n³)
Θ(2ⁿ)
Θ(n!)
```

Asymptotic analysis suppresses constant factors and lower-order terms. Those factors still affect observed runtime for finite inputs.

## 5. Case analysis

### 5.1 Worst case

Maximum resource use over valid inputs of size `n`. It supports upper-bound guarantees.

### 5.2 Average case

Expected cost under an explicit probability distribution. “Average” without a distribution is incomplete.

### 5.3 Best case

Minimum cost. It may be useful for understanding early exit but rarely provides a capacity guarantee.

### 5.4 Amortized cost

Average cost per operation over a sequence, without assuming random inputs. A dynamic array append can be normally cheap with occasional resize; amortized analysis spreads resize work across the sequence.

Do not interchange average-case and amortized analysis.

## 6. Sequential composition

For consecutive blocks:

```text
T(n) = T₁(n) + T₂(n)
```

The dominant asymptotic term determines a tight sum when costs are non-negative.

```python
def two_passes(values):
    total = 0
    for value in values:
        total += value

    positive_count = 0
    for value in values:
        if value > 0:
            positive_count += 1

    return total, positive_count


assert two_passes([2, -1, 4]) == (5, 2)
```

Two linear passes cost `Θ(n) + Θ(n) = Θ(n)`, not `Θ(n²)`.

## 7. Conditional cost

For:

```text
if condition:
    branch_a()
else:
    branch_b()
```

worst-case cost includes condition evaluation plus the more expensive feasible branch. If branch probability is modelled, expected cost weights each branch by its probability.

The number of source lines does not determine complexity. A one-line call can hide a linear or worse operation.

## 8. Loop counting

### 8.1 Linear loop

```python
def count_linear_work(n):
    operations = 0
    for _ in range(n):
        operations += 1
    return operations


assert count_linear_work(0) == 0
assert count_linear_work(10) == 10
```

Cost is `Θ(n)`.

### 8.2 Triangular nested loop

```python
def count_pairs(n):
    operations = 0
    for left in range(n):
        for right in range(left + 1, n):
            operations += 1
    return operations


for n in range(8):
    assert count_pairs(n) == n * (n - 1) // 2
```

```text
(n - 1) + (n - 2) + ... + 1 + 0
= n(n - 1)/2
= Θ(n²)
```

### 8.3 Halving loop

```python
def halving_steps(n):
    if n < 1:
        raise ValueError("n must be positive")
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps


assert halving_steps(1) == 0
assert halving_steps(8) == 3
assert halving_steps(10) == 3
```

The number of iterations is `⌊log₂ n⌋`, so time is `Θ(log n)`.

<!-- TODO(media): Add an animation comparing one-at-a-time decrement with repeated halving, including input sizes and iteration counts. Suggested path: ../Assets/Module-10/linear-vs-logarithmic.gif -->

## 9. Common summations

Useful patterns:

| Sum | Tight bound |
| --- | --- |
| `1 + 1 + ... + 1`, `n` terms | `Θ(n)` |
| `1 + 2 + ... + n` | `Θ(n²)` |
| `1 + 2 + 4 + ... + n` | `Θ(n)` |
| `n + n/2 + n/4 + ...` | `Θ(n)` |
| `log n` levels × `n` work per level | `Θ(n log n)` |

Count dependent loop bounds rather than multiplying all visible bounds mechanically.

## 10. Recurrence analysis

A recurrence expresses recursive cost.

### 10.1 Linear recursion

```text
T(0) = Θ(1)
T(n) = T(n - 1) + Θ(1)
T(n) = Θ(n)
```

### 10.2 Binary divide and combine

```text
T(1) = Θ(1)
T(n) = 2T(n/2) + Θ(n)
T(n) = Θ(n log n)
```

At each of `log₂ n` levels, total non-recursive combination work is `Θ(n)`.

### 10.3 Exponential branching

Naive Fibonacci approximately satisfies:

```text
T(n) = T(n - 1) + T(n - 2) + Θ(1)
```

Its call count grows exponentially. Memoization changes the algorithm by ensuring each distinct subproblem is evaluated once.

## 11. Time and space

### 11.1 Auxiliary space

Memory used beyond required input and output storage under the stated model.

### 11.2 Recursion stack

Recursive depth contributes active frame space. A linear-depth recursion uses `Θ(n)` stack space even when each frame stores constant local data.

### 11.3 Time–space trade-off

Caching can reduce repeated computation by storing results.

```python
def unique_preserving_order(values):
    seen = set()
    result = []

    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)

    return result


assert unique_preserving_order([3, 1, 3, 2, 1]) == [3, 1, 2]
```

The `seen` set uses `Θ(n)` additional space in the worst case to support expected constant-time membership checks.

## 12. Representation effects

The same ADT operation can have different costs under different representations.

Examples:

- FIFO dequeue from the front of a Python list requires shifting remaining references; `deque.popleft()` is designed for efficient end operations [3].
- binary search needs indexed access to realize logarithmic time; ordered linked-list traversal can remain linear despite logarithmic comparisons.
- hash lookup has expected constant cost under ordinary assumptions but collision-heavy worst cases differ.

Complexity belongs to an operation–representation pair.

## 13. Measuring small fragments with `timeit`

`timeit` measures repeated execution while reducing several common timing mistakes [4].

```python
from timeit import repeat


samples = repeat(
    stmt="sum(values)",
    setup="values = list(range(100))",
    repeat=3,
    number=1000,
)

print(len(samples))
assert len(samples) == 3
assert all(sample > 0 for sample in samples)
```

Do not publish the numeric values from one machine as universal performance. Record:

- Python implementation and version;
- dependency versions;
- hardware and operating system;
- input generation;
- warm-up and repetition policy;
- summary statistic; and
- variability.

The minimum repeat can approximate the least system-interfered run for a microbenchmark, but workload-specific statistical analysis may require more.

### 13.1 Fair comparison

Ensure candidates:

- return equivalent results;
- receive equivalent inputs;
- do not reuse mutated state unfairly;
- include or exclude setup consistently; and
- run enough times for measurable duration.

## 14. Profiling whole programs

`cProfile` records deterministic call statistics [5].

Command:

```console
python -m cProfile -s cumulative program.py
```

Interpret columns such as call count, total internal time, and cumulative time. A profiler identifies where runtime was spent in the measured workload; it does not independently prove why the code is slow or which change preserves correctness.

Profile representative end-to-end work before micro-optimizing a helper that contributes little total time.

<!-- TODO(media): Add a profiler-reading animation that identifies a cumulative-time hotspot, drills into its caller, and rejects a low-impact micro-optimization. Suggested path: ../Assets/Module-10/profiling-workflow.mp4 -->

## 15. Memory observation

`sys.getsizeof(obj)` reports memory directly attributed to an object, not recursively the objects it references [6].

```python
import sys

outer = [[1, 2, 3], [4, 5, 6]]
direct_size = sys.getsizeof(outer)

print(direct_size > 0)
assert direct_size > 0
```

Expected output:

```text
True
```

Treat memory measurement as implementation-specific. State whether a measurement includes referenced objects, allocator overhead, shared objects, native-library buffers, and peak rather than final usage.

## 16. Optimization workflow

1. **Define acceptance conditions.** Correct output, latency or throughput target, and memory limit.
2. **Create a representative workload.** Include realistic size, distribution, and failure paths.
3. **Establish a reproducible baseline.**
4. **Profile to find the dominant cost.**
5. **Explain the cost structurally.** Algorithm, representation, I/O, allocation, or repeated work.
6. **Change the narrow responsible layer.**
7. **Run correctness and regression tests.**
8. **Repeat the same measurement protocol.**
9. **Stop when the target is met or the next trade-off is unjustified.**

Algorithmic improvement often has more impact than local syntax changes:

```python
def contains_duplicate_quadratic(values):
    for left in range(len(values)):
        for right in range(left + 1, len(values)):
            if values[left] == values[right]:
                return True
    return False


def contains_duplicate_hash(values):
    seen = set()
    for value in values:
        if value in seen:
            return True
        seen.add(value)
    return False


cases = [
    [],
    [1],
    [1, 2, 3],
    [1, 2, 1],
]

for case in cases:
    assert contains_duplicate_quadratic(case) == contains_duplicate_hash(case)
```

The first function is worst-case `Θ(n²)`. The second is expected `Θ(n)` time with `Θ(n)` extra space under standard hash-table assumptions.

## 17. Common failure modes

### 17.1 Big O treated as exact runtime

Asymptotic bounds omit constants, lower-order terms, hardware, and implementation effects.

### 17.2 Undefined `n`

State whether size means elements, digits, bytes, vertices, edges, or another quantity.

### 17.3 Average case without a distribution

Expected cost requires a probability model.

### 17.4 Multiplying loops mechanically

Dependent bounds and early exits require summation or case reasoning.

### 17.5 Benchmarking unequal work

Candidates must produce equivalent observable results.

### 17.6 Timing once

One sample cannot expose noise or variability.

### 17.7 Optimizing before profiling

The edited code may not dominate total resource use.

### 17.8 Trading correctness for speed

Every candidate must pass the same acceptance tests.

### 17.9 Reading `getsizeof()` as recursive memory

It excludes referenced objects [6].

## 18. Guided practice

### 18.1 Count operations

Derive exact and asymptotic counts for:

```text
for i in range(n):
    for j in range(i):
        operation()
```

### 18.2 Case specification

For linear search, describe best, worst, and an average case under an explicit uniform-position assumption.

### 18.3 Benchmark audit

Review a benchmark that times one candidate after constructing input and another with prebuilt input. Identify the confound and redesign the measurement.

## 19. Independent practice

### Exercise 1 — Complexity table

Analyse five functions supplied by the lecturer.

**Deliverable:** input-size definition, cost recurrence or summation, tight time bound, and auxiliary-space bound.

### Exercise 2 — Duplicate detection evaluation

Compare the two duplicate-detection functions from Section 16.

**Requirements:** correctness parity tests, representative inputs, `timeit` protocol, and written time–space trade-off.

### Exercise 3 — Profiling report

Profile a program with at least three functions.

**Deliverable:** environment, workload, top cumulative-cost functions, one evidence-based candidate change, and before/after results.

### Exercise 4 — Recurrence

Draw a recursion tree for `T(n) = 2T(n/2) + n` and derive its tight bound.

## 20. Knowledge check

1. What must accompany an efficiency claim?
2. How do `O` and `Θ` differ?
3. How do average and amortized cost differ?
4. Why are two consecutive linear loops still linear?
5. What produces logarithmic loop count?
6. Why can caching improve time while worsening space?
7. What does a profiler establish?
8. Why can `sys.getsizeof()` understate container memory?

<details>
<summary>Answer key</summary>

1. Operation, input-size definition, representation, cost model, and case.
2. `O` is an upper bound; `Θ` is a tight upper and lower bound.
3. Average cost uses an input distribution; amortized cost averages over an operation sequence without requiring randomness.
4. Costs add, producing `2n` work, whose tight bound is `Θ(n)`.
5. Reducing remaining problem size by a constant factor each iteration.
6. Stored results avoid recomputation but consume additional memory.
7. Where measured runtime was attributed for the selected workload.
8. It counts only directly attributed storage, not recursively referenced objects.

</details>

## 21. Module synthesis

Efficiency argument:

```text
workload and size
    -> cost model
    -> operation count or recurrence
    -> asymptotic bound
    -> representative measurement
    -> tested optimization
```

Analysis predicts scaling; measurement validates behaviour in a concrete environment. Use both, preserve correctness, and stop when defined performance conditions are satisfied.

## References

1. Black, P. E. “Big-O Notation.” *Dictionary of Algorithms and Data Structures*, National Institute of Standards and Technology, modified 6 September 2019. Accessed 31 August 2026. https://www.nist.gov/dads/HTML/bigOnotation.html
2. Black, P. E. “Theta.” *Dictionary of Algorithms and Data Structures*, National Institute of Standards and Technology, modified 24 February 2016. Accessed 31 August 2026. https://www.nist.gov/dads/HTML/theta.html
3. Python Software Foundation. “`collections.deque`.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/collections.html#collections.deque
4. Python Software Foundation. “`timeit` — Measure Execution Time of Small Code Snippets.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/timeit.html
5. Python Software Foundation. “The Python Profilers.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/profile.html
6. Python Software Foundation. “`sys.getsizeof()`.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/sys.html#sys.getsizeof

---

**Previous module:** Module 9 — Python Classes and Inheritance  
**Next module:** Module 11 — Searching Algorithms
