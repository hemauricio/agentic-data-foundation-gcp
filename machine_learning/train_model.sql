CREATE OR REPLACE MODEL `my_dataset.churn_prediction_model`
OPTIONS(
  model_type='logistic_reg',
  input_label_cols=['Churn']
) AS
SELECT MonthlyCharges, TotalCharges, tenure, Churn
FROM `my_dataset.telco_churn_analytics`;
