import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from keras.metrics import Precision, Recall
from src.config import DEEP_DATA_PATH
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
import os
import winsound
import time
def specificity(y_true, y_pred, threshold=0.5):
    y_pred_thresholded = tf.cast(y_pred > threshold, tf.bool)
    y_true = tf.cast(y_true, tf.bool)

    true_negatives = tf.reduce_sum(tf.cast(tf.logical_and(tf.logical_not(y_true), tf.logical_not(y_pred_thresholded)), dtype=tf.float32))
    false_positives = tf.reduce_sum(tf.cast(tf.logical_and(tf.logical_not(y_true), y_pred_thresholded), dtype=tf.float32))

    return true_negatives / (true_negatives + false_positives + tf.keras.backend.epsilon())

def recall(y_true, y_pred, threshold=0.5):
    y_pred_thresholded = tf.cast(y_pred > threshold, tf.bool)
    y_true = tf.cast(y_true, tf.bool)

    true_positives = tf.reduce_sum(tf.cast(tf.logical_and(y_true, y_pred_thresholded), dtype=tf.float32))
    false_negatives = tf.reduce_sum(tf.cast(tf.logical_and(y_true, tf.logical_not(y_pred_thresholded)), dtype=tf.float32))

    return true_positives / (true_positives + false_negatives + tf.keras.backend.epsilon())

def naive_model(X_test, y_test):
    preds = []
    for x in X_test:
        if float(x[0]) == 1  or float(x[0]) == 0:
            preds.append(1)
        else:
            preds.append(0)

    # Calculate confusion matrix
    tn, fp, fn, tp = confusion_matrix(y_test, preds).ravel()

    # Calculate metrics
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp) if tp + fp != 0 else 0
    specificity = tn / (tn + fp) if tn + fp != 0 else 0
    recall = tp / (tp + fn) if tp + fn != 0 else 0  # Added recall calculation

    return accuracy, precision, specificity, recall


def neural_network(X_train, y_train, X_test, y_test):
    precision = Precision()

    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(100, activation='relu', input_shape=(X_train.shape[1],)),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(100, activation='relu'),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(100, activation='relu'),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(100, activation='relu'),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(100, activation='relu'),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy', precision, specificity, recall])

    model.fit(X_train, y_train, epochs=10, batch_size=64, validation_data=(X_test, y_test))

    results_train = model.evaluate(X_train, y_train)
    results_test = model.evaluate(X_test, y_test)

    loss_train = results_train[0]
    accuracy_train = results_train[1]
    precision_train = results_train[2]
    specificity_train = results_train[3]
    recall_train = results_train[4]

    loss_test = results_test[0]
    accuracy_test = results_test[1]
    precision_test = results_test[2]
    specificity_test = results_test[3]
    recall_test = results_test[4]

    return accuracy_train, precision_train, specificity_train, recall_train, accuracy_test, precision_test, specificity_test, recall_test, loss_train, loss_test



def naive_bayes(X_train, y_train, X_test, y_test):
    # Create a Gaussian Naive Bayes classifier
    nb_model = GaussianNB()

    # Train the model using the training sets
    nb_model.fit(X_train, y_train)

    # Predict on test set
    y_pred = nb_model.predict(X_test)

    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)

    # Precision
    precision = precision_score(y_test, y_pred)

    # Recall
    recall = recall_score(y_test, y_pred)

    # Specificity
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    specificity = tn / (tn + fp)

    # Displaying the metrics
    return accuracy, precision, specificity, recall



def polynomial_log_reg(X_train, y_train, X_test, y_test):
    poly = PolynomialFeatures(degree=2, include_bias=False)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)

    # Create a logistic regression classifier
    log_reg = LogisticRegression(max_iter=10000)

    # Train the model using the training sets with polynomial features
    log_reg.fit(X_train_poly, y_train)

    # Predict on test set with polynomial features
    y_pred = log_reg.predict(X_test_poly)
    y_pred_proba = log_reg.predict_proba(X_test_poly)[:, 1]  # Probabilities for the positive class

    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)

    # Precision
    precision = precision_score(y_test, y_pred)

    # Recall
    recall = recall_score(y_test, y_pred)

    # Specificity
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    specificity = tn / (tn + fp)

    return accuracy, precision, specificity, recall


