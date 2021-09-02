# Piezo Drum Test
# Testing with two piezo drums from a toy drum kit
# Using Adafruit Circuit Playground Express

import time
import board
import analogio
import digitalio

try:
    from audiocore import WaveFile
except ImportError:
    from audioio import WaveFile

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

bpm = 120  # Beats per minute, change this to suit your tempo

# Enable the speaker
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = True

audiofiles = ["elec_cymbal.wav", "elec_hi_snare.wav"]
analogpins = (board.A1, board.A2)
piezoThreshold = 30000  # Adjust this to make the drum pads more/less sensitive
audio = AudioOut(board.SPEAKER)
drumPad = []
for i in range(2):
    drumPad.append(analogio.AnalogIn(analogpins[i]))

def play_file(filename):
    print("playing file " + filename)
    file = open(filename, "rb")
    wave = WaveFile(file)
    audio.play(wave)
    time.sleep(bpm / 960)  # Sixteenth note delay

def getVoltage(pin):  # helper
    return (pin.value)

while True:
    for i in range(2):
        if getVoltage(drumPad[i]) > piezoThreshold:
            print(getVoltage(drumPad[i]))
            play_file(audiofiles[i])