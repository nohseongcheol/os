#include "ağ_ABI.h"

int Start_kullanıcı_program(int bağımsız_değişkenler) {
    (void)bağımsız_değişkenler;
    struct bulut_yuva_ADRES ADRES = {0};
    ADRES.ADRES_Aile = bulut_Aile;
    ADRES.bağlantı_noktası_numarası = 망차례짧은수(9260);
    ADRES.İnternet_adresi.ADRES_değer = ağ_bilgi(geri_döngü_adresi);
    int sunucu_değer = açmak_uç_nokta(bulut_Aile, akış_ağ, akış_aktarım_protokolü);
    if (sunucu_değer < 0 || BIND_ADRES(sunucu_değer, (struct yuva_ADRES *)&ADRES, sizeof(ADRES)) < 0 ||
        통신연결기다리기(sunucu_değer, 4) < 0) return 1;
    if (kabul_etmek_ağ_bağlantısı(sunucu_değer, 0, 0) != -1 || hata_numarası != 11) return 2;
    int konuk_değer = açmak_uç_nokta(bulut_Aile, akış_ağ, akış_aktarım_protokolü);
    if (konuk_değer < 0 || bağla_ağ(konuk_değer, (struct yuva_ADRES *)&ADRES, sizeof(ADRES)) < 0) return 3;
    int Bağlan = kabul_etmek_ağ_bağlantısı(sunucu_değer, 0, 0);
    if (Bağlan < 0) return 4;
    unsigned char 보낼것[1500], GETİRİ_öğe[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int süre_değer = yazma_Dosya_veri(konuk_değer, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (süre_değer <= 0) return 5;
        보낸수 += süre_değer;
    }
    if (yazma_Dosya_veri(konuk_değer, 보낼것, 1) != -1 || hata_numarası != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 BACK_değer EOF가 된다. */
    Kapat_Dosya(konuk_değer);
    int GETİRİ_BAĞ_DEĞ_SAY = 0;
    while (GETİRİ_BAĞ_DEĞ_SAY < 보낸수) {
        int süre_değer = 파일자료읽기(Bağlan, GETİRİ_öğe + GETİRİ_BAĞ_DEĞ_SAY, sizeof(GETİRİ_öğe) - GETİRİ_BAĞ_DEĞ_SAY);
        if (süre_değer <= 0) return 7;
        GETİRİ_BAĞ_DEĞ_SAY += süre_değer;
    }
    for (int 수 = 0; 수 < GETİRİ_BAĞ_DEĞ_SAY; 수++) if (GETİRİ_öğe[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Bağlan, GETİRİ_öğe, 1) != 0) return 9;
    if (yazma_Dosya_veri(Bağlan, 보낼것, 1) != -1 || hata_numarası != 32) return 10;
    Kapat_Dosya(Bağlan); Kapat_Dosya(sunucu_değer);
    const char sonuç[] = "C posix-kor 연결형 iletişim PASS\n";
    yazma_Dosya_veri(1, sonuç, sizeof(sonuç) - 1);
    return 0;
}
