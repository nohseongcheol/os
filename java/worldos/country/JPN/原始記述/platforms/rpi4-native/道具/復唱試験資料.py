"""Independent host TCP/UDP echo peers for native network integration tests."""
import socket
import threading


class 復唱試験資料:
    def __enter__(自身値):
        自身値.接続状態制御 = socket.socket(); 自身値.接続状態制御.bind(('127.0.0.1', 0)); 自身値.接続状態制御.listen(1)
        自身値.データグラム制御 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); 自身値.データグラム制御.bind(('127.0.0.1', 0))
        自身値.接続状態制御.settimeout(30); 自身値.データグラム制御.settimeout(30)
        自身値.TCPポート = 自身値.接続状態制御.getsockname()[1]; 自身値.UDPポート = 自身値.データグラム制御.getsockname()[1]
        自身値.エラー一覧 = []; 自身値.保有受信済み = {}
        def 接続状態制御():
            try:
                接続状態, _ = 自身値.接続状態制御.accept()
                with 接続状態:
                    接続状態.settimeout(5); データ = bytearray()
                    while b'\n' not in データ:
                        断片値 = 接続状態.recv(512)
                        if not 断片値: raise RuntimeError('TCP EOF before request')
                        データ.extend(断片値)
                    自身値.保有受信済み['tcp'] = bytes(データ); 接続状態.sendall(データ)
            except Exception as 補助入口: 自身値.エラー一覧.append(str(補助入口))
        def データグラム制御():
            try:
                データ, 通信相手値 = 自身値.データグラム制御.recvfrom(512); 自身値.保有受信済み['udp'] = データ; 自身値.データグラム制御.sendto(データ, 通信相手値)
            except Exception as 補助入口: 自身値.エラー一覧.append(str(補助入口))
        自身値.スレッド群 = [threading.Thread(target=ファイル入口, daemon=True) for ファイル入口 in (接続状態制御, データグラム制御)]
        for 端末入口 in 自身値.スレッド群: 端末入口.start()
        return 自身値

    def __exit__(自身値, *引数配列):
        自身値.接続状態制御.close(); 自身値.データグラム制御.close()
        for 端末入口 in 自身値.スレッド群: 端末入口.join(timeout=1)
