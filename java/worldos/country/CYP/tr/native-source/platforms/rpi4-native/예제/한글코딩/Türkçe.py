"""Öz çekirdek_değer MicroPython에서 사용하는 한글 işlev_değer İsim."""
import jkoros as işletim_sistemi
metinÇıktısı = print
파일읽기 = işletim_sistemi.read
yazma_Dosya = işletim_sistemi.write
kaldırmak_Dosya = işletim_sistemi.remove
입력읽기 = işletim_sistemi.stdin
Çizim_dikdörtgen = işletim_sistemi.rect
그림기다리기 = işletim_sistemi.wait_key
밀리초 = işletim_sistemi.ticks_ms
açık_veri_birimi = işletim_sistemi.udp_open
göndermek_veri_birimi = işletim_sistemi.udp_send
göndermek_dış_veri_birimi = işletim_sistemi.udp_sendto
almak_veri_birimi = işletim_sistemi.udp_recv
Kapat_ağ = işletim_sistemi.udp_close

def 글해독(veri):
    return veri.decode("utf-8")
