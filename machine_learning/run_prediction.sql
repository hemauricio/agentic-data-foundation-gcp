SELECT 
  hashed_customerID, 
  predicted_Churn, 
  predicted_Churn_probs
FROM ML.PREDICT(
  MODEL `my_dataset.churn_prediction_model`,
  (SELECT * FROM `my_dataset.telco_churn_analytics` LIMIT 10)
);
