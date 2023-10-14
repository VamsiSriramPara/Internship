import sys
import os
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import sounddevice as sd
import numpy as np
import wave

class VoiceRecorder(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.audio_stream = None
        self.recording = False
        self.frames = []
        self.sample_rate = 44100

    def init_ui(self):
        self.setWindowTitle("Voice Recorder")
        self.setGeometry(100, 100, 400, 200)

        self.start_btn = QtWidgets.QPushButton("Start")
        self.stop_btn = QtWidgets.QPushButton("Stop")
        self.save_btn = QtWidgets.QPushButton("Save Recording")

        self.start_btn.clicked.connect(self.start_recording)
        self.stop_btn.clicked.connect(self.stop_recording)
        self.save_btn.clicked.connect(self.save_recording)

        self.status_label = QtWidgets.QLabel("Status: Not Recording")

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.start_btn)
        vbox.addWidget(self.stop_btn)
        vbox.addWidget(self.save_btn)
        vbox.addWidget(self.status_label)

        self.setLayout(vbox)

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.status_label.setText("Status: Recording")
            self.frames = []
            self.audio_stream = sd.InputStream(callback=self.audio_callback)
            self.audio_stream.start()

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.audio_stream.stop()
            self.audio_stream.close()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(f"Error in audio callback: {status}")
            return
        if self.recording:
            self.frames.append(indata.copy())

    def save_recording(self):
        if len(self.frames) == 0:
            QtWidgets.QMessageBox.warning(self, "Warning", "No recording to save.")
            return

        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        file_dialog.setNameFilter("Wave Files (*.wav)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            with wave.open(file_path, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(self.sample_rate)
                wf.writeframes(b"".join(self.frames))
            QtWidgets.QMessageBox.information(self, "Success", "Recording saved successfully.")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    recorder = VoiceRecorder()
    recorder.show()
    sys.exit(app.exec_())
