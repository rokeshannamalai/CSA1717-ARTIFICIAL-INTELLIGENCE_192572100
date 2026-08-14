"""
Resolution Algorithm Implementation
Five propositional-logic proof problems.

The program uses proof by contradiction:
1. Add the knowledge-base clauses.
2. Add the negation of the goal.
3. Repeatedly resolve pairs of clauses.
4. If the empty clause is generated, the goal is proved.
"""

def resolve(ci, cj):
    """Return all resolvents of two clauses."""
    resolvents = set()
    for literal in ci:
        complement = -literal
        if complement in cj:
            new_clause = (ci - {literal}) | (cj - {complement})
            resolvents.add(frozenset(new_clause))
    return resolvents


def clause_text(clause, names):
    if not clause:
        return "□"
    parts = []
    for lit in sorted(clause, key=lambda x: abs(x)):
        parts.append(names[abs(lit)] if lit > 0 else "¬" + names[abs(lit)])
    return " ∨ ".join(parts)


def resolution_prove(clauses, goal, names, verbose=True):
    """Prove goal by adding ¬goal and searching for the empty clause."""
    clauses = {frozenset(c) for c in clauses}
    clauses.add(frozenset({-goal}))

    generated = set()
    steps = []

    while True:
        current = list(clauses)

        for i in range(len(current)):
            for j in range(i + 1, len(current)):
                for resolvent in resolve(current[i], current[j]):
                    if resolvent not in clauses:
                        steps.append((current[i], current[j], resolvent))
                        if not resolvent:
                            if verbose:
                                print("  Resolution steps:")
                                for k, (a, b, r) in enumerate(steps, 1):
                                    print(f"    {k}. ({clause_text(a, names)}) + "
                                          f"({clause_text(b, names)}) -> "
                                          f"{clause_text(r, names)}")
                            return True, steps
                        generated.add(resolvent)

        if not generated:
            if verbose:
                print("  No new clauses. Goal not proved.")
            return False, steps

        clauses |= generated
        generated = set()


def run_problem(number, title, clauses, goal, names):
    print("=" * 70)
    print(f"QUESTION {number}: {title}")
    print("=" * 70)
    print("Initial CNF clauses:")
    for i, c in enumerate(clauses, 1):
        print(f"  C{i}: {clause_text(frozenset(c), names)}")
    print(f"Negated goal: ¬{names[abs(goal)]}")

    proved, steps = resolution_prove(clauses, goal, names)

    if proved:
        print(f"RESULT: Goal {names[abs(goal)]} is PROVED.")
        print("Empty Clause (□) derived.")
    else:
        print(f"RESULT: Goal {names[abs(goal)]} is NOT PROVED.")
    print()
    return proved


def main():
    # Positive integer = literal, negative integer = negated literal.
    results = []

    results.append(run_problem(
        1, "Rain and Wet Ground",
        [{-1, 2}, {1}], 2,
        {1: "R", 2: "W"}
    ))

    results.append(run_problem(
        2, "Student Assignment Submission",
        [{-1, 2}, {1}], 2,
        {1: "S", 2: "M"}
    ))

    results.append(run_problem(
        3, "Library Membership",
        [{-1, 2}, {1}], 2,
        {1: "L", 2: "B"}
    ))

    results.append(run_problem(
        4, "Placement Eligibility",
        [{-1, 2}, {1}], 2,
        {1: "A", 2: "E"}
    ))

    results.append(run_problem(
        5, "Access Control System",
        [{-1, 2}, {-2, 3}, {1}], 3,
        {1: "P", 2: "A", 3: "G"}
    ))

    print("=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    for i, result in enumerate(results, 1):
        print(f"Question {i}: {'PROVED ✓' if result else 'NOT PROVED ✗'}")


if __name__ == "__main__":
    main()
