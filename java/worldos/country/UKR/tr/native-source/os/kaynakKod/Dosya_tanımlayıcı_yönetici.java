// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 kullanıcı_alanı 과정의 파일서술자와 열린 dosya 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class Dosya_tanımlayıcı_yönetici {
    static final int 서술자한도 = 32;
    static final int R_W_bayrak = 2, açmak_girdi = 64, 독점생성 = 128, takas_içindekiler = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] açık_sap = new int[서술자한도], küme_tanımlayıcı = new int[서술자한도];
    static int[] Tip_değer = new int[서술자한도], hedef = new int[서술자한도];
    static int[] Dosya_konum = new int[서술자한도], açık_Ayarlar = new int[서술자한도], Başvuru_BAĞ_DEĞ_SAY = new int[서술자한도];
    static int[] ağ_sap = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] yol_ad = new int[64], devir_veri = new int[1024];

    static int BUL_tanımlayıcı(int Dosya_tanımlayıcı) {
        if (Dosya_tanımlayıcı < 0 || Dosya_tanımlayıcı >= 서술자한도) return -9;
        return açık_sap[Dosya_tanımlayıcı] - 1;
    }
    static int boş_tanımlayıcı(int çalıştır) {
        for (int Dizin = çalıştır; Dizin < 서술자한도; Dizin++) if (açık_sap[Dizin] == 0) return Dizin;
        return -24;
    }
    static int boş_sap() {
        for (int Dizin = 0; Dizin < 서술자한도; Dizin++) if (Başvuru_BAĞ_DEĞ_SAY[Dizin] == 0) return Dizin;
        return -24;
    }
    static int Bağlan(int tanımlayıcı_girdi, int tanımlayıcı_değer_a78cee47, int Dosya_Tip, int Dosya_hedef, int Ayarlar) {
        açık_sap[tanımlayıcı_girdi] = tanımlayıcı_değer_a78cee47 + 1; küme_tanımlayıcı[tanımlayıcı_girdi] = (Ayarlar & 실행시닫기) != 0 ? 1 : 0;
        Tip_değer[tanımlayıcı_değer_a78cee47] = Dosya_Tip; hedef[tanımlayıcı_değer_a78cee47] = Dosya_hedef; Başvuru_BAĞ_DEĞ_SAY[tanımlayıcı_değer_a78cee47] = 1;
        açık_Ayarlar[tanımlayıcı_değer_a78cee47] = Ayarlar & (3 | 이어쓰기 | 기다리지않기); Dosya_konum[tanımlayıcı_değer_a78cee47] = 0;
        ağ_sap[tanımlayıcı_değer_a78cee47] = 0; 수신대기밀리초[tanımlayıcı_değer_a78cee47] = 0;
        return tanımlayıcı_girdi;
    }
    static void Start_işlem() {
        TEMİZ_işlem();
        for (int Dizin = 0; Dizin < 3; Dizin++) Bağlan(Dizin, Dizin, 1, Dizin, Dizin == 0 ? 0 : 1);
    }
    static void TEMİZ_işlem() {
        for (int Dizin = 0; Dizin < 서술자한도; Dizin++) if (açık_sap[Dizin] != 0) Kapat_Dosya(Dizin);
    }
    static int Kapat_Dosya(int tanımlayıcı_girdi) {
        int tanımlayıcı_değer_a78cee47 = BUL_tanımlayıcı(tanımlayıcı_girdi);
        if (tanımlayıcı_değer_a78cee47 < 0) return -9;
        açık_sap[tanımlayıcı_girdi] = 0; küme_tanımlayıcı[tanımlayıcı_girdi] = 0;
        Başvuru_BAĞ_DEĞ_SAY[tanımlayıcı_değer_a78cee47]--;
        if (Başvuru_BAĞ_DEĞ_SAY[tanımlayıcı_değer_a78cee47] == 0) {
            if (Tip_değer[tanımlayıcı_değer_a78cee47] == 2) Bellek_dosya_sistemi.açık_BAĞ_DEĞ_SAY[hedef[tanımlayıcı_değer_a78cee47]]--;
            if (Tip_değer[tanımlayıcı_değer_a78cee47] == 3 && ağ_sap[tanımlayıcı_değer_a78cee47] != 0) ağ_Yığın.Kapat(ağ_sap[tanımlayıcı_değer_a78cee47]);
            Tip_değer[tanımlayıcı_değer_a78cee47] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 bayt_değer 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int ADRES) {
        if (!yürütme_yönetici.klip(ADRES, 1)) return -14;
        int konum = cihaz_değer.기억읽기(ADRES) == '/' ? 1 : 0;
        for (int süre_değer = 0; süre_değer < 64; süre_değer++) {
            if (!yürütme_yönetici.klip(ADRES + konum + süre_değer, 1)) return -14;
            int değer = cihaz_değer.기억읽기(ADRES + konum + süre_değer);
            yol_ad[süre_değer] = değer;
            if (değer == 0) return süre_değer == 0 ? -2 : (Bellek_dosya_sistemi.çek_ad(yol_ad, süre_değer) ? süre_değer : -22);
            if (değer == '/') return -20;
        }
        return -36;
    }
    static int açık_Dosya(int ad_ADRES, int Ayarlar, int izin_verme_izin) {
        int süre_değer = 경로읽기(ad_ADRES);
        if (süre_değer < 0) return süre_değer;
        if ((Ayarlar & ~(3 | açmak_girdi | 독점생성 | takas_içindekiler | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Ayarlar & 3) == 3 || ((Ayarlar & takas_içindekiler) != 0 && (Ayarlar & 3) == 0)) return -22;
        int dosya = Bellek_dosya_sistemi.BUL_girdi(yol_ad, süre_değer);
        if (dosya >= 0 && (Ayarlar & (açmak_girdi | 독점생성)) == (açmak_girdi | 독점생성)) return -17;
        if (dosya == -2 && (Ayarlar & açmak_girdi) == 0) return -2;
        int tanımlayıcı_girdi = boş_tanımlayıcı(0), tanımlayıcı_değer_a78cee47 = boş_sap();
        if (tanımlayıcı_girdi < 0 || tanımlayıcı_değer_a78cee47 < 0) return -24;
        if (dosya == -2) {
            int sonuç = Bellek_dosya_sistemi.depo_değer(yol_ad, süre_değer, yol_ad, 0);
            if (sonuç < 0) return sonuç;
            dosya = Bellek_dosya_sistemi.BUL_girdi(yol_ad, süre_değer);
            Bellek_dosya_sistemi.허가들[dosya] = izin_verme_izin & 511;
        }
        if (dosya < 0) return dosya;
        if ((Ayarlar & takas_içindekiler) != 0) Bellek_dosya_sistemi.boyutlandırmak_Liste[dosya] = 0;
        Bellek_dosya_sistemi.açık_BAĞ_DEĞ_SAY[dosya]++;
        return Bağlan(tanımlayıcı_girdi, tanımlayıcı_değer_a78cee47, 2, dosya, Ayarlar);
    }
    static int 파일읽기(int tanımlayıcı_girdi, int veri_ADRES, int süre_değer) {
        int tanımlayıcı_değer_a78cee47 = BUL_tanımlayıcı(tanımlayıcı_girdi);
        if (tanımlayıcı_değer_a78cee47 < 0 || (açık_Ayarlar[tanımlayıcı_değer_a78cee47] & 3) == 1) return -9;
        if (süre_değer < 0) return -22;
        if (süre_değer == 0) return 0;
        if (!yürütme_yönetici.klip(veri_ADRES, süre_değer)) return -14;
        if (Tip_değer[tanımlayıcı_değer_a78cee47] == 3) return almak_veri_birimi_veri(tanımlayıcı_girdi, veri_ADRES, süre_değer, 0, 0);
        if (Tip_değer[tanımlayıcı_değer_a78cee47] == 1) {
            int GETİRİ_BAĞ_DEĞ_SAY = 0;
            while (GETİRİ_BAĞ_DEĞ_SAY < süre_değer) {
                int değer = SMS_Terminal.직렬읽기();
                if (değer < 0) değer = klavye.Okuma();
                if (değer < 0) {
                    if (GETİRİ_BAĞ_DEĞ_SAY > 0) return GETİRİ_BAĞ_DEĞ_SAY;
                    if ((açık_Ayarlar[tanımlayıcı_değer_a78cee47] & 기다리지않기) != 0) return -11;
                    if (cihaz_değer.사용자남은밀리초() <= 10) return -11;
                    ağ_Yığın.doğrulamak(); cihaz_değer.잠시양보();
                } else {
                    cihaz_değer.yazma_Bellek(veri_ADRES + GETİRİ_BAĞ_DEĞ_SAY, değer); GETİRİ_BAĞ_DEĞ_SAY++;
                }
            }
            return GETİRİ_BAĞ_DEĞ_SAY;
        }
        int dosya = hedef[tanımlayıcı_değer_a78cee47], konum = Dosya_konum[tanımlayıcı_değer_a78cee47];
        if (konum >= Bellek_dosya_sistemi.boyutlandırmak_Liste[dosya]) return 0;
        if (süre_değer > Bellek_dosya_sistemi.boyutlandırmak_Liste[dosya] - konum) süre_değer = Bellek_dosya_sistemi.boyutlandırmak_Liste[dosya] - konum;
        int 원본주소 = cihaz_değer.Dosya_Bellek() + dosya * Bellek_dosya_sistemi.최대크기 + konum;
        for (int Dizin = 0; Dizin < süre_değer; Dizin++) cihaz_değer.yazma_Bellek(veri_ADRES + Dizin, cihaz_değer.기억읽기(원본주소 + Dizin));
        Dosya_konum[tanımlayıcı_değer_a78cee47] += süre_değer;
        return süre_değer;
    }
    static int yazma_Dosya(int tanımlayıcı_girdi, int veri_ADRES, int süre_değer) {
        int tanımlayıcı_değer_a78cee47 = BUL_tanımlayıcı(tanımlayıcı_girdi);
        if (tanımlayıcı_değer_a78cee47 < 0 || (açık_Ayarlar[tanımlayıcı_değer_a78cee47] & 3) == 0) return -9;
        if (süre_değer < 0) return -22;
        if (süre_değer == 0) return 0;
        if (!yürütme_yönetici.klip(veri_ADRES, süre_değer)) return -14;
        if (Tip_değer[tanımlayıcı_değer_a78cee47] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 hedef_değer 주소가 필요하다.
        if (Tip_değer[tanımlayıcı_değer_a78cee47] == 1) {
            if (süre_değer > 16384) süre_değer = 16384;
            for (int Dizin = 0; Dizin < süre_değer; Dizin++) {
                int değer = cihaz_değer.기억읽기(veri_ADRES + Dizin);
                SMS_Terminal.직렬바이트(değer); SMS_Terminal.화면문자(değer);
            }
            return süre_değer;
        }
        int dosya = hedef[tanımlayıcı_değer_a78cee47], Boyut = Bellek_dosya_sistemi.boyutlandırmak_Liste[dosya];
        int konum = (açık_Ayarlar[tanımlayıcı_değer_a78cee47] & 이어쓰기) != 0 ? Boyut : Dosya_konum[tanımlayıcı_değer_a78cee47];
        if (konum >= Bellek_dosya_sistemi.최대크기) return -27;
        if (süre_değer > Bellek_dosya_sistemi.최대크기 - konum) süre_değer = Bellek_dosya_sistemi.최대크기 - konum;
        int hedef_ADRES_08bbd577 = cihaz_değer.Dosya_Bellek() + dosya * Bellek_dosya_sistemi.최대크기;
        for (int Dizin = Boyut; Dizin < konum; Dizin++) cihaz_değer.yazma_Bellek(hedef_ADRES_08bbd577 + Dizin, 0);
        for (int Dizin = 0; Dizin < süre_değer; Dizin++) cihaz_değer.yazma_Bellek(hedef_ADRES_08bbd577 + konum + Dizin, cihaz_değer.기억읽기(veri_ADRES + Dizin));
        Dosya_konum[tanımlayıcı_değer_a78cee47] = konum + süre_değer;
        if (konum + süre_değer > Boyut) Bellek_dosya_sistemi.boyutlandırmak_Liste[dosya] = konum + süre_değer;
        return süre_değer;
    }
    static int arama_Dosya(int tanımlayıcı_girdi, int Ofset_değer, int işlem_kök) {
        int tanımlayıcı_değer_a78cee47 = BUL_tanımlayıcı(tanımlayıcı_girdi);
        if (tanımlayıcı_değer_a78cee47 < 0) return -9;
        if (Tip_değer[tanımlayıcı_değer_a78cee47] != 2) return -29;
        if (işlem_kök < 0 || işlem_kök > 2) return -22;
        int Arka_Plan_değer = işlem_kök == 0 ? 0 : (işlem_kök == 1 ? Dosya_konum[tanımlayıcı_değer_a78cee47] : Bellek_dosya_sistemi.boyutlandırmak_Liste[hedef[tanımlayıcı_değer_a78cee47]]);
        if (Ofset_değer > 0 && Arka_Plan_değer > 2147483647 - Ofset_değer) return -75;
        if (Ofset_değer < 0 && Ofset_değer < -Arka_Plan_değer) return -22;
        Dosya_konum[tanımlayıcı_değer_a78cee47] = Arka_Plan_değer + Ofset_değer;
        return Dosya_konum[tanımlayıcı_değer_a78cee47];
    }
    static int kopya_tanımlayıcı(int tanımlayıcı_girdi, int 새서술자, boolean Ata_değer, int Ayarlar) {
        int tanımlayıcı_değer_a78cee47 = BUL_tanımlayıcı(tanımlayıcı_girdi);
        if (tanımlayıcı_değer_a78cee47 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return Ata_değer ? -9 : -22;
        if (Ata_değer && tanımlayıcı_girdi == 새서술자) return 새서술자;
        if (Ata_değer) { if (açık_sap[새서술자] != 0) Kapat_Dosya(새서술자); }
        else { 새서술자 = boş_tanımlayıcı(새서술자); if (새서술자 < 0) return 새서술자; }
        açık_sap[새서술자] = tanımlayıcı_değer_a78cee47 + 1; küme_tanımlayıcı[새서술자] = Ayarlar; Başvuru_BAĞ_DEĞ_SAY[tanımlayıcı_değer_a78cee47]++;
        return 새서술자;
    }
    static int kaldırmak_Dosya_girdi_ad(int ad_ADRES) {
        int süre_değer = 경로읽기(ad_ADRES);
        if (süre_değer < 0) return süre_değer;
        int dosya = Bellek_dosya_sistemi.BUL_girdi(yol_ad, süre_değer);
        if (dosya < 0) return dosya;
        Bellek_dosya_sistemi.이름들[dosya * 64] = 0;
        return 0;
    }
    static int küme_Dosya_süre(int tanımlayıcı_girdi, int süre_değer) {
        int tanımlayıcı_değer_a78cee47 = BUL_tanımlayıcı(tanımlayıcı_girdi);
        if (tanımlayıcı_değer_a78cee47 < 0) return -9;
        if (Tip_değer[tanımlayıcı_değer_a78cee47] != 2 || (açık_Ayarlar[tanımlayıcı_değer_a78cee47] & 3) == 0 || süre_değer < 0) return -22;
        if (süre_değer > Bellek_dosya_sistemi.최대크기) return -27;
        int dosya = hedef[tanımlayıcı_değer_a78cee47], ADRES = cihaz_değer.Dosya_Bellek() + dosya * Bellek_dosya_sistemi.최대크기;
        for (int Dizin = Bellek_dosya_sistemi.boyutlandırmak_Liste[dosya]; Dizin < süre_değer; Dizin++) cihaz_değer.yazma_Bellek(ADRES + Dizin, 0);
        Bellek_dosya_sistemi.boyutlandırmak_Liste[dosya] = süre_değer;
        return 0;
    }
    static int 파일상태읽기(int tanımlayıcı_girdi, int ADRES) {
        int tanımlayıcı_değer_a78cee47 = BUL_tanımlayıcı(tanımlayıcı_girdi);
        if (tanımlayıcı_değer_a78cee47 < 0) return -9;
        if (!yürütme_yönetici.klip(ADRES, 48)) return -14;
        for (int Dizin = 0; Dizin < 12; Dizin++) yürütme_yönetici.수쓰기(ADRES + Dizin * 4, 0);
        int dosya = hedef[tanımlayıcı_değer_a78cee47], Boyut = Tip_değer[tanımlayıcı_değer_a78cee47] == 2 ? Bellek_dosya_sistemi.boyutlandırmak_Liste[dosya] : 0;
        int izin_verme_izin = Tip_değer[tanımlayıcı_değer_a78cee47] == 2 ? Bellek_dosya_sistemi.허가들[dosya] : 438;
        yürütme_yönetici.수쓰기(ADRES, 1);
        yürütme_yönetici.수쓰기(ADRES + 4, Tip_değer[tanımlayıcı_değer_a78cee47] == 2 ? dosya + 1 : 100 + tanımlayıcı_değer_a78cee47);
        yürütme_yönetici.수쓰기(ADRES + 8, (Tip_değer[tanımlayıcı_değer_a78cee47] == 2 ? 32768 : (Tip_değer[tanımlayıcı_değer_a78cee47] == 1 ? 8192 : 49152)) | izin_verme_izin);
        yürütme_yönetici.수쓰기(ADRES + 12, Tip_değer[tanımlayıcı_değer_a78cee47] == 2 && Bellek_dosya_sistemi.이름들[dosya * 64] == 0 ? 0 : 1);
        yürütme_yönetici.수쓰기(ADRES + 28, Boyut); yürütme_yönetici.수쓰기(ADRES + 32, 512);
        yürütme_yönetici.수쓰기(ADRES + 36, (Boyut + 511) / 512);
        return 0;
    }
    static int denetim_tanımlayıcı(int tanımlayıcı_girdi, int komut, int değer) {
        int tanımlayıcı_değer_a78cee47 = BUL_tanımlayıcı(tanımlayıcı_girdi);
        if (tanımlayıcı_değer_a78cee47 < 0) return -9;
        if (komut == 0 || komut == 1030) return kopya_tanımlayıcı(tanımlayıcı_girdi, değer, false, komut == 1030 ? 1 : 0);
        if (komut == 1) return küme_tanımlayıcı[tanımlayıcı_girdi];
        if (komut == 2) { if ((değer & ~1) != 0) return -22; küme_tanımlayıcı[tanımlayıcı_girdi] = değer; return 0; }
        if (komut == 3) return açık_Ayarlar[tanımlayıcı_değer_a78cee47];
        if (komut == 4) {
            if ((değer & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            açık_Ayarlar[tanımlayıcı_değer_a78cee47] = (açık_Ayarlar[tanımlayıcı_değer_a78cee47] & 3) | (değer & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int açmak_uç_nokta(int 주소체계, int ağ_Tip, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (ağ_Tip != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int tanımlayıcı_girdi = boş_tanımlayıcı(0), tanımlayıcı_değer_a78cee47 = boş_sap();
        if (tanımlayıcı_girdi < 0 || tanımlayıcı_değer_a78cee47 < 0) return -24;
        return Bağlan(tanımlayıcı_girdi, tanımlayıcı_değer_a78cee47, 3, 0, R_W_bayrak);
    }
    static int uç_nokta_tanımlayıcı(int tanımlayıcı_girdi) {
        int tanımlayıcı_değer_a78cee47 = BUL_tanımlayıcı(tanımlayıcı_girdi);
        if (tanımlayıcı_değer_a78cee47 < 0) return -9;
        return Tip_değer[tanımlayıcı_değer_a78cee47] == 3 ? tanımlayıcı_değer_a78cee47 : -88;
    }
    static int ADRES_32(int ADRES) {
        return cihaz_değer.기억읽기(ADRES) << 24 | cihaz_değer.기억읽기(ADRES + 1) << 16
            | cihaz_değer.기억읽기(ADRES + 2) << 8 | cihaz_değer.기억읽기(ADRES + 3);
    }
    static int çek_ADRES(int ADRES, int süre_değer) {
        if (süre_değer < 16) return -22;
        if (!yürütme_yönetici.klip(ADRES, 16)) return -14;
        return yürütme_yönetici.짧은수(ADRES) == 2 ? 0 : -97;
    }
    static int BIND_ADRES(int tanımlayıcı_girdi, int ADRES, int süre_değer) {
        int tanımlayıcı_değer_a78cee47 = uç_nokta_tanımlayıcı(tanımlayıcı_girdi);
        if (tanımlayıcı_değer_a78cee47 < 0) return tanımlayıcı_değer_a78cee47;
        int sonuç = çek_ADRES(ADRES, süre_değer);
        if (sonuç < 0) return sonuç;
        if (ağ_sap[tanımlayıcı_değer_a78cee47] != 0) return -22;
        int ağ_kimliği = ADRES_32(ADRES + 4);
        if (ağ_kimliği != 0 && ağ_kimliği != ağ_Yığın.내주소) return -99;
        int bağlantı_noktası_numarası = cihaz_değer.기억읽기(ADRES + 2) << 8 | cihaz_değer.기억읽기(ADRES + 3);
        sonuç = ağ_Yığın.Aç(bağlantı_noktası_numarası);
        if (sonuç < 0) return sonuç;
        ağ_sap[tanımlayıcı_değer_a78cee47] = sonuç; hedef[tanımlayıcı_değer_a78cee47] = ağ_kimliği;
        return 0;
    }
    static int Otomatik_BIND(int tanımlayıcı_değer_a78cee47) {
        if (ağ_sap[tanımlayıcı_değer_a78cee47] != 0) return 0;
        int sonuç = ağ_Yığın.Aç(0);
        if (sonuç < 0) return sonuç;
        ağ_sap[tanımlayıcı_değer_a78cee47] = sonuç;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 istek 구조체로 전달한다.
    static int göndermek_veri_birimi_veri(int tanımlayıcı_girdi, int veri_ADRES, int süre_değer, int Ayarlar, int istendi_ADRES) {
        int tanımlayıcı_değer_a78cee47 = uç_nokta_tanımlayıcı(tanımlayıcı_girdi);
        if (tanımlayıcı_değer_a78cee47 < 0) return tanımlayıcı_değer_a78cee47;
        if (Ayarlar != 0) return -95;
        if (süre_değer < 0 || süre_değer > 1024) return -90;
        if (süre_değer != 0 && !yürütme_yönetici.klip(veri_ADRES, süre_değer)) return -14;
        if (!yürütme_yönetici.klip(istendi_ADRES, 8)) return -14;
        int ADRES = yürütme_yönetici.수(istendi_ADRES);
        int sonuç = çek_ADRES(ADRES, yürütme_yönetici.수(istendi_ADRES + 4));
        if (sonuç < 0) return sonuç;
        int bağlantı_noktası_numarası = cihaz_değer.기억읽기(ADRES + 2) << 8 | cihaz_değer.기억읽기(ADRES + 3);
        if (bağlantı_noktası_numarası == 0) return -22;
        sonuç = Otomatik_BIND(tanımlayıcı_değer_a78cee47);
        if (sonuç < 0) return sonuç;
        for (int Dizin = 0; Dizin < süre_değer; Dizin++) devir_veri[Dizin] = cihaz_değer.기억읽기(veri_ADRES + Dizin);
        return ağ_Yığın.göndermek(ağ_sap[tanımlayıcı_değer_a78cee47], ADRES_32(ADRES + 4), bağlantı_noktası_numarası, devir_veri, süre_değer);
    }
    static void yazma_ADRES(int ADRES, int süre_değer, int ağ_kimliği, int bağlantı_noktası_numarası) {
        for (int Dizin = 0; Dizin < süre_değer && Dizin < 16; Dizin++) {
            int değer = 0;
            if (Dizin == 0) değer = 2;
            if (Dizin == 2) değer = bağlantı_noktası_numarası >>> 8;
            if (Dizin == 3) değer = bağlantı_noktası_numarası;
            if (Dizin >= 4 && Dizin < 8) değer = ağ_kimliği >>> (56 - Dizin * 8);
            cihaz_değer.yazma_Bellek(ADRES + Dizin, değer & 255);
        }
    }
    static int almak_veri_birimi_veri(int tanımlayıcı_girdi, int veri_ADRES, int süre_değer, int Ayarlar, int istendi_ADRES) {
        int tanımlayıcı_değer_a78cee47 = uç_nokta_tanımlayıcı(tanımlayıcı_girdi);
        if (tanımlayıcı_değer_a78cee47 < 0) return tanımlayıcı_değer_a78cee47;
        if ((Ayarlar & ~64) != 0) return -95;
        if (süre_değer < 0) return -22;
        if (süre_değer != 0 && !yürütme_yönetici.klip(veri_ADRES, süre_değer)) return -14;
        int ADRES = 0, ADRES_süre_ADRES = 0, ADRES_süre = 0;
        if (istendi_ADRES != 0) {
            if (!yürütme_yönetici.klip(istendi_ADRES, 8)) return -14;
            ADRES = yürütme_yönetici.수(istendi_ADRES); ADRES_süre_ADRES = yürütme_yönetici.수(istendi_ADRES + 4);
            if (ADRES != 0) {
                if (!yürütme_yönetici.klip(ADRES_süre_ADRES, 4)) return -14;
                ADRES_süre = yürütme_yönetici.수(ADRES_süre_ADRES);
                if (ADRES_süre < 0) return -22;
                if (!yürütme_yönetici.klip(ADRES, ADRES_süre < 16 ? ADRES_süre : 16)) return -14;
            }
        }
        int sonuç = Otomatik_BIND(tanımlayıcı_değer_a78cee47);
        if (sonuç < 0) return sonuç;
        int çalıştır = cihaz_değer.밀리초();
        while (true) {
            sonuç = ağ_Yığın.almak(ağ_sap[tanımlayıcı_değer_a78cee47], devir_veri, 1024, 0);
            if (sonuç != -11) break;
            if ((Ayarlar & 64) != 0 || (açık_Ayarlar[tanımlayıcı_değer_a78cee47] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[tanımlayıcı_değer_a78cee47] > 0 && cihaz_değer.밀리초() - çalıştır >= 수신대기밀리초[tanımlayıcı_değer_a78cee47]) return -11;
            if (cihaz_değer.사용자남은밀리초() <= 10) return -11;
            cihaz_değer.잠시양보();
        }
        if (sonuç < 0) return sonuç;
        if (sonuç > süre_değer) sonuç = süre_değer;
        for (int Dizin = 0; Dizin < sonuç; Dizin++) cihaz_değer.yazma_Bellek(veri_ADRES + Dizin, devir_veri[Dizin]);
        if (ADRES != 0) {
            yazma_ADRES(ADRES, ADRES_süre, ağ_Yığın.eş_ADRES(ağ_sap[tanımlayıcı_değer_a78cee47]), ağ_Yığın.eş_bağlantı_noktası_numarası(ağ_sap[tanımlayıcı_değer_a78cee47]));
            yürütme_yönetici.수쓰기(ADRES_süre_ADRES, 16);
        }
        return sonuç;
    }
    static int 통신주소읽기(int tanımlayıcı_girdi, int ADRES, int süre_ADRES) {
        int tanımlayıcı_değer_a78cee47 = uç_nokta_tanımlayıcı(tanımlayıcı_girdi);
        if (tanımlayıcı_değer_a78cee47 < 0) return tanımlayıcı_değer_a78cee47;
        if (!yürütme_yönetici.klip(süre_ADRES, 4)) return -14;
        int süre_değer = yürütme_yönetici.수(süre_ADRES);
        if (süre_değer < 0) return -22;
        if (!yürütme_yönetici.klip(ADRES, süre_değer < 16 ? süre_değer : 16)) return -14;
        int yuva_girdi = ağ_Yığın.Dizin(ağ_sap[tanımlayıcı_değer_a78cee47]);
        yazma_ADRES(ADRES, süre_değer, hedef[tanımlayıcı_değer_a78cee47], yuva_girdi < 0 ? 0 : ağ_Yığın.접속번호들[yuva_girdi]);
        yürütme_yönetici.수쓰기(süre_ADRES, 16);
        return 0;
    }
    static int küme_almak_ZAMANAŞIMI(int tanımlayıcı_girdi, int 밀리초) {
        int tanımlayıcı_değer_a78cee47 = uç_nokta_tanımlayıcı(tanımlayıcı_girdi);
        if (tanımlayıcı_değer_a78cee47 < 0) return tanımlayıcı_değer_a78cee47;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[tanımlayıcı_değer_a78cee47] = 밀리초;
        return 0;
    }
}
