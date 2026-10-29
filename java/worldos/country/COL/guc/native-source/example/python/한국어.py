"""자체 커널의 anaajaalaa·통신·화면 호출과 한국어 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as a_yatawajiraaya_a_laülaasü
import sys as 실행환경

def 출력(*ajutuu, 사이=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = 사이
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*ajutuu, **기존인수)

waneepiasü = int
명령인수 = 실행환경.argv
다시시도오류 = 11

class a_yatawaajiraaya_ajachitia(OSError):
    def __init__(자신, ee_iyatialujuna, 설명="a_yatawajiraaya_a_laülaasü 작업에 실패했습니다."):
        super().__init__(ee_iyatialujuna, 설명)
        자신.ee_iyatialujuna = ee_iyatialujuna
        자신.설명 = 설명

def 운영호출(함수, *인수):
    try:
        return 함수(*인수)
    except OSError as ajachitia:
        ee_iyatialujuna = ajachitia.args[0] if ajachitia.args else 0
        raise a_yatawaajiraaya_ajachitia(ee_iyatialujuna)

def 글부호화(글):
    return 글.encode("utf-8")

def 글해독(atijaaya):
    return atijaaya.decode("utf-8")

def 파일읽기(이름):
    return 운영호출(a_yatawajiraaya_a_laülaasü.read, 이름)

def ashajaa_anaajaalaa(이름, atijaaya):
    return 운영호출(a_yatawajiraaya_a_laülaasü.write, 이름, atijaaya)

def 파일지우기(이름):
    return 운영호출(a_yatawajiraaya_a_laülaasü.remove, 이름)

def 전문통신열기(접속번호):
    return 운영호출(a_yatawajiraaya_a_laülaasü.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, atijaaya):
    return 운영호출(a_yatawajiraaya_a_laülaasü.udp_send, 종단, 접속번호, atijaaya)

def 바깥전문보내기(종단, ejepüsee, 접속번호, atijaaya):
    return 운영호출(a_yatawajiraaya_a_laülaasü.udp_sendto, 종단, ejepüsee, 접속번호, atijaaya)

def 전문받기(종단):
    return 운영호출(a_yatawajiraaya_a_laülaasü.udp_recv, 종단)

def asürülaa_kusu(종단):
    return 운영호출(a_yatawajiraaya_a_laülaasü.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(a_yatawajiraaya_a_laülaasü.rect, *인수)

def 화면크기():
    return 운영호출(a_yatawajiraaya_a_laülaasü.screen_size)

def 그림기다리기():
    return 운영호출(a_yatawajiraaya_a_laülaasü.wait_key)

밀리초 = a_yatawajiraaya_a_laülaasü.ticks_ms
