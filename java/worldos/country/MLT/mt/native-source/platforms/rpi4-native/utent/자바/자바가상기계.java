// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. fajl/스택/Referenza/fergħa 경계를 eżegwixxa_kmand 중 검사한다. */
public final class 자바가상기계 {
    static int[] fajl = new int[16 * 16384], 임시파일 = new int[16384], fajl_isem_SMS = new int[512];
    static int[] valur_fiss_tag = new int[8192], 상가 = new int[8192], valur_fiss_SECOND_VALUE = new int[8192], string_Referenza = new int[8192];
    static int[] metodu_isem_SMS = new int[512], metodu_TYPE = new int[512], metodu_aċċess = new int[512], metodu_propjetarju = new int[512];
    static int[] metodu_Bidu = new int[512], metodu_ttermina = new int[512], metodu_Munzell = new int[512], 함수지역 = new int[512];
    static int[] metodu_argument_COUNT = new int[512], metodu_argument_TYPE = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] lokali_VALUE = new int[16384], lokali_TYPE = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] frejm_metodu = new int[128], frejm_pożizzjoni = new int[128], frejm_Munzell = new int[128], frejm_istruzzjoni = new int[128], inizjala_frejm = new int[128];
    static int[] klassi_Definizzjoni_isem = new int[16], klassi_Definizzjoni_daqqas = new int[16], 종부모 = new int[16], klassi_Definizzjoni_stat = new int[16], klassi_slott_COUNT = new int[16], inizjala_klassi_Definizzjoni = new int[16];
    static int[] klassi_interface = new int[16 * 16], klassi_interface_COUNT = new int[16];
    static int[] slott_isem = new int[512], slott_TYPE = new int[512], slott_propjetarju = new int[512], slott_permessi = new int[512], slott_pożizzjoni = new int[512], slott_data = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], ARRAY_element = new int[32768], Store_numru_sħiħ = new int[256];
    static int daqqas, 읽기위치, metodu_COUNT, klassi_isem, frejm_INDEX = -1, 힙끝 = 1, 반환형;
    static int klassi_Definizzjoni_COUNT, slott_COUNT, 잡기수, 현재읽는종, 던진객체, 잠시수, wera_COUNT, ġabra_COUNT;
    static int 현재가닥, fil_COUNT = 1, entrata_klassi_Definizzjoni;
    static int[] fil_frejm = new int[4], fil_stat = new int[4], fil_oġġett = new int[4], fil_mira = new int[4], 가닥대기 = new int[4];
    static boolean żball, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], klassi_fil = new int[16];

    static void żball_VALUE(String Word_SMS) {
        if (żball) return;
        int kategorija_CODE = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) kategorija_CODE = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) kategorija_CODE = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) kategorija_CODE = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) kategorija_CODE = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) kategorija_CODE = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) kategorija_CODE = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) kategorija_CODE = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) kategorija_CODE = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) kategorija_CODE = 15;
        if (kategorija_CODE != 0 && frejm_INDEX >= 0) { 예외던짐(kategorija_CODE, Word_SMS); return; }
        utent.kiteb("JVM error: "); utent.kiteb(Word_SMS); utent.kiteb_karattru_VALUE(10); żball = true;
    }
    static boolean klipp(int serje, int tul_VALUE) {
        if (serje < 0 || serje >= fajl.length || tul_VALUE < 0) return false;
        int klassi_Definizzjoni = serje / 16384;
        return serje % 16384 <= klassi_Definizzjoni_daqqas[klassi_Definizzjoni] && tul_VALUE <= klassi_Definizzjoni_daqqas[klassi_Definizzjoni] - serje % 16384;
    }
    static int byte_VALUE() {
        if (!klipp(읽기위치, 1)) { żball_VALUE("truncated class file"); return 0; }
        return fajl[읽기위치++];
    }
    static int 짧은수() { return byte_VALUE() << 8 | byte_VALUE(); }
    static int numru_sħiħ() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int tul_VALUE) { if (!klipp(읽기위치, tul_VALUE)) żball_VALUE("invalid attribute size"); else 읽기위치 += tul_VALUE; }
    static boolean ċekk_valur_fiss(int 수, int 종류) {
        if (수 <= 0 || 수 >= valur_fiss_tag.length || valur_fiss_tag[수] != 종류) { żball_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int serje, int tul_VALUE, String Word_SMS) {
        if (!klipp(serje, tul_VALUE)) return false;
        int 읽는자리 = serje, 끝 = serje + tul_VALUE;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_SMS.length(); Loop_INDEX++) {
            int kodiċi_tal_karattru = Word_SMS.charAt(Loop_INDEX);
            if (kodiċi_tal_karattru > 0 && kodiċi_tal_karattru < 128) { if (읽는자리 >= 끝 || fajl[읽는자리++] != kodiċi_tal_karattru) return false; }
            else if (kodiċi_tal_karattru < 2048) {
                if (읽는자리 + 2 > 끝 || fajl[읽는자리++] != (192 | (kodiċi_tal_karattru >> 6)) || fajl[읽는자리++] != (128 | (kodiċi_tal_karattru & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || fajl[읽는자리++] != (224 | (kodiċi_tal_karattru >> 12)) || fajl[읽는자리++] != (128 | ((kodiċi_tal_karattru >> 6) & 63)) || fajl[읽는자리++] != (128 | (kodiċi_tal_karattru & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Word_SMS(int valur_fiss_VALUE, String Word_SMS) { return ċekk_valur_fiss(valur_fiss_VALUE, 1) && 구간(상가[valur_fiss_VALUE], valur_fiss_SECOND_VALUE[valur_fiss_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!ċekk_valur_fiss(가, 1) || !ċekk_valur_fiss(나, 1) || valur_fiss_SECOND_VALUE[가] != valur_fiss_SECOND_VALUE[나]) return false;
        for (int 수 = 0; 수 < valur_fiss_SECOND_VALUE[가]; 수++) if (fajl[상가[가] + 수] != fajl[상가[나] + 수]) return false;
        return true;
    }
    static int klassi_isem_SMS(int 수) { return ċekk_valur_fiss(수, 7) && ċekk_valur_fiss(상가[수], 1) ? 상가[수] : 0; }
    static int Referenza_isem(int 수) { return ċekk_valur_fiss(수, 12) && ċekk_valur_fiss(상가[수], 1) ? 상가[수] : 0; }
    static int Referenza_TYPE(int 수) { return ċekk_valur_fiss(수, 12) && ċekk_valur_fiss(valur_fiss_SECOND_VALUE[수], 1) ? valur_fiss_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean vojt_TYPE) {
        if (읽기위치 >= 끝) { żball_VALUE("invalid descriptor"); return 0; }
        int VALUE = byte_VALUE();
        if (VALUE == 'V' && vojt_TYPE) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int serje = 읽기위치;
            while (읽기위치 < 끝 && fajl[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == serje) żball_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        żball_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_VALUE) {
        int 이전 = 읽기위치, 수 = metodu_TYPE[FUNCTION_VALUE];
        if (!ċekk_valur_fiss(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + valur_fiss_SECOND_VALUE[수];
        if (byte_VALUE() != '(') żball_VALUE("invalid method descriptor");
        int element_COUNT = 0;
        while (!żball && 읽기위치 < 끝 && fajl[읽기위치] != ')') {
            if (element_COUNT == 16) { żball_VALUE("too many method arguments"); break; }
            metodu_argument_TYPE[FUNCTION_VALUE * 16 + element_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || byte_VALUE() != ')') żball_VALUE("invalid method descriptor");
        함수반환[FUNCTION_VALUE] = 서술형(끝, true); metodu_argument_COUNT[FUNCTION_VALUE] = element_COUNT;
        if (읽기위치 != 끝) żball_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return metodu_propjetarju[frejm_metodu[frejm_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int element_COUNT = 짧은수();
        for (int 수 = 0; 수 < element_COUNT && !żball; 수++) { ċekk_valur_fiss(상번호(), 1); 건너(numru_sħiħ()); }
    }
    static int kmand_tul(int VALUE) {
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
    static int pożizzjoni_numru_sħiħ(int 읽는자리) {
        if (!klipp(읽는자리, 4)) { żball_VALUE("truncated bytecode operand"); return 0; }
        return fajl[읽는자리] << 24 | fajl[읽는자리 + 1] << 16 | fajl[읽는자리 + 2] << 8 | fajl[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int serje, int 끝) {
        int VALUE = fajl[읽는자리], tul_VALUE = kmand_tul(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_pożizzjoni = 읽는자리 + 1;
            while ((BASE_pożizzjoni - serje) % 4 != 0) BASE_pożizzjoni++;
            if (끝 - BASE_pożizzjoni < (VALUE == 170 ? 12 : 8)) return 0;
            int entrata_COUNT = VALUE == 170 ? pożizzjoni_numru_sħiħ(BASE_pożizzjoni + 8) - pożizzjoni_numru_sħiħ(BASE_pożizzjoni + 4) + 1 : pożizzjoni_numru_sħiħ(BASE_pożizzjoni + 4);
            if (entrata_COUNT < 0 || entrata_COUNT > 2048) return 0;
            tul_VALUE = BASE_pożizzjoni - 읽는자리 + (VALUE == 170 ? 12 + 4 * entrata_COUNT : 8 + 8 * entrata_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_data = fajl[읽는자리 + 1]; tul_VALUE = Word_data == 132 ? 6 : (Word_data == 21 || Word_data == 25 || Word_data == 54 || Word_data == 58) ? 4 : 0;
        }
        return tul_VALUE > 0 && tul_VALUE <= 끝 - 읽는자리 ? tul_VALUE : 0;
    }
    static void ċekk_destinazzjoni_VALUE(int destinazzjoni_VALUE, int FUNCTION_VALUE) {
        if (destinazzjoni_VALUE < metodu_Bidu[FUNCTION_VALUE] || destinazzjoni_VALUE >= metodu_ttermina[FUNCTION_VALUE] || 경계[destinazzjoni_VALUE] != FUNCTION_VALUE + 1) żball_VALUE("invalid branch target");
    }
    static void 클래스읽기(int klassi_Definizzjoni) {
        현재읽는종 = klassi_Definizzjoni; 읽기위치 = klassi_Definizzjoni * 16384; daqqas = 읽기위치 + klassi_Definizzjoni_daqqas[klassi_Definizzjoni];
        if (numru_sħiħ() != 0xcafebabe) { żball_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), verżjoni_VALUE = 짧은수();
        if (verżjoni_VALUE < 45 || verżjoni_VALUE > 52 || 부판 != 0) { żball_VALUE("supported class versions: 45..52, minor 0"); return; }
        int valur_fiss_COUNT = 짧은수(), BASE_pożizzjoni = klassi_Definizzjoni * 512;
        if (valur_fiss_COUNT < 1 || valur_fiss_COUNT > 512) { żball_VALUE("constant pool limit (511)"); return; }
        for (int entrata_COUNT = 1; entrata_COUNT < valur_fiss_COUNT && !żball; entrata_COUNT++) {
            int 수 = BASE_pożizzjoni + entrata_COUNT, 종류 = byte_VALUE(); valur_fiss_tag[수] = 종류;
            if (종류 == 1) { valur_fiss_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(valur_fiss_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = numru_sħiħ();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); valur_fiss_SECOND_VALUE[수] = 상번호(); }
            else żball_VALUE("unsupported constant type");
        }
        int permess_VALUE = 짧은수();
        if ((permess_VALUE & (0x2000 | 0x4000)) != 0) żball_VALUE("annotation/enum class unsupported");
        klassi_Definizzjoni_isem[klassi_Definizzjoni] = klassi_isem_SMS(상번호());
        종부모[klassi_Definizzjoni] = klassi_isem_SMS(상번호());
        int interface_COUNT = 짧은수(); if (interface_COUNT > 16) { żball_VALUE("interface count limit"); return; }
        klassi_interface_COUNT[klassi_Definizzjoni] = interface_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < interface_COUNT; Loop_INDEX++) klassi_interface[klassi_Definizzjoni * 16 + Loop_INDEX] = klassi_isem_SMS(상번호());
        int qasam_COUNT = 짧은수();
        if (qasam_COUNT > 512 - slott_COUNT) { żball_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < qasam_COUNT && !żball; Loop_INDEX++) {
            int fajl_INDEX = slott_COUNT++; slott_propjetarju[fajl_INDEX] = klassi_Definizzjoni; slott_permessi[fajl_INDEX] = 짧은수(); slott_isem[fajl_INDEX] = 상번호(); slott_TYPE[fajl_INDEX] = 상번호();
            ċekk_valur_fiss(slott_isem[fajl_INDEX], 1); ċekk_valur_fiss(slott_TYPE[fajl_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[slott_TYPE[fajl_INDEX]]; int kategorija_CODE = 서술형(읽기위치 + valur_fiss_SECOND_VALUE[slott_TYPE[fajl_INDEX]], false); 읽기위치 = 보존값;
            if ((slott_permessi[fajl_INDEX] & 8) == 0) slott_pożizzjoni[fajl_INDEX] = klassi_slott_COUNT[klassi_Definizzjoni]++;
            int attribut_data = 짧은수();
            for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < attribut_data && !żball; inner_join_pożizzjoni++) {
                int isem_valur_fiss = 상번호(), 유효길이 = numru_sħiħ();
                if (Word_SMS(isem_valur_fiss, "ConstantValue") && 유효길이 == 2) {
                    int data_VALUE = 상번호();
                    if (kategorija_CODE == 1 && ċekk_valur_fiss(data_VALUE, 3)) slott_data[fajl_INDEX] = 상가[data_VALUE];
                    else if (kategorija_CODE == 2 && ċekk_valur_fiss(data_VALUE, 8)) slott_data[fajl_INDEX] = valur_fiss_SMS(상가[data_VALUE]);
                } else 건너(유효길이);
            }
        }
        int element_COUNT = 짧은수();
        if (element_COUNT > 512 - metodu_COUNT) { żball_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < element_COUNT && !żball; Loop_INDEX++) {
            int 수 = metodu_COUNT++; metodu_propjetarju[수] = klassi_Definizzjoni;
            metodu_aċċess[수] = 짧은수(); metodu_isem_SMS[수] = 상번호(); metodu_TYPE[수] = 상번호();
            ċekk_valur_fiss(metodu_isem_SMS[수], 1); 서술읽기(수);
            if ((metodu_aċċess[수] & 8) == 0) {
                if (metodu_argument_COUNT[수] == 16) { żball_VALUE("too many instance method arguments"); return; }
                for (int 비교자리 = metodu_argument_COUNT[수]; 비교자리 > 0; 비교자리--) metodu_argument_TYPE[수 * 16 + 비교자리] = metodu_argument_TYPE[수 * 16 + 비교자리 - 1];
                metodu_argument_TYPE[수 * 16] = 2; metodu_argument_COUNT[수]++;
            }
            if ((metodu_aċċess[수] & 0x100) != 0) żball_VALUE("user native method unsupported");
            if (Word_SMS(metodu_isem_SMS[수], "<clinit>")) inizjala_klassi_Definizzjoni[klassi_Definizzjoni] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (metodu_propjetarju[앞] == klassi_Definizzjoni && 같은말(metodu_isem_SMS[앞], metodu_isem_SMS[수]) && 같은말(metodu_TYPE[앞], metodu_TYPE[수])) żball_VALUE("duplicate method");
            int attribut_COUNT = 짧은수();
            for (int attribut_VALUE = 0; attribut_VALUE < attribut_COUNT && !żball; attribut_VALUE++) {
                int isem = 상번호(), tul_VALUE = numru_sħiħ(), serje = 읽기위치;
                if (!klipp(serje, tul_VALUE)) { żball_VALUE("truncated method attribute"); break; }
                if (Word_SMS(isem, "Code")) {
                    if (metodu_Bidu[수] != 0) żball_VALUE("duplicate Code attribute");
                    metodu_Munzell[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_tul = numru_sħiħ();
                    if (metodu_Munzell[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < metodu_argument_COUNT[수]
                        || CODE_tul < 1 || CODE_tul > 8192) żball_VALUE("method memory limits exceeded");
                    metodu_Bidu[수] = 읽기위치; 건너(CODE_tul); metodu_ttermina[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { żball_VALUE("exception table limit"); return; }
                    for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < 잡는수; inner_join_pożizzjoni++) {
                        int żball_Referenza = 잡기수++; 잡기함수[żball_Referenza] = 수;
                        잡기시작[żball_Referenza] = metodu_Bidu[수] + 짧은수(); 잡기끝[żball_Referenza] = metodu_Bidu[수] + 짧은수();
                        잡기위치[żball_Referenza] = metodu_Bidu[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[żball_Referenza] = 부호값 == 0 ? 0 : klassi_isem_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != serje + tul_VALUE) żball_VALUE("Code attribute size mismatch");
                } else 건너(tul_VALUE);
            }
            if ((metodu_aċċess[수] & 0x400) != 0) continue;
            if (metodu_Bidu[수] == 0) żball_VALUE("missing Code attribute");
            int slott_entrata = metodu_Bidu[수];
            while (slott_entrata < metodu_ttermina[수] && !żball) {
                int tul_VALUE = 길이읽기(slott_entrata, metodu_Bidu[수], metodu_ttermina[수]);
                if (tul_VALUE == 0) { żball_VALUE("unsupported or truncated bytecode"); break; }
                경계[slott_entrata] = 수 + 1; slott_entrata += tul_VALUE;
            }
            slott_entrata = metodu_Bidu[수];
            while (slott_entrata < metodu_ttermina[수] && !żball) {
                int VALUE = fajl[slott_entrata];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) ċekk_destinazzjoni_VALUE(slott_entrata + (short)(fajl[slott_entrata + 1] << 8 | fajl[slott_entrata + 2]), 수);
                if (VALUE == 200) ċekk_destinazzjoni_VALUE(slott_entrata + pożizzjoni_numru_sħiħ(slott_entrata + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = slott_entrata + 1; while ((읽는자리 - metodu_Bidu[수]) % 4 != 0) 읽는자리++;
                    ċekk_destinazzjoni_VALUE(slott_entrata + pożizzjoni_numru_sħiħ(읽는자리), 수);
                    int entrata_COUNT = VALUE == 170 ? pożizzjoni_numru_sħiħ(읽는자리 + 8) - pożizzjoni_numru_sħiħ(읽는자리 + 4) + 1 : pożizzjoni_numru_sħiħ(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < entrata_COUNT; inner_join_pożizzjoni++) ċekk_destinazzjoni_VALUE(slott_entrata + pożizzjoni_numru_sħiħ(읽는자리 + inner_join_pożizzjoni * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                slott_entrata += 길이읽기(slott_entrata, metodu_Bidu[수], metodu_ttermina[수]);
            }
            for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < 잡기수; inner_join_pożizzjoni++) if (잡기함수[inner_join_pożizzjoni] == 수) {
                ċekk_destinazzjoni_VALUE(잡기시작[inner_join_pożizzjoni], 수); ċekk_destinazzjoni_VALUE(잡기위치[inner_join_pożizzjoni], 수);
                if (잡기끝[inner_join_pożizzjoni] != metodu_ttermina[수]) ċekk_destinazzjoni_VALUE(잡기끝[inner_join_pożizzjoni], 수);
                if (잡기시작[inner_join_pożizzjoni] >= 잡기끝[inner_join_pożizzjoni]) żball_VALUE("invalid exception range");
            }
        }
        if (!żball) 속성건너();
        if (읽기위치 != daqqas) żball_VALUE("extra class file data");
    }
    static int alloka_Ħażna(int 종류, int tul_VALUE) { return 새기억(종류, tul_VALUE); }
    static boolean oġġett_VALUE(int Referenza, int 종류) {
        if (!객체유효(Referenza)) return false;
        if (힙[Referenza] != 종류) { żball_VALUE("object type mismatch"); return false; }
        return true;
    }
    static int valur_fiss_SMS(int INDEX) {
        if (!ċekk_valur_fiss(INDEX, 1)) return 0;
        if (string_Referenza[INDEX] != 0) return string_Referenza[INDEX];
        int Referenza = alloka_Ħażna(1, valur_fiss_SECOND_VALUE[INDEX]); if (żball) return 0;
        int 끝 = 상가[INDEX] + valur_fiss_SECOND_VALUE[INDEX], 수 = 상가[INDEX], tul_VALUE = 0;
        while (수 < 끝 && !żball) {
            int VALUE = fajl[수++];
            if (VALUE == 0) żball_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Li_Jmiss_element = fajl[수++];
                if ((Li_Jmiss_element & 192) != 128) żball_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Li_Jmiss_element & 63;
                if (VALUE != 0 && VALUE < 128) żball_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = fajl[수++], 나 = fajl[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) żball_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (VALUE < 2048) żball_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) żball_VALUE("invalid modified UTF-8");
            힙[Referenza + 2 + tul_VALUE++] = VALUE;
        }
        힙[Referenza + 1] = tul_VALUE; string_Referenza[INDEX] = Referenza; return Referenza;
    }
    static int host_karattru(String VALUE) {
        int Referenza = alloka_Ħażna(1, VALUE.length()); if (żball) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) 힙[Referenza + 2 + 수] = VALUE.charAt(수);
        return Referenza;
    }
    static void kiteb_SMS(int Referenza) {
        if (Referenza == 0) { utent.kiteb("null"); return; }
        if (!oġġett_VALUE(Referenza, 1)) return;
        for (int 수 = 0; 수 < 힙[Referenza + 1]; 수++) utent.kiteb_karattru_VALUE(힙[Referenza + 2 + 수]);
    }
    static int ċifra_karattru(int VALUE) {
        int Referenza = alloka_Ħażna(1, 11); if (żball) return 0;
        int tul_VALUE = 0;
        if (VALUE < 0) 힙[Referenza + 2 + tul_VALUE++] = '-'; else VALUE = -VALUE;
        int pożizzjoni_INDEX = 1000000000; boolean serje = false;
        while (pożizzjoni_INDEX != 0) {
            int 수 = -(VALUE / pożizzjoni_INDEX);
            if (수 != 0 || serje || pożizzjoni_INDEX == 1) { 힙[Referenza + 2 + tul_VALUE++] = '0' + 수; serje = true; }
            VALUE %= pożizzjoni_INDEX; pożizzjoni_INDEX /= 10;
        }
        힙[Referenza + 1] = tul_VALUE; return Referenza;
    }
    static int 정수해독(int Referenza) {
        if (!oġġett_VALUE(Referenza, 1)) return 0;
        int tul_VALUE = 힙[Referenza + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (tul_VALUE > 0 && (힙[Referenza + 2] == '-' || 힙[Referenza + 2] == '+')) { 음수 = 힙[Referenza + 2] == '-'; 수++; }
        if (수 == tul_VALUE) żball_VALUE("NumberFormatException");
        for (; 수 < tul_VALUE && !żball; 수++) {
            int ċifra_VALUE = 힙[Referenza + 2 + 수] - '0';
            if (ċifra_VALUE < 0 || ċifra_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && ċifra_VALUE > (음수 ? 8 : 7)) żball_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - ċifra_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (żball) return;
        if (frejm_INDEX < 0 || frejm_Munzell[frejm_INDEX] >= metodu_Munzell[frejm_metodu[frejm_INDEX]]) { żball_VALUE("operand stack overflow"); return; }
        int slott_entrata = frejm_INDEX * 128 + frejm_Munzell[frejm_INDEX]++; 스택값[slott_entrata] = VALUE; 스택형[slott_entrata] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (żball) return 0;
        if (frejm_INDEX < 0 || frejm_Munzell[frejm_INDEX] < 1) { żball_VALUE("operand stack underflow"); return 0; }
        int slott_entrata = frejm_INDEX * 128 + --frejm_Munzell[frejm_INDEX]; 반환형 = 스택형[slott_entrata];
        if (TYPE_VALUE != 0 && 반환형 != TYPE_VALUE) żball_VALUE("operand type mismatch");
        if (반환형 == 2) pproteġa_VALUE(스택값[slott_entrata]);
        return 스택값[slott_entrata];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[frejm_metodu[frejm_INDEX]] || INDEX < 0 || lokali_TYPE[frejm_INDEX * 128 + INDEX] != TYPE_VALUE) { żball_VALUE("invalid or uninitialized local"); return; }
        넣기(lokali_VALUE[frejm_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void kiteb_lokali(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[frejm_metodu[frejm_INDEX]] || INDEX < 0) { żball_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); lokali_VALUE[frejm_INDEX * 128 + INDEX] = VALUE; lokali_TYPE[frejm_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int pożizzjoni = frejm_pożizzjoni[frejm_INDEX];
        if (pożizzjoni < metodu_Bidu[frejm_metodu[frejm_INDEX]] || pożizzjoni >= metodu_ttermina[frejm_metodu[frejm_INDEX]]) { żball_VALUE("instruction pointer out of range"); return 0; }
        frejm_pożizzjoni[frejm_INDEX]++; return fajl[pożizzjoni];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void mexxi_VALUE(int pożizzjoni) {
        int FUNCTION_VALUE = frejm_metodu[frejm_INDEX];
        if (pożizzjoni < metodu_Bidu[FUNCTION_VALUE] || pożizzjoni >= metodu_ttermina[FUNCTION_VALUE] || 경계[pożizzjoni] != FUNCTION_VALUE + 1) żball_VALUE("invalid branch target");
        else frejm_pożizzjoni[frejm_INDEX] = pożizzjoni;
    }
    static void 호출(int FUNCTION_VALUE) {
        if (frejm_INDEX % 32 == 31) { żball_VALUE("call stack limit (32)"); return; }
        int Li_Jmiss_element = frejm_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lokali_TYPE[Li_Jmiss_element * 128 + 수] = 0;
        for (int 수 = metodu_argument_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            lokali_VALUE[Li_Jmiss_element * 128 + 수] = 빼기(metodu_argument_TYPE[FUNCTION_VALUE * 16 + 수]); lokali_TYPE[Li_Jmiss_element * 128 + 수] = metodu_argument_TYPE[FUNCTION_VALUE * 16 + 수];
        }
        if (żball) return;
        frejm_INDEX = Li_Jmiss_element; inizjala_frejm[frejm_INDEX] = 0; frejm_metodu[frejm_INDEX] = FUNCTION_VALUE; frejm_pożizzjoni[frejm_INDEX] = metodu_Bidu[FUNCTION_VALUE]; frejm_Munzell[frejm_INDEX] = 0;
    }
    static void 반환(int TYPE_VALUE) {
        if (TYPE_VALUE != 함수반환[frejm_metodu[frejm_INDEX]]) { żball_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (inizjala_frejm[frejm_INDEX] != 0) klassi_Definizzjoni_stat[inizjala_frejm[frejm_INDEX] - 1] = 2;
        if (틀잠금[frejm_INDEX] != 0) { 잠금풀기(틀잠금[frejm_INDEX]); 틀잠금[frejm_INDEX] = 0; }
        frejm_INDEX--; if (frejm_INDEX >= 현재가닥 * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] Stream_fajl_isem = new int[64];
    static void fajl_Stream_CALL(int propjetarju_VALUE, int isem, int format_VALUE, int kmand) {
        boolean 출력 = Word_SMS(propjetarju_VALUE, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (kmand == 183 && Word_SMS(isem, "<init>")) {
            boolean 이어 = false;
            if (출력 && Word_SMS(format_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { żball_VALUE("unsupported file stream constructor"); return; }
            int fajl_entrata_isem = 빼기(2), Stream_VALUE = 빼기(2);
            if (!oġġett_VALUE(fajl_entrata_isem, 1) || !oġġett_VALUE(Stream_VALUE, 종류) || żball) return;
            if (힙[Stream_VALUE + 3] != 0) { żball_VALUE("file stream already initialized"); return; }
            int tul_VALUE = 힙[fajl_entrata_isem + 1];
            if (tul_VALUE < 1 || tul_VALUE > 63) { żball_VALUE("invalid file name length"); return; }
            for (int slott_entrata = 0; slott_entrata < tul_VALUE; slott_entrata++) {
                int VALUE = 힙[fajl_entrata_isem + 2 + slott_entrata];
                if (VALUE < 1) { żball_VALUE("invalid file stream path"); return; }
                Stream_fajl_isem[slott_entrata] = VALUE;
            }
            Stream_fajl_isem[tul_VALUE] = 0;
            int 서술자 = utent.파일서술자열기(Stream_fajl_isem, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { żball_VALUE("FileNotFoundException: file open failed"); return; }
            힙[Stream_VALUE + 2] = 서술자; 힙[Stream_VALUE + 3] = 1;
            return;
        }
        if (kmand != 182) { żball_VALUE("invalid file stream invocation"); return; }
        if ((출력 && Word_SMS(isem, "write") || !출력 && Word_SMS(isem, "read"))
            && (Word_SMS(format_VALUE, 출력 ? "([B)V" : "([B)I") || Word_SMS(format_VALUE, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean klipp_VALUE = Word_SMS(format_VALUE, 출력 ? "([BII)V" : "([BII)I");
            int entrata_COUNT = klipp_VALUE ? 빼기(1) : 0, 시작점 = klipp_VALUE ? 빼기(1) : 0, data_ARRAY = 빼기(2), oġġett_Referenza = 빼기(2);
            if (!oġġett_VALUE(data_ARRAY, 20) || !oġġett_VALUE(oġġett_Referenza, 종류)) return;
            if (!klipp_VALUE) entrata_COUNT = 힙[data_ARRAY + 1];
            if (시작점 < 0 || entrata_COUNT < 0 || 시작점 > 힙[data_ARRAY + 1] - entrata_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[oġġett_Referenza + 3] == 0 || 힙[oġġett_Referenza + 2] < 0) { żball_VALUE("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < entrata_COUNT && !żball) {
                int 반환값 = 출력 ? utent.파일한바이트쓰기(힙[oġġett_Referenza + 2], 힙[data_ARRAY + 2 + 시작점 + 완료수]) : utent.파일한바이트읽기(힙[oġġett_Referenza + 2]);
                if (반환값 < 0) { żball_VALUE(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[data_ARRAY + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(entrata_COUNT != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Word_SMS(isem, "flush") && Word_SMS(format_VALUE, "()V")) { int oġġett_Referenza = 빼기(2); if (oġġett_VALUE(oġġett_Referenza, 종류) && 힙[oġġett_Referenza + 2] < 0) żball_VALUE("IOException: stream closed"); return; }
        int azzjoni = -1, VALUE = 0;
        if (Word_SMS(isem, "close") && Word_SMS(format_VALUE, "()V")) azzjoni = 0;
        if (!출력 && Word_SMS(isem, "read") && Word_SMS(format_VALUE, "()I")) azzjoni = 1;
        if (출력 && Word_SMS(isem, "write") && Word_SMS(format_VALUE, "(I)V")) { azzjoni = 2; VALUE = 빼기(1); }
        if (azzjoni < 0) { żball_VALUE("unsupported file stream method"); return; }
        int Stream_VALUE = 빼기(2);
        if (!oġġett_VALUE(Stream_VALUE, 종류) || żball) return;
        if (힙[Stream_VALUE + 3] == 0) { żball_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_VALUE + 2];
        if (azzjoni == 0) {
            if (서술자 >= 0 && utent.파일서술자닫기(서술자) < 0) żball_VALUE("IOException: close failed");
            힙[Stream_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { żball_VALUE("IOException: stream closed"); return; }
        if (azzjoni == 1) {
            int miżura = utent.파일한바이트읽기(서술자);
            if (miżura < -1) żball_VALUE("IOException: read failed"); else 넣기(miżura == 256 ? -1 : miżura, 1);
        } else if (utent.파일한바이트쓰기(서술자, VALUE) != 1) żball_VALUE("IOException: write failed");
    }
    static void CALL_metodu(int INDEX, int kmand) {
        if (INDEX <= 0 || INDEX >= valur_fiss_tag.length || (valur_fiss_tag[INDEX] != 10 && valur_fiss_tag[INDEX] != 11)) { żball_VALUE("invalid method reference"); return; }
        int propjetarju_VALUE = klassi_isem_SMS(상가[INDEX]), isem = Referenza_isem(valur_fiss_SECOND_VALUE[INDEX]), format_VALUE = Referenza_TYPE(valur_fiss_SECOND_VALUE[INDEX]);
        if (żball) return;
        if (기본호출(propjetarju_VALUE, isem, format_VALUE, kmand)) return;
        if (Word_SMS(propjetarju_VALUE, "java/io/FileInputStream") || Word_SMS(propjetarju_VALUE, "java/io/FileOutputStream")) {
            fajl_Stream_CALL(propjetarju_VALUE, isem, format_VALUE, kmand); return;
        }
        if (kmand == 184 && Word_SMS(propjetarju_VALUE, "java/lang/Integer") && Word_SMS(isem, "parseInt") && Word_SMS(format_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (kmand == 182 && Word_SMS(propjetarju_VALUE, "java/io/PrintStream") && (Word_SMS(isem, "println") || Word_SMS(isem, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(format_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(format_VALUE, "()V") || !Word_SMS(isem, "println")) żball_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) żball_VALUE("invalid PrintStream receiver");
            if (żball) return;
            if (TYPE_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (TYPE_VALUE == 2) utent.kiteb(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) utent.kiteb_karattru_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) kiteb_SMS(VALUE);
            if (Word_SMS(isem, "println")) utent.kiteb_karattru_VALUE(10);
            return;
        }
        if (kmand == 182 && Word_SMS(propjetarju_VALUE, "java/lang/String")) {
            if (Word_SMS(isem, "length") && Word_SMS(format_VALUE, "()I")) {
                int Referenza = 빼기(2); if (oġġett_VALUE(Referenza, 1)) 넣기(힙[Referenza + 1], 1); return;
            }
            if (Word_SMS(isem, "charAt") && Word_SMS(format_VALUE, "(I)C")) {
                int subscript_VALUE = 빼기(1), Referenza = 빼기(2);
                if (oġġett_VALUE(Referenza, 1)) {
                    if (subscript_VALUE < 0 || subscript_VALUE >= 힙[Referenza + 1]) żball_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[Referenza + 2 + subscript_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(propjetarju_VALUE, "java/lang/StringBuilder")) {
            if (kmand == 183 && Word_SMS(isem, "<init>") && Word_SMS(format_VALUE, "()V")) { oġġett_VALUE(빼기(2), 4); return; }
            if (kmand == 182 && Word_SMS(isem, "toString") && Word_SMS(format_VALUE, "()Ljava/lang/String;")) {
                int Referenza = 빼기(2); if (oġġett_VALUE(Referenza, 4)) 넣기(힙[Referenza + 2] == 0 ? host_karattru("") : 힙[Referenza + 2], 2); return;
            }
            if (kmand == 182 && Word_SMS(isem, "append")) {
                int SMS = 0;
                if (Word_SMS(format_VALUE, "(I)Ljava/lang/StringBuilder;")) SMS = ċifra_karattru(빼기(1));
                else if (Word_SMS(format_VALUE, "(Z)Ljava/lang/StringBuilder;")) SMS = host_karattru(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(format_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); SMS = alloka_Ħażna(1, 1); if (!żball) 힙[SMS + 2] = VALUE & 65535;
                }
                else if (Word_SMS(format_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { SMS = 빼기(2); if (SMS == 0) SMS = host_karattru("null"); }
                else { żball_VALUE("unsupported StringBuilder append"); return; }
                int Referenza = 빼기(2); if (!oġġett_VALUE(Referenza, 4) || !oġġett_VALUE(SMS, 1)) return;
                int 앞 = 힙[Referenza + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], Lura_VALUE_tul = 힙[SMS + 1];
                int 새글 = alloka_Ħażna(1, 앞길이 + Lura_VALUE_tul); if (żball) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < Lura_VALUE_tul; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[SMS + 2 + 수];
                힙[Referenza + 2] = 새글; 넣기(Referenza, 2); return;
            }
        }
        int klassi_Definizzjoni = sab_klassi_Definizzjoni(propjetarju_VALUE); if (klassi_Definizzjoni < 0 || żball) return;
        int fajl_INDEX = sab_metodu(klassi_Definizzjoni, isem, format_VALUE);
        if (fajl_INDEX < 0) {
            for (int kodiċi_tal_karattru = klassi_Definizzjoni, entrata_COUNT = 0; kodiċi_tal_karattru >= 0 && entrata_COUNT < 16; entrata_COUNT++, kodiċi_tal_karattru = 부모종(kodiċi_tal_karattru))
                if (Word_SMS(종부모[kodiċi_tal_karattru], "java/lang/Thread")) { 가닥호출(isem, format_VALUE, kmand); return; }
            żball_VALUE("NoSuchMethodError"); return;
        }
        if (((metodu_aċċess[fajl_INDEX] & 8) != 0) != (kmand == 184)) { żball_VALUE("method static/instance mismatch"); return; }
        if (kmand == 184) { if (!inizjala(metodu_propjetarju[fajl_INDEX], frejm_istruzzjoni[frejm_INDEX])) return; }
        else {
            int 읽는자리 = frejm_Munzell[frejm_INDEX] - metodu_argument_COUNT[fajl_INDEX];
            if (읽는자리 < 0 || 스택형[frejm_INDEX * 128 + 읽는자리] != 2) { żball_VALUE("invalid method receiver"); return; }
            int oġġett_Referenza = 스택값[frejm_INDEX * 128 + 읽는자리];
            if (!객체유효(oġġett_Referenza)) return;
            if (힙[oġġett_Referenza] < 32 || !종포함(힙[oġġett_Referenza] - 32, propjetarju_VALUE)) { żball_VALUE("method receiver type mismatch"); return; }
            if (kmand != 183) fajl_INDEX = sab_metodu(힙[oġġett_Referenza] - 32, isem, format_VALUE);
        }
        if (fajl_INDEX < 0 || (metodu_aċċess[fajl_INDEX] & 0x400) != 0) { żball_VALUE("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((metodu_aċċess[fajl_INDEX] & 32) != 0) {
            if (kmand == 184) { int kodiċi_tal_karattru = metodu_propjetarju[fajl_INDEX]; if (종잠금[kodiċi_tal_karattru] == 0) 종잠금[kodiċi_tal_karattru] = alloka_Ħażna(8, 0); 잠금참조 = 종잠금[kodiċi_tal_karattru]; }
            else 잠금참조 = 스택값[frejm_INDEX * 128 + frejm_Munzell[frejm_INDEX] - metodu_argument_COUNT[fajl_INDEX]];
            if (!잠금얻기(잠금참조)) { if (!żball) frejm_pożizzjoni[frejm_INDEX] = frejm_istruzzjoni[frejm_INDEX]; return; }
        }
        호출(fajl_INDEX); if (!żball) 틀잠금[frejm_INDEX] = 잠금참조;
    }
    static boolean 배열저장가능(int ARRAY_Referenza, int data_VALUE) {
        if (data_VALUE == 0 || ARRAY_element[ARRAY_Referenza] == 0) return true;
        boolean 성공여부 = ARRAY_element[ARRAY_Referenza] == -1 ? (data_VALUE > 0 && data_VALUE < 힙끝 && 힙[data_VALUE] == 1) : 맞는객체(data_VALUE, ARRAY_element[ARRAY_Referenza]);
        if (!성공여부 && !żball) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int ARRAY_slott(int Referenza, int subscript_VALUE, int TYPE_VALUE) {
        if (!oġġett_VALUE(Referenza, TYPE_VALUE)) return 0;
        if (subscript_VALUE < 0 || subscript_VALUE >= 힙[Referenza + 1]) { żball_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Referenza + 2 + subscript_VALUE;
    }
    static void eżegwixxa_kmand() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (żball) { if (던진객체 != 0) 예외처리(); if (żball || frejm_INDEX < 현재가닥 * 32) break; }
            if (frejm_INDEX < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!qaleb_fil()) break; 조각 = 100; }
            if (frejm_INDEX == 0 && klassi_Definizzjoni_stat[entrata_klassi_Definizzjoni] != 2 && !inizjala(entrata_klassi_Definizzjoni, frejm_pożizzjoni[frejm_INDEX])) continue;
            if (frejm_INDEX == 현재가닥 * 32 && 현재가닥 != 0 && (metodu_aċċess[frejm_metodu[frejm_INDEX]] & 32) != 0 && 틀잠금[frejm_INDEX] == 0) {
                int oġġett_Referenza = fil_mira[현재가닥]; if (!잠금얻기(oġġett_Referenza)) { if (żball) break; continue; } 틀잠금[frejm_INDEX] = oġġett_Referenza;
            }
            잠시수 = 0;
            if (--남음 == 0) { żball_VALUE("instruction limit (500000)"); break; }
            int serje = frejm_pożizzjoni[frejm_INDEX]; frejm_istruzzjoni[frejm_INDEX] = serje; int VALUE = 명바();
            if (żball) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = metodu_propjetarju[frejm_metodu[frejm_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= valur_fiss_tag.length) żball_VALUE("invalid ldc constant");
                else if (valur_fiss_tag[수] == 3) 넣기(상가[수], 1);
                else if (valur_fiss_tag[수] == 8) 넣기(valur_fiss_SMS(상가[수]), 2);
                else żball_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { kiteb_lokali(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { kiteb_lokali(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { kiteb_lokali(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int entrata_pożizzjoni = 빼기(1), oġġett_Referenza = 빼기(2), kategorija_CODE = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && oġġett_Referenza > 0 && oġġett_Referenza < 힙끝 && 힙[oġġett_Referenza] == 21) kategorija_CODE = 21;
                int 읽는자리 = ARRAY_slott(oġġett_Referenza, entrata_pożizzjoni, kategorija_CODE); if (!żball) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int entrata_Referenza = 빼기(VALUE == 83 ? 2 : 1), entrata_pożizzjoni = 빼기(1), oġġett_Referenza = 빼기(2), kategorija_CODE = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && oġġett_Referenza > 0 && oġġett_Referenza < 힙끝 && 힙[oġġett_Referenza] == 21) kategorija_CODE = 21;
                int 읽는자리 = ARRAY_slott(oġġett_Referenza, entrata_pożizzjoni, kategorija_CODE);
                if (!żball && kategorija_CODE == 3 && !배열저장가능(oġġett_Referenza, entrata_Referenza)) continue;
                if (!żball) 힙[읽는자리] = kategorija_CODE == 20 ? (byte)entrata_Referenza : kategorija_CODE == 21 ? entrata_Referenza & 1 : kategorija_CODE == 22 ? (char)entrata_Referenza : kategorija_CODE == 23 ? (short)entrata_Referenza : entrata_Referenza;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { Munzell_istruzzjoni(VALUE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), miżura = 0;
                if ((VALUE == 108 || VALUE == 112) && 나 == 0) { żball_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) miżura = 가 + 나;
                if (VALUE == 100) miżura = 가 - 나;
                if (VALUE == 104) miżura = 가 * 나;
                if (VALUE == 108) miżura = 가 / 나;
                if (VALUE == 112) miżura = 가 % 나;
                if (VALUE == 120) miżura = 가 << 나;
                if (VALUE == 122) miżura = 가 >> 나;
                if (VALUE == 124) miżura = 가 >>> 나;
                if (VALUE == 126) miżura = 가 & 나;
                if (VALUE == 128) miżura = 가 | 나;
                if (VALUE == 130) miżura = 가 ^ 나;
                넣기(miżura, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int lokali_ambitu = 명바(), 증분 = (byte)명바(); 지역읽기(lokali_ambitu, 1); 넣기(빼기(1) + 증분, 1); kiteb_lokali(lokali_ambitu, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int destinazzjoni_VALUE = serje + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int 나 = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == 나 : VALUE == 160 || VALUE == 166 ? 가 != 나 : VALUE == 161 ? 가 < 나 : VALUE == 162 ? 가 >= 나 : VALUE == 163 ? 가 > 나 : 가 <= 나;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) mexxi_VALUE(destinazzjoni_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { 반환(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, serje); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { żball_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_metodu(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(klassi_isem_SMS(명상수()), serje); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int kategorija_CODE = 3, komponent = 0;
                if (VALUE == 188) { int 임시값 = 명바(); kategorija_CODE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else komponent = klassi_isem_SMS(명상수());
                if (kategorija_CODE == 0) { żball_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), oġġett_Referenza = alloka_Ħażna(kategorija_CODE, 유효길이); if (!żball) ARRAY_element[oġġett_Referenza] = komponent; 넣기(oġġett_Referenza, 2); continue;
            }
            if (VALUE == 190) {
                int oġġett_Referenza = 빼기(2);
                if (객체유효(oġġett_Referenza)) { int 비교자리 = 힙[oġġett_Referenza]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) żball_VALUE("not an array"); else 넣기(힙[oġġett_Referenza + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int oġġett_Referenza = 빼기(2); if (객체유효(oġġett_Referenza)) { if (힙[oġġett_Referenza] != 9) żball_VALUE("athrow requires supported Throwable"); else { 던진객체 = oġġett_Referenza; żball = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int isem_valur_fiss = klassi_isem_SMS(명상수()), oġġett_Referenza = 빼기(2); boolean MATCH = 맞는객체(oġġett_Referenza, isem_valur_fiss);
                if (VALUE == 193) 넣기(oġġett_Referenza != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !żball) żball_VALUE("ClassCastException"); 넣기(oġġett_Referenza, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = serje + 1, fajl_INDEX = frejm_metodu[frejm_INDEX], tast_Referenza = 빼기(1);
                while ((읽는자리 - metodu_Bidu[fajl_INDEX]) % 4 != 0) 읽는자리++;
                int mira_ADDRESS = pożizzjoni_numru_sħiħ(읽는자리);
                if (VALUE == 170) { int 낮은값 = pożizzjoni_numru_sħiħ(읽는자리 + 4), 높은값 = pożizzjoni_numru_sħiħ(읽는자리 + 8); if (tast_Referenza >= 낮은값 && tast_Referenza <= 높은값) mira_ADDRESS = pożizzjoni_numru_sħiħ(읽는자리 + 12 + (tast_Referenza - 낮은값) * 4); }
                else { int 총수 = pożizzjoni_numru_sħiħ(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (pożizzjoni_numru_sħiħ(읽는자리 + 8 + Loop_INDEX * 8) == tast_Referenza) mira_ADDRESS = pożizzjoni_numru_sħiħ(읽는자리 + 12 + Loop_INDEX * 8); }
                mexxi_VALUE(serje + mira_ADDRESS); continue;
            }
            if (VALUE == 200) { mexxi_VALUE(serje + pożizzjoni_numru_sħiħ(serje + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int oġġett_Referenza = 빼기(2);
                if (VALUE == 195) 잠금풀기(oġġett_Referenza);
                else if (!잠금얻기(oġġett_Referenza) && !żball) { 넣기(oġġett_Referenza, 2); frejm_pożizzjoni[frejm_INDEX] = serje; }
                continue;
            }
            if (VALUE == 196) {
                int kmand_CODE = 명바(), entrata_pożizzjoni = 명짧();
                if (kmand_CODE == 21 || kmand_CODE == 25) 지역읽기(entrata_pożizzjoni, kmand_CODE == 21 ? 1 : 2);
                else if (kmand_CODE == 54 || kmand_CODE == 58) kiteb_lokali(entrata_pożizzjoni, kmand_CODE == 54 ? 1 : 2);
                else if (kmand_CODE == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(entrata_pożizzjoni, 1); 넣기(빼기(1) + DELTA_VALUE, 1); kiteb_lokali(entrata_pożizzjoni, 1); }
                else żball_VALUE("unsupported wide opcode");
                continue;
            }
            żball_VALUE("unsupported bytecode");
        }
    }
    static int sab_klassi_Definizzjoni(int isem) {
        for (int Loop_INDEX = 0; Loop_INDEX < klassi_Definizzjoni_COUNT; Loop_INDEX++) if (klassi_Definizzjoni_isem[Loop_INDEX] != 0 && 같은말(klassi_Definizzjoni_isem[Loop_INDEX], isem)) return Loop_INDEX;
        return karga_klassi_Definizzjoni(valur_fiss_SMS(isem));
    }
    static int karga_klassi_Definizzjoni(int isem_string) {
        if (!oġġett_VALUE(isem_string, 1)) return -1;
        int tul_VALUE = 힙[isem_string + 1];
        if (tul_VALUE < 1 || tul_VALUE > 505 || klassi_Definizzjoni_COUNT == 16) { żball_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < tul_VALUE; Loop_INDEX++) { int kodiċi_tal_karattru = 힙[isem_string + 2 + Loop_INDEX]; fajl_isem_SMS[Loop_INDEX] = kodiċi_tal_karattru == '/' ? '.' : kodiċi_tal_karattru; }
        fajl_isem_SMS[tul_VALUE] = '.'; fajl_isem_SMS[tul_VALUE + 1] = 'c'; fajl_isem_SMS[tul_VALUE + 2] = 'l'; fajl_isem_SMS[tul_VALUE + 3] = 'a'; fajl_isem_SMS[tul_VALUE + 4] = 's'; fajl_isem_SMS[tul_VALUE + 5] = 's'; fajl_isem_SMS[tul_VALUE + 6] = 0;
        int daqqas = utent.파일읽기(fajl_isem_SMS, 임시파일);
        if (daqqas < 0) { żball_VALUE("ClassNotFoundException"); return -1; }
        int klassi_Definizzjoni = klassi_Definizzjoni_COUNT++; klassi_Definizzjoni_daqqas[klassi_Definizzjoni] = daqqas;
        for (int Loop_INDEX = 0; Loop_INDEX < daqqas; Loop_INDEX++) fajl[klassi_Definizzjoni * 16384 + Loop_INDEX] = 임시파일[Loop_INDEX];
        클래스읽기(klassi_Definizzjoni); if (żball) return -1;
        int attwali_data = valur_fiss_SMS(klassi_Definizzjoni_isem[klassi_Definizzjoni]);
        if (!글같음(attwali_data, isem_string, true)) { żball_VALUE("class name does not match file"); return -1; }
        int 부모 = 종부모[klassi_Definizzjoni];
        if (부모 != 0 && !Word_SMS(부모, "java/lang/Object") && !Word_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = sab_klassi_Definizzjoni(부모);
            if (żball || 위 < 0) return -1;
            int 읽는자리 = 위, palk_COUNT = 0;
            while (읽는자리 >= 0 && palk_COUNT++ < 16) {
                if (읽는자리 == klassi_Definizzjoni) { żball_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = klassi_slott_COUNT[위];
            for (int fajl_INDEX = 0; fajl_INDEX < slott_COUNT; fajl_INDEX++) if (slott_propjetarju[fajl_INDEX] == klassi_Definizzjoni && (slott_permessi[fajl_INDEX] & 8) == 0) slott_pożizzjoni[fajl_INDEX] += 시작변위;
            klassi_slott_COUNT[klassi_Definizzjoni] += 시작변위;
        }
        return klassi_Definizzjoni;
    }
    static int 부모종(int klassi_Definizzjoni) {
        int isem = 종부모[klassi_Definizzjoni];
        for (int Loop_INDEX = 0; Loop_INDEX < klassi_Definizzjoni_COUNT; Loop_INDEX++) if (isem != 0 && klassi_Definizzjoni_isem[Loop_INDEX] != 0 && 같은말(klassi_Definizzjoni_isem[Loop_INDEX], isem)) return Loop_INDEX;
        return -1;
    }
    static int sab_metodu(int klassi_Definizzjoni, int isem, int format_VALUE) {
        for (int 깊이 = 0; klassi_Definizzjoni >= 0 && 깊이 < 16; 깊이++, klassi_Definizzjoni = 부모종(klassi_Definizzjoni)) {
            for (int Loop_INDEX = 0; Loop_INDEX < metodu_COUNT; Loop_INDEX++) if (metodu_propjetarju[Loop_INDEX] == klassi_Definizzjoni && 같은말(metodu_isem_SMS[Loop_INDEX], isem) && 같은말(metodu_TYPE[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int isem_metodu(int klassi_Definizzjoni, String isem, String format_VALUE) {
        for (int 깊이 = 0; klassi_Definizzjoni >= 0 && 깊이 < 16; 깊이++, klassi_Definizzjoni = 부모종(klassi_Definizzjoni))
            for (int Loop_INDEX = 0; Loop_INDEX < metodu_COUNT; Loop_INDEX++) if (metodu_propjetarju[Loop_INDEX] == klassi_Definizzjoni && Word_SMS(metodu_isem_SMS[Loop_INDEX], isem) && Word_SMS(metodu_TYPE[Loop_INDEX], format_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int isem) { return fajl[상가[isem]] == 'L' || fajl[상가[isem]] == '[' ? 2 : 1; }
    static boolean inizjala(int klassi_Definizzjoni, int kmand_Bidu) {
        if (klassi_Definizzjoni < 0 || żball) return false;
        if (klassi_Definizzjoni_stat[klassi_Definizzjoni] == 3) { żball_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (klassi_Definizzjoni_stat[klassi_Definizzjoni] == 1 && klassi_fil[klassi_Definizzjoni] != 현재가닥) { frejm_pożizzjoni[frejm_INDEX] = kmand_Bidu; 바꿈요청 = true; return false; }
        if (klassi_Definizzjoni_stat[klassi_Definizzjoni] != 0) return true;
        int 위 = 부모종(klassi_Definizzjoni);
        if (위 >= 0 && !inizjala(위, kmand_Bidu)) return false;
        klassi_Definizzjoni_stat[klassi_Definizzjoni] = 1; klassi_fil[klassi_Definizzjoni] = 현재가닥;
        if (inizjala_klassi_Definizzjoni[klassi_Definizzjoni] != 0) {
            frejm_pożizzjoni[frejm_INDEX] = kmand_Bidu;
            호출(inizjala_klassi_Definizzjoni[klassi_Definizzjoni] - 1); if (!żball) inizjala_frejm[frejm_INDEX] = klassi_Definizzjoni + 1;
            return false;
        }
        klassi_Definizzjoni_stat[klassi_Definizzjoni] = 2; return true;
    }
    static void 필드호출(int INDEX, int kmand, int serje) {
        if (!ċekk_valur_fiss(INDEX, 9)) return;
        int propjetarju_VALUE = klassi_isem_SMS(상가[INDEX]), isem = Referenza_isem(valur_fiss_SECOND_VALUE[INDEX]), format_VALUE = Referenza_TYPE(valur_fiss_SECOND_VALUE[INDEX]);
        if (Word_SMS(propjetarju_VALUE, "java/lang/System") && (Word_SMS(isem, "out") || Word_SMS(isem, "err")) && Word_SMS(format_VALUE, "Ljava/io/PrintStream;") && kmand == 178) { 넣기(-1, 2); return; }
        int klassi_Definizzjoni = sab_klassi_Definizzjoni(propjetarju_VALUE); if (klassi_Definizzjoni < 0 || żball) return;
        int 찾음 = -1;
        for (int 읽는자리 = klassi_Definizzjoni, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int fajl_INDEX = 0; fajl_INDEX < slott_COUNT; fajl_INDEX++) if (slott_propjetarju[fajl_INDEX] == 읽는자리 && 같은말(slott_isem[fajl_INDEX], isem) && 같은말(slott_TYPE[fajl_INDEX], format_VALUE)) 찾음 = fajl_INDEX;
        if (찾음 < 0) { żball_VALUE("NoSuchFieldError"); return; }
        boolean statiku_VALUE = kmand == 178 || kmand == 179;
        if (statiku_VALUE != ((slott_permessi[찾음] & 8) != 0)) { żball_VALUE("field static/instance mismatch"); return; }
        if (statiku_VALUE && !inizjala(slott_propjetarju[찾음], serje)) return;
        int TYPE_VALUE = 형종류(format_VALUE), VALUE = 0;
        if (kmand == 179 || kmand == 181) VALUE = 빼기(TYPE_VALUE);
        if (statiku_VALUE) { if (kmand == 178) 넣기(slott_data[찾음], TYPE_VALUE); else if (!żball) slott_data[찾음] = VALUE; return; }
        int oġġett_Referenza = 빼기(2);
        if (!객체유효(oġġett_Referenza)) return;
        if (힙[oġġett_Referenza] < 32 || !종포함(힙[oġġett_Referenza] - 32, propjetarju_VALUE)) { żball_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = oġġett_Referenza + 2 + slott_pożizzjoni[찾음];
        if (kmand == 180) 넣기(힙[보관칸], TYPE_VALUE);
        else if (!żball) { 힙[보관칸] = VALUE; 힙참조[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int klassi_Definizzjoni, int isem) {
        for (int 중첩깊이 = 0; klassi_Definizzjoni >= 0 && 중첩깊이 < 16; 중첩깊이++, klassi_Definizzjoni = 부모종(klassi_Definizzjoni)) {
            if (같은말(klassi_Definizzjoni_isem[klassi_Definizzjoni], isem) || (종부모[klassi_Definizzjoni] != 0 && 같은말(종부모[klassi_Definizzjoni], isem))) return true;
            for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < klassi_interface_COUNT[klassi_Definizzjoni]; inner_join_pożizzjoni++) if (같은말(klassi_interface[klassi_Definizzjoni * 16 + inner_join_pożizzjoni], isem)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int byte_data, boolean mogħdija) {
        if (첫값 == byte_data) return true;
        if (첫값 <= 0 || byte_data <= 0 || 힙[첫값] != 1 || 힙[byte_data] != 1 || 힙[첫값 + 1] != 힙[byte_data + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) {
            int koordinat_x = 힙[첫값 + 2 + Loop_INDEX], 세로좌표 = 힙[byte_data + 2 + Loop_INDEX];
            if (mogħdija) { if (koordinat_x == '.') koordinat_x = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (koordinat_x != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int oġġett_Referenza) {
        if (oġġett_Referenza == 0) { żball_VALUE("NullPointerException"); return false; }
        if (oġġett_Referenza < 1 || oġġett_Referenza >= 힙끝 || 힙폭[oġġett_Referenza] < 2 || 힙[oġġett_Referenza] == 0) { żball_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void pproteġa_VALUE(int oġġett_Referenza) {
        if (oġġett_Referenza > 0 && oġġett_Referenza < 힙끝 && 힙폭[oġġett_Referenza] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = oġġett_Referenza;
    }
    static void wera_VALUE_487749b8(int oġġett_Referenza) {
        if (oġġett_Referenza > 0 && oġġett_Referenza < 힙끝 && 힙폭[oġġett_Referenza] >= 2 && 힙[oġġett_Referenza] != 0 && 힙표시[oġġett_Referenza] == 0) {
            힙표시[oġġett_Referenza] = 1; 표시대기[wera_COUNT++] = oġġett_Referenza;
        }
    }
    static void 수거() {
        wera_COUNT = 0; ġabra_COUNT++;
        for (int ċekk_pożizzjoni = 1; ċekk_pożizzjoni < 힙끝; ċekk_pożizzjoni += 힙폭[ċekk_pożizzjoni]) 힙표시[ċekk_pożizzjoni] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < string_Referenza.length; Loop_INDEX++) wera_VALUE_487749b8(string_Referenza[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < slott_COUNT; Loop_INDEX++) if ((slott_permessi[Loop_INDEX] & 8) != 0 && 형종류(slott_TYPE[Loop_INDEX]) == 2) wera_VALUE_487749b8(slott_data[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < fil_COUNT; 임시값++) {
            wera_VALUE_487749b8(fil_oġġett[임시값]); wera_VALUE_487749b8(fil_mira[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? frejm_INDEX : fil_frejm[임시값];
            for (int fajl_INDEX = 임시값 * 32; fajl_INDEX <= 꼭대기자리; fajl_INDEX++) {
                for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < 함수지역[frejm_metodu[fajl_INDEX]]; inner_join_pożizzjoni++) if (lokali_TYPE[fajl_INDEX * 128 + inner_join_pożizzjoni] == 2) wera_VALUE_487749b8(lokali_VALUE[fajl_INDEX * 128 + inner_join_pożizzjoni]);
                for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < frejm_Munzell[fajl_INDEX]; inner_join_pożizzjoni++) if (스택형[fajl_INDEX * 128 + inner_join_pożizzjoni] == 2) wera_VALUE_487749b8(스택값[fajl_INDEX * 128 + inner_join_pożizzjoni]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) wera_VALUE_487749b8(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) wera_VALUE_487749b8(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_numru_sħiħ.length; Loop_INDEX++) wera_VALUE_487749b8(Store_numru_sħiħ[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < klassi_Definizzjoni_COUNT; Loop_INDEX++) wera_VALUE_487749b8(종잠금[Loop_INDEX]);
        for (int ċekk_pożizzjoni = 1; ċekk_pożizzjoni < 힙끝; ċekk_pożizzjoni += 힙폭[ċekk_pożizzjoni]) if (잠금깊이[ċekk_pożizzjoni] > 0) wera_VALUE_487749b8(ċekk_pożizzjoni);
        wera_VALUE_487749b8(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) wera_VALUE_487749b8(잠시참조[Loop_INDEX]);
        while (wera_COUNT > 0) {
            int oġġett_Referenza = 표시대기[--wera_COUNT], kategorija_CODE = 힙[oġġett_Referenza];
            for (int Loop_INDEX = oġġett_Referenza + 2; Loop_INDEX < oġġett_Referenza + 힙폭[oġġett_Referenza]; Loop_INDEX++) if (kategorija_CODE == 3 || kategorija_CODE == 4 || 힙참조[Loop_INDEX] != 0) wera_VALUE_487749b8(힙[Loop_INDEX]);
        }
        for (int ċekk_pożizzjoni = 1; ċekk_pożizzjoni < 힙끝; ċekk_pożizzjoni += 힙폭[ċekk_pożizzjoni]) if (힙표시[ċekk_pożizzjoni] == 0) 힙[ċekk_pożizzjoni] = 0;
        for (int ċekk_pożizzjoni = 1; ċekk_pożizzjoni < 힙끝; ċekk_pożizzjoni += 힙폭[ċekk_pożizzjoni]) if (힙[ċekk_pożizzjoni] == 0) {
            while (ċekk_pożizzjoni + 힙폭[ċekk_pożizzjoni] < 힙끝 && 힙[ċekk_pożizzjoni + 힙폭[ċekk_pożizzjoni]] == 0) { int Li_Jmiss_pożizzjoni = ċekk_pożizzjoni + 힙폭[ċekk_pożizzjoni]; 힙폭[ċekk_pożizzjoni] += 힙폭[Li_Jmiss_pożizzjoni]; 힙폭[Li_Jmiss_pożizzjoni] = 0; }
            if (ċekk_pożizzjoni + 힙폭[ċekk_pożizzjoni] == 힙끝) { 힙끝 = ċekk_pożizzjoni; break; }
        }
    }
    static int 새기억(int 종류, int tul_VALUE) {
        if (tul_VALUE < 0) { żball_VALUE("NegativeArraySizeException"); return 0; }
        if (tul_VALUE > 힙.length - 3) { żball_VALUE("object heap exhausted"); return 0; }
        int 필요수 = tul_VALUE + 2, oġġett_Referenza = 0;
        if (필요수 <= 힙.length - 힙끝) { oġġett_Referenza = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { oġġett_Referenza = 읽는자리; break; }
            if (oġġett_Referenza != 0) {
                int 남은길이 = 힙폭[oġġett_Referenza] - 필요수;
                if (남은길이 >= 2) { 힙폭[oġġett_Referenza + 필요수] = 남은길이; 힙[oġġett_Referenza + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { oġġett_Referenza = 힙끝; 힙끝 += 필요수; }
        }
        if (oġġett_Referenza == 0) { żball_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { 힙[oġġett_Referenza + Loop_INDEX] = 0; 힙참조[oġġett_Referenza + Loop_INDEX] = 0; 힙폭[oġġett_Referenza + Loop_INDEX] = 0; }
        ARRAY_element[oġġett_Referenza] = 0;
        힙폭[oġġett_Referenza] = 필요수; 힙[oġġett_Referenza] = 종류; 힙[oġġett_Referenza + 1] = tul_VALUE; pproteġa_VALUE(oġġett_Referenza); return oġġett_Referenza;
    }
    static int 예외종(String isem_valur_fiss) {
        if (자바도구.같음(isem_valur_fiss, "java/lang/Throwable")) return 1;
        if (자바도구.같음(isem_valur_fiss, "java/lang/Exception")) return 2;
        if (자바도구.같음(isem_valur_fiss, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(isem_valur_fiss, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(isem_valur_fiss, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(isem_valur_fiss, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(isem_valur_fiss, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(isem_valur_fiss, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(isem_valur_fiss, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(isem_valur_fiss, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(isem_valur_fiss, "java/io/IOException")) return 11;
        if (자바도구.같음(isem_valur_fiss, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(isem_valur_fiss, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(isem_valur_fiss, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(isem_valur_fiss, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int 예외상수(int isem) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_SMS(isem, 예외이름(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String 예외이름(int kont_VALUE) {
        if (kont_VALUE == 40) return "java/lang/InterruptedException";
        if (kont_VALUE == 41) return "Malti/자체/대기중단예외";
        if (kont_VALUE == 39) return "java/net/SocketException";
        if (kont_VALUE == 20) return "Malti/자체/예외";
        if (kont_VALUE == 21) return "Malti/자체/실행예외";
        if (kont_VALUE == 22) return "Malti/자체/입출력예외";
        if (kont_VALUE == 23) return "Malti/자체/대기시간초과예외";
        if (kont_VALUE == 24) return "Malti/자체/주소확인예외";
        if (kont_VALUE == 25) return "Malti/자체/파일없음예외";
        if (kont_VALUE == 26) return "Malti/자체/통신예외";
        if (kont_VALUE == 27) return "Malti/자체/잘못된인수예외";
        if (kont_VALUE == 28) return "Malti/자체/숫자형식예외";
        if (kont_VALUE == 29) return "Malti/자체/범위예외";
        if (kont_VALUE == 30) return "Malti/자체/배열범위예외";
        if (kont_VALUE == 31) return "Malti/자체/문자열범위예외";
        if (kont_VALUE == 32) return "Malti/자체/빈참조예외";
        if (kont_VALUE == 33) return "Malti/자체/산술예외";
        if (kont_VALUE == 34) return "Malti/자체/상태예외";
        if (kont_VALUE == 35) return "Malti/자체/형변환예외";
        if (kont_VALUE == 36) return "Malti/자체/음수배열크기예외";
        if (kont_VALUE == 37) return "Malti/자체/ARRAY_Store_żball";
        if (kont_VALUE == 38) return "Malti/자체/가닥상태예외";
        if (kont_VALUE == 1) return "java/lang/Throwable"; if (kont_VALUE == 2) return "java/lang/Exception";
        if (kont_VALUE == 3) return "java/lang/RuntimeException"; if (kont_VALUE == 4) return "java/lang/ArithmeticException";
        if (kont_VALUE == 5) return "java/lang/NullPointerException"; if (kont_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (kont_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (kont_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (kont_VALUE == 9) return "java/lang/IllegalArgumentException"; if (kont_VALUE == 10) return "java/lang/NumberFormatException";
        if (kont_VALUE == 11) return "java/io/IOException"; if (kont_VALUE == 12) return "java/io/FileNotFoundException";
        if (kont_VALUE == 17) return "java/lang/ArrayStoreException";
        if (kont_VALUE == 18) return "java/net/UnknownHostException";
        if (kont_VALUE == 19) return "java/net/SocketTimeoutException";
        if (kont_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (kont_VALUE == 13) return "java/lang/IllegalStateException"; if (kont_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int kont_VALUE) {
        if (kont_VALUE == 40) return 2;
        if (kont_VALUE == 41) return 40;
        if (kont_VALUE == 39) return 11;
        if (kont_VALUE == 1) return 0;
        if (kont_VALUE == 2) return 1;
        if (kont_VALUE == 3) return 2;
        if (kont_VALUE == 4) return 3;
        if (kont_VALUE == 5) return 3;
        if (kont_VALUE == 6) return 3;
        if (kont_VALUE == 7) return 6;
        if (kont_VALUE == 8) return 6;
        if (kont_VALUE == 9) return 3;
        if (kont_VALUE == 10) return 9;
        if (kont_VALUE == 11) return 2;
        if (kont_VALUE == 12) return 11;
        if (kont_VALUE == 13) return 3;
        if (kont_VALUE == 14) return 3;
        if (kont_VALUE == 15) return 3;
        if (kont_VALUE == 16) return 9;
        if (kont_VALUE == 17) return 3;
        if (kont_VALUE == 18) return 11;
        if (kont_VALUE == 19) return 11;
        if (kont_VALUE == 20) return 2;
        if (kont_VALUE == 21) return 3;
        if (kont_VALUE == 22) return 11;
        if (kont_VALUE == 23) return 22;
        if (kont_VALUE == 24) return 22;
        if (kont_VALUE == 25) return 22;
        if (kont_VALUE == 26) return 22;
        if (kont_VALUE == 27) return 9;
        if (kont_VALUE == 28) return 27;
        if (kont_VALUE == 29) return 6;
        if (kont_VALUE == 30) return 29;
        if (kont_VALUE == 31) return 29;
        if (kont_VALUE == 32) return 5;
        if (kont_VALUE == 33) return 4;
        if (kont_VALUE == 34) return 13;
        if (kont_VALUE == 35) return 14;
        if (kont_VALUE == 36) return 15;
        if (kont_VALUE == 37) return 17;
        if (kont_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int attwali_VALUE, int 요구값) {
        for (int 깊이 = 0; attwali_VALUE != 0 && 깊이 < 16; 깊이++, attwali_VALUE = 예외부모(attwali_VALUE))
            if (attwali_VALUE == 요구값) return true;
        return false;
    }
    static void 예외던짐(int kont_VALUE, String AQRANI_Referenza) {
        int oġġett_Referenza = 새기억(9, 2); if (żball) return;
        힙[oġġett_Referenza + 2] = kont_VALUE; 힙[oġġett_Referenza + 3] = host_karattru(AQRANI_Referenza); 힙참조[oġġett_Referenza + 3] = 1;
        던진객체 = oġġett_Referenza; żball = true;
    }
    static boolean 맞는객체(int oġġett_Referenza, int isem) {
        if (oġġett_Referenza == 0) return true;
        if (!객체유효(oġġett_Referenza)) return false;
        int kategorija_CODE = 힙[oġġett_Referenza];
        if (Word_SMS(isem, "java/lang/Object")) return true;
        if (kategorija_CODE >= 32) return 종포함(kategorija_CODE - 32, isem);
        if (kategorija_CODE == 9) { int mira_ADDRESS = 예외상수(isem); return mira_ADDRESS != 0 && 예외포함(힙[oġġett_Referenza + 2], mira_ADDRESS); }
        if (kategorija_CODE == 1) return Word_SMS(isem, "java/lang/String") || Word_SMS(isem, "java/lang/CharSequence");
        if (kategorija_CODE == 4) return Word_SMS(isem, "java/lang/StringBuilder") || Word_SMS(isem, "java/lang/CharSequence");
        if (kategorija_CODE == 10) return Word_SMS(isem, "java/util/ArrayList") || Word_SMS(isem, "java/util/List");
        if (kategorija_CODE == 11) return Word_SMS(isem, "java/util/HashMap") || Word_SMS(isem, "java/util/Map");
        if (kategorija_CODE == 12) return Word_SMS(isem, "java/lang/Integer") || Word_SMS(isem, "java/lang/Number");
        if (kategorija_CODE >= 24 && kategorija_CODE <= 28 && 힙[oġġett_Referenza + 13] != 0) return 한국어화면종(isem) == kategorija_CODE || Word_SMS(isem, "Malti/자체/화면구성요소");
        if (kategorija_CODE >= 24 && kategorija_CODE <= 28) return (한국어화면종(isem) == 0 && 화면종(isem) == kategorija_CODE) || Word_SMS(isem, "java/awt/Component") || Word_SMS(isem, "java/awt/Container") || Word_SMS(isem, "javax/swing/JComponent");
        if (kategorija_CODE == 29) return Word_SMS(isem, 힙[oġġett_Referenza + 3] != 0 ? "Malti/자체/동작알림" : "java/awt/event/ActionEvent");
        if (kategorija_CODE == 30) return Word_SMS(isem, "java/awt/FlowLayout") || Word_SMS(isem, "java/awt/LayoutManager");
        if (kategorija_CODE == 17) return Word_SMS(isem, "java/net/Socket");
        if (kategorija_CODE == 18) return Word_SMS(isem, "java/net/ServerSocket");
        if (kategorija_CODE == 19) return Word_SMS(isem, 힙[oġġett_Referenza + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (kategorija_CODE == 14) return Word_SMS(isem, "java/net/InetAddress");
        if (kategorija_CODE == 15) return Word_SMS(isem, "java/net/DatagramSocket");
        if (kategorija_CODE == 16) return Word_SMS(isem, "java/net/DatagramPacket");
        if (kategorija_CODE == 13) return Word_SMS(isem, 힙[oġġett_Referenza + 3] != 0 ? "Malti/자체/작업가닥" : "java/lang/Thread");
        if (kategorija_CODE == 2) return Word_SMS(isem, "[I"); if (kategorija_CODE == 20) return Word_SMS(isem, "[B"); if (kategorija_CODE == 21) return Word_SMS(isem, "[Z");
        if (kategorija_CODE == 22) return Word_SMS(isem, "[C"); if (kategorija_CODE == 23) return Word_SMS(isem, "[S");
        if (kategorija_CODE != 3) return false;
        if (Word_SMS(isem, "[Ljava/lang/Object;")) return true;
        int komponent = ARRAY_element[oġġett_Referenza];
        if (komponent == -1) return Word_SMS(isem, "[Ljava/lang/String;") || Word_SMS(isem, "[Ljava/lang/CharSequence;");
        if (komponent == 0) return false;
        if (배열종비교(komponent, isem)) return true;
        if ((Word_SMS(komponent, "java/lang/String") || Word_SMS(komponent, "java/lang/StringBuilder")) && Word_SMS(isem, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < klassi_Definizzjoni_COUNT; Loop_INDEX++) if (같은말(klassi_Definizzjoni_isem[Loop_INDEX], komponent)) {
            for (int kodiċi_tal_karattru = Loop_INDEX, 중첩깊이 = 0; kodiċi_tal_karattru >= 0 && 중첩깊이 < 16; 중첩깊이++, kodiċi_tal_karattru = 부모종(kodiċi_tal_karattru)) {
                if (배열종비교(종부모[kodiċi_tal_karattru], isem)) return true;
                for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < klassi_interface_COUNT[kodiċi_tal_karattru]; inner_join_pożizzjoni++) if (배열종비교(klassi_interface[kodiċi_tal_karattru * 16 + inner_join_pożizzjoni], isem)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int isem_valur_fiss, int 형식참조) {
        int ċekk_pożizzjoni = 상가[형식참조], entrata_COUNT = valur_fiss_SECOND_VALUE[형식참조];
        if (isem_valur_fiss == 0 || entrata_COUNT < 4 || fajl[ċekk_pożizzjoni] != '[' || fajl[ċekk_pożizzjoni + 1] != 'L' || fajl[ċekk_pożizzjoni + entrata_COUNT - 1] != ';' || valur_fiss_SECOND_VALUE[isem_valur_fiss] != entrata_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < entrata_COUNT - 3; Loop_INDEX++) if (fajl[상가[isem_valur_fiss] + Loop_INDEX] != fajl[ċekk_pożizzjoni + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void 예외처리() {
        if (던진객체 == 0) return;
        żball = false;
        while (frejm_INDEX >= 현재가닥 * 32) {
            int fajl_INDEX = frejm_metodu[frejm_INDEX], 읽는자리 = frejm_istruzzjoni[frejm_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == fajl_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                frejm_pożizzjoni[frejm_INDEX] = 잡기위치[Loop_INDEX]; frejm_Munzell[frejm_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (inizjala_frejm[frejm_INDEX] != 0) klassi_Definizzjoni_stat[inizjala_frejm[frejm_INDEX] - 1] = 3;
            if (틀잠금[frejm_INDEX] != 0) { 잠금풀기(틀잠금[frejm_INDEX]); 틀잠금[frejm_INDEX] = 0; }
            frejm_INDEX--;
        }
        utent.kiteb("Uncaught ");
        if (힙[던진객체] == 9) { utent.kiteb(예외이름(힙[던진객체 + 2])); utent.kiteb(": "); kiteb_SMS(힙[던진객체 + 3]); }
        else utent.kiteb("user exception");
        utent.kiteb_karattru_VALUE(10); 던진객체 = 0; żball = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void Munzell_istruzzjoni(int kmand_CODE) {
        int 첫값 = 빼기(0), 첫형식 = 반환형;
        if (kmand_CODE == 87) return;
        if (kmand_CODE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int byte_data = 빼기(0), SECOND_format = 반환형;
        if (kmand_CODE == 88) return;
        if (kmand_CODE == 90) { 넣기(첫값, 첫형식); 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (kmand_CODE == 92) { 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (kmand_CODE == 95) { 넣기(첫값, 첫형식); 넣기(byte_data, SECOND_format); return; }
        int kodiċi_tal_karattru = 빼기(0), 셋째형식 = 반환형;
        if (kmand_CODE == 91) { 넣기(첫값, 첫형식); 넣기(kodiċi_tal_karattru, 셋째형식); 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); return; }
        if (kmand_CODE == 93) { 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); 넣기(kodiċi_tal_karattru, 셋째형식); 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = 반환형;
        넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(kodiċi_tal_karattru, 셋째형식); 넣기(byte_data, SECOND_format); 넣기(첫값, 첫형식);
    }
    static void 새객체(int isem_valur_fiss, int 시작점) {
        int kategorija_CODE = 0, 유효길이 = 0, 예외참조 = 예외상수(isem_valur_fiss);
        if (Word_SMS(isem_valur_fiss, "java/lang/StringBuilder")) { kategorija_CODE = 4; 유효길이 = 1; }
        if (Word_SMS(isem_valur_fiss, "java/io/FileInputStream")) { kategorija_CODE = 5; 유효길이 = 2; }
        if (Word_SMS(isem_valur_fiss, "java/io/FileOutputStream")) { kategorija_CODE = 6; 유효길이 = 2; }
        if (예외참조 != 0) { kategorija_CODE = 9; 유효길이 = 2; }
        if (Word_SMS(isem_valur_fiss, "java/util/ArrayList")) { kategorija_CODE = 10; 유효길이 = 2; }
        if (Word_SMS(isem_valur_fiss, "java/util/HashMap")) { kategorija_CODE = 11; 유효길이 = 2; }
        if (Word_SMS(isem_valur_fiss, "java/lang/Integer")) { kategorija_CODE = 12; 유효길이 = 1; }
        if (Word_SMS(isem_valur_fiss, "java/net/Socket")) { kategorija_CODE = 17; 유효길이 = 5; }
        if (Word_SMS(isem_valur_fiss, "java/net/ServerSocket")) { kategorija_CODE = 18; 유효길이 = 5; }
        if (Word_SMS(isem_valur_fiss, "java/net/DatagramSocket")) { kategorija_CODE = 15; 유효길이 = 3; }
        if (Word_SMS(isem_valur_fiss, "java/net/DatagramPacket")) { kategorija_CODE = 16; 유효길이 = 4; }
        if (Word_SMS(isem_valur_fiss, "java/lang/Thread") || Word_SMS(isem_valur_fiss, "Malti/자체/작업가닥")) { kategorija_CODE = 13; 유효길이 = 2; }
        if (Word_SMS(isem_valur_fiss, "java/lang/Object")) { kategorija_CODE = 8; }
        if (kategorija_CODE == 0 && 화면종(isem_valur_fiss) != 0) { kategorija_CODE = 화면종(isem_valur_fiss); 유효길이 = 12; }
        if (kategorija_CODE == 0) {
            int kodiċi_tal_karattru = sab_klassi_Definizzjoni(isem_valur_fiss); if (kodiċi_tal_karattru < 0 || żball || !inizjala(kodiċi_tal_karattru, 시작점)) return;
            kategorija_CODE = 32 + kodiċi_tal_karattru; 유효길이 = klassi_slott_COUNT[kodiċi_tal_karattru];
        }
        int oġġett_Referenza = alloka_Ħażna(kategorija_CODE, 유효길이); if (żball) return;
        if (kategorija_CODE == 13 && Word_SMS(isem_valur_fiss, "Malti/자체/작업가닥")) 힙[oġġett_Referenza + 3] = 1;
        if (kategorija_CODE >= 24 && kategorija_CODE <= 28 && 한국어화면종(isem_valur_fiss) != 0) 힙[oġġett_Referenza + 13] = 1;
        if (kategorija_CODE == 5 || kategorija_CODE == 6 || kategorija_CODE == 15 || kategorija_CODE == 17 || kategorija_CODE == 18) 힙[oġġett_Referenza + 2] = -1;
        if (kategorija_CODE == 9) 힙[oġġett_Referenza + 2] = 예외참조;
        넣기(oġġett_Referenza, 2);
    }
    static boolean 값같음(int 첫값, int byte_data) {
        if (첫값 == byte_data) return true;
        if (첫값 == 0 || byte_data == 0 || 첫값 < 0 || byte_data < 0 || 첫값 >= 힙끝 || byte_data >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[byte_data] == 1) return 글같음(첫값, byte_data, false);
        return 힙[첫값] == 12 && 힙[byte_data] == 12 && 힙[첫값 + 2] == 힙[byte_data + 2];
    }
    static int 글조각(int oġġett_Referenza, int Bidu_pożizzjoni, int ttermina_pożizzjoni) {
        if (!oġġett_VALUE(oġġett_Referenza, 1)) return 0;
        if (Bidu_pożizzjoni < 0 || ttermina_pożizzjoni < Bidu_pożizzjoni || ttermina_pożizzjoni > 힙[oġġett_Referenza + 1]) { żball_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = alloka_Ħażna(1, ttermina_pożizzjoni - Bidu_pożizzjoni); if (żball) return 0;
        for (int Loop_INDEX = Bidu_pożizzjoni; Loop_INDEX < ttermina_pożizzjoni; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX - Bidu_pożizzjoni] = 힙[oġġett_Referenza + 2 + Loop_INDEX];
        return 반환값;
    }
    static int ingħaqad_SMS(int 첫값, int byte_data) {
        if (!oġġett_VALUE(첫값, 1) || !oġġett_VALUE(byte_data, 1)) return 0;
        int entrata_COUNT = 힙[첫값 + 1], metodu_INDEX = 힙[byte_data + 1], 반환값 = alloka_Ħażna(1, entrata_COUNT + metodu_INDEX); if (żball) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < entrata_COUNT; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 힙[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < metodu_INDEX; Loop_INDEX++) 힙[반환값 + 2 + entrata_COUNT + Loop_INDEX] = 힙[byte_data + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int propjetarju, int isem_valur_fiss, int 서술상수, int kmand_CODE) {
        if (Word_SMS(propjetarju, "Malti/자체/실행인수") && kmand_CODE == 184) {
            if (Word_SMS(isem_valur_fiss, "element_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(utent.인수개수() - 1, 1); return true; }
            if (Word_SMS(isem_valur_fiss, "SMS") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= utent.인수개수() - 1) 예외던짐(29, "eżegwixxa_kmand 인수 범위를 벗어났습니다");
                else 넣기(host_karattru(utent.인수(순번 + 1)), 2);
                return true;
            }
            żball_VALUE("지원하지 않는 Malti eżegwixxa_kmand 인수 호출"); return true;
        }
        if (Word_SMS(propjetarju, "Malti/자체/작업가닥")) { Proċess_fil(isem_valur_fiss, 서술상수, kmand_CODE, true); return true; }
        if (한국어화면소유(propjetarju)) { 한국어화면호출(propjetarju, isem_valur_fiss, 서술상수, kmand_CODE); return true; }
        if (화면소유(propjetarju)) { 화면호출(propjetarju, isem_valur_fiss, 서술상수, kmand_CODE); return true; }
        if (Word_SMS(propjetarju, "java/net/Socket") || Word_SMS(propjetarju, "java/net/ServerSocket") || Word_SMS(propjetarju, "java/io/InputStream") || Word_SMS(propjetarju, "java/io/OutputStream")) { 흐름호출(propjetarju, isem_valur_fiss, 서술상수, kmand_CODE); return true; }
        if (Word_SMS(propjetarju, "Malti/자체/kernel_VALUE") && kmand_CODE == 184) {
            if (Word_SMS(isem_valur_fiss, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(utent.화면너비(), 1); return true; }
            if (Word_SMS(isem_valur_fiss, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(utent.화면높이(), 1); return true; }
            if (Word_SMS(isem_valur_fiss, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(utent.밀리초(), 1); return true; }
            if (Word_SMS(isem_valur_fiss, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(utent.그림대기(), 1); return true; }
            if (Word_SMS(isem_valur_fiss, "사각형") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), koordinat_x = 빼기(1); 넣기(utent.사각형(koordinat_x, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(propjetarju, "java/net/InetAddress") || Word_SMS(propjetarju, "java/net/DatagramPacket") || Word_SMS(propjetarju, "java/net/DatagramSocket")) { 통신호출(propjetarju, isem_valur_fiss, 서술상수, kmand_CODE); return true; }
        if (Word_SMS(propjetarju, "java/lang/Thread")) { 가닥호출(isem_valur_fiss, 서술상수, kmand_CODE); return true; }
        if (Word_SMS(propjetarju, "java/lang/Object")) {
            if (Word_SMS(isem_valur_fiss, "<init>") && Word_SMS(서술상수, "()V") && kmand_CODE == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(isem_valur_fiss, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_data = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == byte_data ? 1 : 0, 1); return true; }
        }
        if (예외상수(propjetarju) != 0) {
            if (Word_SMS(isem_valur_fiss, "<init>") && kmand_CODE == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int prompt = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), oġġett_Referenza = 빼기(2);
                if (oġġett_VALUE(oġġett_Referenza, 9)) { 힙[oġġett_Referenza + 3] = prompt; 힙참조[oġġett_Referenza + 3] = 1; } return true;
            }
            if ((Word_SMS(isem_valur_fiss, "getMessage") || Word_SMS(isem_valur_fiss, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int oġġett_Referenza = 빼기(2); if (oġġett_VALUE(oġġett_Referenza, 9)) 넣기(힙[oġġett_Referenza + 3], 2); return true; }
        }
        if (Word_SMS(propjetarju, "java/lang/String")) {
            if (kmand_CODE == 182 && Word_SMS(isem_valur_fiss, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int kodifikar_isem = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), oġġett_Referenza = 빼기(2);
                if (!oġġett_VALUE(oġġett_Referenza, 1)) return true;
                if (kodifikar_isem != 0 && !글같음(kodifikar_isem, host_karattru("UTF-8"), false) && !글같음(kodifikar_isem, host_karattru("UTF8"), false) && !글같음(kodifikar_isem, host_karattru("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int entrata_COUNT = 힙[oġġett_Referenza + 1], 반환값 = alloka_Ħażna(20, entrata_COUNT * 3), 사용수 = 0; if (żball) return true;
                for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < entrata_COUNT; inner_join_pożizzjoni++) {
                    int kodiċi_tal_karattru = 힙[oġġett_Referenza + 2 + inner_join_pożizzjoni];
                    if (kodiċi_tal_karattru >= 0xd800 && kodiċi_tal_karattru <= 0xdbff && inner_join_pożizzjoni + 1 < entrata_COUNT && 힙[oġġett_Referenza + 3 + inner_join_pożizzjoni] >= 0xdc00 && 힙[oġġett_Referenza + 3 + inner_join_pożizzjoni] <= 0xdfff) kodiċi_tal_karattru = 0x10000 + ((kodiċi_tal_karattru - 0xd800) << 10) + 힙[oġġett_Referenza + 2 + ++inner_join_pożizzjoni] - 0xdc00;
                    else if (kodiċi_tal_karattru >= 0xd800 && kodiċi_tal_karattru <= 0xdfff) kodiċi_tal_karattru = '?';
                    if (kodiċi_tal_karattru < 128) 힙[반환값 + 2 + 사용수++] = kodiċi_tal_karattru;
                    else { int byte_COUNT = kodiċi_tal_karattru < 2048 ? 2 : kodiċi_tal_karattru < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((byte_COUNT == 2 ? 192 : byte_COUNT == 3 ? 224 : 240) | kodiċi_tal_karattru >> (6 * (byte_COUNT - 1))); for (int 비교자리 = byte_COUNT - 1; 비교자리 > 0; 비교자리--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | kodiċi_tal_karattru >> (6 * (비교자리 - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (kmand_CODE == 184 && Word_SMS(isem_valur_fiss, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(ċifra_karattru(빼기(1)), 2); return true; }
            if (kmand_CODE != 182) return false;
            if (Word_SMS(isem_valur_fiss, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int byte_data = 빼기(2), 첫값 = 빼기(2); if (oġġett_VALUE(첫값, 1)) 넣기(글같음(첫값, byte_data, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(isem_valur_fiss, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (oġġett_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(isem_valur_fiss, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int ttermina_pożizzjoni = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (oġġett_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? ttermina_pożizzjoni : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(isem_valur_fiss, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int byte_data = 빼기(2), 첫값 = 빼기(2); 넣기(ingħaqad_SMS(첫값, byte_data), 2); return true; }
            if (Word_SMS(isem_valur_fiss, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), hash_VALUE = 0; if (oġġett_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) hash_VALUE = hash_VALUE * 31 + 힙[첫값 + 2 + Loop_INDEX]; 넣기(hash_VALUE, 1); } return true; }
            if (Word_SMS(isem_valur_fiss, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (oġġett_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(propjetarju, "java/lang/Integer")) {
            if (kmand_CODE == 184 && Word_SMS(isem_valur_fiss, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int data_VALUE = 빼기(1), oġġett_Referenza = data_VALUE >= -128 && data_VALUE <= 127 ? Store_numru_sħiħ[data_VALUE + 128] : 0; if (oġġett_Referenza == 0) { oġġett_Referenza = alloka_Ħażna(12, 1); if (!żball) { 힙[oġġett_Referenza + 2] = data_VALUE; if (data_VALUE >= -128 && data_VALUE <= 127) Store_numru_sħiħ[data_VALUE + 128] = oġġett_Referenza; } } 넣기(oġġett_Referenza, 2); return true; }
            if (kmand_CODE == 183 && Word_SMS(isem_valur_fiss, "<init>") && Word_SMS(서술상수, "(I)V")) { int data_VALUE = 빼기(1), oġġett_Referenza = 빼기(2); if (oġġett_VALUE(oġġett_Referenza, 12)) 힙[oġġett_Referenza + 2] = data_VALUE; return true; }
            if (kmand_CODE == 182 && Word_SMS(isem_valur_fiss, "intValue") && Word_SMS(서술상수, "()I")) { int oġġett_Referenza = 빼기(2); if (oġġett_VALUE(oġġett_Referenza, 12)) 넣기(힙[oġġett_Referenza + 2], 1); return true; }
            if (kmand_CODE == 184 && Word_SMS(isem_valur_fiss, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(ċifra_karattru(빼기(1)), 2); return true; }
        }
        if (Word_SMS(propjetarju, "java/lang/Math") && kmand_CODE == 184) {
            if (Word_SMS(isem_valur_fiss, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(isem_valur_fiss, "min") || Word_SMS(isem_valur_fiss, "max")) && Word_SMS(서술상수, "(II)I")) { int byte_data = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(isem_valur_fiss, "min") ? (첫값 < byte_data ? 첫값 : byte_data) : (첫값 > byte_data ? 첫값 : byte_data), 1); return true; }
        }
        if (Word_SMS(propjetarju, "java/lang/System") && kmand_CODE == 184) {
            if (Word_SMS(isem_valur_fiss, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(isem_valur_fiss, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int entrata_COUNT = 빼기(1), destinazzjoni_VALUE_INDEX = 빼기(1), byte_data = 빼기(2), Bidu_pożizzjoni = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(byte_data)) {
                    int kategorija_CODE = 힙[첫값];
                    if (힙[byte_data] != kategorija_CODE || (kategorija_CODE != 2 && kategorija_CODE != 3 && (kategorija_CODE < 20 || kategorija_CODE > 23))) żball_VALUE("arraycopy type mismatch");
                    else if (entrata_COUNT < 0 || Bidu_pożizzjoni < 0 || destinazzjoni_VALUE_INDEX < 0 || Bidu_pożizzjoni > 힙[첫값 + 1] - entrata_COUNT || destinazzjoni_VALUE_INDEX > 힙[byte_data + 1] - entrata_COUNT) żball_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == byte_data && destinazzjoni_VALUE_INDEX > Bidu_pożizzjoni) { for (int Loop_INDEX = entrata_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) 힙[byte_data + 2 + destinazzjoni_VALUE_INDEX + Loop_INDEX] = 힙[첫값 + 2 + Bidu_pożizzjoni + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < entrata_COUNT && !żball; Loop_INDEX++) { int data_VALUE = 힙[첫값 + 2 + Bidu_pożizzjoni + Loop_INDEX]; if (kategorija_CODE != 3 || 배열저장가능(byte_data, data_VALUE)) 힙[byte_data + 2 + destinazzjoni_VALUE_INDEX + Loop_INDEX] = data_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(propjetarju, "java/util/ArrayList") || Word_SMS(propjetarju, "java/util/List") || Word_SMS(propjetarju, "java/util/HashMap") || Word_SMS(propjetarju, "java/util/Map")) {
            모음호출(propjetarju, isem_valur_fiss, 서술상수, kmand_CODE); return true;
        }
        return false;
    }
    static void 모음늘리기(int oġġett_Referenza, int 필요수) {
        int 이전값 = 힙[oġġett_Referenza + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int Li_Jmiss_pożizzjoni = 용량값 < 8 ? 8 : 용량값 * 2; if (Li_Jmiss_pożizzjoni < 필요수) Li_Jmiss_pożizzjoni = 필요수;
        int data_ARRAY = alloka_Ħażna(3, Li_Jmiss_pożizzjoni); if (żball) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 용량값; Loop_INDEX++) 힙[data_ARRAY + 2 + Loop_INDEX] = 힙[이전값 + 2 + Loop_INDEX];
        힙[oġġett_Referenza + 2] = data_ARRAY; 힙참조[oġġett_Referenza + 2] = 1;
    }
    static void 모음호출(int propjetarju, int isem_valur_fiss, int 서술상수, int kmand_CODE) {
        boolean 대응참조 = Word_SMS(propjetarju, "java/util/HashMap") || Word_SMS(propjetarju, "java/util/Map"); int kategorija_CODE = 대응참조 ? 11 : 10;
        if (Word_SMS(isem_valur_fiss, "<init>") && kmand_CODE == 183 && Word_SMS(서술상수, "()V")) { int oġġett_Referenza = 빼기(2); if (oġġett_VALUE(oġġett_Referenza, kategorija_CODE)) 모음늘리기(oġġett_Referenza, 8); return; }
        if (kmand_CODE != 182 && kmand_CODE != 185) { żball_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(isem_valur_fiss, "size") && Word_SMS(서술상수, "()I") || Word_SMS(isem_valur_fiss, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int oġġett_Referenza = 빼기(2); if (oġġett_VALUE(oġġett_Referenza, kategorija_CODE)) 넣기(Word_SMS(isem_valur_fiss, "size") ? 힙[oġġett_Referenza + 3] : 힙[oġġett_Referenza + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(isem_valur_fiss, "clear") && Word_SMS(서술상수, "()V")) { int oġġett_Referenza = 빼기(2); if (oġġett_VALUE(oġġett_Referenza, kategorija_CODE)) { int data_ARRAY = 힙[oġġett_Referenza + 2]; for (int Loop_INDEX = 0; Loop_INDEX < 힙[data_ARRAY + 1]; Loop_INDEX++) 힙[data_ARRAY + 2 + Loop_INDEX] = 0; 힙[oġġett_Referenza + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(isem_valur_fiss, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int data_VALUE = 빼기(2), oġġett_Referenza = 빼기(2); if (!oġġett_VALUE(oġġett_Referenza, 10)) return;
            int entrata_COUNT = 힙[oġġett_Referenza + 3]; 모음늘리기(oġġett_Referenza, entrata_COUNT + 1); if (!żball) { 힙[힙[oġġett_Referenza + 2] + 2 + entrata_COUNT] = data_VALUE; 힙[oġġett_Referenza + 3] = entrata_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(isem_valur_fiss, "get") || Word_SMS(isem_valur_fiss, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(isem_valur_fiss, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Word_SMS(isem_valur_fiss, "set"); int data_VALUE = 지정여부 ? 빼기(2) : 0, entrata_pożizzjoni = 빼기(1), oġġett_Referenza = 빼기(2);
            if (!oġġett_VALUE(oġġett_Referenza, 10)) return;
            int entrata_COUNT = 힙[oġġett_Referenza + 3], data_ARRAY = 힙[oġġett_Referenza + 2];
            if (entrata_pożizzjoni < 0 || entrata_pożizzjoni >= entrata_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[data_ARRAY + 2 + entrata_pożizzjoni];
            if (지정여부) 힙[data_ARRAY + 2 + entrata_pożizzjoni] = data_VALUE;
            if (Word_SMS(isem_valur_fiss, "remove")) { for (int Loop_INDEX = entrata_pożizzjoni + 1; Loop_INDEX < entrata_COUNT; Loop_INDEX++) 힙[data_ARRAY + 1 + Loop_INDEX] = 힙[data_ARRAY + 2 + Loop_INDEX]; 힙[data_ARRAY + 1 + entrata_COUNT] = 0; 힙[oġġett_Referenza + 3] = entrata_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(isem_valur_fiss, "get") || Word_SMS(isem_valur_fiss, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(isem_valur_fiss, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(isem_valur_fiss, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(isem_valur_fiss, "put"), neħħa = Word_SMS(isem_valur_fiss, "remove");
            int data_VALUE = 넣기여부 ? 빼기(2) : 0, tast_Referenza = 빼기(2), oġġett_Referenza = 빼기(2); if (!oġġett_VALUE(oġġett_Referenza, 11)) return;
            int entrata_COUNT = 힙[oġġett_Referenza + 3], data_ARRAY = 힙[oġġett_Referenza + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < entrata_COUNT; Loop_INDEX++) if (값같음(tast_Referenza, 힙[data_ARRAY + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[data_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(oġġett_Referenza, (entrata_COUNT + 1) * 2); data_ARRAY = 힙[oġġett_Referenza + 2]; 찾은여부 = entrata_COUNT; if (!żball) 힙[oġġett_Referenza + 3] = entrata_COUNT + 1; }
                if (!żball) { 힙[data_ARRAY + 2 + 2 * 찾은여부] = tast_Referenza; 힙[data_ARRAY + 3 + 2 * 찾은여부] = data_VALUE; }
            }
            if (neħħa && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < entrata_COUNT; Loop_INDEX++) { 힙[data_ARRAY + 2 * Loop_INDEX] = 힙[data_ARRAY + 2 + 2 * Loop_INDEX]; 힙[data_ARRAY + 1 + 2 * Loop_INDEX] = 힙[data_ARRAY + 3 + 2 * Loop_INDEX]; } 힙[data_ARRAY + 2 * entrata_COUNT] = 0; 힙[data_ARRAY + 1 + 2 * entrata_COUNT] = 0; 힙[oġġett_Referenza + 3] = entrata_COUNT - 1; }
            if (Word_SMS(isem_valur_fiss, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        żball_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int oġġett_Referenza) {
        if (!객체유효(oġġett_Referenza)) return false;
        if (잠금깊이[oġġett_Referenza] != 0 && 잠금주인[oġġett_Referenza] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        잠금주인[oġġett_Referenza] = 현재가닥 + 1; 잠금깊이[oġġett_Referenza]++; return true;
    }
    static void 잠금풀기(int oġġett_Referenza) {
        if (!객체유효(oġġett_Referenza)) return;
        if (잠금깊이[oġġett_Referenza] == 0 || 잠금주인[oġġett_Referenza] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[oġġett_Referenza] == 0) 잠금주인[oġġett_Referenza] = 0;
    }
    static boolean qaleb_fil() {
        fil_frejm[현재가닥] = frejm_INDEX;
        if (frejm_INDEX < 현재가닥 * 32) fil_stat[현재가닥] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < fil_COUNT; Loop_INDEX++) if (fil_stat[Loop_INDEX] == 2 && fil_stat[가닥대기[Loop_INDEX]] == 3) fil_stat[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= fil_COUNT; Loop_INDEX++) {
            int Li_Jmiss_pożizzjoni = (현재가닥 + Loop_INDEX) % fil_COUNT;
            if (fil_stat[Li_Jmiss_pożizzjoni] == 1) { 현재가닥 = Li_Jmiss_pożizzjoni; frejm_INDEX = fil_frejm[Li_Jmiss_pożizzjoni]; 바꿈요청 = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < fil_COUNT; Loop_INDEX++) if (fil_stat[Loop_INDEX] != 3) { żball_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int isem_valur_fiss, int 서술상수, int kmand_CODE) { Proċess_fil(isem_valur_fiss, 서술상수, kmand_CODE, false); }
    static void Proċess_fil(int isem_valur_fiss, int 서술상수, int kmand_CODE, boolean Malti) {
        if (kmand_CODE == 184 && Word_SMS(isem_valur_fiss, Malti ? "YIELD_attività" : "yield") && Word_SMS(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (kmand_CODE == 184 && Word_SMS(isem_valur_fiss, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(fil_oġġett[현재가닥], 2); return; }
        if (kmand_CODE == 183 && Word_SMS(isem_valur_fiss, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, Malti ? "(LMalti/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int mira_ADDRESS = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), oġġett_Referenza = 빼기(2);
            if (!객체유효(oġġett_Referenza)) return;
            if (힙[oġġett_Referenza] == 13) { 힙[oġġett_Referenza + 2] = mira_ADDRESS; 힙참조[oġġett_Referenza + 2] = 1; }
            else if (mira_ADDRESS != 0) żball_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (kmand_CODE == 182 && (Word_SMS(isem_valur_fiss, Malti ? "Bidu_attività" : "start") || Word_SMS(isem_valur_fiss, Malti ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || kmand_CODE == 182 && Word_SMS(isem_valur_fiss, Malti ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int oġġett_Referenza = 빼기(2); if (!객체유효(oġġett_Referenza)) return;
            int kont_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < fil_COUNT; Loop_INDEX++) if (fil_oġġett[Loop_INDEX] == oġġett_Referenza) kont_VALUE = Loop_INDEX;
            if (Word_SMS(isem_valur_fiss, Malti ? "살아있는가" : "isAlive")) { 넣기(kont_VALUE >= 0 && fil_stat[kont_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(isem_valur_fiss, Malti ? "기다리기" : "join")) { if (kont_VALUE >= 0 && fil_stat[kont_VALUE] != 3) { 가닥대기[현재가닥] = kont_VALUE; fil_stat[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (kont_VALUE >= 0) { 예외던짐(Malti ? 38 : 16, "thread already started"); return; }
            if (fil_COUNT == 4) { żball_VALUE("thread limit (4 including main)"); return; }
            int mira_ADDRESS = 힙[oġġett_Referenza] == 13 ? 힙[oġġett_Referenza + 2] : oġġett_Referenza;
            int fajl_INDEX = mira_ADDRESS > 0 && 힙[mira_ADDRESS] >= 32 ? isem_metodu(힙[mira_ADDRESS] - 32, Malti ? "eżegwixxa_attività" : "run", "()V") : -1;
            if (mira_ADDRESS != 0 && fajl_INDEX < 0) { żball_VALUE("Runnable.run required"); return; }
            kont_VALUE = fil_COUNT++; fil_oġġett[kont_VALUE] = oġġett_Referenza; fil_mira[kont_VALUE] = mira_ADDRESS;
            int frejm = kont_VALUE * 32; fil_frejm[kont_VALUE] = fajl_INDEX < 0 ? frejm - 1 : frejm; fil_stat[kont_VALUE] = fajl_INDEX < 0 ? 3 : 1;
            if (fajl_INDEX >= 0) { frejm_metodu[frejm] = fajl_INDEX; frejm_pożizzjoni[frejm] = metodu_Bidu[fajl_INDEX]; lokali_VALUE[frejm * 128] = mira_ADDRESS; lokali_TYPE[frejm * 128] = 2; }
            return;
        }
        żball_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], ADDRESS_SMS = new int[16];
    static int lokali_ADDRESS() { return ADDRESS_oġġett(0x7f000001); }
    static int ADDRESS_oġġett(int VALUE) { int oġġett_Referenza = alloka_Ħażna(14, 1); if (!żball) 힙[oġġett_Referenza + 2] = VALUE; return oġġett_Referenza; }
    static int 주소해독(int oġġett_Referenza) {
        if (oġġett_Referenza == 0 || 글같음(oġġett_Referenza, host_karattru("localhost"), false)) return 0x7f000001;
        if (!oġġett_VALUE(oġġett_Referenza, 1)) return 0;
        int data_VALUE = 0, 총수 = 0, ADDRESS_byte = 0, 자릿수 = 0, entrata_COUNT = 힙[oġġett_Referenza + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= entrata_COUNT; Loop_INDEX++) {
            int kodiċi_tal_karattru = Loop_INDEX == entrata_COUNT ? '.' : 힙[oġġett_Referenza + 2 + Loop_INDEX];
            if (kodiċi_tal_karattru == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } data_VALUE = data_VALUE << 8 | ADDRESS_byte; 총수++; ADDRESS_byte = 자릿수 = 0; }
            else { if (kodiċi_tal_karattru < '0' || kodiċi_tal_karattru > '9' || ++자릿수 > 3 || (ADDRESS_byte = ADDRESS_byte * 10 + kodiċi_tal_karattru - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return data_VALUE;
    }
    static int ADDRESS_karattru(int data_VALUE) {
        int entrata_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int ADDRESS_byte = data_VALUE >>> 이동비트 & 255;
            if (ADDRESS_byte >= 100) ADDRESS_SMS[entrata_COUNT++] = '0' + ADDRESS_byte / 100;
            if (ADDRESS_byte >= 10) ADDRESS_SMS[entrata_COUNT++] = '0' + ADDRESS_byte / 10 % 10;
            ADDRESS_SMS[entrata_COUNT++] = '0' + ADDRESS_byte % 10; if (이동비트 != 0) ADDRESS_SMS[entrata_COUNT++] = '.';
        }
        int oġġett_Referenza = alloka_Ħażna(1, entrata_COUNT); if (!żball) for (int Loop_INDEX = 0; Loop_INDEX < entrata_COUNT; Loop_INDEX++) 힙[oġġett_Referenza + 2 + Loop_INDEX] = ADDRESS_SMS[Loop_INDEX]; return oġġett_Referenza;
    }
    static void 통신호출(int propjetarju, int isem_valur_fiss, int 서술상수, int kmand_CODE) {
        if (Word_SMS(propjetarju, "java/net/InetAddress")) {
            if (kmand_CODE == 184 && Word_SMS(isem_valur_fiss, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(lokali_ADDRESS(), 2); return; }
            if (kmand_CODE == 184 && Word_SMS(isem_valur_fiss, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int data_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !żball) 넣기(ADDRESS_oġġett(data_VALUE), 2); return;
            }
            if (kmand_CODE == 182 && Word_SMS(isem_valur_fiss, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int oġġett_Referenza = 빼기(2); if (oġġett_VALUE(oġġett_Referenza, 14)) 넣기(ADDRESS_karattru(힙[oġġett_Referenza + 2]), 2); return; }
        }
        if (Word_SMS(propjetarju, "java/net/DatagramPacket")) {
            if (kmand_CODE == 183 && Word_SMS(isem_valur_fiss, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean destinazzjoni_VALUE_Referenza = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = destinazzjoni_VALUE_Referenza ? 빼기(1) : 0, ADDRESS_Referenza = destinazzjoni_VALUE_Referenza ? 빼기(2) : 0;
                int entrata_COUNT = 빼기(1), data_ARRAY = 빼기(2), oġġett_Referenza = 빼기(2);
                if (!oġġett_VALUE(oġġett_Referenza, 16) || !oġġett_VALUE(data_ARRAY, 20)) return;
                if (entrata_COUNT < 0 || entrata_COUNT > 힙[data_ARRAY + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (ADDRESS_Referenza != 0 && !oġġett_VALUE(ADDRESS_Referenza, 14)) return;
                힙[oġġett_Referenza + 2] = data_ARRAY; 힙참조[oġġett_Referenza + 2] = 1; 힙[oġġett_Referenza + 3] = entrata_COUNT;
                힙[oġġett_Referenza + 4] = ADDRESS_Referenza; 힙참조[oġġett_Referenza + 4] = 1; 힙[oġġett_Referenza + 5] = 접속번호; return;
            }
            if (kmand_CODE == 182 && Word_SMS(isem_valur_fiss, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int entrata_COUNT = 빼기(1), oġġett_Referenza = 빼기(2); if (!oġġett_VALUE(oġġett_Referenza, 16)) return;
                if (entrata_COUNT < 0 || entrata_COUNT > 힙[힙[oġġett_Referenza + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[oġġett_Referenza + 3] = entrata_COUNT; return;
            }
            if (kmand_CODE == 182 && (Word_SMS(isem_valur_fiss, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(isem_valur_fiss, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(isem_valur_fiss, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(isem_valur_fiss, "getPort") && Word_SMS(서술상수, "()I"))) {
                int oġġett_Referenza = 빼기(2); if (!oġġett_VALUE(oġġett_Referenza, 16)) return;
                int entrata_pożizzjoni = Word_SMS(isem_valur_fiss, "getData") ? 2 : Word_SMS(isem_valur_fiss, "getLength") ? 3 : Word_SMS(isem_valur_fiss, "getAddress") ? 4 : 5;
                넣기(힙[oġġett_Referenza + entrata_pożizzjoni], entrata_pożizzjoni == 2 || entrata_pożizzjoni == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(propjetarju, "java/net/DatagramSocket")) {
            if (kmand_CODE == 183 && Word_SMS(isem_valur_fiss, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int 접속번호 = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), oġġett_Referenza = 빼기(2); if (!oġġett_VALUE(oġġett_Referenza, 15)) return;
                if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = utent.fetaħ_netwerk(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[oġġett_Referenza + 2] = 열린파일번호; return;
            }
            if (kmand_CODE == 182 && Word_SMS(isem_valur_fiss, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), oġġett_Referenza = 빼기(2); if (!oġġett_VALUE(oġġett_Referenza, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[oġġett_Referenza + 3] = 밀리초값; return;
            }
            if (kmand_CODE == 182 && Word_SMS(isem_valur_fiss, "getLocalPort") && Word_SMS(서술상수, "()I")) { int oġġett_Referenza = 빼기(2); if (oġġett_VALUE(oġġett_Referenza, 15)) 넣기(힙[oġġett_Referenza + 2] < 0 ? -1 : utent.netwerk_port(힙[oġġett_Referenza + 2]), 1); return; }
            if (kmand_CODE == 182 && Word_SMS(isem_valur_fiss, "isClosed") && Word_SMS(서술상수, "()Z")) { int oġġett_Referenza = 빼기(2); if (oġġett_VALUE(oġġett_Referenza, 15)) 넣기(힙[oġġett_Referenza + 2] < 0 ? 1 : 0, 1); return; }
            if (kmand_CODE == 182 && Word_SMS(isem_valur_fiss, "close") && Word_SMS(서술상수, "()V")) { int oġġett_Referenza = 빼기(2); if (oġġett_VALUE(oġġett_Referenza, 15) && 힙[oġġett_Referenza + 2] >= 0) { utent.파일서술자닫기(힙[oġġett_Referenza + 2]); 힙[oġġett_Referenza + 2] = -1; } return; }
            if (kmand_CODE == 182 && (Word_SMS(isem_valur_fiss, "send") || Word_SMS(isem_valur_fiss, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int pakkett = 빼기(2), oġġett_Referenza = 빼기(2); if (!oġġett_VALUE(pakkett, 16) || !oġġett_VALUE(oġġett_Referenza, 15)) return;
                int data_ARRAY = 힙[pakkett + 2], 유효길이 = 힙[pakkett + 3], 열린파일번호 = 힙[oġġett_Referenza + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(isem_valur_fiss, "send")) {
                    if (!oġġett_VALUE(힙[pakkett + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = 힙[data_ARRAY + 2 + Loop_INDEX];
                    if (utent.bagħat_netwerk(열린파일번호, 힙[힙[pakkett + 4] + 2], 힙[pakkett + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int entrata_COUNT = utent.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (entrata_COUNT == -11) {
                        int 현재시각 = utent.밀리초();
                        if (힙[oġġett_Referenza + 4] == 0) 힙[oġġett_Referenza + 4] = 현재시각 + 1;
                        if (힙[oġġett_Referenza + 3] > 0 && 현재시각 - (힙[oġġett_Referenza + 4] - 1) >= 힙[oġġett_Referenza + 3]) { 힙[oġġett_Referenza + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(oġġett_Referenza, 2); 넣기(pakkett, 2); frejm_pożizzjoni[frejm_INDEX] = frejm_istruzzjoni[frejm_INDEX]; 바꿈요청 = true; return;
                    }
                    힙[oġġett_Referenza + 4] = 0;
                    if (entrata_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < entrata_COUNT; Loop_INDEX++) 힙[data_ARRAY + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    힙[pakkett + 3] = entrata_COUNT; 힙[pakkett + 4] = ADDRESS_oġġett(통신임시[513]); 힙참조[pakkett + 4] = 1; 힙[pakkett + 5] = 통신임시[512];
                }
                return;
            }
        }
        żball_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int oġġett_Referenza) {
        int 현재시각 = utent.밀리초();
        if (힙[oġġett_Referenza + 5] == 0) 힙[oġġett_Referenza + 5] = 현재시각 + 1;
        if (힙[oġġett_Referenza + 3] > 0 && 현재시각 - (힙[oġġett_Referenza + 5] - 1) >= 힙[oġġett_Referenza + 3]) { 힙[oġġett_Referenza + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        frejm_pożizzjoni[frejm_INDEX] = frejm_istruzzjoni[frejm_INDEX]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int propjetarju, int isem_valur_fiss, int 서술상수, int kmand_CODE) {
        boolean 수신쪽 = Word_SMS(propjetarju, "java/net/ServerSocket"), Stream = Word_SMS(propjetarju, "java/io/InputStream") || Word_SMS(propjetarju, "java/io/OutputStream");
        if (!Stream && kmand_CODE == 183 && Word_SMS(isem_valur_fiss, "<init>")) {
            boolean 빈여부 = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && Word_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { żball_VALUE("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), ADDRESS_Referenza = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, oġġett_Referenza = 빼기(2);
            if (!oġġett_VALUE(oġġett_Referenza, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !oġġett_VALUE(ADDRESS_Referenza, 14)) return;
            int netwerk_ADDRESS = 이름지정여부 ? 주소해독(ADDRESS_Referenza) : 주소지정여부 ? 힙[ADDRESS_Referenza + 2] : 0x7f000001;
            if (żball || 던진객체 != 0) return;
            int 열린파일번호 = utent.Stream_kontroll(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? utent.Stream_kontroll(1, 열린파일번호, 접속번호) : utent.AQBAD_Stream(열린파일번호, netwerk_ADDRESS, 접속번호);
            if (처리값 < 0) { utent.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[oġġett_Referenza + 2] = 열린파일번호; 힙[oġġett_Referenza + 4] = 접속번호; 힙[oġġett_Referenza + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!Stream && Word_SMS(isem_valur_fiss, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), oġġett_Referenza = 빼기(2); if (!oġġett_VALUE(oġġett_Referenza, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[oġġett_Referenza + 3] = 밀리초값; return; }
        if (!Stream && Word_SMS(isem_valur_fiss, "close") && Word_SMS(서술상수, "()V")) { int oġġett_Referenza = 빼기(2); if (oġġett_VALUE(oġġett_Referenza, 수신쪽 ? 18 : 17) && 힙[oġġett_Referenza + 2] >= 0) { utent.파일서술자닫기(힙[oġġett_Referenza + 2]); 힙[oġġett_Referenza + 2] = -1; } return; }
        if (!Stream && (Word_SMS(isem_valur_fiss, "getLocalPort") || Word_SMS(isem_valur_fiss, "getPort") || Word_SMS(isem_valur_fiss, "isClosed") || Word_SMS(isem_valur_fiss, "isConnected"))) {
            int oġġett_Referenza = 빼기(2); if (!oġġett_VALUE(oġġett_Referenza, 수신쪽 ? 18 : 17)) return;
            넣기(Word_SMS(isem_valur_fiss, "isClosed") ? 힙[oġġett_Referenza + 2] < 0 ? 1 : 0 : Word_SMS(isem_valur_fiss, "isConnected") ? 힙[oġġett_Referenza + 6] : Word_SMS(isem_valur_fiss, "getPort") ? 힙[oġġett_Referenza + 4] : 힙[oġġett_Referenza + 2] < 0 ? -1 : utent.Stream_kontroll(4, 힙[oġġett_Referenza + 2], 0), 1); return;
        }
        if (수신쪽 && Word_SMS(isem_valur_fiss, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int oġġett_Referenza = 빼기(2); if (!oġġett_VALUE(oġġett_Referenza, 18)) return; int 열린파일번호 = utent.Stream_kontroll(3, 힙[oġġett_Referenza + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(oġġett_Referenza)) 넣기(oġġett_Referenza, 2); return; }
            힙[oġġett_Referenza + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = alloka_Ħażna(17, 5); if (żball) { utent.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = utent.Stream_kontroll(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !Stream && ((Word_SMS(isem_valur_fiss, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(isem_valur_fiss, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int oġġett_Referenza = 빼기(2); if (!oġġett_VALUE(oġġett_Referenza, 17)) return; if (힙[oġġett_Referenza + 2] < 0 || 힙[oġġett_Referenza + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = alloka_Ħażna(19, 4); if (żball) return; 힙[반환값 + 2] = oġġett_Referenza; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(isem_valur_fiss, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Word_SMS(isem_valur_fiss, "read"), 쓰기여부 = Word_SMS(isem_valur_fiss, "write"), imblokka = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), 부분배열여부 = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int entrata_COUNT = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, data_ARRAY = imblokka || 부분배열여부 ? 빼기(2) : 0;
            int data_VALUE = 쓰기여부 && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, oġġett_Referenza = 빼기(2);
            if (!oġġett_VALUE(oġġett_Referenza, 19)) return; int 부모참조 = 힙[oġġett_Referenza + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(isem_valur_fiss, "close") && Word_SMS(서술상수, "()V")) { utent.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Word_SMS(isem_valur_fiss, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[oġġett_Referenza + 3] == 0)) { żball_VALUE("unsupported stream operation"); return; }
            if (imblokka || 부분배열여부) { if (!oġġett_VALUE(data_ARRAY, 20)) return; if (imblokka) entrata_COUNT = 힙[data_ARRAY + 1]; if (시작변위 < 0 || entrata_COUNT < 0 || 시작변위 > 힙[data_ARRAY + 1] - entrata_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else entrata_COUNT = 1;
            if (entrata_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[oġġett_Referenza + 4] : 0, 처리값 = 0;
            while (완료수 < entrata_COUNT) {
                처리값 = 읽기여부 ? utent.파일한바이트읽기(열린파일번호) : utent.파일한바이트쓰기(열린파일번호, imblokka || 부분배열여부 ? 힙[data_ARRAY + 2 + 시작변위 + 완료수] : data_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (imblokka || 부분배열여부)) 힙[data_ARRAY + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(imblokka || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[oġġett_Referenza + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(oġġett_Referenza, 2); if (imblokka || 부분배열여부) 넣기(data_ARRAY, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(entrata_COUNT, 1); } if (쓰기여부 && !(imblokka || 부분배열여부)) 넣기(data_VALUE, 1); } return;
            }
            힙[oġġett_Referenza + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : imblokka || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        żball_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int isem_valur_fiss) {
        if (Word_SMS(isem_valur_fiss, "Malti/자체/tieqa")) return 24;
        if (Word_SMS(isem_valur_fiss, "Malti/자체/tikketta")) return 26;
        if (Word_SMS(isem_valur_fiss, "Malti/자체/buttuna")) return 27;
        if (Word_SMS(isem_valur_fiss, "Malti/자체/qasam_ta_test")) return 28;
        if (Word_SMS(isem_valur_fiss, "Malti/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int isem_valur_fiss) {
        return 한국어화면종(isem_valur_fiss) != 0 || Word_SMS(isem_valur_fiss, "Malti/자체/화면구성요소") || Word_SMS(isem_valur_fiss, "Malti/자체/avveniment_kju");
    }
    static int 화면종(int isem_valur_fiss) {
        int 한국어종 = 한국어화면종(isem_valur_fiss); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(isem_valur_fiss, "javax/swing/JFrame")) return 24;
        if (Word_SMS(isem_valur_fiss, "javax/swing/JPanel")) return 25;
        if (Word_SMS(isem_valur_fiss, "javax/swing/JLabel")) return 26;
        if (Word_SMS(isem_valur_fiss, "javax/swing/JButton")) return 27;
        if (Word_SMS(isem_valur_fiss, "javax/swing/JTextField")) return 28;
        if (Word_SMS(isem_valur_fiss, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(isem_valur_fiss, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int isem_valur_fiss) {
        return 화면종(isem_valur_fiss) != 0 || Word_SMS(isem_valur_fiss, "java/awt/Component") || Word_SMS(isem_valur_fiss, "java/awt/Container") || Word_SMS(isem_valur_fiss, "javax/swing/JComponent") || Word_SMS(isem_valur_fiss, "javax/swing/AbstractButton") || Word_SMS(isem_valur_fiss, "javax/swing/text/JTextComponent") || Word_SMS(isem_valur_fiss, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int oġġett_Referenza) { if (!객체유효(oġġett_Referenza)) return false; if (힙[oġġett_Referenza] < 24 || 힙[oġġett_Referenza] > 28) { żball_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int oġġett_Referenza, int SMS_Referenza) {
        if (SMS_Referenza != 0 && !oġġett_VALUE(SMS_Referenza, 1)) return;
        int entrata_COUNT = SMS_Referenza == 0 ? 0 : 힙[SMS_Referenza + 1]; if (entrata_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < entrata_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = 힙[SMS_Referenza + 2 + Loop_INDEX];
        if (utent.화면글(힙[oġġett_Referenza + 2], 화면글임시, entrata_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[oġġett_Referenza + 3] = SMS_Referenza; 힙참조[oġġett_Referenza + 3] = 1;
    }
    static int 화면문자읽기(int oġġett_Referenza) {
        int kont_VALUE = 힙[oġġett_Referenza + 2], entrata_COUNT = utent.화면연결(8, kont_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (entrata_COUNT < 0) { żball_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < entrata_COUNT; Loop_INDEX++) { int 부호값 = utent.화면연결(9, kont_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = alloka_Ħażna(1, 사용수); if (!żball) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* Malti 객체를 직접 만들고 kernel_VALUE 화면 기능에 연결한다. Swing oġġett_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int propjetarju, int isem_valur_fiss, int 서술상수, int kmand_CODE) {
        if (Word_SMS(propjetarju, "Malti/자체/avveniment_kju")) {
            if (kmand_CODE == 184 && Word_SMS(isem_valur_fiss, "나중에실행") && Word_SMS(서술상수, "(LMalti/자체/실행할일;)V")) {
                int attività_azzjoni = 빼기(2); if (!객체유효(attività_azzjoni)) return;
                if (나중수 == 8) { żball_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = attività_azzjoni; return;
            }
            if (kmand_CODE == 184 && Word_SMS(isem_valur_fiss, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            żball_VALUE("지원하지 않는 Malti 화면 일정 호출"); return;
        }
        if (Word_SMS(propjetarju, "Malti/자체/동작알림")) {
            int 알림 = 빼기(2); if (!oġġett_VALUE(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Word_SMS(isem_valur_fiss, "avveniment_sors") && Word_SMS(서술상수, "()LMalti/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Word_SMS(isem_valur_fiss, "kmand_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Word_SMS(isem_valur_fiss, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else żball_VALUE("지원하지 않는 Malti azzjoni 알림 호출"); return;
        }
        if (kmand_CODE == 183 && Word_SMS(isem_valur_fiss, "<init>")) {
            int 종류 = 한국어화면종(propjetarju), 받이 = 0, 가로 = 0, Vertikali_pożizzjoni = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (utent.화면너비() - 폭) / 2; Vertikali_pożizzjoni = (utent.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIILMalti/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Vertikali_pożizzjoni = 빼기(1); 가로 = 빼기(1);
            } else { żball_VALUE("지원하지 않는 Malti 화면 생성자"); return; }
            int SMS = 빼기(2), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Vertikali_pożizzjoni < 0 || 폭 > utent.화면너비() - 가로 || 높이 > utent.화면높이() - Vertikali_pożizzjoni) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = utent.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { żball_VALUE("화면 element_VALUE 자리가 가득 찼습니다"); return; }
            힙[element_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = element_VALUE;
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = Vertikali_pożizzjoni; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; 힙[element_VALUE + 10] = 2;
            힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1;
            utent.화면연결(1, INDEX, 가로, Vertikali_pożizzjoni, 폭, 높이);
            if (종류 == 24) utent.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(element_VALUE, SMS); return;
        }
        if (kmand_CODE != 182) { żball_VALUE("잘못된 Malti 화면 호출 kmand"); return; }
        if (Word_SMS(isem_valur_fiss, "kiteb_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int SMS = 빼기(2), element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 화면문자설정(element_VALUE, SMS); return;
        }
        if (Word_SMS(isem_valur_fiss, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(화면문자읽기(element_VALUE), 2); return;
        }
        if (Word_SMS(isem_valur_fiss, "동작맡기기") && Word_SMS(서술상수, "(LMalti/자체/동작받이;)V")) {
            int 받이 = 빼기(2), element_VALUE = 빼기(2);
            if (화면객체(element_VALUE)) { 힙[element_VALUE + 4] = 받이; 힙참조[element_VALUE + 4] = 1; 힙[element_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(isem_valur_fiss, "żied_element") && Word_SMS(서술상수, "(LMalti/자체/화면구성요소;)V")) {
            int tfal_VALUE = 빼기(2), 부모 = 빼기(2); if (!화면객체(tfal_VALUE) || !화면객체(부모)) return;
            if (utent.화면연결(2, 힙[부모 + 2], 힙[tfal_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[tfal_VALUE + 11] = 부모; 힙참조[tfal_VALUE + 11] = 1; return;
        }
        if (Word_SMS(isem_valur_fiss, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Vertikali_pożizzjoni = 빼기(1), 가로 = 빼기(1), element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (utent.화면연결(1, 힙[element_VALUE + 2], 가로, Vertikali_pożizzjoni, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[element_VALUE + 5] = 가로; 힙[element_VALUE + 6] = Vertikali_pożizzjoni; 힙[element_VALUE + 7] = 폭; 힙[element_VALUE + 8] = 높이; return;
        }
        if ((Word_SMS(isem_valur_fiss, "wera_tieqa") || Word_SMS(isem_valur_fiss, "agħlaq")) && Word_SMS(서술상수, "()V")) {
            boolean viżibilità_VALUE = Word_SMS(isem_valur_fiss, "wera_tieqa"); int element_VALUE = 빼기(2); if (!화면객체(element_VALUE)) return;
            if (utent.화면연결(viżibilità_VALUE ? 3 : 4, 힙[element_VALUE + 2], viżibilità_VALUE ? 1 : 0, 0, 0, 0) < 0) { żball_VALUE("화면은 interattiv 명령에서 실행해야 합니다"); return; }
            힙[element_VALUE + 9] = viżibilità_VALUE ? 1 : 0; return;
        }
        if (Word_SMS(isem_valur_fiss, "보이는가") && Word_SMS(서술상수, "()Z")) { int element_VALUE = 빼기(2); if (화면객체(element_VALUE)) 넣기(힙[element_VALUE + 9], 1); return; }
        żball_VALUE("지원하지 않는 Malti 화면 metodu_VALUE");
    }
    static void 화면호출(int propjetarju, int isem_valur_fiss, int 서술상수, int kmand_CODE) {
        if (Word_SMS(propjetarju, "javax/swing/SwingUtilities")) {
            if (kmand_CODE == 184 && Word_SMS(isem_valur_fiss, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int oġġett_Referenza = 빼기(2); if (!객체유효(oġġett_Referenza)) return; if (나중수 == 8) { żball_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = oġġett_Referenza; return; }
            if (kmand_CODE == 184 && Word_SMS(isem_valur_fiss, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            żball_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(propjetarju, "java/awt/event/ActionEvent")) {
            int oġġett_Referenza = 빼기(2); if (!oġġett_VALUE(oġġett_Referenza, 29)) return;
            if (Word_SMS(isem_valur_fiss, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[oġġett_Referenza + 2], 2);
            else if (Word_SMS(isem_valur_fiss, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[oġġett_Referenza + 2]), 2);
            else if (Word_SMS(isem_valur_fiss, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else żball_VALUE("unsupported ActionEvent method"); return;
        }
        if (kmand_CODE == 183 && Word_SMS(isem_valur_fiss, "<init>")) {
            int COLUMNS = 0, SMS_Referenza = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_Referenza = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Referenza = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { żball_VALUE("unsupported Swing constructor"); return; }
            int oġġett_Referenza = 빼기(2); if (!객체유효(oġġett_Referenza)) return;
            if (힙[oġġett_Referenza] == 30) { żball_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(oġġett_Referenza) || COLUMNS < 0) return;
            int kont_VALUE = utent.화면연결(0, 힙[oġġett_Referenza] - 23, 0, 0, 0, 0);
            if (kont_VALUE < 1 || kont_VALUE > 32) { żball_VALUE("GUI widget slots exhausted"); return; }
            힙[oġġett_Referenza + 2] = kont_VALUE; 화면참조[kont_VALUE - 1] = oġġett_Referenza; 힙[oġġett_Referenza + 5] = 힙[oġġett_Referenza] == 24 ? 130 : 16; 힙[oġġett_Referenza + 6] = 힙[oġġett_Referenza] == 24 ? 110 : 16;
            힙[oġġett_Referenza + 7] = 힙[oġġett_Referenza] == 24 ? 380 : 220; 힙[oġġett_Referenza + 8] = 힙[oġġett_Referenza] == 24 ? 240 : 28; 힙[oġġett_Referenza + 10] = 1;
            화면문자설정(oġġett_Referenza, SMS_Referenza); return;
        }
        if (Word_SMS(isem_valur_fiss, "setText") || Word_SMS(isem_valur_fiss, "setTitle")) { int SMS_Referenza = 빼기(2), oġġett_Referenza = 빼기(2); if (화면객체(oġġett_Referenza) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(oġġett_Referenza, SMS_Referenza); return; }
        if (Word_SMS(isem_valur_fiss, "getText") || Word_SMS(isem_valur_fiss, "getTitle")) { int oġġett_Referenza = 빼기(2); if (화면객체(oġġett_Referenza) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(oġġett_Referenza), 2); return; }
        if (Word_SMS(isem_valur_fiss, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), oġġett_Referenza = 빼기(2); if (화면객체(oġġett_Referenza)) { 힙[oġġett_Referenza + 4] = 수신참조; 힙참조[oġġett_Referenza + 4] = 1; } return; }
        if (Word_SMS(isem_valur_fiss, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int oġġett_Referenza = 빼기(2); if (화면객체(oġġett_Referenza)) 넣기(oġġett_Referenza, 2); return; }
        if (Word_SMS(isem_valur_fiss, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Tqassim_Referenza = 빼기(2), oġġett_Referenza = 빼기(2); if (화면객체(oġġett_Referenza) && Tqassim_Referenza != 0) żball_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(isem_valur_fiss, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Tqassim_kondizzjoni = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Tqassim_kondizzjoni) 빼기(2);
            int tfal_Referenza = 빼기(2), oġġett_Referenza = 빼기(2); if (!화면객체(tfal_Referenza) || !화면객체(oġġett_Referenza)) return;
            if (utent.화면연결(2, 힙[oġġett_Referenza + 2], 힙[tfal_Referenza + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[tfal_Referenza + 11] = oġġett_Referenza; 힙참조[tfal_Referenza + 11] = 1; if (!Tqassim_kondizzjoni) 넣기(tfal_Referenza, 2); return;
        }
        if (Word_SMS(isem_valur_fiss, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), koordinat_x = 빼기(1), oġġett_Referenza = 빼기(2); if (!화면객체(oġġett_Referenza)) return;
            if (utent.화면연결(1, 힙[oġġett_Referenza + 2], koordinat_x, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[oġġett_Referenza + 5] = koordinat_x; 힙[oġġett_Referenza + 6] = 세로좌표; 힙[oġġett_Referenza + 7] = 너비; 힙[oġġett_Referenza + 8] = 높이; return;
        }
        if (Word_SMS(isem_valur_fiss, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), oġġett_Referenza = 빼기(2); if (!화면객체(oġġett_Referenza)) return;
            if (utent.화면연결(1, 힙[oġġett_Referenza + 2], 힙[oġġett_Referenza + 5], 힙[oġġett_Referenza + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[oġġett_Referenza + 7] = 너비; 힙[oġġett_Referenza + 8] = 높이; } return;
        }
        if (Word_SMS(isem_valur_fiss, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), oġġett_Referenza = 빼기(2); if (!화면객체(oġġett_Referenza)) return; if (상대배치 != 0) { żball_VALUE("only screen centering supported"); return; } 힙[oġġett_Referenza + 5] = (utent.화면너비() - 힙[oġġett_Referenza + 7]) / 2; 힙[oġġett_Referenza + 6] = (utent.화면높이() - 힙[oġġett_Referenza + 8]) / 2; utent.화면연결(1, 힙[oġġett_Referenza + 2], 힙[oġġett_Referenza + 5], 힙[oġġett_Referenza + 6], 힙[oġġett_Referenza + 7], 힙[oġġett_Referenza + 8]); return; }
        if (Word_SMS(isem_valur_fiss, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int politika = 빼기(1), oġġett_Referenza = 빼기(2); if (화면객체(oġġett_Referenza)) { if (politika < 0 || politika > 3) 예외던짐(9, "close policy"); else { 힙[oġġett_Referenza + 10] = politika; utent.화면연결(7, 힙[oġġett_Referenza + 2], politika, 0, 0, 0); } } return; }
        if (Word_SMS(isem_valur_fiss, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int data_VALUE = 빼기(1), oġġett_Referenza = 빼기(2); if (화면객체(oġġett_Referenza)) { int 처리값 = utent.화면연결(3, 힙[oġġett_Referenza + 2], data_VALUE, 0, 0, 0); if (처리값 < 0) żball_VALUE("Swing requires a standalone interactive command"); else 힙[oġġett_Referenza + 9] = data_VALUE; } return; }
        if (Word_SMS(isem_valur_fiss, "dispose") && Word_SMS(서술상수, "()V")) { int oġġett_Referenza = 빼기(2); if (화면객체(oġġett_Referenza)) { utent.화면연결(4, 힙[oġġett_Referenza + 2], 0, 0, 0, 0); 힙[oġġett_Referenza + 9] = 0; } return; }
        if (Word_SMS(isem_valur_fiss, "repaint") || Word_SMS(isem_valur_fiss, "validate")) { int oġġett_Referenza = 빼기(2); if (!화면객체(oġġett_Referenza) || !Word_SMS(서술상수, "()V")) return; utent.화면연결(1, 힙[oġġett_Referenza + 2], 힙[oġġett_Referenza + 5], 힙[oġġett_Referenza + 6], 힙[oġġett_Referenza + 7], 힙[oġġett_Referenza + 8]); return; }
        if (Word_SMS(isem_valur_fiss, "isVisible") && Word_SMS(서술상수, "()Z")) { int oġġett_Referenza = 빼기(2); if (화면객체(oġġett_Referenza)) 넣기(힙[oġġett_Referenza + 9], 1); return; }
        żball_VALUE("unsupported Swing method (native subset)");
    }
    static void 사건실행(int mira_ADDRESS, int 사건번호, boolean Malti) {
        if (mira_ADDRESS < 1 || 힙[mira_ADDRESS] < 32) { żball_VALUE("Java event listener required"); return; }
        int fajl_INDEX = isem_metodu(힙[mira_ADDRESS] - 32, 사건번호 == 0 ? (Malti ? "eżegwixxa_attività" : "run") : (Malti ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (Malti ? "(LMalti/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (fajl_INDEX < 0) { żball_VALUE("event callback missing"); return; }
        현재가닥 = 0; fil_COUNT = 1; frejm_INDEX = 0; fil_stat[0] = 1; frejm_Munzell[0] = 0; 틀잠금[0] = inizjala_frejm[0] = 0; 바꿈요청 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { lokali_VALUE[Loop_INDEX] = lokali_TYPE[Loop_INDEX] = 0; }
        frejm_metodu[0] = fajl_INDEX; frejm_pożizzjoni[0] = metodu_Bidu[fajl_INDEX]; lokali_VALUE[0] = mira_ADDRESS; lokali_TYPE[0] = 2;
        if (사건번호 != 0) { lokali_VALUE[1] = 사건번호; lokali_TYPE[1] = 2; }
        사건중 = true; eżegwixxa_kmand(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!żball) {
            if (나중수 > 0) { int mira_ADDRESS = 나중실행[0], Malti = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(mira_ADDRESS, 0, Malti != 0); continue; }
            if (utent.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = utent.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { żball_VALUE("GUI event I/O failed"); return; }
            int kont_VALUE = 사건번호 & 65535; if (kont_VALUE < 1 || kont_VALUE > 32) continue; int oġġett_Referenza = 화면참조[kont_VALUE - 1]; if (oġġett_Referenza == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[oġġett_Referenza + 10] != 0) 힙[oġġett_Referenza + 9] = 0;
                if (힙[oġġett_Referenza + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && 힙[화면참조[Loop_INDEX]] == 24) utent.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[oġġett_Referenza + 4] != 0) {
                int AQRANI_Referenza = alloka_Ħażna(29, 2); if (żball) return; 힙[AQRANI_Referenza + 2] = oġġett_Referenza; 힙[AQRANI_Referenza + 3] = 힙[oġġett_Referenza + 12]; 힙참조[AQRANI_Referenza + 2] = 1; 사건실행(힙[oġġett_Referenza + 4], AQRANI_Referenza, 힙[oġġett_Referenza + 12] != 0);
            }
        }
    }
    public static int serje() {
        if (utent.인수개수() == 1 && 자바도구.같음(utent.인수(0), "-version")) {
            utent.kiteb("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (utent.인수개수() < 1) { utent.kiteb("Usage: java CLASS [ARGS]\n"); return 2; }
        entrata_klassi_Definizzjoni = karga_klassi_Definizzjoni(host_karattru(utent.인수(0))); if (żball || entrata_klassi_Definizzjoni < 0) return 1;
        int entrata_punt_VALUE = isem_metodu(entrata_klassi_Definizzjoni, "serje", "()V");
        boolean 한국어진입 = entrata_punt_VALUE >= 0 && (metodu_aċċess[entrata_punt_VALUE] & 9) == 9;
        if (!한국어진입) entrata_punt_VALUE = isem_metodu(entrata_klassi_Definizzjoni, "main", "([Ljava/lang/String;)V");
        if (entrata_punt_VALUE < 0 || (metodu_aċċess[entrata_punt_VALUE] & 9) != 9) żball_VALUE("public static void serje() or main(String[] args) required");
        if (żball) return 1;
        int 인수 = alloka_Ħażna(3, utent.인수개수() - 1); ARRAY_element[인수] = -1;
        for (int 수 = 1; 수 < utent.인수개수() && !żball; 수++) 힙[인수 + 1 + 수] = host_karattru(utent.인수(수));
        frejm_INDEX = 0; frejm_metodu[0] = entrata_punt_VALUE; frejm_pożizzjoni[0] = metodu_Bidu[entrata_punt_VALUE]; lokali_VALUE[0] = 한국어진입 ? 0 : 인수; lokali_TYPE[0] = 한국어진입 ? 0 : 2;
        fil_stat[0] = 1; fil_oġġett[0] = alloka_Ħażna(13, 2);
        eżegwixxa_kmand(); if (!żball) 화면사건들(); return żball ? 1 : 0;
    }
}
