#!/usr/bin/env python3
import argparse
from contextlib import ExitStack
import os
import re
from pathlib import Path
import shutil
import subprocess
import atexit
import tempfile

प्रोजेक्ट_मूळ = Path(__file__).resolve().parents[1]
यादृच्छिक_संचिका = []


def स्वच्छता_यादृच्छिक():
    for मार्ग in यादृच्छिक_संचिका:
        try:
            os.unlink(मार्ग)
        except FileNotFoundError:
            pass


atexit.register(स्वच्छता_यादृच्छिक)


def दूरस्_थ_यादृच्छिक_वितर्क():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as फाइल:
        फाइल.write(b'JKRENRG1' + os.urandom(32))
        यादृच्छिक_संचिका.append(फाइल.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(फाइल.name)]


def अनुकृती_मशीन():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    होस्ट = प्रोजेक्ट_मूळ.parent / 'rpi4/build/host'
    भारक = होस्ट / 'lib/ld-musl-x86_64.so.1'
    बायनरी = होस्ट / 'usr/bin/qemu-system-aarch64'
    if भारक.is_file() and बायनरी.is_file():
        return [str(भारक), '--library-path', str(होस्ट / 'usr/lib') + ':' + str(होस्ट / 'lib'),
                str(बायनरी), '-L', str(होस्ट / 'usr/share/qemu')]
    बायनरी = shutil.which('qemu-system-aarch64')
    if not बायनरी:
        raise SystemExit('raspi4b समर्थन_मूल्य QEMU आवश्यक_मूल्य. QEMU_AARCH64로 경로를 지정하세요.')
    return [बायनरी]


def बिंदूघनता_वाचा(पाठ्य):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', पाठ्य):
        raise argparse.ArgumentTypeError('बिंदूघनता_मूल्य स्वरूप_मूल्य: 1920x1080')
    रुंदी_मूल्य, उंची_मूल्य = map(int, पाठ्य.split('x'))
    if not (640 <= रुंदी_मूल्य <= 1920 and 480 <= उंची_मूल्य <= 1080):
        raise argparse.ArgumentTypeError('समर्थन_मूल्य क्लिप: रुंदी_मूल्य 640~1920, उंची_मूल्य 480~1080')
    return रुंदी_मूल्य, उंची_मूल्य


def आदेश(बिंदूघनता_मूल्य=(640, 480)):
    वॉलपेपर_मूल्य = अनुकृती_मशीन()
    समर्थित_वैशिष्ट्ये = subprocess.check_output(वॉलपेपर_मूल्य + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in समर्थित_वैशिष्ट्ये:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. नवीनतम_मूल्य QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    रुंदी_मूल्य, उंची_मूल्य = बिंदूघनता_वाचा('{}x{}'.format(*बिंदूघनता_मूल्य))
    return वॉलपेपर_मूल्य + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(रुंदी_मूल्य),
                   '-global', 'bcm2835-fb.yres=' + str(उंची_मूल्य), '-kernel',
                   str(प्रोजेक्ट_मूळ / 'build/kernel8.img'), '-no-reboot'] + दूरस्_थ_यादृच्छिक_वितर्क()


