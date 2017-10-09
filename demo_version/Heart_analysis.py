#ref.1  http://bluexmas.tistory.com/574 - how to use USB microphone
#ref.2 https://sk8erchoi-tech.blogspot.kr/2016/02/raspberry-pi.html - raspberry-pi USB microphoe
#GPIO usage : https://github.com/splitbrain/rpibplusleaf/blob/master/rpiblusleaf.pdf
#Dataset : https://www.kaggle.com/kinguistics/heartbeat-sounds
#raspberry-pi device design :  http://www.rasplay.org/?p=2203&

from time import localtime , strftime
import RPi.GPIO as GPIO
import time
import sys
import os

# Record heart beat sound
def record_heart_beat():
    file_name = strftime("%y%m%d%H%M%S",localtime()) + ".wav"
    record_run = "arecord -D plughw:1,0 -d 20 %s" %(file_name) # record sound for 20 second
    os.system(record_run)
    return file_name

def analysis_sound(file_name):
    """
    This is analysis heart beat sound with model
    Heart sound can be classified as 3 type
    first one is normal heartbeat sound like …lub……….dub……………. lub……….dub……………. lub……….dub……………. lub……….dub…
    secound one is murmuring sound and extra heart sound like (you can find an asterisk* at the locations a murmur may be.)
    …lub..*...dub……………. lub..*..dub ……………. lub..*..dub ……………. lub..*..dub … or …lub……….dub…*….lub………. dub…*….lub ………. dub…**….lub ……….dub…
    or …lub.lub……….dub………..………. lub. lub……….dub…………….lub.lub……..…….dub……. or …lub………. dub.dub………………….lub.……….dub.dub………………….lub……..…….dub. dub……
    Heart murmurs sound as though there is a “whooshing, roaring, rumbling, or turbulent fluid” noise in one of two temporal locations. They can be a symptom of many heart disorders, some serious.
    In case of extra heart sound , in some situations it is an important sign of disease, which if detected early could help a person. this is important to be able to detect as it cannot be detected by ultrasound very well.
    last one is just noise or artifical sound. if sound is too noisy tell them just do it again.
    """
    ## Here write the code
    ## output is string that ["normal" , "abnormal" , "artifact"]
    return "normal" # for example


GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT) # Green light ; Normal sound
GPIO.setup(24, GPIO.OUT) # Red Light ; Murmur sound or Extra Heart sound
GPIO.setup(25, GPIO.OUT) # Yellow Light ; Artificial sound ; Try again

GPIO.setup(18 , GPIO.IN) # Button
print "Press the button"


try:
    while True :
        # Turn off all light
        GPIO.output(23, False)
        GPIO.output(24, False)
        GPIO.output(25, False)

        if GPIO.input(18)==0:
            print "Button pressed!"
            record = record_heart_beat()

            # Show record is finished with all light
            GPIO.output(23, True)
            GPIO.output(24, True)
            GPIO.output(25, True)
            time.sleep(1)
            GPIO.output(23, False)
            GPIO.output(24, False)
            GPIO.output(25, False)

            diagnosis = analysis_sound(record)

            # Show analysis is finished with all light
            GPIO.output(23, True)
            GPIO.output(24, True)
            GPIO.output(25, True)
            time.sleep(1)
            GPIO.output(23, False)
            GPIO.output(24, False)
            GPIO.output(25, False)


            if diagnosis == "normal" :
                GPIO.output(23, True) # Green light ; Normal sound
                time.sleep(10)
            elif diagnosis == "abnormal":
                GPIO.output(24, True) # Red Light ; Murmur sound or Extra Heart sound
                time.sleep(10)
            else :
                GPIO.output(25, True) # Yellow Light ; Artificial sound ; Try again
                time.sleep(3)

            print “Press the button (CTRL-C to exit)”

except KeyboardInterrupt:
    GPIO.cleanup()
