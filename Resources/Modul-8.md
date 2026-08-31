# Module 8 — Object-Oriented Programming

> **Course:** Algorithms and Programming  
> **Programming language:** Python  
> **Supported runtime:** Python 3.10 or later  
> **Resource type:** Technical learning module  
> **Practical notebook:** Deferred to `../Practice/Modul_8-9.ipynb`  
> **Estimated study time:** 4 hours

## 1. Module scope

Object-oriented programming (OOP) organizes software around objects that combine state, behaviour, identity, and invariants. OOP is useful when a domain contains entities with meaningful lifecycles or when state transitions must be controlled behind stable interfaces.

This module introduces object modelling, class and instance construction, methods, encapsulation conventions, invariants, commands and queries, composition, and responsibility allocation. Module 9 covers inheritance, polymorphism, descriptors, abstract base classes, and Python-specific class mechanics in greater depth.

<!-- TODO(media): Add an animation mapping a domain model to classes, instances, references, method calls, and state transitions. Suggested path: ../Assets/Module-8/domain-to-objects.mp4 -->

## 2. Learning outcomes

After completing this module, a student should be able to:

1. **Identify** candidate objects, responsibilities, state, and relationships from a requirement.
2. **Define** a Python class with validated instance state and behavioural methods.
3. **Distinguish** class objects, instance objects, attributes, and methods.
4. **Preserve** representation invariants across every public state transition.
5. **Separate** commands that change state from queries that return information.
6. **Apply** encapsulation conventions and property-controlled access.
7. **Construct** collaborations through composition.
8. **Evaluate** when procedural or object-oriented organization is the simpler design.

## 3. Object model vocabulary

| Term | Technical meaning |
| --- | --- |
| Class | Object that defines attribute and method behaviour for instances |
| Instance | Object created from a class |
| Attribute | Named value resolved on an object or its class |
| Method | Function retrieved through an object and normally bound to that object |
| State | Values currently associated with an object |
| Behaviour | Operations an object exposes |
| Identity | Property distinguishing an object from other objects |
| Invariant | Condition that must hold for every valid observable state |
| Encapsulation | Controlling state access through a defined interface |
| Composition | One object contains or references collaborating objects |

Python classes are themselves objects and support normal attribute operations [1].

## 4. From requirement to object model

Requirement:

> Maintain a bounded counter that starts within a range, can increment or decrement without leaving the range, and reports its current value.

Model:

| Element | Decision |
| --- | --- |
| Object | `BoundedCounter` instance |
| State | current value, lower bound, upper bound |
| Invariant | `lower <= value <= upper` |
| Commands | `increment()`, `decrement()` |
| Query | `value` |
| Failure | `ValueError` for invalid construction or transition |

OOP is valuable here because state validity depends on all transitions.

## 5. Class and instance construction

```python
class BoundedCounter:
    def __init__(self, value, *, lower=0, upper=100):
        if lower > upper:
            raise ValueError("lower cannot exceed upper")
        if not lower <= value <= upper:
            raise ValueError("initial value outside bounds")
        self._lower = lower
        self._upper = upper
        self._value = value

    @property
    def value(self):
        return self._value

    def increment(self):
        if self._value == self._upper:
            raise ValueError("upper bound reached")
        self._value += 1

    def decrement(self):
        if self._value == self._lower:
            raise ValueError("lower bound reached")
        self._value -= 1


counter = BoundedCounter(2, lower=0, upper=3)
counter.increment()

print(counter.value)
assert counter.value == 3
```

`__init__()` initializes an instance after creation; it does not return the instance [1]. `self` is the conventional name for the receiving instance parameter.

## 6. Attribute lookup and binding

When `counter.increment` is retrieved from an instance, Python creates a bound method that supplies `counter` as the first argument when called [2].

Conceptually:

```text
counter.increment()
BoundedCounter.increment(counter)
```

These calls are equivalent for an ordinary instance method:

```python
class Accumulator:
    def __init__(self):
        self.total = 0

    def add(self, amount):
        self.total += amount


accumulator = Accumulator()
Accumulator.add(accumulator, 5)

assert accumulator.total == 5
```

Call methods through the instance in normal client code. The explicit class call is useful for understanding binding.

## 7. Instance and class attributes

An instance attribute is normally assigned through `self`. A class attribute is stored on the class and is shared through lookup unless shadowed.

```python
class Sensor:
    unit = "°C"

    def __init__(self, identifier):
        self.identifier = identifier


first = Sensor("S-1")
second = Sensor("S-2")

assert first.unit == "°C"
assert second.unit == "°C"
assert first.identifier == "S-1"
assert second.identifier == "S-2"
```

Do not use a mutable class attribute for per-instance state:

```python
class IncorrectRegistry:
    entries = []

    def add(self, value):
        self.entries.append(value)


first = IncorrectRegistry()
second = IncorrectRegistry()
first.add("shared")

assert first.entries is second.entries
```

Allocate mutable per-instance state in `__init__()`.

