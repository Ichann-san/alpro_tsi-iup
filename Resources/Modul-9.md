# Module 9 — Python Classes and Inheritance

> **Course:** Algorithms and Programming  
> **Programming language:** Python  
> **Supported runtime:** Python 3.10 or later  
> **Resource type:** Technical learning module  
> **Practical notebook:** Deferred to `../Practice/Modul_8-9.ipynb`  
> **Estimated study time:** 4 hours

## 1. Module scope

Inheritance creates a specialization relationship between classes and participates in attribute lookup. A correct subclass must preserve the usable contract of its base class, not merely reuse code. Python combines inheritance with dynamic dispatch, method resolution order (MRO), abstract base classes, data classes, and special-method protocols.

This module covers class mechanics, method categories, overriding, `super()`, polymorphism, abstract interfaces, value objects, special methods, multiple inheritance, and composition alternatives.

<!-- TODO(media): Add an animation showing instance attribute lookup through a class hierarchy and dynamic dispatch to an overriding method. Suggested path: ../Assets/Module-9/attribute-lookup-dispatch.mp4 -->

## 2. Learning outcomes

After completing this module, a student should be able to:

1. **Trace** attribute lookup through an instance, class, and MRO.
2. **Implement** a subclass that preserves base-class invariants and contracts.
3. **Use** `super()` for cooperative delegation.
4. **Distinguish** instance methods, class methods, and static methods.
5. **Define** an abstract interface with `ABC` and `@abstractmethod`.
6. **Apply** polymorphism without explicit type-switch chains.
7. **Implement** selected special methods with consistent semantics.
8. **Construct** immutable-style value objects with `@dataclass`.
9. **Choose** inheritance, composition, or protocol-based design.

## 3. Inheritance semantics

`class Subclass(BaseClass):` creates a class whose MRO includes `BaseClass`. Attribute lookup on an instance generally checks:

```text
instance
    -> instance class
    -> base classes in MRO order
    -> AttributeError
```

Classes support multiple base classes, and Python computes a consistent MRO for cooperative lookup [1].

```python
class Message:
    def render(self):
        return "generic"


class WarningMessage(Message):
    def render(self):
        return "warning"


message = WarningMessage()

print(message.render())
print([cls.__name__ for cls in WarningMessage.__mro__])

assert message.render() == "warning"
assert WarningMessage.__mro__[:2] == (WarningMessage, Message)
```

The runtime instance determines which `render` implementation is found. This is **dynamic dispatch**.

## 4. Subtyping and contract preservation

A subclass used where a base class is expected should satisfy the base contract:

- accept all states and inputs promised by the base interface;
- preserve base invariants;
- return compatible results;
- not introduce surprising stronger preconditions; and
- not weaken guaranteed postconditions.

Code reuse alone is not evidence of an is-a relationship.

### 4.1 Valid specialization

```python
class Rectangle:
    def __init__(self, width, height):
        if width < 0 or height < 0:
            raise ValueError("dimensions must be non-negative")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)


shape = Square(4)
assert shape.area() == 16
assert isinstance(shape, Rectangle)
```

This limited immutable-dimension interface permits substitution. If `Rectangle` exposed independent width and height setters, forcing equality in `Square` could violate caller expectations. Contract details determine whether the hierarchy remains valid.

## 5. Overriding methods

An override replaces inherited behaviour at the same method name.

```python
class DiscountPolicy:
    def discount(self, subtotal):
        return 0.0


class PercentageDiscount(DiscountPolicy):
    def __init__(self, rate):
        if not 0 <= rate <= 1:
            raise ValueError("rate must be between 0 and 1")
        self.rate = rate

    def discount(self, subtotal):
        if subtotal < 0:
            raise ValueError("subtotal cannot be negative")
        return subtotal * self.rate


policy = PercentageDiscount(0.10)
assert policy.discount(200) == 20.0
```

Keep signature and failure semantics compatible with the abstraction. A subclass that only accepts integers when the base accepts any real subtotal strengthens the precondition and may break substitution.

## 6. Delegation with `super()`

