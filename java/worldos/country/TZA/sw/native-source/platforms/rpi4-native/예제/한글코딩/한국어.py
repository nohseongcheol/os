"""자체 kiini_thamani_0611a8a8 MicroPython에서 사용하는 한글 KITENDAKAZI_thamani Jina."""
import jkoros as mfumo_endeshi
출력 = print
파일읽기 = mfumo_endeshi.read
andika_faili = mfumo_endeshi.write
ondoa_faili = mfumo_endeshi.remove
입력읽기 = mfumo_endeshi.stdin
네모그리기 = mfumo_endeshi.rect
그림기다리기 = mfumo_endeshi.wait_key
밀리초 = mfumo_endeshi.ticks_ms
전문통신열기 = mfumo_endeshi.udp_open
전문보내기 = mfumo_endeshi.udp_send
바깥전문보내기 = mfumo_endeshi.udp_sendto
전문받기 = mfumo_endeshi.udp_recv
funga_Mtandao = mfumo_endeshi.udp_close

def 글해독(data):
    return data.decode("utf-8")
