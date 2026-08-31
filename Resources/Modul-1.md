# Module 1 — Introduction to Data Structures

> **Course:** Algorithms and Programming  
> **Programming language:** Python  
> **Supported runtime:** Python 3.10 or later  
> **Resource type:** Technical learning module  
> **Practical notebook:** Deferred to `../Practice/Modul_1-3.ipynb`  
> **Estimated study time:** 3–4 hours

## 1. Module scope

A data structure defines how a program organizes data so that a required set of operations can be performed correctly and efficiently. The choice of structure affects:

- which operations are available;
- the meaning and ordering of stored values;
- the cost of access, insertion, deletion, and traversal;
- the invariants that must remain true after every operation; and
- the amount and layout of memory used by an implementation.

This module establishes the vocabulary and analysis framework used throughout the course. It introduces abstract data types, concrete representations, structural invariants, Python's container model, and operation-level complexity. Detailed treatment of Python strings, tuples, lists, dictionaries, recursion, object-oriented design, efficiency, and searching appears in later modules.

<!-- TODO(media): Add a 60–90 second overview animation showing raw values being organized as a sequence, stack, queue, tree, and graph. Include captions and descriptive alt text. Suggested path: ../Assets/Module-1/data-structure-overview.mp4 -->

## 2. Learning outcomes

After completing this module, a student should be able to:

1. **Distinguish** a data type, data structure, abstract data type, and concrete implementation.
2. **Classify** a structure by ordering, access method, mutability, topology, and element constraints.
3. **Specify** a small abstract data type using operations, preconditions, postconditions, and invariants.
4. **Trace** state changes produced by stack and queue operations.
5. **Select** a suitable structure from a stated workload and justify the selection using operation costs.
6. **Implement and verify** basic stack and queue behaviour with Python's standard containers.
7. **Recognize** invalid states, underflow, representation exposure, and other basic failure modes.

## 3. Prerequisites and environment

### 3.1 Required knowledge

Students should already be able to:

- run a Python file or use the interactive interpreter;
- create variables and evaluate expressions;
- read a function or method call such as `items.append(value)`; and
- interpret simple output produced by `print()`.

Branching, iteration, and user-defined functions are not required for the core examples.

### 3.2 Verify Python

Run:

```console
python --version
```

Expected form:

```text
Python 3.x.y
```

The examples in this module use only Python's standard library. No package installation is required.

## 4. Core terminology

### 4.1 Data, data type, and data structure

**Data** is a representation of facts, measurements, symbols, or state that a program can store and process.

A **data type** defines a set of permitted values and the operations applicable to those values. For example, Python's `int` type supports integer arithmetic, ordering, and conversion operations.

A **data structure** organizes a collection of data and the relationships between its elements. A data structure normally exists to support an operation set such as:

- create;
- access or retrieve;
- search;
- insert;
- update;
- delete;
- traverse; and
- aggregate.

The US National Institute of Standards and Technology (NIST) Dictionary of Algorithms and Data Structures defines a data structure in terms of organizing information to improve algorithmic efficiency or conceptual unity [1]. A structure and its algorithms therefore form one design unit: an operation must preserve the structure's legal state.

### 4.2 Abstract data type

An **abstract data type (ADT)** specifies values and operations independently of any programming-language representation [2]. An ADT states *what* behaviour is required. A data structure implementation states *how* that behaviour is realized.

| Level | Main concern | Example |
| --- | --- | --- |
| ADT | Behavioural contract | A stack supports `push`, `pop`, `top`, and `is_empty` with last-in, first-out semantics. |
| Data structure | Organization and representation | A contiguous dynamic array or a linked chain of nodes. |
| Python implementation | Concrete language mechanism | A Python `list` used through `append()` and `pop()`. |

One ADT can have multiple implementations. One concrete structure can also support multiple ADTs. A Python `list` can implement a stack, but using it as a first-in, first-out queue requires front removal and is a poor performance choice for large workloads.

### 4.3 Algorithm

An **algorithm** is a finite, unambiguous procedure that transforms input into output. When an algorithm operates on a data structure, correctness has two parts:

1. the returned result satisfies the operation's postcondition; and
2. the remaining structure still satisfies all representation invariants.

For example, removing the minimum item from a min-heap must return a minimum value *and* restore the heap-order property for the remaining items.

## 5. Behaviour before representation