`super()` delegates to the next implementation in the current MRO, not necessarily to one textually named parent [1].

```python
class LoggedCounter:
    def __init__(self, value=0):
        self.value = value
        self.events = []

    def increment(self):
        self.value += 1


class AuditedCounter(LoggedCounter):
    def increment(self):
        before = self.value
        super().increment()
        self.events.append((before, self.value))


counter = AuditedCounter(4)
counter.increment()

assert counter.value == 5
assert counter.events == [(4, 5)]
```

Use `super()` consistently in cooperative hierarchies. Directly naming a base class can skip another class in a multiple-inheritance MRO.

<!-- TODO(media): Add an MRO animation showing super() dispatching to the next class rather than a hard-coded parent. Suggested path: ../Assets/Module-9/super-mro.gif -->

## 7. Method categories

### 7.1 Instance method

Receives a bound instance as `self`. Use it when behaviour reads or changes instance state.

### 7.2 Class method

Decorated with `@classmethod` and receives the class as `cls`. Common use: alternate constructors that respect subclasses.

### 7.3 Static method

Decorated with `@staticmethod` and receives no automatic instance or class argument. Use it for a helper that belongs conceptually in the class namespace but needs no object state.

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = float(celsius)

    @classmethod
    def from_fahrenheit(cls, fahrenheit):
        return cls((fahrenheit - 32) * 5 / 9)

    @staticmethod
    def is_valid_celsius(value):
        return value >= -273.15


temperature = Temperature.from_fahrenheit(68)

assert round(temperature.celsius, 10) == 20.0
assert Temperature.is_valid_celsius(20)
```

A static method is not a substitute for a module-level function when the operation has no conceptual relation to the class.

## 8. Abstract base classes

The `abc` module supplies infrastructure for abstract base classes (ABCs) [2]. An abstract method defines an operation subclasses must implement before instantiation.

```python
from abc import ABC, abstractmethod
from math import pi


class Shape(ABC):
    @abstractmethod
    def area(self):
        """Return non-negative area."""


class Circle(Shape):
    def __init__(self, radius):
        if radius < 0:
            raise ValueError("radius cannot be negative")
        self.radius = radius

    def area(self):
        return pi * self.radius ** 2


class RectangleShape(Shape):
    def __init__(self, width, height):
        if width < 0 or height < 0:
            raise ValueError("dimensions cannot be negative")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


shapes = [Circle(1), RectangleShape(2, 3)]
areas = [shape.area() for shape in shapes]

assert round(areas[0], 5) == 3.14159
assert areas[1] == 6
```

`Shape()` cannot be instantiated while `area` remains abstract. An ABC formalizes a nominal interface; it does not automatically validate every semantic promise in the docstring.

## 9. Polymorphism

**Polymorphism** allows one operation to work with objects providing compatible behaviour.

```python
def total_area(shapes):
    return sum(shape.area() for shape in shapes)


result = total_area([Circle(2), RectangleShape(3, 4)])
assert round(result, 5) == round(4 * pi + 12, 5)
```

`total_area` does not inspect concrete types. Each object supplies `area()`.

Python also supports structural “duck typing”: an object may participate when it provides the required operations even without inheriting from a named base. Use ABCs when nominal registration, shared semantics, or enforced abstract methods add value.

## 10. Special methods and protocols

Special methods integrate a class with Python syntax and built-ins [3].

| Method | Protocol |
| --- | --- |
| `__repr__` | Developer-oriented representation |
| `__str__` | User-oriented text |
| `__len__` | `len(obj)` |
| `__iter__` | Iteration |
| `__contains__` | `item in obj` |
| `__eq__` | Value equality |
| `__hash__` | Hashing |
| `__enter__` / `__exit__` | Context management |

```python
class CourseRoster:
    def __init__(self, course_code):
        self.course_code = course_code
        self._students = []

    def add(self, student_id):
        if student_id in self._students:
            raise ValueError("duplicate student")
        self._students.append(student_id)

    def __len__(self):
        return len(self._students)

    def __contains__(self, student_id):
        return student_id in self._students

    def __repr__(self):
        return f"CourseRoster({self.course_code!r}, size={len(self)})"


