"""자체 nüvə_VALUE MicroPython에서 사용하는 한글 FUNCTION_VALUE Ad."""
import jkoros as əməliyyat_sistemi
출력 = print
파일읽기 = əməliyyat_sistemi.read
yazmaq_fayl = əməliyyat_sistemi.write
silmək_fayl = əməliyyat_sistemi.remove
입력읽기 = əməliyyat_sistemi.stdin
네모그리기 = əməliyyat_sistemi.rect
그림기다리기 = əməliyyat_sistemi.wait_key
밀리초 = əməliyyat_sistemi.ticks_ms
전문통신열기 = əməliyyat_sistemi.udp_open
전문보내기 = əməliyyat_sistemi.udp_send
바깥전문보내기 = əməliyyat_sistemi.udp_sendto
전문받기 = əməliyyat_sistemi.udp_recv
bağlamaq_Şəbəkə = əməliyyat_sistemi.udp_close

def 글해독(verilənlər):
    return verilənlər.decode("utf-8")
