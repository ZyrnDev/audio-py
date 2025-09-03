import sys
import math
import itertools
from notes import note_frequencies

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <output.wav>")

    filename = sys.argv[1]

    beats_per_minute = 120
    beat_duration = 60 / beats_per_minute # seconds per beat
    quaver_duration = beat_duration / 2
    crochet_duration = beat_duration
    minim_duration = beat_duration * 2
    semibreve_duration = beat_duration * 4

    sample_rate = 44100 # Hz
    sample_size = 1 # bytes
    waves = [
        itertools.chain(
            damped_sin_wave(note_frequencies["E4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["D4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["C4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["D4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["E4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["E4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["E4"], sample_rate, minim_duration),
            damped_sin_wave(note_frequencies["D4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["D4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["D4"], sample_rate, minim_duration),
            damped_sin_wave(note_frequencies["E4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["G4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["G4"], sample_rate, minim_duration),
            damped_sin_wave(note_frequencies["E4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["D4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["C4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["D4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["E4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["E4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["E4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["E4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["D4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["D4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["E4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["D4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["C4"], sample_rate, semibreve_duration),
            zero_wave(sample_rate, crochet_duration * 1),
        ),
        itertools.chain(
            zero_wave(sample_rate, crochet_duration * 1),
            damped_sin_wave(note_frequencies["E4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["D4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["C4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["D4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["E4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["E4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["E4"], sample_rate, minim_duration),
            damped_sin_wave(note_frequencies["D4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["D4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["D4"], sample_rate, minim_duration),
            damped_sin_wave(note_frequencies["E4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["G4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["G4"], sample_rate, minim_duration),
            damped_sin_wave(note_frequencies["E4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["D4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["C4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["D4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["E4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["E4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["E4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["E4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["D4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["D4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["E4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["D4"], sample_rate, crochet_duration),
            damped_sin_wave(note_frequencies["C4"], sample_rate, semibreve_duration),
        ),
    ]

    sample_wave = lambda value: sample_to_int(value, sample_size)
    wave_to_channel = lambda wave: list(map(sample_wave, wave))

    channels = list(map(wave_to_channel, waves))

    with open(filename, "wb") as f:
        write_wav_file(f, channels, sample_rate, sample_size)

def write_wav_file(file, channels, sample_rate, sample_size=1):
    write_riff_chunk(file, channels, sample_size)
    write_format_chunk(file, sample_rate, sample_size, channels)
    write_data_chunk(file, channels, sample_size)


def write_riff_chunk(file, channels, sample_size):
    num_bytes = sum(len(ch) for ch in channels) * sample_size
    file.write(b'RIFF')
    file.write((36 + num_bytes).to_bytes(4, 'little'))
    file.write(b'WAVE')

def write_format_chunk(file, sample_rate, sample_size, channels):
    bytes_per_second = sample_rate * len(channels) * sample_size

    file.write(b'fmt ')
    file.write((0x10).to_bytes(4, 'little'))
    file.write((0x01).to_bytes(2, 'little'))
    file.write(len(channels).to_bytes(2, 'little'))
    file.write((sample_rate).to_bytes(4, 'little'))
    file.write((bytes_per_second).to_bytes(4, 'little'))
    file.write((sample_size).to_bytes(2, 'little'))
    file.write((8 * sample_size).to_bytes(2, 'little'))

def write_data_chunk(file, channels, sample_size):
    # check all channels are the same length
    if len(channels) == 0:
        raise ValueError("no channels provided")

    samples_per_channel = len(channels[0])
    if not all(len(ch) == samples_per_channel for ch in channels):
        raise ValueError("all channels must be the same length")

    file.write(b'data')
    file.write((sum(len(ch) for ch in channels) * sample_size).to_bytes(4, 'little'))
    for i in range(samples_per_channel):
        for ch in channels:
            file.write(ch[i].to_bytes(sample_size, 'little'))


def sin_wave(frequency, sample_rate, duration):
    total_samples = int(sample_rate * duration)
    for n in range(total_samples):
        yield math.sin(2 * math.pi * frequency * n / sample_rate)

def damped_sin_wave(frequency, sample_rate, duration, damping=1):
    for i, sample in enumerate(sin_wave(frequency, sample_rate, duration)):
        yield sample * math.exp(-damping * i / sample_rate)

def zero_wave(sample_rate, duration):
    total_samples = int(sample_rate * duration)
    for _ in range(total_samples):
        yield 0.0

def sample_to_int(sample, sample_size):
    amplitude = (2 ** (8 * sample_size)) / 2 - 1
    base = 2 ** (8 * sample_size - 1)

    return int(sample * amplitude + base)

if __name__ == "__main__":
    main()
