from pydub import AudioSegment
import mp3
from wave import Wave_read


ruta = "/home/bot/BotV6/Duricleto/"
audio = AudioSegment.from_file(ruta+"test.mp3", format="mp3")
print({
    'duration' : audio.duration_seconds,
    'sample_rate' : audio.frame_rate,
    'channels' : audio.channels,
    'sample_width' : audio.sample_width,
    'frame_count' : audio.frame_count(),
    'frame_rate' : audio.frame_rate,
    'frame_width' : audio.frame_width,
})
print()

final = audio.speedup(playback_speed=1.5)

# export to wav
final.export(ruta+"final.wav", format="wav")



with open(ruta+'final.wav', 'rb') as read_file, open('test.mp3', 'wb') as write_file:

    wav_file = Wave_read(read_file)

    sample_size = wav_file.getsampwidth()
    sample_rate = wav_file.getframerate()
    nchannels = wav_file.getnchannels()

    if sample_size != 2:
        raise ValueError("Only PCM 16-bit sample size is supported (input audio: %s)" % sample_size)

    encoder = mp3.Encoder(write_file)
    encoder.set_bit_rate(64)
    encoder.set_channels(nchannels)
    encoder.set_quality(5)   # 2-highest, 7-fastest
    encoder.set_mode(mp3.MODE_STEREO if nchannels == 2 else mp3.MODE_SINGLE_CHANNEL)

    while True:
        pcm_data = wav_file.readframes(8000)
        if pcm_data:
            encoder.write(pcm_data)
        else:
            encoder.flush()
            break


