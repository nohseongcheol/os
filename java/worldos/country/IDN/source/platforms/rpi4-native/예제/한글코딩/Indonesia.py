"""Asli kernel_VALUE MicroPython에서 사용하는 한글 fungsi_VALUE Nama_2."""
import jkoros as sistem_operasi
keluaranTeks = print
파일읽기 = sistem_operasi.read
tulis_file = sistem_operasi.write
hapus_file = sistem_operasi.remove
입력읽기 = sistem_operasi.stdin
Gambar_persegi = sistem_operasi.rect
그림기다리기 = sistem_operasi.wait_key
밀리초 = sistem_operasi.ticks_ms
전문통신열기 = sistem_operasi.udp_open
전문보내기 = sistem_operasi.udp_send
바깥전문보내기 = sistem_operasi.udp_sendto
전문받기 = sistem_operasi.udp_recv
Tutup_jaringan = sistem_operasi.udp_close

def 글해독(data):
    return data.decode("utf-8")
