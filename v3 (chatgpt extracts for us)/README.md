# Predicting ChatGPT's success in solving math word problems

<p align="left">
	<a href="https://github.com/hwelsters/chatgpt-mwp-performance-prediction/stargazers">
		<img alt="Stargazers" src="https://img.shields.io/github/stars/hwelsters/chatgpt-mwp-performance-prediction?style=for-the-badge"></a>
	<a href="https://github.com/hwelsters/chatgpt-mwp-performance-prediction/issues">
		<img alt="Issues" src="https://img.shields.io/github/issues/hwelsters/chatgpt-mwp-performance-prediction?style=for-the-badge"></a>
</p>

## Prerequisites
- Python `v3.7.9`

**Pip packages**
- pandas          `1.3.5`
- sympy           `1.10.1`
- xgboost         `1.6.2`
- scikit-learn    `1.0.2`


We saw from our previous experiments that ChatGPT does a lot worse when it gives answers in JSON form.
So instead, we do the following:

1. Ask ChatGPT for its response.
2. Ask ChatGPT to extract equations from the response
3. Ask ChatGPT to extract final answers from the response

Cool stuff!
-   I solved the system of equations that ChatGPT provided and compared the solve answer to ChatGPT's final answer
    It's pretty promising! Major improvements across all classifiers (except maybe KMeans)