"""tựThân 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 Chủ 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as HệĐiềuHành

đườngDẫnDanhSách = "/lib/.pip.json"


def giáTrịDấuNhậnDạng(DữLiệu):
    return "".join("%02x" % giáTrị for giáTrị in hashlib.sha256(DữLiệu).digest())


def đọcDanhSách():
    if HệĐiềuHành.path_kind(đườngDẫnDanhSách) == 0:
        return {}
    return json.loads(HệĐiềuHành.read(đườngDẫnDanhSách).decode("utf-8"))


def ghiNhậtKý(đườngDẫn, DữLiệu):
    if HệĐiềuHành.write(đườngDẫn, DữLiệu) != len(DữLiệu):
        raise OSError(28)


def kiểmTraĐườngDẫn(đườngDẫn):
    if not isinstance(đườngDẫn, str) or not đườngDẫn.endswith(".py"):
        raise ValueError("Python 소스만 설치할 trịSố 있습니다.")
    if any(giáTrịPhầnCon in ("", ".", "..") or giáTrịPhầnCon.startswith(".") for giáTrịPhầnCon in đườngDẫn.split("/")):
        raise ValueError("허용하지 않는 GóiGộp đườngDẫn")
    if "\\" in đườngDẫn or any(ord(giáTrịKýTự) < 32 or ord(giáTrịKýTự) == 127 for giáTrịKýTự in đườngDẫn):
        raise ValueError("잘못된 đườngDẫn KýTự")
    kếtQuả = "/lib/" + đườngDẫn
    if len(kếtQuả.encode("utf-8")) > 63 or đườngDẫn in ("tiếngViệt.py", "GóiGộp.py"):
        raise ValueError("GóiGộp 경로가 너무 길거나 giáTrịMặcĐịnh 라이브러리와 겹칩니다.")
    return kếtQuả


class nhậnLuồng:
    def __init__(giáTrịBảnThân, điểmCuối):
        giáTrịBảnThân.điểmCuối = điểmCuối
        giáTrịBảnThân.dữLiệuCònLại = b""
        giáTrịBảnThân.chạy = HệĐiềuHành.ticks_ms()

    def đọcĐúngBằng(giáTrịBảnThân, độDài):
        DữLiệu = bytearray()
        while len(DữLiệu) < độDài:
            if HệĐiềuHành.ticks_ms() - giáTrịBảnThân.chạy > 90000:
                raise ValueError("GóiGộp chuyểnTiếpGiáTrị lờiĐáp giáTrịThờiGian 초과")
            if not giáTrịBảnThân.dữLiệuCònLại:
                try:
                    giáTrịBảnThân.dữLiệuCònLại = HệĐiềuHành.tcp_read(giáTrịBảnThân.điểmCuối, 512)
                except OSError as lỗi:
                    if lỗi.args[0] != 11:
                        raise
                    HệĐiềuHành.sleep_ms(10)
                    continue
                if not giáTrịBảnThân.dữLiệuCònLại:
                    raise ValueError("GóiGộp 전송이 중간에 끝났습니다.")
            sốLượngPhầnMục = min(độDài - len(DữLiệu), len(giáTrịBảnThân.dữLiệuCònLại))
            DữLiệu.extend(giáTrịBảnThân.dữLiệuCònLại[:sốLượngPhầnMục])
            giáTrịBảnThân.dữLiệuCònLại = giáTrịBảnThân.dữLiệuCònLại[sốLượngPhầnMục:]
            HệĐiềuHành.sleep_ms(0)
        return bytes(DữLiệu)


def tảiXuống(yêuCầu, sốCổng):
    if len(yêuCầu) > 96 or any(giáTrịKýTự not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for giáTrịKýTự in yêuCầu):
        raise ValueError("사용법: pip install tên 또는 tên==버전")
    điểmCuối = HệĐiềuHành.tcp_open()
    try:
        chạy = HệĐiềuHành.ticks_ms()
        while True:
            try:
                HệĐiềuHành.tcp_connect(điểmCuối, "10.0.2.2", sốCổng)
                break
            except OSError as lỗi:
                if lỗi.args[0] not in (11, 115) or HệĐiềuHành.ticks_ms() - chạy > 5000:
                    raise ValueError("GóiGộp chuyểnTiếpGiáTrị nốiKết giáTrịSựThấtBại: 호스트에서 --network --pip로 실행하십시오.")
                HệĐiềuHành.sleep_ms(10)
        DữLiệu = (yêuCầu + "\n").encode()
        while DữLiệu:
            try:
                sốLượngPhầnMục = HệĐiềuHành.tcp_write(điểmCuối, DữLiệu)
                if not sốLượngPhầnMục:
                    raise ValueError("GóiGộp yêuCầu giáTrịChuyểnGiao giáTrịSựThấtBại")
                DữLiệu = DữLiệu[sốLượngPhầnMục:]
            except OSError as lỗi:
                if lỗi.args[0] != 11:
                    raise
                HệĐiềuHành.sleep_ms(10)
                if HệĐiềuHành.ticks_ms() - chạy > 10000:
                    raise ValueError("GóiGộp yêuCầu giáTrịChuyểnGiao giáTrịThờiGian 초과")
        giáTrịLuồng = nhậnLuồng(điểmCuối)
        giáTrịĐầu = giáTrịLuồng.đọcĐúngBằng(8)
        if giáTrịĐầu[:4] != b"JKP1":
            raise ValueError("GóiGộp giáTrịChuyểnGiao giáTrịQuyƯớc 불일치")
        độDài = (giáTrịĐầu[4] << 24) | (giáTrịĐầu[5] << 16) | (giáTrịĐầu[6] << 8) | giáTrịĐầu[7]
        if độDài > 8192:
            raise ValueError("GóiGộp 명세가 너무 큽니다.")
        đặcTả = json.loads(giáTrịLuồng.đọcĐúngBằng(độDài).decode())
        if "error" in đặcTả:
            raise ValueError(đặcTả["error"])
        if not 1 <= len(đặcTả["files"]) <= 16:
            raise ValueError("꾸러미당 câyNguồn 파일은 1~16개여야 합니다.")
        if sum(giáTrịMục["size"] for giáTrịMục in đặcTả["files"]) > 65536:
            raise ValueError("GóiGộp câyNguồn 합계는 64 KiB 이하여야 합니다.")
        cácMụcTệp = {}
        for giáTrịMục in đặcTả["files"]:
            đườngDẫn = kiểmTraĐườngDẫn(giáTrịMục["path"])
            if đườngDẫn in cácMụcTệp or not 0 <= giáTrịMục["size"] <= 16384:
                raise ValueError("중복 đườngDẫn 또는 Tệp cỡ 초과")
            DữLiệu = giáTrịLuồng.đọcĐúngBằng(giáTrịMục["size"])
            if giáTrịDấuNhậnDạng(DữLiệu) != giáTrịMục["sha256"]:
                raise ValueError("GóiGộp Tệp SHA-256 불일치")
            # 실행하지 않고 phầnMụcHiệnTại MicroPython의 문법으로 먼저 검사한다.
            compile(DữLiệu.decode("utf-8"), đườngDẫn, "exec")
            cácMụcTệp[đườngDẫn] = DữLiệu
            gc.collect()
        return đặcTả, cácMụcTệp
    finally:
        HệĐiềuHành.udp_close(điểmCuối)


def càiĐặtGiáTrị(yêuCầu, sốCổng):
    print("GóiGộp tảiXuống:", yêuCầu)
    đặcTả, cácMụcTệp = tảiXuống(yêuCầu, sốCổng)
    danhSáchMục = đọcDanhSách()
    tên = đặcTả["name"]
    if tên in danhSáchMục:
        if danhSáchMục[tên]["version"] == đặcTả["version"]:
            for đườngDẫn, dữLiệuDấuNhậnDạng in danhSáchMục[tên]["files"].items():
                if HệĐiềuHành.path_kind(đườngDẫn) != 1 or giáTrịDấuNhậnDạng(HệĐiềuHành.read(đườngDẫn)) != dữLiệuDấuNhậnDạng:
                    raise ValueError("설치된 GóiGộp 파일이 달라졌습니다: " + đườngDẫn)
            print("이미 설치됨:", tên, đặcTả["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 giáTrịLùi 설치하십시오.")
    for đườngDẫn in cácMụcTệp:
        if HệĐiềuHành.path_kind(đườngDẫn):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + đườngDẫn)
    danhSáchMục[tên] = {"version": đặcTả["version"], "files": {đườngDẫn: giáTrịDấuNhậnDạng(DữLiệu) for đườngDẫn, DữLiệu in cácMụcTệp.items()}}
    danhSáchMới = json.dumps(danhSáchMục).encode()
    if len(danhSáchMới) > 16384:
        raise ValueError("GóiGộp danhSáchMục cỡ 초과")
    danhSáchTrướcĐó = HệĐiềuHành.read(đườngDẫnDanhSách) if HệĐiềuHành.path_kind(đườngDẫnDanhSách) else None
    tệpĐãTạo = []
    thưMụcĐãTạo = []
    try:
        for đườngDẫn, DữLiệu in cácMụcTệp.items():
            cácPhần = đườngDẫn.split("/")
            for trịSố in range(2, len(cácPhần)):
                giáTrịThưMục = "/".join(cácPhần[:trịSố])
                giáTrịLoại = HệĐiềuHành.path_kind(giáTrịThưMục)
                if giáTrịLoại == 0:
                    HệĐiềuHành.mkdir(giáTrịThưMục)
                    thưMụcĐãTạo.append(giáTrịThưMục)
                elif giáTrịLoại != 2:
                    raise ValueError("giáTrịThưMục 경로에 파일이 있습니다: " + giáTrịThưMục)
            tệpĐãTạo.append(đườngDẫn)
            ghiNhậtKý(đườngDẫn, DữLiệu)
        ghiNhậtKý(đườngDẫnDanhSách, danhSáchMới)
    except Exception:
        for đườngDẫn in tệpĐãTạo:
            if HệĐiềuHành.path_kind(đườngDẫn):
                HệĐiềuHành.remove(đườngDẫn)
        for giáTrịThưMục in reversed(thưMụcĐãTạo):
            HệĐiềuHành.rmdir(giáTrịThưMục)
        if danhSáchTrướcĐó is not None:
            ghiNhậtKý(đườngDẫnDanhSách, danhSáchTrướcĐó)
        elif HệĐiềuHành.path_kind(đườngDẫnDanhSách):
            HệĐiềuHành.remove(đườngDẫnDanhSách)
        raise
    print("càiĐặtGiáTrị làĐầyĐủ:", tên, đặcTả["version"], "→ /lib (RAM)")


def gỡMục(tên):
    danhSáchMục = đọcDanhSách()
    if tên not in danhSáchMục:
        raise ValueError("설치되지 않은 꾸러미입니다: " + tên)
    for đườngDẫn, dữLiệuDấuNhậnDạng in danhSáchMục[tên]["files"].items():
        if HệĐiềuHành.path_kind(đườngDẫn) != 1 or giáTrịDấuNhậnDạng(HệĐiềuHành.read(đườngDẫn)) != dữLiệuDấuNhậnDạng:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + đườngDẫn)
    for đườngDẫn in danhSáchMục[tên]["files"]:
        HệĐiềuHành.remove(đườngDẫn)
    del danhSáchMục[tên]
    ghiNhậtKý(đườngDẫnDanhSách, json.dumps(danhSáchMục).encode())
    print("gỡMục làĐầyĐủ:", tên)


def chạy(cácĐốiSố):
    sốCổng = 8027
    if len(cácĐốiSố) >= 2 and cácĐốiSố[-2] == "--port":
        sốCổng = int(cácĐốiSố[-1])
        cácĐốiSố = cácĐốiSố[:-2]
    if cácĐốiSố == ["list"]:
        for tên, thôngTinHệThống in đọcDanhSách().items():
            print(tên, thôngTinHệThống["version"])
    elif len(cácĐốiSố) == 2 and cácĐốiSố[0] == "install":
        càiĐặtGiáTrị(cácĐốiSố[1], sốCổng)
    elif len(cácĐốiSố) == 2 and cácĐốiSố[0] == "uninstall":
        gỡMục(cácĐốiSố[1])
    elif not cácĐốiSố or cácĐốiSố in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython câyNguồn 설치기 (PyPA pip 전체가 아님)")
        print("pip install tên[==버전] [--port 8027] | pip list | pip uninstall tên")
        print("Chủ: CôngCụ/thựcThiLệnh.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        chạy(sys.argv[1:])
    except Exception as lỗi:
        print("GóiGộp lỗi:", lỗi)
        sys.exit(1)
