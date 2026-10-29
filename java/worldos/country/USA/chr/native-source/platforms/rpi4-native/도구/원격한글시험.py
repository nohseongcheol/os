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
from ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ import 기준


def ᎠᎢᏎᏍᏗ():
    결과자료=기준/'build/verification/remmina';결과자료.mkdir(parents=True,exist_ok=True)
    ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];ᎠᏑᏰᏍᎩ=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            ᎠᏓᏅᏙ_ᎢᏳᏍᏗ_ᎬᏂᎨᏒ_ᏅᎦ=shutil.which('Xvfb')
            if ᎠᏓᏅᏙ_ᎢᏳᏍᏗ_ᎬᏂᎨᏒ_ᏅᎦ: ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ=[ᎠᏓᏅᏙ_ᎢᏳᏍᏗ_ᎬᏂᎨᏒ_ᏅᎦ]
            else:
                뿌리파일계층=기준.parent/'rpi4/build/rootfs'
                ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def ᎠᎢᏎᏍᏗ(ᏗᏓᎦᏘᎸᏍᏗ_array,환경=None,**이름붙인인수):
                ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ=(결과자료/('process-%d.log'%len(기록들))).open('wb');기록들.append(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
                자료위치=subprocess.Popen(ᏗᏓᎦᏘᎸᏍᏗ_array,env=환경,stdout=ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(자료위치);return 자료위치
            환경=dict(os.environ)
            for ᏚᏙᎥᎢ in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(ᏚᏙᎥᎢ,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            ᎬᏂᎨᏒ_ᏱᎬᏁᏗᎢ=ᎠᎢᏎᏍᏗ(ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert ᎬᏂᎨᏒ_ᏱᎬᏁᏗᎢ.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            ᎠᏓᏩᏛᎯᏙᎯ=subprocess.Popen(['python3',str(기준/'도구/ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(ᎠᏓᏩᏛᎯᏙᎯ);ᎠᏑᏰᏍᎩ.register(ᎠᏓᏩᏛᎯᏙᎯ.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,변위=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[변위:]:
                    assert ᎠᏓᏩᏛᎯᏙᎯ.poll() is None and time.monotonic()<마감시각,직렬입출력[변위:].decode('utf-8','replace')
                    for 누름값,_ in ᎠᏑᏰᏍᎩ.select(.1):
                        ᎦᏟᏌᏅᎯ=누름값.fileobj.read(65536)
                        if ᎦᏟᏌᏅᎯ:직렬입출력.extend(ᎦᏟᏌᏅᎯ)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            ᎬᏗᏍᎩ_ᏄᏍᏗᏓᏅᎢ=작업경로/'test.remmina'
            ᎬᏗᏍᎩ_ᏄᏍᏗᏓᏅᎢ.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%접속번호)
            ᎠᎢᏎᏍᏗ(['dbus-run-session','--','remmina','-c',str(ᎬᏗᏍᎩ_ᏄᏍᏗᏓᏅᎢ)],환경=환경,start_new_session=True)
            def 가상입력도구(*ᏗᏓᎦᏘᎸᏍᏗ_array):return subprocess.check_output(['xdotool']+list(ᏗᏓᎦᏘᎸᏍᏗ_array),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;ᏦᎳᏂ=None
            while time.monotonic()<마감시각:
                찾은결과=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if 찾은결과.returncode==0:
                    후보=찾은결과.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    초점요소=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if 초점요소.returncode==0:ᏦᎳᏂ=후보;break
                time.sleep(.1)
            assert ᏦᎳᏂ,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',ᏦᎳᏂ,'280','240','click','1')
            time.sleep(1)
            def 글자입력(ᎠᎪᎵᏰᏗ):가상입력도구('type','--clearmodifiers','--delay','50',ᎠᎪᎵᏰᏗ)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            변위=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),변위)
            변위=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),변위)
            변위=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ, Shift+Space 또는 F9'.encode(),변위);기다리기(b'jkoros-native> ',변위)
            변위=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),변위)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',ᏦᎳᏂ,str(결과자료/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',변위)
            # ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ=Image.open(str(결과자료/'remmina-korean.png')).convert('RGB')
            ᎦᎸᎳᏗ_ᎦᎾᎸᎢ=None
            for 세로 in range(ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ.height):
                가로들=[가로 for 가로 in range(ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ.width) if ᎠᏍᏓᏅᎿᏂᏙᎸ_ᏧᎬᏩᎶᏗᏯ.getpixel((가로,세로))==(32,80,144)]
                if len(가로들)>=500:ᎦᎸᎳᏗ_ᎦᎾᎸᎢ=(min(가로들),세로);break
            assert ᎦᎸᎳᏗ_ᎦᎾᎸᎢ,'native terminal title bar not found'
            가로,세로=ᎦᎸᎳᏗ_ᎦᎾᎸᎢ[0]+564,ᎦᎸᎳᏗ_ᎦᎾᎸᎢ[1]+356
            가상입력도구('mousemove','--window',ᏦᎳᏂ,str(가로),str(세로))
            def 화상기다리기(ᏚᏙᎥᎢ,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',ᏦᎳᏂ,str(결과자료/ᏚᏙᎥᎢ)])
                    bitmap_ᎤᏓᏴᎳᏛ=Image.open(str(결과자료/ᏚᏙᎥᎢ)).convert('RGB')
                    if all(bitmap_ᎤᏓᏴᎳᏛ.getpixel(위치)==빛 for 위치,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+ᏚᏙᎥᎢ
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,세로-7),(255,255,255)),((가로+7,세로+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',ᏦᎳᏂ,str(가로-120),str(세로-80),'mouseup','1')
            time.sleep(.4)
            변위=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',변위)
            가상입력도구('mousemove','--window',ᏦᎳᏂ,'500','45')
            화상기다리기('remmina-resized.png',[
                ((ᎦᎸᎳᏗ_ᎦᎾᎸᎢ[0]+447,ᎦᎸᎳᏗ_ᎦᎾᎸᎢ[1]+279),(39,49,64)),((가로,세로),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(결과자료/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for 자료위치 in reversed(실행과정들):
                if 자료위치.poll() is None:
                    if 자료위치.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(자료위치.pid,signal.SIGTERM)
                    else:자료위치.terminate()
                    try:자료위치.wait(timeout=5)
                    except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            ᎠᏑᏰᏍᎩ.close()
            for ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ in 기록들:ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ.close()
            (결과자료/'serial.log').write_bytes(직렬입출력)
            (결과자료/'report.json').write_text(json.dumps(ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ᎠᎢᏎᏍᏗ()
