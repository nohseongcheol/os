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
from végrehajt_parancs import teendő_gyök


def Futtatás():
    KR_adat=teendő_gyök/'build/verification/remmina';KR_adat.mkdir(parents=True,exist_ok=True)
    ellenőrzés_jelent={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((teendő_gyök/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];szelektor=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            virtuális_kijelző=shutil.which('Xvfb')
            if virtuális_kijelző: kiszolgáló_ÉRTÉK=[virtuális_kijelző]
            else:
                뿌리파일계층=teendő_gyök.parent/'rpi4/build/rootfs'
                kiszolgáló_ÉRTÉK=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Futtatás(argumentum_TÖMB,környezet_5d36e09c=None,**megnevezett_argumentum):
                LOG_REKORD=(KR_adat/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_REKORD)
                adat_pozíció=subprocess.Popen(argumentum_TÖMB,env=környezet_5d36e09c,stdout=LOG_REKORD,stderr=subprocess.STDOUT,**megnevezett_argumentum)
                실행과정들.append(adat_pozíció);return adat_pozíció
            környezet_5d36e09c=dict(os.environ)
            for Név in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):környezet_5d36e09c.pop(Név,None)
            környezet_5d36e09c.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(cikk_DARAB for cikk_DARAB in range(80,200) if not Path('/tmp/.X11-unix/X'+str(cikk_DARAB)).exists() and not Path('/tmp/.X%d-lock'%cikk_DARAB).exists())
            környezet_5d36e09c['DISPLAY']=':'+str(수치)
            kijelző=Futtatás(kiszolgáló_ÉRTÉK+[környezet_5d36e09c['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],környezet_5d36e09c=környezet_5d36e09c)
            határidő_IDŐ=time.monotonic()+30
            while True:
                assert kijelző.poll() is None and time.monotonic()<határidő_IDŐ,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=környezet_5d36e09c,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            vendég=subprocess.Popen(['python3',str(teendő_gyök/'Eszközök/végrehajt_parancs.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(vendég);szelektor.register(vendég.stdout,selectors.EVENT_READ)
            def 기다리기(jelölő,Ofszet_ÉRTÉK=0):
                határidő_IDŐ=time.monotonic()+45
                while jelölő not in 직렬입출력[Ofszet_ÉRTÉK:]:
                    assert vendég.poll() is None and time.monotonic()<határidő_IDŐ,직렬입출력[Ofszet_ÉRTÉK:].decode('utf-8','replace')
                    for 누름값,_ in szelektor.select(.1):
                        adat=누름값.fileobj.read(65536)
                        if adat:직렬입출력.extend(adat)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            portszám=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profil=작업경로/'test.remmina'
            Profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%portszám)
            Futtatás(['dbus-run-session','--','remmina','-c',str(Profil)],környezet_5d36e09c=környezet_5d36e09c,start_new_session=True)
            def virtuális_bevitel_eszköz(*argumentum_TÖMB):return subprocess.check_output(['xdotool']+list(argumentum_TÖMB),env=környezet_5d36e09c,stderr=subprocess.STDOUT)
            határidő_IDŐ=time.monotonic()+60;Ablak=None
            while time.monotonic()<határidő_IDŐ:
                keres_KR=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=környezet_5d36e09c,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if keres_KR.returncode==0:
                    후보=keres_KR.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Szűrt=subprocess.run(['xdotool','windowfocus','--sync',후보],env=környezet_5d36e09c,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Szűrt.returncode==0:Ablak=후보;break
                time.sleep(.1)
            assert Ablak,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            virtuális_bevitel_eszköz('mousemove','--window',Ablak,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Szöveg):virtuális_bevitel_eszköz('type','--clearmodifiers','--delay','50',Szöveg)
            def 누름값(*누름열):virtuális_bevitel_eszköz('key','--clearmodifiers',*누름열)
            Ofszet_ÉRTÉK=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Ofszet_ÉRTÉK)
            Ofszet_ÉRTÉK=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),Ofszet_ÉRTÉK)
            Ofszet_ÉRTÉK=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/nulla_operandus Kulcs_ÉRTÉK, Shift+Space 또는 F9'.encode(),Ofszet_ÉRTÉK);기다리기(b'jkoros-native> ',Ofszet_ÉRTÉK)
            Ofszet_ÉRTÉK=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),Ofszet_ÉRTÉK)
            subprocess.check_call(['import','-display',környezet_5d36e09c['DISPLAY'],'-window',Ablak,str(KR_adat/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',Ofszet_ÉRTÉK)
            # tényleges_adat Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            rajz_ÉRTÉK=Image.open(str(KR_adat/'remmina-korean.png')).convert('RGB')
            címsor=None
            for szektor_pozíció in range(rajz_ÉRTÉK.height):
                가로들=[가로 for 가로 in range(rajz_ÉRTÉK.width) if rajz_ÉRTÉK.getpixel((가로,szektor_pozíció))==(32,80,144)]
                if len(가로들)>=500:címsor=(min(가로들),szektor_pozíció);break
            assert címsor,'native terminal title bar not found'
            가로,szektor_pozíció=címsor[0]+564,címsor[1]+356
            virtuális_bevitel_eszköz('mousemove','--window',Ablak,str(가로),str(szektor_pozíció))
            def 화상기다리기(Név,점들):
                határidő_ÉRTÉK=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',környezet_5d36e09c['DISPLAY'],'-window',Ablak,str(KR_adat/Név)])
                    bitkép_KÉP=Image.open(str(KR_adat/Név)).convert('RGB')
                    if all(bitkép_KÉP.getpixel(Pozíció)==빛 for Pozíció,빛 in 점들):return
                    assert time.monotonic()<határidő_ÉRTÉK,'Remmina framebuffer did not settle: '+Név
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,szektor_pozíció-7),(255,255,255)),((가로+7,szektor_pozíció+7),(255,255,255))])
            virtuális_bevitel_eszköz('mousedown','1','mousemove','--window',Ablak,str(가로-120),str(szektor_pozíció-80),'mouseup','1')
            time.sleep(.4)
            Ofszet_ÉRTÉK=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',Ofszet_ÉRTÉK)
            virtuális_bevitel_eszköz('mousemove','--window',Ablak,'500','45')
            화상기다리기('remmina-resized.png',[
                ((címsor[0]+447,címsor[1]+279),(39,49,64)),((가로,szektor_pozíció),(24,32,48))])
            if shutil.which('dpkg-query'):
                verziószám=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                verziószám=subprocess.check_output(['remmina','--version'],env=környezet_5d36e09c,stderr=subprocess.STDOUT).decode('utf-8','replace')
            ellenőrzés_jelent.update(passed=True,display=környezet_5d36e09c['DISPLAY'],remmina_version=verziószám,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not ellenőrzés_jelent['passed'] and 'környezet_5d36e09c' in locals() and környezet_5d36e09c.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',környezet_5d36e09c['DISPLAY'],'-window','root',str(KR_adat/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for adat_pozíció in reversed(실행과정들):
                if adat_pozíció.poll() is None:
                    if adat_pozíció.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(adat_pozíció.pid,signal.SIGTERM)
                    else:adat_pozíció.terminate()
                    try:adat_pozíció.wait(timeout=5)
                    except subprocess.TimeoutExpired:adat_pozíció.kill();adat_pozíció.wait()
            szelektor.close()
            for Fájl_bejegyzés in 기록들:Fájl_bejegyzés.close()
            (KR_adat/'serial.log').write_bytes(직렬입출력)
            (KR_adat/'report.json').write_text(json.dumps(ellenőrzés_jelent,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Futtatás()
