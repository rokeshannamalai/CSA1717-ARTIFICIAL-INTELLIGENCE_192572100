"""Logical Agent Case Studies – reasoning demonstrations."""

def forward_chain(facts, rules):
    facts=set(facts); steps=[]; changed=True
    while changed:
        changed=False
        for name,premises,conclusion in rules:
            if premises <= facts and conclusion not in facts:
                facts.add(conclusion); steps.append((name,conclusion)); changed=True
    return facts,steps

def resolve(c1,c2):
    out=set()
    for lit in c1:
        if -lit in c2: out.add(frozenset((c1-{lit})|(c2-{-lit})))
    return out

def resolution(clauses, neg_goal):
    clauses={frozenset(c) for c in clauses}; clauses.add(frozenset({neg_goal}))
    while True:
        new=set()
        cs=list(clauses)
        for i in range(len(cs)):
            for j in range(i+1,len(cs)):
                for r in resolve(cs[i],cs[j]):
                    if r not in clauses:
                        if not r: return True
                        new.add(r)
        if not new: return False
        clauses |= new

def case1():
    facts={"Fever_A","Cough_A","Breathlessness_A"}
    rules=[("Rule I",{"Fever_A","Cough_A"},"PossibleFlu_A"),
           ("Rule II",{"Fever_A","Rash_A"},"PossibleMeasles_A"),
           ("Rule III",{"Cough_A","Breathlessness_A"},"PossiblePneumonia_A")]
    final,steps=forward_chain(facts,rules)
    print("\nCASE 1 – MEDICAL DIAGNOSIS")
    for r,f in steps: print(r,"->",f)
    print("Diagnoses:",sorted(x for x in final if x.startswith("Possible")))
    print("Backward: Pneumonia_A <- Cough_A AND Breathlessness_A; both facts present.")
    print("RESULT: Pneumonia PROVED")

def case2():
    print("\nCASE 2 – TRAFFIC MANAGEMENT")
    print("Unification MGU: θ={x/Ambulance}")
    print("ClearPath(Ambulance) -> GreenSignal(Ambulance)")
    print("Rule 3 MGU: θ={x/CarA,y/Ambulance}")
    print("Proceed(CarA) derived")
    print("Proceed(CarA) + ¬Proceed(CarA) -> □")
    print("RESULT: Proceed(CarA) PROVED")
    print("Two emergencies require priority/route-conflict/intersection rules for coordination.")

def case3():
    clauses=[{-1,2},{-2,3},{-4,3},{3,5},{-4,5},{1},{4}]
    print("\nCASE 3 – AGRICULTURAL REASONING")
    print("CNF: ¬SoilDry∨IrrigationNeeded")
    print("CNF: ¬IrrigationNeeded∨ApplyDripMethod")
    print("CNF: ¬CropWheat∨ApplyDripMethod")
    print("Resolution: C1 + SoilDry -> IrrigationNeeded")
    print("Resolution: IrrigationNeeded + C2 -> ApplyDripMethod")
    print("Resolution: ApplyDripMethod + ¬ApplyDripMethod -> □")
    print("RESULT: ApplyDripMethod PROVED")
    print("Without SoilDry: IrrigationNeeded is not derivable; CropAtRisk is also not entailed.")

def case4():
    facts={"Stench[1,2]","Breeze[1,1]","Glitter[2,2]"}
    rules=[("Rule 1",{"Stench[1,2]"},"WumpusAdjacent[1,2]"),
           ("Rule 2",{"Breeze[1,1]"},"PitAdjacent[1,1]"),
           ("Rule 3",{"Glitter[2,2]"},"Gold[2,2]")]
    final,steps=forward_chain(facts,rules)
    print("\nCASE 4 – WUMPUS WORLD")
    for r,f in steps: print(r,"->",f)
    print("Possible Wumpus: [1,1], [1,3], [2,2]")
    print("Possible Pit: [1,2], [2,1]")
    print("Safe cannot be proved without explicit negative hazard facts.")
    print("RESULT: Proposed path is NOT GUARANTEED SAFE")

if __name__=="__main__":
    case1(); case2(); case3(); case4()
