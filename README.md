<h1 align="left">
	ChatGPT MWP Performance Prediction
</h1>

<p align="left">
	<a href="https://github.com/hwelsters/chatgpt-mwp-performance-prediction/stargazers">
		<img alt="Stargazers" src="https://img.shields.io/github/stars/hwelsters/chatgpt-mwp-performance-prediction?style=for-the-badge"></a>
	<a href="https://github.com/hwelsters/chatgpt-mwp-performance-prediction/issues">
		<img alt="Issues" src="https://img.shields.io/github/issues/hwelsters/chatgpt-mwp-performance-prediction?style=for-the-badge"></a>
</p>

<h2 align="left">
	Abstract
</h2>

<p align="left">
	We study the performance of a commercially available large language model (LLM) known as ChatGPT on
	math word problems (MWPs) from the dataset DRAW-1K and ALG-514. 
	<br/>
	<br/>
	We also have released the dataset of ChatGPT’s responses to the MWPs to
	support further work on the characterization of LLM performance and present baseline machine learning
	models to predict if ChatGPT can correctly answer an MWP. We have released a dataset comprised of
	ChatGPT’s responses to support further research in this area.
</p>

Things to show:

This week, I compared how correct ChatGPT's equations are vs how correct its final answers answers in the JSON response.
Show excel sheets.

Another thing I did is this. Based on last week, we saw that asking ChatGPT to give us its answers in JSON form lets us compare its final answer with the answers I got from Sympy.
But one bad thing about it is that ChatGPT performs a lot worse.

Previously, I was using my own algorithm to extract equations from ChatGPT's response.
This time, I used ChatGPT to help me extract the equations and final answers from its response.
So, I just said something like 'Extract the equations and give it to me in JSON form' and I also asked it to extract the final answer.
Then, I used Sympy again and here are my results.
Show excel sheets.

I'm not sure why, but the ML models seem to be a lot better at predicting if ChatGPT's equations are correct. This might be because of the way I clean the equations though.

So in this, the solved equations perform a lot worse. But this might not be ChatGPT's fault. My method of cleaning the equations isn't 100% accurate. Especially when ChatGPT uses slight variations of the same word.

- JSON sympy solve. Equations do better than answers.
- Using ChatGPT to extract equations and the final answer. Answers do better than equations. This is likely my fault since my way of canonicalizing equations might not be accurate. For example, if ChatGPT used two different words to mean the same thing, my algorithm fails.
For example, car's distance = 1 + 2 vs distance of car = 1 + 2

- Probability of num of additions, num of subtractions
- 1: Prompt engineer best output, ask ChatGPT to extract equations in it. Additions, subtractions
- 2: Compare Sympy answer.
- 3: NEED TO SEE: If we can categorize things into 4 categories: SYMPY CORRECT, CHATGPT CORRECT, SYMPY CORRECT AND CHATGPT INCORRECT, SYMPY INCORRECT AND CHATGPT CORRECT, SYMPY INCORRECT AND CHATGPT INCORRECT.