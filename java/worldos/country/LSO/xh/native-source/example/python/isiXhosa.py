"""자체 커널의 iFayili·통신·화면 호출과 isiXhosa 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as Indlela_yokusebenza
import sys as ixesha_lokusebenza_kolwimi_oluqhelekileyo

def 출력(*ixabiso, umahluli=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = umahluli
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*ixabiso, **기존인수)

inani_elipheleleyo = int
명령인수 = ixesha_lokusebenza_kolwimi_oluqhelekileyo.argv
다시시도오류 = 11

class inkqubo_impazamo(OSError):
    def __init__(자신, indeksa, 설명="Indlela_yokusebenza 작업에 실패했습니다."):
        super().__init__(indeksa, 설명)
        자신.indeksa = indeksa
        자신.설명 = 설명

def 운영호출(INKQUBO_ixabiso, *인수):
    try:
        return INKQUBO_ixabiso(*인수)
    except OSError as Impazamo:
        indeksa = Impazamo.args[0] if Impazamo.args else 0
        raise inkqubo_impazamo(indeksa)

def 글부호화(Umbhalo):
    return Umbhalo.encode("utf-8")

def 글해독(iingcombolo):
    return iingcombolo.decode("utf-8")

def 파일읽기(Igama):
    return 운영호출(Indlela_yokusebenza.read, Igama)

def bhala_ifayile(Igama, iingcombolo):
    return 운영호출(Indlela_yokusebenza.write, Igama, iingcombolo)

def shenxisa_ifayile(Igama):
    return 운영호출(Indlela_yokusebenza.remove, Igama)

def 전문통신열기(접속번호):
    return 운영호출(Indlela_yokusebenza.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, iingcombolo):
    return 운영호출(Indlela_yokusebenza.udp_send, 종단, 접속번호, iingcombolo)

def 바깥전문보내기(종단, idilesi, 접속번호, iingcombolo):
    return 운영호출(Indlela_yokusebenza.udp_sendto, 종단, idilesi, 접속번호, iingcombolo)

def 전문받기(종단):
    return 운영호출(Indlela_yokusebenza.udp_recv, 종단)

def vala_Inethiwekhi(종단):
    return 운영호출(Indlela_yokusebenza.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(Indlela_yokusebenza.rect, *인수)

def 화면크기():
    return 운영호출(Indlela_yokusebenza.screen_size)

def 그림기다리기():
    return 운영호출(Indlela_yokusebenza.wait_key)

밀리초 = Indlela_yokusebenza.ticks_ms