roster = CourseRoster("CS204")
roster.add("S001")

assert len(roster) == 1
assert "S001" in roster
assert repr(roster) == "CourseRoster('CS204', size=1)"
```

Implement a protocol only when its conventional meaning fits. `len()` must return a non-negative integer.

## 11. Equality and hashing

Value equality should compare the state that defines domain value. Hashing must satisfy:

```text
if a == b, then hash(a) == hash(b)
```

Mutable equality-relevant state makes stable hashing unsafe. Python normally makes a class unhashable when custom value equality is defined without a compatible hash.

Use immutable value objects as dictionary keys.

## 12. Data classes

`@dataclass` can generate methods such as `__init__`, `__repr__`, and `__eq__` from annotated fields [4].

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


origin = Coordinate(0, 0)
point = Coordinate(3, -2)

assert point == Coordinate(3, -2)
assert point.manhattan_distance(origin) == 5
assert {point: "checkpoint"}[Coordinate(3, -2)] == "checkpoint"
```

`frozen=True` prevents ordinary field assignment and normally enables generated hashing when equality is generated. It does not recursively freeze referenced mutable objects.

### 12.1 Post-initialization validation

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Percentage:
    value: float

    def __post_init__(self):
        if not 0 <= self.value <= 100:
            raise ValueError("percentage outside [0, 100]")


assert Percentage(75).value == 75
```

Use a regular class when generated field-oriented behaviour does not match the desired interface.

<!-- TODO(media): Add a comparison animation of a hand-written value class and equivalent frozen dataclass, including generated equality and representation. Suggested path: ../Assets/Module-9/dataclass-generation.mp4 -->

## 13. Multiple inheritance

Python permits multiple base classes. MRO determines lookup order [1].

```python
class TimestampMixin:
    def metadata(self):
        return {"timestamped": True}


class Serializable:
    def serialize(self):
        return {"type": type(self).__name__}


class Event(TimestampMixin, Serializable):
    pass


event = Event()

assert event.metadata() == {"timestamped": True}
assert event.serialize() == {"type": "Event"}
assert Event.__mro__[:3] == (Event, TimestampMixin, Serializable)
```

Multiple inheritance is most manageable when:

- mixins have narrow responsibilities;
- state ownership is explicit;
- cooperative methods accept compatible signatures; and
- every participating implementation uses `super()` consistently.

Avoid deep hierarchies whose valid combinations are difficult to reason about.

## 14. Composition versus inheritance

Choose inheritance when:

- a real substitutable is-a relationship exists;
- base semantics are stable and documented;
- dynamic dispatch across variants is required; and
- subclass invariants can preserve the base contract.

Choose composition when:

- behaviour must be replaceable at runtime;
- components have independent lifecycles;
- reuse does not imply subtyping;
- several strategies must be combined; or
- inheritance would expose irrelevant methods.

Strategy through composition:

```python
class NoDiscount:
    def discount(self, subtotal):
        return 0


class Checkout:
    def __init__(self, discount_policy):
        self._discount_policy = discount_policy

    def total(self, subtotal):
        return subtotal - self._discount_policy.discount(subtotal)


checkout = Checkout(PercentageDiscount(0.25))
assert checkout.total(80) == 60
```

`Checkout` is not a discount policy; it collaborates with one.

## 15. Inheritance testing

Test a subclass against:

- base-interface cases;
- subclass-specific cases;
- base invariants after overridden methods;
- failure compatibility;
- MRO and cooperative initialization when multiple inheritance is used; and
- polymorphic client functions.

```python
def assert_discount_contract(policy):
    assert policy.discount(0) == 0
    assert policy.discount(100) >= 0
    assert policy.discount(100) <= 100