ADT design starts from observable behaviour. A minimal specification records:

- **state space:** all valid logical states;
- **operations:** names, inputs, outputs, and state changes;
- **preconditions:** facts that must be true before an operation;
- **postconditions:** facts guaranteed after a valid operation;
- **invariants:** facts that must be true in every externally observable valid state; and
- **failure semantics:** the result when a precondition is not satisfied.

### 5.1 Stack ADT

A **stack** is a last-in, first-out (LIFO) collection [3].

Let `S` be a stack and `x` a value. A compact contract is:

| Operation | Precondition | Postcondition |
| --- | --- | --- |
| `new()` | None | Returns an empty stack. |
| `push(S, x)` | `S` is valid. | `x` becomes the top item; size increases by one. |
| `top(S)` | `S` is not empty. | Returns the most recently pushed item without changing `S`. |
| `pop(S)` | `S` is not empty. | Removes and returns the most recently pushed item; size decreases by one. |
| `is_empty(S)` | `S` is valid. | Returns whether `S` contains no items. |

Using functional notation in which `pop` returns `(removed_value, resulting_stack)`, two characteristic laws are:

```text
pop(push(S, x)) = (x, S)
top(push(S, x)) = x
```

These laws describe behaviour, not storage layout.

### 5.2 Queue ADT

A **queue** is a first-in, first-out (FIFO) collection [4].

| Operation | Precondition | Postcondition |
| --- | --- | --- |
| `new()` | None | Returns an empty queue. |
| `enqueue(Q, x)` | `Q` is valid. | `x` becomes the newest item; size increases by one. |
| `front(Q)` | `Q` is not empty. | Returns the oldest item without changing `Q`. |
| `dequeue(Q)` | `Q` is not empty. | Removes and returns the oldest item; size decreases by one. |
| `is_empty(Q)` | `Q` is valid. | Returns whether `Q` contains no items. |

Stack and queue semantics differ only in which item becomes accessible for removal. That difference changes both program behaviour and appropriate implementation choices.

<!-- TODO(media): Add a side-by-side animation of push/pop for LIFO and enqueue/dequeue for FIFO. Show operation names, logical front/top, and state after each operation. Include a transcript and alt text. Suggested path: ../Assets/Module-1/stack-vs-queue.mp4 -->

## 6. Python's object and container model

Python represents program data as objects and relationships between objects. Every object has an **identity**, **type**, and **value** [5].

- **Identity** distinguishes one object from another. `is` compares identity.
- **Type** determines supported operations and constrains possible values.
- **Value** is the object's data content.
- **Mutability** determines whether the value can change after object creation.

A Python variable is a name bound to an object. A container generally stores references to objects rather than embedding independent copies of their values. This model matters when a mutable object is referenced from more than one place; Module 5 examines aliasing and copying in detail.

Run this identity check:

```python
first = [10, 20]
second = first
third = [10, 20]

print(first == second)  # equal values
print(first is second)  # same object
print(first == third)   # equal values
print(first is third)   # different objects

assert first is second
assert first == third
assert first is not third
```

Expected output:

```text
True
True
True
False
```

Do not interpret `id()` as a portable memory address. The language guarantees a stable identity during an object's lifetime; CPython's address-based implementation of `id()` is an implementation detail [5].

<!-- TODO(media): Add an object-reference animation for the previous example. Show three names, two list objects, value equality, and identity equality. Do not imply that variables contain the list values directly. Suggested path: ../Assets/Module-1/python-object-references.gif -->

## 7. Classification dimensions

Labels such as “linear” and “non-linear” are useful but incomplete. A technical comparison should use several independent dimensions.

### 7.1 Logical topology

- **Linear:** each logical position has at most one predecessor and one successor in the primary traversal order. Examples: array, linked list, stack, queue.
- **Hierarchical:** elements form parent–child relationships. A tree has a root and recursively defined subtrees [6].
- **Network:** elements may have arbitrary connections. A graph is commonly formalized as `G = (V, E)`, where `V` is a set of vertices and `E` is a set of edges [7].

A tree is also a constrained graph, but the terms emphasize different invariants and algorithms.

### 7.2 Access model

