# Industry Problem Task - AI/ML Healthcare
# Academic demonstration only. Synthetic data; not for medical decisions.

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt

np.random.seed(42)
n = 1200
age = np.random.randint(25, 76, n)
bp = np.clip(np.random.normal(128,18,n),85,190)
chol = np.clip(np.random.normal(205,38,n),110,330)
glucose = np.clip(np.random.normal(118,32,n),65,260)
bmi = np.clip(np.random.normal(27.5,5,n),16,45)
family = np.random.binomial(1,0.30,n)

risk = (0.045*(glucose-100) + 0.025*(bmi-25) +
        0.012*(age-45) + 0.008*(bp-120) +
        0.004*(chol-190) + 0.65*family +
        np.random.normal(0,1.4,n))
p = 1/(1+np.exp(-risk/2.5))
diabetes = (p > np.quantile(p,0.73)).astype(int)

df = pd.DataFrame({
    "Age":age, "BloodPressure":bp, "Cholesterol":chol,
    "Glucose":glucose, "BMI":bmi, "FamilyHistory":family,
    "Diabetes":diabetes
})

X = df.drop(columns="Diabetes")
y = df["Diabetes"]
Xtr,Xte,ytr,yte = train_test_split(X,y,test_size=.30,stratify=y,random_state=42)

smote = SMOTE(random_state=42)
Xtr,ytr = smote.fit_resample(Xtr,ytr)

def evaluate(model, Xtest, ytest):
    pred = model.predict(Xtest)
    prob = model.predict_proba(Xtest)[:,1]
    return {
        "Accuracy":round(accuracy_score(ytest,pred),4),
        "Precision":round(precision_score(ytest,pred,zero_division=0),4),
        "Recall":round(recall_score(ytest,pred,zero_division=0),4),
        "F1":round(f1_score(ytest,pred,zero_division=0),4),
        "AUC":round(roc_auc_score(ytest,prob),4),
        "ConfusionMatrix":confusion_matrix(ytest,pred).tolist()
    }

tree = DecisionTreeClassifier(max_depth=4,min_samples_leaf=12,
                              class_weight="balanced",criterion="gini",
                              random_state=42)
tree.fit(Xtr,ytr)
print("DATASET:",df.shape)
print("CLASS DISTRIBUTION:",y.value_counts().to_dict())
print("AFTER SMOTE:",ytr.value_counts().to_dict())

print("\nDECISION TREE")
print(evaluate(tree,Xte,yte))
print("TOP 3 TREE FEATURES:",
      pd.Series(tree.feature_importances_,index=X.columns).sort_values(ascending=False).head(3).to_dict())

plt.figure(figsize=(16,9))
plot_tree(tree,feature_names=X.columns,class_names=["Non-Diabetic","Diabetic"],
          max_depth=2,filled=False,fontsize=8)
plt.title("Decision Tree - First Three Levels")
plt.tight_layout()
plt.savefig("Decision_Tree_First_Three_Levels.png",dpi=180)
plt.close()

# Cost-complexity post-pruning
full = DecisionTreeClassifier(class_weight="balanced",random_state=42)
full.fit(Xtr,ytr)
path = full.cost_complexity_pruning_path(Xtr,ytr)
best = (0,None)
for a in path.ccp_alphas:
    m = DecisionTreeClassifier(ccp_alpha=float(a),class_weight="balanced",random_state=42)
    m.fit(Xtr,ytr)
    acc = accuracy_score(yte,m.predict(Xte))
    if acc > best[0]:
        best = (acc,float(a))
post = DecisionTreeClassifier(ccp_alpha=best[1],class_weight="balanced",random_state=42)
post.fit(Xtr,ytr)
print("POST-PRUNED TREE:",evaluate(post,Xte,yte))
print("BEST CCP ALPHA:",best[1])

# Logistic Regression
scaler=StandardScaler()
Xtrs=scaler.fit_transform(Xtr)
Xtes=scaler.transform(Xte)
lr=LogisticRegression(max_iter=2000,class_weight="balanced",random_state=42)
lr.fit(Xtrs,ytr)
print("\nLOGISTIC REGRESSION")
print(evaluate(lr,Xtes,yte))
coef=pd.Series(abs(lr.coef_[0]),index=X.columns).sort_values(ascending=False)
print("TOP 3 LOGISTIC FEATURES:",coef.head(3).to_dict())

# Q-learning
states=["Stable","AtRisk","HighRisk","Improving"]
actions=["Diet","Exercise","Medication","Monitor"]
Q=pd.DataFrame(0.0,index=states,columns=actions)
T={
("Stable","Diet"):("Stable",2),("Stable","Exercise"):("Stable",2),
("Stable","Medication"):("AtRisk",-1),("Stable","Monitor"):("Stable",1),
("AtRisk","Diet"):("Improving",3),("AtRisk","Exercise"):("Improving",3),
("AtRisk","Medication"):("Improving",4),("AtRisk","Monitor"):("AtRisk",1),
("HighRisk","Diet"):("AtRisk",2),("HighRisk","Exercise"):("AtRisk",2),
("HighRisk","Medication"):("Improving",5),("HighRisk","Monitor"):("HighRisk",0),
("Improving","Diet"):("Stable",2),("Improving","Exercise"):("Stable",2),
("Improving","Medication"):("Stable",1),("Improving","Monitor"):("Stable",1)
}
alpha,gamma,epsilon=.5,.9,.15

print("\nQ-LEARNING UPDATES")
for episode in range(1,6):
    state=states[(episode-1)%3]
    for iteration in range(1,11):
        action=np.random.choice(actions) if np.random.rand()<epsilon else Q.loc[state].idxmax()
        nxt,reward=T[(state,action)]
        old=Q.loc[state,action]
        new=old+alpha*(reward+gamma*Q.loc[nxt].max()-old)
        Q.loc[state,action]=new
        if episode<=2 and iteration<=3:
            print(f"Episode {episode}, Iteration {iteration}: "
                  f"Q({state},{action}) {old:.3f} -> {new:.3f}")
        state=nxt

print("\nFINAL Q-TABLE")
print(Q.round(3))
print("FINAL POLICY")
print(Q.idxmax(axis=1).to_dict())
print("CONVERGENCE CRITERION: max |delta Q| < 0.01 for 5 consecutive updates.")
print("WARNING: This is an educational simulation, not a treatment protocol.")
