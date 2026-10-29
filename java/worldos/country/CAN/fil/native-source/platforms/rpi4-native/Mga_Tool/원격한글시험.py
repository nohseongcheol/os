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
from Mag_execute_utos import Project_root


def run():
    sukat_data=Project_root/'build/verification/remmina';sukat_data.mkdir(parents=True,exist_ok=True)
    pagpapatibay_ulat={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_root/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];tagapili=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            virtual_display=shutil.which('Xvfb')
            if virtual_display: server_VALUE=[virtual_display]
            else:
                뿌리파일계층=Project_root.parent/'rpi4/build/rootfs'
                server_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def run(argumento_ARRAY,환경=None,**이름붙인인수):
                LOG_hanay=(sukat_data/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_hanay)
                data_posisyon=subprocess.Popen(argumento_ARRAY,env=환경,stdout=LOG_hanay,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(data_posisyon);return data_posisyon
            환경=dict(os.environ)
            for pangalan in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(pangalan,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(item_COUNT for item_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(item_COUNT)).exists() and not Path('/tmp/.X%d-lock'%item_COUNT).exists())
            환경['DISPLAY']=':'+str(수치)
            display=run(server_VALUE+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert display.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            bisita=subprocess.Popen(['python3',str(Project_root/'Mga_Tool/Mag_execute_utos.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(bisita);tagapili.register(bisita.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,OFFSET_VALUE=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[OFFSET_VALUE:]:
                    assert bisita.poll() is None and time.monotonic()<마감시각,직렬입출력[OFFSET_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in tagapili.select(.1):
                        data=누름값.fileobj.read(65536)
                        if data:직렬입출력.extend(data)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            numero_ng_port=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profile=작업경로/'test.remmina'
            Profile.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%numero_ng_port)
            run(['dbus-run-session','--','remmina','-c',str(Profile)],환경=환경,start_new_session=True)
            def 가상입력도구(*argumento_ARRAY):return subprocess.check_output(['xdotool']+list(argumento_ARRAY),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;window=None
            while time.monotonic()<마감시각:
                SEARCH_sukat=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if SEARCH_sukat.returncode==0:
                    후보=SEARCH_sukat.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Focused=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Focused.returncode==0:window=후보;break
                time.sleep(.1)
            assert window,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',window,'280','240','click','1')
            time.sleep(1)
            def 글자입력(SMS):가상입력도구('type','--clearmodifiers','--delay','50',SMS)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 key_VALUE, Shift+Space 또는 F9'.encode(),OFFSET_VALUE);기다리기(b'jkoros-native> ',OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),OFFSET_VALUE)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',window,str(sukat_data/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',OFFSET_VALUE)
            # totoo_data Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            iginuhit_VALUE=Image.open(str(sukat_data/'remmina-korean.png')).convert('RGB')
            bar_ng_pamagat=None
            for archive_posisyon in range(iginuhit_VALUE.height):
                가로들=[가로 for 가로 in range(iginuhit_VALUE.width) if iginuhit_VALUE.getpixel((가로,archive_posisyon))==(32,80,144)]
                if len(가로들)>=500:bar_ng_pamagat=(min(가로들),archive_posisyon);break
            assert bar_ng_pamagat,'native terminal title bar not found'
            가로,archive_posisyon=bar_ng_pamagat[0]+564,bar_ng_pamagat[1]+356
            가상입력도구('mousemove','--window',window,str(가로),str(archive_posisyon))
            def 화상기다리기(pangalan,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',window,str(sukat_data/pangalan)])
                    bitmap_IMAGE=Image.open(str(sukat_data/pangalan)).convert('RGB')
                    if all(bitmap_IMAGE.getpixel(posisyon)==빛 for posisyon,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+pangalan
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,archive_posisyon-7),(255,255,255)),((가로+7,archive_posisyon+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',window,str(가로-120),str(archive_posisyon-80),'mouseup','1')
            time.sleep(.4)
            OFFSET_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',OFFSET_VALUE)
            가상입력도구('mousemove','--window',window,'500','45')
            화상기다리기('remmina-resized.png',[
                ((bar_ng_pamagat[0]+447,bar_ng_pamagat[1]+279),(39,49,64)),((가로,archive_posisyon),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            pagpapatibay_ulat.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not pagpapatibay_ulat['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(sukat_data/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for data_posisyon in reversed(실행과정들):
                if data_posisyon.poll() is None:
                    if data_posisyon.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(data_posisyon.pid,signal.SIGTERM)
                    else:data_posisyon.terminate()
                    try:data_posisyon.wait(timeout=5)
                    except subprocess.TimeoutExpired:data_posisyon.kill();data_posisyon.wait()
            tagapili.close()
            for file_pagpasok in 기록들:file_pagpasok.close()
            (sukat_data/'serial.log').write_bytes(직렬입출력)
            (sukat_data/'report.json').write_text(json.dumps(pagpapatibay_ulat,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':run()
