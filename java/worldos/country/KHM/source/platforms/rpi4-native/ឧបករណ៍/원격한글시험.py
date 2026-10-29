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
from អនុវត្ត_ពាក្យបញ្ជា import បញ្ចាំង_ឬស


def រត់():
    ការវាស់វែង_ទិន្នន័យ=បញ្ចាំង_ឬស/'build/verification/remmina';ការវាស់វែង_ទិន្នន័យ.mkdir(parents=True,exist_ok=True)
    សុពលភាព_រាយការណ៍={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((បញ្ចាំង_ឬស/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];អ្នកជ្រើសរើស=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            និម្មិត_បង្ហាញ=shutil.which('Xvfb')
            if និម្មិត_បង្ហាញ: ម៉ាស៊ីនមេ_តំលៃ=[និម្មិត_បង្ហាញ]
            else:
                뿌리파일계층=បញ្ចាំង_ឬស.parent/'rpi4/build/rootfs'
                ម៉ាស៊ីនមេ_តំលៃ=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def រត់(អាគុយម៉ង់_អារេ,환경=None,**이름붙인인수):
                កំណត់_ហេតុ_ថត=(ការវាស់វែង_ទិន្នន័យ/('process-%d.log'%len(기록들))).open('wb');기록들.append(កំណត់_ហេតុ_ថត)
                ទិន្នន័យ_កំណត់ទីតាំង=subprocess.Popen(អាគុយម៉ង់_អារេ,env=환경,stdout=កំណត់_ហេតុ_ថត,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(ទិន្នន័យ_កំណត់ទីតាំង);return ទិន្នន័យ_កំណត់ទីតាំង
            환경=dict(os.environ)
            for ឈ្មោះ in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(ឈ្មោះ,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            ឧបករណ៏បង្ហាញ=រត់(ម៉ាស៊ីនមេ_តំលៃ+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert ឧបករណ៏បង្ហាញ.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            ភ្ញៀវ=subprocess.Popen(['python3',str(បញ្ចាំង_ឬស/'ឧបករណ៍/អនុវត្ត_ពាក្យបញ្ជា.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(ភ្ញៀវ);អ្នកជ្រើសរើស.register(ភ្ញៀវ.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,ការបែង_ភាគ_តំលៃ=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[ការបែង_ភាគ_តំលៃ:]:
                    assert ភ្ញៀវ.poll() is None and time.monotonic()<마감시각,직렬입출력[ការបែង_ភាគ_តំលៃ:].decode('utf-8','replace')
                    for 누름값,_ in អ្នកជ្រើសរើស.select(.1):
                        ទិន្នន័យ=누름값.fileobj.read(65536)
                        if ទិន្នន័យ:직렬입출력.extend(ទិន្នន័យ)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            លេខរន្ធ=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            ទម្រង់=작업경로/'test.remmina'
            ទម្រង់.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%លេខរន្ធ)
            រត់(['dbus-run-session','--','remmina','-c',str(ទម្រង់)],환경=환경,start_new_session=True)
            def 가상입력도구(*អាគុយម៉ង់_អារេ):return subprocess.check_output(['xdotool']+list(អាគុយម៉ង់_អារេ),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;វីនដូ=None
            while time.monotonic()<마감시각:
                រុករក_ការវាស់វែង=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if រុករក_ការវាស់វែង.returncode==0:
                    후보=រុករក_ការវាស់វែង.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    ដែលផ្តោត=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if ដែលផ្តោត.returncode==0:វីនដូ=후보;break
                time.sleep(.1)
            assert វីនដូ,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',វីនដូ,'280','240','click','1')
            time.sleep(1)
            def 글자입력(អត្ថបទ):가상입력도구('type','--clearmodifiers','--delay','50',អត្ថបទ)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            ការបែង_ភាគ_តំលៃ=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ការបែង_ភាគ_តំលៃ)
            ការបែង_ភាគ_តំលៃ=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),ការបែង_ភាគ_តំលៃ)
            ការបែង_ភាគ_តំលៃ=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 ឃី_តំលៃ, Shift+Space 또는 F9'.encode(),ការបែង_ភាគ_តំលៃ);기다리기(b'jkoros-native> ',ការបែង_ភាគ_តំលៃ)
            ការបែង_ភាគ_តំលៃ=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),ការបែង_ភាគ_តំលៃ)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',វីនដូ,str(ការវាស់វែង_ទិន្នន័យ/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',ការបែង_ភាគ_តំលៃ)
            # ដែលពិត_ទិន្នន័យ Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            ការគូរ_តំលៃ=Image.open(str(ការវាស់វែង_ទិន្នន័យ/'remmina-korean.png')).convert('RGB')
            របារចំណងជើង=None
            for បញ្ឈរ_កំណត់ទីតាំង in range(ការគូរ_តំលៃ.height):
                가로들=[가로 for 가로 in range(ការគូរ_តំលៃ.width) if ការគូរ_តំលៃ.getpixel((가로,បញ្ឈរ_កំណត់ទីតាំង))==(32,80,144)]
                if len(가로들)>=500:របារចំណងជើង=(min(가로들),បញ្ឈរ_កំណត់ទីតាំង);break
            assert របារចំណងជើង,'native terminal title bar not found'
            가로,បញ្ឈរ_កំណត់ទីតាំង=របារចំណងជើង[0]+564,របារចំណងជើង[1]+356
            가상입력도구('mousemove','--window',វីនដូ,str(가로),str(បញ្ឈរ_កំណត់ទីតាំង))
            def 화상기다리기(ឈ្មោះ,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',វីនដូ,str(ការវាស់វែង_ទិន្នន័យ/ឈ្មោះ)])
                    រូបភាព_bitmap_រូបថត=Image.open(str(ការវាស់វែង_ទិន្នន័យ/ឈ្មោះ)).convert('RGB')
                    if all(រូបភាព_bitmap_រូបថត.getpixel(កំណត់ទីតាំង)==빛 for កំណត់ទីតាំង,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+ឈ្មោះ
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,បញ្ឈរ_កំណត់ទីតាំង-7),(255,255,255)),((가로+7,បញ្ឈរ_កំណត់ទីតាំង+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',វីនដូ,str(가로-120),str(បញ្ឈរ_កំណត់ទីតាំង-80),'mouseup','1')
            time.sleep(.4)
            ការបែង_ភាគ_តំលៃ=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',ការបែង_ភាគ_តំលៃ)
            가상입력도구('mousemove','--window',វីនដូ,'500','45')
            화상기다리기('remmina-resized.png',[
                ((របារចំណងជើង[0]+447,របារចំណងជើង[1]+279),(39,49,64)),((가로,បញ្ឈរ_កំណត់ទីតាំង),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            សុពលភាព_រាយការណ៍.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not សុពលភាព_រាយការណ៍['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(ការវាស់វែង_ទិន្នន័យ/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for ទិន្នន័យ_កំណត់ទីតាំង in reversed(실행과정들):
                if ទិន្នន័យ_កំណត់ទីតាំង.poll() is None:
                    if ទិន្នន័យ_កំណត់ទីតាំង.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(ទិន្នន័យ_កំណត់ទីតាំង.pid,signal.SIGTERM)
                    else:ទិន្នន័យ_កំណត់ទីតាំង.terminate()
                    try:ទិន្នន័យ_កំណត់ទីតាំង.wait(timeout=5)
                    except subprocess.TimeoutExpired:ទិន្នន័យ_កំណត់ទីតាំង.kill();ទិន្នន័យ_កំណត់ទីតាំង.wait()
            អ្នកជ្រើសរើស.close()
            for ឯកសារ_ការបញ្ចូល in 기록들:ឯកសារ_ការបញ្ចូល.close()
            (ការវាស់វែង_ទិន្នន័យ/'serial.log').write_bytes(직렬입출력)
            (ការវាស់វែង_ទិន្នន័យ/'report.json').write_text(json.dumps(សុពលភាព_រាយការណ៍,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':រត់()
