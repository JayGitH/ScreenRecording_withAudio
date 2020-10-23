import pyaudio
import wave
import threading
import time

flag = True


def find_device_index(p):
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['name'].find("立体声混音") >= 0 and info['hostApi'] == 0:  # 字符串内除“立体声混音”外还有字符
            return i
    else:
        return -1


def recoder():
    frame = []
    chunks = 1024
    p = pyaudio.PyAudio()
    index = 2
    stream = p.open(input_device_index=index, format=pyaudio.paInt16,
                    channels=2, rate=44100, input=True, frames_per_buffer=chunks)
    while flag:
        data = stream.read(chunks)
        frame.append(data)

    stream.start_stream()
    stream.close()
    p.terminate()
    return frame


def write_tmp_audio(frames, path):
    p = pyaudio.PyAudio()

    audio = wave.open(path, 'wb')
    # 设置音频参数
    audio.setnchannels(2)
    audio.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    audio.setframerate(1024)

    audio.writeframes(b''.join(frames))  # b" "前缀表示：后面字符串是bytes 类型。
    print("写入音频完成\n")

    audio.close()
    p.terminate()


def is_end():
    while 1:
        tmp = input()
        if tmp == 's':
            global flag
            flag = False
            break


def run_recorder():
    path = "tmp.wav"
    frames = recoder()
    write_tmp_audio(frames, path)


if __name__ == "__main__":
    t1 = threading.Thread(target=is_end)
    t1.setDaemon(True)
    t2 = threading.Thread(target=run_recorder)
    t1.start()
    t2.start()
