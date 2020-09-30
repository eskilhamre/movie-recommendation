import tkinter as tk
from config import config
from data_processing.data_load import DataLoader
from recommendation.recommend_movies import MovieRecommender
from data_processing.user_rating import UserRatingHandler

# all logic we need to connect the recommender algorithm to the UI
loader = DataLoader()
recommender = MovieRecommender(loader)
user_rating_handler = UserRatingHandler(loader.load_movies_with_rating_threshold())
movies_to_be_rated = loader.load_most_rated_movies(config.num_of_movies_for_client, shuffle=True)


def get_recommendation_results():
    client_ratings = user_rating_handler.get_processed_ratings()
    return recommender.recommend(client_ratings, n_recommendations=config.num_of_recommendations_for_client)


# fonts and themes
main_message_font = ("Courier", 38)
button_font = ("Courier", 30)
movies_font = ("Courier", 12)


class MovieRaterApp(tk.Tk):
    """
    this tkinter code structure is heavily inspired by Bryan Oakley's answer on
    https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
    """

    def __init__(self, *args, **kvargs):
        tk.Tk.__init__(self, *args, **kvargs)
        self.title("Movie recommendation")
        frame_classes = (RatePage, RecommendPage)  # all the page classes
        first_page_name = RatePage.__name__  # name of first page to be shown in UI

        # the container is the stack of frames. The one we want visible is raised above the others
        container = tk.Frame(master=self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = dict()  # key: frame name, val: frame instance
        for FrameClass in frame_classes:
            page_name = FrameClass.__name__
            frame_instance = FrameClass(parent=container, controller=self)
            self.frames[page_name] = frame_instance

            # put all of the pages in the same location; only one will be visible
            frame_instance.grid(row=0, column=0, sticky="nsew")

        self.show_frame(first_page_name)

    def show_frame(self, page_name):
        """
        Show the frame corresponding to the page name
        """
        frame = self.frames[page_name]
        frame.tkraise()

    def init_recommendation(self):
        recommender_page_name = RecommendPage.__name__
        recommender_page = self.frames[recommender_page_name]
        recommender_page.show_recommendations()
        self.show_frame(recommender_page_name)


class RatePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.i_current_movie = 0
        self.current_movie = movies_to_be_rated.iloc[self.i_current_movie]

        # label for movie names
        self.lbl_movie_title = tk.Label(master=self, text=self.current_movie["title"], width=30, height=5,
                                        bg="green", fg="white",
                                        font=main_message_font)
        self.lbl_movie_title.pack(fill=tk.BOTH, expand=True)

        # bottom frame
        self.frm_bottom = tk.Frame(master=self, bg="white")
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
                               font=button_font,
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
                                  font=button_font,
                                  command=(lambda: self.handle_new_movie(skip_current=True))
                                  )
        self.btn_skip.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # recommend button
        self.btn_recommend = tk.Button(master=self.frm_bottom_right,
                                       text="Get\nRecommendation",
                                       bg="yellow", fg="red",
                                       font=button_font,
                                       command=self.controller.init_recommendation
                                       )
        self.btn_recommend.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

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
            user_rating_handler.add_rating(self.current_movie.name, rating)

        self.i_current_movie += 1
        # if all movies has been rated, recommendation should now begin
        if self.i_current_movie >= config.num_of_movies_for_client:
            self.controller.init_recommendation()
        else:
            # show next movie
            self.current_movie = movies_to_be_rated.iloc[self.i_current_movie]
            self.lbl_movie_title["text"] = self.current_movie["title"]


class RecommendPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.lbl_recommended_message = tk.Label(master=self,
                                                text="Based on your ratings, I would\nrecommend the following movies:",
                                                width=30, height=5,
                                                bg="green", fg="white",
                                                font=main_message_font
                                                )
        self.lbl_recommended_message.pack(fill=tk.BOTH, expand=True)
        self.frm_scroll_movies = ScrollableMovieFrame(self)
        self.frm_scroll_movies.pack(fill=tk.BOTH, expand=True)

    def show_recommendations(self):
        recommendations = get_recommendation_results()
        self.frm_scroll_movies.populate(recommendations)


class ScrollableMovieFrame(tk.Frame):
    # class code heavily inspired by
    # https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter/3092341#3092341

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.on_frame_configure)

        # heading to scrollbar
        tk.Label(self.frame,
                 text="Nr.",
                 width=3, borderwidth="1",
                 relief="solid",
                 font=movies_font,
                 bg="green", fg="white"
                 ).grid(row=0, column=0)
        tk.Label(self.frame,
                 text="Movie Name",
                 width=60, borderwidth="1",
                 relief="solid",
                 font=movies_font,
                 bg="green", fg="white"
                 ).grid(row=0, column=1)
        tk.Label(self.frame,
                 text="Relative Score",
                 width=20, borderwidth="1",
                 relief="solid",
                 font=movies_font,
                 bg="green", fg="white"
                 ).grid(row=0, column=2)

    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def populate(self, recommendation):
        """Put the recommendation result into the scrollable frame"""

        i = 1
        for movie_id, (title, score) in recommendation.iterrows():
            lbl_nr = tk.Label(self.frame,
                              text=str(i),
                              width=3, borderwidth="5",
                              font=movies_font,
                              bg="green", fg="white"
                              )
            lbl_nr.grid(row=i, column=0)

            lbl_movie_name = tk.Label(self.frame,
                                      text=title,
                                      font=movies_font,
                                      bg="green", fg="white"
                                      )
            lbl_movie_name.grid(row=i, column=1)

            lbl_score = tk.Label(self.frame,
                                 text=str(score),
                                 font=movies_font,
                                 bg="green", fg="white"
                                 )
            lbl_score.grid(row=i, column=2)

            i += 1


if __name__ == "__main__":
    app = MovieRaterApp()  # root
    app.mainloop()
