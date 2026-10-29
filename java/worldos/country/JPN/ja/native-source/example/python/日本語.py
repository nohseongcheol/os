"""内蔵 커널의 ファイル·通信·画面 호출과 日本語 例外. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as 稼働システム
import sys as 実行環境

def 出力(*値, 区切り=" ", 終端="\n", **旧式引数列):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 旧式引数列: 旧式引数列["sep"] = 区切り
    if "end" not in 旧式引数列: 旧式引数列["end"] = 終端
    print(*値, **旧式引数列)

整数値 = int
命令引数列 = 実行環境.argv
試行処理再試行エラー = 11

class システムエラー(OSError):
    def __init__(自身値, 番号, 説明="稼働システム 작업에 실패했습니다."):
        super().__init__(番号, 説明)
        自身値.番号 = 番号
        自身値.説明 = 説明

def 稼働系呼出(関数, *引数):
    try:
        return 関数(*引数)
    except OSError as エラー:
        番号 = エラー.args[0] if エラー.args else 0
        raise システムエラー(番号)

def 本文符号化(文):
    return 文.encode("utf-8")

def 本文復号(データ):
    return データ.decode("utf-8")

def ファイル読取(名前):
    return 稼働系呼出(稼働システム.read, 名前)

def ファイル書込(名前, データ):
    return 稼働系呼出(稼働システム.write, 名前, データ)

def ファイル除去(名前):
    return 稼働系呼出(稼働システム.remove, 名前)

def データグラム開放(ポート番号):
    return 稼働系呼出(稼働システム.udp_open, ポート番号)

def データグラム送信(通信端点, ポート番号, データ):
    return 稼働系呼出(稼働システム.udp_send, 通信端点, ポート番号, データ)

def 外部データグラム送信(通信端点, 番地, ポート番号, データ):
    return 稼働系呼出(稼働システム.udp_sendto, 通信端点, 番地, ポート番号, データ)

def データグラム受取(通信端点):
    return 稼働系呼出(稼働システム.udp_recv, 通信端点)

def 通信網閉鎖(通信端点):
    return 稼働系呼出(稼働システム.udp_close, 通信端点)

def 矩形描画処理(*引数):
    return 稼働系呼出(稼働システム.rect, *引数)

def 画面容量():
    return 稼働系呼出(稼働システム.screen_size)

def 対象描画中待合():
    return 稼働系呼出(稼働システム.wait_key)

ミリ秒 = 稼働システム.ticks_ms
