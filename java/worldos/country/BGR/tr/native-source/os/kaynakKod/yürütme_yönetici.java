// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Okuma 전용 yürütmek_komut 묶음의 ELF32 doğrulamak_5fb2b747, bağımsız_değişkenler İleri_değer, 한 번에 한 kullanıcı_alanı işlem_değer yürütmek_komut. */
public final class yürütme_yönetici {
    static final int Start_kullanıcı_program = 0x04000000;
    static final int kullanıcı_Bitiş = 0x04400000;
    static final int RESİM_Bitiş_ADRES = 0x04200000;
    static final int bağımsız_değişken_Start = 0x04300000;
    static int bağımsız_değişken_BAĞ_DEĞ_SAY = 0;
    static int[] bağımsız_değişken_ADRES = new int[16];

    static boolean klip(int ADRES, int süre_değer) {
        return ADRES >= Start_kullanıcı_program && ADRES < kullanıcı_Bitiş && süre_değer >= 0 && süre_değer <= kullanıcı_Bitiş - ADRES;
    }

    static int 수(int ADRES) { return Bellek_bölge.ayrıştırmak_bilgi(ADRES); }
    static int 짧은수(int ADRES) { return cihaz_değer.기억읽기(ADRES) | cihaz_değer.기억읽기(ADRES + 1) << 8; }
    static void 수쓰기(int ADRES, int değer) {
        for (int Dizin = 0; Dizin < 4; Dizin++) cihaz_değer.yazma_Bellek(ADRES + Dizin, değer >>> (Dizin * 8));
    }

    static int Grup_BAĞ_DEĞ_SAY() {
        int ADRES = cihaz_değer.yürütülebilir_paket_iş();
        int Boyut = cihaz_değer.yürütülebilir_paket_iş_boyutlandırmak();
        if (Boyut < 8 || 수(ADRES) != 0x50414b4a) return 0;
        int öğe_BAĞ_DEĞ_SAY = 수(ADRES + 4);
        return öğe_BAĞ_DEĞ_SAY >= 0 && öğe_BAĞ_DEĞ_SAY <= 32 && öğe_BAĞ_DEĞ_SAY <= (Boyut - 8) / 24 ? öğe_BAĞ_DEĞ_SAY : 0;
    }

    static void girdi_Liste() {
        for (int Dizin = 0; Dizin < Grup_BAĞ_DEĞ_SAY(); Dizin++) {
            int girdi_değer = cihaz_değer.yürütülebilir_paket_iş() + 8 + Dizin * 24;
            for (int karakter_değer = 0; karakter_değer < 16 && cihaz_değer.기억읽기(girdi_değer + karakter_değer) != 0; karakter_değer++)
                SMS_Terminal.문자(cihaz_değer.기억읽기(girdi_değer + karakter_değer));
            SMS_Terminal.Yazma("\n");
        }
    }

    static int BUL_girdi(int[] artış_değer, int çalıştır, int süre_değer) {
        if (süre_değer <= 0 || süre_değer >= 16) return 0;
        for (int Dizin = 0; Dizin < Grup_BAĞ_DEĞ_SAY(); Dizin++) {
            int girdi_değer = cihaz_değer.yürütülebilir_paket_iş() + 8 + Dizin * 24;
            boolean 같음 = cihaz_değer.기억읽기(girdi_değer + süre_değer) == 0;
            for (int karakter_değer = 0; karakter_değer < süre_değer; karakter_değer++)
                if (artış_değer[çalıştır + karakter_değer] != cihaz_değer.기억읽기(girdi_değer + karakter_değer)) 같음 = false;
            if (같음) return girdi_değer;
        }
        return 0;
    }

