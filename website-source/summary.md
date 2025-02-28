# Summary 

Our team set out to understand how people navigate and trust health information. Our goal of examining public trust, frustrations, and sentiment about healthcare and cancer information was met - below are our questions and conclusions based on the analysis from previous sections. 

## Project Approach 

Using our two data sources, Subreddits that mention cancer in comments and the Health Information National Trends Survey (HINTS), we were able to find a linkage between sentiment and many of the HINTS responses. 

## Question 1: Is Trust in the Healtchare System Influenced by Other Factors of Trust? 

Trust in scientists, religious institutions, the government, etc. might help us understand where individuals go and how they might feel when they are looking for medical advice or information related to cancer. After our analysis trying to predict Trust In Healthcare, we found that the XGBoost (Tuned) model was the best choice to predict Trust in Healthcare based on its highest accuracy (74%) and performance for High Trust in Healthcare. It had a strong recall of 90%. While this model still struggled with Low Trust in Healthcare, the improved overall performance makes it the most reliable model for the task at hand.

## Question 2: Doe Sentiment vary Between Cancer and Non-Cancer Subreddits? 

In order to investigate the sentiments and emotions in the Reddit data, the comments from cancer-related and non-cancer subreddits were loaded as Parquet files saved in an Azure Blob container. Using the Spark NLP analyze_sentiment pretrained pipeline, the comments were analyzed to classify their sentiment as positive, negative, or neutral. A custom function mapped sentiment labels to numerical scores (positive = 1, negative = -1, neutral = 0) to compute a weighted sentiment score for each comment. Comments were labeled based on their weighted scores (positive, negative, or neutral). The data was grouped by sentiment labels, and counts were computed for cancer-related and non-cancer subreddits. A Chi-square test was conducted to assess whether the differences in sentiment distribution between the two categories were statistically significant. Bar plots were created using Seaborn and Matplotlib to visualize sentiment distributions for cancer and non-cancer subreddit comments. Our biggest finding on this question was that cancer-related comments have a higher proportion of positive sentiment. 

## Question 3:What are the most frequently used words in Cancer Subreddits?  

This question was target to identify unique or prominent keywords and identify thematic differences in the text-based data. Two separate datasets were loaded: one for cancer-related subreddits and another for non-cancer subreddits. The datasets were combined into a single DataFrame with an additional column specifying the source (cancer or non_cancer). Text content was preprocessed into a column for TF-IDF analysis. Then, the TfidfVectorizer from scikit-learn was applied separately for cancer text data to compute TF-IDF scores for each word in the respective datasets. Standard procedures were followed (common stop words were removed, and the top 20 keywords were extracted based on their aggregated TF-IDF scores across all documents). Words were ranked in descending order of their total TF-IDF scores for the cancer dataset. Rankings allowed for the identification of keywords in the cancer dataset. A word cloud was created to display the rank of keywords, with the top two or three were "time" "removed" and "thank". 

## Question 4: Can we predict if a comment will be cancer related? 

In this question the Machine Learning concept was classifying cancer-related and non-cancer subreddits using machine learning (Naive Bayes and Logistic Regression). For our approach, we loaded cancer-related and non-cancer subreddit comments and added source column to label as cancer and non. Datasets were combined into a single frame. Text was tokenized and stop words removed, and tokens were converted into raw features using CountVectorizer. The TF-IDF scores were computed using the IDF transformer. Using PySpark ML, created a Naive Bayes and Logistic Regression pipeline with the preprocessing steps. Data was split (80/20) for train and test. 

Naive Bayes outperforms Logistic Regression in text classification

Naive Bayes: 

Multinomial Naive Bayes achieved test accuracy of 78%. 
* Precision: 78%
* Recall: 78%
* F1-Score: 78%
* AUC-ROC: 78%


Logistic Regression: 
Achieved test accuracy of 71%. 
* Precision: 71%
* Recall: 71%
* F1-Score: 71%
* AUC-ROC: 71%

As this was text data, it was a little unsurprising that Naive Bayes outperformed logistic regression. Though 78% is not the highest test accuracy, it is still a healthy setting above 50% (blind guess). 

# Takeaways: 

* Subreddits related to cancer revealed a range of emotions, including positivity, negativity, trust, fear, and sadness. These factors suggest that commenters experience complex and multifaceted emotions in their cancer journey.
* Reddit is used as a forum to discuss and look for cancer information with keywords, such as doctor, information, and contact.
* Healthcare professionals could use online forum formats to reach the sentiments of patients while researchers could use the data for patient-centered research.





