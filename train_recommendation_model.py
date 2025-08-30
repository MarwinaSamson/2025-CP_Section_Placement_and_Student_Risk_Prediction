import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib
import os
import numpy as np

# --- Configuration ---
# Define the path where the trained models will be saved
MODEL_SAVE_DIR = 'ml_models'
# Ensure this list matches the target program columns in your dataset
TARGET_PROGRAMS = ['hetero', 'top 5', 'ste', 'spfl', 'sptve']
# Random state for reproducibility
RANDOM_STATE = 42

# --- 1. Data Loading and Initial Preprocessing ---
def load_and_preprocess_data(file_path):
    """
    Loads the dataset and performs initial preprocessing steps.
    """
    print(f"Loading data from: {file_path}")
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: Dataset file not found at {file_path}. Please check the path.")
        exit() # Exit if the file is not found

    print("Original DataFrame Head:")
    print(df.head())
    print("\nDataFrame Info:")
    df.info()

    # Check for missing values
    print("\nMissing values before handling:")
    print(df.isnull().sum())
    # For this dataset, we assume no missing values in critical columns.
    # If there were, you'd add handling here (e.g., df.dropna(), df.fillna()).

    # Drop 'student id' column as it's not a feature for the model
    if 'student id' in df.columns:
        df = df.drop('student id', axis=1)
        print("\nDataFrame Head after dropping 'student id':")
        print(df.head())
    else:
        print("\n'student id' column not found. Skipping drop.")

    return df

# --- 2. Data Splitting ---
def split_data(df):
    """
    Splits the data into features (X) and target variables (y),
    then further splits into training, validation, and test sets.
    """
    # Define features (X) and target variables (y)
    # Features are all columns except the target programs
    X = df.drop(TARGET_PROGRAMS, axis=1)
    # Target variables are the program recommendations
    y = df[TARGET_PROGRAMS]

    print(f"\nFeatures (X) columns: {X.columns.tolist()}")
    print(f"Target (y) columns: {y.columns.tolist()}")

    # Split data into training + validation (85%) and test (15%)
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=0.15, random_state=RANDOM_STATE, stratify=y[TARGET_PROGRAMS[0]]
    )

    # Split training + validation into training (approx 70%) and validation (approx 15%)
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=(0.15 / 0.85), random_state=RANDOM_STATE, stratify=y_train_val[TARGET_PROGRAMS[0]]
    )

    print(f"\nShape of X_train: {X_train.shape}")
    print(f"Shape of X_val: {X_val.shape}")
    print(f"Shape of X_test: {X_test.shape}")
    print(f"Shape of y_train: {y_train.shape}")
    print(f"Shape of y_val: {y_val.shape}")
    print(f"Shape of y_test: {y_test.shape}")

    return X_train, X_val, X_test, y_train, y_val, y_test, X.columns.tolist()

# --- 3. Model Training and Hyperparameter Tuning ---
def train_and_tune_models(X_train, X_val, y_train, y_val):
    """
    Trains and tunes a Decision Tree Classifier for each target program.
    """
    models = {}
    best_params = {}
    best_scores = {}

    # Hyperparameter grid for Decision Tree
    param_grid = {
        'max_depth': [None, 5, 10, 15],
        'min_samples_leaf': [1, 5, 10],
        'criterion': ['gini', 'entropy']
    }

    print("\nTraining and Tuning Models for Each Program:")
    for program in TARGET_PROGRAMS:
        print(f"\n--- Training for program: {program} ---")
        dt_classifier = DecisionTreeClassifier(random_state=RANDOM_STATE)

        grid_search = GridSearchCV(dt_classifier, param_grid, cv=3, scoring='f1', n_jobs=-1, verbose=1)
        grid_search.fit(X_train, y_train[program])

        models[program] = grid_search.best_estimator_
        best_params[program] = grid_search.best_params_
        best_scores[program] = grid_search.best_score_

        print(f"Best parameters for {program}: {best_params[program]}")
        print(f"Best F1-score on training data (cross-validation) for {program}: {best_scores[program]:.4f}")

        y_val_pred = models[program].predict(X_val)
        val_accuracy = accuracy_score(y_val[program], y_val_pred)
        val_precision = precision_score(y_val[program], y_val_pred, zero_division=0)
        val_recall = recall_score(y_val[program], y_val_pred, zero_division=0)
        val_f1 = f1_score(y_val[program], y_val_pred, zero_division=0)

        print(f"Validation Accuracy for {program}: {val_accuracy:.4f}")
        print(f"Validation Precision for {program}: {val_precision:.4f}")
        print(f"Validation Recall for {program}: {val_recall:.4f}")
        print(f"Validation F1-score for {program}: {val_f1:.4f}")

        if len(np.unique(y_val[program])) > 1:
            y_val_proba = models[program].predict_proba(X_val)[:, 1]
            val_roc_auc = roc_auc_score(y_val[program], y_val_proba)
            print(f"Validation ROC AUC for {program}: {val_roc_auc:.4f}")
        else:
            print(f"Validation ROC AUC for {program}: Not applicable (only one class present in validation set)")
    
    return models