<!-- TODO(media): Add an object graph showing class attributes, independent instance dictionaries, and the shared mutable-class-attribute defect. Suggested path: ../Assets/Module-8/class-instance-attributes.gif -->

## 8. Representation invariants

An invariant must hold:

- after successful construction;
- before and after every public method call;
- after successful property assignment; and
- whenever client code can observe state.

Example: a bank account that prohibits negative balance.

```python
class BankAccount:
    def __init__(self, owner, opening_balance=0):
        if opening_balance < 0:
            raise ValueError("opening balance cannot be negative")
        self._owner = owner
        self._balance = opening_balance

    @property
    def owner(self):
        return self._owner

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        if amount > self._balance:
            raise ValueError("insufficient balance")
        self._balance -= amount


account = BankAccount("Rina", 100)
account.deposit(25)
account.withdraw(40)

print(account.balance)
assert account.balance == 85
```

Validation belongs at every boundary capable of violating the invariant. Checking only construction is insufficient.

## 9. Encapsulation in Python

Python does not enforce private instance attributes in the same way as some languages. Naming conventions communicate interface intent:

- `name`: public interface;
- `_name`: non-public implementation detail;
- `__name`: class-local name mangling to reduce accidental subclass collisions.

The leading underscore is a contract signal, not an access-control barrier.

### 9.1 Properties

A property exposes attribute syntax while controlling access:

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("temperature below absolute zero")
        self._celsius = float(value)

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32


temperature = Temperature(20)
temperature.celsius = 25

assert temperature.celsius == 25.0
assert temperature.fahrenheit == 77.0
```

Use a method instead of a property when an operation is expensive, requires significant arguments, performs I/O, or has surprising side effects.

## 10. Commands and queries

A **command** changes state. A **query** returns information without changing state.

| Method | Category | State effect | Return |
| --- | --- | --- | --- |
| `deposit(amount)` | Command | Balance increases | Usually `None` |
| `withdraw(amount)` | Command | Balance decreases | Usually `None` or transaction data |
| `balance` | Query | None | Current numeric balance |
| `can_withdraw(amount)` | Query | None | Boolean |

Separating commands and queries makes testing and reasoning more direct. A method may intentionally return information about a state change, but the contract should not conceal mutation behind a query-like name.

## 11. Composition

Composition models a **has-a** relationship. One object delegates part of its responsibility to another.

```python
class LineItem:
    def __init__(self, description, unit_price, quantity):
        if unit_price < 0 or quantity <= 0:
            raise ValueError("invalid line item")
        self.description = description
        self.unit_price = unit_price
        self.quantity = quantity

    def subtotal(self):
        return self.unit_price * self.quantity


class Order:
    def __init__(self, items=None):
        self._items = list(items) if items is not None else []

    def add_item(self, item):
        if not isinstance(item, LineItem):
            raise TypeError("item must be a LineItem")
        self._items.append(item)

    def total(self):
        return sum(item.subtotal() for item in self._items)


order = Order([
    LineItem("Notebook", 2.5, 4),
    LineItem("Pen", 1.0, 3),
])

print(order.total())
assert order.total() == 13.0
```

`Order` collaborates with `LineItem` rather than inheriting from it. Their lifecycle and substitutability do not form an is-a relationship.

### 11.1 Ownership policy

`Order.__init__` makes a shallow copy of the incoming collection. This prevents later append or removal through the caller's list from changing the order, while the `LineItem` objects remain shared. State whether such sharing is intentional.

<!-- TODO(media): Add a composition diagram and animation for Order containing LineItem references, including shallow-copy ownership at construction. Suggested path: ../Assets/Module-8/order-composition.mp4 -->

## 12. Responsibility allocation

Place behaviour with the object that has the required information and owns the invariant.

Poor allocation:

```text
external code reads account._balance
external code calculates new value
external code writes account._balance
```

Better:

```text
account.withdraw(amount)
```

The object validates the transition atomically from the perspective of its interface.

Avoid “data-only” objects surrounded by unrelated procedural functions when the domain behaviour clearly belongs with the state. Also avoid forcing stateless calculations into classes that add no invariant, lifecycle, or collaboration value.

## 13. Identity and equality

Without a custom equality method, ordinary class instances compare by identity.

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


first = Point(1, 2)
second = Point(1, 2)
alias = first

assert first is alias
assert first is not second
assert first != second
```

Domain value objects may need value equality. Module 9 covers `__eq__` and data classes. Entity objects often retain identity semantics even when selected attributes match.

## 14. Object collaboration example

```python
class Inventory:
    def __init__(self):
        self._quantities = {}

    def add(self, sku, quantity):
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        self._quantities[sku] = self._quantities.get(sku, 0) + quantity

    def remove(self, sku, quantity):
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        available = self._quantities.get(sku, 0)
        if quantity > available:
            raise ValueError("insufficient stock")
        self._quantities[sku] = available - quantity

    def quantity(self, sku):
        return self._quantities.get(sku, 0)


class ReservationService:
    def __init__(self, inventory):
        self._inventory = inventory

    def reserve(self, sku, quantity):
        self._inventory.remove(sku, quantity)
        return {"sku": sku, "quantity": quantity}


inventory = Inventory()
inventory.add("BK-1", 5)
service = ReservationService(inventory)
reservation = service.reserve("BK-1", 2)

assert reservation == {"sku": "BK-1", "quantity": 2}
assert inventory.quantity("BK-1") == 3
```

