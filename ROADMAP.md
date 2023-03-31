Based on the ideas of a few attendees at AAAI MAKE.
- Asking ChatGPT to correct itself and then further gauging its performance.
- Study ChatGPT's nondeterminism
- Compare working correctness with solution correctness (in some cases, the working is correct while the solution is wrong or vice-versa)


Possible future ventures:
Fine-tuning a text-davinci-003 model to perform better on DRAW-1K. 
- Converting sentences to KG which could significantly simplify the dataset and allow us to shrink the dataset

- Creation of a dataset with numbers replaced with symbols instead
- Train-test-split 80:20. We are utilizing a small dataset at the moment simply as a POC since it is expensive to fine-tune OpenAI models on large datasets.
- If the results look promising, we could get a larger dataset.

TODO:
[] Ask ChatGPT to tag parts of response
[] HTML Tag extraction from ChatGPT
[] Limit equations on prompt
[] Clarifying answers
[] Tagging parts of response
[] NLP response tagging to improve prediction
[] Asking ChatGPT to correct itself and then further gauging its performance.

IDEA: We can beat state-of-the-art for ChatGPT