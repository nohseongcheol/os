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
from নিষ্পাদন_আদেশ import 기준


def সঞ্চালন():
    পৰিমাপ_ডাটা=기준/'build/verification/remmina';পৰিমাপ_ডাটা.mkdir(parents=True,exist_ok=True)
    বৈধতা_ৰিপ_ৰ্ট={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];চয়নকাৰী=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            ভাৰ্ছুৱেল_প্রদর্শন=shutil.which('Xvfb')
            if ভাৰ্ছুৱেল_প্রদর্শন: ছাৰ্ভাৰ_মান=[ভাৰ্ছুৱেল_প্রদর্শন]
            else:
                뿌리파일계층=기준.parent/'rpi4/build/rootfs'
                ছাৰ্ভাৰ_মান=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def সঞ্চালন(যুক্তি_শৃঙ্খলা,환경=None,**이름붙인인수):
                লগ_শাৰী=(পৰিমাপ_ডাটা/('process-%d.log'%len(기록들))).open('wb');기록들.append(লগ_শাৰী)
                ডাটা_স্থান_সলনি_কৰক=subprocess.Popen(যুক্তি_শৃঙ্খলা,env=환경,stdout=লগ_শাৰী,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(ডাটা_স্থান_সলনি_কৰক);return ডাটা_স্থান_সলনি_কৰক
            환경=dict(os.environ)
            for নাম in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(নাম,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            প্রদর্শন=সঞ্চালন(ছাৰ্ভাৰ_মান+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert প্রদর্শন.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            অতিথি=subprocess.Popen(['python3',str(기준/'সঁজুলিসমূহ/নিষ্পাদন_আদেশ.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(অতিথি);চয়নকাৰী.register(অতিথি.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,অফছেট_মান=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[অফছেট_মান:]:
                    assert অতিথি.poll() is None and time.monotonic()<마감시각,직렬입출력[অফছেট_মান:].decode('utf-8','replace')
                    for 누름값,_ in চয়নকাৰী.select(.1):
                        ডাটা=누름값.fileobj.read(65536)
                        if ডাটা:직렬입출력.extend(ডাটা)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            প্ৰ_ফাইল=작업경로/'test.remmina'
            প্ৰ_ফাইল.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%접속번호)
            সঞ্চালন(['dbus-run-session','--','remmina','-c',str(প্ৰ_ফাইল)],환경=환경,start_new_session=True)
            def 가상입력도구(*যুক্তি_শৃঙ্খলা):return subprocess.check_output(['xdotool']+list(যুক্তি_শৃঙ্খলা),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;উইণ্ড=None
            while time.monotonic()<마감시각:
                অনুসন্ধান_পৰিমাপ=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if অনুসন্ধান_পৰিমাপ.returncode==0:
                    후보=অনুসন্ধান_পৰিমাপ.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    দৃষ্টি_নিবদ্ধ=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if দৃষ্টি_নিবদ্ধ.returncode==0:উইণ্ড=후보;break
                time.sleep(.1)
            assert উইণ্ড,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',উইণ্ড,'280','240','click','1')
            time.sleep(1)
            def 글자입력(টেক্সট):가상입력도구('type','--clearmodifiers','--delay','50',টেক্সট)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            অফছেট_মান=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),অফছেট_মান)
            অফছেট_মান=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),অফছেট_মান)
            অফছেট_মান=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 কী_মান, Shift+Space 또는 F9'.encode(),অফছেট_মান);기다리기(b'jkoros-native> ',অফছেট_মান)
            অফছেট_মান=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),অফছেট_মান)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',উইণ্ড,str(পৰিমাপ_ডাটা/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',অফছেট_মান)
            # প্ৰকৃত_ডাটা Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            অংকন_মান=Image.open(str(পৰিমাপ_ডাটা/'remmina-korean.png')).convert('RGB')
            শীৰ্ষক_দণ্ডিকা=None
            for উলম্ব_স্থান_সলনি_কৰক in range(অংকন_মান.height):
                가로들=[가로 for 가로 in range(অংকন_মান.width) if অংকন_মান.getpixel((가로,উলম্ব_স্থান_সলনি_কৰক))==(32,80,144)]
                if len(가로들)>=500:শীৰ্ষক_দণ্ডিকা=(min(가로들),উলম্ব_স্থান_সলনি_কৰক);break
            assert শীৰ্ষক_দণ্ডিকা,'native terminal title bar not found'
            가로,উলম্ব_স্থান_সলনি_কৰক=শীৰ্ষক_দণ্ডিকা[0]+564,শীৰ্ষক_দণ্ডিকা[1]+356
            가상입력도구('mousemove','--window',উইণ্ড,str(가로),str(উলম্ব_স্থান_সলনি_কৰক))
            def 화상기다리기(নাম,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',উইণ্ড,str(পৰিমাপ_ডাটা/নাম)])
                    বিটমেপ_ছবি=Image.open(str(পৰিমাপ_ডাটা/নাম)).convert('RGB')
                    if all(বিটমেপ_ছবি.getpixel(অৱস্থান)==빛 for অৱস্থান,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+নাম
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,উলম্ব_স্থান_সলনি_কৰক-7),(255,255,255)),((가로+7,উলম্ব_স্থান_সলনি_কৰক+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',উইণ্ড,str(가로-120),str(উলম্ব_স্থান_সলনি_কৰক-80),'mouseup','1')
            time.sleep(.4)
            অফছেট_মান=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',অফছেট_মান)
            가상입력도구('mousemove','--window',উইণ্ড,'500','45')
            화상기다리기('remmina-resized.png',[
                ((শীৰ্ষক_দণ্ডিকা[0]+447,শীৰ্ষক_দণ্ডিকা[1]+279),(39,49,64)),((가로,উলম্ব_স্থান_সলনি_কৰক),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            বৈধতা_ৰিপ_ৰ্ট.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not বৈধতা_ৰিপ_ৰ্ট['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(পৰিমাপ_ডাটা/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for ডাটা_স্থান_সলনি_কৰক in reversed(실행과정들):
                if ডাটা_স্থান_সলনি_কৰক.poll() is None:
                    if ডাটা_স্থান_সলনি_কৰক.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(ডাটা_স্থান_সলনি_কৰক.pid,signal.SIGTERM)
                    else:ডাটা_স্থান_সলনি_কৰক.terminate()
                    try:ডাটা_স্থান_সলনি_কৰক.wait(timeout=5)
                    except subprocess.TimeoutExpired:ডাটা_স্থান_সলনি_কৰক.kill();ডাটা_স্থান_সলনি_কৰক.wait()
            চয়নকাৰী.close()
            for ফাইল_প্রবিষ্ট in 기록들:ফাইল_প্রবিষ্ট.close()
            (পৰিমাপ_ডাটা/'serial.log').write_bytes(직렬입출력)
            (পৰিমাপ_ডাটা/'report.json').write_text(json.dumps(বৈধতা_ৰিপ_ৰ্ট,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':সঞ্চালন()
