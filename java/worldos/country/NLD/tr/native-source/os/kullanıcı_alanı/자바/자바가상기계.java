// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. dosya/işlenen_Yığın/Başvuru/dal 경계를 yürütmek_komut 중 검사한다. */
public final class 자바가상기계 {
    static int[] dosya = new int[16384], dosya_adı_SMS = new int[64];
    static int[] sabit_etiket = new int[512], 상가 = new int[512], sabit_SANİYE_değer = new int[512], dize_Başvuru = new int[512];
    static int[] metot_ad_SMS = new int[32], metot_TÜR = new int[32], metot_erişim = new int[32];
    static int[] metot_Start = new int[32], metot_Bitiş = new int[32], metot_Yığın = new int[32], 함수지역 = new int[32];
    static int[] metot_bağımsız_değişken_BAĞ_DEĞ_SAY = new int[32], metot_bağımsız_değişken_TÜR = new int[512], metot_İade = new int[32];
    static int[] sınır_değer = new int[16384];
    static int[] yerel_değer = new int[4096], yerel_TÜR = new int[4096], işlenen_Yığın_değer = new int[4096], işlenen_Yığın_TÜR = new int[4096];
    static int[] kare_metot = new int[32], kare_konum = new int[32], kare_Yığın = new int[32];
    static int[] yığın_değer = new int[8192];
    static int Boyut, 읽기위치, sabit_BAĞ_DEĞ_SAY, metot_BAĞ_DEĞ_SAY, sınıf_adı, kare_Dizin = -1, yığın_Bitiş_konum = 1, dönüş_türü;
    static boolean hata;

