"""Öz 커널의 dosya·iletişim·화면 호출과 Türkçe özel_durum. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as işletim_sistemi
import sys as CLR

def metinÇıktısı(*değer, ayıraç=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = ayıraç
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*değer, **기존인수)

bilgi = int
명령인수 = CLR.argv
다시시도오류 = 11

class sistem_hatası(OSError):
    def __init__(자신, Dizin, 설명="işletim_sistemi 작업에 실패했습니다."):
        super().__init__(Dizin, 설명)
        자신.Dizin = Dizin
        자신.설명 = 설명

def 운영호출(işlev_değer, *bağımsız_değişkenler):
    try:
        return işlev_değer(*bağımsız_değişkenler)
    except OSError as hata:
        Dizin = hata.args[0] if hata.args else 0
        raise sistem_hatası(Dizin)

def kodlamak_SMS(metin):
    return metin.encode("utf-8")

def 글해독(veri):
    return veri.decode("utf-8")

def 파일읽기(İsim):
    return 운영호출(işletim_sistemi.read, İsim)

def yazma_Dosya(İsim, veri):
    return 운영호출(işletim_sistemi.write, İsim, veri)

def kaldırmak_Dosya(İsim):
    return 운영호출(işletim_sistemi.remove, İsim)

def açık_veri_birimi(bağlantı_noktası_numarası):
    return 운영호출(işletim_sistemi.udp_open, bağlantı_noktası_numarası)

def göndermek_veri_birimi(uç_nokta, bağlantı_noktası_numarası, veri):
    return 운영호출(işletim_sistemi.udp_send, uç_nokta, bağlantı_noktası_numarası, veri)

def göndermek_dış_veri_birimi(uç_nokta, ADRES, bağlantı_noktası_numarası, veri):
    return 운영호출(işletim_sistemi.udp_sendto, uç_nokta, ADRES, bağlantı_noktası_numarası, veri)

def almak_veri_birimi(uç_nokta):
    return 운영호출(işletim_sistemi.udp_recv, uç_nokta)

def Kapat_ağ(uç_nokta):
    return 운영호출(işletim_sistemi.udp_close, uç_nokta)

def Çizim_dikdörtgen(*bağımsız_değişkenler):
    return 운영호출(işletim_sistemi.rect, *bağımsız_değişkenler)

def 화면크기():
    return 운영호출(işletim_sistemi.screen_size)

def 그림기다리기():
    return 운영호출(işletim_sistemi.wait_key)

밀리초 = işletim_sistemi.ticks_ms
