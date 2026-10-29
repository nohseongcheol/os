"""内蔵 中核値 MicroPython에서 사용하는 한글 関数 名前."""
import jkoros as 稼働システム
出力 = print
ファイル読取 = 稼働システム.read
ファイル書込 = 稼働システム.write
ファイル除去 = 稼働システム.remove
入力読取 = 稼働システム.stdin
矩形描画処理 = 稼働システム.rect
対象描画中待合 = 稼働システム.wait_key
ミリ秒 = 稼働システム.ticks_ms
データグラム開放 = 稼働システム.udp_open
データグラム送信 = 稼働システム.udp_send
外部データグラム送信 = 稼働システム.udp_sendto
データグラム受取 = 稼働システム.udp_recv
通信網閉鎖 = 稼働システム.udp_close

def 本文復号(データ):
    return データ.decode("utf-8")
