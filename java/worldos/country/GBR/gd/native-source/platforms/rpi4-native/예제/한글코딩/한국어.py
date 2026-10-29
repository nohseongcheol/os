"""자체 eitean_VALUE MicroPython에서 사용하는 한글 FUNCTION_VALUE Ainm."""
import jkoros as siostam_obrachaidh
출력 = print
파일읽기 = siostam_obrachaidh.read
sgrìobh_faidhle = siostam_obrachaidh.write
thoir_air_falbh_faidhle = siostam_obrachaidh.remove
입력읽기 = siostam_obrachaidh.stdin
네모그리기 = siostam_obrachaidh.rect
그림기다리기 = siostam_obrachaidh.wait_key
밀리초 = siostam_obrachaidh.ticks_ms
전문통신열기 = siostam_obrachaidh.udp_open
전문보내기 = siostam_obrachaidh.udp_send
바깥전문보내기 = siostam_obrachaidh.udp_sendto
전문받기 = siostam_obrachaidh.udp_recv
dùin_lìonra = siostam_obrachaidh.udp_close

def 글해독(dàta):
    return dàta.decode("utf-8")
