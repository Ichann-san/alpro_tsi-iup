# Week 12, Module 9: Python Classes and Inheritance

**Course:** Algorithms and Programming

**Program:** TSI International Undergraduate Program

**Environment:** Python 3.10 or later; Google Colab or Jupyter for the game

**Prerequisite:** Module 8

**Practical notebook:** [Mini Tetris practicum](../Practice/Modul_8-9.ipynb)

## 1. Learning goal

Module 8 introduced objects and composition. This module adds specialization: different pieces can share an interface while providing different behavior.

After this module, you should be able to:

- define a subclass;
- initialize inherited state with `super()`;
- override a method;
- explain polymorphism through a shared method call;
- choose inheritance or composition for a simple relationship;
- read a property and use a basic special method.

The game uses one base piece class and one square subclass. The other shapes use supplied coordinate data rather than separate classes.

<!-- TODO(media): Add an animation of a T piece changing orientation while a SquarePiece keeps its orientation after the same rotate() call. Suggested path: ../Assets/Module-9/piece-polymorphism.mp4 -->

## 2. Start with shared behavior

A base class contains state and operations shared by its instances.

This small example represents a piece's name and rotation index. It omits coordinates so the inheritance mechanism remains visible.

```python
class DemoPiece:
    def __init__(self, kind):
        self.kind = kind
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

    def __str__(self):
        return f"{self.kind}: rotation {self.rotation}"


tee = DemoPiece("T")
tee.rotate()

assert tee.rotation == 1
print(tee)
```

Expected output:

```text
T: rotation 1
```

The modulo operation cycles through indices 0, 1, 2, and 3. The full notebook uses the number of supplied orientations for each shape.

## 3. Inheritance: specialize a class

A **subclass**, or child class, inherits from a **base class**, or parent class [1].

```text
class ChildClass(ParentClass):
    ...
```

A square piece is a kind of piece. It shares attributes and methods with other pieces, but rotating the square should leave it unchanged.

```python
class DemoSquare(DemoPiece):
    def __init__(self):
        super().__init__("O")

    def rotate(self):
        return None


square = DemoSquare()

assert square.kind == "O"
assert square.rotation == 0
assert isinstance(square, DemoPiece)
```

`DemoSquare` inherits the parent behavior unless it defines a method with the same name.

## 4. Initialization with super

In this single-inheritance example, `super().__init__("O")` runs the base initializer for the current object.

It initializes `kind` and `rotation`. It does not create a second separate piece.

Without base initialization, methods expecting those attributes may fail.

Use the same idea in the practicum:

```text
SquarePiece.__init__
    initializes the inherited Piece state for kind "O"
```

A child initializer may add extra state when needed. The square needs no extra state in this game.

## 5. Method overriding

**Overriding** means defining a method in the child with the same name as an inherited method.

```python
tee = DemoPiece("T")
square = DemoSquare()

tee.rotate()
square.rotate()

assert tee.rotation == 1
assert square.rotation == 0
```

Both objects provide `rotate()`, but each class supplies the applicable behavior.

Keep the method's input and return expectations compatible with the base interface. Here, both implementations accept no additional arguments and return `None`.

## 6. Polymorphism: use the same interface

**Polymorphism** lets code use different objects through compatible operations.

```python
pieces = [DemoPiece("T"), DemoSquare()]

for piece in pieces:
    piece.rotate()

assert pieces[0].rotation == 1
assert pieces[1].rotation == 0
```

The loop calls `rotate()` without choosing a concrete implementation itself. Python finds the method associated with each object.

In the complete game, `TetrisGame.try_rotate()` calls the active piece's rotation method, then asks the board whether the result fits. An invalid rotation restores the earlier orientation.

The square specialization is intentionally small. The example shows how shared method calls work; it does not require a deep class hierarchy.

## 7. Inheritance and composition serve different relationships