def सुरू_करा():
    व्याकरणविश्लेषक = argparse.ArgumentParser(description='स्वकीय Java Pi4 गाभा_मूल्य. अनुक्रमिक_मूल्य 셸은 Ctrl+A X, --desktop은 Ctrl+C로 निर्गमन_करा_अनुप्रयोग.')
    व्याकरणविश्लेषक.add_argument('--display', default='none', help='none 또는 gtk/sdl (होस्ट समर्थन_मूल्य आवश्यक_मूल्य)')
    व्याकरणविश्लेषक.add_argument('--resolution', type=बिंदूघनता_वाचा, default=(640, 480), help='प्रणालीप्रारंभ पडदा आकार. 예: 1920x1080; डिफॉल्ट_मूल्य 640x480')
    व्याकरणविश्लेषक.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC हार्डवेअर_पॉर्ट 5902. कळ_मूल्य 입력은 UART 터미널에서 합니다.')
    व्याकरणविश्लेषक.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    व्याकरणविश्लेषक.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC हार्डवेअर_पॉर्ट')
    व्याकरणविश्लेषक.add_argument('--network', action='store_true', help='सहायक_मूल्य UART SLIP와 QEMU NAT를 जोडा; --desktop과 함께 वापर_मूल्य 가능; 게스트에서 ftpd start')
    व्याकरणविश्लेषक.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    व्याकरणविश्लेषक.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP नियंत्रण_मूल्य हार्डवेअर_पॉर्ट (데이터 50000..50007)')
    व्याकरणविश्लेषक.add_argument('--guest-ip', default=None, help='QEMU NAT फॉरवर्ड_मूल्य लक्ष्य. 기본은 ip.conf의 IP; बदल_करा_मूल्य 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    व्याकरणविश्लेषक.add_argument('--network-host', default='127.0.0.1', help='NAT मूल्य_स्वीकारा पत्ता. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN पत्ता: बाह्य_मूल्य कनेक्शन_e05f319b')
    व्याकरणविश्लेषक.add_argument('--forward', action='append', default=[], help='--network शेवटीजोडा_प्रविष्टी जोडा: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    व्याकरणविश्लेषक.add_argument('--pip', action='store_true', help='PyPI स्रोत_ट्री बंडल संदेशमध्यस्थ_मूल्य सुरू_करा (--network आवश्यक_मूल्य, MicroPython 호환 소스만)')
    व्याकरणविश्लेषक.add_argument('--pip-port', type=int, default=8027, help='बंडल 중계의 localhost TCP हार्डवेअर_पॉर्ट')
    व्याकरणविश्लेषक.add_argument('--pip-cache', type=Path, default=प्रोजेक्ट_मूळ/'build/pip-cache')
    व्याकरणविश्लेषक.add_argument('--pip-offline', action='store_true', help='이미 받은 वितरण_मूल्य 파일만 제공')
    वितर्क_ऍरे = व्याकरणविश्लेषक.parse_args()
    if वितर्क_ऍरे.remote:
        वितर्क_ऍरे.network=True
        वितर्क_ऍरे.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; पासवर्ड_मूल्य: python3 साधने/दूरस्_थ_सेटिंग्ज.py show'.format(वितर्क_ऍरे.network_host,वितर्क_ऍरे.network_host),flush=True)
    if वितर्क_ऍरे.pip and not वितर्क_ऍरे.network: व्याकरणविश्लेषक.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= वितर्क_ऍरे.pip_port <= 65535: व्याकरणविश्लेषक.error('--pip-port 범위는 1~65535입니다.')
    if वितर्क_ऍरे.forward and not वितर्क_ऍरे.network: व्याकरणविश्लेषक.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as संसाधन_मूल्य:
        if वितर्क_ऍरे.pip:
            from बंडल_संदेशमध्यस्थ import बंडल_संदेशमध्यस्थ
            संसाधन_मूल्य.enter_context(बंडल_संदेशमध्यस्थ(वितर्क_ऍरे.pip_port, वितर्क_ऍरे.pip_cache, वितर्क_ऍरे.pip_offline))
            print('बंडल संदेशमध्यस्थ_मूल्य: 127.0.0.1:' + str(वितर्क_ऍरे.pip_port), flush=True)
        कार्यान्वित_करा(वितर्क_ऍरे)


def कार्यान्वित_करा(वितर्क_ऍरे):
    if वितर्क_ऍरे.desktop:
        if वितर्क_ऍरे.vnc or वितर्क_ऍरे.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from डेस्कटॉप_दृश्य import रन_डेस्कटॉप
        raise SystemExit(रन_डेस्कटॉप(वितर्क_ऍरे.port, संचारजाळे=वितर्क_ऍरे.network, संचिका_स्थानांतर_पोर्ट_नंबर=वितर्क_ऍरे.ftp_port, अग्रेषण_नियम_f4578a27=वितर्क_ऍरे.forward, बिंदूघनता_मूल्य=वितर्क_ऍरे.resolution, अतिथी_पत्ता=वितर्क_ऍरे.guest_ip, होस्ट_पत्ता=वितर्क_ऍरे.network_host))
    पर्याय_7f769d16 = ['-display', वितर्क_ऍरे.display, '-serial', 'mon:stdio']
    if वितर्क_ऍरे.vnc:
        पर्याय_7f769d16 += ['-vnc', वितर्क_ऍरे.vnc]
    if वितर्क_ऍरे.network:
        from संचारजाळे_ब्रिज import संचारजाळे_ब्रिज
        with संचारजाळे_ब्रिज(वितर्क_ऍरे.ftp_port, वितर्क_ऍरे.forward, अतिथी_पत्ता=वितर्क_ऍरे.guest_ip, होस्ट_पत्ता=वितर्क_ऍरे.network_host) as ब्रिज:
            राज्य_मूल्य = subprocess.call(आदेश(वितर्क_ऍरे.resolution) + पर्याय_7f769d16 + ब्रिज.अग्रेषित_वितर्क())
            if ब्रिज.त्रुटी: raise SystemExit('network bridge: ' + ब्रिज.त्रुटी)
        raise SystemExit(राज्य_मूल्य)
    raise SystemExit(subprocess.call(आदेश(वितर्क_ऍरे.resolution) + पर्याय_7f769d16))


if __name__ == '__main__':
    सुरू_करा()
