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
from keyra_skipun import verk_rót


def Keyra_2():
    mæld_stærð_gögn=verk_rót/'build/verification/remmina';mæld_stærð_gögn.mkdir(parents=True,exist_ok=True)
    prófun_skrá={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((verk_rót/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];val=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            sýndar_birta=shutil.which('Xvfb')
            if sýndar_birta: þjónn_VALUE=[sýndar_birta]
            else:
                뿌리파일계층=verk_rót.parent/'rpi4/build/rootfs'
                þjónn_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Keyra_2(frumbreyta_ARRAY,환경=None,**이름붙인인수):
                LOG_lína=(mæld_stærð_gögn/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_lína)
                gögn_staða=subprocess.Popen(frumbreyta_ARRAY,env=환경,stdout=LOG_lína,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(gögn_staða);return gögn_staða
            환경=dict(os.environ)
            for Heiti in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Heiti,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(vara_COUNT for vara_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(vara_COUNT)).exists() and not Path('/tmp/.X%d-lock'%vara_COUNT).exists())
            환경['DISPLAY']=':'+str(수치)
            skjár=Keyra_2(þjónn_VALUE+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert skjár.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            gestur=subprocess.Popen(['python3',str(verk_rót/'Verkfæri/keyra_skipun.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(gestur);val.register(gestur.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,OFFSET_VALUE=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[OFFSET_VALUE:]:
                    assert gestur.poll() is None and time.monotonic()<마감시각,직렬입출력[OFFSET_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in val.select(.1):
                        gögn=누름값.fileobj.read(65536)
                        if gögn:직렬입출력.extend(gögn)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            tengisnúmer=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            prófíll=작업경로/'test.remmina'
            prófíll.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%tengisnúmer)
            Keyra_2(['dbus-run-session','--','remmina','-c',str(prófíll)],환경=환경,start_new_session=True)
            def 가상입력도구(*frumbreyta_ARRAY):return subprocess.check_output(['xdotool']+list(frumbreyta_ARRAY),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;Gluggi=None
            while time.monotonic()<마감시각:
                Leit_mæld_stærð=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Leit_mæld_stærð.returncode==0:
                    후보=Leit_mæld_stærð.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Forgangur=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Forgangur.returncode==0:Gluggi=후보;break
                time.sleep(.1)
            assert Gluggi,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',Gluggi,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Texti):가상입력도구('type','--clearmodifiers','--delay','50',Texti)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 Lykill_VALUE, Shift+Space 또는 F9'.encode(),OFFSET_VALUE);기다리기(b'jkoros-native> ',OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),OFFSET_VALUE)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Gluggi,str(mæld_stærð_gögn/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',OFFSET_VALUE)
            # raun_gögn Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            teikning_VALUE=Image.open(str(mæld_stærð_gögn/'remmina-korean.png')).convert('RGB')
            titilstika=None
            for Lóðrétt_staða in range(teikning_VALUE.height):
                가로들=[가로 for 가로 in range(teikning_VALUE.width) if teikning_VALUE.getpixel((가로,Lóðrétt_staða))==(32,80,144)]
                if len(가로들)>=500:titilstika=(min(가로들),Lóðrétt_staða);break
            assert titilstika,'native terminal title bar not found'
            가로,Lóðrétt_staða=titilstika[0]+564,titilstika[1]+356
            가상입력도구('mousemove','--window',Gluggi,str(가로),str(Lóðrétt_staða))
            def 화상기다리기(Heiti,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Gluggi,str(mæld_stærð_gögn/Heiti)])
                    punktamynd_mynd=Image.open(str(mæld_stærð_gögn/Heiti)).convert('RGB')
                    if all(punktamynd_mynd.getpixel(Staðsetning)==빛 for Staðsetning,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+Heiti
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Lóðrétt_staða-7),(255,255,255)),((가로+7,Lóðrétt_staða+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',Gluggi,str(가로-120),str(Lóðrétt_staða-80),'mouseup','1')
            time.sleep(.4)
            OFFSET_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',OFFSET_VALUE)
            가상입력도구('mousemove','--window',Gluggi,'500','45')
            화상기다리기('remmina-resized.png',[
                ((titilstika[0]+447,titilstika[1]+279),(39,49,64)),((가로,Lóðrétt_staða),(24,32,48))])
            if shutil.which('dpkg-query'):
                útgáfa_númer=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                útgáfa_númer=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            prófun_skrá.update(passed=True,display=환경['DISPLAY'],remmina_version=útgáfa_númer,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not prófun_skrá['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(mæld_stærð_gögn/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for gögn_staða in reversed(실행과정들):
                if gögn_staða.poll() is None:
                    if gögn_staða.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(gögn_staða.pid,signal.SIGTERM)
                    else:gögn_staða.terminate()
                    try:gögn_staða.wait(timeout=5)
                    except subprocess.TimeoutExpired:gögn_staða.kill();gögn_staða.wait()
            val.close()
            for skrá_færsla_3d0c1245 in 기록들:skrá_færsla_3d0c1245.close()
            (mæld_stærð_gögn/'serial.log').write_bytes(직렬입출력)
            (mæld_stærð_gögn/'report.json').write_text(json.dumps(prófun_skrá,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Keyra_2()
