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
from Izvedi_ukaz import pobuda_koren


def Zaženi():
    KR_podatki=pobuda_koren/'build/verification/remmina';KR_podatki.mkdir(parents=True,exist_ok=True)
    preverjanje_veljavnosti_prijavi={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((pobuda_koren/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];izbirnik=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            navidezen_zaslon=shutil.which('Xvfb')
            if navidezen_zaslon: strežnik_VALUE=[navidezen_zaslon]
            else:
                뿌리파일계층=pobuda_koren.parent/'rpi4/build/rootfs'
                strežnik_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Zaženi(argument_ARRAY,환경=None,**imenovan_argument):
                LOG_zapis=(KR_podatki/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_zapis)
                podatki_položaj=subprocess.Popen(argument_ARRAY,env=환경,stdout=LOG_zapis,stderr=subprocess.STDOUT,**imenovan_argument)
                실행과정들.append(podatki_položaj);return podatki_položaj
            환경=dict(os.environ)
            for Ime in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Ime,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(element_COUNT for element_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(element_COUNT)).exists() and not Path('/tmp/.X%d-lock'%element_COUNT).exists())
            환경['DISPLAY']=':'+str(수치)
            zaslon=Zaženi(strežnik_VALUE+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            rok_čas=time.monotonic()+30
            while True:
                assert zaslon.poll() is None and time.monotonic()<rok_čas,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            gost=subprocess.Popen(['python3',str(pobuda_koren/'Orodja/Izvedi_ukaz.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(gost);izbirnik.register(gost.stdout,selectors.EVENT_READ)
            def 기다리기(oznaka,odmik_VALUE=0):
                rok_čas=time.monotonic()+45
                while oznaka not in 직렬입출력[odmik_VALUE:]:
                    assert gost.poll() is None and time.monotonic()<rok_čas,직렬입출력[odmik_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in izbirnik.select(.1):
                        podatki=누름값.fileobj.read(65536)
                        if podatki:직렬입출력.extend(podatki)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            številka_vrat=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profil=작업경로/'test.remmina'
            Profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%številka_vrat)
            Zaženi(['dbus-run-session','--','remmina','-c',str(Profil)],환경=환경,start_new_session=True)
            def 가상입력도구(*argument_ARRAY):return subprocess.check_output(['xdotool']+list(argument_ARRAY),env=환경,stderr=subprocess.STDOUT)
            rok_čas=time.monotonic()+60;okno=None
            while time.monotonic()<rok_čas:
                Išči_KR=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Išči_KR.returncode==0:
                    후보=Išči_KR.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    V_fokusu=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if V_fokusu.returncode==0:okno=후보;break
                time.sleep(.1)
            assert okno,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',okno,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Besedilo):가상입력도구('type','--clearmodifiers','--delay','50',Besedilo)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            odmik_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),odmik_VALUE)
            odmik_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),odmik_VALUE)
            odmik_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/nič_operand Ključ_VALUE, Shift+Space 또는 F9'.encode(),odmik_VALUE);기다리기(b'jkoros-native> ',odmik_VALUE)
            odmik_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),odmik_VALUE)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',okno,str(KR_podatki/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',odmik_VALUE)
            # dejanski_podatki Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            risba_VALUE=Image.open(str(KR_podatki/'remmina-korean.png')).convert('RGB')
            naslovna_vrstica=None
            for Navpično_položaj in range(risba_VALUE.height):
                가로들=[가로 for 가로 in range(risba_VALUE.width) if risba_VALUE.getpixel((가로,Navpično_položaj))==(32,80,144)]
                if len(가로들)>=500:naslovna_vrstica=(min(가로들),Navpično_položaj);break
            assert naslovna_vrstica,'native terminal title bar not found'
            가로,Navpično_položaj=naslovna_vrstica[0]+564,naslovna_vrstica[1]+356
            가상입력도구('mousemove','--window',okno,str(가로),str(Navpično_položaj))
            def 화상기다리기(Ime,점들):
                rok_VALUE=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',okno,str(KR_podatki/Ime)])
                    bitna_slika_IMAGE=Image.open(str(KR_podatki/Ime)).convert('RGB')
                    if all(bitna_slika_IMAGE.getpixel(Položaj)==빛 for Položaj,빛 in 점들):return
                    assert time.monotonic()<rok_VALUE,'Remmina framebuffer did not settle: '+Ime
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Navpično_položaj-7),(255,255,255)),((가로+7,Navpično_položaj+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',okno,str(가로-120),str(Navpično_položaj-80),'mouseup','1')
            time.sleep(.4)
            odmik_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',odmik_VALUE)
            가상입력도구('mousemove','--window',okno,'500','45')
            화상기다리기('remmina-resized.png',[
                ((naslovna_vrstica[0]+447,naslovna_vrstica[1]+279),(39,49,64)),((가로,Navpično_položaj),(24,32,48))])
            if shutil.which('dpkg-query'):
                številka_različice=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                številka_različice=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            preverjanje_veljavnosti_prijavi.update(passed=True,display=환경['DISPLAY'],remmina_version=številka_različice,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not preverjanje_veljavnosti_prijavi['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(KR_podatki/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for podatki_položaj in reversed(실행과정들):
                if podatki_položaj.poll() is None:
                    if podatki_položaj.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(podatki_položaj.pid,signal.SIGTERM)
                    else:podatki_položaj.terminate()
                    try:podatki_položaj.wait(timeout=5)
                    except subprocess.TimeoutExpired:podatki_položaj.kill();podatki_položaj.wait()
            izbirnik.close()
            for Datoteka_vnos in 기록들:Datoteka_vnos.close()
            (KR_podatki/'serial.log').write_bytes(직렬입출력)
            (KR_podatki/'report.json').write_text(json.dumps(preverjanje_veljavnosti_prijavi,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Zaženi()
