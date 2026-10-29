// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Ffeil/스택/cyfeiriad/cangen 경계를 Gweithredu_gorchymyn 중 검사한다. */
public final class 자바가상기계 {
    static int[] Ffeil = new int[16384], ffeil_enw_SMS = new int[64];
    static int[] cysonyn_tag = new int[512], 상가 = new int[512], cysonyn_SECOND_VALUE = new int[512], testun_cyfeiriad = new int[512];
    static int[] dull_enw_SMS = new int[32], dull_TYPE = new int[32], dull_mynediad = new int[32];
    static int[] dull_START = new int[32], dull_gorffen = new int[32], dull_pentwr = new int[32], 함수지역 = new int[32];
    static int[] dull_arg_COUNT = new int[32], dull_arg_TYPE = new int[512], dull_return = new int[32];
    static int[] 경계 = new int[16384];
    static int[] lleol_VALUE = new int[4096], lleol_TYPE = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] ffrâm_dull = new int[32], ffrâm_safle = new int[32], ffrâm_pentwr = new int[32];
    static int[] 힙 = new int[8192];
    static int Maint, 읽기위치, cysonyn_COUNT, dull_COUNT, Dosbarth_enw, ffrâm_INDEX = -1, 힙끝 = 1, return_TYPE;
    static boolean Gwall;

    static void methiant_VALUE(String Word_SMS) {
        if (!Gwall) { defnyddiwr.Ysgrifennu("JVM error: "); defnyddiwr.Ysgrifennu(Word_SMS); defnyddiwr.ysgrifennu_nod_VALUE(10); }
        Gwall = true;
    }
    static boolean clip(int Gweithredu_2, int hyd_VALUE) { return Gweithredu_2 >= 0 && hyd_VALUE >= 0 && Gweithredu_2 <= Maint - hyd_VALUE; }
    static int beit_VALUE() {
        if (!clip(읽기위치, 1)) { methiant_VALUE("truncated class file"); return 0; }
        return Ffeil[읽기위치++];
    }
    static int 짧은수() { return beit_VALUE() << 8 | beit_VALUE(); }
    static int cyfanrif() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int hyd_VALUE) { if (!clip(읽기위치, hyd_VALUE)) methiant_VALUE("invalid attribute size"); else 읽기위치 += hyd_VALUE; }
    static boolean gwirio_cysonyn(int 수, int 종류) {
        if (수 <= 0 || 수 >= cysonyn_COUNT || cysonyn_tag[수] != 종류) { methiant_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Gweithredu_2, int hyd_VALUE, String Word_SMS) {
        if (!clip(Gweithredu_2, hyd_VALUE) || hyd_VALUE != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < hyd_VALUE; 수++) if (Ffeil[Gweithredu_2 + 수] != Word_SMS.charAt(수)) return false;
        return true;
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
    static void 속성건너() {
        int eitem_COUNT = 짧은수();
        for (int 수 = 0; 수 < eitem_COUNT && !Gwall; 수++) { gwirio_cysonyn(짧은수(), 1); 건너(cyfanrif()); }
    }
    static int gorchymyn_hyd(int VALUE) {
        if (VALUE == 16 || VALUE == 18 || VALUE == 21 || VALUE == 25 || VALUE == 54 || VALUE == 58 || VALUE == 188) return 2;
        if (VALUE == 17 || VALUE == 19 || VALUE == 132 || VALUE >= 153 && VALUE <= 167
            || VALUE >= 178 && VALUE <= 184 || VALUE == 187 || VALUE == 189 || VALUE == 192 || VALUE == 198 || VALUE == 199) return 3;
        if (VALUE >= 0 && VALUE <= 8 || VALUE >= 26 && VALUE <= 29 || VALUE >= 42 && VALUE <= 46 || VALUE == 50
            || VALUE >= 59 && VALUE <= 62 || VALUE >= 75 && VALUE <= 79 || VALUE == 83 || VALUE == 87 || VALUE == 89 || VALUE == 95
            || VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 116
            || VALUE == 120 || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130
            || VALUE >= 145 && VALUE <= 147 || VALUE == 172 || VALUE == 176 || VALUE == 177 || VALUE == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (cyfanrif() != 0xcafebabe) methiant_VALUE("not a class file");
        int 부판 = 짧은수(), fersiwn_VALUE = 짧은수();
        if (fersiwn_VALUE < 45 || fersiwn_VALUE > 52 || 부판 != 0) methiant_VALUE("supported class versions: 45..52, minor 0");
        cysonyn_COUNT = 짧은수();
        if (cysonyn_COUNT < 1 || cysonyn_COUNT > 512) { methiant_VALUE("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < cysonyn_COUNT && !Gwall; 수++) {
            int 종류 = beit_VALUE(); cysonyn_tag[수] = 종류;
            if (종류 == 1) { cysonyn_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(cysonyn_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = cyfanrif();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); cysonyn_SECOND_VALUE[수] = 짧은수(); }
            else methiant_VALUE("unsupported constant type");
        }
        int hawl_VALUE = 짧은수();
        if ((hawl_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) methiant_VALUE("unsupported class flags");
        Dosbarth_enw = Dosbarth_enw_SMS(짧은수());
        if (!Word_SMS(Dosbarth_enw_SMS(짧은수()), "java/lang/Object")) methiant_VALUE("inheritance unsupported");
        if (짧은수() != 0) methiant_VALUE("interfaces unsupported");
        if (짧은수() != 0) methiant_VALUE("fields unsupported");
        dull_COUNT = 짧은수();
        if (dull_COUNT < 1 || dull_COUNT > 32) { methiant_VALUE("method count limit (32)"); return; }
        for (int 수 = 0; 수 < dull_COUNT && !Gwall; 수++) {
            dull_mynediad[수] = 짧은수(); dull_enw_SMS[수] = 짧은수(); dull_TYPE[수] = 짧은수();
            gwirio_cysonyn(dull_enw_SMS[수], 1); 서술읽기(수);
            if ((dull_mynediad[수] & (0x100 | 0x400 | 0x20)) != 0) methiant_VALUE("native, abstract and synchronized methods unsupported");
            if ((dull_mynediad[수] & 8) == 0 && !Word_SMS(dull_enw_SMS[수], "<init>")) methiant_VALUE("instance methods unsupported");
            if (Word_SMS(dull_enw_SMS[수], "<clinit>")) methiant_VALUE("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(dull_enw_SMS[앞], dull_enw_SMS[수]) && 같은말(dull_TYPE[앞], dull_TYPE[수])) methiant_VALUE("duplicate method");
            int eitem_COUNT = 짧은수();
            for (int priodoledd_VALUE = 0; priodoledd_VALUE < eitem_COUNT && !Gwall; priodoledd_VALUE++) {
                int Enw = 짧은수(), hyd_VALUE = cyfanrif(), Gweithredu_2 = 읽기위치;
                if (!clip(Gweithredu_2, hyd_VALUE)) { methiant_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Enw, "Code")) {
                    if (dull_START[수] != 0) methiant_VALUE("duplicate Code attribute");
                    dull_pentwr[수] = 짧은수(); 함수지역[수] = 짧은수(); int cod_hyd = cyfanrif();
                    if (dull_pentwr[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < dull_arg_COUNT[수]
                        || cod_hyd < 1 || cod_hyd > 8192) methiant_VALUE("method memory limits exceeded");
                    dull_START[수] = 읽기위치; 건너(cod_hyd); dull_gorffen[수] = 읽기위치;
                    if (짧은수() != 0) methiant_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Gweithredu_2 + hyd_VALUE) methiant_VALUE("Code attribute size mismatch");
                } else 건너(hyd_VALUE);
            }
            if (dull_START[수] == 0) methiant_VALUE("missing Code attribute");
            int slot_cofnod = dull_START[수];
            while (slot_cofnod < dull_gorffen[수] && !Gwall) {
                int hyd_VALUE = gorchymyn_hyd(Ffeil[slot_cofnod]);
                if (hyd_VALUE == 0 || hyd_VALUE > dull_gorffen[수] - slot_cofnod) { methiant_VALUE("unsupported or truncated bytecode"); break; }
                경계[slot_cofnod] = 수 + 1; slot_cofnod += hyd_VALUE;
            }
            // 실행하지 않는 경로에도 잘못된 cangen 목적지를 허용하지 않는다.
            slot_cofnod = dull_START[수];
            while (slot_cofnod < dull_gorffen[수] && !Gwall) {
                int VALUE = Ffeil[slot_cofnod];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int cyrchfan_VALUE = slot_cofnod + (short)(Ffeil[slot_cofnod + 1] << 8 | Ffeil[slot_cofnod + 2]);
                    if (cyrchfan_VALUE < dull_START[수] || cyrchfan_VALUE >= dull_gorffen[수] || 경계[cyrchfan_VALUE] != 수 + 1) methiant_VALUE("invalid branch target");
                }
                slot_cofnod += gorchymyn_hyd(VALUE);
            }
        }
        if (!Gwall) 속성건너();
        if (읽기위치 != Maint) methiant_VALUE("extra class file data");
    }
    static int dyrannu_Storio(int 종류, int hyd_VALUE) {
        if (hyd_VALUE < 0 || hyd_VALUE > 힙.length - 힙끝 - 2) { methiant_VALUE("object heap exhausted or negative array size"); return 0; }
        int cyfeiriad = 힙끝; 힙끝 += hyd_VALUE + 2; 힙[cyfeiriad] = 종류; 힙[cyfeiriad + 1] = hyd_VALUE;
        return cyfeiriad;
    }
    static boolean gwrthrych_VALUE(int cyfeiriad, int 종류) {
        if (cyfeiriad < 1 || cyfeiriad >= 힙끝 - 1 || 힙[cyfeiriad] != 종류) { methiant_VALUE("null or invalid object reference"); return false; }
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
        if (ffrâm_INDEX == 31) { methiant_VALUE("call stack limit (32)"); return; }
        int Nesaf_eitem = ffrâm_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) lleol_TYPE[Nesaf_eitem * 128 + 수] = 0;
        for (int 수 = dull_arg_COUNT[SWYDDOGAETH_VALUE] - 1; 수 >= 0; 수--) {
            lleol_VALUE[Nesaf_eitem * 128 + 수] = 빼기(dull_arg_TYPE[SWYDDOGAETH_VALUE * 16 + 수]); lleol_TYPE[Nesaf_eitem * 128 + 수] = dull_arg_TYPE[SWYDDOGAETH_VALUE * 16 + 수];
        }
        ffrâm_INDEX = Nesaf_eitem; ffrâm_dull[ffrâm_INDEX] = SWYDDOGAETH_VALUE; ffrâm_safle[ffrâm_INDEX] = dull_START[SWYDDOGAETH_VALUE]; ffrâm_pentwr[ffrâm_INDEX] = 0;
    }
    static void return_mesur(int TYPE_VALUE) {
        if (TYPE_VALUE != dull_return[ffrâm_dull[ffrâm_INDEX]]) { methiant_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        ffrâm_INDEX--; if (ffrâm_INDEX >= 0 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
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
                if (VALUE < 1 || VALUE > 127) { methiant_VALUE("file stream paths currently require ASCII"); return; }
                ffrwd_ffeil_enw[slot_cofnod] = VALUE;
            }
            ffrwd_ffeil_enw[hyd_VALUE] = 0;
            int 서술자 = defnyddiwr.파일서술자열기(ffrwd_ffeil_enw, Allbwn ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { methiant_VALUE("FileNotFoundException: file open failed"); return; }
            힙[ffrwd_VALUE + 2] = 서술자; 힙[ffrwd_VALUE + 3] = 1;
            return;
        }
        if (Gorchymyn != 182) { methiant_VALUE("invalid file stream invocation"); return; }
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
            if (mesur < -1) methiant_VALUE("IOException: read failed"); else 넣기(mesur, 1);
        } else if (defnyddiwr.파일한바이트쓰기(서술자, VALUE) != 1) methiant_VALUE("IOException: write failed");
    }
    static void CALL_dull(int INDEX, int Gorchymyn) {
        if (!gwirio_cysonyn(INDEX, 10)) return;
        int perchennog_VALUE = Dosbarth_enw_SMS(상가[INDEX]), Enw = cyfeiriad_enw(cysonyn_SECOND_VALUE[INDEX]), fformat_VALUE = cyfeiriad_TYPE(cysonyn_SECOND_VALUE[INDEX]);
        if (Gwall) return;
        if (같은말(perchennog_VALUE, Dosbarth_enw)) {
            if (Gorchymyn != 184) { methiant_VALUE("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < dull_COUNT; 수++) if (같은말(Enw, dull_enw_SMS[수]) && 같은말(fformat_VALUE, dull_TYPE[수])) {
                if ((dull_mynediad[수] & 8) == 0) methiant_VALUE("method is not static"); else 호출(수);
                return;
            }
            methiant_VALUE("NoSuchMethodError"); return;
        }
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
        methiant_VALUE("unsupported library method");
    }
    static int ARAE_slot(int cyfeiriad, int is_ysgrif_VALUE, int TYPE_VALUE) {
        if (!gwrthrych_VALUE(cyfeiriad, TYPE_VALUE)) return 0;
        if (is_ysgrif_VALUE < 0 || is_ysgrif_VALUE >= 힙[cyfeiriad + 1]) { methiant_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return cyfeiriad + 2 + is_ysgrif_VALUE;
    }
    static void Gweithredu_gorchymyn() {
        int 남음 = 500000;
        while (ffrâm_INDEX >= 0 && !Gwall) {
            if (--남음 == 0) { methiant_VALUE("instruction limit (500000)"); break; }
            int Gweithredu_2 = ffrâm_safle[ffrâm_INDEX], VALUE = 명바();
            if (Gwall) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = VALUE == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= cysonyn_COUNT) methiant_VALUE("invalid ldc constant");
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
            if (VALUE == 46 || VALUE == 50) {
                int is_ysgrif_VALUE = 빼기(1), cyfeiriad = 빼기(2), slot_cofnod = ARAE_slot(cyfeiriad, is_ysgrif_VALUE, VALUE == 46 ? 2 : 3);
                if (!Gwall) 넣기(힙[slot_cofnod], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int eitem_elfen = 빼기(VALUE == 79 ? 1 : 2), is_ysgrif_VALUE = 빼기(1), cyfeiriad = 빼기(2), slot_cofnod = ARAE_slot(cyfeiriad, is_ysgrif_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && eitem_elfen != 0) gwrthrych_VALUE(eitem_elfen, 1);
                if (!Gwall) 힙[slot_cofnod] = eitem_elfen; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), TYPE_VALUE = return_TYPE; 넣기(가, TYPE_VALUE); 넣기(가, TYPE_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = return_TYPE, 나 = 빼기(0), 나형 = return_TYPE; 넣기(가, 가형); 넣기(나, 나형); continue; }
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
            if (VALUE == 178) {
                int 수 = 명짧(); if (!gwirio_cysonyn(수, 9)) continue;
                if (!Word_SMS(Dosbarth_enw_SMS(상가[수]), "java/lang/System") || !Word_SMS(cyfeiriad_enw(cysonyn_SECOND_VALUE[수]), "out")
                    || !Word_SMS(cyfeiriad_TYPE(cysonyn_SECOND_VALUE[수]), "Ljava/io/PrintStream;")) methiant_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_dull(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int Enw = Dosbarth_enw_SMS(명짧());
                if (Word_SMS(Enw, "java/lang/StringBuilder")) 넣기(dyrannu_Storio(4, 1), 2);
                else if (Word_SMS(Enw, "java/io/FileInputStream") || Word_SMS(Enw, "java/io/FileOutputStream")) {
                    int cyfeiriad = dyrannu_Storio(Word_SMS(Enw, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!Gwall) { 힙[cyfeiriad + 2] = -1; 넣기(cyfeiriad, 2); }
                } else methiant_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) methiant_VALUE("only int[] newarray is supported"); }
                else if (!Word_SMS(Dosbarth_enw_SMS(명짧()), "java/lang/String")) methiant_VALUE("only String[] anewarray is supported");
                int hyd_VALUE = 빼기(1); 넣기(dyrannu_Storio(VALUE == 188 ? 2 : 3, hyd_VALUE), 2); continue;
            }
            if (VALUE == 190) {
                int cyfeiriad = 빼기(2);
                if (cyfeiriad < 1 || cyfeiriad >= 힙끝 - 1 || (힙[cyfeiriad] != 2 && 힙[cyfeiriad] != 3)) methiant_VALUE("null or invalid array");
                else 넣기(힙[cyfeiriad + 1], 1); continue;
            }
            if (VALUE == 192) {
                int Enw = Dosbarth_enw_SMS(명짧()), cyfeiriad = 빼기(2);
                if (!Word_SMS(Enw, "java/lang/String")) methiant_VALUE("unsupported checkcast");
                else if (cyfeiriad != 0) gwrthrych_VALUE(cyfeiriad, 1);
                넣기(cyfeiriad, 2); continue;
            }
            methiant_VALUE("unsupported bytecode");
        }
    }
    public static int Gweithredu_2() {
        if (defnyddiwr.인수개수() == 1 && 자바도구.같음(defnyddiwr.인수(0), "-version")) {
            defnyddiwr.Ysgrifennu("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (defnyddiwr.인수개수() < 1) { defnyddiwr.Ysgrifennu("Usage: java CLASS [ARGS]\n"); return 2; }
        int hyd_VALUE = 자바도구.Enw(ffeil_enw_SMS, defnyddiwr.인수(0));
        if (hyd_VALUE < 1 || hyd_VALUE > 57) { defnyddiwr.Ysgrifennu("java: invalid class name\n"); return 2; }
        ffeil_enw_SMS[hyd_VALUE] = '.'; ffeil_enw_SMS[hyd_VALUE + 1] = 'c'; ffeil_enw_SMS[hyd_VALUE + 2] = 'l'; ffeil_enw_SMS[hyd_VALUE + 3] = 'a'; ffeil_enw_SMS[hyd_VALUE + 4] = 's'; ffeil_enw_SMS[hyd_VALUE + 5] = 's';
        Maint = defnyddiwr.파일읽기(ffeil_enw_SMS, Ffeil);
        if (Maint < 0) { defnyddiwr.Ysgrifennu("java: cannot read class: "); 자바도구.수쓰기(Maint); defnyddiwr.ysgrifennu_nod_VALUE(10); return 1; }
        클래스읽기(); if (Gwall) return 1;
        int nod_enw = cysonyn_SMS(Dosbarth_enw);
        if (!Gwall && 힙[nod_enw + 1] != hyd_VALUE) methiant_VALUE("class name does not match file");
        for (int 수 = 0; 수 < hyd_VALUE && !Gwall; 수++) if (힙[nod_enw + 2 + 수] != ffeil_enw_SMS[수]) methiant_VALUE("class name does not match file");
        int cofnod_p_VALUE = -1;
        for (int 수 = 0; 수 < dull_COUNT; 수++) if (Word_SMS(dull_enw_SMS[수], "main") && Word_SMS(dull_TYPE[수], "([Ljava/lang/String;)V") && (dull_mynediad[수] & 9) == 9) cofnod_p_VALUE = 수;
        if (cofnod_p_VALUE < 0) methiant_VALUE("public static void main(String[] args) required");
        if (Gwall) return 1;
        int 인수 = dyrannu_Storio(3, defnyddiwr.인수개수() - 1);
        for (int 수 = 1; 수 < defnyddiwr.인수개수() && !Gwall; 수++) 힙[인수 + 1 + 수] = lletya_nod(defnyddiwr.인수(수));
        ffrâm_INDEX = 0; ffrâm_dull[0] = cofnod_p_VALUE; ffrâm_safle[0] = dull_START[cofnod_p_VALUE]; lleol_VALUE[0] = 인수; lleol_TYPE[0] = 2;
        Gweithredu_gorchymyn(); return Gwall ? 1 : 0;
    }
}
