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
from Utfør_kommando import speile_rot


def Kjør_2():
    KR_data=speile_rot/'build/verification/remmina';KR_data.mkdir(parents=True,exist_ok=True)
    validering_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((speile_rot/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];velger=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            virtuell_vise=shutil.which('Xvfb')
            if virtuell_vise: server_VERDI=[virtuell_vise]
            else:
                뿌리파일계층=speile_rot.parent/'rpi4/build/rootfs'
                server_VERDI=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Kjør_2(argument_MATRISE,miljø=None,**navngitt_argument):
                LOG_POST=(KR_data/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_POST)
                data_plassere=subprocess.Popen(argument_MATRISE,env=miljø,stdout=LOG_POST,stderr=subprocess.STDOUT,**navngitt_argument)
                실행과정들.append(data_plassere);return data_plassere
            miljø=dict(os.environ)
            for Navn in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):miljø.pop(Navn,None)
            miljø.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(vare_ANTALL for vare_ANTALL in range(80,200) if not Path('/tmp/.X11-unix/X'+str(vare_ANTALL)).exists() and not Path('/tmp/.X%d-lock'%vare_ANTALL).exists())
            miljø['DISPLAY']=':'+str(수치)
            skjerm=Kjør_2(server_VERDI+[miljø['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],miljø=miljø)
            tidsfrist_TID=time.monotonic()+30
            while True:
                assert skjerm.poll() is None and time.monotonic()<tidsfrist_TID,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=miljø,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            gjest=subprocess.Popen(['python3',str(speile_rot/'Verktøy/Utfør_kommando.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(gjest);velger.register(gjest.stdout,selectors.EVENT_READ)
            def 기다리기(tusj,FORSKYVNING_VERDI=0):
                tidsfrist_TID=time.monotonic()+45
                while tusj not in 직렬입출력[FORSKYVNING_VERDI:]:
                    assert gjest.poll() is None and time.monotonic()<tidsfrist_TID,직렬입출력[FORSKYVNING_VERDI:].decode('utf-8','replace')
                    for 누름값,_ in velger.select(.1):
                        data=누름값.fileobj.read(65536)
                        if data:직렬입출력.extend(data)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            portnummer=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profil=작업경로/'test.remmina'
            Profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%portnummer)
            Kjør_2(['dbus-run-session','--','remmina','-c',str(Profil)],miljø=miljø,start_new_session=True)
            def virtuell_inndata_verktøy(*argument_MATRISE):return subprocess.check_output(['xdotool']+list(argument_MATRISE),env=miljø,stderr=subprocess.STDOUT)
            tidsfrist_TID=time.monotonic()+60;Vindu=None
            while time.monotonic()<tidsfrist_TID:
                SØK_KR=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=miljø,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if SØK_KR.returncode==0:
                    후보=SØK_KR.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Fokus_f7e69dab=subprocess.run(['xdotool','windowfocus','--sync',후보],env=miljø,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Fokus_f7e69dab.returncode==0:Vindu=후보;break
                time.sleep(.1)
            assert Vindu,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            virtuell_inndata_verktøy('mousemove','--window',Vindu,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Tekst):virtuell_inndata_verktøy('type','--clearmodifiers','--delay','50',Tekst)
            def 누름값(*누름열):virtuell_inndata_verktøy('key','--clearmodifiers',*누름열)
            FORSKYVNING_VERDI=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),FORSKYVNING_VERDI)
            FORSKYVNING_VERDI=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),FORSKYVNING_VERDI)
            FORSKYVNING_VERDI=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/null_operand tast_VERDI, Shift+Space 또는 F9'.encode(),FORSKYVNING_VERDI);기다리기(b'jkoros-native> ',FORSKYVNING_VERDI)
            FORSKYVNING_VERDI=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),FORSKYVNING_VERDI)
            subprocess.check_call(['import','-display',miljø['DISPLAY'],'-window',Vindu,str(KR_data/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',FORSKYVNING_VERDI)
            # faktisk_data Remmina의 skjermbilde 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            tegning_VERDI=Image.open(str(KR_data/'remmina-korean.png')).convert('RGB')
            tittellinje=None
            for vertikal_plassere in range(tegning_VERDI.height):
                가로들=[가로 for 가로 in range(tegning_VERDI.width) if tegning_VERDI.getpixel((가로,vertikal_plassere))==(32,80,144)]
                if len(가로들)>=500:tittellinje=(min(가로들),vertikal_plassere);break
            assert tittellinje,'native terminal title bar not found'
            가로,vertikal_plassere=tittellinje[0]+564,tittellinje[1]+356
            virtuell_inndata_verktøy('mousemove','--window',Vindu,str(가로),str(vertikal_plassere))
            def 화상기다리기(Navn,점들):
                tidsfrist_VERDI=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',miljø['DISPLAY'],'-window',Vindu,str(KR_data/Navn)])
                    punktgrafikk_BILDE=Image.open(str(KR_data/Navn)).convert('RGB')
                    if all(punktgrafikk_BILDE.getpixel(Posisjon)==빛 for Posisjon,빛 in 점들):return
                    assert time.monotonic()<tidsfrist_VERDI,'Remmina framebuffer did not settle: '+Navn
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,vertikal_plassere-7),(255,255,255)),((가로+7,vertikal_plassere+7),(255,255,255))])
            virtuell_inndata_verktøy('mousedown','1','mousemove','--window',Vindu,str(가로-120),str(vertikal_plassere-80),'mouseup','1')
            time.sleep(.4)
            FORSKYVNING_VERDI=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',FORSKYVNING_VERDI)
            virtuell_inndata_verktøy('mousemove','--window',Vindu,'500','45')
            화상기다리기('remmina-resized.png',[
                ((tittellinje[0]+447,tittellinje[1]+279),(39,49,64)),((가로,vertikal_plassere),(24,32,48))])
            if shutil.which('dpkg-query'):
                versjonsnummer=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                versjonsnummer=subprocess.check_output(['remmina','--version'],env=miljø,stderr=subprocess.STDOUT).decode('utf-8','replace')
            validering_rapport.update(passed=True,display=miljø['DISPLAY'],remmina_version=versjonsnummer,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not validering_rapport['passed'] and 'miljø' in locals() and miljø.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',miljø['DISPLAY'],'-window','root',str(KR_data/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for data_plassere in reversed(실행과정들):
                if data_plassere.poll() is None:
                    if data_plassere.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(data_plassere.pid,signal.SIGTERM)
                    else:data_plassere.terminate()
                    try:data_plassere.wait(timeout=5)
                    except subprocess.TimeoutExpired:data_plassere.kill();data_plassere.wait()
            velger.close()
            for Fil_oppføring in 기록들:Fil_oppføring.close()
            (KR_data/'serial.log').write_bytes(직렬입출력)
            (KR_data/'report.json').write_text(json.dumps(validering_rapport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Kjør_2()
