# Integrated Experiments
# Experiment 1: Decision Tree Classification
# Experiment 2: Reinforcement Learning - Q-Learning

import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


def experiment_1():
    print("=" * 70)
    print("EXPERIMENT 1: DECISION TREE CLASSIFICATION")
    print("=" * 70)

    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target, name="target")

    df = X.copy()
    df["target"] = y

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    model = DecisionTreeClassifier(
        criterion="gini", random_state=42
    )
    model.fit(X_train, y_train)

    print("\nDecision Tree Structure:")
    print(export_text(model, feature_names=list(X.columns)))

    root_index = model.tree_.feature[0]
    print("\nRoot node feature:", X.columns[root_index])
    print("Root threshold:", round(model.tree_.threshold[0], 4))

    y_pred = model.predict(X_test)

    print("\nAccuracy:", round(accuracy_score(y_test, y_pred), 4))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(classification_report(
        y_test, y_pred, target_names=iris.target_names
    ))

    mis = X_test[y_test.values != y_pred].copy()
    mis["Actual"] = y_test[y_test.values != y_pred].map(
        dict(enumerate(iris.target_names))
    ).values
    mis["Predicted"] = pd.Series(y_pred[y_test.values != y_pred],
                                 index=mis.index).map(
        dict(enumerate(iris.target_names))
    )

    print("\nMisclassified instances:")
    if mis.empty:
        print("No misclassified instances in this test split.")
    else:
        print(mis)

    plt.figure(figsize=(14, 8))
    plot_tree(
        model,
        feature_names=iris.feature_names,
        class_names=iris.target_names,
        filled=True,
        rounded=True
    )
    plt.title("Experiment 1 - Decision Tree on Iris Dataset")
    plt.tight_layout()
    plt.savefig("decision_tree.png", dpi=180)
    plt.show()

    return model, accuracy_score(y_test, y_pred), confusion_matrix(y_test, y_pred), mis


def experiment_2():
    print("\n" + "=" * 70)
    print("EXPERIMENT 2: Q-LEARNING - 4x4 GRID WORLD")
    print("=" * 70)

    GRID = 4
    START, GOAL = 0, 15
    OBSTACLES = {5, 10}

    # 0=Up, 1=Down, 2=Left, 3=Right
    action_names = ["U", "D", "L", "R"]

    alpha = 0.1
    gamma = 0.9
    epsilon = 1.0
    epsilon_min = 0.05
    epsilon_decay = 0.97

    episodes = 100
    max_steps = 100

    Q = np.zeros((16, 4))
    episode_rewards = []
    q_history = {}

    def step(state, action):
        row, col = divmod(state, GRID)
        nr, nc = row, col

        if action == 0:
            nr -= 1
        elif action == 1:
            nr += 1
        elif action == 2:
            nc -= 1
        else:
            nc += 1

        if nr < 0 or nr >= GRID or nc < 0 or nc >= GRID:
            return state, -1, False

        next_state = nr * GRID + nc

        if next_state == GOAL:
            return next_state, 10, True

        if next_state in OBSTACLES:
            return state, -5, False

        return next_state, -1, False

    for ep in range(1, episodes + 1):
        state = START
        total_reward = 0

        for _ in range(max_steps):
            if random.random() < epsilon:
                action = random.randint(0, 3)
            else:
                action = int(np.argmax(Q[state]))

            next_state, reward, done = step(state, action)

            Q[state, action] += alpha * (
                reward + gamma * np.max(Q[next_state]) - Q[state, action]
            )

            state = next_state
            total_reward += reward

            if done:
                break

        episode_rewards.append(total_reward)

        if ep in [1, 50, 100]:
            q_history[ep] = {
                0: Q[0].copy(),
                6: Q[6].copy()
            }

        epsilon = max(epsilon_min, epsilon * epsilon_decay)

    print("\nHyperparameters:")
    print("alpha =", alpha)
    print("gamma =", gamma)
    print("initial epsilon = 1.0")
    print("episodes =", episodes)

    print("\nQ-values for representative states:")
    for ep in [1, 50, 100]:
        print(f"\nEpisode {ep}")
        print("State 0 [U,D,L,R]:", np.round(q_history[ep][0], 4))
        print("State 6 [U,D,L,R]:", np.round(q_history[ep][6], 4))

    print("\nFinal Q-table:")
    for s in range(16):
        print(f"State {s:2d}: {np.round(Q[s], 4)}")

    policy = np.argmax(Q, axis=1)

    print("\nFinal Learned Policy:")
    for r in range(GRID):
        row = []
        for c in range(GRID):
            s = r * GRID + c
            if s == START:
                row.append("S")
            elif s == GOAL:
                row.append("G")
            elif s in OBSTACLES:
                row.append("X")
            else:
                row.append(action_names[policy[s]])
        print(row)

    plt.figure(figsize=(10, 5))
    plt.plot(range(1, episodes + 1), episode_rewards)
    plt.xlabel("Episode")
    plt.ylabel("Cumulative Reward")
    plt.title("Experiment 2 - Q-Learning Cumulative Reward")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("q_learning_reward.png", dpi=180)
    plt.show()

    # Combined output image
    from PIL import Image
    tree_img = Image.open("decision_tree.png").convert("RGB")
    reward_img = Image.open("q_learning_reward.png").convert("RGB")

    canvas = Image.new("RGB", (tree_img.width + reward_img.width, max(tree_img.height, reward_img.height)), "white")
    canvas.paste(tree_img, (0, 0))
    canvas.paste(reward_img, (tree_img.width, 0))
    canvas.save("Output.png")

    return Q, episode_rewards, policy


if __name__ == "__main__":
    random.seed(42)
    np.random.seed(42)
    experiment_1()
    experiment_2()
    print("\nAll experiments completed successfully.")
