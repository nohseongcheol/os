"""자체 커널의 ፋይል·통신·화면 호출과 ትግርኛ 예외. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as ስርዓት_ስርሒት
import sys as ግዜ_ስራሕ_ናይ_ሓባር_ቛንቛ

def 출력(*ዋጋ, ፈላዪ=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = ፈላዪ
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*ዋጋ, **기존인수)

ኢንቲጀር = int
명령인수 = ግዜ_ስራሕ_ናይ_ሓባር_ቛንቛ.argv
다시시도오류 = 11

class ስርዓት_ጌጋ(OSError):
    def __init__(자신, መሐበሪ, 설명="ስርዓት_ስርሒት 작업에 실패했습니다."):
        super().__init__(መሐበሪ, 설명)
        자신.መሐበሪ = መሐበሪ
        자신.설명 = 설명

def 운영호출(ተግባር_ዋጋ, *인수):
    try:
        return ተግባር_ዋጋ(*인수)
    except OSError as ጌጋ:
        መሐበሪ = ጌጋ.args[0] if ጌጋ.args else 0
        raise ስርዓት_ጌጋ(መሐበሪ)

def 글부호화(ጽሑፍ):
    return ጽሑፍ.encode("utf-8")

def 글해독(ሓበሬታ):
    return ሓበሬታ.decode("utf-8")

def 파일읽기(ሽም):
    return 운영호출(ስርዓት_ስርሒት.read, ሽም)

def ጸሓፍ_ፋይል(ሽም, ሓበሬታ):
    return 운영호출(ስርዓት_ስርሒት.write, ሽም, ሓበሬታ)

def ኣልግስ_ፋይል(ሽም):
    return 운영호출(ስርዓት_ስርሒት.remove, ሽም)

def 전문통신열기(접속번호):
    return 운영호출(ስርዓት_ስርሒት.udp_open, 접속번호)

def 전문보내기(종단, 접속번호, ሓበሬታ):
    return 운영호출(ስርዓት_ስርሒት.udp_send, 종단, 접속번호, ሓበሬታ)

def 바깥전문보내기(종단, ኣድራሻ, 접속번호, ሓበሬታ):
    return 운영호출(ስርዓት_ስርሒት.udp_sendto, 종단, ኣድራሻ, 접속번호, ሓበሬታ)

def 전문받기(종단):
    return 운영호출(ስርዓት_ስርሒት.udp_recv, 종단)

def ዕጸው_ማሕበራዊ_ኔትወርክ(종단):
    return 운영호출(ስርዓት_ስርሒት.udp_close, 종단)

def 네모그리기(*인수):
    return 운영호출(ስርዓት_ስርሒት.rect, *인수)

def 화면크기():
    return 운영호출(ስርዓት_ስርሒት.screen_size)

def 그림기다리기():
    return 운영호출(ስርዓት_ስርሒት.wait_key)

밀리초 = ስርዓት_ስርሒት.ticks_ms
