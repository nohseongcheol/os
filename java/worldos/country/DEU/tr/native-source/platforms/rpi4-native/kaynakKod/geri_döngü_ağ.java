// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 katman_değer_e65604ef: 단일 çekirdek_değer 안의 IPv4/UDP 루프백 devir_değer.
 * dış_değer IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * Bitiş_puan 8개, 끝점당 veri_birimi 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class geri_döngü_ağ {
    static int[] kullanmak_değer = new int[8];
    static int[] taşımak_değer = new int[8];
    static int[] ADRES = new int[8];
    static int[] ön_kamera_değer = new int[8];
    static int[] öğe_BAĞ_DEĞ_SAY = new int[8];
    static int[] GETİRİ_taşımak = new int[8];
    static int[] süre_değer = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] veri = new int[32 * 512];
    static int[] İleri_değer = new int[512];
    static int Sonraki_uç_nokta = 49152;
    static int doğrulamak(int Dizin) { return Dizin >= 32 && Dizin < 40 && kullanmak_değer[Dizin - 32] != 0 ? Dizin - 32 : -1; }
    static boolean 겹침(int Dizin) {
        for (int yuva_girdi = 0; yuva_girdi < 8; yuva_girdi++) if (kullanmak_değer[yuva_girdi] != 0 && taşımak_değer[yuva_girdi] == Dizin) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int aday = Sonraki_uç_nokta++;
            if (Sonraki_uç_nokta > 65535) Sonraki_uç_nokta = 49152;
            if (!겹침(aday)) return aday;
        }
        return -98;
    }
    public static int açmak_girdi(int bölge_değer, int Tip_değer, int sözleşme_değeri) {
        if (bölge_değer != 2) return -97;
        if (Tip_değer != 2 || (sözleşme_değeri != 0 && sözleşme_değeri != 17)) return -93;
        for (int yuva_girdi = 0; yuva_girdi < 8; yuva_girdi++) if (kullanmak_değer[yuva_girdi] == 0) {
            kullanmak_değer[yuva_girdi] = 1; taşımak_değer[yuva_girdi] = 0; ADRES[yuva_girdi] = 0; ön_kamera_değer[yuva_girdi] = 0; öğe_BAĞ_DEĞ_SAY[yuva_girdi] = 0; GETİRİ_taşımak[yuva_girdi] = 0;
            return yuva_girdi + 32;
        }
        return -24;
    }
    public static int BIND_uç_nokta(int Dizin, int ağ_kimliği, int uç_nokta_bağlantı_noktası_numarası) {
        int yuva_girdi = doğrulamak(Dizin);
        if (yuva_girdi < 0) return -9;
        if (ağ_kimliği != 0 && ağ_kimliği != 0x7f000001) return -99;
        if (taşımak_değer[yuva_girdi] != 0 || uç_nokta_bağlantı_noktası_numarası < 0 || uç_nokta_bağlantı_noktası_numarası > 65535) return -22;
        if (uç_nokta_bağlantı_noktası_numarası == 0) uç_nokta_bağlantı_noktası_numarası = 임시창구();
        if (uç_nokta_bağlantı_noktası_numarası < 0) return uç_nokta_bağlantı_noktası_numarası;
        if (겹침(uç_nokta_bağlantı_noktası_numarası)) return -98;
        taşımak_değer[yuva_girdi] = uç_nokta_bağlantı_noktası_numarası; ADRES[yuva_girdi] = ağ_kimliği; return 0;
    }
    public static int 자료넣기(int Dizin, int değer) {
        if (Dizin < 0 || Dizin >= 512) return -22;
        İleri_değer[Dizin] = değer & 255; return 0;
    }
    public static int 자료읽기(int Dizin) { return Dizin >= 0 && Dizin < 512 ? İleri_değer[Dizin] : -22; }
    public static int göndermek(int Dizin, int ağ_kimliği, int uç_nokta_bağlantı_noktası_numarası, int Boyut) {
        int yuva_girdi = doğrulamak(Dizin);
        if (yuva_girdi < 0) return -9;
        if (ağ_kimliği != 0x7f000001) return -101;
        if (uç_nokta_bağlantı_noktası_numarası < 1 || uç_nokta_bağlantı_noktası_numarası > 65535) return -22;
        if (Boyut < 0 || Boyut > 512) return -90;
        if (taşımak_değer[yuva_girdi] == 0) {
            int sonuç = BIND_uç_nokta(Dizin, 0x7f000001, 0);
            if (sonuç < 0) return sonuç;
        }
        int hedef_değer = -1;
        for (int aday = 0; aday < 8; aday++) if (kullanmak_değer[aday] != 0 && taşımak_değer[aday] == uç_nokta_bağlantı_noktası_numarası) hedef_değer = aday;
        if (hedef_değer < 0) return -111;
        if (öğe_BAĞ_DEĞ_SAY[hedef_değer] == 4) return -11;
        int konum_dizini = hedef_değer * 4 + (ön_kamera_değer[hedef_değer] + öğe_BAĞ_DEĞ_SAY[hedef_değer]) % 4;
        for (int bayt_değer = 0; bayt_değer < Boyut; bayt_değer++) veri[konum_dizini * 512 + bayt_değer] = İleri_değer[bayt_değer];
        süre_değer[konum_dizini] = Boyut; 보낸창구[konum_dizini] = taşımak_değer[yuva_girdi]; öğe_BAĞ_DEĞ_SAY[hedef_değer]++;
        return Boyut;
    }
    public static int almak(int Dizin, int kapasite_değer) {
        int yuva_girdi = doğrulamak(Dizin);
        if (yuva_girdi < 0) return -9;
        if (kapasite_değer < 0 || kapasite_değer > 512) return -22;
        if (öğe_BAĞ_DEĞ_SAY[yuva_girdi] == 0) return -11;
        int konum_dizini = yuva_girdi * 4 + ön_kamera_değer[yuva_girdi];
        int Boyut = süre_değer[konum_dizini] < kapasite_değer ? süre_değer[konum_dizini] : kapasite_değer;
        for (int bayt_değer = 0; bayt_değer < Boyut; bayt_değer++) İleri_değer[bayt_değer] = veri[konum_dizini * 512 + bayt_değer];
        GETİRİ_taşımak[yuva_girdi] = 보낸창구[konum_dizini]; ön_kamera_değer[yuva_girdi] = (ön_kamera_değer[yuva_girdi] + 1) % 4; öğe_BAĞ_DEĞ_SAY[yuva_girdi]--;
        return Boyut;
    }
    public static int 창구읽기(int Dizin) { int yuva_girdi = doğrulamak(Dizin); return yuva_girdi < 0 ? -9 : taşımak_değer[yuva_girdi]; }
    public static int 주소읽기(int Dizin) { int yuva_girdi = doğrulamak(Dizin); return yuva_girdi < 0 ? -9 : ADRES[yuva_girdi]; }
    public static int gönderen_uç_nokta(int Dizin) { int yuva_girdi = doğrulamak(Dizin); return yuva_girdi < 0 ? -9 : GETİRİ_taşımak[yuva_girdi]; }
    public static int Kapat(int Dizin) {
        int yuva_girdi = doğrulamak(Dizin); if (yuva_girdi < 0) return -9;
        kullanmak_değer[yuva_girdi] = 0; öğe_BAĞ_DEĞ_SAY[yuva_girdi] = 0; taşımak_değer[yuva_girdi] = 0; return 0;
    }
}
