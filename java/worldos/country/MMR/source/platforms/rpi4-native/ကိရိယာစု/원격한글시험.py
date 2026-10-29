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
from စက်မောင်း import စီမံကိန်းအမြစ်


def လုပ်ဆောင်():
    ရလဒ်ဒေတာ=စီမံကိန်းအမြစ်/'build/verification/remmina';ရလဒ်ဒေတာ.mkdir(parents=True,exist_ok=True)
    검증기록={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((စီမံကိန်းအမြစ်/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as လုပ်ဆောင်လမ်း:
        လုပ်ဆောင်လမ်း=Path(လုပ်ဆောင်လမ်း);실행과정들=[];준비선택기=selectors.DefaultSelector();အစဉ်ဆက်အဝင်အထွက်=bytearray()
        기록들=[]
        try:
            အတုမြင်ကွင်း=shutil.which('Xvfb')
            if အတုမြင်ကွင်း: ဝန်ဆောင်စက်တန်ဖိုး=[အတုမြင်ကွင်း]
            else:
                뿌리파일계층=စီမံကိန်းအမြစ်.parent/'rpi4/build/rootfs'
                ဝန်ဆောင်စက်တန်ဖိုး=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def လုပ်ဆောင်(ပေးအချက်အခင်းအကျင်း,ဝန်းကျင်=None,**이름붙인인수):
                မှတ်တမ်းမှတ်တမ်းတစ်ခု=(ရလဒ်ဒေတာ/('process-%d.log'%len(기록들))).open('wb');기록들.append(မှတ်တမ်းမှတ်တမ်းတစ်ခု)
                ဒေတာနေရာ=subprocess.Popen(ပေးအချက်အခင်းအကျင်း,env=ဝန်းကျင်,stdout=မှတ်တမ်းမှတ်တမ်းတစ်ခု,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(ဒေတာနေရာ);return ဒေတာနေရာ
            ဝန်းကျင်=dict(os.environ)
            for အမည် in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):ဝန်းကျင်.pop(အမည်,None)
            ဝန်းကျင်.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(လုပ်ဆောင်လမ်း/'config'),XDG_DATA_HOME=str(လုပ်ဆောင်လမ်း/'data'),XDG_CACHE_HOME=str(လုပ်ဆောင်လမ်း/'cache'))
            ကိန်းဂဏန်းတန်ဖိုး=next(အရေအတွက် for အရေအတွက် in range(80,200) if not Path('/tmp/.X11-unix/X'+str(အရေအတွက်)).exists() and not Path('/tmp/.X%d-lock'%အရေအတွက်).exists())
            ဝန်းကျင်['DISPLAY']=':'+str(ကိန်းဂဏန်းတန်ဖိုး)
            မြင်ကွင်းကိရိယာ=လုပ်ဆောင်(ဝန်ဆောင်စက်တန်ဖိုး+[ဝန်းကျင်['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],ဝန်းကျင်=ဝန်းကျင်)
            마감시각=time.monotonic()+30
            while True:
                assert မြင်ကွင်းကိရိယာ.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=ဝန်းကျင်,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            ဧည့်သည်=subprocess.Popen(['python3',str(စီမံကိန်းအမြစ်/'ကိရိယာစု/စက်မောင်း.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(ဧည့်သည်);준비선택기.register(ဧည့်သည်.stdout,selectors.EVENT_READ)
            def စောင့်(확인표시,အရွေ့တန်ဖိုး=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in အစဉ်ဆက်အဝင်အထွက်[အရွေ့တန်ဖိုး:]:
                    assert ဧည့်သည်.poll() is None and time.monotonic()<마감시각,အစဉ်ဆက်အဝင်အထွက်[အရွေ့တန်ဖိုး:].decode('utf-8','replace')
                    for 누름값,_ in 준비선택기.select(.1):
                        ဒေတာ=누름값.fileobj.read(65536)
                        if ဒေတာ:အစဉ်ဆက်အဝင်အထွက်.extend(ဒေတာ)
            စောင့်(b'TERMINAL READY');စောင့်(b'jkoros-native> ',အစဉ်ဆက်အဝင်အထွက်.rfind(b'TERMINAL READY'))
            ဆက်သွယ်ပေါက်ကိန်း=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',အစဉ်ဆက်အဝင်အထွက်).group(1))
            ချိတ်ဆက်ပုံစံ=လုပ်ဆောင်လမ်း/'test.remmina'
            ချိတ်ဆက်ပုံစံ.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%ဆက်သွယ်ပေါက်ကိန်း)
            လုပ်ဆောင်(['dbus-run-session','--','remmina','-c',str(ချိတ်ဆက်ပုံစံ)],ဝန်းကျင်=ဝန်းကျင်,start_new_session=True)
            def အတုအဝင်ကိရိယာတစ်ခု(*ပေးအချက်အခင်းအကျင်း):return subprocess.check_output(['xdotool']+list(ပေးအချက်အခင်းအကျင်း),env=ဝန်းကျင်,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;ဝင်း=None
            while time.monotonic()<마감시각:
                ရလဒ်ရှာဖွေ=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=ဝန်းကျင်,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if ရလဒ်ရှာဖွေ.returncode==0:
                    အဆိုပြုချက်=ရလဒ်ရှာဖွေ.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    초점요소=subprocess.run(['xdotool','windowfocus','--sync',အဆိုပြုချက်],env=ဝန်းကျင်,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if 초점요소.returncode==0:ဝင်း=အဆိုပြုချက်;break
                time.sleep(.1)
            assert ဝင်း,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            အတုအဝင်ကိရိယာတစ်ခု('mousemove','--window',ဝင်း,'280','240','click','1')
            time.sleep(1)
            def 글자입력(စာသား):အတုအဝင်ကိရိယာတစ်ခု('type','--clearmodifiers','--delay','50',စာသား)
            def 누름값(*누름열):အတုအဝင်ကိရိယာတစ်ခု('key','--clearmodifiers',*누름열)
            အရွေ့တန်ဖိုး=len(အစဉ်ဆက်အဝင်အထွက်);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            စောင့်('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),အရွေ့တန်ဖိုး)
            အရွေ့တန်ဖိုး=len(အစဉ်ဆက်အဝင်အထွက်);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            စောင့်('\r\n과 갑사\r\njkoros-native> '.encode(),အရွေ့တန်ဖိုး)
            အရွေ့တန်ဖိုး=len(အစဉ်ဆက်အဝင်အထွက်);글자입력('help ko');누름값('Return')
            စောင့်('한/သုညတွက်ချက်ခံ သော့တန်ဖိုး, Shift+Space 또는 F9'.encode(),အရွေ့တန်ဖိုး);စောင့်(b'jkoros-native> ',အရွေ့တန်ဖိုး)
            အရွေ့တန်ဖိုး=len(အစဉ်ဆက်အဝင်အထွက်);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            စောင့်('읽'.encode(),အရွေ့တန်ဖိုး)
            subprocess.check_call(['import','-display',ဝန်းကျင်['DISPLAY'],'-window',ဝင်း,str(ရလဒ်ဒေတာ/'remmina-korean.png')])
            누름값('F9','Return')
            စောင့်(b'jkoros-native> ',အရွေ့တန်ဖိုး)
            # တကယ့်ဒေတာ Remmina의 မျက်နှာပြင် 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            ပုံဆွဲမှု=Image.open(str(ရလဒ်ဒေတာ/'remmina-korean.png')).convert('RGB')
            제목줄=None
            for ဒေါင်လိုက်တည်နေရာ in range(ပုံဆွဲမှု.height):
                가로들=[အလျားတည်နေရာ for အလျားတည်နေရာ in range(ပုံဆွဲမှု.width) if ပုံဆွဲမှု.getpixel((အလျားတည်နေရာ,ဒေါင်လိုက်တည်နေရာ))==(32,80,144)]
                if len(가로들)>=500:제목줄=(min(가로들),ဒေါင်လိုက်တည်နေရာ);break
            assert 제목줄,'native terminal title bar not found'
            အလျားတည်နေရာ,ဒေါင်လိုက်တည်နေရာ=제목줄[0]+564,제목줄[1]+356
            အတုအဝင်ကိရိယာတစ်ခု('mousemove','--window',ဝင်း,str(အလျားတည်နေရာ),str(ဒေါင်လိုက်တည်နေရာ))
            def 화상기다리기(အမည်,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',ဝန်းကျင်['DISPLAY'],'-window',ဝင်း,str(ရလဒ်ဒေတာ/အမည်)])
                    ဘစ်မြေပုံစက်ပုံရိပ်=Image.open(str(ရလဒ်ဒေတာ/အမည်)).convert('RGB')
                    if all(ဘစ်မြေပုံစက်ပုံရိပ်.getpixel(နေရာ)==အလင်း for နေရာ,အလင်း in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+အမည်
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((အလျားတည်နေရာ-7,ဒေါင်လိုက်တည်နေရာ-7),(255,255,255)),((အလျားတည်နေရာ+7,ဒေါင်လိုက်တည်နေရာ+7),(255,255,255))])
            အတုအဝင်ကိရိယာတစ်ခု('mousedown','1','mousemove','--window',ဝင်း,str(အလျားတည်နေရာ-120),str(ဒေါင်လိုက်တည်နေရာ-80),'mouseup','1')
            time.sleep(.4)
            အရွေ့တန်ဖိုး=len(အစဉ်ဆက်အဝင်အထွက်);글자입력('terminal size');누름값('Return')
            စောင့်(b'TERMINAL SIZE 53x14\r\n',အရွေ့တန်ဖိုး)
            အတုအဝင်ကိရိယာတစ်ခု('mousemove','--window',ဝင်း,'500','45')
            화상기다리기('remmina-resized.png',[
                ((제목줄[0]+447,제목줄[1]+279),(39,49,64)),((အလျားတည်နေရာ,ဒေါင်လိုက်တည်နေရာ),(24,32,48))])
            if shutil.which('dpkg-query'):
                ထုတ်ဝေမှုကိန်း=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                ထုတ်ဝေမှုကိန်း=subprocess.check_output(['remmina','--version'],env=ဝန်းကျင်,stderr=subprocess.STDOUT).decode('utf-8','replace')
            검증기록.update(passed=True,display=ဝန်းကျင်['DISPLAY'],remmina_version=ထုတ်ဝေမှုကိန်း,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not 검증기록['passed'] and 'ဝန်းကျင်' in locals() and ဝန်းကျင်.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',ဝန်းကျင်['DISPLAY'],'-window','root',str(ရလဒ်ဒေတာ/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for ဒေတာနေရာ in reversed(실행과정들):
                if ဒေတာနေရာ.poll() is None:
                    if ဒေတာနေရာ.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(ဒေတာနေရာ.pid,signal.SIGTERM)
                    else:ဒေတာနေရာ.terminate()
                    try:ဒေတာနေရာ.wait(timeout=5)
                    except subprocess.TimeoutExpired:ဒေတာနေရာ.kill();ဒေတာနေရာ.wait()
            준비선택기.close()
            for ဖိုင်အချက် in 기록들:ဖိုင်အချက်.close()
            (ရလဒ်ဒေတာ/'serial.log').write_bytes(အစဉ်ဆက်အဝင်အထွက်)
            (ရလဒ်ဒေတာ/'report.json').write_text(json.dumps(검증기록,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':လုပ်ဆောင်()
