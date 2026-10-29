from Türkçe import metinÇıktısı, açık_veri_birimi, göndermek_dış_veri_birimi, almak_veri_birimi, Kapat_ağ, 밀리초
from Türkçe import sistem_hatası, 다시시도오류, kodlamak_SMS, 명령인수, bilgi
uç_nokta = açık_veri_birimi(0)
try:
    veri_birimi = kodlamak_SMS("PYTHON UDP Türkçe")
    göndermek_dış_veri_birimi(uç_nokta, "10.0.2.2", bilgi(명령인수[1]), veri_birimi)
    çalıştır = 밀리초()
    while True:
        try:
            yanıt, taşımak_değer = almak_veri_birimi(uç_nokta)
            break
        except sistem_hatası as hata:
            if hata.Dizin != 다시시도오류 or 밀리초() - çalıştır >= 700:
                raise
    assert yanıt == veri_birimi
    metinÇıktısı("PYTHON 네트워크 doğrulamak: UDP Türkçe")
finally:
    Kapat_ağ(uç_nokta)
