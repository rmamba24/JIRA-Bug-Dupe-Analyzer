import pandas as pd
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('wordnet')

global df

# this function pre-processes the descriptions column to compare descriptions in the file.
def process_descriptions(text):
    lemmatizer = WordNetLemmatizer()
    words = text.split()
    return ' '.join([lemmatizer.lemmatize(w.lower()) for w in words])

def find_similarities(df, input_description=None, key1=None, key2=None):
    # pre-process the descriptions
    df['Processed_Description'] = df['Description'].apply(process_descriptions)

    # vectorize the descriptions
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['Processed_Description'])

    if input_description and input_description.strip():
        # this function compares the typed descriptions
        input_processed = process_descriptions(input_description)
        input_vec = vectorizer.transform([input_processed])
        similarities = cosine_similarity(input_vec, tfidf_matrix)
    else:
        # comparing based on issue keys
        if key1 not in df['Key'].values:
            return f"Key {key1} not found in the data.", None
        if key2 and key2 not in df['Key'].values:
            return f"Key {key2} not found in the data.", None

        idx1 = df.index[df['Key'] == key1].tolist()[0]
        if key2:
            idx2 = df.index[df['Key'] == key2].tolist()[0]
            similarity = cosine_similarity(tfidf_matrix[idx1], tfidf_matrix[idx2])
            scaled_similarity = round(similarity[0][0] * 100, 2)  #the similarity score scales from 0-100.
            return f'Similarity Score: {scaled_similarity}', None
        else:
            similarities = cosine_similarity(tfidf_matrix[idx1], tfidf_matrix)

    # this function identifies similar issues
    similar_indices = similarities[0].argsort()[-3:][::-1]
    if key1:
        idx1 = df.index[df['Key'] == key1].tolist()[0]
        similar_indices = similar_indices[similar_indices != idx1]
    similar_issues = df.iloc[similar_indices]
    scaled_similarities = (similarities[0][similar_indices] * 100).round(2)
    return "Similar Issues Found:", (similar_issues, scaled_similarities)

# this sector of the code tackles the basic GUI.
def open_file():
    global df  # declare df as global within this function
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if file_path:
        df = pd.read_excel(file_path)
        file_label.config(text=f"File loaded: {file_path.split('/')[-1]}")
    else:
        file_label.config(text="No file selected")

def on_submit():
    global df  # declare df as global within this function
    key1 = entry_key1.get()
    key2 = entry_key2.get()
    input_description = desc_text.get("1.0", tk.END)

    if key1 or key2:
        # Compare by keys
        message, data = find_similarities(df, key1=key1, key2=key2)
        if data:
            # display similarity score
            messagebox.showinfo("Similarity Score", message)
        else:
            result_label.config(text=message)
    else:
        # compare by typed description
        message, data = find_similarities(df, input_description=input_description)
        result_label.config(text=message)
        if data:
            display_similar_issues(data)

def display_similar_issues(data):
    similar_issues, similarities = data
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    for i, (index, row) in enumerate(similar_issues.iterrows()):
        output_text.insert(tk.END, f"Issue Key: {row['Key']}\n")
        output_text.insert(tk.END, f"Summary: {row['Summary']}\n")
        output_text.insert(tk.END, f"Similarity Score: {similarities[i]}%\n")
        output_text.insert(tk.END, "----------------------------------------\n")
    output_text.config(state=tk.DISABLED)

# GUI Setup
root = tk.Tk()
root.title("JIRA Export Similarity/Duplicate Analyzer - Russ beta v1.0.1")
root.geometry("800x600")

open_file_button = tk.Button(root, text="Open JIRA Export", command=open_file)
open_file_button.pack()

file_label = tk.Label(root, text="No file selected")
file_label.pack()

label_key1 = tk.Label(root, text="[REQUIRED] Enter Issue Key:")
label_key1.pack()
entry_key1 = tk.Entry(root)
entry_key1.pack()

label_key2 = tk.Label(root, text="[OPTIONAL] Enter another to compare similarity:")
label_key2.pack()
entry_key2 = tk.Entry(root)
entry_key2.pack()

description_text = (
    "Alternatively, type your bug description to find similar bugs in the database.                "
    "*IMPORTANT: Leave the Issue Key fields blank if you want to use this feature.*                       "
    "*ALSO IMPORTANT: If you do not wish to use this feature, leave the field below blank.*"
)

description_label = tk.Label(root, text=description_text, wraplength=500)
description_label.pack()

result_label = tk.Label(root, text="")
result_label.pack()

output_text = scrolledtext.ScrolledText(root, state=tk.DISABLED, height=15, width=90)
output_text.pack()

root.mainloop()
