#include "ağ_ABI.h"
static bulut_yuva_ADRES ADRES(unsigned taşımak_değer) {
    bulut_yuva_ADRES değer = {}; değer.ADRES_Aile = bulut_Aile;
    değer.bağlantı_noktası_numarası = 망차례짧은수(taşımak_değer); değer.İnternet_adresi.ADRES_değer = ağ_bilgi(geri_döngü_adresi); return değer;
}
extern "C" int Start_kullanıcı_program(int) {
    int 보내는곳 = açmak_uç_nokta(bulut_Aile, veri_birimi_yuvası, 0);
    int 받는곳 = açmak_uç_nokta(bulut_Aile, veri_birimi_yuvası, veri_birimi_protokol);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    bulut_yuva_ADRES 도착 = ADRES(7777), 출발 = ADRES(7778), 보낸주소 = {};
    yuva_ADRES_süre_TÜR ADRES_süre = sizeof(보낸주소);
    if (BIND_ADRES(받는곳, (yuva_ADRES *)&도착, sizeof(도착))) return 2;
    if (BIND_ADRES(보내는곳, (yuva_ADRES *)&도착, sizeof(도착)) != -1 || hata_numarası != 98) return 3;
    if (BIND_ADRES(보내는곳, (yuva_ADRES *)&출발, sizeof(출발))) return 4;
    static const char içerik_değer[] = "한글 UDP loopback 😀";
    char GETİRİ_değer[64] = {};
    if (göndermek_veri_birimi_veri(보내는곳, içerik_değer, sizeof(içerik_değer), 0, (yuva_ADRES *)&도착, sizeof(도착)) != sizeof(içerik_değer)) return 5;
    if (almak_veri_birimi_veri(받는곳, (void *)içerik_değer, sizeof(içerik_değer), 0, 0, 0) != -1 || hata_numarası != 14) return 6;
    if (almak_veri_birimi_veri(받는곳, GETİRİ_değer, sizeof(GETİRİ_değer), 0, (yuva_ADRES *)&보낸주소, &ADRES_süre) != sizeof(içerik_değer)) return 7;
    if (ADRES_süre != sizeof(보낸주소) || 장치차례짧은수(보낸주소.bağlantı_noktası_numarası) != 7778 || cihaz_düzen_bilgi(보낸주소.İnternet_adresi.ADRES_değer) != geri_döngü_adresi) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(içerik_değer); 순번++) if (GETİRİ_değer[순번] != içerik_değer[순번]) return 9;
    if (almak_veri_birimi_veri(받는곳, GETİRİ_değer, sizeof(GETİRİ_değer), 0, 0, 0) != -1 || hata_numarası != 11) return 10;
    if (göndermek_veri_birimi_veri(받는곳, GETİRİ_değer, sizeof(içerik_değer), 0, (yuva_ADRES *)&보낸주소, sizeof(보낸주소)) != sizeof(içerik_değer)) return 11;
    if (almak_veri_birimi_veri(보내는곳, GETİRİ_değer, 4, 0, 0, 0) != 4) return 12;
    if (almak_veri_birimi_veri(보내는곳, GETİRİ_değer, 4, 0, 0, 0) != -1 || hata_numarası != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (göndermek_veri_birimi_veri(보내는곳, içerik_değer, sizeof(içerik_değer), 0, (yuva_ADRES *)&도착, sizeof(도착)) != sizeof(içerik_değer)) return 14;
    if (göndermek_veri_birimi_veri(보내는곳, içerik_değer, sizeof(içerik_değer), 0, (yuva_ADRES *)&도착, sizeof(도착)) != -1 || hata_numarası != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (almak_veri_birimi_veri(받는곳, GETİRİ_değer, sizeof(GETİRİ_değer), 0, 0, 0) != sizeof(içerik_değer)) return 16;
    if (göndermek_veri_birimi_veri(보내는곳, 0, 0, 0, (yuva_ADRES *)&도착, sizeof(도착)) != 0 ||
        almak_veri_birimi_veri(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.İnternet_adresi.ADRES_değer = ağ_bilgi(0x08080808);
    if (göndermek_veri_birimi_veri(보내는곳, içerik_değer, sizeof(içerik_değer), 0, (yuva_ADRES *)&도착, sizeof(도착)) != -1 || hata_numarası != 101) return 17;
    if (açmak_uç_nokta(bulut_Aile, akış_ağ, veri_birimi_protokol) != -1 || hata_numarası != 93) return 18;
    ADRES_süre = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (yuva_ADRES *)&보낸주소, &ADRES_süre) || 장치차례짧은수(보낸주소.bağlantı_noktası_numarası) != 7777) return 19;
    if (Kapat_Dosya(받는곳) || Kapat_Dosya(받는곳) != -1 || hata_numarası != 9) return 20;
    // 보내는곳은 열어 둔다: Çıkış_program 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    yazma_Dosya_veri(1, 완료, sizeof(완료) - 1);
    return 0;
}
