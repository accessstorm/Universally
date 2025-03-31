from django import forms

class PredictorForm(forms.Form):
    """
    Form for uploading a CSV file and configuring the Random Forest prediction.
    """
    csv_file = forms.FileField(
        label='Upload CSV File',
        help_text='Upload the dataset for prediction.',
        widget=forms.ClearableFileInput(attrs={'accept': '.csv'})
    )
    target_column = forms.CharField(
        label='Target Column Name',
        help_text='Enter the exact name of the column you want to predict.',
        max_length=100
    )
    # Feature columns could be dynamically populated later, start with target only
    # feature_columns = forms.MultipleChoiceField(
    #     label='Feature Columns',
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple,
    #     help_text='Select columns to use as features (optional, uses all others if blank).'
    # )
    test_size = forms.FloatField(
        label='Test Set Size (Fraction)',
        min_value=0.1,
        max_value=0.9,
        initial=0.25,
        help_text='Fraction of the data to use for the test set (e.g., 0.25 for 25%).'
    )
    n_estimators = forms.IntegerField(
        label='Number of Trees (n_estimators)',
        min_value=10,
        max_value=500,
        initial=100,
        help_text='Number of trees in the Random Forest.'
    )
    max_depth = forms.IntegerField(
        label='Maximum Tree Depth (max_depth)',
        min_value=1,
        required=False, # Make optional, None means nodes expand until pure
        help_text='Maximum depth of each tree (optional).'
    )
    random_state = forms.IntegerField(
        label='Random State',
        initial=42,
        help_text='Seed for reproducibility.'
    )

    def clean_csv_file(self):
        """
        Validate the uploaded file type.
        """
        file = self.cleaned_data.get('csv_file')
        if file:
            if not file.name.endswith('.csv'):
                raise forms.ValidationError("File must be a CSV.")
        return file
