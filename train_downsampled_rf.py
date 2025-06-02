import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data/downsampled.csv", parse_dates=['startDate', 'endDate'])
df['value'] = pd.to_numeric(df['value'], errors='coerce')
df['duration_sec'] = (df['endDate'] - df['startDate']).dt.total_seconds()
df['hour'] = df['startDate'].dt.hour
df.dropna(subset=['value', 'duration_sec', 'hour', 'person']) 

# Encode labels
le = LabelEncoder()
df['person_encoded'] = le.fit_transform(df['person']) 

# Features & Target
X = df[['value', 'duration_sec', 'hour']]
y = df['person_encoded']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y # Stratified split to maintain class distribution
)

# Scale
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test) 

# Train model
clf = RandomForestClassifier(
    n_estimators=100,
    max_depth=100,
    min_samples_split=20,
    min_samples_leaf=2,
    max_features='sqrt', 
    class_weight='balanced', # Handle class imbalance
    random_state=42,
    n_jobs=-1
)

# Evaluate with cross-validation
cv_scores = cross_val_score(clf, X_train, y_train, cv=5, scoring='accuracy')
print(f"Cross-Validation Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print("Classification Report for Downsampled:")
print(classification_report(y_test, y_pred, target_names=le.classes_)) 

# Confusion matrix
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt="d",
            xticklabels=le.classes_, yticklabels=le.classes_, cmap="Blues") 
plt.title("Confusion Matrix - Downsampled")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("visualisations/downsample_cfmatrix.pdf") 

plt.show()
plt.close()