"""자체 kernel_atuutilik MicroPython에서 사용하는 한글 sugiakkannirut_atuutilik atiq."""
import jkoros as qarasaujakkut_aulattijjut
출력 = print
파일읽기 = qarasaujakkut_aulattijjut.read
titiraq_ini = qarasaujakkut_aulattijjut.write
sanirvalli_ini = qarasaujakkut_aulattijjut.remove
입력읽기 = qarasaujakkut_aulattijjut.stdin
네모그리기 = qarasaujakkut_aulattijjut.rect
그림기다리기 = qarasaujakkut_aulattijjut.wait_key
밀리초 = qarasaujakkut_aulattijjut.ticks_ms
전문통신열기 = qarasaujakkut_aulattijjut.udp_open
전문보내기 = qarasaujakkut_aulattijjut.udp_send
바깥전문보내기 = qarasaujakkut_aulattijjut.udp_sendto
전문받기 = qarasaujakkut_aulattijjut.udp_recv
matuli_Kasuqatigiitsimajut = qarasaujakkut_aulattijjut.udp_close

def 글해독(titiqqat):
    return titiqqat.decode("utf-8")