def knn(X_train, y_train, X_test, y_test):

    # Create a K-NN classifier. You can change 'n_neighbors' to optimize performance
    knn = KNeighborsClassifier(n_neighbors=20)

    # Train the model using the training sets
    knn.fit(X_train, y_train)

    # Predict on test set
    y_pred = knn.predict(X_test)

    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)

    # Precision
    precision = precision_score(y_test, y_pred)

    # Recall
    recall = recall_score(y_test, y_pred)

    # Specificity
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    specificity = tn / (tn + fp)

    # Displaying the metrics
    return accuracy, precision, specificity, recall


def rfc(X_train, y_train, X_test, y_test):
    # Create a Random Forest classifier
    rf = RandomForestClassifier(n_estimators=1000)  # n_estimators is the number of trees in the forest

    # Train the model using the training sets
    rf.fit(X_train, y_train)

    # Predict on the test set
    y_pred = rf.predict(X_test)

    # Evaluate the model
    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)

    # Precision
    precision = precision_score(y_test, y_pred)

    # Recall
    recall = recall_score(y_test, y_pred)

    # Specificity
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    specificity = tn / (tn + fp)

    # Displaying the metrics
    return accuracy, precision, specificity, recall


def run_all_splits():
    all_results = []

    num_prev_prices = 20
    running_data_preprocesings = ["Bollinger", "Bollinger", "Turtle", "Box"]
    identifiers = ['test11bollinger', 'test22bollinger', 'test1turtles', 'test1box']

    splits_to_do = ["34_33_33", "80_10_10", "10_80_10", "10_10_80"]

    for i, val in enumerate(running_data_preprocesings):
        running_data_preprocesing = running_data_preprocesings[i]
        identifier = identifiers[i]
        for split_to_do in splits_to_do:
            print(f"Doing {split_to_do}, {identifier}")
            try:
                path = os.path.join(DEEP_DATA_PATH, f'deep{running_data_preprocesing}',
                                    f'{split_to_do}_scaled_combined_{identifier}_20100104_to_20201231_doctest2_numP{num_prev_prices}.csv')

                df = pd.read_csv(path, low_memory=False)

                X = df[[f'PrevPrice_{i}' for i in range(num_prev_prices + 1)]].values
                y = df['is_trade'].values

                # Train-test split
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False, random_state=42)

                # Running each model
                # nn_vals = neural_network(X_train, y_train, X_test, y_test)
                naive_vals = naive_model(X_test, y_test)
                # naive_bayes_vals = naive_bayes(X_train, y_train, X_test, y_test)
                # log_vals = polynomial_log_reg(X_train, y_train, X_test, y_test)
                # knn_vals = knn(X_train, y_train, X_test, y_test)
                # rfc_vals = rfc(X_train, y_train, X_test, y_test)

                # Collecting results
                # all_results.append(['NN', split_to_do, identifier, *nn_vals[:4], *nn_vals[4:8], nn_vals[8], nn_vals[9]])
                all_results.append(['Naive', split_to_do, identifier, '', '', '', '', *naive_vals, '', ''])
                # all_results.append(['Naive Bayes', split_to_do, identifier, '', '', '', '', *naive_bayes_vals, '', ''])
                # all_results.append(['Log Reg', split_to_do, identifier, '', '', '', '', *log_vals, '', ''])
                # all_results.append(['KNN', split_to_do, identifier, '', '', '', '', *knn_vals, '', ''])
                # all_results.append(['RFC', split_to_do, identifier, '', '', '', '', *rfc_vals, '', ''])

            except Exception as e:
                print(f"Error occurred: {e}")
                # Play a beep sound
                frequency = 2500  # Set Frequency in Hertz
                duration = 10000  # Set Duration in milliseconds (1000 ms = 1 second)
                winsound.Beep(frequency, duration)

    # Displaying the results
    for result in all_results:
        print(', '.join(map(str, result)))


    # Writing the results to a CSV file
    columns = ['Model', 'Split', 'Identifier', 'Accuracy Train', 'Precision Train', 'Specificity Train', 'Recall Train',
               'Accuracy Test', 'Precision Test', 'Specificity Test', 'Recall Test', 'Loss Train', 'Loss Test']

    print(all_results)
    results_df = pd.DataFrame(all_results, columns=columns)
    results_df.to_csv('model_comparison_results.csv', index=False)

    frequency = 500  # Set Frequency in Hertz
    duration = 10000  # Set Duration in milliseconds (1000 ms = 1 second)
    winsound.Beep(frequency, duration)

run_all_splits()