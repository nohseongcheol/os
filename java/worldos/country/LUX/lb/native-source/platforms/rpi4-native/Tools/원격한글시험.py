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
from ausféieren_Befeel import projezéieren_Racinn


def Laf():
    Mooss_Daten=projezéieren_Racinn/'build/verification/remmina';Mooss_Daten.mkdir(parents=True,exist_ok=True)
    Validatioun_mellen={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projezéieren_Racinn/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];Selekteur=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            virtuell_Bildschierm=shutil.which('Xvfb')
            if virtuell_Bildschierm: Server_VALUE=[virtuell_Bildschierm]
            else:
                뿌리파일계층=projezéieren_Racinn.parent/'rpi4/build/rootfs'
                Server_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Laf(Argument_ARRAY,환경=None,**이름붙인인수):
                LOG_Rei=(Mooss_Daten/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_Rei)
                Daten_positionéieren=subprocess.Popen(Argument_ARRAY,env=환경,stdout=LOG_Rei,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(Daten_positionéieren);return Daten_positionéieren
            환경=dict(os.environ)
            for Numm in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Numm,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(Element_COUNT for Element_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(Element_COUNT)).exists() and not Path('/tmp/.X%d-lock'%Element_COUNT).exists())
            환경['DISPLAY']=':'+str(수치)
            Bildschierm=Laf(Server_VALUE+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert Bildschierm.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            Gaascht=subprocess.Popen(['python3',str(projezéieren_Racinn/'Tools/ausféieren_Befeel.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(Gaascht);Selekteur.register(Gaascht.stdout,selectors.EVENT_READ)
            def 기다리기(Markéierung,OFFSET_VALUE=0):
                마감시각=time.monotonic()+45
                while Markéierung not in 직렬입출력[OFFSET_VALUE:]:
                    assert Gaascht.poll() is None and time.monotonic()<마감시각,직렬입출력[OFFSET_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in Selekteur.select(.1):
                        Daten=누름값.fileobj.read(65536)
                        if Daten:직렬입출력.extend(Daten)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profil=작업경로/'test.remmina'
            Profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%접속번호)
            Laf(['dbus-run-session','--','remmina','-c',str(Profil)],환경=환경,start_new_session=True)
            def 가상입력도구(*Argument_ARRAY):return subprocess.check_output(['xdotool']+list(Argument_ARRAY),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;Fënster=None
            while time.monotonic()<마감시각:
                Sich_Mooss=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Sich_Mooss.returncode==0:
                    후보=Sich_Mooss.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Wichteg=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Wichteg.returncode==0:Fënster=후보;break
                time.sleep(.1)
            assert Fënster,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',Fënster,'280','240','click','1')
            time.sleep(1)
            def 글자입력(SMS):가상입력도구('type','--clearmodifiers','--delay','50',SMS)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 Tast_VALUE, Shift+Space 또는 F9'.encode(),OFFSET_VALUE);기다리기(b'jkoros-native> ',OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),OFFSET_VALUE)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Fënster,str(Mooss_Daten/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',OFFSET_VALUE)
            # aktuell_Daten Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            Zeechnung_VALUE=Image.open(str(Mooss_Daten/'remmina-korean.png')).convert('RGB')
            Titelläischt=None
            for Vertikal_positionéieren in range(Zeechnung_VALUE.height):
                가로들=[가로 for 가로 in range(Zeechnung_VALUE.width) if Zeechnung_VALUE.getpixel((가로,Vertikal_positionéieren))==(32,80,144)]
                if len(가로들)>=500:Titelläischt=(min(가로들),Vertikal_positionéieren);break
            assert Titelläischt,'native terminal title bar not found'
            가로,Vertikal_positionéieren=Titelläischt[0]+564,Titelläischt[1]+356
            가상입력도구('mousemove','--window',Fënster,str(가로),str(Vertikal_positionéieren))
            def 화상기다리기(Numm,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Fënster,str(Mooss_Daten/Numm)])
                    Bitmap_Bild=Image.open(str(Mooss_Daten/Numm)).convert('RGB')
                    if all(Bitmap_Bild.getpixel(positionéieren)==빛 for positionéieren,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+Numm
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Vertikal_positionéieren-7),(255,255,255)),((가로+7,Vertikal_positionéieren+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',Fënster,str(가로-120),str(Vertikal_positionéieren-80),'mouseup','1')
            time.sleep(.4)
            OFFSET_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',OFFSET_VALUE)
            가상입력도구('mousemove','--window',Fënster,'500','45')
            화상기다리기('remmina-resized.png',[
                ((Titelläischt[0]+447,Titelläischt[1]+279),(39,49,64)),((가로,Vertikal_positionéieren),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            Validatioun_mellen.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not Validatioun_mellen['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(Mooss_Daten/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for Daten_positionéieren in reversed(실행과정들):
                if Daten_positionéieren.poll() is None:
                    if Daten_positionéieren.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(Daten_positionéieren.pid,signal.SIGTERM)
                    else:Daten_positionéieren.terminate()
                    try:Daten_positionéieren.wait(timeout=5)
                    except subprocess.TimeoutExpired:Daten_positionéieren.kill();Daten_positionéieren.wait()
            Selekteur.close()
            for Fichier_Agab in 기록들:Fichier_Agab.close()
            (Mooss_Daten/'serial.log').write_bytes(직렬입출력)
            (Mooss_Daten/'report.json').write_text(json.dumps(Validatioun_mellen,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Laf()
