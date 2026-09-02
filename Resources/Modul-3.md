# Module 3: Basic String Manipulation

**Course:** Algorithms and Programming

**Program:** TSI International Undergraduate Program

**Programming language:** Python 3.10 or later

**Prerequisites:** Modules 1 and 2

**Estimated study time:** 3 to 4 hours

## 1. Module scope

A **string** is Python's standard type for text. Industrial Systems programs use strings for product codes, operator names, machine labels, categories, and records read from files or keyboards.

This module covers direct operations that beginners can combine with variables, lists, branches, and loops. Unicode internals, encoded bytes, normalization standards, and regular expressions appear only as an unassessed technical preview.

<!-- TODO(media): Add a visual walkthrough that transforms "  pump | 024 | line a  " into fields, validates them, and constructs "TSI-PUMP-024". Suggested path: ../Assets/Module-3/product-code-pipeline.mp4 -->

## 2. Learning outcomes

After completing this module, a student should be able to:

1. create and display string values;
2. combine and repeat strings;
3. calculate string length and access characters with indexing;
4. extract substrings with slicing;
5. explain string immutability;
6. test whether text contains a substring;
7. apply common cleaning methods;
8. split structured text into fields and join fields into output;
9. validate basic digit-only input;
10. normalize a simple product record into a standard code.

## 3. Prerequisite check

Before continuing, confirm that you can:

- assign values to variables;
- use `print()` and f-strings;
- compare values in an `if` statement;
- process list items with a `for` loop.

No custom function definition is required in this module. Functions are introduced in Module 4.

### 3.1 Suggested study schedule

| Activity | Time |
| --- | ---: |
| String creation, length, indexing, and slicing | 55 minutes |
| Immutability and common methods | 45 minutes |
| Splitting, joining, validation, and formatting | 45 minutes |
| Product Code Cleaner study case | 35 minutes |
| Practice and knowledge check | 30 minutes |
| **Total** | **210 minutes** |

## 4. Creating string values

Python represents text with `str` objects. String literals may use single or double quotation marks [1].

```python
product_name = "Hydraulic Pump"
machine_code = 'MC-04'

print(product_name)
print(machine_code)
```

Digits inside quotation marks are still text:

```python
numeric_code = "024"
quantity = 24

assert type(numeric_code).__name__ == "str"
assert type(quantity).__name__ == "int"
```

Choose quotation marks that keep the text readable:

```python
message = "Operator's report"
print(message)
```

## 5. String input and output

`input()` always returns a string:

```python
product = input("Product name: ")
print(f"Recorded product: {product}")
```

When numeric calculation is required, validate or convert the text before using it as a number.

For fixed examples in this module, variables simulate previously entered input:

```python
raw_product = "  Hydraulic Pump  "
print(raw_product)
```

## 6. Concatenation and repetition

The `+` operator concatenates strings:

```python
department = "TSI"
separator = "-"
item_number = "024"

code = department + separator + item_number
assert code == "TSI-024"
```

Both operands must be strings:

```text
item_number = 24
code = "TSI-" + item_number
```

Convert the number or use an f-string:

```python
item_number = 24

code_a = "TSI-" + str(item_number)
code_b = f"TSI-{item_number}"

assert code_a == "TSI-24"
assert code_b == "TSI-24"
```

The `*` operator repeats a string:

```python
line = "=" * 20
print(line)
```

Output:

```text
====================
```

## 7. String length

`len(text)` returns the number of code points in a string for the examples used here [1].

```python
machine_code = "MC-04"

code_length = len(machine_code)
assert code_length == 5
```

Spaces count as characters:

```python
label = "Line A"
assert len(label) == 6
```

An empty string has length zero:

```python
empty_text = ""
assert len(empty_text) == 0
```

## 8. Indexing characters

String indexing starts at zero [1]:

```python
code = "PUMP"

assert code[0] == "P"
assert code[1] == "U"
assert code[3] == "P"
```

Negative indices count from the end:

```python
code = "PUMP"

assert code[-1] == "P"
assert code[-2] == "M"
```

Index diagram:

```text
Character:  P   U   M   P
Index:      0   1   2   3
Negative:  -4  -3  -2  -1
```

An index outside the valid range raises `IndexError`:

```text
code = "PUMP"
print(code[4])
```

Check the length before using a position that may not exist.

## 9. Slicing substrings

A slice uses `text[start:stop]`. The start position is included, and the stop position is excluded [1].

```python
batch_code = "TSI-2026-024"

program = batch_code[0:3]
year = batch_code[4:8]
number = batch_code[9:12]

assert program == "TSI"
assert year == "2026"
assert number == "024"
```

Useful omitted boundaries:

```python
batch_code = "TSI-2026-024"

assert batch_code[:3] == "TSI"
assert batch_code[4:] == "2026-024"
assert batch_code[-3:] == "024"
```

<!-- TODO(media): Add an index-strip animation for "TSI-2026-024" showing zero-based indices and the half-open slices [0:3], [4:8], and [-3:]. Suggested path: ../Assets/Module-3/string-indexing.gif -->

## 10. String immutability

Strings are immutable. Their existing characters cannot be replaced by item assignment [2].