    static void hata_değer(String Word_SMS) {
        if (!hata) { kullanıcı_alanı.Yazma("JVM error: "); kullanıcı_alanı.Yazma(Word_SMS); kullanıcı_alanı.yazma_karakter_değer(10); }
        hata = true;
    }
    static boolean klip(int çalıştır, int süre_değer) { return çalıştır >= 0 && süre_değer >= 0 && çalıştır <= Boyut - süre_değer; }
    static int bayt_değer() {
        if (!klip(읽기위치, 1)) { hata_değer("truncated class file"); return 0; }
        return dosya[읽기위치++];
    }
    static int 짧은수() { return bayt_değer() << 8 | bayt_değer(); }
    static int bilgi() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int süre_değer) { if (!klip(읽기위치, süre_değer)) hata_değer("invalid attribute size"); else 읽기위치 += süre_değer; }
    static boolean çek_sabit(int 수, int Tip_değer) {
        if (수 <= 0 || 수 >= sabit_BAĞ_DEĞ_SAY || sabit_etiket[수] != Tip_değer) { hata_değer("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_aralık(int çalıştır, int süre_değer, String Word_SMS) {
        if (!klip(çalıştır, süre_değer) || süre_değer != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < süre_değer; 수++) if (dosya[çalıştır + 수] != Word_SMS.charAt(수)) return false;
        return true;
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
    static void atlamak_öznitelik() {
        int öğe_BAĞ_DEĞ_SAY = 짧은수();
        for (int 수 = 0; 수 < öğe_BAĞ_DEĞ_SAY && !hata; 수++) { çek_sabit(짧은수(), 1); 건너(bilgi()); }
    }
    static int komut_süre(int değer) {
        if (değer == 16 || değer == 18 || değer == 21 || değer == 25 || değer == 54 || değer == 58 || değer == 188) return 2;
        if (değer == 17 || değer == 19 || değer == 132 || değer >= 153 && değer <= 167
            || değer >= 178 && değer <= 184 || değer == 187 || değer == 189 || değer == 192 || değer == 198 || değer == 199) return 3;
        if (değer >= 0 && değer <= 8 || değer >= 26 && değer <= 29 || değer >= 42 && değer <= 46 || değer == 50
            || değer >= 59 && değer <= 62 || değer >= 75 && değer <= 79 || değer == 83 || değer == 87 || değer == 89 || değer == 95
            || değer == 96 || değer == 100 || değer == 104 || değer == 108 || değer == 112 || değer == 116
            || değer == 120 || değer == 122 || değer == 124 || değer == 126 || değer == 128 || değer == 130
            || değer >= 145 && değer <= 147 || değer == 172 || değer == 176 || değer == 177 || değer == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (bilgi() != 0xcafebabe) hata_değer("not a class file");
        int 부판 = 짧은수(), sürüm_değer = 짧은수();
        if (sürüm_değer < 45 || sürüm_değer > 52 || 부판 != 0) hata_değer("supported class versions: 45..52, minor 0");
        sabit_BAĞ_DEĞ_SAY = 짧은수();
        if (sabit_BAĞ_DEĞ_SAY < 1 || sabit_BAĞ_DEĞ_SAY > 512) { hata_değer("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < sabit_BAĞ_DEĞ_SAY && !hata; 수++) {
            int Tip_değer = bayt_değer(); sabit_etiket[수] = Tip_değer;
            if (Tip_değer == 1) { sabit_SANİYE_değer[수] = 짧은수(); 상가[수] = 읽기위치; 건너(sabit_SANİYE_değer[수]); }
            else if (Tip_değer == 3) 상가[수] = bilgi();
            else if (Tip_değer == 7 || Tip_değer == 8) 상가[수] = 짧은수();
            else if (Tip_değer == 9 || Tip_değer == 10 || Tip_değer == 12) { 상가[수] = 짧은수(); sabit_SANİYE_değer[수] = 짧은수(); }
            else hata_değer("unsupported constant type");
        }
        int izin_değer = 짧은수();
        if ((izin_değer & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) hata_değer("unsupported class flags");
        sınıf_adı = sınıf_adı_SMS(짧은수());
        if (!Word_SMS(sınıf_adı_SMS(짧은수()), "java/lang/Object")) hata_değer("inheritance unsupported");
        if (짧은수() != 0) hata_değer("interfaces unsupported");
        if (짧은수() != 0) hata_değer("fields unsupported");
        metot_BAĞ_DEĞ_SAY = 짧은수();
        if (metot_BAĞ_DEĞ_SAY < 1 || metot_BAĞ_DEĞ_SAY > 32) { hata_değer("method count limit (32)"); return; }
        for (int 수 = 0; 수 < metot_BAĞ_DEĞ_SAY && !hata; 수++) {
            metot_erişim[수] = 짧은수(); metot_ad_SMS[수] = 짧은수(); metot_TÜR[수] = 짧은수();
            çek_sabit(metot_ad_SMS[수], 1); 서술읽기(수);
            if ((metot_erişim[수] & (0x100 | 0x400 | 0x20)) != 0) hata_değer("native, abstract and synchronized methods unsupported");
            if ((metot_erişim[수] & 8) == 0 && !Word_SMS(metot_ad_SMS[수], "<init>")) hata_değer("instance methods unsupported");
            if (Word_SMS(metot_ad_SMS[수], "<clinit>")) hata_değer("class initializers unsupported");
            for (int ön_kamera_değer = 0; ön_kamera_değer < 수; ön_kamera_değer++) if (같은말(metot_ad_SMS[ön_kamera_değer], metot_ad_SMS[수]) && 같은말(metot_TÜR[ön_kamera_değer], metot_TÜR[수])) hata_değer("duplicate method");
            int öğe_BAĞ_DEĞ_SAY = 짧은수();
            for (int öznitelik_değer = 0; öznitelik_değer < öğe_BAĞ_DEĞ_SAY && !hata; öznitelik_değer++) {
                int İsim = 짧은수(), süre_değer = bilgi(), çalıştır = 읽기위치;
                if (!klip(çalıştır, süre_değer)) { hata_değer("truncated method attribute"); break; }
                if (Word_SMS(İsim, "Code")) {
                    if (metot_Start[수] != 0) hata_değer("duplicate Code attribute");
                    metot_Yığın[수] = 짧은수(); 함수지역[수] = 짧은수(); int KOD_süre = bilgi();
                    if (metot_Yığın[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metot_bağımsız_değişken_BAĞ_DEĞ_SAY[수]
                        || KOD_süre < 1 || KOD_süre > 8192) hata_değer("method memory limits exceeded");
                    metot_Start[수] = 읽기위치; 건너(KOD_süre); metot_Bitiş[수] = 읽기위치;
                    if (짧은수() != 0) hata_değer("exception handlers unsupported");
                    atlamak_öznitelik();
                    if (읽기위치 != çalıştır + süre_değer) hata_değer("Code attribute size mismatch");
                } else 건너(süre_değer);
            }
            if (metot_Start[수] == 0) hata_değer("missing Code attribute");
            int yuva_girdi = metot_Start[수];
            while (yuva_girdi < metot_Bitiş[수] && !hata) {
                int süre_değer = komut_süre(dosya[yuva_girdi]);
                if (süre_değer == 0 || süre_değer > metot_Bitiş[수] - yuva_girdi) { hata_değer("unsupported or truncated bytecode"); break; }
                sınır_değer[yuva_girdi] = 수 + 1; yuva_girdi += süre_değer;
            }
            // 실행하지 않는 경로에도 잘못된 dal 목적지를 허용하지 않는다.
            yuva_girdi = metot_Start[수];
            while (yuva_girdi < metot_Bitiş[수] && !hata) {
                int değer = dosya[yuva_girdi];
                if (değer >= 153 && değer <= 167 || değer == 198 || değer == 199) {
                    int hedef_değer = yuva_girdi + (short)(dosya[yuva_girdi + 1] << 8 | dosya[yuva_girdi + 2]);
                    if (hedef_değer < metot_Start[수] || hedef_değer >= metot_Bitiş[수] || sınır_değer[hedef_değer] != 수 + 1) hata_değer("invalid branch target");
                }
                yuva_girdi += komut_süre(değer);
            }
        }
        if (!hata) atlamak_öznitelik();
        if (읽기위치 != Boyut) hata_değer("extra class file data");
    }
    static int ayırmak_Depolama(int Tip_değer, int süre_değer) {
        if (süre_değer < 0 || süre_değer > yığın_değer.length - yığın_Bitiş_konum - 2) { hata_değer("object heap exhausted or negative array size"); return 0; }
        int Başvuru = yığın_Bitiş_konum; yığın_Bitiş_konum += süre_değer + 2; yığın_değer[Başvuru] = Tip_değer; yığın_değer[Başvuru + 1] = süre_değer;
        return Başvuru;
    }
    static boolean nesne_değer(int Başvuru, int Tip_değer) {
        if (Başvuru < 1 || Başvuru >= yığın_Bitiş_konum - 1 || yığın_değer[Başvuru] != Tip_değer) { hata_değer("null or invalid object reference"); return false; }
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
        if (kare_Dizin == 31) { hata_değer("call stack limit (32)"); return; }
        int Sonraki_öğe = kare_Dizin + 1;
        for (int 수 = 0; 수 < 128; 수++) yerel_TÜR[Sonraki_öğe * 128 + 수] = 0;
        for (int 수 = metot_bağımsız_değişken_BAĞ_DEĞ_SAY[işlev_değer] - 1; 수 >= 0; 수--) {
            yerel_değer[Sonraki_öğe * 128 + 수] = 빼기(metot_bağımsız_değişken_TÜR[işlev_değer * 16 + 수]); yerel_TÜR[Sonraki_öğe * 128 + 수] = metot_bağımsız_değişken_TÜR[işlev_değer * 16 + 수];
        }
        kare_Dizin = Sonraki_öğe; kare_metot[kare_Dizin] = işlev_değer; kare_konum[kare_Dizin] = metot_Start[işlev_değer]; kare_Yığın[kare_Dizin] = 0;
    }
    static void İade_KR(int TÜR_değer) {
        if (TÜR_değer != metot_İade[kare_metot[kare_Dizin]]) { hata_değer("return type mismatch"); return; }
        int değer = TÜR_değer == 0 ? 0 : 빼기(TÜR_değer);
        kare_Dizin--; if (kare_Dizin >= 0 && TÜR_değer != 0) 넣기(değer, TÜR_değer);
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
                if (değer < 1 || değer > 127) { hata_değer("file stream paths currently require ASCII"); return; }
                akış_dosya_adı[yuva_girdi] = değer;
            }
            akış_dosya_adı[süre_değer] = 0;
            int tanımlayıcı_girdi = kullanıcı_alanı.açık_Dosya_tanımlayıcı(akış_dosya_adı, metinÇıktısı ? (이어 ? 1089 : 577) : 0);
            if (tanımlayıcı_girdi < 0) { hata_değer("FileNotFoundException: file open failed"); return; }
            yığın_değer[akış_değer + 2] = tanımlayıcı_girdi; yığın_değer[akış_değer + 3] = 1;
            return;
        }
        if (komut != 182) { hata_değer("invalid file stream invocation"); return; }
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
            if (sonuç < -1) hata_değer("IOException: read failed"); else 넣기(sonuç, 1);
        } else if (kullanıcı_alanı.파일한바이트쓰기(tanımlayıcı_girdi, değer) != 1) hata_değer("IOException: write failed");
    }
    static void Ara_metot(int Dizin, int komut) {
        if (!çek_sabit(Dizin, 10)) return;
        int sahip_değer = sınıf_adı_SMS(상가[Dizin]), İsim = Başvuru_ad(sabit_SANİYE_değer[Dizin]), biçim_değer = başvuru_türü(sabit_SANİYE_değer[Dizin]);
        if (hata) return;
        if (같은말(sahip_değer, sınıf_adı)) {
            if (komut != 184) { hata_değer("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < metot_BAĞ_DEĞ_SAY; 수++) if (같은말(İsim, metot_ad_SMS[수]) && 같은말(biçim_değer, metot_TÜR[수])) {
                if ((metot_erişim[수] & 8) == 0) hata_değer("method is not static"); else 호출(수);
                return;
            }
            hata_değer("NoSuchMethodError"); return;
        }
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
        hata_değer("unsupported library method");
    }
    static int DİZİ_yuva(int Başvuru, int alt_simge_değer, int TÜR_değer) {
        if (!nesne_değer(Başvuru, TÜR_değer)) return 0;
        if (alt_simge_değer < 0 || alt_simge_değer >= yığın_değer[Başvuru + 1]) { hata_değer("ArrayIndexOutOfBoundsException"); return 0; }
        return Başvuru + 2 + alt_simge_değer;
    }
    static void yürütmek_komut() {
        int 남음 = 500000;
        while (kare_Dizin >= 0 && !hata) {
            if (--남음 == 0) { hata_değer("instruction limit (500000)"); break; }
            int çalıştır = kare_konum[kare_Dizin], değer = 명바();
            if (hata) break;
            if (değer == 0) continue;
            if (değer == 1) { 넣기(0, 2); continue; }
            if (değer >= 2 && değer <= 8) { 넣기(değer - 3, 1); continue; }
            if (değer == 16) { 넣기((byte)명바(), 1); continue; }
            if (değer == 17) { 넣기((short)명짧(), 1); continue; }
            if (değer == 18 || değer == 19) {
                int 수 = değer == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= sabit_BAĞ_DEĞ_SAY) hata_değer("invalid ldc constant");
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
            if (değer == 46 || değer == 50) {
                int alt_simge_değer = 빼기(1), Başvuru = 빼기(2), yuva_girdi = DİZİ_yuva(Başvuru, alt_simge_değer, değer == 46 ? 2 : 3);
                if (!hata) 넣기(yığın_değer[yuva_girdi], değer == 46 ? 1 : 2); continue;
            }
            if (değer == 79 || değer == 83) {
                int öğe_öğe = 빼기(değer == 79 ? 1 : 2), alt_simge_değer = 빼기(1), Başvuru = 빼기(2), yuva_girdi = DİZİ_yuva(Başvuru, alt_simge_değer, değer == 79 ? 2 : 3);
                if (değer == 83 && öğe_öğe != 0) nesne_değer(öğe_öğe, 1);
                if (!hata) yığın_değer[yuva_girdi] = öğe_öğe; continue;
            }
            if (değer == 87) { 빼기(0); continue; }
            if (değer == 89) { int 가 = 빼기(0), TÜR_değer = dönüş_türü; 넣기(가, TÜR_değer); 넣기(가, TÜR_değer); continue; }
            if (değer == 95) { int 가 = 빼기(0), 가형 = dönüş_türü, SANİYE_işlenen = 빼기(0), SANİYE_işlenen_TÜR = dönüş_türü; 넣기(가, 가형); 넣기(SANİYE_işlenen, SANİYE_işlenen_TÜR); continue; }
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
            if (değer == 178) {
                int 수 = 명짧(); if (!çek_sabit(수, 9)) continue;
                if (!Word_SMS(sınıf_adı_SMS(상가[수]), "java/lang/System") || !Word_SMS(Başvuru_ad(sabit_SANİYE_değer[수]), "out")
                    || !Word_SMS(başvuru_türü(sabit_SANİYE_değer[수]), "Ljava/io/PrintStream;")) hata_değer("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (değer == 182 || değer == 183 || değer == 184) { Ara_metot(명짧(), değer); continue; }
            if (değer == 187) {
                int İsim = sınıf_adı_SMS(명짧());
                if (Word_SMS(İsim, "java/lang/StringBuilder")) 넣기(ayırmak_Depolama(4, 1), 2);
                else if (Word_SMS(İsim, "java/io/FileInputStream") || Word_SMS(İsim, "java/io/FileOutputStream")) {
                    int Başvuru = ayırmak_Depolama(Word_SMS(İsim, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!hata) { yığın_değer[Başvuru + 2] = -1; 넣기(Başvuru, 2); }
                } else hata_değer("unsupported object construction");
                continue;
            }
            if (değer == 188 || değer == 189) {
                if (değer == 188) { if (명바() != 10) hata_değer("only int[] newarray is supported"); }
                else if (!Word_SMS(sınıf_adı_SMS(명짧()), "java/lang/String")) hata_değer("only String[] anewarray is supported");
                int süre_değer = 빼기(1); 넣기(ayırmak_Depolama(değer == 188 ? 2 : 3, süre_değer), 2); continue;
            }
            if (değer == 190) {
                int Başvuru = 빼기(2);
                if (Başvuru < 1 || Başvuru >= yığın_Bitiş_konum - 1 || (yığın_değer[Başvuru] != 2 && yığın_değer[Başvuru] != 3)) hata_değer("null or invalid array");
                else 넣기(yığın_değer[Başvuru + 1], 1); continue;
            }
            if (değer == 192) {
                int İsim = sınıf_adı_SMS(명짧()), Başvuru = 빼기(2);
                if (!Word_SMS(İsim, "java/lang/String")) hata_değer("unsupported checkcast");
                else if (Başvuru != 0) nesne_değer(Başvuru, 1);
                넣기(Başvuru, 2); continue;
            }
            hata_değer("unsupported bytecode");
        }
    }
    public static int çalıştır() {
        if (kullanıcı_alanı.인수개수() == 1 && 자바도구.같음(kullanıcı_alanı.bağımsız_değişkenler(0), "-version")) {
            kullanıcı_alanı.Yazma("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (kullanıcı_alanı.인수개수() < 1) { kullanıcı_alanı.Yazma("Usage: java CLASS [ARGS]\n"); return 2; }
        int süre_değer = 자바도구.İsim(dosya_adı_SMS, kullanıcı_alanı.bağımsız_değişkenler(0));
        if (süre_değer < 1 || süre_değer > 57) { kullanıcı_alanı.Yazma("java: invalid class name\n"); return 2; }
        dosya_adı_SMS[süre_değer] = '.'; dosya_adı_SMS[süre_değer + 1] = 'c'; dosya_adı_SMS[süre_değer + 2] = 'l'; dosya_adı_SMS[süre_değer + 3] = 'a'; dosya_adı_SMS[süre_değer + 4] = 's'; dosya_adı_SMS[süre_değer + 5] = 's';
        Boyut = kullanıcı_alanı.파일읽기(dosya_adı_SMS, dosya);
        if (Boyut < 0) { kullanıcı_alanı.Yazma("java: cannot read class: "); 자바도구.수쓰기(Boyut); kullanıcı_alanı.yazma_karakter_değer(10); return 1; }
        클래스읽기(); if (hata) return 1;
        int karakter_ad = sabit_SMS(sınıf_adı);
        if (!hata && yığın_değer[karakter_ad + 1] != süre_değer) hata_değer("class name does not match file");
        for (int 수 = 0; 수 < süre_değer && !hata; 수++) if (yığın_değer[karakter_ad + 2 + 수] != dosya_adı_SMS[수]) hata_değer("class name does not match file");
        int giriş_noktası_değer = -1;
        for (int 수 = 0; 수 < metot_BAĞ_DEĞ_SAY; 수++) if (Word_SMS(metot_ad_SMS[수], "main") && Word_SMS(metot_TÜR[수], "([Ljava/lang/String;)V") && (metot_erişim[수] & 9) == 9) giriş_noktası_değer = 수;
        if (giriş_noktası_değer < 0) hata_değer("public static void main(String[] args) required");
        if (hata) return 1;
        int bağımsız_değişkenler = ayırmak_Depolama(3, kullanıcı_alanı.인수개수() - 1);
        for (int 수 = 1; 수 < kullanıcı_alanı.인수개수() && !hata; 수++) yığın_değer[bağımsız_değişkenler + 1 + 수] = konak_karakter(kullanıcı_alanı.bağımsız_değişkenler(수));
        kare_Dizin = 0; kare_metot[0] = giriş_noktası_değer; kare_konum[0] = metot_Start[giriş_noktası_değer]; yerel_değer[0] = bağımsız_değişkenler; yerel_TÜR[0] = 2;
        yürütmek_komut(); return hata ? 1 : 0;
    }
}
