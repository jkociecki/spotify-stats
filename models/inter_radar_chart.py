import numpy as np
import matplotlib.pyplot as plt
from math import pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk


def create_radar_chart(ax, categories, values, color='lightblue'):
    """
    Create radar chart with given categories and values
    :param ax: plot axis object
    :param categories: list of categories to display, corresponding to the values
    :param values: numerical values for each category
    :param color: color of the radar chart
    :return: created radar chart
    """
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    ax.clear()
    ax.set_facecolor('#2e2e2e')
    ax.figure.set_facecolor('#2e2e2e')
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10, color='white')

    ax.set_rlabel_position(0)
    ax.set_yticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    ax.set_yticklabels(["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1"], color="grey", size=7)
    ax.set_ylim(0, 1)

    values = values + values[:1]
    ax.plot(angles, values, linewidth=2, linestyle='solid', color=color, marker='o')
    ax.fill(angles, values, color, alpha=0.25)

    return ax


class RadarChartFrame(ctk.CTkFrame):
    """
    Radar chart frame for displaying and interacting with radar charts
    """
    def __init__(self, parent, categories, values):
        """
        Initialize RadarChartFrame
        :param parent: parent frame for the radar chart
        :param categories: categories to display on the radar chart
        :param values: values for each category
        """
        super().__init__(parent)
        self.categories = categories
        self.values = values
        self.frame = ctk.CTkFrame(self, corner_radius=10)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.create_chart()

    def create_chart(self):
        """
        Create radar chart, place it in canvas
        setup event listeners for interaction
        :return: interactive radar chart
        """

        self.fig, self.ax = plt.subplots(subplot_kw={'polar': True})
        create_radar_chart(self.ax, self.categories, self.values)

        # Integrate Matplotlib figure with Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.selected_point = None

    def on_click(self, event):
        """
        Handle click event on radar chart
        Choose the closest point to the click event with a tolerance radius
        :param event: on click event
        :return: None
        """
        if event.inaxes != self.ax:
            return

        # Find the closest point to the click event
        distances = []
        for line in self.ax.lines:
            for x, y in zip(line.get_xdata(), line.get_ydata()):
                distances.append(np.sqrt((x - event.xdata) ** 2 + (y - event.ydata) ** 2))

        if distances:
            closest_point_idx = np.argmin(distances) % len(self.categories)
            # Check if the click was close enough to a point (tolerance radius)
            if distances[closest_point_idx] < 0.05:
                self.selected_point = closest_point_idx

    def on_motion(self, event):
        """
        Handle motion event on radar chart
        Change the value of the selected point based on the y coordinate of the event
        :param event: motion of the mouse
        :return: None
        """
        if self.selected_point is None or event.inaxes != self.ax:
            return

        new_radius = min(max(event.ydata, 0), 1)
        self.values[self.selected_point] = new_radius
        create_radar_chart(self.ax, self.categories, self.values)
        self.canvas.draw_idle()

    def on_release(self, event):
        """
        Handle release event on radar chart
        Reset the selected point to None
        :param event: release of the mouse click
        :return: None
        """
        self.selected_point = None

    def get_current_state(self):
        """
        Get the current state of the radar chart
        :return: categories and values
        """
        return zip(self.categories, self.values)
