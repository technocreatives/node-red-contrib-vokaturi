#!/usr/bin/env python
import scipy.io.wavfile
import sys
import os,inspect
import json


#initialize data to be output
data = {}

if ( len(sys.argv) != 2 ) :
    print("No .wav file provided")
    print("Usage "+ sys.argv[0] +" <path/to/file.wav>")
    data['valid'] = 0 ;
    data['error'] = "No .wav file provided";
    print(json.dumps(data));
    exit(-1);


#import inspect, os
#print inspect.getfile(inspect.currentframe())
#print os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

vokaturi_path = os.path.dirname(os.path.realpath(__file__)) +'/OpenVokaturi-2-1b'
#print(vokaturi_path)

sys.path.append(vokaturi_path + '/api')
import Vokaturi

print ("Loading library...")
if sys.platform.startswith("linux"):
    Vokaturi.load(vokaturi_path + '/lib/Vokaturi_linux64.so')
elif sys.platform == "darwin":
    Vokaturi.load(vokaturi_path + '/lib/Vokaturi_mac64.so')

print ("Analyzed by: %s" % Vokaturi.versionAndLicense())

print("Reading sound file...")
file_name = sys.argv[1]

if os.path.isfile(file_name):
    # file exists

    data['input'] = file_name;

    try:
        (sample_rate, samples) = scipy.io.wavfile.read(file_name)
        print("   sample rate %.3f Hz" % sample_rate)

        print ("Allocating Vokaturi sample array...")
        buffer_length = len(samples)
        print ("   %d samples, %d channels" % (buffer_length, samples.ndim))
        c_buffer = Vokaturi.SampleArrayC(buffer_length)

        if samples.ndim == 1:
            c_buffer[:] = samples[:] / 32768.0  # mono
        else:
            c_buffer[:] = 0.5*(samples[:,0]+0.0+samples[:,1]) / 32768.0  # stereo

            #print ("Creating VokaturiVoice...")
        voice = Vokaturi.Voice (sample_rate, buffer_length)

        #print("Filling VokaturiVoice with samples...")
        voice.fill(buffer_length, c_buffer)

        print("Extracting emotions from VokaturiVoice...")
        quality = Vokaturi.Quality()
        emotionProbabilities = Vokaturi.EmotionProbabilities()
        voice.extract(quality, emotionProbabilities)


        data['valid'] = quality.valid;

        if quality.valid:
            print("Neutral: %.3f" % emotionProbabilities.neutrality)
            print("Happy: %.3f" % emotionProbabilities.happiness)
            print("Sad: %.3f" % emotionProbabilities.sadness)
            print("Angry: %.3f" % emotionProbabilities.anger)
            print("Fear: %.3f" % emotionProbabilities.fear)

            data['probabilities'] = {};
            data['probabilities']['neutral'] = emotionProbabilities.neutrality;
            data['probabilities']['happy'] = emotionProbabilities.happiness;
            data['probabilities']['sad'] = emotionProbabilities.sadness;
            data['probabilities']['angry'] = emotionProbabilities.anger;
            data['probabilities']['fear'] = emotionProbabilities.fear;

        voice.destroy()
    except Exception as ex :
        print("Wav : bad format " + str(ex));
        data['valid'] = 0;
        data['error'] =str(ex);
else:
    data['valid'] = 0;
    data['error'] = "File " + file_name + " doesn't exist";




json_data = json.dumps(data);

print(json_data)
