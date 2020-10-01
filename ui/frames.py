import tkinter as tk
from logic_ui_interface import interface as logic
from config import config

# fonts and color themes
main_message_font = ("Courier", 38)
button_font = ("Courier", 30)
movies_font = ("Courier", 12)
clr_bright = "#FEF9E0"
clr_light_green = "#94D5C0"
clr_dark_green = "#56796F"
clr_light_blue = "#36AAB4"
clr_dark_blue = "#1D5980"


class RatePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.i_current_movie = 0
        self.current_movie = logic.movies_to_be_rated.iloc[self.i_current_movie]

        self.frm_left = tk.Frame(master=self, bg=clr_dark_blue, padx=50, pady=20)
        self.frm_left.pack(side="left", fill=tk.BOTH, expand=True)
        self.frm_left.rowconfigure([0, 1], weight=1, minsize=250)

        self.frm_right = tk.Frame(master=self, bg=clr_bright, padx=50, pady=20)
        self.frm_right.pack(side="right", fill=tk.BOTH, expand=True)

        # label for movie names
        self.lbl_movie_title = tk.Label(master=self.frm_left, text=self.current_movie["title"],
                                        width=10, height=2,
                                        bg=clr_dark_blue, fg=clr_bright,
                                        font=main_message_font)
        self.lbl_movie_title.grid(row=0, column=0, sticky="nsew")

        # frame that contains rate buttons
        self.frm_rate_buttons = tk.Frame(master=self.frm_left, bg=clr_dark_blue, padx=0, pady=50)
        self.frm_rate_buttons.grid(row=1, column=0, sticky="nsew")
        self.frm_rate_buttons.rowconfigure(0, weight=1)
        self.frm_rate_buttons.columnconfigure([0, 1, 2, 3, 4], minsize=150, weight=1)

        # rating buttons
        self.buttons = set()
        for i in range(5):
            button = tk.Button(master=self.frm_rate_buttons,
                               text=str(i + 1),
                               bg=clr_light_green, fg=clr_dark_blue,
                               font=button_font,
                               command=(lambda j=i + 1: self.handle_new_movie(rating=j))
                               )
            button.grid(row=0, column=i, sticky="nsew", padx=15, pady=10)
            self.buttons.add(button)

        # skip button
        self.btn_skip = tk.Button(master=self.frm_right,
                                  text="Skip\nMovie",
                                  bg=clr_light_green, fg=clr_bright,
                                  font=button_font,
                                  command=(lambda: self.handle_new_movie(skip_current=True))
                                  )
        self.btn_skip.pack(side="bottom", fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.buttons.add(self.btn_skip)

        # recommend button
        self.btn_recommend = tk.Button(master=self.frm_right,
                                       text="Give me\nRecommendations",
                                       bg=clr_light_green, fg=clr_bright,
                                       font=button_font,
                                       command=self.controller.init_recommendation
                                       )
        self.btn_recommend.pack(side="bottom", fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.buttons.add(self.btn_recommend)

    def handle_new_movie(self, rating=-1, skip_current=False):
        """
        Brings a new movie to the screen for the client to rate. If there are no movies left,
        initializes recommendation phase instead.

        If skip_current flag is set to False, then this is interpreted as a movie rating,
        and thus the rating is registered. The rating parameter should then be a value
        (1-5)

        If, however, skip_current flag is set to False, it only brings the next movie to the screen, ignoring
        the rating parameter.
        """
        if not skip_current:
            # register rating
            logic.user_rating_handler.add_rating(self.current_movie.name, rating)

        self.i_current_movie += 1
        # if all movies has been rated, recommendation should now begin
        if self.i_current_movie >= config.num_of_movies_for_client:
            self.controller.init_recommendation()
        else:
            # show next movie
            self.current_movie = logic.movies_to_be_rated.iloc[self.i_current_movie]
            self.lbl_movie_title["text"] = self.current_movie["title"]

    def disable_buttons(self):
        for button in self.buttons:
            button["state"] = "disable"


class RecommendPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.lbl_recommended_message = tk.Label(master=self,
                                                text="Based on your ratings, I would\nrecommend the following movies:",
                                                width=30, height=5,
                                                bg=clr_dark_blue, fg=clr_bright,
                                                font=main_message_font
                                                )
        self.lbl_recommended_message.pack(fill=tk.BOTH, expand=True)
        self.frm_scroll_movies = ScrollableMovieFrame(self)
        self.frm_scroll_movies.pack(fill=tk.BOTH, expand=True)

    def show_recommendations(self):
        recommendations = logic.get_recommendation_results()
        self.frm_scroll_movies.populate(recommendations)


class ScrollableMovieFrame(tk.Frame):
    # class code heavily inspired by
    # https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter/3092341#3092341

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.bg_color = clr_dark_blue
        self.fg_color = clr_bright

        self.canvas = tk.Canvas(self, borderwidth=0, background=self.bg_color)
        self.frame = tk.Frame(self.canvas, background=self.bg_color)
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
                 bg=self.bg_color, fg=self.fg_color
                 ).grid(row=0, column=0)
        tk.Label(self.frame,
                 text="Movie Name",
                 width=60, borderwidth="1",
                 relief="solid",
                 font=movies_font,
                 bg=self.bg_color, fg=self.fg_color
                 ).grid(row=0, column=1)
        tk.Label(self.frame,
                 text="Recommendation Score",
                 width=20, borderwidth="1",
                 relief="solid",
                 font=movies_font,
                 bg=self.bg_color, fg=self.fg_color
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
                              bg=self.bg_color, fg=self.fg_color
                              )
            lbl_nr.grid(row=i, column=0)

            lbl_movie_name = tk.Label(self.frame,
                                      text=title,
                                      font=movies_font,
                                      bg=self.bg_color, fg=self.fg_color
                                      )
            lbl_movie_name.grid(row=i, column=1)

            lbl_score = tk.Label(self.frame,
                                 text=str(score)[:5],
                                 font=movies_font,
                                 bg=self.bg_color, fg=self.fg_color
                                 )
            lbl_score.grid(row=i, column=2)

            i += 1
