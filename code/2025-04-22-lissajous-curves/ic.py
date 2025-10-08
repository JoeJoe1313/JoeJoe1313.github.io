import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider


class LissajousDashboard:
    def __init__(self):
        # Set up the figure and subplots
        self.fig = plt.figure(figsize=(12, 10))
        self.ax = self.fig.add_subplot(111)
        plt.subplots_adjust(left=0.1, bottom=0.3)

        # Initial parameter values
        self.a_init = 3
        self.b_init = 2
        self.delta_init = np.pi / 4
        self.num_points = 1000
        self.trace_length = 200

        # Animation control
        self.animation_running = False
        self.anim = None
        self.t = 0  # Time parameter

        # Set up plot
        self.setup_plot()

        # Create sliders
        self.create_sliders()

        # Create buttons
        self.create_buttons()

        # Plot initial curve
        self.update_static_curve(None)

    def setup_plot(self):
        """Set up the plot appearance"""
        self.ax.set_xlim(-1.1, 1.1)
        self.ax.set_ylim(-1.1, 1.1)
        self.ax.grid(True)
        self.ax.set_aspect("equal")
        self.ax.set_title(
            f"Lissajous Curve (a={self.a_init}, b={self.b_init}, δ={self.delta_init:.2f})"
        )
        self.ax.set_xlabel("x = sin(a·t + δ)")
        self.ax.set_ylabel("y = sin(b·t)")

        # Create a line object for the static curve
        (self.line,) = self.ax.plot([], [], "b-", lw=1.5)

        # Create a point object for the animation
        (self.point,) = self.ax.plot([], [], "ro", markersize=8)

        # Create a line for the trace
        (self.trace,) = self.ax.plot([], [], "r-", lw=1, alpha=0.5)
        self.trace_history_x = []
        self.trace_history_y = []

    def create_sliders(self):
        """Create parameter sliders"""
        # Create axes for sliders
        ax_a = plt.axes([0.1, 0.2, 0.65, 0.03])
        ax_b = plt.axes([0.1, 0.15, 0.65, 0.03])
        ax_delta = plt.axes([0.1, 0.1, 0.65, 0.03])
        ax_trace = plt.axes([0.1, 0.05, 0.65, 0.03])

        # Create sliders
        self.slider_a = Slider(ax_a, "a", 1, 10, valinit=self.a_init, valstep=0.1)
        self.slider_b = Slider(ax_b, "b", 1, 10, valinit=self.b_init, valstep=0.1)
        self.slider_delta = Slider(
            ax_delta, "δ", 0, 2 * np.pi, valinit=self.delta_init, valstep=np.pi / 12
        )
        self.slider_trace = Slider(
            ax_trace, "Trace Length", 10, 500, valinit=self.trace_length, valstep=10
        )

        # Register update functions
        self.slider_a.on_changed(self.update_static_curve)
        self.slider_b.on_changed(self.update_static_curve)
        self.slider_delta.on_changed(self.update_static_curve)
        self.slider_trace.on_changed(self.update_trace_length)

    def create_buttons(self):
        """Create control buttons"""
        # Create axes for buttons
        ax_anim = plt.axes([0.8, 0.2, 0.15, 0.05])
        ax_reset = plt.axes([0.8, 0.1, 0.15, 0.05])

        # Create buttons
        self.button_anim = Button(ax_anim, "Start Animation")
        self.button_reset = Button(ax_reset, "Reset")

        # Register update functions
        self.button_anim.on_clicked(self.toggle_animation)
        self.button_reset.on_clicked(self.reset)

    def update_static_curve(self, val):
        """Update the static curve when parameters change"""
        # Get current parameter values
        a = self.slider_a.val
        b = self.slider_b.val
        delta = self.slider_delta.val

        # Generate new curve data
        t = np.linspace(0, 2 * np.pi, self.num_points)
        x = np.sin(a * t + delta)
        y = np.sin(b * t)

        # Update the line data
        self.line.set_data(x, y)

        # Update title with frequency ratio
        ratio = a / b if b != 0 else float("inf")
        self.ax.set_title(
            f"Lissajous Curve (a={a:.1f}, b={b:.1f}, δ={delta:.2f}, ratio={ratio:.2f})"
        )

        # Redraw the canvas
        self.fig.canvas.draw_idle()

        # Reset trace history if animation is running
        self.trace_history_x = []
        self.trace_history_y = []
        self.trace.set_data([], [])

    def update_trace_length(self, val):
        """Update the trace length"""
        self.trace_length = int(self.slider_trace.val)

        # Trim trace history if needed
        if len(self.trace_history_x) > self.trace_length:
            self.trace_history_x = self.trace_history_x[-self.trace_length :]
            self.trace_history_y = self.trace_history_y[-self.trace_length :]
            self.trace.set_data(self.trace_history_x, self.trace_history_y)
            self.fig.canvas.draw_idle()

    def animate(self, frame):
        """Animation update function"""
        # Get current parameter values
        a = self.slider_a.val
        b = self.slider_b.val
        delta = self.slider_delta.val

        # Update time parameter
        self.t += 0.02

        # Calculate new position
        x = np.sin(a * self.t + delta)
        y = np.sin(b * self.t)

        # Update point position
        self.point.set_data([x], [y])

        # Update trace history
        self.trace_history_x.append(x)
        self.trace_history_y.append(y)

        # Limit trace length
        if len(self.trace_history_x) > self.trace_length:
            self.trace_history_x.pop(0)
            self.trace_history_y.pop(0)

        # Update trace line
        self.trace.set_data(self.trace_history_x, self.trace_history_y)

        return self.point, self.trace

    def toggle_animation(self, event):
        """Toggle animation on/off"""
        if not self.animation_running:
            # Start animation
            self.anim = animation.FuncAnimation(
                self.fig, self.animate, interval=30, blit=True
            )
            self.button_anim.label.set_text("Stop Animation")
            self.animation_running = True
        else:
            # Stop animation
            if self.anim is not None:
                self.anim.event_source.stop()
                self.anim = None
            self.button_anim.label.set_text("Start Animation")
            self.animation_running = False
        self.fig.canvas.draw_idle()

    def reset(self, event):
        """Reset all parameters to initial values"""
        # Stop animation if running
        if self.animation_running:
            self.toggle_animation(None)

        # Reset sliders
        self.slider_a.set_val(self.a_init)
        self.slider_b.set_val(self.b_init)
        self.slider_delta.set_val(self.delta_init)
        self.slider_trace.set_val(self.trace_length)

        # Reset trace
        self.trace_history_x = []
        self.trace_history_y = []
        self.trace.set_data([], [])
        self.point.set_data([], [])
        self.t = 0

        # Update plot
        self.update_static_curve(None)

    def show(self):
        """Display the dashboard"""
        plt.show()


# Create and show the dashboard
if __name__ == "__main__":
    dashboard = LissajousDashboard()
    dashboard.show()
