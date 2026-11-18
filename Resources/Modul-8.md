# Week 12, Module 8: Object-Oriented Programming

**Course:** Algorithms and Programming

**Program:** TSI International Undergraduate Program

**Environment:** Python 3.10 or later; Google Colab or Jupyter for the game

**Prerequisites:** Functions, lists, dictionaries, and basic assertions

**Practical notebook:** [Mini Tetris practicum](../Practice/Modul_8-9.ipynb)

## 1. Learning goal

Object-oriented programming, or **OOP**, groups related data and operations into objects. This week, a small falling-block game makes those relationships visible.

After this module, you should be able to:

- create a class and independent objects;
- initialize attributes with `__init__`;
- use `self` inside methods;
- distinguish instance attributes from class attributes;
- explain encapsulation, abstraction, and composition.

The notebook builds Mini Tetris with a 10-column, 20-row board. Display code and shape definitions are supplied. You complete selected Python methods.

<!-- TODO(media): Add an animation showing two Piece objects with independent positions and the effect of calling move() on one object. Suggested path: ../Assets/Module-8/piece-instances.mp4 -->

## 2. From separate values to an object

A falling block has a position. It can also move.

```python
class BlockExample:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


block = BlockExample(x=3, y=0)
block.move(1, 2)

print(block.x, block.y)
assert (block.x, block.y) == (4, 2)
```

Expected output:

```text
4 2
```

The class describes how blocks store and change their position. Each created block holds its own current position.

## 3. Class, object, attribute, and method

| Term | Meaning | Example |
| --- | --- | --- |
| Class | Definition used to create objects | `BlockExample` |
| Object or instance | One value created from a class | `block` |
| Attribute | A named value associated with an object | `block.x` |
| Method | An operation called through an object | `block.move(1, 2)` |
| State | The object's current attribute values | x is 4, y is 2 |

Python classes combine data with functionality [1]. A method can read or change the attributes associated with its instance.

## 4. Initialization and self

`BlockExample(x=3, y=0)` creates an instance and calls its initializer.

```python
first = BlockExample(x=3, y=0)
second = BlockExample(x=3, y=0)

first.move(-1, 1)

assert (first.x, first.y) == (2, 1)
assert (second.x, second.y) == (3, 0)
assert first is not second
```

Inside `move()`, `self` refers to the receiving object. Calling `first.move(...)` changes first; it does not change second.

Technical points:

- `__init__` initializes an instance after it has been created.
- Use `self.name` for state needed by other methods.
- A variable assigned without `self` is normally local to that method call.
- An initializer should not return a calculated result.

## 5. Instance and class attributes

An **instance attribute** holds state for one object. A **class attribute** belongs to the class and is available through its instances [1].

```python
class BoardExample:
    EMPTY = 0

    def __init__(self, width=4):
        self.width = width
        self._cells = [self.EMPTY] * width


first_board = BoardExample()
second_board = BoardExample()

assert BoardExample.EMPTY == 0
assert first_board.width == 4
assert first_board._cells is not second_board._cells
```

The immutable constant `EMPTY` is shared. Each instance receives a new list.

Create mutable board state inside `__init__`. Putting one grid list directly in the class body would share that list across game boards.

## 6. Encapsulation: let the object manage its data

**Encapsulation** groups state with the methods responsible for using it. In Python, a leading underscore marks an implementation detail by convention [1].

Extend the small board example with operations:

```python
class BoardExample:
    EMPTY = 0

    def __init__(self, width=4):
        self.width = width
        self._cells = [self.EMPTY] * width

    def occupy(self, x):
        if x < 0 or x >= self.width:
            raise ValueError("Position outside the board.")
        if self._cells[x] != self.EMPTY:
            raise ValueError("Position already occupied.")
        self._cells[x] = 1

    def snapshot(self):
        return self._cells.copy()


board = BoardExample()
board.occupy(1)

view = board.snapshot()
view[1] = 0

assert board.snapshot() == [0, 1, 0, 0]
```

The caller uses `occupy()` rather than changing the board's internal list. `snapshot()` returns a copy, so changes to the returned list do not change the board.

The underscore does not enforce privacy. It communicates which attributes callers should leave to the class.

This short example uses one row. The notebook's `Board` uses a list of independent rows.

## 7. Abstraction: use an operation through its interface

**Abstraction** exposes the operations a caller needs while hiding unnecessary implementation details.

A game can ask:

```text
board.can_place(piece.cells())
```

The caller needs a Boolean answer. The board owns the loop that checks boundaries and occupied positions.

The full board offers a small interface:

| Method | Purpose | Changes board state? |
| --- | --- | --- |
| `can_place(cells)` | Check whether coordinates are valid and empty | No |
| `place(piece)` | Store a valid piece as settled cells | Yes |
| `clear_lines()` | Remove full rows and return their count | Yes |
| `snapshot()` | Return copied rows for display or tests | No |

Encapsulation concerns how state is managed. Abstraction concerns what callers need to know to use an object.

<!-- TODO(media): Add a diagram showing TetrisGame calling Board.can_place() while boundary and occupancy checks remain inside Board. Suggested path: ../Assets/Module-8/board-interface.png -->

## 8. Composition: one object contains others

**Composition** describes a has-a relationship. A game has a board and an active piece.

```python
class GameExample:
    def __init__(self):
        self.board = BoardExample(width=4)
        self.active = BlockExample(x=0, y=0)

    def step(self):
        self.active.move(0, 1)


demo_game = GameExample()
demo_game.step()

assert demo_game.active.y == 1
assert demo_game.board.snapshot() == [0, 0, 0, 0]
```

This example only demonstrates object ownership. The notebook adds collision checks and settlement.

The full game divides responsibility:

- `Piece` describes occupied coordinates and changes its position.
- `Board` decides whether coordinates fit.
- `TetrisGame` accepts a valid move or restores the old position.
- Supplied notebook helpers display the result and process buttons.

The game does not inherit from the board. Their relationship is has-a, rather than is-a.

## 9. Test objects by observing state

Check what changes after a command and what remains unchanged after failure.

```python
board = BoardExample(width=4)
before = board.snapshot()
error_detected = False

try:
    board.occupy(-1)
except ValueError:
    error_detected = True

assert error_detected
assert board.snapshot() == before
```

Useful game checks include:

- moving one piece leaves another piece unchanged;
- two boards do not share their grid;
- an invalid move preserves the old position;
- a snapshot cannot be used to modify the original board.

These checks continue the testing and exception concepts from Module 7.

## 10. Practicum task

In [Modul_8-9.ipynb](../Practice/Modul_8-9.ipynb), complete Easy Task 1:

1. initialize the Piece object's kind, position, and rotation;
2. implement its movement method;
3. run the supplied checks for independent instances.

Later, the final task adds board validation and object collaboration. The display, buttons, rotation data, and row-clearing algorithm are supplied.

## 11. Knowledge check

1. How does a class differ from an instance?
2. What does self refer to in a method?
3. Why should a board's mutable grid be created in its initializer?
4. What does a leading underscore communicate?
5. How does snapshot protect the board from accidental caller mutation?
6. How do encapsulation and abstraction differ?
7. Why is a game containing a board an example of composition?

## References

1. Python Software Foundation. "Classes." *The Python Tutorial*. Accessed 17 November 2026. https://docs.python.org/3.10/tutorial/classes.html

---

**Previous module:** [Module 7: Testing, Debugging, Exceptions, and Assertions](Modul-7.md)

**Next module:** [Module 9: Python Classes and Inheritance](Modul-9.md)