- **Positional access:** retrieve an item by index or position.
- **Sequential access:** reach an item by following an order from a starting point.
- **Key-based access:** retrieve a value using an associated key.
- **Membership access:** determine whether an equal element is present.
- **Priority access:** retrieve the item with minimum or maximum priority.
- **Relationship access:** retrieve neighbours, children, or connected elements.

### 7.3 Ordering semantics

A collection may be:

- ordered by insertion position;
- sorted by a comparison key;
- ordered by priority;
- partially ordered by an invariant; or
- logically unordered.

“Unordered” does not mean random. It means that position is not part of the ADT's contract. Python dictionaries preserve insertion order, while Python sets do not provide positional indexing [5].

### 7.4 Mutability

- A **mutable** structure can change its contained references after construction.
- An **immutable** structure cannot change its directly contained references after construction.

Python `list`, `dict`, and `set` objects are mutable. `tuple`, `str`, and `frozenset` objects are immutable [5]. An immutable container may still reference a mutable object; immutability applies to the container's direct references, not recursively to every reachable object.

### 7.5 Capacity and growth

- **Fixed capacity:** maximum element count is selected at construction or allocation time.
- **Dynamic capacity:** representation may grow or shrink while the program runs.
- **Bounded dynamic:** logical content changes, but a fixed maximum length is enforced.

Python's `collections.deque(maxlen=n)` is a bounded dynamic structure. After it reaches `maxlen`, adding an item to one end discards an item from the opposite end [8].

### 7.6 Element constraints

- **Homogeneous:** elements share a representation or declared type.
- **Heterogeneous:** elements may have different types.
- **Unique:** duplicate-equivalent elements are rejected or coalesced.
- **Hashable-only:** elements or keys must provide a stable hash compatible with equality.

Python lists can contain references to objects of different types. Python sets require hashable elements and retain only unique-equivalent elements. Python dictionary keys must be hashable [5].

## 8. Structure catalogue

This catalogue separates logical behaviour from typical representation. Complexity values are conventional asymptotic costs for the named representation, not universal guarantees for every implementation.

| Structure or ADT | Defining property | Primary operations | Typical representation | Python mechanism |
| --- | --- | --- | --- | --- |
| Array | Indexed sequence in contiguous storage | index, update, traverse | Contiguous element slots | `list` provides a dynamic sequence interface; `array.array` stores restricted homogeneous values. |
| Linked list | Nodes connected by links | insert/delete near known node, sequential traverse | Nodes with next or previous links | Custom node objects; no dedicated built-in linked list. |
| Stack | LIFO removal | push, top, pop | Dynamic array or linked list | `list.append()` and `list.pop()` |
| Queue | FIFO removal | enqueue, front, dequeue | Circular buffer or linked list | `collections.deque` |
| Deque | Insert/remove at both ends | append, append-left, pop, pop-left | Block-linked or circular representation | `collections.deque` |
| Set | Unique elements; membership-oriented | add, remove, contains | Hash table or search tree | `set`, `frozenset` |
| Mapping | Keys associated with values | insert, find, update, delete by key | Hash table or search tree | `dict` |
| Priority queue | Access by priority | insert, find-min/max, delete-min/max | Heap or balanced search tree | `heapq` over a list |
| Tree | Rooted parent–child hierarchy | insert, remove, traverse, search | Linked nodes or array encoding | Custom objects; some specialized standard-library representations |
| Graph | Vertices connected by edges | add vertex/edge, traverse, path query | Adjacency list or matrix | Commonly `dict` plus `set`/`list`; no general built-in graph type |

### 8.1 Logical versus physical order

Logical order is part of the abstraction. Physical order is part of the implementation.

For example, a circular queue may logically contain:

```text
front -> A, B, C <- rear
```

while its array slots physically appear as:

```text
[B, C, empty, empty, A]
```

Indices plus wrap-around arithmetic recover the logical FIFO order. Algorithms should normally depend on the queue operations, not the physical slot layout.

<!-- TODO(media): Add an animation showing a circular queue wrapping across the end of an array while logical order stays unchanged. Include indices, front/rear markers, and alt text. Suggested path: ../Assets/Module-1/circular-queue.gif -->

## 9. Representation invariants

A **representation invariant** is a predicate that must hold for every valid internal state of an implementation.

Examples:

- stack size equals the number of stored items;
- queue front and rear indices remain within their permitted range;
- linked-list links connect the intended node sequence;
- each dictionary key is unique under equality;
- every child in a min-heap has a value greater than or equal to its parent.

