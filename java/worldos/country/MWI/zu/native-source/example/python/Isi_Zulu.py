"""자체 커널의 Ihele·통신·화면 호출과 Isi_Zulu 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as isistimu_yokusebenza
import sys as isikhathi_sokusebenza_solimi_esivamile

def 출력(*inani, isihlukanisi=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = isihlukanisi
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*inani, **기존인수)

inamba = int
명령인수 = isikhathi_sokusebenza_solimi_esivamile.argv
다시시도오류 = 11

class isistimu_iphutha(OSError):
    def __init__(자신, thola_inkomba, 설명="isistimu_yokusebenza 작업에 실패했습니다."):
        super().__init__(thola_inkomba, 설명)
        자신.thola_inkomba = thola_inkomba
        자신.설명 = 설명

def 운영호출(umsebenzi_inani, *인수):
    try:
        return umsebenzi_inani(*인수)
    except OSError as Iphutha:
        thola_inkomba = Iphutha.args[0] if Iphutha.args else 0
        raise isistimu_iphutha(thola_inkomba)

def 글부호화(Itekisi):
    return Itekisi.encode("utf-8")

def 글해독(imininingwane):
    return imininingwane.decode("utf-8")

def 파일읽기(Igama):
    return 운영호출(isistimu_yokusebenza.read, Igama)

def bhala_ifayela(Igama, imininingwane):
    return 운영호출(isistimu_yokusebenza.write, Igama, imininingwane)

def khipha_ifayela(Igama):
    return 운영호출(isistimu_yokusebenza.remove, Igama)

def 전문통신열기(접속번호):
    return 운영호출(isistimu_yokusebenza.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, imininingwane):
    return 운영호출(isistimu_yokusebenza.udp_send, 종단, 접속번호, imininingwane)

def 바깥전문보내기(종단, ikheli, 접속번호, imininingwane):
    return 운영호출(isistimu_yokusebenza.udp_sendto, 종단, ikheli, 접속번호, imininingwane)

def 전문받기(종단):
    return 운영호출(isistimu_yokusebenza.udp_recv, 종단)

def vala_iNethiwekhi(종단):
    return 운영호출(isistimu_yokusebenza.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(isistimu_yokusebenza.rect, *인수)

def 화면크기():
    return 운영호출(isistimu_yokusebenza.screen_size)

def 그림기다리기():
    return 운영호출(isistimu_yokusebenza.wait_key)

밀리초 = isistimu_yokusebenza.ticks_ms
