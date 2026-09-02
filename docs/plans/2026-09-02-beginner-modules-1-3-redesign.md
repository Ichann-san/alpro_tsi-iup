# Beginner Redesign for Modules 1-3

**Date:** 2 September 2026  
**Status:** Approved  
**Program:** TSI International Undergraduate Program  
**Audience:** Third-semester Industrial Systems students with no assumed programming experience  
**Runtime:** Python 3.10 or later

This design supersedes the learning progression in `2026-09-01-practicum-modules-1-3-design.md`.

## 1. Design decision

Modules 1-3 will use a foundation-first spiral. Students first run a minimal Python program, then work with values and expressions, then organize several values, control program execution, and manipulate structured text.

The material will remain technically accurate, but advanced vocabulary and implementation detail will appear only after students have a concrete operation to connect it to.

The em dash character will not be used in the revised modules or notebooks. Normal hyphens and colons will be used instead.

## 2. Module sequence

### Module 1: Python Fundamentals and Introduction to Data Structures

Students will learn:

1. how to run `print("Hello, World!")`;
2. source code, output, comments, syntax, and case sensitivity;
3. `int`, `float`, `str`, and `bool` values;
4. variables, assignment, and naming;
5. arithmetic, comparison, and basic logical operators;
6. `input()`, explicit type conversion, and f-string output;
7. why several related values need a data structure;
8. basic list creation, indexing, updating, `append()`, `len()`, and `sum()`.

Stacks and queues will remain as a short conceptual preview. Students will not implement or be assessed on them in Module 1.

The module study case will be a Daily Production Calculator. It will use hourly production values to compute total production, average production, and the difference from a target.

### Module 2: Basic Branching and Iteration

Students will learn:

1. Boolean conditions;
2. `if`, `if`-`else`, and `if`-`elif`-`else`;
3. simple nested decisions;
4. `for` loops over lists and `range()`;
5. basic `while` loops;
6. counter and accumulator patterns;
7. introductory `break` and `continue`;
8. loop tracing and practical termination reasoning.

Structural pattern matching, formal loop invariants, loop `else`, mutation during collection iteration, and detailed cost analysis will be removed from the core beginner path.

The module study case will be a Production Target Tracker. It will classify daily output, count successful days, and stop at a sentinel value.

### Module 3: Basic String Manipulation

Students will learn:

1. string literals, input, and output;
2. concatenation and repetition;
3. `len()`, indexing, slicing, and membership;
4. string immutability;
5. `strip()`, `lower()`, `upper()`, `title()`, and `replace()`;
6. `split()` and `join()`;
7. basic validation with `isdigit()`;
8. f-string formatting.

Unicode internals, encoded bytes, normalization forms, and regular expressions will be limited to an optional technical preview and will not be assessed.

The module study case will be a Product Code Cleaner that converts inconsistent product data into a standard identifier.

## 3. Practicum sequence

The student notebook will contain only examples, starter code, `TODO` markers, and visible checks. Complete answers will remain in `Instructor-Solutions/Modul_1-3_solution.ipynb`, which is ignored by Git.

Each module section will contain:

1. a short executable review beginning at the learner's current level;
2. one guided completion activity;
3. one easy independent task;
4. visible `assert` checks;
5. one short checkpoint question.

The easy tasks will be:

- Module 1: Daily Production Calculator
- Module 2: Production Target Tracker
- Module 3: Product Code Cleaner

## 4. Final task

The medium final task will be the Production Line Log Challenge. It will accept a comma-separated string such as `G12,D3,G8,R2,G7`.

Students will:

- split the input into records;
- validate a one-letter status and positive integer quantity;
- count good, defective, and reworked units;
- count malformed records without terminating the program;
- track the longest continuous run of good units;
- compare good output with a production target;
- produce an exact formatted report.

The difficulty will come from parsing, state tracking, boundary cases, and ordering the conditions correctly. The solution will not require functions beyond the beginner material already demonstrated in the notebook.

## 5. Learning alignment

| Outcome | Instruction | Practice | Evidence |
| --- | --- | --- | --- |
| Execute basic Python statements | Module 1 syntax, values, variables, output | Guided expression completion | Correct observed output and assertions |
| Calculate with a simple list | Module 1 list operations | Daily Production Calculator | Correct total, average, and target difference |
| Select and repeat operations | Module 2 conditions and loops | Production Target Tracker | Correct classifications, counts, and sentinel behavior |
| Normalize structured text | Module 3 string operations | Product Code Cleaner | Correct standard code and rejected malformed input |
| Integrate Modules 1-3 | All three modules | Production Line Log Challenge | Correct counts, longest run, status, and report for normal and edge cases |

## 6. Verification requirements

Before delivery:

1. execute every complete Python example in Modules 1-3;
2. parse both notebooks as valid notebook JSON;
3. compile every code cell;
4. execute the instructor notebook from a clean namespace;
5. confirm student validation cells fail only because starter work is incomplete;
6. verify learning outcomes map to instruction and assessment;
7. confirm no em dash character exists in the revised modules or notebooks;
8. confirm the instructor solution remains ignored by Git;
9. leave the README and other practicum notebooks unchanged.

