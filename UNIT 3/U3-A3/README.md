# Resolution Algorithm Implementation

## Project Overview
This project demonstrates propositional-logic theorem proving using the **Resolution Algorithm**.

The project contains five problems:
1. Rain and Wet Ground
2. Student Assignment Submission
3. Library Membership
4. Placement Eligibility
5. Access Control System

For each problem, the knowledge base is converted into CNF, the goal is negated, and resolution is applied until the **Empty Clause (□)** is obtained.

## Folder Structure

```text
Resolution_Algorithm_Project/
├── Problem.pdf
├── Solution.pdf
├── Python_Code.py
├── Output.png
├── Report.pdf
└── README.md
```

## Requirements
- Python 3.x
- No external Python packages are required to run `Python_Code.py`.

## How to Run

Open a terminal in this folder and run:

```bash
python Python_Code.py
```

The program prints:
- Initial CNF clauses
- Negated goal
- Resolution steps
- Empty Clause when the goal is proved
- Final summary

## Resolution Principle

For two clauses containing complementary literals:

```text
(A ∨ B) and (¬B ∨ C)
```

resolution produces:

```text
A ∨ C
```

A goal is proved by contradiction when:

```text
Knowledge Base + ¬Goal ⟹ □
```

where `□` is the Empty Clause.

## Expected Result

All five goals are proved:

| Question | Result |
|---|---|
| Rain and Wet Ground | PROVED |
| Student Assignment Submission | PROVED |
| Library Membership | PROVED |
| Placement Eligibility | PROVED |
| Access Control System | PROVED |

## Files

- `Problem.pdf` – Original problem statements.
- `Solution.pdf` – Step-by-step manual solutions.
- `Python_Code.py` – Resolution Algorithm implementation.
- `Output.png` – Captured program output.
- `Report.pdf` – Formal project report.
- `README.md` – Project documentation.

## Author
Resolution Algorithm Academic Mini Project