Invalid:

```text
code = "tsi-024"
code[0] = "T"
```

Create a new string instead:

```python
code = "tsi-024"
corrected_code = "T" + code[1:]

assert code == "tsi-024"
assert corrected_code == "Tsi-024"
```

Most string methods also return a new string:

```python
raw_code = "  tsi-024  "
clean_code = raw_code.strip().upper()

assert raw_code == "  tsi-024  "
assert clean_code == "TSI-024"
```

Store the returned value when the program needs the change.

## 11. Membership tests

The `in` operator checks whether one string occurs inside another:

```python
machine_code = "LINE-A-CUTTER"

assert "CUTTER" in machine_code
assert "WELDER" not in machine_code
```

Membership is case-sensitive:

```python
message = "Machine Active"

assert "Active" in message
assert "active" not in message
```

Normalize case first when the comparison should be case-insensitive:

```python
message = "Machine Active"
normalized_message = message.lower()

assert "active" in normalized_message
```

## 12. Common cleaning methods

String methods return new strings [2].

| Method | Purpose | Example result |
| --- | --- | --- |
| `strip()` | Remove surrounding whitespace | `"  pump ".strip()` gives `"pump"` |
| `lower()` | Convert cased characters to lowercase | `"Pump".lower()` gives `"pump"` |
| `upper()` | Convert cased characters to uppercase | `"tsi".upper()` gives `"TSI"` |
| `title()` | Apply title-style casing | `"line operator".title()` gives `"Line Operator"` |
| `replace(a, b)` | Replace occurrences of `a` with `b` | `"A B".replace(" ", "-")` gives `"A-B"` |

```python
raw_label = "  hydraulic pump  "

clean_label = raw_label.strip()
upper_label = clean_label.upper()
code_label = upper_label.replace(" ", "-")

assert clean_label == "hydraulic pump"
assert upper_label == "HYDRAULIC PUMP"
assert code_label == "HYDRAULIC-PUMP"
```

Method calls may be chained:

```python
raw_label = "  hydraulic pump  "
code_label = raw_label.strip().upper().replace(" ", "-")

assert code_label == "HYDRAULIC-PUMP"
```

For text containing repeated internal spaces, use `split()` and `join()` as shown next.

## 13. Splitting and joining

`split(separator)` divides one string into a list of fields [2].

```python
record = "PUMP|024|LINE A"
fields = record.split("|")

assert fields == ["PUMP", "024", "LINE A"]
assert fields[0] == "PUMP"
```

When no separator is supplied, `split()` divides on whitespace and combines repeated whitespace:

```python
raw_name = "  ana   putri  "
words = raw_name.split()

assert words == ["ana", "putri"]
```

`separator.join(items)` combines string items:

```python
words = ["ana", "putri"]
clean_name = " ".join(words).title()

assert clean_name == "Ana Putri"
```

A common whitespace-normalization pattern is:

```python
raw_text = "  bearing   inspection   report "
clean_text = " ".join(raw_text.split())

assert clean_text == "bearing inspection report"
```

## 14. Basic validation

`isdigit()` returns `True` when a non-empty string contains only digit characters as defined by Python [2].

```python
item_number = "024"
invalid_number = "02A"
empty_number = ""

assert item_number.isdigit() is True
assert invalid_number.isdigit() is False
assert empty_number.isdigit() is False
```

Combine validation with a branch:

```python
quantity_text = "125"

if quantity_text.isdigit():
    quantity = int(quantity_text)
    message = f"Accepted quantity: {quantity}"
else:
    message = "Invalid quantity"

assert message == "Accepted quantity: 125"
```

A leading minus sign is not a digit:

```python
assert "-5".isdigit() is False
```

Use a different validation rule when signed integers are required.

## 15. Formatting string output

An f-string inserts expressions into a string [3]:

```python
product = "Pump"
quantity = 24
defect_rate = 0.0375

report = f"{product}: {quantity} units, defects {defect_rate:.1%}"
assert report == "Pump: 24 units, defects 3.8%"
```

Common format specifications:

| Format | Meaning | Example |
| --- | --- | --- |
| `{value:.2f}` | Two digits after the decimal point | `12.50` |
| `{value:,}` | Thousands separator | `25,000` |
| `{value:.1%}` | Percentage with one decimal place | `3.8%` |
| `{value:03d}` | Integer padded to width three | `024` |

```python
item_number = 24
formatted_number = f"{item_number:03d}"

assert formatted_number == "024"
```

## 16. Study case: Product Code Cleaner

### 16.1 Problem

A raw record contains:

```text
product name | item number | production line
```

The standard product code must follow:

```text
TSI-PRODUCT-NNN
```

Requirements:

- exactly three fields;
- surrounding whitespace removed;
- product name converted to uppercase;
- spaces inside the product name converted to hyphens;
- item number contains digits only;
- item number padded to three positions;
- line name converted to title case.

### 16.2 Implementation

