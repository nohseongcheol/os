"""자체 커널의 FAYL·통신·화면 호출과 한국어 istisna. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as əməliyyat_sistemi
import sys as ümumi_dil_icrası

def 출력(*VALUE, ayırıcı=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = ayırıcı
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

tam_ədəd = int
명령인수 = ümumi_dil_icrası.argv
다시시도오류 = 11

class sistem_səhv(OSError):
    def __init__(자신, INDEX, 설명="əməliyyat_sistemi 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(FUNCTION_VALUE, *인수):
    try:
        return FUNCTION_VALUE(*인수)
    except OSError as XƏTA:
        INDEX = XƏTA.args[0] if XƏTA.args else 0
        raise sistem_səhv(INDEX)

def 글부호화(Mətn):
    return Mətn.encode("utf-8")

def 글해독(verilənlər):
    return verilənlər.decode("utf-8")

def 파일읽기(Ad):
    return 운영호출(əməliyyat_sistemi.read, Ad)

def yazmaq_fayl(Ad, verilənlər):
    return 운영호출(əməliyyat_sistemi.write, Ad, verilənlər)

def silmək_fayl(Ad):
    return 운영호출(əməliyyat_sistemi.remove, Ad)

def 전문통신열기(접속번호):
    return 운영호출(əməliyyat_sistemi.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, verilənlər):
    return 운영호출(əməliyyat_sistemi.udp_send, 종단, 접속번호, verilənlər)

def 바깥전문보내기(종단, ünvan, 접속번호, verilənlər):
    return 운영호출(əməliyyat_sistemi.udp_sendto, 종단, ünvan, 접속번호, verilənlər)

def 전문받기(종단):
    return 운영호출(əməliyyat_sistemi.udp_recv, 종단)

def bağlamaq_Şəbəkə(종단):
    return 운영호출(əməliyyat_sistemi.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(əməliyyat_sistemi.rect, *인수)

def 화면크기():
    return 운영호출(əməliyyat_sistemi.screen_size)

def 그림기다리기():
    return 운영호출(əməliyyat_sistemi.wait_key)

밀리초 = əməliyyat_sistemi.ticks_ms
