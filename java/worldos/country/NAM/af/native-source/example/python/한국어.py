"""자체 커널의 Lêer·통신·화면 호출과 한국어 uitsondering. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as bedryfstelsel
import sys as algemene_taallooptyd

def Afvoer(*VALUE, verdeelstreep=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = verdeelstreep
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

heelgetal = int
명령인수 = algemene_taallooptyd.argv
다시시도오류 = 11

class stelsel_fout(OSError):
    def __init__(자신, INDEX, 설명="bedryfstelsel 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(funksie_VALUE, *인수):
    try:
        return funksie_VALUE(*인수)
    except OSError as Fout:
        INDEX = Fout.args[0] if Fout.args else 0
        raise stelsel_fout(INDEX)

def 글부호화(Teks):
    return Teks.encode("utf-8")

def 글해독(data):
    return data.decode("utf-8")

def 파일읽기(Naam):
    return 운영호출(bedryfstelsel.read, Naam)

def skryf_lêer(Naam, data):
    return 운영호출(bedryfstelsel.write, Naam, data)

def verwyder_lêer(Naam):
    return 운영호출(bedryfstelsel.remove, Naam)

def 전문통신열기(접속번호):
    return 운영호출(bedryfstelsel.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, data):
    return 운영호출(bedryfstelsel.udp_send, 종단, 접속번호, data)

def 바깥전문보내기(종단, adres, 접속번호, data):
    return 운영호출(bedryfstelsel.udp_sendto, 종단, adres, 접속번호, data)

def 전문받기(종단):
    return 운영호출(bedryfstelsel.udp_recv, 종단)

def sluit_Netwerk(종단):
    return 운영호출(bedryfstelsel.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(bedryfstelsel.rect, *인수)

def 화면크기():
    return 운영호출(bedryfstelsel.screen_size)

def 그림기다리기():
    return 운영호출(bedryfstelsel.wait_key)

밀리초 = bedryfstelsel.ticks_ms
