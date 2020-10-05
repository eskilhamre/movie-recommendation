# movie-recommendation
A simple movie recommendation program.

## Acknowlegdements
This program uses the small MovieLens dataset (100 000 ratings). My intentions of use is purely educational and non-commercial.
The dataset can be found here: [MovieLens Dataset](https://grouplens.org/datasets/movielens/)

## Requirements
Make sure you have Python installed on your computer, along with an IDE that supports Python. I use Python 3.8 and Pycharm.
Also, you need to have installed the following Python libraries: Pandas, Numpy, Scipy, Sklearn and Tkinter.

## How to run the program
First add the src/ folder to your PYTHONPATH. Then you can run the program from the
- *terminal*: Make sure your current directory is src/. Then type *python main.py*
- *IDE*: Open the project with src/ as root folder. Then run *main.py*

## Usage
The client is asked to rate (or skip) several movies on the scale 1-5. At any point the client may end the rating phase (by the clicking the 
"Give me recommendations" button), at which point the program will display a bunch of recommended movies based of off the clients ratings.

## Algorithmic description
The program uses a collaborative filtering approach combined with my own varaint of the k-nearest neighbor algorithm (I use
the cosine simularities between the vectors as a measure of distance.) The recommendation is based on a weighted
average of the ratings of the k-nearest neighbors (i.e. the k most similar ratings from the MovieLens dataset.)

## Future planned features
* At this point the program will recommend movies that the user already rated. I plan to filter out those movies.
* Find optimal k of the k-NN algorhtm by testing using MSE as the cost function.
* Let the client choose some other alternative to k-NN. The problem with k-NN is that the entire dataset must fit in memory.
I plan to explore K-means and DBScan. This would allow me to use even larger datasets, and probably perform much better.