`ReservationService` depends on an inventory collaborator. The reference is passed explicitly, making the dependency replaceable in testing.

## 15. Testing objects

Test:

- valid construction;
- invalid construction;
- each state transition;
- boundary transitions;
- invariants after failures;
- query non-mutation; and
- collaboration effects.

```python
account = BankAccount("Rina", 50)

try:
    account.withdraw(60)
except ValueError:
    pass

assert account.balance == 50
```

The failed command must leave the object in its prior valid state. Validate before mutating or provide rollback semantics.

## 16. When not to use OOP

A function or small module may be better when:

- transformation is stateless;
- data has no controlled lifecycle;
- behaviour does not vary by object;
- a class would only wrap one function; or
- state can be represented transparently without invariants.

OOP can add indirection, mutable state, identity concerns, and larger test surfaces. Select it because objects clarify responsibility and invariants, not because a program contains nouns.

## 17. Common failure modes

### 17.1 Mutable class attribute used as instance state

All instances share one object through class lookup.

### 17.2 Public state bypasses invariants

Direct mutation can avoid validation. Provide methods or controlled properties.

### 17.3 Method with unrelated responsibilities

A “manager” method performing validation, persistence, calculation, and formatting has low cohesion.

### 17.4 Query with hidden mutation

A method named `current_total()` should not clear items or write files.

### 17.5 Inheritance used for containment

An order has line items; it is not a line item.

### 17.6 Partial state mutation before failure

Validate all preconditions before committing changes, or design an explicit transaction.

### 17.7 Exposing a mutable internal collection

Returning `self._items` lets callers bypass methods. Return an immutable view, iterator, or deliberate copy when required.

## 18. Guided practice

### 18.1 Invariant table

For `BankAccount`, list every public transition, its preconditions, successful postcondition, and state after failure.

### 18.2 Responsibility mapping

Model a library loan with `Book`, `Member`, and `Loan`. Assign state and behaviour without creating a universal manager class.

### 18.3 Composition audit

Explain why `ReservationService` has an `Inventory` reference. State whether it owns the inventory lifecycle or only collaborates with it.

## 19. Independent practice

### Exercise 1 — Bounded stack class

Implement a stack object with fixed positive capacity.

**Required operations:** `push`, `pop`, `top`, `is_empty`, and `size`.

**Failure semantics:** reject overflow and underflow without corrupting state.

### Exercise 2 — Grade book

Design a `GradeBook` that records named assessments and numeric scores.

**Requirements:** scores range from `0` to `100`, duplicate assessment names are rejected, and `mean()` fails on an empty grade book.

### Exercise 3 — Composition

Create `Course` and `Enrollment` objects. A course contains enrollment references and enforces capacity.

**Deliverable:** class-responsibility table, invariants, implementation, and tests.

### Exercise 4 — Procedural comparison

Solve one stateless conversion task with both a function and a class. Justify which interface is smaller and clearer.

## 20. Knowledge check

1. What is an object invariant?
2. What does `self` represent?
3. How do class and instance attributes differ?
4. Why is a mutable class attribute dangerous for per-instance data?
5. What distinguishes a command from a query?
6. What relationship does composition model?
7. Why should failure leave an object valid?
8. When can a function be better than a class?

<details>
<summary>Answer key</summary>

1. A condition true for every valid observable object state.
2. The receiving instance bound to an ordinary instance method call.
3. Class attributes are resolved on the class and shared through lookup; instance attributes belong to one instance.
4. Instances can mutate the same shared object unexpectedly.
5. A command changes state; a query observes without changing state.
6. A has-a or collaborates-with relationship.
7. Later methods rely on the invariant; partial invalid state causes secondary failures.
8. When the behaviour is stateless and no lifecycle, identity, controlled state, or collaboration needs a class.

</details>

## 21. Module synthesis

Object design sequence:

```text
domain responsibility
    -> state and identity
    -> invariant
    -> commands and queries
    -> collaboration boundaries
    -> tests for transitions and failures
```

Classes should protect meaningful state and expose a cohesive interface. Composition makes dependencies explicit. Use OOP where it reduces conceptual coupling; do not introduce objects that merely rename procedural steps.

## References

1. Python Software Foundation. “Classes.” *The Python Tutorial*. Accessed 31 August 2026. https://docs.python.org/3/tutorial/classes.html
2. Python Software Foundation. “Data Model: Instance Methods.” *Python Language Reference*. Accessed 31 August 2026. https://docs.python.org/3/reference/datamodel.html#instance-methods

---

**Previous module:** Module 7 — Testing, Debugging, and Exceptions  
**Next module:** Module 9 — Python Classes and Inheritance
