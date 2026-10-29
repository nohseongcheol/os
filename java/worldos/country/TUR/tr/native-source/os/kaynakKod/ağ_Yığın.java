// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statik_değer IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class ağ_Yığın {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int ağ_maskesi = 0xffffff00; /* ip.conf:NETMASK */
    static final int ağ_geçidi_değer = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] artış_kare = new int[1536], çıktı_kare = new int[1536];
    static int[] 접속번호들 = new int[4], GETİRİ_süre = new int[4], GETİRİ_ADRES = new int[4], GETİRİ_bağlantı_noktası_numarası = new int[4];
    static int[] GETİRİ_veri = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, tanımlayıcı_değer = 0, 폐기수 = 0;

    static int bilgi_16(int[] kare_Dizin, int konum) { return (kare_Dizin[konum] << 8) | kare_Dizin[konum + 1]; }
    static int bilgi_32(int[] kare_Dizin, int konum) { return (bilgi_16(kare_Dizin, konum) << 16) | bilgi_16(kare_Dizin, konum + 2); }
    static void 넣기16(int[] kare_Dizin, int konum, int değer) { kare_Dizin[konum] = (değer >>> 8) & 255; kare_Dizin[konum + 1] = değer & 255; }
    static void 넣기32(int[] kare_Dizin, int konum, int değer) { 넣기16(kare_Dizin, konum, değer >>> 16); 넣기16(kare_Dizin, konum + 2, değer); }
    static int SUM_değer(int[] kare_Dizin, int çalıştır, int süre_değer, int değer) {
        for (int Dizin = 0; Dizin < süre_değer; Dizin += 2)
            değer += (kare_Dizin[çalıştır + Dizin] << 8) | (Dizin + 1 < süre_değer ? kare_Dizin[çalıştır + Dizin + 1] : 0);
        while ((değer >>> 16) != 0) değer = (değer & 65535) + (değer >>> 16);
        return değer;
    }
    static int 가상머리합(int 출발, int 도착, int süre_değer) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + süre_değer;
    }

    static void TEMİZ_işlem() {
        for (int Dizin = 0; Dizin < 4; Dizin++) {
            접속번호들[Dizin] = 0; GETİRİ_süre[Dizin] = -1; GETİRİ_ADRES[Dizin] = 0; GETİRİ_bağlantı_noktası_numarası[Dizin] = 0;
        }
        for (int Dizin = 0; Dizin < 64; Dizin++) if (ağ_sürücü.almak(artış_kare) == 0) break;
    }
    static int Dizin(int sap_değer) { return sap_değer >= 3 && sap_değer < 7 && 접속번호들[sap_değer - 3] != 0 ? sap_değer - 3 : -1; }
    static int Aç(int bağlantı_noktası_numarası) {
        if (ağ_sürücü.입출력기준주소 == 0) return -19;
        if (bağlantı_noktası_numarası < 0 || bağlantı_noktası_numarası > 65535) return -22;
        if (bağlantı_noktası_numarası != 0) for (int Dizin = 0; Dizin < 4; Dizin++) if (접속번호들[Dizin] == bağlantı_noktası_numarası) return -98;
        for (int Dizin = 0; Dizin < 4; Dizin++) if (접속번호들[Dizin] == 0) {
            if (bağlantı_noktası_numarası == 0) {
                bağlantı_noktası_numarası = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int ön_kamera_değer = 0; ön_kamera_değer < 4; ön_kamera_değer++) if (접속번호들[ön_kamera_değer] == bağlantı_noktası_numarası) 겹침 = true;
                    if (겹침) bağlantı_noktası_numarası++;
                }
            }
            접속번호들[Dizin] = bağlantı_noktası_numarası; GETİRİ_süre[Dizin] = -1;
            return Dizin + 3;
        }
        return -24;
    }
    static int Kapat(int sap_değer) {
        int yuva_girdi = Dizin(sap_değer);
        if (yuva_girdi < 0) return -9;
        접속번호들[yuva_girdi] = 0; GETİRİ_süre[yuva_girdi] = -1;
        return 0;
    }
    static int eş_ADRES(int sap_değer) { int yuva_girdi = Dizin(sap_değer); return yuva_girdi < 0 ? -9 : GETİRİ_ADRES[yuva_girdi]; }
    static int eş_bağlantı_noktası_numarası(int sap_değer) { int yuva_girdi = Dizin(sap_değer); return yuva_girdi < 0 ? -9 : GETİRİ_bağlantı_noktası_numarası[yuva_girdi]; }

    static void 바깥머리(int Tip_değer, boolean yayın_değer) {
        for (int Dizin = 0; Dizin < 6; Dizin++) {
            çıktı_kare[Dizin] = yayın_değer ? 255 : 찾은장치[Dizin];
            çıktı_kare[6 + Dizin] = ağ_sürücü.cihaz_ADRES[Dizin];
        }
        넣기16(çıktı_kare, 12, Tip_değer);
    }
    static void istek_ADRES(int hedef_değer) {
        바깥머리(0x0806, true);
        넣기16(çıktı_kare, 14, 1); 넣기16(çıktı_kare, 16, 0x0800);
        çıktı_kare[18] = 6; çıktı_kare[19] = 4; 넣기16(çıktı_kare, 20, 1);
        for (int Dizin = 0; Dizin < 6; Dizin++) {
            çıktı_kare[22 + Dizin] = ağ_sürücü.cihaz_ADRES[Dizin]; çıktı_kare[32 + Dizin] = 0;
        }
        넣기32(çıktı_kare, 28, 내주소); 넣기32(çıktı_kare, 38, hedef_değer);
        ağ_sürücü.göndermek(çıktı_kare, 42);
    }
    static void işlem_ADRES(int süre_değer) {
        if (süre_değer < 42 || bilgi_16(artış_kare, 14) != 1 || bilgi_16(artış_kare, 16) != 0x0800
            || artış_kare[18] != 6 || artış_kare[19] != 4 || bilgi_32(artış_kare, 38) != 내주소) { 폐기수++; return; }
        int Tip_değer = bilgi_16(artış_kare, 20), eş_değer = bilgi_32(artış_kare, 28);
        if (Tip_değer == 2 && eş_değer == 찾을주소) {
            for (int Dizin = 0; Dizin < 6; Dizin++) {
                if (artış_kare[6 + Dizin] != artış_kare[22 + Dizin] || artış_kare[32 + Dizin] != ağ_sürücü.cihaz_ADRES[Dizin]) return;
            }
            for (int Dizin = 0; Dizin < 6; Dizin++) 찾은장치[Dizin] = artış_kare[22 + Dizin];
            찾은주소 = eş_değer;
        } else if (Tip_değer == 1) {
            바깥머리(0x0806, false);
            넣기16(çıktı_kare, 14, 1); 넣기16(çıktı_kare, 16, 0x0800);
            çıktı_kare[18] = 6; çıktı_kare[19] = 4; 넣기16(çıktı_kare, 20, 2);
            for (int Dizin = 0; Dizin < 6; Dizin++) {
                çıktı_kare[Dizin] = artış_kare[22 + Dizin]; çıktı_kare[32 + Dizin] = artış_kare[22 + Dizin];
                çıktı_kare[22 + Dizin] = ağ_sürücü.cihaz_ADRES[Dizin];
            }
            넣기32(çıktı_kare, 28, 내주소); 넣기32(çıktı_kare, 38, eş_değer);
            ağ_sürücü.göndermek(çıktı_kare, 42);
        }
    }

    static void işlem_kare(int süre_değer) {
        if (süre_değer < 14 || süre_değer > artış_kare.length) { 폐기수++; return; }
        boolean 자기 = true, yayın_değer = true;
        for (int Dizin = 0; Dizin < 6; Dizin++) {
            if (artış_kare[Dizin] != ağ_sürücü.cihaz_ADRES[Dizin]) 자기 = false;
            if (artış_kare[Dizin] != 255) yayın_değer = false;
        }
        if (!자기 && !yayın_değer) return;
        if (bilgi_16(artış_kare, 12) == 0x0806) { işlem_ADRES(süre_değer); return; }
        if (bilgi_16(artış_kare, 12) != 0x0800) return;
        if (süre_değer < 34 || (artış_kare[14] >>> 4) != 4) { 폐기수++; return; }
        int Başlık_süre = (artış_kare[14] & 15) * 4, toplam_süre = bilgi_16(artış_kare, 16);
        if (Başlık_süre < 20 || Başlık_süre > 60 || toplam_süre < Başlık_süre + 8 || toplam_süre > süre_değer - 14
            || (bilgi_16(artış_kare, 20) & 0x3fff) != 0 || artış_kare[23] != 17
            || bilgi_32(artış_kare, 30) != 내주소 || SUM_değer(artış_kare, 14, Başlık_süre, 0) != 65535) { 폐기수++; return; }
        int çalıştır = 14 + Başlık_süre, veri_süre = bilgi_16(artış_kare, çalıştır + 4);
        if (veri_süre < 8 || veri_süre != toplam_süre - Başlık_süre || veri_süre > 1032) { 폐기수++; return; }
        int 출발 = bilgi_32(artış_kare, 26);
        if (bilgi_16(artış_kare, çalıştır + 6) != 0 && SUM_değer(artış_kare, çalıştır, veri_süre, 가상머리합(출발, 내주소, veri_süre)) != 65535) {
            폐기수++; return;
        }
        int hedef_değer = bilgi_16(artış_kare, çalıştır + 2);
        for (int yuva_girdi = 0; yuva_girdi < 4; yuva_girdi++) if (접속번호들[yuva_girdi] != 0 && 접속번호들[yuva_girdi] == hedef_değer) {
            if (GETİRİ_süre[yuva_girdi] >= 0) { 폐기수++; return; }
            GETİRİ_süre[yuva_girdi] = veri_süre - 8; GETİRİ_ADRES[yuva_girdi] = 출발; GETİRİ_bağlantı_noktası_numarası[yuva_girdi] = bilgi_16(artış_kare, çalıştır);
            for (int Dizin = 0; Dizin < veri_süre - 8; Dizin++) GETİRİ_veri[yuva_girdi * 1024 + Dizin] = artış_kare[çalıştır + 8 + Dizin];
            return;
        }
    }

    static void doğrulamak() {
        for (int Dizin = 0; Dizin < 16; Dizin++) {
            int süre_değer = ağ_sürücü.almak(artış_kare);
            if (süre_değer == 0) return;
            işlem_kare(süre_değer);
        }
    }
    static int BUL_ADRES(int ADRES) {
        if (ADRES == 0 || ADRES == -1 || (ADRES >>> 28) >= 14 || (ADRES >>> 24) == 127 || ADRES == 내주소) return -101;
        int Sonraki_öğe = (ADRES & ağ_maskesi) == (내주소 & ağ_maskesi) ? ADRES : ağ_geçidi_değer;
        if (Sonraki_öğe == 찾은주소) return 0;
        찾을주소 = Sonraki_öğe;
        int çalıştır = cihaz_değer.밀리초(), Sonraki_istek = çalıştır;
        while (cihaz_değer.밀리초() - çalıştır < 1000) {
            if (cihaz_değer.밀리초() - Sonraki_istek >= 0) { istek_ADRES(Sonraki_öğe); Sonraki_istek += 300; }
            doğrulamak();
            if (찾은주소 == Sonraki_öğe) return 0;
            cihaz_değer.잠시양보();
        }
        return -110;
    }
    static int göndermek(int sap_değer, int ADRES, int bağlantı_noktası_numarası, int[] veri, int süre_değer) {
        int yuva_girdi = Dizin(sap_değer);
        if (yuva_girdi < 0) return -9;
        if (ağ_sürücü.입출력기준주소 == 0) return -19;
        if (bağlantı_noktası_numarası < 1 || bağlantı_noktası_numarası > 65535 || süre_değer < 0 || süre_değer > 1024) return -22;
        int sonuç = BUL_ADRES(ADRES);
        if (sonuç < 0) return sonuç;
        바깥머리(0x0800, false);
        çıktı_kare[14] = 0x45; çıktı_kare[15] = 0; 넣기16(çıktı_kare, 16, 28 + süre_değer);
        넣기16(çıktı_kare, 18, tanımlayıcı_değer++); 넣기16(çıktı_kare, 20, 0x4000);
        çıktı_kare[22] = 64; çıktı_kare[23] = 17; 넣기16(çıktı_kare, 24, 0);
        넣기32(çıktı_kare, 26, 내주소); 넣기32(çıktı_kare, 30, ADRES);
        넣기16(çıktı_kare, 24, ~SUM_değer(çıktı_kare, 14, 20, 0));
        넣기16(çıktı_kare, 34, 접속번호들[yuva_girdi]); 넣기16(çıktı_kare, 36, bağlantı_noktası_numarası);
        넣기16(çıktı_kare, 38, süre_değer + 8); 넣기16(çıktı_kare, 40, 0);
        for (int Dizin = 0; Dizin < süre_değer; Dizin++) çıktı_kare[42 + Dizin] = veri[Dizin] & 255;
        int sağlama_toplamı = (~SUM_değer(çıktı_kare, 34, süre_değer + 8, 가상머리합(내주소, ADRES, süre_değer + 8))) & 65535;
        넣기16(çıktı_kare, 40, sağlama_toplamı == 0 ? 65535 : sağlama_toplamı);
        sonuç = ağ_sürücü.göndermek(çıktı_kare, süre_değer + 42);
        return sonuç < 0 ? sonuç : süre_değer;
    }
    static int almak(int sap_değer, int[] veri, int kapasite_değer, int 제한) {
        int yuva_girdi = Dizin(sap_değer);
        if (yuva_girdi < 0) return -9;
        int çalıştır = cihaz_değer.밀리초();
        while (true) {
            doğrulamak();
            int süre_değer = GETİRİ_süre[yuva_girdi];
            if (süre_değer >= 0) {
                GETİRİ_süre[yuva_girdi] = -1;
                if (süre_değer > kapasite_değer) return -90;
                for (int Dizin = 0; Dizin < süre_değer; Dizin++) veri[Dizin] = GETİRİ_veri[yuva_girdi * 1024 + Dizin];
                return süre_değer;
            }
            if (제한 == 0) return -11;
            if (cihaz_değer.밀리초() - çalıştır >= 제한) return -110;
            cihaz_değer.잠시양보();
        }
    }
    static void Durum_değer() {
        SMS_Terminal.Yazma(ağ_sürücü.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminal.Yazma("TX: "); SMS_Terminal.수쓰기(ağ_sürücü.송신수);
        SMS_Terminal.Yazma(" RX: "); SMS_Terminal.수쓰기(ağ_sürücü.almak_BAĞ_DEĞ_SAY);
        SMS_Terminal.Yazma(" DROP: "); SMS_Terminal.수쓰기(폐기수);
        SMS_Terminal.Yazma("\n");
    }
}
