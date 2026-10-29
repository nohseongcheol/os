// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Ffeil/스택/cyfeiriad/cangen 경계를 Gweithredu_gorchymyn 중 검사한다. */
public final class 자바가상기계 {
    static int[] Ffeil = new int[16 * 16384], 임시파일 = new int[16384], ffeil_enw_SMS = new int[512];
    static int[] cysonyn_tag = new int[8192], 상가 = new int[8192], cysonyn_SECOND_VALUE = new int[8192], testun_cyfeiriad = new int[8192];
    static int[] dull_enw_SMS = new int[512], dull_TYPE = new int[512], dull_mynediad = new int[512], dull_perchennog = new int[512];
    static int[] dull_START = new int[512], dull_gorffen = new int[512], dull_pentwr = new int[512], 함수지역 = new int[512];
    static int[] dull_arg_COUNT = new int[512], dull_arg_TYPE = new int[8192], dull_return = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] lleol_VALUE = new int[16384], lleol_TYPE = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] ffrâm_dull = new int[128], ffrâm_safle = new int[128], ffrâm_pentwr = new int[128], ffrâm_cyfarwyddyd = new int[128], ymgychwyn_ffrâm = new int[128];
    static int[] Dosbarth_Diffiniad_enw = new int[16], Dosbarth_Diffiniad_newid_maint = new int[16], 종부모 = new int[16], Dosbarth_Diffiniad_cyflwr = new int[16], Dosbarth_slot_COUNT = new int[16], ymgychwyn_Dosbarth_Diffiniad = new int[16];
    static int[] Dosbarth_rhyngwyneb = new int[16 * 16], Dosbarth_rhyngwyneb_COUNT = new int[16];
    static int[] slot_enw = new int[512], slot_TYPE = new int[512], slot_perchennog = new int[512], slot_caniatâd = new int[512], slot_safle = new int[512], slot_data = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], ARAE_elfen = new int[32768], Store_cyfanrif = new int[256];
    static int Maint, 읽기위치, dull_COUNT, Dosbarth_enw, ffrâm_INDEX = -1, 힙끝 = 1, return_TYPE;
    static int Dosbarth_Diffiniad_COUNT, slot_COUNT, 잡기수, 현재읽는종, 던진객체, 잠시수, dangos_COUNT, Casgliad_COUNT;
    static int 현재가닥, edefyn_COUNT = 1, cofnod_Dosbarth_Diffiniad;
    static int[] edefyn_ffrâm = new int[4], edefyn_cyflwr = new int[4], edefyn_gwrthrych = new int[4], edefyn_targed = new int[4], 가닥대기 = new int[4];
    static boolean Gwall, newid_cais_HTTP;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], Dosbarth_edefyn = new int[16];

    static void methiant_VALUE(String Word_SMS) {
        if (Gwall) return;
        int ardal_cod = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) ardal_cod = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) ardal_cod = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) ardal_cod = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) ardal_cod = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) ardal_cod = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) ardal_cod = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) ardal_cod = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) ardal_cod = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) ardal_cod = 15;
        if (ardal_cod != 0 && ffrâm_INDEX >= 0) { 예외던짐(ardal_cod, Word_SMS); return; }
        defnyddiwr.Ysgrifennu("JVM error: "); defnyddiwr.Ysgrifennu(Word_SMS); defnyddiwr.ysgrifennu_nod_VALUE(10); Gwall = true;
    }
    static boolean clip(int Gweithredu_2, int hyd_VALUE) {
        if (Gweithredu_2 < 0 || Gweithredu_2 >= Ffeil.length || hyd_VALUE < 0) return false;
        int Dosbarth_Diffiniad = Gweithredu_2 / 16384;
        return Gweithredu_2 % 16384 <= Dosbarth_Diffiniad_newid_maint[Dosbarth_Diffiniad] && hyd_VALUE <= Dosbarth_Diffiniad_newid_maint[Dosbarth_Diffiniad] - Gweithredu_2 % 16384;
    }
    static int beit_VALUE() {
        if (!clip(읽기위치, 1)) { methiant_VALUE("truncated class file"); return 0; }
        return Ffeil[읽기위치++];
    }
    static int 짧은수() { return beit_VALUE() << 8 | beit_VALUE(); }
    static int cyfanrif() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int hyd_VALUE) { if (!clip(읽기위치, hyd_VALUE)) methiant_VALUE("invalid attribute size"); else 읽기위치 += hyd_VALUE; }
    static boolean gwirio_cysonyn(int 수, int 종류) {
        if (수 <= 0 || 수 >= cysonyn_tag.length || cysonyn_tag[수] != 종류) { methiant_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Gweithredu_2, int hyd_VALUE, String Word_SMS) {
        if (!clip(Gweithredu_2, hyd_VALUE)) return false;
        int 읽는자리 = Gweithredu_2, 끝 = Gweithredu_2 + hyd_VALUE;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_SMS.length(); Loop_INDEX++) {
            int cod_nod = Word_SMS.charAt(Loop_INDEX);
            if (cod_nod > 0 && cod_nod < 128) { if (읽는자리 >= 끝 || Ffeil[읽는자리++] != cod_nod) return false; }
            else if (cod_nod < 2048) {
                if (읽는자리 + 2 > 끝 || Ffeil[읽는자리++] != (192 | (cod_nod >> 6)) || Ffeil[읽는자리++] != (128 | (cod_nod & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Ffeil[읽는자리++] != (224 | (cod_nod >> 12)) || Ffeil[읽는자리++] != (128 | ((cod_nod >> 6) & 63)) || Ffeil[읽는자리++] != (128 | (cod_nod & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Word_SMS(int cysonyn_VALUE, String Word_SMS) { return gwirio_cysonyn(cysonyn_VALUE, 1) && 구간(상가[cysonyn_VALUE], cysonyn_SECOND_VALUE[cysonyn_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!gwirio_cysonyn(가, 1) || !gwirio_cysonyn(나, 1) || cysonyn_SECOND_VALUE[가] != cysonyn_SECOND_VALUE[나]) return false;
        for (int 수 = 0; 수 < cysonyn_SECOND_VALUE[가]; 수++) if (Ffeil[상가[가] + 수] != Ffeil[상가[나] + 수]) return false;
        return true;
    }
    static int Dosbarth_enw_SMS(int 수) { return gwirio_cysonyn(수, 7) && gwirio_cysonyn(상가[수], 1) ? 상가[수] : 0; }
    static int cyfeiriad_enw(int 수) { return gwirio_cysonyn(수, 12) && gwirio_cysonyn(상가[수], 1) ? 상가[수] : 0; }
    static int cyfeiriad_TYPE(int 수) { return gwirio_cysonyn(수, 12) && gwirio_cysonyn(cysonyn_SECOND_VALUE[수], 1) ? cysonyn_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean gwag_TYPE) {
        if (읽기위치 >= 끝) { methiant_VALUE("invalid descriptor"); return 0; }
        int VALUE = beit_VALUE();
        if (VALUE == 'V' && gwag_TYPE) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Gweithredu_2 = 읽기위치;
            while (읽기위치 < 끝 && Ffeil[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Gweithredu_2) methiant_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        methiant_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int SWYDDOGAETH_VALUE) {
        int 이전 = 읽기위치, 수 = dull_TYPE[SWYDDOGAETH_VALUE];
        if (!gwirio_cysonyn(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + cysonyn_SECOND_VALUE[수];
        if (beit_VALUE() != '(') methiant_VALUE("invalid method descriptor");
        int eitem_COUNT = 0;
        while (!Gwall && 읽기위치 < 끝 && Ffeil[읽기위치] != ')') {
            if (eitem_COUNT == 16) { methiant_VALUE("too many method arguments"); break; }
            dull_arg_TYPE[SWYDDOGAETH_VALUE * 16 + eitem_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || beit_VALUE() != ')') methiant_VALUE("invalid method descriptor");
        dull_return[SWYDDOGAETH_VALUE] = 서술형(끝, true); dull_arg_COUNT[SWYDDOGAETH_VALUE] = eitem_COUNT;
        if (읽기위치 != 끝) methiant_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return dull_perchennog[ffrâm_dull[ffrâm_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int eitem_COUNT = 짧은수();
        for (int 수 = 0; 수 < eitem_COUNT && !Gwall; 수++) { gwirio_cysonyn(상번호(), 1); 건너(cyfanrif()); }
    }
    static int gorchymyn_hyd(int VALUE) {
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
    static int safle_cyfanrif(int 읽는자리) {
        if (!clip(읽는자리, 4)) { methiant_VALUE("truncated bytecode operand"); return 0; }
        return Ffeil[읽는자리] << 24 | Ffeil[읽는자리 + 1] << 16 | Ffeil[읽는자리 + 2] << 8 | Ffeil[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Gweithredu_2, int 끝) {
        int VALUE = Ffeil[읽는자리], hyd_VALUE = gorchymyn_hyd(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_safle = 읽는자리 + 1;
            while ((BASE_safle - Gweithredu_2) % 4 != 0) BASE_safle++;
            if (끝 - BASE_safle < (VALUE == 170 ? 12 : 8)) return 0;
            int cofnod_COUNT = VALUE == 170 ? safle_cyfanrif(BASE_safle + 8) - safle_cyfanrif(BASE_safle + 4) + 1 : safle_cyfanrif(BASE_safle + 4);
            if (cofnod_COUNT < 0 || cofnod_COUNT > 2048) return 0;
            hyd_VALUE = BASE_safle - 읽는자리 + (VALUE == 170 ? 12 + 4 * cofnod_COUNT : 8 + 8 * cofnod_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_data = Ffeil[읽는자리 + 1]; hyd_VALUE = Word_data == 132 ? 6 : (Word_data == 21 || Word_data == 25 || Word_data == 54 || Word_data == 58) ? 4 : 0;
        }
        return hyd_VALUE > 0 && hyd_VALUE <= 끝 - 읽는자리 ? hyd_VALUE : 0;
    }
    static void gwirio_cyrchfan_VALUE(int cyrchfan_VALUE, int SWYDDOGAETH_VALUE) {
        if (cyrchfan_VALUE < dull_START[SWYDDOGAETH_VALUE] || cyrchfan_VALUE >= dull_gorffen[SWYDDOGAETH_VALUE] || 경계[cyrchfan_VALUE] != SWYDDOGAETH_VALUE + 1) methiant_VALUE("invalid branch target");
    }
    static void 클래스읽기(int Dosbarth_Diffiniad) {
        현재읽는종 = Dosbarth_Diffiniad; 읽기위치 = Dosbarth_Diffiniad * 16384; Maint = 읽기위치 + Dosbarth_Diffiniad_newid_maint[Dosbarth_Diffiniad];
        if (cyfanrif() != 0xcafebabe) { methiant_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), fersiwn_VALUE = 짧은수();
        if (fersiwn_VALUE < 45 || fersiwn_VALUE > 52 || 부판 != 0) { methiant_VALUE("supported class versions: 45..52, minor 0"); return; }
        int cysonyn_COUNT = 짧은수(), BASE_safle = Dosbarth_Diffiniad * 512;
        if (cysonyn_COUNT < 1 || cysonyn_COUNT > 512) { methiant_VALUE("constant pool limit (511)"); return; }
        for (int cofnod_COUNT = 1; cofnod_COUNT < cysonyn_COUNT && !Gwall; cofnod_COUNT++) {
            int 수 = BASE_safle + cofnod_COUNT, 종류 = beit_VALUE(); cysonyn_tag[수] = 종류;
            if (종류 == 1) { cysonyn_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(cysonyn_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = cyfanrif();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); cysonyn_SECOND_VALUE[수] = 상번호(); }
            else methiant_VALUE("unsupported constant type");
        }
        int hawl_VALUE = 짧은수();
        if ((hawl_VALUE & (0x2000 | 0x4000)) != 0) methiant_VALUE("annotation/enum class unsupported");
        Dosbarth_Diffiniad_enw[Dosbarth_Diffiniad] = Dosbarth_enw_SMS(상번호());
        종부모[Dosbarth_Diffiniad] = Dosbarth_enw_SMS(상번호());
        int rhyngwyneb_COUNT = 짧은수(); if (rhyngwyneb_COUNT > 16) { methiant_VALUE("interface count limit"); return; }
        Dosbarth_rhyngwyneb_COUNT[Dosbarth_Diffiniad] = rhyngwyneb_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < rhyngwyneb_COUNT; Loop_INDEX++) Dosbarth_rhyngwyneb[Dosbarth_Diffiniad * 16 + Loop_INDEX] = Dosbarth_enw_SMS(상번호());
        int maes_COUNT = 짧은수();
        if (maes_COUNT > 512 - slot_COUNT) { methiant_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < maes_COUNT && !Gwall; Loop_INDEX++) {
            int ffeil_INDEX = slot_COUNT++; slot_perchennog[ffeil_INDEX] = Dosbarth_Diffiniad; slot_caniatâd[ffeil_INDEX] = 짧은수(); slot_enw[ffeil_INDEX] = 상번호(); slot_TYPE[ffeil_INDEX] = 상번호();
            gwirio_cysonyn(slot_enw[ffeil_INDEX], 1); gwirio_cysonyn(slot_TYPE[ffeil_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[slot_TYPE[ffeil_INDEX]]; int ardal_cod = 서술형(읽기위치 + cysonyn_SECOND_VALUE[slot_TYPE[ffeil_INDEX]], false); 읽기위치 = 보존값;
            if ((slot_caniatâd[ffeil_INDEX] & 8) == 0) slot_safle[ffeil_INDEX] = Dosbarth_slot_COUNT[Dosbarth_Diffiniad]++;
            int priodoledd_data = 짧은수();
            for (int uno_mewnol_safle = 0; uno_mewnol_safle < priodoledd_data && !Gwall; uno_mewnol_safle++) {
                int enw_cysonyn = 상번호(), 유효길이 = cyfanrif();
                if (Word_SMS(enw_cysonyn, "ConstantValue") && 유효길이 == 2) {
                    int data_VALUE = 상번호();
                    if (ardal_cod == 1 && gwirio_cysonyn(data_VALUE, 3)) slot_data[ffeil_INDEX] = 상가[data_VALUE];
                    else if (ardal_cod == 2 && gwirio_cysonyn(data_VALUE, 8)) slot_data[ffeil_INDEX] = cysonyn_SMS(상가[data_VALUE]);
                } else 건너(유효길이);
            }
        }
        int eitem_COUNT = 짧은수();
        if (eitem_COUNT > 512 - dull_COUNT) { methiant_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < eitem_COUNT && !Gwall; Loop_INDEX++) {
            int 수 = dull_COUNT++; dull_perchennog[수] = Dosbarth_Diffiniad;
            dull_mynediad[수] = 짧은수(); dull_enw_SMS[수] = 상번호(); dull_TYPE[수] = 상번호();
            gwirio_cysonyn(dull_enw_SMS[수], 1); 서술읽기(수);
            if ((dull_mynediad[수] & 8) == 0) {
                if (dull_arg_COUNT[수] == 16) { methiant_VALUE("too many instance method arguments"); return; }
                for (int 비교자리 = dull_arg_COUNT[수]; 비교자리 > 0; 비교자리--) dull_arg_TYPE[수 * 16 + 비교자리] = dull_arg_TYPE[수 * 16 + 비교자리 - 1];
                dull_arg_TYPE[수 * 16] = 2; dull_arg_COUNT[수]++;
            }
            if ((dull_mynediad[수] & 0x100) != 0) methiant_VALUE("user native method unsupported");
            if (Word_SMS(dull_enw_SMS[수], "<clinit>")) ymgychwyn_Dosbarth_Diffiniad[Dosbarth_Diffiniad] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (dull_perchennog[앞] == Dosbarth_Diffiniad && 같은말(dull_enw_SMS[앞], dull_enw_SMS[수]) && 같은말(dull_TYPE[앞], dull_TYPE[수])) methiant_VALUE("duplicate method");
            int priodoledd_COUNT = 짧은수();
            for (int priodoledd_VALUE = 0; priodoledd_VALUE < priodoledd_COUNT && !Gwall; priodoledd_VALUE++) {
                int Enw = 상번호(), hyd_VALUE = cyfanrif(), Gweithredu_2 = 읽기위치;
                if (!clip(Gweithredu_2, hyd_VALUE)) { methiant_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Enw, "Code")) {
                    if (dull_START[수] != 0) methiant_VALUE("duplicate Code attribute");
                    dull_pentwr[수] = 짧은수(); 함수지역[수] = 짧은수(); int cod_hyd = cyfanrif();
                    if (dull_pentwr[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < dull_arg_COUNT[수]
                        || cod_hyd < 1 || cod_hyd > 8192) methiant_VALUE("method memory limits exceeded");
                    dull_START[수] = 읽기위치; 건너(cod_hyd); dull_gorffen[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { methiant_VALUE("exception table limit"); return; }
                    for (int uno_mewnol_safle = 0; uno_mewnol_safle < 잡는수; uno_mewnol_safle++) {
                        int gwall_cyfeiriad = 잡기수++; 잡기함수[gwall_cyfeiriad] = 수;
                        잡기시작[gwall_cyfeiriad] = dull_START[수] + 짧은수(); 잡기끝[gwall_cyfeiriad] = dull_START[수] + 짧은수();
                        잡기위치[gwall_cyfeiriad] = dull_START[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[gwall_cyfeiriad] = 부호값 == 0 ? 0 : Dosbarth_enw_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Gweithredu_2 + hyd_VALUE) methiant_VALUE("Code attribute size mismatch");
                } else 건너(hyd_VALUE);
            }
            if ((dull_mynediad[수] & 0x400) != 0) continue;
            if (dull_START[수] == 0) methiant_VALUE("missing Code attribute");
            int slot_cofnod = dull_START[수];
            while (slot_cofnod < dull_gorffen[수] && !Gwall) {
                int hyd_VALUE = 길이읽기(slot_cofnod, dull_START[수], dull_gorffen[수]);
                if (hyd_VALUE == 0) { methiant_VALUE("unsupported or truncated bytecode"); break; }
                경계[slot_cofnod] = 수 + 1; slot_cofnod += hyd_VALUE;
            }
            slot_cofnod = dull_START[수];
            while (slot_cofnod < dull_gorffen[수] && !Gwall) {
                int VALUE = Ffeil[slot_cofnod];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) gwirio_cyrchfan_VALUE(slot_cofnod + (short)(Ffeil[slot_cofnod + 1] << 8 | Ffeil[slot_cofnod + 2]), 수);
                if (VALUE == 200) gwirio_cyrchfan_VALUE(slot_cofnod + safle_cyfanrif(slot_cofnod + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = slot_cofnod + 1; while ((읽는자리 - dull_START[수]) % 4 != 0) 읽는자리++;
                    gwirio_cyrchfan_VALUE(slot_cofnod + safle_cyfanrif(읽는자리), 수);
                    int cofnod_COUNT = VALUE == 170 ? safle_cyfanrif(읽는자리 + 8) - safle_cyfanrif(읽는자리 + 4) + 1 : safle_cyfanrif(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int uno_mewnol_safle = 0; uno_mewnol_safle < cofnod_COUNT; uno_mewnol_safle++) gwirio_cyrchfan_VALUE(slot_cofnod + safle_cyfanrif(읽는자리 + uno_mewnol_safle * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                slot_cofnod += 길이읽기(slot_cofnod, dull_START[수], dull_gorffen[수]);
            }
            for (int uno_mewnol_safle = 0; uno_mewnol_safle < 잡기수; uno_mewnol_safle++) if (잡기함수[uno_mewnol_safle] == 수) {
                gwirio_cyrchfan_VALUE(잡기시작[uno_mewnol_safle], 수); gwirio_cyrchfan_VALUE(잡기위치[uno_mewnol_safle], 수);
                if (잡기끝[uno_mewnol_safle] != dull_gorffen[수]) gwirio_cyrchfan_VALUE(잡기끝[uno_mewnol_safle], 수);
                if (잡기시작[uno_mewnol_safle] >= 잡기끝[uno_mewnol_safle]) methiant_VALUE("invalid exception range");
            }
        }
        if (!Gwall) 속성건너();
        if (읽기위치 != Maint) methiant_VALUE("extra class file data");
    }
    static int dyrannu_Storio(int 종류, int hyd_VALUE) { return 새기억(종류, hyd_VALUE); }
    static boolean gwrthrych_VALUE(int cyfeiriad, int 종류) {
        if (!객체유효(cyfeiriad)) return false;
        if (힙[cyfeiriad] != 종류) { methiant_VALUE("object type mismatch"); return false; }
        return true;
    }
    static int cysonyn_SMS(int INDEX) {
        if (!gwirio_cysonyn(INDEX, 1)) return 0;
        if (testun_cyfeiriad[INDEX] != 0) return testun_cyfeiriad[INDEX];
        int cyfeiriad = dyrannu_Storio(1, cysonyn_SECOND_VALUE[INDEX]); if (Gwall) return 0;
        int 끝 = 상가[INDEX] + cysonyn_SECOND_VALUE[INDEX], 수 = 상가[INDEX], hyd_VALUE = 0;
        while (수 < 끝 && !Gwall) {
            int VALUE = Ffeil[수++];
            if (VALUE == 0) methiant_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Nesaf_eitem = Ffeil[수++];
                if ((Nesaf_eitem & 192) != 128) methiant_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Nesaf_eitem & 63;
                if (VALUE != 0 && VALUE < 128) methiant_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = Ffeil[수++], 나 = Ffeil[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) methiant_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (VALUE < 2048) methiant_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) methiant_VALUE("invalid modified UTF-8");
            힙[cyfeiriad + 2 + hyd_VALUE++] = VALUE;
        }
        힙[cyfeiriad + 1] = hyd_VALUE; testun_cyfeiriad[INDEX] = cyfeiriad; return cyfeiriad;
    }
    static int lletya_nod(String VALUE) {
        int cyfeiriad = dyrannu_Storio(1, VALUE.length()); if (Gwall) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) 힙[cyfeiriad + 2 + 수] = VALUE.charAt(수);
        return cyfeiriad;
    }
    static void ysgrifennu_SMS(int cyfeiriad) {
        if (cyfeiriad == 0) { defnyddiwr.Ysgrifennu("null"); return; }
        if (!gwrthrych_VALUE(cyfeiriad, 1)) return;
        for (int 수 = 0; 수 < 힙[cyfeiriad + 1]; 수++) defnyddiwr.ysgrifennu_nod_VALUE(힙[cyfeiriad + 2 + 수]);
    }
    static int digid_nod(int VALUE) {
        int cyfeiriad = dyrannu_Storio(1, 11); if (Gwall) return 0;
        int hyd_VALUE = 0;
        if (VALUE < 0) 힙[cyfeiriad + 2 + hyd_VALUE++] = '-'; else VALUE = -VALUE;
        int safle_INDEX = 1000000000; boolean Gweithredu_2 = false;
        while (safle_INDEX != 0) {
            int 수 = -(VALUE / safle_INDEX);
            if (수 != 0 || Gweithredu_2 || safle_INDEX == 1) { 힙[cyfeiriad + 2 + hyd_VALUE++] = '0' + 수; Gweithredu_2 = true; }
            VALUE %= safle_INDEX; safle_INDEX /= 10;
        }
        힙[cyfeiriad + 1] = hyd_VALUE; return cyfeiriad;
    }
    static int 정수해독(int cyfeiriad) {
        if (!gwrthrych_VALUE(cyfeiriad, 1)) return 0;
        int hyd_VALUE = 힙[cyfeiriad + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (hyd_VALUE > 0 && (힙[cyfeiriad + 2] == '-' || 힙[cyfeiriad + 2] == '+')) { 음수 = 힙[cyfeiriad + 2] == '-'; 수++; }
        if (수 == hyd_VALUE) methiant_VALUE("NumberFormatException");
        for (; 수 < hyd_VALUE && !Gwall; 수++) {
            int digid_VALUE = 힙[cyfeiriad + 2 + 수] - '0';
            if (digid_VALUE < 0 || digid_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && digid_VALUE > (음수 ? 8 : 7)) methiant_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - digid_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (Gwall) return;
        if (ffrâm_INDEX < 0 || ffrâm_pentwr[ffrâm_INDEX] >= dull_pentwr[ffrâm_dull[ffrâm_INDEX]]) { methiant_VALUE("operand stack overflow"); return; }
        int slot_cofnod = ffrâm_INDEX * 128 + ffrâm_pentwr[ffrâm_INDEX]++; 스택값[slot_cofnod] = VALUE; 스택형[slot_cofnod] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (Gwall) return 0;
        if (ffrâm_INDEX < 0 || ffrâm_pentwr[ffrâm_INDEX] < 1) { methiant_VALUE("operand stack underflow"); return 0; }
        int slot_cofnod = ffrâm_INDEX * 128 + --ffrâm_pentwr[ffrâm_INDEX]; return_TYPE = 스택형[slot_cofnod];
        if (TYPE_VALUE != 0 && return_TYPE != TYPE_VALUE) methiant_VALUE("operand type mismatch");
        if (return_TYPE == 2) diogelu_VALUE(스택값[slot_cofnod]);
        return 스택값[slot_cofnod];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[ffrâm_dull[ffrâm_INDEX]] || INDEX < 0 || lleol_TYPE[ffrâm_INDEX * 128 + INDEX] != TYPE_VALUE) { methiant_VALUE("invalid or uninitialized local"); return; }
        넣기(lleol_VALUE[ffrâm_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void ysgrifennu_lleol(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[ffrâm_dull[ffrâm_INDEX]] || INDEX < 0) { methiant_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); lleol_VALUE[ffrâm_INDEX * 128 + INDEX] = VALUE; lleol_TYPE[ffrâm_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int safle = ffrâm_safle[ffrâm_INDEX];
        if (safle < dull_START[ffrâm_dull[ffrâm_INDEX]] || safle >= dull_gorffen[ffrâm_dull[ffrâm_INDEX]]) { methiant_VALUE("instruction pointer out of range"); return 0; }
        ffrâm_safle[ffrâm_INDEX]++; return Ffeil[safle];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void symud_VALUE(int safle) {
        int SWYDDOGAETH_VALUE = ffrâm_dull[ffrâm_INDEX];
        if (safle < dull_START[SWYDDOGAETH_VALUE] || safle >= dull_gorffen[SWYDDOGAETH_VALUE] || 경계[safle] != SWYDDOGAETH_VALUE + 1) methiant_VALUE("invalid branch target");
        else ffrâm_safle[ffrâm_INDEX] = safle;
    }
    static void 호출(int SWYDDOGAETH_VALUE) {
        if (ffrâm_INDEX % 32 == 31) { methiant_VALUE("call stack limit (32)"); return; }
        int Nesaf_eitem = ffrâm_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lleol_TYPE[Nesaf_eitem * 128 + 수] = 0;
        for (int 수 = dull_arg_COUNT[SWYDDOGAETH_VALUE] - 1; 수 >= 0; 수--) {
            lleol_VALUE[Nesaf_eitem * 128 + 수] = 빼기(dull_arg_TYPE[SWYDDOGAETH_VALUE * 16 + 수]); lleol_TYPE[Nesaf_eitem * 128 + 수] = dull_arg_TYPE[SWYDDOGAETH_VALUE * 16 + 수];
        }
        if (Gwall) return;
        ffrâm_INDEX = Nesaf_eitem; ymgychwyn_ffrâm[ffrâm_INDEX] = 0; ffrâm_dull[ffrâm_INDEX] = SWYDDOGAETH_VALUE; ffrâm_safle[ffrâm_INDEX] = dull_START[SWYDDOGAETH_VALUE]; ffrâm_pentwr[ffrâm_INDEX] = 0;
    }
    static void return_mesur(int TYPE_VALUE) {
        if (TYPE_VALUE != dull_return[ffrâm_dull[ffrâm_INDEX]]) { methiant_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (ymgychwyn_ffrâm[ffrâm_INDEX] != 0) Dosbarth_Diffiniad_cyflwr[ymgychwyn_ffrâm[ffrâm_INDEX] - 1] = 2;
        if (틀잠금[ffrâm_INDEX] != 0) { 잠금풀기(틀잠금[ffrâm_INDEX]); 틀잠금[ffrâm_INDEX] = 0; }
        ffrâm_INDEX--; if (ffrâm_INDEX >= 현재가닥 * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] ffrwd_ffeil_enw = new int[64];
    static void ffeil_ffrwd_CALL(int perchennog_VALUE, int Enw, int fformat_VALUE, int Gorchymyn) {
        boolean Allbwn = Word_SMS(perchennog_VALUE, "java/io/FileOutputStream");
        int 종류 = Allbwn ? 6 : 5;
        if (Gorchymyn == 183 && Word_SMS(Enw, "<init>")) {
            boolean 이어 = false;
            if (Allbwn && Word_SMS(fformat_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(fformat_VALUE, "(Ljava/lang/String;)V")) { methiant_VALUE("unsupported file stream constructor"); return; }
            int ffeil_cofnod_enw = 빼기(2), ffrwd_VALUE = 빼기(2);
            if (!gwrthrych_VALUE(ffeil_cofnod_enw, 1) || !gwrthrych_VALUE(ffrwd_VALUE, 종류) || Gwall) return;
            if (힙[ffrwd_VALUE + 3] != 0) { methiant_VALUE("file stream already initialized"); return; }
            int hyd_VALUE = 힙[ffeil_cofnod_enw + 1];
            if (hyd_VALUE < 1 || hyd_VALUE > 63) { methiant_VALUE("invalid file name length"); return; }
            for (int slot_cofnod = 0; slot_cofnod < hyd_VALUE; slot_cofnod++) {
                int VALUE = 힙[ffeil_cofnod_enw + 2 + slot_cofnod];
                if (VALUE < 1) { methiant_VALUE("invalid file stream path"); return; }
                ffrwd_ffeil_enw[slot_cofnod] = VALUE;
            }
            ffrwd_ffeil_enw[hyd_VALUE] = 0;
            int 서술자 = defnyddiwr.파일서술자열기(ffrwd_ffeil_enw, Allbwn ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { methiant_VALUE("FileNotFoundException: file open failed"); return; }
            힙[ffrwd_VALUE + 2] = 서술자; 힙[ffrwd_VALUE + 3] = 1;
            return;
        }
        if (Gorchymyn != 182) { methiant_VALUE("invalid file stream invocation"); return; }
        if ((Allbwn && Word_SMS(Enw, "write") || !Allbwn && Word_SMS(Enw, "read"))
            && (Word_SMS(fformat_VALUE, Allbwn ? "([B)V" : "([B)I") || Word_SMS(fformat_VALUE, Allbwn ? "([BII)V" : "([BII)I"))) {
            boolean clip_VALUE = Word_SMS(fformat_VALUE, Allbwn ? "([BII)V" : "([BII)I");
            int cofnod_COUNT = clip_VALUE ? 빼기(1) : 0, 시작점 = clip_VALUE ? 빼기(1) : 0, data_ARAE = 빼기(2), gwrthrych_cyfeiriad = 빼기(2);
            if (!gwrthrych_VALUE(data_ARAE, 20) || !gwrthrych_VALUE(gwrthrych_cyfeiriad, 종류)) return;
            if (!clip_VALUE) cofnod_COUNT = 힙[data_ARAE + 1];
            if (시작점 < 0 || cofnod_COUNT < 0 || 시작점 > 힙[data_ARAE + 1] - cofnod_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[gwrthrych_cyfeiriad + 3] == 0 || 힙[gwrthrych_cyfeiriad + 2] < 0) { methiant_VALUE("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < cofnod_COUNT && !Gwall) {
                int 반환값 = Allbwn ? defnyddiwr.파일한바이트쓰기(힙[gwrthrych_cyfeiriad + 2], 힙[data_ARAE + 2 + 시작점 + 완료수]) : defnyddiwr.파일한바이트읽기(힙[gwrthrych_cyfeiriad + 2]);
                if (반환값 < 0) { methiant_VALUE(Allbwn ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Allbwn && 반환값 == 256) break;
                if (!Allbwn) 힙[data_ARAE + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!Allbwn) 넣기(cofnod_COUNT != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (Allbwn && Word_SMS(Enw, "flush") && Word_SMS(fformat_VALUE, "()V")) { int gwrthrych_cyfeiriad = 빼기(2); if (gwrthrych_VALUE(gwrthrych_cyfeiriad, 종류) && 힙[gwrthrych_cyfeiriad + 2] < 0) methiant_VALUE("IOException: stream closed"); return; }
        int Gweithrediad = -1, VALUE = 0;
        if (Word_SMS(Enw, "close") && Word_SMS(fformat_VALUE, "()V")) Gweithrediad = 0;
        if (!Allbwn && Word_SMS(Enw, "read") && Word_SMS(fformat_VALUE, "()I")) Gweithrediad = 1;
        if (Allbwn && Word_SMS(Enw, "write") && Word_SMS(fformat_VALUE, "(I)V")) { Gweithrediad = 2; VALUE = 빼기(1); }
        if (Gweithrediad < 0) { methiant_VALUE("unsupported file stream method"); return; }
        int ffrwd_VALUE = 빼기(2);
        if (!gwrthrych_VALUE(ffrwd_VALUE, 종류) || Gwall) return;
        if (힙[ffrwd_VALUE + 3] == 0) { methiant_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[ffrwd_VALUE + 2];
        if (Gweithrediad == 0) {
            if (서술자 >= 0 && defnyddiwr.파일서술자닫기(서술자) < 0) methiant_VALUE("IOException: close failed");
            힙[ffrwd_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { methiant_VALUE("IOException: stream closed"); return; }
        if (Gweithrediad == 1) {
            int mesur = defnyddiwr.파일한바이트읽기(서술자);
            if (mesur < -1) methiant_VALUE("IOException: read failed"); else 넣기(mesur == 256 ? -1 : mesur, 1);
        } else if (defnyddiwr.파일한바이트쓰기(서술자, VALUE) != 1) methiant_VALUE("IOException: write failed");
    }
    static void CALL_dull(int INDEX, int Gorchymyn) {
        if (INDEX <= 0 || INDEX >= cysonyn_tag.length || (cysonyn_tag[INDEX] != 10 && cysonyn_tag[INDEX] != 11)) { methiant_VALUE("invalid method reference"); return; }
        int perchennog_VALUE = Dosbarth_enw_SMS(상가[INDEX]), Enw = cyfeiriad_enw(cysonyn_SECOND_VALUE[INDEX]), fformat_VALUE = cyfeiriad_TYPE(cysonyn_SECOND_VALUE[INDEX]);
        if (Gwall) return;
        if (기본호출(perchennog_VALUE, Enw, fformat_VALUE, Gorchymyn)) return;
        if (Word_SMS(perchennog_VALUE, "java/io/FileInputStream") || Word_SMS(perchennog_VALUE, "java/io/FileOutputStream")) {
            ffeil_ffrwd_CALL(perchennog_VALUE, Enw, fformat_VALUE, Gorchymyn); return;
        }
        if (Gorchymyn == 184 && Word_SMS(perchennog_VALUE, "java/lang/Integer") && Word_SMS(Enw, "parseInt") && Word_SMS(fformat_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Gorchymyn == 182 && Word_SMS(perchennog_VALUE, "java/io/PrintStream") && (Word_SMS(Enw, "println") || Word_SMS(Enw, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(fformat_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(fformat_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(fformat_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(fformat_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(fformat_VALUE, "()V") || !Word_SMS(Enw, "println")) methiant_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) methiant_VALUE("invalid PrintStream receiver");
            if (Gwall) return;
            if (TYPE_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (TYPE_VALUE == 2) defnyddiwr.Ysgrifennu(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) defnyddiwr.ysgrifennu_nod_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) ysgrifennu_SMS(VALUE);
            if (Word_SMS(Enw, "println")) defnyddiwr.ysgrifennu_nod_VALUE(10);
            return;
        }
        if (Gorchymyn == 182 && Word_SMS(perchennog_VALUE, "java/lang/String")) {
            if (Word_SMS(Enw, "length") && Word_SMS(fformat_VALUE, "()I")) {
                int cyfeiriad = 빼기(2); if (gwrthrych_VALUE(cyfeiriad, 1)) 넣기(힙[cyfeiriad + 1], 1); return;
            }
            if (Word_SMS(Enw, "charAt") && Word_SMS(fformat_VALUE, "(I)C")) {
                int is_ysgrif_VALUE = 빼기(1), cyfeiriad = 빼기(2);
                if (gwrthrych_VALUE(cyfeiriad, 1)) {
                    if (is_ysgrif_VALUE < 0 || is_ysgrif_VALUE >= 힙[cyfeiriad + 1]) methiant_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[cyfeiriad + 2 + is_ysgrif_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(perchennog_VALUE, "java/lang/StringBuilder")) {
            if (Gorchymyn == 183 && Word_SMS(Enw, "<init>") && Word_SMS(fformat_VALUE, "()V")) { gwrthrych_VALUE(빼기(2), 4); return; }
            if (Gorchymyn == 182 && Word_SMS(Enw, "toString") && Word_SMS(fformat_VALUE, "()Ljava/lang/String;")) {
                int cyfeiriad = 빼기(2); if (gwrthrych_VALUE(cyfeiriad, 4)) 넣기(힙[cyfeiriad + 2] == 0 ? lletya_nod("") : 힙[cyfeiriad + 2], 2); return;
            }
            if (Gorchymyn == 182 && Word_SMS(Enw, "append")) {
                int Testun = 0;
                if (Word_SMS(fformat_VALUE, "(I)Ljava/lang/StringBuilder;")) Testun = digid_nod(빼기(1));
                else if (Word_SMS(fformat_VALUE, "(Z)Ljava/lang/StringBuilder;")) Testun = lletya_nod(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(fformat_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Testun = dyrannu_Storio(1, 1); if (!Gwall) 힙[Testun + 2] = VALUE & 65535;
                }
                else if (Word_SMS(fformat_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Testun = 빼기(2); if (Testun == 0) Testun = lletya_nod("null"); }
                else { methiant_VALUE("unsupported StringBuilder append"); return; }
                int cyfeiriad = 빼기(2); if (!gwrthrych_VALUE(cyfeiriad, 4) || !gwrthrych_VALUE(Testun, 1)) return;
                int 앞 = 힙[cyfeiriad + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], BACK_VALUE_hyd = 힙[Testun + 1];
                int 새글 = dyrannu_Storio(1, 앞길이 + BACK_VALUE_hyd); if (Gwall) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < BACK_VALUE_hyd; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[Testun + 2 + 수];
                힙[cyfeiriad + 2] = 새글; 넣기(cyfeiriad, 2); return;
            }
        }
        int Dosbarth_Diffiniad = FIND_Dosbarth_Diffiniad(perchennog_VALUE); if (Dosbarth_Diffiniad < 0 || Gwall) return;
        int ffeil_INDEX = FIND_dull(Dosbarth_Diffiniad, Enw, fformat_VALUE);
        if (ffeil_INDEX < 0) {
            for (int cod_nod = Dosbarth_Diffiniad, cofnod_COUNT = 0; cod_nod >= 0 && cofnod_COUNT < 16; cofnod_COUNT++, cod_nod = 부모종(cod_nod))
                if (Word_SMS(종부모[cod_nod], "java/lang/Thread")) { 가닥호출(Enw, fformat_VALUE, Gorchymyn); return; }
            methiant_VALUE("NoSuchMethodError"); return;
        }
        if (((dull_mynediad[ffeil_INDEX] & 8) != 0) != (Gorchymyn == 184)) { methiant_VALUE("method static/instance mismatch"); return; }
        if (Gorchymyn == 184) { if (!ymgychwyn(dull_perchennog[ffeil_INDEX], ffrâm_cyfarwyddyd[ffrâm_INDEX])) return; }
        else {
            int 읽는자리 = ffrâm_pentwr[ffrâm_INDEX] - dull_arg_COUNT[ffeil_INDEX];
            if (읽는자리 < 0 || 스택형[ffrâm_INDEX * 128 + 읽는자리] != 2) { methiant_VALUE("invalid method receiver"); return; }
            int gwrthrych_cyfeiriad = 스택값[ffrâm_INDEX * 128 + 읽는자리];
            if (!객체유효(gwrthrych_cyfeiriad)) return;
            if (힙[gwrthrych_cyfeiriad] < 32 || !종포함(힙[gwrthrych_cyfeiriad] - 32, perchennog_VALUE)) { methiant_VALUE("method receiver type mismatch"); return; }
            if (Gorchymyn != 183) ffeil_INDEX = FIND_dull(힙[gwrthrych_cyfeiriad] - 32, Enw, fformat_VALUE);
        }
        if (ffeil_INDEX < 0 || (dull_mynediad[ffeil_INDEX] & 0x400) != 0) { methiant_VALUE("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((dull_mynediad[ffeil_INDEX] & 32) != 0) {
            if (Gorchymyn == 184) { int cod_nod = dull_perchennog[ffeil_INDEX]; if (종잠금[cod_nod] == 0) 종잠금[cod_nod] = dyrannu_Storio(8, 0); 잠금참조 = 종잠금[cod_nod]; }
            else 잠금참조 = 스택값[ffrâm_INDEX * 128 + ffrâm_pentwr[ffrâm_INDEX] - dull_arg_COUNT[ffeil_INDEX]];
            if (!잠금얻기(잠금참조)) { if (!Gwall) ffrâm_safle[ffrâm_INDEX] = ffrâm_cyfarwyddyd[ffrâm_INDEX]; return; }
        }
        호출(ffeil_INDEX); if (!Gwall) 틀잠금[ffrâm_INDEX] = 잠금참조;
    }
    static boolean 배열저장가능(int ARAE_cyfeiriad, int data_VALUE) {
        if (data_VALUE == 0 || ARAE_elfen[ARAE_cyfeiriad] == 0) return true;
        boolean 성공여부 = ARAE_elfen[ARAE_cyfeiriad] == -1 ? (data_VALUE > 0 && data_VALUE < 힙끝 && 힙[data_VALUE] == 1) : 맞는객체(data_VALUE, ARAE_elfen[ARAE_cyfeiriad]);
        if (!성공여부 && !Gwall) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int ARAE_slot(int cyfeiriad, int is_ysgrif_VALUE, int TYPE_VALUE) {
        if (!gwrthrych_VALUE(cyfeiriad, TYPE_VALUE)) return 0;
        if (is_ysgrif_VALUE < 0 || is_ysgrif_VALUE >= 힙[cyfeiriad + 1]) { methiant_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return cyfeiriad + 2 + is_ysgrif_VALUE;
    }
    static void Gweithredu_gorchymyn() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (Gwall) { if (던진객체 != 0) dolen_eithriad(); if (Gwall || ffrâm_INDEX < 현재가닥 * 32) break; }
            if (ffrâm_INDEX < 현재가닥 * 32 || newid_cais_HTTP || --조각 == 0) { if (!newid_edefyn()) break; 조각 = 100; }
            if (ffrâm_INDEX == 0 && Dosbarth_Diffiniad_cyflwr[cofnod_Dosbarth_Diffiniad] != 2 && !ymgychwyn(cofnod_Dosbarth_Diffiniad, ffrâm_safle[ffrâm_INDEX])) continue;
            if (ffrâm_INDEX == 현재가닥 * 32 && 현재가닥 != 0 && (dull_mynediad[ffrâm_dull[ffrâm_INDEX]] & 32) != 0 && 틀잠금[ffrâm_INDEX] == 0) {
                int gwrthrych_cyfeiriad = edefyn_targed[현재가닥]; if (!잠금얻기(gwrthrych_cyfeiriad)) { if (Gwall) break; continue; } 틀잠금[ffrâm_INDEX] = gwrthrych_cyfeiriad;
            }
            잠시수 = 0;
            if (--남음 == 0) { methiant_VALUE("instruction limit (500000)"); break; }
            int Gweithredu_2 = ffrâm_safle[ffrâm_INDEX]; ffrâm_cyfarwyddyd[ffrâm_INDEX] = Gweithredu_2; int VALUE = 명바();
            if (Gwall) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = dull_perchennog[ffrâm_dull[ffrâm_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= cysonyn_tag.length) methiant_VALUE("invalid ldc constant");
                else if (cysonyn_tag[수] == 3) 넣기(상가[수], 1);
                else if (cysonyn_tag[수] == 8) 넣기(cysonyn_SMS(상가[수]), 2);
                else methiant_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { ysgrifennu_lleol(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { ysgrifennu_lleol(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { ysgrifennu_lleol(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int cofnod_safle = 빼기(1), gwrthrych_cyfeiriad = 빼기(2), ardal_cod = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && gwrthrych_cyfeiriad > 0 && gwrthrych_cyfeiriad < 힙끝 && 힙[gwrthrych_cyfeiriad] == 21) ardal_cod = 21;
                int 읽는자리 = ARAE_slot(gwrthrych_cyfeiriad, cofnod_safle, ardal_cod); if (!Gwall) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int cofnod_cyfeiriad = 빼기(VALUE == 83 ? 2 : 1), cofnod_safle = 빼기(1), gwrthrych_cyfeiriad = 빼기(2), ardal_cod = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && gwrthrych_cyfeiriad > 0 && gwrthrych_cyfeiriad < 힙끝 && 힙[gwrthrych_cyfeiriad] == 21) ardal_cod = 21;
                int 읽는자리 = ARAE_slot(gwrthrych_cyfeiriad, cofnod_safle, ardal_cod);
                if (!Gwall && ardal_cod == 3 && !배열저장가능(gwrthrych_cyfeiriad, cofnod_cyfeiriad)) continue;
                if (!Gwall) 힙[읽는자리] = ardal_cod == 20 ? (byte)cofnod_cyfeiriad : ardal_cod == 21 ? cofnod_cyfeiriad & 1 : ardal_cod == 22 ? (char)cofnod_cyfeiriad : ardal_cod == 23 ? (short)cofnod_cyfeiriad : cofnod_cyfeiriad;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { pentwr_cyfarwyddyd(VALUE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), mesur = 0;
                if ((VALUE == 108 || VALUE == 112) && 나 == 0) { methiant_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) mesur = 가 + 나;
                if (VALUE == 100) mesur = 가 - 나;
                if (VALUE == 104) mesur = 가 * 나;
                if (VALUE == 108) mesur = 가 / 나;
                if (VALUE == 112) mesur = 가 % 나;
                if (VALUE == 120) mesur = 가 << 나;
                if (VALUE == 122) mesur = 가 >> 나;
                if (VALUE == 124) mesur = 가 >>> 나;
                if (VALUE == 126) mesur = 가 & 나;
                if (VALUE == 128) mesur = 가 | 나;
                if (VALUE == 130) mesur = 가 ^ 나;
                넣기(mesur, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int lleol_cwmpas = 명바(), 증분 = (byte)명바(); 지역읽기(lleol_cwmpas, 1); 넣기(빼기(1) + 증분, 1); ysgrifennu_lleol(lleol_cwmpas, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int cyrchfan_VALUE = Gweithredu_2 + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int 나 = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == 나 : VALUE == 160 || VALUE == 166 ? 가 != 나 : VALUE == 161 ? 가 < 나 : VALUE == 162 ? 가 >= 나 : VALUE == 163 ? 가 > 나 : 가 <= 나;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) symud_VALUE(cyrchfan_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { return_mesur(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, Gweithredu_2); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { methiant_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_dull(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(Dosbarth_enw_SMS(명상수()), Gweithredu_2); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int ardal_cod = 3, cydran = 0;
                if (VALUE == 188) { int 임시값 = 명바(); ardal_cod = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else cydran = Dosbarth_enw_SMS(명상수());
                if (ardal_cod == 0) { methiant_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), gwrthrych_cyfeiriad = dyrannu_Storio(ardal_cod, 유효길이); if (!Gwall) ARAE_elfen[gwrthrych_cyfeiriad] = cydran; 넣기(gwrthrych_cyfeiriad, 2); continue;
            }
            if (VALUE == 190) {
                int gwrthrych_cyfeiriad = 빼기(2);
                if (객체유효(gwrthrych_cyfeiriad)) { int 비교자리 = 힙[gwrthrych_cyfeiriad]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) methiant_VALUE("not an array"); else 넣기(힙[gwrthrych_cyfeiriad + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int gwrthrych_cyfeiriad = 빼기(2); if (객체유효(gwrthrych_cyfeiriad)) { if (힙[gwrthrych_cyfeiriad] != 9) methiant_VALUE("athrow requires supported Throwable"); else { 던진객체 = gwrthrych_cyfeiriad; Gwall = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int enw_cysonyn = Dosbarth_enw_SMS(명상수()), gwrthrych_cyfeiriad = 빼기(2); boolean MATCH = 맞는객체(gwrthrych_cyfeiriad, enw_cysonyn);
                if (VALUE == 193) 넣기(gwrthrych_cyfeiriad != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !Gwall) methiant_VALUE("ClassCastException"); 넣기(gwrthrych_cyfeiriad, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = Gweithredu_2 + 1, ffeil_INDEX = ffrâm_dull[ffrâm_INDEX], bysell_cyfeiriad = 빼기(1);
                while ((읽는자리 - dull_START[ffeil_INDEX]) % 4 != 0) 읽는자리++;
                int targed_ADDRESS = safle_cyfanrif(읽는자리);
                if (VALUE == 170) { int 낮은값 = safle_cyfanrif(읽는자리 + 4), 높은값 = safle_cyfanrif(읽는자리 + 8); if (bysell_cyfeiriad >= 낮은값 && bysell_cyfeiriad <= 높은값) targed_ADDRESS = safle_cyfanrif(읽는자리 + 12 + (bysell_cyfeiriad - 낮은값) * 4); }
                else { int 총수 = safle_cyfanrif(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (safle_cyfanrif(읽는자리 + 8 + Loop_INDEX * 8) == bysell_cyfeiriad) targed_ADDRESS = safle_cyfanrif(읽는자리 + 12 + Loop_INDEX * 8); }
                symud_VALUE(Gweithredu_2 + targed_ADDRESS); continue;
            }
            if (VALUE == 200) { symud_VALUE(Gweithredu_2 + safle_cyfanrif(Gweithredu_2 + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int gwrthrych_cyfeiriad = 빼기(2);
                if (VALUE == 195) 잠금풀기(gwrthrych_cyfeiriad);
                else if (!잠금얻기(gwrthrych_cyfeiriad) && !Gwall) { 넣기(gwrthrych_cyfeiriad, 2); ffrâm_safle[ffrâm_INDEX] = Gweithredu_2; }
                continue;
            }
            if (VALUE == 196) {
                int gorchymyn_cod = 명바(), cofnod_safle = 명짧();
                if (gorchymyn_cod == 21 || gorchymyn_cod == 25) 지역읽기(cofnod_safle, gorchymyn_cod == 21 ? 1 : 2);
                else if (gorchymyn_cod == 54 || gorchymyn_cod == 58) ysgrifennu_lleol(cofnod_safle, gorchymyn_cod == 54 ? 1 : 2);
                else if (gorchymyn_cod == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(cofnod_safle, 1); 넣기(빼기(1) + DELTA_VALUE, 1); ysgrifennu_lleol(cofnod_safle, 1); }
                else methiant_VALUE("unsupported wide opcode");
                continue;
            }
            methiant_VALUE("unsupported bytecode");
        }
    }
    static int FIND_Dosbarth_Diffiniad(int Enw) {
        for (int Loop_INDEX = 0; Loop_INDEX < Dosbarth_Diffiniad_COUNT; Loop_INDEX++) if (Dosbarth_Diffiniad_enw[Loop_INDEX] != 0 && 같은말(Dosbarth_Diffiniad_enw[Loop_INDEX], Enw)) return Loop_INDEX;
        return llwyth_Dosbarth_Diffiniad(cysonyn_SMS(Enw));
    }
    static int llwyth_Dosbarth_Diffiniad(int enw_testun) {
        if (!gwrthrych_VALUE(enw_testun, 1)) return -1;
        int hyd_VALUE = 힙[enw_testun + 1];
        if (hyd_VALUE < 1 || hyd_VALUE > 505 || Dosbarth_Diffiniad_COUNT == 16) { methiant_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < hyd_VALUE; Loop_INDEX++) { int cod_nod = 힙[enw_testun + 2 + Loop_INDEX]; ffeil_enw_SMS[Loop_INDEX] = cod_nod == '/' ? '.' : cod_nod; }
        ffeil_enw_SMS[hyd_VALUE] = '.'; ffeil_enw_SMS[hyd_VALUE + 1] = 'c'; ffeil_enw_SMS[hyd_VALUE + 2] = 'l'; ffeil_enw_SMS[hyd_VALUE + 3] = 'a'; ffeil_enw_SMS[hyd_VALUE + 4] = 's'; ffeil_enw_SMS[hyd_VALUE + 5] = 's'; ffeil_enw_SMS[hyd_VALUE + 6] = 0;
        int Maint = defnyddiwr.파일읽기(ffeil_enw_SMS, 임시파일);
        if (Maint < 0) { methiant_VALUE("ClassNotFoundException"); return -1; }
        int Dosbarth_Diffiniad = Dosbarth_Diffiniad_COUNT++; Dosbarth_Diffiniad_newid_maint[Dosbarth_Diffiniad] = Maint;
        for (int Loop_INDEX = 0; Loop_INDEX < Maint; Loop_INDEX++) Ffeil[Dosbarth_Diffiniad * 16384 + Loop_INDEX] = 임시파일[Loop_INDEX];
        클래스읽기(Dosbarth_Diffiniad); if (Gwall) return -1;
        int go_iawn_data = cysonyn_SMS(Dosbarth_Diffiniad_enw[Dosbarth_Diffiniad]);
        if (!글같음(go_iawn_data, enw_testun, true)) { methiant_VALUE("class name does not match file"); return -1; }
        int 부모 = 종부모[Dosbarth_Diffiniad];
        if (부모 != 0 && !Word_SMS(부모, "java/lang/Object") && !Word_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_Dosbarth_Diffiniad(부모);
            if (Gwall || 위 < 0) return -1;
            int 읽는자리 = 위, cam_COUNT = 0;
            while (읽는자리 >= 0 && cam_COUNT++ < 16) {
                if (읽는자리 == Dosbarth_Diffiniad) { methiant_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = Dosbarth_slot_COUNT[위];
            for (int ffeil_INDEX = 0; ffeil_INDEX < slot_COUNT; ffeil_INDEX++) if (slot_perchennog[ffeil_INDEX] == Dosbarth_Diffiniad && (slot_caniatâd[ffeil_INDEX] & 8) == 0) slot_safle[ffeil_INDEX] += 시작변위;
            Dosbarth_slot_COUNT[Dosbarth_Diffiniad] += 시작변위;
        }
        return Dosbarth_Diffiniad;
    }
    static int 부모종(int Dosbarth_Diffiniad) {
        int Enw = 종부모[Dosbarth_Diffiniad];
        for (int Loop_INDEX = 0; Loop_INDEX < Dosbarth_Diffiniad_COUNT; Loop_INDEX++) if (Enw != 0 && Dosbarth_Diffiniad_enw[Loop_INDEX] != 0 && 같은말(Dosbarth_Diffiniad_enw[Loop_INDEX], Enw)) return Loop_INDEX;
        return -1;
    }
    static int FIND_dull(int Dosbarth_Diffiniad, int Enw, int fformat_VALUE) {
        for (int 깊이 = 0; Dosbarth_Diffiniad >= 0 && 깊이 < 16; 깊이++, Dosbarth_Diffiniad = 부모종(Dosbarth_Diffiniad)) {
            for (int Loop_INDEX = 0; Loop_INDEX < dull_COUNT; Loop_INDEX++) if (dull_perchennog[Loop_INDEX] == Dosbarth_Diffiniad && 같은말(dull_enw_SMS[Loop_INDEX], Enw) && 같은말(dull_TYPE[Loop_INDEX], fformat_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int enw_dull(int Dosbarth_Diffiniad, String Enw, String fformat_VALUE) {
        for (int 깊이 = 0; Dosbarth_Diffiniad >= 0 && 깊이 < 16; 깊이++, Dosbarth_Diffiniad = 부모종(Dosbarth_Diffiniad))
            for (int Loop_INDEX = 0; Loop_INDEX < dull_COUNT; Loop_INDEX++) if (dull_perchennog[Loop_INDEX] == Dosbarth_Diffiniad && Word_SMS(dull_enw_SMS[Loop_INDEX], Enw) && Word_SMS(dull_TYPE[Loop_INDEX], fformat_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int Enw) { return Ffeil[상가[Enw]] == 'L' || Ffeil[상가[Enw]] == '[' ? 2 : 1; }
    static boolean ymgychwyn(int Dosbarth_Diffiniad, int gorchymyn_START) {
        if (Dosbarth_Diffiniad < 0 || Gwall) return false;
        if (Dosbarth_Diffiniad_cyflwr[Dosbarth_Diffiniad] == 3) { methiant_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (Dosbarth_Diffiniad_cyflwr[Dosbarth_Diffiniad] == 1 && Dosbarth_edefyn[Dosbarth_Diffiniad] != 현재가닥) { ffrâm_safle[ffrâm_INDEX] = gorchymyn_START; newid_cais_HTTP = true; return false; }
        if (Dosbarth_Diffiniad_cyflwr[Dosbarth_Diffiniad] != 0) return true;
        int 위 = 부모종(Dosbarth_Diffiniad);
        if (위 >= 0 && !ymgychwyn(위, gorchymyn_START)) return false;
        Dosbarth_Diffiniad_cyflwr[Dosbarth_Diffiniad] = 1; Dosbarth_edefyn[Dosbarth_Diffiniad] = 현재가닥;
        if (ymgychwyn_Dosbarth_Diffiniad[Dosbarth_Diffiniad] != 0) {
            ffrâm_safle[ffrâm_INDEX] = gorchymyn_START;
            호출(ymgychwyn_Dosbarth_Diffiniad[Dosbarth_Diffiniad] - 1); if (!Gwall) ymgychwyn_ffrâm[ffrâm_INDEX] = Dosbarth_Diffiniad + 1;
            return false;
        }
        Dosbarth_Diffiniad_cyflwr[Dosbarth_Diffiniad] = 2; return true;
    }
    static void 필드호출(int INDEX, int Gorchymyn, int Gweithredu_2) {
        if (!gwirio_cysonyn(INDEX, 9)) return;
        int perchennog_VALUE = Dosbarth_enw_SMS(상가[INDEX]), Enw = cyfeiriad_enw(cysonyn_SECOND_VALUE[INDEX]), fformat_VALUE = cyfeiriad_TYPE(cysonyn_SECOND_VALUE[INDEX]);
        if (Word_SMS(perchennog_VALUE, "java/lang/System") && (Word_SMS(Enw, "out") || Word_SMS(Enw, "err")) && Word_SMS(fformat_VALUE, "Ljava/io/PrintStream;") && Gorchymyn == 178) { 넣기(-1, 2); return; }
        int Dosbarth_Diffiniad = FIND_Dosbarth_Diffiniad(perchennog_VALUE); if (Dosbarth_Diffiniad < 0 || Gwall) return;
        int 찾음 = -1;
        for (int 읽는자리 = Dosbarth_Diffiniad, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int ffeil_INDEX = 0; ffeil_INDEX < slot_COUNT; ffeil_INDEX++) if (slot_perchennog[ffeil_INDEX] == 읽는자리 && 같은말(slot_enw[ffeil_INDEX], Enw) && 같은말(slot_TYPE[ffeil_INDEX], fformat_VALUE)) 찾음 = ffeil_INDEX;
        if (찾음 < 0) { methiant_VALUE("NoSuchFieldError"); return; }
        boolean statig_VALUE = Gorchymyn == 178 || Gorchymyn == 179;
        if (statig_VALUE != ((slot_caniatâd[찾음] & 8) != 0)) { methiant_VALUE("field static/instance mismatch"); return; }
        if (statig_VALUE && !ymgychwyn(slot_perchennog[찾음], Gweithredu_2)) return;
        int TYPE_VALUE = 형종류(fformat_VALUE), VALUE = 0;
        if (Gorchymyn == 179 || Gorchymyn == 181) VALUE = 빼기(TYPE_VALUE);
        if (statig_VALUE) { if (Gorchymyn == 178) 넣기(slot_data[찾음], TYPE_VALUE); else if (!Gwall) slot_data[찾음] = VALUE; return; }
        int gwrthrych_cyfeiriad = 빼기(2);
        if (!객체유효(gwrthrych_cyfeiriad)) return;
        if (힙[gwrthrych_cyfeiriad] < 32 || !종포함(힙[gwrthrych_cyfeiriad] - 32, perchennog_VALUE)) { methiant_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = gwrthrych_cyfeiriad + 2 + slot_safle[찾음];
        if (Gorchymyn == 180) 넣기(힙[보관칸], TYPE_VALUE);
        else if (!Gwall) { 힙[보관칸] = VALUE; 힙참조[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Dosbarth_Diffiniad, int Enw) {
        for (int 중첩깊이 = 0; Dosbarth_Diffiniad >= 0 && 중첩깊이 < 16; 중첩깊이++, Dosbarth_Diffiniad = 부모종(Dosbarth_Diffiniad)) {
            if (같은말(Dosbarth_Diffiniad_enw[Dosbarth_Diffiniad], Enw) || (종부모[Dosbarth_Diffiniad] != 0 && 같은말(종부모[Dosbarth_Diffiniad], Enw))) return true;
            for (int uno_mewnol_safle = 0; uno_mewnol_safle < Dosbarth_rhyngwyneb_COUNT[Dosbarth_Diffiniad]; uno_mewnol_safle++) if (같은말(Dosbarth_rhyngwyneb[Dosbarth_Diffiniad * 16 + uno_mewnol_safle], Enw)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int beit_data, boolean LLWYBR) {
        if (첫값 == beit_data) return true;
        if (첫값 <= 0 || beit_data <= 0 || 힙[첫값] != 1 || 힙[beit_data] != 1 || 힙[첫값 + 1] != 힙[beit_data + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) {
            int cyfesuryn_x = 힙[첫값 + 2 + Loop_INDEX], Y_cyfesuryn = 힙[beit_data + 2 + Loop_INDEX];
            if (LLWYBR) { if (cyfesuryn_x == '.') cyfesuryn_x = '/'; if (Y_cyfesuryn == '.') Y_cyfesuryn = '/'; }
            if (cyfesuryn_x != Y_cyfesuryn) return false;
        }
        return true;
    }
    static boolean 객체유효(int gwrthrych_cyfeiriad) {
        if (gwrthrych_cyfeiriad == 0) { methiant_VALUE("NullPointerException"); return false; }
        if (gwrthrych_cyfeiriad < 1 || gwrthrych_cyfeiriad >= 힙끝 || 힙폭[gwrthrych_cyfeiriad] < 2 || 힙[gwrthrych_cyfeiriad] == 0) { methiant_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void diogelu_VALUE(int gwrthrych_cyfeiriad) {
        if (gwrthrych_cyfeiriad > 0 && gwrthrych_cyfeiriad < 힙끝 && 힙폭[gwrthrych_cyfeiriad] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = gwrthrych_cyfeiriad;
    }
    static void sioe_VALUE(int gwrthrych_cyfeiriad) {
        if (gwrthrych_cyfeiriad > 0 && gwrthrych_cyfeiriad < 힙끝 && 힙폭[gwrthrych_cyfeiriad] >= 2 && 힙[gwrthrych_cyfeiriad] != 0 && 힙표시[gwrthrych_cyfeiriad] == 0) {
            힙표시[gwrthrych_cyfeiriad] = 1; 표시대기[dangos_COUNT++] = gwrthrych_cyfeiriad;
        }
    }
    static void 수거() {
        dangos_COUNT = 0; Casgliad_COUNT++;
        for (int gwirio_safle = 1; gwirio_safle < 힙끝; gwirio_safle += 힙폭[gwirio_safle]) 힙표시[gwirio_safle] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < testun_cyfeiriad.length; Loop_INDEX++) sioe_VALUE(testun_cyfeiriad[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < slot_COUNT; Loop_INDEX++) if ((slot_caniatâd[Loop_INDEX] & 8) != 0 && 형종류(slot_TYPE[Loop_INDEX]) == 2) sioe_VALUE(slot_data[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < edefyn_COUNT; 임시값++) {
            sioe_VALUE(edefyn_gwrthrych[임시값]); sioe_VALUE(edefyn_targed[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? ffrâm_INDEX : edefyn_ffrâm[임시값];
            for (int ffeil_INDEX = 임시값 * 32; ffeil_INDEX <= 꼭대기자리; ffeil_INDEX++) {
                for (int uno_mewnol_safle = 0; uno_mewnol_safle < 함수지역[ffrâm_dull[ffeil_INDEX]]; uno_mewnol_safle++) if (lleol_TYPE[ffeil_INDEX * 128 + uno_mewnol_safle] == 2) sioe_VALUE(lleol_VALUE[ffeil_INDEX * 128 + uno_mewnol_safle]);
                for (int uno_mewnol_safle = 0; uno_mewnol_safle < ffrâm_pentwr[ffeil_INDEX]; uno_mewnol_safle++) if (스택형[ffeil_INDEX * 128 + uno_mewnol_safle] == 2) sioe_VALUE(스택값[ffeil_INDEX * 128 + uno_mewnol_safle]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) sioe_VALUE(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) sioe_VALUE(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_cyfanrif.length; Loop_INDEX++) sioe_VALUE(Store_cyfanrif[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Dosbarth_Diffiniad_COUNT; Loop_INDEX++) sioe_VALUE(종잠금[Loop_INDEX]);
        for (int gwirio_safle = 1; gwirio_safle < 힙끝; gwirio_safle += 힙폭[gwirio_safle]) if (잠금깊이[gwirio_safle] > 0) sioe_VALUE(gwirio_safle);
        sioe_VALUE(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) sioe_VALUE(잠시참조[Loop_INDEX]);
        while (dangos_COUNT > 0) {
            int gwrthrych_cyfeiriad = 표시대기[--dangos_COUNT], ardal_cod = 힙[gwrthrych_cyfeiriad];
            for (int Loop_INDEX = gwrthrych_cyfeiriad + 2; Loop_INDEX < gwrthrych_cyfeiriad + 힙폭[gwrthrych_cyfeiriad]; Loop_INDEX++) if (ardal_cod == 3 || ardal_cod == 4 || 힙참조[Loop_INDEX] != 0) sioe_VALUE(힙[Loop_INDEX]);
        }
        for (int gwirio_safle = 1; gwirio_safle < 힙끝; gwirio_safle += 힙폭[gwirio_safle]) if (힙표시[gwirio_safle] == 0) 힙[gwirio_safle] = 0;
        for (int gwirio_safle = 1; gwirio_safle < 힙끝; gwirio_safle += 힙폭[gwirio_safle]) if (힙[gwirio_safle] == 0) {
            while (gwirio_safle + 힙폭[gwirio_safle] < 힙끝 && 힙[gwirio_safle + 힙폭[gwirio_safle]] == 0) { int Nesaf_safle = gwirio_safle + 힙폭[gwirio_safle]; 힙폭[gwirio_safle] += 힙폭[Nesaf_safle]; 힙폭[Nesaf_safle] = 0; }
            if (gwirio_safle + 힙폭[gwirio_safle] == 힙끝) { 힙끝 = gwirio_safle; break; }
        }
    }
    static int 새기억(int 종류, int hyd_VALUE) {
        if (hyd_VALUE < 0) { methiant_VALUE("NegativeArraySizeException"); return 0; }
        if (hyd_VALUE > 힙.length - 3) { methiant_VALUE("object heap exhausted"); return 0; }
        int 필요수 = hyd_VALUE + 2, gwrthrych_cyfeiriad = 0;
        if (필요수 <= 힙.length - 힙끝) { gwrthrych_cyfeiriad = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { gwrthrych_cyfeiriad = 읽는자리; break; }
            if (gwrthrych_cyfeiriad != 0) {
                int 남은길이 = 힙폭[gwrthrych_cyfeiriad] - 필요수;
                if (남은길이 >= 2) { 힙폭[gwrthrych_cyfeiriad + 필요수] = 남은길이; 힙[gwrthrych_cyfeiriad + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { gwrthrych_cyfeiriad = 힙끝; 힙끝 += 필요수; }
        }
        if (gwrthrych_cyfeiriad == 0) { methiant_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { 힙[gwrthrych_cyfeiriad + Loop_INDEX] = 0; 힙참조[gwrthrych_cyfeiriad + Loop_INDEX] = 0; 힙폭[gwrthrych_cyfeiriad + Loop_INDEX] = 0; }
        ARAE_elfen[gwrthrych_cyfeiriad] = 0;
        힙폭[gwrthrych_cyfeiriad] = 필요수; 힙[gwrthrych_cyfeiriad] = 종류; 힙[gwrthrych_cyfeiriad + 1] = hyd_VALUE; diogelu_VALUE(gwrthrych_cyfeiriad); return gwrthrych_cyfeiriad;
    }
    static int eithriad_Dosbarth(String enw_cysonyn) {
        if (자바도구.같음(enw_cysonyn, "java/lang/Throwable")) return 1;
        if (자바도구.같음(enw_cysonyn, "java/lang/Exception")) return 2;
        if (자바도구.같음(enw_cysonyn, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(enw_cysonyn, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(enw_cysonyn, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(enw_cysonyn, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(enw_cysonyn, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(enw_cysonyn, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(enw_cysonyn, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(enw_cysonyn, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(enw_cysonyn, "java/io/IOException")) return 11;
        if (자바도구.같음(enw_cysonyn, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(enw_cysonyn, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(enw_cysonyn, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(enw_cysonyn, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int eithriad_cysonyn(int Enw) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_SMS(Enw, eithriad_enw(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String eithriad_enw(int cyfrif_VALUE) {
        if (cyfrif_VALUE == 40) return "java/lang/InterruptedException";
        if (cyfrif_VALUE == 41) return "Cymraeg/자체/대기중단예외";
        if (cyfrif_VALUE == 39) return "java/net/SocketException";
        if (cyfrif_VALUE == 20) return "Cymraeg/자체/eithriad";
        if (cyfrif_VALUE == 21) return "Cymraeg/자체/실행예외";
        if (cyfrif_VALUE == 22) return "Cymraeg/자체/I_O_eithriad";
        if (cyfrif_VALUE == 23) return "Cymraeg/자체/aros_TIMEOUT_eithriad";
        if (cyfrif_VALUE == 24) return "Cymraeg/자체/ADDRESS_LOOKUP_eithriad";
        if (cyfrif_VALUE == 25) return "Cymraeg/자체/파일없음예외";
        if (cyfrif_VALUE == 26) return "Cymraeg/자체/통신예외";
        if (cyfrif_VALUE == 27) return "Cymraeg/자체/annilys_arg_eithriad";
        if (cyfrif_VALUE == 28) return "Cymraeg/자체/숫자형식예외";
        if (cyfrif_VALUE == 29) return "Cymraeg/자체/범위예외";
        if (cyfrif_VALUE == 30) return "Cymraeg/자체/배열범위예외";
        if (cyfrif_VALUE == 31) return "Cymraeg/자체/문자열범위예외";
        if (cyfrif_VALUE == 32) return "Cymraeg/자체/NWL_cyfeiriad_eithriad";
        if (cyfrif_VALUE == 33) return "Cymraeg/자체/산술예외";
        if (cyfrif_VALUE == 34) return "Cymraeg/자체/cyflwr_eithriad";
        if (cyfrif_VALUE == 35) return "Cymraeg/자체/TYPE_Castio_eithriad";
        if (cyfrif_VALUE == 36) return "Cymraeg/자체/음수배열크기예외";
        if (cyfrif_VALUE == 37) return "Cymraeg/자체/ARAE_Store_methiant";
        if (cyfrif_VALUE == 38) return "Cymraeg/자체/edefyn_cyflwr_eithriad";
        if (cyfrif_VALUE == 1) return "java/lang/Throwable"; if (cyfrif_VALUE == 2) return "java/lang/Exception";
        if (cyfrif_VALUE == 3) return "java/lang/RuntimeException"; if (cyfrif_VALUE == 4) return "java/lang/ArithmeticException";
        if (cyfrif_VALUE == 5) return "java/lang/NullPointerException"; if (cyfrif_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (cyfrif_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (cyfrif_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (cyfrif_VALUE == 9) return "java/lang/IllegalArgumentException"; if (cyfrif_VALUE == 10) return "java/lang/NumberFormatException";
        if (cyfrif_VALUE == 11) return "java/io/IOException"; if (cyfrif_VALUE == 12) return "java/io/FileNotFoundException";
        if (cyfrif_VALUE == 17) return "java/lang/ArrayStoreException";
        if (cyfrif_VALUE == 18) return "java/net/UnknownHostException";
        if (cyfrif_VALUE == 19) return "java/net/SocketTimeoutException";
        if (cyfrif_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (cyfrif_VALUE == 13) return "java/lang/IllegalStateException"; if (cyfrif_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int cyfrif_VALUE) {
        if (cyfrif_VALUE == 40) return 2;
        if (cyfrif_VALUE == 41) return 40;
        if (cyfrif_VALUE == 39) return 11;
        if (cyfrif_VALUE == 1) return 0;
        if (cyfrif_VALUE == 2) return 1;
        if (cyfrif_VALUE == 3) return 2;
        if (cyfrif_VALUE == 4) return 3;
        if (cyfrif_VALUE == 5) return 3;
        if (cyfrif_VALUE == 6) return 3;
        if (cyfrif_VALUE == 7) return 6;
        if (cyfrif_VALUE == 8) return 6;
        if (cyfrif_VALUE == 9) return 3;
        if (cyfrif_VALUE == 10) return 9;
        if (cyfrif_VALUE == 11) return 2;
        if (cyfrif_VALUE == 12) return 11;
        if (cyfrif_VALUE == 13) return 3;
        if (cyfrif_VALUE == 14) return 3;
        if (cyfrif_VALUE == 15) return 3;
        if (cyfrif_VALUE == 16) return 9;
        if (cyfrif_VALUE == 17) return 3;
        if (cyfrif_VALUE == 18) return 11;
        if (cyfrif_VALUE == 19) return 11;
        if (cyfrif_VALUE == 20) return 2;
        if (cyfrif_VALUE == 21) return 3;
        if (cyfrif_VALUE == 22) return 11;
        if (cyfrif_VALUE == 23) return 22;
        if (cyfrif_VALUE == 24) return 22;
        if (cyfrif_VALUE == 25) return 22;
        if (cyfrif_VALUE == 26) return 22;
        if (cyfrif_VALUE == 27) return 9;
        if (cyfrif_VALUE == 28) return 27;
        if (cyfrif_VALUE == 29) return 6;
        if (cyfrif_VALUE == 30) return 29;
        if (cyfrif_VALUE == 31) return 29;
        if (cyfrif_VALUE == 32) return 5;
        if (cyfrif_VALUE == 33) return 4;
        if (cyfrif_VALUE == 34) return 13;
        if (cyfrif_VALUE == 35) return 14;
        if (cyfrif_VALUE == 36) return 15;
        if (cyfrif_VALUE == 37) return 17;
        if (cyfrif_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int go_iawn_VALUE, int 요구값) {
        for (int 깊이 = 0; go_iawn_VALUE != 0 && 깊이 < 16; 깊이++, go_iawn_VALUE = 예외부모(go_iawn_VALUE))
            if (go_iawn_VALUE == 요구값) return true;
        return false;
    }
    static void 예외던짐(int cyfrif_VALUE, String GWYBODAETH_cyfeiriad) {
        int gwrthrych_cyfeiriad = 새기억(9, 2); if (Gwall) return;
        힙[gwrthrych_cyfeiriad + 2] = cyfrif_VALUE; 힙[gwrthrych_cyfeiriad + 3] = lletya_nod(GWYBODAETH_cyfeiriad); 힙참조[gwrthrych_cyfeiriad + 3] = 1;
        던진객체 = gwrthrych_cyfeiriad; Gwall = true;
    }
    static boolean 맞는객체(int gwrthrych_cyfeiriad, int Enw) {
        if (gwrthrych_cyfeiriad == 0) return true;
        if (!객체유효(gwrthrych_cyfeiriad)) return false;
        int ardal_cod = 힙[gwrthrych_cyfeiriad];
        if (Word_SMS(Enw, "java/lang/Object")) return true;
        if (ardal_cod >= 32) return 종포함(ardal_cod - 32, Enw);
        if (ardal_cod == 9) { int targed_ADDRESS = eithriad_cysonyn(Enw); return targed_ADDRESS != 0 && 예외포함(힙[gwrthrych_cyfeiriad + 2], targed_ADDRESS); }
        if (ardal_cod == 1) return Word_SMS(Enw, "java/lang/String") || Word_SMS(Enw, "java/lang/CharSequence");
        if (ardal_cod == 4) return Word_SMS(Enw, "java/lang/StringBuilder") || Word_SMS(Enw, "java/lang/CharSequence");
        if (ardal_cod == 10) return Word_SMS(Enw, "java/util/ArrayList") || Word_SMS(Enw, "java/util/List");
        if (ardal_cod == 11) return Word_SMS(Enw, "java/util/HashMap") || Word_SMS(Enw, "java/util/Map");
        if (ardal_cod == 12) return Word_SMS(Enw, "java/lang/Integer") || Word_SMS(Enw, "java/lang/Number");
        if (ardal_cod >= 24 && ardal_cod <= 28 && 힙[gwrthrych_cyfeiriad + 13] != 0) return 한국어화면종(Enw) == ardal_cod || Word_SMS(Enw, "Cymraeg/자체/화면구성요소");
        if (ardal_cod >= 24 && ardal_cod <= 28) return (한국어화면종(Enw) == 0 && 화면종(Enw) == ardal_cod) || Word_SMS(Enw, "java/awt/Component") || Word_SMS(Enw, "java/awt/Container") || Word_SMS(Enw, "javax/swing/JComponent");
        if (ardal_cod == 29) return Word_SMS(Enw, 힙[gwrthrych_cyfeiriad + 3] != 0 ? "Cymraeg/자체/동작알림" : "java/awt/event/ActionEvent");
        if (ardal_cod == 30) return Word_SMS(Enw, "java/awt/FlowLayout") || Word_SMS(Enw, "java/awt/LayoutManager");
        if (ardal_cod == 17) return Word_SMS(Enw, "java/net/Socket");
        if (ardal_cod == 18) return Word_SMS(Enw, "java/net/ServerSocket");
        if (ardal_cod == 19) return Word_SMS(Enw, 힙[gwrthrych_cyfeiriad + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (ardal_cod == 14) return Word_SMS(Enw, "java/net/InetAddress");
        if (ardal_cod == 15) return Word_SMS(Enw, "java/net/DatagramSocket");
        if (ardal_cod == 16) return Word_SMS(Enw, "java/net/DatagramPacket");
        if (ardal_cod == 13) return Word_SMS(Enw, 힙[gwrthrych_cyfeiriad + 3] != 0 ? "Cymraeg/자체/작업가닥" : "java/lang/Thread");
        if (ardal_cod == 2) return Word_SMS(Enw, "[I"); if (ardal_cod == 20) return Word_SMS(Enw, "[B"); if (ardal_cod == 21) return Word_SMS(Enw, "[Z");
        if (ardal_cod == 22) return Word_SMS(Enw, "[C"); if (ardal_cod == 23) return Word_SMS(Enw, "[S");
        if (ardal_cod != 3) return false;
        if (Word_SMS(Enw, "[Ljava/lang/Object;")) return true;
        int cydran = ARAE_elfen[gwrthrych_cyfeiriad];
        if (cydran == -1) return Word_SMS(Enw, "[Ljava/lang/String;") || Word_SMS(Enw, "[Ljava/lang/CharSequence;");
        if (cydran == 0) return false;
        if (배열종비교(cydran, Enw)) return true;
        if ((Word_SMS(cydran, "java/lang/String") || Word_SMS(cydran, "java/lang/StringBuilder")) && Word_SMS(Enw, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < Dosbarth_Diffiniad_COUNT; Loop_INDEX++) if (같은말(Dosbarth_Diffiniad_enw[Loop_INDEX], cydran)) {
            for (int cod_nod = Loop_INDEX, 중첩깊이 = 0; cod_nod >= 0 && 중첩깊이 < 16; 중첩깊이++, cod_nod = 부모종(cod_nod)) {
                if (배열종비교(종부모[cod_nod], Enw)) return true;
                for (int uno_mewnol_safle = 0; uno_mewnol_safle < Dosbarth_rhyngwyneb_COUNT[cod_nod]; uno_mewnol_safle++) if (배열종비교(Dosbarth_rhyngwyneb[cod_nod * 16 + uno_mewnol_safle], Enw)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int enw_cysonyn, int 형식참조) {
        int gwirio_safle = 상가[형식참조], cofnod_COUNT = cysonyn_SECOND_VALUE[형식참조];
        if (enw_cysonyn == 0 || cofnod_COUNT < 4 || Ffeil[gwirio_safle] != '[' || Ffeil[gwirio_safle + 1] != 'L' || Ffeil[gwirio_safle + cofnod_COUNT - 1] != ';' || cysonyn_SECOND_VALUE[enw_cysonyn] != cofnod_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < cofnod_COUNT - 3; Loop_INDEX++) if (Ffeil[상가[enw_cysonyn] + Loop_INDEX] != Ffeil[gwirio_safle + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void dolen_eithriad() {
        if (던진객체 == 0) return;
        Gwall = false;
        while (ffrâm_INDEX >= 현재가닥 * 32) {
            int ffeil_INDEX = ffrâm_dull[ffrâm_INDEX], 읽는자리 = ffrâm_cyfarwyddyd[ffrâm_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == ffeil_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                ffrâm_safle[ffrâm_INDEX] = 잡기위치[Loop_INDEX]; ffrâm_pentwr[ffrâm_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (ymgychwyn_ffrâm[ffrâm_INDEX] != 0) Dosbarth_Diffiniad_cyflwr[ymgychwyn_ffrâm[ffrâm_INDEX] - 1] = 3;
            if (틀잠금[ffrâm_INDEX] != 0) { 잠금풀기(틀잠금[ffrâm_INDEX]); 틀잠금[ffrâm_INDEX] = 0; }
            ffrâm_INDEX--;
        }
        defnyddiwr.Ysgrifennu("Uncaught ");
        if (힙[던진객체] == 9) { defnyddiwr.Ysgrifennu(eithriad_enw(힙[던진객체 + 2])); defnyddiwr.Ysgrifennu(": "); ysgrifennu_SMS(힙[던진객체 + 3]); }
        else defnyddiwr.Ysgrifennu("user exception");
        defnyddiwr.ysgrifennu_nod_VALUE(10); 던진객체 = 0; Gwall = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void pentwr_cyfarwyddyd(int gorchymyn_cod) {
        int 첫값 = 빼기(0), 첫형식 = return_TYPE;
        if (gorchymyn_cod == 87) return;
        if (gorchymyn_cod == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int beit_data = 빼기(0), SECOND_fformat = return_TYPE;
        if (gorchymyn_cod == 88) return;
        if (gorchymyn_cod == 90) { 넣기(첫값, 첫형식); 넣기(beit_data, SECOND_fformat); 넣기(첫값, 첫형식); return; }
        if (gorchymyn_cod == 92) { 넣기(beit_data, SECOND_fformat); 넣기(첫값, 첫형식); 넣기(beit_data, SECOND_fformat); 넣기(첫값, 첫형식); return; }
        if (gorchymyn_cod == 95) { 넣기(첫값, 첫형식); 넣기(beit_data, SECOND_fformat); return; }
        int cod_nod = 빼기(0), 셋째형식 = return_TYPE;
        if (gorchymyn_cod == 91) { 넣기(첫값, 첫형식); 넣기(cod_nod, 셋째형식); 넣기(beit_data, SECOND_fformat); 넣기(첫값, 첫형식); return; }
        if (gorchymyn_cod == 93) { 넣기(beit_data, SECOND_fformat); 넣기(첫값, 첫형식); 넣기(cod_nod, 셋째형식); 넣기(beit_data, SECOND_fformat); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = return_TYPE;
        넣기(beit_data, SECOND_fformat); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(cod_nod, 셋째형식); 넣기(beit_data, SECOND_fformat); 넣기(첫값, 첫형식);
    }
    static void 새객체(int enw_cysonyn, int 시작점) {
        int ardal_cod = 0, 유효길이 = 0, eithriad_cyfeiriad = eithriad_cysonyn(enw_cysonyn);
        if (Word_SMS(enw_cysonyn, "java/lang/StringBuilder")) { ardal_cod = 4; 유효길이 = 1; }
        if (Word_SMS(enw_cysonyn, "java/io/FileInputStream")) { ardal_cod = 5; 유효길이 = 2; }
        if (Word_SMS(enw_cysonyn, "java/io/FileOutputStream")) { ardal_cod = 6; 유효길이 = 2; }
        if (eithriad_cyfeiriad != 0) { ardal_cod = 9; 유효길이 = 2; }
        if (Word_SMS(enw_cysonyn, "java/util/ArrayList")) { ardal_cod = 10; 유효길이 = 2; }
        if (Word_SMS(enw_cysonyn, "java/util/HashMap")) { ardal_cod = 11; 유효길이 = 2; }
        if (Word_SMS(enw_cysonyn, "java/lang/Integer")) { ardal_cod = 12; 유효길이 = 1; }
        if (Word_SMS(enw_cysonyn, "java/net/Socket")) { ardal_cod = 17; 유효길이 = 5; }
        if (Word_SMS(enw_cysonyn, "java/net/ServerSocket")) { ardal_cod = 18; 유효길이 = 5; }
        if (Word_SMS(enw_cysonyn, "java/net/DatagramSocket")) { ardal_cod = 15; 유효길이 = 3; }
        if (Word_SMS(enw_cysonyn, "java/net/DatagramPacket")) { ardal_cod = 16; 유효길이 = 4; }
        if (Word_SMS(enw_cysonyn, "java/lang/Thread") || Word_SMS(enw_cysonyn, "Cymraeg/자체/작업가닥")) { ardal_cod = 13; 유효길이 = 2; }
        if (Word_SMS(enw_cysonyn, "java/lang/Object")) { ardal_cod = 8; }
        if (ardal_cod == 0 && 화면종(enw_cysonyn) != 0) { ardal_cod = 화면종(enw_cysonyn); 유효길이 = 12; }
        if (ardal_cod == 0) {
            int cod_nod = FIND_Dosbarth_Diffiniad(enw_cysonyn); if (cod_nod < 0 || Gwall || !ymgychwyn(cod_nod, 시작점)) return;
            ardal_cod = 32 + cod_nod; 유효길이 = Dosbarth_slot_COUNT[cod_nod];
        }
        int gwrthrych_cyfeiriad = dyrannu_Storio(ardal_cod, 유효길이); if (Gwall) return;
        if (ardal_cod == 13 && Word_SMS(enw_cysonyn, "Cymraeg/자체/작업가닥")) 힙[gwrthrych_cyfeiriad + 3] = 1;
        if (ardal_cod >= 24 && ardal_cod <= 28 && 한국어화면종(enw_cysonyn) != 0) 힙[gwrthrych_cyfeiriad + 13] = 1;
        if (ardal_cod == 5 || ardal_cod == 6 || ardal_cod == 15 || ardal_cod == 17 || ardal_cod == 18) 힙[gwrthrych_cyfeiriad + 2] = -1;
        if (ardal_cod == 9) 힙[gwrthrych_cyfeiriad + 2] = eithriad_cyfeiriad;
        넣기(gwrthrych_cyfeiriad, 2);
    }
    static boolean 값같음(int 첫값, int beit_data) {
        if (첫값 == beit_data) return true;
        if (첫값 == 0 || beit_data == 0 || 첫값 < 0 || beit_data < 0 || 첫값 >= 힙끝 || beit_data >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[beit_data] == 1) return 글같음(첫값, beit_data, false);
        return 힙[첫값] == 12 && 힙[beit_data] == 12 && 힙[첫값 + 2] == 힙[beit_data + 2];
    }
    static int 글조각(int gwrthrych_cyfeiriad, int START_safle, int gorffen_safle) {
        if (!gwrthrych_VALUE(gwrthrych_cyfeiriad, 1)) return 0;
        if (START_safle < 0 || gorffen_safle < START_safle || gorffen_safle > 힙[gwrthrych_cyfeiriad + 1]) { methiant_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = dyrannu_Storio(1, gorffen_safle - START_safle); if (Gwall) return 0;
        for (int Loop_INDEX = START_safle; Loop_INDEX < gorffen_safle; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX - START_safle] = 힙[gwrthrych_cyfeiriad + 2 + Loop_INDEX];
        return 반환값;
    }
    static int uno_SMS(int 첫값, int beit_data) {
        if (!gwrthrych_VALUE(첫값, 1) || !gwrthrych_VALUE(beit_data, 1)) return 0;
        int cofnod_COUNT = 힙[첫값 + 1], dull_INDEX = 힙[beit_data + 1], 반환값 = dyrannu_Storio(1, cofnod_COUNT + dull_INDEX); if (Gwall) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < cofnod_COUNT; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 힙[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < dull_INDEX; Loop_INDEX++) 힙[반환값 + 2 + cofnod_COUNT + Loop_INDEX] = 힙[beit_data + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int perchennog, int enw_cysonyn, int 서술상수, int gorchymyn_cod) {
        if (Word_SMS(perchennog, "Cymraeg/자체/실행인수") && gorchymyn_cod == 184) {
            if (Word_SMS(enw_cysonyn, "eitem_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(defnyddiwr.인수개수() - 1, 1); return true; }
            if (Word_SMS(enw_cysonyn, "Testun") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= defnyddiwr.인수개수() - 1) 예외던짐(29, "Gweithredu_gorchymyn 인수 범위를 벗어났습니다");
                else 넣기(lletya_nod(defnyddiwr.인수(순번 + 1)), 2);
                return true;
            }
            methiant_VALUE("지원하지 않는 Cymraeg Gweithredu_gorchymyn 인수 호출"); return true;
        }
        if (Word_SMS(perchennog, "Cymraeg/자체/작업가닥")) { Proses_edefyn(enw_cysonyn, 서술상수, gorchymyn_cod, true); return true; }
        if (한국어화면소유(perchennog)) { 한국어화면호출(perchennog, enw_cysonyn, 서술상수, gorchymyn_cod); return true; }
        if (화면소유(perchennog)) { 화면호출(perchennog, enw_cysonyn, 서술상수, gorchymyn_cod); return true; }
        if (Word_SMS(perchennog, "java/net/Socket") || Word_SMS(perchennog, "java/net/ServerSocket") || Word_SMS(perchennog, "java/io/InputStream") || Word_SMS(perchennog, "java/io/OutputStream")) { 흐름호출(perchennog, enw_cysonyn, 서술상수, gorchymyn_cod); return true; }
        if (Word_SMS(perchennog, "Cymraeg/자체/cnewyllyn_VALUE") && gorchymyn_cod == 184) {
            if (Word_SMS(enw_cysonyn, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(defnyddiwr.화면너비(), 1); return true; }
            if (Word_SMS(enw_cysonyn, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(defnyddiwr.화면높이(), 1); return true; }
            if (Word_SMS(enw_cysonyn, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(defnyddiwr.밀리초(), 1); return true; }
            if (Word_SMS(enw_cysonyn, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(defnyddiwr.그림대기(), 1); return true; }
            if (Word_SMS(enw_cysonyn, "사각형") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Y_cyfesuryn = 빼기(1), cyfesuryn_x = 빼기(1); 넣기(defnyddiwr.사각형(cyfesuryn_x, Y_cyfesuryn, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(perchennog, "java/net/InetAddress") || Word_SMS(perchennog, "java/net/DatagramPacket") || Word_SMS(perchennog, "java/net/DatagramSocket")) { 통신호출(perchennog, enw_cysonyn, 서술상수, gorchymyn_cod); return true; }
        if (Word_SMS(perchennog, "java/lang/Thread")) { 가닥호출(enw_cysonyn, 서술상수, gorchymyn_cod); return true; }
        if (Word_SMS(perchennog, "java/lang/Object")) {
            if (Word_SMS(enw_cysonyn, "<init>") && Word_SMS(서술상수, "()V") && gorchymyn_cod == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(enw_cysonyn, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int beit_data = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == beit_data ? 1 : 0, 1); return true; }
        }
        if (eithriad_cysonyn(perchennog) != 0) {
            if (Word_SMS(enw_cysonyn, "<init>") && gorchymyn_cod == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int neges_1dd14da4 = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), gwrthrych_cyfeiriad = 빼기(2);
                if (gwrthrych_VALUE(gwrthrych_cyfeiriad, 9)) { 힙[gwrthrych_cyfeiriad + 3] = neges_1dd14da4; 힙참조[gwrthrych_cyfeiriad + 3] = 1; } return true;
            }
            if ((Word_SMS(enw_cysonyn, "getMessage") || Word_SMS(enw_cysonyn, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int gwrthrych_cyfeiriad = 빼기(2); if (gwrthrych_VALUE(gwrthrych_cyfeiriad, 9)) 넣기(힙[gwrthrych_cyfeiriad + 3], 2); return true; }
        }
        if (Word_SMS(perchennog, "java/lang/String")) {
            if (gorchymyn_cod == 182 && Word_SMS(enw_cysonyn, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int amgodio_enw = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), gwrthrych_cyfeiriad = 빼기(2);
                if (!gwrthrych_VALUE(gwrthrych_cyfeiriad, 1)) return true;
                if (amgodio_enw != 0 && !글같음(amgodio_enw, lletya_nod("UTF-8"), false) && !글같음(amgodio_enw, lletya_nod("UTF8"), false) && !글같음(amgodio_enw, lletya_nod("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int cofnod_COUNT = 힙[gwrthrych_cyfeiriad + 1], 반환값 = dyrannu_Storio(20, cofnod_COUNT * 3), 사용수 = 0; if (Gwall) return true;
                for (int uno_mewnol_safle = 0; uno_mewnol_safle < cofnod_COUNT; uno_mewnol_safle++) {
                    int cod_nod = 힙[gwrthrych_cyfeiriad + 2 + uno_mewnol_safle];
                    if (cod_nod >= 0xd800 && cod_nod <= 0xdbff && uno_mewnol_safle + 1 < cofnod_COUNT && 힙[gwrthrych_cyfeiriad + 3 + uno_mewnol_safle] >= 0xdc00 && 힙[gwrthrych_cyfeiriad + 3 + uno_mewnol_safle] <= 0xdfff) cod_nod = 0x10000 + ((cod_nod - 0xd800) << 10) + 힙[gwrthrych_cyfeiriad + 2 + ++uno_mewnol_safle] - 0xdc00;
                    else if (cod_nod >= 0xd800 && cod_nod <= 0xdfff) cod_nod = '?';
                    if (cod_nod < 128) 힙[반환값 + 2 + 사용수++] = cod_nod;
                    else { int beit_COUNT = cod_nod < 2048 ? 2 : cod_nod < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((beit_COUNT == 2 ? 192 : beit_COUNT == 3 ? 224 : 240) | cod_nod >> (6 * (beit_COUNT - 1))); for (int 비교자리 = beit_COUNT - 1; 비교자리 > 0; 비교자리--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | cod_nod >> (6 * (비교자리 - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (gorchymyn_cod == 184 && Word_SMS(enw_cysonyn, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(digid_nod(빼기(1)), 2); return true; }
            if (gorchymyn_cod != 182) return false;
            if (Word_SMS(enw_cysonyn, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int beit_data = 빼기(2), 첫값 = 빼기(2); if (gwrthrych_VALUE(첫값, 1)) 넣기(글같음(첫값, beit_data, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(enw_cysonyn, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (gwrthrych_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(enw_cysonyn, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int gorffen_safle = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (gwrthrych_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? gorffen_safle : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(enw_cysonyn, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int beit_data = 빼기(2), 첫값 = 빼기(2); 넣기(uno_SMS(첫값, beit_data), 2); return true; }
            if (Word_SMS(enw_cysonyn, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), hash_VALUE = 0; if (gwrthrych_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) hash_VALUE = hash_VALUE * 31 + 힙[첫값 + 2 + Loop_INDEX]; 넣기(hash_VALUE, 1); } return true; }
            if (Word_SMS(enw_cysonyn, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (gwrthrych_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(perchennog, "java/lang/Integer")) {
            if (gorchymyn_cod == 184 && Word_SMS(enw_cysonyn, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int data_VALUE = 빼기(1), gwrthrych_cyfeiriad = data_VALUE >= -128 && data_VALUE <= 127 ? Store_cyfanrif[data_VALUE + 128] : 0; if (gwrthrych_cyfeiriad == 0) { gwrthrych_cyfeiriad = dyrannu_Storio(12, 1); if (!Gwall) { 힙[gwrthrych_cyfeiriad + 2] = data_VALUE; if (data_VALUE >= -128 && data_VALUE <= 127) Store_cyfanrif[data_VALUE + 128] = gwrthrych_cyfeiriad; } } 넣기(gwrthrych_cyfeiriad, 2); return true; }
            if (gorchymyn_cod == 183 && Word_SMS(enw_cysonyn, "<init>") && Word_SMS(서술상수, "(I)V")) { int data_VALUE = 빼기(1), gwrthrych_cyfeiriad = 빼기(2); if (gwrthrych_VALUE(gwrthrych_cyfeiriad, 12)) 힙[gwrthrych_cyfeiriad + 2] = data_VALUE; return true; }
            if (gorchymyn_cod == 182 && Word_SMS(enw_cysonyn, "intValue") && Word_SMS(서술상수, "()I")) { int gwrthrych_cyfeiriad = 빼기(2); if (gwrthrych_VALUE(gwrthrych_cyfeiriad, 12)) 넣기(힙[gwrthrych_cyfeiriad + 2], 1); return true; }
            if (gorchymyn_cod == 184 && Word_SMS(enw_cysonyn, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(digid_nod(빼기(1)), 2); return true; }
        }
        if (Word_SMS(perchennog, "java/lang/Math") && gorchymyn_cod == 184) {
            if (Word_SMS(enw_cysonyn, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(enw_cysonyn, "min") || Word_SMS(enw_cysonyn, "max")) && Word_SMS(서술상수, "(II)I")) { int beit_data = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(enw_cysonyn, "min") ? (첫값 < beit_data ? 첫값 : beit_data) : (첫값 > beit_data ? 첫값 : beit_data), 1); return true; }
        }
        if (Word_SMS(perchennog, "java/lang/System") && gorchymyn_cod == 184) {
            if (Word_SMS(enw_cysonyn, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(enw_cysonyn, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int cofnod_COUNT = 빼기(1), cyrchfan_VALUE_INDEX = 빼기(1), beit_data = 빼기(2), START_safle = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(beit_data)) {
                    int ardal_cod = 힙[첫값];
                    if (힙[beit_data] != ardal_cod || (ardal_cod != 2 && ardal_cod != 3 && (ardal_cod < 20 || ardal_cod > 23))) methiant_VALUE("arraycopy type mismatch");
                    else if (cofnod_COUNT < 0 || START_safle < 0 || cyrchfan_VALUE_INDEX < 0 || START_safle > 힙[첫값 + 1] - cofnod_COUNT || cyrchfan_VALUE_INDEX > 힙[beit_data + 1] - cofnod_COUNT) methiant_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == beit_data && cyrchfan_VALUE_INDEX > START_safle) { for (int Loop_INDEX = cofnod_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) 힙[beit_data + 2 + cyrchfan_VALUE_INDEX + Loop_INDEX] = 힙[첫값 + 2 + START_safle + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < cofnod_COUNT && !Gwall; Loop_INDEX++) { int data_VALUE = 힙[첫값 + 2 + START_safle + Loop_INDEX]; if (ardal_cod != 3 || 배열저장가능(beit_data, data_VALUE)) 힙[beit_data + 2 + cyrchfan_VALUE_INDEX + Loop_INDEX] = data_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(perchennog, "java/util/ArrayList") || Word_SMS(perchennog, "java/util/List") || Word_SMS(perchennog, "java/util/HashMap") || Word_SMS(perchennog, "java/util/Map")) {
            모음호출(perchennog, enw_cysonyn, 서술상수, gorchymyn_cod); return true;
        }
        return false;
    }
    static void 모음늘리기(int gwrthrych_cyfeiriad, int 필요수) {
        int 이전값 = 힙[gwrthrych_cyfeiriad + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int Nesaf_safle = 용량값 < 8 ? 8 : 용량값 * 2; if (Nesaf_safle < 필요수) Nesaf_safle = 필요수;
        int data_ARAE = dyrannu_Storio(3, Nesaf_safle); if (Gwall) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 용량값; Loop_INDEX++) 힙[data_ARAE + 2 + Loop_INDEX] = 힙[이전값 + 2 + Loop_INDEX];
        힙[gwrthrych_cyfeiriad + 2] = data_ARAE; 힙참조[gwrthrych_cyfeiriad + 2] = 1;
    }
    static void 모음호출(int perchennog, int enw_cysonyn, int 서술상수, int gorchymyn_cod) {
        boolean 대응참조 = Word_SMS(perchennog, "java/util/HashMap") || Word_SMS(perchennog, "java/util/Map"); int ardal_cod = 대응참조 ? 11 : 10;
        if (Word_SMS(enw_cysonyn, "<init>") && gorchymyn_cod == 183 && Word_SMS(서술상수, "()V")) { int gwrthrych_cyfeiriad = 빼기(2); if (gwrthrych_VALUE(gwrthrych_cyfeiriad, ardal_cod)) 모음늘리기(gwrthrych_cyfeiriad, 8); return; }
        if (gorchymyn_cod != 182 && gorchymyn_cod != 185) { methiant_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(enw_cysonyn, "size") && Word_SMS(서술상수, "()I") || Word_SMS(enw_cysonyn, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int gwrthrych_cyfeiriad = 빼기(2); if (gwrthrych_VALUE(gwrthrych_cyfeiriad, ardal_cod)) 넣기(Word_SMS(enw_cysonyn, "size") ? 힙[gwrthrych_cyfeiriad + 3] : 힙[gwrthrych_cyfeiriad + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(enw_cysonyn, "clear") && Word_SMS(서술상수, "()V")) { int gwrthrych_cyfeiriad = 빼기(2); if (gwrthrych_VALUE(gwrthrych_cyfeiriad, ardal_cod)) { int data_ARAE = 힙[gwrthrych_cyfeiriad + 2]; for (int Loop_INDEX = 0; Loop_INDEX < 힙[data_ARAE + 1]; Loop_INDEX++) 힙[data_ARAE + 2 + Loop_INDEX] = 0; 힙[gwrthrych_cyfeiriad + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(enw_cysonyn, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int data_VALUE = 빼기(2), gwrthrych_cyfeiriad = 빼기(2); if (!gwrthrych_VALUE(gwrthrych_cyfeiriad, 10)) return;
            int cofnod_COUNT = 힙[gwrthrych_cyfeiriad + 3]; 모음늘리기(gwrthrych_cyfeiriad, cofnod_COUNT + 1); if (!Gwall) { 힙[힙[gwrthrych_cyfeiriad + 2] + 2 + cofnod_COUNT] = data_VALUE; 힙[gwrthrych_cyfeiriad + 3] = cofnod_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(enw_cysonyn, "get") || Word_SMS(enw_cysonyn, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(enw_cysonyn, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Word_SMS(enw_cysonyn, "set"); int data_VALUE = 지정여부 ? 빼기(2) : 0, cofnod_safle = 빼기(1), gwrthrych_cyfeiriad = 빼기(2);
            if (!gwrthrych_VALUE(gwrthrych_cyfeiriad, 10)) return;
            int cofnod_COUNT = 힙[gwrthrych_cyfeiriad + 3], data_ARAE = 힙[gwrthrych_cyfeiriad + 2];
            if (cofnod_safle < 0 || cofnod_safle >= cofnod_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[data_ARAE + 2 + cofnod_safle];
            if (지정여부) 힙[data_ARAE + 2 + cofnod_safle] = data_VALUE;
            if (Word_SMS(enw_cysonyn, "remove")) { for (int Loop_INDEX = cofnod_safle + 1; Loop_INDEX < cofnod_COUNT; Loop_INDEX++) 힙[data_ARAE + 1 + Loop_INDEX] = 힙[data_ARAE + 2 + Loop_INDEX]; 힙[data_ARAE + 1 + cofnod_COUNT] = 0; 힙[gwrthrych_cyfeiriad + 3] = cofnod_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(enw_cysonyn, "get") || Word_SMS(enw_cysonyn, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(enw_cysonyn, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(enw_cysonyn, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(enw_cysonyn, "put"), tynnu = Word_SMS(enw_cysonyn, "remove");
            int data_VALUE = 넣기여부 ? 빼기(2) : 0, bysell_cyfeiriad = 빼기(2), gwrthrych_cyfeiriad = 빼기(2); if (!gwrthrych_VALUE(gwrthrych_cyfeiriad, 11)) return;
            int cofnod_COUNT = 힙[gwrthrych_cyfeiriad + 3], data_ARAE = 힙[gwrthrych_cyfeiriad + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < cofnod_COUNT; Loop_INDEX++) if (값같음(bysell_cyfeiriad, 힙[data_ARAE + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[data_ARAE + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(gwrthrych_cyfeiriad, (cofnod_COUNT + 1) * 2); data_ARAE = 힙[gwrthrych_cyfeiriad + 2]; 찾은여부 = cofnod_COUNT; if (!Gwall) 힙[gwrthrych_cyfeiriad + 3] = cofnod_COUNT + 1; }
                if (!Gwall) { 힙[data_ARAE + 2 + 2 * 찾은여부] = bysell_cyfeiriad; 힙[data_ARAE + 3 + 2 * 찾은여부] = data_VALUE; }
            }
            if (tynnu && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < cofnod_COUNT; Loop_INDEX++) { 힙[data_ARAE + 2 * Loop_INDEX] = 힙[data_ARAE + 2 + 2 * Loop_INDEX]; 힙[data_ARAE + 1 + 2 * Loop_INDEX] = 힙[data_ARAE + 3 + 2 * Loop_INDEX]; } 힙[data_ARAE + 2 * cofnod_COUNT] = 0; 힙[data_ARAE + 1 + 2 * cofnod_COUNT] = 0; 힙[gwrthrych_cyfeiriad + 3] = cofnod_COUNT - 1; }
            if (Word_SMS(enw_cysonyn, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        methiant_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int gwrthrych_cyfeiriad) {
        if (!객체유효(gwrthrych_cyfeiriad)) return false;
        if (잠금깊이[gwrthrych_cyfeiriad] != 0 && 잠금주인[gwrthrych_cyfeiriad] != 현재가닥 + 1) { newid_cais_HTTP = true; return false; }
        잠금주인[gwrthrych_cyfeiriad] = 현재가닥 + 1; 잠금깊이[gwrthrych_cyfeiriad]++; return true;
    }
    static void 잠금풀기(int gwrthrych_cyfeiriad) {
        if (!객체유효(gwrthrych_cyfeiriad)) return;
        if (잠금깊이[gwrthrych_cyfeiriad] == 0 || 잠금주인[gwrthrych_cyfeiriad] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[gwrthrych_cyfeiriad] == 0) 잠금주인[gwrthrych_cyfeiriad] = 0;
    }
    static boolean newid_edefyn() {
        edefyn_ffrâm[현재가닥] = ffrâm_INDEX;
        if (ffrâm_INDEX < 현재가닥 * 32) edefyn_cyflwr[현재가닥] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < edefyn_COUNT; Loop_INDEX++) if (edefyn_cyflwr[Loop_INDEX] == 2 && edefyn_cyflwr[가닥대기[Loop_INDEX]] == 3) edefyn_cyflwr[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= edefyn_COUNT; Loop_INDEX++) {
            int Nesaf_safle = (현재가닥 + Loop_INDEX) % edefyn_COUNT;
            if (edefyn_cyflwr[Nesaf_safle] == 1) { 현재가닥 = Nesaf_safle; ffrâm_INDEX = edefyn_ffrâm[Nesaf_safle]; newid_cais_HTTP = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < edefyn_COUNT; Loop_INDEX++) if (edefyn_cyflwr[Loop_INDEX] != 3) { methiant_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int enw_cysonyn, int 서술상수, int gorchymyn_cod) { Proses_edefyn(enw_cysonyn, 서술상수, gorchymyn_cod, false); }
    static void Proses_edefyn(int enw_cysonyn, int 서술상수, int gorchymyn_cod, boolean Cymraeg) {
        if (gorchymyn_cod == 184 && Word_SMS(enw_cysonyn, Cymraeg ? "atal_tasg" : "yield") && Word_SMS(서술상수, "()V")) { newid_cais_HTTP = true; return; }
        if (gorchymyn_cod == 184 && Word_SMS(enw_cysonyn, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(edefyn_gwrthrych[현재가닥], 2); return; }
        if (gorchymyn_cod == 183 && Word_SMS(enw_cysonyn, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, Cymraeg ? "(LCymraeg/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int targed_ADDRESS = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), gwrthrych_cyfeiriad = 빼기(2);
            if (!객체유효(gwrthrych_cyfeiriad)) return;
            if (힙[gwrthrych_cyfeiriad] == 13) { 힙[gwrthrych_cyfeiriad + 2] = targed_ADDRESS; 힙참조[gwrthrych_cyfeiriad + 2] = 1; }
            else if (targed_ADDRESS != 0) methiant_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (gorchymyn_cod == 182 && (Word_SMS(enw_cysonyn, Cymraeg ? "START_tasg" : "start") || Word_SMS(enw_cysonyn, Cymraeg ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || gorchymyn_cod == 182 && Word_SMS(enw_cysonyn, Cymraeg ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int gwrthrych_cyfeiriad = 빼기(2); if (!객체유효(gwrthrych_cyfeiriad)) return;
            int cyfrif_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < edefyn_COUNT; Loop_INDEX++) if (edefyn_gwrthrych[Loop_INDEX] == gwrthrych_cyfeiriad) cyfrif_VALUE = Loop_INDEX;
            if (Word_SMS(enw_cysonyn, Cymraeg ? "살아있는가" : "isAlive")) { 넣기(cyfrif_VALUE >= 0 && edefyn_cyflwr[cyfrif_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(enw_cysonyn, Cymraeg ? "기다리기" : "join")) { if (cyfrif_VALUE >= 0 && edefyn_cyflwr[cyfrif_VALUE] != 3) { 가닥대기[현재가닥] = cyfrif_VALUE; edefyn_cyflwr[현재가닥] = 2; newid_cais_HTTP = true; } return; }
            if (cyfrif_VALUE >= 0) { 예외던짐(Cymraeg ? 38 : 16, "thread already started"); return; }
            if (edefyn_COUNT == 4) { methiant_VALUE("thread limit (4 including main)"); return; }
            int targed_ADDRESS = 힙[gwrthrych_cyfeiriad] == 13 ? 힙[gwrthrych_cyfeiriad + 2] : gwrthrych_cyfeiriad;
            int ffeil_INDEX = targed_ADDRESS > 0 && 힙[targed_ADDRESS] >= 32 ? enw_dull(힙[targed_ADDRESS] - 32, Cymraeg ? "Gweithredu" : "run", "()V") : -1;
            if (targed_ADDRESS != 0 && ffeil_INDEX < 0) { methiant_VALUE("Runnable.run required"); return; }
            cyfrif_VALUE = edefyn_COUNT++; edefyn_gwrthrych[cyfrif_VALUE] = gwrthrych_cyfeiriad; edefyn_targed[cyfrif_VALUE] = targed_ADDRESS;
            int ffrâm = cyfrif_VALUE * 32; edefyn_ffrâm[cyfrif_VALUE] = ffeil_INDEX < 0 ? ffrâm - 1 : ffrâm; edefyn_cyflwr[cyfrif_VALUE] = ffeil_INDEX < 0 ? 3 : 1;
            if (ffeil_INDEX >= 0) { ffrâm_dull[ffrâm] = ffeil_INDEX; ffrâm_safle[ffrâm] = dull_START[ffeil_INDEX]; lleol_VALUE[ffrâm * 128] = targed_ADDRESS; lleol_TYPE[ffrâm * 128] = 2; }
            return;
        }
        methiant_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], ADDRESS_SMS = new int[16];
    static int lleol_ADDRESS() { return ADDRESS_gwrthrych(0x7f000001); }
    static int ADDRESS_gwrthrych(int VALUE) { int gwrthrych_cyfeiriad = dyrannu_Storio(14, 1); if (!Gwall) 힙[gwrthrych_cyfeiriad + 2] = VALUE; return gwrthrych_cyfeiriad; }
    static int 주소해독(int gwrthrych_cyfeiriad) {
        if (gwrthrych_cyfeiriad == 0 || 글같음(gwrthrych_cyfeiriad, lletya_nod("localhost"), false)) return 0x7f000001;
        if (!gwrthrych_VALUE(gwrthrych_cyfeiriad, 1)) return 0;
        int data_VALUE = 0, 총수 = 0, ADDRESS_beit = 0, 자릿수 = 0, cofnod_COUNT = 힙[gwrthrych_cyfeiriad + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= cofnod_COUNT; Loop_INDEX++) {
            int cod_nod = Loop_INDEX == cofnod_COUNT ? '.' : 힙[gwrthrych_cyfeiriad + 2 + Loop_INDEX];
            if (cod_nod == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } data_VALUE = data_VALUE << 8 | ADDRESS_beit; 총수++; ADDRESS_beit = 자릿수 = 0; }
            else { if (cod_nod < '0' || cod_nod > '9' || ++자릿수 > 3 || (ADDRESS_beit = ADDRESS_beit * 10 + cod_nod - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return data_VALUE;
    }
    static int ADDRESS_nod(int data_VALUE) {
        int cofnod_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int ADDRESS_beit = data_VALUE >>> 이동비트 & 255;
            if (ADDRESS_beit >= 100) ADDRESS_SMS[cofnod_COUNT++] = '0' + ADDRESS_beit / 100;
            if (ADDRESS_beit >= 10) ADDRESS_SMS[cofnod_COUNT++] = '0' + ADDRESS_beit / 10 % 10;
            ADDRESS_SMS[cofnod_COUNT++] = '0' + ADDRESS_beit % 10; if (이동비트 != 0) ADDRESS_SMS[cofnod_COUNT++] = '.';
        }
        int gwrthrych_cyfeiriad = dyrannu_Storio(1, cofnod_COUNT); if (!Gwall) for (int Loop_INDEX = 0; Loop_INDEX < cofnod_COUNT; Loop_INDEX++) 힙[gwrthrych_cyfeiriad + 2 + Loop_INDEX] = ADDRESS_SMS[Loop_INDEX]; return gwrthrych_cyfeiriad;
    }
    static void 통신호출(int perchennog, int enw_cysonyn, int 서술상수, int gorchymyn_cod) {
        if (Word_SMS(perchennog, "java/net/InetAddress")) {
            if (gorchymyn_cod == 184 && Word_SMS(enw_cysonyn, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(lleol_ADDRESS(), 2); return; }
            if (gorchymyn_cod == 184 && Word_SMS(enw_cysonyn, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int data_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !Gwall) 넣기(ADDRESS_gwrthrych(data_VALUE), 2); return;
            }
            if (gorchymyn_cod == 182 && Word_SMS(enw_cysonyn, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int gwrthrych_cyfeiriad = 빼기(2); if (gwrthrych_VALUE(gwrthrych_cyfeiriad, 14)) 넣기(ADDRESS_nod(힙[gwrthrych_cyfeiriad + 2]), 2); return; }
        }
        if (Word_SMS(perchennog, "java/net/DatagramPacket")) {
            if (gorchymyn_cod == 183 && Word_SMS(enw_cysonyn, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean cyrchfan_VALUE_cyfeiriad = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int rhif_porth = cyrchfan_VALUE_cyfeiriad ? 빼기(1) : 0, ADDRESS_cyfeiriad = cyrchfan_VALUE_cyfeiriad ? 빼기(2) : 0;
                int cofnod_COUNT = 빼기(1), data_ARAE = 빼기(2), gwrthrych_cyfeiriad = 빼기(2);
                if (!gwrthrych_VALUE(gwrthrych_cyfeiriad, 16) || !gwrthrych_VALUE(data_ARAE, 20)) return;
                if (cofnod_COUNT < 0 || cofnod_COUNT > 힙[data_ARAE + 1] || rhif_porth < 0 || rhif_porth > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (ADDRESS_cyfeiriad != 0 && !gwrthrych_VALUE(ADDRESS_cyfeiriad, 14)) return;
                힙[gwrthrych_cyfeiriad + 2] = data_ARAE; 힙참조[gwrthrych_cyfeiriad + 2] = 1; 힙[gwrthrych_cyfeiriad + 3] = cofnod_COUNT;
                힙[gwrthrych_cyfeiriad + 4] = ADDRESS_cyfeiriad; 힙참조[gwrthrych_cyfeiriad + 4] = 1; 힙[gwrthrych_cyfeiriad + 5] = rhif_porth; return;
            }
            if (gorchymyn_cod == 182 && Word_SMS(enw_cysonyn, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int cofnod_COUNT = 빼기(1), gwrthrych_cyfeiriad = 빼기(2); if (!gwrthrych_VALUE(gwrthrych_cyfeiriad, 16)) return;
                if (cofnod_COUNT < 0 || cofnod_COUNT > 힙[힙[gwrthrych_cyfeiriad + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[gwrthrych_cyfeiriad + 3] = cofnod_COUNT; return;
            }
            if (gorchymyn_cod == 182 && (Word_SMS(enw_cysonyn, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(enw_cysonyn, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(enw_cysonyn, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(enw_cysonyn, "getPort") && Word_SMS(서술상수, "()I"))) {
                int gwrthrych_cyfeiriad = 빼기(2); if (!gwrthrych_VALUE(gwrthrych_cyfeiriad, 16)) return;
                int cofnod_safle = Word_SMS(enw_cysonyn, "getData") ? 2 : Word_SMS(enw_cysonyn, "getLength") ? 3 : Word_SMS(enw_cysonyn, "getAddress") ? 4 : 5;
                넣기(힙[gwrthrych_cyfeiriad + cofnod_safle], cofnod_safle == 2 || cofnod_safle == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(perchennog, "java/net/DatagramSocket")) {
            if (gorchymyn_cod == 183 && Word_SMS(enw_cysonyn, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int rhif_porth = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), gwrthrych_cyfeiriad = 빼기(2); if (!gwrthrych_VALUE(gwrthrych_cyfeiriad, 15)) return;
                if (rhif_porth < 0 || rhif_porth > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = defnyddiwr.agor_Rhwydwaith(rhif_porth); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[gwrthrych_cyfeiriad + 2] = 열린파일번호; return;
            }
            if (gorchymyn_cod == 182 && Word_SMS(enw_cysonyn, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), gwrthrych_cyfeiriad = 빼기(2); if (!gwrthrych_VALUE(gwrthrych_cyfeiriad, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[gwrthrych_cyfeiriad + 3] = 밀리초값; return;
            }
            if (gorchymyn_cod == 182 && Word_SMS(enw_cysonyn, "getLocalPort") && Word_SMS(서술상수, "()I")) { int gwrthrych_cyfeiriad = 빼기(2); if (gwrthrych_VALUE(gwrthrych_cyfeiriad, 15)) 넣기(힙[gwrthrych_cyfeiriad + 2] < 0 ? -1 : defnyddiwr.Rhwydwaith_porth(힙[gwrthrych_cyfeiriad + 2]), 1); return; }
            if (gorchymyn_cod == 182 && Word_SMS(enw_cysonyn, "isClosed") && Word_SMS(서술상수, "()Z")) { int gwrthrych_cyfeiriad = 빼기(2); if (gwrthrych_VALUE(gwrthrych_cyfeiriad, 15)) 넣기(힙[gwrthrych_cyfeiriad + 2] < 0 ? 1 : 0, 1); return; }
            if (gorchymyn_cod == 182 && Word_SMS(enw_cysonyn, "close") && Word_SMS(서술상수, "()V")) { int gwrthrych_cyfeiriad = 빼기(2); if (gwrthrych_VALUE(gwrthrych_cyfeiriad, 15) && 힙[gwrthrych_cyfeiriad + 2] >= 0) { defnyddiwr.파일서술자닫기(힙[gwrthrych_cyfeiriad + 2]); 힙[gwrthrych_cyfeiriad + 2] = -1; } return; }
            if (gorchymyn_cod == 182 && (Word_SMS(enw_cysonyn, "send") || Word_SMS(enw_cysonyn, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int 전문참조 = 빼기(2), gwrthrych_cyfeiriad = 빼기(2); if (!gwrthrych_VALUE(전문참조, 16) || !gwrthrych_VALUE(gwrthrych_cyfeiriad, 15)) return;
                int data_ARAE = 힙[전문참조 + 2], 유효길이 = 힙[전문참조 + 3], 열린파일번호 = 힙[gwrthrych_cyfeiriad + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(enw_cysonyn, "send")) {
                    if (!gwrthrych_VALUE(힙[전문참조 + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = 힙[data_ARAE + 2 + Loop_INDEX];
                    if (defnyddiwr.anfon_Rhwydwaith(열린파일번호, 힙[힙[전문참조 + 4] + 2], 힙[전문참조 + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int cofnod_COUNT = defnyddiwr.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (cofnod_COUNT == -11) {
                        int 현재시각 = defnyddiwr.밀리초();
                        if (힙[gwrthrych_cyfeiriad + 4] == 0) 힙[gwrthrych_cyfeiriad + 4] = 현재시각 + 1;
                        if (힙[gwrthrych_cyfeiriad + 3] > 0 && 현재시각 - (힙[gwrthrych_cyfeiriad + 4] - 1) >= 힙[gwrthrych_cyfeiriad + 3]) { 힙[gwrthrych_cyfeiriad + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(gwrthrych_cyfeiriad, 2); 넣기(전문참조, 2); ffrâm_safle[ffrâm_INDEX] = ffrâm_cyfarwyddyd[ffrâm_INDEX]; newid_cais_HTTP = true; return;
                    }
                    힙[gwrthrych_cyfeiriad + 4] = 0;
                    if (cofnod_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < cofnod_COUNT; Loop_INDEX++) 힙[data_ARAE + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    힙[전문참조 + 3] = cofnod_COUNT; 힙[전문참조 + 4] = ADDRESS_gwrthrych(통신임시[513]); 힙참조[전문참조 + 4] = 1; 힙[전문참조 + 5] = 통신임시[512];
                }
                return;
            }
        }
        methiant_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int gwrthrych_cyfeiriad) {
        int 현재시각 = defnyddiwr.밀리초();
        if (힙[gwrthrych_cyfeiriad + 5] == 0) 힙[gwrthrych_cyfeiriad + 5] = 현재시각 + 1;
        if (힙[gwrthrych_cyfeiriad + 3] > 0 && 현재시각 - (힙[gwrthrych_cyfeiriad + 5] - 1) >= 힙[gwrthrych_cyfeiriad + 3]) { 힙[gwrthrych_cyfeiriad + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        ffrâm_safle[ffrâm_INDEX] = ffrâm_cyfarwyddyd[ffrâm_INDEX]; newid_cais_HTTP = true; return true;
    }
    static void 흐름호출(int perchennog, int enw_cysonyn, int 서술상수, int gorchymyn_cod) {
        boolean 수신쪽 = Word_SMS(perchennog, "java/net/ServerSocket"), ffrwd = Word_SMS(perchennog, "java/io/InputStream") || Word_SMS(perchennog, "java/io/OutputStream");
        if (!ffrwd && gorchymyn_cod == 183 && Word_SMS(enw_cysonyn, "<init>")) {
            boolean technoleg_gwybodaeth_gwag_cyflwr = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(technoleg_gwybodaeth_gwag_cyflwr || 수신쪽 && Word_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { methiant_VALUE("unsupported socket constructor"); return; }
            int rhif_porth = technoleg_gwybodaeth_gwag_cyflwr ? 0 : 빼기(1), ADDRESS_cyfeiriad = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, gwrthrych_cyfeiriad = 빼기(2);
            if (!gwrthrych_VALUE(gwrthrych_cyfeiriad, 수신쪽 ? 18 : 17)) return;
            if (rhif_porth < 0 || rhif_porth > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !gwrthrych_VALUE(ADDRESS_cyfeiriad, 14)) return;
            int Rhwydwaith_ADDRESS = 이름지정여부 ? 주소해독(ADDRESS_cyfeiriad) : 주소지정여부 ? 힙[ADDRESS_cyfeiriad + 2] : 0x7f000001;
            if (Gwall || 던진객체 != 0) return;
            int 열린파일번호 = defnyddiwr.ffrwd_rheoli(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = technoleg_gwybodaeth_gwag_cyflwr ? 0 : 수신쪽 ? defnyddiwr.ffrwd_rheoli(1, 열린파일번호, rhif_porth) : defnyddiwr.Cysylltu_ffrwd(열린파일번호, Rhwydwaith_ADDRESS, rhif_porth);
            if (처리값 < 0) { defnyddiwr.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[gwrthrych_cyfeiriad + 2] = 열린파일번호; 힙[gwrthrych_cyfeiriad + 4] = rhif_porth; 힙[gwrthrych_cyfeiriad + 6] = technoleg_gwybodaeth_gwag_cyflwr ? 0 : 1; return;
        }
        if (!ffrwd && Word_SMS(enw_cysonyn, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), gwrthrych_cyfeiriad = 빼기(2); if (!gwrthrych_VALUE(gwrthrych_cyfeiriad, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[gwrthrych_cyfeiriad + 3] = 밀리초값; return; }
        if (!ffrwd && Word_SMS(enw_cysonyn, "close") && Word_SMS(서술상수, "()V")) { int gwrthrych_cyfeiriad = 빼기(2); if (gwrthrych_VALUE(gwrthrych_cyfeiriad, 수신쪽 ? 18 : 17) && 힙[gwrthrych_cyfeiriad + 2] >= 0) { defnyddiwr.파일서술자닫기(힙[gwrthrych_cyfeiriad + 2]); 힙[gwrthrych_cyfeiriad + 2] = -1; } return; }
        if (!ffrwd && (Word_SMS(enw_cysonyn, "getLocalPort") || Word_SMS(enw_cysonyn, "getPort") || Word_SMS(enw_cysonyn, "isClosed") || Word_SMS(enw_cysonyn, "isConnected"))) {
            int gwrthrych_cyfeiriad = 빼기(2); if (!gwrthrych_VALUE(gwrthrych_cyfeiriad, 수신쪽 ? 18 : 17)) return;
            넣기(Word_SMS(enw_cysonyn, "isClosed") ? 힙[gwrthrych_cyfeiriad + 2] < 0 ? 1 : 0 : Word_SMS(enw_cysonyn, "isConnected") ? 힙[gwrthrych_cyfeiriad + 6] : Word_SMS(enw_cysonyn, "getPort") ? 힙[gwrthrych_cyfeiriad + 4] : 힙[gwrthrych_cyfeiriad + 2] < 0 ? -1 : defnyddiwr.ffrwd_rheoli(4, 힙[gwrthrych_cyfeiriad + 2], 0), 1); return;
        }
        if (수신쪽 && Word_SMS(enw_cysonyn, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int gwrthrych_cyfeiriad = 빼기(2); if (!gwrthrych_VALUE(gwrthrych_cyfeiriad, 18)) return; int 열린파일번호 = defnyddiwr.ffrwd_rheoli(3, 힙[gwrthrych_cyfeiriad + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(gwrthrych_cyfeiriad)) 넣기(gwrthrych_cyfeiriad, 2); return; }
            힙[gwrthrych_cyfeiriad + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = dyrannu_Storio(17, 5); if (Gwall) { defnyddiwr.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = defnyddiwr.ffrwd_rheoli(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !ffrwd && ((Word_SMS(enw_cysonyn, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(enw_cysonyn, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int gwrthrych_cyfeiriad = 빼기(2); if (!gwrthrych_VALUE(gwrthrych_cyfeiriad, 17)) return; if (힙[gwrthrych_cyfeiriad + 2] < 0 || 힙[gwrthrych_cyfeiriad + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = dyrannu_Storio(19, 4); if (Gwall) return; 힙[반환값 + 2] = gwrthrych_cyfeiriad; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(enw_cysonyn, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (ffrwd) {
            boolean 읽기여부 = Word_SMS(enw_cysonyn, "read"), technoleg_gwybodaeth_ysgrifennu_gweithrediad = Word_SMS(enw_cysonyn, "write"), rhwystro = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), technoleg_gwybodaeth_IS_ARAE = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int cofnod_COUNT = technoleg_gwybodaeth_IS_ARAE ? 빼기(1) : 0, 시작변위 = technoleg_gwybodaeth_IS_ARAE ? 빼기(1) : 0, data_ARAE = rhwystro || technoleg_gwybodaeth_IS_ARAE ? 빼기(2) : 0;
            int data_VALUE = technoleg_gwybodaeth_ysgrifennu_gweithrediad && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, gwrthrych_cyfeiriad = 빼기(2);
            if (!gwrthrych_VALUE(gwrthrych_cyfeiriad, 19)) return; int 부모참조 = 힙[gwrthrych_cyfeiriad + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(enw_cysonyn, "close") && Word_SMS(서술상수, "()V")) { defnyddiwr.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Word_SMS(enw_cysonyn, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !technoleg_gwybodaeth_ysgrifennu_gweithrediad) || 읽기여부 != (힙[gwrthrych_cyfeiriad + 3] == 0)) { methiant_VALUE("unsupported stream operation"); return; }
            if (rhwystro || technoleg_gwybodaeth_IS_ARAE) { if (!gwrthrych_VALUE(data_ARAE, 20)) return; if (rhwystro) cofnod_COUNT = 힙[data_ARAE + 1]; if (시작변위 < 0 || cofnod_COUNT < 0 || 시작변위 > 힙[data_ARAE + 1] - cofnod_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else cofnod_COUNT = 1;
            if (cofnod_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = technoleg_gwybodaeth_ysgrifennu_gweithrediad ? 힙[gwrthrych_cyfeiriad + 4] : 0, 처리값 = 0;
            while (완료수 < cofnod_COUNT) {
                처리값 = 읽기여부 ? defnyddiwr.파일한바이트읽기(열린파일번호) : defnyddiwr.파일한바이트쓰기(열린파일번호, rhwystro || technoleg_gwybodaeth_IS_ARAE ? 힙[data_ARAE + 2 + 시작변위 + 완료수] : data_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (rhwystro || technoleg_gwybodaeth_IS_ARAE)) 힙[data_ARAE + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(rhwystro || technoleg_gwybodaeth_IS_ARAE)) break;
            }
            if (처리값 == -11 && (technoleg_gwybodaeth_ysgrifennu_gweithrediad || 완료수 == 0)) {
                힙[gwrthrych_cyfeiriad + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(gwrthrych_cyfeiriad, 2); if (rhwystro || technoleg_gwybodaeth_IS_ARAE) 넣기(data_ARAE, 2); if (technoleg_gwybodaeth_IS_ARAE) { 넣기(시작변위, 1); 넣기(cofnod_COUNT, 1); } if (technoleg_gwybodaeth_ysgrifennu_gweithrediad && !(rhwystro || technoleg_gwybodaeth_IS_ARAE)) 넣기(data_VALUE, 1); } return;
            }
            힙[gwrthrych_cyfeiriad + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : rhwystro || technoleg_gwybodaeth_IS_ARAE ? 완료수 : 처리값, 1); return;
        }
        methiant_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int enw_cysonyn) {
        if (Word_SMS(enw_cysonyn, "Cymraeg/자체/ffenestr")) return 24;
        if (Word_SMS(enw_cysonyn, "Cymraeg/자체/label")) return 26;
        if (Word_SMS(enw_cysonyn, "Cymraeg/자체/botwm")) return 27;
        if (Word_SMS(enw_cysonyn, "Cymraeg/자체/maes_testun")) return 28;
        if (Word_SMS(enw_cysonyn, "Cymraeg/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int enw_cysonyn) {
        return 한국어화면종(enw_cysonyn) != 0 || Word_SMS(enw_cysonyn, "Cymraeg/자체/화면구성요소") || Word_SMS(enw_cysonyn, "Cymraeg/자체/digwyddiad_ciw");
    }
    static int 화면종(int enw_cysonyn) {
        int 한국어종 = 한국어화면종(enw_cysonyn); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(enw_cysonyn, "javax/swing/JFrame")) return 24;
        if (Word_SMS(enw_cysonyn, "javax/swing/JPanel")) return 25;
        if (Word_SMS(enw_cysonyn, "javax/swing/JLabel")) return 26;
        if (Word_SMS(enw_cysonyn, "javax/swing/JButton")) return 27;
        if (Word_SMS(enw_cysonyn, "javax/swing/JTextField")) return 28;
        if (Word_SMS(enw_cysonyn, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(enw_cysonyn, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int enw_cysonyn) {
        return 화면종(enw_cysonyn) != 0 || Word_SMS(enw_cysonyn, "java/awt/Component") || Word_SMS(enw_cysonyn, "java/awt/Container") || Word_SMS(enw_cysonyn, "javax/swing/JComponent") || Word_SMS(enw_cysonyn, "javax/swing/AbstractButton") || Word_SMS(enw_cysonyn, "javax/swing/text/JTextComponent") || Word_SMS(enw_cysonyn, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int gwrthrych_cyfeiriad) { if (!객체유효(gwrthrych_cyfeiriad)) return false; if (힙[gwrthrych_cyfeiriad] < 24 || 힙[gwrthrych_cyfeiriad] > 28) { methiant_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int gwrthrych_cyfeiriad, int SMS_cyfeiriad) {
        if (SMS_cyfeiriad != 0 && !gwrthrych_VALUE(SMS_cyfeiriad, 1)) return;
        int cofnod_COUNT = SMS_cyfeiriad == 0 ? 0 : 힙[SMS_cyfeiriad + 1]; if (cofnod_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < cofnod_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = 힙[SMS_cyfeiriad + 2 + Loop_INDEX];
        if (defnyddiwr.화면글(힙[gwrthrych_cyfeiriad + 2], 화면글임시, cofnod_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[gwrthrych_cyfeiriad + 3] = SMS_cyfeiriad; 힙참조[gwrthrych_cyfeiriad + 3] = 1;
    }
    static int 화면문자읽기(int gwrthrych_cyfeiriad) {
        int cyfrif_VALUE = 힙[gwrthrych_cyfeiriad + 2], cofnod_COUNT = defnyddiwr.화면연결(8, cyfrif_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (cofnod_COUNT < 0) { methiant_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < cofnod_COUNT; Loop_INDEX++) { int 부호값 = defnyddiwr.화면연결(9, cyfrif_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = dyrannu_Storio(1, 사용수); if (!Gwall) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* Cymraeg 객체를 직접 만들고 cnewyllyn_VALUE 화면 기능에 연결한다. Swing gwrthrych_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int perchennog, int enw_cysonyn, int 서술상수, int gorchymyn_cod) {
        if (Word_SMS(perchennog, "Cymraeg/자체/digwyddiad_ciw")) {
            if (gorchymyn_cod == 184 && Word_SMS(enw_cysonyn, "나중에실행") && Word_SMS(서술상수, "(LCymraeg/자체/실행할일;)V")) {
                int tasg_gweithred = 빼기(2); if (!객체유효(tasg_gweithred)) return;
                if (나중수 == 8) { methiant_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = tasg_gweithred; return;
            }
            if (gorchymyn_cod == 184 && Word_SMS(enw_cysonyn, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            methiant_VALUE("지원하지 않는 Cymraeg 화면 일정 호출"); return;
        }
        if (Word_SMS(perchennog, "Cymraeg/자체/동작알림")) {
            int 알림 = 빼기(2); if (!gwrthrych_VALUE(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Word_SMS(enw_cysonyn, "digwyddiad_ffynhonnell") && Word_SMS(서술상수, "()LCymraeg/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Word_SMS(enw_cysonyn, "gorchymyn_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Word_SMS(enw_cysonyn, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else methiant_VALUE("지원하지 않는 Cymraeg Gweithrediad 알림 호출"); return;
        }
        if (gorchymyn_cod == 183 && Word_SMS(enw_cysonyn, "<init>")) {
            int 종류 = 한국어화면종(perchennog), 받이 = 0, 가로 = 0, Ar_i_fyny_safle = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (defnyddiwr.화면너비() - 폭) / 2; Ar_i_fyny_safle = (defnyddiwr.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIILCymraeg/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Ar_i_fyny_safle = 빼기(1); 가로 = 빼기(1);
            } else { methiant_VALUE("지원하지 않는 Cymraeg 화면 생성자"); return; }
            int Testun = 빼기(2), elfen_VALUE = 빼기(2); if (!화면객체(elfen_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Ar_i_fyny_safle < 0 || 폭 > defnyddiwr.화면너비() - 가로 || 높이 > defnyddiwr.화면높이() - Ar_i_fyny_safle) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = defnyddiwr.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { methiant_VALUE("화면 elfen_VALUE 자리가 가득 찼습니다"); return; }
            힙[elfen_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = elfen_VALUE;
            힙[elfen_VALUE + 5] = 가로; 힙[elfen_VALUE + 6] = Ar_i_fyny_safle; 힙[elfen_VALUE + 7] = 폭; 힙[elfen_VALUE + 8] = 높이; 힙[elfen_VALUE + 10] = 2;
            힙[elfen_VALUE + 4] = 받이; 힙참조[elfen_VALUE + 4] = 1; 힙[elfen_VALUE + 12] = 1;
            defnyddiwr.화면연결(1, INDEX, 가로, Ar_i_fyny_safle, 폭, 높이);
            if (종류 == 24) defnyddiwr.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(elfen_VALUE, Testun); return;
        }
        if (gorchymyn_cod != 182) { methiant_VALUE("잘못된 Cymraeg 화면 호출 Gorchymyn"); return; }
        if (Word_SMS(enw_cysonyn, "ysgrifennu_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Testun = 빼기(2), elfen_VALUE = 빼기(2); if (화면객체(elfen_VALUE)) 화면문자설정(elfen_VALUE, Testun); return;
        }
        if (Word_SMS(enw_cysonyn, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int elfen_VALUE = 빼기(2); if (화면객체(elfen_VALUE)) 넣기(화면문자읽기(elfen_VALUE), 2); return;
        }
        if (Word_SMS(enw_cysonyn, "동작맡기기") && Word_SMS(서술상수, "(LCymraeg/자체/동작받이;)V")) {
            int 받이 = 빼기(2), elfen_VALUE = 빼기(2);
            if (화면객체(elfen_VALUE)) { 힙[elfen_VALUE + 4] = 받이; 힙참조[elfen_VALUE + 4] = 1; 힙[elfen_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(enw_cysonyn, "ychwanegu_elfen") && Word_SMS(서술상수, "(LCymraeg/자체/화면구성요소;)V")) {
            int iselfen_VALUE = 빼기(2), 부모 = 빼기(2); if (!화면객체(iselfen_VALUE) || !화면객체(부모)) return;
            if (defnyddiwr.화면연결(2, 힙[부모 + 2], 힙[iselfen_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[iselfen_VALUE + 11] = 부모; 힙참조[iselfen_VALUE + 11] = 1; return;
        }
        if (Word_SMS(enw_cysonyn, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Ar_i_fyny_safle = 빼기(1), 가로 = 빼기(1), elfen_VALUE = 빼기(2); if (!화면객체(elfen_VALUE)) return;
            if (defnyddiwr.화면연결(1, 힙[elfen_VALUE + 2], 가로, Ar_i_fyny_safle, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[elfen_VALUE + 5] = 가로; 힙[elfen_VALUE + 6] = Ar_i_fyny_safle; 힙[elfen_VALUE + 7] = 폭; 힙[elfen_VALUE + 8] = 높이; return;
        }
        if ((Word_SMS(enw_cysonyn, "sioe_ffenestr") || Word_SMS(enw_cysonyn, "Cau")) && Word_SMS(서술상수, "()V")) {
            boolean gwelededd_VALUE = Word_SMS(enw_cysonyn, "sioe_ffenestr"); int elfen_VALUE = 빼기(2); if (!화면객체(elfen_VALUE)) return;
            if (defnyddiwr.화면연결(gwelededd_VALUE ? 3 : 4, 힙[elfen_VALUE + 2], gwelededd_VALUE ? 1 : 0, 0, 0, 0) < 0) { methiant_VALUE("화면은 rhyngweithiol 명령에서 실행해야 합니다"); return; }
            힙[elfen_VALUE + 9] = gwelededd_VALUE ? 1 : 0; return;
        }
        if (Word_SMS(enw_cysonyn, "보이는가") && Word_SMS(서술상수, "()Z")) { int elfen_VALUE = 빼기(2); if (화면객체(elfen_VALUE)) 넣기(힙[elfen_VALUE + 9], 1); return; }
        methiant_VALUE("지원하지 않는 Cymraeg 화면 dull_VALUE");
    }
    static void 화면호출(int perchennog, int enw_cysonyn, int 서술상수, int gorchymyn_cod) {
        if (Word_SMS(perchennog, "javax/swing/SwingUtilities")) {
            if (gorchymyn_cod == 184 && Word_SMS(enw_cysonyn, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int gwrthrych_cyfeiriad = 빼기(2); if (!객체유효(gwrthrych_cyfeiriad)) return; if (나중수 == 8) { methiant_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = gwrthrych_cyfeiriad; return; }
            if (gorchymyn_cod == 184 && Word_SMS(enw_cysonyn, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            methiant_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(perchennog, "java/awt/event/ActionEvent")) {
            int gwrthrych_cyfeiriad = 빼기(2); if (!gwrthrych_VALUE(gwrthrych_cyfeiriad, 29)) return;
            if (Word_SMS(enw_cysonyn, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[gwrthrych_cyfeiriad + 2], 2);
            else if (Word_SMS(enw_cysonyn, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[gwrthrych_cyfeiriad + 2]), 2);
            else if (Word_SMS(enw_cysonyn, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else methiant_VALUE("unsupported ActionEvent method"); return;
        }
        if (gorchymyn_cod == 183 && Word_SMS(enw_cysonyn, "<init>")) {
            int COLUMNS = 0, SMS_cyfeiriad = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_cyfeiriad = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_cyfeiriad = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { methiant_VALUE("unsupported Swing constructor"); return; }
            int gwrthrych_cyfeiriad = 빼기(2); if (!객체유효(gwrthrych_cyfeiriad)) return;
            if (힙[gwrthrych_cyfeiriad] == 30) { methiant_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(gwrthrych_cyfeiriad) || COLUMNS < 0) return;
            int cyfrif_VALUE = defnyddiwr.화면연결(0, 힙[gwrthrych_cyfeiriad] - 23, 0, 0, 0, 0);
            if (cyfrif_VALUE < 1 || cyfrif_VALUE > 32) { methiant_VALUE("GUI widget slots exhausted"); return; }
            힙[gwrthrych_cyfeiriad + 2] = cyfrif_VALUE; 화면참조[cyfrif_VALUE - 1] = gwrthrych_cyfeiriad; 힙[gwrthrych_cyfeiriad + 5] = 힙[gwrthrych_cyfeiriad] == 24 ? 130 : 16; 힙[gwrthrych_cyfeiriad + 6] = 힙[gwrthrych_cyfeiriad] == 24 ? 110 : 16;
            힙[gwrthrych_cyfeiriad + 7] = 힙[gwrthrych_cyfeiriad] == 24 ? 380 : 220; 힙[gwrthrych_cyfeiriad + 8] = 힙[gwrthrych_cyfeiriad] == 24 ? 240 : 28; 힙[gwrthrych_cyfeiriad + 10] = 1;
            화면문자설정(gwrthrych_cyfeiriad, SMS_cyfeiriad); return;
        }
        if (Word_SMS(enw_cysonyn, "setText") || Word_SMS(enw_cysonyn, "setTitle")) { int SMS_cyfeiriad = 빼기(2), gwrthrych_cyfeiriad = 빼기(2); if (화면객체(gwrthrych_cyfeiriad) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(gwrthrych_cyfeiriad, SMS_cyfeiriad); return; }
        if (Word_SMS(enw_cysonyn, "getText") || Word_SMS(enw_cysonyn, "getTitle")) { int gwrthrych_cyfeiriad = 빼기(2); if (화면객체(gwrthrych_cyfeiriad) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(gwrthrych_cyfeiriad), 2); return; }
        if (Word_SMS(enw_cysonyn, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), gwrthrych_cyfeiriad = 빼기(2); if (화면객체(gwrthrych_cyfeiriad)) { 힙[gwrthrych_cyfeiriad + 4] = 수신참조; 힙참조[gwrthrych_cyfeiriad + 4] = 1; } return; }
        if (Word_SMS(enw_cysonyn, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int gwrthrych_cyfeiriad = 빼기(2); if (화면객체(gwrthrych_cyfeiriad)) 넣기(gwrthrych_cyfeiriad, 2); return; }
        if (Word_SMS(enw_cysonyn, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Llywio_cyfeiriad = 빼기(2), gwrthrych_cyfeiriad = 빼기(2); if (화면객체(gwrthrych_cyfeiriad) && Llywio_cyfeiriad != 0) methiant_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(enw_cysonyn, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Llywio_cyflwr = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Llywio_cyflwr) 빼기(2);
            int iselfen_cyfeiriad = 빼기(2), gwrthrych_cyfeiriad = 빼기(2); if (!화면객체(iselfen_cyfeiriad) || !화면객체(gwrthrych_cyfeiriad)) return;
            if (defnyddiwr.화면연결(2, 힙[gwrthrych_cyfeiriad + 2], 힙[iselfen_cyfeiriad + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[iselfen_cyfeiriad + 11] = gwrthrych_cyfeiriad; 힙참조[iselfen_cyfeiriad + 11] = 1; if (!Llywio_cyflwr) 넣기(iselfen_cyfeiriad, 2); return;
        }
        if (Word_SMS(enw_cysonyn, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Y_cyfesuryn = 빼기(1), cyfesuryn_x = 빼기(1), gwrthrych_cyfeiriad = 빼기(2); if (!화면객체(gwrthrych_cyfeiriad)) return;
            if (defnyddiwr.화면연결(1, 힙[gwrthrych_cyfeiriad + 2], cyfesuryn_x, Y_cyfesuryn, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[gwrthrych_cyfeiriad + 5] = cyfesuryn_x; 힙[gwrthrych_cyfeiriad + 6] = Y_cyfesuryn; 힙[gwrthrych_cyfeiriad + 7] = 너비; 힙[gwrthrych_cyfeiriad + 8] = 높이; return;
        }
        if (Word_SMS(enw_cysonyn, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), gwrthrych_cyfeiriad = 빼기(2); if (!화면객체(gwrthrych_cyfeiriad)) return;
            if (defnyddiwr.화면연결(1, 힙[gwrthrych_cyfeiriad + 2], 힙[gwrthrych_cyfeiriad + 5], 힙[gwrthrych_cyfeiriad + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[gwrthrych_cyfeiriad + 7] = 너비; 힙[gwrthrych_cyfeiriad + 8] = 높이; } return;
        }
        if (Word_SMS(enw_cysonyn, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), gwrthrych_cyfeiriad = 빼기(2); if (!화면객체(gwrthrych_cyfeiriad)) return; if (상대배치 != 0) { methiant_VALUE("only screen centering supported"); return; } 힙[gwrthrych_cyfeiriad + 5] = (defnyddiwr.화면너비() - 힙[gwrthrych_cyfeiriad + 7]) / 2; 힙[gwrthrych_cyfeiriad + 6] = (defnyddiwr.화면높이() - 힙[gwrthrych_cyfeiriad + 8]) / 2; defnyddiwr.화면연결(1, 힙[gwrthrych_cyfeiriad + 2], 힙[gwrthrych_cyfeiriad + 5], 힙[gwrthrych_cyfeiriad + 6], 힙[gwrthrych_cyfeiriad + 7], 힙[gwrthrych_cyfeiriad + 8]); return; }
        if (Word_SMS(enw_cysonyn, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int polisi = 빼기(1), gwrthrych_cyfeiriad = 빼기(2); if (화면객체(gwrthrych_cyfeiriad)) { if (polisi < 0 || polisi > 3) 예외던짐(9, "close policy"); else { 힙[gwrthrych_cyfeiriad + 10] = polisi; defnyddiwr.화면연결(7, 힙[gwrthrych_cyfeiriad + 2], polisi, 0, 0, 0); } } return; }
        if (Word_SMS(enw_cysonyn, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int data_VALUE = 빼기(1), gwrthrych_cyfeiriad = 빼기(2); if (화면객체(gwrthrych_cyfeiriad)) { int 처리값 = defnyddiwr.화면연결(3, 힙[gwrthrych_cyfeiriad + 2], data_VALUE, 0, 0, 0); if (처리값 < 0) methiant_VALUE("Swing requires a standalone interactive command"); else 힙[gwrthrych_cyfeiriad + 9] = data_VALUE; } return; }
        if (Word_SMS(enw_cysonyn, "dispose") && Word_SMS(서술상수, "()V")) { int gwrthrych_cyfeiriad = 빼기(2); if (화면객체(gwrthrych_cyfeiriad)) { defnyddiwr.화면연결(4, 힙[gwrthrych_cyfeiriad + 2], 0, 0, 0, 0); 힙[gwrthrych_cyfeiriad + 9] = 0; } return; }
        if (Word_SMS(enw_cysonyn, "repaint") || Word_SMS(enw_cysonyn, "validate")) { int gwrthrych_cyfeiriad = 빼기(2); if (!화면객체(gwrthrych_cyfeiriad) || !Word_SMS(서술상수, "()V")) return; defnyddiwr.화면연결(1, 힙[gwrthrych_cyfeiriad + 2], 힙[gwrthrych_cyfeiriad + 5], 힙[gwrthrych_cyfeiriad + 6], 힙[gwrthrych_cyfeiriad + 7], 힙[gwrthrych_cyfeiriad + 8]); return; }
        if (Word_SMS(enw_cysonyn, "isVisible") && Word_SMS(서술상수, "()Z")) { int gwrthrych_cyfeiriad = 빼기(2); if (화면객체(gwrthrych_cyfeiriad)) 넣기(힙[gwrthrych_cyfeiriad + 9], 1); return; }
        methiant_VALUE("unsupported Swing method (native subset)");
    }
    static void 사건실행(int targed_ADDRESS, int 사건번호, boolean Cymraeg) {
        if (targed_ADDRESS < 1 || 힙[targed_ADDRESS] < 32) { methiant_VALUE("Java event listener required"); return; }
        int ffeil_INDEX = enw_dull(힙[targed_ADDRESS] - 32, 사건번호 == 0 ? (Cymraeg ? "Gweithredu" : "run") : (Cymraeg ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (Cymraeg ? "(LCymraeg/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (ffeil_INDEX < 0) { methiant_VALUE("event callback missing"); return; }
        현재가닥 = 0; edefyn_COUNT = 1; ffrâm_INDEX = 0; edefyn_cyflwr[0] = 1; ffrâm_pentwr[0] = 0; 틀잠금[0] = ymgychwyn_ffrâm[0] = 0; newid_cais_HTTP = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { lleol_VALUE[Loop_INDEX] = lleol_TYPE[Loop_INDEX] = 0; }
        ffrâm_dull[0] = ffeil_INDEX; ffrâm_safle[0] = dull_START[ffeil_INDEX]; lleol_VALUE[0] = targed_ADDRESS; lleol_TYPE[0] = 2;
        if (사건번호 != 0) { lleol_VALUE[1] = 사건번호; lleol_TYPE[1] = 2; }
        사건중 = true; Gweithredu_gorchymyn(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!Gwall) {
            if (나중수 > 0) { int targed_ADDRESS = 나중실행[0], Cymraeg = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(targed_ADDRESS, 0, Cymraeg != 0); continue; }
            if (defnyddiwr.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = defnyddiwr.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { methiant_VALUE("GUI event I/O failed"); return; }
            int cyfrif_VALUE = 사건번호 & 65535; if (cyfrif_VALUE < 1 || cyfrif_VALUE > 32) continue; int gwrthrych_cyfeiriad = 화면참조[cyfrif_VALUE - 1]; if (gwrthrych_cyfeiriad == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[gwrthrych_cyfeiriad + 10] != 0) 힙[gwrthrych_cyfeiriad + 9] = 0;
                if (힙[gwrthrych_cyfeiriad + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && 힙[화면참조[Loop_INDEX]] == 24) defnyddiwr.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[gwrthrych_cyfeiriad + 4] != 0) {
                int GWYBODAETH_cyfeiriad = dyrannu_Storio(29, 2); if (Gwall) return; 힙[GWYBODAETH_cyfeiriad + 2] = gwrthrych_cyfeiriad; 힙[GWYBODAETH_cyfeiriad + 3] = 힙[gwrthrych_cyfeiriad + 12]; 힙참조[GWYBODAETH_cyfeiriad + 2] = 1; 사건실행(힙[gwrthrych_cyfeiriad + 4], GWYBODAETH_cyfeiriad, 힙[gwrthrych_cyfeiriad + 12] != 0);
            }
        }
    }
    public static int Gweithredu_2() {
        if (defnyddiwr.인수개수() == 1 && 자바도구.같음(defnyddiwr.인수(0), "-version")) {
            defnyddiwr.Ysgrifennu("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (defnyddiwr.인수개수() < 1) { defnyddiwr.Ysgrifennu("Usage: java CLASS [ARGS]\n"); return 2; }
        cofnod_Dosbarth_Diffiniad = llwyth_Dosbarth_Diffiniad(lletya_nod(defnyddiwr.인수(0))); if (Gwall || cofnod_Dosbarth_Diffiniad < 0) return 1;
        int cofnod_p_VALUE = enw_dull(cofnod_Dosbarth_Diffiniad, "Gweithredu_2", "()V");
        boolean 한국어진입 = cofnod_p_VALUE >= 0 && (dull_mynediad[cofnod_p_VALUE] & 9) == 9;
        if (!한국어진입) cofnod_p_VALUE = enw_dull(cofnod_Dosbarth_Diffiniad, "main", "([Ljava/lang/String;)V");
        if (cofnod_p_VALUE < 0 || (dull_mynediad[cofnod_p_VALUE] & 9) != 9) methiant_VALUE("public static void Gweithredu_2() or main(String[] args) required");
        if (Gwall) return 1;
        int 인수 = dyrannu_Storio(3, defnyddiwr.인수개수() - 1); ARAE_elfen[인수] = -1;
        for (int 수 = 1; 수 < defnyddiwr.인수개수() && !Gwall; 수++) 힙[인수 + 1 + 수] = lletya_nod(defnyddiwr.인수(수));
        ffrâm_INDEX = 0; ffrâm_dull[0] = cofnod_p_VALUE; ffrâm_safle[0] = dull_START[cofnod_p_VALUE]; lleol_VALUE[0] = 한국어진입 ? 0 : 인수; lleol_TYPE[0] = 한국어진입 ? 0 : 2;
        edefyn_cyflwr[0] = 1; edefyn_gwrthrych[0] = dyrannu_Storio(13, 2);
        Gweithredu_gorchymyn(); if (!Gwall) 화면사건들(); return Gwall ? 1 : 0;
    }
}
