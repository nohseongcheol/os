"""자체 커널의 Fayil·통신·화면 호출과 한국어 banbanchi. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as OS
import sys as lokacin_bude_yaren_gama_gari

def 출력(*Daraja, mai_rabawa=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = mai_rabawa
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*Daraja, **기존인수)

Lamba_mara = int
명령인수 = lokacin_bude_yaren_gama_gari.argv
다시시도오류 = 11

class na_ura_Kuskure(OSError):
    def __init__(자신, Indes, 설명="OS 작업에 실패했습니다."):
        super().__init__(Indes, 설명)
        자신.Indes = Indes
        자신.설명 = 설명

def 운영호출(AIKI_Daraja, *인수):
    try:
        return AIKI_Daraja(*인수)
    except OSError as Kuskure:
        Indes = Kuskure.args[0] if Kuskure.args else 0
        raise na_ura_Kuskure(Indes)

def 글부호화(SMS):
    return SMS.encode("utf-8")

def 글해독(Tarin_bayani):
    return Tarin_bayani.decode("utf-8")

def 파일읽기(Suna):
    return 운영호출(OS.read, Suna)

def Rubuta_Fayil(Suna, Tarin_bayani):
    return 운영호출(OS.write, Suna, Tarin_bayani)

def Cire_Fayil(Suna):
    return 운영호출(OS.remove, Suna)

def 전문통신열기(lambar_kafa):
    return 운영호출(OS.udp_open, lambar_kafa)

def 전문보내기(종단, lambar_kafa, Tarin_bayani):
    return 운영호출(OS.udp_send, 종단, lambar_kafa, Tarin_bayani)

def 바깥전문보내기(종단, imel, lambar_kafa, Tarin_bayani):
    return 운영호출(OS.udp_sendto, 종단, imel, lambar_kafa, Tarin_bayani)

def 전문받기(종단):
    return 운영호출(OS.udp_recv, 종단)

def Rufe_Hanyar_sadarwa(종단):
    return 운영호출(OS.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(OS.rect, *인수)

def 화면크기():
    return 운영호출(OS.screen_size)

def 그림기다리기():
    return 운영호출(OS.wait_key)

밀리초 = OS.ticks_ms
