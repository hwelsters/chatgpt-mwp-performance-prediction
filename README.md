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
- nltk `v3.8.1`

## Running the program in a Docker container
- The program will output files into a folder named `output`. If the folder doesn't exist yet, create it  
- Write one of the following from the base folder to run the program:

```bash
# Using Docker Compose:
> 	docker compose up --build
> 	docker-compose up --build

# Using just the Docker CLI
> 	docker build -t math_prediction .
	docker run \
	--name math_prediction \
	-v "$(pwd)"/src:/app/src:ro \
	-v "$(pwd)"/input:/app/input:ro \
	-v "$(pwd)"/output:/app/output math_prediction
```
