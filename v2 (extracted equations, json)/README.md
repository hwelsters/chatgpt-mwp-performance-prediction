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
- nltk            `3.8.1`
- pandas          `1.3.5`
- sympy           `1.10.1`
- plotly          `5.13.0`
- xgboost         `1.6.2`
- scikit-learn    `1.0.2`


Since ChatGPT gave us equations in a more consistent format, 
I can now throw the equations into Sympy to do cool stuff with it!

Cool stuff!
-   I solved the system of equations that ChatGPT provided and compared the solve answer to ChatGPT's final answer
    It's pretty promising! Major improvements across all classifiers (except maybe KMeans)