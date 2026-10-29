"""자체 커널의 फायल·통신·화면 호출과 한국어 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as ऑपरेटिंग_प्रणाली
import sys as सामान्य_भास_रनटायम

def 출력(*मोल, विभाजक=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = विभाजक
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*मोल, **기존인수)

पुर्णांक = int
명령인수 = सामान्य_भास_रनटायम.argv
다시시도오류 = 11

class प्रणाली_चूक(OSError):
    def __init__(자신, INDEX, 설명="ऑपरेटिंग_प्रणाली 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(फंक्शन_मोल, *인수):
    try:
        return फंक्शन_मोल(*인수)
    except OSError as चूक:
        INDEX = चूक.args[0] if चूक.args else 0
        raise प्रणाली_चूक(INDEX)

def 글부호화(SMS):
    return SMS.encode("utf-8")

def 글해독(डेटा):
    return डेटा.decode("utf-8")

def 파일읽기(नांव):
    return 운영호출(ऑपरेटिंग_प्रणाली.read, नांव)

def बरोवचें_फायल(नांव, डेटा):
    return 운영호출(ऑपरेटिंग_प्रणाली.write, नांव, डेटा)

def काडचें_फायल(नांव):
    return 운영호출(ऑपरेटिंग_प्रणाली.remove, नांव)

def 전문통신열기(접속번호):
    return 운영호출(ऑपरेटिंग_प्रणाली.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, डेटा):
    return 운영호출(ऑपरेटिंग_प्रणाली.udp_send, 종단, 접속번호, डेटा)

def 바깥전문보내기(종단, नामो, 접속번호, डेटा):
    return 운영호출(ऑपरेटिंग_प्रणाली.udp_sendto, 종단, नामो, 접속번호, डेटा)

def 전문받기(종단):
    return 운영호출(ऑपरेटिंग_प्रणाली.udp_recv, 종단)

def शेवट_नॅटवर्क(종단):
    return 운영호출(ऑपरेटिंग_प्रणाली.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(ऑपरेटिंग_प्रणाली.rect, *인수)

def 화면크기():
    return 운영호출(ऑपरेटिंग_प्रणाली.screen_size)

def 그림기다리기():
    return 운영호출(ऑपरेटिंग_प्रणाली.wait_key)

밀리초 = ऑपरेटिंग_प्रणाली.ticks_ms
