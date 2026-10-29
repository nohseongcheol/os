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
from Provést_příkaz import akce_kořen


def Spustit_2():
    KV_data=akce_kořen/'build/verification/remmina';KV_data.mkdir(parents=True,exist_ok=True)
    ověření_Zpráva={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((akce_kořen/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];selektor=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            virtuální_displej=shutil.which('Xvfb')
            if virtuální_displej: server_HODNOTA=[virtuální_displej]
            else:
                뿌리파일계층=akce_kořen.parent/'rpi4/build/rootfs'
                server_HODNOTA=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Spustit_2(argument_pole,prostředí_5d36e09c=None,**pojmenovaný_argument):
                LOGZ_ZÁZNAM=(KV_data/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOGZ_ZÁZNAM)
                data_pozice=subprocess.Popen(argument_pole,env=prostředí_5d36e09c,stdout=LOGZ_ZÁZNAM,stderr=subprocess.STDOUT,**pojmenovaný_argument)
                실행과정들.append(data_pozice);return data_pozice
            prostředí_5d36e09c=dict(os.environ)
            for Název in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):prostředí_5d36e09c.pop(Název,None)
            prostředí_5d36e09c.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(zboží_POČET for zboží_POČET in range(80,200) if not Path('/tmp/.X11-unix/X'+str(zboží_POČET)).exists() and not Path('/tmp/.X%d-lock'%zboží_POČET).exists())
            prostředí_5d36e09c['DISPLAY']=':'+str(수치)
            displej=Spustit_2(server_HODNOTA+[prostředí_5d36e09c['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],prostředí_5d36e09c=prostředí_5d36e09c)
            konečný_termín_ČAS=time.monotonic()+30
            while True:
                assert displej.poll() is None and time.monotonic()<konečný_termín_ČAS,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=prostředí_5d36e09c,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            host=subprocess.Popen(['python3',str(akce_kořen/'nástroje/Provést_příkaz.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(host);selektor.register(host.stdout,selectors.EVENT_READ)
            def 기다리기(značka,POSUN_HODNOTA=0):
                konečný_termín_ČAS=time.monotonic()+45
                while značka not in 직렬입출력[POSUN_HODNOTA:]:
                    assert host.poll() is None and time.monotonic()<konečný_termín_ČAS,직렬입출력[POSUN_HODNOTA:].decode('utf-8','replace')
                    for 누름값,_ in selektor.select(.1):
                        data=누름값.fileobj.read(65536)
                        if data:직렬입출력.extend(data)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            číslo_portu=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profil=작업경로/'test.remmina'
            Profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%číslo_portu)
            Spustit_2(['dbus-run-session','--','remmina','-c',str(Profil)],prostředí_5d36e09c=prostředí_5d36e09c,start_new_session=True)
            def virtuální_vstup_nástroj(*argument_pole):return subprocess.check_output(['xdotool']+list(argument_pole),env=prostředí_5d36e09c,stderr=subprocess.STDOUT)
            konečný_termín_ČAS=time.monotonic()+60;Okno=None
            while time.monotonic()<konečný_termín_ČAS:
                HLEDAT_KV=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=prostředí_5d36e09c,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if HLEDAT_KV.returncode==0:
                    후보=HLEDAT_KV.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Prioritní=subprocess.run(['xdotool','windowfocus','--sync',후보],env=prostředí_5d36e09c,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Prioritní.returncode==0:Okno=후보;break
                time.sleep(.1)
            assert Okno,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            virtuální_vstup_nástroj('mousemove','--window',Okno,'280','240','click','1')
            time.sleep(1)
            def 글자입력(text):virtuální_vstup_nástroj('type','--clearmodifiers','--delay','50',text)
            def 누름값(*누름열):virtuální_vstup_nástroj('key','--clearmodifiers',*누름열)
            POSUN_HODNOTA=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),POSUN_HODNOTA)
            POSUN_HODNOTA=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),POSUN_HODNOTA)
            POSUN_HODNOTA=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/nula_operand Klíč_HODNOTA, Shift+Space 또는 F9'.encode(),POSUN_HODNOTA);기다리기(b'jkoros-native> ',POSUN_HODNOTA)
            POSUN_HODNOTA=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),POSUN_HODNOTA)
            subprocess.check_call(['import','-display',prostředí_5d36e09c['DISPLAY'],'-window',Okno,str(KV_data/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',POSUN_HODNOTA)
            # skutečný_data Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            kreslení_HODNOTA=Image.open(str(KV_data/'remmina-korean.png')).convert('RGB')
            záhlaví=None
            for Svislá_pozice in range(kreslení_HODNOTA.height):
                가로들=[가로 for 가로 in range(kreslení_HODNOTA.width) if kreslení_HODNOTA.getpixel((가로,Svislá_pozice))==(32,80,144)]
                if len(가로들)>=500:záhlaví=(min(가로들),Svislá_pozice);break
            assert záhlaví,'native terminal title bar not found'
            가로,Svislá_pozice=záhlaví[0]+564,záhlaví[1]+356
            virtuální_vstup_nástroj('mousemove','--window',Okno,str(가로),str(Svislá_pozice))
            def 화상기다리기(Název,점들):
                konečný_termín_HODNOTA=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',prostředí_5d36e09c['DISPLAY'],'-window',Okno,str(KV_data/Název)])
                    rastrový_obrázek_image=Image.open(str(KV_data/Název)).convert('RGB')
                    if all(rastrový_obrázek_image.getpixel(pozice)==빛 for pozice,빛 in 점들):return
                    assert time.monotonic()<konečný_termín_HODNOTA,'Remmina framebuffer did not settle: '+Název
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Svislá_pozice-7),(255,255,255)),((가로+7,Svislá_pozice+7),(255,255,255))])
            virtuální_vstup_nástroj('mousedown','1','mousemove','--window',Okno,str(가로-120),str(Svislá_pozice-80),'mouseup','1')
            time.sleep(.4)
            POSUN_HODNOTA=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',POSUN_HODNOTA)
            virtuální_vstup_nástroj('mousemove','--window',Okno,'500','45')
            화상기다리기('remmina-resized.png',[
                ((záhlaví[0]+447,záhlaví[1]+279),(39,49,64)),((가로,Svislá_pozice),(24,32,48))])
            if shutil.which('dpkg-query'):
                číslo_verze=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                číslo_verze=subprocess.check_output(['remmina','--version'],env=prostředí_5d36e09c,stderr=subprocess.STDOUT).decode('utf-8','replace')
            ověření_Zpráva.update(passed=True,display=prostředí_5d36e09c['DISPLAY'],remmina_version=číslo_verze,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not ověření_Zpráva['passed'] and 'prostředí_5d36e09c' in locals() and prostředí_5d36e09c.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',prostředí_5d36e09c['DISPLAY'],'-window','root',str(KV_data/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for data_pozice in reversed(실행과정들):
                if data_pozice.poll() is None:
                    if data_pozice.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(data_pozice.pid,signal.SIGTERM)
                    else:data_pozice.terminate()
                    try:data_pozice.wait(timeout=5)
                    except subprocess.TimeoutExpired:data_pozice.kill();data_pozice.wait()
            selektor.close()
            for Soubor_položka in 기록들:Soubor_položka.close()
            (KV_data/'serial.log').write_bytes(직렬입출력)
            (KV_data/'report.json').write_text(json.dumps(ověření_Zpráva,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Spustit_2()
