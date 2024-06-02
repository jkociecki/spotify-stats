import numpy as np
import matplotlib.pyplot as plt
from math import pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk


def create_radar_chart(ax, categories, values, color='lightblue'):
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
    def __init__(self, parent, categories, values):
        super().__init__(parent)
        self.categories = categories
        self.values = values

        self.frame = ctk.CTkFrame(self, corner_radius=10)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_chart()

    def create_chart(self):
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
        if self.selected_point is None or event.inaxes != self.ax:
            return

        new_radius = min(max(event.ydata, 0), 1)
        self.values[self.selected_point] = new_radius
        create_radar_chart(self.ax, self.categories, self.values)
        self.canvas.draw_idle()

    def on_release(self, event):
        self.selected_point = None

    def get_current_state(self):
        return zip(self.categories, self.values)
