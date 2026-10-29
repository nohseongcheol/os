// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Faýl/스택/Salgylanma/şahalanma 경계를 ýerine_ýetir_buýruk 중 검사한다. */
public final class 자바가상기계 {
    static int[] Faýl = new int[16384], faýl_at_SMS = new int[64];
    static int[] hemişelik_bellik = new int[512], 상가 = new int[512], 상나 = new int[512], setir_Salgylanma = new int[512];
    static int[] usul_at_SMS = new int[32], usul_ýaz = new int[32], usul_ygtyýarlylyk = new int[32];
    static int[] usul_başlat = new int[32], usul_tamamla = new int[32], usul_Desse = new int[32], 함수지역 = new int[32];
    static int[] 함수인수수 = new int[32], usul_argument_ýaz = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] ýerli_baha = new int[4096], ýerli_ýaz = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] kadr_usul = new int[32], 틀위치 = new int[32], kadr_Desse = new int[32];
    static int[] 힙 = new int[8192];
    static int Ululyk, 읽기위치, 상수수, 함수수, klas_at, kadr_indeks = -1, 힙끝 = 1, 반환형;
    static boolean Hata;

    static void näsazlyk_baha(String Söz_SMS) {
        if (!Hata) { ulanyjy.Ýaz("JVM error: "); ulanyjy.Ýaz(Söz_SMS); ulanyjy.ýaz_nyşan_baha(10); }
        Hata = true;
    }
    static boolean klip(int Bitir, int dowamlylyk_baha) { return Bitir >= 0 && dowamlylyk_baha >= 0 && Bitir <= Ululyk - dowamlylyk_baha; }
    static int baýt_baha() {
        if (!klip(읽기위치, 1)) { näsazlyk_baha("truncated class file"); return 0; }
        return Faýl[읽기위치++];
    }
    static int 짧은수() { return baýt_baha() << 8 | baýt_baha(); }
    static int bitin() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int dowamlylyk_baha) { if (!klip(읽기위치, dowamlylyk_baha)) näsazlyk_baha("invalid attribute size"); else 읽기위치 += dowamlylyk_baha; }
    static boolean derňe_hemişelik(int 수, int 종류) {
        if (수 <= 0 || 수 >= 상수수 || hemişelik_bellik[수] != 종류) { näsazlyk_baha("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Bitir, int dowamlylyk_baha, String Söz_SMS) {
        if (!klip(Bitir, dowamlylyk_baha) || dowamlylyk_baha != Söz_SMS.length()) return false;
        for (int 수 = 0; 수 < dowamlylyk_baha; 수++) if (Faýl[Bitir + 수] != Söz_SMS.charAt(수)) return false;
        return true;
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
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !Hata; 수++) { derňe_hemişelik(짧은수(), 1); 건너(bitin()); }
    }
    static int buýruk_dowamlylyk(int baha) {
        if (baha == 16 || baha == 18 || baha == 21 || baha == 25 || baha == 54 || baha == 58 || baha == 188) return 2;
        if (baha == 17 || baha == 19 || baha == 132 || baha >= 153 && baha <= 167
            || baha >= 178 && baha <= 184 || baha == 187 || baha == 189 || baha == 192 || baha == 198 || baha == 199) return 3;
        if (baha >= 0 && baha <= 8 || baha >= 26 && baha <= 29 || baha >= 42 && baha <= 46 || baha == 50
            || baha >= 59 && baha <= 62 || baha >= 75 && baha <= 79 || baha == 83 || baha == 87 || baha == 89 || baha == 95
            || baha == 96 || baha == 100 || baha == 104 || baha == 108 || baha == 112 || baha == 116
            || baha == 120 || baha == 122 || baha == 124 || baha == 126 || baha == 128 || baha == 130
            || baha >= 145 && baha <= 147 || baha == 172 || baha == 176 || baha == 177 || baha == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (bitin() != 0xcafebabe) näsazlyk_baha("not a class file");
        int 부판 = 짧은수(), wersiýa_baha = 짧은수();
        if (wersiýa_baha < 45 || wersiýa_baha > 52 || 부판 != 0) näsazlyk_baha("supported class versions: 45..52, minor 0");
        상수수 = 짧은수();
        if (상수수 < 1 || 상수수 > 512) { näsazlyk_baha("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < 상수수 && !Hata; 수++) {
            int 종류 = baýt_baha(); hemişelik_bellik[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = bitin();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); 상나[수] = 짧은수(); }
            else näsazlyk_baha("unsupported constant type");
        }
        int rugsat_baha = 짧은수();
        if ((rugsat_baha & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) näsazlyk_baha("unsupported class flags");
        klas_at = klas_at_SMS(짧은수());
        if (!Söz_SMS(klas_at_SMS(짧은수()), "java/lang/Object")) näsazlyk_baha("inheritance unsupported");
        if (짧은수() != 0) näsazlyk_baha("interfaces unsupported");
        if (짧은수() != 0) näsazlyk_baha("fields unsupported");
        함수수 = 짧은수();
        if (함수수 < 1 || 함수수 > 32) { näsazlyk_baha("method count limit (32)"); return; }
        for (int 수 = 0; 수 < 함수수 && !Hata; 수++) {
            usul_ygtyýarlylyk[수] = 짧은수(); usul_at_SMS[수] = 짧은수(); usul_ýaz[수] = 짧은수();
            derňe_hemişelik(usul_at_SMS[수], 1); 서술읽기(수);
            if ((usul_ygtyýarlylyk[수] & (0x100 | 0x400 | 0x20)) != 0) näsazlyk_baha("native, abstract and synchronized methods unsupported");
            if ((usul_ygtyýarlylyk[수] & 8) == 0 && !Söz_SMS(usul_at_SMS[수], "<init>")) näsazlyk_baha("instance methods unsupported");
            if (Söz_SMS(usul_at_SMS[수], "<clinit>")) näsazlyk_baha("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(usul_at_SMS[앞], usul_at_SMS[수]) && 같은말(usul_ýaz[앞], usul_ýaz[수])) näsazlyk_baha("duplicate method");
            int 개수 = 짧은수();
            for (int alamat_baha = 0; alamat_baha < 개수 && !Hata; alamat_baha++) {
                int Ad = 짧은수(), dowamlylyk_baha = bitin(), Bitir = 읽기위치;
                if (!klip(Bitir, dowamlylyk_baha)) { näsazlyk_baha("truncated method attribute"); break; }
                if (Söz_SMS(Ad, "Code")) {
                    if (usul_başlat[수] != 0) näsazlyk_baha("duplicate Code attribute");
                    usul_Desse[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = bitin();
                    if (usul_Desse[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) näsazlyk_baha("method memory limits exceeded");
                    usul_başlat[수] = 읽기위치; 건너(코드길이); usul_tamamla[수] = 읽기위치;
                    if (짧은수() != 0) näsazlyk_baha("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Bitir + dowamlylyk_baha) näsazlyk_baha("Code attribute size mismatch");
                } else 건너(dowamlylyk_baha);
            }
            if (usul_başlat[수] == 0) näsazlyk_baha("missing Code attribute");
            int ýer_girizmeklik = usul_başlat[수];
            while (ýer_girizmeklik < usul_tamamla[수] && !Hata) {
                int dowamlylyk_baha = buýruk_dowamlylyk(Faýl[ýer_girizmeklik]);
                if (dowamlylyk_baha == 0 || dowamlylyk_baha > usul_tamamla[수] - ýer_girizmeklik) { näsazlyk_baha("unsupported or truncated bytecode"); break; }
                경계[ýer_girizmeklik] = 수 + 1; ýer_girizmeklik += dowamlylyk_baha;
            }
            // 실행하지 않는 경로에도 잘못된 şahalanma 목적지를 허용하지 않는다.
            ýer_girizmeklik = usul_başlat[수];
            while (ýer_girizmeklik < usul_tamamla[수] && !Hata) {
                int baha = Faýl[ýer_girizmeklik];
                if (baha >= 153 && baha <= 167 || baha == 198 || baha == 199) {
                    int barylmaly_ýer_baha = ýer_girizmeklik + (short)(Faýl[ýer_girizmeklik + 1] << 8 | Faýl[ýer_girizmeklik + 2]);
                    if (barylmaly_ýer_baha < usul_başlat[수] || barylmaly_ýer_baha >= usul_tamamla[수] || 경계[barylmaly_ýer_baha] != 수 + 1) näsazlyk_baha("invalid branch target");
                }
                ýer_girizmeklik += buýruk_dowamlylyk(baha);
            }
        }
        if (!Hata) 속성건너();
        if (읽기위치 != Ululyk) näsazlyk_baha("extra class file data");
    }
    static int bölüp_aýyr_Ammar(int 종류, int dowamlylyk_baha) {
        if (dowamlylyk_baha < 0 || dowamlylyk_baha > 힙.length - 힙끝 - 2) { näsazlyk_baha("object heap exhausted or negative array size"); return 0; }
        int Salgylanma = 힙끝; 힙끝 += dowamlylyk_baha + 2; 힙[Salgylanma] = 종류; 힙[Salgylanma + 1] = dowamlylyk_baha;
        return Salgylanma;
    }
    static boolean obýekt_baha(int Salgylanma, int 종류) {
        if (Salgylanma < 1 || Salgylanma >= 힙끝 - 1 || 힙[Salgylanma] != 종류) { näsazlyk_baha("null or invalid object reference"); return false; }
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
        if (kadr_indeks == 31) { näsazlyk_baha("call stack limit (32)"); return; }
        int 다음 = kadr_indeks + 1;
        for (int 수 = 0; 수 < 128; 수++) ýerli_ýaz[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[FUNCTION_baha] - 1; 수 >= 0; 수--) {
            ýerli_baha[다음 * 128 + 수] = 빼기(usul_argument_ýaz[FUNCTION_baha * 16 + 수]); ýerli_ýaz[다음 * 128 + 수] = usul_argument_ýaz[FUNCTION_baha * 16 + 수];
        }
        kadr_indeks = 다음; kadr_usul[kadr_indeks] = FUNCTION_baha; 틀위치[kadr_indeks] = usul_başlat[FUNCTION_baha]; kadr_Desse[kadr_indeks] = 0;
    }
    static void 반환(int ýaz_baha) {
        if (ýaz_baha != 함수반환[kadr_usul[kadr_indeks]]) { näsazlyk_baha("return type mismatch"); return; }
        int baha = ýaz_baha == 0 ? 0 : 빼기(ýaz_baha);
        kadr_indeks--; if (kadr_indeks >= 0 && ýaz_baha != 0) 넣기(baha, ýaz_baha);
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
                if (baha < 1 || baha > 127) { näsazlyk_baha("file stream paths currently require ASCII"); return; }
                Stream_faýl_at[ýer_girizmeklik] = baha;
            }
            Stream_faýl_at[dowamlylyk_baha] = 0;
            int 서술자 = ulanyjy.파일서술자열기(Stream_faýl_at, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { näsazlyk_baha("FileNotFoundException: file open failed"); return; }
            힙[Stream_baha + 2] = 서술자; 힙[Stream_baha + 3] = 1;
            return;
        }
        if (buýruk != 182) { näsazlyk_baha("invalid file stream invocation"); return; }
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
            if (결과 < -1) näsazlyk_baha("IOException: read failed"); else 넣기(결과, 1);
        } else if (ulanyjy.파일한바이트쓰기(서술자, baha) != 1) näsazlyk_baha("IOException: write failed");
    }
    static void Jaň_usul(int indeks, int buýruk) {
        if (!derňe_hemişelik(indeks, 10)) return;
        int eýe_baha = klas_at_SMS(상가[indeks]), Ad = Salgylanma_at(상나[indeks]), format_baha = Salgylanma_ýaz(상나[indeks]);
        if (Hata) return;
        if (같은말(eýe_baha, klas_at)) {
            if (buýruk != 184) { näsazlyk_baha("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < 함수수; 수++) if (같은말(Ad, usul_at_SMS[수]) && 같은말(format_baha, usul_ýaz[수])) {
                if ((usul_ygtyýarlylyk[수] & 8) == 0) näsazlyk_baha("method is not static"); else 호출(수);
                return;
            }
            näsazlyk_baha("NoSuchMethodError"); return;
        }
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
        näsazlyk_baha("unsupported library method");
    }
    static int ARRAY_ýer(int Salgylanma, int aşaky_indeks_baha, int ýaz_baha) {
        if (!obýekt_baha(Salgylanma, ýaz_baha)) return 0;
        if (aşaky_indeks_baha < 0 || aşaky_indeks_baha >= 힙[Salgylanma + 1]) { näsazlyk_baha("ArrayIndexOutOfBoundsException"); return 0; }
        return Salgylanma + 2 + aşaky_indeks_baha;
    }
    static void ýerine_ýetir_buýruk() {
        int 남음 = 500000;
        while (kadr_indeks >= 0 && !Hata) {
            if (--남음 == 0) { näsazlyk_baha("instruction limit (500000)"); break; }
            int Bitir = 틀위치[kadr_indeks], baha = 명바();
            if (Hata) break;
            if (baha == 0) continue;
            if (baha == 1) { 넣기(0, 2); continue; }
            if (baha >= 2 && baha <= 8) { 넣기(baha - 3, 1); continue; }
            if (baha == 16) { 넣기((byte)명바(), 1); continue; }
            if (baha == 17) { 넣기((short)명짧(), 1); continue; }
            if (baha == 18 || baha == 19) {
                int 수 = baha == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= 상수수) näsazlyk_baha("invalid ldc constant");
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
            if (baha == 46 || baha == 50) {
                int aşaky_indeks_baha = 빼기(1), Salgylanma = 빼기(2), ýer_girizmeklik = ARRAY_ýer(Salgylanma, aşaky_indeks_baha, baha == 46 ? 2 : 3);
                if (!Hata) 넣기(힙[ýer_girizmeklik], baha == 46 ? 1 : 2); continue;
            }
            if (baha == 79 || baha == 83) {
                int element_element = 빼기(baha == 79 ? 1 : 2), aşaky_indeks_baha = 빼기(1), Salgylanma = 빼기(2), ýer_girizmeklik = ARRAY_ýer(Salgylanma, aşaky_indeks_baha, baha == 79 ? 2 : 3);
                if (baha == 83 && element_element != 0) obýekt_baha(element_element, 1);
                if (!Hata) 힙[ýer_girizmeklik] = element_element; continue;
            }
            if (baha == 87) { 빼기(0); continue; }
            if (baha == 89) { int 가 = 빼기(0), ýaz_baha = 반환형; 넣기(가, ýaz_baha); 넣기(가, ýaz_baha); continue; }
            if (baha == 95) { int 가 = 빼기(0), 가형 = 반환형, 나 = 빼기(0), 나형 = 반환형; 넣기(가, 가형); 넣기(나, 나형); continue; }
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
            if (baha == 178) {
                int 수 = 명짧(); if (!derňe_hemişelik(수, 9)) continue;
                if (!Söz_SMS(klas_at_SMS(상가[수]), "java/lang/System") || !Söz_SMS(Salgylanma_at(상나[수]), "out")
                    || !Söz_SMS(Salgylanma_ýaz(상나[수]), "Ljava/io/PrintStream;")) näsazlyk_baha("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (baha == 182 || baha == 183 || baha == 184) { Jaň_usul(명짧(), baha); continue; }
            if (baha == 187) {
                int Ad = klas_at_SMS(명짧());
                if (Söz_SMS(Ad, "java/lang/StringBuilder")) 넣기(bölüp_aýyr_Ammar(4, 1), 2);
                else if (Söz_SMS(Ad, "java/io/FileInputStream") || Söz_SMS(Ad, "java/io/FileOutputStream")) {
                    int Salgylanma = bölüp_aýyr_Ammar(Söz_SMS(Ad, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!Hata) { 힙[Salgylanma + 2] = -1; 넣기(Salgylanma, 2); }
                } else näsazlyk_baha("unsupported object construction");
                continue;
            }
            if (baha == 188 || baha == 189) {
                if (baha == 188) { if (명바() != 10) näsazlyk_baha("only int[] newarray is supported"); }
                else if (!Söz_SMS(klas_at_SMS(명짧()), "java/lang/String")) näsazlyk_baha("only String[] anewarray is supported");
                int dowamlylyk_baha = 빼기(1); 넣기(bölüp_aýyr_Ammar(baha == 188 ? 2 : 3, dowamlylyk_baha), 2); continue;
            }
            if (baha == 190) {
                int Salgylanma = 빼기(2);
                if (Salgylanma < 1 || Salgylanma >= 힙끝 - 1 || (힙[Salgylanma] != 2 && 힙[Salgylanma] != 3)) näsazlyk_baha("null or invalid array");
                else 넣기(힙[Salgylanma + 1], 1); continue;
            }
            if (baha == 192) {
                int Ad = klas_at_SMS(명짧()), Salgylanma = 빼기(2);
                if (!Söz_SMS(Ad, "java/lang/String")) näsazlyk_baha("unsupported checkcast");
                else if (Salgylanma != 0) obýekt_baha(Salgylanma, 1);
                넣기(Salgylanma, 2); continue;
            }
            näsazlyk_baha("unsupported bytecode");
        }
    }
    public static int Bitir() {
        if (ulanyjy.인수개수() == 1 && 자바도구.같음(ulanyjy.인수(0), "-version")) {
            ulanyjy.Ýaz("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (ulanyjy.인수개수() < 1) { ulanyjy.Ýaz("Usage: java CLASS [ARGS]\n"); return 2; }
        int dowamlylyk_baha = 자바도구.Ad(faýl_at_SMS, ulanyjy.인수(0));
        if (dowamlylyk_baha < 1 || dowamlylyk_baha > 57) { ulanyjy.Ýaz("java: invalid class name\n"); return 2; }
        faýl_at_SMS[dowamlylyk_baha] = '.'; faýl_at_SMS[dowamlylyk_baha + 1] = 'c'; faýl_at_SMS[dowamlylyk_baha + 2] = 'l'; faýl_at_SMS[dowamlylyk_baha + 3] = 'a'; faýl_at_SMS[dowamlylyk_baha + 4] = 's'; faýl_at_SMS[dowamlylyk_baha + 5] = 's';
        Ululyk = ulanyjy.파일읽기(faýl_at_SMS, Faýl);
        if (Ululyk < 0) { ulanyjy.Ýaz("java: cannot read class: "); 자바도구.수쓰기(Ululyk); ulanyjy.ýaz_nyşan_baha(10); return 1; }
        클래스읽기(); if (Hata) return 1;
        int nyşan_at = hemişelik_SMS(klas_at);
        if (!Hata && 힙[nyşan_at + 1] != dowamlylyk_baha) näsazlyk_baha("class name does not match file");
        for (int 수 = 0; 수 < dowamlylyk_baha && !Hata; 수++) if (힙[nyşan_at + 2 + 수] != faýl_at_SMS[수]) näsazlyk_baha("class name does not match file");
        int girizmeklik_utuk_baha = -1;
        for (int 수 = 0; 수 < 함수수; 수++) if (Söz_SMS(usul_at_SMS[수], "main") && Söz_SMS(usul_ýaz[수], "([Ljava/lang/String;)V") && (usul_ygtyýarlylyk[수] & 9) == 9) girizmeklik_utuk_baha = 수;
        if (girizmeklik_utuk_baha < 0) näsazlyk_baha("public static void main(String[] args) required");
        if (Hata) return 1;
        int 인수 = bölüp_aýyr_Ammar(3, ulanyjy.인수개수() - 1);
        for (int 수 = 1; 수 < ulanyjy.인수개수() && !Hata; 수++) 힙[인수 + 1 + 수] = esasy_nyşan(ulanyjy.인수(수));
        kadr_indeks = 0; kadr_usul[0] = girizmeklik_utuk_baha; 틀위치[0] = usul_başlat[girizmeklik_utuk_baha]; ýerli_baha[0] = 인수; ýerli_ýaz[0] = 2;
        ýerine_ýetir_buýruk(); return Hata ? 1 : 0;
    }
}
