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
from Suorita_komento import aloite_juuri


def Suorita_2():
    KR_data=aloite_juuri/'build/verification/remmina';KR_data.mkdir(parents=True,exist_ok=True)
    vahvistus_raportti={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((aloite_juuri/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];valitsin=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            virtuaalinen_näyttö=shutil.which('Xvfb')
            if virtuaalinen_näyttö: palvelin_ARVO=[virtuaalinen_näyttö]
            else:
                뿌리파일계층=aloite_juuri.parent/'rpi4/build/rootfs'
                palvelin_ARVO=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Suorita_2(argumentti_MATRIISI,ympäristö=None,**nimetty_argumentti):
                LOG_TIETUE=(KR_data/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_TIETUE)
                data_toimi=subprocess.Popen(argumentti_MATRIISI,env=ympäristö,stdout=LOG_TIETUE,stderr=subprocess.STDOUT,**nimetty_argumentti)
                실행과정들.append(data_toimi);return data_toimi
            ympäristö=dict(os.environ)
            for Nimi in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):ympäristö.pop(Nimi,None)
            ympäristö.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(kohde_LASKE for kohde_LASKE in range(80,200) if not Path('/tmp/.X11-unix/X'+str(kohde_LASKE)).exists() and not Path('/tmp/.X%d-lock'%kohde_LASKE).exists())
            ympäristö['DISPLAY']=':'+str(수치)
            näyttö=Suorita_2(palvelin_ARVO+[ympäristö['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],ympäristö=ympäristö)
            määräaika_AIKA=time.monotonic()+30
            while True:
                assert näyttö.poll() is None and time.monotonic()<määräaika_AIKA,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=ympäristö,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            vieras=subprocess.Popen(['python3',str(aloite_juuri/'työkalut/Suorita_komento.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(vieras);valitsin.register(vieras.stdout,selectors.EVENT_READ)
            def 기다리기(merkintä,SIIRTYMÄ_ARVO=0):
                määräaika_AIKA=time.monotonic()+45
                while merkintä not in 직렬입출력[SIIRTYMÄ_ARVO:]:
                    assert vieras.poll() is None and time.monotonic()<määräaika_AIKA,직렬입출력[SIIRTYMÄ_ARVO:].decode('utf-8','replace')
                    for 누름값,_ in valitsin.select(.1):
                        data=누름값.fileobj.read(65536)
                        if data:직렬입출력.extend(data)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            portin_numero=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profiili=작업경로/'test.remmina'
            Profiili.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%portin_numero)
            Suorita_2(['dbus-run-session','--','remmina','-c',str(Profiili)],ympäristö=ympäristö,start_new_session=True)
            def virtuaalinen_syöte_työkalu(*argumentti_MATRIISI):return subprocess.check_output(['xdotool']+list(argumentti_MATRIISI),env=ympäristö,stderr=subprocess.STDOUT)
            määräaika_AIKA=time.monotonic()+60;Ikkuna=None
            while time.monotonic()<määräaika_AIKA:
                Hae_KR=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=ympäristö,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Hae_KR.returncode==0:
                    후보=Hae_KR.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Tärkeät=subprocess.run(['xdotool','windowfocus','--sync',후보],env=ympäristö,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Tärkeät.returncode==0:Ikkuna=후보;break
                time.sleep(.1)
            assert Ikkuna,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            virtuaalinen_syöte_työkalu('mousemove','--window',Ikkuna,'280','240','click','1')
            time.sleep(1)
            def 글자입력(teksti):virtuaalinen_syöte_työkalu('type','--clearmodifiers','--delay','50',teksti)
            def 누름값(*누름열):virtuaalinen_syöte_työkalu('key','--clearmodifiers',*누름열)
            SIIRTYMÄ_ARVO=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),SIIRTYMÄ_ARVO)
            SIIRTYMÄ_ARVO=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),SIIRTYMÄ_ARVO)
            SIIRTYMÄ_ARVO=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/nolla_operandi Avain_ARVO, Shift+Space 또는 F9'.encode(),SIIRTYMÄ_ARVO);기다리기(b'jkoros-native> ',SIIRTYMÄ_ARVO)
            SIIRTYMÄ_ARVO=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),SIIRTYMÄ_ARVO)
            subprocess.check_call(['import','-display',ympäristö['DISPLAY'],'-window',Ikkuna,str(KR_data/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',SIIRTYMÄ_ARVO)
            # todellinen_data Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            piirustus_ARVO=Image.open(str(KR_data/'remmina-korean.png')).convert('RGB')
            otsikkorivi=None
            for toimiala_toimi in range(piirustus_ARVO.height):
                가로들=[가로 for 가로 in range(piirustus_ARVO.width) if piirustus_ARVO.getpixel((가로,toimiala_toimi))==(32,80,144)]
                if len(가로들)>=500:otsikkorivi=(min(가로들),toimiala_toimi);break
            assert otsikkorivi,'native terminal title bar not found'
            가로,toimiala_toimi=otsikkorivi[0]+564,otsikkorivi[1]+356
            virtuaalinen_syöte_työkalu('mousemove','--window',Ikkuna,str(가로),str(toimiala_toimi))
            def 화상기다리기(Nimi,점들):
                määräaika_ARVO=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',ympäristö['DISPLAY'],'-window',Ikkuna,str(KR_data/Nimi)])
                    bittikartta_KUVA=Image.open(str(KR_data/Nimi)).convert('RGB')
                    if all(bittikartta_KUVA.getpixel(paikka)==빛 for paikka,빛 in 점들):return
                    assert time.monotonic()<määräaika_ARVO,'Remmina framebuffer did not settle: '+Nimi
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,toimiala_toimi-7),(255,255,255)),((가로+7,toimiala_toimi+7),(255,255,255))])
            virtuaalinen_syöte_työkalu('mousedown','1','mousemove','--window',Ikkuna,str(가로-120),str(toimiala_toimi-80),'mouseup','1')
            time.sleep(.4)
            SIIRTYMÄ_ARVO=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',SIIRTYMÄ_ARVO)
            virtuaalinen_syöte_työkalu('mousemove','--window',Ikkuna,'500','45')
            화상기다리기('remmina-resized.png',[
                ((otsikkorivi[0]+447,otsikkorivi[1]+279),(39,49,64)),((가로,toimiala_toimi),(24,32,48))])
            if shutil.which('dpkg-query'):
                versionumero=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                versionumero=subprocess.check_output(['remmina','--version'],env=ympäristö,stderr=subprocess.STDOUT).decode('utf-8','replace')
            vahvistus_raportti.update(passed=True,display=ympäristö['DISPLAY'],remmina_version=versionumero,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not vahvistus_raportti['passed'] and 'ympäristö' in locals() and ympäristö.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',ympäristö['DISPLAY'],'-window','root',str(KR_data/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for data_toimi in reversed(실행과정들):
                if data_toimi.poll() is None:
                    if data_toimi.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(data_toimi.pid,signal.SIGTERM)
                    else:data_toimi.terminate()
                    try:data_toimi.wait(timeout=5)
                    except subprocess.TimeoutExpired:data_toimi.kill();data_toimi.wait()
            valitsin.close()
            for Tiedosto_merkintä in 기록들:Tiedosto_merkintä.close()
            (KR_data/'serial.log').write_bytes(직렬입출력)
            (KR_data/'report.json').write_text(json.dumps(vahvistus_raportti,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Suorita_2()