```python
raw_record = "  hydraulic   pump | 24 | line a  "
fields = raw_record.split("|")

if len(fields) == 3:
    product_name = "-".join(fields[0].strip().upper().split())
    item_text = fields[1].strip()
    line_name = " ".join(fields[2].strip().split()).title()

    if product_name != "" and item_text.isdigit() and line_name != "":
        item_number = int(item_text)
        product_code = f"TSI-{product_name}-{item_number:03d}"
        result = f"{product_code} | {line_name}"
    else:
        result = "INVALID RECORD"
else:
    result = "INVALID RECORD"

print(result)
assert result == "TSI-HYDRAULIC-PUMP-024 | Line A"
```

Output:

```text
TSI-HYDRAULIC-PUMP-024 | Line A
```

### 16.3 Processing several records

```python
raw_records = [
    "pump|7|line a",
    "steel bracket|42|line b",
    "invalid|A3|line c",
]
valid_codes = []

for raw_record in raw_records:
    fields = raw_record.split("|")

    if len(fields) != 3:
        continue

    product_name = "-".join(fields[0].strip().upper().split())
    item_text = fields[1].strip()

    if product_name == "" or not item_text.isdigit():
        continue

    item_number = int(item_text)
    valid_codes.append(f"TSI-{product_name}-{item_number:03d}")

assert valid_codes == ["TSI-PUMP-007", "TSI-STEEL-BRACKET-042"]
```

This version applies Module 2 control flow to string records.

<!-- TODO(media): Add a pipeline diagram showing split, field-count check, per-field cleanup, digit validation, conversion, and formatted output. Suggested path: ../Assets/Module-3/string-validation-pipeline.png -->

## 17. Optional technical preview

This section is not assessed.

Python strings represent Unicode text. Visually similar text may use different code-point sequences. External files and networks store encoded bytes rather than abstract text. Regular expressions describe more complex text patterns.

These topics matter in production systems, but they introduce additional concepts that are not required for the current exercises. They may be revisited after functions, exceptions, and testing.

## 18. Common beginner errors

### 18.1 Missing quotation marks

```text
product = pump
```

Use `"pump"` for literal text.

### 18.2 Combining text and numbers directly

```text
code = "TSI-" + 24
```

Use `str(24)` or an f-string.

### 18.3 Using an invalid index

Check `len(text)` when the string may be shorter than expected.

### 18.4 Expecting a method to modify the original string

```text
name = " pump "
name.strip()
```

Store the returned value:

```text
name = name.strip()
```

### 18.5 Using `split()` without validating field count

A missing or additional separator changes the number of fields. Check `len(fields)` before indexing.

### 18.6 Converting before validation

`int("A3")` raises `ValueError`. For the unsigned item-number format in this module, check `isdigit()` first.

## 19. Guided practice

Given:

```python
raw_code = "  tsi pump 15  "
```

Complete the transformations:

```text
clean_code = ______________________________________
standard_code = ___________________________________
```

Expected value:

```text
TSI-PUMP-15
```

Then split this record and extract the second field:

```text
record = "VALVE|031|LINE B"
fields = ___________________________________________
item_number = ______________________________________
```

Expected `item_number`:

```text
031
```

## 20. Independent practice

### Task 1: Operator label

Convert `"  siti   rahma  "` to `"Siti Rahma"` using `split()`, `join()`, and `title()`.

### Task 2: Batch code inspection

For `"TSI-2026-075"`, extract the program, year, and number using slices.

### Task 3: Location normalization

Convert inconsistent location input such as `" line   a "` to `"LINE-A"`.

### Task 4: Record validation

Validate `"PUMP|024"`. The record is valid only when it contains two non-empty fields and the second field contains digits only.

## 21. Knowledge check

1. What type represents text in Python?
2. What is the first valid string index?
3. Does the stop position of a slice belong to the result?
4. Can an existing string character be replaced by index assignment?
5. What does `strip()` remove in the default form?
6. What does `split("|")` return?
7. Why should field count be checked before indexing split fields?
8. What does `isdigit()` return for an empty string?
9. Which f-string specification formats `7` as `007`?

<details>
<summary>Answer guide</summary>

1. `str`.
2. `0`.
3. No. The stop position is excluded.
4. No. Strings are immutable.
5. Surrounding whitespace.
6. A list of substrings separated at each pipe.
7. Missing or extra separators change the list length and may make the expected index invalid.
8. `False`.
9. `{value:03d}`.

</details>

## 22. Module synthesis

A basic string-processing pipeline is:

```text
raw text
    -> split into fields
    -> validate structure
    -> clean each field
    -> validate content
    -> format result
```

Keep the raw input separate from the cleaned result. Validate structure before indexing, and validate numeric text before conversion.

## References

1. Python Software Foundation. "An Informal Introduction to Python: Text." *Python 3.14.7 Documentation*. Accessed 2 September 2026. https://docs.python.org/3/tutorial/introduction.html#text
2. Python Software Foundation. "Text Sequence Type: `str`." *Python 3.14.7 Documentation*. Accessed 2 September 2026. https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str
3. Python Software Foundation. "Formatted String Literals." *Python 3.14.7 Documentation*. Accessed 2 September 2026. https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals

---

**Previous module:** Module 2: Basic Branching and Iteration

**Next module:** Module 4: Decomposition, Abstraction, and Functions
