"""자체 커널의 Fichier·통신·화면 호출과 한국어 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as Betribssystem
import sys as Common_Language_Runtime

def 출력(*VALUE, Trennzeechen=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = Trennzeechen
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

Ganzzuel = int
명령인수 = Common_Language_Runtime.argv
다시시도오류 = 11

class System_Feeler(OSError):
    def __init__(자신, INDEX, 설명="Betribssystem 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(FUNCTION_VALUE, *인수):
    try:
        return FUNCTION_VALUE(*인수)
    except OSError as Feeler:
        INDEX = Feeler.args[0] if Feeler.args else 0
        raise System_Feeler(INDEX)

def 글부호화(SMS):
    return SMS.encode("utf-8")

def 글해독(Daten):
    return Daten.decode("utf-8")

def 파일읽기(Numm):
    return 운영호출(Betribssystem.read, Numm)

def schreiwen_Fichier(Numm, Daten):
    return 운영호출(Betribssystem.write, Numm, Daten)

def ewechhuelen_Fichier(Numm):
    return 운영호출(Betribssystem.remove, Numm)

def 전문통신열기(접속번호):
    return 운영호출(Betribssystem.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, Daten):
    return 운영호출(Betribssystem.udp_send, 종단, 접속번호, Daten)

def 바깥전문보내기(종단, Adress, 접속번호, Daten):
    return 운영호출(Betribssystem.udp_sendto, 종단, Adress, 접속번호, Daten)

def 전문받기(종단):
    return 운영호출(Betribssystem.udp_recv, 종단)

def Clôture_Reseau(종단):
    return 운영호출(Betribssystem.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(Betribssystem.rect, *인수)

def 화면크기():
    return 운영호출(Betribssystem.screen_size)

def 그림기다리기():
    return 운영호출(Betribssystem.wait_key)

밀리초 = Betribssystem.ticks_ms
