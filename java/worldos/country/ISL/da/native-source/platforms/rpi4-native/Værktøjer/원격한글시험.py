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
from Udfør_kommando import To_do_rod


def Kør_2():
    KR_data=To_do_rod/'build/verification/remmina';KR_data.mkdir(parents=True,exist_ok=True)
    validering_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((To_do_rod/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];selektor=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            virtuel_vise=shutil.which('Xvfb')
            if virtuel_vise: server_VÆRDI=[virtuel_vise]
            else:
                뿌리파일계층=To_do_rod.parent/'rpi4/build/rootfs'
                server_VÆRDI=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Kør_2(argument_MATRIX,miljø=None,**navngivet_argument):
                LOG_post=(KR_data/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_post)
                data_placere=subprocess.Popen(argument_MATRIX,env=miljø,stdout=LOG_post,stderr=subprocess.STDOUT,**navngivet_argument)
                실행과정들.append(data_placere);return data_placere
            miljø=dict(os.environ)
            for Navn in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):miljø.pop(Navn,None)
            miljø.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(vare_TÆL for vare_TÆL in range(80,200) if not Path('/tmp/.X11-unix/X'+str(vare_TÆL)).exists() and not Path('/tmp/.X%d-lock'%vare_TÆL).exists())
            miljø['DISPLAY']=':'+str(수치)
            skærm=Kør_2(server_VÆRDI+[miljø['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],miljø=miljø)
            deadline_TID=time.monotonic()+30
            while True:
                assert skærm.poll() is None and time.monotonic()<deadline_TID,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=miljø,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            gæst=subprocess.Popen(['python3',str(To_do_rod/'Værktøjer/Udfør_kommando.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(gæst);selektor.register(gæst.stdout,selectors.EVENT_READ)
            def 기다리기(mærke,FORSKYDNING_VÆRDI=0):
                deadline_TID=time.monotonic()+45
                while mærke not in 직렬입출력[FORSKYDNING_VÆRDI:]:
                    assert gæst.poll() is None and time.monotonic()<deadline_TID,직렬입출력[FORSKYDNING_VÆRDI:].decode('utf-8','replace')
                    for 누름값,_ in selektor.select(.1):
                        data=누름값.fileobj.read(65536)
                        if data:직렬입출력.extend(data)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            portnummer=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profil=작업경로/'test.remmina'
            Profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%portnummer)
            Kør_2(['dbus-run-session','--','remmina','-c',str(Profil)],miljø=miljø,start_new_session=True)
            def virtuel_input_værktøj(*argument_MATRIX):return subprocess.check_output(['xdotool']+list(argument_MATRIX),env=miljø,stderr=subprocess.STDOUT)
            deadline_TID=time.monotonic()+60;Vindue=None
            while time.monotonic()<deadline_TID:
                SØG_KR=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=miljø,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if SØG_KR.returncode==0:
                    후보=SØG_KR.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Fokuseret=subprocess.run(['xdotool','windowfocus','--sync',후보],env=miljø,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Fokuseret.returncode==0:Vindue=후보;break
                time.sleep(.1)
            assert Vindue,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            virtuel_input_værktøj('mousemove','--window',Vindue,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Tekst):virtuel_input_værktøj('type','--clearmodifiers','--delay','50',Tekst)
            def 누름값(*누름열):virtuel_input_værktøj('key','--clearmodifiers',*누름열)
            FORSKYDNING_VÆRDI=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),FORSKYDNING_VÆRDI)
            FORSKYDNING_VÆRDI=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),FORSKYDNING_VÆRDI)
            FORSKYDNING_VÆRDI=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/nul_operand tast_VÆRDI, Shift+Space 또는 F9'.encode(),FORSKYDNING_VÆRDI);기다리기(b'jkoros-native> ',FORSKYDNING_VÆRDI)
            FORSKYDNING_VÆRDI=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),FORSKYDNING_VÆRDI)
            subprocess.check_call(['import','-display',miljø['DISPLAY'],'-window',Vindue,str(KR_data/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',FORSKYDNING_VÆRDI)
            # faktisk_data Remmina의 skærmbillede 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            tegning_VÆRDI=Image.open(str(KR_data/'remmina-korean.png')).convert('RGB')
            titellinje=None
            for Lodret_placere in range(tegning_VÆRDI.height):
                가로들=[가로 for 가로 in range(tegning_VÆRDI.width) if tegning_VÆRDI.getpixel((가로,Lodret_placere))==(32,80,144)]
                if len(가로들)>=500:titellinje=(min(가로들),Lodret_placere);break
            assert titellinje,'native terminal title bar not found'
            가로,Lodret_placere=titellinje[0]+564,titellinje[1]+356
            virtuel_input_værktøj('mousemove','--window',Vindue,str(가로),str(Lodret_placere))
            def 화상기다리기(Navn,점들):
                deadline_VÆRDI=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',miljø['DISPLAY'],'-window',Vindue,str(KR_data/Navn)])
                    bitmap_Image=Image.open(str(KR_data/Navn)).convert('RGB')
                    if all(bitmap_Image.getpixel(Placering)==빛 for Placering,빛 in 점들):return
                    assert time.monotonic()<deadline_VÆRDI,'Remmina framebuffer did not settle: '+Navn
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Lodret_placere-7),(255,255,255)),((가로+7,Lodret_placere+7),(255,255,255))])
            virtuel_input_værktøj('mousedown','1','mousemove','--window',Vindue,str(가로-120),str(Lodret_placere-80),'mouseup','1')
            time.sleep(.4)
            FORSKYDNING_VÆRDI=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',FORSKYDNING_VÆRDI)
            virtuel_input_værktøj('mousemove','--window',Vindue,'500','45')
            화상기다리기('remmina-resized.png',[
                ((titellinje[0]+447,titellinje[1]+279),(39,49,64)),((가로,Lodret_placere),(24,32,48))])
            if shutil.which('dpkg-query'):
                versionsnummer=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                versionsnummer=subprocess.check_output(['remmina','--version'],env=miljø,stderr=subprocess.STDOUT).decode('utf-8','replace')
            validering_rapport.update(passed=True,display=miljø['DISPLAY'],remmina_version=versionsnummer,
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
            for data_placere in reversed(실행과정들):
                if data_placere.poll() is None:
                    if data_placere.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(data_placere.pid,signal.SIGTERM)
                    else:data_placere.terminate()
                    try:data_placere.wait(timeout=5)
                    except subprocess.TimeoutExpired:data_placere.kill();data_placere.wait()
            selektor.close()
            for fil_post in 기록들:fil_post.close()
            (KR_data/'serial.log').write_bytes(직렬입출력)
            (KR_data/'report.json').write_text(json.dumps(validering_rapport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Kør_2()
