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
from ئىجرا_قىلىش_بۇيرۇق import كۆرسىتىش_يىلتىز


def ئىجرا_قىل_2():
    ئۆلچەم_مەلۇمات=كۆرسىتىش_يىلتىز/'build/verification/remmina';ئۆلچەم_مەلۇمات.mkdir(parents=True,exist_ok=True)
    دەلىللەش_خەۋەر={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((كۆرسىتىش_يىلتىز/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];تاللىغۇچ=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            مەۋھۇم_كۆرسەتكۈچ=shutil.which('Xvfb')
            if مەۋھۇم_كۆرسەتكۈچ: مۇلازىمىتېر_قىممىتى=[مەۋھۇم_كۆرسەتكۈچ]
            else:
                뿌리파일계층=كۆرسىتىش_يىلتىز.parent/'rpi4/build/rootfs'
                مۇلازىمىتېر_قىممىتى=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def ئىجرا_قىل_2(دەلىل_رەت,환경=None,**이름붙인인수):
                خاتىرە_قۇر=(ئۆلچەم_مەلۇمات/('process-%d.log'%len(기록들))).open('wb');기록들.append(خاتىرە_قۇر)
                مەلۇمات_ئورۇنلاشتۇرۇش=subprocess.Popen(دەلىل_رەت,env=환경,stdout=خاتىرە_قۇر,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(مەلۇمات_ئورۇنلاشتۇرۇش);return مەلۇمات_ئورۇنلاشتۇرۇش
            환경=dict(os.environ)
            for ئاتى in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(ئاتى,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            كۆرسەتكۈچ=ئىجرا_قىل_2(مۇلازىمىتېر_قىممىتى+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert كۆرسەتكۈچ.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            مېھمان=subprocess.Popen(['python3',str(كۆرسىتىش_يىلتىز/'قوراللار/ئىجرا_قىلىش_بۇيرۇق.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(مېھمان);تاللىغۇچ.register(مېھمان.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,ئاغما_قىممىتى=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[ئاغما_قىممىتى:]:
                    assert مېھمان.poll() is None and time.monotonic()<마감시각,직렬입출력[ئاغما_قىممىتى:].decode('utf-8','replace')
                    for 누름값,_ in تاللىغۇچ.select(.1):
                        مەلۇمات=누름값.fileobj.read(65536)
                        if مەلۇمات:직렬입출력.extend(مەلۇمات)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            ئارخىپ_1c9b560a=작업경로/'test.remmina'
            ئارخىپ_1c9b560a.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%접속번호)
            ئىجرا_قىل_2(['dbus-run-session','--','remmina','-c',str(ئارخىپ_1c9b560a)],환경=환경,start_new_session=True)
            def 가상입력도구(*دەلىل_رەت):return subprocess.check_output(['xdotool']+list(دەلىل_رەت),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;كۆزنەك=None
            while time.monotonic()<마감시각:
                ئىزدەش_ئۆلچەم=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if ئىزدەش_ئۆلچەم.returncode==0:
                    후보=ئىزدەش_ئۆلچەم.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    نۇقتىلىق=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if نۇقتىلىق.returncode==0:كۆزنەك=후보;break
                time.sleep(.1)
            assert كۆزنەك,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',كۆزنەك,'280','240','click','1')
            time.sleep(1)
            def 글자입력(تېكىست):가상입력도구('type','--clearmodifiers','--delay','50',تېكىست)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            ئاغما_قىممىتى=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ئاغما_قىممىتى)
            ئاغما_قىممىتى=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),ئاغما_قىممىتى)
            ئاغما_قىممىتى=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 ئاچقۇچ_قىممىتى, Shift+Space 또는 F9'.encode(),ئاغما_قىممىتى);기다리기(b'jkoros-native> ',ئاغما_قىممىتى)
            ئاغما_قىممىتى=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),ئاغما_قىممىتى)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',كۆزنەك,str(ئۆلچەم_مەلۇمات/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',ئاغما_قىممىتى)
            # ھەقىقىي_مەلۇمات Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            سىزىش_قىممىتى=Image.open(str(ئۆلچەم_مەلۇمات/'remmina-korean.png')).convert('RGB')
            تېما_بالدىقى=None
            for تىك_ئورۇنلاشتۇرۇش in range(سىزىش_قىممىتى.height):
                가로들=[가로 for 가로 in range(سىزىش_قىممىتى.width) if سىزىش_قىممىتى.getpixel((가로,تىك_ئورۇنلاشتۇرۇش))==(32,80,144)]
                if len(가로들)>=500:تېما_بالدىقى=(min(가로들),تىك_ئورۇنلاشتۇرۇش);break
            assert تېما_بالدىقى,'native terminal title bar not found'
            가로,تىك_ئورۇنلاشتۇرۇش=تېما_بالدىقى[0]+564,تېما_بالدىقى[1]+356
            가상입력도구('mousemove','--window',كۆزنەك,str(가로),str(تىك_ئورۇنلاشتۇرۇش))
            def 화상기다리기(ئاتى,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',كۆزنەك,str(ئۆلچەم_مەلۇمات/ئاتى)])
                    چېكىتلىك_تەسۋىر_رەسىم=Image.open(str(ئۆلچەم_مەلۇمات/ئاتى)).convert('RGB')
                    if all(چېكىتلىك_تەسۋىر_رەسىم.getpixel(ئورۇن)==빛 for ئورۇن,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+ئاتى
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,تىك_ئورۇنلاشتۇرۇش-7),(255,255,255)),((가로+7,تىك_ئورۇنلاشتۇرۇش+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',كۆزنەك,str(가로-120),str(تىك_ئورۇنلاشتۇرۇش-80),'mouseup','1')
            time.sleep(.4)
            ئاغما_قىممىتى=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',ئاغما_قىممىتى)
            가상입력도구('mousemove','--window',كۆزنەك,'500','45')
            화상기다리기('remmina-resized.png',[
                ((تېما_بالدىقى[0]+447,تېما_بالدىقى[1]+279),(39,49,64)),((가로,تىك_ئورۇنلاشتۇرۇش),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            دەلىللەش_خەۋەر.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not دەلىللەش_خەۋەر['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(ئۆلچەم_مەلۇمات/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for مەلۇمات_ئورۇنلاشتۇرۇش in reversed(실행과정들):
                if مەلۇمات_ئورۇنلاشتۇرۇش.poll() is None:
                    if مەلۇمات_ئورۇنلاشتۇرۇش.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(مەلۇمات_ئورۇنلاشتۇرۇش.pid,signal.SIGTERM)
                    else:مەلۇمات_ئورۇنلاشتۇرۇش.terminate()
                    try:مەلۇمات_ئورۇنلاشتۇرۇش.wait(timeout=5)
                    except subprocess.TimeoutExpired:مەلۇمات_ئورۇنلاشتۇرۇش.kill();مەلۇمات_ئورۇنلاشتۇرۇش.wait()
            تاللىغۇچ.close()
            for ھۆججەت_كىرگۈزۈش in 기록들:ھۆججەت_كىرگۈزۈش.close()
            (ئۆلچەم_مەلۇمات/'serial.log').write_bytes(직렬입출력)
            (ئۆلچەم_مەلۇمات/'report.json').write_text(json.dumps(دەلىللەش_خەۋەر,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ئىجرا_قىل_2()
