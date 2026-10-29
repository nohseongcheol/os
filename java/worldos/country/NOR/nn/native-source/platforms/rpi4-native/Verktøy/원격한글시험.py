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
from Utfør_kommando import spegle_rot


def Køyr_2():
    forretningsmål_data=spegle_rot/'build/verification/remmina';forretningsmål_data.mkdir(parents=True,exist_ok=True)
    validering_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((spegle_rot/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];veljar=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            virtuell_vise=shutil.which('Xvfb')
            if virtuell_vise: tenar_VALUE=[virtuell_vise]
            else:
                뿌리파일계층=spegle_rot.parent/'rpi4/build/rootfs'
                tenar_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Køyr_2(argument_ARRAY,환경=None,**namngitt_argument):
                LOG_rad=(forretningsmål_data/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_rad)
                data_plassere=subprocess.Popen(argument_ARRAY,env=환경,stdout=LOG_rad,stderr=subprocess.STDOUT,**namngitt_argument)
                실행과정들.append(data_plassere);return data_plassere
            환경=dict(os.environ)
            for Namn in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Namn,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(vare_COUNT for vare_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(vare_COUNT)).exists() and not Path('/tmp/.X%d-lock'%vare_COUNT).exists())
            환경['DISPLAY']=':'+str(수치)
            skjerm=Køyr_2(tenar_VALUE+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert skjerm.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            gjest=subprocess.Popen(['python3',str(spegle_rot/'Verktøy/Utfør_kommando.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(gjest);veljar.register(gjest.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,OFFSET_VALUE=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[OFFSET_VALUE:]:
                    assert gjest.poll() is None and time.monotonic()<마감시각,직렬입출력[OFFSET_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in veljar.select(.1):
                        data=누름값.fileobj.read(65536)
                        if data:직렬입출력.extend(data)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            portnummer=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profil=작업경로/'test.remmina'
            Profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%portnummer)
            Køyr_2(['dbus-run-session','--','remmina','-c',str(Profil)],환경=환경,start_new_session=True)
            def 가상입력도구(*argument_ARRAY):return subprocess.check_output(['xdotool']+list(argument_ARRAY),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;vindauge=None
            while time.monotonic()<마감시각:
                Søk_forretningsmål=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Søk_forretningsmål.returncode==0:
                    후보=Søk_forretningsmål.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Fokus_f7e69dab=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Fokus_f7e69dab.returncode==0:vindauge=후보;break
                time.sleep(.1)
            assert vindauge,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',vindauge,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Tekst):가상입력도구('type','--clearmodifiers','--delay','50',Tekst)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 tast_VALUE, Shift+Space 또는 F9'.encode(),OFFSET_VALUE);기다리기(b'jkoros-native> ',OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),OFFSET_VALUE)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',vindauge,str(forretningsmål_data/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',OFFSET_VALUE)
            # faktisk_data Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            teikning_VALUE=Image.open(str(forretningsmål_data/'remmina-korean.png')).convert('RGB')
            tittelline=None
            for vertikalvising_plassere in range(teikning_VALUE.height):
                가로들=[가로 for 가로 in range(teikning_VALUE.width) if teikning_VALUE.getpixel((가로,vertikalvising_plassere))==(32,80,144)]
                if len(가로들)>=500:tittelline=(min(가로들),vertikalvising_plassere);break
            assert tittelline,'native terminal title bar not found'
            가로,vertikalvising_plassere=tittelline[0]+564,tittelline[1]+356
            가상입력도구('mousemove','--window',vindauge,str(가로),str(vertikalvising_plassere))
            def 화상기다리기(Namn,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',vindauge,str(forretningsmål_data/Namn)])
                    punktgrafikk_IMAGE=Image.open(str(forretningsmål_data/Namn)).convert('RGB')
                    if all(punktgrafikk_IMAGE.getpixel(Posisjon)==빛 for Posisjon,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+Namn
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,vertikalvising_plassere-7),(255,255,255)),((가로+7,vertikalvising_plassere+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',vindauge,str(가로-120),str(vertikalvising_plassere-80),'mouseup','1')
            time.sleep(.4)
            OFFSET_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',OFFSET_VALUE)
            가상입력도구('mousemove','--window',vindauge,'500','45')
            화상기다리기('remmina-resized.png',[
                ((tittelline[0]+447,tittelline[1]+279),(39,49,64)),((가로,vertikalvising_plassere),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            validering_rapport.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not validering_rapport['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(forretningsmål_data/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for data_plassere in reversed(실행과정들):
                if data_plassere.poll() is None:
                    if data_plassere.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(data_plassere.pid,signal.SIGTERM)
                    else:data_plassere.terminate()
                    try:data_plassere.wait(timeout=5)
                    except subprocess.TimeoutExpired:data_plassere.kill();data_plassere.wait()
            veljar.close()
            for fil_oppføring in 기록들:fil_oppføring.close()
            (forretningsmål_data/'serial.log').write_bytes(직렬입출력)
            (forretningsmål_data/'report.json').write_text(json.dumps(validering_rapport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Køyr_2()
