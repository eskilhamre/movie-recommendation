import tkinter as tk
from ui.frames import RatePage, RecommendPage


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
        """Show the frame corresponding to the page name"""
        frame = self.frames[page_name]
        frame.tkraise()

    def init_recommendation(self):
        """Performs the operations necessary to show the recommendation frame."""
        # disable all rate page buttons to avoid program crash
        rate_page_name = RatePage.__name__
        rate_page = self.frames[rate_page_name]
        rate_page.disable_buttons()

        # switch page
        recommend_page_name = RecommendPage.__name__
        recommend_page = self.frames[recommend_page_name]
        recommend_page.show_recommendations()
        self.show_frame(recommend_page_name)
