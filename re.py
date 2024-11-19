# -*- coding: utf-8 -*-
"""re.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TcwXKkFd3KsU9FpXWhq5xl-32NSxUmU9
"""



from google.colab import drive
drive.mount('/content/drive')

import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import re
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

data = pd.read_csv('/content/drive/MyDrive/project-re/project (2).csv')
data.head()

# unique ratings
pd.unique(data['Rate'])



sns.countplot(data=data,
			x='Rate',
			order=data.Rate.value_counts().index)

# rating label(final)
pos_neg = []
for i in range(len(data['Rate'])):
	if data['Rate'][i] <3:
		pos_neg.append(0)
	elif data['Rate'][i] ==3:
		pos_neg.append(-1)
	else:
		pos_neg.append(1)
data['label'] = pos_neg

from tqdm import tqdm


def preprocess_text(text_data):
	preprocessed_text = []

	for sentence in tqdm(text_data):
		# Removing punctuations
		sentence = re.sub(r'[^\w\s]', '', sentence)

		# Converting lowercase and removing stopwords
		preprocessed_text.append(' '.join(token.lower()
										for token in nltk.word_tokenize(sentence)
										if token.lower() not in stopwords.words('english')))

	return preprocessed_text

import nltk
nltk.download('punkt')

preprocessed_review = preprocess_text(data['Review'].values)
data['Review'] = preprocessed_review

data.head(5)

data["label"].value_counts()

consolidated = ' '.join(
	word for word in data['Review'][data['label'] == 1].astype(str))
wordCloud = WordCloud(width=1600, height=800,
					random_state=21, max_font_size=110)
plt.figure(figsize=(15, 10))
plt.imshow(wordCloud.generate(consolidated), interpolation='bilinear')
plt.axis('off')
plt.show()

cv = TfidfVectorizer(max_features=2500)
X = cv.fit_transform(data['Review'] ).toarray()
X

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, data['label'],
													test_size=0.33,
													stratify=data['label'],
													random_state = 42)

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score  # Import accuracy_score

model = DecisionTreeClassifier(random_state=0)
model.fit(X_train, y_train)

# Testing the model
pred = model.predict(X_train)
print(accuracy_score(y_train, pred))



from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Create a Decision Tree classifier
model = DecisionTreeClassifier(random_state=0)

# Train the model on the training data
model.fit(X_train, y_train)

# Predict the labels for the training data
train_pred = model.predict(X_train)

# Evaluate the accuracy of the model on the training data
train_accuracy = accuracy_score(y_train, train_pred)
print("Training Accuracy:", train_accuracy)

# Predict the labels for the test data
test_pred = model.predict(X_test)

# Evaluate the accuracy of the model on the test data
test_accuracy = accuracy_score(y_test, test_pred)
print("Test Accuracy:", test_accuracy)

import matplotlib.pyplot as plt

# Plotting the training and testing accuracies
plt.plot(["Training", "Testing"], [train_accuracy, test_accuracy], marker='o', linestyle='-')
plt.title("Training vs Testing Accuracy")
plt.xlabel("Dataset")
plt.ylabel("Accuracy")
plt.ylim(0, 1)  # Set y-axis limit to 0-1 for accuracy
plt.grid(True)
plt.show()

import pandas as pd
import numpy as np
import math
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Load the dataset
data = pd.read_csv('/content/drive/MyDrive/project-re/project (2).csv')

# Assuming 'target_column' is the name of your target column
X = data.drop('Sentiment', axis=1)  # Features
y = data['Sentiment']  # Target variable



# One-hot encode categorical variables
X = pd.get_dummies(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Train a Decision Tree classifier
model = DecisionTreeClassifier(random_state=0)
model.fit(X_train, y_train)

# Define functions for entropy and information gain
def entropy(y):
    class_counts = Counter(y)
    total_samples = len(y)
    entropy = 0
    for count in class_counts.values():
        probability = count / total_samples
        entropy -= probability * math.log2(probability)
    return entropy

def information_gain(X, y, feature_index):
    total_entropy = entropy(y)
    unique_values = np.unique(X.iloc[:, feature_index])
    new_entropy = 0
    for value in unique_values:
        subset_indices = np.where(X.iloc[:, feature_index] == value)[0]
        subset_entropy = entropy(y.iloc[subset_indices])
        subset_weight = len(subset_indices) / len(y)
        new_entropy += subset_weight * subset_entropy
    information_gain = total_entropy - new_entropy
    return information_gain

# Calculate entropy of the target variable
target_entropy = entropy(y_train)
print("Entropy of target variable:", target_entropy)

# Calculate information gain for each feature
information_gains = []
for feature_index in range(X_train.shape[1]):
    information_gains.append(information_gain(X_train, y_train, feature_index))

# Print information gains for each feature
print("Information gains for each feature:")
for i, gain in enumerate(information_gains):
    print("Feature", i, ":", gain)

# Calculate gain ratio for each feature
total_feature_entropy = sum(information_gains)
gain_ratios = [gain / total_feature_entropy if total_feature_entropy != 0 else 0 for gain in information_gains]

# Print gain ratios for each feature
print("Gain ratios for each feature:")
for i, ratio in enumerate(gain_ratios):
    print("Feature", i, ":", ratio)

# Train a Decision Tree classifier
model = DecisionTreeClassifier(random_state=0)
model.fit(X_train, y_train)

# Evaluate the accuracy of the model on the training data
train_pred = model.predict(X_train)
train_accuracy = accuracy_score(y_train, train_pred)
print("Training Accuracy:", train_accuracy)

# Evaluate the accuracy of the model on the test data
test_pred = model.predict(X_test)
test_accuracy = accuracy_score(y_test, test_pred)
print("Test Accuracy:", test_accuracy)

import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

# Plot the decision tree
plt.figure(figsize=(20,10))
plot_tree(model, feature_names=X.columns, class_names=model.classes_, filled=True)
plt.show()

data.columns

