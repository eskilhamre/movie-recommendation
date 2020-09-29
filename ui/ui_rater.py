import tkinter as tk


class UIRater:

    def __init__(self, app_runner):
        self.app_runner = app_runner
        self.most_rated_movies = self.app_runner.loader.load_most_rated_movies(100, shuffle=True)

        self.root = tk.Tk()
        self.root.title("Movie recommendation")

    def init_rating(self):
        self.root.mainloop()
