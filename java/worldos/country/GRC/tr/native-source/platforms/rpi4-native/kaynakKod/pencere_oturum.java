// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 kabuk Durum_değer. dosya 저장소는 공유하고 yol/değişken_değer/LOG_KAYIT/입력은 분리한다. */
public final class pencere_oturum {
    static int[] 보관 = new int[4 * 30000], Hazırlan = new int[4];
    static int geçerli_öğe, konum;
    static boolean 이어읽기;
    static void DİZİ_değer(int[] veri, boolean depo_değer) {
        for (int Loop_Dizin = 0; Loop_Dizin < veri.length; Loop_Dizin++) { if (depo_değer) 보관[konum++] = veri[Loop_Dizin]; else veri[Loop_Dizin] = 보관[konum++]; }
    }
    static int değer(int veri_değer, boolean 저장여부) { if (저장여부) { 보관[konum++] = veri_değer; return veri_değer; } return 보관[konum++]; }
    static void arama_konum(int 보관칸, boolean 저장여부) {
        konum = 보관칸 * 30000;
        DİZİ_değer(BellekDosyaları.geçerli_öğe, 저장여부); BellekDosyaları.geçerli_süre_6ac7278b = değer(BellekDosyaları.geçerli_süre_6ac7278b, 저장여부);
        DİZİ_değer(kabuk_söz_dizimi.değişken_ad, 저장여부); DİZİ_değer(kabuk_söz_dizimi.değişken_veri, 저장여부); DİZİ_değer(kabuk_söz_dizimi.이름길이, 저장여부); DİZİ_değer(kabuk_söz_dizimi.değer_süre, 저장여부);
        kabuk_söz_dizimi.Durum_değer = değer(kabuk_söz_dizimi.Durum_değer, 저장여부);
        DİZİ_değer(satır_düzenleyicisi.LOG_KAYIT, 저장여부); DİZİ_değer(satır_düzenleyicisi.LOG_süre, 저장여부); DİZİ_değer(satır_düzenleyicisi.depo_değer, 저장여부); DİZİ_değer(KomutYorumlayıcı.girdi_satırı, 저장여부);
        satır_düzenleyicisi.LOG_BAĞ_DEĞ_SAY = değer(satır_düzenleyicisi.LOG_BAĞ_DEĞ_SAY, 저장여부); satır_düzenleyicisi.LOG_KAYIT_Bitiş = değer(satır_düzenleyicisi.LOG_KAYIT_Bitiş, 저장여부);
        satır_düzenleyicisi.Ara_değer = değer(satır_düzenleyicisi.Ara_değer, 저장여부); satır_düzenleyicisi.저장길이 = değer(satır_düzenleyicisi.저장길이, 저장여부);
        satır_düzenleyicisi.Boyut = değer(satır_düzenleyicisi.Boyut, 저장여부); satır_düzenleyicisi.imleç_değer = değer(satır_düzenleyicisi.imleç_değer, 저장여부); satır_düzenleyicisi.Start_pencere = değer(satır_düzenleyicisi.Start_pencere, 저장여부);
        Hazırlan[보관칸] = 1;
    }
    static void işlem_değer_girdi() {
        int 사건번호 = Pano.uçbirim(12); if (사건번호 == 0) return;
        arama_konum(geçerli_öğe, true);
        for (int Loop_Dizin = 0; Loop_Dizin < 4; Loop_Dizin++) {
            if ((사건번호 & (1 << (8 + Loop_Dizin))) != 0) { Pano.denetim_kullanıcı_program(32 + Loop_Dizin); Hazırlan[Loop_Dizin] = 0; }
            if ((사건번호 & (1 << (4 + Loop_Dizin))) != 0 && Loop_Dizin != geçerli_öğe) Hazırlan[Loop_Dizin] = 0;
        }
        int Sonraki_konum = (사건번호 & 15) - 1; if (Sonraki_konum < 0) Sonraki_konum = 0;
        if (Hazırlan[Sonraki_konum] == 0) for (int Loop_Dizin = 0; Loop_Dizin < 30000; Loop_Dizin++) 보관[Sonraki_konum * 30000 + Loop_Dizin] = 0;
        geçerli_öğe = Sonraki_konum; arama_konum(geçerli_öğe, false); Pano.uçbirim(100 + geçerli_öğe); 이어읽기 = true;
        단말.Yazma("\nTERMINAL FOCUS "); 단말.수(geçerli_öğe + 1); 단말.문자(10);
    }
    static boolean özgeçmiş_yürütme() {
        if (Pano.denetim_kullanıcı_program(16 + geçerli_öğe) == 0) return false;
        셸입출력.İzin_Ver_devralmak = true; 셸입출력.çalıştır(false, false); Pano.입출력전환(1);
        int 처리값 = Pano.denetim_kullanıcı_program(geçerli_öğe); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; kabuk_söz_dizimi.Durum_değer = 처리값 < 0 ? 126 : 처리값; 단말.Yazma("exit "); 단말.수(처리값); 단말.문자(10); Pano.uçbirim(3); }
        return true;
    }
}