# --- 4. Model Evaluation ---
def evaluate_models(models, X_test, y_test):
    """
    Evaluates the trained models on the unseen test set.
    """
    print("\nEvaluating Models on Test Set:")
    test_results = {}

    for program in TARGET_PROGRAMS:
        print(f"\n--- Evaluating for program: {program} ---")
        model = models[program]
        y_test_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test[program], y_test_pred)
        precision = precision_score(y_test[program], y_test_pred, zero_division=0)
        recall = recall_score(y_test[program], y_test_pred, zero_division=0)
        f1 = f1_score(y_test[program], y_test_pred, zero_division=0)

        test_results[program] = {
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1-score': f1
        }

        print(f"Test Accuracy for {program}: {accuracy:.4f}")
        print(f"Test Precision for {program}: {precision:.4f}")
        print(f"Test Recall for {program}: {recall:.4f}")
        print(f"Test F1-score for {program}: {f1:.4f}")

        if len(np.unique(y_test[program])) > 1:
            y_test_proba = model.predict_proba(X_test)[:, 1]
            roc_auc = roc_auc_score(y_test[program], y_test_proba)
            test_results[program]['ROC AUC'] = roc_auc
            print(f"Test ROC AUC for {program}: {roc_auc:.4f}")
        else:
            print(f"Test ROC AUC for {program}: Not applicable (only one class present in test set)")

    print("\nSummary of Test Results:")
    for program, metrics in test_results.items():
        print(f"\nProgram: {program}")
        for metric, value in metrics.items():
            print(f"  {metric}: {value:.4f}")

# --- 5. Model Saving ---
def save_models(models, feature_columns):
    """
    Saves the trained models and feature column names to disk.
    """
    os.makedirs(MODEL_SAVE_DIR, exist_ok=True)
    print(f"\nSaving trained models to '{MODEL_SAVE_DIR}' directory:")

    for program, model in models.items():
        model_filename = os.path.join(MODEL_SAVE_DIR, f'decision_tree_model_{program}.joblib')
        joblib.dump(model, model_filename)
        print(f"Model for {program} saved to {model_filename}")

    feature_columns_filename = os.path.join(MODEL_SAVE_DIR, 'feature_columns.joblib')
    joblib.dump(feature_columns, feature_columns_filename)
    print(f"Feature columns saved to {feature_columns_filename}")

# --- Main Execution ---
if __name__ == "__main__":
    # Replace this with your actual dataset path inside the 'data' folder
    dataset_path = os.path.join('data', 'data_program_recommendation.csv')

    df = load_and_preprocess_data(dataset_path)
    X_train, X_val, X_test, y_train, y_val, y_test, feature_cols = split_data(df)
    trained_models = train_and_tune_models(X_train, X_val, y_train, y_val)
    evaluate_models(trained_models, X_test, y_test)
    save_models(trained_models, feature_cols)

    print("\nModel training process completed successfully!")
