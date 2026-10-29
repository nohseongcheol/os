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
from Izvrši_komanda import projicirati_koijen


def Pokreni():
    mjera_podaci=projicirati_koijen/'build/verification/remmina';mjera_podaci.mkdir(parents=True,exist_ok=True)
    provjera_izvještaj={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projicirati_koijen/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];birač=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            virtualno_ekran=shutil.which('Xvfb')
            if virtualno_ekran: server_VALUE=[virtualno_ekran]
            else:
                뿌리파일계층=projicirati_koijen.parent/'rpi4/build/rootfs'
                server_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Pokreni(argument_niz,operativno_okruženje=None,**이름붙인인수):
                LOG_red=(mjera_podaci/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_red)
                podaci_položaj=subprocess.Popen(argument_niz,env=operativno_okruženje,stdout=LOG_red,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(podaci_položaj);return podaci_položaj
            operativno_okruženje=dict(os.environ)
            for Naziv in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):operativno_okruženje.pop(Naziv,None)
            operativno_okruženje.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(stavka_COUNT for stavka_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(stavka_COUNT)).exists() and not Path('/tmp/.X%d-lock'%stavka_COUNT).exists())
            operativno_okruženje['DISPLAY']=':'+str(수치)
            ekran=Pokreni(server_VALUE+[operativno_okruženje['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],operativno_okruženje=operativno_okruženje)
            마감시각=time.monotonic()+30
            while True:
                assert ekran.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=operativno_okruženje,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            gost=subprocess.Popen(['python3',str(projicirati_koijen/'Alati/Izvrši_komanda.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(gost);birač.register(gost.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,Pomak_VALUE=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[Pomak_VALUE:]:
                    assert gost.poll() is None and time.monotonic()<마감시각,직렬입출력[Pomak_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in birač.select(.1):
                        podaci=누름값.fileobj.read(65536)
                        if podaci:직렬입출력.extend(podaci)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            broj_priključka=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profil=작업경로/'test.remmina'
            Profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%broj_priključka)
            Pokreni(['dbus-run-session','--','remmina','-c',str(Profil)],operativno_okruženje=operativno_okruženje,start_new_session=True)
            def 가상입력도구(*argument_niz):return subprocess.check_output(['xdotool']+list(argument_niz),env=operativno_okruženje,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;prozor=None
            while time.monotonic()<마감시각:
                Traži_mjera=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=operativno_okruženje,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Traži_mjera.returncode==0:
                    후보=Traži_mjera.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    U_fokusu=subprocess.run(['xdotool','windowfocus','--sync',후보],env=operativno_okruženje,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if U_fokusu.returncode==0:prozor=후보;break
                time.sleep(.1)
            assert prozor,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',prozor,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Tekst):가상입력도구('type','--clearmodifiers','--delay','50',Tekst)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            Pomak_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Pomak_VALUE)
            Pomak_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),Pomak_VALUE)
            Pomak_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 ključ_VALUE, Shift+Space 또는 F9'.encode(),Pomak_VALUE);기다리기(b'jkoros-native> ',Pomak_VALUE)
            Pomak_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),Pomak_VALUE)
            subprocess.check_call(['import','-display',operativno_okruženje['DISPLAY'],'-window',prozor,str(mjera_podaci/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',Pomak_VALUE)
            # stvaran_podaci Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            ucrtavanje_VALUE=Image.open(str(mjera_podaci/'remmina-korean.png')).convert('RGB')
            traka_s_naslovom=None
            for Vertikalno_položaj in range(ucrtavanje_VALUE.height):
                가로들=[가로 for 가로 in range(ucrtavanje_VALUE.width) if ucrtavanje_VALUE.getpixel((가로,Vertikalno_položaj))==(32,80,144)]
                if len(가로들)>=500:traka_s_naslovom=(min(가로들),Vertikalno_položaj);break
            assert traka_s_naslovom,'native terminal title bar not found'
            가로,Vertikalno_položaj=traka_s_naslovom[0]+564,traka_s_naslovom[1]+356
            가상입력도구('mousemove','--window',prozor,str(가로),str(Vertikalno_položaj))
            def 화상기다리기(Naziv,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',operativno_okruženje['DISPLAY'],'-window',prozor,str(mjera_podaci/Naziv)])
                    rasterska_slika_IMAGE=Image.open(str(mjera_podaci/Naziv)).convert('RGB')
                    if all(rasterska_slika_IMAGE.getpixel(Pozicija)==빛 for Pozicija,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+Naziv
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Vertikalno_položaj-7),(255,255,255)),((가로+7,Vertikalno_položaj+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',prozor,str(가로-120),str(Vertikalno_položaj-80),'mouseup','1')
            time.sleep(.4)
            Pomak_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',Pomak_VALUE)
            가상입력도구('mousemove','--window',prozor,'500','45')
            화상기다리기('remmina-resized.png',[
                ((traka_s_naslovom[0]+447,traka_s_naslovom[1]+279),(39,49,64)),((가로,Vertikalno_položaj),(24,32,48))])
            if shutil.which('dpkg-query'):
                broj_verzije=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                broj_verzije=subprocess.check_output(['remmina','--version'],env=operativno_okruženje,stderr=subprocess.STDOUT).decode('utf-8','replace')
            provjera_izvještaj.update(passed=True,display=operativno_okruženje['DISPLAY'],remmina_version=broj_verzije,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not provjera_izvještaj['passed'] and 'operativno_okruženje' in locals() and operativno_okruženje.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',operativno_okruženje['DISPLAY'],'-window','root',str(mjera_podaci/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for podaci_položaj in reversed(실행과정들):
                if podaci_položaj.poll() is None:
                    if podaci_položaj.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(podaci_položaj.pid,signal.SIGTERM)
                    else:podaci_položaj.terminate()
                    try:podaci_položaj.wait(timeout=5)
                    except subprocess.TimeoutExpired:podaci_položaj.kill();podaci_položaj.wait()
            birač.close()
            for fajl_unos in 기록들:fajl_unos.close()
            (mjera_podaci/'serial.log').write_bytes(직렬입출력)
            (mjera_podaci/'report.json').write_text(json.dumps(provjera_izvještaj,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Pokreni()
