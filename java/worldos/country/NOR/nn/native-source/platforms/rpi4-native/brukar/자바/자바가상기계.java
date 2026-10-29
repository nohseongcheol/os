// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Fil/스택/Oppslagsverk/grein 경계를 Utfør_kommando 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fil = new int[16 * 16384], 임시파일 = new int[16384], fil_namn_SMS = new int[512];
    static int[] konstant_kode = new int[8192], 상가 = new int[8192], konstant_SECOND_VALUE = new int[8192], streng_Oppslagsverk = new int[8192];
    static int[] metode_namn_SMS = new int[512], metode_TYPE = new int[512], metode_tilgang = new int[512], metode_eigar = new int[512];
    static int[] metode_START = new int[512], metode_avslutte = new int[512], metode_Stabel = new int[512], 함수지역 = new int[512];
    static int[] metode_argument_COUNT = new int[512], metode_argument_TYPE = new int[8192], metode_levere_tilbake = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] lokal_VALUE = new int[16384], lokal_TYPE = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] rute_metode = new int[128], rute_plassere = new int[128], rute_Stabel = new int[128], rute_instruksjon = new int[128], starte_rute = new int[128];
    static int[] 종이름 = new int[16], 종크기 = new int[16], 종부모 = new int[16], 종상태 = new int[16], time_felt_COUNT = new int[16], 종초기화 = new int[16];
    static int[] time_grensesnitt = new int[16 * 16], time_grensesnitt_COUNT = new int[16];
    static int[] felt_namn = new int[512], felt_TYPE = new int[512], felt_eigar = new int[512], felt_løyve = new int[512], felt_plassere = new int[512], felt_data = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], ARRAY_element = new int[32768], Store_heiltal = new int[256];
    static int Storleik, 읽기위치, metode_COUNT, time_namn, rute_INDEX = -1, 힙끝 = 1, levere_tilbake_TYPE;
    static int 종수, felt_COUNT, 잡기수, 현재읽는종, 던진객체, 잠시수, vise_COUNT, Samling_COUNT;
    static int betalt_tråd, tråd_COUNT = 1, 시작종;
    static int[] tråd_rute = new int[4], tråd_status = new int[4], tråd_objekt = new int[4], tråd_mål = new int[4], 가닥대기 = new int[4];
    static boolean FEIL, 바꿈요청;
    static int[] blokkere_eigar = new int[32768], 잠금깊이 = new int[32768], rute_blokkere = new int[128], time_blokkere = new int[16], time_tråd = new int[16];

    static void feil_VALUE(String Word_SMS) {
        if (FEIL) return;
        int kategori_CODE = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) kategori_CODE = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) kategori_CODE = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) kategori_CODE = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) kategori_CODE = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) kategori_CODE = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) kategori_CODE = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) kategori_CODE = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) kategori_CODE = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) kategori_CODE = 15;
        if (kategori_CODE != 0 && rute_INDEX >= 0) { 예외던짐(kategori_CODE, Word_SMS); return; }
        brukar.Skriv("JVM error: "); brukar.Skriv(Word_SMS); brukar.skrive_teikn_VALUE(10); FEIL = true;
    }
    static boolean klipp(int Køyr_2, int lengd_VALUE) {
        if (Køyr_2 < 0 || Køyr_2 >= Fil.length || lengd_VALUE < 0) return false;
        int 종 = Køyr_2 / 16384;
        return Køyr_2 % 16384 <= 종크기[종] && lengd_VALUE <= 종크기[종] - Køyr_2 % 16384;
    }
    static int byte_VALUE() {
        if (!klipp(읽기위치, 1)) { feil_VALUE("truncated class file"); return 0; }
        return Fil[읽기위치++];
    }
    static int 짧은수() { return byte_VALUE() << 8 | byte_VALUE(); }
    static int heiltal() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int lengd_VALUE) { if (!klipp(읽기위치, lengd_VALUE)) feil_VALUE("invalid attribute size"); else 읽기위치 += lengd_VALUE; }
    static boolean sjekk_konstant(int 수, int 종류) {
        if (수 <= 0 || 수 >= konstant_kode.length || konstant_kode[수] != 종류) { feil_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Køyr_2, int lengd_VALUE, String Word_SMS) {
        if (!klipp(Køyr_2, lengd_VALUE)) return false;
        int 읽는자리 = Køyr_2, 끝 = Køyr_2 + lengd_VALUE;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_SMS.length(); Loop_INDEX++) {
            int teiknkode = Word_SMS.charAt(Loop_INDEX);
            if (teiknkode > 0 && teiknkode < 128) { if (읽는자리 >= 끝 || Fil[읽는자리++] != teiknkode) return false; }
            else if (teiknkode < 2048) {
                if (읽는자리 + 2 > 끝 || Fil[읽는자리++] != (192 | (teiknkode >> 6)) || Fil[읽는자리++] != (128 | (teiknkode & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Fil[읽는자리++] != (224 | (teiknkode >> 12)) || Fil[읽는자리++] != (128 | ((teiknkode >> 6) & 63)) || Fil[읽는자리++] != (128 | (teiknkode & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Word_SMS(int konstant_VALUE, String Word_SMS) { return sjekk_konstant(konstant_VALUE, 1) && 구간(상가[konstant_VALUE], konstant_SECOND_VALUE[konstant_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!sjekk_konstant(가, 1) || !sjekk_konstant(나, 1) || konstant_SECOND_VALUE[가] != konstant_SECOND_VALUE[나]) return false;
        for (int 수 = 0; 수 < konstant_SECOND_VALUE[가]; 수++) if (Fil[상가[가] + 수] != Fil[상가[나] + 수]) return false;
        return true;
    }
    static int time_namn_SMS(int 수) { return sjekk_konstant(수, 7) && sjekk_konstant(상가[수], 1) ? 상가[수] : 0; }
    static int Oppslagsverk_namn(int 수) { return sjekk_konstant(수, 12) && sjekk_konstant(상가[수], 1) ? 상가[수] : 0; }
    static int Oppslagsverk_TYPE(int 수) { return sjekk_konstant(수, 12) && sjekk_konstant(konstant_SECOND_VALUE[수], 1) ? konstant_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean tom_TYPE) {
        if (읽기위치 >= 끝) { feil_VALUE("invalid descriptor"); return 0; }
        int VALUE = byte_VALUE();
        if (VALUE == 'V' && tom_TYPE) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Køyr_2 = 읽기위치;
            while (읽기위치 < 끝 && Fil[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Køyr_2) feil_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        feil_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_VALUE) {
        int 이전 = 읽기위치, 수 = metode_TYPE[FUNCTION_VALUE];
        if (!sjekk_konstant(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + konstant_SECOND_VALUE[수];
        if (byte_VALUE() != '(') feil_VALUE("invalid method descriptor");
        int vare_COUNT = 0;
        while (!FEIL && 읽기위치 < 끝 && Fil[읽기위치] != ')') {
            if (vare_COUNT == 16) { feil_VALUE("too many method arguments"); break; }
            metode_argument_TYPE[FUNCTION_VALUE * 16 + vare_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || byte_VALUE() != ')') feil_VALUE("invalid method descriptor");
        metode_levere_tilbake[FUNCTION_VALUE] = 서술형(끝, true); metode_argument_COUNT[FUNCTION_VALUE] = vare_COUNT;
        if (읽기위치 != 끝) feil_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return metode_eigar[rute_metode[rute_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int vare_COUNT = 짧은수();
        for (int 수 = 0; 수 < vare_COUNT && !FEIL; 수++) { sjekk_konstant(상번호(), 1); 건너(heiltal()); }
    }
    static int kommando_lengd(int VALUE) {
        if (VALUE == 16 || VALUE == 18 || VALUE == 21 || VALUE == 25 || VALUE == 54 || VALUE == 58 || VALUE == 188) return 2;
        if (VALUE == 17 || VALUE == 19 || VALUE == 132 || VALUE >= 153 && VALUE <= 167
            || VALUE >= 178 && VALUE <= 184 || VALUE == 187 || VALUE == 189 || VALUE == 192 || VALUE == 193 || VALUE == 198 || VALUE == 199) return 3;
        if (VALUE == 185 || VALUE == 200) return 5;
        if (VALUE >= 0 && VALUE <= 8 || VALUE >= 26 && VALUE <= 29 || VALUE >= 42 && VALUE <= 46 || VALUE >= 50 && VALUE <= 53
            || VALUE >= 59 && VALUE <= 62 || VALUE >= 75 && VALUE <= 79 || VALUE >= 83 && VALUE <= 95
            || VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 116
            || VALUE == 120 || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130
            || VALUE >= 145 && VALUE <= 147 || VALUE == 172 || VALUE == 176 || VALUE == 177 || VALUE == 190 || VALUE == 191
            || VALUE == 194 || VALUE == 195) return 1;
        return 0;
    }
    static int plassere_heiltal(int 읽는자리) {
        if (!klipp(읽는자리, 4)) { feil_VALUE("truncated bytecode operand"); return 0; }
        return Fil[읽는자리] << 24 | Fil[읽는자리 + 1] << 16 | Fil[읽는자리 + 2] << 8 | Fil[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Køyr_2, int 끝) {
        int VALUE = Fil[읽는자리], lengd_VALUE = kommando_lengd(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_plassere = 읽는자리 + 1;
            while ((BASE_plassere - Køyr_2) % 4 != 0) BASE_plassere++;
            if (끝 - BASE_plassere < (VALUE == 170 ? 12 : 8)) return 0;
            int oppføring_COUNT = VALUE == 170 ? plassere_heiltal(BASE_plassere + 8) - plassere_heiltal(BASE_plassere + 4) + 1 : plassere_heiltal(BASE_plassere + 4);
            if (oppføring_COUNT < 0 || oppføring_COUNT > 2048) return 0;
            lengd_VALUE = BASE_plassere - 읽는자리 + (VALUE == 170 ? 12 + 4 * oppføring_COUNT : 8 + 8 * oppføring_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_data = Fil[읽는자리 + 1]; lengd_VALUE = Word_data == 132 ? 6 : (Word_data == 21 || Word_data == 25 || Word_data == 54 || Word_data == 58) ? 4 : 0;
        }
        return lengd_VALUE > 0 && lengd_VALUE <= 끝 - 읽는자리 ? lengd_VALUE : 0;
    }
    static void sjekk_mål_VALUE(int mål_VALUE, int FUNCTION_VALUE) {
        if (mål_VALUE < metode_START[FUNCTION_VALUE] || mål_VALUE >= metode_avslutte[FUNCTION_VALUE] || 경계[mål_VALUE] != FUNCTION_VALUE + 1) feil_VALUE("invalid branch target");
    }
    static void 클래스읽기(int 종) {
        현재읽는종 = 종; 읽기위치 = 종 * 16384; Storleik = 읽기위치 + 종크기[종];
        if (heiltal() != 0xcafebabe) { feil_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), versjon_VALUE = 짧은수();
        if (versjon_VALUE < 45 || versjon_VALUE > 52 || 부판 != 0) { feil_VALUE("supported class versions: 45..52, minor 0"); return; }
        int konstant_COUNT = 짧은수(), BASE_plassere = 종 * 512;
        if (konstant_COUNT < 1 || konstant_COUNT > 512) { feil_VALUE("constant pool limit (511)"); return; }
        for (int oppføring_COUNT = 1; oppføring_COUNT < konstant_COUNT && !FEIL; oppføring_COUNT++) {
            int 수 = BASE_plassere + oppføring_COUNT, 종류 = byte_VALUE(); konstant_kode[수] = 종류;
            if (종류 == 1) { konstant_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(konstant_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = heiltal();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); konstant_SECOND_VALUE[수] = 상번호(); }
            else feil_VALUE("unsupported constant type");
        }
        int løyve_VALUE = 짧은수();
        if ((løyve_VALUE & (0x2000 | 0x4000)) != 0) feil_VALUE("annotation/enum class unsupported");
        종이름[종] = time_namn_SMS(상번호());
        종부모[종] = time_namn_SMS(상번호());
        int grensesnitt_COUNT = 짧은수(); if (grensesnitt_COUNT > 16) { feil_VALUE("interface count limit"); return; }
        time_grensesnitt_COUNT[종] = grensesnitt_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < grensesnitt_COUNT; Loop_INDEX++) time_grensesnitt[종 * 16 + Loop_INDEX] = time_namn_SMS(상번호());
        int felt_COUNT_7de3ee76 = 짧은수();
        if (felt_COUNT_7de3ee76 > 512 - felt_COUNT) { feil_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < felt_COUNT_7de3ee76 && !FEIL; Loop_INDEX++) {
            int fil_INDEX = felt_COUNT++; felt_eigar[fil_INDEX] = 종; felt_løyve[fil_INDEX] = 짧은수(); felt_namn[fil_INDEX] = 상번호(); felt_TYPE[fil_INDEX] = 상번호();
            sjekk_konstant(felt_namn[fil_INDEX], 1); sjekk_konstant(felt_TYPE[fil_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[felt_TYPE[fil_INDEX]]; int kategori_CODE = 서술형(읽기위치 + konstant_SECOND_VALUE[felt_TYPE[fil_INDEX]], false); 읽기위치 = 보존값;
            if ((felt_løyve[fil_INDEX] & 8) == 0) felt_plassere[fil_INDEX] = time_felt_COUNT[종]++;
            int attributt_data = 짧은수();
            for (int indre_kopling_plassere = 0; indre_kopling_plassere < attributt_data && !FEIL; indre_kopling_plassere++) {
                int namn_konstant = 상번호(), 유효길이 = heiltal();
                if (Word_SMS(namn_konstant, "ConstantValue") && 유효길이 == 2) {
                    int data_VALUE = 상번호();
                    if (kategori_CODE == 1 && sjekk_konstant(data_VALUE, 3)) felt_data[fil_INDEX] = 상가[data_VALUE];
                    else if (kategori_CODE == 2 && sjekk_konstant(data_VALUE, 8)) felt_data[fil_INDEX] = konstant_SMS(상가[data_VALUE]);
                } else 건너(유효길이);
            }
        }
        int vare_COUNT = 짧은수();
        if (vare_COUNT > 512 - metode_COUNT) { feil_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < vare_COUNT && !FEIL; Loop_INDEX++) {
            int 수 = metode_COUNT++; metode_eigar[수] = 종;
            metode_tilgang[수] = 짧은수(); metode_namn_SMS[수] = 상번호(); metode_TYPE[수] = 상번호();
            sjekk_konstant(metode_namn_SMS[수], 1); 서술읽기(수);
            if ((metode_tilgang[수] & 8) == 0) {
                if (metode_argument_COUNT[수] == 16) { feil_VALUE("too many instance method arguments"); return; }
                for (int Samanlikning_plassere = metode_argument_COUNT[수]; Samanlikning_plassere > 0; Samanlikning_plassere--) metode_argument_TYPE[수 * 16 + Samanlikning_plassere] = metode_argument_TYPE[수 * 16 + Samanlikning_plassere - 1];
                metode_argument_TYPE[수 * 16] = 2; metode_argument_COUNT[수]++;
            }
            if ((metode_tilgang[수] & 0x100) != 0) feil_VALUE("user native method unsupported");
            if (Word_SMS(metode_namn_SMS[수], "<clinit>")) 종초기화[종] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (metode_eigar[앞] == 종 && 같은말(metode_namn_SMS[앞], metode_namn_SMS[수]) && 같은말(metode_TYPE[앞], metode_TYPE[수])) feil_VALUE("duplicate method");
            int attributt_COUNT = 짧은수();
            for (int attributt_VALUE = 0; attributt_VALUE < attributt_COUNT && !FEIL; attributt_VALUE++) {
                int Namn = 상번호(), lengd_VALUE = heiltal(), Køyr_2 = 읽기위치;
                if (!klipp(Køyr_2, lengd_VALUE)) { feil_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Namn, "Code")) {
                    if (metode_START[수] != 0) feil_VALUE("duplicate Code attribute");
                    metode_Stabel[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_lengd = heiltal();
                    if (metode_Stabel[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metode_argument_COUNT[수]
                        || CODE_lengd < 1 || CODE_lengd > 8192) feil_VALUE("method memory limits exceeded");
                    metode_START[수] = 읽기위치; 건너(CODE_lengd); metode_avslutte[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { feil_VALUE("exception table limit"); return; }
                    for (int indre_kopling_plassere = 0; indre_kopling_plassere < 잡는수; indre_kopling_plassere++) {
                        int feil_Oppslagsverk = 잡기수++; 잡기함수[feil_Oppslagsverk] = 수;
                        잡기시작[feil_Oppslagsverk] = metode_START[수] + 짧은수(); 잡기끝[feil_Oppslagsverk] = metode_START[수] + 짧은수();
                        잡기위치[feil_Oppslagsverk] = metode_START[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[feil_Oppslagsverk] = 부호값 == 0 ? 0 : time_namn_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Køyr_2 + lengd_VALUE) feil_VALUE("Code attribute size mismatch");
                } else 건너(lengd_VALUE);
            }
            if ((metode_tilgang[수] & 0x400) != 0) continue;
            if (metode_START[수] == 0) feil_VALUE("missing Code attribute");
            int felt_oppføring = metode_START[수];
            while (felt_oppføring < metode_avslutte[수] && !FEIL) {
                int lengd_VALUE = 길이읽기(felt_oppføring, metode_START[수], metode_avslutte[수]);
                if (lengd_VALUE == 0) { feil_VALUE("unsupported or truncated bytecode"); break; }
                경계[felt_oppføring] = 수 + 1; felt_oppføring += lengd_VALUE;
            }
            felt_oppføring = metode_START[수];
            while (felt_oppføring < metode_avslutte[수] && !FEIL) {
                int VALUE = Fil[felt_oppføring];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) sjekk_mål_VALUE(felt_oppføring + (short)(Fil[felt_oppføring + 1] << 8 | Fil[felt_oppføring + 2]), 수);
                if (VALUE == 200) sjekk_mål_VALUE(felt_oppføring + plassere_heiltal(felt_oppføring + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = felt_oppføring + 1; while ((읽는자리 - metode_START[수]) % 4 != 0) 읽는자리++;
                    sjekk_mål_VALUE(felt_oppføring + plassere_heiltal(읽는자리), 수);
                    int oppføring_COUNT = VALUE == 170 ? plassere_heiltal(읽는자리 + 8) - plassere_heiltal(읽는자리 + 4) + 1 : plassere_heiltal(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int indre_kopling_plassere = 0; indre_kopling_plassere < oppføring_COUNT; indre_kopling_plassere++) sjekk_mål_VALUE(felt_oppføring + plassere_heiltal(읽는자리 + indre_kopling_plassere * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                felt_oppføring += 길이읽기(felt_oppføring, metode_START[수], metode_avslutte[수]);
            }
            for (int indre_kopling_plassere = 0; indre_kopling_plassere < 잡기수; indre_kopling_plassere++) if (잡기함수[indre_kopling_plassere] == 수) {
                sjekk_mål_VALUE(잡기시작[indre_kopling_plassere], 수); sjekk_mål_VALUE(잡기위치[indre_kopling_plassere], 수);
                if (잡기끝[indre_kopling_plassere] != metode_avslutte[수]) sjekk_mål_VALUE(잡기끝[indre_kopling_plassere], 수);
                if (잡기시작[indre_kopling_plassere] >= 잡기끝[indre_kopling_plassere]) feil_VALUE("invalid exception range");
            }
        }
        if (!FEIL) 속성건너();
        if (읽기위치 != Storleik) feil_VALUE("extra class file data");
    }
    static int tildele_Lagring(int 종류, int lengd_VALUE) { return 새기억(종류, lengd_VALUE); }
    static boolean objekt_VALUE(int Oppslagsverk, int 종류) {
        if (!객체유효(Oppslagsverk)) return false;
        if (힙[Oppslagsverk] != 종류) { feil_VALUE("object type mismatch"); return false; }
        return true;
    }
    static int konstant_SMS(int INDEX) {
        if (!sjekk_konstant(INDEX, 1)) return 0;
        if (streng_Oppslagsverk[INDEX] != 0) return streng_Oppslagsverk[INDEX];
        int Oppslagsverk = tildele_Lagring(1, konstant_SECOND_VALUE[INDEX]); if (FEIL) return 0;
        int 끝 = 상가[INDEX] + konstant_SECOND_VALUE[INDEX], 수 = 상가[INDEX], lengd_VALUE = 0;
        while (수 < 끝 && !FEIL) {
            int VALUE = Fil[수++];
            if (VALUE == 0) feil_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Neste_vare = Fil[수++];
                if ((Neste_vare & 192) != 128) feil_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Neste_vare & 63;
                if (VALUE != 0 && VALUE < 128) feil_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = Fil[수++], 나 = Fil[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) feil_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (VALUE < 2048) feil_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) feil_VALUE("invalid modified UTF-8");
            힙[Oppslagsverk + 2 + lengd_VALUE++] = VALUE;
        }
        힙[Oppslagsverk + 1] = lengd_VALUE; streng_Oppslagsverk[INDEX] = Oppslagsverk; return Oppslagsverk;
    }
    static int vert_teikn(String VALUE) {
        int Oppslagsverk = tildele_Lagring(1, VALUE.length()); if (FEIL) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) 힙[Oppslagsverk + 2 + 수] = VALUE.charAt(수);
        return Oppslagsverk;
    }
    static void skrive_SMS(int Oppslagsverk) {
        if (Oppslagsverk == 0) { brukar.Skriv("null"); return; }
        if (!objekt_VALUE(Oppslagsverk, 1)) return;
        for (int 수 = 0; 수 < 힙[Oppslagsverk + 1]; 수++) brukar.skrive_teikn_VALUE(힙[Oppslagsverk + 2 + 수]);
    }
    static int siffer_teikn(int VALUE) {
        int Oppslagsverk = tildele_Lagring(1, 11); if (FEIL) return 0;
        int lengd_VALUE = 0;
        if (VALUE < 0) 힙[Oppslagsverk + 2 + lengd_VALUE++] = '-'; else VALUE = -VALUE;
        int plassere_INDEX = 1000000000; boolean Køyr_2 = false;
        while (plassere_INDEX != 0) {
            int 수 = -(VALUE / plassere_INDEX);
            if (수 != 0 || Køyr_2 || plassere_INDEX == 1) { 힙[Oppslagsverk + 2 + lengd_VALUE++] = '0' + 수; Køyr_2 = true; }
            VALUE %= plassere_INDEX; plassere_INDEX /= 10;
        }
        힙[Oppslagsverk + 1] = lengd_VALUE; return Oppslagsverk;
    }
    static int 정수해독(int Oppslagsverk) {
        if (!objekt_VALUE(Oppslagsverk, 1)) return 0;
        int lengd_VALUE = 힙[Oppslagsverk + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (lengd_VALUE > 0 && (힙[Oppslagsverk + 2] == '-' || 힙[Oppslagsverk + 2] == '+')) { 음수 = 힙[Oppslagsverk + 2] == '-'; 수++; }
        if (수 == lengd_VALUE) feil_VALUE("NumberFormatException");
        for (; 수 < lengd_VALUE && !FEIL; 수++) {
            int siffer_VALUE = 힙[Oppslagsverk + 2 + 수] - '0';
            if (siffer_VALUE < 0 || siffer_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && siffer_VALUE > (음수 ? 8 : 7)) feil_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - siffer_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (FEIL) return;
        if (rute_INDEX < 0 || rute_Stabel[rute_INDEX] >= metode_Stabel[rute_metode[rute_INDEX]]) { feil_VALUE("operand stack overflow"); return; }
        int felt_oppføring = rute_INDEX * 128 + rute_Stabel[rute_INDEX]++; 스택값[felt_oppføring] = VALUE; 스택형[felt_oppføring] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (FEIL) return 0;
        if (rute_INDEX < 0 || rute_Stabel[rute_INDEX] < 1) { feil_VALUE("operand stack underflow"); return 0; }
        int felt_oppføring = rute_INDEX * 128 + --rute_Stabel[rute_INDEX]; levere_tilbake_TYPE = 스택형[felt_oppføring];
        if (TYPE_VALUE != 0 && levere_tilbake_TYPE != TYPE_VALUE) feil_VALUE("operand type mismatch");
        if (levere_tilbake_TYPE == 2) verne_VALUE(스택값[felt_oppføring]);
        return 스택값[felt_oppføring];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[rute_metode[rute_INDEX]] || INDEX < 0 || lokal_TYPE[rute_INDEX * 128 + INDEX] != TYPE_VALUE) { feil_VALUE("invalid or uninitialized local"); return; }
        넣기(lokal_VALUE[rute_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void skrive_lokal(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[rute_metode[rute_INDEX]] || INDEX < 0) { feil_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); lokal_VALUE[rute_INDEX * 128 + INDEX] = VALUE; lokal_TYPE[rute_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int Posisjon = rute_plassere[rute_INDEX];
        if (Posisjon < metode_START[rute_metode[rute_INDEX]] || Posisjon >= metode_avslutte[rute_metode[rute_INDEX]]) { feil_VALUE("instruction pointer out of range"); return 0; }
        rute_plassere[rute_INDEX]++; return Fil[Posisjon];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void flytte_VALUE(int Posisjon) {
        int FUNCTION_VALUE = rute_metode[rute_INDEX];
        if (Posisjon < metode_START[FUNCTION_VALUE] || Posisjon >= metode_avslutte[FUNCTION_VALUE] || 경계[Posisjon] != FUNCTION_VALUE + 1) feil_VALUE("invalid branch target");
        else rute_plassere[rute_INDEX] = Posisjon;
    }
    static void 호출(int FUNCTION_VALUE) {
        if (rute_INDEX % 32 == 31) { feil_VALUE("call stack limit (32)"); return; }
        int Neste_vare = rute_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokal_TYPE[Neste_vare * 128 + 수] = 0;
        for (int 수 = metode_argument_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            lokal_VALUE[Neste_vare * 128 + 수] = 빼기(metode_argument_TYPE[FUNCTION_VALUE * 16 + 수]); lokal_TYPE[Neste_vare * 128 + 수] = metode_argument_TYPE[FUNCTION_VALUE * 16 + 수];
        }
        if (FEIL) return;
        rute_INDEX = Neste_vare; starte_rute[rute_INDEX] = 0; rute_metode[rute_INDEX] = FUNCTION_VALUE; rute_plassere[rute_INDEX] = metode_START[FUNCTION_VALUE]; rute_Stabel[rute_INDEX] = 0;
    }
    static void levere_tilbake_forretningsmål(int TYPE_VALUE) {
        if (TYPE_VALUE != metode_levere_tilbake[rute_metode[rute_INDEX]]) { feil_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (starte_rute[rute_INDEX] != 0) 종상태[starte_rute[rute_INDEX] - 1] = 2;
        if (rute_blokkere[rute_INDEX] != 0) { frigi_blokkere(rute_blokkere[rute_INDEX]); rute_blokkere[rute_INDEX] = 0; }
        rute_INDEX--; if (rute_INDEX >= betalt_tråd * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] Stream_fil_namn = new int[64];
    static void fil_Stream_CALL(int eigar_VALUE, int Namn, int format_VALUE, int Kommando) {
        boolean Utdata = Word_SMS(eigar_VALUE, "java/io/FileOutputStream");
        int 종류 = Utdata ? 6 : 5;
        if (Kommando == 183 && Word_SMS(Namn, "<init>")) {
            boolean 이어 = false;
            if (Utdata && Word_SMS(format_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { feil_VALUE("unsupported file stream constructor"); return; }
            int fil_oppføring_namn = 빼기(2), Stream_VALUE = 빼기(2);
            if (!objekt_VALUE(fil_oppføring_namn, 1) || !objekt_VALUE(Stream_VALUE, 종류) || FEIL) return;
            if (힙[Stream_VALUE + 3] != 0) { feil_VALUE("file stream already initialized"); return; }
            int lengd_VALUE = 힙[fil_oppføring_namn + 1];
            if (lengd_VALUE < 1 || lengd_VALUE > 63) { feil_VALUE("invalid file name length"); return; }
            for (int felt_oppføring = 0; felt_oppføring < lengd_VALUE; felt_oppføring++) {
                int VALUE = 힙[fil_oppføring_namn + 2 + felt_oppføring];
                if (VALUE < 1) { feil_VALUE("invalid file stream path"); return; }
                Stream_fil_namn[felt_oppføring] = VALUE;
            }
            Stream_fil_namn[lengd_VALUE] = 0;
            int 서술자 = brukar.파일서술자열기(Stream_fil_namn, Utdata ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { feil_VALUE("FileNotFoundException: file open failed"); return; }
            힙[Stream_VALUE + 2] = 서술자; 힙[Stream_VALUE + 3] = 1;
            return;
        }
        if (Kommando != 182) { feil_VALUE("invalid file stream invocation"); return; }
        if ((Utdata && Word_SMS(Namn, "write") || !Utdata && Word_SMS(Namn, "read"))
            && (Word_SMS(format_VALUE, Utdata ? "([B)V" : "([B)I") || Word_SMS(format_VALUE, Utdata ? "([BII)V" : "([BII)I"))) {
            boolean klipp_VALUE = Word_SMS(format_VALUE, Utdata ? "([BII)V" : "([BII)I");
            int oppføring_COUNT = klipp_VALUE ? 빼기(1) : 0, 시작점 = klipp_VALUE ? 빼기(1) : 0, data_ARRAY = 빼기(2), objekt_Oppslagsverk = 빼기(2);
            if (!objekt_VALUE(data_ARRAY, 20) || !objekt_VALUE(objekt_Oppslagsverk, 종류)) return;
            if (!klipp_VALUE) oppføring_COUNT = 힙[data_ARRAY + 1];
            if (시작점 < 0 || oppføring_COUNT < 0 || 시작점 > 힙[data_ARRAY + 1] - oppføring_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[objekt_Oppslagsverk + 3] == 0 || 힙[objekt_Oppslagsverk + 2] < 0) { feil_VALUE("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < oppføring_COUNT && !FEIL) {
                int 반환값 = Utdata ? brukar.파일한바이트쓰기(힙[objekt_Oppslagsverk + 2], 힙[data_ARRAY + 2 + 시작점 + 완료수]) : brukar.파일한바이트읽기(힙[objekt_Oppslagsverk + 2]);
                if (반환값 < 0) { feil_VALUE(Utdata ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Utdata && 반환값 == 256) break;
                if (!Utdata) 힙[data_ARRAY + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!Utdata) 넣기(oppføring_COUNT != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (Utdata && Word_SMS(Namn, "flush") && Word_SMS(format_VALUE, "()V")) { int objekt_Oppslagsverk = 빼기(2); if (objekt_VALUE(objekt_Oppslagsverk, 종류) && 힙[objekt_Oppslagsverk + 2] < 0) feil_VALUE("IOException: stream closed"); return; }
        int Handling = -1, VALUE = 0;
        if (Word_SMS(Namn, "close") && Word_SMS(format_VALUE, "()V")) Handling = 0;
        if (!Utdata && Word_SMS(Namn, "read") && Word_SMS(format_VALUE, "()I")) Handling = 1;
        if (Utdata && Word_SMS(Namn, "write") && Word_SMS(format_VALUE, "(I)V")) { Handling = 2; VALUE = 빼기(1); }
        if (Handling < 0) { feil_VALUE("unsupported file stream method"); return; }
        int Stream_VALUE = 빼기(2);
        if (!objekt_VALUE(Stream_VALUE, 종류) || FEIL) return;
        if (힙[Stream_VALUE + 3] == 0) { feil_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_VALUE + 2];
        if (Handling == 0) {
            if (서술자 >= 0 && brukar.파일서술자닫기(서술자) < 0) feil_VALUE("IOException: close failed");
            힙[Stream_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { feil_VALUE("IOException: stream closed"); return; }
        if (Handling == 1) {
            int forretningsmål = brukar.파일한바이트읽기(서술자);
            if (forretningsmål < -1) feil_VALUE("IOException: read failed"); else 넣기(forretningsmål == 256 ? -1 : forretningsmål, 1);
        } else if (brukar.파일한바이트쓰기(서술자, VALUE) != 1) feil_VALUE("IOException: write failed");
    }
    static void CALL_metode(int INDEX, int Kommando) {
        if (INDEX <= 0 || INDEX >= konstant_kode.length || (konstant_kode[INDEX] != 10 && konstant_kode[INDEX] != 11)) { feil_VALUE("invalid method reference"); return; }
        int eigar_VALUE = time_namn_SMS(상가[INDEX]), Namn = Oppslagsverk_namn(konstant_SECOND_VALUE[INDEX]), format_VALUE = Oppslagsverk_TYPE(konstant_SECOND_VALUE[INDEX]);
        if (FEIL) return;
        if (기본호출(eigar_VALUE, Namn, format_VALUE, Kommando)) return;
        if (Word_SMS(eigar_VALUE, "java/io/FileInputStream") || Word_SMS(eigar_VALUE, "java/io/FileOutputStream")) {
            fil_Stream_CALL(eigar_VALUE, Namn, format_VALUE, Kommando); return;
        }
        if (Kommando == 184 && Word_SMS(eigar_VALUE, "java/lang/Integer") && Word_SMS(Namn, "parseInt") && Word_SMS(format_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Kommando == 182 && Word_SMS(eigar_VALUE, "java/io/PrintStream") && (Word_SMS(Namn, "println") || Word_SMS(Namn, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(format_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(format_VALUE, "()V") || !Word_SMS(Namn, "println")) feil_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) feil_VALUE("invalid PrintStream receiver");
            if (FEIL) return;
            if (TYPE_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (TYPE_VALUE == 2) brukar.Skriv(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) brukar.skrive_teikn_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) skrive_SMS(VALUE);
            if (Word_SMS(Namn, "println")) brukar.skrive_teikn_VALUE(10);
            return;
        }
        if (Kommando == 182 && Word_SMS(eigar_VALUE, "java/lang/String")) {
            if (Word_SMS(Namn, "length") && Word_SMS(format_VALUE, "()I")) {
                int Oppslagsverk = 빼기(2); if (objekt_VALUE(Oppslagsverk, 1)) 넣기(힙[Oppslagsverk + 1], 1); return;
            }
            if (Word_SMS(Namn, "charAt") && Word_SMS(format_VALUE, "(I)C")) {
                int senka_skrift_VALUE = 빼기(1), Oppslagsverk = 빼기(2);
                if (objekt_VALUE(Oppslagsverk, 1)) {
                    if (senka_skrift_VALUE < 0 || senka_skrift_VALUE >= 힙[Oppslagsverk + 1]) feil_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[Oppslagsverk + 2 + senka_skrift_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(eigar_VALUE, "java/lang/StringBuilder")) {
            if (Kommando == 183 && Word_SMS(Namn, "<init>") && Word_SMS(format_VALUE, "()V")) { objekt_VALUE(빼기(2), 4); return; }
            if (Kommando == 182 && Word_SMS(Namn, "toString") && Word_SMS(format_VALUE, "()Ljava/lang/String;")) {
                int Oppslagsverk = 빼기(2); if (objekt_VALUE(Oppslagsverk, 4)) 넣기(힙[Oppslagsverk + 2] == 0 ? vert_teikn("") : 힙[Oppslagsverk + 2], 2); return;
            }
            if (Kommando == 182 && Word_SMS(Namn, "append")) {
                int Tekst = 0;
                if (Word_SMS(format_VALUE, "(I)Ljava/lang/StringBuilder;")) Tekst = siffer_teikn(빼기(1));
                else if (Word_SMS(format_VALUE, "(Z)Ljava/lang/StringBuilder;")) Tekst = vert_teikn(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(format_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Tekst = tildele_Lagring(1, 1); if (!FEIL) 힙[Tekst + 2] = VALUE & 65535;
                }
                else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Tekst = 빼기(2); if (Tekst == 0) Tekst = vert_teikn("null"); }
                else { feil_VALUE("unsupported StringBuilder append"); return; }
                int Oppslagsverk = 빼기(2); if (!objekt_VALUE(Oppslagsverk, 4) || !objekt_VALUE(Tekst, 1)) return;
                int 앞 = 힙[Oppslagsverk + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], TILBAKE_VALUE_lengd = 힙[Tekst + 1];
                int 새글 = tildele_Lagring(1, 앞길이 + TILBAKE_VALUE_lengd); if (FEIL) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < TILBAKE_VALUE_lengd; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[Tekst + 2 + 수];
                힙[Oppslagsverk + 2] = 새글; 넣기(Oppslagsverk, 2); return;
            }
        }
        int 종 = 종찾기(eigar_VALUE); if (종 < 0 || FEIL) return;
        int fil_INDEX = Søk_metode(종, Namn, format_VALUE);
        if (fil_INDEX < 0) {
            for (int teiknkode = 종, oppføring_COUNT = 0; teiknkode >= 0 && oppføring_COUNT < 16; oppføring_COUNT++, teiknkode = forelder_time(teiknkode))
                if (Word_SMS(종부모[teiknkode], "java/lang/Thread")) { 가닥호출(Namn, format_VALUE, Kommando); return; }
            feil_VALUE("NoSuchMethodError"); return;
        }
        if (((metode_tilgang[fil_INDEX] & 8) != 0) != (Kommando == 184)) { feil_VALUE("method static/instance mismatch"); return; }
        if (Kommando == 184) { if (!starte(metode_eigar[fil_INDEX], rute_instruksjon[rute_INDEX])) return; }
        else {
            int 읽는자리 = rute_Stabel[rute_INDEX] - metode_argument_COUNT[fil_INDEX];
            if (읽는자리 < 0 || 스택형[rute_INDEX * 128 + 읽는자리] != 2) { feil_VALUE("invalid method receiver"); return; }
            int objekt_Oppslagsverk = 스택값[rute_INDEX * 128 + 읽는자리];
            if (!객체유효(objekt_Oppslagsverk)) return;
            if (힙[objekt_Oppslagsverk] < 32 || !종포함(힙[objekt_Oppslagsverk] - 32, eigar_VALUE)) { feil_VALUE("method receiver type mismatch"); return; }
            if (Kommando != 183) fil_INDEX = Søk_metode(힙[objekt_Oppslagsverk] - 32, Namn, format_VALUE);
        }
        if (fil_INDEX < 0 || (metode_tilgang[fil_INDEX] & 0x400) != 0) { feil_VALUE("AbstractMethodError"); return; }
        int blokkere_Oppslagsverk = 0;
        if ((metode_tilgang[fil_INDEX] & 32) != 0) {
            if (Kommando == 184) { int teiknkode = metode_eigar[fil_INDEX]; if (time_blokkere[teiknkode] == 0) time_blokkere[teiknkode] = tildele_Lagring(8, 0); blokkere_Oppslagsverk = time_blokkere[teiknkode]; }
            else blokkere_Oppslagsverk = 스택값[rute_INDEX * 128 + rute_Stabel[rute_INDEX] - metode_argument_COUNT[fil_INDEX]];
            if (!잠금얻기(blokkere_Oppslagsverk)) { if (!FEIL) rute_plassere[rute_INDEX] = rute_instruksjon[rute_INDEX]; return; }
        }
        호출(fil_INDEX); if (!FEIL) rute_blokkere[rute_INDEX] = blokkere_Oppslagsverk;
    }
    static boolean 배열저장가능(int ARRAY_Oppslagsverk, int data_VALUE) {
        if (data_VALUE == 0 || ARRAY_element[ARRAY_Oppslagsverk] == 0) return true;
        boolean 성공여부 = ARRAY_element[ARRAY_Oppslagsverk] == -1 ? (data_VALUE > 0 && data_VALUE < 힙끝 && 힙[data_VALUE] == 1) : 맞는객체(data_VALUE, ARRAY_element[ARRAY_Oppslagsverk]);
        if (!성공여부 && !FEIL) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int ARRAY_felt(int Oppslagsverk, int senka_skrift_VALUE, int TYPE_VALUE) {
        if (!objekt_VALUE(Oppslagsverk, TYPE_VALUE)) return 0;
        if (senka_skrift_VALUE < 0 || senka_skrift_VALUE >= 힙[Oppslagsverk + 1]) { feil_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Oppslagsverk + 2 + senka_skrift_VALUE;
    }
    static void Utfør_kommando() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (FEIL) { if (던진객체 != 0) handtak_unntak(); if (FEIL || rute_INDEX < betalt_tråd * 32) break; }
            if (rute_INDEX < betalt_tråd * 32 || 바꿈요청 || --조각 == 0) { if (!byte_tråd()) break; 조각 = 100; }
            if (rute_INDEX == 0 && 종상태[시작종] != 2 && !starte(시작종, rute_plassere[rute_INDEX])) continue;
            if (rute_INDEX == betalt_tråd * 32 && betalt_tråd != 0 && (metode_tilgang[rute_metode[rute_INDEX]] & 32) != 0 && rute_blokkere[rute_INDEX] == 0) {
                int objekt_Oppslagsverk = tråd_mål[betalt_tråd]; if (!잠금얻기(objekt_Oppslagsverk)) { if (FEIL) break; continue; } rute_blokkere[rute_INDEX] = objekt_Oppslagsverk;
            }
            잠시수 = 0;
            if (--남음 == 0) { feil_VALUE("instruction limit (500000)"); break; }
            int Køyr_2 = rute_plassere[rute_INDEX]; rute_instruksjon[rute_INDEX] = Køyr_2; int VALUE = 명바();
            if (FEIL) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = metode_eigar[rute_metode[rute_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= konstant_kode.length) feil_VALUE("invalid ldc constant");
                else if (konstant_kode[수] == 3) 넣기(상가[수], 1);
                else if (konstant_kode[수] == 8) 넣기(konstant_SMS(상가[수]), 2);
                else feil_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { skrive_lokal(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { skrive_lokal(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { skrive_lokal(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int oppføring_plassere = 빼기(1), objekt_Oppslagsverk = 빼기(2), kategori_CODE = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && objekt_Oppslagsverk > 0 && objekt_Oppslagsverk < 힙끝 && 힙[objekt_Oppslagsverk] == 21) kategori_CODE = 21;
                int 읽는자리 = ARRAY_felt(objekt_Oppslagsverk, oppføring_plassere, kategori_CODE); if (!FEIL) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int oppføring_Oppslagsverk = 빼기(VALUE == 83 ? 2 : 1), oppføring_plassere = 빼기(1), objekt_Oppslagsverk = 빼기(2), kategori_CODE = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && objekt_Oppslagsverk > 0 && objekt_Oppslagsverk < 힙끝 && 힙[objekt_Oppslagsverk] == 21) kategori_CODE = 21;
                int 읽는자리 = ARRAY_felt(objekt_Oppslagsverk, oppføring_plassere, kategori_CODE);
                if (!FEIL && kategori_CODE == 3 && !배열저장가능(objekt_Oppslagsverk, oppføring_Oppslagsverk)) continue;
                if (!FEIL) 힙[읽는자리] = kategori_CODE == 20 ? (byte)oppføring_Oppslagsverk : kategori_CODE == 21 ? oppføring_Oppslagsverk & 1 : kategori_CODE == 22 ? (char)oppføring_Oppslagsverk : kategori_CODE == 23 ? (short)oppføring_Oppslagsverk : oppføring_Oppslagsverk;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { Stabel_instruksjon(VALUE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), forretningsmål = 0;
                if ((VALUE == 108 || VALUE == 112) && 나 == 0) { feil_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) forretningsmål = 가 + 나;
                if (VALUE == 100) forretningsmål = 가 - 나;
                if (VALUE == 104) forretningsmål = 가 * 나;
                if (VALUE == 108) forretningsmål = 가 / 나;
                if (VALUE == 112) forretningsmål = 가 % 나;
                if (VALUE == 120) forretningsmål = 가 << 나;
                if (VALUE == 122) forretningsmål = 가 >> 나;
                if (VALUE == 124) forretningsmål = 가 >>> 나;
                if (VALUE == 126) forretningsmål = 가 & 나;
                if (VALUE == 128) forretningsmål = 가 | 나;
                if (VALUE == 130) forretningsmål = 가 ^ 나;
                넣기(forretningsmål, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int lokal_område = 명바(), 증분 = (byte)명바(); 지역읽기(lokal_område, 1); 넣기(빼기(1) + 증분, 1); skrive_lokal(lokal_område, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int mål_VALUE = Køyr_2 + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int 나 = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == 나 : VALUE == 160 || VALUE == 166 ? 가 != 나 : VALUE == 161 ? 가 < 나 : VALUE == 162 ? 가 >= 나 : VALUE == 163 ? 가 > 나 : 가 <= 나;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) flytte_VALUE(mål_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { levere_tilbake_forretningsmål(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, Køyr_2); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { feil_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_metode(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(time_namn_SMS(명상수()), Køyr_2); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int kategori_CODE = 3, komponent = 0;
                if (VALUE == 188) { int 임시값 = 명바(); kategori_CODE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else komponent = time_namn_SMS(명상수());
                if (kategori_CODE == 0) { feil_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), objekt_Oppslagsverk = tildele_Lagring(kategori_CODE, 유효길이); if (!FEIL) ARRAY_element[objekt_Oppslagsverk] = komponent; 넣기(objekt_Oppslagsverk, 2); continue;
            }
            if (VALUE == 190) {
                int objekt_Oppslagsverk = 빼기(2);
                if (객체유효(objekt_Oppslagsverk)) { int Samanlikning_plassere = 힙[objekt_Oppslagsverk]; if (Samanlikning_plassere != 2 && Samanlikning_plassere != 3 && (Samanlikning_plassere < 20 || Samanlikning_plassere > 23)) feil_VALUE("not an array"); else 넣기(힙[objekt_Oppslagsverk + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int objekt_Oppslagsverk = 빼기(2); if (객체유효(objekt_Oppslagsverk)) { if (힙[objekt_Oppslagsverk] != 9) feil_VALUE("athrow requires supported Throwable"); else { 던진객체 = objekt_Oppslagsverk; FEIL = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int namn_konstant = time_namn_SMS(명상수()), objekt_Oppslagsverk = 빼기(2); boolean MATCH = 맞는객체(objekt_Oppslagsverk, namn_konstant);
                if (VALUE == 193) 넣기(objekt_Oppslagsverk != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !FEIL) feil_VALUE("ClassCastException"); 넣기(objekt_Oppslagsverk, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = Køyr_2 + 1, fil_INDEX = rute_metode[rute_INDEX], tast_Oppslagsverk = 빼기(1);
                while ((읽는자리 - metode_START[fil_INDEX]) % 4 != 0) 읽는자리++;
                int mål_ADDRESS = plassere_heiltal(읽는자리);
                if (VALUE == 170) { int 낮은값 = plassere_heiltal(읽는자리 + 4), 높은값 = plassere_heiltal(읽는자리 + 8); if (tast_Oppslagsverk >= 낮은값 && tast_Oppslagsverk <= 높은값) mål_ADDRESS = plassere_heiltal(읽는자리 + 12 + (tast_Oppslagsverk - 낮은값) * 4); }
                else { int 총수 = plassere_heiltal(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (plassere_heiltal(읽는자리 + 8 + Loop_INDEX * 8) == tast_Oppslagsverk) mål_ADDRESS = plassere_heiltal(읽는자리 + 12 + Loop_INDEX * 8); }
                flytte_VALUE(Køyr_2 + mål_ADDRESS); continue;
            }
            if (VALUE == 200) { flytte_VALUE(Køyr_2 + plassere_heiltal(Køyr_2 + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int objekt_Oppslagsverk = 빼기(2);
                if (VALUE == 195) frigi_blokkere(objekt_Oppslagsverk);
                else if (!잠금얻기(objekt_Oppslagsverk) && !FEIL) { 넣기(objekt_Oppslagsverk, 2); rute_plassere[rute_INDEX] = Køyr_2; }
                continue;
            }
            if (VALUE == 196) {
                int kommando_CODE = 명바(), oppføring_plassere = 명짧();
                if (kommando_CODE == 21 || kommando_CODE == 25) 지역읽기(oppføring_plassere, kommando_CODE == 21 ? 1 : 2);
                else if (kommando_CODE == 54 || kommando_CODE == 58) skrive_lokal(oppføring_plassere, kommando_CODE == 54 ? 1 : 2);
                else if (kommando_CODE == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(oppføring_plassere, 1); 넣기(빼기(1) + DELTA_VALUE, 1); skrive_lokal(oppføring_plassere, 1); }
                else feil_VALUE("unsupported wide opcode");
                continue;
            }
            feil_VALUE("unsupported bytecode");
        }
    }
    static int 종찾기(int Namn) {
        for (int Loop_INDEX = 0; Loop_INDEX < 종수; Loop_INDEX++) if (종이름[Loop_INDEX] != 0 && 같은말(종이름[Loop_INDEX], Namn)) return Loop_INDEX;
        return 종적재(konstant_SMS(Namn));
    }
    static int 종적재(int namn_streng) {
        if (!objekt_VALUE(namn_streng, 1)) return -1;
        int lengd_VALUE = 힙[namn_streng + 1];
        if (lengd_VALUE < 1 || lengd_VALUE > 505 || 종수 == 16) { feil_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < lengd_VALUE; Loop_INDEX++) { int teiknkode = 힙[namn_streng + 2 + Loop_INDEX]; fil_namn_SMS[Loop_INDEX] = teiknkode == '/' ? '.' : teiknkode; }
        fil_namn_SMS[lengd_VALUE] = '.'; fil_namn_SMS[lengd_VALUE + 1] = 'c'; fil_namn_SMS[lengd_VALUE + 2] = 'l'; fil_namn_SMS[lengd_VALUE + 3] = 'a'; fil_namn_SMS[lengd_VALUE + 4] = 's'; fil_namn_SMS[lengd_VALUE + 5] = 's'; fil_namn_SMS[lengd_VALUE + 6] = 0;
        int Storleik = brukar.파일읽기(fil_namn_SMS, 임시파일);
        if (Storleik < 0) { feil_VALUE("ClassNotFoundException"); return -1; }
        int 종 = 종수++; 종크기[종] = Storleik;
        for (int Loop_INDEX = 0; Loop_INDEX < Storleik; Loop_INDEX++) Fil[종 * 16384 + Loop_INDEX] = 임시파일[Loop_INDEX];
        클래스읽기(종); if (FEIL) return -1;
        int faktisk_data = konstant_SMS(종이름[종]);
        if (!글같음(faktisk_data, namn_streng, true)) { feil_VALUE("class name does not match file"); return -1; }
        int forelder_VALUE = 종부모[종];
        if (forelder_VALUE != 0 && !Word_SMS(forelder_VALUE, "java/lang/Object") && !Word_SMS(forelder_VALUE, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = 종찾기(forelder_VALUE);
            if (FEIL || 위 < 0) return -1;
            int 읽는자리 = 위, stadium_COUNT = 0;
            while (읽는자리 >= 0 && stadium_COUNT++ < 16) {
                if (읽는자리 == 종) { feil_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = forelder_time(읽는자리);
            }
            int 시작변위 = time_felt_COUNT[위];
            for (int fil_INDEX = 0; fil_INDEX < felt_COUNT; fil_INDEX++) if (felt_eigar[fil_INDEX] == 종 && (felt_løyve[fil_INDEX] & 8) == 0) felt_plassere[fil_INDEX] += 시작변위;
            time_felt_COUNT[종] += 시작변위;
        }
        return 종;
    }
    static int forelder_time(int 종) {
        int Namn = 종부모[종];
        for (int Loop_INDEX = 0; Loop_INDEX < 종수; Loop_INDEX++) if (Namn != 0 && 종이름[Loop_INDEX] != 0 && 같은말(종이름[Loop_INDEX], Namn)) return Loop_INDEX;
        return -1;
    }
    static int Søk_metode(int 종, int Namn, int format_VALUE) {
        for (int 깊이 = 0; 종 >= 0 && 깊이 < 16; 깊이++, 종 = forelder_time(종)) {
            for (int Loop_INDEX = 0; Loop_INDEX < metode_COUNT; Loop_INDEX++) if (metode_eigar[Loop_INDEX] == 종 && 같은말(metode_namn_SMS[Loop_INDEX], Namn) && 같은말(metode_TYPE[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int namn_metode(int 종, String Namn, String format_VALUE) {
        for (int 깊이 = 0; 종 >= 0 && 깊이 < 16; 깊이++, 종 = forelder_time(종))
            for (int Loop_INDEX = 0; Loop_INDEX < metode_COUNT; Loop_INDEX++) if (metode_eigar[Loop_INDEX] == 종 && Word_SMS(metode_namn_SMS[Loop_INDEX], Namn) && Word_SMS(metode_TYPE[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int Namn) { return Fil[상가[Namn]] == 'L' || Fil[상가[Namn]] == '[' ? 2 : 1; }
    static boolean starte(int 종, int kommando_START) {
        if (종 < 0 || FEIL) return false;
        if (종상태[종] == 3) { feil_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (종상태[종] == 1 && time_tråd[종] != betalt_tråd) { rute_plassere[rute_INDEX] = kommando_START; 바꿈요청 = true; return false; }
        if (종상태[종] != 0) return true;
        int 위 = forelder_time(종);
        if (위 >= 0 && !starte(위, kommando_START)) return false;
        종상태[종] = 1; time_tråd[종] = betalt_tråd;
        if (종초기화[종] != 0) {
            rute_plassere[rute_INDEX] = kommando_START;
            호출(종초기화[종] - 1); if (!FEIL) starte_rute[rute_INDEX] = 종 + 1;
            return false;
        }
        종상태[종] = 2; return true;
    }
    static void 필드호출(int INDEX, int Kommando, int Køyr_2) {
        if (!sjekk_konstant(INDEX, 9)) return;
        int eigar_VALUE = time_namn_SMS(상가[INDEX]), Namn = Oppslagsverk_namn(konstant_SECOND_VALUE[INDEX]), format_VALUE = Oppslagsverk_TYPE(konstant_SECOND_VALUE[INDEX]);
        if (Word_SMS(eigar_VALUE, "java/lang/System") && (Word_SMS(Namn, "out") || Word_SMS(Namn, "err")) && Word_SMS(format_VALUE, "Ljava/io/PrintStream;") && Kommando == 178) { 넣기(-1, 2); return; }
        int 종 = 종찾기(eigar_VALUE); if (종 < 0 || FEIL) return;
        int 찾음 = -1;
        for (int 읽는자리 = 종, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = forelder_time(읽는자리))
            for (int fil_INDEX = 0; fil_INDEX < felt_COUNT; fil_INDEX++) if (felt_eigar[fil_INDEX] == 읽는자리 && 같은말(felt_namn[fil_INDEX], Namn) && 같은말(felt_TYPE[fil_INDEX], format_VALUE)) 찾음 = fil_INDEX;
        if (찾음 < 0) { feil_VALUE("NoSuchFieldError"); return; }
        boolean statisk_VALUE = Kommando == 178 || Kommando == 179;
        if (statisk_VALUE != ((felt_løyve[찾음] & 8) != 0)) { feil_VALUE("field static/instance mismatch"); return; }
        if (statisk_VALUE && !starte(felt_eigar[찾음], Køyr_2)) return;
        int TYPE_VALUE = 형종류(format_VALUE), VALUE = 0;
        if (Kommando == 179 || Kommando == 181) VALUE = 빼기(TYPE_VALUE);
        if (statisk_VALUE) { if (Kommando == 178) 넣기(felt_data[찾음], TYPE_VALUE); else if (!FEIL) felt_data[찾음] = VALUE; return; }
        int objekt_Oppslagsverk = 빼기(2);
        if (!객체유효(objekt_Oppslagsverk)) return;
        if (힙[objekt_Oppslagsverk] < 32 || !종포함(힙[objekt_Oppslagsverk] - 32, eigar_VALUE)) { feil_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = objekt_Oppslagsverk + 2 + felt_plassere[찾음];
        if (Kommando == 180) 넣기(힙[보관칸], TYPE_VALUE);
        else if (!FEIL) { 힙[보관칸] = VALUE; 힙참조[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int 종, int Namn) {
        for (int 중첩깊이 = 0; 종 >= 0 && 중첩깊이 < 16; 중첩깊이++, 종 = forelder_time(종)) {
            if (같은말(종이름[종], Namn) || (종부모[종] != 0 && 같은말(종부모[종], Namn))) return true;
            for (int indre_kopling_plassere = 0; indre_kopling_plassere < time_grensesnitt_COUNT[종]; indre_kopling_plassere++) if (같은말(time_grensesnitt[종 * 16 + indre_kopling_plassere], Namn)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int byte_data, boolean STIGE) {
        if (첫값 == byte_data) return true;
        if (첫값 <= 0 || byte_data <= 0 || 힙[첫값] != 1 || 힙[byte_data] != 1 || 힙[첫값 + 1] != 힙[byte_data + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) {
            int x_koordinat = 힙[첫값 + 2 + Loop_INDEX], Y_koordinat = 힙[byte_data + 2 + Loop_INDEX];
            if (STIGE) { if (x_koordinat == '.') x_koordinat = '/'; if (Y_koordinat == '.') Y_koordinat = '/'; }
            if (x_koordinat != Y_koordinat) return false;
        }
        return true;
    }
    static boolean 객체유효(int objekt_Oppslagsverk) {
        if (objekt_Oppslagsverk == 0) { feil_VALUE("NullPointerException"); return false; }
        if (objekt_Oppslagsverk < 1 || objekt_Oppslagsverk >= 힙끝 || 힙폭[objekt_Oppslagsverk] < 2 || 힙[objekt_Oppslagsverk] == 0) { feil_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void verne_VALUE(int objekt_Oppslagsverk) {
        if (objekt_Oppslagsverk > 0 && objekt_Oppslagsverk < 힙끝 && 힙폭[objekt_Oppslagsverk] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = objekt_Oppslagsverk;
    }
    static void vise_VALUE_487749b8(int objekt_Oppslagsverk) {
        if (objekt_Oppslagsverk > 0 && objekt_Oppslagsverk < 힙끝 && 힙폭[objekt_Oppslagsverk] >= 2 && 힙[objekt_Oppslagsverk] != 0 && 힙표시[objekt_Oppslagsverk] == 0) {
            힙표시[objekt_Oppslagsverk] = 1; 표시대기[vise_COUNT++] = objekt_Oppslagsverk;
        }
    }
    static void 수거() {
        vise_COUNT = 0; Samling_COUNT++;
        for (int sjekk_plassere = 1; sjekk_plassere < 힙끝; sjekk_plassere += 힙폭[sjekk_plassere]) 힙표시[sjekk_plassere] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < streng_Oppslagsverk.length; Loop_INDEX++) vise_VALUE_487749b8(streng_Oppslagsverk[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < felt_COUNT; Loop_INDEX++) if ((felt_løyve[Loop_INDEX] & 8) != 0 && 형종류(felt_TYPE[Loop_INDEX]) == 2) vise_VALUE_487749b8(felt_data[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < tråd_COUNT; 임시값++) {
            vise_VALUE_487749b8(tråd_objekt[임시값]); vise_VALUE_487749b8(tråd_mål[임시값]);
            int 꼭대기자리 = 임시값 == betalt_tråd ? rute_INDEX : tråd_rute[임시값];
            for (int fil_INDEX = 임시값 * 32; fil_INDEX <= 꼭대기자리; fil_INDEX++) {
                for (int indre_kopling_plassere = 0; indre_kopling_plassere < 함수지역[rute_metode[fil_INDEX]]; indre_kopling_plassere++) if (lokal_TYPE[fil_INDEX * 128 + indre_kopling_plassere] == 2) vise_VALUE_487749b8(lokal_VALUE[fil_INDEX * 128 + indre_kopling_plassere]);
                for (int indre_kopling_plassere = 0; indre_kopling_plassere < rute_Stabel[fil_INDEX]; indre_kopling_plassere++) if (스택형[fil_INDEX * 128 + indre_kopling_plassere] == 2) vise_VALUE_487749b8(스택값[fil_INDEX * 128 + indre_kopling_plassere]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) vise_VALUE_487749b8(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) vise_VALUE_487749b8(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_heiltal.length; Loop_INDEX++) vise_VALUE_487749b8(Store_heiltal[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 종수; Loop_INDEX++) vise_VALUE_487749b8(time_blokkere[Loop_INDEX]);
        for (int sjekk_plassere = 1; sjekk_plassere < 힙끝; sjekk_plassere += 힙폭[sjekk_plassere]) if (잠금깊이[sjekk_plassere] > 0) vise_VALUE_487749b8(sjekk_plassere);
        vise_VALUE_487749b8(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) vise_VALUE_487749b8(잠시참조[Loop_INDEX]);
        while (vise_COUNT > 0) {
            int objekt_Oppslagsverk = 표시대기[--vise_COUNT], kategori_CODE = 힙[objekt_Oppslagsverk];
            for (int Loop_INDEX = objekt_Oppslagsverk + 2; Loop_INDEX < objekt_Oppslagsverk + 힙폭[objekt_Oppslagsverk]; Loop_INDEX++) if (kategori_CODE == 3 || kategori_CODE == 4 || 힙참조[Loop_INDEX] != 0) vise_VALUE_487749b8(힙[Loop_INDEX]);
        }
        for (int sjekk_plassere = 1; sjekk_plassere < 힙끝; sjekk_plassere += 힙폭[sjekk_plassere]) if (힙표시[sjekk_plassere] == 0) 힙[sjekk_plassere] = 0;
        for (int sjekk_plassere = 1; sjekk_plassere < 힙끝; sjekk_plassere += 힙폭[sjekk_plassere]) if (힙[sjekk_plassere] == 0) {
            while (sjekk_plassere + 힙폭[sjekk_plassere] < 힙끝 && 힙[sjekk_plassere + 힙폭[sjekk_plassere]] == 0) { int Neste_plassere = sjekk_plassere + 힙폭[sjekk_plassere]; 힙폭[sjekk_plassere] += 힙폭[Neste_plassere]; 힙폭[Neste_plassere] = 0; }
            if (sjekk_plassere + 힙폭[sjekk_plassere] == 힙끝) { 힙끝 = sjekk_plassere; break; }
        }
    }
    static int 새기억(int 종류, int lengd_VALUE) {
        if (lengd_VALUE < 0) { feil_VALUE("NegativeArraySizeException"); return 0; }
        if (lengd_VALUE > 힙.length - 3) { feil_VALUE("object heap exhausted"); return 0; }
        int 필요수 = lengd_VALUE + 2, objekt_Oppslagsverk = 0;
        if (필요수 <= 힙.length - 힙끝) { objekt_Oppslagsverk = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { objekt_Oppslagsverk = 읽는자리; break; }
            if (objekt_Oppslagsverk != 0) {
                int 남은길이 = 힙폭[objekt_Oppslagsverk] - 필요수;
                if (남은길이 >= 2) { 힙폭[objekt_Oppslagsverk + 필요수] = 남은길이; 힙[objekt_Oppslagsverk + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { objekt_Oppslagsverk = 힙끝; 힙끝 += 필요수; }
        }
        if (objekt_Oppslagsverk == 0) { feil_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { 힙[objekt_Oppslagsverk + Loop_INDEX] = 0; 힙참조[objekt_Oppslagsverk + Loop_INDEX] = 0; 힙폭[objekt_Oppslagsverk + Loop_INDEX] = 0; }
        ARRAY_element[objekt_Oppslagsverk] = 0;
        힙폭[objekt_Oppslagsverk] = 필요수; 힙[objekt_Oppslagsverk] = 종류; 힙[objekt_Oppslagsverk + 1] = lengd_VALUE; verne_VALUE(objekt_Oppslagsverk); return objekt_Oppslagsverk;
    }
    static int unntak_time(String namn_konstant) {
        if (자바도구.같음(namn_konstant, "java/lang/Throwable")) return 1;
        if (자바도구.같음(namn_konstant, "java/lang/Exception")) return 2;
        if (자바도구.같음(namn_konstant, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(namn_konstant, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(namn_konstant, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(namn_konstant, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(namn_konstant, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(namn_konstant, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(namn_konstant, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(namn_konstant, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(namn_konstant, "java/io/IOException")) return 11;
        if (자바도구.같음(namn_konstant, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(namn_konstant, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(namn_konstant, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(namn_konstant, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int unntak_konstant(int Namn) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_SMS(Namn, unntak_namn(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String unntak_namn(int konto_VALUE) {
        if (konto_VALUE == 40) return "java/lang/InterruptedException";
        if (konto_VALUE == 41) return "한국어/자체/대기중단예외";
        if (konto_VALUE == 39) return "java/net/SocketException";
        if (konto_VALUE == 20) return "한국어/자체/unntak";
        if (konto_VALUE == 21) return "한국어/자체/실행예외";
        if (konto_VALUE == 22) return "한국어/자체/I_U_unntak";
        if (konto_VALUE == 23) return "한국어/자체/vent_TIMEOUT_unntak";
        if (konto_VALUE == 24) return "한국어/자체/ADDRESS_LOOKUP_unntak";
        if (konto_VALUE == 25) return "한국어/자체/파일없음예외";
        if (konto_VALUE == 26) return "한국어/자체/통신예외";
        if (konto_VALUE == 27) return "한국어/자체/ugyldig_argument_unntak";
        if (konto_VALUE == 28) return "한국어/자체/숫자형식예외";
        if (konto_VALUE == 29) return "한국어/자체/범위예외";
        if (konto_VALUE == 30) return "한국어/자체/배열범위예외";
        if (konto_VALUE == 31) return "한국어/자체/문자열범위예외";
        if (konto_VALUE == 32) return "한국어/자체/NULL_Oppslagsverk_unntak";
        if (konto_VALUE == 33) return "한국어/자체/산술예외";
        if (konto_VALUE == 34) return "한국어/자체/status_unntak";
        if (konto_VALUE == 35) return "한국어/자체/TYPE_strøyme_unntak";
        if (konto_VALUE == 36) return "한국어/자체/음수배열크기예외";
        if (konto_VALUE == 37) return "한국어/자체/ARRAY_Store_feil";
        if (konto_VALUE == 38) return "한국어/자체/tråd_status_unntak";
        if (konto_VALUE == 1) return "java/lang/Throwable"; if (konto_VALUE == 2) return "java/lang/Exception";
        if (konto_VALUE == 3) return "java/lang/RuntimeException"; if (konto_VALUE == 4) return "java/lang/ArithmeticException";
        if (konto_VALUE == 5) return "java/lang/NullPointerException"; if (konto_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (konto_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (konto_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (konto_VALUE == 9) return "java/lang/IllegalArgumentException"; if (konto_VALUE == 10) return "java/lang/NumberFormatException";
        if (konto_VALUE == 11) return "java/io/IOException"; if (konto_VALUE == 12) return "java/io/FileNotFoundException";
        if (konto_VALUE == 17) return "java/lang/ArrayStoreException";
        if (konto_VALUE == 18) return "java/net/UnknownHostException";
        if (konto_VALUE == 19) return "java/net/SocketTimeoutException";
        if (konto_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (konto_VALUE == 13) return "java/lang/IllegalStateException"; if (konto_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int unntak_forelder(int konto_VALUE) {
        if (konto_VALUE == 40) return 2;
        if (konto_VALUE == 41) return 40;
        if (konto_VALUE == 39) return 11;
        if (konto_VALUE == 1) return 0;
        if (konto_VALUE == 2) return 1;
        if (konto_VALUE == 3) return 2;
        if (konto_VALUE == 4) return 3;
        if (konto_VALUE == 5) return 3;
        if (konto_VALUE == 6) return 3;
        if (konto_VALUE == 7) return 6;
        if (konto_VALUE == 8) return 6;
        if (konto_VALUE == 9) return 3;
        if (konto_VALUE == 10) return 9;
        if (konto_VALUE == 11) return 2;
        if (konto_VALUE == 12) return 11;
        if (konto_VALUE == 13) return 3;
        if (konto_VALUE == 14) return 3;
        if (konto_VALUE == 15) return 3;
        if (konto_VALUE == 16) return 9;
        if (konto_VALUE == 17) return 3;
        if (konto_VALUE == 18) return 11;
        if (konto_VALUE == 19) return 11;
        if (konto_VALUE == 20) return 2;
        if (konto_VALUE == 21) return 3;
        if (konto_VALUE == 22) return 11;
        if (konto_VALUE == 23) return 22;
        if (konto_VALUE == 24) return 22;
        if (konto_VALUE == 25) return 22;
        if (konto_VALUE == 26) return 22;
        if (konto_VALUE == 27) return 9;
        if (konto_VALUE == 28) return 27;
        if (konto_VALUE == 29) return 6;
        if (konto_VALUE == 30) return 29;
        if (konto_VALUE == 31) return 29;
        if (konto_VALUE == 32) return 5;
        if (konto_VALUE == 33) return 4;
        if (konto_VALUE == 34) return 13;
        if (konto_VALUE == 35) return 14;
        if (konto_VALUE == 36) return 15;
        if (konto_VALUE == 37) return 17;
        if (konto_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int faktisk_VALUE, int 요구값) {
        for (int 깊이 = 0; faktisk_VALUE != 0 && 깊이 < 16; 깊이++, faktisk_VALUE = unntak_forelder(faktisk_VALUE))
            if (faktisk_VALUE == 요구값) return true;
        return false;
    }
    static void 예외던짐(int konto_VALUE, String Viktig_Oppslagsverk) {
        int objekt_Oppslagsverk = 새기억(9, 2); if (FEIL) return;
        힙[objekt_Oppslagsverk + 2] = konto_VALUE; 힙[objekt_Oppslagsverk + 3] = vert_teikn(Viktig_Oppslagsverk); 힙참조[objekt_Oppslagsverk + 3] = 1;
        던진객체 = objekt_Oppslagsverk; FEIL = true;
    }
    static boolean 맞는객체(int objekt_Oppslagsverk, int Namn) {
        if (objekt_Oppslagsverk == 0) return true;
        if (!객체유효(objekt_Oppslagsverk)) return false;
        int kategori_CODE = 힙[objekt_Oppslagsverk];
        if (Word_SMS(Namn, "java/lang/Object")) return true;
        if (kategori_CODE >= 32) return 종포함(kategori_CODE - 32, Namn);
        if (kategori_CODE == 9) { int mål_ADDRESS = unntak_konstant(Namn); return mål_ADDRESS != 0 && 예외포함(힙[objekt_Oppslagsverk + 2], mål_ADDRESS); }
        if (kategori_CODE == 1) return Word_SMS(Namn, "java/lang/String") || Word_SMS(Namn, "java/lang/CharSequence");
        if (kategori_CODE == 4) return Word_SMS(Namn, "java/lang/StringBuilder") || Word_SMS(Namn, "java/lang/CharSequence");
        if (kategori_CODE == 10) return Word_SMS(Namn, "java/util/ArrayList") || Word_SMS(Namn, "java/util/List");
        if (kategori_CODE == 11) return Word_SMS(Namn, "java/util/HashMap") || Word_SMS(Namn, "java/util/Map");
        if (kategori_CODE == 12) return Word_SMS(Namn, "java/lang/Integer") || Word_SMS(Namn, "java/lang/Number");
        if (kategori_CODE >= 24 && kategori_CODE <= 28 && 힙[objekt_Oppslagsverk + 13] != 0) return 한국어화면종(Namn) == kategori_CODE || Word_SMS(Namn, "한국어/자체/화면구성요소");
        if (kategori_CODE >= 24 && kategori_CODE <= 28) return (한국어화면종(Namn) == 0 && 화면종(Namn) == kategori_CODE) || Word_SMS(Namn, "java/awt/Component") || Word_SMS(Namn, "java/awt/Container") || Word_SMS(Namn, "javax/swing/JComponent");
        if (kategori_CODE == 29) return Word_SMS(Namn, 힙[objekt_Oppslagsverk + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (kategori_CODE == 30) return Word_SMS(Namn, "java/awt/FlowLayout") || Word_SMS(Namn, "java/awt/LayoutManager");
        if (kategori_CODE == 17) return Word_SMS(Namn, "java/net/Socket");
        if (kategori_CODE == 18) return Word_SMS(Namn, "java/net/ServerSocket");
        if (kategori_CODE == 19) return Word_SMS(Namn, 힙[objekt_Oppslagsverk + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (kategori_CODE == 14) return Word_SMS(Namn, "java/net/InetAddress");
        if (kategori_CODE == 15) return Word_SMS(Namn, "java/net/DatagramSocket");
        if (kategori_CODE == 16) return Word_SMS(Namn, "java/net/DatagramPacket");
        if (kategori_CODE == 13) return Word_SMS(Namn, 힙[objekt_Oppslagsverk + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (kategori_CODE == 2) return Word_SMS(Namn, "[I"); if (kategori_CODE == 20) return Word_SMS(Namn, "[B"); if (kategori_CODE == 21) return Word_SMS(Namn, "[Z");
        if (kategori_CODE == 22) return Word_SMS(Namn, "[C"); if (kategori_CODE == 23) return Word_SMS(Namn, "[S");
        if (kategori_CODE != 3) return false;
        if (Word_SMS(Namn, "[Ljava/lang/Object;")) return true;
        int komponent = ARRAY_element[objekt_Oppslagsverk];
        if (komponent == -1) return Word_SMS(Namn, "[Ljava/lang/String;") || Word_SMS(Namn, "[Ljava/lang/CharSequence;");
        if (komponent == 0) return false;
        if (배열종비교(komponent, Namn)) return true;
        if ((Word_SMS(komponent, "java/lang/String") || Word_SMS(komponent, "java/lang/StringBuilder")) && Word_SMS(Namn, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < 종수; Loop_INDEX++) if (같은말(종이름[Loop_INDEX], komponent)) {
            for (int teiknkode = Loop_INDEX, 중첩깊이 = 0; teiknkode >= 0 && 중첩깊이 < 16; 중첩깊이++, teiknkode = forelder_time(teiknkode)) {
                if (배열종비교(종부모[teiknkode], Namn)) return true;
                for (int indre_kopling_plassere = 0; indre_kopling_plassere < time_grensesnitt_COUNT[teiknkode]; indre_kopling_plassere++) if (배열종비교(time_grensesnitt[teiknkode * 16 + indre_kopling_plassere], Namn)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int namn_konstant, int 형식참조) {
        int sjekk_plassere = 상가[형식참조], oppføring_COUNT = konstant_SECOND_VALUE[형식참조];
        if (namn_konstant == 0 || oppføring_COUNT < 4 || Fil[sjekk_plassere] != '[' || Fil[sjekk_plassere + 1] != 'L' || Fil[sjekk_plassere + oppføring_COUNT - 1] != ';' || konstant_SECOND_VALUE[namn_konstant] != oppføring_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < oppføring_COUNT - 3; Loop_INDEX++) if (Fil[상가[namn_konstant] + Loop_INDEX] != Fil[sjekk_plassere + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void handtak_unntak() {
        if (던진객체 == 0) return;
        FEIL = false;
        while (rute_INDEX >= betalt_tråd * 32) {
            int fil_INDEX = rute_metode[rute_INDEX], 읽는자리 = rute_instruksjon[rute_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == fil_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                rute_plassere[rute_INDEX] = 잡기위치[Loop_INDEX]; rute_Stabel[rute_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (starte_rute[rute_INDEX] != 0) 종상태[starte_rute[rute_INDEX] - 1] = 3;
            if (rute_blokkere[rute_INDEX] != 0) { frigi_blokkere(rute_blokkere[rute_INDEX]); rute_blokkere[rute_INDEX] = 0; }
            rute_INDEX--;
        }
        brukar.Skriv("Uncaught ");
        if (힙[던진객체] == 9) { brukar.Skriv(unntak_namn(힙[던진객체 + 2])); brukar.Skriv(": "); skrive_SMS(힙[던진객체 + 3]); }
        else brukar.Skriv("user exception");
        brukar.skrive_teikn_VALUE(10); 던진객체 = 0; FEIL = true;
    }
    // 이 JVM의 스택 항목은 betalt_vare category-1(int/reference)만 허용한다.
    static void Stabel_instruksjon(int kommando_CODE) {
        int 첫값 = 빼기(0), 첫형식 = levere_tilbake_TYPE;
        if (kommando_CODE == 87) return;
        if (kommando_CODE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int byte_data = 빼기(0), SECOND_format = levere_tilbake_TYPE;
        if (kommando_CODE == 88) return;
        if (kommando_CODE == 90) { 넣기(첫값, 첫형식); 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (kommando_CODE == 92) { 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (kommando_CODE == 95) { 넣기(첫값, 첫형식); 넣기(byte_data, SECOND_format); return; }
        int teiknkode = 빼기(0), 셋째형식 = levere_tilbake_TYPE;
        if (kommando_CODE == 91) { 넣기(첫값, 첫형식); 넣기(teiknkode, 셋째형식); 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (kommando_CODE == 93) { 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); 넣기(teiknkode, 셋째형식); 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = levere_tilbake_TYPE;
        넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(teiknkode, 셋째형식); 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식);
    }
    static void 새객체(int namn_konstant, int 시작점) {
        int kategori_CODE = 0, 유효길이 = 0, unntak_Oppslagsverk = unntak_konstant(namn_konstant);
        if (Word_SMS(namn_konstant, "java/lang/StringBuilder")) { kategori_CODE = 4; 유효길이 = 1; }
        if (Word_SMS(namn_konstant, "java/io/FileInputStream")) { kategori_CODE = 5; 유효길이 = 2; }
        if (Word_SMS(namn_konstant, "java/io/FileOutputStream")) { kategori_CODE = 6; 유효길이 = 2; }
        if (unntak_Oppslagsverk != 0) { kategori_CODE = 9; 유효길이 = 2; }
        if (Word_SMS(namn_konstant, "java/util/ArrayList")) { kategori_CODE = 10; 유효길이 = 2; }
        if (Word_SMS(namn_konstant, "java/util/HashMap")) { kategori_CODE = 11; 유효길이 = 2; }
        if (Word_SMS(namn_konstant, "java/lang/Integer")) { kategori_CODE = 12; 유효길이 = 1; }
        if (Word_SMS(namn_konstant, "java/net/Socket")) { kategori_CODE = 17; 유효길이 = 5; }
        if (Word_SMS(namn_konstant, "java/net/ServerSocket")) { kategori_CODE = 18; 유효길이 = 5; }
        if (Word_SMS(namn_konstant, "java/net/DatagramSocket")) { kategori_CODE = 15; 유효길이 = 3; }
        if (Word_SMS(namn_konstant, "java/net/DatagramPacket")) { kategori_CODE = 16; 유효길이 = 4; }
        if (Word_SMS(namn_konstant, "java/lang/Thread") || Word_SMS(namn_konstant, "한국어/자체/작업가닥")) { kategori_CODE = 13; 유효길이 = 2; }
        if (Word_SMS(namn_konstant, "java/lang/Object")) { kategori_CODE = 8; }
        if (kategori_CODE == 0 && 화면종(namn_konstant) != 0) { kategori_CODE = 화면종(namn_konstant); 유효길이 = 12; }
        if (kategori_CODE == 0) {
            int teiknkode = 종찾기(namn_konstant); if (teiknkode < 0 || FEIL || !starte(teiknkode, 시작점)) return;
            kategori_CODE = 32 + teiknkode; 유효길이 = time_felt_COUNT[teiknkode];
        }
        int objekt_Oppslagsverk = tildele_Lagring(kategori_CODE, 유효길이); if (FEIL) return;
        if (kategori_CODE == 13 && Word_SMS(namn_konstant, "한국어/자체/작업가닥")) 힙[objekt_Oppslagsverk + 3] = 1;
        if (kategori_CODE >= 24 && kategori_CODE <= 28 && 한국어화면종(namn_konstant) != 0) 힙[objekt_Oppslagsverk + 13] = 1;
        if (kategori_CODE == 5 || kategori_CODE == 6 || kategori_CODE == 15 || kategori_CODE == 17 || kategori_CODE == 18) 힙[objekt_Oppslagsverk + 2] = -1;
        if (kategori_CODE == 9) 힙[objekt_Oppslagsverk + 2] = unntak_Oppslagsverk;
        넣기(objekt_Oppslagsverk, 2);
    }
    static boolean 값같음(int 첫값, int byte_data) {
        if (첫값 == byte_data) return true;
        if (첫값 == 0 || byte_data == 0 || 첫값 < 0 || byte_data < 0 || 첫값 >= 힙끝 || byte_data >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[byte_data] == 1) return 글같음(첫값, byte_data, false);
        return 힙[첫값] == 12 && 힙[byte_data] == 12 && 힙[첫값 + 2] == 힙[byte_data + 2];
    }
    static int 글조각(int objekt_Oppslagsverk, int START_plassere, int avslutte_plassere) {
        if (!objekt_VALUE(objekt_Oppslagsverk, 1)) return 0;
        if (START_plassere < 0 || avslutte_plassere < START_plassere || avslutte_plassere > 힙[objekt_Oppslagsverk + 1]) { feil_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = tildele_Lagring(1, avslutte_plassere - START_plassere); if (FEIL) return 0;
        for (int Loop_INDEX = START_plassere; Loop_INDEX < avslutte_plassere; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX - START_plassere] = 힙[objekt_Oppslagsverk + 2 + Loop_INDEX];
        return 반환값;
    }
    static int Bli_med_SMS(int 첫값, int byte_data) {
        if (!objekt_VALUE(첫값, 1) || !objekt_VALUE(byte_data, 1)) return 0;
        int oppføring_COUNT = 힙[첫값 + 1], metode_INDEX = 힙[byte_data + 1], 반환값 = tildele_Lagring(1, oppføring_COUNT + metode_INDEX); if (FEIL) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < oppføring_COUNT; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 힙[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < metode_INDEX; Loop_INDEX++) 힙[반환값 + 2 + oppføring_COUNT + Loop_INDEX] = 힙[byte_data + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int eigar, int namn_konstant, int 서술상수, int kommando_CODE) {
        if (Word_SMS(eigar, "한국어/자체/실행인수") && kommando_CODE == 184) {
            if (Word_SMS(namn_konstant, "vare_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(brukar.인수개수() - 1, 1); return true; }
            if (Word_SMS(namn_konstant, "Tekst") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= brukar.인수개수() - 1) 예외던짐(29, "Utfør_kommando Argument 범위를 벗어났습니다");
                else 넣기(vert_teikn(brukar.Argument(순번 + 1)), 2);
                return true;
            }
            feil_VALUE("지원하지 않는 한국어 Utfør_kommando Argument 호출"); return true;
        }
        if (Word_SMS(eigar, "한국어/자체/작업가닥")) { Prosess_tråd(namn_konstant, 서술상수, kommando_CODE, true); return true; }
        if (한국어화면소유(eigar)) { 한국어화면호출(eigar, namn_konstant, 서술상수, kommando_CODE); return true; }
        if (화면소유(eigar)) { 화면호출(eigar, namn_konstant, 서술상수, kommando_CODE); return true; }
        if (Word_SMS(eigar, "java/net/Socket") || Word_SMS(eigar, "java/net/ServerSocket") || Word_SMS(eigar, "java/io/InputStream") || Word_SMS(eigar, "java/io/OutputStream")) { 흐름호출(eigar, namn_konstant, 서술상수, kommando_CODE); return true; }
        if (Word_SMS(eigar, "한국어/자체/kjerne_VALUE") && kommando_CODE == 184) {
            if (Word_SMS(namn_konstant, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(brukar.화면너비(), 1); return true; }
            if (Word_SMS(namn_konstant, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(brukar.화면높이(), 1); return true; }
            if (Word_SMS(namn_konstant, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(brukar.밀리초(), 1); return true; }
            if (Word_SMS(namn_konstant, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(brukar.그림대기(), 1); return true; }
            if (Word_SMS(namn_konstant, "사각형") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinat = 빼기(1), x_koordinat = 빼기(1); 넣기(brukar.사각형(x_koordinat, Y_koordinat, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(eigar, "java/net/InetAddress") || Word_SMS(eigar, "java/net/DatagramPacket") || Word_SMS(eigar, "java/net/DatagramSocket")) { 통신호출(eigar, namn_konstant, 서술상수, kommando_CODE); return true; }
        if (Word_SMS(eigar, "java/lang/Thread")) { 가닥호출(namn_konstant, 서술상수, kommando_CODE); return true; }
        if (Word_SMS(eigar, "java/lang/Object")) {
            if (Word_SMS(namn_konstant, "<init>") && Word_SMS(서술상수, "()V") && kommando_CODE == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(namn_konstant, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_data = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == byte_data ? 1 : 0, 1); return true; }
        }
        if (unntak_konstant(eigar) != 0) {
            if (Word_SMS(namn_konstant, "<init>") && kommando_CODE == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int spørsmål = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objekt_Oppslagsverk = 빼기(2);
                if (objekt_VALUE(objekt_Oppslagsverk, 9)) { 힙[objekt_Oppslagsverk + 3] = spørsmål; 힙참조[objekt_Oppslagsverk + 3] = 1; } return true;
            }
            if ((Word_SMS(namn_konstant, "getMessage") || Word_SMS(namn_konstant, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objekt_Oppslagsverk = 빼기(2); if (objekt_VALUE(objekt_Oppslagsverk, 9)) 넣기(힙[objekt_Oppslagsverk + 3], 2); return true; }
        }
        if (Word_SMS(eigar, "java/lang/String")) {
            if (kommando_CODE == 182 && Word_SMS(namn_konstant, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int koding_namn = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), objekt_Oppslagsverk = 빼기(2);
                if (!objekt_VALUE(objekt_Oppslagsverk, 1)) return true;
                if (koding_namn != 0 && !글같음(koding_namn, vert_teikn("UTF-8"), false) && !글같음(koding_namn, vert_teikn("UTF8"), false) && !글같음(koding_namn, vert_teikn("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int oppføring_COUNT = 힙[objekt_Oppslagsverk + 1], 반환값 = tildele_Lagring(20, oppføring_COUNT * 3), 사용수 = 0; if (FEIL) return true;
                for (int indre_kopling_plassere = 0; indre_kopling_plassere < oppføring_COUNT; indre_kopling_plassere++) {
                    int teiknkode = 힙[objekt_Oppslagsverk + 2 + indre_kopling_plassere];
                    if (teiknkode >= 0xd800 && teiknkode <= 0xdbff && indre_kopling_plassere + 1 < oppføring_COUNT && 힙[objekt_Oppslagsverk + 3 + indre_kopling_plassere] >= 0xdc00 && 힙[objekt_Oppslagsverk + 3 + indre_kopling_plassere] <= 0xdfff) teiknkode = 0x10000 + ((teiknkode - 0xd800) << 10) + 힙[objekt_Oppslagsverk + 2 + ++indre_kopling_plassere] - 0xdc00;
                    else if (teiknkode >= 0xd800 && teiknkode <= 0xdfff) teiknkode = '?';
                    if (teiknkode < 128) 힙[반환값 + 2 + 사용수++] = teiknkode;
                    else { int byte_COUNT = teiknkode < 2048 ? 2 : teiknkode < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((byte_COUNT == 2 ? 192 : byte_COUNT == 3 ? 224 : 240) | teiknkode >> (6 * (byte_COUNT - 1))); for (int Samanlikning_plassere = byte_COUNT - 1; Samanlikning_plassere > 0; Samanlikning_plassere--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | teiknkode >> (6 * (Samanlikning_plassere - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (kommando_CODE == 184 && Word_SMS(namn_konstant, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(siffer_teikn(빼기(1)), 2); return true; }
            if (kommando_CODE != 182) return false;
            if (Word_SMS(namn_konstant, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_data = 빼기(2), 첫값 = 빼기(2); if (objekt_VALUE(첫값, 1)) 넣기(글같음(첫값, byte_data, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(namn_konstant, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (objekt_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(namn_konstant, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int avslutte_plassere = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (objekt_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? avslutte_plassere : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(namn_konstant, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int byte_data = 빼기(2), 첫값 = 빼기(2); 넣기(Bli_med_SMS(첫값, byte_data), 2); return true; }
            if (Word_SMS(namn_konstant, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), hash_VALUE = 0; if (objekt_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) hash_VALUE = hash_VALUE * 31 + 힙[첫값 + 2 + Loop_INDEX]; 넣기(hash_VALUE, 1); } return true; }
            if (Word_SMS(namn_konstant, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (objekt_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(eigar, "java/lang/Integer")) {
            if (kommando_CODE == 184 && Word_SMS(namn_konstant, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int data_VALUE = 빼기(1), objekt_Oppslagsverk = data_VALUE >= -128 && data_VALUE <= 127 ? Store_heiltal[data_VALUE + 128] : 0; if (objekt_Oppslagsverk == 0) { objekt_Oppslagsverk = tildele_Lagring(12, 1); if (!FEIL) { 힙[objekt_Oppslagsverk + 2] = data_VALUE; if (data_VALUE >= -128 && data_VALUE <= 127) Store_heiltal[data_VALUE + 128] = objekt_Oppslagsverk; } } 넣기(objekt_Oppslagsverk, 2); return true; }
            if (kommando_CODE == 183 && Word_SMS(namn_konstant, "<init>") && Word_SMS(서술상수, "(I)V")) { int data_VALUE = 빼기(1), objekt_Oppslagsverk = 빼기(2); if (objekt_VALUE(objekt_Oppslagsverk, 12)) 힙[objekt_Oppslagsverk + 2] = data_VALUE; return true; }
            if (kommando_CODE == 182 && Word_SMS(namn_konstant, "intValue") && Word_SMS(서술상수, "()I")) { int objekt_Oppslagsverk = 빼기(2); if (objekt_VALUE(objekt_Oppslagsverk, 12)) 넣기(힙[objekt_Oppslagsverk + 2], 1); return true; }
            if (kommando_CODE == 184 && Word_SMS(namn_konstant, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(siffer_teikn(빼기(1)), 2); return true; }
        }
        if (Word_SMS(eigar, "java/lang/Math") && kommando_CODE == 184) {
            if (Word_SMS(namn_konstant, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(namn_konstant, "min") || Word_SMS(namn_konstant, "max")) && Word_SMS(서술상수, "(II)I")) { int byte_data = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(namn_konstant, "min") ? (첫값 < byte_data ? 첫값 : byte_data) : (첫값 > byte_data ? 첫값 : byte_data), 1); return true; }
        }
        if (Word_SMS(eigar, "java/lang/System") && kommando_CODE == 184) {
            if (Word_SMS(namn_konstant, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(namn_konstant, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int oppføring_COUNT = 빼기(1), mål_VALUE_INDEX = 빼기(1), byte_data = 빼기(2), START_plassere = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(byte_data)) {
                    int kategori_CODE = 힙[첫값];
                    if (힙[byte_data] != kategori_CODE || (kategori_CODE != 2 && kategori_CODE != 3 && (kategori_CODE < 20 || kategori_CODE > 23))) feil_VALUE("arraycopy type mismatch");
                    else if (oppføring_COUNT < 0 || START_plassere < 0 || mål_VALUE_INDEX < 0 || START_plassere > 힙[첫값 + 1] - oppføring_COUNT || mål_VALUE_INDEX > 힙[byte_data + 1] - oppføring_COUNT) feil_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == byte_data && mål_VALUE_INDEX > START_plassere) { for (int Loop_INDEX = oppføring_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) 힙[byte_data + 2 + mål_VALUE_INDEX + Loop_INDEX] = 힙[첫값 + 2 + START_plassere + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < oppføring_COUNT && !FEIL; Loop_INDEX++) { int data_VALUE = 힙[첫값 + 2 + START_plassere + Loop_INDEX]; if (kategori_CODE != 3 || 배열저장가능(byte_data, data_VALUE)) 힙[byte_data + 2 + mål_VALUE_INDEX + Loop_INDEX] = data_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(eigar, "java/util/ArrayList") || Word_SMS(eigar, "java/util/List") || Word_SMS(eigar, "java/util/HashMap") || Word_SMS(eigar, "java/util/Map")) {
            모음호출(eigar, namn_konstant, 서술상수, kommando_CODE); return true;
        }
        return false;
    }
    static void 모음늘리기(int objekt_Oppslagsverk, int 필요수) {
        int 이전값 = 힙[objekt_Oppslagsverk + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int Neste_plassere = 용량값 < 8 ? 8 : 용량값 * 2; if (Neste_plassere < 필요수) Neste_plassere = 필요수;
        int data_ARRAY = tildele_Lagring(3, Neste_plassere); if (FEIL) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 용량값; Loop_INDEX++) 힙[data_ARRAY + 2 + Loop_INDEX] = 힙[이전값 + 2 + Loop_INDEX];
        힙[objekt_Oppslagsverk + 2] = data_ARRAY; 힙참조[objekt_Oppslagsverk + 2] = 1;
    }
    static void 모음호출(int eigar, int namn_konstant, int 서술상수, int kommando_CODE) {
        boolean 대응참조 = Word_SMS(eigar, "java/util/HashMap") || Word_SMS(eigar, "java/util/Map"); int kategori_CODE = 대응참조 ? 11 : 10;
        if (Word_SMS(namn_konstant, "<init>") && kommando_CODE == 183 && Word_SMS(서술상수, "()V")) { int objekt_Oppslagsverk = 빼기(2); if (objekt_VALUE(objekt_Oppslagsverk, kategori_CODE)) 모음늘리기(objekt_Oppslagsverk, 8); return; }
        if (kommando_CODE != 182 && kommando_CODE != 185) { feil_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(namn_konstant, "size") && Word_SMS(서술상수, "()I") || Word_SMS(namn_konstant, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int objekt_Oppslagsverk = 빼기(2); if (objekt_VALUE(objekt_Oppslagsverk, kategori_CODE)) 넣기(Word_SMS(namn_konstant, "size") ? 힙[objekt_Oppslagsverk + 3] : 힙[objekt_Oppslagsverk + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(namn_konstant, "clear") && Word_SMS(서술상수, "()V")) { int objekt_Oppslagsverk = 빼기(2); if (objekt_VALUE(objekt_Oppslagsverk, kategori_CODE)) { int data_ARRAY = 힙[objekt_Oppslagsverk + 2]; for (int Loop_INDEX = 0; Loop_INDEX < 힙[data_ARRAY + 1]; Loop_INDEX++) 힙[data_ARRAY + 2 + Loop_INDEX] = 0; 힙[objekt_Oppslagsverk + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(namn_konstant, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int data_VALUE = 빼기(2), objekt_Oppslagsverk = 빼기(2); if (!objekt_VALUE(objekt_Oppslagsverk, 10)) return;
            int oppføring_COUNT = 힙[objekt_Oppslagsverk + 3]; 모음늘리기(objekt_Oppslagsverk, oppføring_COUNT + 1); if (!FEIL) { 힙[힙[objekt_Oppslagsverk + 2] + 2 + oppføring_COUNT] = data_VALUE; 힙[objekt_Oppslagsverk + 3] = oppføring_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(namn_konstant, "get") || Word_SMS(namn_konstant, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(namn_konstant, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Word_SMS(namn_konstant, "set"); int data_VALUE = 지정여부 ? 빼기(2) : 0, oppføring_plassere = 빼기(1), objekt_Oppslagsverk = 빼기(2);
            if (!objekt_VALUE(objekt_Oppslagsverk, 10)) return;
            int oppføring_COUNT = 힙[objekt_Oppslagsverk + 3], data_ARRAY = 힙[objekt_Oppslagsverk + 2];
            if (oppføring_plassere < 0 || oppføring_plassere >= oppføring_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[data_ARRAY + 2 + oppføring_plassere];
            if (지정여부) 힙[data_ARRAY + 2 + oppføring_plassere] = data_VALUE;
            if (Word_SMS(namn_konstant, "remove")) { for (int Loop_INDEX = oppføring_plassere + 1; Loop_INDEX < oppføring_COUNT; Loop_INDEX++) 힙[data_ARRAY + 1 + Loop_INDEX] = 힙[data_ARRAY + 2 + Loop_INDEX]; 힙[data_ARRAY + 1 + oppføring_COUNT] = 0; 힙[objekt_Oppslagsverk + 3] = oppføring_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(namn_konstant, "get") || Word_SMS(namn_konstant, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(namn_konstant, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(namn_konstant, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(namn_konstant, "put"), fjerne = Word_SMS(namn_konstant, "remove");
            int data_VALUE = 넣기여부 ? 빼기(2) : 0, tast_Oppslagsverk = 빼기(2), objekt_Oppslagsverk = 빼기(2); if (!objekt_VALUE(objekt_Oppslagsverk, 11)) return;
            int oppføring_COUNT = 힙[objekt_Oppslagsverk + 3], data_ARRAY = 힙[objekt_Oppslagsverk + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < oppføring_COUNT; Loop_INDEX++) if (값같음(tast_Oppslagsverk, 힙[data_ARRAY + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[data_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(objekt_Oppslagsverk, (oppføring_COUNT + 1) * 2); data_ARRAY = 힙[objekt_Oppslagsverk + 2]; 찾은여부 = oppføring_COUNT; if (!FEIL) 힙[objekt_Oppslagsverk + 3] = oppføring_COUNT + 1; }
                if (!FEIL) { 힙[data_ARRAY + 2 + 2 * 찾은여부] = tast_Oppslagsverk; 힙[data_ARRAY + 3 + 2 * 찾은여부] = data_VALUE; }
            }
            if (fjerne && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < oppføring_COUNT; Loop_INDEX++) { 힙[data_ARRAY + 2 * Loop_INDEX] = 힙[data_ARRAY + 2 + 2 * Loop_INDEX]; 힙[data_ARRAY + 1 + 2 * Loop_INDEX] = 힙[data_ARRAY + 3 + 2 * Loop_INDEX]; } 힙[data_ARRAY + 2 * oppføring_COUNT] = 0; 힙[data_ARRAY + 1 + 2 * oppføring_COUNT] = 0; 힙[objekt_Oppslagsverk + 3] = oppføring_COUNT - 1; }
            if (Word_SMS(namn_konstant, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        feil_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int objekt_Oppslagsverk) {
        if (!객체유효(objekt_Oppslagsverk)) return false;
        if (잠금깊이[objekt_Oppslagsverk] != 0 && blokkere_eigar[objekt_Oppslagsverk] != betalt_tråd + 1) { 바꿈요청 = true; return false; }
        blokkere_eigar[objekt_Oppslagsverk] = betalt_tråd + 1; 잠금깊이[objekt_Oppslagsverk]++; return true;
    }
    static void frigi_blokkere(int objekt_Oppslagsverk) {
        if (!객체유효(objekt_Oppslagsverk)) return;
        if (잠금깊이[objekt_Oppslagsverk] == 0 || blokkere_eigar[objekt_Oppslagsverk] != betalt_tråd + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[objekt_Oppslagsverk] == 0) blokkere_eigar[objekt_Oppslagsverk] = 0;
    }
    static boolean byte_tråd() {
        tråd_rute[betalt_tråd] = rute_INDEX;
        if (rute_INDEX < betalt_tråd * 32) tråd_status[betalt_tråd] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < tråd_COUNT; Loop_INDEX++) if (tråd_status[Loop_INDEX] == 2 && tråd_status[가닥대기[Loop_INDEX]] == 3) tråd_status[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= tråd_COUNT; Loop_INDEX++) {
            int Neste_plassere = (betalt_tråd + Loop_INDEX) % tråd_COUNT;
            if (tråd_status[Neste_plassere] == 1) { betalt_tråd = Neste_plassere; rute_INDEX = tråd_rute[Neste_plassere]; 바꿈요청 = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < tråd_COUNT; Loop_INDEX++) if (tråd_status[Loop_INDEX] != 3) { feil_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int namn_konstant, int 서술상수, int kommando_CODE) { Prosess_tråd(namn_konstant, 서술상수, kommando_CODE, false); }
    static void Prosess_tråd(int namn_konstant, int 서술상수, int kommando_CODE, boolean 한국어) {
        if (kommando_CODE == 184 && Word_SMS(namn_konstant, 한국어 ? "YIELD_oppgåve" : "yield") && Word_SMS(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (kommando_CODE == 184 && Word_SMS(namn_konstant, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(tråd_objekt[betalt_tråd], 2); return; }
        if (kommando_CODE == 183 && Word_SMS(namn_konstant, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int mål_ADDRESS = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), objekt_Oppslagsverk = 빼기(2);
            if (!객체유효(objekt_Oppslagsverk)) return;
            if (힙[objekt_Oppslagsverk] == 13) { 힙[objekt_Oppslagsverk + 2] = mål_ADDRESS; 힙참조[objekt_Oppslagsverk + 2] = 1; }
            else if (mål_ADDRESS != 0) feil_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (kommando_CODE == 182 && (Word_SMS(namn_konstant, 한국어 ? "START_oppgåve" : "start") || Word_SMS(namn_konstant, 한국어 ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || kommando_CODE == 182 && Word_SMS(namn_konstant, 한국어 ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int objekt_Oppslagsverk = 빼기(2); if (!객체유효(objekt_Oppslagsverk)) return;
            int konto_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < tråd_COUNT; Loop_INDEX++) if (tråd_objekt[Loop_INDEX] == objekt_Oppslagsverk) konto_VALUE = Loop_INDEX;
            if (Word_SMS(namn_konstant, 한국어 ? "살아있는가" : "isAlive")) { 넣기(konto_VALUE >= 0 && tråd_status[konto_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(namn_konstant, 한국어 ? "기다리기" : "join")) { if (konto_VALUE >= 0 && tråd_status[konto_VALUE] != 3) { 가닥대기[betalt_tråd] = konto_VALUE; tråd_status[betalt_tråd] = 2; 바꿈요청 = true; } return; }
            if (konto_VALUE >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (tråd_COUNT == 4) { feil_VALUE("thread limit (4 including main)"); return; }
            int mål_ADDRESS = 힙[objekt_Oppslagsverk] == 13 ? 힙[objekt_Oppslagsverk + 2] : objekt_Oppslagsverk;
            int fil_INDEX = mål_ADDRESS > 0 && 힙[mål_ADDRESS] >= 32 ? namn_metode(힙[mål_ADDRESS] - 32, 한국어 ? "Køyr" : "run", "()V") : -1;
            if (mål_ADDRESS != 0 && fil_INDEX < 0) { feil_VALUE("Runnable.run required"); return; }
            konto_VALUE = tråd_COUNT++; tråd_objekt[konto_VALUE] = objekt_Oppslagsverk; tråd_mål[konto_VALUE] = mål_ADDRESS;
            int rute = konto_VALUE * 32; tråd_rute[konto_VALUE] = fil_INDEX < 0 ? rute - 1 : rute; tråd_status[konto_VALUE] = fil_INDEX < 0 ? 3 : 1;
            if (fil_INDEX >= 0) { rute_metode[rute] = fil_INDEX; rute_plassere[rute] = metode_START[fil_INDEX]; lokal_VALUE[rute * 128] = mål_ADDRESS; lokal_TYPE[rute * 128] = 2; }
            return;
        }
        feil_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], ADDRESS_SMS = new int[16];
    static int lokal_ADDRESS() { return ADDRESS_objekt(0x7f000001); }
    static int ADDRESS_objekt(int VALUE) { int objekt_Oppslagsverk = tildele_Lagring(14, 1); if (!FEIL) 힙[objekt_Oppslagsverk + 2] = VALUE; return objekt_Oppslagsverk; }
    static int 주소해독(int objekt_Oppslagsverk) {
        if (objekt_Oppslagsverk == 0 || 글같음(objekt_Oppslagsverk, vert_teikn("localhost"), false)) return 0x7f000001;
        if (!objekt_VALUE(objekt_Oppslagsverk, 1)) return 0;
        int data_VALUE = 0, 총수 = 0, ADDRESS_byte = 0, 자릿수 = 0, oppføring_COUNT = 힙[objekt_Oppslagsverk + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= oppføring_COUNT; Loop_INDEX++) {
            int teiknkode = Loop_INDEX == oppføring_COUNT ? '.' : 힙[objekt_Oppslagsverk + 2 + Loop_INDEX];
            if (teiknkode == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } data_VALUE = data_VALUE << 8 | ADDRESS_byte; 총수++; ADDRESS_byte = 자릿수 = 0; }
            else { if (teiknkode < '0' || teiknkode > '9' || ++자릿수 > 3 || (ADDRESS_byte = ADDRESS_byte * 10 + teiknkode - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return data_VALUE;
    }
    static int ADDRESS_teikn(int data_VALUE) {
        int oppføring_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int ADDRESS_byte = data_VALUE >>> 이동비트 & 255;
            if (ADDRESS_byte >= 100) ADDRESS_SMS[oppføring_COUNT++] = '0' + ADDRESS_byte / 100;
            if (ADDRESS_byte >= 10) ADDRESS_SMS[oppføring_COUNT++] = '0' + ADDRESS_byte / 10 % 10;
            ADDRESS_SMS[oppføring_COUNT++] = '0' + ADDRESS_byte % 10; if (이동비트 != 0) ADDRESS_SMS[oppføring_COUNT++] = '.';
        }
        int objekt_Oppslagsverk = tildele_Lagring(1, oppføring_COUNT); if (!FEIL) for (int Loop_INDEX = 0; Loop_INDEX < oppføring_COUNT; Loop_INDEX++) 힙[objekt_Oppslagsverk + 2 + Loop_INDEX] = ADDRESS_SMS[Loop_INDEX]; return objekt_Oppslagsverk;
    }
    static void 통신호출(int eigar, int namn_konstant, int 서술상수, int kommando_CODE) {
        if (Word_SMS(eigar, "java/net/InetAddress")) {
            if (kommando_CODE == 184 && Word_SMS(namn_konstant, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(lokal_ADDRESS(), 2); return; }
            if (kommando_CODE == 184 && Word_SMS(namn_konstant, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int data_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !FEIL) 넣기(ADDRESS_objekt(data_VALUE), 2); return;
            }
            if (kommando_CODE == 182 && Word_SMS(namn_konstant, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int objekt_Oppslagsverk = 빼기(2); if (objekt_VALUE(objekt_Oppslagsverk, 14)) 넣기(ADDRESS_teikn(힙[objekt_Oppslagsverk + 2]), 2); return; }
        }
        if (Word_SMS(eigar, "java/net/DatagramPacket")) {
            if (kommando_CODE == 183 && Word_SMS(namn_konstant, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean mål_VALUE_Oppslagsverk = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int portnummer = mål_VALUE_Oppslagsverk ? 빼기(1) : 0, ADDRESS_Oppslagsverk = mål_VALUE_Oppslagsverk ? 빼기(2) : 0;
                int oppføring_COUNT = 빼기(1), data_ARRAY = 빼기(2), objekt_Oppslagsverk = 빼기(2);
                if (!objekt_VALUE(objekt_Oppslagsverk, 16) || !objekt_VALUE(data_ARRAY, 20)) return;
                if (oppføring_COUNT < 0 || oppføring_COUNT > 힙[data_ARRAY + 1] || portnummer < 0 || portnummer > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (ADDRESS_Oppslagsverk != 0 && !objekt_VALUE(ADDRESS_Oppslagsverk, 14)) return;
                힙[objekt_Oppslagsverk + 2] = data_ARRAY; 힙참조[objekt_Oppslagsverk + 2] = 1; 힙[objekt_Oppslagsverk + 3] = oppføring_COUNT;
                힙[objekt_Oppslagsverk + 4] = ADDRESS_Oppslagsverk; 힙참조[objekt_Oppslagsverk + 4] = 1; 힙[objekt_Oppslagsverk + 5] = portnummer; return;
            }
            if (kommando_CODE == 182 && Word_SMS(namn_konstant, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int oppføring_COUNT = 빼기(1), objekt_Oppslagsverk = 빼기(2); if (!objekt_VALUE(objekt_Oppslagsverk, 16)) return;
                if (oppføring_COUNT < 0 || oppføring_COUNT > 힙[힙[objekt_Oppslagsverk + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[objekt_Oppslagsverk + 3] = oppføring_COUNT; return;
            }
            if (kommando_CODE == 182 && (Word_SMS(namn_konstant, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(namn_konstant, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(namn_konstant, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(namn_konstant, "getPort") && Word_SMS(서술상수, "()I"))) {
                int objekt_Oppslagsverk = 빼기(2); if (!objekt_VALUE(objekt_Oppslagsverk, 16)) return;
                int oppføring_plassere = Word_SMS(namn_konstant, "getData") ? 2 : Word_SMS(namn_konstant, "getLength") ? 3 : Word_SMS(namn_konstant, "getAddress") ? 4 : 5;
                넣기(힙[objekt_Oppslagsverk + oppføring_plassere], oppføring_plassere == 2 || oppføring_plassere == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(eigar, "java/net/DatagramSocket")) {
            if (kommando_CODE == 183 && Word_SMS(namn_konstant, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int portnummer = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), objekt_Oppslagsverk = 빼기(2); if (!objekt_VALUE(objekt_Oppslagsverk, 15)) return;
                if (portnummer < 0 || portnummer > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = brukar.opne_Nettverk(portnummer); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[objekt_Oppslagsverk + 2] = 열린파일번호; return;
            }
            if (kommando_CODE == 182 && Word_SMS(namn_konstant, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), objekt_Oppslagsverk = 빼기(2); if (!objekt_VALUE(objekt_Oppslagsverk, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objekt_Oppslagsverk + 3] = 밀리초값; return;
            }
            if (kommando_CODE == 182 && Word_SMS(namn_konstant, "getLocalPort") && Word_SMS(서술상수, "()I")) { int objekt_Oppslagsverk = 빼기(2); if (objekt_VALUE(objekt_Oppslagsverk, 15)) 넣기(힙[objekt_Oppslagsverk + 2] < 0 ? -1 : brukar.Nettverk_port(힙[objekt_Oppslagsverk + 2]), 1); return; }
            if (kommando_CODE == 182 && Word_SMS(namn_konstant, "isClosed") && Word_SMS(서술상수, "()Z")) { int objekt_Oppslagsverk = 빼기(2); if (objekt_VALUE(objekt_Oppslagsverk, 15)) 넣기(힙[objekt_Oppslagsverk + 2] < 0 ? 1 : 0, 1); return; }
            if (kommando_CODE == 182 && Word_SMS(namn_konstant, "close") && Word_SMS(서술상수, "()V")) { int objekt_Oppslagsverk = 빼기(2); if (objekt_VALUE(objekt_Oppslagsverk, 15) && 힙[objekt_Oppslagsverk + 2] >= 0) { brukar.파일서술자닫기(힙[objekt_Oppslagsverk + 2]); 힙[objekt_Oppslagsverk + 2] = -1; } return; }
            if (kommando_CODE == 182 && (Word_SMS(namn_konstant, "send") || Word_SMS(namn_konstant, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int pakke = 빼기(2), objekt_Oppslagsverk = 빼기(2); if (!objekt_VALUE(pakke, 16) || !objekt_VALUE(objekt_Oppslagsverk, 15)) return;
                int data_ARRAY = 힙[pakke + 2], 유효길이 = 힙[pakke + 3], 열린파일번호 = 힙[objekt_Oppslagsverk + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(namn_konstant, "send")) {
                    if (!objekt_VALUE(힙[pakke + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = 힙[data_ARRAY + 2 + Loop_INDEX];
                    if (brukar.sende_Nettverk(열린파일번호, 힙[힙[pakke + 4] + 2], 힙[pakke + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int oppføring_COUNT = brukar.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (oppføring_COUNT == -11) {
                        int gjeldande_klokkeslett = brukar.밀리초();
                        if (힙[objekt_Oppslagsverk + 4] == 0) 힙[objekt_Oppslagsverk + 4] = gjeldande_klokkeslett + 1;
                        if (힙[objekt_Oppslagsverk + 3] > 0 && gjeldande_klokkeslett - (힙[objekt_Oppslagsverk + 4] - 1) >= 힙[objekt_Oppslagsverk + 3]) { 힙[objekt_Oppslagsverk + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(objekt_Oppslagsverk, 2); 넣기(pakke, 2); rute_plassere[rute_INDEX] = rute_instruksjon[rute_INDEX]; 바꿈요청 = true; return;
                    }
                    힙[objekt_Oppslagsverk + 4] = 0;
                    if (oppføring_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < oppføring_COUNT; Loop_INDEX++) 힙[data_ARRAY + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    힙[pakke + 3] = oppføring_COUNT; 힙[pakke + 4] = ADDRESS_objekt(통신임시[513]); 힙참조[pakke + 4] = 1; 힙[pakke + 5] = 통신임시[512];
                }
                return;
            }
        }
        feil_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int objekt_Oppslagsverk) {
        int gjeldande_klokkeslett = brukar.밀리초();
        if (힙[objekt_Oppslagsverk + 5] == 0) 힙[objekt_Oppslagsverk + 5] = gjeldande_klokkeslett + 1;
        if (힙[objekt_Oppslagsverk + 3] > 0 && gjeldande_klokkeslett - (힙[objekt_Oppslagsverk + 5] - 1) >= 힙[objekt_Oppslagsverk + 3]) { 힙[objekt_Oppslagsverk + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        rute_plassere[rute_INDEX] = rute_instruksjon[rute_INDEX]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int eigar, int namn_konstant, int 서술상수, int kommando_CODE) {
        boolean 수신쪽 = Word_SMS(eigar, "java/net/ServerSocket"), Stream = Word_SMS(eigar, "java/io/InputStream") || Word_SMS(eigar, "java/io/OutputStream");
        if (!Stream && kommando_CODE == 183 && Word_SMS(namn_konstant, "<init>")) {
            boolean informasjonsteknologi_tom_status = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(informasjonsteknologi_tom_status || 수신쪽 && Word_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { feil_VALUE("unsupported socket constructor"); return; }
            int portnummer = informasjonsteknologi_tom_status ? 0 : 빼기(1), ADDRESS_Oppslagsverk = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, objekt_Oppslagsverk = 빼기(2);
            if (!objekt_VALUE(objekt_Oppslagsverk, 수신쪽 ? 18 : 17)) return;
            if (portnummer < 0 || portnummer > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !objekt_VALUE(ADDRESS_Oppslagsverk, 14)) return;
            int Nettverk_ADDRESS = 이름지정여부 ? 주소해독(ADDRESS_Oppslagsverk) : 주소지정여부 ? 힙[ADDRESS_Oppslagsverk + 2] : 0x7f000001;
            if (FEIL || 던진객체 != 0) return;
            int 열린파일번호 = brukar.Stream_styring(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = informasjonsteknologi_tom_status ? 0 : 수신쪽 ? brukar.Stream_styring(1, 열린파일번호, portnummer) : brukar.KOPLE_TIL_Stream(열린파일번호, Nettverk_ADDRESS, portnummer);
            if (처리값 < 0) { brukar.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[objekt_Oppslagsverk + 2] = 열린파일번호; 힙[objekt_Oppslagsverk + 4] = portnummer; 힙[objekt_Oppslagsverk + 6] = informasjonsteknologi_tom_status ? 0 : 1; return;
        }
        if (!Stream && Word_SMS(namn_konstant, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), objekt_Oppslagsverk = 빼기(2); if (!objekt_VALUE(objekt_Oppslagsverk, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[objekt_Oppslagsverk + 3] = 밀리초값; return; }
        if (!Stream && Word_SMS(namn_konstant, "close") && Word_SMS(서술상수, "()V")) { int objekt_Oppslagsverk = 빼기(2); if (objekt_VALUE(objekt_Oppslagsverk, 수신쪽 ? 18 : 17) && 힙[objekt_Oppslagsverk + 2] >= 0) { brukar.파일서술자닫기(힙[objekt_Oppslagsverk + 2]); 힙[objekt_Oppslagsverk + 2] = -1; } return; }
        if (!Stream && (Word_SMS(namn_konstant, "getLocalPort") || Word_SMS(namn_konstant, "getPort") || Word_SMS(namn_konstant, "isClosed") || Word_SMS(namn_konstant, "isConnected"))) {
            int objekt_Oppslagsverk = 빼기(2); if (!objekt_VALUE(objekt_Oppslagsverk, 수신쪽 ? 18 : 17)) return;
            넣기(Word_SMS(namn_konstant, "isClosed") ? 힙[objekt_Oppslagsverk + 2] < 0 ? 1 : 0 : Word_SMS(namn_konstant, "isConnected") ? 힙[objekt_Oppslagsverk + 6] : Word_SMS(namn_konstant, "getPort") ? 힙[objekt_Oppslagsverk + 4] : 힙[objekt_Oppslagsverk + 2] < 0 ? -1 : brukar.Stream_styring(4, 힙[objekt_Oppslagsverk + 2], 0), 1); return;
        }
        if (수신쪽 && Word_SMS(namn_konstant, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int objekt_Oppslagsverk = 빼기(2); if (!objekt_VALUE(objekt_Oppslagsverk, 18)) return; int 열린파일번호 = brukar.Stream_styring(3, 힙[objekt_Oppslagsverk + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(objekt_Oppslagsverk)) 넣기(objekt_Oppslagsverk, 2); return; }
            힙[objekt_Oppslagsverk + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = tildele_Lagring(17, 5); if (FEIL) { brukar.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = brukar.Stream_styring(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !Stream && ((Word_SMS(namn_konstant, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(namn_konstant, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int objekt_Oppslagsverk = 빼기(2); if (!objekt_VALUE(objekt_Oppslagsverk, 17)) return; if (힙[objekt_Oppslagsverk + 2] < 0 || 힙[objekt_Oppslagsverk + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = tildele_Lagring(19, 4); if (FEIL) return; 힙[반환값 + 2] = objekt_Oppslagsverk; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(namn_konstant, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Word_SMS(namn_konstant, "read"), informasjonsteknologi_skrive_operasjon = Word_SMS(namn_konstant, "write"), Blokker = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), informasjonsteknologi_SUBARRAY = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int oppføring_COUNT = informasjonsteknologi_SUBARRAY ? 빼기(1) : 0, 시작변위 = informasjonsteknologi_SUBARRAY ? 빼기(1) : 0, data_ARRAY = Blokker || informasjonsteknologi_SUBARRAY ? 빼기(2) : 0;
            int data_VALUE = informasjonsteknologi_skrive_operasjon && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, objekt_Oppslagsverk = 빼기(2);
            if (!objekt_VALUE(objekt_Oppslagsverk, 19)) return; int forelder_Oppslagsverk = 힙[objekt_Oppslagsverk + 2], 열린파일번호 = 힙[forelder_Oppslagsverk + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(namn_konstant, "close") && Word_SMS(서술상수, "()V")) { brukar.파일서술자닫기(열린파일번호); 힙[forelder_Oppslagsverk + 2] = -1; return; }
            if (Word_SMS(namn_konstant, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !informasjonsteknologi_skrive_operasjon) || 읽기여부 != (힙[objekt_Oppslagsverk + 3] == 0)) { feil_VALUE("unsupported stream operation"); return; }
            if (Blokker || informasjonsteknologi_SUBARRAY) { if (!objekt_VALUE(data_ARRAY, 20)) return; if (Blokker) oppføring_COUNT = 힙[data_ARRAY + 1]; if (시작변위 < 0 || oppføring_COUNT < 0 || 시작변위 > 힙[data_ARRAY + 1] - oppføring_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else oppføring_COUNT = 1;
            if (oppføring_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = informasjonsteknologi_skrive_operasjon ? 힙[objekt_Oppslagsverk + 4] : 0, 처리값 = 0;
            while (완료수 < oppføring_COUNT) {
                처리값 = 읽기여부 ? brukar.파일한바이트읽기(열린파일번호) : brukar.파일한바이트쓰기(열린파일번호, Blokker || informasjonsteknologi_SUBARRAY ? 힙[data_ARRAY + 2 + 시작변위 + 완료수] : data_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (Blokker || informasjonsteknologi_SUBARRAY)) 힙[data_ARRAY + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(Blokker || informasjonsteknologi_SUBARRAY)) break;
            }
            if (처리값 == -11 && (informasjonsteknologi_skrive_operasjon || 완료수 == 0)) {
                힙[objekt_Oppslagsverk + 4] = 완료수;
                if (흐름대기(forelder_Oppslagsverk)) { 넣기(objekt_Oppslagsverk, 2); if (Blokker || informasjonsteknologi_SUBARRAY) 넣기(data_ARRAY, 2); if (informasjonsteknologi_SUBARRAY) { 넣기(시작변위, 1); 넣기(oppføring_COUNT, 1); } if (informasjonsteknologi_skrive_operasjon && !(Blokker || informasjonsteknologi_SUBARRAY)) 넣기(data_VALUE, 1); } return;
            }
            힙[objekt_Oppslagsverk + 4] = 0; 힙[forelder_Oppslagsverk + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : Blokker || informasjonsteknologi_SUBARRAY ? 완료수 : 처리값, 1); return;
        }
        feil_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int namn_konstant) {
        if (Word_SMS(namn_konstant, "한국어/자체/vindauge")) return 24;
        if (Word_SMS(namn_konstant, "한국어/자체/Etikett")) return 26;
        if (Word_SMS(namn_konstant, "한국어/자체/knapp")) return 27;
        if (Word_SMS(namn_konstant, "한국어/자체/SMS_felt")) return 28;
        if (Word_SMS(namn_konstant, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int namn_konstant) {
        return 한국어화면종(namn_konstant) != 0 || Word_SMS(namn_konstant, "한국어/자체/화면구성요소") || Word_SMS(namn_konstant, "한국어/자체/hending_kø");
    }
    static int 화면종(int namn_konstant) {
        int 한국어종 = 한국어화면종(namn_konstant); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(namn_konstant, "javax/swing/JFrame")) return 24;
        if (Word_SMS(namn_konstant, "javax/swing/JPanel")) return 25;
        if (Word_SMS(namn_konstant, "javax/swing/JLabel")) return 26;
        if (Word_SMS(namn_konstant, "javax/swing/JButton")) return 27;
        if (Word_SMS(namn_konstant, "javax/swing/JTextField")) return 28;
        if (Word_SMS(namn_konstant, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(namn_konstant, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int namn_konstant) {
        return 화면종(namn_konstant) != 0 || Word_SMS(namn_konstant, "java/awt/Component") || Word_SMS(namn_konstant, "java/awt/Container") || Word_SMS(namn_konstant, "javax/swing/JComponent") || Word_SMS(namn_konstant, "javax/swing/AbstractButton") || Word_SMS(namn_konstant, "javax/swing/text/JTextComponent") || Word_SMS(namn_konstant, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int objekt_Oppslagsverk) { if (!객체유효(objekt_Oppslagsverk)) return false; if (힙[objekt_Oppslagsverk] < 24 || 힙[objekt_Oppslagsverk] > 28) { feil_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int objekt_Oppslagsverk, int SMS_Oppslagsverk) {
        if (SMS_Oppslagsverk != 0 && !objekt_VALUE(SMS_Oppslagsverk, 1)) return;
        int oppføring_COUNT = SMS_Oppslagsverk == 0 ? 0 : 힙[SMS_Oppslagsverk + 1]; if (oppføring_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < oppføring_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = 힙[SMS_Oppslagsverk + 2 + Loop_INDEX];
        if (brukar.화면글(힙[objekt_Oppslagsverk + 2], 화면글임시, oppføring_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[objekt_Oppslagsverk + 3] = SMS_Oppslagsverk; 힙참조[objekt_Oppslagsverk + 3] = 1;
    }
    static int 화면문자읽기(int objekt_Oppslagsverk) {
        int konto_VALUE = 힙[objekt_Oppslagsverk + 2], oppføring_COUNT = brukar.화면연결(8, konto_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (oppføring_COUNT < 0) { feil_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < oppføring_COUNT; Loop_INDEX++) { int 부호값 = brukar.화면연결(9, konto_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = tildele_Lagring(1, 사용수); if (!FEIL) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 kjerne_VALUE 화면 기능에 연결한다. Swing objekt_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int eigar, int namn_konstant, int 서술상수, int kommando_CODE) {
        if (Word_SMS(eigar, "한국어/자체/hending_kø")) {
            if (kommando_CODE == 184 && Word_SMS(namn_konstant, "나중에실행") && Word_SMS(서술상수, "(L한국어/자체/실행할일;)V")) {
                int oppgåve_handling = 빼기(2); if (!객체유효(oppgåve_handling)) return;
                if (나중수 == 8) { feil_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = oppgåve_handling; return;
            }
            if (kommando_CODE == 184 && Word_SMS(namn_konstant, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            feil_VALUE("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (Word_SMS(eigar, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!objekt_VALUE(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Word_SMS(namn_konstant, "hending_kjelde") && Word_SMS(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Word_SMS(namn_konstant, "kommando_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Word_SMS(namn_konstant, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else feil_VALUE("지원하지 않는 한국어 Handling 알림 호출"); return;
        }
        if (kommando_CODE == 183 && Word_SMS(namn_konstant, "<init>")) {
            int 종류 = 한국어화면종(eigar), 받이 = 0, 가로 = 0, vertikalvising_plassere = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (brukar.화면너비() - 폭) / 2; vertikalvising_plassere = (brukar.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); vertikalvising_plassere = 빼기(1); 가로 = 빼기(1);
            } else { feil_VALUE("지원하지 않는 한국어 화면 생성자"); return; }
            int Tekst = 빼기(2), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || vertikalvising_plassere < 0 || 폭 > brukar.화면너비() - 가로 || 높이 > brukar.화면높이() - vertikalvising_plassere) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = brukar.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { feil_VALUE("화면 element_VALUE 자리가 가득 찼습니다"); return; }
            힙[element_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = element_VALUE;
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = vertikalvising_plassere; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; 힙[element_VALUE + 10] = 2;
            힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1;
            brukar.화면연결(1, INDEX, 가로, vertikalvising_plassere, 폭, 높이);
            if (종류 == 24) brukar.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(element_VALUE, Tekst); return;
        }
        if (kommando_CODE != 182) { feil_VALUE("잘못된 한국어 화면 호출 Kommando"); return; }
        if (Word_SMS(namn_konstant, "skrive_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Tekst = 빼기(2), element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 화면문자설정(element_VALUE, Tekst); return;
        }
        if (Word_SMS(namn_konstant, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(화면문자읽기(element_VALUE), 2); return;
        }
        if (Word_SMS(namn_konstant, "동작맡기기") && Word_SMS(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), element_VALUE = 빼기(2);
            if (화면객체(element_VALUE)) { 힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(namn_konstant, "leggje_til_element") && Word_SMS(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int underordna_VALUE = 빼기(2), forelder_VALUE = 빼기(2); if (!화면객체(underordna_VALUE) || !화면객체(forelder_VALUE)) return;
            if (brukar.화면연결(2, 힙[forelder_VALUE + 2], 힙[underordna_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[underordna_VALUE + 11] = forelder_VALUE; 힙참조[underordna_VALUE + 11] = 1; return;
        }
        if (Word_SMS(namn_konstant, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), vertikalvising_plassere = 빼기(1), 가로 = 빼기(1), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (brukar.화면연결(1, 힙[element_VALUE + 2], 가로, vertikalvising_plassere, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = vertikalvising_plassere; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; return;
        }
        if ((Word_SMS(namn_konstant, "vise_vindauge") || Word_SMS(namn_konstant, "Lukk")) && Word_SMS(서술상수, "()V")) {
            boolean synlegheit_VALUE = Word_SMS(namn_konstant, "vise_vindauge"); int element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (brukar.화면연결(synlegheit_VALUE ? 3 : 4, 힙[element_VALUE + 2], synlegheit_VALUE ? 1 : 0, 0, 0, 0) < 0) { feil_VALUE("화면은 interaktiv 명령에서 실행해야 합니다"); return; }
            힙[element_VALUE + 9] = synlegheit_VALUE ? 1 : 0; return;
        }
        if (Word_SMS(namn_konstant, "보이는가") && Word_SMS(서술상수, "()Z")) { int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(힙[element_VALUE + 9], 1); return; }
        feil_VALUE("지원하지 않는 한국어 화면 metode_VALUE");
    }
    static void 화면호출(int eigar, int namn_konstant, int 서술상수, int kommando_CODE) {
        if (Word_SMS(eigar, "javax/swing/SwingUtilities")) {
            if (kommando_CODE == 184 && Word_SMS(namn_konstant, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int objekt_Oppslagsverk = 빼기(2); if (!객체유효(objekt_Oppslagsverk)) return; if (나중수 == 8) { feil_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = objekt_Oppslagsverk; return; }
            if (kommando_CODE == 184 && Word_SMS(namn_konstant, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            feil_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(eigar, "java/awt/event/ActionEvent")) {
            int objekt_Oppslagsverk = 빼기(2); if (!objekt_VALUE(objekt_Oppslagsverk, 29)) return;
            if (Word_SMS(namn_konstant, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[objekt_Oppslagsverk + 2], 2);
            else if (Word_SMS(namn_konstant, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[objekt_Oppslagsverk + 2]), 2);
            else if (Word_SMS(namn_konstant, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else feil_VALUE("unsupported ActionEvent method"); return;
        }
        if (kommando_CODE == 183 && Word_SMS(namn_konstant, "<init>")) {
            int COLUMNS = 0, SMS_Oppslagsverk = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_Oppslagsverk = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Oppslagsverk = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { feil_VALUE("unsupported Swing constructor"); return; }
            int objekt_Oppslagsverk = 빼기(2); if (!객체유효(objekt_Oppslagsverk)) return;
            if (힙[objekt_Oppslagsverk] == 30) { feil_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(objekt_Oppslagsverk) || COLUMNS < 0) return;
            int konto_VALUE = brukar.화면연결(0, 힙[objekt_Oppslagsverk] - 23, 0, 0, 0, 0);
            if (konto_VALUE < 1 || konto_VALUE > 32) { feil_VALUE("GUI widget slots exhausted"); return; }
            힙[objekt_Oppslagsverk + 2] = konto_VALUE; 화면참조[konto_VALUE - 1] = objekt_Oppslagsverk; 힙[objekt_Oppslagsverk + 5] = 힙[objekt_Oppslagsverk] == 24 ? 130 : 16; 힙[objekt_Oppslagsverk + 6] = 힙[objekt_Oppslagsverk] == 24 ? 110 : 16;
            힙[objekt_Oppslagsverk + 7] = 힙[objekt_Oppslagsverk] == 24 ? 380 : 220; 힙[objekt_Oppslagsverk + 8] = 힙[objekt_Oppslagsverk] == 24 ? 240 : 28; 힙[objekt_Oppslagsverk + 10] = 1;
            화면문자설정(objekt_Oppslagsverk, SMS_Oppslagsverk); return;
        }
        if (Word_SMS(namn_konstant, "setText") || Word_SMS(namn_konstant, "setTitle")) { int SMS_Oppslagsverk = 빼기(2), objekt_Oppslagsverk = 빼기(2); if (화면객체(objekt_Oppslagsverk) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(objekt_Oppslagsverk, SMS_Oppslagsverk); return; }
        if (Word_SMS(namn_konstant, "getText") || Word_SMS(namn_konstant, "getTitle")) { int objekt_Oppslagsverk = 빼기(2); if (화면객체(objekt_Oppslagsverk) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(objekt_Oppslagsverk), 2); return; }
        if (Word_SMS(namn_konstant, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), objekt_Oppslagsverk = 빼기(2); if (화면객체(objekt_Oppslagsverk)) { 힙[objekt_Oppslagsverk + 4] = 수신참조; 힙참조[objekt_Oppslagsverk + 4] = 1; } return; }
        if (Word_SMS(namn_konstant, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int objekt_Oppslagsverk = 빼기(2); if (화면객체(objekt_Oppslagsverk)) 넣기(objekt_Oppslagsverk, 2); return; }
        if (Word_SMS(namn_konstant, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Oppsett_Oppslagsverk = 빼기(2), objekt_Oppslagsverk = 빼기(2); if (화면객체(objekt_Oppslagsverk) && Oppsett_Oppslagsverk != 0) feil_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(namn_konstant, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Oppsett_tilstand = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Oppsett_tilstand) 빼기(2);
            int underordna_Oppslagsverk = 빼기(2), objekt_Oppslagsverk = 빼기(2); if (!화면객체(underordna_Oppslagsverk) || !화면객체(objekt_Oppslagsverk)) return;
            if (brukar.화면연결(2, 힙[objekt_Oppslagsverk + 2], 힙[underordna_Oppslagsverk + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[underordna_Oppslagsverk + 11] = objekt_Oppslagsverk; 힙참조[underordna_Oppslagsverk + 11] = 1; if (!Oppsett_tilstand) 넣기(underordna_Oppslagsverk, 2); return;
        }
        if (Word_SMS(namn_konstant, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Y_koordinat = 빼기(1), x_koordinat = 빼기(1), objekt_Oppslagsverk = 빼기(2); if (!화면객체(objekt_Oppslagsverk)) return;
            if (brukar.화면연결(1, 힙[objekt_Oppslagsverk + 2], x_koordinat, Y_koordinat, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[objekt_Oppslagsverk + 5] = x_koordinat; 힙[objekt_Oppslagsverk + 6] = Y_koordinat; 힙[objekt_Oppslagsverk + 7] = 너비; 힙[objekt_Oppslagsverk + 8] = 높이; return;
        }
        if (Word_SMS(namn_konstant, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), objekt_Oppslagsverk = 빼기(2); if (!화면객체(objekt_Oppslagsverk)) return;
            if (brukar.화면연결(1, 힙[objekt_Oppslagsverk + 2], 힙[objekt_Oppslagsverk + 5], 힙[objekt_Oppslagsverk + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[objekt_Oppslagsverk + 7] = 너비; 힙[objekt_Oppslagsverk + 8] = 높이; } return;
        }
        if (Word_SMS(namn_konstant, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), objekt_Oppslagsverk = 빼기(2); if (!화면객체(objekt_Oppslagsverk)) return; if (상대배치 != 0) { feil_VALUE("only screen centering supported"); return; } 힙[objekt_Oppslagsverk + 5] = (brukar.화면너비() - 힙[objekt_Oppslagsverk + 7]) / 2; 힙[objekt_Oppslagsverk + 6] = (brukar.화면높이() - 힙[objekt_Oppslagsverk + 8]) / 2; brukar.화면연결(1, 힙[objekt_Oppslagsverk + 2], 힙[objekt_Oppslagsverk + 5], 힙[objekt_Oppslagsverk + 6], 힙[objekt_Oppslagsverk + 7], 힙[objekt_Oppslagsverk + 8]); return; }
        if (Word_SMS(namn_konstant, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int policy = 빼기(1), objekt_Oppslagsverk = 빼기(2); if (화면객체(objekt_Oppslagsverk)) { if (policy < 0 || policy > 3) 예외던짐(9, "close policy"); else { 힙[objekt_Oppslagsverk + 10] = policy; brukar.화면연결(7, 힙[objekt_Oppslagsverk + 2], policy, 0, 0, 0); } } return; }
        if (Word_SMS(namn_konstant, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int data_VALUE = 빼기(1), objekt_Oppslagsverk = 빼기(2); if (화면객체(objekt_Oppslagsverk)) { int 처리값 = brukar.화면연결(3, 힙[objekt_Oppslagsverk + 2], data_VALUE, 0, 0, 0); if (처리값 < 0) feil_VALUE("Swing requires a standalone interactive command"); else 힙[objekt_Oppslagsverk + 9] = data_VALUE; } return; }
        if (Word_SMS(namn_konstant, "dispose") && Word_SMS(서술상수, "()V")) { int objekt_Oppslagsverk = 빼기(2); if (화면객체(objekt_Oppslagsverk)) { brukar.화면연결(4, 힙[objekt_Oppslagsverk + 2], 0, 0, 0, 0); 힙[objekt_Oppslagsverk + 9] = 0; } return; }
        if (Word_SMS(namn_konstant, "repaint") || Word_SMS(namn_konstant, "validate")) { int objekt_Oppslagsverk = 빼기(2); if (!화면객체(objekt_Oppslagsverk) || !Word_SMS(서술상수, "()V")) return; brukar.화면연결(1, 힙[objekt_Oppslagsverk + 2], 힙[objekt_Oppslagsverk + 5], 힙[objekt_Oppslagsverk + 6], 힙[objekt_Oppslagsverk + 7], 힙[objekt_Oppslagsverk + 8]); return; }
        if (Word_SMS(namn_konstant, "isVisible") && Word_SMS(서술상수, "()Z")) { int objekt_Oppslagsverk = 빼기(2); if (화면객체(objekt_Oppslagsverk)) 넣기(힙[objekt_Oppslagsverk + 9], 1); return; }
        feil_VALUE("unsupported Swing method (native subset)");
    }
    static void 사건실행(int mål_ADDRESS, int 사건번호, boolean 한국어) {
        if (mål_ADDRESS < 1 || 힙[mål_ADDRESS] < 32) { feil_VALUE("Java event listener required"); return; }
        int fil_INDEX = namn_metode(힙[mål_ADDRESS] - 32, 사건번호 == 0 ? (한국어 ? "Køyr" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (fil_INDEX < 0) { feil_VALUE("event callback missing"); return; }
        betalt_tråd = 0; tråd_COUNT = 1; rute_INDEX = 0; tråd_status[0] = 1; rute_Stabel[0] = 0; rute_blokkere[0] = starte_rute[0] = 0; 바꿈요청 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { lokal_VALUE[Loop_INDEX] = lokal_TYPE[Loop_INDEX] = 0; }
        rute_metode[0] = fil_INDEX; rute_plassere[0] = metode_START[fil_INDEX]; lokal_VALUE[0] = mål_ADDRESS; lokal_TYPE[0] = 2;
        if (사건번호 != 0) { lokal_VALUE[1] = 사건번호; lokal_TYPE[1] = 2; }
        사건중 = true; Utfør_kommando(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!FEIL) {
            if (나중수 > 0) { int mål_ADDRESS = 나중실행[0], 한국어 = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(mål_ADDRESS, 0, 한국어 != 0); continue; }
            if (brukar.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = brukar.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { feil_VALUE("GUI event I/O failed"); return; }
            int konto_VALUE = 사건번호 & 65535; if (konto_VALUE < 1 || konto_VALUE > 32) continue; int objekt_Oppslagsverk = 화면참조[konto_VALUE - 1]; if (objekt_Oppslagsverk == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[objekt_Oppslagsverk + 10] != 0) 힙[objekt_Oppslagsverk + 9] = 0;
                if (힙[objekt_Oppslagsverk + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && 힙[화면참조[Loop_INDEX]] == 24) brukar.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[objekt_Oppslagsverk + 4] != 0) {
                int Viktig_Oppslagsverk = tildele_Lagring(29, 2); if (FEIL) return; 힙[Viktig_Oppslagsverk + 2] = objekt_Oppslagsverk; 힙[Viktig_Oppslagsverk + 3] = 힙[objekt_Oppslagsverk + 12]; 힙참조[Viktig_Oppslagsverk + 2] = 1; 사건실행(힙[objekt_Oppslagsverk + 4], Viktig_Oppslagsverk, 힙[objekt_Oppslagsverk + 12] != 0);
            }
        }
    }
    public static int Køyr_2() {
        if (brukar.인수개수() == 1 && 자바도구.같음(brukar.Argument(0), "-version")) {
            brukar.Skriv("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (brukar.인수개수() < 1) { brukar.Skriv("Usage: java CLASS [ARGS]\n"); return 2; }
        시작종 = 종적재(vert_teikn(brukar.Argument(0))); if (FEIL || 시작종 < 0) return 1;
        int oppføring_p_VALUE = namn_metode(시작종, "Køyr_2", "()V");
        boolean 한국어진입 = oppføring_p_VALUE >= 0 && (metode_tilgang[oppføring_p_VALUE] & 9) == 9;
        if (!한국어진입) oppføring_p_VALUE = namn_metode(시작종, "main", "([Ljava/lang/String;)V");
        if (oppføring_p_VALUE < 0 || (metode_tilgang[oppføring_p_VALUE] & 9) != 9) feil_VALUE("public static void Køyr_2() or main(String[] args) required");
        if (FEIL) return 1;
        int Argument = tildele_Lagring(3, brukar.인수개수() - 1); ARRAY_element[Argument] = -1;
        for (int 수 = 1; 수 < brukar.인수개수() && !FEIL; 수++) 힙[Argument + 1 + 수] = vert_teikn(brukar.Argument(수));
        rute_INDEX = 0; rute_metode[0] = oppføring_p_VALUE; rute_plassere[0] = metode_START[oppføring_p_VALUE]; lokal_VALUE[0] = 한국어진입 ? 0 : Argument; lokal_TYPE[0] = 한국어진입 ? 0 : 2;
        tråd_status[0] = 1; tråd_objekt[0] = tildele_Lagring(13, 2);
        Utfør_kommando(); if (!FEIL) 화면사건들(); return FEIL ? 1 : 0;
    }
}