| Relationship | Design choice | Reason |
| --- | --- | --- |
| SquarePiece is a Piece | Inheritance | It supports the piece interface |
| TetrisGame has a Board | Composition | The game coordinates a separate object |
| TetrisGame has an active Piece | Composition | The active piece changes during play |
| Display uses a TetrisGame | Collaboration through a reference | It reads state and calls game methods |

Avoid making `TetrisGame` inherit from `Board` only to reuse board methods. A game owns more than a grid.

The four central OOP ideas now have concrete examples:

- **Encapsulation:** the board manages its non-public grid.
- **Abstraction:** callers use operations such as can_place without repeating internal checks.
- **Inheritance:** SquarePiece specializes Piece.
- **Polymorphism:** one rotate call works with different piece objects.

<!-- TODO(media): Add a diagram distinguishing the SquarePiece is-a relationship from the TetrisGame has-a relationships. Suggested path: ../Assets/Module-9/inheritance-and-composition.png -->

## 8. A property for observing state

A property allows method-controlled access using attribute syntax.

```python
class ScoreExample:
    def __init__(self):
        self._score = 0

    @property
    def score(self):
        return self._score

    def award_lines(self, count):
        if count < 0:
            raise ValueError("Line count cannot be negative.")
        self._score += 100 * count


result = ScoreExample()
result.award_lines(2)

assert result.score == 200
```

Read `result.score` without parentheses. The property has no setter, so ordinary assignment to `result.score` raises `AttributeError`.

The underscore itself does not enforce privacy. The property provides a public reading interface while game methods own score changes.

In the full game, `game.score` follows this pattern.

## 9. A special method for readable output

A **special method** integrates an object with a Python operation. Python calls `__str__` when formatting an object as a readable string [1].

```python
piece = DemoPiece("L")
piece.rotate()

assert str(piece) == "L: rotation 1"
print(piece)
```

Expected output:

```text
L: rotation 1
```

The notebook supplies this method. More advanced special methods, class methods, static methods, and multiple inheritance are optional later study; they are not needed to complete the game.

## 10. Follow one game action

When the player clicks Left:

1. The supplied interface calls `game.try_move(-1, 0)`.
2. The game asks its active piece to change position.
3. The board checks the proposed occupied cells.
4. The game accepts a valid move or restores the previous position.
5. The display reads the resulting state.

When downward movement fails, the game settles the piece, clears full rows, updates the score, and creates another active piece.

The interface owns buttons and timing. The Python objects own game rules. Rendering and control helpers are supplied so the assessed work stays focused on OOP.

## 11. Practicum tasks

Open [Modul_8-9.ipynb](../Practice/Modul_8-9.ipynb).

### Easy Task 2: square specialization

Complete the SquarePiece initializer using super, then override rotate to keep its state unchanged. Run the polymorphism checks.

### Final task: make the objects collaborate

Complete Board.can_place and TetrisGame.try_move.

Success conditions:

- cells outside the board are rejected;
- occupied cells block movement;
- rejected moves preserve the old position;
- downward settlement and row clearing still work;
- the completed game runs through the supplied notebook buttons.

Add two tests using fresh objects and explain one example of inheritance and one example of composition from your implementation.

## 12. Knowledge check

1. What does a subclass inherit?
2. Why does the square initializer call super?
3. What does overriding change?
4. How does the shared rotate loop demonstrate polymorphism?
5. Why should the game contain a Board instead of inherit from it?
6. What is the difference between game.score and a method call?
7. Which object decides whether a proposed position fits?
8. What state must be restored after an invalid move?

## References

1. Python Software Foundation. "Classes: Inheritance and Private Variables." *The Python Tutorial*. Accessed 17 November 2026. https://docs.python.org/3.10/tutorial/classes.html

---

**Previous module:** [Module 8: Object-Oriented Programming](Modul-8.md)

**Next module:** [Module 10: Program Efficiency](Modul-10.md)
