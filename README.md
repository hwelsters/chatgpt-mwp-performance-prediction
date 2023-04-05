# Predicting ChatGPT's success in solving math word problems

<p align="left">
	<a href="https://github.com/hwelsters/sleepyask/stargazers">
		<img alt="Stargazers" src="https://img.shields.io/github/stars/hwelsters/improved-octo-happiness?style=for-the-badge"></a>
	<a href="https://github.com/hwelsters/sleepyask/issues">
		<img alt="Issues" src="https://img.shields.io/github/issues/hwelsters/improved-octo-happiness?style=for-the-badge"></a>
</p>

## Prerequisites
- Docker  
- Python `v3.7.9`

**Pip packages**
- nltk          `v3.8.1`
- pandas        `1.3.5`
- xlsxwriter    `3.0.9`
- scikit-learn  `1.0.2`
- xgboost       `1.6.2`

## Running the program in a Docker container
- We use Docker to produce results that can easily be reproduced on any computer
- The program will output files into a folder with the following file path: `$(base_directory)/output`. If the folder doesn't exist yet, create it  
- Write one of the following from the base folder to run the program:

```bash
# Using Docker Compose:
> docker compose up
> docker-compose up

# Using just the Docker CLI
> docker build -t math_prediction .
  docker run \
  --name math_prediction \
  -v "$(pwd)"/src:/app/src:ro \
  -v "$(pwd)"/input:/app/input:ro \
  -v "$(pwd)"/output:/app/output math_prediction
```

- The first run might take a while but the next few runs should be a lot faster.