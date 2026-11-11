SELECT * FROM ML.EVALUATE(
  MODEL `my_dataset.churn_prediction_model`,
  (SELECT MonthlyCharges, TotalCharges, tenure, Churn FROM `my_dataset.telco_churn_analytics`)
);
