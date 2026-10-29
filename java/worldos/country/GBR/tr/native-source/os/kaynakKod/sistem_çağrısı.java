// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 kullanıcı_alanı işaretçi/길이는 erişim_girdi 전에 검사한다. */
public final class sistem_çağrısı {
    static int[] 임시자료 = new int[1024];

    static int DİZİ_süre(int ADRES) {
        if (!yürütme_yönetici.klip(ADRES, 4)) return -14;
        int süre_değer = yürütme_yönetici.수(ADRES);
        if (süre_değer < 0 || süre_değer > (yürütme_yönetici.kullanıcı_Bitiş - ADRES - 4) / 4) return -14;
        return süre_değer;
    }

    public static int işlem_değer_girdi(int Dizin, int 가, int SANİYE_işlenen, int 다, int 라, int 마) {
        if (Dizin == 30) return Dosya_tanımlayıcı_yönetici.açık_Dosya(가, SANİYE_işlenen, 다);
        if (Dizin == 31) return Dosya_tanımlayıcı_yönetici.파일읽기(가, SANİYE_işlenen, 다);
        if (Dizin == 32) return Dosya_tanımlayıcı_yönetici.yazma_Dosya(가, SANİYE_işlenen, 다);
        if (Dizin == 33) return Dosya_tanımlayıcı_yönetici.Kapat_Dosya(가);
        if (Dizin == 34) return Dosya_tanımlayıcı_yönetici.arama_Dosya(가, SANİYE_işlenen, 다);
        if (Dizin == 35) return Dosya_tanımlayıcı_yönetici.kopya_tanımlayıcı(가, 0, false, 0);
        if (Dizin == 36) return Dosya_tanımlayıcı_yönetici.kopya_tanımlayıcı(가, SANİYE_işlenen, true, 0);
        if (Dizin == 37) return Dosya_tanımlayıcı_yönetici.파일상태읽기(가, SANİYE_işlenen);
        if (Dizin == 38) return Dosya_tanımlayıcı_yönetici.kaldırmak_Dosya_girdi_ad(가);
        if (Dizin == 39) return Dosya_tanımlayıcı_yönetici.küme_Dosya_süre(가, SANİYE_işlenen);
        if (Dizin == 40) return Dosya_tanımlayıcı_yönetici.denetim_tanımlayıcı(가, SANİYE_işlenen, 다);
        if (Dizin == 41) return Dosya_tanımlayıcı_yönetici.açmak_uç_nokta(가, SANİYE_işlenen, 다);
        if (Dizin == 42) return Dosya_tanımlayıcı_yönetici.BIND_ADRES(가, SANİYE_işlenen, 다);
        if (Dizin == 43) return Dosya_tanımlayıcı_yönetici.göndermek_veri_birimi_veri(가, SANİYE_işlenen, 다, 라, 마);
        if (Dizin == 44) return Dosya_tanımlayıcı_yönetici.almak_veri_birimi_veri(가, SANİYE_işlenen, 다, 라, 마);
        if (Dizin == 45) return Dosya_tanımlayıcı_yönetici.통신주소읽기(가, SANİYE_işlenen, 다);
        if (Dizin == 46) return Dosya_tanımlayıcı_yönetici.küme_almak_ZAMANAŞIMI(가, SANİYE_işlenen);
        if (Dizin == 47) {
            int tanımlayıcı_değer_a78cee47 = Dosya_tanımlayıcı_yönetici.BUL_tanımlayıcı(가);
            if (tanımlayıcı_değer_a78cee47 < 0) return -9;
            if (Dosya_tanımlayıcı_yönetici.Tip_değer[tanımlayıcı_değer_a78cee47] != 2) return -22;
            return 파일보존.eşitlemek();
        }
        if (Dizin == 1) {
            int süre_değer = DİZİ_süre(가);
            if (süre_değer < 0) return süre_değer;
            if (süre_değer > 4096) return -90;
            for (int karakter_değer = 0; karakter_değer < süre_değer; karakter_değer++) SMS_Terminal.문자(yürütme_yönetici.수(가 + 4 + karakter_değer * 4) & 65535);
            return süre_değer;
        }
        if (Dizin == 2) return yürütme_yönetici.bağımsız_değişken_BAĞ_DEĞ_SAY;
        if (Dizin == 3) return 가 >= 0 && 가 < yürütme_yönetici.bağımsız_değişken_BAĞ_DEĞ_SAY ? yürütme_yönetici.bağımsız_değişken_ADRES[가] : 0;
        if (Dizin == 10) return ağ_Yığın.Aç(가);
        if (Dizin == 11) {
            int süre_değer = DİZİ_süre(라);
            if (süre_değer < 0) return süre_değer;
            if (마 < 0 || 마 > süre_değer || 마 > 1024) return -90;
            for (int konum = 0; konum < 마; konum++) 임시자료[konum] = yürütme_yönetici.수(라 + 4 + konum * 4) & 255;
            return ağ_Yığın.göndermek(가, SANİYE_işlenen, 다, 임시자료, 마);
        }
        if (Dizin == 12) {
            int süre_değer = DİZİ_süre(SANİYE_işlenen);
            if (süre_değer < 0) return süre_değer;
            if (다 < 0 || 다 > 2000) return -22;
            int sonuç = ağ_Yığın.almak(가, 임시자료, süre_değer < 1024 ? süre_değer : 1024, 다);
            if (sonuç >= 0) for (int konum = 0; konum < sonuç; konum++) yürütme_yönetici.수쓰기(SANİYE_işlenen + 4 + konum * 4, 임시자료[konum]);
            return sonuç;
        }
        if (Dizin == 13) return ağ_Yığın.Kapat(가);
        if (Dizin == 14) return ağ_Yığın.내주소;
        if (Dizin == 15) return ağ_Yığın.eş_ADRES(가);
        if (Dizin == 16) return ağ_Yığın.eş_bağlantı_noktası_numarası(가);
        if (Dizin == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminal.문자(가); return 1;
        }
        if (Dizin == 20 || Dizin == 21) {
            int ad_boyutlandırmak = DİZİ_süre(가), veri_boyutlandırmak = DİZİ_süre(SANİYE_işlenen);
            if (ad_boyutlandırmak < 0 || veri_boyutlandırmak < 0) return -14;
            if (ad_boyutlandırmak < 1 || ad_boyutlandırmak > 64) return -22;
            int süre_değer = 0;
            while (süre_değer < ad_boyutlandırmak && yürütme_yönetici.수(가 + 4 + süre_değer * 4) != 0) {
                Bellek_dosya_sistemi.İsim[süre_değer] = yürütme_yönetici.수(가 + 4 + süre_değer * 4);
                süre_değer++;
            }
            if (!Bellek_dosya_sistemi.çek_ad(Bellek_dosya_sistemi.İsim, süre_değer)) return -22;
            if (Dizin == 20) {
                int dosya = Bellek_dosya_sistemi.BUL_girdi(Bellek_dosya_sistemi.İsim, süre_değer);
                if (dosya < 0) return dosya;
                int Boyut = Bellek_dosya_sistemi.boyutlandırmak_Liste[dosya];
                if (Boyut > veri_boyutlandırmak) return -90;
                int ADRES = cihaz_değer.Dosya_Bellek() + dosya * Bellek_dosya_sistemi.최대크기;
                for (int 수 = 0; 수 < Boyut; 수++) yürütme_yönetici.수쓰기(SANİYE_işlenen + 4 + 수 * 4, cihaz_değer.기억읽기(ADRES + 수));
                return Boyut;
            }
            if (다 < 0 || 다 > veri_boyutlandırmak) return -22;
            if (다 > Bellek_dosya_sistemi.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Bellek_dosya_sistemi.Düzenle_değer[수] = yürütme_yönetici.수(SANİYE_işlenen + 4 + 수 * 4) & 255;
            return Bellek_dosya_sistemi.depo_değer(Bellek_dosya_sistemi.İsim, süre_değer, Bellek_dosya_sistemi.Düzenle_değer, 다);
        }
        return -38;
    }
}