For a zero-indexed min-heap stored in array `a`, the heap-order invariant is:

```text
a[k] <= a[2k + 1]    when the left child exists
a[k] <= a[2k + 2]    when the right child exists
```

Python's `heapq` module uses this array representation and keeps the minimum element at index `0` [9].

Test the invariant indirectly by using only the heap interface:

```python
import heapq

priorities = [40, 10, 30, 20]
heapq.heapify(priorities)

first = heapq.heappop(priorities)
second = heapq.heappop(priorities)

print(first, second)
print(priorities)

assert (first, second) == (10, 20)
assert priorities[0] == 30
```

Expected output:

```text
10 20
[30, 40]
```

The internal array is not globally sorted. Only the heap-order relationships are required. Code that sorts or edits internal heap positions directly may destroy the intended representation or add unnecessary cost.

## 10. Operation-level efficiency

Correctness is mandatory; efficiency is evaluated relative to a workload. Let `n` denote the current number of elements.

### 10.1 Cost measures

- **Time complexity** models growth in executed work as `n` grows.
- **Space complexity** models growth in required memory.
- **Auxiliary space** excludes storage occupied by the input and output when the analysis explicitly adopts that convention.
- **Worst-case cost** bounds the most expensive input or state of size `n`.
- **Average-case cost** uses a stated probability model over inputs or states.
- **Amortized cost** distributes the cost of occasional expensive operations across a sequence of operations.

### 10.2 Asymptotic notation

- `O(f(n))`: asymptotic upper bound.
- `Ω(f(n))`: asymptotic lower bound.
- `Θ(f(n))`: asymptotically tight bound.

Common growth classes:

```text
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ)
```

Asymptotic notation suppresses constant factors and lower-order terms. It does not measure exact runtime, guarantee one implementation is faster for every input size, or replace profiling.

### 10.3 Costs depend on operations and representation

| Operation | Dynamic array | Singly linked list | Hash table, expected | Balanced search tree |
| --- | ---: | ---: | ---: | ---: |
| Access by numeric index | `O(1)` | `O(n)` | Not its interface | Not positional unless augmented |
| Search by value | `O(n)` | `O(n)` | `O(1)` by key | `O(log n)` by ordered key |
| Insert at front | `O(n)` | `O(1)` | Not positional | Not positional |
| Append at end | Amortized `O(1)` | `O(1)` with tail pointer | Not positional | Not positional |
| Delete known front node | `O(n)` | `O(1)` | Not positional | Not positional |

The table assumes the required node or key is already known where stated. Searching for a linked-list position can dominate an otherwise constant-time link update.

The hash-table values are expected costs under an effective hash function and ordinary load management; collision-heavy worst cases can be linear [11]. The balanced-tree values assume ordering by the searched key.

Python documentation gives one concrete consequence: `list.pop(0)` requires `O(n)` element movement, while `collections.deque` supports append and pop operations at either end with approximately `O(1)` performance [8].

Module 10 develops formal efficiency analysis. In this module, apply one rule: **state the operation, representation, and case before stating a complexity**.

## 11. Worked example: stack implementation

Python's `list` supports efficient append and removal at the right end, making that end a suitable stack top [10].

```python
undo_stack = []

undo_stack.append("insert title")
undo_stack.append("format heading")
undo_stack.append("delete paragraph")

latest_action = undo_stack.pop()

print(latest_action)
print(undo_stack)

assert latest_action == "delete paragraph"
assert undo_stack == ["insert title", "format heading"]
```

Expected output:

```text
delete paragraph
['insert title', 'format heading']
```

### 11.1 State trace

| Step | Operation | Stack from bottom to top | Returned value |
| ---: | --- | --- | --- |
| 0 | create | `[]` | — |
| 1 | push `"insert title"` | `["insert title"]` | — |
| 2 | push `"format heading"` | `["insert title", "format heading"]` | — |
| 3 | push `"delete paragraph"` | `["insert title", "format heading", "delete paragraph"]` | — |
| 4 | pop | `["insert title", "format heading"]` | `"delete paragraph"` |

The implementation convention is “rightmost item is top.” Reversing that convention would still permit a correct stack, but front insertion and removal on a Python list would impose linear movement costs.

### 11.2 Underflow

Calling `pop()` on an empty list raises `IndexError`:

