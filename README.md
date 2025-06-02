# health-data-classifier

## Output of extract_data.py
Exported 224397 records to 'data/shlok.csv' with person='shlok'.
Exported 5063078 records to 'data/akhil.csv' with person='akhil'.
Combined both CSVs into 'data/raw_data.csv'

## Output of process_data.py
Exported 224397 records to 'data/downsampled.csv' with person='shlok'.
Exported 224397 records to 'data/downsampled.csv' with person='akhil'.

## Result of Downsampled Random Forest model
Classification Report for Downsampled: (First Model)
              precision    recall  f1-score   support

       akhil       0.69      0.69      0.69     44880
       shlok       0.69      0.70      0.69     44879

    accuracy                           0.69     89759
   macro avg       0.69      0.69      0.69     89759
weighted avg       0.69      0.69      0.69     89759

Cross-Validation Accuracy: 0.7172 ± 0.0007
Classification Report for Downsampled:
              precision    recall  f1-score   support

       akhil       0.72      0.72      0.72     44880
       shlok       0.72      0.72      0.72     44879

    accuracy                           0.72     89759
   macro avg       0.72      0.72      0.72     89759
weighted avg       0.72      0.72      0.72     89759

The data is hidden because of privacy reasons and will only be used to train the model. 