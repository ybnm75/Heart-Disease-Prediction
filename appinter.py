import tkinter as tk
from tkinter import messagebox
import pickle
import numpy as np
from PIL import Image, ImageTk

def proceed_to_prediction():
    welcome_screen.destroy()  # Close the welcome screen
    prediction_screen()

def prediction_screen():
    # Load the pre-trained models
    pmc_model_path = r"C:\Users\pc\Downloads\pmc.pk1"
    knn_model_path = r"C:\Users\pc\Downloads\knn.pk1"

    with open(pmc_model_path, 'rb') as file:
        pmc_model = pickle.load(file)

    with open(knn_model_path, 'rb') as file:
        knn_model = pickle.load(file)

    # Create Tkinter app
    root = tk.Tk()
    root.title("Heart Disease Predictor")

    # Center the window on the screen
    window_width = 600  # Set your desired window width
    window_height = 600  # Set your desired window height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    # Add a title at the top of the interface
    title_label = tk.Label(root, text="Heart Disease Predictor", font=("Helvetica", 16, "bold"))
    title_label.grid(row=0, columnspan=2, pady=10)

    # Dropdown menu for model selection
    model_selection_label = tk.Label(root, text="Select Model:")
    model_selection_label.grid(row=1, column=0, padx=10, pady=5)

    selected_model = tk.StringVar(root)
    selected_model.set("PMC")  # Default selected model

    model_dropdown = tk.OptionMenu(root, selected_model, "PMC", "KNN")
    model_dropdown.grid(row=1, column=1, padx=10, pady=5)

    # Function to predict heart disease based on the selected model
    def predict_heart_disease(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal):
        selected_model_name = selected_model.get()
        if selected_model_name == "PMC":
            model = pmc_model
        else:
            model = knn_model

        # Preprocess the input data
        user_data = np.array([age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]).reshape(1, -1)
        # Make prediction
        prediction = model.predict(user_data)
        probability1 = model.predict_proba(user_data)[0][1]  # Probability of belonging to class 1
        probability0 = model.predict_proba(user_data)[0][0]  # Probability of belonging to class 0
        if prediction[0] == 1:
            messagebox.showinfo("Prediction", f"You are at risk of heart disease with a probability of {probability1:.2%}")
        else:
            messagebox.showinfo("Prediction", f"You are not at risk of heart disease with a probability of {probability0:.2%}.")

    # Create labels and entry fields for user input
    labels = ["Age:", "Sex:", "Chest Pain Type:", "Resting Blood Pressure:", "Cholesterol:",
              "Fasting Blood Sugar:", "Resting Electrocardiographic Results:", "Maximum Heart Rate Achieved:",
              "Exercise Induced Angina:", "Oldpeak:", "Slope of the Peak Exercise ST Segment:",
              "Number of Major Vessels Colored by Fluoroscopy:", "Thalassemia:"]
    entries = []

    for i, label_text in enumerate(labels):
        tk.Label(root, text=label_text).grid(row=i+2, column=0, padx=10, pady=5)  # Align labels to the right
        entry = tk.Entry(root)
        entry.grid(row=i+2, column=1, padx=10, pady=5)  # Align entries to the left
        entries.append(entry)

    # Function to get user input and trigger prediction
    def get_user_input_and_predict():
        # Get user input for all symptoms
        age = int(entries[0].get())
        sex = int(entries[1].get())
        cp = int(entries[2].get())
        trestbps = int(entries[3].get())
        chol = int(entries[4].get())
        fbs = int(entries[5].get())
        restecg = int(entries[6].get())
        thalach = int(entries[7].get())
        exang = int(entries[8].get())
        oldpeak = float(entries[9].get())
        slope = int(entries[10].get())
        ca = int(entries[11].get())
        thal = int(entries[12].get())

        # Call predict_heart_disease function with all inputs
        predict_heart_disease(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal)

    # Button to trigger prediction
    predict_button = tk.Button(root, text="Predict", command=get_user_input_and_predict)
    predict_button.grid(row=len(labels)+2, columnspan=2, padx=10, pady=10)

    # Run the Tkinter event loop
    root.mainloop()

# Create the welcome screen
welcome_screen = tk.Tk()
welcome_screen.title("Welcome to Heart Disease Predictor")

# Add a title at the top of the interface
title_label = tk.Label(welcome_screen, text="Heart Disease Predictor", font=("Helvetica", 24, "bold"))
title_label.pack(pady=20)

# Add an image to show the subject of the project
# Replace "heart.jpg" with the path to your image file
pil_image = Image.open("heart.jpg")

# Resize the image to fit the screen while maintaining aspect ratio
width, height = pil_image.size
max_height = welcome_screen.winfo_screenheight() - 100  # Adjust this value as needed
resize_factor = 0.5
new_width = int(width * resize_factor)
new_height = int(height * resize_factor)
pil_image = pil_image.resize((new_width, new_height))

# Convert the Pillow image to a Tkinter-compatible format
tk_image = ImageTk.PhotoImage(pil_image)
image_label = tk.Label(welcome_screen, image=tk_image)
image_label.pack(pady=20)

# Add a list of student names
student_names = "Presented By:\n\nAit Djebbara Ramzi \nAyad Tasnime Dalel \nBouzid Yasmine \nGuerch Lina \nZiane Lina "
student_label = tk.Label(welcome_screen, text=student_names, font=("Helvetica", 12))
student_label.pack()

# Add a proceed button to go to the prediction screen
proceed_button = tk.Button(welcome_screen, text="Proceed", command=proceed_to_prediction)
proceed_button.pack(pady=20)

# Run the Tkinter event loop for the welcome screen
welcome_screen.mainloop()
