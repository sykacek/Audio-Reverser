import numpy
import struct
import wave
from playsound import playsound
import sys

#check argv
file = sys.argv[1]
if file.find(".wav") == -1:
    print("Invalid file format")
    sys.exit(1)

#dsp function
def dsp(data: tuple):
    temp = data[::-1]
    return temp

#get bytes and audio quality
wav = wave.open(file, 'r')

nf = wav.getnframes()
fr = wav.getframerate()
sw = wav.getsampwidth()
if sw == 3:
    print("Unsupported bit depth (24 bit)")
    sys.exit(1)
data = wav.readframes(nf)
nc = wav.getnchannels() 
ct = wav.getcomptype()
cn = wav.getcompname()

print(wav.getparams())

wav.close()

print(len(data))

data = struct.unpack('{n}h'.format(n=nf*nc), data)
data = dsp(data)

print("Maximum in raw buffer was {n}".format(n=numpy.argmax(data)))

#open and write to outup file
revf = file.replace(".wav", "-rev.wav")
wav = wave.open(revf, 'w')

wav.setcomptype(comptype="NONE", compname="not compressed")
wav.setcomptype(compname=cn, comptype=ct)
wav.setnchannels(nc)
wav.setsampwidth(sw)
wav.setframerate(fr)
wav.setnframes(nf)

#debug

bytedata = (struct.pack('{n}h'.format(n=nf*nc), *data))
print("Maximum value in bytes was {n}".format(n=numpy.argmax(bytedata)))


wav.writeframes(bytedata)
wav.close()