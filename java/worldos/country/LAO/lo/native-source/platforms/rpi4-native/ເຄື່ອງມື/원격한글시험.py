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
from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ໂຄງ_ການ_ເລກຮາກ


def ແລ່ນ():
    ມາດຕະການ_ຂໍ້ມູນ=ໂຄງ_ການ_ເລກຮາກ/'build/verification/remmina';ມາດຕະການ_ຂໍ້ມູນ.mkdir(parents=True,exist_ok=True)
    ໃຊ້ໄດ້_ລາຍງານ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];ຕົວ_ໃຊ້_ເລືອກ=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            ຈໍາລອງ_ສະແດງຜົນ=shutil.which('Xvfb')
            if ຈໍາລອງ_ສະແດງຜົນ: 서버=[ຈໍາລອງ_ສະແດງຜົນ]
            else:
                뿌리파일계층=ໂຄງ_ການ_ເລກຮາກ.parent/'rpi4/build/rootfs'
                서버=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def ແລ່ນ(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ,환경=None,**이름붙인인수):
                ບັນທຶກ_ແຖວ=(ມາດຕະການ_ຂໍ້ມູນ/('process-%d.log'%len(기록들))).open('wb');기록들.append(ບັນທຶກ_ແຖວ)
                ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ=subprocess.Popen(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ,env=환경,stdout=ບັນທຶກ_ແຖວ,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ);return ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ
            환경=dict(os.environ)
            for ຊື່ in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(ຊື່,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            ສະແດງຜົນ=ແລ່ນ(서버+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert ສະແດງຜົນ.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            ແຂກ=subprocess.Popen(['python3',str(ໂຄງ_ການ_ເລກຮາກ/'ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(ແຂກ);ຕົວ_ໃຊ້_ເລືອກ.register(ແຂກ.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,ອອບເຊັດ_ຄ່າ=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[ອອບເຊັດ_ຄ່າ:]:
                    assert ແຂກ.poll() is None and time.monotonic()<마감시각,직렬입출력[ອອບເຊັດ_ຄ່າ:].decode('utf-8','replace')
                    for 누름값,_ in ຕົວ_ໃຊ້_ເລືອກ.select(.1):
                        ຂໍ້ມູນ=누름값.fileobj.read(65536)
                        if ຂໍ້ມູນ:직렬입출력.extend(ຂໍ້ມູນ)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            ຫມາຍເລກພອດ=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            ໂປຣໄຟລ໌=작업경로/'test.remmina'
            ໂປຣໄຟລ໌.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%ຫມາຍເລກພອດ)
            ແລ່ນ(['dbus-run-session','--','remmina','-c',str(ໂປຣໄຟລ໌)],환경=환경,start_new_session=True)
            def 가상입력도구(*ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ):return subprocess.check_output(['xdotool']+list(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;ວິນໂດ=None
            while time.monotonic()<마감시각:
                ຊອກຫາ_ມາດຕະການ=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if ຊອກຫາ_ມາດຕະການ.returncode==0:
                    후보=ຊອກຫາ_ມາດຕະການ.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    ຮວມ=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if ຮວມ.returncode==0:ວິນໂດ=후보;break
                time.sleep(.1)
            assert ວິນໂດ,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',ວິນໂດ,'280','240','click','1')
            time.sleep(1)
            def 글자입력(ຂໍ້ຄວາມ):가상입력도구('type','--clearmodifiers','--delay','50',ຂໍ້ຄວາມ)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            ອອບເຊັດ_ຄ່າ=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ອອບເຊັດ_ຄ່າ)
            ອອບເຊັດ_ຄ່າ=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),ອອບເຊັດ_ຄ່າ)
            ອອບເຊັດ_ຄ່າ=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 ກະແຈ_ຄ່າ, Shift+Space 또는 F9'.encode(),ອອບເຊັດ_ຄ່າ);기다리기(b'jkoros-native> ',ອອບເຊັດ_ຄ່າ)
            ອອບເຊັດ_ຄ່າ=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),ອອບເຊັດ_ຄ່າ)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',ວິນໂດ,str(ມາດຕະການ_ຂໍ້ມູນ/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',ອອບເຊັດ_ຄ່າ)
            # ຕົວ_ຈິງ_ຂໍ້ມູນ Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            ການ_ແຕ້ມ_ຄ່າ=Image.open(str(ມາດຕະການ_ຂໍ້ມູນ/'remmina-korean.png')).convert('RGB')
            ແຖບຫົວຂໍ້=None
            for ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ in range(ການ_ແຕ້ມ_ຄ່າ.height):
                가로들=[가로 for 가로 in range(ການ_ແຕ້ມ_ຄ່າ.width) if ການ_ແຕ້ມ_ຄ່າ.getpixel((가로,ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ))==(32,80,144)]
                if len(가로들)>=500:ແຖບຫົວຂໍ້=(min(가로들),ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ);break
            assert ແຖບຫົວຂໍ້,'native terminal title bar not found'
            가로,ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ=ແຖບຫົວຂໍ້[0]+564,ແຖບຫົວຂໍ້[1]+356
            가상입력도구('mousemove','--window',ວິນໂດ,str(가로),str(ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ))
            def 화상기다리기(ຊື່,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',ວິນໂດ,str(ມາດຕະການ_ຂໍ້ມູນ/ຊື່)])
                    ບິດແມັບ_ຮູບ=Image.open(str(ມາດຕະການ_ຂໍ້ມູນ/ຊື່)).convert('RGB')
                    if all(ບິດແມັບ_ຮູບ.getpixel(ຈັດຕໍາແຫນ່ງ)==빛 for ຈັດຕໍາແຫນ່ງ,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+ຊື່
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ-7),(255,255,255)),((가로+7,ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',ວິນໂດ,str(가로-120),str(ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ-80),'mouseup','1')
            time.sleep(.4)
            ອອບເຊັດ_ຄ່າ=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',ອອບເຊັດ_ຄ່າ)
            가상입력도구('mousemove','--window',ວິນໂດ,'500','45')
            화상기다리기('remmina-resized.png',[
                ((ແຖບຫົວຂໍ້[0]+447,ແຖບຫົວຂໍ້[1]+279),(39,49,64)),((가로,ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            ໃຊ້ໄດ້_ລາຍງານ.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not ໃຊ້ໄດ້_ລາຍງານ['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(ມາດຕະການ_ຂໍ້ມູນ/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ in reversed(실행과정들):
                if ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.poll() is None:
                    if ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.pid,signal.SIGTERM)
                    else:ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.terminate()
                    try:ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.wait(timeout=5)
                    except subprocess.TimeoutExpired:ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.kill();ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.wait()
            ຕົວ_ໃຊ້_ເລືອກ.close()
            for ຟາຍ_ເຂົ້າໃນ in 기록들:ຟາຍ_ເຂົ້າໃນ.close()
            (ມາດຕະການ_ຂໍ້ມູນ/'serial.log').write_bytes(직렬입출력)
            (ມາດຕະການ_ຂໍ້ມູນ/'report.json').write_text(json.dumps(ໃຊ້ໄດ້_ລາຍງານ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ແລ່ນ()
