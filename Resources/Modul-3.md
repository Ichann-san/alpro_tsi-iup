# Module 3 — String Manipulation

> **Course:** Algorithms and Programming  
> **Programming language:** Python  
> **Supported runtime:** Python 3.10 or later  
> **Resource type:** Technical learning module  
> **Practical notebook:** Deferred to `../Practice/Modul_1-3.ipynb`  
> **Estimated study time:** 3–4 hours

## 1. Module scope

Text processing includes representation, indexing, normalization, tokenization, validation, formatting, and encoding. Python's `str` type represents immutable Unicode text; `bytes` represents binary octets. Treating those types as interchangeable is a source of corrupted data and failed comparisons.

This module focuses on deterministic transformations and explicit contracts. Regular expressions are introduced for pattern-based work, but direct string operations remain preferable when the grammar is simple.

<!-- TODO(media): Add an animation showing Unicode text transformed through normalization, tokenization, validation, and encoding. Include code-point and byte views with descriptive alt text. Suggested path: ../Assets/Module-3/text-processing-pipeline.mp4 -->

## 2. Learning outcomes

After completing this module, a student should be able to:

1. **Distinguish** Unicode text, code points, encoded bytes, and user-perceived characters.
2. **Apply** indexing and slicing while respecting string immutability.
3. **Construct** normalization pipelines using case conversion, trimming, replacement, splitting, and joining.
4. **Format** values with f-strings and the format specification mini-language.
5. **Encode and decode** text with an explicit character encoding and error policy.
6. **Select** direct string methods or regular expressions from the required pattern complexity.
7. **Diagnose** boundary errors, unintended escape processing, lossy normalization, and encoding mismatches.

## 3. Prerequisites

Students should be able to:

- write conditional statements and loops;
- trace sequence indexing; and
- distinguish mutable and immutable objects at an introductory level.

All examples use the standard library.

## 4. Text representation

### 4.1 `str`

Python `str` is an immutable sequence of Unicode code points [1]. Python has no separate character type: indexing a string returns another string of length one.

```python
text = "Data"

print(len(text))
print(text[0], text[-1])
print(type(text[0]).__name__)

assert len(text) == 4
assert text[0] == "D"
assert text[-1] == "a"
```

Expected output:

```text
4
D a
str
```

A Unicode **code point** is not always a displayed character. Combining marks and multi-code-point emoji sequences can produce one user-perceived grapheme. Therefore, `len(text)` is not a universal measure of visible symbols.

### 4.2 `bytes`

`bytes` is an immutable sequence of integers from `0` through `255`. Text becomes bytes through **encoding**; bytes become text through **decoding**.

```text
Unicode text --encode(codec)--> bytes
bytes --decode(codec)--> Unicode text
```

The codec is part of the data contract. UTF-8 is widely used, but a program must not guess an encoding when the producer defines one.

### 4.3 Immutability

This is invalid:

```python
name = "Mira"
# name[0] = "K"  # TypeError: 'str' object does not support item assignment
```

Create a new value instead:

```python
name = "Mira"
renamed = "K" + name[1:]

print(renamed)
assert renamed == "Kira"
assert name == "Mira"
```

## 5. Literals and escape processing

Quoted literals may use single, double, or triple delimiters. Backslash introduces escapes such as `\n`, `\t`, and `\\`.

```python
record = "alpha\t42\nbeta\t17"
print(record)
```

Expected output:

```text
alpha	42
beta	17
```

A raw string literal such as `r"\d+\.\d+"` preserves backslashes for the regular-expression parser. Raw literals still obey lexical rules: they cannot end with an odd number of backslashes.

Use raw strings for most regular-expression patterns and Windows-style literal paths. Use ordinary strings when Python escape processing is intended.

## 6. Indexing and slicing

For a string of length `n`, valid positive indices are `0` through `n - 1`. Negative indices count from the end.

The slice `text[start:stop:step]` selects positions in a half-open interval; `stop` is excluded.

```python
code = "ALGORITHM"

print(code[:4])
print(code[4:])
print(code[::2])
print(code[::-1])

assert code[:4] == "ALGO"
assert code[4:] == "RITHM"
assert code[::2] == "AGRTM"
assert code[::-1] == "MHTIROGLA"
```

