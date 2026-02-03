import sys
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFileDialog
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# ---------------- API URLs ----------------
API_URL = "http://localhost:8000/api/upload/"
HISTORY_URL = "http://localhost:8000/api/history/"


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(200, 200, 600, 600)

        layout = QVBoxLayout()

        # Title
        title = QLabel("Desktop App – Chemical Equipment Visualizer")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Labels
        self.status_label = QLabel("No file uploaded")
        self.summary_label = QLabel("")
        self.history_label = QLabel("")

        # Buttons
        upload_btn = QPushButton("Upload CSV")
        upload_btn.clicked.connect(self.upload_csv)

        history_btn = QPushButton("View Last 5 Uploads")
        history_btn.clicked.connect(self.load_history)

        # Matplotlib setup
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)

        # Layout order
        layout.addWidget(title)
        layout.addWidget(upload_btn)
        layout.addWidget(history_btn)
        layout.addWidget(self.status_label)
        layout.addWidget(self.summary_label)
        layout.addWidget(self.canvas)
        layout.addWidget(self.history_label)

        self.setLayout(layout)

    # ---------------- CSV Upload ----------------
    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)"
        )

        if not file_path:
            return

        self.status_label.setText("Uploading CSV to backend...")

        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                response = requests.post(API_URL, files=files)

            if response.status_code != 200:
                self.status_label.setText("Upload failed ❌")
                return

            data = response.json()
            summary = data["summary"]

            # Show summary
            summary_text = (
                f"Total Equipment: {summary['total_equipment']}\n"
                f"Avg Flowrate: {summary['average_flowrate']}\n"
                f"Avg Pressure: {summary['average_pressure']}\n"
                f"Avg Temperature: {summary['average_temperature']}"
            )

            self.status_label.setText("Upload successful ✅")
            self.summary_label.setText(summary_text)

            # Draw chart
            type_dist = summary["equipment_type_distribution"]

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.bar(type_dist.keys(), type_dist.values())
            ax.set_title("Equipment Type Distribution")
            ax.set_xlabel("Equipment Type")
            ax.set_ylabel("Count")

            self.canvas.draw()

        except Exception as e:
            self.status_label.setText("Backend error ❌")
            print("UPLOAD ERROR:", e)

    # ---------------- History ----------------
    def load_history(self):
        try:
            response = requests.get(HISTORY_URL)
            data = response.json()

            if not data:
                self.history_label.setText("No history found")
                return

            text = "Last 5 Uploads:\n\n"
            for d in data:
                summary = d["summary"]
                text += (
                    f"- {d['uploaded_at']}\n"
                    f"  Total Equipment: {summary['total_equipment']}\n\n"
                )

            self.history_label.setText(text)

        except Exception as e:
            self.history_label.setText("History error ❌")
            print("HISTORY ERROR:", e)


# ---------------- App Entry ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

