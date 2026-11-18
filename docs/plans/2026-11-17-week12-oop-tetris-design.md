# Week 12 OOP Practicum Design

Status: Approved

Date: 17 November 2026

## Purpose and constraints

Teach the fundamentals of object-oriented programming through one small retro Tetris game. The audience is beginner students in the TSI International Undergraduate Program. The target environment is Google Colab or a browser-based Jupyter notebook with a Python kernel and ipywidgets.

The learning resources remain Markdown and a self-contained notebook. The selected System Design template informs this document's requirements, responsibilities, lifecycle, alternatives, and acceptance criteria. No separate Word deliverable is needed.

## Learning scope

Module 8 introduces classes, objects, attributes, methods, `self`, `__init__`, instance state, encapsulation, abstraction, and composition. Module 9 adds inheritance, `super()`, overriding, polymorphism, and brief notes on class attributes, properties, and `__str__`.

Advanced class mechanics, matrix rotation mathematics, and graphics programming are outside the assessed core. Examples and exercises use the same falling-block game throughout.

## Components and contracts

| Component | State | Responsibility |
| --- | --- | --- |
| `Piece` | kind, x, y, rotation | Report occupied cells, move, and rotate |
| `SquarePiece(Piece)` | Inherited piece state | Specialize construction and preserve square orientation |
| `Board` | width, height, non-public grid | Check placement, settle pieces, and clear full rows |
| `TetrisGame` | board, active piece, score, lines, game-over flag | Coordinate movement, falling, locking, spawning, and restart |
| Supplied notebook helpers | widgets and one timer task | Render the board and translate buttons into game method calls |

`Board.can_place(cells)` returns a Boolean without changing the grid. `TetrisGame.try_move(dx, dy)` commits a valid move or restores the original position and returns `False`. Rotation is also rejected without changing the prior state when the new orientation would overlap settled blocks or cross an edge.

Each board owns independent grid rows. `snapshot()` returns copied rows for display. A leading underscore communicates non-public state; it is not an access-control mechanism.

## Game lifecycle

1. Create an empty 10 by 20 board and spawn a piece.
2. Buttons request movement, rotation, or a drop.
3. Collision checks accept or reject the requested state change.
4. A timer or Down button advances one falling step.
5. A blocked downward step settles the piece, clears full rows, and adds 100 points per row.
6. Spawn the next piece. A blocked spawn ends the game.
7. Restart clears the board, score, and game-over state.

The interface starts paused. Start creates at most one background timer. Stop, restart, replacement of the interface, and game over cancel or end that timer. The notebook never starts an endless blocking loop during Run All.

## Game presentation

Use seven supplied shapes, basic rotation states, button controls, a dark background, monospace text, square cells, and a green accent. Include automatic falling, left/right movement, rotation, manual Down, hard Drop, score, completed-row clearing, game over, and restart. Wall kicks, audio, menus, and difficulty levels are excluded.

## Student work and instructor material

- Easy Module 8 task: complete `Piece.__init__` and `Piece.move`.
- Easy Module 9 task: complete `SquarePiece.__init__` and `SquarePiece.rotate`.
- Medium final task: complete `Board.can_place` and `TetrisGame.try_move`.
- Provide shape data, rendering, timer handling, line clearing, and other orchestration methods.
- Include runnable reviews, explicit contracts, unchanged validation cells, and short reflection questions.
- Store complete answers in `Instructor-Solutions/Modul_8-9_solution.ipynb`, using the existing ignore rule.

Estimated practicum time is 180 minutes. Media remains represented by TODO comments. Use full English and avoid em dashes.

## Alternatives

A text-only step game offers simpler setup but less interactive feedback. A JavaScript canvas offers smoother browser control but introduces a second programming language and more bridging code. The approved approach uses Python objects with supplied ipywidgets controls.

## Verification and delivery

Verify piece independence, board independence, movement boundaries, occupied-cell collisions, rotation rollback, one-row and multiple-row clearing, scoring, blocked spawning, hard drops, restart, and timer cancellation. Check notebook schemas, clean execution of instructor cells, matching student validation cells, and absence of instructor implementations in student task cells. Exercise actual widget callbacks locally; report any inability to run a live Colab session separately.

Deliver revised `Resources/Modul-8.md`, `Resources/Modul-9.md`, the student notebook, and the ignored instructor notebook. Leave other modules and README unchanged.