Expected output:

```text
ALGO
RITHM
AGRTM
MHTIROGLA
```

An invalid single index raises `IndexError`. A slice safely clips out-of-range bounds.

<!-- TODO(media): Add an indexed-string animation showing positive indices, negative indices, and half-open slices over the same text. Suggested path: ../Assets/Module-3/string-slicing.gif -->

## 7. Core string operations

### 7.1 Concatenation and repetition

- `left + right` creates concatenated text.
- `text * n` repeats text `n` times.
- Adjacent string literals are combined at compile time.

Repeated concatenation inside a large loop may allocate many intermediate strings. Accumulate fragments and call `"".join(fragments)` when constructing text from many pieces.

### 7.2 Membership and search

| Requirement | Operation | Failure or absence result |
| --- | --- | --- |
| Substring exists | `fragment in text` | `False` |
| First position, optional | `text.find(fragment)` | `-1` |
| First position, required | `text.index(fragment)` | `ValueError` |
| Number of non-overlapping matches | `text.count(fragment)` | `0` |
| Prefix or suffix | `startswith()` / `endswith()` | `False` |

Choose `index()` only when absence violates a precondition. Choose `find()` when absence is an expected outcome.

### 7.3 Trimming and affix removal

`strip(chars)` removes any leading or trailing characters belonging to the supplied character set. It does not remove an exact prefix.

```python
raw = "  report.csv  \n"
clean = raw.strip()

versioned = "v2-report.csv"
without_version = versioned.removeprefix("v2-")

print(clean)
print(without_version)

assert clean == "report.csv"
assert without_version == "report.csv"
```

Failure distinction:

```python
assert "archive.tar.gz".rstrip(".gz") == "archive.tar"
assert "archive.tar.gz".removesuffix(".gz") == "archive.tar"
```

Those results happen to match, but `rstrip(".gz")` means “remove trailing periods, g characters, or z characters repeatedly.” For exact affixes, use `removeprefix()` or `removesuffix()`.

### 7.4 Replacement

`text.replace(old, new, count=-1)` returns a new string. Replacements are literal, non-regex transformations.

## 8. Splitting and joining

### 8.1 Tokenization with `split()`

With no separator, `split()` treats runs of whitespace as one delimiter and omits leading or trailing empty fields. With an explicit separator, adjacent delimiters produce empty fields.

```python
line = "  north   east  south "
tokens = line.split()

csv_like = "A,,C"
fields = csv_like.split(",")

print(tokens)
print(fields)

assert tokens == ["north", "east", "south"]
assert fields == ["A", "", "C"]
```

Use a CSV parser for actual CSV data. Quoting, embedded newlines, and delimiter escaping exceed `split(",")` semantics.

### 8.2 Construction with `join()`

The separator owns `join()`:

```python
path_parts = ["courses", "algorithms", "module-3"]
logical_path = "/".join(path_parts)

print(logical_path)
assert logical_path == "courses/algorithms/module-3"
```

Every joined item must be a string. Convert non-string values explicitly so the formatting policy remains visible.

### 8.3 Lines and partitions

- `splitlines()` handles several Unicode line boundaries.
- `partition(separator)` returns `(before, separator, after)` and always returns three strings.
- `rpartition(separator)` searches from the right.

`partition()` is useful when exactly one split point is required and absence must remain observable.

## 9. Case conversion and normalization

### 9.1 Case

`lower()` is appropriate for display transformations. `casefold()` is a stronger Unicode-aware normalization intended for caseless matching [1].

```python
left = "Straße"
right = "STRASSE"

print(left.casefold())
assert left.casefold() == right.casefold()
```

Expected output:

```text
strasse
```

Case normalization can collapse distinct source forms. Preserve original text when auditability or display fidelity matters.

### 9.2 Unicode normalization

Visually similar text can have different code-point sequences. `unicodedata.normalize()` supports normalization forms including NFC and NFD [2].

```python
import unicodedata

composed = "é"
decomposed = "e\u0301"

print(composed == decomposed)
print(unicodedata.normalize("NFC", composed) ==
      unicodedata.normalize("NFC", decomposed))

assert composed != decomposed
assert unicodedata.normalize("NFC", composed) == unicodedata.normalize("NFC", decomposed)
```

