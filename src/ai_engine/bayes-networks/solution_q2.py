import pandas as pd
import numpy as np
from collections import defaultdict
from typing import Dict, Tuple
from sklearn.model_selection import train_test_split

def print_cpt_table(cpt: Dict, title: str, feature_name: str):
    print(f"\n{title}")
    print(f"{feature_name:<20} {'Y=0 (No Diabetes)':<25} {'Y=1 (Diabetes)':<25}")

    feature_values = sorted(set(k[0] for k in cpt.keys()))
    
    for fv in feature_values:
        prob_y0 = cpt.get((fv, 0), 0)
        prob_y1 = cpt.get((fv, 1), 0)
        print(f"{fv:<20} {prob_y0:<25.6f} {prob_y1:<25.6f}")
    

def compute_prior_probabilites(y_train):
   
    count_yes=0
    for y in y_train: 
        if y == 1: 
            count_yes+=1
    prob_yes = count_yes/len(y_train)
    cpt_table = {
        0: 1 - prob_yes, 
        1: prob_yes
    }
    return cpt_table

def conditional_probality_glucose(X_train, y_train):
    cpt_glucose = {}
        
    for y_value in [0, 1]:
        glucose_given_y = X_train[y_train == y_value]['glucose']
        counts = glucose_given_y.value_counts()
        total = len(glucose_given_y)
        
        # compute probs
        for x in X_train['glucose'].unique():
            cpt_glucose[(x, y_value)] = counts.get(x, 0) / total
    
    return cpt_glucose

def conditional_probability_blood_pressure(X_train, y_train):
    cpt_bloodpressure = {}

    for y_value in [0,1]:
        blood_pressure_given_y = X_train[y_train == y_value]['bloodpressure']
        counts = blood_pressure_given_y.value_counts()
        total=len(blood_pressure_given_y)

        for x in X_train['bloodpressure'].unique():
            cpt_bloodpressure[(x, y_value)] = counts.get(x, 0) / total

    return cpt_bloodpressure

def inference(cpt_y, cpt_glucose, cpt_blood_pressure, x1, x2):
    unnormalized = {}
    
    for y_value in [0, 1]:
        # P(Y) * P(X1|Y) * P(X2|Y)
        p_y = cpt_y.get(y_value, 0)
        p_x1_given_y = cpt_glucose.get((x1, y_value), 0)
        p_x2_given_y = cpt_blood_pressure.get((x2, y_value), 0)
        
        unnormalized[y_value] = p_y * p_x1_given_y * p_x2_given_y
    
    # Normalize
    total = sum(unnormalized.values())
    
    if total == 0:
        # Handle unseen combinations (shouldn't happen with proper data)
        return {0: 0.5, 1: 0.5}
    
    normalized = {y: prob / total for y, prob in unnormalized.items()}
    
    return normalized
def create_table(X_test, cpt_y, cpt_glucose, cpt_bloodpressure):
    lookup_table = {}
    unique_combinations = X_test[['glucose', 'bloodpressure']].drop_duplicates()
    for _, row in unique_combinations.iterrows():
        x1, x2 = int(row['glucose']), int(row['bloodpressure'])
        lookup_table[(x1, x2)] = inference(cpt_y, cpt_glucose, cpt_bloodpressure, x1, x2)
    
    return lookup_table
def predict(X_test,table, cpt_y, cpt_glucose, cpt_bloodpressure):
    predictions = []
    
    for _, row in X_test.iterrows():
        x1, x2 = int(row['glucose']), int(row['bloodpressure'])
        
        probs = table.get((x1, x2))
    
        # Predict Y=1 if P(Y=1|x1,x2) > P(Y=0|x1,x2)
        prediction = 1 if probs[1] > probs[0] else 0
        predictions.append(prediction)
    
    return np.array(predictions)
    
def compute_accuracy(y_true, y_pred):
    correct = np.sum(y_true.values == y_pred)
    total = len(y_true)
    return correct / total

def main():
    
    print("Question 2: Naive Bayes Classifier for Diabetes Prediction")
    
    # load and split into stratified dataset
    filepath = r'Naive-Bayes-Classification-Data.csv'
    df = pd.read_csv(filepath)
    X_train, X_test, y_train, y_test = train_test_split(
        df[['glucose', 'bloodpressure']],
        df['diabetes'],
        test_size=0.3,
        random_state=42
    )

    
    print("\nDataset Information:")
    print(f"  Total samples: {len(X_train) + len(X_test)}")
    print(f"  Training samples: {len(X_train)} (70%)")
    print(f"  Testing samples: {len(X_test)} (30%)")
    print(f"  Training diabetes distribution: Y=0: {sum(y_train == 0)}, Y=1: {sum(y_train == 1)}")
    print(f"  Testing diabetes distribution: Y=0: {sum(y_test == 0)}, Y=1: {sum(y_test == 1)}")


    print("Question 2.1 Introducting Conditional Independence Assumptions.")
    
    print("Question 2.1.1. Compute the Prior Probabilites of diabetes. P(Y).")
    cpt_prior_table= compute_prior_probabilites(y_train=y_train)
    print(f"The prior probabilies of diabetes (Y=1) is {cpt_prior_table[1]:.4f}, and the probality of no diabetes is {cpt_prior_table[0]:.4f}.")
    
    print("Question 2.1.2 The conditional probabilities of glucose blood levels given Y.")
    cpt_glucose = conditional_probality_glucose(X_train, y_train)
    for key,value in cpt_glucose.items():
        print(f"The conditional probabilites for glucose levels and diabetes diagnosis {key} are {value:.4f}")
    
    print("Question 2.1.3 The conditional probabilities of blood pressure levels given Y.")
    cpt_blood_pressure = conditional_probability_blood_pressure(X_train, y_train)
    for key, value in cpt_blood_pressure.items():
        print(f"The conditional probabilites for blood pressure and diabetes diagnosis {key} are {value:.4f}")
    

    print("Question 2.2 Implementing Inference by Enumeration.")
    print("Question 2.2.1 Write code to answer the inference query: P(Y|X1, X2)")
    print("Question 2.2.2 Generate a lookup table for P (Y | X1, X2) using the test data.")
    table = create_table(X_test, cpt_prior_table, cpt_glucose, cpt_blood_pressure)
    for i, ((x1,x2), probs) in enumerate(table.items()):
        print(f"{x1} {x2} {probs[0]:.6f} {probs[1]:.6f}")
        if i > 10: 
            break

    print("Question 2.3 Generating Predictions")
    print("Question 2.3.1 For each test data point: Compute P(Y = 1 | x1, x2) and P (Y = 0 | x1, x2) and Predict Y = 1 if P (Y = 1 | x1, x2) > P (Y = 0 | x1, x2); otherwise, predict Y = 0.")
    test_predictions = predict(X_test,table, cpt_prior_table, cpt_glucose, cpt_blood_pressure)
    i=0
    for pred in test_predictions: 
        print(f"Prediction: {pred:.4f}")
        if i> 10: 
            break
        i+=1
    print("Question 2.3.2 Generating Accuracy Reports")
    accuracy = compute_accuracy(y_test, test_predictions)
    print(f"Accuracy: {accuracy:.4f}")
if __name__ == "__main__":
    main()