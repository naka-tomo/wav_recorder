#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pyaudio
import wave
import time
import sys
import os
from select import select

WORD_LIST = [
"たぬき", 
"ばなな",
]

NUM_ITR = 5

RATE = 16000
FORMAT = pyaudio.paInt16 # 16bit
CHANNELS = 1             # モノラル
DEVICE_INDEX = 0



def kbhit():
    dr,dw,de = select([sys.stdin], [], [], 0)
    return dr != []

def record():
    
    CHUNK = 1024
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index = DEVICE_INDEX,
                    frames_per_buffer=1024)
    
   
    frames = []
    
    while 1:
        data = stream.read(CHUNK)
        frames.append(data)
        
        if kbhit():
            data = stream.read(CHUNK)
            frames.append(data)
            break

        print(">", end="")
        sys.stdout.flush()
    
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    return frames

def save_wav( frames, file_name ):
    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def main():
    
    try:
        os.mkdir("wav")
    except:
        pass

    for w in WORD_LIST:
        num_record = 0
        
        
        while num_record < NUM_ITR:
            file_name = "wav/%s_%03d.wav" % (w, num_record)
            
            
            if os.path.exists(file_name):
                print( file_name, "already exists. skip. " )
                num_record += 1
                continue

            print("---------------------------")
            print(w, "を録音します．")
            time.sleep(1)
            print("停止するには何かキーを押してください．")
            frames = record()
            
            
            while 1:
                c = input("s:save, r:rerecord, q:quit -> " )
                
                if c=="s":
                    save_wav( frames, file_name  )
                    print("  %sに保存しました．" % file_name )
                    num_record += 1
                    break
                elif c=="r":
                    break
                elif c=="q":
                    exit()


if __name__ == "__main__":
    main()