assert_discount_contract(DiscountPolicy())
assert_discount_contract(PercentageDiscount(0.20))
```

Contract tests do not replace subclass-specific tests, but they expose broken substitutability.

## 16. Common failure modes

### 16.1 Inheritance for code reuse only

Shared code does not establish a subtype relationship. Extract a collaborator or function.

### 16.2 Stronger subclass precondition

Base clients may supply valid inputs that the subclass rejects.

### 16.3 Direct base-class call in cooperative hierarchy

`Base.method(self)` can skip MRO participants. Prefer `super()`.

### 16.4 Incorrect special-method semantics

Syntax protocols carry expectations. Surprising `__len__` or `__eq__` behaviour damages generic code.

### 16.5 Mutable hashable object

Changing equality-relevant state after dictionary insertion can make the object unreachable by lookup.

### 16.6 Overuse of type checks

A long `isinstance` chain can indicate missing polymorphic behaviour.

### 16.7 Deep hierarchy

Behaviour distributed across many ancestors becomes difficult to locate and validate.

### 16.8 Frozen means deeply immutable

A frozen dataclass can still reference mutable objects.

## 17. Guided practice

### 17.1 MRO trace

Create classes `A`, `B(A)`, `C(A)`, and `D(B, C)`. Print `D.__mro__` and predict which override runs.

### 17.2 Contract audit

For a base `Storage.read(key) -> bytes` contract, evaluate a subclass that returns `None` for missing keys while the base promises `KeyError`.

### 17.3 Composition conversion

Replace an inheritance relationship `ReportPrinter(Report)` with a report object and printer collaborator. State the reduced coupling.

## 18. Independent practice

### Exercise 1 — Shape hierarchy

Implement an abstract `Shape` with `area()` and `perimeter()`. Add validated rectangle and circle subclasses.

**Success criteria:** polymorphic aggregate functions work without concrete type checks.

### Exercise 2 — Value object

Implement a frozen `StudentId` dataclass with normalized department and numeric identifier fields.

**Requirements:** validation in `__post_init__`, stable equality, and dictionary-key use.

### Exercise 3 — Cooperative mixin

Create a narrow audit mixin that records successful state transitions while delegating with `super()`.

**Deliverable:** MRO explanation and tests proving the base transition still occurs once.

### Exercise 4 — Hierarchy review

Review a supplied hierarchy for substitutability violations. Recommend inheritance or composition for every relationship and justify the contract effects.

## 19. Knowledge check

1. What determines Python's attribute lookup order?
2. What must a valid subtype preserve?
3. What does zero-argument `super()` mean?
4. When is a class method useful?
5. What does `@abstractmethod` enforce?
6. What requirement connects equality and hashing?
7. Does `frozen=True` recursively freeze fields?
8. When is composition preferable to inheritance?

<details>
<summary>Answer key</summary>

1. The instance, its class, and base classes in the computed MRO.
2. The usable base contract, including accepted inputs, invariants, results, and failure semantics.
3. Delegate to the next implementation in the current MRO.
4. For behaviour associated with the class, especially alternate constructors that preserve subclass construction.
5. Classes retaining abstract methods cannot be instantiated.
6. Equal objects must have equal hash values.
7. No. Referenced mutable objects remain mutable.
8. When reuse does not imply subtyping, components vary independently, or runtime collaboration is clearer.

</details>

## 20. Module synthesis

Hierarchy decision:

```text
shared interface
    -> substitutable semantics?
        -> yes: inheritance or ABC
        -> no: composition or standalone protocol
```

Inheritance participates in contracts and lookup, not only reuse. Keep hierarchies shallow, use `super()` cooperatively, and test base behaviour against every subtype. Use data classes for field-oriented value objects and composition for independent collaborators.

## References

1. Python Software Foundation. “Classes: Inheritance and Multiple Inheritance.” *The Python Tutorial*. Accessed 31 August 2026. https://docs.python.org/3/tutorial/classes.html#inheritance
2. Python Software Foundation. “`abc` — Abstract Base Classes.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/abc.html
3. Python Software Foundation. “Data Model: Special Method Names.” *Python Language Reference*. Accessed 31 August 2026. https://docs.python.org/3/reference/datamodel.html#special-method-names
4. Python Software Foundation. “`dataclasses` — Data Classes.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/dataclasses.html

---

**Previous module:** Module 8 — Object-Oriented Programming  
**Next module:** Module 10 — Program Efficiency
