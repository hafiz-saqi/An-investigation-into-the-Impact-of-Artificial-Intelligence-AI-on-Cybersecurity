import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd
import pickle
import time
from datetime import datetime

# Function to load the pre-trained Random Forest Classifier
def load_model():
    with open('random_forest_classifier0032.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

# Function to handle file upload
def upload_file():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filename:
        df = pd.read_csv(filename)
        return df
    else:
        return None

# Function to detect network intrusions with styled output and developer name
def detect_intrusions():
    global df
    if df is None:
        messagebox.showerror("Error", "Please upload a CSV file first!")
        return

    start_time = time.time()
    model = load_model()

    try:
        X = df.drop(columns=['Label', 'Attack'])
    except KeyError:
        messagebox.showerror("Error", "CSV file must contain 'Label' and 'Attack' columns.")
        return

    y_pred = model.predict(X)
    end_time = time.time()
    detection_time = end_time - start_time
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Fix for more readable row numbers (starting from 1 instead of 0)
    attack_indices = df[y_pred == 1].index.tolist()
    display_indices = [i + 4 for i in attack_indices]  # for human-readable row numbers
    attack_names = df.loc[attack_indices, 'Attack'].tolist()

    if len(attack_indices) > 0:
        detection_results = (
            f"🛡️ Output Time Stamp ({timestamp})\n\n"
            f"🔍 Detected attacks: {len(attack_indices)}\n"
            f"📍 Row numbers: {display_indices}\n"
            f"🚨 Attack names: {attack_names}\n\n"
            f"⏱️ Detection Time: {detection_time:.4f} seconds\n\n"
            f"🤖 AI Embedded NIDS Project Developer: Hafiz Saqi"
        )
    else:
        detection_results = (
            f"✅ No attacks detected!\n\n"
            f"⏱️ Detection Time: {detection_time:.4f} seconds\n\n"
            f"🤖 AI Embedded NIDS Project Developer: Hafiz Saqi"
        )

    # Display results
    result_window = tk.Tk()
    result_window.title("Detection Results")
    result_window.configure(bg="sky blue")
    result_window.geometry("800x400")

    text = scrolledtext.ScrolledText(result_window, wrap="word", height=20, width=80, bg="white", font=("Consolas", 11))
    text.insert("1.0", detection_results)
    text.pack(expand=True, fill="both")

    result_window.mainloop()

# Main GUI function
def main():
    global df
    root = tk.Tk()
    root.title("Network Intrusion Detection System")
    root.configure(bg="sky blue")
    root.geometry("800x400")

    def upload():
        global df
        df = upload_file()
        if df is not None:
            upload_label.config(text="✅ File Uploaded Successfully!")
        else:
            upload_label.config(text="❌ Upload Failed!")

    def detect():
        detect_intrusions()

    upload_button = tk.Button(root, text="Upload CSV File", command=upload, bg="Yellow")
    detect_button = tk.Button(root, text="Detect", command=detect, bg="Salmon")
    upload_label = tk.Label(root, text="", bg="lightblue", fg="Red")

    upload_button.pack(expand=True, pady=10)
    detect_button.pack(expand=True, pady=10)
    upload_label.pack(expand=True)

    root.mainloop()

if __name__ == "__main__":
    df = None
    main()