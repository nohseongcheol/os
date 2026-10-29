// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Faýl/스택/Salgylanma/şahalanma 경계를 ýerine_ýetir_buýruk 중 검사한다. */
public final class 자바가상기계 {
    static int[] Faýl = new int[16 * 16384], 임시파일 = new int[16384], faýl_at_SMS = new int[512];
    static int[] hemişelik_bellik = new int[8192], 상가 = new int[8192], 상나 = new int[8192], setir_Salgylanma = new int[8192];
    static int[] usul_at_SMS = new int[512], usul_ýaz = new int[512], usul_ygtyýarlylyk = new int[512], usul_eýe = new int[512];
    static int[] usul_başlat = new int[512], usul_tamamla = new int[512], usul_Desse = new int[512], 함수지역 = new int[512];
    static int[] 함수인수수 = new int[512], usul_argument_ýaz = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] ýerli_baha = new int[16384], ýerli_ýaz = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] kadr_usul = new int[128], 틀위치 = new int[128], kadr_Desse = new int[128], kadr_instruksiýa = new int[128], ulanyşa_taýýarla_kadr = new int[128];
    static int[] klas_Kesgitleme_at = new int[16], klas_Kesgitleme_ölçegi_üýtget = new int[16], 종부모 = new int[16], klas_Kesgitleme_ýagdaý = new int[16], 종칸수 = new int[16], ulanyşa_taýýarla_klas_Kesgitleme = new int[16];
    static int[] klas_interfeýs = new int[16 * 16], 종접면수 = new int[16];
    static int[] ýer_at = new int[512], ýer_ýaz = new int[512], ýer_eýe = new int[512], ýer_rugsatlar = new int[512], 칸위치 = new int[512], ýer_maglumat = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], ARRAY_element = new int[32768], Store_bitin = new int[256];
    static int Ululyk, 읽기위치, 함수수, klas_at, kadr_indeks = -1, 힙끝 = 1, 반환형;
    static int 종수, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, 표시수, 수거횟수;
    static int 현재가닥, 가닥수 = 1, girizmeklik_klas_Kesgitleme;
    static int[] akym_kadr = new int[4], akym_ýagdaý = new int[4], akym_obýekt = new int[4], akym_niýet = new int[4], 가닥대기 = new int[4];
    static boolean Hata, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], klas_akym = new int[16];

    static void näsazlyk_baha(String Söz_SMS) {
        if (Hata) return;
        int 분류코드 = 0;
        if (자바도구.같음(Söz_SMS, "ArithmeticException: / by zero")) 분류코드 = 4;
        if (자바도구.같음(Söz_SMS, "NullPointerException") || 자바도구.같음(Söz_SMS, "null or invalid array")) 분류코드 = 5;
        if (자바도구.같음(Söz_SMS, "ArrayIndexOutOfBoundsException")) 분류코드 = 7;
        if (자바도구.같음(Söz_SMS, "StringIndexOutOfBoundsException")) 분류코드 = 8;
        if (자바도구.같음(Söz_SMS, "NumberFormatException")) 분류코드 = 10;
        if (자바도구.같음(Söz_SMS, "FileNotFoundException: file open failed")) 분류코드 = 12;
        if (자바도구.같음(Söz_SMS, "IOException: stream closed") || 자바도구.같음(Söz_SMS, "IOException: read failed") || 자바도구.같음(Söz_SMS, "IOException: write failed")) 분류코드 = 11;
        if (자바도구.같음(Söz_SMS, "ClassCastException")) 분류코드 = 14;
        if (자바도구.같음(Söz_SMS, "NegativeArraySizeException")) 분류코드 = 15;
        if (분류코드 != 0 && kadr_indeks >= 0) { 예외던짐(분류코드, Söz_SMS); return; }
        ulanyjy.Ýaz("JVM error: "); ulanyjy.Ýaz(Söz_SMS); ulanyjy.ýaz_nyşan_baha(10); Hata = true;
    }
    static boolean klip(int Bitir, int dowamlylyk_baha) {
        if (Bitir < 0 || Bitir >= Faýl.length || dowamlylyk_baha < 0) return false;
        int klas_Kesgitleme = Bitir / 16384;
        return Bitir % 16384 <= klas_Kesgitleme_ölçegi_üýtget[klas_Kesgitleme] && dowamlylyk_baha <= klas_Kesgitleme_ölçegi_üýtget[klas_Kesgitleme] - Bitir % 16384;
    }
    static int baýt_baha() {
        if (!klip(읽기위치, 1)) { näsazlyk_baha("truncated class file"); return 0; }
        return Faýl[읽기위치++];
    }
    static int 짧은수() { return baýt_baha() << 8 | baýt_baha(); }
    static int bitin() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int dowamlylyk_baha) { if (!klip(읽기위치, dowamlylyk_baha)) näsazlyk_baha("invalid attribute size"); else 읽기위치 += dowamlylyk_baha; }
    static boolean derňe_hemişelik(int 수, int 종류) {
        if (수 <= 0 || 수 >= hemişelik_bellik.length || hemişelik_bellik[수] != 종류) { näsazlyk_baha("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Bitir, int dowamlylyk_baha, String Söz_SMS) {
        if (!klip(Bitir, dowamlylyk_baha)) return false;
        int 읽는자리 = Bitir, 끝 = Bitir + dowamlylyk_baha;
        for (int sikl_indeks = 0; sikl_indeks < Söz_SMS.length(); sikl_indeks++) {
            int nyşanyň_kody = Söz_SMS.charAt(sikl_indeks);
            if (nyşanyň_kody > 0 && nyşanyň_kody < 128) { if (읽는자리 >= 끝 || Faýl[읽는자리++] != nyşanyň_kody) return false; }
            else if (nyşanyň_kody < 2048) {
                if (읽는자리 + 2 > 끝 || Faýl[읽는자리++] != (192 | (nyşanyň_kody >> 6)) || Faýl[읽는자리++] != (128 | (nyşanyň_kody & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Faýl[읽는자리++] != (224 | (nyşanyň_kody >> 12)) || Faýl[읽는자리++] != (128 | ((nyşanyň_kody >> 6) & 63)) || Faýl[읽는자리++] != (128 | (nyşanyň_kody & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Söz_SMS(int hemişelik_baha, String Söz_SMS) { return derňe_hemişelik(hemişelik_baha, 1) && 구간(상가[hemişelik_baha], 상나[hemişelik_baha], Söz_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!derňe_hemişelik(가, 1) || !derňe_hemişelik(나, 1) || 상나[가] != 상나[나]) return false;
        for (int 수 = 0; 수 < 상나[가]; 수++) if (Faýl[상가[가] + 수] != Faýl[상가[나] + 수]) return false;
        return true;
    }
    static int klas_at_SMS(int 수) { return derňe_hemişelik(수, 7) && derňe_hemişelik(상가[수], 1) ? 상가[수] : 0; }
    static int Salgylanma_at(int 수) { return derňe_hemişelik(수, 12) && derňe_hemişelik(상가[수], 1) ? 상가[수] : 0; }
    static int Salgylanma_ýaz(int 수) { return derňe_hemişelik(수, 12) && derňe_hemişelik(상나[수], 1) ? 상나[수] : 0; }
    static int 서술형(int 끝, boolean boş_ýaz) {
        if (읽기위치 >= 끝) { näsazlyk_baha("invalid descriptor"); return 0; }
        int baha = baýt_baha();
        if (baha == 'V' && boş_ýaz) return 0;
        if (baha == 'I' || baha == 'B' || baha == 'C' || baha == 'S' || baha == 'Z') return 1;
        if (baha == '[') { 서술형(끝, false); return 2; }
        if (baha == 'L') {
            int Bitir = 읽기위치;
            while (읽기위치 < 끝 && Faýl[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Bitir) näsazlyk_baha("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        näsazlyk_baha("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_baha) {
        int 이전 = 읽기위치, 수 = usul_ýaz[FUNCTION_baha];
        if (!derňe_hemişelik(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + 상나[수];
        if (baýt_baha() != '(') näsazlyk_baha("invalid method descriptor");
        int 개수 = 0;
        while (!Hata && 읽기위치 < 끝 && Faýl[읽기위치] != ')') {
            if (개수 == 16) { näsazlyk_baha("too many method arguments"); break; }
            usul_argument_ýaz[FUNCTION_baha * 16 + 개수++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || baýt_baha() != ')') näsazlyk_baha("invalid method descriptor");
        함수반환[FUNCTION_baha] = 서술형(끝, true); 함수인수수[FUNCTION_baha] = 개수;
        if (읽기위치 != 끝) näsazlyk_baha("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int baha = 짧은수(); return baha == 0 ? 0 : 현재읽는종 * 512 + baha; }
    static int 명상수() { return usul_eýe[kadr_usul[kadr_indeks]] * 512 + 명짧(); }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !Hata; 수++) { derňe_hemişelik(상번호(), 1); 건너(bitin()); }
    }
    static int buýruk_dowamlylyk(int baha) {
        if (baha == 16 || baha == 18 || baha == 21 || baha == 25 || baha == 54 || baha == 58 || baha == 188) return 2;
        if (baha == 17 || baha == 19 || baha == 132 || baha >= 153 && baha <= 167
            || baha >= 178 && baha <= 184 || baha == 187 || baha == 189 || baha == 192 || baha == 193 || baha == 198 || baha == 199) return 3;
        if (baha == 185 || baha == 200) return 5;
        if (baha >= 0 && baha <= 8 || baha >= 26 && baha <= 29 || baha >= 42 && baha <= 46 || baha >= 50 && baha <= 53
            || baha >= 59 && baha <= 62 || baha >= 75 && baha <= 79 || baha >= 83 && baha <= 95
            || baha == 96 || baha == 100 || baha == 104 || baha == 108 || baha == 112 || baha == 116
            || baha == 120 || baha == 122 || baha == 124 || baha == 126 || baha == 128 || baha == 130
            || baha >= 145 && baha <= 147 || baha == 172 || baha == 176 || baha == 177 || baha == 190 || baha == 191
            || baha == 194 || baha == 195) return 1;
        return 0;
    }
    static int 위치정수(int 읽는자리) {
        if (!klip(읽는자리, 4)) { näsazlyk_baha("truncated bytecode operand"); return 0; }
        return Faýl[읽는자리] << 24 | Faýl[읽는자리 + 1] << 16 | Faýl[읽는자리 + 2] << 8 | Faýl[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Bitir, int 끝) {
        int baha = Faýl[읽는자리], dowamlylyk_baha = buýruk_dowamlylyk(baha);
        if (baha == 170 || baha == 171) {
            int 기준자리 = 읽는자리 + 1;
            while ((기준자리 - Bitir) % 4 != 0) 기준자리++;
            if (끝 - 기준자리 < (baha == 170 ? 12 : 8)) return 0;
            int 항목수 = baha == 170 ? 위치정수(기준자리 + 8) - 위치정수(기준자리 + 4) + 1 : 위치정수(기준자리 + 4);
            if (항목수 < 0 || 항목수 > 2048) return 0;
            dowamlylyk_baha = 기준자리 - 읽는자리 + (baha == 170 ? 12 + 4 * 항목수 : 8 + 8 * 항목수);
        }
        if (baha == 196 && 읽는자리 + 1 < 끝) {
            int Söz_maglumat = Faýl[읽는자리 + 1]; dowamlylyk_baha = Söz_maglumat == 132 ? 6 : (Söz_maglumat == 21 || Söz_maglumat == 25 || Söz_maglumat == 54 || Söz_maglumat == 58) ? 4 : 0;
        }
        return dowamlylyk_baha > 0 && dowamlylyk_baha <= 끝 - 읽는자리 ? dowamlylyk_baha : 0;
    }
    static void derňe_barylmaly_ýer_baha(int barylmaly_ýer_baha, int FUNCTION_baha) {
        if (barylmaly_ýer_baha < usul_başlat[FUNCTION_baha] || barylmaly_ýer_baha >= usul_tamamla[FUNCTION_baha] || 경계[barylmaly_ýer_baha] != FUNCTION_baha + 1) näsazlyk_baha("invalid branch target");
    }
    static void 클래스읽기(int klas_Kesgitleme) {
        현재읽는종 = klas_Kesgitleme; 읽기위치 = klas_Kesgitleme * 16384; Ululyk = 읽기위치 + klas_Kesgitleme_ölçegi_üýtget[klas_Kesgitleme];
        if (bitin() != 0xcafebabe) { näsazlyk_baha("not a class file"); return; }
        int 부판 = 짧은수(), wersiýa_baha = 짧은수();
        if (wersiýa_baha < 45 || wersiýa_baha > 52 || 부판 != 0) { näsazlyk_baha("supported class versions: 45..52, minor 0"); return; }
        int 상수수 = 짧은수(), 기준자리 = klas_Kesgitleme * 512;
        if (상수수 < 1 || 상수수 > 512) { näsazlyk_baha("constant pool limit (511)"); return; }
        for (int 항목수 = 1; 항목수 < 상수수 && !Hata; 항목수++) {
            int 수 = 기준자리 + 항목수, 종류 = baýt_baha(); hemişelik_bellik[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = bitin();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); 상나[수] = 상번호(); }
            else näsazlyk_baha("unsupported constant type");
        }
        int rugsat_baha = 짧은수();
        if ((rugsat_baha & (0x2000 | 0x4000)) != 0) näsazlyk_baha("annotation/enum class unsupported");
        klas_Kesgitleme_at[klas_Kesgitleme] = klas_at_SMS(상번호());
        종부모[klas_Kesgitleme] = klas_at_SMS(상번호());
        int 접면수 = 짧은수(); if (접면수 > 16) { näsazlyk_baha("interface count limit"); return; }
        종접면수[klas_Kesgitleme] = 접면수;
        for (int sikl_indeks = 0; sikl_indeks < 접면수; sikl_indeks++) klas_interfeýs[klas_Kesgitleme * 16 + sikl_indeks] = klas_at_SMS(상번호());
        int 필드수 = 짧은수();
        if (필드수 > 512 - 칸수) { näsazlyk_baha("field count limit (512)"); return; }
        for (int sikl_indeks = 0; sikl_indeks < 필드수 && !Hata; sikl_indeks++) {
            int faýl_indeks = 칸수++; ýer_eýe[faýl_indeks] = klas_Kesgitleme; ýer_rugsatlar[faýl_indeks] = 짧은수(); ýer_at[faýl_indeks] = 상번호(); ýer_ýaz[faýl_indeks] = 상번호();
            derňe_hemişelik(ýer_at[faýl_indeks], 1); derňe_hemişelik(ýer_ýaz[faýl_indeks], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[ýer_ýaz[faýl_indeks]]; int 분류코드 = 서술형(읽기위치 + 상나[ýer_ýaz[faýl_indeks]], false); 읽기위치 = 보존값;
            if ((ýer_rugsatlar[faýl_indeks] & 8) == 0) 칸위치[faýl_indeks] = 종칸수[klas_Kesgitleme]++;
            int alamat_maglumat = 짧은수();
            for (int 안쪽자리 = 0; 안쪽자리 < alamat_maglumat && !Hata; 안쪽자리++) {
                int at_hemişelik = 상번호(), 유효길이 = bitin();
                if (Söz_SMS(at_hemişelik, "ConstantValue") && 유효길이 == 2) {
                    int maglumat_baha = 상번호();
                    if (분류코드 == 1 && derňe_hemişelik(maglumat_baha, 3)) ýer_maglumat[faýl_indeks] = 상가[maglumat_baha];
                    else if (분류코드 == 2 && derňe_hemişelik(maglumat_baha, 8)) ýer_maglumat[faýl_indeks] = hemişelik_SMS(상가[maglumat_baha]);
                } else 건너(유효길이);
            }
        }
        int 개수 = 짧은수();
        if (개수 > 512 - 함수수) { näsazlyk_baha("method count limit (512)"); return; }
        for (int sikl_indeks = 0; sikl_indeks < 개수 && !Hata; sikl_indeks++) {
            int 수 = 함수수++; usul_eýe[수] = klas_Kesgitleme;
            usul_ygtyýarlylyk[수] = 짧은수(); usul_at_SMS[수] = 상번호(); usul_ýaz[수] = 상번호();
            derňe_hemişelik(usul_at_SMS[수], 1); 서술읽기(수);
            if ((usul_ygtyýarlylyk[수] & 8) == 0) {
                if (함수인수수[수] == 16) { näsazlyk_baha("too many instance method arguments"); return; }
                for (int 비교자리 = 함수인수수[수]; 비교자리 > 0; 비교자리--) usul_argument_ýaz[수 * 16 + 비교자리] = usul_argument_ýaz[수 * 16 + 비교자리 - 1];
                usul_argument_ýaz[수 * 16] = 2; 함수인수수[수]++;
            }
            if ((usul_ygtyýarlylyk[수] & 0x100) != 0) näsazlyk_baha("user native method unsupported");
            if (Söz_SMS(usul_at_SMS[수], "<clinit>")) ulanyşa_taýýarla_klas_Kesgitleme[klas_Kesgitleme] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (usul_eýe[앞] == klas_Kesgitleme && 같은말(usul_at_SMS[앞], usul_at_SMS[수]) && 같은말(usul_ýaz[앞], usul_ýaz[수])) näsazlyk_baha("duplicate method");
            int 속성수 = 짧은수();
            for (int alamat_baha = 0; alamat_baha < 속성수 && !Hata; alamat_baha++) {
                int Ad = 상번호(), dowamlylyk_baha = bitin(), Bitir = 읽기위치;
                if (!klip(Bitir, dowamlylyk_baha)) { näsazlyk_baha("truncated method attribute"); break; }
                if (Söz_SMS(Ad, "Code")) {
                    if (usul_başlat[수] != 0) näsazlyk_baha("duplicate Code attribute");
                    usul_Desse[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = bitin();
                    if (usul_Desse[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) näsazlyk_baha("method memory limits exceeded");
                    usul_başlat[수] = 읽기위치; 건너(코드길이); usul_tamamla[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { näsazlyk_baha("exception table limit"); return; }
                    for (int 안쪽자리 = 0; 안쪽자리 < 잡는수; 안쪽자리++) {
                        int säwlik_Salgylanma = 잡기수++; 잡기함수[säwlik_Salgylanma] = 수;
                        잡기시작[säwlik_Salgylanma] = usul_başlat[수] + 짧은수(); 잡기끝[säwlik_Salgylanma] = usul_başlat[수] + 짧은수();
                        잡기위치[säwlik_Salgylanma] = usul_başlat[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[säwlik_Salgylanma] = 부호값 == 0 ? 0 : klas_at_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Bitir + dowamlylyk_baha) näsazlyk_baha("Code attribute size mismatch");
                } else 건너(dowamlylyk_baha);
            }
            if ((usul_ygtyýarlylyk[수] & 0x400) != 0) continue;
            if (usul_başlat[수] == 0) näsazlyk_baha("missing Code attribute");
            int ýer_girizmeklik = usul_başlat[수];
            while (ýer_girizmeklik < usul_tamamla[수] && !Hata) {
                int dowamlylyk_baha = 길이읽기(ýer_girizmeklik, usul_başlat[수], usul_tamamla[수]);
                if (dowamlylyk_baha == 0) { näsazlyk_baha("unsupported or truncated bytecode"); break; }
                경계[ýer_girizmeklik] = 수 + 1; ýer_girizmeklik += dowamlylyk_baha;
            }
            ýer_girizmeklik = usul_başlat[수];
            while (ýer_girizmeklik < usul_tamamla[수] && !Hata) {
                int baha = Faýl[ýer_girizmeklik];
                if (baha >= 153 && baha <= 167 || baha == 198 || baha == 199) derňe_barylmaly_ýer_baha(ýer_girizmeklik + (short)(Faýl[ýer_girizmeklik + 1] << 8 | Faýl[ýer_girizmeklik + 2]), 수);
                if (baha == 200) derňe_barylmaly_ýer_baha(ýer_girizmeklik + 위치정수(ýer_girizmeklik + 1), 수);
                if (baha == 170 || baha == 171) {
                    int 읽는자리 = ýer_girizmeklik + 1; while ((읽는자리 - usul_başlat[수]) % 4 != 0) 읽는자리++;
                    derňe_barylmaly_ýer_baha(ýer_girizmeklik + 위치정수(읽는자리), 수);
                    int 항목수 = baha == 170 ? 위치정수(읽는자리 + 8) - 위치정수(읽는자리 + 4) + 1 : 위치정수(읽는자리 + 4);
                    읽는자리 += baha == 170 ? 12 : 8;
                    for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) derňe_barylmaly_ýer_baha(ýer_girizmeklik + 위치정수(읽는자리 + 안쪽자리 * (baha == 170 ? 4 : 8) + (baha == 170 ? 0 : 4)), 수);
                }
                ýer_girizmeklik += 길이읽기(ýer_girizmeklik, usul_başlat[수], usul_tamamla[수]);
            }
            for (int 안쪽자리 = 0; 안쪽자리 < 잡기수; 안쪽자리++) if (잡기함수[안쪽자리] == 수) {
                derňe_barylmaly_ýer_baha(잡기시작[안쪽자리], 수); derňe_barylmaly_ýer_baha(잡기위치[안쪽자리], 수);
                if (잡기끝[안쪽자리] != usul_tamamla[수]) derňe_barylmaly_ýer_baha(잡기끝[안쪽자리], 수);
                if (잡기시작[안쪽자리] >= 잡기끝[안쪽자리]) näsazlyk_baha("invalid exception range");
            }
        }
        if (!Hata) 속성건너();
        if (읽기위치 != Ululyk) näsazlyk_baha("extra class file data");
    }
    static int bölüp_aýyr_Ammar(int 종류, int dowamlylyk_baha) { return 새기억(종류, dowamlylyk_baha); }
    static boolean obýekt_baha(int Salgylanma, int 종류) {
        if (!객체유효(Salgylanma)) return false;
        if (힙[Salgylanma] != 종류) { näsazlyk_baha("object type mismatch"); return false; }
        return true;
    }
    static int hemişelik_SMS(int indeks) {
        if (!derňe_hemişelik(indeks, 1)) return 0;
        if (setir_Salgylanma[indeks] != 0) return setir_Salgylanma[indeks];
        int Salgylanma = bölüp_aýyr_Ammar(1, 상나[indeks]); if (Hata) return 0;
        int 끝 = 상가[indeks] + 상나[indeks], 수 = 상가[indeks], dowamlylyk_baha = 0;
        while (수 < 끝 && !Hata) {
            int baha = Faýl[수++];
            if (baha == 0) näsazlyk_baha("invalid modified UTF-8");
            else if (baha >= 192 && baha <= 223 && 수 < 끝) {
                int 다음 = Faýl[수++];
                if ((다음 & 192) != 128) näsazlyk_baha("invalid modified UTF-8");
                baha = (baha & 31) << 6 | 다음 & 63;
                if (baha != 0 && baha < 128) näsazlyk_baha("overlong modified UTF-8");
            } else if (baha >= 224 && baha <= 239 && 수 + 1 < 끝) {
                int 가 = Faýl[수++], 나 = Faýl[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) näsazlyk_baha("invalid modified UTF-8");
                baha = (baha & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (baha < 2048) näsazlyk_baha("overlong modified UTF-8");
            } else if (baha >= 128) näsazlyk_baha("invalid modified UTF-8");
            힙[Salgylanma + 2 + dowamlylyk_baha++] = baha;
        }
        힙[Salgylanma + 1] = dowamlylyk_baha; setir_Salgylanma[indeks] = Salgylanma; return Salgylanma;
    }
    static int esasy_nyşan(String baha) {
        int Salgylanma = bölüp_aýyr_Ammar(1, baha.length()); if (Hata) return 0;
        for (int 수 = 0; 수 < baha.length(); 수++) 힙[Salgylanma + 2 + 수] = baha.charAt(수);
        return Salgylanma;
    }
    static void ýaz_SMS(int Salgylanma) {
        if (Salgylanma == 0) { ulanyjy.Ýaz("null"); return; }
        if (!obýekt_baha(Salgylanma, 1)) return;
        for (int 수 = 0; 수 < 힙[Salgylanma + 1]; 수++) ulanyjy.ýaz_nyşan_baha(힙[Salgylanma + 2 + 수]);
    }
    static int san_nyşan(int baha) {
        int Salgylanma = bölüp_aýyr_Ammar(1, 11); if (Hata) return 0;
        int dowamlylyk_baha = 0;
        if (baha < 0) 힙[Salgylanma + 2 + dowamlylyk_baha++] = '-'; else baha = -baha;
        int 자리 = 1000000000; boolean Bitir = false;
        while (자리 != 0) {
            int 수 = -(baha / 자리);
            if (수 != 0 || Bitir || 자리 == 1) { 힙[Salgylanma + 2 + dowamlylyk_baha++] = '0' + 수; Bitir = true; }
            baha %= 자리; 자리 /= 10;
        }
        힙[Salgylanma + 1] = dowamlylyk_baha; return Salgylanma;
    }
    static int 정수해독(int Salgylanma) {
        if (!obýekt_baha(Salgylanma, 1)) return 0;
        int dowamlylyk_baha = 힙[Salgylanma + 1], 수 = 0, baha = 0; boolean 음수 = false;
        if (dowamlylyk_baha > 0 && (힙[Salgylanma + 2] == '-' || 힙[Salgylanma + 2] == '+')) { 음수 = 힙[Salgylanma + 2] == '-'; 수++; }
        if (수 == dowamlylyk_baha) näsazlyk_baha("NumberFormatException");
        for (; 수 < dowamlylyk_baha && !Hata; 수++) {
            int san_baha = 힙[Salgylanma + 2 + 수] - '0';
            if (san_baha < 0 || san_baha > 9 || baha < -214748364 || baha == -214748364 && san_baha > (음수 ? 8 : 7)) näsazlyk_baha("NumberFormatException");
            baha = baha * 10 - san_baha;
        }
        return 음수 ? baha : -baha;
    }
    static void 넣기(int baha, int ýaz_baha) {
        if (Hata) return;
        if (kadr_indeks < 0 || kadr_Desse[kadr_indeks] >= usul_Desse[kadr_usul[kadr_indeks]]) { näsazlyk_baha("operand stack overflow"); return; }
        int ýer_girizmeklik = kadr_indeks * 128 + kadr_Desse[kadr_indeks]++; 스택값[ýer_girizmeklik] = baha; 스택형[ýer_girizmeklik] = ýaz_baha;
    }
    static int 빼기(int ýaz_baha) {
        if (Hata) return 0;
        if (kadr_indeks < 0 || kadr_Desse[kadr_indeks] < 1) { näsazlyk_baha("operand stack underflow"); return 0; }
        int ýer_girizmeklik = kadr_indeks * 128 + --kadr_Desse[kadr_indeks]; 반환형 = 스택형[ýer_girizmeklik];
        if (ýaz_baha != 0 && 반환형 != ýaz_baha) näsazlyk_baha("operand type mismatch");
        if (반환형 == 2) gora_baha(스택값[ýer_girizmeklik]);
        return 스택값[ýer_girizmeklik];
    }
    static void 지역읽기(int indeks, int ýaz_baha) {
        if (indeks >= 함수지역[kadr_usul[kadr_indeks]] || indeks < 0 || ýerli_ýaz[kadr_indeks * 128 + indeks] != ýaz_baha) { näsazlyk_baha("invalid or uninitialized local"); return; }
        넣기(ýerli_baha[kadr_indeks * 128 + indeks], ýaz_baha);
    }
    static void ýaz_ýerli(int indeks, int ýaz_baha) {
        if (indeks >= 함수지역[kadr_usul[kadr_indeks]] || indeks < 0) { näsazlyk_baha("local index out of range"); return; }
        int baha = 빼기(ýaz_baha); ýerli_baha[kadr_indeks * 128 + indeks] = baha; ýerli_ýaz[kadr_indeks * 128 + indeks] = ýaz_baha;
    }
    static int 명바() {
        int 위치 = 틀위치[kadr_indeks];
        if (위치 < usul_başlat[kadr_usul[kadr_indeks]] || 위치 >= usul_tamamla[kadr_usul[kadr_indeks]]) { näsazlyk_baha("instruction pointer out of range"); return 0; }
        틀위치[kadr_indeks]++; return Faýl[위치];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void ýerini_üýtget_baha(int 위치) {
        int FUNCTION_baha = kadr_usul[kadr_indeks];
        if (위치 < usul_başlat[FUNCTION_baha] || 위치 >= usul_tamamla[FUNCTION_baha] || 경계[위치] != FUNCTION_baha + 1) näsazlyk_baha("invalid branch target");
        else 틀위치[kadr_indeks] = 위치;
    }
    static void 호출(int FUNCTION_baha) {
        if (kadr_indeks % 32 == 31) { näsazlyk_baha("call stack limit (32)"); return; }
        int 다음 = kadr_indeks + 1;
        for (int 수 = 0; 수 < 128; 수++) ýerli_ýaz[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[FUNCTION_baha] - 1; 수 >= 0; 수--) {
            ýerli_baha[다음 * 128 + 수] = 빼기(usul_argument_ýaz[FUNCTION_baha * 16 + 수]); ýerli_ýaz[다음 * 128 + 수] = usul_argument_ýaz[FUNCTION_baha * 16 + 수];
        }
        if (Hata) return;
        kadr_indeks = 다음; ulanyşa_taýýarla_kadr[kadr_indeks] = 0; kadr_usul[kadr_indeks] = FUNCTION_baha; 틀위치[kadr_indeks] = usul_başlat[FUNCTION_baha]; kadr_Desse[kadr_indeks] = 0;
    }
    static void 반환(int ýaz_baha) {
        if (ýaz_baha != 함수반환[kadr_usul[kadr_indeks]]) { näsazlyk_baha("return type mismatch"); return; }
        int baha = ýaz_baha == 0 ? 0 : 빼기(ýaz_baha);
        if (ulanyşa_taýýarla_kadr[kadr_indeks] != 0) klas_Kesgitleme_ýagdaý[ulanyşa_taýýarla_kadr[kadr_indeks] - 1] = 2;
        if (틀잠금[kadr_indeks] != 0) { 잠금풀기(틀잠금[kadr_indeks]); 틀잠금[kadr_indeks] = 0; }
        kadr_indeks--; if (kadr_indeks >= 현재가닥 * 32 && ýaz_baha != 0) 넣기(baha, ýaz_baha);
    }
    static int[] Stream_faýl_at = new int[64];
    static void faýl_Stream_Jaň(int eýe_baha, int Ad, int format_baha, int buýruk) {
        boolean 출력 = Söz_SMS(eýe_baha, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (buýruk == 183 && Söz_SMS(Ad, "<init>")) {
            boolean 이어 = false;
            if (출력 && Söz_SMS(format_baha, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Söz_SMS(format_baha, "(Ljava/lang/String;)V")) { näsazlyk_baha("unsupported file stream constructor"); return; }
            int faýl_girizmeklik_at = 빼기(2), Stream_baha = 빼기(2);
            if (!obýekt_baha(faýl_girizmeklik_at, 1) || !obýekt_baha(Stream_baha, 종류) || Hata) return;
            if (힙[Stream_baha + 3] != 0) { näsazlyk_baha("file stream already initialized"); return; }
            int dowamlylyk_baha = 힙[faýl_girizmeklik_at + 1];
            if (dowamlylyk_baha < 1 || dowamlylyk_baha > 63) { näsazlyk_baha("invalid file name length"); return; }
            for (int ýer_girizmeklik = 0; ýer_girizmeklik < dowamlylyk_baha; ýer_girizmeklik++) {
                int baha = 힙[faýl_girizmeklik_at + 2 + ýer_girizmeklik];
                if (baha < 1) { näsazlyk_baha("invalid file stream path"); return; }
                Stream_faýl_at[ýer_girizmeklik] = baha;
            }
            Stream_faýl_at[dowamlylyk_baha] = 0;
            int 서술자 = ulanyjy.파일서술자열기(Stream_faýl_at, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { näsazlyk_baha("FileNotFoundException: file open failed"); return; }
            힙[Stream_baha + 2] = 서술자; 힙[Stream_baha + 3] = 1;
            return;
        }
        if (buýruk != 182) { näsazlyk_baha("invalid file stream invocation"); return; }
        if ((출력 && Söz_SMS(Ad, "write") || !출력 && Söz_SMS(Ad, "read"))
            && (Söz_SMS(format_baha, 출력 ? "([B)V" : "([B)I") || Söz_SMS(format_baha, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean klip_baha = Söz_SMS(format_baha, 출력 ? "([BII)V" : "([BII)I");
            int 항목수 = klip_baha ? 빼기(1) : 0, 시작점 = klip_baha ? 빼기(1) : 0, maglumat_ARRAY = 빼기(2), obýekt_Salgylanma = 빼기(2);
            if (!obýekt_baha(maglumat_ARRAY, 20) || !obýekt_baha(obýekt_Salgylanma, 종류)) return;
            if (!klip_baha) 항목수 = 힙[maglumat_ARRAY + 1];
            if (시작점 < 0 || 항목수 < 0 || 시작점 > 힙[maglumat_ARRAY + 1] - 항목수) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[obýekt_Salgylanma + 3] == 0 || 힙[obýekt_Salgylanma + 2] < 0) { näsazlyk_baha("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < 항목수 && !Hata) {
                int 반환값 = 출력 ? ulanyjy.파일한바이트쓰기(힙[obýekt_Salgylanma + 2], 힙[maglumat_ARRAY + 2 + 시작점 + 완료수]) : ulanyjy.파일한바이트읽기(힙[obýekt_Salgylanma + 2]);
                if (반환값 < 0) { näsazlyk_baha(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[maglumat_ARRAY + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(항목수 != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Söz_SMS(Ad, "flush") && Söz_SMS(format_baha, "()V")) { int obýekt_Salgylanma = 빼기(2); if (obýekt_baha(obýekt_Salgylanma, 종류) && 힙[obýekt_Salgylanma + 2] < 0) näsazlyk_baha("IOException: stream closed"); return; }
        int iş = -1, baha = 0;
        if (Söz_SMS(Ad, "close") && Söz_SMS(format_baha, "()V")) iş = 0;
        if (!출력 && Söz_SMS(Ad, "read") && Söz_SMS(format_baha, "()I")) iş = 1;
        if (출력 && Söz_SMS(Ad, "write") && Söz_SMS(format_baha, "(I)V")) { iş = 2; baha = 빼기(1); }
        if (iş < 0) { näsazlyk_baha("unsupported file stream method"); return; }
        int Stream_baha = 빼기(2);
        if (!obýekt_baha(Stream_baha, 종류) || Hata) return;
        if (힙[Stream_baha + 3] == 0) { näsazlyk_baha("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_baha + 2];
        if (iş == 0) {
            if (서술자 >= 0 && ulanyjy.파일서술자닫기(서술자) < 0) näsazlyk_baha("IOException: close failed");
            힙[Stream_baha + 2] = -1; return;
        }
        if (서술자 < 0) { näsazlyk_baha("IOException: stream closed"); return; }
        if (iş == 1) {
            int 결과 = ulanyjy.파일한바이트읽기(서술자);
            if (결과 < -1) näsazlyk_baha("IOException: read failed"); else 넣기(결과 == 256 ? -1 : 결과, 1);
        } else if (ulanyjy.파일한바이트쓰기(서술자, baha) != 1) näsazlyk_baha("IOException: write failed");
    }
    static void Jaň_usul(int indeks, int buýruk) {
        if (indeks <= 0 || indeks >= hemişelik_bellik.length || (hemişelik_bellik[indeks] != 10 && hemişelik_bellik[indeks] != 11)) { näsazlyk_baha("invalid method reference"); return; }
        int eýe_baha = klas_at_SMS(상가[indeks]), Ad = Salgylanma_at(상나[indeks]), format_baha = Salgylanma_ýaz(상나[indeks]);
        if (Hata) return;
        if (기본호출(eýe_baha, Ad, format_baha, buýruk)) return;
        if (Söz_SMS(eýe_baha, "java/io/FileInputStream") || Söz_SMS(eýe_baha, "java/io/FileOutputStream")) {
            faýl_Stream_Jaň(eýe_baha, Ad, format_baha, buýruk); return;
        }
        if (buýruk == 184 && Söz_SMS(eýe_baha, "java/lang/Integer") && Söz_SMS(Ad, "parseInt") && Söz_SMS(format_baha, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (buýruk == 182 && Söz_SMS(eýe_baha, "java/io/PrintStream") && (Söz_SMS(Ad, "println") || Söz_SMS(Ad, "print"))) {
            int ýaz_baha = 0, baha = 0;
            if (Söz_SMS(format_baha, "(I)V")) { ýaz_baha = 1; baha = 빼기(1); }
            else if (Söz_SMS(format_baha, "(Z)V")) { ýaz_baha = 2; baha = 빼기(1); }
            else if (Söz_SMS(format_baha, "(C)V")) { ýaz_baha = 3; baha = 빼기(1); }
            else if (Söz_SMS(format_baha, "(Ljava/lang/String;)V")) { ýaz_baha = 4; baha = 빼기(2); }
            else if (!Söz_SMS(format_baha, "()V") || !Söz_SMS(Ad, "println")) näsazlyk_baha("unsupported print descriptor");
            if (빼기(2) != -1) näsazlyk_baha("invalid PrintStream receiver");
            if (Hata) return;
            if (ýaz_baha == 1) 자바도구.수쓰기(baha);
            if (ýaz_baha == 2) ulanyjy.Ýaz(baha == 0 ? "false" : "true");
            if (ýaz_baha == 3) ulanyjy.ýaz_nyşan_baha(baha & 65535);
            if (ýaz_baha == 4) ýaz_SMS(baha);
            if (Söz_SMS(Ad, "println")) ulanyjy.ýaz_nyşan_baha(10);
            return;
        }
        if (buýruk == 182 && Söz_SMS(eýe_baha, "java/lang/String")) {
            if (Söz_SMS(Ad, "length") && Söz_SMS(format_baha, "()I")) {
                int Salgylanma = 빼기(2); if (obýekt_baha(Salgylanma, 1)) 넣기(힙[Salgylanma + 1], 1); return;
            }
            if (Söz_SMS(Ad, "charAt") && Söz_SMS(format_baha, "(I)C")) {
                int aşaky_indeks_baha = 빼기(1), Salgylanma = 빼기(2);
                if (obýekt_baha(Salgylanma, 1)) {
                    if (aşaky_indeks_baha < 0 || aşaky_indeks_baha >= 힙[Salgylanma + 1]) näsazlyk_baha("StringIndexOutOfBoundsException"); else 넣기(힙[Salgylanma + 2 + aşaky_indeks_baha], 1);
                }
                return;
            }
        }
        if (Söz_SMS(eýe_baha, "java/lang/StringBuilder")) {
            if (buýruk == 183 && Söz_SMS(Ad, "<init>") && Söz_SMS(format_baha, "()V")) { obýekt_baha(빼기(2), 4); return; }
            if (buýruk == 182 && Söz_SMS(Ad, "toString") && Söz_SMS(format_baha, "()Ljava/lang/String;")) {
                int Salgylanma = 빼기(2); if (obýekt_baha(Salgylanma, 4)) 넣기(힙[Salgylanma + 2] == 0 ? esasy_nyşan("") : 힙[Salgylanma + 2], 2); return;
            }
            if (buýruk == 182 && Söz_SMS(Ad, "append")) {
                int Metin = 0;
                if (Söz_SMS(format_baha, "(I)Ljava/lang/StringBuilder;")) Metin = san_nyşan(빼기(1));
                else if (Söz_SMS(format_baha, "(Z)Ljava/lang/StringBuilder;")) Metin = esasy_nyşan(빼기(1) == 0 ? "false" : "true");
                else if (Söz_SMS(format_baha, "(C)Ljava/lang/StringBuilder;")) {
                    int baha = 빼기(1); Metin = bölüp_aýyr_Ammar(1, 1); if (!Hata) 힙[Metin + 2] = baha & 65535;
                }
                else if (Söz_SMS(format_baha, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Metin = 빼기(2); if (Metin == 0) Metin = esasy_nyşan("null"); }
                else { näsazlyk_baha("unsupported StringBuilder append"); return; }
                int Salgylanma = 빼기(2); if (!obýekt_baha(Salgylanma, 4) || !obýekt_baha(Metin, 1)) return;
                int 앞 = 힙[Salgylanma + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], Yza_baha_dowamlylyk = 힙[Metin + 1];
                int 새글 = bölüp_aýyr_Ammar(1, 앞길이 + Yza_baha_dowamlylyk); if (Hata) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < Yza_baha_dowamlylyk; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[Metin + 2 + 수];
                힙[Salgylanma + 2] = 새글; 넣기(Salgylanma, 2); return;
            }
        }
        int klas_Kesgitleme = tap_klas_Kesgitleme(eýe_baha); if (klas_Kesgitleme < 0 || Hata) return;
        int faýl_indeks = tap_usul(klas_Kesgitleme, Ad, format_baha);
        if (faýl_indeks < 0) {
            for (int nyşanyň_kody = klas_Kesgitleme, 항목수 = 0; nyşanyň_kody >= 0 && 항목수 < 16; 항목수++, nyşanyň_kody = 부모종(nyşanyň_kody))
                if (Söz_SMS(종부모[nyşanyň_kody], "java/lang/Thread")) { 가닥호출(Ad, format_baha, buýruk); return; }
            näsazlyk_baha("NoSuchMethodError"); return;
        }
        if (((usul_ygtyýarlylyk[faýl_indeks] & 8) != 0) != (buýruk == 184)) { näsazlyk_baha("method static/instance mismatch"); return; }
        if (buýruk == 184) { if (!ulanyşa_taýýarla(usul_eýe[faýl_indeks], kadr_instruksiýa[kadr_indeks])) return; }
        else {
            int 읽는자리 = kadr_Desse[kadr_indeks] - 함수인수수[faýl_indeks];
            if (읽는자리 < 0 || 스택형[kadr_indeks * 128 + 읽는자리] != 2) { näsazlyk_baha("invalid method receiver"); return; }
            int obýekt_Salgylanma = 스택값[kadr_indeks * 128 + 읽는자리];
            if (!객체유효(obýekt_Salgylanma)) return;
            if (힙[obýekt_Salgylanma] < 32 || !종포함(힙[obýekt_Salgylanma] - 32, eýe_baha)) { näsazlyk_baha("method receiver type mismatch"); return; }
            if (buýruk != 183) faýl_indeks = tap_usul(힙[obýekt_Salgylanma] - 32, Ad, format_baha);
        }
        if (faýl_indeks < 0 || (usul_ygtyýarlylyk[faýl_indeks] & 0x400) != 0) { näsazlyk_baha("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((usul_ygtyýarlylyk[faýl_indeks] & 32) != 0) {
            if (buýruk == 184) { int nyşanyň_kody = usul_eýe[faýl_indeks]; if (종잠금[nyşanyň_kody] == 0) 종잠금[nyşanyň_kody] = bölüp_aýyr_Ammar(8, 0); 잠금참조 = 종잠금[nyşanyň_kody]; }
            else 잠금참조 = 스택값[kadr_indeks * 128 + kadr_Desse[kadr_indeks] - 함수인수수[faýl_indeks]];
            if (!잠금얻기(잠금참조)) { if (!Hata) 틀위치[kadr_indeks] = kadr_instruksiýa[kadr_indeks]; return; }
        }
        호출(faýl_indeks); if (!Hata) 틀잠금[kadr_indeks] = 잠금참조;
    }
    static boolean 배열저장가능(int ARRAY_Salgylanma, int maglumat_baha) {
        if (maglumat_baha == 0 || ARRAY_element[ARRAY_Salgylanma] == 0) return true;
        boolean 성공여부 = ARRAY_element[ARRAY_Salgylanma] == -1 ? (maglumat_baha > 0 && maglumat_baha < 힙끝 && 힙[maglumat_baha] == 1) : 맞는객체(maglumat_baha, ARRAY_element[ARRAY_Salgylanma]);
        if (!성공여부 && !Hata) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int ARRAY_ýer(int Salgylanma, int aşaky_indeks_baha, int ýaz_baha) {
        if (!obýekt_baha(Salgylanma, ýaz_baha)) return 0;
        if (aşaky_indeks_baha < 0 || aşaky_indeks_baha >= 힙[Salgylanma + 1]) { näsazlyk_baha("ArrayIndexOutOfBoundsException"); return 0; }
        return Salgylanma + 2 + aşaky_indeks_baha;
    }
    static void ýerine_ýetir_buýruk() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (Hata) { if (던진객체 != 0) 예외처리(); if (Hata || kadr_indeks < 현재가닥 * 32) break; }
            if (kadr_indeks < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!calşyr_akym()) break; 조각 = 100; }
            if (kadr_indeks == 0 && klas_Kesgitleme_ýagdaý[girizmeklik_klas_Kesgitleme] != 2 && !ulanyşa_taýýarla(girizmeklik_klas_Kesgitleme, 틀위치[kadr_indeks])) continue;
            if (kadr_indeks == 현재가닥 * 32 && 현재가닥 != 0 && (usul_ygtyýarlylyk[kadr_usul[kadr_indeks]] & 32) != 0 && 틀잠금[kadr_indeks] == 0) {
                int obýekt_Salgylanma = akym_niýet[현재가닥]; if (!잠금얻기(obýekt_Salgylanma)) { if (Hata) break; continue; } 틀잠금[kadr_indeks] = obýekt_Salgylanma;
            }
            잠시수 = 0;
            if (--남음 == 0) { näsazlyk_baha("instruction limit (500000)"); break; }
            int Bitir = 틀위치[kadr_indeks]; kadr_instruksiýa[kadr_indeks] = Bitir; int baha = 명바();
            if (Hata) break;
            if (baha == 0) continue;
            if (baha == 1) { 넣기(0, 2); continue; }
            if (baha >= 2 && baha <= 8) { 넣기(baha - 3, 1); continue; }
            if (baha == 16) { 넣기((byte)명바(), 1); continue; }
            if (baha == 17) { 넣기((short)명짧(), 1); continue; }
            if (baha == 18 || baha == 19) {
                int 수 = usul_eýe[kadr_usul[kadr_indeks]] * 512 + (baha == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= hemişelik_bellik.length) näsazlyk_baha("invalid ldc constant");
                else if (hemişelik_bellik[수] == 3) 넣기(상가[수], 1);
                else if (hemişelik_bellik[수] == 8) 넣기(hemişelik_SMS(상가[수]), 2);
                else näsazlyk_baha("unsupported ldc constant");
                continue;
            }
            if (baha == 21 || baha == 25) { 지역읽기(명바(), baha == 21 ? 1 : 2); continue; }
            if (baha >= 26 && baha <= 29) { 지역읽기(baha - 26, 1); continue; }
            if (baha >= 42 && baha <= 45) { 지역읽기(baha - 42, 2); continue; }
            if (baha == 54 || baha == 58) { ýaz_ýerli(명바(), baha == 54 ? 1 : 2); continue; }
            if (baha >= 59 && baha <= 62) { ýaz_ýerli(baha - 59, 1); continue; }
            if (baha >= 75 && baha <= 78) { ýaz_ýerli(baha - 75, 2); continue; }
            if (baha == 46 || baha >= 50 && baha <= 53) {
                int 항목자리 = 빼기(1), obýekt_Salgylanma = 빼기(2), 분류코드 = baha == 46 ? 2 : baha == 50 ? 3 : baha == 51 ? 20 : baha == 52 ? 22 : 23;
                if (baha == 51 && obýekt_Salgylanma > 0 && obýekt_Salgylanma < 힙끝 && 힙[obýekt_Salgylanma] == 21) 분류코드 = 21;
                int 읽는자리 = ARRAY_ýer(obýekt_Salgylanma, 항목자리, 분류코드); if (!Hata) 넣기(힙[읽는자리], baha == 50 ? 2 : 1); continue;
            }
            if (baha == 79 || baha >= 83 && baha <= 86) {
                int girizmeklik_Salgylanma = 빼기(baha == 83 ? 2 : 1), 항목자리 = 빼기(1), obýekt_Salgylanma = 빼기(2), 분류코드 = baha == 79 ? 2 : baha == 83 ? 3 : baha == 84 ? 20 : baha == 85 ? 22 : 23;
                if (baha == 84 && obýekt_Salgylanma > 0 && obýekt_Salgylanma < 힙끝 && 힙[obýekt_Salgylanma] == 21) 분류코드 = 21;
                int 읽는자리 = ARRAY_ýer(obýekt_Salgylanma, 항목자리, 분류코드);
                if (!Hata && 분류코드 == 3 && !배열저장가능(obýekt_Salgylanma, girizmeklik_Salgylanma)) continue;
                if (!Hata) 힙[읽는자리] = 분류코드 == 20 ? (byte)girizmeklik_Salgylanma : 분류코드 == 21 ? girizmeklik_Salgylanma & 1 : 분류코드 == 22 ? (char)girizmeklik_Salgylanma : 분류코드 == 23 ? (short)girizmeklik_Salgylanma : girizmeklik_Salgylanma;
                continue;
            }
            if (baha >= 87 && baha <= 95) { Desse_instruksiýa(baha); continue; }
            if (baha == 96 || baha == 100 || baha == 104 || baha == 108 || baha == 112 || baha == 120
                || baha == 122 || baha == 124 || baha == 126 || baha == 128 || baha == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), 결과 = 0;
                if ((baha == 108 || baha == 112) && 나 == 0) { näsazlyk_baha("ArithmeticException: / by zero"); continue; }
                if (baha == 96) 결과 = 가 + 나;
                if (baha == 100) 결과 = 가 - 나;
                if (baha == 104) 결과 = 가 * 나;
                if (baha == 108) 결과 = 가 / 나;
                if (baha == 112) 결과 = 가 % 나;
                if (baha == 120) 결과 = 가 << 나;
                if (baha == 122) 결과 = 가 >> 나;
                if (baha == 124) 결과 = 가 >>> 나;
                if (baha == 126) 결과 = 가 & 나;
                if (baha == 128) 결과 = 가 | 나;
                if (baha == 130) 결과 = 가 ^ 나;
                넣기(결과, 1); continue;
            }
            if (baha == 116) { 넣기(-빼기(1), 1); continue; }
            if (baha == 132) {
                int ýerli_elýeterli_gor = 명바(), 증분 = (byte)명바(); 지역읽기(ýerli_elýeterli_gor, 1); 넣기(빼기(1) + 증분, 1); ýaz_ýerli(ýerli_elýeterli_gor, 1); continue;
            }
            if (baha >= 145 && baha <= 147) {
                int 수 = 빼기(1); 넣기(baha == 145 ? (byte)수 : baha == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (baha >= 153 && baha <= 167 || baha == 198 || baha == 199) {
                int barylmaly_ýer_baha = Bitir + (short)명짧(); boolean 갈까 = baha == 167;
                if (baha >= 153 && baha <= 158) {
                    int 수 = 빼기(1); 갈까 = baha == 153 ? 수 == 0 : baha == 154 ? 수 != 0 : baha == 155 ? 수 < 0 : baha == 156 ? 수 >= 0 : baha == 157 ? 수 > 0 : 수 <= 0;
                } else if (baha >= 159 && baha <= 166) {
                    int 나 = 빼기(baha >= 165 ? 2 : 1), 가 = 빼기(baha >= 165 ? 2 : 1);
                    갈까 = baha == 159 || baha == 165 ? 가 == 나 : baha == 160 || baha == 166 ? 가 != 나 : baha == 161 ? 가 < 나 : baha == 162 ? 가 >= 나 : baha == 163 ? 가 > 나 : 가 <= 나;
                } else if (baha == 198 || baha == 199) { int 수 = 빼기(2); 갈까 = baha == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) ýerini_üýtget_baha(barylmaly_ýer_baha); continue;
            }
            if (baha == 172 || baha == 176 || baha == 177) { 반환(baha == 172 ? 1 : baha == 176 ? 2 : 0); continue; }
            if (baha >= 178 && baha <= 181) { 필드호출(명상수(), baha, Bitir); continue; }
            if (baha >= 182 && baha <= 185) {
                int 부호값 = 명상수();
                if (baha == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { näsazlyk_baha("invalid invokeinterface operands"); continue; } }
                Jaň_usul(부호값, baha); continue;
            }
            if (baha == 187) { 새객체(klas_at_SMS(명상수()), Bitir); continue; }
            if (baha == 188 || baha == 189) {
                int 분류코드 = 3, komponent = 0;
                if (baha == 188) { int 임시값 = 명바(); 분류코드 = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else komponent = klas_at_SMS(명상수());
                if (분류코드 == 0) { näsazlyk_baha("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), obýekt_Salgylanma = bölüp_aýyr_Ammar(분류코드, 유효길이); if (!Hata) ARRAY_element[obýekt_Salgylanma] = komponent; 넣기(obýekt_Salgylanma, 2); continue;
            }
            if (baha == 190) {
                int obýekt_Salgylanma = 빼기(2);
                if (객체유효(obýekt_Salgylanma)) { int 비교자리 = 힙[obýekt_Salgylanma]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) näsazlyk_baha("not an array"); else 넣기(힙[obýekt_Salgylanma + 1], 1); }
                continue;
            }
            if (baha == 191) {
                int obýekt_Salgylanma = 빼기(2); if (객체유효(obýekt_Salgylanma)) { if (힙[obýekt_Salgylanma] != 9) näsazlyk_baha("athrow requires supported Throwable"); else { 던진객체 = obýekt_Salgylanma; Hata = true; } }
                continue;
            }
            if (baha == 192 || baha == 193) {
                int at_hemişelik = klas_at_SMS(명상수()), obýekt_Salgylanma = 빼기(2); boolean 일치여부 = 맞는객체(obýekt_Salgylanma, at_hemişelik);
                if (baha == 193) 넣기(obýekt_Salgylanma != 0 && 일치여부 ? 1 : 0, 1);
                else { if (!일치여부 && !Hata) näsazlyk_baha("ClassCastException"); 넣기(obýekt_Salgylanma, 2); }
                continue;
            }
            if (baha == 170 || baha == 171) {
                int 읽는자리 = Bitir + 1, faýl_indeks = kadr_usul[kadr_indeks], açar_Salgylanma = 빼기(1);
                while ((읽는자리 - usul_başlat[faýl_indeks]) % 4 != 0) 읽는자리++;
                int niýet_salgy = 위치정수(읽는자리);
                if (baha == 170) { int 낮은값 = 위치정수(읽는자리 + 4), 높은값 = 위치정수(읽는자리 + 8); if (açar_Salgylanma >= 낮은값 && açar_Salgylanma <= 높은값) niýet_salgy = 위치정수(읽는자리 + 12 + (açar_Salgylanma - 낮은값) * 4); }
                else { int 총수 = 위치정수(읽는자리 + 4); for (int sikl_indeks = 0; sikl_indeks < 총수; sikl_indeks++) if (위치정수(읽는자리 + 8 + sikl_indeks * 8) == açar_Salgylanma) niýet_salgy = 위치정수(읽는자리 + 12 + sikl_indeks * 8); }
                ýerini_üýtget_baha(Bitir + niýet_salgy); continue;
            }
            if (baha == 200) { ýerini_üýtget_baha(Bitir + 위치정수(Bitir + 1)); continue; }
            if (baha == 194 || baha == 195) {
                int obýekt_Salgylanma = 빼기(2);
                if (baha == 195) 잠금풀기(obýekt_Salgylanma);
                else if (!잠금얻기(obýekt_Salgylanma) && !Hata) { 넣기(obýekt_Salgylanma, 2); 틀위치[kadr_indeks] = Bitir; }
                continue;
            }
            if (baha == 196) {
                int 명령코드 = 명바(), 항목자리 = 명짧();
                if (명령코드 == 21 || 명령코드 == 25) 지역읽기(항목자리, 명령코드 == 21 ? 1 : 2);
                else if (명령코드 == 54 || 명령코드 == 58) ýaz_ýerli(항목자리, 명령코드 == 54 ? 1 : 2);
                else if (명령코드 == 132) { int 변화량 = (short)명짧(); 지역읽기(항목자리, 1); 넣기(빼기(1) + 변화량, 1); ýaz_ýerli(항목자리, 1); }
                else näsazlyk_baha("unsupported wide opcode");
                continue;
            }
            näsazlyk_baha("unsupported bytecode");
        }
    }
    static int tap_klas_Kesgitleme(int Ad) {
        for (int sikl_indeks = 0; sikl_indeks < 종수; sikl_indeks++) if (klas_Kesgitleme_at[sikl_indeks] != 0 && 같은말(klas_Kesgitleme_at[sikl_indeks], Ad)) return sikl_indeks;
        return ýük_klas_Kesgitleme(hemişelik_SMS(Ad));
    }
    static int ýük_klas_Kesgitleme(int at_setir) {
        if (!obýekt_baha(at_setir, 1)) return -1;
        int dowamlylyk_baha = 힙[at_setir + 1];
        if (dowamlylyk_baha < 1 || dowamlylyk_baha > 505 || 종수 == 16) { näsazlyk_baha("class name/count limit"); return -1; }
        for (int sikl_indeks = 0; sikl_indeks < dowamlylyk_baha; sikl_indeks++) { int nyşanyň_kody = 힙[at_setir + 2 + sikl_indeks]; faýl_at_SMS[sikl_indeks] = nyşanyň_kody == '/' ? '.' : nyşanyň_kody; }
        faýl_at_SMS[dowamlylyk_baha] = '.'; faýl_at_SMS[dowamlylyk_baha + 1] = 'c'; faýl_at_SMS[dowamlylyk_baha + 2] = 'l'; faýl_at_SMS[dowamlylyk_baha + 3] = 'a'; faýl_at_SMS[dowamlylyk_baha + 4] = 's'; faýl_at_SMS[dowamlylyk_baha + 5] = 's'; faýl_at_SMS[dowamlylyk_baha + 6] = 0;
        int Ululyk = ulanyjy.파일읽기(faýl_at_SMS, 임시파일);
        if (Ululyk < 0) { näsazlyk_baha("ClassNotFoundException"); return -1; }
        int klas_Kesgitleme = 종수++; klas_Kesgitleme_ölçegi_üýtget[klas_Kesgitleme] = Ululyk;
        for (int sikl_indeks = 0; sikl_indeks < Ululyk; sikl_indeks++) Faýl[klas_Kesgitleme * 16384 + sikl_indeks] = 임시파일[sikl_indeks];
        클래스읽기(klas_Kesgitleme); if (Hata) return -1;
        int hakyky_maglumat = hemişelik_SMS(klas_Kesgitleme_at[klas_Kesgitleme]);
        if (!글같음(hakyky_maglumat, at_setir, true)) { näsazlyk_baha("class name does not match file"); return -1; }
        int 부모 = 종부모[klas_Kesgitleme];
        if (부모 != 0 && !Söz_SMS(부모, "java/lang/Object") && !Söz_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = tap_klas_Kesgitleme(부모);
            if (Hata || 위 < 0) return -1;
            int 읽는자리 = 위, 단계수 = 0;
            while (읽는자리 >= 0 && 단계수++ < 16) {
                if (읽는자리 == klas_Kesgitleme) { näsazlyk_baha("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int faýl_indeks = 0; faýl_indeks < 칸수; faýl_indeks++) if (ýer_eýe[faýl_indeks] == klas_Kesgitleme && (ýer_rugsatlar[faýl_indeks] & 8) == 0) 칸위치[faýl_indeks] += 시작변위;
            종칸수[klas_Kesgitleme] += 시작변위;
        }
        return klas_Kesgitleme;
    }
    static int 부모종(int klas_Kesgitleme) {
        int Ad = 종부모[klas_Kesgitleme];
        for (int sikl_indeks = 0; sikl_indeks < 종수; sikl_indeks++) if (Ad != 0 && klas_Kesgitleme_at[sikl_indeks] != 0 && 같은말(klas_Kesgitleme_at[sikl_indeks], Ad)) return sikl_indeks;
        return -1;
    }
    static int tap_usul(int klas_Kesgitleme, int Ad, int format_baha) {
        for (int 깊이 = 0; klas_Kesgitleme >= 0 && 깊이 < 16; 깊이++, klas_Kesgitleme = 부모종(klas_Kesgitleme)) {
            for (int sikl_indeks = 0; sikl_indeks < 함수수; sikl_indeks++) if (usul_eýe[sikl_indeks] == klas_Kesgitleme && 같은말(usul_at_SMS[sikl_indeks], Ad) && 같은말(usul_ýaz[sikl_indeks], format_baha)) return sikl_indeks;
        }
        return -1;
    }
    static int at_usul(int klas_Kesgitleme, String Ad, String format_baha) {
        for (int 깊이 = 0; klas_Kesgitleme >= 0 && 깊이 < 16; 깊이++, klas_Kesgitleme = 부모종(klas_Kesgitleme))
            for (int sikl_indeks = 0; sikl_indeks < 함수수; sikl_indeks++) if (usul_eýe[sikl_indeks] == klas_Kesgitleme && Söz_SMS(usul_at_SMS[sikl_indeks], Ad) && Söz_SMS(usul_ýaz[sikl_indeks], format_baha)) return sikl_indeks;
        return -1;
    }
    static int 형종류(int Ad) { return Faýl[상가[Ad]] == 'L' || Faýl[상가[Ad]] == '[' ? 2 : 1; }
    static boolean ulanyşa_taýýarla(int klas_Kesgitleme, int buýruk_başlat) {
        if (klas_Kesgitleme < 0 || Hata) return false;
        if (klas_Kesgitleme_ýagdaý[klas_Kesgitleme] == 3) { näsazlyk_baha("NoClassDefFoundError: initialization failed"); return false; }
        if (klas_Kesgitleme_ýagdaý[klas_Kesgitleme] == 1 && klas_akym[klas_Kesgitleme] != 현재가닥) { 틀위치[kadr_indeks] = buýruk_başlat; 바꿈요청 = true; return false; }
        if (klas_Kesgitleme_ýagdaý[klas_Kesgitleme] != 0) return true;
        int 위 = 부모종(klas_Kesgitleme);
        if (위 >= 0 && !ulanyşa_taýýarla(위, buýruk_başlat)) return false;
        klas_Kesgitleme_ýagdaý[klas_Kesgitleme] = 1; klas_akym[klas_Kesgitleme] = 현재가닥;
        if (ulanyşa_taýýarla_klas_Kesgitleme[klas_Kesgitleme] != 0) {
            틀위치[kadr_indeks] = buýruk_başlat;
            호출(ulanyşa_taýýarla_klas_Kesgitleme[klas_Kesgitleme] - 1); if (!Hata) ulanyşa_taýýarla_kadr[kadr_indeks] = klas_Kesgitleme + 1;
            return false;
        }
        klas_Kesgitleme_ýagdaý[klas_Kesgitleme] = 2; return true;
    }
    static void 필드호출(int indeks, int buýruk, int Bitir) {
        if (!derňe_hemişelik(indeks, 9)) return;
        int eýe_baha = klas_at_SMS(상가[indeks]), Ad = Salgylanma_at(상나[indeks]), format_baha = Salgylanma_ýaz(상나[indeks]);
        if (Söz_SMS(eýe_baha, "java/lang/System") && (Söz_SMS(Ad, "out") || Söz_SMS(Ad, "err")) && Söz_SMS(format_baha, "Ljava/io/PrintStream;") && buýruk == 178) { 넣기(-1, 2); return; }
        int klas_Kesgitleme = tap_klas_Kesgitleme(eýe_baha); if (klas_Kesgitleme < 0 || Hata) return;
        int 찾음 = -1;
        for (int 읽는자리 = klas_Kesgitleme, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int faýl_indeks = 0; faýl_indeks < 칸수; faýl_indeks++) if (ýer_eýe[faýl_indeks] == 읽는자리 && 같은말(ýer_at[faýl_indeks], Ad) && 같은말(ýer_ýaz[faýl_indeks], format_baha)) 찾음 = faýl_indeks;
        if (찾음 < 0) { näsazlyk_baha("NoSuchFieldError"); return; }
        boolean statiki_baha = buýruk == 178 || buýruk == 179;
        if (statiki_baha != ((ýer_rugsatlar[찾음] & 8) != 0)) { näsazlyk_baha("field static/instance mismatch"); return; }
        if (statiki_baha && !ulanyşa_taýýarla(ýer_eýe[찾음], Bitir)) return;
        int ýaz_baha = 형종류(format_baha), baha = 0;
        if (buýruk == 179 || buýruk == 181) baha = 빼기(ýaz_baha);
        if (statiki_baha) { if (buýruk == 178) 넣기(ýer_maglumat[찾음], ýaz_baha); else if (!Hata) ýer_maglumat[찾음] = baha; return; }
        int obýekt_Salgylanma = 빼기(2);
        if (!객체유효(obýekt_Salgylanma)) return;
        if (힙[obýekt_Salgylanma] < 32 || !종포함(힙[obýekt_Salgylanma] - 32, eýe_baha)) { näsazlyk_baha("field receiver type mismatch"); return; }
        int 보관칸 = obýekt_Salgylanma + 2 + 칸위치[찾음];
        if (buýruk == 180) 넣기(힙[보관칸], ýaz_baha);
        else if (!Hata) { 힙[보관칸] = baha; 힙참조[보관칸] = ýaz_baha == 2 ? 1 : 0; }
    }
    static boolean 종포함(int klas_Kesgitleme, int Ad) {
        for (int 중첩깊이 = 0; klas_Kesgitleme >= 0 && 중첩깊이 < 16; 중첩깊이++, klas_Kesgitleme = 부모종(klas_Kesgitleme)) {
            if (같은말(klas_Kesgitleme_at[klas_Kesgitleme], Ad) || (종부모[klas_Kesgitleme] != 0 && 같은말(종부모[klas_Kesgitleme], Ad))) return true;
            for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[klas_Kesgitleme]; 안쪽자리++) if (같은말(klas_interfeýs[klas_Kesgitleme * 16 + 안쪽자리], Ad)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int baýt_maglumat, boolean Ýol) {
        if (첫값 == baýt_maglumat) return true;
        if (첫값 <= 0 || baýt_maglumat <= 0 || 힙[첫값] != 1 || 힙[baýt_maglumat] != 1 || 힙[첫값 + 1] != 힙[baýt_maglumat + 1]) return false;
        for (int sikl_indeks = 0; sikl_indeks < 힙[첫값 + 1]; sikl_indeks++) {
            int x_koordinatasy = 힙[첫값 + 2 + sikl_indeks], 세로좌표 = 힙[baýt_maglumat + 2 + sikl_indeks];
            if (Ýol) { if (x_koordinatasy == '.') x_koordinatasy = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (x_koordinatasy != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int obýekt_Salgylanma) {
        if (obýekt_Salgylanma == 0) { näsazlyk_baha("NullPointerException"); return false; }
        if (obýekt_Salgylanma < 1 || obýekt_Salgylanma >= 힙끝 || 힙폭[obýekt_Salgylanma] < 2 || 힙[obýekt_Salgylanma] == 0) { näsazlyk_baha("invalid object reference"); return false; }
        return true;
    }
    static void gora_baha(int obýekt_Salgylanma) {
        if (obýekt_Salgylanma > 0 && obýekt_Salgylanma < 힙끝 && 힙폭[obýekt_Salgylanma] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = obýekt_Salgylanma;
    }
    static void görkez_baha_487749b8(int obýekt_Salgylanma) {
        if (obýekt_Salgylanma > 0 && obýekt_Salgylanma < 힙끝 && 힙폭[obýekt_Salgylanma] >= 2 && 힙[obýekt_Salgylanma] != 0 && 힙표시[obýekt_Salgylanma] == 0) {
            힙표시[obýekt_Salgylanma] = 1; 표시대기[표시수++] = obýekt_Salgylanma;
        }
    }
    static void 수거() {
        표시수 = 0; 수거횟수++;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) 힙표시[검사자리] = 0;
        for (int sikl_indeks = 0; sikl_indeks < setir_Salgylanma.length; sikl_indeks++) görkez_baha_487749b8(setir_Salgylanma[sikl_indeks]);
        for (int sikl_indeks = 0; sikl_indeks < 칸수; sikl_indeks++) if ((ýer_rugsatlar[sikl_indeks] & 8) != 0 && 형종류(ýer_ýaz[sikl_indeks]) == 2) görkez_baha_487749b8(ýer_maglumat[sikl_indeks]);
        for (int 임시값 = 0; 임시값 < 가닥수; 임시값++) {
            görkez_baha_487749b8(akym_obýekt[임시값]); görkez_baha_487749b8(akym_niýet[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? kadr_indeks : akym_kadr[임시값];
            for (int faýl_indeks = 임시값 * 32; faýl_indeks <= 꼭대기자리; faýl_indeks++) {
                for (int 안쪽자리 = 0; 안쪽자리 < 함수지역[kadr_usul[faýl_indeks]]; 안쪽자리++) if (ýerli_ýaz[faýl_indeks * 128 + 안쪽자리] == 2) görkez_baha_487749b8(ýerli_baha[faýl_indeks * 128 + 안쪽자리]);
                for (int 안쪽자리 = 0; 안쪽자리 < kadr_Desse[faýl_indeks]; 안쪽자리++) if (스택형[faýl_indeks * 128 + 안쪽자리] == 2) görkez_baha_487749b8(스택값[faýl_indeks * 128 + 안쪽자리]);
            }
        }
        for (int sikl_indeks = 0; sikl_indeks < 화면참조.length; sikl_indeks++) görkez_baha_487749b8(화면참조[sikl_indeks]);
        for (int sikl_indeks = 0; sikl_indeks < 나중수; sikl_indeks++) görkez_baha_487749b8(나중실행[sikl_indeks]);
        for (int sikl_indeks = 0; sikl_indeks < Store_bitin.length; sikl_indeks++) görkez_baha_487749b8(Store_bitin[sikl_indeks]);
        for (int sikl_indeks = 0; sikl_indeks < 종수; sikl_indeks++) görkez_baha_487749b8(종잠금[sikl_indeks]);
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (잠금깊이[검사자리] > 0) görkez_baha_487749b8(검사자리);
        görkez_baha_487749b8(던진객체);
        for (int sikl_indeks = 0; sikl_indeks < 잠시수; sikl_indeks++) görkez_baha_487749b8(잠시참조[sikl_indeks]);
        while (표시수 > 0) {
            int obýekt_Salgylanma = 표시대기[--표시수], 분류코드 = 힙[obýekt_Salgylanma];
            for (int sikl_indeks = obýekt_Salgylanma + 2; sikl_indeks < obýekt_Salgylanma + 힙폭[obýekt_Salgylanma]; sikl_indeks++) if (분류코드 == 3 || 분류코드 == 4 || 힙참조[sikl_indeks] != 0) görkez_baha_487749b8(힙[sikl_indeks]);
        }
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙표시[검사자리] == 0) 힙[검사자리] = 0;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙[검사자리] == 0) {
            while (검사자리 + 힙폭[검사자리] < 힙끝 && 힙[검사자리 + 힙폭[검사자리]] == 0) { int 다음자리 = 검사자리 + 힙폭[검사자리]; 힙폭[검사자리] += 힙폭[다음자리]; 힙폭[다음자리] = 0; }
            if (검사자리 + 힙폭[검사자리] == 힙끝) { 힙끝 = 검사자리; break; }
        }
    }
    static int 새기억(int 종류, int dowamlylyk_baha) {
        if (dowamlylyk_baha < 0) { näsazlyk_baha("NegativeArraySizeException"); return 0; }
        if (dowamlylyk_baha > 힙.length - 3) { näsazlyk_baha("object heap exhausted"); return 0; }
        int 필요수 = dowamlylyk_baha + 2, obýekt_Salgylanma = 0;
        if (필요수 <= 힙.length - 힙끝) { obýekt_Salgylanma = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { obýekt_Salgylanma = 읽는자리; break; }
            if (obýekt_Salgylanma != 0) {
                int 남은길이 = 힙폭[obýekt_Salgylanma] - 필요수;
                if (남은길이 >= 2) { 힙폭[obýekt_Salgylanma + 필요수] = 남은길이; 힙[obýekt_Salgylanma + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { obýekt_Salgylanma = 힙끝; 힙끝 += 필요수; }
        }
        if (obýekt_Salgylanma == 0) { näsazlyk_baha("object heap exhausted"); return 0; }
        for (int sikl_indeks = 0; sikl_indeks < 필요수; sikl_indeks++) { 힙[obýekt_Salgylanma + sikl_indeks] = 0; 힙참조[obýekt_Salgylanma + sikl_indeks] = 0; 힙폭[obýekt_Salgylanma + sikl_indeks] = 0; }
        ARRAY_element[obýekt_Salgylanma] = 0;
        힙폭[obýekt_Salgylanma] = 필요수; 힙[obýekt_Salgylanma] = 종류; 힙[obýekt_Salgylanma + 1] = dowamlylyk_baha; gora_baha(obýekt_Salgylanma); return obýekt_Salgylanma;
    }
    static int 예외종(String at_hemişelik) {
        if (자바도구.같음(at_hemişelik, "java/lang/Throwable")) return 1;
        if (자바도구.같음(at_hemişelik, "java/lang/Exception")) return 2;
        if (자바도구.같음(at_hemişelik, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(at_hemişelik, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(at_hemişelik, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(at_hemişelik, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(at_hemişelik, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(at_hemişelik, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(at_hemişelik, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(at_hemişelik, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(at_hemişelik, "java/io/IOException")) return 11;
        if (자바도구.같음(at_hemişelik, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(at_hemişelik, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(at_hemişelik, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(at_hemişelik, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int 예외상수(int Ad) {
        for (int sikl_indeks = 1; sikl_indeks <= 41; sikl_indeks++) if (Söz_SMS(Ad, 예외이름(sikl_indeks))) return sikl_indeks;
        return 0;
    }
    static String 예외이름(int hasap_baha) {
        if (hasap_baha == 40) return "java/lang/InterruptedException";
        if (hasap_baha == 41) return "한국어/자체/대기중단예외";
        if (hasap_baha == 39) return "java/net/SocketException";
        if (hasap_baha == 20) return "한국어/자체/예외";
        if (hasap_baha == 21) return "한국어/자체/실행예외";
        if (hasap_baha == 22) return "한국어/자체/입출력예외";
        if (hasap_baha == 23) return "한국어/자체/대기시간초과예외";
        if (hasap_baha == 24) return "한국어/자체/주소확인예외";
        if (hasap_baha == 25) return "한국어/자체/파일없음예외";
        if (hasap_baha == 26) return "한국어/자체/통신예외";
        if (hasap_baha == 27) return "한국어/자체/잘못된인수예외";
        if (hasap_baha == 28) return "한국어/자체/숫자형식예외";
        if (hasap_baha == 29) return "한국어/자체/범위예외";
        if (hasap_baha == 30) return "한국어/자체/배열범위예외";
        if (hasap_baha == 31) return "한국어/자체/문자열범위예외";
        if (hasap_baha == 32) return "한국어/자체/빈참조예외";
        if (hasap_baha == 33) return "한국어/자체/산술예외";
        if (hasap_baha == 34) return "한국어/자체/상태예외";
        if (hasap_baha == 35) return "한국어/자체/형변환예외";
        if (hasap_baha == 36) return "한국어/자체/음수배열크기예외";
        if (hasap_baha == 37) return "한국어/자체/ARRAY_Store_näsazlyk";
        if (hasap_baha == 38) return "한국어/자체/가닥상태예외";
        if (hasap_baha == 1) return "java/lang/Throwable"; if (hasap_baha == 2) return "java/lang/Exception";
        if (hasap_baha == 3) return "java/lang/RuntimeException"; if (hasap_baha == 4) return "java/lang/ArithmeticException";
        if (hasap_baha == 5) return "java/lang/NullPointerException"; if (hasap_baha == 6) return "java/lang/IndexOutOfBoundsException";
        if (hasap_baha == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (hasap_baha == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (hasap_baha == 9) return "java/lang/IllegalArgumentException"; if (hasap_baha == 10) return "java/lang/NumberFormatException";
        if (hasap_baha == 11) return "java/io/IOException"; if (hasap_baha == 12) return "java/io/FileNotFoundException";
        if (hasap_baha == 17) return "java/lang/ArrayStoreException";
        if (hasap_baha == 18) return "java/net/UnknownHostException";
        if (hasap_baha == 19) return "java/net/SocketTimeoutException";
        if (hasap_baha == 16) return "java/lang/IllegalThreadStateException";
        if (hasap_baha == 13) return "java/lang/IllegalStateException"; if (hasap_baha == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int hasap_baha) {
        if (hasap_baha == 40) return 2;
        if (hasap_baha == 41) return 40;
        if (hasap_baha == 39) return 11;
        if (hasap_baha == 1) return 0;
        if (hasap_baha == 2) return 1;
        if (hasap_baha == 3) return 2;
        if (hasap_baha == 4) return 3;
        if (hasap_baha == 5) return 3;
        if (hasap_baha == 6) return 3;
        if (hasap_baha == 7) return 6;
        if (hasap_baha == 8) return 6;
        if (hasap_baha == 9) return 3;
        if (hasap_baha == 10) return 9;
        if (hasap_baha == 11) return 2;
        if (hasap_baha == 12) return 11;
        if (hasap_baha == 13) return 3;
        if (hasap_baha == 14) return 3;
        if (hasap_baha == 15) return 3;
        if (hasap_baha == 16) return 9;
        if (hasap_baha == 17) return 3;
        if (hasap_baha == 18) return 11;
        if (hasap_baha == 19) return 11;
        if (hasap_baha == 20) return 2;
        if (hasap_baha == 21) return 3;
        if (hasap_baha == 22) return 11;
        if (hasap_baha == 23) return 22;
        if (hasap_baha == 24) return 22;
        if (hasap_baha == 25) return 22;
        if (hasap_baha == 26) return 22;
        if (hasap_baha == 27) return 9;
        if (hasap_baha == 28) return 27;
        if (hasap_baha == 29) return 6;
        if (hasap_baha == 30) return 29;
        if (hasap_baha == 31) return 29;
        if (hasap_baha == 32) return 5;
        if (hasap_baha == 33) return 4;
        if (hasap_baha == 34) return 13;
        if (hasap_baha == 35) return 14;
        if (hasap_baha == 36) return 15;
        if (hasap_baha == 37) return 17;
        if (hasap_baha == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int hakyky_baha, int 요구값) {
        for (int 깊이 = 0; hakyky_baha != 0 && 깊이 < 16; 깊이++, hakyky_baha = 예외부모(hakyky_baha))
            if (hakyky_baha == 요구값) return true;
        return false;
    }
    static void 예외던짐(int hasap_baha, String README_Salgylanma) {
        int obýekt_Salgylanma = 새기억(9, 2); if (Hata) return;
        힙[obýekt_Salgylanma + 2] = hasap_baha; 힙[obýekt_Salgylanma + 3] = esasy_nyşan(README_Salgylanma); 힙참조[obýekt_Salgylanma + 3] = 1;
        던진객체 = obýekt_Salgylanma; Hata = true;
    }
    static boolean 맞는객체(int obýekt_Salgylanma, int Ad) {
        if (obýekt_Salgylanma == 0) return true;
        if (!객체유효(obýekt_Salgylanma)) return false;
        int 분류코드 = 힙[obýekt_Salgylanma];
        if (Söz_SMS(Ad, "java/lang/Object")) return true;
        if (분류코드 >= 32) return 종포함(분류코드 - 32, Ad);
        if (분류코드 == 9) { int niýet_salgy = 예외상수(Ad); return niýet_salgy != 0 && 예외포함(힙[obýekt_Salgylanma + 2], niýet_salgy); }
        if (분류코드 == 1) return Söz_SMS(Ad, "java/lang/String") || Söz_SMS(Ad, "java/lang/CharSequence");
        if (분류코드 == 4) return Söz_SMS(Ad, "java/lang/StringBuilder") || Söz_SMS(Ad, "java/lang/CharSequence");
        if (분류코드 == 10) return Söz_SMS(Ad, "java/util/ArrayList") || Söz_SMS(Ad, "java/util/List");
        if (분류코드 == 11) return Söz_SMS(Ad, "java/util/HashMap") || Söz_SMS(Ad, "java/util/Map");
        if (분류코드 == 12) return Söz_SMS(Ad, "java/lang/Integer") || Söz_SMS(Ad, "java/lang/Number");
        if (분류코드 >= 24 && 분류코드 <= 28 && 힙[obýekt_Salgylanma + 13] != 0) return 한국어화면종(Ad) == 분류코드 || Söz_SMS(Ad, "한국어/자체/화면구성요소");
        if (분류코드 >= 24 && 분류코드 <= 28) return (한국어화면종(Ad) == 0 && 화면종(Ad) == 분류코드) || Söz_SMS(Ad, "java/awt/Component") || Söz_SMS(Ad, "java/awt/Container") || Söz_SMS(Ad, "javax/swing/JComponent");
        if (분류코드 == 29) return Söz_SMS(Ad, 힙[obýekt_Salgylanma + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (분류코드 == 30) return Söz_SMS(Ad, "java/awt/FlowLayout") || Söz_SMS(Ad, "java/awt/LayoutManager");
        if (분류코드 == 17) return Söz_SMS(Ad, "java/net/Socket");
        if (분류코드 == 18) return Söz_SMS(Ad, "java/net/ServerSocket");
        if (분류코드 == 19) return Söz_SMS(Ad, 힙[obýekt_Salgylanma + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (분류코드 == 14) return Söz_SMS(Ad, "java/net/InetAddress");
        if (분류코드 == 15) return Söz_SMS(Ad, "java/net/DatagramSocket");
        if (분류코드 == 16) return Söz_SMS(Ad, "java/net/DatagramPacket");
        if (분류코드 == 13) return Söz_SMS(Ad, 힙[obýekt_Salgylanma + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (분류코드 == 2) return Söz_SMS(Ad, "[I"); if (분류코드 == 20) return Söz_SMS(Ad, "[B"); if (분류코드 == 21) return Söz_SMS(Ad, "[Z");
        if (분류코드 == 22) return Söz_SMS(Ad, "[C"); if (분류코드 == 23) return Söz_SMS(Ad, "[S");
        if (분류코드 != 3) return false;
        if (Söz_SMS(Ad, "[Ljava/lang/Object;")) return true;
        int komponent = ARRAY_element[obýekt_Salgylanma];
        if (komponent == -1) return Söz_SMS(Ad, "[Ljava/lang/String;") || Söz_SMS(Ad, "[Ljava/lang/CharSequence;");
        if (komponent == 0) return false;
        if (배열종비교(komponent, Ad)) return true;
        if ((Söz_SMS(komponent, "java/lang/String") || Söz_SMS(komponent, "java/lang/StringBuilder")) && Söz_SMS(Ad, "[Ljava/lang/CharSequence;")) return true;
        for (int sikl_indeks = 0; sikl_indeks < 종수; sikl_indeks++) if (같은말(klas_Kesgitleme_at[sikl_indeks], komponent)) {
            for (int nyşanyň_kody = sikl_indeks, 중첩깊이 = 0; nyşanyň_kody >= 0 && 중첩깊이 < 16; 중첩깊이++, nyşanyň_kody = 부모종(nyşanyň_kody)) {
                if (배열종비교(종부모[nyşanyň_kody], Ad)) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[nyşanyň_kody]; 안쪽자리++) if (배열종비교(klas_interfeýs[nyşanyň_kody * 16 + 안쪽자리], Ad)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int at_hemişelik, int 형식참조) {
        int 검사자리 = 상가[형식참조], 항목수 = 상나[형식참조];
        if (at_hemişelik == 0 || 항목수 < 4 || Faýl[검사자리] != '[' || Faýl[검사자리 + 1] != 'L' || Faýl[검사자리 + 항목수 - 1] != ';' || 상나[at_hemişelik] != 항목수 - 3) return false;
        for (int sikl_indeks = 0; sikl_indeks < 항목수 - 3; sikl_indeks++) if (Faýl[상가[at_hemişelik] + sikl_indeks] != Faýl[검사자리 + 2 + sikl_indeks]) return false;
        return true;
    }
    static void 예외처리() {
        if (던진객체 == 0) return;
        Hata = false;
        while (kadr_indeks >= 현재가닥 * 32) {
            int faýl_indeks = kadr_usul[kadr_indeks], 읽는자리 = kadr_instruksiýa[kadr_indeks];
            for (int sikl_indeks = 0; sikl_indeks < 잡기수; sikl_indeks++) if (잡기함수[sikl_indeks] == faýl_indeks && 읽는자리 >= 잡기시작[sikl_indeks] && 읽는자리 < 잡기끝[sikl_indeks]
                && (잡기종[sikl_indeks] == 0 || 맞는객체(던진객체, 잡기종[sikl_indeks]))) {
                틀위치[kadr_indeks] = 잡기위치[sikl_indeks]; kadr_Desse[kadr_indeks] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (ulanyşa_taýýarla_kadr[kadr_indeks] != 0) klas_Kesgitleme_ýagdaý[ulanyşa_taýýarla_kadr[kadr_indeks] - 1] = 3;
            if (틀잠금[kadr_indeks] != 0) { 잠금풀기(틀잠금[kadr_indeks]); 틀잠금[kadr_indeks] = 0; }
            kadr_indeks--;
        }
        ulanyjy.Ýaz("Uncaught ");
        if (힙[던진객체] == 9) { ulanyjy.Ýaz(예외이름(힙[던진객체 + 2])); ulanyjy.Ýaz(": "); ýaz_SMS(힙[던진객체 + 3]); }
        else ulanyjy.Ýaz("user exception");
        ulanyjy.ýaz_nyşan_baha(10); 던진객체 = 0; Hata = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void Desse_instruksiýa(int 명령코드) {
        int 첫값 = 빼기(0), 첫형식 = 반환형;
        if (명령코드 == 87) return;
        if (명령코드 == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int baýt_maglumat = 빼기(0), 둘째형식 = 반환형;
        if (명령코드 == 88) return;
        if (명령코드 == 90) { 넣기(첫값, 첫형식); 넣기(baýt_maglumat, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 92) { 넣기(baýt_maglumat, 둘째형식); 넣기(첫값, 첫형식); 넣기(baýt_maglumat, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 95) { 넣기(첫값, 첫형식); 넣기(baýt_maglumat, 둘째형식); return; }
        int nyşanyň_kody = 빼기(0), 셋째형식 = 반환형;
        if (명령코드 == 91) { 넣기(첫값, 첫형식); 넣기(nyşanyň_kody, 셋째형식); 넣기(baýt_maglumat, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 93) { 넣기(baýt_maglumat, 둘째형식); 넣기(첫값, 첫형식); 넣기(nyşanyň_kody, 셋째형식); 넣기(baýt_maglumat, 둘째형식); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = 반환형;
        넣기(baýt_maglumat, 둘째형식); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(nyşanyň_kody, 셋째형식); 넣기(baýt_maglumat, 둘째형식); 넣기(첫값, 첫형식);
    }
    static void 새객체(int at_hemişelik, int 시작점) {
        int 분류코드 = 0, 유효길이 = 0, 예외참조 = 예외상수(at_hemişelik);
        if (Söz_SMS(at_hemişelik, "java/lang/StringBuilder")) { 분류코드 = 4; 유효길이 = 1; }
        if (Söz_SMS(at_hemişelik, "java/io/FileInputStream")) { 분류코드 = 5; 유효길이 = 2; }
        if (Söz_SMS(at_hemişelik, "java/io/FileOutputStream")) { 분류코드 = 6; 유효길이 = 2; }
        if (예외참조 != 0) { 분류코드 = 9; 유효길이 = 2; }
        if (Söz_SMS(at_hemişelik, "java/util/ArrayList")) { 분류코드 = 10; 유효길이 = 2; }
        if (Söz_SMS(at_hemişelik, "java/util/HashMap")) { 분류코드 = 11; 유효길이 = 2; }
        if (Söz_SMS(at_hemişelik, "java/lang/Integer")) { 분류코드 = 12; 유효길이 = 1; }
        if (Söz_SMS(at_hemişelik, "java/net/Socket")) { 분류코드 = 17; 유효길이 = 5; }
        if (Söz_SMS(at_hemişelik, "java/net/ServerSocket")) { 분류코드 = 18; 유효길이 = 5; }
        if (Söz_SMS(at_hemişelik, "java/net/DatagramSocket")) { 분류코드 = 15; 유효길이 = 3; }
        if (Söz_SMS(at_hemişelik, "java/net/DatagramPacket")) { 분류코드 = 16; 유효길이 = 4; }
        if (Söz_SMS(at_hemişelik, "java/lang/Thread") || Söz_SMS(at_hemişelik, "한국어/자체/작업가닥")) { 분류코드 = 13; 유효길이 = 2; }
        if (Söz_SMS(at_hemişelik, "java/lang/Object")) { 분류코드 = 8; }
        if (분류코드 == 0 && 화면종(at_hemişelik) != 0) { 분류코드 = 화면종(at_hemişelik); 유효길이 = 12; }
        if (분류코드 == 0) {
            int nyşanyň_kody = tap_klas_Kesgitleme(at_hemişelik); if (nyşanyň_kody < 0 || Hata || !ulanyşa_taýýarla(nyşanyň_kody, 시작점)) return;
            분류코드 = 32 + nyşanyň_kody; 유효길이 = 종칸수[nyşanyň_kody];
        }
        int obýekt_Salgylanma = bölüp_aýyr_Ammar(분류코드, 유효길이); if (Hata) return;
        if (분류코드 == 13 && Söz_SMS(at_hemişelik, "한국어/자체/작업가닥")) 힙[obýekt_Salgylanma + 3] = 1;
        if (분류코드 >= 24 && 분류코드 <= 28 && 한국어화면종(at_hemişelik) != 0) 힙[obýekt_Salgylanma + 13] = 1;
        if (분류코드 == 5 || 분류코드 == 6 || 분류코드 == 15 || 분류코드 == 17 || 분류코드 == 18) 힙[obýekt_Salgylanma + 2] = -1;
        if (분류코드 == 9) 힙[obýekt_Salgylanma + 2] = 예외참조;
        넣기(obýekt_Salgylanma, 2);
    }
    static boolean 값같음(int 첫값, int baýt_maglumat) {
        if (첫값 == baýt_maglumat) return true;
        if (첫값 == 0 || baýt_maglumat == 0 || 첫값 < 0 || baýt_maglumat < 0 || 첫값 >= 힙끝 || baýt_maglumat >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[baýt_maglumat] == 1) return 글같음(첫값, baýt_maglumat, false);
        return 힙[첫값] == 12 && 힙[baýt_maglumat] == 12 && 힙[첫값 + 2] == 힙[baýt_maglumat + 2];
    }
    static int 글조각(int obýekt_Salgylanma, int 시작자리, int 끝자리) {
        if (!obýekt_baha(obýekt_Salgylanma, 1)) return 0;
        if (시작자리 < 0 || 끝자리 < 시작자리 || 끝자리 > 힙[obýekt_Salgylanma + 1]) { näsazlyk_baha("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = bölüp_aýyr_Ammar(1, 끝자리 - 시작자리); if (Hata) return 0;
        for (int sikl_indeks = 시작자리; sikl_indeks < 끝자리; sikl_indeks++) 힙[반환값 + 2 + sikl_indeks - 시작자리] = 힙[obýekt_Salgylanma + 2 + sikl_indeks];
        return 반환값;
    }
    static int goşul_SMS(int 첫값, int baýt_maglumat) {
        if (!obýekt_baha(첫값, 1) || !obýekt_baha(baýt_maglumat, 1)) return 0;
        int 항목수 = 힙[첫값 + 1], usul_indeks = 힙[baýt_maglumat + 1], 반환값 = bölüp_aýyr_Ammar(1, 항목수 + usul_indeks); if (Hata) return 0;
        for (int sikl_indeks = 0; sikl_indeks < 항목수; sikl_indeks++) 힙[반환값 + 2 + sikl_indeks] = 힙[첫값 + 2 + sikl_indeks];
        for (int sikl_indeks = 0; sikl_indeks < usul_indeks; sikl_indeks++) 힙[반환값 + 2 + 항목수 + sikl_indeks] = 힙[baýt_maglumat + 2 + sikl_indeks];
        return 반환값;
    }
    static boolean 기본호출(int eýe, int at_hemişelik, int 서술상수, int 명령코드) {
        if (Söz_SMS(eýe, "한국어/자체/실행인수") && 명령코드 == 184) {
            if (Söz_SMS(at_hemişelik, "개수") && Söz_SMS(서술상수, "()I")) { 넣기(ulanyjy.인수개수() - 1, 1); return true; }
            if (Söz_SMS(at_hemişelik, "Metin") && Söz_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= ulanyjy.인수개수() - 1) 예외던짐(29, "ýerine_ýetir_buýruk 인수 범위를 벗어났습니다");
                else 넣기(esasy_nyşan(ulanyjy.인수(순번 + 1)), 2);
                return true;
            }
            näsazlyk_baha("지원하지 않는 한국어 ýerine_ýetir_buýruk 인수 호출"); return true;
        }
        if (Söz_SMS(eýe, "한국어/자체/작업가닥")) { Proses_akym(at_hemişelik, 서술상수, 명령코드, true); return true; }
        if (한국어화면소유(eýe)) { 한국어화면호출(eýe, at_hemişelik, 서술상수, 명령코드); return true; }
        if (화면소유(eýe)) { 화면호출(eýe, at_hemişelik, 서술상수, 명령코드); return true; }
        if (Söz_SMS(eýe, "java/net/Socket") || Söz_SMS(eýe, "java/net/ServerSocket") || Söz_SMS(eýe, "java/io/InputStream") || Söz_SMS(eýe, "java/io/OutputStream")) { 흐름호출(eýe, at_hemişelik, 서술상수, 명령코드); return true; }
        if (Söz_SMS(eýe, "한국어/자체/ýadro_baha") && 명령코드 == 184) {
            if (Söz_SMS(at_hemişelik, "화면너비") && Söz_SMS(서술상수, "()I")) { 넣기(ulanyjy.화면너비(), 1); return true; }
            if (Söz_SMS(at_hemişelik, "화면높이") && Söz_SMS(서술상수, "()I")) { 넣기(ulanyjy.화면높이(), 1); return true; }
            if (Söz_SMS(at_hemişelik, "밀리초") && Söz_SMS(서술상수, "()I")) { 넣기(ulanyjy.밀리초(), 1); return true; }
            if (Söz_SMS(at_hemişelik, "그림대기") && Söz_SMS(서술상수, "()I")) { 넣기(ulanyjy.그림대기(), 1); return true; }
            if (Söz_SMS(at_hemişelik, "사각형") && Söz_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), x_koordinatasy = 빼기(1); 넣기(ulanyjy.사각형(x_koordinatasy, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Söz_SMS(eýe, "java/net/InetAddress") || Söz_SMS(eýe, "java/net/DatagramPacket") || Söz_SMS(eýe, "java/net/DatagramSocket")) { 통신호출(eýe, at_hemişelik, 서술상수, 명령코드); return true; }
        if (Söz_SMS(eýe, "java/lang/Thread")) { 가닥호출(at_hemişelik, 서술상수, 명령코드); return true; }
        if (Söz_SMS(eýe, "java/lang/Object")) {
            if (Söz_SMS(at_hemişelik, "<init>") && Söz_SMS(서술상수, "()V") && 명령코드 == 183) { 객체유효(빼기(2)); return true; }
            if (Söz_SMS(at_hemişelik, "equals") && Söz_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int baýt_maglumat = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == baýt_maglumat ? 1 : 0, 1); return true; }
        }
        if (예외상수(eýe) != 0) {
            if (Söz_SMS(at_hemişelik, "<init>") && 명령코드 == 183 && (Söz_SMS(서술상수, "()V") || Söz_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int çagyryş = Söz_SMS(서술상수, "()V") ? 0 : 빼기(2), obýekt_Salgylanma = 빼기(2);
                if (obýekt_baha(obýekt_Salgylanma, 9)) { 힙[obýekt_Salgylanma + 3] = çagyryş; 힙참조[obýekt_Salgylanma + 3] = 1; } return true;
            }
            if ((Söz_SMS(at_hemişelik, "getMessage") || Söz_SMS(at_hemişelik, "설명")) && Söz_SMS(서술상수, "()Ljava/lang/String;")) { int obýekt_Salgylanma = 빼기(2); if (obýekt_baha(obýekt_Salgylanma, 9)) 넣기(힙[obýekt_Salgylanma + 3], 2); return true; }
        }
        if (Söz_SMS(eýe, "java/lang/String")) {
            if (명령코드 == 182 && Söz_SMS(at_hemişelik, "getBytes") && (Söz_SMS(서술상수, "()[B") || Söz_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int kodlaşdyrma_at = Söz_SMS(서술상수, "()[B") ? 0 : 빼기(2), obýekt_Salgylanma = 빼기(2);
                if (!obýekt_baha(obýekt_Salgylanma, 1)) return true;
                if (kodlaşdyrma_at != 0 && !글같음(kodlaşdyrma_at, esasy_nyşan("UTF-8"), false) && !글같음(kodlaşdyrma_at, esasy_nyşan("UTF8"), false) && !글같음(kodlaşdyrma_at, esasy_nyşan("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int 항목수 = 힙[obýekt_Salgylanma + 1], 반환값 = bölüp_aýyr_Ammar(20, 항목수 * 3), 사용수 = 0; if (Hata) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) {
                    int nyşanyň_kody = 힙[obýekt_Salgylanma + 2 + 안쪽자리];
                    if (nyşanyň_kody >= 0xd800 && nyşanyň_kody <= 0xdbff && 안쪽자리 + 1 < 항목수 && 힙[obýekt_Salgylanma + 3 + 안쪽자리] >= 0xdc00 && 힙[obýekt_Salgylanma + 3 + 안쪽자리] <= 0xdfff) nyşanyň_kody = 0x10000 + ((nyşanyň_kody - 0xd800) << 10) + 힙[obýekt_Salgylanma + 2 + ++안쪽자리] - 0xdc00;
                    else if (nyşanyň_kody >= 0xd800 && nyşanyň_kody <= 0xdfff) nyşanyň_kody = '?';
                    if (nyşanyň_kody < 128) 힙[반환값 + 2 + 사용수++] = nyşanyň_kody;
                    else { int 바이트수 = nyşanyň_kody < 2048 ? 2 : nyşanyň_kody < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((바이트수 == 2 ? 192 : 바이트수 == 3 ? 224 : 240) | nyşanyň_kody >> (6 * (바이트수 - 1))); for (int 비교자리 = 바이트수 - 1; 비교자리 > 0; 비교자리--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | nyşanyň_kody >> (6 * (비교자리 - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (명령코드 == 184 && Söz_SMS(at_hemişelik, "valueOf") && Söz_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(san_nyşan(빼기(1)), 2); return true; }
            if (명령코드 != 182) return false;
            if (Söz_SMS(at_hemişelik, "equals") && Söz_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int baýt_maglumat = 빼기(2), 첫값 = 빼기(2); if (obýekt_baha(첫값, 1)) 넣기(글같음(첫값, baýt_maglumat, false) ? 1 : 0, 1); return true; }
            if (Söz_SMS(at_hemişelik, "isEmpty") && Söz_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (obýekt_baha(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Söz_SMS(at_hemişelik, "substring") && (Söz_SMS(서술상수, "(I)Ljava/lang/String;") || Söz_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean 둘째값 = Söz_SMS(서술상수, "(II)Ljava/lang/String;"); int 끝자리 = 둘째값 ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (obýekt_baha(첫값, 1)) 넣기(글조각(첫값, 시작점, 둘째값 ? 끝자리 : 힙[첫값 + 1]), 2); return true;
            }
            if (Söz_SMS(at_hemişelik, "concat") && Söz_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int baýt_maglumat = 빼기(2), 첫값 = 빼기(2); 넣기(goşul_SMS(첫값, baýt_maglumat), 2); return true; }
            if (Söz_SMS(at_hemişelik, "hashCode") && Söz_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), heş_kody_baha = 0; if (obýekt_baha(첫값, 1)) { for (int sikl_indeks = 0; sikl_indeks < 힙[첫값 + 1]; sikl_indeks++) heş_kody_baha = heş_kody_baha * 31 + 힙[첫값 + 2 + sikl_indeks]; 넣기(heş_kody_baha, 1); } return true; }
            if (Söz_SMS(at_hemişelik, "toString") && Söz_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (obýekt_baha(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Söz_SMS(eýe, "java/lang/Integer")) {
            if (명령코드 == 184 && Söz_SMS(at_hemişelik, "valueOf") && Söz_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int maglumat_baha = 빼기(1), obýekt_Salgylanma = maglumat_baha >= -128 && maglumat_baha <= 127 ? Store_bitin[maglumat_baha + 128] : 0; if (obýekt_Salgylanma == 0) { obýekt_Salgylanma = bölüp_aýyr_Ammar(12, 1); if (!Hata) { 힙[obýekt_Salgylanma + 2] = maglumat_baha; if (maglumat_baha >= -128 && maglumat_baha <= 127) Store_bitin[maglumat_baha + 128] = obýekt_Salgylanma; } } 넣기(obýekt_Salgylanma, 2); return true; }
            if (명령코드 == 183 && Söz_SMS(at_hemişelik, "<init>") && Söz_SMS(서술상수, "(I)V")) { int maglumat_baha = 빼기(1), obýekt_Salgylanma = 빼기(2); if (obýekt_baha(obýekt_Salgylanma, 12)) 힙[obýekt_Salgylanma + 2] = maglumat_baha; return true; }
            if (명령코드 == 182 && Söz_SMS(at_hemişelik, "intValue") && Söz_SMS(서술상수, "()I")) { int obýekt_Salgylanma = 빼기(2); if (obýekt_baha(obýekt_Salgylanma, 12)) 넣기(힙[obýekt_Salgylanma + 2], 1); return true; }
            if (명령코드 == 184 && Söz_SMS(at_hemişelik, "toString") && Söz_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(san_nyşan(빼기(1)), 2); return true; }
        }
        if (Söz_SMS(eýe, "java/lang/Math") && 명령코드 == 184) {
            if (Söz_SMS(at_hemişelik, "abs") && Söz_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Söz_SMS(at_hemişelik, "min") || Söz_SMS(at_hemişelik, "max")) && Söz_SMS(서술상수, "(II)I")) { int baýt_maglumat = 빼기(1), 첫값 = 빼기(1); 넣기(Söz_SMS(at_hemişelik, "min") ? (첫값 < baýt_maglumat ? 첫값 : baýt_maglumat) : (첫값 > baýt_maglumat ? 첫값 : baýt_maglumat), 1); return true; }
        }
        if (Söz_SMS(eýe, "java/lang/System") && 명령코드 == 184) {
            if (Söz_SMS(at_hemişelik, "gc") && Söz_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Söz_SMS(at_hemişelik, "arraycopy") && Söz_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int 항목수 = 빼기(1), barylmaly_ýer_baha_indeks = 빼기(1), baýt_maglumat = 빼기(2), 시작자리 = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(baýt_maglumat)) {
                    int 분류코드 = 힙[첫값];
                    if (힙[baýt_maglumat] != 분류코드 || (분류코드 != 2 && 분류코드 != 3 && (분류코드 < 20 || 분류코드 > 23))) näsazlyk_baha("arraycopy type mismatch");
                    else if (항목수 < 0 || 시작자리 < 0 || barylmaly_ýer_baha_indeks < 0 || 시작자리 > 힙[첫값 + 1] - 항목수 || barylmaly_ýer_baha_indeks > 힙[baýt_maglumat + 1] - 항목수) näsazlyk_baha("ArrayIndexOutOfBoundsException");
                    else if (첫값 == baýt_maglumat && barylmaly_ýer_baha_indeks > 시작자리) { for (int sikl_indeks = 항목수 - 1; sikl_indeks >= 0; sikl_indeks--) 힙[baýt_maglumat + 2 + barylmaly_ýer_baha_indeks + sikl_indeks] = 힙[첫값 + 2 + 시작자리 + sikl_indeks]; }
                    else { for (int sikl_indeks = 0; sikl_indeks < 항목수 && !Hata; sikl_indeks++) { int maglumat_baha = 힙[첫값 + 2 + 시작자리 + sikl_indeks]; if (분류코드 != 3 || 배열저장가능(baýt_maglumat, maglumat_baha)) 힙[baýt_maglumat + 2 + barylmaly_ýer_baha_indeks + sikl_indeks] = maglumat_baha; } }
                }
                return true;
            }
        }
        if (Söz_SMS(eýe, "java/util/ArrayList") || Söz_SMS(eýe, "java/util/List") || Söz_SMS(eýe, "java/util/HashMap") || Söz_SMS(eýe, "java/util/Map")) {
            모음호출(eýe, at_hemişelik, 서술상수, 명령코드); return true;
        }
        return false;
    }
    static void 모음늘리기(int obýekt_Salgylanma, int 필요수) {
        int 이전값 = 힙[obýekt_Salgylanma + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int 다음자리 = 용량값 < 8 ? 8 : 용량값 * 2; if (다음자리 < 필요수) 다음자리 = 필요수;
        int maglumat_ARRAY = bölüp_aýyr_Ammar(3, 다음자리); if (Hata) return;
        for (int sikl_indeks = 0; sikl_indeks < 용량값; sikl_indeks++) 힙[maglumat_ARRAY + 2 + sikl_indeks] = 힙[이전값 + 2 + sikl_indeks];
        힙[obýekt_Salgylanma + 2] = maglumat_ARRAY; 힙참조[obýekt_Salgylanma + 2] = 1;
    }
    static void 모음호출(int eýe, int at_hemişelik, int 서술상수, int 명령코드) {
        boolean 대응참조 = Söz_SMS(eýe, "java/util/HashMap") || Söz_SMS(eýe, "java/util/Map"); int 분류코드 = 대응참조 ? 11 : 10;
        if (Söz_SMS(at_hemişelik, "<init>") && 명령코드 == 183 && Söz_SMS(서술상수, "()V")) { int obýekt_Salgylanma = 빼기(2); if (obýekt_baha(obýekt_Salgylanma, 분류코드)) 모음늘리기(obýekt_Salgylanma, 8); return; }
        if (명령코드 != 182 && 명령코드 != 185) { näsazlyk_baha("invalid collection invocation"); return; }
        if (Söz_SMS(at_hemişelik, "size") && Söz_SMS(서술상수, "()I") || Söz_SMS(at_hemişelik, "isEmpty") && Söz_SMS(서술상수, "()Z")) {
            int obýekt_Salgylanma = 빼기(2); if (obýekt_baha(obýekt_Salgylanma, 분류코드)) 넣기(Söz_SMS(at_hemişelik, "size") ? 힙[obýekt_Salgylanma + 3] : 힙[obýekt_Salgylanma + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Söz_SMS(at_hemişelik, "clear") && Söz_SMS(서술상수, "()V")) { int obýekt_Salgylanma = 빼기(2); if (obýekt_baha(obýekt_Salgylanma, 분류코드)) { int maglumat_ARRAY = 힙[obýekt_Salgylanma + 2]; for (int sikl_indeks = 0; sikl_indeks < 힙[maglumat_ARRAY + 1]; sikl_indeks++) 힙[maglumat_ARRAY + 2 + sikl_indeks] = 0; 힙[obýekt_Salgylanma + 3] = 0; } return; }
        if (!대응참조 && Söz_SMS(at_hemişelik, "add") && Söz_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int maglumat_baha = 빼기(2), obýekt_Salgylanma = 빼기(2); if (!obýekt_baha(obýekt_Salgylanma, 10)) return;
            int 항목수 = 힙[obýekt_Salgylanma + 3]; 모음늘리기(obýekt_Salgylanma, 항목수 + 1); if (!Hata) { 힙[힙[obýekt_Salgylanma + 2] + 2 + 항목수] = maglumat_baha; 힙[obýekt_Salgylanma + 3] = 항목수 + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Söz_SMS(at_hemişelik, "get") || Söz_SMS(at_hemişelik, "remove")) && Söz_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Söz_SMS(at_hemişelik, "set") && Söz_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Söz_SMS(at_hemişelik, "set"); int maglumat_baha = 지정여부 ? 빼기(2) : 0, 항목자리 = 빼기(1), obýekt_Salgylanma = 빼기(2);
            if (!obýekt_baha(obýekt_Salgylanma, 10)) return;
            int 항목수 = 힙[obýekt_Salgylanma + 3], maglumat_ARRAY = 힙[obýekt_Salgylanma + 2];
            if (항목자리 < 0 || 항목자리 >= 항목수) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[maglumat_ARRAY + 2 + 항목자리];
            if (지정여부) 힙[maglumat_ARRAY + 2 + 항목자리] = maglumat_baha;
            if (Söz_SMS(at_hemişelik, "remove")) { for (int sikl_indeks = 항목자리 + 1; sikl_indeks < 항목수; sikl_indeks++) 힙[maglumat_ARRAY + 1 + sikl_indeks] = 힙[maglumat_ARRAY + 2 + sikl_indeks]; 힙[maglumat_ARRAY + 1 + 항목수] = 0; 힙[obýekt_Salgylanma + 3] = 항목수 - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Söz_SMS(at_hemişelik, "get") || Söz_SMS(at_hemişelik, "remove")) && Söz_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Söz_SMS(at_hemişelik, "put") && Söz_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Söz_SMS(at_hemişelik, "containsKey") && Söz_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Söz_SMS(at_hemişelik, "put"), aýyr = Söz_SMS(at_hemişelik, "remove");
            int maglumat_baha = 넣기여부 ? 빼기(2) : 0, açar_Salgylanma = 빼기(2), obýekt_Salgylanma = 빼기(2); if (!obýekt_baha(obýekt_Salgylanma, 11)) return;
            int 항목수 = 힙[obýekt_Salgylanma + 3], maglumat_ARRAY = 힙[obýekt_Salgylanma + 2], 찾은여부 = -1;
            for (int sikl_indeks = 0; sikl_indeks < 항목수; sikl_indeks++) if (값같음(açar_Salgylanma, 힙[maglumat_ARRAY + 2 + 2 * sikl_indeks])) { 찾은여부 = sikl_indeks; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[maglumat_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(obýekt_Salgylanma, (항목수 + 1) * 2); maglumat_ARRAY = 힙[obýekt_Salgylanma + 2]; 찾은여부 = 항목수; if (!Hata) 힙[obýekt_Salgylanma + 3] = 항목수 + 1; }
                if (!Hata) { 힙[maglumat_ARRAY + 2 + 2 * 찾은여부] = açar_Salgylanma; 힙[maglumat_ARRAY + 3 + 2 * 찾은여부] = maglumat_baha; }
            }
            if (aýyr && 찾은여부 >= 0) { for (int sikl_indeks = 찾은여부 + 1; sikl_indeks < 항목수; sikl_indeks++) { 힙[maglumat_ARRAY + 2 * sikl_indeks] = 힙[maglumat_ARRAY + 2 + 2 * sikl_indeks]; 힙[maglumat_ARRAY + 1 + 2 * sikl_indeks] = 힙[maglumat_ARRAY + 3 + 2 * sikl_indeks]; } 힙[maglumat_ARRAY + 2 * 항목수] = 0; 힙[maglumat_ARRAY + 1 + 2 * 항목수] = 0; 힙[obýekt_Salgylanma + 3] = 항목수 - 1; }
            if (Söz_SMS(at_hemişelik, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        näsazlyk_baha("unsupported collection method");
    }
    static boolean 잠금얻기(int obýekt_Salgylanma) {
        if (!객체유효(obýekt_Salgylanma)) return false;
        if (잠금깊이[obýekt_Salgylanma] != 0 && 잠금주인[obýekt_Salgylanma] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        잠금주인[obýekt_Salgylanma] = 현재가닥 + 1; 잠금깊이[obýekt_Salgylanma]++; return true;
    }
    static void 잠금풀기(int obýekt_Salgylanma) {
        if (!객체유효(obýekt_Salgylanma)) return;
        if (잠금깊이[obýekt_Salgylanma] == 0 || 잠금주인[obýekt_Salgylanma] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[obýekt_Salgylanma] == 0) 잠금주인[obýekt_Salgylanma] = 0;
    }
    static boolean calşyr_akym() {
        akym_kadr[현재가닥] = kadr_indeks;
        if (kadr_indeks < 현재가닥 * 32) akym_ýagdaý[현재가닥] = 3;
        for (int sikl_indeks = 0; sikl_indeks < 가닥수; sikl_indeks++) if (akym_ýagdaý[sikl_indeks] == 2 && akym_ýagdaý[가닥대기[sikl_indeks]] == 3) akym_ýagdaý[sikl_indeks] = 1;
        for (int sikl_indeks = 1; sikl_indeks <= 가닥수; sikl_indeks++) {
            int 다음자리 = (현재가닥 + sikl_indeks) % 가닥수;
            if (akym_ýagdaý[다음자리] == 1) { 현재가닥 = 다음자리; kadr_indeks = akym_kadr[다음자리]; 바꿈요청 = false; return true; }
        }
        for (int sikl_indeks = 0; sikl_indeks < 가닥수; sikl_indeks++) if (akym_ýagdaý[sikl_indeks] != 3) { näsazlyk_baha("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int at_hemişelik, int 서술상수, int 명령코드) { Proses_akym(at_hemişelik, 서술상수, 명령코드, false); }
    static void Proses_akym(int at_hemişelik, int 서술상수, int 명령코드, boolean 한국어) {
        if (명령코드 == 184 && Söz_SMS(at_hemişelik, 한국어 ? "togtatmak_tabşyryk" : "yield") && Söz_SMS(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (명령코드 == 184 && Söz_SMS(at_hemişelik, "currentThread") && Söz_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(akym_obýekt[현재가닥], 2); return; }
        if (명령코드 == 183 && Söz_SMS(at_hemişelik, "<init>") && (Söz_SMS(서술상수, "()V") || Söz_SMS(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int niýet_salgy = Söz_SMS(서술상수, "()V") ? 0 : 빼기(2), obýekt_Salgylanma = 빼기(2);
            if (!객체유효(obýekt_Salgylanma)) return;
            if (힙[obýekt_Salgylanma] == 13) { 힙[obýekt_Salgylanma + 2] = niýet_salgy; 힙참조[obýekt_Salgylanma + 2] = 1; }
            else if (niýet_salgy != 0) näsazlyk_baha("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (명령코드 == 182 && (Söz_SMS(at_hemişelik, 한국어 ? "başlat_tabşyryk" : "start") || Söz_SMS(at_hemişelik, 한국어 ? "기다리기" : "join")) && Söz_SMS(서술상수, "()V") || 명령코드 == 182 && Söz_SMS(at_hemişelik, 한국어 ? "살아있는가" : "isAlive") && Söz_SMS(서술상수, "()Z")) {
            int obýekt_Salgylanma = 빼기(2); if (!객체유효(obýekt_Salgylanma)) return;
            int hasap_baha = -1; for (int sikl_indeks = 0; sikl_indeks < 가닥수; sikl_indeks++) if (akym_obýekt[sikl_indeks] == obýekt_Salgylanma) hasap_baha = sikl_indeks;
            if (Söz_SMS(at_hemişelik, 한국어 ? "살아있는가" : "isAlive")) { 넣기(hasap_baha >= 0 && akym_ýagdaý[hasap_baha] != 3 ? 1 : 0, 1); return; }
            if (Söz_SMS(at_hemişelik, 한국어 ? "기다리기" : "join")) { if (hasap_baha >= 0 && akym_ýagdaý[hasap_baha] != 3) { 가닥대기[현재가닥] = hasap_baha; akym_ýagdaý[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (hasap_baha >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (가닥수 == 4) { näsazlyk_baha("thread limit (4 including main)"); return; }
            int niýet_salgy = 힙[obýekt_Salgylanma] == 13 ? 힙[obýekt_Salgylanma + 2] : obýekt_Salgylanma;
            int faýl_indeks = niýet_salgy > 0 && 힙[niýet_salgy] >= 32 ? at_usul(힙[niýet_salgy] - 32, 한국어 ? "ýerine_ýetir_tabşyryk" : "run", "()V") : -1;
            if (niýet_salgy != 0 && faýl_indeks < 0) { näsazlyk_baha("Runnable.run required"); return; }
            hasap_baha = 가닥수++; akym_obýekt[hasap_baha] = obýekt_Salgylanma; akym_niýet[hasap_baha] = niýet_salgy;
            int kadr = hasap_baha * 32; akym_kadr[hasap_baha] = faýl_indeks < 0 ? kadr - 1 : kadr; akym_ýagdaý[hasap_baha] = faýl_indeks < 0 ? 3 : 1;
            if (faýl_indeks >= 0) { kadr_usul[kadr] = faýl_indeks; 틀위치[kadr] = usul_başlat[faýl_indeks]; ýerli_baha[kadr * 128] = niýet_salgy; ýerli_ýaz[kadr * 128] = 2; }
            return;
        }
        näsazlyk_baha("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], salgy_SMS = new int[16];
    static int ýerli_salgy() { return salgy_obýekt(0x7f000001); }
    static int salgy_obýekt(int baha) { int obýekt_Salgylanma = bölüp_aýyr_Ammar(14, 1); if (!Hata) 힙[obýekt_Salgylanma + 2] = baha; return obýekt_Salgylanma; }
    static int 주소해독(int obýekt_Salgylanma) {
        if (obýekt_Salgylanma == 0 || 글같음(obýekt_Salgylanma, esasy_nyşan("localhost"), false)) return 0x7f000001;
        if (!obýekt_baha(obýekt_Salgylanma, 1)) return 0;
        int maglumat_baha = 0, 총수 = 0, salgy_baýt = 0, 자릿수 = 0, 항목수 = 힙[obýekt_Salgylanma + 1];
        for (int sikl_indeks = 0; sikl_indeks <= 항목수; sikl_indeks++) {
            int nyşanyň_kody = sikl_indeks == 항목수 ? '.' : 힙[obýekt_Salgylanma + 2 + sikl_indeks];
            if (nyşanyň_kody == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } maglumat_baha = maglumat_baha << 8 | salgy_baýt; 총수++; salgy_baýt = 자릿수 = 0; }
            else { if (nyşanyň_kody < '0' || nyşanyň_kody > '9' || ++자릿수 > 3 || (salgy_baýt = salgy_baýt * 10 + nyşanyň_kody - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return maglumat_baha;
    }
    static int salgy_nyşan(int maglumat_baha) {
        int 항목수 = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int salgy_baýt = maglumat_baha >>> 이동비트 & 255;
            if (salgy_baýt >= 100) salgy_SMS[항목수++] = '0' + salgy_baýt / 100;
            if (salgy_baýt >= 10) salgy_SMS[항목수++] = '0' + salgy_baýt / 10 % 10;
            salgy_SMS[항목수++] = '0' + salgy_baýt % 10; if (이동비트 != 0) salgy_SMS[항목수++] = '.';
        }
        int obýekt_Salgylanma = bölüp_aýyr_Ammar(1, 항목수); if (!Hata) for (int sikl_indeks = 0; sikl_indeks < 항목수; sikl_indeks++) 힙[obýekt_Salgylanma + 2 + sikl_indeks] = salgy_SMS[sikl_indeks]; return obýekt_Salgylanma;
    }
    static void 통신호출(int eýe, int at_hemişelik, int 서술상수, int 명령코드) {
        if (Söz_SMS(eýe, "java/net/InetAddress")) {
            if (명령코드 == 184 && Söz_SMS(at_hemişelik, "getLoopbackAddress") && Söz_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(ýerli_salgy(), 2); return; }
            if (명령코드 == 184 && Söz_SMS(at_hemişelik, "getByName") && Söz_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int maglumat_baha = 주소해독(빼기(2)); if (던진객체 == 0 && !Hata) 넣기(salgy_obýekt(maglumat_baha), 2); return;
            }
            if (명령코드 == 182 && Söz_SMS(at_hemişelik, "getHostAddress") && Söz_SMS(서술상수, "()Ljava/lang/String;")) { int obýekt_Salgylanma = 빼기(2); if (obýekt_baha(obýekt_Salgylanma, 14)) 넣기(salgy_nyşan(힙[obýekt_Salgylanma + 2]), 2); return; }
        }
        if (Söz_SMS(eýe, "java/net/DatagramPacket")) {
            if (명령코드 == 183 && Söz_SMS(at_hemişelik, "<init>") && (Söz_SMS(서술상수, "([BI)V") || Söz_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean barylmaly_ýer_baha_Salgylanma = Söz_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = barylmaly_ýer_baha_Salgylanma ? 빼기(1) : 0, salgy_Salgylanma = barylmaly_ýer_baha_Salgylanma ? 빼기(2) : 0;
                int 항목수 = 빼기(1), maglumat_ARRAY = 빼기(2), obýekt_Salgylanma = 빼기(2);
                if (!obýekt_baha(obýekt_Salgylanma, 16) || !obýekt_baha(maglumat_ARRAY, 20)) return;
                if (항목수 < 0 || 항목수 > 힙[maglumat_ARRAY + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (salgy_Salgylanma != 0 && !obýekt_baha(salgy_Salgylanma, 14)) return;
                힙[obýekt_Salgylanma + 2] = maglumat_ARRAY; 힙참조[obýekt_Salgylanma + 2] = 1; 힙[obýekt_Salgylanma + 3] = 항목수;
                힙[obýekt_Salgylanma + 4] = salgy_Salgylanma; 힙참조[obýekt_Salgylanma + 4] = 1; 힙[obýekt_Salgylanma + 5] = 접속번호; return;
            }
            if (명령코드 == 182 && Söz_SMS(at_hemişelik, "setLength") && Söz_SMS(서술상수, "(I)V")) {
                int 항목수 = 빼기(1), obýekt_Salgylanma = 빼기(2); if (!obýekt_baha(obýekt_Salgylanma, 16)) return;
                if (항목수 < 0 || 항목수 > 힙[힙[obýekt_Salgylanma + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[obýekt_Salgylanma + 3] = 항목수; return;
            }
            if (명령코드 == 182 && (Söz_SMS(at_hemişelik, "getData") && Söz_SMS(서술상수, "()[B") || Söz_SMS(at_hemişelik, "getLength") && Söz_SMS(서술상수, "()I") || Söz_SMS(at_hemişelik, "getAddress") && Söz_SMS(서술상수, "()Ljava/net/InetAddress;") || Söz_SMS(at_hemişelik, "getPort") && Söz_SMS(서술상수, "()I"))) {
                int obýekt_Salgylanma = 빼기(2); if (!obýekt_baha(obýekt_Salgylanma, 16)) return;
                int 항목자리 = Söz_SMS(at_hemişelik, "getData") ? 2 : Söz_SMS(at_hemişelik, "getLength") ? 3 : Söz_SMS(at_hemişelik, "getAddress") ? 4 : 5;
                넣기(힙[obýekt_Salgylanma + 항목자리], 항목자리 == 2 || 항목자리 == 4 ? 2 : 1); return;
            }
        }
        if (Söz_SMS(eýe, "java/net/DatagramSocket")) {
            if (명령코드 == 183 && Söz_SMS(at_hemişelik, "<init>") && (Söz_SMS(서술상수, "()V") || Söz_SMS(서술상수, "(I)V"))) {
                int 접속번호 = Söz_SMS(서술상수, "()V") ? 0 : 빼기(1), obýekt_Salgylanma = 빼기(2); if (!obýekt_baha(obýekt_Salgylanma, 15)) return;
                if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = ulanyjy.aç_Tor(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[obýekt_Salgylanma + 2] = 열린파일번호; return;
            }
            if (명령코드 == 182 && Söz_SMS(at_hemişelik, "setSoTimeout") && Söz_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), obýekt_Salgylanma = 빼기(2); if (!obýekt_baha(obýekt_Salgylanma, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[obýekt_Salgylanma + 3] = 밀리초값; return;
            }
            if (명령코드 == 182 && Söz_SMS(at_hemişelik, "getLocalPort") && Söz_SMS(서술상수, "()I")) { int obýekt_Salgylanma = 빼기(2); if (obýekt_baha(obýekt_Salgylanma, 15)) 넣기(힙[obýekt_Salgylanma + 2] < 0 ? -1 : ulanyjy.Tor_port(힙[obýekt_Salgylanma + 2]), 1); return; }
            if (명령코드 == 182 && Söz_SMS(at_hemişelik, "isClosed") && Söz_SMS(서술상수, "()Z")) { int obýekt_Salgylanma = 빼기(2); if (obýekt_baha(obýekt_Salgylanma, 15)) 넣기(힙[obýekt_Salgylanma + 2] < 0 ? 1 : 0, 1); return; }
            if (명령코드 == 182 && Söz_SMS(at_hemişelik, "close") && Söz_SMS(서술상수, "()V")) { int obýekt_Salgylanma = 빼기(2); if (obýekt_baha(obýekt_Salgylanma, 15) && 힙[obýekt_Salgylanma + 2] >= 0) { ulanyjy.파일서술자닫기(힙[obýekt_Salgylanma + 2]); 힙[obýekt_Salgylanma + 2] = -1; } return; }
            if (명령코드 == 182 && (Söz_SMS(at_hemişelik, "send") || Söz_SMS(at_hemişelik, "receive")) && Söz_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int 전문참조 = 빼기(2), obýekt_Salgylanma = 빼기(2); if (!obýekt_baha(전문참조, 16) || !obýekt_baha(obýekt_Salgylanma, 15)) return;
                int maglumat_ARRAY = 힙[전문참조 + 2], 유효길이 = 힙[전문참조 + 3], 열린파일번호 = 힙[obýekt_Salgylanma + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Söz_SMS(at_hemişelik, "send")) {
                    if (!obýekt_baha(힙[전문참조 + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int sikl_indeks = 0; sikl_indeks < 유효길이; sikl_indeks++) 통신임시[sikl_indeks] = 힙[maglumat_ARRAY + 2 + sikl_indeks];
                    if (ulanyjy.iber_Tor(열린파일번호, 힙[힙[전문참조 + 4] + 2], 힙[전문참조 + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int 항목수 = ulanyjy.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (항목수 == -11) {
                        int 현재시각 = ulanyjy.밀리초();
                        if (힙[obýekt_Salgylanma + 4] == 0) 힙[obýekt_Salgylanma + 4] = 현재시각 + 1;
                        if (힙[obýekt_Salgylanma + 3] > 0 && 현재시각 - (힙[obýekt_Salgylanma + 4] - 1) >= 힙[obýekt_Salgylanma + 3]) { 힙[obýekt_Salgylanma + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(obýekt_Salgylanma, 2); 넣기(전문참조, 2); 틀위치[kadr_indeks] = kadr_instruksiýa[kadr_indeks]; 바꿈요청 = true; return;
                    }
                    힙[obýekt_Salgylanma + 4] = 0;
                    if (항목수 < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int sikl_indeks = 0; sikl_indeks < 항목수; sikl_indeks++) 힙[maglumat_ARRAY + 2 + sikl_indeks] = (byte)통신임시[sikl_indeks];
                    힙[전문참조 + 3] = 항목수; 힙[전문참조 + 4] = salgy_obýekt(통신임시[513]); 힙참조[전문참조 + 4] = 1; 힙[전문참조 + 5] = 통신임시[512];
                }
                return;
            }
        }
        näsazlyk_baha("unsupported java.net method");
    }
    static boolean 흐름대기(int obýekt_Salgylanma) {
        int 현재시각 = ulanyjy.밀리초();
        if (힙[obýekt_Salgylanma + 5] == 0) 힙[obýekt_Salgylanma + 5] = 현재시각 + 1;
        if (힙[obýekt_Salgylanma + 3] > 0 && 현재시각 - (힙[obýekt_Salgylanma + 5] - 1) >= 힙[obýekt_Salgylanma + 3]) { 힙[obýekt_Salgylanma + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        틀위치[kadr_indeks] = kadr_instruksiýa[kadr_indeks]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int eýe, int at_hemişelik, int 서술상수, int 명령코드) {
        boolean 수신쪽 = Söz_SMS(eýe, "java/net/ServerSocket"), Stream = Söz_SMS(eýe, "java/io/InputStream") || Söz_SMS(eýe, "java/io/OutputStream");
        if (!Stream && 명령코드 == 183 && Söz_SMS(at_hemişelik, "<init>")) {
            boolean 빈여부 = Söz_SMS(서술상수, "()V"), 이름지정여부 = Söz_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Söz_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && Söz_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { näsazlyk_baha("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), salgy_Salgylanma = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, obýekt_Salgylanma = 빼기(2);
            if (!obýekt_baha(obýekt_Salgylanma, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !obýekt_baha(salgy_Salgylanma, 14)) return;
            int Tor_salgy = 이름지정여부 ? 주소해독(salgy_Salgylanma) : 주소지정여부 ? 힙[salgy_Salgylanma + 2] : 0x7f000001;
            if (Hata || 던진객체 != 0) return;
            int 열린파일번호 = ulanyjy.Stream_dolandyryş(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? ulanyjy.Stream_dolandyryş(1, 열린파일번호, 접속번호) : ulanyjy.Birikme_Stream(열린파일번호, Tor_salgy, 접속번호);
            if (처리값 < 0) { ulanyjy.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[obýekt_Salgylanma + 2] = 열린파일번호; 힙[obýekt_Salgylanma + 4] = 접속번호; 힙[obýekt_Salgylanma + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!Stream && Söz_SMS(at_hemişelik, "setSoTimeout") && Söz_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), obýekt_Salgylanma = 빼기(2); if (!obýekt_baha(obýekt_Salgylanma, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[obýekt_Salgylanma + 3] = 밀리초값; return; }
        if (!Stream && Söz_SMS(at_hemişelik, "close") && Söz_SMS(서술상수, "()V")) { int obýekt_Salgylanma = 빼기(2); if (obýekt_baha(obýekt_Salgylanma, 수신쪽 ? 18 : 17) && 힙[obýekt_Salgylanma + 2] >= 0) { ulanyjy.파일서술자닫기(힙[obýekt_Salgylanma + 2]); 힙[obýekt_Salgylanma + 2] = -1; } return; }
        if (!Stream && (Söz_SMS(at_hemişelik, "getLocalPort") || Söz_SMS(at_hemişelik, "getPort") || Söz_SMS(at_hemişelik, "isClosed") || Söz_SMS(at_hemişelik, "isConnected"))) {
            int obýekt_Salgylanma = 빼기(2); if (!obýekt_baha(obýekt_Salgylanma, 수신쪽 ? 18 : 17)) return;
            넣기(Söz_SMS(at_hemişelik, "isClosed") ? 힙[obýekt_Salgylanma + 2] < 0 ? 1 : 0 : Söz_SMS(at_hemişelik, "isConnected") ? 힙[obýekt_Salgylanma + 6] : Söz_SMS(at_hemişelik, "getPort") ? 힙[obýekt_Salgylanma + 4] : 힙[obýekt_Salgylanma + 2] < 0 ? -1 : ulanyjy.Stream_dolandyryş(4, 힙[obýekt_Salgylanma + 2], 0), 1); return;
        }
        if (수신쪽 && Söz_SMS(at_hemişelik, "accept") && Söz_SMS(서술상수, "()Ljava/net/Socket;")) {
            int obýekt_Salgylanma = 빼기(2); if (!obýekt_baha(obýekt_Salgylanma, 18)) return; int 열린파일번호 = ulanyjy.Stream_dolandyryş(3, 힙[obýekt_Salgylanma + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(obýekt_Salgylanma)) 넣기(obýekt_Salgylanma, 2); return; }
            힙[obýekt_Salgylanma + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = bölüp_aýyr_Ammar(17, 5); if (Hata) { ulanyjy.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = ulanyjy.Stream_dolandyryş(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !Stream && ((Söz_SMS(at_hemişelik, "getInputStream") && Söz_SMS(서술상수, "()Ljava/io/InputStream;")) || (Söz_SMS(at_hemişelik, "getOutputStream") && Söz_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int obýekt_Salgylanma = 빼기(2); if (!obýekt_baha(obýekt_Salgylanma, 17)) return; if (힙[obýekt_Salgylanma + 2] < 0 || 힙[obýekt_Salgylanma + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = bölüp_aýyr_Ammar(19, 4); if (Hata) return; 힙[반환값 + 2] = obýekt_Salgylanma; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Söz_SMS(at_hemişelik, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Söz_SMS(at_hemişelik, "read"), 쓰기여부 = Söz_SMS(at_hemişelik, "write"), bökde = Söz_SMS(서술상수, "([B)I") || Söz_SMS(서술상수, "([B)V"), 부분배열여부 = Söz_SMS(서술상수, "([BII)I") || Söz_SMS(서술상수, "([BII)V");
            int 항목수 = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, maglumat_ARRAY = bökde || 부분배열여부 ? 빼기(2) : 0;
            int maglumat_baha = 쓰기여부 && Söz_SMS(서술상수, "(I)V") ? 빼기(1) : 0, obýekt_Salgylanma = 빼기(2);
            if (!obýekt_baha(obýekt_Salgylanma, 19)) return; int 부모참조 = 힙[obýekt_Salgylanma + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Söz_SMS(at_hemişelik, "close") && Söz_SMS(서술상수, "()V")) { ulanyjy.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Söz_SMS(at_hemişelik, "flush") && Söz_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[obýekt_Salgylanma + 3] == 0)) { näsazlyk_baha("unsupported stream operation"); return; }
            if (bökde || 부분배열여부) { if (!obýekt_baha(maglumat_ARRAY, 20)) return; if (bökde) 항목수 = 힙[maglumat_ARRAY + 1]; if (시작변위 < 0 || 항목수 < 0 || 시작변위 > 힙[maglumat_ARRAY + 1] - 항목수) { 예외던짐(6, "stream array bounds"); return; } }
            else 항목수 = 1;
            if (항목수 == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[obýekt_Salgylanma + 4] : 0, 처리값 = 0;
            while (완료수 < 항목수) {
                처리값 = 읽기여부 ? ulanyjy.파일한바이트읽기(열린파일번호) : ulanyjy.파일한바이트쓰기(열린파일번호, bökde || 부분배열여부 ? 힙[maglumat_ARRAY + 2 + 시작변위 + 완료수] : maglumat_baha);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (bökde || 부분배열여부)) 힙[maglumat_ARRAY + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(bökde || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[obýekt_Salgylanma + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(obýekt_Salgylanma, 2); if (bökde || 부분배열여부) 넣기(maglumat_ARRAY, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(항목수, 1); } if (쓰기여부 && !(bökde || 부분배열여부)) 넣기(maglumat_baha, 1); } return;
            }
            힙[obýekt_Salgylanma + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : bökde || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        näsazlyk_baha("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int at_hemişelik) {
        if (Söz_SMS(at_hemişelik, "한국어/자체/penjire")) return 24;
        if (Söz_SMS(at_hemişelik, "한국어/자체/belgi")) return 26;
        if (Söz_SMS(at_hemişelik, "한국어/자체/düwme")) return 27;
        if (Söz_SMS(at_hemişelik, "한국어/자체/tekst_meýdançasy")) return 28;
        if (Söz_SMS(at_hemişelik, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int at_hemişelik) {
        return 한국어화면종(at_hemişelik) != 0 || Söz_SMS(at_hemişelik, "한국어/자체/화면구성요소") || Söz_SMS(at_hemişelik, "한국어/자체/waka_nobat");
    }
    static int 화면종(int at_hemişelik) {
        int 한국어종 = 한국어화면종(at_hemişelik); if (한국어종 != 0) return 한국어종;
        if (Söz_SMS(at_hemişelik, "javax/swing/JFrame")) return 24;
        if (Söz_SMS(at_hemişelik, "javax/swing/JPanel")) return 25;
        if (Söz_SMS(at_hemişelik, "javax/swing/JLabel")) return 26;
        if (Söz_SMS(at_hemişelik, "javax/swing/JButton")) return 27;
        if (Söz_SMS(at_hemişelik, "javax/swing/JTextField")) return 28;
        if (Söz_SMS(at_hemişelik, "java/awt/event/ActionEvent")) return 29;
        if (Söz_SMS(at_hemişelik, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int at_hemişelik) {
        return 화면종(at_hemişelik) != 0 || Söz_SMS(at_hemişelik, "java/awt/Component") || Söz_SMS(at_hemişelik, "java/awt/Container") || Söz_SMS(at_hemişelik, "javax/swing/JComponent") || Söz_SMS(at_hemişelik, "javax/swing/AbstractButton") || Söz_SMS(at_hemişelik, "javax/swing/text/JTextComponent") || Söz_SMS(at_hemişelik, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int obýekt_Salgylanma) { if (!객체유효(obýekt_Salgylanma)) return false; if (힙[obýekt_Salgylanma] < 24 || 힙[obýekt_Salgylanma] > 28) { näsazlyk_baha("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int obýekt_Salgylanma, int SMS_Salgylanma) {
        if (SMS_Salgylanma != 0 && !obýekt_baha(SMS_Salgylanma, 1)) return;
        int 항목수 = SMS_Salgylanma == 0 ? 0 : 힙[SMS_Salgylanma + 1]; if (항목수 > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int sikl_indeks = 0; sikl_indeks < 항목수; sikl_indeks++) 화면글임시[sikl_indeks] = 힙[SMS_Salgylanma + 2 + sikl_indeks];
        if (ulanyjy.화면글(힙[obýekt_Salgylanma + 2], 화면글임시, 항목수) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[obýekt_Salgylanma + 3] = SMS_Salgylanma; 힙참조[obýekt_Salgylanma + 3] = 1;
    }
    static int 화면문자읽기(int obýekt_Salgylanma) {
        int hasap_baha = 힙[obýekt_Salgylanma + 2], 항목수 = ulanyjy.화면연결(8, hasap_baha, 0, 0, 0, 0), 사용수 = 0;
        if (항목수 < 0) { näsazlyk_baha("GUI text read failed"); return 0; }
        for (int sikl_indeks = 0; sikl_indeks < 항목수; sikl_indeks++) { int 부호값 = ulanyjy.화면연결(9, hasap_baha, sikl_indeks, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = bölüp_aýyr_Ammar(1, 사용수); if (!Hata) for (int sikl_indeks = 0; sikl_indeks < 사용수; sikl_indeks++) 힙[반환값 + 2 + sikl_indeks] = 화면글임시[sikl_indeks]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 ýadro_baha 화면 기능에 연결한다. Swing obýekt_baha/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int eýe, int at_hemişelik, int 서술상수, int 명령코드) {
        if (Söz_SMS(eýe, "한국어/자체/waka_nobat")) {
            if (명령코드 == 184 && Söz_SMS(at_hemişelik, "나중에실행") && Söz_SMS(서술상수, "(L한국어/자체/실행할일;)V")) {
                int tabşyryk_iş = 빼기(2); if (!객체유효(tabşyryk_iş)) return;
                if (나중수 == 8) { näsazlyk_baha("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = tabşyryk_iş; return;
            }
            if (명령코드 == 184 && Söz_SMS(at_hemişelik, "사건처리중인가") && Söz_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            näsazlyk_baha("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (Söz_SMS(eýe, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!obýekt_baha(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Söz_SMS(at_hemişelik, "waka_gor") && Söz_SMS(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Söz_SMS(at_hemişelik, "buýruk_SMS") && Söz_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Söz_SMS(at_hemişelik, "indeks") && Söz_SMS(서술상수, "()I")) 넣기(1001, 1);
            else näsazlyk_baha("지원하지 않는 한국어 iş 알림 호출"); return;
        }
        if (명령코드 == 183 && Söz_SMS(at_hemişelik, "<init>")) {
            int 종류 = 한국어화면종(eýe), 받이 = 0, 가로 = 0, 세로 = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Söz_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (ulanyjy.화면너비() - 폭) / 2; 세로 = (ulanyjy.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Söz_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Söz_SMS(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); 세로 = 빼기(1); 가로 = 빼기(1);
            } else { näsazlyk_baha("지원하지 않는 한국어 화면 생성자"); return; }
            int Metin = 빼기(2), element_baha = 빼기(2); if (!화면객체(element_baha)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || 세로 < 0 || 폭 > ulanyjy.화면너비() - 가로 || 높이 > ulanyjy.화면높이() - 세로) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int indeks = ulanyjy.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (indeks < 1 || indeks > 32) { näsazlyk_baha("화면 element_baha 자리가 가득 찼습니다"); return; }
            힙[element_baha + 2] = indeks; 화면참조[indeks - 1] = element_baha;
            힙[element_baha + 5] = 가로; 힙[element_baha + 6] = 세로; 힙[element_baha + 7] = 폭; 힙[element_baha + 8] = 높이; 힙[element_baha + 10] = 2;
            힙[element_baha + 4] = 받이; 힙참조[element_baha + 4] = 1; 힙[element_baha + 12] = 1;
            ulanyjy.화면연결(1, indeks, 가로, 세로, 폭, 높이);
            if (종류 == 24) ulanyjy.화면연결(7, indeks, 2, 0, 0, 0);
            화면문자설정(element_baha, Metin); return;
        }
        if (명령코드 != 182) { näsazlyk_baha("잘못된 한국어 화면 호출 buýruk"); return; }
        if (Söz_SMS(at_hemişelik, "ýaz_SMS") && Söz_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Metin = 빼기(2), element_baha = 빼기(2); if (화면객체(element_baha)) 화면문자설정(element_baha, Metin); return;
        }
        if (Söz_SMS(at_hemişelik, "글읽기") && Söz_SMS(서술상수, "()Ljava/lang/String;")) {
            int element_baha = 빼기(2); if (화면객체(element_baha)) 넣기(화면문자읽기(element_baha), 2); return;
        }
        if (Söz_SMS(at_hemişelik, "동작맡기기") && Söz_SMS(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), element_baha = 빼기(2);
            if (화면객체(element_baha)) { 힙[element_baha + 4] = 받이; 힙참조[element_baha + 4] = 1; 힙[element_baha + 12] = 1; } return;
        }
        if (Söz_SMS(at_hemişelik, "goş_element") && Söz_SMS(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int çaga_baha = 빼기(2), 부모 = 빼기(2); if (!화면객체(çaga_baha) || !화면객체(부모)) return;
            if (ulanyjy.화면연결(2, 힙[부모 + 2], 힙[çaga_baha + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[çaga_baha + 11] = 부모; 힙참조[çaga_baha + 11] = 1; return;
        }
        if (Söz_SMS(at_hemişelik, "자리정하기") && Söz_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), 세로 = 빼기(1), 가로 = 빼기(1), element_baha = 빼기(2); if (!화면객체(element_baha)) return;
            if (ulanyjy.화면연결(1, 힙[element_baha + 2], 가로, 세로, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[element_baha + 5] = 가로; 힙[element_baha + 6] = 세로; 힙[element_baha + 7] = 폭; 힙[element_baha + 8] = 높이; return;
        }
        if ((Söz_SMS(at_hemişelik, "görkez_penjire") || Söz_SMS(at_hemişelik, "Ýap")) && Söz_SMS(서술상수, "()V")) {
            boolean görünijilik_baha = Söz_SMS(at_hemişelik, "görkez_penjire"); int element_baha = 빼기(2); if (!화면객체(element_baha)) return;
            if (ulanyjy.화면연결(görünijilik_baha ? 3 : 4, 힙[element_baha + 2], görünijilik_baha ? 1 : 0, 0, 0, 0) < 0) { näsazlyk_baha("화면은 interaktiw 명령에서 실행해야 합니다"); return; }
            힙[element_baha + 9] = görünijilik_baha ? 1 : 0; return;
        }
        if (Söz_SMS(at_hemişelik, "보이는가") && Söz_SMS(서술상수, "()Z")) { int element_baha = 빼기(2); if (화면객체(element_baha)) 넣기(힙[element_baha + 9], 1); return; }
        näsazlyk_baha("지원하지 않는 한국어 화면 usul_baha");
    }
    static void 화면호출(int eýe, int at_hemişelik, int 서술상수, int 명령코드) {
        if (Söz_SMS(eýe, "javax/swing/SwingUtilities")) {
            if (명령코드 == 184 && Söz_SMS(at_hemişelik, "invokeLater") && Söz_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int obýekt_Salgylanma = 빼기(2); if (!객체유효(obýekt_Salgylanma)) return; if (나중수 == 8) { näsazlyk_baha("invokeLater queue full"); return; } 나중실행[나중수++] = obýekt_Salgylanma; return; }
            if (명령코드 == 184 && Söz_SMS(at_hemişelik, "isEventDispatchThread") && Söz_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            näsazlyk_baha("unsupported SwingUtilities method"); return;
        }
        if (Söz_SMS(eýe, "java/awt/event/ActionEvent")) {
            int obýekt_Salgylanma = 빼기(2); if (!obýekt_baha(obýekt_Salgylanma, 29)) return;
            if (Söz_SMS(at_hemişelik, "getSource") && Söz_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[obýekt_Salgylanma + 2], 2);
            else if (Söz_SMS(at_hemişelik, "getActionCommand") && Söz_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[obýekt_Salgylanma + 2]), 2);
            else if (Söz_SMS(at_hemişelik, "getID") && Söz_SMS(서술상수, "()I")) 넣기(1001, 1);
            else näsazlyk_baha("unsupported ActionEvent method"); return;
        }
        if (명령코드 == 183 && Söz_SMS(at_hemişelik, "<init>")) {
            int 열수 = 0, SMS_Salgylanma = 0;
            if (Söz_SMS(서술상수, "(I)V")) 열수 = 빼기(1);
            else if (Söz_SMS(서술상수, "(Ljava/lang/String;I)V")) { 열수 = 빼기(1); SMS_Salgylanma = 빼기(2); }
            else if (Söz_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Salgylanma = 빼기(2);
            else if (Söz_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Söz_SMS(서술상수, "()V")) { näsazlyk_baha("unsupported Swing constructor"); return; }
            int obýekt_Salgylanma = 빼기(2); if (!객체유효(obýekt_Salgylanma)) return;
            if (힙[obýekt_Salgylanma] == 30) { näsazlyk_baha("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(obýekt_Salgylanma) || 열수 < 0) return;
            int hasap_baha = ulanyjy.화면연결(0, 힙[obýekt_Salgylanma] - 23, 0, 0, 0, 0);
            if (hasap_baha < 1 || hasap_baha > 32) { näsazlyk_baha("GUI widget slots exhausted"); return; }
            힙[obýekt_Salgylanma + 2] = hasap_baha; 화면참조[hasap_baha - 1] = obýekt_Salgylanma; 힙[obýekt_Salgylanma + 5] = 힙[obýekt_Salgylanma] == 24 ? 130 : 16; 힙[obýekt_Salgylanma + 6] = 힙[obýekt_Salgylanma] == 24 ? 110 : 16;
            힙[obýekt_Salgylanma + 7] = 힙[obýekt_Salgylanma] == 24 ? 380 : 220; 힙[obýekt_Salgylanma + 8] = 힙[obýekt_Salgylanma] == 24 ? 240 : 28; 힙[obýekt_Salgylanma + 10] = 1;
            화면문자설정(obýekt_Salgylanma, SMS_Salgylanma); return;
        }
        if (Söz_SMS(at_hemişelik, "setText") || Söz_SMS(at_hemişelik, "setTitle")) { int SMS_Salgylanma = 빼기(2), obýekt_Salgylanma = 빼기(2); if (화면객체(obýekt_Salgylanma) && Söz_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(obýekt_Salgylanma, SMS_Salgylanma); return; }
        if (Söz_SMS(at_hemişelik, "getText") || Söz_SMS(at_hemişelik, "getTitle")) { int obýekt_Salgylanma = 빼기(2); if (화면객체(obýekt_Salgylanma) && Söz_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(obýekt_Salgylanma), 2); return; }
        if (Söz_SMS(at_hemişelik, "addActionListener") && Söz_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), obýekt_Salgylanma = 빼기(2); if (화면객체(obýekt_Salgylanma)) { 힙[obýekt_Salgylanma + 4] = 수신참조; 힙참조[obýekt_Salgylanma + 4] = 1; } return; }
        if (Söz_SMS(at_hemişelik, "getContentPane") && Söz_SMS(서술상수, "()Ljava/awt/Container;")) { int obýekt_Salgylanma = 빼기(2); if (화면객체(obýekt_Salgylanma)) 넣기(obýekt_Salgylanma, 2); return; }
        if (Söz_SMS(at_hemişelik, "setLayout") && Söz_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Ýerleşiş_Salgylanma = 빼기(2), obýekt_Salgylanma = 빼기(2); if (화면객체(obýekt_Salgylanma) && Ýerleşiş_Salgylanma != 0) näsazlyk_baha("only absolute layout (null) is supported"); return; }
        if (Söz_SMS(at_hemişelik, "add") && (Söz_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Söz_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Ýerleşiş_şert = Söz_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Ýerleşiş_şert) 빼기(2);
            int çaga_Salgylanma = 빼기(2), obýekt_Salgylanma = 빼기(2); if (!화면객체(çaga_Salgylanma) || !화면객체(obýekt_Salgylanma)) return;
            if (ulanyjy.화면연결(2, 힙[obýekt_Salgylanma + 2], 힙[çaga_Salgylanma + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[çaga_Salgylanma + 11] = obýekt_Salgylanma; 힙참조[çaga_Salgylanma + 11] = 1; if (!Ýerleşiş_şert) 넣기(çaga_Salgylanma, 2); return;
        }
        if (Söz_SMS(at_hemişelik, "setBounds") && Söz_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), x_koordinatasy = 빼기(1), obýekt_Salgylanma = 빼기(2); if (!화면객체(obýekt_Salgylanma)) return;
            if (ulanyjy.화면연결(1, 힙[obýekt_Salgylanma + 2], x_koordinatasy, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[obýekt_Salgylanma + 5] = x_koordinatasy; 힙[obýekt_Salgylanma + 6] = 세로좌표; 힙[obýekt_Salgylanma + 7] = 너비; 힙[obýekt_Salgylanma + 8] = 높이; return;
        }
        if (Söz_SMS(at_hemişelik, "setSize") && Söz_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), obýekt_Salgylanma = 빼기(2); if (!화면객체(obýekt_Salgylanma)) return;
            if (ulanyjy.화면연결(1, 힙[obýekt_Salgylanma + 2], 힙[obýekt_Salgylanma + 5], 힙[obýekt_Salgylanma + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[obýekt_Salgylanma + 7] = 너비; 힙[obýekt_Salgylanma + 8] = 높이; } return;
        }
        if (Söz_SMS(at_hemişelik, "setLocationRelativeTo") && Söz_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), obýekt_Salgylanma = 빼기(2); if (!화면객체(obýekt_Salgylanma)) return; if (상대배치 != 0) { näsazlyk_baha("only screen centering supported"); return; } 힙[obýekt_Salgylanma + 5] = (ulanyjy.화면너비() - 힙[obýekt_Salgylanma + 7]) / 2; 힙[obýekt_Salgylanma + 6] = (ulanyjy.화면높이() - 힙[obýekt_Salgylanma + 8]) / 2; ulanyjy.화면연결(1, 힙[obýekt_Salgylanma + 2], 힙[obýekt_Salgylanma + 5], 힙[obýekt_Salgylanma + 6], 힙[obýekt_Salgylanma + 7], 힙[obýekt_Salgylanma + 8]); return; }
        if (Söz_SMS(at_hemişelik, "setDefaultCloseOperation") && Söz_SMS(서술상수, "(I)V")) { int syýasat = 빼기(1), obýekt_Salgylanma = 빼기(2); if (화면객체(obýekt_Salgylanma)) { if (syýasat < 0 || syýasat > 3) 예외던짐(9, "close policy"); else { 힙[obýekt_Salgylanma + 10] = syýasat; ulanyjy.화면연결(7, 힙[obýekt_Salgylanma + 2], syýasat, 0, 0, 0); } } return; }
        if (Söz_SMS(at_hemişelik, "setVisible") && Söz_SMS(서술상수, "(Z)V")) { int maglumat_baha = 빼기(1), obýekt_Salgylanma = 빼기(2); if (화면객체(obýekt_Salgylanma)) { int 처리값 = ulanyjy.화면연결(3, 힙[obýekt_Salgylanma + 2], maglumat_baha, 0, 0, 0); if (처리값 < 0) näsazlyk_baha("Swing requires a standalone interactive command"); else 힙[obýekt_Salgylanma + 9] = maglumat_baha; } return; }
        if (Söz_SMS(at_hemişelik, "dispose") && Söz_SMS(서술상수, "()V")) { int obýekt_Salgylanma = 빼기(2); if (화면객체(obýekt_Salgylanma)) { ulanyjy.화면연결(4, 힙[obýekt_Salgylanma + 2], 0, 0, 0, 0); 힙[obýekt_Salgylanma + 9] = 0; } return; }
        if (Söz_SMS(at_hemişelik, "repaint") || Söz_SMS(at_hemişelik, "validate")) { int obýekt_Salgylanma = 빼기(2); if (!화면객체(obýekt_Salgylanma) || !Söz_SMS(서술상수, "()V")) return; ulanyjy.화면연결(1, 힙[obýekt_Salgylanma + 2], 힙[obýekt_Salgylanma + 5], 힙[obýekt_Salgylanma + 6], 힙[obýekt_Salgylanma + 7], 힙[obýekt_Salgylanma + 8]); return; }
        if (Söz_SMS(at_hemişelik, "isVisible") && Söz_SMS(서술상수, "()Z")) { int obýekt_Salgylanma = 빼기(2); if (화면객체(obýekt_Salgylanma)) 넣기(힙[obýekt_Salgylanma + 9], 1); return; }
        näsazlyk_baha("unsupported Swing method (native subset)");
    }
    static void 사건실행(int niýet_salgy, int 사건번호, boolean 한국어) {
        if (niýet_salgy < 1 || 힙[niýet_salgy] < 32) { näsazlyk_baha("Java event listener required"); return; }
        int faýl_indeks = at_usul(힙[niýet_salgy] - 32, 사건번호 == 0 ? (한국어 ? "ýerine_ýetir_tabşyryk" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (faýl_indeks < 0) { näsazlyk_baha("event callback missing"); return; }
        현재가닥 = 0; 가닥수 = 1; kadr_indeks = 0; akym_ýagdaý[0] = 1; kadr_Desse[0] = 0; 틀잠금[0] = ulanyşa_taýýarla_kadr[0] = 0; 바꿈요청 = false;
        for (int sikl_indeks = 0; sikl_indeks < 128; sikl_indeks++) { ýerli_baha[sikl_indeks] = ýerli_ýaz[sikl_indeks] = 0; }
        kadr_usul[0] = faýl_indeks; 틀위치[0] = usul_başlat[faýl_indeks]; ýerli_baha[0] = niýet_salgy; ýerli_ýaz[0] = 2;
        if (사건번호 != 0) { ýerli_baha[1] = 사건번호; ýerli_ýaz[1] = 2; }
        사건중 = true; ýerine_ýetir_buýruk(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!Hata) {
            if (나중수 > 0) { int niýet_salgy = 나중실행[0], 한국어 = 나중한국어[0]; for (int sikl_indeks = 1; sikl_indeks < 나중수; sikl_indeks++) { 나중실행[sikl_indeks - 1] = 나중실행[sikl_indeks]; 나중한국어[sikl_indeks - 1] = 나중한국어[sikl_indeks]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(niýet_salgy, 0, 한국어 != 0); continue; }
            if (ulanyjy.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = ulanyjy.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { näsazlyk_baha("GUI event I/O failed"); return; }
            int hasap_baha = 사건번호 & 65535; if (hasap_baha < 1 || hasap_baha > 32) continue; int obýekt_Salgylanma = 화면참조[hasap_baha - 1]; if (obýekt_Salgylanma == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[obýekt_Salgylanma + 10] != 0) 힙[obýekt_Salgylanma + 9] = 0;
                if (힙[obýekt_Salgylanma + 10] == 3) for (int sikl_indeks = 0; sikl_indeks < 32; sikl_indeks++) if (화면참조[sikl_indeks] != 0 && 힙[화면참조[sikl_indeks]] == 24) ulanyjy.화면연결(4, sikl_indeks + 1, 0, 0, 0, 0);
            } else if (힙[obýekt_Salgylanma + 4] != 0) {
                int README_Salgylanma = bölüp_aýyr_Ammar(29, 2); if (Hata) return; 힙[README_Salgylanma + 2] = obýekt_Salgylanma; 힙[README_Salgylanma + 3] = 힙[obýekt_Salgylanma + 12]; 힙참조[README_Salgylanma + 2] = 1; 사건실행(힙[obýekt_Salgylanma + 4], README_Salgylanma, 힙[obýekt_Salgylanma + 12] != 0);
            }
        }
    }
    public static int Bitir() {
        if (ulanyjy.인수개수() == 1 && 자바도구.같음(ulanyjy.인수(0), "-version")) {
            ulanyjy.Ýaz("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (ulanyjy.인수개수() < 1) { ulanyjy.Ýaz("Usage: java CLASS [ARGS]\n"); return 2; }
        girizmeklik_klas_Kesgitleme = ýük_klas_Kesgitleme(esasy_nyşan(ulanyjy.인수(0))); if (Hata || girizmeklik_klas_Kesgitleme < 0) return 1;
        int girizmeklik_utuk_baha = at_usul(girizmeklik_klas_Kesgitleme, "Bitir", "()V");
        boolean 한국어진입 = girizmeklik_utuk_baha >= 0 && (usul_ygtyýarlylyk[girizmeklik_utuk_baha] & 9) == 9;
        if (!한국어진입) girizmeklik_utuk_baha = at_usul(girizmeklik_klas_Kesgitleme, "main", "([Ljava/lang/String;)V");
        if (girizmeklik_utuk_baha < 0 || (usul_ygtyýarlylyk[girizmeklik_utuk_baha] & 9) != 9) näsazlyk_baha("public static void Bitir() or main(String[] args) required");
        if (Hata) return 1;
        int 인수 = bölüp_aýyr_Ammar(3, ulanyjy.인수개수() - 1); ARRAY_element[인수] = -1;
        for (int 수 = 1; 수 < ulanyjy.인수개수() && !Hata; 수++) 힙[인수 + 1 + 수] = esasy_nyşan(ulanyjy.인수(수));
        kadr_indeks = 0; kadr_usul[0] = girizmeklik_utuk_baha; 틀위치[0] = usul_başlat[girizmeklik_utuk_baha]; ýerli_baha[0] = 한국어진입 ? 0 : 인수; ýerli_ýaz[0] = 한국어진입 ? 0 : 2;
        akym_ýagdaý[0] = 1; akym_obýekt[0] = bölüp_aýyr_Ammar(13, 2);
        ýerine_ýetir_buýruk(); if (!Hata) 화면사건들(); return Hata ? 1 : 0;
    }
}
