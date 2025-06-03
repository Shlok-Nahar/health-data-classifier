# Health Data Classifier

This project builds a machine learning model to classify health data between two individuals: Shlok and Akhil.

---

## Data Processing Pipeline

### Output of `extract_data.py`
```
Exported 224,397 records to 'data/shlok.csv' with person='shlok'.
Exported 5,063,078 records to 'data/akhil.csv' with person='akhil'.
Combined both CSVs into 'data/raw_data.csv'.
```

### Output of `process_data.py`
```
Exported 224,397 records to 'data/downsampled.csv' with person='shlok'.
Exported 224,397 records to 'data/downsampled.csv' with person='akhil'.
```

---

## Model Performance (Random Forest Classifier on Downsampled Data)

### First Model (Initial Run)
```
Classification Report:
              precision    recall  f1-score   support

       akhil       0.69      0.69      0.69     44,880
       shlok       0.69      0.70      0.69     44,879

    accuracy                           0.69     89,759
   macro avg       0.69      0.69      0.69     89,759
weighted avg       0.69      0.69      0.69     89,759
```

---

### Improved Model (After (Attempted) Parameter Tuning)
```
Cross-Validation Accuracy: 0.7172 ± 0.0007

Classification Report:
              precision    recall  f1-score   support

       akhil       0.72      0.72      0.72     44,880
       shlok       0.72      0.72      0.72     44,879

    accuracy                           0.72     89,759
   macro avg       0.72      0.72      0.72     89,759
weighted avg       0.72      0.72      0.72     89,759
```

---

The data is hidden because of privacy reasons and was only used to train the model. 
