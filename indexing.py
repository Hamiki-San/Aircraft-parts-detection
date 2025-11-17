from ultralytics import YOLO
import os

def get_model_info(model_path):
    """
    Loads a YOLO model and provides information about its classes and
    guidance on where to find training metrics.

    Args:
        model_path (str): The path to the .pt model file.
    """
    print(f"Loading model from: {model_path}")
    
    # 1. Load the .pt file
    try:
        model = YOLO(model_path)
    except FileNotFoundError:
        print(f"Error: Model file not found at '{model_path}'. Please check the path.")
        return
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        return

    # 2. Access the 'names' attribute to get class names and indices
    if hasattr(model, 'names'):
        class_names = model.names
        print("\n--- Model Class Names ---")
        for idx, name in class_names.items():
            print(f"Index: {idx}, Name: {name}")
    else:
        print("Warning: Class names could not be found in the model.")

    # 3. Provide guidance on where to find accuracy and dataset information
    print("\n--- Training Metrics and Dataset Information ---")
    print("This information is not stored in the '.pt' model file itself.")
    print("It is typically saved in the directory where the model was trained.")

    # Get the parent directory of the model file
    model_dir = os.path.dirname(os.path.abspath(model_path))
    
    # Check for the run directory, which usually contains the logs
    runs_dir = os.path.join(model_dir, 'runs')
    if not os.path.exists(runs_dir):
        print(f"Tip: The 'runs' directory (e.g., '{runs_dir}') was not found.")
        print("Look for the 'runs' directory in your project to find the training logs.")
        return

    # Look for the last training run
    last_run_dir = None
    runs = sorted([d for d in os.listdir(runs_dir) if os.path.isdir(os.path.join(runs_dir, d))])
    if runs:
        last_run_dir = os.path.join(runs_dir, runs[-1])

    if last_run_dir and os.path.exists(last_run_dir):
        print(f"Based on the project structure, training logs may be located here:")
        print(f"  - Directory: {last_run_dir}")
        
        # Guide the user to the metrics file
        metrics_file = os.path.join(last_run_dir, 'results.csv')
        if os.path.exists(metrics_file):
            print(f"  - Accuracy, Precision, Recall, and other metrics are in: {metrics_file}")
        else:
            print(f"  - The 'results.csv' file was not found. Look for other log files.")

        # Guide the user to the dataset info file
        args_file = os.path.join(last_run_dir, 'args.yaml')
        if os.path.exists(args_file):
            print(f"  - Dataset information (e.g., path, names) is in: {args_file}")
        else:
            print(f"  - The 'args.yaml' file was not found. Look for other configuration files.")
    else:
        print("Could not locate the training run directory. Please navigate to the folder where you ran `model.train()`.")

# Example usage:
# Replace 'abishai_model.pt' with the actual path to your model file
get_model_info('yolo11s.pt')
