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
from نفاذ_کریں_حکم import عکس_ڈالنا_روٹ


def چلائیں():
    پیمائش_کوائف=عکس_ڈالنا_روٹ/'build/verification/remmina';پیمائش_کوائف.mkdir(parents=True,exist_ok=True)
    توثیق_رپورٹ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((عکس_ڈالنا_روٹ/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];منتخب_کنندہ=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            مجازی_ڈسپلے=shutil.which('Xvfb')
            if مجازی_ڈسپلے: سرور_قدر=[مجازی_ڈسپلے]
            else:
                뿌리파일계층=عکس_ڈالنا_روٹ.parent/'rpi4/build/rootfs'
                سرور_قدر=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def چلائیں(دلائل_لڑی,환경=None,**이름붙인인수):
                لاگ_صف=(پیمائش_کوائف/('process-%d.log'%len(기록들))).open('wb');기록들.append(لاگ_صف)
                کوائف_پوزیشن_ٹھیک_کریں=subprocess.Popen(دلائل_لڑی,env=환경,stdout=لاگ_صف,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(کوائف_پوزیشن_ٹھیک_کریں);return کوائف_پوزیشن_ٹھیک_کریں
            환경=dict(os.environ)
            for نام in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(نام,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            ڈسپلے=چلائیں(سرور_قدر+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert ڈسپلے.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            مہمان=subprocess.Popen(['python3',str(عکس_ڈالنا_روٹ/'ٹولز/نفاذ_کریں_حکم.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(مہمان);منتخب_کنندہ.register(مہمان.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,آفسٹ_قدر=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[آفسٹ_قدر:]:
                    assert مہمان.poll() is None and time.monotonic()<마감시각,직렬입출력[آفسٹ_قدر:].decode('utf-8','replace')
                    for 누름값,_ in منتخب_کنندہ.select(.1):
                        کوائف=누름값.fileobj.read(65536)
                        if کوائف:직렬입출력.extend(کوائف)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            دہانہ_نمبر=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            پروفائل=작업경로/'test.remmina'
            پروفائل.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%دہانہ_نمبر)
            چلائیں(['dbus-run-session','--','remmina','-c',str(پروفائل)],환경=환경,start_new_session=True)
            def 가상입력도구(*دلائل_لڑی):return subprocess.check_output(['xdotool']+list(دلائل_لڑی),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;ونڈو=None
            while time.monotonic()<마감시각:
                تلاش_پیمائش=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if تلاش_پیمائش.returncode==0:
                    후보=تلاش_پیمائش.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    مرکوز=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if مرکوز.returncode==0:ونڈو=후보;break
                time.sleep(.1)
            assert ونڈو,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',ونڈو,'280','240','click','1')
            time.sleep(1)
            def 글자입력(متن):가상입력도구('type','--clearmodifiers','--delay','50',متن)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            آفسٹ_قدر=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),آفسٹ_قدر)
            آفسٹ_قدر=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),آفسٹ_قدر)
            آفسٹ_قدر=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 کلید_قدر, Shift+Space 또는 F9'.encode(),آفسٹ_قدر);기다리기(b'jkoros-native> ',آفسٹ_قدر)
            آفسٹ_قدر=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),آفسٹ_قدر)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',ونڈو,str(پیمائش_کوائف/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',آفسٹ_قدر)
            # اصل_کوائف Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            ڈرائنگ_قدر=Image.open(str(پیمائش_کوائف/'remmina-korean.png')).convert('RGB')
            عنوان_بار=None
            for عمودی_پوزیشن_ٹھیک_کریں in range(ڈرائنگ_قدر.height):
                가로들=[가로 for 가로 in range(ڈرائنگ_قدر.width) if ڈرائنگ_قدر.getpixel((가로,عمودی_پوزیشن_ٹھیک_کریں))==(32,80,144)]
                if len(가로들)>=500:عنوان_بار=(min(가로들),عمودی_پوزیشن_ٹھیک_کریں);break
            assert عنوان_بار,'native terminal title bar not found'
            가로,عمودی_پوزیشن_ٹھیک_کریں=عنوان_بار[0]+564,عنوان_بار[1]+356
            가상입력도구('mousemove','--window',ونڈو,str(가로),str(عمودی_پوزیشن_ٹھیک_کریں))
            def 화상기다리기(نام,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',ونڈو,str(پیمائش_کوائف/نام)])
                    بِٹ_میپ_نقش=Image.open(str(پیمائش_کوائف/نام)).convert('RGB')
                    if all(بِٹ_میپ_نقش.getpixel(مقام)==빛 for مقام,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+نام
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,عمودی_پوزیشن_ٹھیک_کریں-7),(255,255,255)),((가로+7,عمودی_پوزیشن_ٹھیک_کریں+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',ونڈو,str(가로-120),str(عمودی_پوزیشن_ٹھیک_کریں-80),'mouseup','1')
            time.sleep(.4)
            آفسٹ_قدر=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',آفسٹ_قدر)
            가상입력도구('mousemove','--window',ونڈو,'500','45')
            화상기다리기('remmina-resized.png',[
                ((عنوان_بار[0]+447,عنوان_بار[1]+279),(39,49,64)),((가로,عمودی_پوزیشن_ٹھیک_کریں),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            توثیق_رپورٹ.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not توثیق_رپورٹ['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(پیمائش_کوائف/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for کوائف_پوزیشن_ٹھیک_کریں in reversed(실행과정들):
                if کوائف_پوزیشن_ٹھیک_کریں.poll() is None:
                    if کوائف_پوزیشن_ٹھیک_کریں.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(کوائف_پوزیشن_ٹھیک_کریں.pid,signal.SIGTERM)
                    else:کوائف_پوزیشن_ٹھیک_کریں.terminate()
                    try:کوائف_پوزیشن_ٹھیک_کریں.wait(timeout=5)
                    except subprocess.TimeoutExpired:کوائف_پوزیشن_ٹھیک_کریں.kill();کوائف_پوزیشن_ٹھیک_کریں.wait()
            منتخب_کنندہ.close()
            for فائل_اندراج in 기록들:فائل_اندراج.close()
            (پیمائش_کوائف/'serial.log').write_bytes(직렬입출력)
            (پیمائش_کوائف/'report.json').write_text(json.dumps(توثیق_رپورٹ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':چلائیں()
