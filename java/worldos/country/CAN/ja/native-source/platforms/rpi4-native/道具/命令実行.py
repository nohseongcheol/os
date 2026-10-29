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

計画根 = Path(__file__).resolve().parents[1]
乱数ファイル群 = []


def 後始末乱数():
    for 経路 in 乱数ファイル群:
        try:
            os.unlink(経路)
        except FileNotFoundError:
            pass


atexit.register(後始末乱数)


def 遠隔乱数引数列():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as ファイル:
        ファイル.write(b'JKRENRG1' + os.urandom(32))
        乱数ファイル群.append(ファイル.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(ファイル.name)]


def 試験用模擬機械():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    ホスト = 計画根.parent / 'rpi4/build/host'
    ローダー = ホスト / 'lib/ld-musl-x86_64.so.1'
    二進 = ホスト / 'usr/bin/qemu-system-aarch64'
    if ローダー.is_file() and 二進.is_file():
        return [str(ローダー), '--library-path', str(ホスト / 'usr/lib') + ':' + str(ホスト / 'lib'),
                str(二進), '-L', str(ホスト / 'usr/share/qemu')]
    二進 = shutil.which('qemu-system-aarch64')
    if not 二進:
        raise SystemExit('raspi4b 支援値 QEMU 必要値. QEMU_AARCH64로 경로를 지정하세요.')
    return [二進]


def 解像度読取(文):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', 文):
        raise argparse.ArgumentTypeError('解像度値 書式値: 1920x1080')
    幅値, 高さ値 = map(int, 文.split('x'))
    if not (640 <= 幅値 <= 1920 and 480 <= 高さ値 <= 1080):
        raise argparse.ArgumentTypeError('支援値 切抜き: 幅値 640~1920, 高さ値 480~1080')
    return 幅値, 高さ値


def 命令(解像度値=(640, 480)):
    背景値 = 試験用模擬機械()
    対応済み機能一覧 = subprocess.check_output(背景値 + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 対応済み機能一覧:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 最新値 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    幅値, 高さ値 = 解像度読取('{}x{}'.format(*解像度値))
    return 背景値 + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(幅値),
                   '-global', 'bcm2835-fb.yres=' + str(高さ値), '-kernel',
                   str(計画根 / 'build/kernel8.img'), '-no-reboot'] + 遠隔乱数引数列()


def 起動処理():
    引数解析器 = argparse.ArgumentParser(description='内蔵 Java Pi4 中核値. 直列値 셸은 Ctrl+A X, --desktop은 Ctrl+C로 終了点プログラム.')
    引数解析器.add_argument('--display', default='none', help='none 또는 gtk/sdl (ホスト 支援値 必要値)')
    引数解析器.add_argument('--resolution', type=解像度読取, default=(640, 480), help='起動 画面 容量. 예: 1920x1080; 既定値 640x480')
    引数解析器.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 機器ポート 5902. キー値 입력은 UART 터미널에서 합니다.')
    引数解析器.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    引数解析器.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 機器ポート')
    引数解析器.add_argument('--network', action='store_true', help='補助値 UART SLIP와 QEMU NAT를 接続; --desktop과 함께 使用値 가능; 게스트에서 ftpd start')
    引数解析器.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    引数解析器.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP 制御値 機器ポート (데이터 50000..50007)')
    引数解析器.add_argument('--guest-ip', default=None, help='QEMU NAT 前方値 対象値. 기본은 ip.conf의 IP; 値変更 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    引数解析器.add_argument('--network-host', default='127.0.0.1', help='NAT 値受取 番地. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN 番地: 外部値 接続状態')
    引数解析器.add_argument('--forward', action='append', default=[], help='--network 入口追記 接続: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    引数解析器.add_argument('--pip', action='store_true', help='PyPI ソース木 パッケージ 値中継 起動処理 (--network 必要値, MicroPython 호환 소스만)')
    引数解析器.add_argument('--pip-port', type=int, default=8027, help='パッケージ 중계의 localhost TCP 機器ポート')
    引数解析器.add_argument('--pip-cache', type=Path, default=計画根/'build/pip-cache')
    引数解析器.add_argument('--pip-offline', action='store_true', help='이미 받은 配布値 파일만 제공')
    引数配列 = 引数解析器.parse_args()
    if 引数配列.remote:
        引数配列.network=True
        引数配列.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; 合言葉値: python3 道具/遠隔設定値.py show'.format(引数配列.network_host,引数配列.network_host),flush=True)
    if 引数配列.pip and not 引数配列.network: 引数解析器.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= 引数配列.pip_port <= 65535: 引数解析器.error('--pip-port 범위는 1~65535입니다.')
    if 引数配列.forward and not 引数配列.network: 引数解析器.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as 資源値:
        if 引数配列.pip:
            from 束中継 import 束中継
            資源値.enter_context(束中継(引数配列.pip_port, 引数配列.pip_cache, 引数配列.pip_offline))
            print('パッケージ 値中継: 127.0.0.1:' + str(引数配列.pip_port), flush=True)
        作業実行(引数配列)


def 作業実行(引数配列):
    if 引数配列.desktop:
        if 引数配列.vnc or 引数配列.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from デスクトップ表示像 import デスクトップ起動処理
        raise SystemExit(デスクトップ起動処理(引数配列.port, 通信使用=引数配列.network, ファイル転送ポート番号=引数配列.ftp_port, 転送中規則一覧=引数配列.forward, 解像度値=引数配列.resolution, ゲスト番地=引数配列.guest_ip, ホスト番地=引数配列.network_host))
    選択項目 = ['-display', 引数配列.display, '-serial', 'mon:stdio']
    if 引数配列.vnc:
        選択項目 += ['-vnc', 引数配列.vnc]
    if 引数配列.network:
        from 通信網橋渡し import 通信網橋渡し
        with 通信網橋渡し(引数配列.ftp_port, 引数配列.forward, ゲスト番地=引数配列.guest_ip, ホスト番地=引数配列.network_host) as 橋渡し:
            状況値 = subprocess.call(命令(引数配列.resolution) + 選択項目 + 橋渡し.転送済み引数())
            if 橋渡し.エラー: raise SystemExit('network bridge: ' + 橋渡し.エラー)
        raise SystemExit(状況値)
    raise SystemExit(subprocess.call(命令(引数配列.resolution) + 選択項目))


if __name__ == '__main__':
    起動処理()
