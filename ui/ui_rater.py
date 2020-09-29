import tkinter as tk
import config


class UIRater:

    def __init__(self, app_runner):
        self.app_runner = app_runner
        self.most_rated_movies = self.app_runner.loader.load_most_rated_movies(config.num_of_movies_for_client,
                                                                               shuffle=True)
        print(self.most_rated_movies)
        self.i_current_movie = 0
        self.current_movie = self.most_rated_movies.iloc[self.i_current_movie]

        # fonts
        self.movie_font = ("Courier", 38)
        self.button_font = ("Courier", 30)

        self.root = tk.Tk()
        self.root.title("Movie recommendation")

        # movie rating frame
        self.frm_rating = tk.Frame(master=self.root)
        self.frm_rating.pack()

        # label for movie names
        self.lbl_movie_title = tk.Label(master=self.frm_rating, text=self.current_movie["title"], width=30, height=5,
                                        bg="green", fg="white",
                                        font=self.movie_font)
        self.lbl_movie_title.pack(fill=tk.BOTH, expand=True)

        # bottom frame
        self.frm_bottom = tk.Frame(master=self.frm_rating, bg="white")
        self.frm_bottom.pack(fill=tk.BOTH)

        # bottom left frame
        self.frm_bottom_left = tk.Frame(master=self.frm_bottom, bg="blue", padx=50, pady=20)
        self.frm_bottom_left.grid(row=0, column=0, sticky="nsew")
        self.frm_bottom_left.rowconfigure(0, weight=1)
        self.frm_bottom_left.columnconfigure([0, 1, 2, 3, 4], minsize=100, weight=1)

        # rating buttons
        self.buttons = set()
        for i in range(5):
            button = tk.Button(master=self.frm_bottom_left,
                               text=str(i + 1),
                               bg="yellow", fg="blue",
                               font=self.button_font,
                               command=(lambda j=i + 1: self.handle_new_movie(rating=j))
                               )
            button.grid(row=0, column=i, sticky="nsew", padx=10, pady=30)
            self.buttons.add(button)

        # bottom right frame
        self.frm_bottom_right = tk.Frame(master=self.frm_bottom, bg="red")
        self.frm_bottom_right.grid(row=0, column=1, sticky="nsew")

        # skip button
        self.btn_skip = tk.Button(master=self.frm_bottom_right,
                                  text="Skip\nMovie",
                                  bg="yellow", fg="red",
                                  font=self.button_font,
                                  command=(lambda: self.handle_new_movie(skip_current=True))
                                  )
        self.btn_skip.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # recommend button
        self.btn_recommend = tk.Button(master=self.frm_bottom_right,
                                       text="Get\nRecommendation",
                                       bg="yellow", fg="red",
                                       font=self.button_font,
                                       command=self.init_recommendation()
                                       )
        self.btn_recommend.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # start UI
        self.root.mainloop()

    def handle_new_movie(self, rating=-1, skip_current=False):
        """
        Brings a new movie to the screen for the client to rate. If there are no movies left,
        initializes recommendation phase instead.

        If skip_current flag is set to False, then this is interpreted as a movie rating,
        and thus the rating is registered. The rating parameter should then be a value
        (1-5)

        If, however, skip_current flag is set to false, it only brings the next movie to the screen, ignoring
        the rating parameter.
        """
        if not skip_current:
            # register rating
            self.app_runner.user_rating.add_rating(self.current_movie.name, rating)

        self.i_current_movie += 1
        # if all movies has been rated, recommendation should now begin
        if self.i_current_movie >= config.num_of_movies_for_client:
            self.init_recommendation()
        else:
            # show next movie
            self.current_movie = self.most_rated_movies.iloc[self.i_current_movie]
            self.lbl_movie_title["text"] = self.current_movie["title"]

    def init_recommendation(self):
        pass
