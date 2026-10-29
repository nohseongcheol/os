"""Asli kernel_VALUE MicroPython에서 사용하는 한글 fungsi_VALUE Nama."""
import jkoros as sistem_pengendalian
출력 = print
파일읽기 = sistem_pengendalian.read
tulis_fail = sistem_pengendalian.write
alih_keluar_fail = sistem_pengendalian.remove
입력읽기 = sistem_pengendalian.stdin
Lukis_segi_empat_tepat = sistem_pengendalian.rect
그림기다리기 = sistem_pengendalian.wait_key
밀리초 = sistem_pengendalian.ticks_ms
전문통신열기 = sistem_pengendalian.udp_open
전문보내기 = sistem_pengendalian.udp_send
바깥전문보내기 = sistem_pengendalian.udp_sendto
전문받기 = sistem_pengendalian.udp_recv
Tutup_rangkaian = sistem_pengendalian.udp_close

def 글해독(data):
    return data.decode("utf-8")
