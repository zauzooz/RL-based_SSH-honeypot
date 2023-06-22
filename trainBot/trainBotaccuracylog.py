import datetime
import os
import json
import logging

def accuracy_log(formatted_datetime: str, predict: dict):
    n_sample = len(predict)
    n_true_predictions = [i for i in predict.values()].count(1)

    data = {
        "day time" : formatted_datetime,
        "predicts" : predict,
        "n_samples" : n_sample,
        "n_true_predicts" : n_true_predictions,
        "accuracy" : float(n_true_predictions / n_sample)
    }
    print(f"n_true_predict: {n_true_predictions}/{n_sample}")

    json.dump(
        data,
        open(f"trainBot/accuracy_log/accuracy_{formatted_datetime}.json", "w"),
        indent=6
    )