```python
empty_stack = []

try:
    empty_stack.pop()
except IndexError as error:
    print(type(error).__name__)
```

Expected output:

```text
IndexError
```

This example only observes the failure. Module 7 covers exception handling and recovery policies in detail.

## 12. Worked example: queue implementation

Use `collections.deque` when a workload requires insertion and removal at opposite ends [8], [10].

```python
from collections import deque

print_queue = deque()

print_queue.append("report.pdf")
print_queue.append("diagram.png")
print_queue.append("notes.txt")

next_job = print_queue.popleft()

print(next_job)
print(list(print_queue))

assert next_job == "report.pdf"
assert list(print_queue) == ["diagram.png", "notes.txt"]
```

Expected output:

```text
report.pdf
['diagram.png', 'notes.txt']
```

### 12.1 State trace

| Step | Operation | Queue from front to rear | Returned value |
| ---: | --- | --- | --- |
| 0 | create | `[]` | — |
| 1 | enqueue `"report.pdf"` | `["report.pdf"]` | — |
| 2 | enqueue `"diagram.png"` | `["report.pdf", "diagram.png"]` | — |
| 3 | enqueue `"notes.txt"` | `["report.pdf", "diagram.png", "notes.txt"]` | — |
| 4 | dequeue | `["diagram.png", "notes.txt"]` | `"report.pdf"` |

The conversion `list(print_queue)` is used only to produce a familiar display and assertion. Queue updates still use `append()` and `popleft()`.

## 13. Worked example: bounded history

A bounded deque gives explicit capacity semantics:

```python
from collections import deque

recent_readings = deque(maxlen=3)

recent_readings.append(21.4)
recent_readings.append(21.6)
recent_readings.append(21.5)
recent_readings.append(21.8)

print(list(recent_readings))

assert list(recent_readings) == [21.6, 21.5, 21.8]
assert recent_readings.maxlen == 3
```

Expected output:

```text
[21.6, 21.5, 21.8]
```

The fourth append does not create an overflow error. The deque automatically discards the oldest item from the opposite end. This behaviour is appropriate only when loss of the oldest record is part of the intended contract.

## 14. Selecting a data structure

Do not select a structure from its name alone. Derive the choice from the workload.

### 14.1 Selection procedure

1. **Define semantics.** Determine ordering, duplicate handling, and the item eligible for access or removal.
2. **List dominant operations.** Include expected frequency, such as “one million membership checks and ten insertions.”
3. **State constraints.** Include maximum size, memory limit, mutability, persistence, concurrency, and required worst-case guarantees.
4. **Identify candidate ADTs.** Match semantics before representation.
5. **Compare implementations.** Evaluate time, space, failure behaviour, and library support.
6. **Validate with representative inputs.** Complexity guides selection; measurements confirm behaviour in the actual environment.

### 14.2 Decision examples

| Requirement | Suitable starting point | Technical reason |
| --- | --- | --- |
| Undo the most recent edit | Stack | Required removal order is LIFO. |
| Process requests by arrival time | Queue | Required removal order is FIFO. |
| Retain only the 100 newest events | Bounded deque | Fixed logical capacity with automatic oldest-item eviction. |
| Test whether a unique identifier was observed | Set | Membership and uniqueness define the workload. |
| Retrieve a student record by student ID | Mapping | The key determines the retrieved value. |
| Repeatedly process the lowest-cost pending task | Min-priority queue | Minimum-priority access is the dominant operation. |
| Represent prerequisite relationships between courses | Directed graph | Courses are vertices; prerequisite relations are directed edges. |

### 14.3 Counterexample: choosing by appearance

A list of tasks sorted once by priority may *look* like a priority queue. If tasks are repeatedly inserted and the minimum repeatedly removed, preserving a fully sorted list can perform more work than maintaining only a heap-order invariant. The correct choice follows the operation sequence, not the display format.

## 15. Interfaces and representation boundaries

Clients should operate through a structure's public interface. Depending directly on internal representation creates **representation exposure**.

For a stack implemented with a list:

- permitted stack operations are conceptually `push`, `pop`, `top`, and `is_empty`;
- arbitrary middle insertion is a list operation, not a stack operation;
- sorting the backing list changes stack order without using the stack contract; and
- direct replacement of internal storage can invalidate metadata or aliases in a larger implementation.

