# Amber-JIRA-Tracker
 Prototype JIRA Issue Dupe Parser Tool 

#### 1. Background

This tool was developed internally for purposes of creating process improvements for QA Testers in Amber Studio. The primary focus of the application enables testers to do the following:

1. Upload a JIRA Export containing bug reports for a certain time period. Unfortunately, this is the only method that is available. 
2. Compare two different issues/bugs that may or may not have similarities based on syntax, style of writing, and context. 
3. Also be able to create your own description in one of the fields, after which the tool will compare against the entire provided database to check for similarities.
4. A similarity score is always given, ranging from 0.0% - 100%. 

In essence, testers can identify similar or duplicate bug reports and improve the overall efficiency of bug tracking and resolution processes. 

Note that this is the first version of the tool, and many more improvements will come along the way, including GUI fixes, UX improvements, additional features and so on. 

#### 2. Features
- **Compare Bug Reports by Issue Keys**: Users can input two bug report keys to compare their descriptions and receive a similarity score.
- **Compare a Typed Description Against Existing Reports**: Users can type a custom bug report description and find similar existing reports in the system.
- **Standalone Executable**: The tool can be compiled into a standalone executable file (.exe) for easy distribution and usage without requiring a separate Python environment.

#### 3. Libraries and Dependencies Used
- **Pandas**: Used for data manipulation and analysis. It is particularly suited for handling and analyzing input data in tabular format (like Excel files).
- **Tkinter**: A standard library for Python's GUI applications. Used to create the user interface for this tool.
- **Scikit-learn**: Utilized for NLP (Natural Language Processing). Specifically, it provides the TF-IDF (Term Frequency-Inverse Document Frequency) vectorizer and cosine similarity measures to analyze and compare the textual content of bug reports.
- **NLTK (Natural Language Toolkit)**: A leading platform for building Python programs to work with human language data. It is used for text preprocessing, such as tokenization and lemmatization.
- **PyInstaller**: A tool used to convert Python applications into stand-alone executables, under Windows, Linux, and Mac OS X.

#### 4. Short Breakdown of the Code
- **Data Loading**: The application uses Pandas to load bug reports from an Excel file.
- **GUI Creation**: The GUI, built with Tkinter, includes input fields for bug report keys and a large text box for typing a custom description.
- **Text Preprocessing**: Text descriptions are preprocessed using NLTK's lemmatization to convert words into their base or root form.
- **Text Comparison**: The TF-IDF vectorizer from Scikit-learn is used to convert text descriptions into a matrix of TF-IDF features. Cosine similarity is then used to calculate the similarity between bug reports.
- **Executable Creation**: PyInstaller is used to bundle the application and all its dependencies into a single executable file for distribution.



#### 5. Limitations

- You must type the EXACT Issue Key (no spaces) or it will not be able to find the string. 
- The interface is really clunky, this was meant to demonstrate its working capability. 
- This is meant to be a local tool, which means that it can't access JIRA directly. You can only upload an excel based export in .xlx or .xlsx format. 
- It is not LIVE, which means that you will have to continuously export bug reports should you wish to compare with newer reports for a certain fixed period of time. 