// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** çekirdek_değer 안의 연결형 bayt_değer akış_değer. Ethernet/TCP 패킷 스택이 아닌 루프백 socket katman_değer_e65604ef. */
public final class akış_ağ {
    static int[] Durum_değer = new int[16], taşımak_değer = new int[16], 짝 = new int[16], eş_taşımak = new int[16], bekle_değer = new int[16], bilgi_teknolojisi_sınır = new int[16];
    static int[] ön_kamera_değer = new int[16], 수 = new int[16], veri = new int[16 * 1024];
    static int Sonraki_öğe = 50000;
    static int doğrulamak(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Durum_değer[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int bağlantı_noktası_numarası) { for (int Loop_Dizin = 0; Loop_Dizin < 16; Loop_Dizin++) if (Durum_değer[Loop_Dizin] != 0 && bilgi_teknolojisi_sınır[Loop_Dizin] != 0 && taşımak_değer[Loop_Dizin] == bağlantı_noktası_numarası) return true; return false; }
    public static int açmak_girdi() {
        for (int Loop_Dizin = 0; Loop_Dizin < 16; Loop_Dizin++) if (Durum_değer[Loop_Dizin] == 0) { Durum_değer[Loop_Dizin] = 1; eş_taşımak[Loop_Dizin] = taşımak_değer[Loop_Dizin] = ön_kamera_değer[Loop_Dizin] = 수[Loop_Dizin] = bekle_değer[Loop_Dizin] = bilgi_teknolojisi_sınır[Loop_Dizin] = 0; 짝[Loop_Dizin] = -1; return Loop_Dizin + 40; }
        return -24;
    }
    public static int BIND_uç_nokta(int 열린파일번호, int yuva_ADRES, int bağlantı_noktası_numarası) {
        int Loop_Dizin = doğrulamak(열린파일번호); if (Loop_Dizin < 0) return -9;
        if (yuva_ADRES != 0 && yuva_ADRES != 0x7f000001) return -99;
        if (Durum_değer[Loop_Dizin] != 1 || bağlantı_noktası_numarası < 0 || bağlantı_noktası_numarası > 65535) return -22;
        if (bağlantı_noktası_numarası == 0) { do { bağlantı_noktası_numarası = Sonraki_öğe++; if (Sonraki_öğe > 65535) Sonraki_öğe = 50000; } while (사용중(bağlantı_noktası_numarası)); }
        if (사용중(bağlantı_noktası_numarası)) return -98; taşımak_değer[Loop_Dizin] = bağlantı_noktası_numarası; bilgi_teknolojisi_sınır[Loop_Dizin] = 1; Durum_değer[Loop_Dizin] = 2; return 0;
    }
    public static int dinlemek_uç_nokta(int 열린파일번호, int Kapsam) { int Loop_Dizin = doğrulamak(열린파일번호); if (Loop_Dizin < 0) return -9; if (Durum_değer[Loop_Dizin] != 2 || Kapsam < 1) return -22; Durum_değer[Loop_Dizin] = 3; return 0; }
    public static int Bağlan(int 열린파일번호, int yuva_ADRES, int bağlantı_noktası_numarası) {
        int Loop_Dizin = doğrulamak(열린파일번호); if (Loop_Dizin < 0) return -9; if (yuva_ADRES != 0x7f000001) return -101;
        if (bağlantı_noktası_numarası < 1 || bağlantı_noktası_numarası > 65535 || Durum_değer[Loop_Dizin] > 2) return -22;
        int almak_sayfa = -1; for (int iç_konum = 0; iç_konum < 16; iç_konum++) if (Durum_değer[iç_konum] == 3 && taşımak_değer[iç_konum] == bağlantı_noktası_numarası) almak_sayfa = iç_konum;
        if (almak_sayfa < 0) return -111;
        int 대기여부 = 0; for (int iç_konum = 0; iç_konum < 16; iç_konum++) if (bekle_değer[iç_konum] == almak_sayfa + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (Durum_değer[Loop_Dizin] == 1) { int 처리값 = BIND_uç_nokta(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int Diğer = açmak_girdi(); if (Diğer < 0) return Diğer; Diğer -= 40;
        Durum_değer[Loop_Dizin] = Durum_değer[Diğer] = 4; 짝[Loop_Dizin] = Diğer; 짝[Diğer] = Loop_Dizin; taşımak_değer[Diğer] = bağlantı_noktası_numarası; eş_taşımak[Loop_Dizin] = bağlantı_noktası_numarası; eş_taşımak[Diğer] = taşımak_değer[Loop_Dizin]; bekle_değer[Diğer] = almak_sayfa + 1; return 0;
    }
    public static int kabul_etmek_cxn(int 열린파일번호) { int Loop_Dizin = doğrulamak(열린파일번호); if (Loop_Dizin < 0) return -9; if (Durum_değer[Loop_Dizin] != 3) return -22; for (int iç_konum = 0; iç_konum < 16; iç_konum++) if (Durum_değer[iç_konum] != 0 && bekle_değer[iç_konum] == Loop_Dizin + 1) { bekle_değer[iç_konum] = 0; return iç_konum + 40; } return -11; }
    public static int Yazma(int 열린파일번호, int girdi_BAĞ_DEĞ_SAY) {
        int Loop_Dizin = doğrulamak(열린파일번호); if (Loop_Dizin < 0) return -9; if (Durum_değer[Loop_Dizin] != 4) return -107;
        if (girdi_BAĞ_DEĞ_SAY < 0 || girdi_BAĞ_DEĞ_SAY > 512) return -22; if (girdi_BAĞ_DEĞ_SAY == 0) return 0;
        int iç_konum = 짝[Loop_Dizin]; if (iç_konum < 0) return -32; int toplam_BAĞ_DEĞ_SAY = 1024 - 수[iç_konum]; if (toplam_BAĞ_DEĞ_SAY == 0) return -11; if (toplam_BAĞ_DEĞ_SAY > girdi_BAĞ_DEĞ_SAY) toplam_BAĞ_DEĞ_SAY = girdi_BAĞ_DEĞ_SAY;
        for (int Karşılaştırma_konum = 0; Karşılaştırma_konum < toplam_BAĞ_DEĞ_SAY; Karşılaştırma_konum++) veri[iç_konum * 1024 + (ön_kamera_değer[iç_konum] + 수[iç_konum] + Karşılaştırma_konum) % 1024] = geri_döngü_ağ.İleri_değer[Karşılaştırma_konum]; 수[iç_konum] += toplam_BAĞ_DEĞ_SAY; return toplam_BAĞ_DEĞ_SAY;
    }
    public static int Okuma(int 열린파일번호, int girdi_BAĞ_DEĞ_SAY) {
        int Loop_Dizin = doğrulamak(열린파일번호); if (Loop_Dizin < 0) return -9; if (Durum_değer[Loop_Dizin] != 4) return -107; if (girdi_BAĞ_DEĞ_SAY < 0 || girdi_BAĞ_DEĞ_SAY > 512) return -22;
        if (girdi_BAĞ_DEĞ_SAY == 0) return 0; if (수[Loop_Dizin] == 0) return 짝[Loop_Dizin] < 0 ? 0 : -11; if (girdi_BAĞ_DEĞ_SAY > 수[Loop_Dizin]) girdi_BAĞ_DEĞ_SAY = 수[Loop_Dizin];
        for (int Karşılaştırma_konum = 0; Karşılaştırma_konum < girdi_BAĞ_DEĞ_SAY; Karşılaştırma_konum++) geri_döngü_ağ.İleri_değer[Karşılaştırma_konum] = veri[Loop_Dizin * 1024 + (ön_kamera_değer[Loop_Dizin] + Karşılaştırma_konum) % 1024]; ön_kamera_değer[Loop_Dizin] = (ön_kamera_değer[Loop_Dizin] + girdi_BAĞ_DEĞ_SAY) % 1024; 수[Loop_Dizin] -= girdi_BAĞ_DEĞ_SAY; return girdi_BAĞ_DEĞ_SAY;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_Dizin = doğrulamak(열린파일번호); return Loop_Dizin < 0 ? -9 : taşımak_değer[Loop_Dizin]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_Dizin = doğrulamak(열린파일번호); return Loop_Dizin < 0 ? -9 : eş_taşımak[Loop_Dizin]; }
    public static int Kapat(int 열린파일번호) {
        int Loop_Dizin = doğrulamak(열린파일번호); if (Loop_Dizin < 0) return -9;
        if (Durum_değer[Loop_Dizin] == 3) for (int iç_konum = 0; iç_konum < 16; iç_konum++) if (bekle_değer[iç_konum] == Loop_Dizin + 1) { if (짝[iç_konum] >= 0) 짝[짝[iç_konum]] = -1; Durum_değer[iç_konum] = bekle_değer[iç_konum] = bilgi_teknolojisi_sınır[iç_konum] = 0; }
        if (짝[Loop_Dizin] >= 0) 짝[짝[Loop_Dizin]] = -1; Durum_değer[Loop_Dizin] = bilgi_teknolojisi_sınır[Loop_Dizin] = 수[Loop_Dizin] = bekle_değer[Loop_Dizin] = 0; return 0;
    }
}