Restricting operations makes invariants easier to preserve and allows the representation to change without forcing client-code changes. Modules 4, 8, and 9 develop function interfaces, classes, encapsulation, and inheritance.

## 16. Common failure modes

### 16.1 Confusing an ADT with one implementation

Incorrect claim:

> A stack is a Python list.

Correct distinction:

> A stack is a LIFO ADT. A Python list is one possible stack implementation.

### 16.2 Reporting complexity without a case

“Insertion is `O(1)`” is incomplete. Insertion where? Into which representation? Is the location already known? Is the claim worst-case or amortized?

A complete statement is:

> Appending to a dynamic array is typically amortized `O(1)`; inserting at its front is `O(n)` because existing elements must move.

### 16.3 Using a list as a high-volume FIFO queue

`list.pop(0)` shifts the remaining references and has linear cost. Use `deque.popleft()` for efficient removal at the left end [8].

### 16.4 Treating physical layout as logical behaviour

A heap array is not a sorted array. A circular queue's physical slots are not necessarily in front-to-rear order. Inspect operations and invariants, not only printed storage.

### 16.5 Ignoring empty-state operations

`list.pop()` and `deque.popleft()` raise `IndexError` when empty. The ADT contract must define whether the caller must prevent underflow or the implementation must translate it into another result.

### 16.6 Assuming mutability is recursive

An immutable tuple may reference a mutable list. The tuple's direct references cannot be replaced, but the referenced list can still change. Treat object reachability and container mutability as separate properties [5].

### 16.7 Depending on accidental order

If order affects correctness, use a structure whose contract guarantees the needed order. Set iteration order is not a positional interface.

## 17. Guided practice

### 17.1 Trace a stack

Start with an empty stack. Apply:

```text
push(4), push(7), pop(), push(9), top()
```

Record:

1. each intermediate state from bottom to top;
2. every returned value; and
3. the final size.

**Success criteria:** the `pop()` result follows LIFO order, `top()` does not change the state, and every state is shown.

### 17.2 Trace a queue

Start with an empty queue. Apply:

```text
enqueue(A), enqueue(B), dequeue(), enqueue(C), front()
```

Record each state from front to rear.

**Success criteria:** `dequeue()` returns `A`, `front()` returns `B` without removal, and the final queue is `[B, C]`.

### 17.3 Separate abstraction from implementation

For each item, label it **ADT**, **representation**, **Python implementation**, or **operation**:

1. FIFO queue
2. linked nodes
3. `collections.deque`
4. dequeue
5. binary heap
6. `heapq.heappop()`

**Success criteria:** each label identifies the item's abstraction level rather than its application domain.

## 18. Independent practice

### Exercise 1 — Structure selection

Select one principal structure for each workload and justify the choice in two technical sentences.

1. A syntax checker must match each closing bracket with the most recent unmatched opening bracket.
2. A service must process support tickets in arrival order.
3. A program must reject duplicate registration codes.
4. A route planner must represent roads connecting locations.
5. A scheduler must repeatedly select the pending event with the earliest timestamp.

**Deliverable:** a five-row table containing workload, chosen ADT, dominant operation, and justification.

**Constraints:** use only structures introduced in this module. Do not justify a choice only with “faster” or “easier.”

### Exercise 2 — Bounded event history

Create a Python program using `collections.deque` with a maximum length of `4`.

1. Append event IDs `"E101"` through `"E105"` in numeric order.
2. Print the remaining IDs from oldest to newest.
3. Assert the maximum length and final content.

**Expected output:**

```text
['E102', 'E103', 'E104', 'E105']
```

**Success criteria:** no manual deletion is used, both assertions pass, and the output exactly matches the specified list.

### Exercise 3 — Contract analysis

Write a contract for a `Bag` ADT. A bag is an unordered collection that permits duplicate values.

Specify:

- `new`;
- `add`;
- `remove_one`;
- `count`;
- `size`; and
- empty-state behaviour for `remove_one`.

**Deliverable:** one operation table with inputs, preconditions, outputs, postconditions, and failure semantics.

**Success criteria:** removing one value changes its multiplicity by exactly one, duplicate values remain permitted, and failure behaviour is unambiguous.

### Exercise 4 — Representation comparison

Compare a dynamic array and a singly linked list for this workload:

