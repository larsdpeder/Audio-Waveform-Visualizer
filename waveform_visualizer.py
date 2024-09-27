import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.io import wavfile
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
from pydub import AudioSegment
import os
import tempfile

def convert_to_wav(input_file):
    audio = AudioSegment.from_file(input_file)
    temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    audio.export(temp_wav.name, format='wav')
    return temp_wav.name

def create_waveform_video(audio_file, output_file):
    temp_wav_name = None
    try:
        # Convert to WAV if not already
        if not audio_file.lower().endswith('.wav'):
            print("Converting audio to WAV format...")
            temp_wav_name = convert_to_wav(audio_file)
            audio_file = temp_wav_name

        # Read the WAV file
        sample_rate, audio_data = wavfile.read(audio_file)
        
        # If stereo, take the mean of both channels
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        
        # Normalize audio data
        audio_data = audio_data / np.max(np.abs(audio_data))
        
        # Calculate duration
        duration = len(audio_data) / sample_rate
        
        # Set up the figure and axis
        fig, ax = plt.subplots(figsize=(16, 9), facecolor='black')
        ax.set_facecolor('black')
        ax.set_ylim(-1, 1)
        ax.set_xlim(0, 1)  # Set x-axis from 0 to 1
        
        # Add subtle grid
        ax.grid(color='dimgray', linestyle=':', linewidth=0.5, alpha=0.5)
        
        # Remove axis labels
        ax.set_xticks([])
        ax.set_yticks([])
        
        line, = ax.plot([], [], color='white', lw=2)
        
        # Number of points to display
        num_points = 1000
        
        # Animation function
        def animate(frame):
            start = frame * sample_rate // 30
            end = start + num_points
            x = np.linspace(0, 1, num_points)
            y = audio_data[start:end]
            if len(y) < num_points:
                y = np.pad(y, (0, num_points - len(y)), 'constant')
            line.set_data(x, y)
            return line,
        
        # Create the animation
        anim = FuncAnimation(fig, animate, frames=int(30 * duration), 
                             interval=1000/30, blit=True)
        
        # Save the animation as a temporary file
        temp_video = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
        anim.save(temp_video.name, fps=30, extra_args=['-vcodec', 'libx264'])
        
        # Close the matplotlib figure
        plt.close(fig)
        
        # Load the temporary video file
        video = VideoFileClip(temp_video.name)
        
        # Load the audio file
        audio = AudioFileClip(audio_file)
        
        # Set the audio of the video
        final_video = video.set_audio(audio)
        
        # Write the final video file
        final_video.write_videofile(output_file, codec='libx264', audio_codec='aac')
        
        # Close the clips
        video.close()
        audio.close()
        final_video.close()
        
        # Remove the temporary video file
        os.unlink(temp_video.name)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Clean up the temporary WAV file if it was created
        if temp_wav_name and os.path.exists(temp_wav_name):
            os.unlink(temp_wav_name)

def main():
    while True:
        audio_file = input("Enter the path to your audio file: ").strip()
        if os.path.isfile(audio_file):
            break
        else:
            print("Invalid file path. Please try again.")

    output_file = input("Enter the name for the output MP4 file (default: output.mp4): ").strip()
    if not output_file:
        output_file = "output.mp4"
    elif not output_file.lower().endswith('.mp4'):
        output_file += '.mp4'

    print(f"Creating video from {audio_file}...")
    create_waveform_video(audio_file, output_file)
    print(f"Video created successfully: {output_file}")

if __name__ == "__main__":
    main()
