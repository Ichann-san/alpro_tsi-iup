# Practicum Modules 1–3: Approved Design

**Date:** 1 September 2026  
**Artifact:** `Practice/Modul_1-3.ipynb`  
**Audience:** College students who have completed theory Modules 1–3  
**Language:** English  
**Runtime:** Python 3.10 or later, standard library only

## 1. Instructional objective

The practicum will move from reviewed examples to partially scaffolded implementation, then to independent application. It will assess whether students can use elementary data structures, control flow, and string operations together in a small deterministic program.

The student notebook will contain instructions, starter code, explicit `TODO` markers, and visible validation cells. It will not contain completed answers. Instructor solutions will be stored separately in an ignored local directory.

## 2. Learning alignment

| Section | Observable performance | Evidence |
| --- | --- | --- |
| Module 1 | Select and operate on stack- and queue-like structures while preserving stated invariants | Completed bounded request queue and passing assertions |
| Module 2 | Construct terminating branches and loops and explain their stop conditions | Completed guarded counter and request-processing loop with passing assertions |
| Module 3 | Normalize, split, validate, and format text without mutating strings | Completed request-record normalizer with passing assertions |
| Final task | Integrate Modules 1–3 into a deterministic command processor | Correct queue state, event log, rejection behavior, and summary across representative cases |

## 3. Notebook sequence

Each module section will use the same learning progression:

1. A brief technical review using a complete executable example.
2. One guided completion snippet with constrained missing logic.
3. One easy independent task with a precise contract and visible tests.
4. A short checkpoint identifying the relevant invariant, termination condition, or normalization rule.

The final section will contain one medium-difficulty integration task.

## 4. Tasks

### Module 1 — data structures

- Review: list stack operations, `deque` queue operations, aliases, and state invariants.
- Guided completion: complete queue insertion and removal behavior.
- Easy task: implement a bounded request queue that retains valid FIFO behavior and rejects overflow without exposing internal state.

### Module 2 — branching and iteration

- Review: mutually exclusive branches, `for`, `while`, `break`, and explicit termination.
- Guided completion: complete a `while True` counter whose `if` branch stops at a defined limit.
- Easy task: process a finite sequence of request statuses, skip invalid entries, stop on a sentinel, and count accepted entries.

### Module 3 — string manipulation

- Review: string immutability, indexing, slicing, trimming, case normalization, splitting, joining, and f-string formatting.
- Guided completion: complete a text-normalization pipeline.
- Easy task: normalize and validate a pipe-delimited student request record using direct string methods.

### Final task — Campus Help-Desk Queue Processor

Students will complete a processor for textual commands such as `ADD`, `SERVE`, and `QUIT`. The processor will:

- normalize command text and fields;
- validate record structure and priority values;
- store requests in high- and normal-priority FIFO queues;
- control processing with branches and terminating loops;
- reject malformed commands without corrupting queue state;
- return a deterministic event log and final summary.

The task is medium difficulty because students must coordinate multiple contracts and edge cases, but it requires no topic beyond Modules 1–3.

## 5. Feedback and assessment

- Student-facing checks will use visible `assert` statements and descriptive failure messages.
- Starter cells will remain syntactically valid by using `pass`, placeholder values, or `NotImplementedError` where appropriate.
- Tests will cover nominal input, empty state, capacity or boundary behavior, malformed records, sentinel termination, normalization, and ordering.
- Rubrics will reward contract correctness, data-structure choice, termination, normalization, output format, and code clarity.
- The notebook will state that modifying tests does not constitute task completion.

## 6. File and repository policy

- Populate `Practice/Modul_1-3.ipynb` with the student practicum.
- Create `Instructor-Solutions/Modul_1-3_solution.ipynb` with fully executable solutions.
- Add `/Instructor-Solutions/` to `.gitignore`; the solution notebook must remain local and untracked.
- Do not modify the README or other practicum notebooks.

## 7. Verification

Before delivery:

1. Parse both notebooks as valid notebook JSON.
2. Compile every Python code cell.
3. Execute all complete review cells.
4. Confirm that expected student starter checks fail for missing work rather than syntax defects.
5. Execute the instructor notebook from a clean namespace and require all checks to pass.
6. Confirm Git ignores the instructor solution and that deferred files are unchanged.

