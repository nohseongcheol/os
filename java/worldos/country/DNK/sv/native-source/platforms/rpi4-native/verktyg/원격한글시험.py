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
from köra_kommando import åtgärd_rot


def Kör():
    KR_data=åtgärd_rot/'build/verification/remmina';KR_data.mkdir(parents=True,exist_ok=True)
    validering_Rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((åtgärd_rot/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];väljare=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            virtuell_visa=shutil.which('Xvfb')
            if virtuell_visa: server_värde=[virtuell_visa]
            else:
                뿌리파일계층=åtgärd_rot.parent/'rpi4/build/rootfs'
                server_värde=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Kör(argument_MATRIS,miljö=None,**namngivna_argument):
                LOG_POST=(KR_data/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_POST)
                data_placera=subprocess.Popen(argument_MATRIS,env=miljö,stdout=LOG_POST,stderr=subprocess.STDOUT,**namngivna_argument)
                실행과정들.append(data_placera);return data_placera
            miljö=dict(os.environ)
            for Namn in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):miljö.pop(Namn,None)
            miljö.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(objekt_ANTAL for objekt_ANTAL in range(80,200) if not Path('/tmp/.X11-unix/X'+str(objekt_ANTAL)).exists() and not Path('/tmp/.X%d-lock'%objekt_ANTAL).exists())
            miljö['DISPLAY']=':'+str(수치)
            skärm=Kör(server_värde+[miljö['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],miljö=miljö)
            måldatum_tid=time.monotonic()+30
            while True:
                assert skärm.poll() is None and time.monotonic()<måldatum_tid,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=miljö,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            gäst=subprocess.Popen(['python3',str(åtgärd_rot/'verktyg/köra_kommando.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(gäst);väljare.register(gäst.stdout,selectors.EVENT_READ)
            def 기다리기(markör_8b722c5f,FÖRSKJUTNING_värde=0):
                måldatum_tid=time.monotonic()+45
                while markör_8b722c5f not in 직렬입출력[FÖRSKJUTNING_värde:]:
                    assert gäst.poll() is None and time.monotonic()<måldatum_tid,직렬입출력[FÖRSKJUTNING_värde:].decode('utf-8','replace')
                    for 누름값,_ in väljare.select(.1):
                        data=누름값.fileobj.read(65536)
                        if data:직렬입출력.extend(data)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            portnummer=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profil=작업경로/'test.remmina'
            Profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%portnummer)
            Kör(['dbus-run-session','--','remmina','-c',str(Profil)],miljö=miljö,start_new_session=True)
            def virtuell_indata_verktyg(*argument_MATRIS):return subprocess.check_output(['xdotool']+list(argument_MATRIS),env=miljö,stderr=subprocess.STDOUT)
            måldatum_tid=time.monotonic()+60;Fönster=None
            while time.monotonic()<måldatum_tid:
                SÖK_KR=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=miljö,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if SÖK_KR.returncode==0:
                    kandidat=SÖK_KR.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Prioriterad=subprocess.run(['xdotool','windowfocus','--sync',kandidat],env=miljö,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Prioriterad.returncode==0:Fönster=kandidat;break
                time.sleep(.1)
            assert Fönster,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            virtuell_indata_verktyg('mousemove','--window',Fönster,'280','240','click','1')
            time.sleep(1)
            def 글자입력(text):virtuell_indata_verktyg('type','--clearmodifiers','--delay','50',text)
            def 누름값(*누름열):virtuell_indata_verktyg('key','--clearmodifiers',*누름열)
            FÖRSKJUTNING_värde=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),FÖRSKJUTNING_värde)
            FÖRSKJUTNING_värde=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),FÖRSKJUTNING_värde)
            FÖRSKJUTNING_värde=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/noll_operand Nyckel_värde, Shift+Space 또는 F9'.encode(),FÖRSKJUTNING_värde);기다리기(b'jkoros-native> ',FÖRSKJUTNING_värde)
            FÖRSKJUTNING_värde=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),FÖRSKJUTNING_värde)
            subprocess.check_call(['import','-display',miljö['DISPLAY'],'-window',Fönster,str(KR_data/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',FÖRSKJUTNING_värde)
            # verklig_data Remmina의 skärmbild 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            ritning_värde=Image.open(str(KR_data/'remmina-korean.png')).convert('RGB')
            namnlist=None
            for bransch_placera in range(ritning_värde.height):
                가로들=[가로 for 가로 in range(ritning_värde.width) if ritning_värde.getpixel((가로,bransch_placera))==(32,80,144)]
                if len(가로들)>=500:namnlist=(min(가로들),bransch_placera);break
            assert namnlist,'native terminal title bar not found'
            가로,bransch_placera=namnlist[0]+564,namnlist[1]+356
            virtuell_indata_verktyg('mousemove','--window',Fönster,str(가로),str(bransch_placera))
            def 화상기다리기(Namn,점들):
                måldatum_värde=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',miljö['DISPLAY'],'-window',Fönster,str(KR_data/Namn)])
                    bitmapp_BILD=Image.open(str(KR_data/Namn)).convert('RGB')
                    if all(bitmapp_BILD.getpixel(position)==빛 for position,빛 in 점들):return
                    assert time.monotonic()<måldatum_värde,'Remmina framebuffer did not settle: '+Namn
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,bransch_placera-7),(255,255,255)),((가로+7,bransch_placera+7),(255,255,255))])
            virtuell_indata_verktyg('mousedown','1','mousemove','--window',Fönster,str(가로-120),str(bransch_placera-80),'mouseup','1')
            time.sleep(.4)
            FÖRSKJUTNING_värde=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',FÖRSKJUTNING_värde)
            virtuell_indata_verktyg('mousemove','--window',Fönster,'500','45')
            화상기다리기('remmina-resized.png',[
                ((namnlist[0]+447,namnlist[1]+279),(39,49,64)),((가로,bransch_placera),(24,32,48))])
            if shutil.which('dpkg-query'):
                versionsnummer=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                versionsnummer=subprocess.check_output(['remmina','--version'],env=miljö,stderr=subprocess.STDOUT).decode('utf-8','replace')
            validering_Rapport.update(passed=True,display=miljö['DISPLAY'],remmina_version=versionsnummer,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not validering_Rapport['passed'] and 'miljö' in locals() and miljö.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',miljö['DISPLAY'],'-window','root',str(KR_data/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for data_placera in reversed(실행과정들):
                if data_placera.poll() is None:
                    if data_placera.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(data_placera.pid,signal.SIGTERM)
                    else:data_placera.terminate()
                    try:data_placera.wait(timeout=5)
                    except subprocess.TimeoutExpired:data_placera.kill();data_placera.wait()
            väljare.close()
            for fil_post in 기록들:fil_post.close()
            (KR_data/'serial.log').write_bytes(직렬입출력)
            (KR_data/'report.json').write_text(json.dumps(validering_Rapport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Kör()
