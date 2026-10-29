// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. faidhle/스택/fiosrachadh/meur 경계를 gnìomhaich_àithne 중 검사한다. */
public final class 자바가상기계 {
    static int[] faidhle = new int[16384], faidhle_ainm_SMS = new int[64];
    static int[] cunbhalachan_taga = new int[512], 상가 = new int[512], cunbhalachan_SECOND_VALUE = new int[512], sreang_fiosrachadh = new int[512];
    static int[] dòigh_ainm_SMS = new int[32], dòigh_TYPE = new int[32], dòigh_inntrigeadh = new int[32];
    static int[] dòigh_Start = new int[32], dòigh_crìochnaich = new int[32], dòigh_stac = new int[32], 함수지역 = new int[32];
    static int[] dòigh_argamaid_COUNT = new int[32], dòigh_argamaid_TYPE = new int[512], dòigh_return = new int[32];
    static int[] 경계 = new int[16384];
    static int[] ionadail_VALUE = new int[4096], ionadail_TYPE = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] frèam_dòigh = new int[32], frèam_suidhich = new int[32], frèam_stac = new int[32];
    static int[] 힙 = new int[8192];
    static int atharraich_am_meud, 읽기위치, cunbhalachan_COUNT, dòigh_COUNT, clas_ainm, frèam_INDEX = -1, 힙끝 = 1, return_TYPE;
    static boolean Mearachd;

    static void fàilligeadh_VALUE(String Word_SMS) {
        if (!Mearachd) { cleachdaiche.sgrìobh("JVM error: "); cleachdaiche.sgrìobh(Word_SMS); cleachdaiche.sgrìobh_caractar_VALUE(10); }
        Mearachd = true;
    }
    static boolean cliop(int ruith, int faid_VALUE) { return ruith >= 0 && faid_VALUE >= 0 && ruith <= atharraich_am_meud - faid_VALUE; }
    static int baidht_VALUE() {
        if (!cliop(읽기위치, 1)) { fàilligeadh_VALUE("truncated class file"); return 0; }
        return faidhle[읽기위치++];
    }
    static int 짧은수() { return baidht_VALUE() << 8 | baidht_VALUE(); }
    static int àireamh_shlàn() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int faid_VALUE) { if (!cliop(읽기위치, faid_VALUE)) fàilligeadh_VALUE("invalid attribute size"); else 읽기위치 += faid_VALUE; }
    static boolean seic_cunbhalachan(int 수, int 종류) {
        if (수 <= 0 || 수 >= cunbhalachan_COUNT || cunbhalachan_taga[수] != 종류) { fàilligeadh_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int ruith, int faid_VALUE, String Word_SMS) {
        if (!cliop(ruith, faid_VALUE) || faid_VALUE != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < faid_VALUE; 수++) if (faidhle[ruith + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static boolean Word_SMS(int cunbhalachan_VALUE, String Word_SMS) { return seic_cunbhalachan(cunbhalachan_VALUE, 1) && 구간(상가[cunbhalachan_VALUE], cunbhalachan_SECOND_VALUE[cunbhalachan_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!seic_cunbhalachan(가, 1) || !seic_cunbhalachan(나, 1) || cunbhalachan_SECOND_VALUE[가] != cunbhalachan_SECOND_VALUE[나]) return false;
        for (int 수 = 0; 수 < cunbhalachan_SECOND_VALUE[가]; 수++) if (faidhle[상가[가] + 수] != faidhle[상가[나] + 수]) return false;
        return true;
    }
    static int clas_ainm_SMS(int 수) { return seic_cunbhalachan(수, 7) && seic_cunbhalachan(상가[수], 1) ? 상가[수] : 0; }
    static int fiosrachadh_ainm(int 수) { return seic_cunbhalachan(수, 12) && seic_cunbhalachan(상가[수], 1) ? 상가[수] : 0; }
    static int fiosrachadh_TYPE(int 수) { return seic_cunbhalachan(수, 12) && seic_cunbhalachan(cunbhalachan_SECOND_VALUE[수], 1) ? cunbhalachan_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean falamh_TYPE) {
        if (읽기위치 >= 끝) { fàilligeadh_VALUE("invalid descriptor"); return 0; }
        int VALUE = baidht_VALUE();
        if (VALUE == 'V' && falamh_TYPE) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int ruith = 읽기위치;
            while (읽기위치 < 끝 && faidhle[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == ruith) fàilligeadh_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        fàilligeadh_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_VALUE) {
        int 이전 = 읽기위치, 수 = dòigh_TYPE[FUNCTION_VALUE];
        if (!seic_cunbhalachan(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + cunbhalachan_SECOND_VALUE[수];
        if (baidht_VALUE() != '(') fàilligeadh_VALUE("invalid method descriptor");
        int nì_COUNT = 0;
        while (!Mearachd && 읽기위치 < 끝 && faidhle[읽기위치] != ')') {
            if (nì_COUNT == 16) { fàilligeadh_VALUE("too many method arguments"); break; }
            dòigh_argamaid_TYPE[FUNCTION_VALUE * 16 + nì_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || baidht_VALUE() != ')') fàilligeadh_VALUE("invalid method descriptor");
        dòigh_return[FUNCTION_VALUE] = 서술형(끝, true); dòigh_argamaid_COUNT[FUNCTION_VALUE] = nì_COUNT;
        if (읽기위치 != 끝) fàilligeadh_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int nì_COUNT = 짧은수();
        for (int 수 = 0; 수 < nì_COUNT && !Mearachd; 수++) { seic_cunbhalachan(짧은수(), 1); 건너(àireamh_shlàn()); }
    }
    static int àithne_faid(int VALUE) {
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
        if (àireamh_shlàn() != 0xcafebabe) fàilligeadh_VALUE("not a class file");
        int 부판 = 짧은수(), tionndadh_VALUE = 짧은수();
        if (tionndadh_VALUE < 45 || tionndadh_VALUE > 52 || 부판 != 0) fàilligeadh_VALUE("supported class versions: 45..52, minor 0");
        cunbhalachan_COUNT = 짧은수();
        if (cunbhalachan_COUNT < 1 || cunbhalachan_COUNT > 512) { fàilligeadh_VALUE("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < cunbhalachan_COUNT && !Mearachd; 수++) {
            int 종류 = baidht_VALUE(); cunbhalachan_taga[수] = 종류;
            if (종류 == 1) { cunbhalachan_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(cunbhalachan_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = àireamh_shlàn();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); cunbhalachan_SECOND_VALUE[수] = 짧은수(); }
            else fàilligeadh_VALUE("unsupported constant type");
        }
        int cead_VALUE = 짧은수();
        if ((cead_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) fàilligeadh_VALUE("unsupported class flags");
        clas_ainm = clas_ainm_SMS(짧은수());
        if (!Word_SMS(clas_ainm_SMS(짧은수()), "java/lang/Object")) fàilligeadh_VALUE("inheritance unsupported");
        if (짧은수() != 0) fàilligeadh_VALUE("interfaces unsupported");
        if (짧은수() != 0) fàilligeadh_VALUE("fields unsupported");
        dòigh_COUNT = 짧은수();
        if (dòigh_COUNT < 1 || dòigh_COUNT > 32) { fàilligeadh_VALUE("method count limit (32)"); return; }
        for (int 수 = 0; 수 < dòigh_COUNT && !Mearachd; 수++) {
            dòigh_inntrigeadh[수] = 짧은수(); dòigh_ainm_SMS[수] = 짧은수(); dòigh_TYPE[수] = 짧은수();
            seic_cunbhalachan(dòigh_ainm_SMS[수], 1); 서술읽기(수);
            if ((dòigh_inntrigeadh[수] & (0x100 | 0x400 | 0x20)) != 0) fàilligeadh_VALUE("native, abstract and synchronized methods unsupported");
            if ((dòigh_inntrigeadh[수] & 8) == 0 && !Word_SMS(dòigh_ainm_SMS[수], "<init>")) fàilligeadh_VALUE("instance methods unsupported");
            if (Word_SMS(dòigh_ainm_SMS[수], "<clinit>")) fàilligeadh_VALUE("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(dòigh_ainm_SMS[앞], dòigh_ainm_SMS[수]) && 같은말(dòigh_TYPE[앞], dòigh_TYPE[수])) fàilligeadh_VALUE("duplicate method");
            int nì_COUNT = 짧은수();
            for (int buadh_VALUE = 0; buadh_VALUE < nì_COUNT && !Mearachd; buadh_VALUE++) {
                int Ainm = 짧은수(), faid_VALUE = àireamh_shlàn(), ruith = 읽기위치;
                if (!cliop(ruith, faid_VALUE)) { fàilligeadh_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Ainm, "Code")) {
                    if (dòigh_Start[수] != 0) fàilligeadh_VALUE("duplicate Code attribute");
                    dòigh_stac[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_faid = àireamh_shlàn();
                    if (dòigh_stac[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < dòigh_argamaid_COUNT[수]
                        || CODE_faid < 1 || CODE_faid > 8192) fàilligeadh_VALUE("method memory limits exceeded");
                    dòigh_Start[수] = 읽기위치; 건너(CODE_faid); dòigh_crìochnaich[수] = 읽기위치;
                    if (짧은수() != 0) fàilligeadh_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != ruith + faid_VALUE) fàilligeadh_VALUE("Code attribute size mismatch");
                } else 건너(faid_VALUE);
            }
            if (dòigh_Start[수] == 0) fàilligeadh_VALUE("missing Code attribute");
            int slot_cur_a_steach = dòigh_Start[수];
            while (slot_cur_a_steach < dòigh_crìochnaich[수] && !Mearachd) {
                int faid_VALUE = àithne_faid(faidhle[slot_cur_a_steach]);
                if (faid_VALUE == 0 || faid_VALUE > dòigh_crìochnaich[수] - slot_cur_a_steach) { fàilligeadh_VALUE("unsupported or truncated bytecode"); break; }
                경계[slot_cur_a_steach] = 수 + 1; slot_cur_a_steach += faid_VALUE;
            }
            // 실행하지 않는 경로에도 잘못된 meur 목적지를 허용하지 않는다.
            slot_cur_a_steach = dòigh_Start[수];
            while (slot_cur_a_steach < dòigh_crìochnaich[수] && !Mearachd) {
                int VALUE = faidhle[slot_cur_a_steach];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int ceann_uidhe_VALUE = slot_cur_a_steach + (short)(faidhle[slot_cur_a_steach + 1] << 8 | faidhle[slot_cur_a_steach + 2]);
                    if (ceann_uidhe_VALUE < dòigh_Start[수] || ceann_uidhe_VALUE >= dòigh_crìochnaich[수] || 경계[ceann_uidhe_VALUE] != 수 + 1) fàilligeadh_VALUE("invalid branch target");
                }
                slot_cur_a_steach += àithne_faid(VALUE);
            }
        }
        if (!Mearachd) 속성건너();
        if (읽기위치 != atharraich_am_meud) fàilligeadh_VALUE("extra class file data");
    }
    static int sònraich_stòras(int 종류, int faid_VALUE) {
        if (faid_VALUE < 0 || faid_VALUE > 힙.length - 힙끝 - 2) { fàilligeadh_VALUE("object heap exhausted or negative array size"); return 0; }
        int fiosrachadh = 힙끝; 힙끝 += faid_VALUE + 2; 힙[fiosrachadh] = 종류; 힙[fiosrachadh + 1] = faid_VALUE;
        return fiosrachadh;
    }
    static boolean nì_VALUE(int fiosrachadh, int 종류) {
        if (fiosrachadh < 1 || fiosrachadh >= 힙끝 - 1 || 힙[fiosrachadh] != 종류) { fàilligeadh_VALUE("null or invalid object reference"); return false; }
        return true;
    }
    static int cunbhalachan_SMS(int INDEX) {
        if (!seic_cunbhalachan(INDEX, 1)) return 0;
        if (sreang_fiosrachadh[INDEX] != 0) return sreang_fiosrachadh[INDEX];
        int fiosrachadh = sònraich_stòras(1, cunbhalachan_SECOND_VALUE[INDEX]); if (Mearachd) return 0;
        int 끝 = 상가[INDEX] + cunbhalachan_SECOND_VALUE[INDEX], 수 = 상가[INDEX], faid_VALUE = 0;
        while (수 < 끝 && !Mearachd) {
            int VALUE = faidhle[수++];
            if (VALUE == 0) fàilligeadh_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int air_adhart_nì = faidhle[수++];
                if ((air_adhart_nì & 192) != 128) fàilligeadh_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | air_adhart_nì & 63;
                if (VALUE != 0 && VALUE < 128) fàilligeadh_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = faidhle[수++], 나 = faidhle[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) fàilligeadh_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (VALUE < 2048) fàilligeadh_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) fàilligeadh_VALUE("invalid modified UTF-8");
            힙[fiosrachadh + 2 + faid_VALUE++] = VALUE;
        }
        힙[fiosrachadh + 1] = faid_VALUE; sreang_fiosrachadh[INDEX] = fiosrachadh; return fiosrachadh;
    }
    static int òstair_caractar(String VALUE) {
        int fiosrachadh = sònraich_stòras(1, VALUE.length()); if (Mearachd) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) 힙[fiosrachadh + 2 + 수] = VALUE.charAt(수);
        return fiosrachadh;
    }
    static void sgrìobh_SMS(int fiosrachadh) {
        if (fiosrachadh == 0) { cleachdaiche.sgrìobh("null"); return; }
        if (!nì_VALUE(fiosrachadh, 1)) return;
        for (int 수 = 0; 수 < 힙[fiosrachadh + 1]; 수++) cleachdaiche.sgrìobh_caractar_VALUE(힙[fiosrachadh + 2 + 수]);
    }
    static int figear_caractar(int VALUE) {
        int fiosrachadh = sònraich_stòras(1, 11); if (Mearachd) return 0;
        int faid_VALUE = 0;
        if (VALUE < 0) 힙[fiosrachadh + 2 + faid_VALUE++] = '-'; else VALUE = -VALUE;
        int suidhich_INDEX = 1000000000; boolean ruith = false;
        while (suidhich_INDEX != 0) {
            int 수 = -(VALUE / suidhich_INDEX);
            if (수 != 0 || ruith || suidhich_INDEX == 1) { 힙[fiosrachadh + 2 + faid_VALUE++] = '0' + 수; ruith = true; }
            VALUE %= suidhich_INDEX; suidhich_INDEX /= 10;
        }
        힙[fiosrachadh + 1] = faid_VALUE; return fiosrachadh;
    }
    static int 정수해독(int fiosrachadh) {
        if (!nì_VALUE(fiosrachadh, 1)) return 0;
        int faid_VALUE = 힙[fiosrachadh + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (faid_VALUE > 0 && (힙[fiosrachadh + 2] == '-' || 힙[fiosrachadh + 2] == '+')) { 음수 = 힙[fiosrachadh + 2] == '-'; 수++; }
        if (수 == faid_VALUE) fàilligeadh_VALUE("NumberFormatException");
        for (; 수 < faid_VALUE && !Mearachd; 수++) {
            int figear_VALUE = 힙[fiosrachadh + 2 + 수] - '0';
            if (figear_VALUE < 0 || figear_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && figear_VALUE > (음수 ? 8 : 7)) fàilligeadh_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - figear_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (Mearachd) return;
        if (frèam_INDEX < 0 || frèam_stac[frèam_INDEX] >= dòigh_stac[frèam_dòigh[frèam_INDEX]]) { fàilligeadh_VALUE("operand stack overflow"); return; }
        int slot_cur_a_steach = frèam_INDEX * 128 + frèam_stac[frèam_INDEX]++; 스택값[slot_cur_a_steach] = VALUE; 스택형[slot_cur_a_steach] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (Mearachd) return 0;
        if (frèam_INDEX < 0 || frèam_stac[frèam_INDEX] < 1) { fàilligeadh_VALUE("operand stack underflow"); return 0; }
        int slot_cur_a_steach = frèam_INDEX * 128 + --frèam_stac[frèam_INDEX]; return_TYPE = 스택형[slot_cur_a_steach];
        if (TYPE_VALUE != 0 && return_TYPE != TYPE_VALUE) fàilligeadh_VALUE("operand type mismatch");
        return 스택값[slot_cur_a_steach];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[frèam_dòigh[frèam_INDEX]] || INDEX < 0 || ionadail_TYPE[frèam_INDEX * 128 + INDEX] != TYPE_VALUE) { fàilligeadh_VALUE("invalid or uninitialized local"); return; }
        넣기(ionadail_VALUE[frèam_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void sgrìobh_ionadail(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[frèam_dòigh[frèam_INDEX]] || INDEX < 0) { fàilligeadh_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); ionadail_VALUE[frèam_INDEX * 128 + INDEX] = VALUE; ionadail_TYPE[frèam_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int suidhich = frèam_suidhich[frèam_INDEX];
        if (suidhich < dòigh_Start[frèam_dòigh[frèam_INDEX]] || suidhich >= dòigh_crìochnaich[frèam_dòigh[frèam_INDEX]]) { fàilligeadh_VALUE("instruction pointer out of range"); return 0; }
        frèam_suidhich[frèam_INDEX]++; return faidhle[suidhich];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void gluais_VALUE(int suidhich) {
        int FUNCTION_VALUE = frèam_dòigh[frèam_INDEX];
        if (suidhich < dòigh_Start[FUNCTION_VALUE] || suidhich >= dòigh_crìochnaich[FUNCTION_VALUE] || 경계[suidhich] != FUNCTION_VALUE + 1) fàilligeadh_VALUE("invalid branch target");
        else frèam_suidhich[frèam_INDEX] = suidhich;
    }
    static void 호출(int FUNCTION_VALUE) {
        if (frèam_INDEX == 31) { fàilligeadh_VALUE("call stack limit (32)"); return; }
        int air_adhart_nì = frèam_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) ionadail_TYPE[air_adhart_nì * 128 + 수] = 0;
        for (int 수 = dòigh_argamaid_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            ionadail_VALUE[air_adhart_nì * 128 + 수] = 빼기(dòigh_argamaid_TYPE[FUNCTION_VALUE * 16 + 수]); ionadail_TYPE[air_adhart_nì * 128 + 수] = dòigh_argamaid_TYPE[FUNCTION_VALUE * 16 + 수];
        }
        frèam_INDEX = air_adhart_nì; frèam_dòigh[frèam_INDEX] = FUNCTION_VALUE; frèam_suidhich[frèam_INDEX] = dòigh_Start[FUNCTION_VALUE]; frèam_stac[frèam_INDEX] = 0;
    }
    static void return_tomhas(int TYPE_VALUE) {
        if (TYPE_VALUE != dòigh_return[frèam_dòigh[frèam_INDEX]]) { fàilligeadh_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        frèam_INDEX--; if (frèam_INDEX >= 0 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] sruth_faidhle_ainm = new int[64];
    static void faidhle_sruth_CALL(int sealbhadair_VALUE, int Ainm, int fòrmat_VALUE, int àithne) {
        boolean 출력 = Word_SMS(sealbhadair_VALUE, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (àithne == 183 && Word_SMS(Ainm, "<init>")) {
            boolean 이어 = false;
            if (출력 && Word_SMS(fòrmat_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(fòrmat_VALUE, "(Ljava/lang/String;)V")) { fàilligeadh_VALUE("unsupported file stream constructor"); return; }
            int faidhle_cur_a_steach_ainm = 빼기(2), sruth_VALUE = 빼기(2);
            if (!nì_VALUE(faidhle_cur_a_steach_ainm, 1) || !nì_VALUE(sruth_VALUE, 종류) || Mearachd) return;
            if (힙[sruth_VALUE + 3] != 0) { fàilligeadh_VALUE("file stream already initialized"); return; }
            int faid_VALUE = 힙[faidhle_cur_a_steach_ainm + 1];
            if (faid_VALUE < 1 || faid_VALUE > 63) { fàilligeadh_VALUE("invalid file name length"); return; }
            for (int slot_cur_a_steach = 0; slot_cur_a_steach < faid_VALUE; slot_cur_a_steach++) {
                int VALUE = 힙[faidhle_cur_a_steach_ainm + 2 + slot_cur_a_steach];
                if (VALUE < 1 || VALUE > 127) { fàilligeadh_VALUE("file stream paths currently require ASCII"); return; }
                sruth_faidhle_ainm[slot_cur_a_steach] = VALUE;
            }
            sruth_faidhle_ainm[faid_VALUE] = 0;
            int 서술자 = cleachdaiche.파일서술자열기(sruth_faidhle_ainm, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { fàilligeadh_VALUE("FileNotFoundException: file open failed"); return; }
            힙[sruth_VALUE + 2] = 서술자; 힙[sruth_VALUE + 3] = 1;
            return;
        }
        if (àithne != 182) { fàilligeadh_VALUE("invalid file stream invocation"); return; }
        int Gnìomh = -1, VALUE = 0;
        if (Word_SMS(Ainm, "close") && Word_SMS(fòrmat_VALUE, "()V")) Gnìomh = 0;
        if (!출력 && Word_SMS(Ainm, "read") && Word_SMS(fòrmat_VALUE, "()I")) Gnìomh = 1;
        if (출력 && Word_SMS(Ainm, "write") && Word_SMS(fòrmat_VALUE, "(I)V")) { Gnìomh = 2; VALUE = 빼기(1); }
        if (Gnìomh < 0) { fàilligeadh_VALUE("unsupported file stream method"); return; }
        int sruth_VALUE = 빼기(2);
        if (!nì_VALUE(sruth_VALUE, 종류) || Mearachd) return;
        if (힙[sruth_VALUE + 3] == 0) { fàilligeadh_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[sruth_VALUE + 2];
        if (Gnìomh == 0) {
            if (서술자 >= 0 && cleachdaiche.파일서술자닫기(서술자) < 0) fàilligeadh_VALUE("IOException: close failed");
            힙[sruth_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { fàilligeadh_VALUE("IOException: stream closed"); return; }
        if (Gnìomh == 1) {
            int tomhas = cleachdaiche.파일한바이트읽기(서술자);
            if (tomhas < -1) fàilligeadh_VALUE("IOException: read failed"); else 넣기(tomhas, 1);
        } else if (cleachdaiche.파일한바이트쓰기(서술자, VALUE) != 1) fàilligeadh_VALUE("IOException: write failed");
    }
    static void CALL_dòigh(int INDEX, int àithne) {
        if (!seic_cunbhalachan(INDEX, 10)) return;
        int sealbhadair_VALUE = clas_ainm_SMS(상가[INDEX]), Ainm = fiosrachadh_ainm(cunbhalachan_SECOND_VALUE[INDEX]), fòrmat_VALUE = fiosrachadh_TYPE(cunbhalachan_SECOND_VALUE[INDEX]);
        if (Mearachd) return;
        if (같은말(sealbhadair_VALUE, clas_ainm)) {
            if (àithne != 184) { fàilligeadh_VALUE("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < dòigh_COUNT; 수++) if (같은말(Ainm, dòigh_ainm_SMS[수]) && 같은말(fòrmat_VALUE, dòigh_TYPE[수])) {
                if ((dòigh_inntrigeadh[수] & 8) == 0) fàilligeadh_VALUE("method is not static"); else 호출(수);
                return;
            }
            fàilligeadh_VALUE("NoSuchMethodError"); return;
        }
        if (Word_SMS(sealbhadair_VALUE, "java/io/FileInputStream") || Word_SMS(sealbhadair_VALUE, "java/io/FileOutputStream")) {
            faidhle_sruth_CALL(sealbhadair_VALUE, Ainm, fòrmat_VALUE, àithne); return;
        }
        if (àithne == 184 && Word_SMS(sealbhadair_VALUE, "java/lang/Integer") && Word_SMS(Ainm, "parseInt") && Word_SMS(fòrmat_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (àithne == 182 && Word_SMS(sealbhadair_VALUE, "java/io/PrintStream") && (Word_SMS(Ainm, "println") || Word_SMS(Ainm, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(fòrmat_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(fòrmat_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(fòrmat_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(fòrmat_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(fòrmat_VALUE, "()V") || !Word_SMS(Ainm, "println")) fàilligeadh_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) fàilligeadh_VALUE("invalid PrintStream receiver");
            if (Mearachd) return;
            if (TYPE_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (TYPE_VALUE == 2) cleachdaiche.sgrìobh(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) cleachdaiche.sgrìobh_caractar_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) sgrìobh_SMS(VALUE);
            if (Word_SMS(Ainm, "println")) cleachdaiche.sgrìobh_caractar_VALUE(10);
            return;
        }
        if (àithne == 182 && Word_SMS(sealbhadair_VALUE, "java/lang/String")) {
            if (Word_SMS(Ainm, "length") && Word_SMS(fòrmat_VALUE, "()I")) {
                int fiosrachadh = 빼기(2); if (nì_VALUE(fiosrachadh, 1)) 넣기(힙[fiosrachadh + 1], 1); return;
            }
            if (Word_SMS(Ainm, "charAt") && Word_SMS(fòrmat_VALUE, "(I)C")) {
                int fo_sgrìobhte_VALUE = 빼기(1), fiosrachadh = 빼기(2);
                if (nì_VALUE(fiosrachadh, 1)) {
                    if (fo_sgrìobhte_VALUE < 0 || fo_sgrìobhte_VALUE >= 힙[fiosrachadh + 1]) fàilligeadh_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[fiosrachadh + 2 + fo_sgrìobhte_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(sealbhadair_VALUE, "java/lang/StringBuilder")) {
            if (àithne == 183 && Word_SMS(Ainm, "<init>") && Word_SMS(fòrmat_VALUE, "()V")) { nì_VALUE(빼기(2), 4); return; }
            if (àithne == 182 && Word_SMS(Ainm, "toString") && Word_SMS(fòrmat_VALUE, "()Ljava/lang/String;")) {
                int fiosrachadh = 빼기(2); if (nì_VALUE(fiosrachadh, 4)) 넣기(힙[fiosrachadh + 2] == 0 ? òstair_caractar("") : 힙[fiosrachadh + 2], 2); return;
            }
            if (àithne == 182 && Word_SMS(Ainm, "append")) {
                int SMS = 0;
                if (Word_SMS(fòrmat_VALUE, "(I)Ljava/lang/StringBuilder;")) SMS = figear_caractar(빼기(1));
                else if (Word_SMS(fòrmat_VALUE, "(Z)Ljava/lang/StringBuilder;")) SMS = òstair_caractar(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(fòrmat_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); SMS = sònraich_stòras(1, 1); if (!Mearachd) 힙[SMS + 2] = VALUE & 65535;
                }
                else if (Word_SMS(fòrmat_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { SMS = 빼기(2); if (SMS == 0) SMS = òstair_caractar("null"); }
                else { fàilligeadh_VALUE("unsupported StringBuilder append"); return; }
                int fiosrachadh = 빼기(2); if (!nì_VALUE(fiosrachadh, 4) || !nì_VALUE(SMS, 1)) return;
                int 앞 = 힙[fiosrachadh + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], Air_ais_VALUE_faid = 힙[SMS + 1];
                int 새글 = sònraich_stòras(1, 앞길이 + Air_ais_VALUE_faid); if (Mearachd) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < Air_ais_VALUE_faid; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[SMS + 2 + 수];
                힙[fiosrachadh + 2] = 새글; 넣기(fiosrachadh, 2); return;
            }
        }
        fàilligeadh_VALUE("unsupported library method");
    }
    static int ARRAY_slot(int fiosrachadh, int fo_sgrìobhte_VALUE, int TYPE_VALUE) {
        if (!nì_VALUE(fiosrachadh, TYPE_VALUE)) return 0;
        if (fo_sgrìobhte_VALUE < 0 || fo_sgrìobhte_VALUE >= 힙[fiosrachadh + 1]) { fàilligeadh_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return fiosrachadh + 2 + fo_sgrìobhte_VALUE;
    }
    static void gnìomhaich_àithne() {
        int 남음 = 500000;
        while (frèam_INDEX >= 0 && !Mearachd) {
            if (--남음 == 0) { fàilligeadh_VALUE("instruction limit (500000)"); break; }
            int ruith = frèam_suidhich[frèam_INDEX], VALUE = 명바();
            if (Mearachd) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = VALUE == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= cunbhalachan_COUNT) fàilligeadh_VALUE("invalid ldc constant");
                else if (cunbhalachan_taga[수] == 3) 넣기(상가[수], 1);
                else if (cunbhalachan_taga[수] == 8) 넣기(cunbhalachan_SMS(상가[수]), 2);
                else fàilligeadh_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { sgrìobh_ionadail(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { sgrìobh_ionadail(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { sgrìobh_ionadail(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE == 50) {
                int fo_sgrìobhte_VALUE = 빼기(1), fiosrachadh = 빼기(2), slot_cur_a_steach = ARRAY_slot(fiosrachadh, fo_sgrìobhte_VALUE, VALUE == 46 ? 2 : 3);
                if (!Mearachd) 넣기(힙[slot_cur_a_steach], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int nì_eileamaid = 빼기(VALUE == 79 ? 1 : 2), fo_sgrìobhte_VALUE = 빼기(1), fiosrachadh = 빼기(2), slot_cur_a_steach = ARRAY_slot(fiosrachadh, fo_sgrìobhte_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && nì_eileamaid != 0) nì_VALUE(nì_eileamaid, 1);
                if (!Mearachd) 힙[slot_cur_a_steach] = nì_eileamaid; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), TYPE_VALUE = return_TYPE; 넣기(가, TYPE_VALUE); 넣기(가, TYPE_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = return_TYPE, 나 = 빼기(0), 나형 = return_TYPE; 넣기(가, 가형); 넣기(나, 나형); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), tomhas = 0;
                if ((VALUE == 108 || VALUE == 112) && 나 == 0) { fàilligeadh_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) tomhas = 가 + 나;
                if (VALUE == 100) tomhas = 가 - 나;
                if (VALUE == 104) tomhas = 가 * 나;
                if (VALUE == 108) tomhas = 가 / 나;
                if (VALUE == 112) tomhas = 가 % 나;
                if (VALUE == 120) tomhas = 가 << 나;
                if (VALUE == 122) tomhas = 가 >> 나;
                if (VALUE == 124) tomhas = 가 >>> 나;
                if (VALUE == 126) tomhas = 가 & 나;
                if (VALUE == 128) tomhas = 가 | 나;
                if (VALUE == 130) tomhas = 가 ^ 나;
                넣기(tomhas, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int ionadail_sgòp = 명바(), 증분 = (byte)명바(); 지역읽기(ionadail_sgòp, 1); 넣기(빼기(1) + 증분, 1); sgrìobh_ionadail(ionadail_sgòp, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int ceann_uidhe_VALUE = ruith + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int 나 = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == 나 : VALUE == 160 || VALUE == 166 ? 가 != 나 : VALUE == 161 ? 가 < 나 : VALUE == 162 ? 가 >= 나 : VALUE == 163 ? 가 > 나 : 가 <= 나;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) gluais_VALUE(ceann_uidhe_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { return_tomhas(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE == 178) {
                int 수 = 명짧(); if (!seic_cunbhalachan(수, 9)) continue;
                if (!Word_SMS(clas_ainm_SMS(상가[수]), "java/lang/System") || !Word_SMS(fiosrachadh_ainm(cunbhalachan_SECOND_VALUE[수]), "out")
                    || !Word_SMS(fiosrachadh_TYPE(cunbhalachan_SECOND_VALUE[수]), "Ljava/io/PrintStream;")) fàilligeadh_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_dòigh(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int Ainm = clas_ainm_SMS(명짧());
                if (Word_SMS(Ainm, "java/lang/StringBuilder")) 넣기(sònraich_stòras(4, 1), 2);
                else if (Word_SMS(Ainm, "java/io/FileInputStream") || Word_SMS(Ainm, "java/io/FileOutputStream")) {
                    int fiosrachadh = sònraich_stòras(Word_SMS(Ainm, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!Mearachd) { 힙[fiosrachadh + 2] = -1; 넣기(fiosrachadh, 2); }
                } else fàilligeadh_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) fàilligeadh_VALUE("only int[] newarray is supported"); }
                else if (!Word_SMS(clas_ainm_SMS(명짧()), "java/lang/String")) fàilligeadh_VALUE("only String[] anewarray is supported");
                int faid_VALUE = 빼기(1); 넣기(sònraich_stòras(VALUE == 188 ? 2 : 3, faid_VALUE), 2); continue;
            }
            if (VALUE == 190) {
                int fiosrachadh = 빼기(2);
                if (fiosrachadh < 1 || fiosrachadh >= 힙끝 - 1 || (힙[fiosrachadh] != 2 && 힙[fiosrachadh] != 3)) fàilligeadh_VALUE("null or invalid array");
                else 넣기(힙[fiosrachadh + 1], 1); continue;
            }
            if (VALUE == 192) {
                int Ainm = clas_ainm_SMS(명짧()), fiosrachadh = 빼기(2);
                if (!Word_SMS(Ainm, "java/lang/String")) fàilligeadh_VALUE("unsupported checkcast");
                else if (fiosrachadh != 0) nì_VALUE(fiosrachadh, 1);
                넣기(fiosrachadh, 2); continue;
            }
            fàilligeadh_VALUE("unsupported bytecode");
        }
    }
    public static int ruith() {
        if (cleachdaiche.인수개수() == 1 && 자바도구.같음(cleachdaiche.인수(0), "-version")) {
            cleachdaiche.sgrìobh("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (cleachdaiche.인수개수() < 1) { cleachdaiche.sgrìobh("Usage: java CLASS [ARGS]\n"); return 2; }
        int faid_VALUE = 자바도구.Ainm(faidhle_ainm_SMS, cleachdaiche.인수(0));
        if (faid_VALUE < 1 || faid_VALUE > 57) { cleachdaiche.sgrìobh("java: invalid class name\n"); return 2; }
        faidhle_ainm_SMS[faid_VALUE] = '.'; faidhle_ainm_SMS[faid_VALUE + 1] = 'c'; faidhle_ainm_SMS[faid_VALUE + 2] = 'l'; faidhle_ainm_SMS[faid_VALUE + 3] = 'a'; faidhle_ainm_SMS[faid_VALUE + 4] = 's'; faidhle_ainm_SMS[faid_VALUE + 5] = 's';
        atharraich_am_meud = cleachdaiche.파일읽기(faidhle_ainm_SMS, faidhle);
        if (atharraich_am_meud < 0) { cleachdaiche.sgrìobh("java: cannot read class: "); 자바도구.수쓰기(atharraich_am_meud); cleachdaiche.sgrìobh_caractar_VALUE(10); return 1; }
        클래스읽기(); if (Mearachd) return 1;
        int caractar_ainm = cunbhalachan_SMS(clas_ainm);
        if (!Mearachd && 힙[caractar_ainm + 1] != faid_VALUE) fàilligeadh_VALUE("class name does not match file");
        for (int 수 = 0; 수 < faid_VALUE && !Mearachd; 수++) if (힙[caractar_ainm + 2 + 수] != faidhle_ainm_SMS[수]) fàilligeadh_VALUE("class name does not match file");
        int cur_a_steach_puing_VALUE = -1;
        for (int 수 = 0; 수 < dòigh_COUNT; 수++) if (Word_SMS(dòigh_ainm_SMS[수], "main") && Word_SMS(dòigh_TYPE[수], "([Ljava/lang/String;)V") && (dòigh_inntrigeadh[수] & 9) == 9) cur_a_steach_puing_VALUE = 수;
        if (cur_a_steach_puing_VALUE < 0) fàilligeadh_VALUE("public static void main(String[] args) required");
        if (Mearachd) return 1;
        int 인수 = sònraich_stòras(3, cleachdaiche.인수개수() - 1);
        for (int 수 = 1; 수 < cleachdaiche.인수개수() && !Mearachd; 수++) 힙[인수 + 1 + 수] = òstair_caractar(cleachdaiche.인수(수));
        frèam_INDEX = 0; frèam_dòigh[0] = cur_a_steach_puing_VALUE; frèam_suidhich[0] = dòigh_Start[cur_a_steach_puing_VALUE]; ionadail_VALUE[0] = 인수; ionadail_TYPE[0] = 2;
        gnìomhaich_àithne(); return Mearachd ? 1 : 0;
    }
}
