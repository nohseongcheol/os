"""자체 커널의 ፋይል·통신·화면 호출과 አማርኛ ልዩነት. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as ስርዓተ_ክወና
import sys as የጋራ_ቋንቋ_ማስኬጃ_ጊዜ

def ውጤት(*እሴት, ከፋፋይ=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = ከፋፋይ
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*እሴት, **기존인수)

ኢንተጀር = int
명령인수 = የጋራ_ቋንቋ_ማስኬጃ_ጊዜ.argv
다시시도오류 = 11

class ስርዓት_ስህተት(OSError):
    def __init__(자신, መረጃ_ጠቆመ, 설명="ስርዓተ_ክወና 작업에 실패했습니다."):
        super().__init__(መረጃ_ጠቆመ, 설명)
        자신.መረጃ_ጠቆመ = መረጃ_ጠቆመ
        자신.설명 = 설명

def 운영호출(ተግባር_እሴት, *인수):
    try:
        return ተግባር_እሴት(*인수)
    except OSError as ስህተት:
        መረጃ_ጠቆመ = ስህተት.args[0] if ስህተት.args else 0
        raise ስርዓት_ስህተት(መረጃ_ጠቆመ)

def 글부호화(ጽሁፍ):
    return ጽሁፍ.encode("utf-8")

def 글해독(ውሂብ):
    return ውሂብ.decode("utf-8")

def 파일읽기(ስም):
    return 운영호출(ስርዓተ_ክወና.read, ስም)

def ጻፍ_ፋይል(ስም, ውሂብ):
    return 운영호출(ስርዓተ_ክወና.write, ስም, ውሂብ)

def አስወግድ_ፋይል(ስም):
    return 운영호출(ስርዓተ_ክወና.remove, ስም)

def 전문통신열기(የወደብ_ቁጥር):
    return 운영호출(ስርዓተ_ክወና.udp_open, የወደብ_ቁጥር)

def 전문보내기(종단, የወደብ_ቁጥር, ውሂብ):
    return 운영호출(ስርዓተ_ክወና.udp_send, 종단, የወደብ_ቁጥር, ውሂብ)

def 바깥전문보내기(종단, አድራሻ, የወደብ_ቁጥር, ውሂብ):
    return 운영호출(ስርዓተ_ክወና.udp_sendto, 종단, አድራሻ, የወደብ_ቁጥር, ውሂብ)

def 전문받기(종단):
    return 운영호출(ስርዓተ_ክወና.udp_recv, 종단)

def ዝጋ_መረብ(종단):
    return 운영호출(ስርዓተ_ክወና.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(ስርዓተ_ክወና.rect, *인수)

def 화면크기():
    return 운영호출(ስርዓተ_ክወና.screen_size)

def 그림기다리기():
    return 운영호출(ስርዓተ_ክወና.wait_key)

밀리초 = ስርዓተ_ክወና.ticks_ms
