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
from কার্যকর_করুন_আদেশ import প্রকল্প_মূল


def চালনা():
    পরিমাপ_ডাটা=প্রকল্প_মূল/'build/verification/remmina';পরিমাপ_ডাটা.mkdir(parents=True,exist_ok=True)
    বৈধকরণ_রিপোর্ট={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((প্রকল্প_মূল/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];নির্বাচক=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            কল্পিত_ডিসপ্লে=shutil.which('Xvfb')
            if কল্পিত_ডিসপ্লে: সার্ভার_মান=[কল্পিত_ডিসপ্লে]
            else:
                뿌리파일계층=প্রকল্প_মূল.parent/'rpi4/build/rootfs'
                সার্ভার_মান=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def চালনা(যুক্তি_অ্যারে,환경=None,**이름붙인인수):
                লগ_সারি=(পরিমাপ_ডাটা/('process-%d.log'%len(기록들))).open('wb');기록들.append(লগ_সারি)
                ডাটা_পদ=subprocess.Popen(যুক্তি_অ্যারে,env=환경,stdout=লগ_সারি,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(ডাটা_পদ);return ডাটা_পদ
            환경=dict(os.environ)
            for নাম in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(নাম,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            ডিসপ্লে=চালনা(সার্ভার_মান+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert ডিসপ্লে.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            অতিথি=subprocess.Popen(['python3',str(প্রকল্প_মূল/'সরঞ্জামগুলি/কার্যকর_করুন_আদেশ.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(অতিথি);নির্বাচক.register(অতিথি.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,অফসেট_মান=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[অফসেট_মান:]:
                    assert অতিথি.poll() is None and time.monotonic()<마감시각,직렬입출력[অফসেট_মান:].decode('utf-8','replace')
                    for 누름값,_ in নির্বাচক.select(.1):
                        ডাটা=누름값.fileobj.read(65536)
                        if ডাটা:직렬입출력.extend(ডাটা)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            পোর্ট_নম্বর=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            বিবরণী=작업경로/'test.remmina'
            বিবরণী.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%পোর্ট_নম্বর)
            চালনা(['dbus-run-session','--','remmina','-c',str(বিবরণী)],환경=환경,start_new_session=True)
            def 가상입력도구(*যুক্তি_অ্যারে):return subprocess.check_output(['xdotool']+list(যুক্তি_অ্যারে),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;উইন্ডো=None
            while time.monotonic()<마감시각:
                দেখুন_পরিমাপ=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if দেখুন_পরিমাপ.returncode==0:
                    후보=দেখুন_পরিমাপ.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    ফোকাসযুক্ত=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if ফোকাসযুক্ত.returncode==0:উইন্ডো=후보;break
                time.sleep(.1)
            assert উইন্ডো,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',উইন্ডো,'280','240','click','1')
            time.sleep(1)
            def 글자입력(পাঠ):가상입력도구('type','--clearmodifiers','--delay','50',পাঠ)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            অফসেট_মান=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),অফসেট_মান)
            অফসেট_মান=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),অফসেট_মান)
            অফসেট_মান=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 কী_মান, Shift+Space 또는 F9'.encode(),অফসেট_মান);기다리기(b'jkoros-native> ',অফসেট_মান)
            অফসেট_মান=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),অফসেট_মান)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',উইন্ডো,str(পরিমাপ_ডাটা/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',অফসেট_মান)
            # প্রকৃত_ডাটা Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            অঙ্কন_মান=Image.open(str(পরিমাপ_ডাটা/'remmina-korean.png')).convert('RGB')
            শিরোনাম_বার=None
            for উল্লম্ব_পদ in range(অঙ্কন_মান.height):
                가로들=[가로 for 가로 in range(অঙ্কন_মান.width) if অঙ্কন_মান.getpixel((가로,উল্লম্ব_পদ))==(32,80,144)]
                if len(가로들)>=500:শিরোনাম_বার=(min(가로들),উল্লম্ব_পদ);break
            assert শিরোনাম_বার,'native terminal title bar not found'
            가로,উল্লম্ব_পদ=শিরোনাম_বার[0]+564,শিরোনাম_বার[1]+356
            가상입력도구('mousemove','--window',উইন্ডো,str(가로),str(উল্লম্ব_পদ))
            def 화상기다리기(নাম,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',উইন্ডো,str(পরিমাপ_ডাটা/নাম)])
                    বিটম্যাপ_ছবি=Image.open(str(পরিমাপ_ডাটা/নাম)).convert('RGB')
                    if all(বিটম্যাপ_ছবি.getpixel(অবস্থান)==빛 for অবস্থান,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+নাম
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,উল্লম্ব_পদ-7),(255,255,255)),((가로+7,উল্লম্ব_পদ+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',উইন্ডো,str(가로-120),str(উল্লম্ব_পদ-80),'mouseup','1')
            time.sleep(.4)
            অফসেট_মান=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',অফসেট_মান)
            가상입력도구('mousemove','--window',উইন্ডো,'500','45')
            화상기다리기('remmina-resized.png',[
                ((শিরোনাম_বার[0]+447,শিরোনাম_বার[1]+279),(39,49,64)),((가로,উল্লম্ব_পদ),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            বৈধকরণ_রিপোর্ট.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not বৈধকরণ_রিপোর্ট['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(পরিমাপ_ডাটা/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for ডাটা_পদ in reversed(실행과정들):
                if ডাটা_পদ.poll() is None:
                    if ডাটা_পদ.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(ডাটা_পদ.pid,signal.SIGTERM)
                    else:ডাটা_পদ.terminate()
                    try:ডাটা_পদ.wait(timeout=5)
                    except subprocess.TimeoutExpired:ডাটা_পদ.kill();ডাটা_পদ.wait()
            নির্বাচক.close()
            for ফাইল_ভুক্তি in 기록들:ফাইল_ভুক্তি.close()
            (পরিমাপ_ডাটা/'serial.log').write_bytes(직렬입출력)
            (পরিমাপ_ডাটা/'report.json').write_text(json.dumps(বৈধকরণ_রিপোর্ট,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':চালনা()
