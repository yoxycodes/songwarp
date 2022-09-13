import sys
from pydub import AudioSegment

# First argument is the path to the file
# Second argument is the semitones to transpose
def main(argv):
    try:
        input_file = str(argv[1])
        semitones = int(argv[2])
    except IndexError:
        print(f"Usage: {__name__}.py <input_file> <semitones>")
        sys.exit(1)

    # Decode the audio file into an AudioSegment object
    sound = AudioSegment.from_file(input_file, format=input_file.split(".")[-1])

    # Shift the pitch up by half an octave (speed will increase proportionally)
    new_sample_rate = int(sound.frame_rate * (2.0 ** (semitones / 12)))

    # Keep the same samples but tell the computer they ought to be played at the 
    # new, higher sample rate. This file sounds like a chipmunk but has a weird sample rate.
    hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

    # Now we just convert it to a common sample rate (44.1k - standard audio CD) to 
    # make sure it works in regular audio players. Other than potentially losing audio quality (if
    # you set it too low - 44.1k is plenty) this should now noticeable change how the audio sounds.
    hipitch_sound = hipitch_sound.set_frame_rate(44100)

    # Export / save pitch changed sound
    hipitch_sound.export(f"{input_file}-transposed.{input_file.split('.')[-1]}", format=input_file.split(".")[-1])

if __name__ == '__main__':
    main(sys.argv)
