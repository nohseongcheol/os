// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. dosya/işlenen_Yığın/Başvuru/dal 경계를 yürütmek_komut 중 검사한다. */
public final class 자바가상기계 {
    static int[] dosya = new int[16 * 16384], geçici_dosya = new int[16384], dosya_adı_SMS = new int[512];
    static int[] sabit_etiket = new int[8192], 상가 = new int[8192], sabit_SANİYE_değer = new int[8192], dize_Başvuru = new int[8192];
    static int[] metot_ad_SMS = new int[512], metot_TÜR = new int[512], metot_erişim = new int[512], metot_sahip = new int[512];
    static int[] metot_Start = new int[512], metot_Bitiş = new int[512], metot_Yığın = new int[512], 함수지역 = new int[512];
    static int[] metot_bağımsız_değişken_BAĞ_DEĞ_SAY = new int[512], metot_bağımsız_değişken_TÜR = new int[8192], metot_İade = new int[512];
    static int[] sınır_değer = new int[16 * 16384];
    static int[] yerel_değer = new int[16384], yerel_TÜR = new int[16384], işlenen_Yığın_değer = new int[16384], işlenen_Yığın_TÜR = new int[16384];
    static int[] kare_metot = new int[128], kare_konum = new int[128], kare_Yığın = new int[128], 틀명령 = new int[128], 틀초기화 = new int[128];
    static int[] Sınıf_Tanım_ad = new int[16], Sınıf_Tanım_boyutlandırmak = new int[16], Sınıf_Tanım_ana = new int[16], Sınıf_Tanım_Durum = new int[16], Sınıf_yuva_BAĞ_DEĞ_SAY = new int[16], 종초기화 = new int[16];
    static int[] Sınıf_arabirim = new int[16 * 16], Sınıf_arabirim_BAĞ_DEĞ_SAY = new int[16];
    static int[] yuva_ad = new int[512], yuva_TÜR = new int[512], yuva_sahip = new int[512], yuva_izinler = new int[512], yuva_konum = new int[512], yuva_veri = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] yığın_değer = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], yığın_Başvuru = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], dizi_öğesi = new int[32768], depo_bilgi = new int[256];
    static int Boyut, 읽기위치, metot_BAĞ_DEĞ_SAY, sınıf_adı, kare_Dizin = -1, yığın_Bitiş_konum = 1, dönüş_türü;
    static int Sınıf_Tanım_BAĞ_DEĞ_SAY, yuva_BAĞ_DEĞ_SAY, 잡기수, 현재읽는종, 던진객체, 잠시수, monitör_BAĞ_DEĞ_SAY, tahsilat_BAĞ_DEĞ_SAY;
    static int geçerli_yazışma, yazışma_BAĞ_DEĞ_SAY = 1, girdi_Sınıf_Tanım;
    static int[] yazışma_kare = new int[4], yazışma_Durum = new int[4], yazışma_nesne = new int[4], yazışma_hedef = new int[4], 가닥대기 = new int[4];
    static boolean hata, değişiklik_isteği;
    static int[] kilit_sahip = new int[32768], 잠금깊이 = new int[32768], kare_kilit = new int[128], Sınıf_kilit = new int[16], Sınıf_yazışma = new int[16];

    static void hata_değer(String Word_SMS) {
        if (hata) return;
        int alan_KOD = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) alan_KOD = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) alan_KOD = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) alan_KOD = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) alan_KOD = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) alan_KOD = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) alan_KOD = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) alan_KOD = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) alan_KOD = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) alan_KOD = 15;
        if (alan_KOD != 0 && kare_Dizin >= 0) { 예외던짐(alan_KOD, Word_SMS); return; }
        kullanıcı_alanı.Yazma("JVM error: "); kullanıcı_alanı.Yazma(Word_SMS); kullanıcı_alanı.yazma_karakter_değer(10); hata = true;
    }
    static boolean klip(int çalıştır, int süre_değer) {
        if (çalıştır < 0 || çalıştır >= dosya.length || süre_değer < 0) return false;
        int Sınıf_Tanım = çalıştır / 16384;
        return çalıştır % 16384 <= Sınıf_Tanım_boyutlandırmak[Sınıf_Tanım] && süre_değer <= Sınıf_Tanım_boyutlandırmak[Sınıf_Tanım] - çalıştır % 16384;
    }
    static int bayt_değer() {
        if (!klip(읽기위치, 1)) { hata_değer("truncated class file"); return 0; }
        return dosya[읽기위치++];
    }
    static int 짧은수() { return bayt_değer() << 8 | bayt_değer(); }
    static int bilgi() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int süre_değer) { if (!klip(읽기위치, süre_değer)) hata_değer("invalid attribute size"); else 읽기위치 += süre_değer; }
    static boolean çek_sabit(int 수, int Tip_değer) {
        if (수 <= 0 || 수 >= sabit_etiket.length || sabit_etiket[수] != Tip_değer) { hata_değer("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_aralık(int çalıştır, int süre_değer, String Word_SMS) {
        if (!klip(çalıştır, süre_değer)) return false;
        int 읽는자리 = çalıştır, 끝 = çalıştır + süre_değer;
        for (int Loop_Dizin = 0; Loop_Dizin < Word_SMS.length(); Loop_Dizin++) {
            int kod_noktası = Word_SMS.charAt(Loop_Dizin);
            if (kod_noktası > 0 && kod_noktası < 128) { if (읽는자리 >= 끝 || dosya[읽는자리++] != kod_noktası) return false; }
            else if (kod_noktası < 2048) {
                if (읽는자리 + 2 > 끝 || dosya[읽는자리++] != (192 | (kod_noktası >> 6)) || dosya[읽는자리++] != (128 | (kod_noktası & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || dosya[읽는자리++] != (224 | (kod_noktası >> 12)) || dosya[읽는자리++] != (128 | ((kod_noktası >> 6) & 63)) || dosya[읽는자리++] != (128 | (kod_noktası & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Word_SMS(int sabit_değer, String Word_SMS) { return çek_sabit(sabit_değer, 1) && SMS_aralık(상가[sabit_değer], sabit_SANİYE_değer[sabit_değer], Word_SMS); }
    static boolean 같은말(int 가, int SANİYE_işlenen) {
        if (!çek_sabit(가, 1) || !çek_sabit(SANİYE_işlenen, 1) || sabit_SANİYE_değer[가] != sabit_SANİYE_değer[SANİYE_işlenen]) return false;
        for (int 수 = 0; 수 < sabit_SANİYE_değer[가]; 수++) if (dosya[상가[가] + 수] != dosya[상가[SANİYE_işlenen] + 수]) return false;
        return true;
    }
    static int sınıf_adı_SMS(int 수) { return çek_sabit(수, 7) && çek_sabit(상가[수], 1) ? 상가[수] : 0; }
    static int Başvuru_ad(int 수) { return çek_sabit(수, 12) && çek_sabit(상가[수], 1) ? 상가[수] : 0; }
    static int başvuru_türü(int 수) { return çek_sabit(수, 12) && çek_sabit(sabit_SANİYE_değer[수], 1) ? sabit_SANİYE_değer[수] : 0; }
    static int tanımlayıcı_TÜR(int 끝, boolean boş_TÜR) {
        if (읽기위치 >= 끝) { hata_değer("invalid descriptor"); return 0; }
        int değer = bayt_değer();
        if (değer == 'V' && boş_TÜR) return 0;
        if (değer == 'I' || değer == 'B' || değer == 'C' || değer == 'S' || değer == 'Z') return 1;
        if (değer == '[') { tanımlayıcı_TÜR(끝, false); return 2; }
        if (değer == 'L') {
            int çalıştır = 읽기위치;
            while (읽기위치 < 끝 && dosya[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == çalıştır) hata_değer("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        hata_değer("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int işlev_değer) {
        int Önceki_öğe = 읽기위치, 수 = metot_TÜR[işlev_değer];
        if (!çek_sabit(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + sabit_SANİYE_değer[수];
        if (bayt_değer() != '(') hata_değer("invalid method descriptor");
        int öğe_BAĞ_DEĞ_SAY = 0;
        while (!hata && 읽기위치 < 끝 && dosya[읽기위치] != ')') {
            if (öğe_BAĞ_DEĞ_SAY == 16) { hata_değer("too many method arguments"); break; }
            metot_bağımsız_değişken_TÜR[işlev_değer * 16 + öğe_BAĞ_DEĞ_SAY++] = tanımlayıcı_TÜR(끝, false);
        }
        if (읽기위치 >= 끝 || bayt_değer() != ')') hata_değer("invalid method descriptor");
        metot_İade[işlev_değer] = tanımlayıcı_TÜR(끝, true); metot_bağımsız_değişken_BAĞ_DEĞ_SAY[işlev_değer] = öğe_BAĞ_DEĞ_SAY;
        if (읽기위치 != 끝) hata_değer("invalid method descriptor");
        읽기위치 = Önceki_öğe;
    }
    static int 상번호() { int değer = 짧은수(); return değer == 0 ? 0 : 현재읽는종 * 512 + değer; }
    static int 명상수() { return metot_sahip[kare_metot[kare_Dizin]] * 512 + 명짧(); }
    static void atlamak_öznitelik() {
        int öğe_BAĞ_DEĞ_SAY = 짧은수();
        for (int 수 = 0; 수 < öğe_BAĞ_DEĞ_SAY && !hata; 수++) { çek_sabit(상번호(), 1); 건너(bilgi()); }
    }
    static int komut_süre(int değer) {
        if (değer == 16 || değer == 18 || değer == 21 || değer == 25 || değer == 54 || değer == 58 || değer == 188) return 2;
        if (değer == 17 || değer == 19 || değer == 132 || değer >= 153 && değer <= 167
            || değer >= 178 && değer <= 184 || değer == 187 || değer == 189 || değer == 192 || değer == 193 || değer == 198 || değer == 199) return 3;
        if (değer == 185 || değer == 200) return 5;
        if (değer >= 0 && değer <= 8 || değer >= 26 && değer <= 29 || değer >= 42 && değer <= 46 || değer >= 50 && değer <= 53
            || değer >= 59 && değer <= 62 || değer >= 75 && değer <= 79 || değer >= 83 && değer <= 95
            || değer == 96 || değer == 100 || değer == 104 || değer == 108 || değer == 112 || değer == 116
            || değer == 120 || değer == 122 || değer == 124 || değer == 126 || değer == 128 || değer == 130
            || değer >= 145 && değer <= 147 || değer == 172 || değer == 176 || değer == 177 || değer == 190 || değer == 191
            || değer == 194 || değer == 195) return 1;
        return 0;
    }
    static int konum_bilgi(int 읽는자리) {
        if (!klip(읽는자리, 4)) { hata_değer("truncated bytecode operand"); return 0; }
        return dosya[읽는자리] << 24 | dosya[읽는자리 + 1] << 16 | dosya[읽는자리 + 2] << 8 | dosya[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int çalıştır, int 끝) {
        int değer = dosya[읽는자리], süre_değer = komut_süre(değer);
        if (değer == 170 || değer == 171) {
            int TABAN_konum = 읽는자리 + 1;
            while ((TABAN_konum - çalıştır) % 4 != 0) TABAN_konum++;
            if (끝 - TABAN_konum < (değer == 170 ? 12 : 8)) return 0;
            int girdi_BAĞ_DEĞ_SAY = değer == 170 ? konum_bilgi(TABAN_konum + 8) - konum_bilgi(TABAN_konum + 4) + 1 : konum_bilgi(TABAN_konum + 4);
            if (girdi_BAĞ_DEĞ_SAY < 0 || girdi_BAĞ_DEĞ_SAY > 2048) return 0;
            süre_değer = TABAN_konum - 읽는자리 + (değer == 170 ? 12 + 4 * girdi_BAĞ_DEĞ_SAY : 8 + 8 * girdi_BAĞ_DEĞ_SAY);
        }
        if (değer == 196 && 읽는자리 + 1 < 끝) {
            int Word_veri = dosya[읽는자리 + 1]; süre_değer = Word_veri == 132 ? 6 : (Word_veri == 21 || Word_veri == 25 || Word_veri == 54 || Word_veri == 58) ? 4 : 0;
        }
        return süre_değer > 0 && süre_değer <= 끝 - 읽는자리 ? süre_değer : 0;
    }
    static void çek_hedef_değer(int hedef_değer, int işlev_değer) {
        if (hedef_değer < metot_Start[işlev_değer] || hedef_değer >= metot_Bitiş[işlev_değer] || sınır_değer[hedef_değer] != işlev_değer + 1) hata_değer("invalid branch target");
    }
    static void 클래스읽기(int Sınıf_Tanım) {
        현재읽는종 = Sınıf_Tanım; 읽기위치 = Sınıf_Tanım * 16384; Boyut = 읽기위치 + Sınıf_Tanım_boyutlandırmak[Sınıf_Tanım];
        if (bilgi() != 0xcafebabe) { hata_değer("not a class file"); return; }
        int 부판 = 짧은수(), sürüm_değer = 짧은수();
        if (sürüm_değer < 45 || sürüm_değer > 52 || 부판 != 0) { hata_değer("supported class versions: 45..52, minor 0"); return; }
        int sabit_BAĞ_DEĞ_SAY = 짧은수(), TABAN_konum = Sınıf_Tanım * 512;
        if (sabit_BAĞ_DEĞ_SAY < 1 || sabit_BAĞ_DEĞ_SAY > 512) { hata_değer("constant pool limit (511)"); return; }
        for (int girdi_BAĞ_DEĞ_SAY = 1; girdi_BAĞ_DEĞ_SAY < sabit_BAĞ_DEĞ_SAY && !hata; girdi_BAĞ_DEĞ_SAY++) {
            int 수 = TABAN_konum + girdi_BAĞ_DEĞ_SAY, Tip_değer = bayt_değer(); sabit_etiket[수] = Tip_değer;
            if (Tip_değer == 1) { sabit_SANİYE_değer[수] = 짧은수(); 상가[수] = 읽기위치; 건너(sabit_SANİYE_değer[수]); }
            else if (Tip_değer == 3) 상가[수] = bilgi();
            else if (Tip_değer == 7 || Tip_değer == 8) 상가[수] = 상번호();
            else if (Tip_değer == 9 || Tip_değer == 10 || Tip_değer == 11 || Tip_değer == 12) { 상가[수] = 상번호(); sabit_SANİYE_değer[수] = 상번호(); }
            else hata_değer("unsupported constant type");
        }
        int izin_değer = 짧은수();
        if ((izin_değer & (0x2000 | 0x4000)) != 0) hata_değer("annotation/enum class unsupported");
        Sınıf_Tanım_ad[Sınıf_Tanım] = sınıf_adı_SMS(상번호());
        Sınıf_Tanım_ana[Sınıf_Tanım] = sınıf_adı_SMS(상번호());
        int arabirim_BAĞ_DEĞ_SAY = 짧은수(); if (arabirim_BAĞ_DEĞ_SAY > 16) { hata_değer("interface count limit"); return; }
        Sınıf_arabirim_BAĞ_DEĞ_SAY[Sınıf_Tanım] = arabirim_BAĞ_DEĞ_SAY;
        for (int Loop_Dizin = 0; Loop_Dizin < arabirim_BAĞ_DEĞ_SAY; Loop_Dizin++) Sınıf_arabirim[Sınıf_Tanım * 16 + Loop_Dizin] = sınıf_adı_SMS(상번호());
        int Alan_BAĞ_DEĞ_SAY = 짧은수();
        if (Alan_BAĞ_DEĞ_SAY > 512 - yuva_BAĞ_DEĞ_SAY) { hata_değer("field count limit (512)"); return; }
        for (int Loop_Dizin = 0; Loop_Dizin < Alan_BAĞ_DEĞ_SAY && !hata; Loop_Dizin++) {
            int Dosya_Dizin = yuva_BAĞ_DEĞ_SAY++; yuva_sahip[Dosya_Dizin] = Sınıf_Tanım; yuva_izinler[Dosya_Dizin] = 짧은수(); yuva_ad[Dosya_Dizin] = 상번호(); yuva_TÜR[Dosya_Dizin] = 상번호();
            çek_sabit(yuva_ad[Dosya_Dizin], 1); çek_sabit(yuva_TÜR[Dosya_Dizin], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[yuva_TÜR[Dosya_Dizin]]; int alan_KOD = tanımlayıcı_TÜR(읽기위치 + sabit_SANİYE_değer[yuva_TÜR[Dosya_Dizin]], false); 읽기위치 = 보존값;
            if ((yuva_izinler[Dosya_Dizin] & 8) == 0) yuva_konum[Dosya_Dizin] = Sınıf_yuva_BAĞ_DEĞ_SAY[Sınıf_Tanım]++;
            int öznitelik_veri = 짧은수();
            for (int iç_konum = 0; iç_konum < öznitelik_veri && !hata; iç_konum++) {
                int ad_sabit = 상번호(), geçerli_süre = bilgi();
                if (Word_SMS(ad_sabit, "ConstantValue") && geçerli_süre == 2) {
                    int veri_değer = 상번호();
                    if (alan_KOD == 1 && çek_sabit(veri_değer, 3)) yuva_veri[Dosya_Dizin] = 상가[veri_değer];
                    else if (alan_KOD == 2 && çek_sabit(veri_değer, 8)) yuva_veri[Dosya_Dizin] = sabit_SMS(상가[veri_değer]);
                } else 건너(geçerli_süre);
            }
        }
        int öğe_BAĞ_DEĞ_SAY = 짧은수();
        if (öğe_BAĞ_DEĞ_SAY > 512 - metot_BAĞ_DEĞ_SAY) { hata_değer("method count limit (512)"); return; }
        for (int Loop_Dizin = 0; Loop_Dizin < öğe_BAĞ_DEĞ_SAY && !hata; Loop_Dizin++) {
            int 수 = metot_BAĞ_DEĞ_SAY++; metot_sahip[수] = Sınıf_Tanım;
            metot_erişim[수] = 짧은수(); metot_ad_SMS[수] = 상번호(); metot_TÜR[수] = 상번호();
            çek_sabit(metot_ad_SMS[수], 1); 서술읽기(수);
            if ((metot_erişim[수] & 8) == 0) {
                if (metot_bağımsız_değişken_BAĞ_DEĞ_SAY[수] == 16) { hata_değer("too many instance method arguments"); return; }
                for (int Karşılaştırma_konum = metot_bağımsız_değişken_BAĞ_DEĞ_SAY[수]; Karşılaştırma_konum > 0; Karşılaştırma_konum--) metot_bağımsız_değişken_TÜR[수 * 16 + Karşılaştırma_konum] = metot_bağımsız_değişken_TÜR[수 * 16 + Karşılaştırma_konum - 1];
                metot_bağımsız_değişken_TÜR[수 * 16] = 2; metot_bağımsız_değişken_BAĞ_DEĞ_SAY[수]++;
            }
            if ((metot_erişim[수] & 0x100) != 0) hata_değer("user native method unsupported");
            if (Word_SMS(metot_ad_SMS[수], "<clinit>")) 종초기화[Sınıf_Tanım] = 수 + 1;
            for (int ön_kamera_değer = 0; ön_kamera_değer < 수; ön_kamera_değer++) if (metot_sahip[ön_kamera_değer] == Sınıf_Tanım && 같은말(metot_ad_SMS[ön_kamera_değer], metot_ad_SMS[수]) && 같은말(metot_TÜR[ön_kamera_değer], metot_TÜR[수])) hata_değer("duplicate method");
            int öznitelik_BAĞ_DEĞ_SAY = 짧은수();
            for (int öznitelik_değer = 0; öznitelik_değer < öznitelik_BAĞ_DEĞ_SAY && !hata; öznitelik_değer++) {
                int İsim = 상번호(), süre_değer = bilgi(), çalıştır = 읽기위치;
                if (!klip(çalıştır, süre_değer)) { hata_değer("truncated method attribute"); break; }
                if (Word_SMS(İsim, "Code")) {
                    if (metot_Start[수] != 0) hata_değer("duplicate Code attribute");
                    metot_Yığın[수] = 짧은수(); 함수지역[수] = 짧은수(); int KOD_süre = bilgi();
                    if (metot_Yığın[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metot_bağımsız_değişken_BAĞ_DEĞ_SAY[수]
                        || KOD_süre < 1 || KOD_süre > 8192) hata_değer("method memory limits exceeded");
                    metot_Start[수] = 읽기위치; 건너(KOD_süre); metot_Bitiş[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { hata_değer("exception table limit"); return; }
                    for (int iç_konum = 0; iç_konum < 잡는수; iç_konum++) {
                        int hata_Başvuru = 잡기수++; 잡기함수[hata_Başvuru] = 수;
                        잡기시작[hata_Başvuru] = metot_Start[수] + 짧은수(); 잡기끝[hata_Başvuru] = metot_Start[수] + 짧은수();
                        잡기위치[hata_Başvuru] = metot_Start[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[hata_Başvuru] = 부호값 == 0 ? 0 : sınıf_adı_SMS(부호값);
                    }
                    atlamak_öznitelik();
                    if (읽기위치 != çalıştır + süre_değer) hata_değer("Code attribute size mismatch");
                } else 건너(süre_değer);
            }
            if ((metot_erişim[수] & 0x400) != 0) continue;
            if (metot_Start[수] == 0) hata_değer("missing Code attribute");
            int yuva_girdi = metot_Start[수];
            while (yuva_girdi < metot_Bitiş[수] && !hata) {
                int süre_değer = 길이읽기(yuva_girdi, metot_Start[수], metot_Bitiş[수]);
                if (süre_değer == 0) { hata_değer("unsupported or truncated bytecode"); break; }
                sınır_değer[yuva_girdi] = 수 + 1; yuva_girdi += süre_değer;
            }
            yuva_girdi = metot_Start[수];
            while (yuva_girdi < metot_Bitiş[수] && !hata) {
                int değer = dosya[yuva_girdi];
                if (değer >= 153 && değer <= 167 || değer == 198 || değer == 199) çek_hedef_değer(yuva_girdi + (short)(dosya[yuva_girdi + 1] << 8 | dosya[yuva_girdi + 2]), 수);
                if (değer == 200) çek_hedef_değer(yuva_girdi + konum_bilgi(yuva_girdi + 1), 수);
                if (değer == 170 || değer == 171) {
                    int 읽는자리 = yuva_girdi + 1; while ((읽는자리 - metot_Start[수]) % 4 != 0) 읽는자리++;
                    çek_hedef_değer(yuva_girdi + konum_bilgi(읽는자리), 수);
                    int girdi_BAĞ_DEĞ_SAY = değer == 170 ? konum_bilgi(읽는자리 + 8) - konum_bilgi(읽는자리 + 4) + 1 : konum_bilgi(읽는자리 + 4);
                    읽는자리 += değer == 170 ? 12 : 8;
                    for (int iç_konum = 0; iç_konum < girdi_BAĞ_DEĞ_SAY; iç_konum++) çek_hedef_değer(yuva_girdi + konum_bilgi(읽는자리 + iç_konum * (değer == 170 ? 4 : 8) + (değer == 170 ? 0 : 4)), 수);
                }
                yuva_girdi += 길이읽기(yuva_girdi, metot_Start[수], metot_Bitiş[수]);
            }
            for (int iç_konum = 0; iç_konum < 잡기수; iç_konum++) if (잡기함수[iç_konum] == 수) {
                çek_hedef_değer(잡기시작[iç_konum], 수); çek_hedef_değer(잡기위치[iç_konum], 수);
                if (잡기끝[iç_konum] != metot_Bitiş[수]) çek_hedef_değer(잡기끝[iç_konum], 수);
                if (잡기시작[iç_konum] >= 잡기끝[iç_konum]) hata_değer("invalid exception range");
            }
        }
        if (!hata) atlamak_öznitelik();
        if (읽기위치 != Boyut) hata_değer("extra class file data");
    }
    static int ayırmak_Depolama(int Tip_değer, int süre_değer) { return 새기억(Tip_değer, süre_değer); }
    static boolean nesne_değer(int Başvuru, int Tip_değer) {
        if (!bilgi_teknolojisi_geçerli_nesne(Başvuru)) return false;
        if (yığın_değer[Başvuru] != Tip_değer) { hata_değer("object type mismatch"); return false; }
        return true;
    }
    static int sabit_SMS(int Dizin) {
        if (!çek_sabit(Dizin, 1)) return 0;
        if (dize_Başvuru[Dizin] != 0) return dize_Başvuru[Dizin];
        int Başvuru = ayırmak_Depolama(1, sabit_SANİYE_değer[Dizin]); if (hata) return 0;
        int 끝 = 상가[Dizin] + sabit_SANİYE_değer[Dizin], 수 = 상가[Dizin], süre_değer = 0;
        while (수 < 끝 && !hata) {
            int değer = dosya[수++];
            if (değer == 0) hata_değer("invalid modified UTF-8");
            else if (değer >= 192 && değer <= 223 && 수 < 끝) {
                int Sonraki_öğe = dosya[수++];
                if ((Sonraki_öğe & 192) != 128) hata_değer("invalid modified UTF-8");
                değer = (değer & 31) << 6 | Sonraki_öğe & 63;
                if (değer != 0 && değer < 128) hata_değer("overlong modified UTF-8");
            } else if (değer >= 224 && değer <= 239 && 수 + 1 < 끝) {
                int 가 = dosya[수++], SANİYE_işlenen = dosya[수++];
                if ((가 & 192) != 128 || (SANİYE_işlenen & 192) != 128) hata_değer("invalid modified UTF-8");
                değer = (değer & 15) << 12 | (가 & 63) << 6 | SANİYE_işlenen & 63;
                if (değer < 2048) hata_değer("overlong modified UTF-8");
            } else if (değer >= 128) hata_değer("invalid modified UTF-8");
            yığın_değer[Başvuru + 2 + süre_değer++] = değer;
        }
        yığın_değer[Başvuru + 1] = süre_değer; dize_Başvuru[Dizin] = Başvuru; return Başvuru;
    }
    static int konak_karakter(String değer) {
        int Başvuru = ayırmak_Depolama(1, değer.length()); if (hata) return 0;
        for (int 수 = 0; 수 < değer.length(); 수++) yığın_değer[Başvuru + 2 + 수] = değer.charAt(수);
        return Başvuru;
    }
    static void yazma_SMS(int Başvuru) {
        if (Başvuru == 0) { kullanıcı_alanı.Yazma("null"); return; }
        if (!nesne_değer(Başvuru, 1)) return;
        for (int 수 = 0; 수 < yığın_değer[Başvuru + 1]; 수++) kullanıcı_alanı.yazma_karakter_değer(yığın_değer[Başvuru + 2 + 수]);
    }
    static int rakam_karakter(int değer) {
        int Başvuru = ayırmak_Depolama(1, 11); if (hata) return 0;
        int süre_değer = 0;
        if (değer < 0) yığın_değer[Başvuru + 2 + süre_değer++] = '-'; else değer = -değer;
        int konum_dizini = 1000000000; boolean çalıştır = false;
        while (konum_dizini != 0) {
            int 수 = -(değer / konum_dizini);
            if (수 != 0 || çalıştır || konum_dizini == 1) { yığın_değer[Başvuru + 2 + süre_değer++] = '0' + 수; çalıştır = true; }
            değer %= konum_dizini; konum_dizini /= 10;
        }
        yığın_değer[Başvuru + 1] = süre_değer; return Başvuru;
    }
    static int 정수해독(int Başvuru) {
        if (!nesne_değer(Başvuru, 1)) return 0;
        int süre_değer = yığın_değer[Başvuru + 1], 수 = 0, değer = 0; boolean Negatif_değer = false;
        if (süre_değer > 0 && (yığın_değer[Başvuru + 2] == '-' || yığın_değer[Başvuru + 2] == '+')) { Negatif_değer = yığın_değer[Başvuru + 2] == '-'; 수++; }
        if (수 == süre_değer) hata_değer("NumberFormatException");
        for (; 수 < süre_değer && !hata; 수++) {
            int rakam_değer = yığın_değer[Başvuru + 2 + 수] - '0';
            if (rakam_değer < 0 || rakam_değer > 9 || değer < -214748364 || değer == -214748364 && rakam_değer > (Negatif_değer ? 8 : 7)) hata_değer("NumberFormatException");
            değer = değer * 10 - rakam_değer;
        }
        return Negatif_değer ? değer : -değer;
    }
    static void 넣기(int değer, int TÜR_değer) {
        if (hata) return;
        if (kare_Dizin < 0 || kare_Yığın[kare_Dizin] >= metot_Yığın[kare_metot[kare_Dizin]]) { hata_değer("operand stack overflow"); return; }
        int yuva_girdi = kare_Dizin * 128 + kare_Yığın[kare_Dizin]++; işlenen_Yığın_değer[yuva_girdi] = değer; işlenen_Yığın_TÜR[yuva_girdi] = TÜR_değer;
    }
    static int 빼기(int TÜR_değer) {
        if (hata) return 0;
        if (kare_Dizin < 0 || kare_Yığın[kare_Dizin] < 1) { hata_değer("operand stack underflow"); return 0; }
        int yuva_girdi = kare_Dizin * 128 + --kare_Yığın[kare_Dizin]; dönüş_türü = işlenen_Yığın_TÜR[yuva_girdi];
        if (TÜR_değer != 0 && dönüş_türü != TÜR_değer) hata_değer("operand type mismatch");
        if (dönüş_türü == 2) korumak_değer(işlenen_Yığın_değer[yuva_girdi]);
        return işlenen_Yığın_değer[yuva_girdi];
    }
    static void 지역읽기(int Dizin, int TÜR_değer) {
        if (Dizin >= 함수지역[kare_metot[kare_Dizin]] || Dizin < 0 || yerel_TÜR[kare_Dizin * 128 + Dizin] != TÜR_değer) { hata_değer("invalid or uninitialized local"); return; }
        넣기(yerel_değer[kare_Dizin * 128 + Dizin], TÜR_değer);
    }
    static void yazma_yerel(int Dizin, int TÜR_değer) {
        if (Dizin >= 함수지역[kare_metot[kare_Dizin]] || Dizin < 0) { hata_değer("local index out of range"); return; }
        int değer = 빼기(TÜR_değer); yerel_değer[kare_Dizin * 128 + Dizin] = değer; yerel_TÜR[kare_Dizin * 128 + Dizin] = TÜR_değer;
    }
    static int 명바() {
        int konum = kare_konum[kare_Dizin];
        if (konum < metot_Start[kare_metot[kare_Dizin]] || konum >= metot_Bitiş[kare_metot[kare_Dizin]]) { hata_değer("instruction pointer out of range"); return 0; }
        kare_konum[kare_Dizin]++; return dosya[konum];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void taşımak_değer_83b651b8(int konum) {
        int işlev_değer = kare_metot[kare_Dizin];
        if (konum < metot_Start[işlev_değer] || konum >= metot_Bitiş[işlev_değer] || sınır_değer[konum] != işlev_değer + 1) hata_değer("invalid branch target");
        else kare_konum[kare_Dizin] = konum;
    }
    static void 호출(int işlev_değer) {
        if (kare_Dizin % 32 == 31) { hata_değer("call stack limit (32)"); return; }
        int Sonraki_öğe = kare_Dizin + 1;
        for (int 수 = 0; 수 < 128; 수++) yerel_TÜR[Sonraki_öğe * 128 + 수] = 0;
        for (int 수 = metot_bağımsız_değişken_BAĞ_DEĞ_SAY[işlev_değer] - 1; 수 >= 0; 수--) {
            yerel_değer[Sonraki_öğe * 128 + 수] = 빼기(metot_bağımsız_değişken_TÜR[işlev_değer * 16 + 수]); yerel_TÜR[Sonraki_öğe * 128 + 수] = metot_bağımsız_değişken_TÜR[işlev_değer * 16 + 수];
        }
        if (hata) return;
        kare_Dizin = Sonraki_öğe; 틀초기화[kare_Dizin] = 0; kare_metot[kare_Dizin] = işlev_değer; kare_konum[kare_Dizin] = metot_Start[işlev_değer]; kare_Yığın[kare_Dizin] = 0;
    }
    static void İade_KR(int TÜR_değer) {
        if (TÜR_değer != metot_İade[kare_metot[kare_Dizin]]) { hata_değer("return type mismatch"); return; }
        int değer = TÜR_değer == 0 ? 0 : 빼기(TÜR_değer);
        if (틀초기화[kare_Dizin] != 0) Sınıf_Tanım_Durum[틀초기화[kare_Dizin] - 1] = 2;
        if (kare_kilit[kare_Dizin] != 0) { sürüm_kilit(kare_kilit[kare_Dizin]); kare_kilit[kare_Dizin] = 0; }
        kare_Dizin--; if (kare_Dizin >= geçerli_yazışma * 32 && TÜR_değer != 0) 넣기(değer, TÜR_değer);
    }
    static int[] akış_dosya_adı = new int[64];
    static void Dosya_akış_Ara(int sahip_değer, int İsim, int biçim_değer, int komut) {
        boolean metinÇıktısı = Word_SMS(sahip_değer, "java/io/FileOutputStream");
        int Tip_değer = metinÇıktısı ? 6 : 5;
        if (komut == 183 && Word_SMS(İsim, "<init>")) {
            boolean 이어 = false;
            if (metinÇıktısı && Word_SMS(biçim_değer, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(biçim_değer, "(Ljava/lang/String;)V")) { hata_değer("unsupported file stream constructor"); return; }
            int Dosya_girdi_ad = 빼기(2), akış_değer = 빼기(2);
            if (!nesne_değer(Dosya_girdi_ad, 1) || !nesne_değer(akış_değer, Tip_değer) || hata) return;
            if (yığın_değer[akış_değer + 3] != 0) { hata_değer("file stream already initialized"); return; }
            int süre_değer = yığın_değer[Dosya_girdi_ad + 1];
            if (süre_değer < 1 || süre_değer > 63) { hata_değer("invalid file name length"); return; }
            for (int yuva_girdi = 0; yuva_girdi < süre_değer; yuva_girdi++) {
                int değer = yığın_değer[Dosya_girdi_ad + 2 + yuva_girdi];
                if (değer < 1) { hata_değer("invalid file stream path"); return; }
                akış_dosya_adı[yuva_girdi] = değer;
            }
            akış_dosya_adı[süre_değer] = 0;
            int tanımlayıcı_girdi = kullanıcı_alanı.açık_Dosya_tanımlayıcı(akış_dosya_adı, metinÇıktısı ? (이어 ? 1089 : 577) : 0);
            if (tanımlayıcı_girdi < 0) { hata_değer("FileNotFoundException: file open failed"); return; }
            yığın_değer[akış_değer + 2] = tanımlayıcı_girdi; yığın_değer[akış_değer + 3] = 1;
            return;
        }
        if (komut != 182) { hata_değer("invalid file stream invocation"); return; }
        if ((metinÇıktısı && Word_SMS(İsim, "write") || !metinÇıktısı && Word_SMS(İsim, "read"))
            && (Word_SMS(biçim_değer, metinÇıktısı ? "([B)V" : "([B)I") || Word_SMS(biçim_değer, metinÇıktısı ? "([BII)V" : "([BII)I"))) {
            boolean klip_değer = Word_SMS(biçim_değer, metinÇıktısı ? "([BII)V" : "([BII)I");
            int girdi_BAĞ_DEĞ_SAY = klip_değer ? 빼기(1) : 0, 시작점 = klip_değer ? 빼기(1) : 0, veri_DİZİ = 빼기(2), nesne_Başvuru = 빼기(2);
            if (!nesne_değer(veri_DİZİ, 20) || !nesne_değer(nesne_Başvuru, Tip_değer)) return;
            if (!klip_değer) girdi_BAĞ_DEĞ_SAY = yığın_değer[veri_DİZİ + 1];
            if (시작점 < 0 || girdi_BAĞ_DEĞ_SAY < 0 || 시작점 > yığın_değer[veri_DİZİ + 1] - girdi_BAĞ_DEĞ_SAY) { 예외던짐(6, "file buffer bounds"); return; }
            if (yığın_değer[nesne_Başvuru + 3] == 0 || yığın_değer[nesne_Başvuru + 2] < 0) { hata_değer("IOException: stream closed"); return; }
            int Bitenler_BAĞ_DEĞ_SAY = 0;
            while (Bitenler_BAĞ_DEĞ_SAY < girdi_BAĞ_DEĞ_SAY && !hata) {
                int 반환값 = metinÇıktısı ? kullanıcı_alanı.파일한바이트쓰기(yığın_değer[nesne_Başvuru + 2], yığın_değer[veri_DİZİ + 2 + 시작점 + Bitenler_BAĞ_DEĞ_SAY]) : kullanıcı_alanı.파일한바이트읽기(yığın_değer[nesne_Başvuru + 2]);
                if (반환값 < 0) { hata_değer(metinÇıktısı ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!metinÇıktısı && 반환값 == 256) break;
                if (!metinÇıktısı) yığın_değer[veri_DİZİ + 2 + 시작점 + Bitenler_BAĞ_DEĞ_SAY] = (byte)반환값;
                Bitenler_BAĞ_DEĞ_SAY++;
            }
            if (!metinÇıktısı) 넣기(girdi_BAĞ_DEĞ_SAY != 0 && Bitenler_BAĞ_DEĞ_SAY == 0 ? -1 : Bitenler_BAĞ_DEĞ_SAY, 1);
            return;
        }
        if (metinÇıktısı && Word_SMS(İsim, "flush") && Word_SMS(biçim_değer, "()V")) { int nesne_Başvuru = 빼기(2); if (nesne_değer(nesne_Başvuru, Tip_değer) && yığın_değer[nesne_Başvuru + 2] < 0) hata_değer("IOException: stream closed"); return; }
        int Eylem = -1, değer = 0;
        if (Word_SMS(İsim, "close") && Word_SMS(biçim_değer, "()V")) Eylem = 0;
        if (!metinÇıktısı && Word_SMS(İsim, "read") && Word_SMS(biçim_değer, "()I")) Eylem = 1;
        if (metinÇıktısı && Word_SMS(İsim, "write") && Word_SMS(biçim_değer, "(I)V")) { Eylem = 2; değer = 빼기(1); }
        if (Eylem < 0) { hata_değer("unsupported file stream method"); return; }
        int akış_değer = 빼기(2);
        if (!nesne_değer(akış_değer, Tip_değer) || hata) return;
        if (yığın_değer[akış_değer + 3] == 0) { hata_değer("uninitialized file stream"); return; }
        int tanımlayıcı_girdi = yığın_değer[akış_değer + 2];
        if (Eylem == 0) {
            if (tanımlayıcı_girdi >= 0 && kullanıcı_alanı.Kapat_Dosya_tanımlayıcı(tanımlayıcı_girdi) < 0) hata_değer("IOException: close failed");
            yığın_değer[akış_değer + 2] = -1; return;
        }
        if (tanımlayıcı_girdi < 0) { hata_değer("IOException: stream closed"); return; }
        if (Eylem == 1) {
            int sonuç = kullanıcı_alanı.파일한바이트읽기(tanımlayıcı_girdi);
            if (sonuç < -1) hata_değer("IOException: read failed"); else 넣기(sonuç == 256 ? -1 : sonuç, 1);
        } else if (kullanıcı_alanı.파일한바이트쓰기(tanımlayıcı_girdi, değer) != 1) hata_değer("IOException: write failed");
    }
    static void Ara_metot(int Dizin, int komut) {
        if (Dizin <= 0 || Dizin >= sabit_etiket.length || (sabit_etiket[Dizin] != 10 && sabit_etiket[Dizin] != 11)) { hata_değer("invalid method reference"); return; }
        int sahip_değer = sınıf_adı_SMS(상가[Dizin]), İsim = Başvuru_ad(sabit_SANİYE_değer[Dizin]), biçim_değer = başvuru_türü(sabit_SANİYE_değer[Dizin]);
        if (hata) return;
        if (기본호출(sahip_değer, İsim, biçim_değer, komut)) return;
        if (Word_SMS(sahip_değer, "java/io/FileInputStream") || Word_SMS(sahip_değer, "java/io/FileOutputStream")) {
            Dosya_akış_Ara(sahip_değer, İsim, biçim_değer, komut); return;
        }
        if (komut == 184 && Word_SMS(sahip_değer, "java/lang/Integer") && Word_SMS(İsim, "parseInt") && Word_SMS(biçim_değer, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (komut == 182 && Word_SMS(sahip_değer, "java/io/PrintStream") && (Word_SMS(İsim, "println") || Word_SMS(İsim, "print"))) {
            int TÜR_değer = 0, değer = 0;
            if (Word_SMS(biçim_değer, "(I)V")) { TÜR_değer = 1; değer = 빼기(1); }
            else if (Word_SMS(biçim_değer, "(Z)V")) { TÜR_değer = 2; değer = 빼기(1); }
            else if (Word_SMS(biçim_değer, "(C)V")) { TÜR_değer = 3; değer = 빼기(1); }
            else if (Word_SMS(biçim_değer, "(Ljava/lang/String;)V")) { TÜR_değer = 4; değer = 빼기(2); }
            else if (!Word_SMS(biçim_değer, "()V") || !Word_SMS(İsim, "println")) hata_değer("unsupported print descriptor");
            if (빼기(2) != -1) hata_değer("invalid PrintStream receiver");
            if (hata) return;
            if (TÜR_değer == 1) 자바도구.수쓰기(değer);
            if (TÜR_değer == 2) kullanıcı_alanı.Yazma(değer == 0 ? "false" : "true");
            if (TÜR_değer == 3) kullanıcı_alanı.yazma_karakter_değer(değer & 65535);
            if (TÜR_değer == 4) yazma_SMS(değer);
            if (Word_SMS(İsim, "println")) kullanıcı_alanı.yazma_karakter_değer(10);
            return;
        }
        if (komut == 182 && Word_SMS(sahip_değer, "java/lang/String")) {
            if (Word_SMS(İsim, "length") && Word_SMS(biçim_değer, "()I")) {
                int Başvuru = 빼기(2); if (nesne_değer(Başvuru, 1)) 넣기(yığın_değer[Başvuru + 1], 1); return;
            }
            if (Word_SMS(İsim, "charAt") && Word_SMS(biçim_değer, "(I)C")) {
                int alt_simge_değer = 빼기(1), Başvuru = 빼기(2);
                if (nesne_değer(Başvuru, 1)) {
                    if (alt_simge_değer < 0 || alt_simge_değer >= yığın_değer[Başvuru + 1]) hata_değer("StringIndexOutOfBoundsException"); else 넣기(yığın_değer[Başvuru + 2 + alt_simge_değer], 1);
                }
                return;
            }
        }
        if (Word_SMS(sahip_değer, "java/lang/StringBuilder")) {
            if (komut == 183 && Word_SMS(İsim, "<init>") && Word_SMS(biçim_değer, "()V")) { nesne_değer(빼기(2), 4); return; }
            if (komut == 182 && Word_SMS(İsim, "toString") && Word_SMS(biçim_değer, "()Ljava/lang/String;")) {
                int Başvuru = 빼기(2); if (nesne_değer(Başvuru, 4)) 넣기(yığın_değer[Başvuru + 2] == 0 ? konak_karakter("") : yığın_değer[Başvuru + 2], 2); return;
            }
            if (komut == 182 && Word_SMS(İsim, "append")) {
                int metin = 0;
                if (Word_SMS(biçim_değer, "(I)Ljava/lang/StringBuilder;")) metin = rakam_karakter(빼기(1));
                else if (Word_SMS(biçim_değer, "(Z)Ljava/lang/StringBuilder;")) metin = konak_karakter(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(biçim_değer, "(C)Ljava/lang/StringBuilder;")) {
                    int değer = 빼기(1); metin = ayırmak_Depolama(1, 1); if (!hata) yığın_değer[metin + 2] = değer & 65535;
                }
                else if (Word_SMS(biçim_değer, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { metin = 빼기(2); if (metin == 0) metin = konak_karakter("null"); }
                else { hata_değer("unsupported StringBuilder append"); return; }
                int Başvuru = 빼기(2); if (!nesne_değer(Başvuru, 4) || !nesne_değer(metin, 1)) return;
                int ön_kamera_değer = yığın_değer[Başvuru + 2], ön_kamera_değer_süre = ön_kamera_değer == 0 ? 0 : yığın_değer[ön_kamera_değer + 1], BACK_değer_süre = yığın_değer[metin + 1];
                int 새글 = ayırmak_Depolama(1, ön_kamera_değer_süre + BACK_değer_süre); if (hata) return;
                for (int 수 = 0; 수 < ön_kamera_değer_süre; 수++) yığın_değer[새글 + 2 + 수] = yığın_değer[ön_kamera_değer + 2 + 수];
                for (int 수 = 0; 수 < BACK_değer_süre; 수++) yığın_değer[새글 + 2 + ön_kamera_değer_süre + 수] = yığın_değer[metin + 2 + 수];
                yığın_değer[Başvuru + 2] = 새글; 넣기(Başvuru, 2); return;
            }
        }
        int Sınıf_Tanım = BUL_Sınıf_Tanım(sahip_değer); if (Sınıf_Tanım < 0 || hata) return;
        int Dosya_Dizin = BUL_metot(Sınıf_Tanım, İsim, biçim_değer);
        if (Dosya_Dizin < 0) {
            for (int kod_noktası = Sınıf_Tanım, girdi_BAĞ_DEĞ_SAY = 0; kod_noktası >= 0 && girdi_BAĞ_DEĞ_SAY < 16; girdi_BAĞ_DEĞ_SAY++, kod_noktası = ana_Sınıf(kod_noktası))
                if (Word_SMS(Sınıf_Tanım_ana[kod_noktası], "java/lang/Thread")) { 가닥호출(İsim, biçim_değer, komut); return; }
            hata_değer("NoSuchMethodError"); return;
        }
        if (((metot_erişim[Dosya_Dizin] & 8) != 0) != (komut == 184)) { hata_değer("method static/instance mismatch"); return; }
        if (komut == 184) { if (!başlat(metot_sahip[Dosya_Dizin], 틀명령[kare_Dizin])) return; }
        else {
            int 읽는자리 = kare_Yığın[kare_Dizin] - metot_bağımsız_değişken_BAĞ_DEĞ_SAY[Dosya_Dizin];
            if (읽는자리 < 0 || işlenen_Yığın_TÜR[kare_Dizin * 128 + 읽는자리] != 2) { hata_değer("invalid method receiver"); return; }
            int nesne_Başvuru = işlenen_Yığın_değer[kare_Dizin * 128 + 읽는자리];
            if (!bilgi_teknolojisi_geçerli_nesne(nesne_Başvuru)) return;
            if (yığın_değer[nesne_Başvuru] < 32 || !종포함(yığın_değer[nesne_Başvuru] - 32, sahip_değer)) { hata_değer("method receiver type mismatch"); return; }
            if (komut != 183) Dosya_Dizin = BUL_metot(yığın_değer[nesne_Başvuru] - 32, İsim, biçim_değer);
        }
        if (Dosya_Dizin < 0 || (metot_erişim[Dosya_Dizin] & 0x400) != 0) { hata_değer("AbstractMethodError"); return; }
        int kilit_Başvuru = 0;
        if ((metot_erişim[Dosya_Dizin] & 32) != 0) {
            if (komut == 184) { int kod_noktası = metot_sahip[Dosya_Dizin]; if (Sınıf_kilit[kod_noktası] == 0) Sınıf_kilit[kod_noktası] = ayırmak_Depolama(8, 0); kilit_Başvuru = Sınıf_kilit[kod_noktası]; }
            else kilit_Başvuru = işlenen_Yığın_değer[kare_Dizin * 128 + kare_Yığın[kare_Dizin] - metot_bağımsız_değişken_BAĞ_DEĞ_SAY[Dosya_Dizin]];
            if (!잠금얻기(kilit_Başvuru)) { if (!hata) kare_konum[kare_Dizin] = 틀명령[kare_Dizin]; return; }
        }
        호출(Dosya_Dizin); if (!hata) kare_kilit[kare_Dizin] = kilit_Başvuru;
    }
    static boolean 배열저장가능(int DİZİ_Başvuru, int veri_değer) {
        if (veri_değer == 0 || dizi_öğesi[DİZİ_Başvuru] == 0) return true;
        boolean 성공여부 = dizi_öğesi[DİZİ_Başvuru] == -1 ? (veri_değer > 0 && veri_değer < yığın_Bitiş_konum && yığın_değer[veri_değer] == 1) : 맞는객체(veri_değer, dizi_öğesi[DİZİ_Başvuru]);
        if (!성공여부 && !hata) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int DİZİ_yuva(int Başvuru, int alt_simge_değer, int TÜR_değer) {
        if (!nesne_değer(Başvuru, TÜR_değer)) return 0;
        if (alt_simge_değer < 0 || alt_simge_değer >= yığın_değer[Başvuru + 1]) { hata_değer("ArrayIndexOutOfBoundsException"); return 0; }
        return Başvuru + 2 + alt_simge_değer;
    }
    static void yürütmek_komut() {
        int 남음 = 500000, parça_değer = 100;
        while (true) {
            if (hata) { if (던진객체 != 0) sap_özel_durum(); if (hata || kare_Dizin < geçerli_yazışma * 32) break; }
            if (kare_Dizin < geçerli_yazışma * 32 || değişiklik_isteği || --parça_değer == 0) { if (!geçiş_yazışma()) break; parça_değer = 100; }
            if (kare_Dizin == 0 && Sınıf_Tanım_Durum[girdi_Sınıf_Tanım] != 2 && !başlat(girdi_Sınıf_Tanım, kare_konum[kare_Dizin])) continue;
            if (kare_Dizin == geçerli_yazışma * 32 && geçerli_yazışma != 0 && (metot_erişim[kare_metot[kare_Dizin]] & 32) != 0 && kare_kilit[kare_Dizin] == 0) {
                int nesne_Başvuru = yazışma_hedef[geçerli_yazışma]; if (!잠금얻기(nesne_Başvuru)) { if (hata) break; continue; } kare_kilit[kare_Dizin] = nesne_Başvuru;
            }
            잠시수 = 0;
            if (--남음 == 0) { hata_değer("instruction limit (500000)"); break; }
            int çalıştır = kare_konum[kare_Dizin]; 틀명령[kare_Dizin] = çalıştır; int değer = 명바();
            if (hata) break;
            if (değer == 0) continue;
            if (değer == 1) { 넣기(0, 2); continue; }
            if (değer >= 2 && değer <= 8) { 넣기(değer - 3, 1); continue; }
            if (değer == 16) { 넣기((byte)명바(), 1); continue; }
            if (değer == 17) { 넣기((short)명짧(), 1); continue; }
            if (değer == 18 || değer == 19) {
                int 수 = metot_sahip[kare_metot[kare_Dizin]] * 512 + (değer == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= sabit_etiket.length) hata_değer("invalid ldc constant");
                else if (sabit_etiket[수] == 3) 넣기(상가[수], 1);
                else if (sabit_etiket[수] == 8) 넣기(sabit_SMS(상가[수]), 2);
                else hata_değer("unsupported ldc constant");
                continue;
            }
            if (değer == 21 || değer == 25) { 지역읽기(명바(), değer == 21 ? 1 : 2); continue; }
            if (değer >= 26 && değer <= 29) { 지역읽기(değer - 26, 1); continue; }
            if (değer >= 42 && değer <= 45) { 지역읽기(değer - 42, 2); continue; }
            if (değer == 54 || değer == 58) { yazma_yerel(명바(), değer == 54 ? 1 : 2); continue; }
            if (değer >= 59 && değer <= 62) { yazma_yerel(değer - 59, 1); continue; }
            if (değer >= 75 && değer <= 78) { yazma_yerel(değer - 75, 2); continue; }
            if (değer == 46 || değer >= 50 && değer <= 53) {
                int girdi_konum = 빼기(1), nesne_Başvuru = 빼기(2), alan_KOD = değer == 46 ? 2 : değer == 50 ? 3 : değer == 51 ? 20 : değer == 52 ? 22 : 23;
                if (değer == 51 && nesne_Başvuru > 0 && nesne_Başvuru < yığın_Bitiş_konum && yığın_değer[nesne_Başvuru] == 21) alan_KOD = 21;
                int 읽는자리 = DİZİ_yuva(nesne_Başvuru, girdi_konum, alan_KOD); if (!hata) 넣기(yığın_değer[읽는자리], değer == 50 ? 2 : 1); continue;
            }
            if (değer == 79 || değer >= 83 && değer <= 86) {
                int girdi_Başvuru = 빼기(değer == 83 ? 2 : 1), girdi_konum = 빼기(1), nesne_Başvuru = 빼기(2), alan_KOD = değer == 79 ? 2 : değer == 83 ? 3 : değer == 84 ? 20 : değer == 85 ? 22 : 23;
                if (değer == 84 && nesne_Başvuru > 0 && nesne_Başvuru < yığın_Bitiş_konum && yığın_değer[nesne_Başvuru] == 21) alan_KOD = 21;
                int 읽는자리 = DİZİ_yuva(nesne_Başvuru, girdi_konum, alan_KOD);
                if (!hata && alan_KOD == 3 && !배열저장가능(nesne_Başvuru, girdi_Başvuru)) continue;
                if (!hata) yığın_değer[읽는자리] = alan_KOD == 20 ? (byte)girdi_Başvuru : alan_KOD == 21 ? girdi_Başvuru & 1 : alan_KOD == 22 ? (char)girdi_Başvuru : alan_KOD == 23 ? (short)girdi_Başvuru : girdi_Başvuru;
                continue;
            }
            if (değer >= 87 && değer <= 95) { 스택명령(değer); continue; }
            if (değer == 96 || değer == 100 || değer == 104 || değer == 108 || değer == 112 || değer == 120
                || değer == 122 || değer == 124 || değer == 126 || değer == 128 || değer == 130) {
                int SANİYE_işlenen = 빼기(1), 가 = 빼기(1), sonuç = 0;
                if ((değer == 108 || değer == 112) && SANİYE_işlenen == 0) { hata_değer("ArithmeticException: / by zero"); continue; }
                if (değer == 96) sonuç = 가 + SANİYE_işlenen;
                if (değer == 100) sonuç = 가 - SANİYE_işlenen;
                if (değer == 104) sonuç = 가 * SANİYE_işlenen;
                if (değer == 108) sonuç = 가 / SANİYE_işlenen;
                if (değer == 112) sonuç = 가 % SANİYE_işlenen;
                if (değer == 120) sonuç = 가 << SANİYE_işlenen;
                if (değer == 122) sonuç = 가 >> SANİYE_işlenen;
                if (değer == 124) sonuç = 가 >>> SANİYE_işlenen;
                if (değer == 126) sonuç = 가 & SANİYE_işlenen;
                if (değer == 128) sonuç = 가 | SANİYE_işlenen;
                if (değer == 130) sonuç = 가 ^ SANİYE_işlenen;
                넣기(sonuç, 1); continue;
            }
            if (değer == 116) { 넣기(-빼기(1), 1); continue; }
            if (değer == 132) {
                int yerel_Scope = 명바(), artış_adım = (byte)명바(); 지역읽기(yerel_Scope, 1); 넣기(빼기(1) + artış_adım, 1); yazma_yerel(yerel_Scope, 1); continue;
            }
            if (değer >= 145 && değer <= 147) {
                int 수 = 빼기(1); 넣기(değer == 145 ? (byte)수 : değer == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (değer >= 153 && değer <= 167 || değer == 198 || değer == 199) {
                int hedef_değer = çalıştır + (short)명짧(); boolean 갈까 = değer == 167;
                if (değer >= 153 && değer <= 158) {
                    int 수 = 빼기(1); 갈까 = değer == 153 ? 수 == 0 : değer == 154 ? 수 != 0 : değer == 155 ? 수 < 0 : değer == 156 ? 수 >= 0 : değer == 157 ? 수 > 0 : 수 <= 0;
                } else if (değer >= 159 && değer <= 166) {
                    int SANİYE_işlenen = 빼기(değer >= 165 ? 2 : 1), 가 = 빼기(değer >= 165 ? 2 : 1);
                    갈까 = değer == 159 || değer == 165 ? 가 == SANİYE_işlenen : değer == 160 || değer == 166 ? 가 != SANİYE_işlenen : değer == 161 ? 가 < SANİYE_işlenen : değer == 162 ? 가 >= SANİYE_işlenen : değer == 163 ? 가 > SANİYE_işlenen : 가 <= SANİYE_işlenen;
                } else if (değer == 198 || değer == 199) { int 수 = 빼기(2); 갈까 = değer == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) taşımak_değer_83b651b8(hedef_değer); continue;
            }
            if (değer == 172 || değer == 176 || değer == 177) { İade_KR(değer == 172 ? 1 : değer == 176 ? 2 : 0); continue; }
            if (değer >= 178 && değer <= 181) { 필드호출(명상수(), değer, çalıştır); continue; }
            if (değer >= 182 && değer <= 185) {
                int 부호값 = 명상수();
                if (değer == 185) { int toplam_BAĞ_DEĞ_SAY = 명바(); if (toplam_BAĞ_DEĞ_SAY == 0 || 명바() != 0) { hata_değer("invalid invokeinterface operands"); continue; } }
                Ara_metot(부호값, değer); continue;
            }
            if (değer == 187) { 새객체(sınıf_adı_SMS(명상수()), çalıştır); continue; }
            if (değer == 188 || değer == 189) {
                int alan_KOD = 3, bileşen = 0;
                if (değer == 188) { int 임시값 = 명바(); alan_KOD = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else bileşen = sınıf_adı_SMS(명상수());
                if (alan_KOD == 0) { hata_değer("unsupported primitive array type"); continue; }
                int geçerli_süre = 빼기(1), nesne_Başvuru = ayırmak_Depolama(alan_KOD, geçerli_süre); if (!hata) dizi_öğesi[nesne_Başvuru] = bileşen; 넣기(nesne_Başvuru, 2); continue;
            }
            if (değer == 190) {
                int nesne_Başvuru = 빼기(2);
                if (bilgi_teknolojisi_geçerli_nesne(nesne_Başvuru)) { int Karşılaştırma_konum = yığın_değer[nesne_Başvuru]; if (Karşılaştırma_konum != 2 && Karşılaştırma_konum != 3 && (Karşılaştırma_konum < 20 || Karşılaştırma_konum > 23)) hata_değer("not an array"); else 넣기(yığın_değer[nesne_Başvuru + 1], 1); }
                continue;
            }
            if (değer == 191) {
                int nesne_Başvuru = 빼기(2); if (bilgi_teknolojisi_geçerli_nesne(nesne_Başvuru)) { if (yığın_değer[nesne_Başvuru] != 9) hata_değer("athrow requires supported Throwable"); else { 던진객체 = nesne_Başvuru; hata = true; } }
                continue;
            }
            if (değer == 192 || değer == 193) {
                int ad_sabit = sınıf_adı_SMS(명상수()), nesne_Başvuru = 빼기(2); boolean KAÇINCI = 맞는객체(nesne_Başvuru, ad_sabit);
                if (değer == 193) 넣기(nesne_Başvuru != 0 && KAÇINCI ? 1 : 0, 1);
                else { if (!KAÇINCI && !hata) hata_değer("ClassCastException"); 넣기(nesne_Başvuru, 2); }
                continue;
            }
            if (değer == 170 || değer == 171) {
                int 읽는자리 = çalıştır + 1, Dosya_Dizin = kare_metot[kare_Dizin], tuş_Başvuru = 빼기(1);
                while ((읽는자리 - metot_Start[Dosya_Dizin]) % 4 != 0) 읽는자리++;
                int hedef_ADRES = konum_bilgi(읽는자리);
                if (değer == 170) { int 낮은값 = konum_bilgi(읽는자리 + 4), 높은값 = konum_bilgi(읽는자리 + 8); if (tuş_Başvuru >= 낮은값 && tuş_Başvuru <= 높은값) hedef_ADRES = konum_bilgi(읽는자리 + 12 + (tuş_Başvuru - 낮은값) * 4); }
                else { int toplam_BAĞ_DEĞ_SAY = konum_bilgi(읽는자리 + 4); for (int Loop_Dizin = 0; Loop_Dizin < toplam_BAĞ_DEĞ_SAY; Loop_Dizin++) if (konum_bilgi(읽는자리 + 8 + Loop_Dizin * 8) == tuş_Başvuru) hedef_ADRES = konum_bilgi(읽는자리 + 12 + Loop_Dizin * 8); }
                taşımak_değer_83b651b8(çalıştır + hedef_ADRES); continue;
            }
            if (değer == 200) { taşımak_değer_83b651b8(çalıştır + konum_bilgi(çalıştır + 1)); continue; }
            if (değer == 194 || değer == 195) {
                int nesne_Başvuru = 빼기(2);
                if (değer == 195) sürüm_kilit(nesne_Başvuru);
                else if (!잠금얻기(nesne_Başvuru) && !hata) { 넣기(nesne_Başvuru, 2); kare_konum[kare_Dizin] = çalıştır; }
                continue;
            }
            if (değer == 196) {
                int komut_KOD = 명바(), girdi_konum = 명짧();
                if (komut_KOD == 21 || komut_KOD == 25) 지역읽기(girdi_konum, komut_KOD == 21 ? 1 : 2);
                else if (komut_KOD == 54 || komut_KOD == 58) yazma_yerel(girdi_konum, komut_KOD == 54 ? 1 : 2);
                else if (komut_KOD == 132) { int DELTA_değer = (short)명짧(); 지역읽기(girdi_konum, 1); 넣기(빼기(1) + DELTA_değer, 1); yazma_yerel(girdi_konum, 1); }
                else hata_değer("unsupported wide opcode");
                continue;
            }
            hata_değer("unsupported bytecode");
        }
    }
    static int BUL_Sınıf_Tanım(int İsim) {
        for (int Loop_Dizin = 0; Loop_Dizin < Sınıf_Tanım_BAĞ_DEĞ_SAY; Loop_Dizin++) if (Sınıf_Tanım_ad[Loop_Dizin] != 0 && 같은말(Sınıf_Tanım_ad[Loop_Dizin], İsim)) return Loop_Dizin;
        return yük_Sınıf_Tanım(sabit_SMS(İsim));
    }
    static int yük_Sınıf_Tanım(int ad_dize) {
        if (!nesne_değer(ad_dize, 1)) return -1;
        int süre_değer = yığın_değer[ad_dize + 1];
        if (süre_değer < 1 || süre_değer > 505 || Sınıf_Tanım_BAĞ_DEĞ_SAY == 16) { hata_değer("class name/count limit"); return -1; }
        for (int Loop_Dizin = 0; Loop_Dizin < süre_değer; Loop_Dizin++) { int kod_noktası = yığın_değer[ad_dize + 2 + Loop_Dizin]; dosya_adı_SMS[Loop_Dizin] = kod_noktası == '/' ? '.' : kod_noktası; }
        dosya_adı_SMS[süre_değer] = '.'; dosya_adı_SMS[süre_değer + 1] = 'c'; dosya_adı_SMS[süre_değer + 2] = 'l'; dosya_adı_SMS[süre_değer + 3] = 'a'; dosya_adı_SMS[süre_değer + 4] = 's'; dosya_adı_SMS[süre_değer + 5] = 's'; dosya_adı_SMS[süre_değer + 6] = 0;
        int Boyut = kullanıcı_alanı.파일읽기(dosya_adı_SMS, geçici_dosya);
        if (Boyut < 0) { hata_değer("ClassNotFoundException"); return -1; }
        int Sınıf_Tanım = Sınıf_Tanım_BAĞ_DEĞ_SAY++; Sınıf_Tanım_boyutlandırmak[Sınıf_Tanım] = Boyut;
        for (int Loop_Dizin = 0; Loop_Dizin < Boyut; Loop_Dizin++) dosya[Sınıf_Tanım * 16384 + Loop_Dizin] = geçici_dosya[Loop_Dizin];
        클래스읽기(Sınıf_Tanım); if (hata) return -1;
        int fiili_veri = sabit_SMS(Sınıf_Tanım_ad[Sınıf_Tanım]);
        if (!metinler_eşit(fiili_veri, ad_dize, true)) { hata_değer("class name does not match file"); return -1; }
        int ana_değer = Sınıf_Tanım_ana[Sınıf_Tanım];
        if (ana_değer != 0 && !Word_SMS(ana_değer, "java/lang/Object") && !Word_SMS(ana_değer, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 yeniden_denemek_değer 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = BUL_Sınıf_Tanım(ana_değer);
            if (hata || 위 < 0) return -1;
            int 읽는자리 = 위, aşama_BAĞ_DEĞ_SAY = 0;
            while (읽는자리 >= 0 && aşama_BAĞ_DEĞ_SAY++ < 16) {
                if (읽는자리 == Sınıf_Tanım) { hata_değer("cyclic inheritance"); return -1; }
                읽는자리 = ana_Sınıf(읽는자리);
            }
            int 시작변위 = Sınıf_yuva_BAĞ_DEĞ_SAY[위];
            for (int Dosya_Dizin = 0; Dosya_Dizin < yuva_BAĞ_DEĞ_SAY; Dosya_Dizin++) if (yuva_sahip[Dosya_Dizin] == Sınıf_Tanım && (yuva_izinler[Dosya_Dizin] & 8) == 0) yuva_konum[Dosya_Dizin] += 시작변위;
            Sınıf_yuva_BAĞ_DEĞ_SAY[Sınıf_Tanım] += 시작변위;
        }
        return Sınıf_Tanım;
    }
    static int ana_Sınıf(int Sınıf_Tanım) {
        int İsim = Sınıf_Tanım_ana[Sınıf_Tanım];
        for (int Loop_Dizin = 0; Loop_Dizin < Sınıf_Tanım_BAĞ_DEĞ_SAY; Loop_Dizin++) if (İsim != 0 && Sınıf_Tanım_ad[Loop_Dizin] != 0 && 같은말(Sınıf_Tanım_ad[Loop_Dizin], İsim)) return Loop_Dizin;
        return -1;
    }
    static int BUL_metot(int Sınıf_Tanım, int İsim, int biçim_değer) {
        for (int 깊이 = 0; Sınıf_Tanım >= 0 && 깊이 < 16; 깊이++, Sınıf_Tanım = ana_Sınıf(Sınıf_Tanım)) {
            for (int Loop_Dizin = 0; Loop_Dizin < metot_BAĞ_DEĞ_SAY; Loop_Dizin++) if (metot_sahip[Loop_Dizin] == Sınıf_Tanım && 같은말(metot_ad_SMS[Loop_Dizin], İsim) && 같은말(metot_TÜR[Loop_Dizin], biçim_değer)) return Loop_Dizin;
        }
        return -1;
    }
    static int ad_metot(int Sınıf_Tanım, String İsim, String biçim_değer) {
        for (int 깊이 = 0; Sınıf_Tanım >= 0 && 깊이 < 16; 깊이++, Sınıf_Tanım = ana_Sınıf(Sınıf_Tanım))
            for (int Loop_Dizin = 0; Loop_Dizin < metot_BAĞ_DEĞ_SAY; Loop_Dizin++) if (metot_sahip[Loop_Dizin] == Sınıf_Tanım && Word_SMS(metot_ad_SMS[Loop_Dizin], İsim) && Word_SMS(metot_TÜR[Loop_Dizin], biçim_değer)) return Loop_Dizin;
        return -1;
    }
    static int TÜR_Tip(int İsim) { return dosya[상가[İsim]] == 'L' || dosya[상가[İsim]] == '[' ? 2 : 1; }
    static boolean başlat(int Sınıf_Tanım, int komut_Start) {
        if (Sınıf_Tanım < 0 || hata) return false;
        if (Sınıf_Tanım_Durum[Sınıf_Tanım] == 3) { hata_değer("NoClassDefFoundError: initialization failed"); return false; }
        if (Sınıf_Tanım_Durum[Sınıf_Tanım] == 1 && Sınıf_yazışma[Sınıf_Tanım] != geçerli_yazışma) { kare_konum[kare_Dizin] = komut_Start; değişiklik_isteği = true; return false; }
        if (Sınıf_Tanım_Durum[Sınıf_Tanım] != 0) return true;
        int 위 = ana_Sınıf(Sınıf_Tanım);
        if (위 >= 0 && !başlat(위, komut_Start)) return false;
        Sınıf_Tanım_Durum[Sınıf_Tanım] = 1; Sınıf_yazışma[Sınıf_Tanım] = geçerli_yazışma;
        if (종초기화[Sınıf_Tanım] != 0) {
            kare_konum[kare_Dizin] = komut_Start;
            호출(종초기화[Sınıf_Tanım] - 1); if (!hata) 틀초기화[kare_Dizin] = Sınıf_Tanım + 1;
            return false;
        }
        Sınıf_Tanım_Durum[Sınıf_Tanım] = 2; return true;
    }
    static void 필드호출(int Dizin, int komut, int çalıştır) {
        if (!çek_sabit(Dizin, 9)) return;
        int sahip_değer = sınıf_adı_SMS(상가[Dizin]), İsim = Başvuru_ad(sabit_SANİYE_değer[Dizin]), biçim_değer = başvuru_türü(sabit_SANİYE_değer[Dizin]);
        if (Word_SMS(sahip_değer, "java/lang/System") && (Word_SMS(İsim, "out") || Word_SMS(İsim, "err")) && Word_SMS(biçim_değer, "Ljava/io/PrintStream;") && komut == 178) { 넣기(-1, 2); return; }
        int Sınıf_Tanım = BUL_Sınıf_Tanım(sahip_değer); if (Sınıf_Tanım < 0 || hata) return;
        int 찾음 = -1;
        for (int 읽는자리 = Sınıf_Tanım, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = ana_Sınıf(읽는자리))
            for (int Dosya_Dizin = 0; Dosya_Dizin < yuva_BAĞ_DEĞ_SAY; Dosya_Dizin++) if (yuva_sahip[Dosya_Dizin] == 읽는자리 && 같은말(yuva_ad[Dosya_Dizin], İsim) && 같은말(yuva_TÜR[Dosya_Dizin], biçim_değer)) 찾음 = Dosya_Dizin;
        if (찾음 < 0) { hata_değer("NoSuchFieldError"); return; }
        boolean statik_değer = komut == 178 || komut == 179;
        if (statik_değer != ((yuva_izinler[찾음] & 8) != 0)) { hata_değer("field static/instance mismatch"); return; }
        if (statik_değer && !başlat(yuva_sahip[찾음], çalıştır)) return;
        int TÜR_değer = TÜR_Tip(biçim_değer), değer = 0;
        if (komut == 179 || komut == 181) değer = 빼기(TÜR_değer);
        if (statik_değer) { if (komut == 178) 넣기(yuva_veri[찾음], TÜR_değer); else if (!hata) yuva_veri[찾음] = değer; return; }
        int nesne_Başvuru = 빼기(2);
        if (!bilgi_teknolojisi_geçerli_nesne(nesne_Başvuru)) return;
        if (yığın_değer[nesne_Başvuru] < 32 || !종포함(yığın_değer[nesne_Başvuru] - 32, sahip_değer)) { hata_değer("field receiver type mismatch"); return; }
        int 보관칸 = nesne_Başvuru + 2 + yuva_konum[찾음];
        if (komut == 180) 넣기(yığın_değer[보관칸], TÜR_değer);
        else if (!hata) { yığın_değer[보관칸] = değer; yığın_Başvuru[보관칸] = TÜR_değer == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Sınıf_Tanım, int İsim) {
        for (int 중첩깊이 = 0; Sınıf_Tanım >= 0 && 중첩깊이 < 16; 중첩깊이++, Sınıf_Tanım = ana_Sınıf(Sınıf_Tanım)) {
            if (같은말(Sınıf_Tanım_ad[Sınıf_Tanım], İsim) || (Sınıf_Tanım_ana[Sınıf_Tanım] != 0 && 같은말(Sınıf_Tanım_ana[Sınıf_Tanım], İsim))) return true;
            for (int iç_konum = 0; iç_konum < Sınıf_arabirim_BAĞ_DEĞ_SAY[Sınıf_Tanım]; iç_konum++) if (같은말(Sınıf_arabirim[Sınıf_Tanım * 16 + iç_konum], İsim)) return true;
        }
        return false;
    }
    static boolean metinler_eşit(int 첫값, int bayt_veri, boolean yol) {
        if (첫값 == bayt_veri) return true;
        if (첫값 <= 0 || bayt_veri <= 0 || yığın_değer[첫값] != 1 || yığın_değer[bayt_veri] != 1 || yığın_değer[첫값 + 1] != yığın_değer[bayt_veri + 1]) return false;
        for (int Loop_Dizin = 0; Loop_Dizin < yığın_değer[첫값 + 1]; Loop_Dizin++) {
            int x_koordinatı = yığın_değer[첫값 + 2 + Loop_Dizin], Y_koordinat = yığın_değer[bayt_veri + 2 + Loop_Dizin];
            if (yol) { if (x_koordinatı == '.') x_koordinatı = '/'; if (Y_koordinat == '.') Y_koordinat = '/'; }
            if (x_koordinatı != Y_koordinat) return false;
        }
        return true;
    }
    static boolean bilgi_teknolojisi_geçerli_nesne(int nesne_Başvuru) {
        if (nesne_Başvuru == 0) { hata_değer("NullPointerException"); return false; }
        if (nesne_Başvuru < 1 || nesne_Başvuru >= yığın_Bitiş_konum || 힙폭[nesne_Başvuru] < 2 || yığın_değer[nesne_Başvuru] == 0) { hata_değer("invalid object reference"); return false; }
        return true;
    }
    static void korumak_değer(int nesne_Başvuru) {
        if (nesne_Başvuru > 0 && nesne_Başvuru < yığın_Bitiş_konum && 힙폭[nesne_Başvuru] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = nesne_Başvuru;
    }
    static void şov_değer(int nesne_Başvuru) {
        if (nesne_Başvuru > 0 && nesne_Başvuru < yığın_Bitiş_konum && 힙폭[nesne_Başvuru] >= 2 && yığın_değer[nesne_Başvuru] != 0 && 힙표시[nesne_Başvuru] == 0) {
            힙표시[nesne_Başvuru] = 1; 표시대기[monitör_BAĞ_DEĞ_SAY++] = nesne_Başvuru;
        }
    }
    static void 수거() {
        monitör_BAĞ_DEĞ_SAY = 0; tahsilat_BAĞ_DEĞ_SAY++;
        for (int çek_konum = 1; çek_konum < yığın_Bitiş_konum; çek_konum += 힙폭[çek_konum]) 힙표시[çek_konum] = 0;
        for (int Loop_Dizin = 0; Loop_Dizin < dize_Başvuru.length; Loop_Dizin++) şov_değer(dize_Başvuru[Loop_Dizin]);
        for (int Loop_Dizin = 0; Loop_Dizin < yuva_BAĞ_DEĞ_SAY; Loop_Dizin++) if ((yuva_izinler[Loop_Dizin] & 8) != 0 && TÜR_Tip(yuva_TÜR[Loop_Dizin]) == 2) şov_değer(yuva_veri[Loop_Dizin]);
        for (int 임시값 = 0; 임시값 < yazışma_BAĞ_DEĞ_SAY; 임시값++) {
            şov_değer(yazışma_nesne[임시값]); şov_değer(yazışma_hedef[임시값]);
            int 꼭대기자리 = 임시값 == geçerli_yazışma ? kare_Dizin : yazışma_kare[임시값];
            for (int Dosya_Dizin = 임시값 * 32; Dosya_Dizin <= 꼭대기자리; Dosya_Dizin++) {
                for (int iç_konum = 0; iç_konum < 함수지역[kare_metot[Dosya_Dizin]]; iç_konum++) if (yerel_TÜR[Dosya_Dizin * 128 + iç_konum] == 2) şov_değer(yerel_değer[Dosya_Dizin * 128 + iç_konum]);
                for (int iç_konum = 0; iç_konum < kare_Yığın[Dosya_Dizin]; iç_konum++) if (işlenen_Yığın_TÜR[Dosya_Dizin * 128 + iç_konum] == 2) şov_değer(işlenen_Yığın_değer[Dosya_Dizin * 128 + iç_konum]);
            }
        }
        for (int Loop_Dizin = 0; Loop_Dizin < 화면참조.length; Loop_Dizin++) şov_değer(화면참조[Loop_Dizin]);
        for (int Loop_Dizin = 0; Loop_Dizin < 나중수; Loop_Dizin++) şov_değer(나중실행[Loop_Dizin]);
        for (int Loop_Dizin = 0; Loop_Dizin < depo_bilgi.length; Loop_Dizin++) şov_değer(depo_bilgi[Loop_Dizin]);
        for (int Loop_Dizin = 0; Loop_Dizin < Sınıf_Tanım_BAĞ_DEĞ_SAY; Loop_Dizin++) şov_değer(Sınıf_kilit[Loop_Dizin]);
        for (int çek_konum = 1; çek_konum < yığın_Bitiş_konum; çek_konum += 힙폭[çek_konum]) if (잠금깊이[çek_konum] > 0) şov_değer(çek_konum);
        şov_değer(던진객체);
        for (int Loop_Dizin = 0; Loop_Dizin < 잠시수; Loop_Dizin++) şov_değer(잠시참조[Loop_Dizin]);
        while (monitör_BAĞ_DEĞ_SAY > 0) {
            int nesne_Başvuru = 표시대기[--monitör_BAĞ_DEĞ_SAY], alan_KOD = yığın_değer[nesne_Başvuru];
            for (int Loop_Dizin = nesne_Başvuru + 2; Loop_Dizin < nesne_Başvuru + 힙폭[nesne_Başvuru]; Loop_Dizin++) if (alan_KOD == 3 || alan_KOD == 4 || yığın_Başvuru[Loop_Dizin] != 0) şov_değer(yığın_değer[Loop_Dizin]);
        }
        for (int çek_konum = 1; çek_konum < yığın_Bitiş_konum; çek_konum += 힙폭[çek_konum]) if (힙표시[çek_konum] == 0) yığın_değer[çek_konum] = 0;
        for (int çek_konum = 1; çek_konum < yığın_Bitiş_konum; çek_konum += 힙폭[çek_konum]) if (yığın_değer[çek_konum] == 0) {
            while (çek_konum + 힙폭[çek_konum] < yığın_Bitiş_konum && yığın_değer[çek_konum + 힙폭[çek_konum]] == 0) { int Sonraki_konum = çek_konum + 힙폭[çek_konum]; 힙폭[çek_konum] += 힙폭[Sonraki_konum]; 힙폭[Sonraki_konum] = 0; }
            if (çek_konum + 힙폭[çek_konum] == yığın_Bitiş_konum) { yığın_Bitiş_konum = çek_konum; break; }
        }
    }
    static int 새기억(int Tip_değer, int süre_değer) {
        if (süre_değer < 0) { hata_değer("NegativeArraySizeException"); return 0; }
        if (süre_değer > yığın_değer.length - 3) { hata_değer("object heap exhausted"); return 0; }
        int 필요수 = süre_değer + 2, nesne_Başvuru = 0;
        if (필요수 <= yığın_değer.length - yığın_Bitiş_konum) { nesne_Başvuru = yığın_Bitiş_konum; yığın_Bitiş_konum += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < yığın_Bitiş_konum; 읽는자리 += 힙폭[읽는자리]) if (yığın_değer[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { nesne_Başvuru = 읽는자리; break; }
            if (nesne_Başvuru != 0) {
                int 남은길이 = 힙폭[nesne_Başvuru] - 필요수;
                if (남은길이 >= 2) { 힙폭[nesne_Başvuru + 필요수] = 남은길이; yığın_değer[nesne_Başvuru + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= yığın_değer.length - yığın_Bitiş_konum) { nesne_Başvuru = yığın_Bitiş_konum; yığın_Bitiş_konum += 필요수; }
        }
        if (nesne_Başvuru == 0) { hata_değer("object heap exhausted"); return 0; }
        for (int Loop_Dizin = 0; Loop_Dizin < 필요수; Loop_Dizin++) { yığın_değer[nesne_Başvuru + Loop_Dizin] = 0; yığın_Başvuru[nesne_Başvuru + Loop_Dizin] = 0; 힙폭[nesne_Başvuru + Loop_Dizin] = 0; }
        dizi_öğesi[nesne_Başvuru] = 0;
        힙폭[nesne_Başvuru] = 필요수; yığın_değer[nesne_Başvuru] = Tip_değer; yığın_değer[nesne_Başvuru + 1] = süre_değer; korumak_değer(nesne_Başvuru); return nesne_Başvuru;
    }
    static int özel_durum_Sınıf(String ad_sabit) {
        if (자바도구.같음(ad_sabit, "java/lang/Throwable")) return 1;
        if (자바도구.같음(ad_sabit, "java/lang/Exception")) return 2;
        if (자바도구.같음(ad_sabit, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(ad_sabit, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(ad_sabit, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(ad_sabit, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(ad_sabit, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(ad_sabit, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(ad_sabit, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(ad_sabit, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(ad_sabit, "java/io/IOException")) return 11;
        if (자바도구.같음(ad_sabit, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(ad_sabit, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(ad_sabit, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(ad_sabit, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int özel_durum_sabit(int İsim) {
        for (int Loop_Dizin = 1; Loop_Dizin <= 41; Loop_Dizin++) if (Word_SMS(İsim, özel_durum_ad(Loop_Dizin))) return Loop_Dizin;
        return 0;
    }
    static String özel_durum_ad(int hesap_değer) {
        if (hesap_değer == 40) return "java/lang/InterruptedException";
        if (hesap_değer == 41) return "Türkçe/Öz/대기중단예외";
        if (hesap_değer == 39) return "java/net/SocketException";
        if (hesap_değer == 20) return "Türkçe/Öz/özel_durum";
        if (hesap_değer == 21) return "Türkçe/Öz/yürütme_özel_durum";
        if (hesap_değer == 22) return "Türkçe/Öz/G_Ç_özel_durum";
        if (hesap_değer == 23) return "Türkçe/Öz/bekle_ZAMANAŞIMI_özel_durum";
        if (hesap_değer == 24) return "Türkçe/Öz/ADRES_ARA_özel_durum";
        if (hesap_değer == 25) return "Türkçe/Öz/파일없음예외";
        if (hesap_değer == 26) return "Türkçe/Öz/iletişim_özel_durum";
        if (hesap_değer == 27) return "Türkçe/Öz/geçersiz_bağımsız_değişken_özel_durum";
        if (hesap_değer == 28) return "Türkçe/Öz/숫자형식예외";
        if (hesap_değer == 29) return "Türkçe/Öz/범위예외";
        if (hesap_değer == 30) return "Türkçe/Öz/배열범위예외";
        if (hesap_değer == 31) return "Türkçe/Öz/문자열범위예외";
        if (hesap_değer == 32) return "Türkçe/Öz/boş_referans_özel_durum";
        if (hesap_değer == 33) return "Türkçe/Öz/산술예외";
        if (hesap_değer == 34) return "Türkçe/Öz/Durum_özel_durum";
        if (hesap_değer == 35) return "Türkçe/Öz/TÜR_Yayın_özel_durum";
        if (hesap_değer == 36) return "Türkçe/Öz/Negatif_DİZİ_boyutlandırmak_hata";
        if (hesap_değer == 37) return "Türkçe/Öz/DİZİ_depo_hata";
        if (hesap_değer == 38) return "Türkçe/Öz/yazışma_Durum_özel_durum";
        if (hesap_değer == 1) return "java/lang/Throwable"; if (hesap_değer == 2) return "java/lang/Exception";
        if (hesap_değer == 3) return "java/lang/RuntimeException"; if (hesap_değer == 4) return "java/lang/ArithmeticException";
        if (hesap_değer == 5) return "java/lang/NullPointerException"; if (hesap_değer == 6) return "java/lang/IndexOutOfBoundsException";
        if (hesap_değer == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (hesap_değer == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (hesap_değer == 9) return "java/lang/IllegalArgumentException"; if (hesap_değer == 10) return "java/lang/NumberFormatException";
        if (hesap_değer == 11) return "java/io/IOException"; if (hesap_değer == 12) return "java/io/FileNotFoundException";
        if (hesap_değer == 17) return "java/lang/ArrayStoreException";
        if (hesap_değer == 18) return "java/net/UnknownHostException";
        if (hesap_değer == 19) return "java/net/SocketTimeoutException";
        if (hesap_değer == 16) return "java/lang/IllegalThreadStateException";
        if (hesap_değer == 13) return "java/lang/IllegalStateException"; if (hesap_değer == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int özel_durum_ana(int hesap_değer) {
        if (hesap_değer == 40) return 2;
        if (hesap_değer == 41) return 40;
        if (hesap_değer == 39) return 11;
        if (hesap_değer == 1) return 0;
        if (hesap_değer == 2) return 1;
        if (hesap_değer == 3) return 2;
        if (hesap_değer == 4) return 3;
        if (hesap_değer == 5) return 3;
        if (hesap_değer == 6) return 3;
        if (hesap_değer == 7) return 6;
        if (hesap_değer == 8) return 6;
        if (hesap_değer == 9) return 3;
        if (hesap_değer == 10) return 9;
        if (hesap_değer == 11) return 2;
        if (hesap_değer == 12) return 11;
        if (hesap_değer == 13) return 3;
        if (hesap_değer == 14) return 3;
        if (hesap_değer == 15) return 3;
        if (hesap_değer == 16) return 9;
        if (hesap_değer == 17) return 3;
        if (hesap_değer == 18) return 11;
        if (hesap_değer == 19) return 11;
        if (hesap_değer == 20) return 2;
        if (hesap_değer == 21) return 3;
        if (hesap_değer == 22) return 11;
        if (hesap_değer == 23) return 22;
        if (hesap_değer == 24) return 22;
        if (hesap_değer == 25) return 22;
        if (hesap_değer == 26) return 22;
        if (hesap_değer == 27) return 9;
        if (hesap_değer == 28) return 27;
        if (hesap_değer == 29) return 6;
        if (hesap_değer == 30) return 29;
        if (hesap_değer == 31) return 29;
        if (hesap_değer == 32) return 5;
        if (hesap_değer == 33) return 4;
        if (hesap_değer == 34) return 13;
        if (hesap_değer == 35) return 14;
        if (hesap_değer == 36) return 15;
        if (hesap_değer == 37) return 17;
        if (hesap_değer == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int gerçek_değer, int 요구값) {
        for (int 깊이 = 0; gerçek_değer != 0 && 깊이 < 16; 깊이++, gerçek_değer = özel_durum_ana(gerçek_değer))
            if (gerçek_değer == 요구값) return true;
        return false;
    }
    static void 예외던짐(int hesap_değer, String 안내참조) {
        int nesne_Başvuru = 새기억(9, 2); if (hata) return;
        yığın_değer[nesne_Başvuru + 2] = hesap_değer; yığın_değer[nesne_Başvuru + 3] = konak_karakter(안내참조); yığın_Başvuru[nesne_Başvuru + 3] = 1;
        던진객체 = nesne_Başvuru; hata = true;
    }
    static boolean 맞는객체(int nesne_Başvuru, int İsim) {
        if (nesne_Başvuru == 0) return true;
        if (!bilgi_teknolojisi_geçerli_nesne(nesne_Başvuru)) return false;
        int alan_KOD = yığın_değer[nesne_Başvuru];
        if (Word_SMS(İsim, "java/lang/Object")) return true;
        if (alan_KOD >= 32) return 종포함(alan_KOD - 32, İsim);
        if (alan_KOD == 9) { int hedef_ADRES = özel_durum_sabit(İsim); return hedef_ADRES != 0 && 예외포함(yığın_değer[nesne_Başvuru + 2], hedef_ADRES); }
        if (alan_KOD == 1) return Word_SMS(İsim, "java/lang/String") || Word_SMS(İsim, "java/lang/CharSequence");
        if (alan_KOD == 4) return Word_SMS(İsim, "java/lang/StringBuilder") || Word_SMS(İsim, "java/lang/CharSequence");
        if (alan_KOD == 10) return Word_SMS(İsim, "java/util/ArrayList") || Word_SMS(İsim, "java/util/List");
        if (alan_KOD == 11) return Word_SMS(İsim, "java/util/HashMap") || Word_SMS(İsim, "java/util/Map");
        if (alan_KOD == 12) return Word_SMS(İsim, "java/lang/Integer") || Word_SMS(İsim, "java/lang/Number");
        if (alan_KOD >= 24 && alan_KOD <= 28 && yığın_değer[nesne_Başvuru + 13] != 0) return 한국어화면종(İsim) == alan_KOD || Word_SMS(İsim, "Türkçe/Öz/화면구성요소");
        if (alan_KOD >= 24 && alan_KOD <= 28) return (한국어화면종(İsim) == 0 && 화면종(İsim) == alan_KOD) || Word_SMS(İsim, "java/awt/Component") || Word_SMS(İsim, "java/awt/Container") || Word_SMS(İsim, "javax/swing/JComponent");
        if (alan_KOD == 29) return Word_SMS(İsim, yığın_değer[nesne_Başvuru + 3] != 0 ? "Türkçe/Öz/Eylem_uyarı" : "java/awt/event/ActionEvent");
        if (alan_KOD == 30) return Word_SMS(İsim, "java/awt/FlowLayout") || Word_SMS(İsim, "java/awt/LayoutManager");
        if (alan_KOD == 17) return Word_SMS(İsim, "java/net/Socket");
        if (alan_KOD == 18) return Word_SMS(İsim, "java/net/ServerSocket");
        if (alan_KOD == 19) return Word_SMS(İsim, yığın_değer[nesne_Başvuru + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (alan_KOD == 14) return Word_SMS(İsim, "java/net/InetAddress");
        if (alan_KOD == 15) return Word_SMS(İsim, "java/net/DatagramSocket");
        if (alan_KOD == 16) return Word_SMS(İsim, "java/net/DatagramPacket");
        if (alan_KOD == 13) return Word_SMS(İsim, yığın_değer[nesne_Başvuru + 3] != 0 ? "Türkçe/Öz/arkaPlanGörevi" : "java/lang/Thread");
        if (alan_KOD == 2) return Word_SMS(İsim, "[I"); if (alan_KOD == 20) return Word_SMS(İsim, "[B"); if (alan_KOD == 21) return Word_SMS(İsim, "[Z");
        if (alan_KOD == 22) return Word_SMS(İsim, "[C"); if (alan_KOD == 23) return Word_SMS(İsim, "[S");
        if (alan_KOD != 3) return false;
        if (Word_SMS(İsim, "[Ljava/lang/Object;")) return true;
        int bileşen = dizi_öğesi[nesne_Başvuru];
        if (bileşen == -1) return Word_SMS(İsim, "[Ljava/lang/String;") || Word_SMS(İsim, "[Ljava/lang/CharSequence;");
        if (bileşen == 0) return false;
        if (배열종비교(bileşen, İsim)) return true;
        if ((Word_SMS(bileşen, "java/lang/String") || Word_SMS(bileşen, "java/lang/StringBuilder")) && Word_SMS(İsim, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_Dizin = 0; Loop_Dizin < Sınıf_Tanım_BAĞ_DEĞ_SAY; Loop_Dizin++) if (같은말(Sınıf_Tanım_ad[Loop_Dizin], bileşen)) {
            for (int kod_noktası = Loop_Dizin, 중첩깊이 = 0; kod_noktası >= 0 && 중첩깊이 < 16; 중첩깊이++, kod_noktası = ana_Sınıf(kod_noktası)) {
                if (배열종비교(Sınıf_Tanım_ana[kod_noktası], İsim)) return true;
                for (int iç_konum = 0; iç_konum < Sınıf_arabirim_BAĞ_DEĞ_SAY[kod_noktası]; iç_konum++) if (배열종비교(Sınıf_arabirim[kod_noktası * 16 + iç_konum], İsim)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int ad_sabit, int tanımlayıcı) {
        int çek_konum = 상가[tanımlayıcı], girdi_BAĞ_DEĞ_SAY = sabit_SANİYE_değer[tanımlayıcı];
        if (ad_sabit == 0 || girdi_BAĞ_DEĞ_SAY < 4 || dosya[çek_konum] != '[' || dosya[çek_konum + 1] != 'L' || dosya[çek_konum + girdi_BAĞ_DEĞ_SAY - 1] != ';' || sabit_SANİYE_değer[ad_sabit] != girdi_BAĞ_DEĞ_SAY - 3) return false;
        for (int Loop_Dizin = 0; Loop_Dizin < girdi_BAĞ_DEĞ_SAY - 3; Loop_Dizin++) if (dosya[상가[ad_sabit] + Loop_Dizin] != dosya[çek_konum + 2 + Loop_Dizin]) return false;
        return true;
    }
    static void sap_özel_durum() {
        if (던진객체 == 0) return;
        hata = false;
        while (kare_Dizin >= geçerli_yazışma * 32) {
            int Dosya_Dizin = kare_metot[kare_Dizin], 읽는자리 = 틀명령[kare_Dizin];
            for (int Loop_Dizin = 0; Loop_Dizin < 잡기수; Loop_Dizin++) if (잡기함수[Loop_Dizin] == Dosya_Dizin && 읽는자리 >= 잡기시작[Loop_Dizin] && 읽는자리 < 잡기끝[Loop_Dizin]
                && (잡기종[Loop_Dizin] == 0 || 맞는객체(던진객체, 잡기종[Loop_Dizin]))) {
                kare_konum[kare_Dizin] = 잡기위치[Loop_Dizin]; kare_Yığın[kare_Dizin] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (틀초기화[kare_Dizin] != 0) Sınıf_Tanım_Durum[틀초기화[kare_Dizin] - 1] = 3;
            if (kare_kilit[kare_Dizin] != 0) { sürüm_kilit(kare_kilit[kare_Dizin]); kare_kilit[kare_Dizin] = 0; }
            kare_Dizin--;
        }
        kullanıcı_alanı.Yazma("Uncaught ");
        if (yığın_değer[던진객체] == 9) { kullanıcı_alanı.Yazma(özel_durum_ad(yığın_değer[던진객체 + 2])); kullanıcı_alanı.Yazma(": "); yazma_SMS(yığın_değer[던진객체 + 3]); }
        else kullanıcı_alanı.Yazma("user exception");
        kullanıcı_alanı.yazma_karakter_değer(10); 던진객체 = 0; hata = true;
    }
    // 이 JVM의 işlenen_Yığın 항목은 geçerli_öğe category-1(int/reference)만 허용한다.
    static void 스택명령(int komut_KOD) {
        int 첫값 = 빼기(0), 첫형식 = dönüş_türü;
        if (komut_KOD == 87) return;
        if (komut_KOD == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int bayt_veri = 빼기(0), SANİYE_biçim = dönüş_türü;
        if (komut_KOD == 88) return;
        if (komut_KOD == 90) { 넣기(첫값, 첫형식); 넣기(bayt_veri, SANİYE_biçim); 넣기(첫값, 첫형식); return; }
        if (komut_KOD == 92) { 넣기(bayt_veri, SANİYE_biçim); 넣기(첫값, 첫형식); 넣기(bayt_veri, SANİYE_biçim); 넣기(첫값, 첫형식); return; }
        if (komut_KOD == 95) { 넣기(첫값, 첫형식); 넣기(bayt_veri, SANİYE_biçim); return; }
        int kod_noktası = 빼기(0), 셋째형식 = dönüş_türü;
        if (komut_KOD == 91) { 넣기(첫값, 첫형식); 넣기(kod_noktası, 셋째형식); 넣기(bayt_veri, SANİYE_biçim); 넣기(첫값, 첫형식); return; }
        if (komut_KOD == 93) { 넣기(bayt_veri, SANİYE_biçim); 넣기(첫값, 첫형식); 넣기(kod_noktası, 셋째형식); 넣기(bayt_veri, SANİYE_biçim); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = dönüş_türü;
        넣기(bayt_veri, SANİYE_biçim); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(kod_noktası, 셋째형식); 넣기(bayt_veri, SANİYE_biçim); 넣기(첫값, 첫형식);
    }
    static void 새객체(int ad_sabit, int 시작점) {
        int alan_KOD = 0, geçerli_süre = 0, özel_durum_Başvuru = özel_durum_sabit(ad_sabit);
        if (Word_SMS(ad_sabit, "java/lang/StringBuilder")) { alan_KOD = 4; geçerli_süre = 1; }
        if (Word_SMS(ad_sabit, "java/io/FileInputStream")) { alan_KOD = 5; geçerli_süre = 2; }
        if (Word_SMS(ad_sabit, "java/io/FileOutputStream")) { alan_KOD = 6; geçerli_süre = 2; }
        if (özel_durum_Başvuru != 0) { alan_KOD = 9; geçerli_süre = 2; }
        if (Word_SMS(ad_sabit, "java/util/ArrayList")) { alan_KOD = 10; geçerli_süre = 2; }
        if (Word_SMS(ad_sabit, "java/util/HashMap")) { alan_KOD = 11; geçerli_süre = 2; }
        if (Word_SMS(ad_sabit, "java/lang/Integer")) { alan_KOD = 12; geçerli_süre = 1; }
        if (Word_SMS(ad_sabit, "java/net/Socket")) { alan_KOD = 17; geçerli_süre = 5; }
        if (Word_SMS(ad_sabit, "java/net/ServerSocket")) { alan_KOD = 18; geçerli_süre = 5; }
        if (Word_SMS(ad_sabit, "java/net/DatagramSocket")) { alan_KOD = 15; geçerli_süre = 3; }
        if (Word_SMS(ad_sabit, "java/net/DatagramPacket")) { alan_KOD = 16; geçerli_süre = 4; }
        if (Word_SMS(ad_sabit, "java/lang/Thread") || Word_SMS(ad_sabit, "Türkçe/Öz/arkaPlanGörevi")) { alan_KOD = 13; geçerli_süre = 2; }
        if (Word_SMS(ad_sabit, "java/lang/Object")) { alan_KOD = 8; }
        if (alan_KOD == 0 && 화면종(ad_sabit) != 0) { alan_KOD = 화면종(ad_sabit); geçerli_süre = 12; }
        if (alan_KOD == 0) {
            int kod_noktası = BUL_Sınıf_Tanım(ad_sabit); if (kod_noktası < 0 || hata || !başlat(kod_noktası, 시작점)) return;
            alan_KOD = 32 + kod_noktası; geçerli_süre = Sınıf_yuva_BAĞ_DEĞ_SAY[kod_noktası];
        }
        int nesne_Başvuru = ayırmak_Depolama(alan_KOD, geçerli_süre); if (hata) return;
        if (alan_KOD == 13 && Word_SMS(ad_sabit, "Türkçe/Öz/arkaPlanGörevi")) yığın_değer[nesne_Başvuru + 3] = 1;
        if (alan_KOD >= 24 && alan_KOD <= 28 && 한국어화면종(ad_sabit) != 0) yığın_değer[nesne_Başvuru + 13] = 1;
        if (alan_KOD == 5 || alan_KOD == 6 || alan_KOD == 15 || alan_KOD == 17 || alan_KOD == 18) yığın_değer[nesne_Başvuru + 2] = -1;
        if (alan_KOD == 9) yığın_değer[nesne_Başvuru + 2] = özel_durum_Başvuru;
        넣기(nesne_Başvuru, 2);
    }
    static boolean 값같음(int 첫값, int bayt_veri) {
        if (첫값 == bayt_veri) return true;
        if (첫값 == 0 || bayt_veri == 0 || 첫값 < 0 || bayt_veri < 0 || 첫값 >= yığın_Bitiş_konum || bayt_veri >= yığın_Bitiş_konum) return false;
        if (yığın_değer[첫값] == 1 && yığın_değer[bayt_veri] == 1) return metinler_eşit(첫값, bayt_veri, false);
        return yığın_değer[첫값] == 12 && yığın_değer[bayt_veri] == 12 && yığın_değer[첫값 + 2] == yığın_değer[bayt_veri + 2];
    }
    static int SMS_parça(int nesne_Başvuru, int Start_konum, int Bitiş_konum) {
        if (!nesne_değer(nesne_Başvuru, 1)) return 0;
        if (Start_konum < 0 || Bitiş_konum < Start_konum || Bitiş_konum > yığın_değer[nesne_Başvuru + 1]) { hata_değer("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = ayırmak_Depolama(1, Bitiş_konum - Start_konum); if (hata) return 0;
        for (int Loop_Dizin = Start_konum; Loop_Dizin < Bitiş_konum; Loop_Dizin++) yığın_değer[반환값 + 2 + Loop_Dizin - Start_konum] = yığın_değer[nesne_Başvuru + 2 + Loop_Dizin];
        return 반환값;
    }
    static int Katıl_SMS(int 첫값, int bayt_veri) {
        if (!nesne_değer(첫값, 1) || !nesne_değer(bayt_veri, 1)) return 0;
        int girdi_BAĞ_DEĞ_SAY = yığın_değer[첫값 + 1], metot_Dizin = yığın_değer[bayt_veri + 1], 반환값 = ayırmak_Depolama(1, girdi_BAĞ_DEĞ_SAY + metot_Dizin); if (hata) return 0;
        for (int Loop_Dizin = 0; Loop_Dizin < girdi_BAĞ_DEĞ_SAY; Loop_Dizin++) yığın_değer[반환값 + 2 + Loop_Dizin] = yığın_değer[첫값 + 2 + Loop_Dizin];
        for (int Loop_Dizin = 0; Loop_Dizin < metot_Dizin; Loop_Dizin++) yığın_değer[반환값 + 2 + girdi_BAĞ_DEĞ_SAY + Loop_Dizin] = yığın_değer[bayt_veri + 2 + Loop_Dizin];
        return 반환값;
    }
    static boolean 기본호출(int sahip, int ad_sabit, int tanımlayıcı_sabit, int komut_KOD) {
        if (Word_SMS(sahip, "Türkçe/Öz/실행인수") && komut_KOD == 184) {
            if (Word_SMS(ad_sabit, "öğe_BAĞ_DEĞ_SAY") && Word_SMS(tanımlayıcı_sabit, "()I")) { 넣기(kullanıcı_alanı.인수개수() - 1, 1); return true; }
            if (Word_SMS(ad_sabit, "metin") && Word_SMS(tanımlayıcı_sabit, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= kullanıcı_alanı.인수개수() - 1) 예외던짐(29, "yürütmek_komut bağımsız_değişkenler 범위를 벗어났습니다");
                else 넣기(konak_karakter(kullanıcı_alanı.bağımsız_değişkenler(순번 + 1)), 2);
                return true;
            }
            hata_değer("지원하지 않는 Türkçe yürütmek_komut bağımsız_değişkenler 호출"); return true;
        }
        if (Word_SMS(sahip, "Türkçe/Öz/arkaPlanGörevi")) { işlem_yazışma(ad_sabit, tanımlayıcı_sabit, komut_KOD, true); return true; }
        if (한국어화면소유(sahip)) { 한국어화면호출(sahip, ad_sabit, tanımlayıcı_sabit, komut_KOD); return true; }
        if (화면소유(sahip)) { 화면호출(sahip, ad_sabit, tanımlayıcı_sabit, komut_KOD); return true; }
        if (Word_SMS(sahip, "java/net/Socket") || Word_SMS(sahip, "java/net/ServerSocket") || Word_SMS(sahip, "java/io/InputStream") || Word_SMS(sahip, "java/io/OutputStream")) { 흐름호출(sahip, ad_sabit, tanımlayıcı_sabit, komut_KOD); return true; }
        if (Word_SMS(sahip, "Türkçe/Öz/çekirdek_değer") && komut_KOD == 184) {
            if (Word_SMS(ad_sabit, "화면너비") && Word_SMS(tanımlayıcı_sabit, "()I")) { 넣기(kullanıcı_alanı.화면너비(), 1); return true; }
            if (Word_SMS(ad_sabit, "화면높이") && Word_SMS(tanımlayıcı_sabit, "()I")) { 넣기(kullanıcı_alanı.화면높이(), 1); return true; }
            if (Word_SMS(ad_sabit, "밀리초") && Word_SMS(tanımlayıcı_sabit, "()I")) { 넣기(kullanıcı_alanı.밀리초(), 1); return true; }
            if (Word_SMS(ad_sabit, "그림대기") && Word_SMS(tanımlayıcı_sabit, "()I")) { 넣기(kullanıcı_alanı.그림대기(), 1); return true; }
            if (Word_SMS(ad_sabit, "dikdörtgen") && Word_SMS(tanımlayıcı_sabit, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinat = 빼기(1), x_koordinatı = 빼기(1); 넣기(kullanıcı_alanı.dikdörtgen(x_koordinatı, Y_koordinat, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(sahip, "java/net/InetAddress") || Word_SMS(sahip, "java/net/DatagramPacket") || Word_SMS(sahip, "java/net/DatagramSocket")) { 통신호출(sahip, ad_sabit, tanımlayıcı_sabit, komut_KOD); return true; }
        if (Word_SMS(sahip, "java/lang/Thread")) { 가닥호출(ad_sabit, tanımlayıcı_sabit, komut_KOD); return true; }
        if (Word_SMS(sahip, "java/lang/Object")) {
            if (Word_SMS(ad_sabit, "<init>") && Word_SMS(tanımlayıcı_sabit, "()V") && komut_KOD == 183) { bilgi_teknolojisi_geçerli_nesne(빼기(2)); return true; }
            if (Word_SMS(ad_sabit, "equals") && Word_SMS(tanımlayıcı_sabit, "(Ljava/lang/Object;)Z")) { int bayt_veri = 빼기(2), 첫값 = 빼기(2); if (bilgi_teknolojisi_geçerli_nesne(첫값)) 넣기(첫값 == bayt_veri ? 1 : 0, 1); return true; }
        }
        if (özel_durum_sabit(sahip) != 0) {
            if (Word_SMS(ad_sabit, "<init>") && komut_KOD == 183 && (Word_SMS(tanımlayıcı_sabit, "()V") || Word_SMS(tanımlayıcı_sabit, "(Ljava/lang/String;)V"))) {
                int istem = Word_SMS(tanımlayıcı_sabit, "()V") ? 0 : 빼기(2), nesne_Başvuru = 빼기(2);
                if (nesne_değer(nesne_Başvuru, 9)) { yığın_değer[nesne_Başvuru + 3] = istem; yığın_Başvuru[nesne_Başvuru + 3] = 1; } return true;
            }
            if ((Word_SMS(ad_sabit, "getMessage") || Word_SMS(ad_sabit, "설명")) && Word_SMS(tanımlayıcı_sabit, "()Ljava/lang/String;")) { int nesne_Başvuru = 빼기(2); if (nesne_değer(nesne_Başvuru, 9)) 넣기(yığın_değer[nesne_Başvuru + 3], 2); return true; }
        }
        if (Word_SMS(sahip, "java/lang/String")) {
            if (komut_KOD == 182 && Word_SMS(ad_sabit, "getBytes") && (Word_SMS(tanımlayıcı_sabit, "()[B") || Word_SMS(tanımlayıcı_sabit, "(Ljava/lang/String;)[B"))) {
                int kodlama_ad = Word_SMS(tanımlayıcı_sabit, "()[B") ? 0 : 빼기(2), nesne_Başvuru = 빼기(2);
                if (!nesne_değer(nesne_Başvuru, 1)) return true;
                if (kodlama_ad != 0 && !metinler_eşit(kodlama_ad, konak_karakter("UTF-8"), false) && !metinler_eşit(kodlama_ad, konak_karakter("UTF8"), false) && !metinler_eşit(kodlama_ad, konak_karakter("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int girdi_BAĞ_DEĞ_SAY = yığın_değer[nesne_Başvuru + 1], 반환값 = ayırmak_Depolama(20, girdi_BAĞ_DEĞ_SAY * 3), 사용수 = 0; if (hata) return true;
                for (int iç_konum = 0; iç_konum < girdi_BAĞ_DEĞ_SAY; iç_konum++) {
                    int kod_noktası = yığın_değer[nesne_Başvuru + 2 + iç_konum];
                    if (kod_noktası >= 0xd800 && kod_noktası <= 0xdbff && iç_konum + 1 < girdi_BAĞ_DEĞ_SAY && yığın_değer[nesne_Başvuru + 3 + iç_konum] >= 0xdc00 && yığın_değer[nesne_Başvuru + 3 + iç_konum] <= 0xdfff) kod_noktası = 0x10000 + ((kod_noktası - 0xd800) << 10) + yığın_değer[nesne_Başvuru + 2 + ++iç_konum] - 0xdc00;
                    else if (kod_noktası >= 0xd800 && kod_noktası <= 0xdfff) kod_noktası = '?';
                    if (kod_noktası < 128) yığın_değer[반환값 + 2 + 사용수++] = kod_noktası;
                    else { int bayt_BAĞ_DEĞ_SAY = kod_noktası < 2048 ? 2 : kod_noktası < 65536 ? 3 : 4; yığın_değer[반환값 + 2 + 사용수++] = (byte)((bayt_BAĞ_DEĞ_SAY == 2 ? 192 : bayt_BAĞ_DEĞ_SAY == 3 ? 224 : 240) | kod_noktası >> (6 * (bayt_BAĞ_DEĞ_SAY - 1))); for (int Karşılaştırma_konum = bayt_BAĞ_DEĞ_SAY - 1; Karşılaştırma_konum > 0; Karşılaştırma_konum--) yığın_değer[반환값 + 2 + 사용수++] = (byte)(128 | kod_noktası >> (6 * (Karşılaştırma_konum - 1)) & 63); }
                }
                yığın_değer[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (komut_KOD == 184 && Word_SMS(ad_sabit, "valueOf") && Word_SMS(tanımlayıcı_sabit, "(I)Ljava/lang/String;")) { 넣기(rakam_karakter(빼기(1)), 2); return true; }
            if (komut_KOD != 182) return false;
            if (Word_SMS(ad_sabit, "equals") && Word_SMS(tanımlayıcı_sabit, "(Ljava/lang/Object;)Z")) { int bayt_veri = 빼기(2), 첫값 = 빼기(2); if (nesne_değer(첫값, 1)) 넣기(metinler_eşit(첫값, bayt_veri, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(ad_sabit, "isEmpty") && Word_SMS(tanımlayıcı_sabit, "()Z")) { int 첫값 = 빼기(2); if (nesne_değer(첫값, 1)) 넣기(yığın_değer[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(ad_sabit, "substring") && (Word_SMS(tanımlayıcı_sabit, "(I)Ljava/lang/String;") || Word_SMS(tanımlayıcı_sabit, "(II)Ljava/lang/String;"))) {
                boolean SANİYE_değer = Word_SMS(tanımlayıcı_sabit, "(II)Ljava/lang/String;"); int Bitiş_konum = SANİYE_değer ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (nesne_değer(첫값, 1)) 넣기(SMS_parça(첫값, 시작점, SANİYE_değer ? Bitiş_konum : yığın_değer[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(ad_sabit, "concat") && Word_SMS(tanımlayıcı_sabit, "(Ljava/lang/String;)Ljava/lang/String;")) { int bayt_veri = 빼기(2), 첫값 = 빼기(2); 넣기(Katıl_SMS(첫값, bayt_veri), 2); return true; }
            if (Word_SMS(ad_sabit, "hashCode") && Word_SMS(tanımlayıcı_sabit, "()I")) { int 첫값 = 빼기(2), özet_değer_bb8f435c = 0; if (nesne_değer(첫값, 1)) { for (int Loop_Dizin = 0; Loop_Dizin < yığın_değer[첫값 + 1]; Loop_Dizin++) özet_değer_bb8f435c = özet_değer_bb8f435c * 31 + yığın_değer[첫값 + 2 + Loop_Dizin]; 넣기(özet_değer_bb8f435c, 1); } return true; }
            if (Word_SMS(ad_sabit, "toString") && Word_SMS(tanımlayıcı_sabit, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (nesne_değer(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(sahip, "java/lang/Integer")) {
            if (komut_KOD == 184 && Word_SMS(ad_sabit, "valueOf") && Word_SMS(tanımlayıcı_sabit, "(I)Ljava/lang/Integer;")) { int veri_değer = 빼기(1), nesne_Başvuru = veri_değer >= -128 && veri_değer <= 127 ? depo_bilgi[veri_değer + 128] : 0; if (nesne_Başvuru == 0) { nesne_Başvuru = ayırmak_Depolama(12, 1); if (!hata) { yığın_değer[nesne_Başvuru + 2] = veri_değer; if (veri_değer >= -128 && veri_değer <= 127) depo_bilgi[veri_değer + 128] = nesne_Başvuru; } } 넣기(nesne_Başvuru, 2); return true; }
            if (komut_KOD == 183 && Word_SMS(ad_sabit, "<init>") && Word_SMS(tanımlayıcı_sabit, "(I)V")) { int veri_değer = 빼기(1), nesne_Başvuru = 빼기(2); if (nesne_değer(nesne_Başvuru, 12)) yığın_değer[nesne_Başvuru + 2] = veri_değer; return true; }
            if (komut_KOD == 182 && Word_SMS(ad_sabit, "intValue") && Word_SMS(tanımlayıcı_sabit, "()I")) { int nesne_Başvuru = 빼기(2); if (nesne_değer(nesne_Başvuru, 12)) 넣기(yığın_değer[nesne_Başvuru + 2], 1); return true; }
            if (komut_KOD == 184 && Word_SMS(ad_sabit, "toString") && Word_SMS(tanımlayıcı_sabit, "(I)Ljava/lang/String;")) { 넣기(rakam_karakter(빼기(1)), 2); return true; }
        }
        if (Word_SMS(sahip, "java/lang/Math") && komut_KOD == 184) {
            if (Word_SMS(ad_sabit, "abs") && Word_SMS(tanımlayıcı_sabit, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(ad_sabit, "min") || Word_SMS(ad_sabit, "max")) && Word_SMS(tanımlayıcı_sabit, "(II)I")) { int bayt_veri = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(ad_sabit, "min") ? (첫값 < bayt_veri ? 첫값 : bayt_veri) : (첫값 > bayt_veri ? 첫값 : bayt_veri), 1); return true; }
        }
        if (Word_SMS(sahip, "java/lang/System") && komut_KOD == 184) {
            if (Word_SMS(ad_sabit, "gc") && Word_SMS(tanımlayıcı_sabit, "()V")) { 수거(); return true; }
            if (Word_SMS(ad_sabit, "arraycopy") && Word_SMS(tanımlayıcı_sabit, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int girdi_BAĞ_DEĞ_SAY = 빼기(1), hedef_değer_Dizin = 빼기(1), bayt_veri = 빼기(2), Start_konum = 빼기(1), 첫값 = 빼기(2);
                if (bilgi_teknolojisi_geçerli_nesne(첫값) && bilgi_teknolojisi_geçerli_nesne(bayt_veri)) {
                    int alan_KOD = yığın_değer[첫값];
                    if (yığın_değer[bayt_veri] != alan_KOD || (alan_KOD != 2 && alan_KOD != 3 && (alan_KOD < 20 || alan_KOD > 23))) hata_değer("arraycopy type mismatch");
                    else if (girdi_BAĞ_DEĞ_SAY < 0 || Start_konum < 0 || hedef_değer_Dizin < 0 || Start_konum > yığın_değer[첫값 + 1] - girdi_BAĞ_DEĞ_SAY || hedef_değer_Dizin > yığın_değer[bayt_veri + 1] - girdi_BAĞ_DEĞ_SAY) hata_değer("ArrayIndexOutOfBoundsException");
                    else if (첫값 == bayt_veri && hedef_değer_Dizin > Start_konum) { for (int Loop_Dizin = girdi_BAĞ_DEĞ_SAY - 1; Loop_Dizin >= 0; Loop_Dizin--) yığın_değer[bayt_veri + 2 + hedef_değer_Dizin + Loop_Dizin] = yığın_değer[첫값 + 2 + Start_konum + Loop_Dizin]; }
                    else { for (int Loop_Dizin = 0; Loop_Dizin < girdi_BAĞ_DEĞ_SAY && !hata; Loop_Dizin++) { int veri_değer = yığın_değer[첫값 + 2 + Start_konum + Loop_Dizin]; if (alan_KOD != 3 || 배열저장가능(bayt_veri, veri_değer)) yığın_değer[bayt_veri + 2 + hedef_değer_Dizin + Loop_Dizin] = veri_değer; } }
                }
                return true;
            }
        }
        if (Word_SMS(sahip, "java/util/ArrayList") || Word_SMS(sahip, "java/util/List") || Word_SMS(sahip, "java/util/HashMap") || Word_SMS(sahip, "java/util/Map")) {
            모음호출(sahip, ad_sabit, tanımlayıcı_sabit, komut_KOD); return true;
        }
        return false;
    }
    static void 모음늘리기(int nesne_Başvuru, int 필요수) {
        int Önceki_değer = yığın_değer[nesne_Başvuru + 2], kapasite_veri = Önceki_değer == 0 ? 0 : yığın_değer[Önceki_değer + 1];
        if (kapasite_veri >= 필요수) return;
        int Sonraki_konum = kapasite_veri < 8 ? 8 : kapasite_veri * 2; if (Sonraki_konum < 필요수) Sonraki_konum = 필요수;
        int veri_DİZİ = ayırmak_Depolama(3, Sonraki_konum); if (hata) return;
        for (int Loop_Dizin = 0; Loop_Dizin < kapasite_veri; Loop_Dizin++) yığın_değer[veri_DİZİ + 2 + Loop_Dizin] = yığın_değer[Önceki_değer + 2 + Loop_Dizin];
        yığın_değer[nesne_Başvuru + 2] = veri_DİZİ; yığın_Başvuru[nesne_Başvuru + 2] = 1;
    }
    static void 모음호출(int sahip, int ad_sabit, int tanımlayıcı_sabit, int komut_KOD) {
        boolean 대응참조 = Word_SMS(sahip, "java/util/HashMap") || Word_SMS(sahip, "java/util/Map"); int alan_KOD = 대응참조 ? 11 : 10;
        if (Word_SMS(ad_sabit, "<init>") && komut_KOD == 183 && Word_SMS(tanımlayıcı_sabit, "()V")) { int nesne_Başvuru = 빼기(2); if (nesne_değer(nesne_Başvuru, alan_KOD)) 모음늘리기(nesne_Başvuru, 8); return; }
        if (komut_KOD != 182 && komut_KOD != 185) { hata_değer("invalid collection invocation"); return; }
        if (Word_SMS(ad_sabit, "size") && Word_SMS(tanımlayıcı_sabit, "()I") || Word_SMS(ad_sabit, "isEmpty") && Word_SMS(tanımlayıcı_sabit, "()Z")) {
            int nesne_Başvuru = 빼기(2); if (nesne_değer(nesne_Başvuru, alan_KOD)) 넣기(Word_SMS(ad_sabit, "size") ? yığın_değer[nesne_Başvuru + 3] : yığın_değer[nesne_Başvuru + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(ad_sabit, "clear") && Word_SMS(tanımlayıcı_sabit, "()V")) { int nesne_Başvuru = 빼기(2); if (nesne_değer(nesne_Başvuru, alan_KOD)) { int veri_DİZİ = yığın_değer[nesne_Başvuru + 2]; for (int Loop_Dizin = 0; Loop_Dizin < yığın_değer[veri_DİZİ + 1]; Loop_Dizin++) yığın_değer[veri_DİZİ + 2 + Loop_Dizin] = 0; yığın_değer[nesne_Başvuru + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(ad_sabit, "add") && Word_SMS(tanımlayıcı_sabit, "(Ljava/lang/Object;)Z")) {
            int veri_değer = 빼기(2), nesne_Başvuru = 빼기(2); if (!nesne_değer(nesne_Başvuru, 10)) return;
            int girdi_BAĞ_DEĞ_SAY = yığın_değer[nesne_Başvuru + 3]; 모음늘리기(nesne_Başvuru, girdi_BAĞ_DEĞ_SAY + 1); if (!hata) { yığın_değer[yığın_değer[nesne_Başvuru + 2] + 2 + girdi_BAĞ_DEĞ_SAY] = veri_değer; yığın_değer[nesne_Başvuru + 3] = girdi_BAĞ_DEĞ_SAY + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(ad_sabit, "get") || Word_SMS(ad_sabit, "remove")) && Word_SMS(tanımlayıcı_sabit, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(ad_sabit, "set") && Word_SMS(tanımlayıcı_sabit, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean bilgi_teknolojisi_Atanmış = Word_SMS(ad_sabit, "set"); int veri_değer = bilgi_teknolojisi_Atanmış ? 빼기(2) : 0, girdi_konum = 빼기(1), nesne_Başvuru = 빼기(2);
            if (!nesne_değer(nesne_Başvuru, 10)) return;
            int girdi_BAĞ_DEĞ_SAY = yığın_değer[nesne_Başvuru + 3], veri_DİZİ = yığın_değer[nesne_Başvuru + 2];
            if (girdi_konum < 0 || girdi_konum >= girdi_BAĞ_DEĞ_SAY) { 예외던짐(6, "list index"); return; }
            int Önceki_değer = yığın_değer[veri_DİZİ + 2 + girdi_konum];
            if (bilgi_teknolojisi_Atanmış) yığın_değer[veri_DİZİ + 2 + girdi_konum] = veri_değer;
            if (Word_SMS(ad_sabit, "remove")) { for (int Loop_Dizin = girdi_konum + 1; Loop_Dizin < girdi_BAĞ_DEĞ_SAY; Loop_Dizin++) yığın_değer[veri_DİZİ + 1 + Loop_Dizin] = yığın_değer[veri_DİZİ + 2 + Loop_Dizin]; yığın_değer[veri_DİZİ + 1 + girdi_BAĞ_DEĞ_SAY] = 0; yığın_değer[nesne_Başvuru + 3] = girdi_BAĞ_DEĞ_SAY - 1; }
            넣기(Önceki_değer, 2); return;
        }
        if (대응참조 && (Word_SMS(ad_sabit, "get") || Word_SMS(ad_sabit, "remove")) && Word_SMS(tanımlayıcı_sabit, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(ad_sabit, "put") && Word_SMS(tanımlayıcı_sabit, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(ad_sabit, "containsKey") && Word_SMS(tanımlayıcı_sabit, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(ad_sabit, "put"), kaldırmak = Word_SMS(ad_sabit, "remove");
            int veri_değer = 넣기여부 ? 빼기(2) : 0, tuş_Başvuru = 빼기(2), nesne_Başvuru = 빼기(2); if (!nesne_değer(nesne_Başvuru, 11)) return;
            int girdi_BAĞ_DEĞ_SAY = yığın_değer[nesne_Başvuru + 3], veri_DİZİ = yığın_değer[nesne_Başvuru + 2], 찾은여부 = -1;
            for (int Loop_Dizin = 0; Loop_Dizin < girdi_BAĞ_DEĞ_SAY; Loop_Dizin++) if (값같음(tuş_Başvuru, yığın_değer[veri_DİZİ + 2 + 2 * Loop_Dizin])) { 찾은여부 = Loop_Dizin; break; }
            int Önceki_değer = 찾은여부 < 0 ? 0 : yığın_değer[veri_DİZİ + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(nesne_Başvuru, (girdi_BAĞ_DEĞ_SAY + 1) * 2); veri_DİZİ = yığın_değer[nesne_Başvuru + 2]; 찾은여부 = girdi_BAĞ_DEĞ_SAY; if (!hata) yığın_değer[nesne_Başvuru + 3] = girdi_BAĞ_DEĞ_SAY + 1; }
                if (!hata) { yığın_değer[veri_DİZİ + 2 + 2 * 찾은여부] = tuş_Başvuru; yığın_değer[veri_DİZİ + 3 + 2 * 찾은여부] = veri_değer; }
            }
            if (kaldırmak && 찾은여부 >= 0) { for (int Loop_Dizin = 찾은여부 + 1; Loop_Dizin < girdi_BAĞ_DEĞ_SAY; Loop_Dizin++) { yığın_değer[veri_DİZİ + 2 * Loop_Dizin] = yığın_değer[veri_DİZİ + 2 + 2 * Loop_Dizin]; yığın_değer[veri_DİZİ + 1 + 2 * Loop_Dizin] = yığın_değer[veri_DİZİ + 3 + 2 * Loop_Dizin]; } yığın_değer[veri_DİZİ + 2 * girdi_BAĞ_DEĞ_SAY] = 0; yığın_değer[veri_DİZİ + 1 + 2 * girdi_BAĞ_DEĞ_SAY] = 0; yığın_değer[nesne_Başvuru + 3] = girdi_BAĞ_DEĞ_SAY - 1; }
            if (Word_SMS(ad_sabit, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(Önceki_değer, 2);
            return;
        }
        hata_değer("unsupported collection method");
    }
    static boolean 잠금얻기(int nesne_Başvuru) {
        if (!bilgi_teknolojisi_geçerli_nesne(nesne_Başvuru)) return false;
        if (잠금깊이[nesne_Başvuru] != 0 && kilit_sahip[nesne_Başvuru] != geçerli_yazışma + 1) { değişiklik_isteği = true; return false; }
        kilit_sahip[nesne_Başvuru] = geçerli_yazışma + 1; 잠금깊이[nesne_Başvuru]++; return true;
    }
    static void sürüm_kilit(int nesne_Başvuru) {
        if (!bilgi_teknolojisi_geçerli_nesne(nesne_Başvuru)) return;
        if (잠금깊이[nesne_Başvuru] == 0 || kilit_sahip[nesne_Başvuru] != geçerli_yazışma + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[nesne_Başvuru] == 0) kilit_sahip[nesne_Başvuru] = 0;
    }
    static boolean geçiş_yazışma() {
        yazışma_kare[geçerli_yazışma] = kare_Dizin;
        if (kare_Dizin < geçerli_yazışma * 32) yazışma_Durum[geçerli_yazışma] = 3;
        for (int Loop_Dizin = 0; Loop_Dizin < yazışma_BAĞ_DEĞ_SAY; Loop_Dizin++) if (yazışma_Durum[Loop_Dizin] == 2 && yazışma_Durum[가닥대기[Loop_Dizin]] == 3) yazışma_Durum[Loop_Dizin] = 1;
        for (int Loop_Dizin = 1; Loop_Dizin <= yazışma_BAĞ_DEĞ_SAY; Loop_Dizin++) {
            int Sonraki_konum = (geçerli_yazışma + Loop_Dizin) % yazışma_BAĞ_DEĞ_SAY;
            if (yazışma_Durum[Sonraki_konum] == 1) { geçerli_yazışma = Sonraki_konum; kare_Dizin = yazışma_kare[Sonraki_konum]; değişiklik_isteği = false; return true; }
        }
        for (int Loop_Dizin = 0; Loop_Dizin < yazışma_BAĞ_DEĞ_SAY; Loop_Dizin++) if (yazışma_Durum[Loop_Dizin] != 3) { hata_değer("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int ad_sabit, int tanımlayıcı_sabit, int komut_KOD) { işlem_yazışma(ad_sabit, tanımlayıcı_sabit, komut_KOD, false); }
    static void işlem_yazışma(int ad_sabit, int tanımlayıcı_sabit, int komut_KOD, boolean Türkçe) {
        if (komut_KOD == 184 && Word_SMS(ad_sabit, Türkçe ? "ÖDEME_Görev" : "yield") && Word_SMS(tanımlayıcı_sabit, "()V")) { değişiklik_isteği = true; return; }
        if (komut_KOD == 184 && Word_SMS(ad_sabit, "currentThread") && Word_SMS(tanımlayıcı_sabit, "()Ljava/lang/Thread;")) { 넣기(yazışma_nesne[geçerli_yazışma], 2); return; }
        if (komut_KOD == 183 && Word_SMS(ad_sabit, "<init>") && (Word_SMS(tanımlayıcı_sabit, "()V") || Word_SMS(tanımlayıcı_sabit, Türkçe ? "(LTürkçe/Öz/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int hedef_ADRES = Word_SMS(tanımlayıcı_sabit, "()V") ? 0 : 빼기(2), nesne_Başvuru = 빼기(2);
            if (!bilgi_teknolojisi_geçerli_nesne(nesne_Başvuru)) return;
            if (yığın_değer[nesne_Başvuru] == 13) { yığın_değer[nesne_Başvuru + 2] = hedef_ADRES; yığın_Başvuru[nesne_Başvuru + 2] = 1; }
            else if (hedef_ADRES != 0) hata_değer("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (komut_KOD == 182 && (Word_SMS(ad_sabit, Türkçe ? "Start_Görev" : "start") || Word_SMS(ad_sabit, Türkçe ? "기다리기" : "join")) && Word_SMS(tanımlayıcı_sabit, "()V") || komut_KOD == 182 && Word_SMS(ad_sabit, Türkçe ? "살아있는가" : "isAlive") && Word_SMS(tanımlayıcı_sabit, "()Z")) {
            int nesne_Başvuru = 빼기(2); if (!bilgi_teknolojisi_geçerli_nesne(nesne_Başvuru)) return;
            int hesap_değer = -1; for (int Loop_Dizin = 0; Loop_Dizin < yazışma_BAĞ_DEĞ_SAY; Loop_Dizin++) if (yazışma_nesne[Loop_Dizin] == nesne_Başvuru) hesap_değer = Loop_Dizin;
            if (Word_SMS(ad_sabit, Türkçe ? "살아있는가" : "isAlive")) { 넣기(hesap_değer >= 0 && yazışma_Durum[hesap_değer] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(ad_sabit, Türkçe ? "기다리기" : "join")) { if (hesap_değer >= 0 && yazışma_Durum[hesap_değer] != 3) { 가닥대기[geçerli_yazışma] = hesap_değer; yazışma_Durum[geçerli_yazışma] = 2; değişiklik_isteği = true; } return; }
            if (hesap_değer >= 0) { 예외던짐(Türkçe ? 38 : 16, "thread already started"); return; }
            if (yazışma_BAĞ_DEĞ_SAY == 4) { hata_değer("thread limit (4 including main)"); return; }
            int hedef_ADRES = yığın_değer[nesne_Başvuru] == 13 ? yığın_değer[nesne_Başvuru + 2] : nesne_Başvuru;
            int Dosya_Dizin = hedef_ADRES > 0 && yığın_değer[hedef_ADRES] >= 32 ? ad_metot(yığın_değer[hedef_ADRES] - 32, Türkçe ? "Çalıştır" : "run", "()V") : -1;
            if (hedef_ADRES != 0 && Dosya_Dizin < 0) { hata_değer("Runnable.run required"); return; }
            hesap_değer = yazışma_BAĞ_DEĞ_SAY++; yazışma_nesne[hesap_değer] = nesne_Başvuru; yazışma_hedef[hesap_değer] = hedef_ADRES;
            int kare = hesap_değer * 32; yazışma_kare[hesap_değer] = Dosya_Dizin < 0 ? kare - 1 : kare; yazışma_Durum[hesap_değer] = Dosya_Dizin < 0 ? 3 : 1;
            if (Dosya_Dizin >= 0) { kare_metot[kare] = Dosya_Dizin; kare_konum[kare] = metot_Start[Dosya_Dizin]; yerel_değer[kare * 128] = hedef_ADRES; yerel_TÜR[kare * 128] = 2; }
            return;
        }
        hata_değer("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], ADRES_SMS = new int[16];
    static int yerel_ADRES() { return ADRES_nesne(0x7f000001); }
    static int ADRES_nesne(int değer) { int nesne_Başvuru = ayırmak_Depolama(14, 1); if (!hata) yığın_değer[nesne_Başvuru + 2] = değer; return nesne_Başvuru; }
    static int 주소해독(int nesne_Başvuru) {
        if (nesne_Başvuru == 0 || metinler_eşit(nesne_Başvuru, konak_karakter("localhost"), false)) return 0x7f000001;
        if (!nesne_değer(nesne_Başvuru, 1)) return 0;
        int veri_değer = 0, toplam_BAĞ_DEĞ_SAY = 0, ADRES_bayt = 0, 자릿수 = 0, girdi_BAĞ_DEĞ_SAY = yığın_değer[nesne_Başvuru + 1];
        for (int Loop_Dizin = 0; Loop_Dizin <= girdi_BAĞ_DEĞ_SAY; Loop_Dizin++) {
            int kod_noktası = Loop_Dizin == girdi_BAĞ_DEĞ_SAY ? '.' : yığın_değer[nesne_Başvuru + 2 + Loop_Dizin];
            if (kod_noktası == '.') { if (자릿수 == 0 || toplam_BAĞ_DEĞ_SAY == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } veri_değer = veri_değer << 8 | ADRES_bayt; toplam_BAĞ_DEĞ_SAY++; ADRES_bayt = 자릿수 = 0; }
            else { if (kod_noktası < '0' || kod_noktası > '9' || ++자릿수 > 3 || (ADRES_bayt = ADRES_bayt * 10 + kod_noktası - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (toplam_BAĞ_DEĞ_SAY != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return veri_değer;
    }
    static int ADRES_karakter(int veri_değer) {
        int girdi_BAĞ_DEĞ_SAY = 0;
        for (int kaydırmak = 24; kaydırmak >= 0; kaydırmak -= 8) {
            int ADRES_bayt = veri_değer >>> kaydırmak & 255;
            if (ADRES_bayt >= 100) ADRES_SMS[girdi_BAĞ_DEĞ_SAY++] = '0' + ADRES_bayt / 100;
            if (ADRES_bayt >= 10) ADRES_SMS[girdi_BAĞ_DEĞ_SAY++] = '0' + ADRES_bayt / 10 % 10;
            ADRES_SMS[girdi_BAĞ_DEĞ_SAY++] = '0' + ADRES_bayt % 10; if (kaydırmak != 0) ADRES_SMS[girdi_BAĞ_DEĞ_SAY++] = '.';
        }
        int nesne_Başvuru = ayırmak_Depolama(1, girdi_BAĞ_DEĞ_SAY); if (!hata) for (int Loop_Dizin = 0; Loop_Dizin < girdi_BAĞ_DEĞ_SAY; Loop_Dizin++) yığın_değer[nesne_Başvuru + 2 + Loop_Dizin] = ADRES_SMS[Loop_Dizin]; return nesne_Başvuru;
    }
    static void 통신호출(int sahip, int ad_sabit, int tanımlayıcı_sabit, int komut_KOD) {
        if (Word_SMS(sahip, "java/net/InetAddress")) {
            if (komut_KOD == 184 && Word_SMS(ad_sabit, "getLoopbackAddress") && Word_SMS(tanımlayıcı_sabit, "()Ljava/net/InetAddress;")) { 넣기(yerel_ADRES(), 2); return; }
            if (komut_KOD == 184 && Word_SMS(ad_sabit, "getByName") && Word_SMS(tanımlayıcı_sabit, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int veri_değer = 주소해독(빼기(2)); if (던진객체 == 0 && !hata) 넣기(ADRES_nesne(veri_değer), 2); return;
            }
            if (komut_KOD == 182 && Word_SMS(ad_sabit, "getHostAddress") && Word_SMS(tanımlayıcı_sabit, "()Ljava/lang/String;")) { int nesne_Başvuru = 빼기(2); if (nesne_değer(nesne_Başvuru, 14)) 넣기(ADRES_karakter(yığın_değer[nesne_Başvuru + 2]), 2); return; }
        }
        if (Word_SMS(sahip, "java/net/DatagramPacket")) {
            if (komut_KOD == 183 && Word_SMS(ad_sabit, "<init>") && (Word_SMS(tanımlayıcı_sabit, "([BI)V") || Word_SMS(tanımlayıcı_sabit, "([BILjava/net/InetAddress;I)V"))) {
                boolean hedef_değer_Başvuru = Word_SMS(tanımlayıcı_sabit, "([BILjava/net/InetAddress;I)V"); int bağlantı_noktası_numarası = hedef_değer_Başvuru ? 빼기(1) : 0, ADRES_Başvuru = hedef_değer_Başvuru ? 빼기(2) : 0;
                int girdi_BAĞ_DEĞ_SAY = 빼기(1), veri_DİZİ = 빼기(2), nesne_Başvuru = 빼기(2);
                if (!nesne_değer(nesne_Başvuru, 16) || !nesne_değer(veri_DİZİ, 20)) return;
                if (girdi_BAĞ_DEĞ_SAY < 0 || girdi_BAĞ_DEĞ_SAY > yığın_değer[veri_DİZİ + 1] || bağlantı_noktası_numarası < 0 || bağlantı_noktası_numarası > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (ADRES_Başvuru != 0 && !nesne_değer(ADRES_Başvuru, 14)) return;
                yığın_değer[nesne_Başvuru + 2] = veri_DİZİ; yığın_Başvuru[nesne_Başvuru + 2] = 1; yığın_değer[nesne_Başvuru + 3] = girdi_BAĞ_DEĞ_SAY;
                yığın_değer[nesne_Başvuru + 4] = ADRES_Başvuru; yığın_Başvuru[nesne_Başvuru + 4] = 1; yığın_değer[nesne_Başvuru + 5] = bağlantı_noktası_numarası; return;
            }
            if (komut_KOD == 182 && Word_SMS(ad_sabit, "setLength") && Word_SMS(tanımlayıcı_sabit, "(I)V")) {
                int girdi_BAĞ_DEĞ_SAY = 빼기(1), nesne_Başvuru = 빼기(2); if (!nesne_değer(nesne_Başvuru, 16)) return;
                if (girdi_BAĞ_DEĞ_SAY < 0 || girdi_BAĞ_DEĞ_SAY > yığın_değer[yığın_değer[nesne_Başvuru + 2] + 1]) 예외던짐(9, "invalid datagram length"); else yığın_değer[nesne_Başvuru + 3] = girdi_BAĞ_DEĞ_SAY; return;
            }
            if (komut_KOD == 182 && (Word_SMS(ad_sabit, "getData") && Word_SMS(tanımlayıcı_sabit, "()[B") || Word_SMS(ad_sabit, "getLength") && Word_SMS(tanımlayıcı_sabit, "()I") || Word_SMS(ad_sabit, "getAddress") && Word_SMS(tanımlayıcı_sabit, "()Ljava/net/InetAddress;") || Word_SMS(ad_sabit, "getPort") && Word_SMS(tanımlayıcı_sabit, "()I"))) {
                int nesne_Başvuru = 빼기(2); if (!nesne_değer(nesne_Başvuru, 16)) return;
                int girdi_konum = Word_SMS(ad_sabit, "getData") ? 2 : Word_SMS(ad_sabit, "getLength") ? 3 : Word_SMS(ad_sabit, "getAddress") ? 4 : 5;
                넣기(yığın_değer[nesne_Başvuru + girdi_konum], girdi_konum == 2 || girdi_konum == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(sahip, "java/net/DatagramSocket")) {
            if (komut_KOD == 183 && Word_SMS(ad_sabit, "<init>") && (Word_SMS(tanımlayıcı_sabit, "()V") || Word_SMS(tanımlayıcı_sabit, "(I)V"))) {
                int bağlantı_noktası_numarası = Word_SMS(tanımlayıcı_sabit, "()V") ? 0 : 빼기(1), nesne_Başvuru = 빼기(2); if (!nesne_değer(nesne_Başvuru, 15)) return;
                if (bağlantı_noktası_numarası < 0 || bağlantı_noktası_numarası > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = kullanıcı_alanı.açık_ağ(bağlantı_noktası_numarası); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else yığın_değer[nesne_Başvuru + 2] = 열린파일번호; return;
            }
            if (komut_KOD == 182 && Word_SMS(ad_sabit, "setSoTimeout") && Word_SMS(tanımlayıcı_sabit, "(I)V")) {
                int 밀리초값 = 빼기(1), nesne_Başvuru = 빼기(2); if (!nesne_değer(nesne_Başvuru, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else yığın_değer[nesne_Başvuru + 3] = 밀리초값; return;
            }
            if (komut_KOD == 182 && Word_SMS(ad_sabit, "getLocalPort") && Word_SMS(tanımlayıcı_sabit, "()I")) { int nesne_Başvuru = 빼기(2); if (nesne_değer(nesne_Başvuru, 15)) 넣기(yığın_değer[nesne_Başvuru + 2] < 0 ? -1 : kullanıcı_alanı.ağ_taşımak(yığın_değer[nesne_Başvuru + 2]), 1); return; }
            if (komut_KOD == 182 && Word_SMS(ad_sabit, "isClosed") && Word_SMS(tanımlayıcı_sabit, "()Z")) { int nesne_Başvuru = 빼기(2); if (nesne_değer(nesne_Başvuru, 15)) 넣기(yığın_değer[nesne_Başvuru + 2] < 0 ? 1 : 0, 1); return; }
            if (komut_KOD == 182 && Word_SMS(ad_sabit, "close") && Word_SMS(tanımlayıcı_sabit, "()V")) { int nesne_Başvuru = 빼기(2); if (nesne_değer(nesne_Başvuru, 15) && yığın_değer[nesne_Başvuru + 2] >= 0) { kullanıcı_alanı.Kapat_Dosya_tanımlayıcı(yığın_değer[nesne_Başvuru + 2]); yığın_değer[nesne_Başvuru + 2] = -1; } return; }
            if (komut_KOD == 182 && (Word_SMS(ad_sabit, "send") || Word_SMS(ad_sabit, "receive")) && Word_SMS(tanımlayıcı_sabit, "(Ljava/net/DatagramPacket;)V")) {
                int paket = 빼기(2), nesne_Başvuru = 빼기(2); if (!nesne_değer(paket, 16) || !nesne_değer(nesne_Başvuru, 15)) return;
                int veri_DİZİ = yığın_değer[paket + 2], geçerli_süre = yığın_değer[paket + 3], 열린파일번호 = yığın_değer[nesne_Başvuru + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(ad_sabit, "send")) {
                    if (!nesne_değer(yığın_değer[paket + 4], 14)) return;
                    if (geçerli_süre > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_Dizin = 0; Loop_Dizin < geçerli_süre; Loop_Dizin++) 통신임시[Loop_Dizin] = yığın_değer[veri_DİZİ + 2 + Loop_Dizin];
                    if (kullanıcı_alanı.göndermek_ağ(열린파일번호, yığın_değer[yığın_değer[paket + 4] + 2], yığın_değer[paket + 5], 통신임시, geçerli_süre) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int girdi_BAĞ_DEĞ_SAY = kullanıcı_alanı.almak_ağ(열린파일번호, 통신임시, geçerli_süre > 512 ? 512 : geçerli_süre);
                    if (girdi_BAĞ_DEĞ_SAY == -11) {
                        int geçerli_zaman = kullanıcı_alanı.밀리초();
                        if (yığın_değer[nesne_Başvuru + 4] == 0) yığın_değer[nesne_Başvuru + 4] = geçerli_zaman + 1;
                        if (yığın_değer[nesne_Başvuru + 3] > 0 && geçerli_zaman - (yığın_değer[nesne_Başvuru + 4] - 1) >= yığın_değer[nesne_Başvuru + 3]) { yığın_değer[nesne_Başvuru + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(nesne_Başvuru, 2); 넣기(paket, 2); kare_konum[kare_Dizin] = 틀명령[kare_Dizin]; değişiklik_isteği = true; return;
                    }
                    yığın_değer[nesne_Başvuru + 4] = 0;
                    if (girdi_BAĞ_DEĞ_SAY < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_Dizin = 0; Loop_Dizin < girdi_BAĞ_DEĞ_SAY; Loop_Dizin++) yığın_değer[veri_DİZİ + 2 + Loop_Dizin] = (byte)통신임시[Loop_Dizin];
                    yığın_değer[paket + 3] = girdi_BAĞ_DEĞ_SAY; yığın_değer[paket + 4] = ADRES_nesne(통신임시[513]); yığın_Başvuru[paket + 4] = 1; yığın_değer[paket + 5] = 통신임시[512];
                }
                return;
            }
        }
        hata_değer("unsupported java.net method");
    }
    static boolean 흐름대기(int nesne_Başvuru) {
        int geçerli_zaman = kullanıcı_alanı.밀리초();
        if (yığın_değer[nesne_Başvuru + 5] == 0) yığın_değer[nesne_Başvuru + 5] = geçerli_zaman + 1;
        if (yığın_değer[nesne_Başvuru + 3] > 0 && geçerli_zaman - (yığın_değer[nesne_Başvuru + 5] - 1) >= yığın_değer[nesne_Başvuru + 3]) { yığın_değer[nesne_Başvuru + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        kare_konum[kare_Dizin] = 틀명령[kare_Dizin]; değişiklik_isteği = true; return true;
    }
    static void 흐름호출(int sahip, int ad_sabit, int tanımlayıcı_sabit, int komut_KOD) {
        boolean almak_sayfa = Word_SMS(sahip, "java/net/ServerSocket"), akış = Word_SMS(sahip, "java/io/InputStream") || Word_SMS(sahip, "java/io/OutputStream");
        if (!akış && komut_KOD == 183 && Word_SMS(ad_sabit, "<init>")) {
            boolean bilgi_teknolojisi_boş_Durum = Word_SMS(tanımlayıcı_sabit, "()V"), 이름지정여부 = Word_SMS(tanımlayıcı_sabit, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(tanımlayıcı_sabit, "(Ljava/net/InetAddress;I)V");
            if (!(bilgi_teknolojisi_boş_Durum || almak_sayfa && Word_SMS(tanımlayıcı_sabit, "(I)V") || !almak_sayfa && (이름지정여부 || 주소지정여부))) { hata_değer("unsupported socket constructor"); return; }
            int bağlantı_noktası_numarası = bilgi_teknolojisi_boş_Durum ? 0 : 빼기(1), ADRES_Başvuru = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, nesne_Başvuru = 빼기(2);
            if (!nesne_değer(nesne_Başvuru, almak_sayfa ? 18 : 17)) return;
            if (bağlantı_noktası_numarası < 0 || bağlantı_noktası_numarası > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !nesne_değer(ADRES_Başvuru, 14)) return;
            int ağ_kimliği = 이름지정여부 ? 주소해독(ADRES_Başvuru) : 주소지정여부 ? yığın_değer[ADRES_Başvuru + 2] : 0x7f000001;
            if (hata || 던진객체 != 0) return;
            int 열린파일번호 = kullanıcı_alanı.akış_denetim(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = bilgi_teknolojisi_boş_Durum ? 0 : almak_sayfa ? kullanıcı_alanı.akış_denetim(1, 열린파일번호, bağlantı_noktası_numarası) : kullanıcı_alanı.bağla_akış(열린파일번호, ağ_kimliği, bağlantı_noktası_numarası);
            if (처리값 < 0) { kullanıcı_alanı.Kapat_Dosya_tanımlayıcı(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            yığın_değer[nesne_Başvuru + 2] = 열린파일번호; yığın_değer[nesne_Başvuru + 4] = bağlantı_noktası_numarası; yığın_değer[nesne_Başvuru + 6] = bilgi_teknolojisi_boş_Durum ? 0 : 1; return;
        }
        if (!akış && Word_SMS(ad_sabit, "setSoTimeout") && Word_SMS(tanımlayıcı_sabit, "(I)V")) { int 밀리초값 = 빼기(1), nesne_Başvuru = 빼기(2); if (!nesne_değer(nesne_Başvuru, almak_sayfa ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else yığın_değer[nesne_Başvuru + 3] = 밀리초값; return; }
        if (!akış && Word_SMS(ad_sabit, "close") && Word_SMS(tanımlayıcı_sabit, "()V")) { int nesne_Başvuru = 빼기(2); if (nesne_değer(nesne_Başvuru, almak_sayfa ? 18 : 17) && yığın_değer[nesne_Başvuru + 2] >= 0) { kullanıcı_alanı.Kapat_Dosya_tanımlayıcı(yığın_değer[nesne_Başvuru + 2]); yığın_değer[nesne_Başvuru + 2] = -1; } return; }
        if (!akış && (Word_SMS(ad_sabit, "getLocalPort") || Word_SMS(ad_sabit, "getPort") || Word_SMS(ad_sabit, "isClosed") || Word_SMS(ad_sabit, "isConnected"))) {
            int nesne_Başvuru = 빼기(2); if (!nesne_değer(nesne_Başvuru, almak_sayfa ? 18 : 17)) return;
            넣기(Word_SMS(ad_sabit, "isClosed") ? yığın_değer[nesne_Başvuru + 2] < 0 ? 1 : 0 : Word_SMS(ad_sabit, "isConnected") ? yığın_değer[nesne_Başvuru + 6] : Word_SMS(ad_sabit, "getPort") ? yığın_değer[nesne_Başvuru + 4] : yığın_değer[nesne_Başvuru + 2] < 0 ? -1 : kullanıcı_alanı.akış_denetim(4, yığın_değer[nesne_Başvuru + 2], 0), 1); return;
        }
        if (almak_sayfa && Word_SMS(ad_sabit, "accept") && Word_SMS(tanımlayıcı_sabit, "()Ljava/net/Socket;")) {
            int nesne_Başvuru = 빼기(2); if (!nesne_değer(nesne_Başvuru, 18)) return; int 열린파일번호 = kullanıcı_alanı.akış_denetim(3, yığın_değer[nesne_Başvuru + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(nesne_Başvuru)) 넣기(nesne_Başvuru, 2); return; }
            yığın_değer[nesne_Başvuru + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = ayırmak_Depolama(17, 5); if (hata) { kullanıcı_alanı.Kapat_Dosya_tanımlayıcı(열린파일번호); return; } yığın_değer[반환값 + 2] = 열린파일번호; yığın_değer[반환값 + 4] = kullanıcı_alanı.akış_denetim(5, 열린파일번호, 0); yığın_değer[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!almak_sayfa && !akış && ((Word_SMS(ad_sabit, "getInputStream") && Word_SMS(tanımlayıcı_sabit, "()Ljava/io/InputStream;")) || (Word_SMS(ad_sabit, "getOutputStream") && Word_SMS(tanımlayıcı_sabit, "()Ljava/io/OutputStream;")))) {
            int nesne_Başvuru = 빼기(2); if (!nesne_değer(nesne_Başvuru, 17)) return; if (yığın_değer[nesne_Başvuru + 2] < 0 || yığın_değer[nesne_Başvuru + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = ayırmak_Depolama(19, 4); if (hata) return; yığın_değer[반환값 + 2] = nesne_Başvuru; yığın_Başvuru[반환값 + 2] = 1; yığın_değer[반환값 + 3] = Word_SMS(ad_sabit, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (akış) {
            boolean 읽기여부 = Word_SMS(ad_sabit, "read"), bilgi_teknolojisi_yazma_işlem = Word_SMS(ad_sabit, "write"), blok = Word_SMS(tanımlayıcı_sabit, "([B)I") || Word_SMS(tanımlayıcı_sabit, "([B)V"), bilgi_teknolojisi_ALTDİZİ = Word_SMS(tanımlayıcı_sabit, "([BII)I") || Word_SMS(tanımlayıcı_sabit, "([BII)V");
            int girdi_BAĞ_DEĞ_SAY = bilgi_teknolojisi_ALTDİZİ ? 빼기(1) : 0, 시작변위 = bilgi_teknolojisi_ALTDİZİ ? 빼기(1) : 0, veri_DİZİ = blok || bilgi_teknolojisi_ALTDİZİ ? 빼기(2) : 0;
            int veri_değer = bilgi_teknolojisi_yazma_işlem && Word_SMS(tanımlayıcı_sabit, "(I)V") ? 빼기(1) : 0, nesne_Başvuru = 빼기(2);
            if (!nesne_değer(nesne_Başvuru, 19)) return; int ana_Başvuru = yığın_değer[nesne_Başvuru + 2], 열린파일번호 = yığın_değer[ana_Başvuru + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(ad_sabit, "close") && Word_SMS(tanımlayıcı_sabit, "()V")) { kullanıcı_alanı.Kapat_Dosya_tanımlayıcı(열린파일번호); yığın_değer[ana_Başvuru + 2] = -1; return; }
            if (Word_SMS(ad_sabit, "flush") && Word_SMS(tanımlayıcı_sabit, "()V")) return;
            if ((!읽기여부 && !bilgi_teknolojisi_yazma_işlem) || 읽기여부 != (yığın_değer[nesne_Başvuru + 3] == 0)) { hata_değer("unsupported stream operation"); return; }
            if (blok || bilgi_teknolojisi_ALTDİZİ) { if (!nesne_değer(veri_DİZİ, 20)) return; if (blok) girdi_BAĞ_DEĞ_SAY = yığın_değer[veri_DİZİ + 1]; if (시작변위 < 0 || girdi_BAĞ_DEĞ_SAY < 0 || 시작변위 > yığın_değer[veri_DİZİ + 1] - girdi_BAĞ_DEĞ_SAY) { 예외던짐(6, "stream array bounds"); return; } }
            else girdi_BAĞ_DEĞ_SAY = 1;
            if (girdi_BAĞ_DEĞ_SAY == 0) { if (읽기여부) 넣기(0, 1); return; }
            int Bitenler_BAĞ_DEĞ_SAY = bilgi_teknolojisi_yazma_işlem ? yığın_değer[nesne_Başvuru + 4] : 0, 처리값 = 0;
            while (Bitenler_BAĞ_DEĞ_SAY < girdi_BAĞ_DEĞ_SAY) {
                처리값 = 읽기여부 ? kullanıcı_alanı.파일한바이트읽기(열린파일번호) : kullanıcı_alanı.파일한바이트쓰기(열린파일번호, blok || bilgi_teknolojisi_ALTDİZİ ? yığın_değer[veri_DİZİ + 2 + 시작변위 + Bitenler_BAĞ_DEĞ_SAY] : veri_değer);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (blok || bilgi_teknolojisi_ALTDİZİ)) yığın_değer[veri_DİZİ + 2 + 시작변위 + Bitenler_BAĞ_DEĞ_SAY] = (byte)처리값;
                Bitenler_BAĞ_DEĞ_SAY++; if (읽기여부 && !(blok || bilgi_teknolojisi_ALTDİZİ)) break;
            }
            if (처리값 == -11 && (bilgi_teknolojisi_yazma_işlem || Bitenler_BAĞ_DEĞ_SAY == 0)) {
                yığın_değer[nesne_Başvuru + 4] = Bitenler_BAĞ_DEĞ_SAY;
                if (흐름대기(ana_Başvuru)) { 넣기(nesne_Başvuru, 2); if (blok || bilgi_teknolojisi_ALTDİZİ) 넣기(veri_DİZİ, 2); if (bilgi_teknolojisi_ALTDİZİ) { 넣기(시작변위, 1); 넣기(girdi_BAĞ_DEĞ_SAY, 1); } if (bilgi_teknolojisi_yazma_işlem && !(blok || bilgi_teknolojisi_ALTDİZİ)) 넣기(veri_değer, 1); } return;
            }
            yığın_değer[nesne_Başvuru + 4] = 0; yığın_değer[ana_Başvuru + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(Bitenler_BAĞ_DEĞ_SAY == 0 && 처리값 == 256 ? -1 : blok || bilgi_teknolojisi_ALTDİZİ ? Bitenler_BAĞ_DEĞ_SAY : 처리값, 1); return;
        }
        hata_değer("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int ad_sabit) {
        if (Word_SMS(ad_sabit, "Türkçe/Öz/Pencere")) return 24;
        if (Word_SMS(ad_sabit, "Türkçe/Öz/Etiket")) return 26;
        if (Word_SMS(ad_sabit, "Türkçe/Öz/düğme")) return 27;
        if (Word_SMS(ad_sabit, "Türkçe/Öz/metin_alanı")) return 28;
        if (Word_SMS(ad_sabit, "Türkçe/Öz/Eylem_uyarı")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int ad_sabit) {
        return 한국어화면종(ad_sabit) != 0 || Word_SMS(ad_sabit, "Türkçe/Öz/화면구성요소") || Word_SMS(ad_sabit, "Türkçe/Öz/olay_sıra");
    }
    static int 화면종(int ad_sabit) {
        int 한국어종 = 한국어화면종(ad_sabit); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(ad_sabit, "javax/swing/JFrame")) return 24;
        if (Word_SMS(ad_sabit, "javax/swing/JPanel")) return 25;
        if (Word_SMS(ad_sabit, "javax/swing/JLabel")) return 26;
        if (Word_SMS(ad_sabit, "javax/swing/JButton")) return 27;
        if (Word_SMS(ad_sabit, "javax/swing/JTextField")) return 28;
        if (Word_SMS(ad_sabit, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(ad_sabit, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int ad_sabit) {
        return 화면종(ad_sabit) != 0 || Word_SMS(ad_sabit, "java/awt/Component") || Word_SMS(ad_sabit, "java/awt/Container") || Word_SMS(ad_sabit, "javax/swing/JComponent") || Word_SMS(ad_sabit, "javax/swing/AbstractButton") || Word_SMS(ad_sabit, "javax/swing/text/JTextComponent") || Word_SMS(ad_sabit, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int nesne_Başvuru) { if (!bilgi_teknolojisi_geçerli_nesne(nesne_Başvuru)) return false; if (yığın_değer[nesne_Başvuru] < 24 || yığın_değer[nesne_Başvuru] > 28) { hata_değer("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int nesne_Başvuru, int SMS_Başvuru) {
        if (SMS_Başvuru != 0 && !nesne_değer(SMS_Başvuru, 1)) return;
        int girdi_BAĞ_DEĞ_SAY = SMS_Başvuru == 0 ? 0 : yığın_değer[SMS_Başvuru + 1]; if (girdi_BAĞ_DEĞ_SAY > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_Dizin = 0; Loop_Dizin < girdi_BAĞ_DEĞ_SAY; Loop_Dizin++) 화면글임시[Loop_Dizin] = yığın_değer[SMS_Başvuru + 2 + Loop_Dizin];
        if (kullanıcı_alanı.화면글(yığın_değer[nesne_Başvuru + 2], 화면글임시, girdi_BAĞ_DEĞ_SAY) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        yığın_değer[nesne_Başvuru + 3] = SMS_Başvuru; yığın_Başvuru[nesne_Başvuru + 3] = 1;
    }
    static int 화면문자읽기(int nesne_Başvuru) {
        int hesap_değer = yığın_değer[nesne_Başvuru + 2], girdi_BAĞ_DEĞ_SAY = kullanıcı_alanı.화면연결(8, hesap_değer, 0, 0, 0, 0), 사용수 = 0;
        if (girdi_BAĞ_DEĞ_SAY < 0) { hata_değer("GUI text read failed"); return 0; }
        for (int Loop_Dizin = 0; Loop_Dizin < girdi_BAĞ_DEĞ_SAY; Loop_Dizin++) { int 부호값 = kullanıcı_alanı.화면연결(9, hesap_değer, Loop_Dizin, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = ayırmak_Depolama(1, 사용수); if (!hata) for (int Loop_Dizin = 0; Loop_Dizin < 사용수; Loop_Dizin++) yığın_değer[반환값 + 2 + Loop_Dizin] = 화면글임시[Loop_Dizin]; return 반환값;
    }
    /* Türkçe 객체를 직접 만들고 çekirdek_değer 화면 기능에 연결한다. Swing nesne_değer/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int sahip, int ad_sabit, int tanımlayıcı_sabit, int komut_KOD) {
        if (Word_SMS(sahip, "Türkçe/Öz/olay_sıra")) {
            if (komut_KOD == 184 && Word_SMS(ad_sabit, "나중에실행") && Word_SMS(tanımlayıcı_sabit, "(LTürkçe/Öz/실행할일;)V")) {
                int Görev_Eylem = 빼기(2); if (!bilgi_teknolojisi_geçerli_nesne(Görev_Eylem)) return;
                if (나중수 == 8) { hata_değer("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = Görev_Eylem; return;
            }
            if (komut_KOD == 184 && Word_SMS(ad_sabit, "사건처리중인가") && Word_SMS(tanımlayıcı_sabit, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            hata_değer("지원하지 않는 Türkçe 화면 일정 호출"); return;
        }
        if (Word_SMS(sahip, "Türkçe/Öz/Eylem_uyarı")) {
            int uyarı = 빼기(2); if (!nesne_değer(uyarı, 29) || yığın_değer[uyarı + 3] == 0) return;
            if (Word_SMS(ad_sabit, "olay_kaynağı") && Word_SMS(tanımlayıcı_sabit, "()LTürkçe/Öz/화면구성요소;")) 넣기(yığın_değer[uyarı + 2], 2);
            else if (Word_SMS(ad_sabit, "komut_SMS") && Word_SMS(tanımlayıcı_sabit, "()Ljava/lang/String;")) 넣기(화면문자읽기(yığın_değer[uyarı + 2]), 2);
            else if (Word_SMS(ad_sabit, "Dizin") && Word_SMS(tanımlayıcı_sabit, "()I")) 넣기(1001, 1);
            else hata_değer("지원하지 않는 Türkçe Eylem uyarı 호출"); return;
        }
        if (komut_KOD == 183 && Word_SMS(ad_sabit, "<init>")) {
            int Tip_değer = 한국어화면종(sahip), 받이 = 0, 가로 = 0, Dikey_konum = 0, 폭 = 0, 높이 = 0;
            if (Tip_değer == 24 && Word_SMS(tanımlayıcı_sabit, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (kullanıcı_alanı.화면너비() - 폭) / 2; Dikey_konum = (kullanıcı_alanı.화면높이() - 높이) / 2;
            } else if ((Tip_değer == 26 || Tip_değer == 28) && Word_SMS(tanımlayıcı_sabit, "(Ljava/lang/String;IIII)V") || Tip_değer == 27 && Word_SMS(tanımlayıcı_sabit, "(Ljava/lang/String;IIIILTürkçe/Öz/동작받이;)V")) {
                if (Tip_değer == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Dikey_konum = 빼기(1); 가로 = 빼기(1);
            } else { hata_değer("지원하지 않는 Türkçe 화면 생성자"); return; }
            int metin = 빼기(2), öğe_değer = 빼기(2); if (!화면객체(öğe_değer)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Dikey_konum < 0 || 폭 > kullanıcı_alanı.화면너비() - 가로 || 높이 > kullanıcı_alanı.화면높이() - Dikey_konum) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int Dizin = kullanıcı_alanı.화면연결(0, Tip_değer - 23, 0, 0, 0, 0);
            if (Dizin < 1 || Dizin > 32) { hata_değer("화면 öğe_değer 자리가 가득 찼습니다"); return; }
            yığın_değer[öğe_değer + 2] = Dizin; 화면참조[Dizin - 1] = öğe_değer;
            yığın_değer[öğe_değer + 5] = 가로; yığın_değer[öğe_değer + 6] = Dikey_konum; yığın_değer[öğe_değer + 7] = 폭; yığın_değer[öğe_değer + 8] = 높이; yığın_değer[öğe_değer + 10] = 2;
            yığın_değer[öğe_değer + 4] = 받이; yığın_Başvuru[öğe_değer + 4] = 1; yığın_değer[öğe_değer + 12] = 1;
            kullanıcı_alanı.화면연결(1, Dizin, 가로, Dikey_konum, 폭, 높이);
            if (Tip_değer == 24) kullanıcı_alanı.화면연결(7, Dizin, 2, 0, 0, 0);
            화면문자설정(öğe_değer, metin); return;
        }
        if (komut_KOD != 182) { hata_değer("잘못된 Türkçe 화면 호출 komut"); return; }
        if (Word_SMS(ad_sabit, "yazma_SMS") && Word_SMS(tanımlayıcı_sabit, "(Ljava/lang/String;)V")) {
            int metin = 빼기(2), öğe_değer = 빼기(2); if (화면객체(öğe_değer)) 화면문자설정(öğe_değer, metin); return;
        }
        if (Word_SMS(ad_sabit, "글읽기") && Word_SMS(tanımlayıcı_sabit, "()Ljava/lang/String;")) {
            int öğe_değer = 빼기(2); if (화면객체(öğe_değer)) 넣기(화면문자읽기(öğe_değer), 2); return;
        }
        if (Word_SMS(ad_sabit, "동작맡기기") && Word_SMS(tanımlayıcı_sabit, "(LTürkçe/Öz/동작받이;)V")) {
            int 받이 = 빼기(2), öğe_değer = 빼기(2);
            if (화면객체(öğe_değer)) { yığın_değer[öğe_değer + 4] = 받이; yığın_Başvuru[öğe_değer + 4] = 1; yığın_değer[öğe_değer + 12] = 1; } return;
        }
        if (Word_SMS(ad_sabit, "Ekle_öğe") && Word_SMS(tanımlayıcı_sabit, "(LTürkçe/Öz/화면구성요소;)V")) {
            int alt_değer = 빼기(2), ana_değer = 빼기(2); if (!화면객체(alt_değer) || !화면객체(ana_değer)) return;
            if (kullanıcı_alanı.화면연결(2, yığın_değer[ana_değer + 2], yığın_değer[alt_değer + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            yığın_değer[alt_değer + 11] = ana_değer; yığın_Başvuru[alt_değer + 11] = 1; return;
        }
        if (Word_SMS(ad_sabit, "자리정하기") && Word_SMS(tanımlayıcı_sabit, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Dikey_konum = 빼기(1), 가로 = 빼기(1), öğe_değer = 빼기(2); if (!화면객체(öğe_değer)) return;
            if (kullanıcı_alanı.화면연결(1, yığın_değer[öğe_değer + 2], 가로, Dikey_konum, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            yığın_değer[öğe_değer + 5] = 가로; yığın_değer[öğe_değer + 6] = Dikey_konum; yığın_değer[öğe_değer + 7] = 폭; yığın_değer[öğe_değer + 8] = 높이; return;
        }
        if ((Word_SMS(ad_sabit, "şov_pencere") || Word_SMS(ad_sabit, "Kapat")) && Word_SMS(tanımlayıcı_sabit, "()V")) {
            boolean Görünürlük_değer = Word_SMS(ad_sabit, "şov_pencere"); int öğe_değer = 빼기(2); if (!화면객체(öğe_değer)) return;
            if (kullanıcı_alanı.화면연결(Görünürlük_değer ? 3 : 4, yığın_değer[öğe_değer + 2], Görünürlük_değer ? 1 : 0, 0, 0, 0) < 0) { hata_değer("화면은 devralmak 명령에서 실행해야 합니다"); return; }
            yığın_değer[öğe_değer + 9] = Görünürlük_değer ? 1 : 0; return;
        }
        if (Word_SMS(ad_sabit, "보이는가") && Word_SMS(tanımlayıcı_sabit, "()Z")) { int öğe_değer = 빼기(2); if (화면객체(öğe_değer)) 넣기(yığın_değer[öğe_değer + 9], 1); return; }
        hata_değer("지원하지 않는 Türkçe 화면 metot_değer");
    }
    static void 화면호출(int sahip, int ad_sabit, int tanımlayıcı_sabit, int komut_KOD) {
        if (Word_SMS(sahip, "javax/swing/SwingUtilities")) {
            if (komut_KOD == 184 && Word_SMS(ad_sabit, "invokeLater") && Word_SMS(tanımlayıcı_sabit, "(Ljava/lang/Runnable;)V")) { int nesne_Başvuru = 빼기(2); if (!bilgi_teknolojisi_geçerli_nesne(nesne_Başvuru)) return; if (나중수 == 8) { hata_değer("invokeLater queue full"); return; } 나중실행[나중수++] = nesne_Başvuru; return; }
            if (komut_KOD == 184 && Word_SMS(ad_sabit, "isEventDispatchThread") && Word_SMS(tanımlayıcı_sabit, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            hata_değer("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(sahip, "java/awt/event/ActionEvent")) {
            int nesne_Başvuru = 빼기(2); if (!nesne_değer(nesne_Başvuru, 29)) return;
            if (Word_SMS(ad_sabit, "getSource") && Word_SMS(tanımlayıcı_sabit, "()Ljava/lang/Object;")) 넣기(yığın_değer[nesne_Başvuru + 2], 2);
            else if (Word_SMS(ad_sabit, "getActionCommand") && Word_SMS(tanımlayıcı_sabit, "()Ljava/lang/String;")) 넣기(화면문자읽기(yığın_değer[nesne_Başvuru + 2]), 2);
            else if (Word_SMS(ad_sabit, "getID") && Word_SMS(tanımlayıcı_sabit, "()I")) 넣기(1001, 1);
            else hata_değer("unsupported ActionEvent method"); return;
        }
        if (komut_KOD == 183 && Word_SMS(ad_sabit, "<init>")) {
            int SÜTUNSAY = 0, SMS_Başvuru = 0;
            if (Word_SMS(tanımlayıcı_sabit, "(I)V")) SÜTUNSAY = 빼기(1);
            else if (Word_SMS(tanımlayıcı_sabit, "(Ljava/lang/String;I)V")) { SÜTUNSAY = 빼기(1); SMS_Başvuru = 빼기(2); }
            else if (Word_SMS(tanımlayıcı_sabit, "(Ljava/lang/String;)V")) SMS_Başvuru = 빼기(2);
            else if (Word_SMS(tanımlayıcı_sabit, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(tanımlayıcı_sabit, "()V")) { hata_değer("unsupported Swing constructor"); return; }
            int nesne_Başvuru = 빼기(2); if (!bilgi_teknolojisi_geçerli_nesne(nesne_Başvuru)) return;
            if (yığın_değer[nesne_Başvuru] == 30) { hata_değer("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(nesne_Başvuru) || SÜTUNSAY < 0) return;
            int hesap_değer = kullanıcı_alanı.화면연결(0, yığın_değer[nesne_Başvuru] - 23, 0, 0, 0, 0);
            if (hesap_değer < 1 || hesap_değer > 32) { hata_değer("GUI widget slots exhausted"); return; }
            yığın_değer[nesne_Başvuru + 2] = hesap_değer; 화면참조[hesap_değer - 1] = nesne_Başvuru; yığın_değer[nesne_Başvuru + 5] = yığın_değer[nesne_Başvuru] == 24 ? 130 : 16; yığın_değer[nesne_Başvuru + 6] = yığın_değer[nesne_Başvuru] == 24 ? 110 : 16;
            yığın_değer[nesne_Başvuru + 7] = yığın_değer[nesne_Başvuru] == 24 ? 380 : 220; yığın_değer[nesne_Başvuru + 8] = yığın_değer[nesne_Başvuru] == 24 ? 240 : 28; yığın_değer[nesne_Başvuru + 10] = 1;
            화면문자설정(nesne_Başvuru, SMS_Başvuru); return;
        }
        if (Word_SMS(ad_sabit, "setText") || Word_SMS(ad_sabit, "setTitle")) { int SMS_Başvuru = 빼기(2), nesne_Başvuru = 빼기(2); if (화면객체(nesne_Başvuru) && Word_SMS(tanımlayıcı_sabit, "(Ljava/lang/String;)V")) 화면문자설정(nesne_Başvuru, SMS_Başvuru); return; }
        if (Word_SMS(ad_sabit, "getText") || Word_SMS(ad_sabit, "getTitle")) { int nesne_Başvuru = 빼기(2); if (화면객체(nesne_Başvuru) && Word_SMS(tanımlayıcı_sabit, "()Ljava/lang/String;")) 넣기(화면문자읽기(nesne_Başvuru), 2); return; }
        if (Word_SMS(ad_sabit, "addActionListener") && Word_SMS(tanımlayıcı_sabit, "(Ljava/awt/event/ActionListener;)V")) { int almak_Başvuru = 빼기(2), nesne_Başvuru = 빼기(2); if (화면객체(nesne_Başvuru)) { yığın_değer[nesne_Başvuru + 4] = almak_Başvuru; yığın_Başvuru[nesne_Başvuru + 4] = 1; } return; }
        if (Word_SMS(ad_sabit, "getContentPane") && Word_SMS(tanımlayıcı_sabit, "()Ljava/awt/Container;")) { int nesne_Başvuru = 빼기(2); if (화면객체(nesne_Başvuru)) 넣기(nesne_Başvuru, 2); return; }
        if (Word_SMS(ad_sabit, "setLayout") && Word_SMS(tanımlayıcı_sabit, "(Ljava/awt/LayoutManager;)V")) { int Düzen_Başvuru = 빼기(2), nesne_Başvuru = 빼기(2); if (화면객체(nesne_Başvuru) && Düzen_Başvuru != 0) hata_değer("only absolute layout (null) is supported"); return; }
        if (Word_SMS(ad_sabit, "add") && (Word_SMS(tanımlayıcı_sabit, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(tanımlayıcı_sabit, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Düzen_koşul = Word_SMS(tanımlayıcı_sabit, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Düzen_koşul) 빼기(2);
            int alt_Başvuru = 빼기(2), nesne_Başvuru = 빼기(2); if (!화면객체(alt_Başvuru) || !화면객체(nesne_Başvuru)) return;
            if (kullanıcı_alanı.화면연결(2, yığın_değer[nesne_Başvuru + 2], yığın_değer[alt_Başvuru + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            yığın_değer[alt_Başvuru + 11] = nesne_Başvuru; yığın_Başvuru[alt_Başvuru + 11] = 1; if (!Düzen_koşul) 넣기(alt_Başvuru, 2); return;
        }
        if (Word_SMS(ad_sabit, "setBounds") && Word_SMS(tanımlayıcı_sabit, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinat = 빼기(1), x_koordinatı = 빼기(1), nesne_Başvuru = 빼기(2); if (!화면객체(nesne_Başvuru)) return;
            if (kullanıcı_alanı.화면연결(1, yığın_değer[nesne_Başvuru + 2], x_koordinatı, Y_koordinat, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            yığın_değer[nesne_Başvuru + 5] = x_koordinatı; yığın_değer[nesne_Başvuru + 6] = Y_koordinat; yığın_değer[nesne_Başvuru + 7] = 너비; yığın_değer[nesne_Başvuru + 8] = 높이; return;
        }
        if (Word_SMS(ad_sabit, "setSize") && Word_SMS(tanımlayıcı_sabit, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), nesne_Başvuru = 빼기(2); if (!화면객체(nesne_Başvuru)) return;
            if (kullanıcı_alanı.화면연결(1, yığın_değer[nesne_Başvuru + 2], yığın_değer[nesne_Başvuru + 5], yığın_değer[nesne_Başvuru + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { yığın_değer[nesne_Başvuru + 7] = 너비; yığın_değer[nesne_Başvuru + 8] = 높이; } return;
        }
        if (Word_SMS(ad_sabit, "setLocationRelativeTo") && Word_SMS(tanımlayıcı_sabit, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), nesne_Başvuru = 빼기(2); if (!화면객체(nesne_Başvuru)) return; if (상대배치 != 0) { hata_değer("only screen centering supported"); return; } yığın_değer[nesne_Başvuru + 5] = (kullanıcı_alanı.화면너비() - yığın_değer[nesne_Başvuru + 7]) / 2; yığın_değer[nesne_Başvuru + 6] = (kullanıcı_alanı.화면높이() - yığın_değer[nesne_Başvuru + 8]) / 2; kullanıcı_alanı.화면연결(1, yığın_değer[nesne_Başvuru + 2], yığın_değer[nesne_Başvuru + 5], yığın_değer[nesne_Başvuru + 6], yığın_değer[nesne_Başvuru + 7], yığın_değer[nesne_Başvuru + 8]); return; }
        if (Word_SMS(ad_sabit, "setDefaultCloseOperation") && Word_SMS(tanımlayıcı_sabit, "(I)V")) { int ilke = 빼기(1), nesne_Başvuru = 빼기(2); if (화면객체(nesne_Başvuru)) { if (ilke < 0 || ilke > 3) 예외던짐(9, "close policy"); else { yığın_değer[nesne_Başvuru + 10] = ilke; kullanıcı_alanı.화면연결(7, yığın_değer[nesne_Başvuru + 2], ilke, 0, 0, 0); } } return; }
        if (Word_SMS(ad_sabit, "setVisible") && Word_SMS(tanımlayıcı_sabit, "(Z)V")) { int veri_değer = 빼기(1), nesne_Başvuru = 빼기(2); if (화면객체(nesne_Başvuru)) { int 처리값 = kullanıcı_alanı.화면연결(3, yığın_değer[nesne_Başvuru + 2], veri_değer, 0, 0, 0); if (처리값 < 0) hata_değer("Swing requires a standalone interactive command"); else yığın_değer[nesne_Başvuru + 9] = veri_değer; } return; }
        if (Word_SMS(ad_sabit, "dispose") && Word_SMS(tanımlayıcı_sabit, "()V")) { int nesne_Başvuru = 빼기(2); if (화면객체(nesne_Başvuru)) { kullanıcı_alanı.화면연결(4, yığın_değer[nesne_Başvuru + 2], 0, 0, 0, 0); yığın_değer[nesne_Başvuru + 9] = 0; } return; }
        if (Word_SMS(ad_sabit, "repaint") || Word_SMS(ad_sabit, "validate")) { int nesne_Başvuru = 빼기(2); if (!화면객체(nesne_Başvuru) || !Word_SMS(tanımlayıcı_sabit, "()V")) return; kullanıcı_alanı.화면연결(1, yığın_değer[nesne_Başvuru + 2], yığın_değer[nesne_Başvuru + 5], yığın_değer[nesne_Başvuru + 6], yığın_değer[nesne_Başvuru + 7], yığın_değer[nesne_Başvuru + 8]); return; }
        if (Word_SMS(ad_sabit, "isVisible") && Word_SMS(tanımlayıcı_sabit, "()Z")) { int nesne_Başvuru = 빼기(2); if (화면객체(nesne_Başvuru)) 넣기(yığın_değer[nesne_Başvuru + 9], 1); return; }
        hata_değer("unsupported Swing method (native subset)");
    }
    static void göndermek_olay(int hedef_ADRES, int 사건번호, boolean Türkçe) {
        if (hedef_ADRES < 1 || yığın_değer[hedef_ADRES] < 32) { hata_değer("Java event listener required"); return; }
        int Dosya_Dizin = ad_metot(yığın_değer[hedef_ADRES] - 32, 사건번호 == 0 ? (Türkçe ? "Çalıştır" : "run") : (Türkçe ? "almak_Eylem" : "actionPerformed"), 사건번호 == 0 ? "()V" : (Türkçe ? "(LTürkçe/Öz/Eylem_uyarı;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (Dosya_Dizin < 0) { hata_değer("event callback missing"); return; }
        geçerli_yazışma = 0; yazışma_BAĞ_DEĞ_SAY = 1; kare_Dizin = 0; yazışma_Durum[0] = 1; kare_Yığın[0] = 0; kare_kilit[0] = 틀초기화[0] = 0; değişiklik_isteği = false;
        for (int Loop_Dizin = 0; Loop_Dizin < 128; Loop_Dizin++) { yerel_değer[Loop_Dizin] = yerel_TÜR[Loop_Dizin] = 0; }
        kare_metot[0] = Dosya_Dizin; kare_konum[0] = metot_Start[Dosya_Dizin]; yerel_değer[0] = hedef_ADRES; yerel_TÜR[0] = 2;
        if (사건번호 != 0) { yerel_değer[1] = 사건번호; yerel_TÜR[1] = 2; }
        사건중 = true; yürütmek_komut(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!hata) {
            if (나중수 > 0) { int hedef_ADRES = 나중실행[0], Türkçe = 나중한국어[0]; for (int Loop_Dizin = 1; Loop_Dizin < 나중수; Loop_Dizin++) { 나중실행[Loop_Dizin - 1] = 나중실행[Loop_Dizin]; 나중한국어[Loop_Dizin - 1] = 나중한국어[Loop_Dizin]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; göndermek_olay(hedef_ADRES, 0, Türkçe != 0); continue; }
            if (kullanıcı_alanı.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = kullanıcı_alanı.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { hata_değer("GUI event I/O failed"); return; }
            int hesap_değer = 사건번호 & 65535; if (hesap_değer < 1 || hesap_değer > 32) continue; int nesne_Başvuru = 화면참조[hesap_değer - 1]; if (nesne_Başvuru == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (yığın_değer[nesne_Başvuru + 10] != 0) yığın_değer[nesne_Başvuru + 9] = 0;
                if (yığın_değer[nesne_Başvuru + 10] == 3) for (int Loop_Dizin = 0; Loop_Dizin < 32; Loop_Dizin++) if (화면참조[Loop_Dizin] != 0 && yığın_değer[화면참조[Loop_Dizin]] == 24) kullanıcı_alanı.화면연결(4, Loop_Dizin + 1, 0, 0, 0, 0);
            } else if (yığın_değer[nesne_Başvuru + 4] != 0) {
                int 안내참조 = ayırmak_Depolama(29, 2); if (hata) return; yığın_değer[안내참조 + 2] = nesne_Başvuru; yığın_değer[안내참조 + 3] = yığın_değer[nesne_Başvuru + 12]; yığın_Başvuru[안내참조 + 2] = 1; göndermek_olay(yığın_değer[nesne_Başvuru + 4], 안내참조, yığın_değer[nesne_Başvuru + 12] != 0);
            }
        }
    }
    public static int çalıştır() {
        if (kullanıcı_alanı.인수개수() == 1 && 자바도구.같음(kullanıcı_alanı.bağımsız_değişkenler(0), "-version")) {
            kullanıcı_alanı.Yazma("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (kullanıcı_alanı.인수개수() < 1) { kullanıcı_alanı.Yazma("Usage: java CLASS [ARGS]\n"); return 2; }
        girdi_Sınıf_Tanım = yük_Sınıf_Tanım(konak_karakter(kullanıcı_alanı.bağımsız_değişkenler(0))); if (hata || girdi_Sınıf_Tanım < 0) return 1;
        int giriş_noktası_değer = ad_metot(girdi_Sınıf_Tanım, "çalıştır", "()V");
        boolean 한국어진입 = giriş_noktası_değer >= 0 && (metot_erişim[giriş_noktası_değer] & 9) == 9;
        if (!한국어진입) giriş_noktası_değer = ad_metot(girdi_Sınıf_Tanım, "main", "([Ljava/lang/String;)V");
        if (giriş_noktası_değer < 0 || (metot_erişim[giriş_noktası_değer] & 9) != 9) hata_değer("public static void çalıştır() or main(String[] args) required");
        if (hata) return 1;
        int bağımsız_değişkenler = ayırmak_Depolama(3, kullanıcı_alanı.인수개수() - 1); dizi_öğesi[bağımsız_değişkenler] = -1;
        for (int 수 = 1; 수 < kullanıcı_alanı.인수개수() && !hata; 수++) yığın_değer[bağımsız_değişkenler + 1 + 수] = konak_karakter(kullanıcı_alanı.bağımsız_değişkenler(수));
        kare_Dizin = 0; kare_metot[0] = giriş_noktası_değer; kare_konum[0] = metot_Start[giriş_noktası_değer]; yerel_değer[0] = 한국어진입 ? 0 : bağımsız_değişkenler; yerel_TÜR[0] = 한국어진입 ? 0 : 2;
        yazışma_Durum[0] = 1; yazışma_nesne[0] = ayırmak_Depolama(13, 2);
        yürütmek_komut(); if (!hata) 화면사건들(); return hata ? 1 : 0;
    }
}