Expected output:

```text
False
True
```

Choose a normalization form according to the system contract. Normalization is not transliteration and does not remove all visually confusing distinctions.

<!-- TODO(media): Add an animation showing composed U+00E9 and decomposed U+0065 U+0301 becoming equivalent under NFC. Include code-point labels and alt text. Suggested path: ../Assets/Module-3/unicode-normalization.mp4 -->

## 10. Formatting values

Formatted string literals, or **f-strings**, evaluate expressions and apply optional format specifications.

```python
course = "Algorithms"
completed = 7
total = 12
ratio = completed / total

message = f"{course:<12} {completed:02d}/{total:02d} ({ratio:.1%})"
print(message)

assert message == "Algorithms   07/12 (58.3%)"
```

Expected output:

```text
Algorithms   07/12 (58.3%)
```

Common fields:

| Specification | Meaning | Example |
| --- | --- | --- |
| `:02d` | Decimal integer, width 2, zero-padded | `07` |
| `:.2f` | Fixed point, two digits after decimal | `3.14` |
| `:.1%` | Percentage, one fractional digit | `58.3%` |
| `:<12` | Left-align in width 12 | Text field |
| `:,` | Thousands separator | `1,000,000` |

Formatting produces text; it does not change the numeric value.

## 11. Encoding and decoding

```python
text = "café"
payload = text.encode("utf-8")
restored = payload.decode("utf-8")

print(payload)
print(restored)

assert payload == b"caf\xc3\xa9"
assert restored == text
```

Expected output:

```text
b'caf\xc3\xa9'
café
```

An incorrect codec can raise `UnicodeDecodeError` or silently produce incorrect text. Error policies such as `"ignore"` and `"replace"` are lossy; use them only when data-loss behaviour is explicit.

Keep text as `str` inside application logic. Encode at output boundaries and decode at input boundaries.

## 12. Regular expressions

A regular expression specifies a set of matching strings. Python provides matching through the `re` module [3].

Use direct methods for:

- exact prefixes and suffixes;
- literal replacement;
- one fixed delimiter; and
- simple membership tests.

Use a regex for:

- character classes;
- repeated variable-width structure;
- optional components;
- capture groups; and
- validated full-string patterns.

### 12.1 Validation

`re.fullmatch()` requires the complete input to match:

```python
import re

identifier_pattern = re.compile(r"[A-Z]{2}-\d{4}")

valid = identifier_pattern.fullmatch("CS-2048") is not None
invalid = identifier_pattern.fullmatch("CS-2048-extra") is None

print(valid, invalid)
assert valid and invalid
```

Expected output:

```text
True True
```

Prefer raw strings for regex patterns because both Python literals and regex syntax use backslashes [3].

### 12.2 Extraction

Named groups communicate field meaning:

```python
import re

match = re.fullmatch(
    r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})",
    "2026-08-31",
)

assert match is not None
parts = match.groupdict()
print(parts)
assert parts == {"year": "2026", "month": "08", "day": "31"}
```

A regex can validate shape, but it does not automatically validate domain semantics. The pattern accepts `2026-99-99`; calendar validation requires additional logic or a date parser.

## 13. Designing a normalization pipeline

Order transformations from representation-level requirements to domain rules:

```text
decode bytes
    -> Unicode normalization
    -> boundary whitespace policy
    -> case policy
    -> structural validation
    -> tokenization
    -> domain transformation
```

Each stage should state whether it is lossless. For identifiers, aggressive whitespace or punctuation removal may merge distinct values.

Example:

```python
import unicodedata

raw_tag = "  Déjà   Vu "
normalized = unicodedata.normalize("NFC", raw_tag)
tokens = normalized.casefold().split()
canonical = "-".join(tokens)

print(canonical)
assert canonical == "déjà-vu"
```

## 14. Common failure modes

### 14.1 Confusing bytes and text

`b"data" != "data"`. Decode incoming bytes before text processing.

### 14.2 Assuming visible characters equal `len()`

Code points, combining marks, and grapheme clusters are different units.