    static int doğrulamak_5fb2b747(int dosya, int süre_değer) {
        if (süre_değer < 52 || 수(dosya) != 0x464c457f || cihaz_değer.기억읽기(dosya + 4) != 1
            || cihaz_değer.기억읽기(dosya + 5) != 1 || cihaz_değer.기억읽기(dosya + 6) != 1
            || 짧은수(dosya + 16) != 2 || 짧은수(dosya + 18) != 3 || 수(dosya + 20) != 1
            || 짧은수(dosya + 40) != 52 || 짧은수(dosya + 42) != 32) return -8;
        int giriş_noktası_değer = 수(dosya + 24);
        int tablo_konum = 수(dosya + 28);
        int öğe_BAĞ_DEĞ_SAY = 짧은수(dosya + 44);
        if (öğe_BAĞ_DEĞ_SAY == 0 || öğe_BAĞ_DEĞ_SAY > 16 || tablo_konum < 52 || tablo_konum > süre_değer - öğe_BAĞ_DEĞ_SAY * 32) return -8;
        boolean bilgi_teknolojisi_yürütülebilir = false;
        for (int Dizin = 0; Dizin < öğe_BAĞ_DEĞ_SAY; Dizin++) {
            int arama_tablosu = dosya + tablo_konum + Dizin * 32;
            int Tip_değer = 수(arama_tablosu);
            if (Tip_değer == 2 || Tip_değer == 3) return -8; // 동적 Bağlan/ayrıştırıcı_48ee4b1b 미지원
            if (Tip_değer != 1) continue;
            int konum = 수(arama_tablosu + 4), ADRES = 수(arama_tablosu + 8), dosya_boyutu = 수(arama_tablosu + 16), Bellek_boyutlandırmak = 수(arama_tablosu + 20);
            int hizalamak_değer = 수(arama_tablosu + 28);
            if (ADRES < Start_kullanıcı_program || ADRES >= RESİM_Bitiş_ADRES || Bellek_boyutlandırmak < 0 || Bellek_boyutlandırmak > RESİM_Bitiş_ADRES - ADRES
                || dosya_boyutu < 0 || dosya_boyutu > Bellek_boyutlandırmak || konum < 0 || (dosya_boyutu > 0 && konum > süre_değer - dosya_boyutu)
                || (hizalamak_değer != 0 && (hizalamak_değer < 0 || (hizalamak_değer & (hizalamak_değer - 1)) != 0
                    || ((ADRES - konum) & (hizalamak_değer - 1)) != 0))) return -8;
            for (int ön_kamera_değer = 0; ön_kamera_değer < Dizin; ön_kamera_değer++) {
                int Önceki_öğe = dosya + tablo_konum + ön_kamera_değer * 32;
                if (수(Önceki_öğe) == 1 && Bellek_boyutlandırmak > 0 && 수(Önceki_öğe + 20) > 0
                    && ADRES < 수(Önceki_öğe + 8) + 수(Önceki_öğe + 20) && 수(Önceki_öğe + 8) < ADRES + Bellek_boyutlandırmak) return -8;
            }
            if ((수(arama_tablosu + 24) & 1) != 0 && giriş_noktası_değer >= ADRES && giriş_noktası_değer - ADRES < dosya_boyutu) bilgi_teknolojisi_yürütülebilir = true;
        }
        return bilgi_teknolojisi_yürütülebilir ? giriş_noktası_değer : -8;
    }

    static int yürütmek_komut(int[] artış_değer, int çalıştır, int süre_değer) {
        while (çalıştır < süre_değer && artış_değer[çalıştır] == ' ') çalıştır++;
        int 끝 = çalıştır;
        while (끝 < süre_değer && artış_değer[끝] != ' ') 끝++;
        int girdi_değer = BUL_girdi(artış_değer, çalıştır, 끝 - çalıştır);
        if (girdi_değer == 0) return -2;
        int konum = 수(girdi_değer + 16), Boyut = 수(girdi_değer + 20);
        if (konum < 8 + Grup_BAĞ_DEĞ_SAY() * 24 || Boyut < 52 || konum > cihaz_değer.yürütülebilir_paket_iş_boyutlandırmak() - Boyut) return -8;
        int dosya = cihaz_değer.yürütülebilir_paket_iş() + konum;
        int giriş_noktası_değer = doğrulamak_5fb2b747(dosya, Boyut);
        if (giriş_noktası_değer < 0) return giriş_noktası_değer;
        cihaz_değer.kullanıcı_takas_içindekiler();
        int tablo_konum = 수(dosya + 28), öğe_BAĞ_DEĞ_SAY = 짧은수(dosya + 44);
        for (int Dizin = 0; Dizin < öğe_BAĞ_DEĞ_SAY; Dizin++) {
            int arama_tablosu = dosya + tablo_konum + Dizin * 32;
            if (수(arama_tablosu) != 1) continue;
            int 원본 = dosya + 수(arama_tablosu + 4), hedef_değer = 수(arama_tablosu + 8), dosya_boyutu = 수(arama_tablosu + 16);
            for (int bayt_değer = 0; bayt_değer < dosya_boyutu; bayt_değer++) cihaz_değer.yazma_Bellek(hedef_değer + bayt_değer, cihaz_değer.기억읽기(원본 + bayt_değer));
        }
        bağımsız_değişken_BAĞ_DEĞ_SAY = 0;
        int depo_değer = bağımsız_değişken_Start;
        while (끝 < süre_değer) {
            while (끝 < süre_değer && artış_değer[끝] == ' ') 끝++;
            if (끝 == süre_değer) break;
            if (bağımsız_değişken_BAĞ_DEĞ_SAY == bağımsız_değişken_ADRES.length) return -22;
            çalıştır = 끝;
            while (끝 < süre_değer && artış_değer[끝] != ' ') 끝++;
            bağımsız_değişken_ADRES[bağımsız_değişken_BAĞ_DEĞ_SAY++] = depo_değer;
            수쓰기(depo_değer, 끝 - çalıştır);
            for (int karakter_değer = çalıştır; karakter_değer < 끝; karakter_değer++) 수쓰기(depo_değer + 4 + (karakter_değer - çalıştır) * 4, artış_değer[karakter_değer]);
            depo_değer += 4 + (끝 - çalıştır) * 4;
        }
        ağ_Yığın.TEMİZ_işlem();
        Dosya_tanımlayıcı_yönetici.Start_işlem();
        int sonuç = cihaz_değer.çalıştırma_kullanıcı_program(giriş_noktası_değer, kullanıcı_Bitiş - 16);
        Dosya_tanımlayıcı_yönetici.TEMİZ_işlem();
        ağ_Yığın.TEMİZ_işlem();
        return sonuç;
    }
}
