# Modules 4-6 Beginner-First Redesign

**Status:** Approved  
**Date:** 25 September 2026  
**Course:** Algorithms and Programming  
**Program:** TSI International Undergraduate Program

## 1. Context

Modules 1-3 establish Python syntax, variables, basic containers, branching, iteration, and string manipulation for students with no assumed programming background. Modules 4-6 must continue that progression without requiring advanced Python features in the practicum.

The local `presentation_res` directory contains MIT 6.0001 Fall 2016 lecture slides for the relevant topics. These files are source material only and must remain outside version control. Their examples must be adapted to Python 3.10 or later and to an Industrial Systems context.

## 2. Approved approach

Use a layered design:

- detailed Markdown modules for lecture explanation and independent study;
- a clearly identified core learning path for beginners;
- technical extensions that deepen the theory without becoming practicum requirements;
- a focused practicum containing only the essential skills from each module;
- one easy task per module and one medium final task combining Modules 4-6.

## 3. Module scope

### Module 4: Decomposition, Abstraction, and Functions

Core content:

- motivation for functions;
- function definition and calls;
- parameters and arguments;
- return values;
- `print()` versus `return`;
- local variables and basic scope;
- decomposition into small functions;
- simple contracts and docstrings.

Technical extensions may cover pure functions, side effects, mutable arguments, type hints, default parameters, cohesion, and coupling. Positional-only parameters, `*args`, `**kwargs`, `nonlocal`, and higher-order functions are outside the assessed core.

Study case: decompose a production-cost calculation into small functions.

### Module 5: Tuples, Lists, and Aliasing

Core content:

- tuple and list construction;
- indexing, slicing, and iteration;
- tuple packing and unpacking;
- list mutation and common methods;
- equality and identity;
- aliasing;
- independent list copies;
- safe mutation patterns.

Technical extensions may cover shallow copies of nested lists, ownership of mutable data, and tuple immutability boundaries. Deep-copy internals and advanced hashability rules are outside the assessed core.

Study case: process shift-output records without modifying the original measurements.

### Module 6: Dictionaries and Recursion

Dictionaries will be taught before recursion because the mapping model is more concrete and later supports recursive examples.

Core content:

- dictionary creation, lookup, insertion, and update;
- membership tests and iteration;
- frequency counting;
- recursive functions;
- base cases and recursive cases;
- progress toward termination;
- tracing calls and combining returned results.

Technical extensions may cover nested dictionaries, recursive traversal, recursion limits, recursion versus iteration, and memoization as a preview. Formal recurrence analysis, induction proofs, and advanced hash-table internals are outside the assessed core.

Study case: represent component requirements in a dictionary and recursively calculate material quantities.

## 4. Practicum design

Target student file: `Practice/Modul_4-6.ipynb`

Each module section contains:

1. a brief code-based review;
2. complete runnable examples;
3. one guided completion;
4. one easy independent task;
5. validation cells that students must not edit;
6. one short conceptual checkpoint.

The module tasks are:

- Module 4: Production Cost Calculator;
- Module 5: Shift Output Summary;
- Module 6: Inventory and Package Counter.

The medium final task is a Multi-Level Bill of Materials Calculator. It combines functions, tuples, lists, dictionaries, alias-safe handling, and simple recursion. The task uses a finite acyclic bill of materials and does not require exception handling, classes, or efficiency analysis.

## 5. Instructor material

Create `Instructor-Solutions/Modul_4-6_solution.ipynb` with complete implementations, assertions, expected results, and checkpoint guidance. The student notebook must not contain solution code.

The existing `/Instructor-Solutions/` ignore rule remains in effect.

## 6. Repository policy

Add `/presentation_res/` to `.gitignore`. The directory is currently untracked, so no tracked-file removal is required.

Keep `README.md` unchanged. Media remains represented by `TODO(media)` comments only. Edited material must not use the em dash character.

## 7. Verification

- Validate Markdown structure and internal navigation.
- Run complete code examples where practical.
- Parse both notebooks as valid notebook version 4 JSON.
- Execute the instructor solution notebook from a clean kernel.
- Confirm student and solution task contracts agree.
- Confirm no answer implementation appears in the student notebook.
- Confirm `presentation_res` and `Instructor-Solutions` are ignored.
- Scan edited files for the em dash character.
- Review the Git diff for scope and accidental changes.