```text
90% indexed reads
5% appends
5% insertions at the front
maximum size: 50,000 elements
```

**Deliverable:** a 150–250 word recommendation that:

1. identifies the dominant operation;
2. states relevant asymptotic costs;
3. selects a representation;
4. acknowledges one disadvantage of the selection; and
5. states what measurement would be useful before production use.

## 19. Knowledge check

1. What is the difference between an ADT and a data structure implementation?
2. Which property distinguishes a queue from a stack?
3. Why is `list.pop(0)` unsuitable for a large FIFO workload?
4. Does `O(1)` mean an operation takes one machine instruction?
5. Can an immutable Python container reference a mutable object?
6. Which invariant is maintained by a min-heap?
7. Why can a heap's internal array be unsorted?
8. What must be stated before a complexity claim is technically meaningful?

<details>
<summary>Answer key</summary>

1. An ADT specifies values and observable operations independently of representation; an implementation chooses a concrete organization and algorithms.
2. A queue removes the earliest enqueued item (FIFO); a stack removes the most recently pushed item (LIFO).
3. Removing index zero shifts all remaining list references, producing linear-time movement.
4. No. It means the operation's work is asymptotically bounded independently of input size under the stated cost model.
5. Yes. The immutable container's direct references remain fixed, while a referenced mutable object's value may change.
6. Every parent value is less than or equal to its children, so the root contains a minimum value.
7. The heap requires only parent–child ordering, not total ordering between all pairs of elements.
8. The operation, representation, input-size definition, and relevant case or cost model.

</details>

## 20. Module synthesis

Use this dependency chain when analysing a programming problem:

```text
problem constraints
    -> required semantics
    -> ADT operations and failure rules
    -> candidate representations
    -> operation and space costs
    -> verified implementation
```

Core distinctions:

- **ADT:** behavioural contract.
- **Data structure:** organization of values and relationships.
- **Implementation:** concrete code and storage representation.
- **Invariant:** condition preserved by every valid operation.
- **Complexity:** growth of an operation's resource cost under a stated model.

A correct selection begins with required behaviour and dominant operations. Language syntax comes after those decisions.

## References

1. Black, P. E. “Data Structure.” *Dictionary of Algorithms and Data Structures*, National Institute of Standards and Technology, modified 20 September 2024. Accessed 31 August 2026. https://www.nist.gov/dads/HTML/dataStructure.html
2. Black, P. E. “Abstract Data Type.” *Dictionary of Algorithms and Data Structures*, National Institute of Standards and Technology, modified 10 February 2005. Accessed 31 August 2026. https://www.nist.gov/dads/HTML/abstractDataType.html
3. Black, P. E. “Stack.” *Dictionary of Algorithms and Data Structures*, National Institute of Standards and Technology, modified 1 October 2019. Accessed 31 August 2026. https://www.nist.gov/dads/HTML/stack.html
4. Black, P. E. “Queue.” *Dictionary of Algorithms and Data Structures*, National Institute of Standards and Technology, modified 14 December 2020. Accessed 31 August 2026. https://www.nist.gov/dads/HTML/queue.html
5. Python Software Foundation. “Data Model.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/reference/datamodel.html
6. Black, P. E., and *Algorithms and Theory of Computation Handbook*. “Tree.” *Dictionary of Algorithms and Data Structures*, National Institute of Standards and Technology, modified 15 December 2017. Accessed 31 August 2026. https://www.nist.gov/dads/HTML/tree.html
7. Black, P. E., and P. J. Tanenbaum. “Graph.” *Dictionary of Algorithms and Data Structures*, National Institute of Standards and Technology, modified 18 July 2022. Accessed 31 August 2026. https://www.nist.gov/dads/HTML/graph.html
8. Python Software Foundation. “`collections` — Container Datatypes.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/collections.html#collections.deque
9. Python Software Foundation. “`heapq` — Heap Queue Algorithm.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/heapq.html
10. Python Software Foundation. “Data Structures.” *The Python Tutorial*. Accessed 31 August 2026. https://docs.python.org/3/tutorial/datastructures.html
11. Black, P. E. “Hash Table.” *Dictionary of Algorithms and Data Structures*, National Institute of Standards and Technology, modified 20 April 2022. Accessed 31 August 2026. https://www.nist.gov/dads/HTML/hashtab.html

---

**Next module:** Module 2 — Branching and Iteration
