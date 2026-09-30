import os
import math
import struct
import wave
import random

def generate_wav(filepath, samples, sample_rate=44100):
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    with wave.open(filepath, 'w') as wav_file:
        n_channels = 1
        sampwidth = 2
        n_frames = len(samples)
        wav_file.setparams((n_channels, sampwidth, sample_rate, n_frames, 'NONE', 'not compressed'))
        
        raw_data = bytearray()
        for sample in samples:
            # Clamp between -32767 and 32767
            val = int(max(-32767, min(32767, sample * 32767)))
            raw_data.extend(struct.pack('<h', val))
        wav_file.writeframes(raw_data)

def generate_slice_sound(filepath):
    sample_rate = 44100
    duration = 0.16
    total_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(total_samples):
        t = i / sample_rate
        # Frequency sweep from 1400 Hz down to 400 Hz
        freq = 1400 - (1000 * (i / total_samples))
        # Tone
        tone = math.sin(2 * math.pi * freq * t)
        # Noise component for whoosh
        noise = (random.random() * 2 - 1) * 0.4
        # Amplitude envelope: fast attack, exponential decay
        env = math.exp(-18 * t)
        sample = (tone * 0.7 + noise * 0.3) * env
        samples.append(sample)
        
    generate_wav(filepath, samples, sample_rate)

def generate_bomb_sound(filepath):
    sample_rate = 44100
    duration = 0.55
    total_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(total_samples):
        t = i / sample_rate
        # Low frequency drop 120 Hz -> 35 Hz
        freq = 120 * math.exp(-4 * t)
        tone = math.sin(2 * math.pi * freq * t)
        # Heavy noise for explosion
        noise = (random.random() * 2 - 1)
        # Envelope: immediate attack, exponential decay
        env = math.exp(-6.5 * t)
        sample = (tone * 0.4 + noise * 0.6) * env
        samples.append(sample)
        
    generate_wav(filepath, samples, sample_rate)

def generate_game_over_sound(filepath):
    sample_rate = 44100
    duration = 1.0
    total_samples = int(sample_rate * duration)
    samples = []
    
    # Four descending notes: G4 (392Hz), E4 (329.6Hz), C4 (261.6Hz), G3 (196Hz)
    notes = [392.0, 329.63, 261.63, 196.0]
    note_dur = duration / len(notes)
    
    for i in range(total_samples):
        t = i / sample_rate
        note_idx = min(int(t / note_dur), len(notes) - 1)
        freq = notes[note_idx]
        note_t = t - (note_idx * note_dur)
        
        # Soft organ / chime harmonic
        tone = (math.sin(2 * math.pi * freq * t) * 0.7 + 
                math.sin(2 * math.pi * freq * 2 * t) * 0.2 +
                math.sin(2 * math.pi * freq * 3 * t) * 0.1)
        env = math.exp(-4.5 * note_t)
        sample = tone * env * 0.8
        samples.append(sample)
        
    generate_wav(filepath, samples, sample_rate)

def ensure_sound_effects(sounds_dir):
    slice_path = os.path.join(sounds_dir, "slice.wav")
    bomb_path = os.path.join(sounds_dir, "bomb.wav")
    game_over_path = os.path.join(sounds_dir, "game_over.wav")
    
    if not os.path.exists(slice_path):
        generate_slice_sound(slice_path)
    if not os.path.exists(bomb_path):
        generate_bomb_sound(bomb_path)
    if not os.path.exists(game_over_path):
        generate_game_over_sound(game_over_path)
        
    return slice_path, bomb_path, game_over_path

if __name__ == "__main__":
    sounds_path = os.path.join(os.path.dirname(__file__), "..", "sounds")
    ensure_sound_effects(sounds_path)
    print("Sound effects successfully synthesized!")
