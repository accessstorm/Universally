from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import io  # To read InMemoryUploadedFile

from .forms import PredictorForm

@login_required
def predictor_view(request):
    """
    Handles CSV upload, Random Forest model training, and prediction display.
    """
    form = PredictorForm()
    results = None
    column_names = []  # To potentially populate feature selection later

    if request.method == 'POST':
        form = PredictorForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file: InMemoryUploadedFile = form.cleaned_data['csv_file']
            target_column = form.cleaned_data['target_column']
            test_size = form.cleaned_data['test_size']
            n_estimators = form.cleaned_data['n_estimators']
            max_depth = form.cleaned_data['max_depth']  # Can be None
            random_state = form.cleaned_data['random_state']

            try:
                # Read CSV data into pandas DataFrame
                # Use io.StringIO to read the in-memory file content
                file_content = csv_file.read().decode('utf-8')
                df = pd.read_csv(io.StringIO(file_content))
                column_names = df.columns.tolist()

                # --- Data Preprocessing ---
                if target_column not in df.columns:
                    raise ValueError(f"Target column '{target_column}' not found in the uploaded CSV.")

                # Drop rows with missing values (simple strategy)
                original_count = len(df)
                df.dropna(inplace=True)
                dropped_count = original_count - len(df)
                
                if df.empty:
                    raise ValueError("Dataset became empty after dropping rows with missing values.")
                
                if dropped_count > 0:
                    messages.warning(request, f"Dropped {dropped_count} rows with missing values.")

                # Separate features (X) and target (y)
                X = df.drop(columns=[target_column])
                y = df[target_column]

                # Check if target is categorical or numerical
                is_classification = y.dtype == 'object' or pd.api.types.is_categorical_dtype(y) or y.nunique() < 15  # Better heuristic

                # Handle categorical features (simple one-hot encoding)
                X = pd.get_dummies(X, drop_first=True)  # drop_first avoids multicollinearity
                
                if X.empty:
                    raise ValueError("After processing categorical features, no features remain. Check your data.")

                # Prepare target variable
                if is_classification:
                    # Encode target labels if classification
                    le = LabelEncoder()
                    y = le.fit_transform(y)
                    target_labels = le.classes_  # Store labels for display

                # --- Train/Test Split ---
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=test_size, random_state=random_state
                )

                # --- Model Training & Prediction ---
                if is_classification:
                    model = RandomForestClassifier(
                        n_estimators=n_estimators,
                        max_depth=max_depth,
                        random_state=random_state,
                        n_jobs=-1  # Use all available cores
                    )
                    model_type = "Classification"
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                    # Metrics
                    accuracy = accuracy_score(y_test, y_pred)
                    metrics = {'Accuracy': f"{accuracy:.4f}"}
                else:  # Regression
                    model = RandomForestRegressor(
                        n_estimators=n_estimators,
                        max_depth=max_depth,
                        random_state=random_state,
                        n_jobs=-1  # Use all available cores
                    )
                    model_type = "Regression"
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                    # Metrics
                    mse = mean_squared_error(y_test, y_pred)
                    r2 = r2_score(y_test, y_pred)
                    metrics = {'Mean Squared Error': f"{mse:.4f}", 'R-squared': f"{r2:.4f}"}

                # --- Prepare Results for Template ---
                # Limit results display to avoid huge tables
                max_results_display = 50
                
                # Convert to DataFrame first if they're numpy arrays to ensure proper indexing
                X_test_df = pd.DataFrame(X_test)
                y_test_series = pd.Series(y_test, index=X_test_df.index)
                y_pred_series = pd.Series(y_pred, index=X_test_df.index)
                
                # Get the indices we'll use for display
                sample_indices = X_test_df.index[:max_results_display]
                
                # Create a results DataFrame with just the samples we want
                results_df = X_test_df.loc[sample_indices].copy()
                
                # Add actual and predicted values
                if is_classification:
                    # Map numeric predictions back to labels
                    actual_values = pd.Series(le.inverse_transform(y_test_series.loc[sample_indices]), 
                                             index=sample_indices)
                    predicted_values = pd.Series(le.inverse_transform(y_pred_series.loc[sample_indices]), 
                                                index=sample_indices)
                else:
                    actual_values = y_test_series.loc[sample_indices]
                    predicted_values = y_pred_series.loc[sample_indices]
                
                results_df[f'Actual {target_column}'] = actual_values
                results_df[f'Predicted {target_column}'] = predicted_values

                # Format feature importances
                feature_importances = None
                if hasattr(model, 'feature_importances_'):
                    feature_importances = sorted(
                        zip(X.columns, model.feature_importances_), 
                        key=lambda x: x[1], 
                        reverse=True
                    )

                results = {
                    'model_type': model_type,
                    'metrics': metrics,
                    'predictions_html': results_df.to_html(
                        classes='table-auto w-full text-sm text-left text-gray-500 dark:text-gray-400', 
                        border=0,
                        float_format='%.4f'  # Format floats to 4 decimal places
                    ),
                    'feature_importances': feature_importances,
                    'num_results_shown': min(len(y_test), max_results_display),
                    'total_test_samples': len(y_test)
                }
                messages.success(request, "Prediction completed successfully!")

            except ValueError as ve:
                messages.error(request, f"Data Processing Error: {ve}")
            except pd.errors.EmptyDataError:
                messages.error(request, "The uploaded CSV file is empty or invalid.")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {e}")
                # Consider logging the full error traceback here for debugging
        else:
            messages.error(request, "Please correct the errors in the form.")

    context = {
        'form': form,
        'results': results,
        'column_names': column_names  # Pass column names for potential future use
    }
    return render(request, 'predictor/predictor_tool.html', context)