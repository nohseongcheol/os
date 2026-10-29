"""자체 커널의 faili·통신·화면 호출과 한국어 vighairi. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as mfumo_endeshi
import sys as muda_wa_kuendesha_lugha_ya_kawaida

def 출력(*thamani, kitenganishi=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = kitenganishi
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*thamani, **기존인수)

namba_kamili = int
명령인수 = muda_wa_kuendesha_lugha_ya_kawaida.argv
다시시도오류 = 11

class mfumo_kosa(OSError):
    def __init__(자신, kielezo, 설명="mfumo_endeshi 작업에 실패했습니다."):
        super().__init__(kielezo, 설명)
        자신.kielezo = kielezo
        자신.설명 = 설명

def 운영호출(KITENDAKAZI_thamani, *인수):
    try:
        return KITENDAKAZI_thamani(*인수)
    except OSError as kosa:
        kielezo = kosa.args[0] if kosa.args else 0
        raise mfumo_kosa(kielezo)

def 글부호화(SMS):
    return SMS.encode("utf-8")

def 글해독(data):
    return data.decode("utf-8")

def 파일읽기(Jina):
    return 운영호출(mfumo_endeshi.read, Jina)

def andika_faili(Jina, data):
    return 운영호출(mfumo_endeshi.write, Jina, data)

def ondoa_faili(Jina):
    return 운영호출(mfumo_endeshi.remove, Jina)

def 전문통신열기(namba_ya_kituo):
    return 운영호출(mfumo_endeshi.udp_open, namba_ya_kituo)

def 전문보내기(종단, namba_ya_kituo, data):
    return 운영호출(mfumo_endeshi.udp_send, 종단, namba_ya_kituo, data)

def 바깥전문보내기(종단, anwani, namba_ya_kituo, data):
    return 운영호출(mfumo_endeshi.udp_sendto, 종단, anwani, namba_ya_kituo, data)

def 전문받기(종단):
    return 운영호출(mfumo_endeshi.udp_recv, 종단)

def funga_Mtandao(종단):
    return 운영호출(mfumo_endeshi.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(mfumo_endeshi.rect, *인수)

def 화면크기():
    return 운영호출(mfumo_endeshi.screen_size)

def 그림기다리기():
    return 운영호출(mfumo_endeshi.wait_key)

밀리초 = mfumo_endeshi.ticks_ms
