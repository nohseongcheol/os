#!/usr/bin/env python3
"""実際データ QEMU/VNC에서 端末 隅値 引摺り値·ポインタ·동적 文字値 槽入口·編集値 内容物値 보존를 검사한다."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from PIL import Image
from デスクトップ表示像 import 厳密値
from 命令実行 import 計画根


def 窓寸法変更中試験(幅値, 高さ値, 結果経路):
    with socket.socket() as 一時値:
        一時値.bind(('127.0.0.1', 0)); ポート番号 = 一時値.getsockname()[1]
    容量本文 = '{}x{}'.format(幅値, 高さ値)
    プロセス値 = subprocess.Popen(['python3', str(計画根/'道具/命令実行.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(ポート番号), '--resolution', 容量本文], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    選択器 = selectors.DefaultSelector(); 選択器.register(プロセス値.stdout, selectors.EVENT_READ)
    履歴記録記録 = bytearray(); 遠隔値 = None; 転送値 = None; ポインタ隠蔽=[False]

    def 待機(値表示, 起動処理=0):
        期限値 = time.monotonic() + 60
        while 値表示 not in 履歴記録記録[起動処理:]:
            if time.monotonic() > 期限値 or プロセス値.poll() is not None or b'HALTED' in 履歴記録記録 or b'PANIC:' in 履歴記録記録:
                raise AssertionError(履歴記録記録[起動処理:].decode('utf-8', 'replace'))
            for イベント, _ in 選択器.select(.1):
                データ = イベント.fileobj.read(65536)
                if データ: 履歴記録記録.extend(データ)
        return 履歴記録記録[起動処理:].decode('utf-8', 'replace')

    def クリックボタン(記号, 判定押下済み=True): 遠隔値.sendall(struct.pack('>BBHI', 4, int(判定押下済み), 0, 記号))

    def 本文送信(文):
        起動処理 = len(履歴記録記録)
        for 文字値 in 文:
            記号 = 0xff0d if 文字値 == '\n' else ord(文字値) if ord(文字値) < 256 else 0x1000000 | ord(文字値)
            クリックボタン(記号); クリックボタン(記号, False)
        return 起動処理

    def シェル(文): return 待機(b'\r\n__RESIZE_DONE__\r\n', 本文送信(文+'; echo __RESIZE_DONE__\n'))

    def 点位置(水平位置, 垂直位置, 判定押下済み): 遠隔値.sendall(struct.pack('>BBHH', 5, 判定押下済み, 水平位置, 垂直位置))

    def クリック値(水平位置, 垂直位置): 点位置(水平位置, 垂直位置, 1); 点位置(水平位置, 垂直位置, 0)

    def ビットマップイメージ():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 実際データ 너비를 쓴다.
        遠隔値.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 幅値, 高さ値))
        描画 = Image.new('RGB', (幅値, 高さ値)); 面積値 = 0
        while True:
            種別値 = 厳密値(遠隔値, 1)[0]
            if 種別値 == 2: continue
            if 種別値 == 3:
                長さ = struct.unpack('>I', 厳密値(遠隔値, 7)[3:])[0]; 厳密値(遠隔値, 長さ); continue
            assert 種別値 == 0, 種別値
            項目個数 = struct.unpack('>H', 厳密値(遠隔値, 3)[1:])[0]
            for _ in range(項目個数):
                水平位置, 垂直位置, 幅跨域, 長さ, 符号化状態値 = struct.unpack('>HHHHi', 厳密値(遠隔値, 12))
                if 符号化状態値 == -239:
                    assert 幅跨域==0 and 長さ==0, 'remote cursor must be hidden'
                    ポインタ隠蔽[0]=True
                    continue
                assert 符号化状態値 == 0 and 水平位置+幅跨域 <= 幅値 and 垂直位置+長さ <= 高さ値
                描画.paste(Image.frombytes('RGB', (幅跨域, 長さ), 厳密値(遠隔値, 幅跨域*長さ*4), 'raw', 'BGRX'), (水平位置, 垂直位置))
                面積値 += 幅跨域*長さ
            if 面積値:
                assert 面積値 == 幅値*高さ値, 面積値
                return 描画

    def 画素検査(座標値, 色値):
        期限値 = time.monotonic()+10
        while True:
            描画 = ビットマップイメージ()
            if 描画.getpixel(座標値) == 色値: return 描画
            if time.monotonic() > 期限値: raise AssertionError((座標値, 描画.getpixel(座標値), 色値))

    def 送出転送ファイル群(名前, データ): 転送値.storbinary('STOR '+名前, io.BytesIO(データ))

    try:
        待機(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+容量本文+' RGB32').encode() in 履歴記録記録
        print('BOOT:', 容量本文, flush=True)
        遠隔番号 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', 履歴記録記録).group(1))
        遠隔値 = socket.create_connection(('127.0.0.1', 遠隔番号), timeout=20)
        assert 厳密値(遠隔値, 12) == b'RFB 003.008\n'; 遠隔値.sendall(b'RFB 003.008\n')
        assert 1 in 厳密値(遠隔値, 厳密値(遠隔値, 1)[0]); 遠隔値.sendall(b'\x01')
        assert 厳密値(遠隔値, 4) == b'\0'*4; 遠隔値.sendall(b'\x01')
        初期状況 = 厳密値(遠隔値, 24); assert struct.unpack('>HH', 初期状況[:4]) == (幅値, 高さ値)
        厳密値(遠隔値, struct.unpack('>I', 初期状況[20:])[0])
        遠隔値.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        遠隔値.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        画素検査((幅値-1, 高さ値-1), (24, 32, 48))
        def 一時停止短時間だけ(秒数値=.25):
            終端=time.monotonic()+秒数値
            while time.monotonic()<終端:
                for イベント,_ in 選択器.select(.02):
                    データ=イベント.fileobj.read(65536)
                    if データ:履歴記録記録.extend(データ)
        窓=[12,48,568,360]
        def 容量検証():
            列値,行番号値=(窓[2]-24)//8,(窓[3]-56)//16
            文=シェル('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(列値,行番号値) in 文,文
            # 実際データ 窓 테두리: 단지 容量 照会値 값만 바뀐 것이 아닌지 확인한다.
            点位置(幅値-1,10,0);一時停止短時間だけ()
            画素検査((窓[0],窓[1]),(32,80,144))
            描画=画素検査((窓[0]+窓[2]-1,窓[1]+窓[3]-1),(39,49,64))
            return 描画
        def 隅値(方向):
            return (窓[0]+(3 if 方向 in (1,3) else 窓[2]-4),窓[1]+(3 if 方向<=2 else 窓[3]-4))
        def 寸法変更引摺り(方向,差分値,ボタン=1):
            先頭位置被演算子,三値=隅値(方向);点位置(先頭位置被演算子,三値,0);一時停止短時間だけ()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            白画素=(先頭位置被演算子-7 if 方向 in (1,4) else 先頭位置被演算子+7,三値-7)
            画素検査(白画素,(255,255,255))
            点位置(先頭位置被演算子,三値,ボタン)
            終端位置水平=max(0,min(幅値-1,先頭位置被演算子+差分値[0]));終端位置垂直=max(0,min(高さ値-1,三値+差分値[1]))
            点位置(終端位置水平,終端位置垂直,ボタン);点位置(終端位置水平,終端位置垂直,0);一時停止短時間だけ()
            if ボタン==1:
                左値,上端値,幅跨域,長さ=窓;右値,下端値=左値+幅跨域,上端値+長さ
                if 方向 in (1,3):左値=max(0,min(右値-360,左値+終端位置水平-先頭位置被演算子))
                else:右値=max(左値+360,min(幅値,右値+終端位置水平-先頭位置被演算子))
                if 方向<=2:上端値=max(34,min(下端値-216,上端値+終端位置垂直-三値))
                else:下端値=max(上端値+216,min(高さ値,下端値+終端位置垂直-三値))
                窓[:]=[左値,上端値,右値-左値,下端値-上端値]
        容量検証();assert ポインタ隠蔽[0]
        寸法変更引摺り(4,(-100,-60),4);容量検証() # 右 버튼은 크기를 바꾸지 않는다.
        for 方向,差分値 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            寸法変更引摺り(方向,差分値);容量検証()
        # 入力値 중인 긴 ハングル文字列 명령은 改行/水平位置 스크롤과 무관하게 그대로 실행된다.
        長整数本文='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        本文送信("echo '"+長整数本文+"'");一時停止短時間だけ()
        寸法変更引摺り(4,(-1000,-1000));assert 窓[2:]==[360,216]
        寸法変更引摺り(4,(幅値,高さ値))
        起動処理=本文送信('\n');待機(('\r\n'+長整数本文+'\r\n').encode(),起動処理);容量検証()
        # vi가 編集値 중에 画面 크기를 再試行処理値 읽고, 저장하지 않은 한글도 유지한다.
        シェル('ftpd start')
        転送値=ftplib.FTP();転送値.encoding='utf-8';転送値.connect('127.0.0.1',ポート番号,timeout=20);転送値.login()
        待機(b'NORMAL',本文送信('vi /크기자료.txt\n'))
        待機(b'INSERT',本文送信('i미저장 한글 データ\n'));一時停止短時間だけ()
        寸法変更引摺り(4,(-幅値,-高さ値))
        # ANSI 行番号値 이동에 새 行番号値 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((窓[3]-56)//16)).encode() in 履歴記録記録[-4096:]
        本文送信('작은 창에서도 継続状態値 書込\n');一時停止短時間だけ()
        寸法変更引摺り(4,(幅値,高さ値))
        本文送信('큰 창에서도 継続状態値 書込\n');一時停止短時間だけ()
        クリックボタン(0xff1b);クリックボタン(0xff1b,False);一時停止短時間だけ()
        待機(b'jkoros-native> ',本文送信(':wq\n'))
        内容物値=bytearray();転送値.retrbinary('RETR 크기자료.txt',内容物値.extend)
        assert 内容物値=='미저장 한글 データ\n작은 창에서도 継続状態値 書込\n큰 창에서도 継続状態値 書込\n'.encode(),内容物値
        容量検証().save(str(結果経路/(容量本文+'-large.png')))
        # 두 번째 창은 既定値 容量, 再試行処理値 先頭位置項目 창을 고르면 앞에서 바꾼 크기가 유지된다.
        起動処理=len(履歴記録記録);クリック値(70,16);待機(b'TERMINAL FOCUS 2',起動処理)
        assert 'TERMINAL SIZE 68x19' in シェル('terminal size')
        起動処理=len(履歴記録記録);クリック値(180,16);待機(b'TERMINAL FOCUS 1',起動処理);容量検証()
        寸法変更引摺り(4,(-幅値,-高さ値));容量検証().save(str(結果経路/(容量本文+'-small.png')))
        # 容量 値変更 後端値 X 닫기도 새로운 右 가장자리를 사용한다.
        起動処理=len(履歴記録記録);クリック値(窓[0]+窓[2]-20,窓[1]+15);待機(b'TERMINAL FOCUS 2',起動処理)
        assert 'RESIZE CLOSED' in シェル('echo RESIZE CLOSED')
        print('PASS:',容量本文,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if 転送値:転送値.close()
        if 遠隔値:遠隔値.close()
        if プロセス値.poll() is None:
            プロセス値.terminate()
            try:プロセス値.wait(timeout=8)
            except subprocess.TimeoutExpired:プロセス値.kill();プロセス値.wait()
        選択器.close();プロセス値.stdout.close();(結果経路/(容量本文+'.log')).write_bytes(履歴記録記録)


def 起動処理():
    結果経路=計画根/'build/verification/resize';結果経路.mkdir(parents=True,exist_ok=True)
    履歴記録記録={'passed':False,'kernel_sha256':hashlib.sha256((計画根/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 幅値,高さ値 in ((640,480),(1920,1080)):
            窓寸法変更中試験(幅値,高さ値,結果経路);履歴記録記録['resolutions'].append([幅値,高さ値])
        履歴記録記録.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(結果経路/'report.json').write_text(json.dumps(履歴記録記録,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':起動処理()
