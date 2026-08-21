import tkinter as tk
from tkinter import ttk, messagebox
from netmiko import ConnectHandler
import re
import threading
import time
from collections import deque


class CiscoBandwidthMonitor:

    def __init__(self, root):
        self.root = root
        self.root.title("Cisco Interface Bandwidth Monitor")
        self.root.geometry("950x700")

        self.running = False
        self.connection = None

        # Keep the last 60 measurements
        self.max_points = 60

        self.rx_history = deque(maxlen=self.max_points)
        self.tx_history = deque(maxlen=self.max_points)

        self.create_gui()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

    # --------------------------------------------------
    # GUI
    # --------------------------------------------------

    def create_gui(self):

        # Connection frame
        connection_frame = ttk.LabelFrame(
            self.root,
            text="Cisco Router SSH"
        )
        connection_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            connection_frame,
            text="Router IP:"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.ip_entry = ttk.Entry(
            connection_frame,
            width=18
        )
        self.ip_entry.insert(
            0,
            "192.168.1.1"
        )
        self.ip_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(
            connection_frame,
            text="Username:"
        ).grid(row=0, column=2, padx=5, pady=5)

        self.username_entry = ttk.Entry(
            connection_frame,
            width=15
        )
        self.username_entry.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        ttk.Label(
            connection_frame,
            text="Password:"
        ).grid(row=0, column=4, padx=5, pady=5)

        self.password_entry = ttk.Entry(
            connection_frame,
            width=15,
            show="*"
        )
        self.password_entry.grid(
            row=0,
            column=5,
            padx=5,
            pady=5
        )

        ttk.Label(
            connection_frame,
            text="Interface:"
        ).grid(row=1, column=0, padx=5, pady=5)

        self.interface_entry = ttk.Entry(
            connection_frame,
            width=18
        )
        self.interface_entry.insert(
            0,
            "GigabitEthernet0/0"
        )
        self.interface_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(
            connection_frame,
            text="Poll (seconds):"
        ).grid(row=1, column=2, padx=5, pady=5)

        self.interval_entry = ttk.Entry(
            connection_frame,
            width=15
        )
        self.interval_entry.insert(
            0,
            "5"
        )
        self.interval_entry.grid(
            row=1,
            column=3,
            padx=5,
            pady=5
        )

        # Buttons
        self.start_button = ttk.Button(
            connection_frame,
            text="Connect / Start",
            command=self.start
        )
        self.start_button.grid(
            row=1,
            column=4,
            padx=5,
            pady=5
        )

        self.stop_button = ttk.Button(
            connection_frame,
            text="Stop",
            command=self.stop,
            state="disabled"
        )
        self.stop_button.grid(
            row=1,
            column=5,
            padx=5,
            pady=5
        )

        # --------------------------------------------------
        # Bandwidth labels
        # --------------------------------------------------

        stats_frame = ttk.Frame(self.root)
        stats_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.rx_label = ttk.Label(
            stats_frame,
            text="RX: 0.00 Mbps",
            font=("Arial", 16),
            foreground="green"
        )
        self.rx_label.pack(
            side="left",
            expand=True
        )

        self.tx_label = ttk.Label(
            stats_frame,
            text="TX: 0.00 Mbps",
            font=("Arial", 16),
            foreground="blue"
        )
        self.tx_label.pack(
            side="left",
            expand=True
        )

        self.total_label = ttk.Label(
            stats_frame,
            text="Total: 0.00 Mbps",
            font=("Arial", 16)
        )
        self.total_label.pack(
            side="left",
            expand=True
        )

        # --------------------------------------------------
        # Graph
        # --------------------------------------------------

        graph_frame = ttk.LabelFrame(
            self.root,
            text="Live RX / TX Bandwidth"
        )
        graph_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.canvas = tk.Canvas(
            graph_frame,
            background="#111827",
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        self.canvas.bind(
            "<Configure>",
            lambda event: self.draw_graph()
        )

        # --------------------------------------------------
        # Status
        # --------------------------------------------------

        self.status_label = ttk.Label(
            self.root,
            text="Status: Disconnected"
        )
        self.status_label.pack(
            pady=5
        )

    # --------------------------------------------------
    # Start monitoring
    # --------------------------------------------------

    def start(self):

        if self.running:
            return

        try:
            interval = float(
                self.interval_entry.get()
            )

            if interval < 1:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid interval",
                "Poll interval must be at least 1 second."
            )
            return

        self.rx_history.clear()
        self.tx_history.clear()

        self.running = True

        self.start_button.config(
            state="disabled"
        )

        self.stop_button.config(
            state="normal"
        )

        thread = threading.Thread(
            target=self.monitor,
            daemon=True
        )

        thread.start()

    # --------------------------------------------------
    # SSH monitoring
    # --------------------------------------------------

    def monitor(self):

        router_ip = self.ip_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        interface = self.interface_entry.get().strip()

        try:

            self.update_status(
                "Connecting..."
            )

            device = {
                "device_type": "cisco_ios",
                "host": router_ip,
                "username": username,
                "password": password,
                "port": 22,
                "timeout": 10,
            }

            self.connection = ConnectHandler(
                **device
            )

            self.update_status(
                "Connected"
            )

            previous_rx = None
            previous_tx = None
            previous_time = None

            interval = float(
                self.interval_entry.get()
            )

            while self.running:

                command = (
                    f"show interfaces {interface}"
                )

                output = self.connection.send_command(
                    command
                )

                rx_bytes, tx_bytes = (
                    self.parse_interface(output)
                )

                if rx_bytes is None or tx_bytes is None:

                    self.update_status(
                        "Unable to read interface counters"
                    )

                    time.sleep(interval)
                    continue

                current_time = time.time()

                if previous_rx is not None:

                    elapsed = (
                        current_time -
                        previous_time
                    )

                    rx_mbps = self.calculate_mbps(
                        previous_rx,
                        rx_bytes,
                        elapsed
                    )

                    tx_mbps = self.calculate_mbps(
                        previous_tx,
                        tx_bytes,
                        elapsed
                    )

                    total_mbps = (
                        rx_mbps +
                        tx_mbps
                    )

                    self.root.after(
                        0,
                        self.add_measurement,
                        rx_mbps,
                        tx_mbps,
                        total_mbps
                    )

                previous_rx = rx_bytes
                previous_tx = tx_bytes
                previous_time = current_time

                time.sleep(interval)

        except Exception as e:

            self.update_status(
                f"Error: {e}"
            )

        finally:

            if self.connection:

                try:
                    self.connection.disconnect()
                except Exception:
                    pass

                self.connection = None

    # --------------------------------------------------
    # Parse Cisco interface output
    # --------------------------------------------------

    def parse_interface(self, output):

        rx_match = re.search(
            r"(\d+)\s+bytes input",
            output,
            re.IGNORECASE
        )

        tx_match = re.search(
            r"(\d+)\s+bytes output",
            output,
            re.IGNORECASE
        )

        if not rx_match or not tx_match:
            return None, None

        rx_bytes = int(
            rx_match.group(1)
        )

        tx_bytes = int(
            tx_match.group(1)
        )

        return rx_bytes, tx_bytes

    # --------------------------------------------------
    # Calculate Mbps
    # --------------------------------------------------

    def calculate_mbps(
        self,
        old_value,
        new_value,
        elapsed
    ):

        if elapsed <= 0:
            return 0

        difference = new_value - old_value

        # Counter rollover protection
        if difference < 0:
            difference += 2 ** 32

        bits_per_second = (
            difference * 8
        ) / elapsed

        return bits_per_second / 1_000_000

    # --------------------------------------------------
    # Add graph measurement
    # --------------------------------------------------

    def add_measurement(
        self,
        rx,
        tx,
        total
    ):

        self.rx_history.append(rx)
        self.tx_history.append(tx)

        self.rx_label.config(
            text=f"RX: {rx:.2f} Mbps"
        )

        self.tx_label.config(
            text=f"TX: {tx:.2f} Mbps"
        )

        self.total_label.config(
            text=f"Total: {total:.2f} Mbps"
        )

        self.draw_graph()

    # --------------------------------------------------
    # Draw graph
    # --------------------------------------------------

    def draw_graph(self):

        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width < 100 or height < 100:
            return

        # Margins
        left = 60
        right = 20
        top = 30
        bottom = 40

        graph_width = width - left - right
        graph_height = height - top - bottom

        # No data yet
        if not self.rx_history:
            self.canvas.create_text(
                width / 2,
                height / 2,
                text="Waiting for bandwidth data...",
                fill="white",
                font=("Arial", 14)
            )
            return

        # Determine Y-axis maximum
        max_value = max(
            max(self.rx_history, default=0),
            max(self.tx_history, default=0)
        )

        if max_value <= 0:
            max_value = 10

        # Add 20% headroom
        max_value *= 1.2

        # --------------------------------------------------
        # Grid
        # --------------------------------------------------

        grid_lines = 5

        for i in range(grid_lines + 1):

            y = (
                top +
                graph_height -
                (i / grid_lines) * graph_height
            )

            value = (
                max_value *
                i /
                grid_lines
            )

            self.canvas.create_line(
                left,
                y,
                width - right,
                y,
                fill="#374151"
            )

            self.canvas.create_text(
                left - 8,
                y,
                text=f"{value:.1f}",
                fill="#9CA3AF",
                anchor="e",
                font=("Arial", 9)
            )

        # --------------------------------------------------
        # Axis labels
        # --------------------------------------------------

        self.canvas.create_text(
            15,
            top,
            text="Mbps",
            fill="#D1D5DB",
            anchor="w",
            font=("Arial", 9)
        )

        # --------------------------------------------------
        # Draw RX
        # --------------------------------------------------

        self.draw_line(
            self.rx_history,
            left,
            top,
            graph_width,
            graph_height,
            max_value,
            "#22C55E"
        )

        # --------------------------------------------------
        # Draw TX
        # --------------------------------------------------

        self.draw_line(
            self.tx_history,
            left,
            top,
            graph_width,
            graph_height,
            max_value,
            "#3B82F6"
        )

        # --------------------------------------------------
        # Legend
        # --------------------------------------------------

        self.canvas.create_line(
            width - 170,
            15,
            width - 140,
            15,
            fill="#22C55E",
            width=3
        )

        self.canvas.create_text(
            width - 135,
            15,
            text="RX",
            fill="white",
            anchor="w"
        )

        self.canvas.create_line(
            width - 90,
            15,
            width - 60,
            15,
            fill="#3B82F6",
            width=3
        )

        self.canvas.create_text(
            width - 55,
            15,
            text="TX",
            fill="white",
            anchor="w"
        )

    # --------------------------------------------------
    # Draw individual line
    # --------------------------------------------------

    def draw_line(
        self,
        values,
        left,
        top,
        graph_width,
        graph_height,
        max_value,
        color
    ):

        if len(values) < 2:
            return

        points = []

        count = len(values)

        for i, value in enumerate(values):

            x = (
                left +
                (i / (self.max_points - 1))
                * graph_width
            )

            y = (
                top +
                graph_height -
                (value / max_value)
                * graph_height
            )

            points.extend([x, y])

        self.canvas.create_line(
            points,
            fill=color,
            width=2,
            smooth=True
        )

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    def update_status(self, text):

        self.root.after(
            0,
            lambda: self.status_label.config(
                text=f"Status: {text}"
            )
        )

    # --------------------------------------------------
    # Stop
    # --------------------------------------------------

    def stop(self):

        self.running = False

        self.start_button.config(
            state="normal"
        )

        self.stop_button.config(
            state="disabled"
        )

        self.update_status(
            "Stopped"
        )

    # --------------------------------------------------
    # Close application
    # --------------------------------------------------

    def on_close(self):

        self.running = False

        if self.connection:

            try:
                self.connection.disconnect()
            except Exception:
                pass

        self.root.destroy()


# ------------------------------------------------------
# Main
# ------------------------------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = CiscoBandwidthMonitor(root)

    root.mainloop()