### 14.3 Using `strip()` for an exact prefix

`strip(chars)` treats `chars` as a set. Use `removeprefix()` or `removesuffix()`.

### 14.4 Using `split(",")` as a CSV parser

CSV quoting and embedded delimiters require the `csv` module or a tabular-data library.

### 14.5 Normalizing without retaining source data

Lossy case, whitespace, or punctuation rules may prevent later audit or correction.

### 14.6 Regex overreach

Complex nested patterns can become difficult to verify and may have poor backtracking behaviour. Use staged parsing when a grammar has nested or context-dependent structure.

### 14.7 Encoding without an explicit codec

Default encodings vary by interface and environment. State the codec at system boundaries.

## 15. Guided practice

### 15.1 Slice trace

For `text = "COMPUTING"`, determine:

- `text[1:5]`;
- `text[-3:]`;
- `text[::3]`; and
- `text[::-1]`.

**Success criteria:** every answer identifies selected indices as well as the resulting string.

### 15.2 Token policy

Compare `" A  B ".split()` with `" A  B ".split(" ")`. Explain the empty strings in the second result.

### 15.3 Validation boundary

Explain why `re.search(r"\d{4}", "ID-2026-X")` and `re.fullmatch(r"\d{4}", "ID-2026-X")` answer different questions.

## 16. Independent practice

### Exercise 1 — Identifier canonicalization

Convert `"  Data Structures  "` to `"data-structures"`.

**Constraints:** use `strip()`, `casefold()`, `split()`, and `join()`; do not use a regex.

### Exercise 2 — Structured code validation

Accept only codes with three uppercase ASCII letters, a colon, and four digits, such as `"CSE:2048"`.

**Required cases:** accept `"CSE:2048"`; reject `"CsE:2048"`, `"CSE-2048"`, and `"CSE:20480"`.

**Deliverable:** compiled regex and assertions.

### Exercise 3 — Word-frequency input preparation

Given a paragraph:

1. normalize it with NFC;
2. apply caseless normalization;
3. replace `","`, `"."`, `":"`, and `";"` with spaces;
4. split into tokens.

**Deliverable:** token list and a written statement of information lost by the pipeline.

### Exercise 4 — Encoding contract

Encode `"อัลกอริทึม"` as UTF-8 and restore it.

**Success criteria:** round-trip equality holds, payload type is `bytes`, and restored type is `str`.

## 17. Knowledge check

1. Why is `str` immutable?
2. What does the stop index of a slice mean?
3. How do `find()` and `index()` differ on absence?
4. Why is `casefold()` used for caseless matching?
5. What problem does Unicode normalization address?
6. Why is `split(",")` insufficient for general CSV?
7. When should `re.fullmatch()` be preferred over `re.search()`?
8. Why must encoding be explicit at a data boundary?

<details>
<summary>Answer key</summary>

1. Its code-point sequence cannot be modified after construction; transformations return new strings.
2. It is the first excluded position.
3. `find()` returns `-1`; `index()` raises `ValueError`.
4. It applies a stronger Unicode caseless transformation than `lower()`.
5. Equivalent text may use different code-point sequences, such as composed and decomposed forms.
6. CSV supports quoting, escaped delimiters, and embedded newlines.
7. When the complete input must satisfy the pattern.
8. The same bytes can decode differently under different codecs, and invalid sequences require a defined error policy.

</details>

## 18. Module synthesis

Text processing is a representation pipeline, not a collection of unrelated methods:

```text
bytes boundary
    -> decoded Unicode
    -> explicit normalization
    -> validated structure
    -> domain tokens or fields
    -> formatted or encoded output
```

Preserve source data when transformations are lossy. Choose the simplest operation whose contract matches the grammar.

## References

1. Python Software Foundation. “Text Sequence Type — `str`.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str
2. Python Software Foundation. “`unicodedata` — Unicode Database.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/unicodedata.html
3. Python Software Foundation. “`re` — Regular Expression Operations.” *Python 3 Documentation*. Accessed 31 August 2026. https://docs.python.org/3/library/re.html

---

**Previous module:** Module 2 — Branching and Iteration  
**Next module:** Module 4 — Decomposition, Abstraction, and Functions
