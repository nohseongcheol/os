#!/usr/bin/env python3
"""Exercise the installed Remmina in an isolated X display and D-Bus session.

Needs Remmina's VNC plugin, xdotool, Xvfb (or the existing ARM64 Xvfb rootfs
and qemu-aarch64), dbus-run-session, and ImageMagick import. Never uses :0.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import shutil
import subprocess
import tempfile
import time
from εκτελώ_εντολή import έργο_ρίζα


def Εκτέλεση_2():
    μέτρηση_δεδομένα=έργο_ρίζα/'build/verification/remmina';μέτρηση_δεδομένα.mkdir(parents=True,exist_ok=True)
    επικύρωση_έκθεση={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((έργο_ρίζα/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];επιλογέας=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            εικονικός_οθόνη=shutil.which('Xvfb')
            if εικονικός_οθόνη: διακομιστής_τιμή=[εικονικός_οθόνη]
            else:
                뿌리파일계층=έργο_ρίζα.parent/'rpi4/build/rootfs'
                διακομιστής_τιμή=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Εκτέλεση_2(όρισμα_πίνακας,περιβάλλον_5d36e09c=None,**καθορισμένο_όρισμα):
                καταγράφω_ρεκόρ=(μέτρηση_δεδομένα/('process-%d.log'%len(기록들))).open('wb');기록들.append(καταγράφω_ρεκόρ)
                δεδομένα_θέση=subprocess.Popen(όρισμα_πίνακας,env=περιβάλλον_5d36e09c,stdout=καταγράφω_ρεκόρ,stderr=subprocess.STDOUT,**καθορισμένο_όρισμα)
                실행과정들.append(δεδομένα_θέση);return δεδομένα_θέση
            περιβάλλον_5d36e09c=dict(os.environ)
            for Όνομα in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):περιβάλλον_5d36e09c.pop(Όνομα,None)
            περιβάλλον_5d36e09c.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            περιβάλλον_5d36e09c['DISPLAY']=':'+str(수치)
            οθόνη=Εκτέλεση_2(διακομιστής_τιμή+[περιβάλλον_5d36e09c['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],περιβάλλον_5d36e09c=περιβάλλον_5d36e09c)
            προθεσμία_ώρα=time.monotonic()+30
            while True:
                assert οθόνη.poll() is None and time.monotonic()<προθεσμία_ώρα,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=περιβάλλον_5d36e09c,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            Επισκέπτης=subprocess.Popen(['python3',str(έργο_ρίζα/'Εργαλεία/εκτελώ_εντολή.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(Επισκέπτης);επιλογέας.register(Επισκέπτης.stdout,selectors.EVENT_READ)
            def 기다리기(δείκτης_8b722c5f,Υπέρθεση_τιμή=0):
                προθεσμία_ώρα=time.monotonic()+45
                while δείκτης_8b722c5f not in 직렬입출력[Υπέρθεση_τιμή:]:
                    assert Επισκέπτης.poll() is None and time.monotonic()<προθεσμία_ώρα,직렬입출력[Υπέρθεση_τιμή:].decode('utf-8','replace')
                    for 누름값,_ in επιλογέας.select(.1):
                        δεδομένα=누름값.fileobj.read(65536)
                        if δεδομένα:직렬입출력.extend(δεδομένα)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            αριθμός_θύρας=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Προφίλ=작업경로/'test.remmina'
            Προφίλ.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%αριθμός_θύρας)
            Εκτέλεση_2(['dbus-run-session','--','remmina','-c',str(Προφίλ)],περιβάλλον_5d36e09c=περιβάλλον_5d36e09c,start_new_session=True)
            def εικονικός_είσοδος_εργαλείο(*όρισμα_πίνακας):return subprocess.check_output(['xdotool']+list(όρισμα_πίνακας),env=περιβάλλον_5d36e09c,stderr=subprocess.STDOUT)
            προθεσμία_ώρα=time.monotonic()+60;Παράθυρο=None
            while time.monotonic()<προθεσμία_ώρα:
                αναζητώ_μέτρηση=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=περιβάλλον_5d36e09c,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if αναζητώ_μέτρηση.returncode==0:
                    후보=αναζητώ_μέτρηση.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Εστίαση_f7e69dab=subprocess.run(['xdotool','windowfocus','--sync',후보],env=περιβάλλον_5d36e09c,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Εστίαση_f7e69dab.returncode==0:Παράθυρο=후보;break
                time.sleep(.1)
            assert Παράθυρο,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            εικονικός_είσοδος_εργαλείο('mousemove','--window',Παράθυρο,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Κείμενο):εικονικός_είσοδος_εργαλείο('type','--clearmodifiers','--delay','50',Κείμενο)
            def 누름값(*누름열):εικονικός_είσοδος_εργαλείο('key','--clearmodifiers',*누름열)
            Υπέρθεση_τιμή=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Υπέρθεση_τιμή)
            Υπέρθεση_τιμή=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),Υπέρθεση_τιμή)
            Υπέρθεση_τιμή=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/μηδέν_τελεστέος Κλειδί_τιμή, Shift+Space 또는 F9'.encode(),Υπέρθεση_τιμή);기다리기(b'jkoros-native> ',Υπέρθεση_τιμή)
            Υπέρθεση_τιμή=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),Υπέρθεση_τιμή)
            subprocess.check_call(['import','-display',περιβάλλον_5d36e09c['DISPLAY'],'-window',Παράθυρο,str(μέτρηση_δεδομένα/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',Υπέρθεση_τιμή)
            # πραγματικός_δεδομένα Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            σχέδιο_τιμή=Image.open(str(μέτρηση_δεδομένα/'remmina-korean.png')).convert('RGB')
            λεζάντα=None
            for τομέας_θέση in range(σχέδιο_τιμή.height):
                가로들=[가로 for 가로 in range(σχέδιο_τιμή.width) if σχέδιο_τιμή.getpixel((가로,τομέας_θέση))==(32,80,144)]
                if len(가로들)>=500:λεζάντα=(min(가로들),τομέας_θέση);break
            assert λεζάντα,'native terminal title bar not found'
            가로,τομέας_θέση=λεζάντα[0]+564,λεζάντα[1]+356
            εικονικός_είσοδος_εργαλείο('mousemove','--window',Παράθυρο,str(가로),str(τομέας_θέση))
            def 화상기다리기(Όνομα,점들):
                προθεσμία_τιμή=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',περιβάλλον_5d36e09c['DISPLAY'],'-window',Παράθυρο,str(μέτρηση_δεδομένα/Όνομα)])
                    화상=Image.open(str(μέτρηση_δεδομένα/Όνομα)).convert('RGB')
                    if all(화상.getpixel(Θέση)==빛 for Θέση,빛 in 점들):return
                    assert time.monotonic()<προθεσμία_τιμή,'Remmina framebuffer did not settle: '+Όνομα
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,τομέας_θέση-7),(255,255,255)),((가로+7,τομέας_θέση+7),(255,255,255))])
            εικονικός_είσοδος_εργαλείο('mousedown','1','mousemove','--window',Παράθυρο,str(가로-120),str(τομέας_θέση-80),'mouseup','1')
            time.sleep(.4)
            Υπέρθεση_τιμή=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',Υπέρθεση_τιμή)
            εικονικός_είσοδος_εργαλείο('mousemove','--window',Παράθυρο,'500','45')
            화상기다리기('remmina-resized.png',[
                ((λεζάντα[0]+447,λεζάντα[1]+279),(39,49,64)),((가로,τομέας_θέση),(24,32,48))])
            if shutil.which('dpkg-query'):
                αριθμός_έκδοσης=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                αριθμός_έκδοσης=subprocess.check_output(['remmina','--version'],env=περιβάλλον_5d36e09c,stderr=subprocess.STDOUT).decode('utf-8','replace')
            επικύρωση_έκθεση.update(passed=True,display=περιβάλλον_5d36e09c['DISPLAY'],remmina_version=αριθμός_έκδοσης,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not επικύρωση_έκθεση['passed'] and 'περιβάλλον_5d36e09c' in locals() and περιβάλλον_5d36e09c.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',περιβάλλον_5d36e09c['DISPLAY'],'-window','root',str(μέτρηση_δεδομένα/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for δεδομένα_θέση in reversed(실행과정들):
                if δεδομένα_θέση.poll() is None:
                    if δεδομένα_θέση.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(δεδομένα_θέση.pid,signal.SIGTERM)
                    else:δεδομένα_θέση.terminate()
                    try:δεδομένα_θέση.wait(timeout=5)
                    except subprocess.TimeoutExpired:δεδομένα_θέση.kill();δεδομένα_θέση.wait()
            επιλογέας.close()
            for Αρχείο_καταχώρηση in 기록들:Αρχείο_καταχώρηση.close()
            (μέτρηση_δεδομένα/'serial.log').write_bytes(직렬입출력)
            (μέτρηση_δεδομένα/'report.json').write_text(json.dumps(επικύρωση_έκθεση,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Εκτέλεση_2()
