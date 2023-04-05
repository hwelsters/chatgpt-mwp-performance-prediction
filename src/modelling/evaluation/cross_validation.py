from sklearn.model_selection import KFold
from sklearn.metrics import classification_report


def cross_validate(model, x_data, y_data, n_splits, random_state=42, shuffle=True):
    cross_fold = KFold(n_splits, random_state=random_state, shuffle=shuffle)

    cross_validation_results = []
    for i, (train_index, test_index) in enumerate(cross_fold.split(x_data)):
        x_train, y_train = x_data.iloc[train_index], y_data.iloc[train_index]
        x_test, y_test = x_data.iloc[test_index], y_data.iloc[test_index]

        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)

        report = classification_report(y_test, y_pred, target_names=[
                                       '0', '1'], output_dict=True)
        cross_validation_results.append({"0": report["0"], "1": report["1"]})

    total_precision_0 = 0
    total_recall_0 = 0
    total_f1_0 = 0
    total_precision_1 = 0
    total_recall_1 = 0
    total_f1_1 = 0

    for result in cross_validation_results:
        total_precision_0 += result["0"]["precision"]
        total_recall_0 += result["0"]["recall"]
        total_f1_0 += result["0"]["f1-score"]
        total_precision_1 += result["1"]["precision"]
        total_recall_1 += result["1"]["recall"]
        total_f1_1 += result["1"]["f1-score"]

    average_precision_0 = total_precision_0 / len(cross_validation_results)
    average_recall_0 = total_recall_0 / len(cross_validation_results)
    average_f1_0 = total_f1_0 / len(cross_validation_results)
    average_precision_1 = total_precision_1 / len(cross_validation_results)
    average_recall_1 = total_recall_1 / len(cross_validation_results)
    average_f1_1 = total_f1_1 / len(cross_validation_results)

    cross_validation_results.append({"0":
                                     {
                                         "average precision": average_precision_0,
                                         "average recall": average_recall_0,
                                         "average f1-score": average_f1_0
                                     }, "1":
                                     {
                                         "average precision": average_precision_1,
                                         "average recall": average_recall_1,
                                         "average f1-score": average_f1_1
                                     }
                                     })

    return {"0":
            {
                "average precision": average_precision_0,
                "average recall": average_recall_0,
                "average f1-score": average_f1_0
            }, "1":
            {
                "average precision": average_precision_1,
                "average recall": average_recall_1,
                "average f1-score": average_f1_1
            }
            }
