import os
import pandas as pd
import dill
import json

path = os.environ.get('PROJECT_PATH', '.')
def load_model(model_path):
    with open(model_path, 'rb') as file:
        model = dill.load(file)
    return model


def predict(model, data):
    try:
        y = model.predict(data)
        return y
    except Exception as e:
        print(f"Prediction error: {e}")
        return None


def save_predictions(predictions, output_path):
    df = pd.DataFrame(predictions, columns=["Prediction"])
    df.to_csv(output_path, index=False)
    print(f"Predictions saved to {output_path}")


def process_files(model, folder_path):
    all_predictions = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.json'):
            with open(file_path) as fin:
                form = json.load(fin)
                df = pd.DataFrame.from_dict([form])
                predictions = predict(model, df)
                if predictions is not None:
                    print(f'{form["id"]}: {predictions[0]}')
                    all_predictions.append({"id": form["id"], "prediction": predictions[0]})
                else:
                    print(f'Unable to make predictions for {filename}')

    return all_predictions


def main():
    model_path = f'{path}/data/models/cars_pipe_202312171628.pkl'
    test_data_folder = f'{path}/data/test/'
    model = load_model(model_path)
    all_predictions = process_files(model, test_data_folder)
    output_file_path = f'{path}/data/predictions/predictions.csv'
    if all_predictions:
        final_df = pd.DataFrame(all_predictions)
        final_df.to_csv(output_file_path, index=False)
        print(f"Predictions saved to {output_file_path}")
    else:
        print("No valid predictions to save.")


if __name__ == '__main__':
    main()