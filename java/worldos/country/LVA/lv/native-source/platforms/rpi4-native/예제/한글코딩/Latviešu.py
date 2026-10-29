"""savs kodols_VALUE MicroPython에서 사용하는 한글 FUNCTION_VALUE Nosaukums."""
import jkoros as operētājsistēma
Izvade = print
파일읽기 = operētājsistēma.read
rakstīšana_Fails = operētājsistēma.write
noņemt_Fails = operētājsistēma.remove
입력읽기 = operētājsistēma.stdin
zīmēt_taisnstūris = operētājsistēma.rect
그림기다리기 = operētājsistēma.wait_key
밀리초 = operētājsistēma.ticks_ms
atvērt_datogramma = operētājsistēma.udp_open
sūtīt_datogramma = operētājsistēma.udp_send
sūtīt_ārējs_datogramma = operētājsistēma.udp_sendto
saņemt_datogramma = operētājsistēma.udp_recv
Aizvērt_tīkls = operētājsistēma.udp_close

def 글해독(dati):
    return dati.decode("utf-8")
