# Logical Agent Case Studies

## Folder Structure
```text
Logical_Agent_Case_Studies_Project/
├── Problem.pdf
├── Solution.pdf
├── Python_Code.py
├── Output.png
├── Report.pdf
└── README.md
```

## Topics
- Propositional Logic
- First-Order Logic
- Forward Chaining
- Backward Chaining
- Modus Ponens
- Unification / MGU
- CNF Conversion
- Resolution Refutation
- Wumpus World

## Run
```bash
python Python_Code.py
```

The program demonstrates the requested reasoning for all four case studies.

## Notes
Case Study 2: Proceed(CarA) follows because ClearPath(Ambulance) gives GreenSignal(Ambulance), which combines with Vehicle(CarA) and Behind(CarA,Ambulance).

Case Study 3: Removing SoilDry does not make ¬ApplyDripMethod true. Therefore CropAtRisk cannot be concluded under ordinary open-world logic.

Case Study 4: The supplied rules identify adjacent hazard possibilities but do not identify exact hazard cells. Since explicit negative Wumpus/Pit facts are absent, Safe cells cannot be proved.
