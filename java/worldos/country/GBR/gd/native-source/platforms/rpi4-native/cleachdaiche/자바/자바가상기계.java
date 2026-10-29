// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. faidhle/스택/fiosrachadh/meur 경계를 gnìomhaich_àithne 중 검사한다. */
public final class 자바가상기계 {
    static int[] faidhle = new int[16 * 16384], 임시파일 = new int[16384], faidhle_ainm_SMS = new int[512];
    static int[] cunbhalachan_taga = new int[8192], 상가 = new int[8192], cunbhalachan_SECOND_VALUE = new int[8192], sreang_fiosrachadh = new int[8192];
    static int[] dòigh_ainm_SMS = new int[512], dòigh_TYPE = new int[512], dòigh_inntrigeadh = new int[512], dòigh_sealbhadair = new int[512];
    static int[] dòigh_Start = new int[512], dòigh_crìochnaich = new int[512], dòigh_stac = new int[512], 함수지역 = new int[512];
    static int[] dòigh_argamaid_COUNT = new int[512], dòigh_argamaid_TYPE = new int[8192], dòigh_return = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] ionadail_VALUE = new int[16384], ionadail_TYPE = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] frèam_dòigh = new int[128], frèam_suidhich = new int[128], frèam_stac = new int[128], frèam_treòrachadh = new int[128], ro_shuidhich_frèam = new int[128];
    static int[] clas_deifinisean_ainm = new int[16], clas_deifinisean_atharraich_am_meud = new int[16], 종부모 = new int[16], clas_deifinisean_cor = new int[16], clas_slot_COUNT = new int[16], ro_shuidhich_clas_deifinisean = new int[16];
    static int[] clas_eadar_aghaidh = new int[16 * 16], clas_eadar_aghaidh_COUNT = new int[16];
    static int[] slot_ainm = new int[512], slot_TYPE = new int[512], slot_sealbhadair = new int[512], slot_ceadan = new int[512], slot_suidhich = new int[512], slot_dàta = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], ARRAY_eileamaid = new int[32768], Store_àireamh_shlàn = new int[256];
    static int atharraich_am_meud, 읽기위치, dòigh_COUNT, clas_ainm, frèam_INDEX = -1, 힙끝 = 1, return_TYPE;
    static int clas_deifinisean_COUNT, slot_COUNT, 잡기수, 현재읽는종, 던진객체, 잠시수, taisbean_COUNT, cruinneachadh_COUNT;
    static int 현재가닥, snàithlean_COUNT = 1, cur_a_steach_clas_deifinisean;
    static int[] snàithlean_frèam = new int[4], snàithlean_cor = new int[4], snàithlean_nì = new int[4], snàithlean_targaid = new int[4], 가닥대기 = new int[4];
    static boolean Mearachd, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], clas_snàithlean = new int[16];

    static void fàilligeadh_VALUE(String Word_SMS) {
        if (Mearachd) return;
        int roinn_seòrsa_CODE = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) roinn_seòrsa_CODE = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) roinn_seòrsa_CODE = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) roinn_seòrsa_CODE = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) roinn_seòrsa_CODE = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) roinn_seòrsa_CODE = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) roinn_seòrsa_CODE = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) roinn_seòrsa_CODE = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) roinn_seòrsa_CODE = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) roinn_seòrsa_CODE = 15;
        if (roinn_seòrsa_CODE != 0 && frèam_INDEX >= 0) { 예외던짐(roinn_seòrsa_CODE, Word_SMS); return; }
        cleachdaiche.sgrìobh("JVM error: "); cleachdaiche.sgrìobh(Word_SMS); cleachdaiche.sgrìobh_caractar_VALUE(10); Mearachd = true;
    }
    static boolean cliop(int ruith, int faid_VALUE) {
        if (ruith < 0 || ruith >= faidhle.length || faid_VALUE < 0) return false;
        int clas_deifinisean = ruith / 16384;
        return ruith % 16384 <= clas_deifinisean_atharraich_am_meud[clas_deifinisean] && faid_VALUE <= clas_deifinisean_atharraich_am_meud[clas_deifinisean] - ruith % 16384;
    }
    static int baidht_VALUE() {
        if (!cliop(읽기위치, 1)) { fàilligeadh_VALUE("truncated class file"); return 0; }
        return faidhle[읽기위치++];
    }
    static int 짧은수() { return baidht_VALUE() << 8 | baidht_VALUE(); }
    static int àireamh_shlàn() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int faid_VALUE) { if (!cliop(읽기위치, faid_VALUE)) fàilligeadh_VALUE("invalid attribute size"); else 읽기위치 += faid_VALUE; }
    static boolean seic_cunbhalachan(int 수, int 종류) {
        if (수 <= 0 || 수 >= cunbhalachan_taga.length || cunbhalachan_taga[수] != 종류) { fàilligeadh_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int ruith, int faid_VALUE, String Word_SMS) {
        if (!cliop(ruith, faid_VALUE)) return false;
        int 읽는자리 = ruith, 끝 = ruith + faid_VALUE;
        for (int lùb_INDEX = 0; lùb_INDEX < Word_SMS.length(); lùb_INDEX++) {
            int còd_a_charactair = Word_SMS.charAt(lùb_INDEX);
            if (còd_a_charactair > 0 && còd_a_charactair < 128) { if (읽는자리 >= 끝 || faidhle[읽는자리++] != còd_a_charactair) return false; }
            else if (còd_a_charactair < 2048) {
                if (읽는자리 + 2 > 끝 || faidhle[읽는자리++] != (192 | (còd_a_charactair >> 6)) || faidhle[읽는자리++] != (128 | (còd_a_charactair & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || faidhle[읽는자리++] != (224 | (còd_a_charactair >> 12)) || faidhle[읽는자리++] != (128 | ((còd_a_charactair >> 6) & 63)) || faidhle[읽는자리++] != (128 | (còd_a_charactair & 63))) return false;
        }
        return 읽는자리 == 끝;
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
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return dòigh_sealbhadair[frèam_dòigh[frèam_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int nì_COUNT = 짧은수();
        for (int 수 = 0; 수 < nì_COUNT && !Mearachd; 수++) { seic_cunbhalachan(상번호(), 1); 건너(àireamh_shlàn()); }
    }
    static int àithne_faid(int VALUE) {
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
    static int suidhich_àireamh_shlàn(int 읽는자리) {
        if (!cliop(읽는자리, 4)) { fàilligeadh_VALUE("truncated bytecode operand"); return 0; }
        return faidhle[읽는자리] << 24 | faidhle[읽는자리 + 1] << 16 | faidhle[읽는자리 + 2] << 8 | faidhle[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int ruith, int 끝) {
        int VALUE = faidhle[읽는자리], faid_VALUE = àithne_faid(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_suidhich = 읽는자리 + 1;
            while ((BASE_suidhich - ruith) % 4 != 0) BASE_suidhich++;
            if (끝 - BASE_suidhich < (VALUE == 170 ? 12 : 8)) return 0;
            int cur_a_steach_COUNT = VALUE == 170 ? suidhich_àireamh_shlàn(BASE_suidhich + 8) - suidhich_àireamh_shlàn(BASE_suidhich + 4) + 1 : suidhich_àireamh_shlàn(BASE_suidhich + 4);
            if (cur_a_steach_COUNT < 0 || cur_a_steach_COUNT > 2048) return 0;
            faid_VALUE = BASE_suidhich - 읽는자리 + (VALUE == 170 ? 12 + 4 * cur_a_steach_COUNT : 8 + 8 * cur_a_steach_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_dàta = faidhle[읽는자리 + 1]; faid_VALUE = Word_dàta == 132 ? 6 : (Word_dàta == 21 || Word_dàta == 25 || Word_dàta == 54 || Word_dàta == 58) ? 4 : 0;
        }
        return faid_VALUE > 0 && faid_VALUE <= 끝 - 읽는자리 ? faid_VALUE : 0;
    }
    static void seic_ceann_uidhe_VALUE(int ceann_uidhe_VALUE, int FUNCTION_VALUE) {
        if (ceann_uidhe_VALUE < dòigh_Start[FUNCTION_VALUE] || ceann_uidhe_VALUE >= dòigh_crìochnaich[FUNCTION_VALUE] || 경계[ceann_uidhe_VALUE] != FUNCTION_VALUE + 1) fàilligeadh_VALUE("invalid branch target");
    }
    static void 클래스읽기(int clas_deifinisean) {
        현재읽는종 = clas_deifinisean; 읽기위치 = clas_deifinisean * 16384; atharraich_am_meud = 읽기위치 + clas_deifinisean_atharraich_am_meud[clas_deifinisean];
        if (àireamh_shlàn() != 0xcafebabe) { fàilligeadh_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), tionndadh_VALUE = 짧은수();
        if (tionndadh_VALUE < 45 || tionndadh_VALUE > 52 || 부판 != 0) { fàilligeadh_VALUE("supported class versions: 45..52, minor 0"); return; }
        int cunbhalachan_COUNT = 짧은수(), BASE_suidhich = clas_deifinisean * 512;
        if (cunbhalachan_COUNT < 1 || cunbhalachan_COUNT > 512) { fàilligeadh_VALUE("constant pool limit (511)"); return; }
        for (int cur_a_steach_COUNT = 1; cur_a_steach_COUNT < cunbhalachan_COUNT && !Mearachd; cur_a_steach_COUNT++) {
            int 수 = BASE_suidhich + cur_a_steach_COUNT, 종류 = baidht_VALUE(); cunbhalachan_taga[수] = 종류;
            if (종류 == 1) { cunbhalachan_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(cunbhalachan_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = àireamh_shlàn();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); cunbhalachan_SECOND_VALUE[수] = 상번호(); }
            else fàilligeadh_VALUE("unsupported constant type");
        }
        int cead_VALUE = 짧은수();
        if ((cead_VALUE & (0x2000 | 0x4000)) != 0) fàilligeadh_VALUE("annotation/enum class unsupported");
        clas_deifinisean_ainm[clas_deifinisean] = clas_ainm_SMS(상번호());
        종부모[clas_deifinisean] = clas_ainm_SMS(상번호());
        int eadar_aghaidh_COUNT = 짧은수(); if (eadar_aghaidh_COUNT > 16) { fàilligeadh_VALUE("interface count limit"); return; }
        clas_eadar_aghaidh_COUNT[clas_deifinisean] = eadar_aghaidh_COUNT;
        for (int lùb_INDEX = 0; lùb_INDEX < eadar_aghaidh_COUNT; lùb_INDEX++) clas_eadar_aghaidh[clas_deifinisean * 16 + lùb_INDEX] = clas_ainm_SMS(상번호());
        int raon_COUNT = 짧은수();
        if (raon_COUNT > 512 - slot_COUNT) { fàilligeadh_VALUE("field count limit (512)"); return; }
        for (int lùb_INDEX = 0; lùb_INDEX < raon_COUNT && !Mearachd; lùb_INDEX++) {
            int faidhle_INDEX = slot_COUNT++; slot_sealbhadair[faidhle_INDEX] = clas_deifinisean; slot_ceadan[faidhle_INDEX] = 짧은수(); slot_ainm[faidhle_INDEX] = 상번호(); slot_TYPE[faidhle_INDEX] = 상번호();
            seic_cunbhalachan(slot_ainm[faidhle_INDEX], 1); seic_cunbhalachan(slot_TYPE[faidhle_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[slot_TYPE[faidhle_INDEX]]; int roinn_seòrsa_CODE = 서술형(읽기위치 + cunbhalachan_SECOND_VALUE[slot_TYPE[faidhle_INDEX]], false); 읽기위치 = 보존값;
            if ((slot_ceadan[faidhle_INDEX] & 8) == 0) slot_suidhich[faidhle_INDEX] = clas_slot_COUNT[clas_deifinisean]++;
            int buadh_dàta = 짧은수();
            for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < buadh_dàta && !Mearachd; Inner_Join_suidhich++) {
                int ainm_cunbhalachan = 상번호(), 유효길이 = àireamh_shlàn();
                if (Word_SMS(ainm_cunbhalachan, "ConstantValue") && 유효길이 == 2) {
                    int dàta_VALUE = 상번호();
                    if (roinn_seòrsa_CODE == 1 && seic_cunbhalachan(dàta_VALUE, 3)) slot_dàta[faidhle_INDEX] = 상가[dàta_VALUE];
                    else if (roinn_seòrsa_CODE == 2 && seic_cunbhalachan(dàta_VALUE, 8)) slot_dàta[faidhle_INDEX] = cunbhalachan_SMS(상가[dàta_VALUE]);
                } else 건너(유효길이);
            }
        }
        int nì_COUNT = 짧은수();
        if (nì_COUNT > 512 - dòigh_COUNT) { fàilligeadh_VALUE("method count limit (512)"); return; }
        for (int lùb_INDEX = 0; lùb_INDEX < nì_COUNT && !Mearachd; lùb_INDEX++) {
            int 수 = dòigh_COUNT++; dòigh_sealbhadair[수] = clas_deifinisean;
            dòigh_inntrigeadh[수] = 짧은수(); dòigh_ainm_SMS[수] = 상번호(); dòigh_TYPE[수] = 상번호();
            seic_cunbhalachan(dòigh_ainm_SMS[수], 1); 서술읽기(수);
            if ((dòigh_inntrigeadh[수] & 8) == 0) {
                if (dòigh_argamaid_COUNT[수] == 16) { fàilligeadh_VALUE("too many instance method arguments"); return; }
                for (int 비교자리 = dòigh_argamaid_COUNT[수]; 비교자리 > 0; 비교자리--) dòigh_argamaid_TYPE[수 * 16 + 비교자리] = dòigh_argamaid_TYPE[수 * 16 + 비교자리 - 1];
                dòigh_argamaid_TYPE[수 * 16] = 2; dòigh_argamaid_COUNT[수]++;
            }
            if ((dòigh_inntrigeadh[수] & 0x100) != 0) fàilligeadh_VALUE("user native method unsupported");
            if (Word_SMS(dòigh_ainm_SMS[수], "<clinit>")) ro_shuidhich_clas_deifinisean[clas_deifinisean] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (dòigh_sealbhadair[앞] == clas_deifinisean && 같은말(dòigh_ainm_SMS[앞], dòigh_ainm_SMS[수]) && 같은말(dòigh_TYPE[앞], dòigh_TYPE[수])) fàilligeadh_VALUE("duplicate method");
            int buadh_COUNT = 짧은수();
            for (int buadh_VALUE = 0; buadh_VALUE < buadh_COUNT && !Mearachd; buadh_VALUE++) {
                int Ainm = 상번호(), faid_VALUE = àireamh_shlàn(), ruith = 읽기위치;
                if (!cliop(ruith, faid_VALUE)) { fàilligeadh_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Ainm, "Code")) {
                    if (dòigh_Start[수] != 0) fàilligeadh_VALUE("duplicate Code attribute");
                    dòigh_stac[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_faid = àireamh_shlàn();
                    if (dòigh_stac[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < dòigh_argamaid_COUNT[수]
                        || CODE_faid < 1 || CODE_faid > 8192) fàilligeadh_VALUE("method memory limits exceeded");
                    dòigh_Start[수] = 읽기위치; 건너(CODE_faid); dòigh_crìochnaich[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { fàilligeadh_VALUE("exception table limit"); return; }
                    for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < 잡는수; Inner_Join_suidhich++) {
                        int mearachd_fiosrachadh = 잡기수++; 잡기함수[mearachd_fiosrachadh] = 수;
                        잡기시작[mearachd_fiosrachadh] = dòigh_Start[수] + 짧은수(); 잡기끝[mearachd_fiosrachadh] = dòigh_Start[수] + 짧은수();
                        잡기위치[mearachd_fiosrachadh] = dòigh_Start[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[mearachd_fiosrachadh] = 부호값 == 0 ? 0 : clas_ainm_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != ruith + faid_VALUE) fàilligeadh_VALUE("Code attribute size mismatch");
                } else 건너(faid_VALUE);
            }
            if ((dòigh_inntrigeadh[수] & 0x400) != 0) continue;
            if (dòigh_Start[수] == 0) fàilligeadh_VALUE("missing Code attribute");
            int slot_cur_a_steach = dòigh_Start[수];
            while (slot_cur_a_steach < dòigh_crìochnaich[수] && !Mearachd) {
                int faid_VALUE = 길이읽기(slot_cur_a_steach, dòigh_Start[수], dòigh_crìochnaich[수]);
                if (faid_VALUE == 0) { fàilligeadh_VALUE("unsupported or truncated bytecode"); break; }
                경계[slot_cur_a_steach] = 수 + 1; slot_cur_a_steach += faid_VALUE;
            }
            slot_cur_a_steach = dòigh_Start[수];
            while (slot_cur_a_steach < dòigh_crìochnaich[수] && !Mearachd) {
                int VALUE = faidhle[slot_cur_a_steach];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) seic_ceann_uidhe_VALUE(slot_cur_a_steach + (short)(faidhle[slot_cur_a_steach + 1] << 8 | faidhle[slot_cur_a_steach + 2]), 수);
                if (VALUE == 200) seic_ceann_uidhe_VALUE(slot_cur_a_steach + suidhich_àireamh_shlàn(slot_cur_a_steach + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = slot_cur_a_steach + 1; while ((읽는자리 - dòigh_Start[수]) % 4 != 0) 읽는자리++;
                    seic_ceann_uidhe_VALUE(slot_cur_a_steach + suidhich_àireamh_shlàn(읽는자리), 수);
                    int cur_a_steach_COUNT = VALUE == 170 ? suidhich_àireamh_shlàn(읽는자리 + 8) - suidhich_àireamh_shlàn(읽는자리 + 4) + 1 : suidhich_àireamh_shlàn(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < cur_a_steach_COUNT; Inner_Join_suidhich++) seic_ceann_uidhe_VALUE(slot_cur_a_steach + suidhich_àireamh_shlàn(읽는자리 + Inner_Join_suidhich * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                slot_cur_a_steach += 길이읽기(slot_cur_a_steach, dòigh_Start[수], dòigh_crìochnaich[수]);
            }
            for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < 잡기수; Inner_Join_suidhich++) if (잡기함수[Inner_Join_suidhich] == 수) {
                seic_ceann_uidhe_VALUE(잡기시작[Inner_Join_suidhich], 수); seic_ceann_uidhe_VALUE(잡기위치[Inner_Join_suidhich], 수);
                if (잡기끝[Inner_Join_suidhich] != dòigh_crìochnaich[수]) seic_ceann_uidhe_VALUE(잡기끝[Inner_Join_suidhich], 수);
                if (잡기시작[Inner_Join_suidhich] >= 잡기끝[Inner_Join_suidhich]) fàilligeadh_VALUE("invalid exception range");
            }
        }
        if (!Mearachd) 속성건너();
        if (읽기위치 != atharraich_am_meud) fàilligeadh_VALUE("extra class file data");
    }
    static int sònraich_stòras(int 종류, int faid_VALUE) { return 새기억(종류, faid_VALUE); }
    static boolean nì_VALUE(int fiosrachadh, int 종류) {
        if (!객체유효(fiosrachadh)) return false;
        if (힙[fiosrachadh] != 종류) { fàilligeadh_VALUE("object type mismatch"); return false; }
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
        if (return_TYPE == 2) dìon_VALUE(스택값[slot_cur_a_steach]);
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
        if (frèam_INDEX % 32 == 31) { fàilligeadh_VALUE("call stack limit (32)"); return; }
        int air_adhart_nì = frèam_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) ionadail_TYPE[air_adhart_nì * 128 + 수] = 0;
        for (int 수 = dòigh_argamaid_COUNT[FUNCTION_VALUE] - 1; 수 >= 0; 수--) {
            ionadail_VALUE[air_adhart_nì * 128 + 수] = 빼기(dòigh_argamaid_TYPE[FUNCTION_VALUE * 16 + 수]); ionadail_TYPE[air_adhart_nì * 128 + 수] = dòigh_argamaid_TYPE[FUNCTION_VALUE * 16 + 수];
        }
        if (Mearachd) return;
        frèam_INDEX = air_adhart_nì; ro_shuidhich_frèam[frèam_INDEX] = 0; frèam_dòigh[frèam_INDEX] = FUNCTION_VALUE; frèam_suidhich[frèam_INDEX] = dòigh_Start[FUNCTION_VALUE]; frèam_stac[frèam_INDEX] = 0;
    }
    static void return_tomhas(int TYPE_VALUE) {
        if (TYPE_VALUE != dòigh_return[frèam_dòigh[frèam_INDEX]]) { fàilligeadh_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (ro_shuidhich_frèam[frèam_INDEX] != 0) clas_deifinisean_cor[ro_shuidhich_frèam[frèam_INDEX] - 1] = 2;
        if (틀잠금[frèam_INDEX] != 0) { 잠금풀기(틀잠금[frèam_INDEX]); 틀잠금[frèam_INDEX] = 0; }
        frèam_INDEX--; if (frèam_INDEX >= 현재가닥 * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
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
                if (VALUE < 1) { fàilligeadh_VALUE("invalid file stream path"); return; }
                sruth_faidhle_ainm[slot_cur_a_steach] = VALUE;
            }
            sruth_faidhle_ainm[faid_VALUE] = 0;
            int 서술자 = cleachdaiche.파일서술자열기(sruth_faidhle_ainm, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { fàilligeadh_VALUE("FileNotFoundException: file open failed"); return; }
            힙[sruth_VALUE + 2] = 서술자; 힙[sruth_VALUE + 3] = 1;
            return;
        }
        if (àithne != 182) { fàilligeadh_VALUE("invalid file stream invocation"); return; }
        if ((출력 && Word_SMS(Ainm, "write") || !출력 && Word_SMS(Ainm, "read"))
            && (Word_SMS(fòrmat_VALUE, 출력 ? "([B)V" : "([B)I") || Word_SMS(fòrmat_VALUE, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean cliop_VALUE = Word_SMS(fòrmat_VALUE, 출력 ? "([BII)V" : "([BII)I");
            int cur_a_steach_COUNT = cliop_VALUE ? 빼기(1) : 0, 시작점 = cliop_VALUE ? 빼기(1) : 0, dàta_ARRAY = 빼기(2), nì_fiosrachadh = 빼기(2);
            if (!nì_VALUE(dàta_ARRAY, 20) || !nì_VALUE(nì_fiosrachadh, 종류)) return;
            if (!cliop_VALUE) cur_a_steach_COUNT = 힙[dàta_ARRAY + 1];
            if (시작점 < 0 || cur_a_steach_COUNT < 0 || 시작점 > 힙[dàta_ARRAY + 1] - cur_a_steach_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[nì_fiosrachadh + 3] == 0 || 힙[nì_fiosrachadh + 2] < 0) { fàilligeadh_VALUE("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < cur_a_steach_COUNT && !Mearachd) {
                int 반환값 = 출력 ? cleachdaiche.파일한바이트쓰기(힙[nì_fiosrachadh + 2], 힙[dàta_ARRAY + 2 + 시작점 + 완료수]) : cleachdaiche.파일한바이트읽기(힙[nì_fiosrachadh + 2]);
                if (반환값 < 0) { fàilligeadh_VALUE(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[dàta_ARRAY + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(cur_a_steach_COUNT != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Word_SMS(Ainm, "flush") && Word_SMS(fòrmat_VALUE, "()V")) { int nì_fiosrachadh = 빼기(2); if (nì_VALUE(nì_fiosrachadh, 종류) && 힙[nì_fiosrachadh + 2] < 0) fàilligeadh_VALUE("IOException: stream closed"); return; }
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
            if (tomhas < -1) fàilligeadh_VALUE("IOException: read failed"); else 넣기(tomhas == 256 ? -1 : tomhas, 1);
        } else if (cleachdaiche.파일한바이트쓰기(서술자, VALUE) != 1) fàilligeadh_VALUE("IOException: write failed");
    }
    static void CALL_dòigh(int INDEX, int àithne) {
        if (INDEX <= 0 || INDEX >= cunbhalachan_taga.length || (cunbhalachan_taga[INDEX] != 10 && cunbhalachan_taga[INDEX] != 11)) { fàilligeadh_VALUE("invalid method reference"); return; }
        int sealbhadair_VALUE = clas_ainm_SMS(상가[INDEX]), Ainm = fiosrachadh_ainm(cunbhalachan_SECOND_VALUE[INDEX]), fòrmat_VALUE = fiosrachadh_TYPE(cunbhalachan_SECOND_VALUE[INDEX]);
        if (Mearachd) return;
        if (기본호출(sealbhadair_VALUE, Ainm, fòrmat_VALUE, àithne)) return;
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
        int clas_deifinisean = FIND_clas_deifinisean(sealbhadair_VALUE); if (clas_deifinisean < 0 || Mearachd) return;
        int faidhle_INDEX = FIND_dòigh(clas_deifinisean, Ainm, fòrmat_VALUE);
        if (faidhle_INDEX < 0) {
            for (int còd_a_charactair = clas_deifinisean, cur_a_steach_COUNT = 0; còd_a_charactair >= 0 && cur_a_steach_COUNT < 16; cur_a_steach_COUNT++, còd_a_charactair = 부모종(còd_a_charactair))
                if (Word_SMS(종부모[còd_a_charactair], "java/lang/Thread")) { 가닥호출(Ainm, fòrmat_VALUE, àithne); return; }
            fàilligeadh_VALUE("NoSuchMethodError"); return;
        }
        if (((dòigh_inntrigeadh[faidhle_INDEX] & 8) != 0) != (àithne == 184)) { fàilligeadh_VALUE("method static/instance mismatch"); return; }
        if (àithne == 184) { if (!ro_shuidhich(dòigh_sealbhadair[faidhle_INDEX], frèam_treòrachadh[frèam_INDEX])) return; }
        else {
            int 읽는자리 = frèam_stac[frèam_INDEX] - dòigh_argamaid_COUNT[faidhle_INDEX];
            if (읽는자리 < 0 || 스택형[frèam_INDEX * 128 + 읽는자리] != 2) { fàilligeadh_VALUE("invalid method receiver"); return; }
            int nì_fiosrachadh = 스택값[frèam_INDEX * 128 + 읽는자리];
            if (!객체유효(nì_fiosrachadh)) return;
            if (힙[nì_fiosrachadh] < 32 || !종포함(힙[nì_fiosrachadh] - 32, sealbhadair_VALUE)) { fàilligeadh_VALUE("method receiver type mismatch"); return; }
            if (àithne != 183) faidhle_INDEX = FIND_dòigh(힙[nì_fiosrachadh] - 32, Ainm, fòrmat_VALUE);
        }
        if (faidhle_INDEX < 0 || (dòigh_inntrigeadh[faidhle_INDEX] & 0x400) != 0) { fàilligeadh_VALUE("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((dòigh_inntrigeadh[faidhle_INDEX] & 32) != 0) {
            if (àithne == 184) { int còd_a_charactair = dòigh_sealbhadair[faidhle_INDEX]; if (종잠금[còd_a_charactair] == 0) 종잠금[còd_a_charactair] = sònraich_stòras(8, 0); 잠금참조 = 종잠금[còd_a_charactair]; }
            else 잠금참조 = 스택값[frèam_INDEX * 128 + frèam_stac[frèam_INDEX] - dòigh_argamaid_COUNT[faidhle_INDEX]];
            if (!잠금얻기(잠금참조)) { if (!Mearachd) frèam_suidhich[frèam_INDEX] = frèam_treòrachadh[frèam_INDEX]; return; }
        }
        호출(faidhle_INDEX); if (!Mearachd) 틀잠금[frèam_INDEX] = 잠금참조;
    }
    static boolean 배열저장가능(int ARRAY_fiosrachadh, int dàta_VALUE) {
        if (dàta_VALUE == 0 || ARRAY_eileamaid[ARRAY_fiosrachadh] == 0) return true;
        boolean 성공여부 = ARRAY_eileamaid[ARRAY_fiosrachadh] == -1 ? (dàta_VALUE > 0 && dàta_VALUE < 힙끝 && 힙[dàta_VALUE] == 1) : 맞는객체(dàta_VALUE, ARRAY_eileamaid[ARRAY_fiosrachadh]);
        if (!성공여부 && !Mearachd) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int ARRAY_slot(int fiosrachadh, int fo_sgrìobhte_VALUE, int TYPE_VALUE) {
        if (!nì_VALUE(fiosrachadh, TYPE_VALUE)) return 0;
        if (fo_sgrìobhte_VALUE < 0 || fo_sgrìobhte_VALUE >= 힙[fiosrachadh + 1]) { fàilligeadh_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return fiosrachadh + 2 + fo_sgrìobhte_VALUE;
    }
    static void gnìomhaich_àithne() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (Mearachd) { if (던진객체 != 0) 예외처리(); if (Mearachd || frèam_INDEX < 현재가닥 * 32) break; }
            if (frèam_INDEX < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!SWITCH_snàithlean()) break; 조각 = 100; }
            if (frèam_INDEX == 0 && clas_deifinisean_cor[cur_a_steach_clas_deifinisean] != 2 && !ro_shuidhich(cur_a_steach_clas_deifinisean, frèam_suidhich[frèam_INDEX])) continue;
            if (frèam_INDEX == 현재가닥 * 32 && 현재가닥 != 0 && (dòigh_inntrigeadh[frèam_dòigh[frèam_INDEX]] & 32) != 0 && 틀잠금[frèam_INDEX] == 0) {
                int nì_fiosrachadh = snàithlean_targaid[현재가닥]; if (!잠금얻기(nì_fiosrachadh)) { if (Mearachd) break; continue; } 틀잠금[frèam_INDEX] = nì_fiosrachadh;
            }
            잠시수 = 0;
            if (--남음 == 0) { fàilligeadh_VALUE("instruction limit (500000)"); break; }
            int ruith = frèam_suidhich[frèam_INDEX]; frèam_treòrachadh[frèam_INDEX] = ruith; int VALUE = 명바();
            if (Mearachd) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = dòigh_sealbhadair[frèam_dòigh[frèam_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= cunbhalachan_taga.length) fàilligeadh_VALUE("invalid ldc constant");
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
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int cur_a_steach_suidhich = 빼기(1), nì_fiosrachadh = 빼기(2), roinn_seòrsa_CODE = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && nì_fiosrachadh > 0 && nì_fiosrachadh < 힙끝 && 힙[nì_fiosrachadh] == 21) roinn_seòrsa_CODE = 21;
                int 읽는자리 = ARRAY_slot(nì_fiosrachadh, cur_a_steach_suidhich, roinn_seòrsa_CODE); if (!Mearachd) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int cur_a_steach_fiosrachadh = 빼기(VALUE == 83 ? 2 : 1), cur_a_steach_suidhich = 빼기(1), nì_fiosrachadh = 빼기(2), roinn_seòrsa_CODE = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && nì_fiosrachadh > 0 && nì_fiosrachadh < 힙끝 && 힙[nì_fiosrachadh] == 21) roinn_seòrsa_CODE = 21;
                int 읽는자리 = ARRAY_slot(nì_fiosrachadh, cur_a_steach_suidhich, roinn_seòrsa_CODE);
                if (!Mearachd && roinn_seòrsa_CODE == 3 && !배열저장가능(nì_fiosrachadh, cur_a_steach_fiosrachadh)) continue;
                if (!Mearachd) 힙[읽는자리] = roinn_seòrsa_CODE == 20 ? (byte)cur_a_steach_fiosrachadh : roinn_seòrsa_CODE == 21 ? cur_a_steach_fiosrachadh & 1 : roinn_seòrsa_CODE == 22 ? (char)cur_a_steach_fiosrachadh : roinn_seòrsa_CODE == 23 ? (short)cur_a_steach_fiosrachadh : cur_a_steach_fiosrachadh;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { stac_treòrachadh(VALUE); continue; }
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
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, ruith); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { fàilligeadh_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_dòigh(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(clas_ainm_SMS(명상수()), ruith); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int roinn_seòrsa_CODE = 3, co_phàirt = 0;
                if (VALUE == 188) { int 임시값 = 명바(); roinn_seòrsa_CODE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else co_phàirt = clas_ainm_SMS(명상수());
                if (roinn_seòrsa_CODE == 0) { fàilligeadh_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), nì_fiosrachadh = sònraich_stòras(roinn_seòrsa_CODE, 유효길이); if (!Mearachd) ARRAY_eileamaid[nì_fiosrachadh] = co_phàirt; 넣기(nì_fiosrachadh, 2); continue;
            }
            if (VALUE == 190) {
                int nì_fiosrachadh = 빼기(2);
                if (객체유효(nì_fiosrachadh)) { int 비교자리 = 힙[nì_fiosrachadh]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) fàilligeadh_VALUE("not an array"); else 넣기(힙[nì_fiosrachadh + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int nì_fiosrachadh = 빼기(2); if (객체유효(nì_fiosrachadh)) { if (힙[nì_fiosrachadh] != 9) fàilligeadh_VALUE("athrow requires supported Throwable"); else { 던진객체 = nì_fiosrachadh; Mearachd = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int ainm_cunbhalachan = clas_ainm_SMS(명상수()), nì_fiosrachadh = 빼기(2); boolean MATCH = 맞는객체(nì_fiosrachadh, ainm_cunbhalachan);
                if (VALUE == 193) 넣기(nì_fiosrachadh != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !Mearachd) fàilligeadh_VALUE("ClassCastException"); 넣기(nì_fiosrachadh, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = ruith + 1, faidhle_INDEX = frèam_dòigh[frèam_INDEX], Iuchair_fiosrachadh = 빼기(1);
                while ((읽는자리 - dòigh_Start[faidhle_INDEX]) % 4 != 0) 읽는자리++;
                int targaid_ADDRESS = suidhich_àireamh_shlàn(읽는자리);
                if (VALUE == 170) { int 낮은값 = suidhich_àireamh_shlàn(읽는자리 + 4), 높은값 = suidhich_àireamh_shlàn(읽는자리 + 8); if (Iuchair_fiosrachadh >= 낮은값 && Iuchair_fiosrachadh <= 높은값) targaid_ADDRESS = suidhich_àireamh_shlàn(읽는자리 + 12 + (Iuchair_fiosrachadh - 낮은값) * 4); }
                else { int 총수 = suidhich_àireamh_shlàn(읽는자리 + 4); for (int lùb_INDEX = 0; lùb_INDEX < 총수; lùb_INDEX++) if (suidhich_àireamh_shlàn(읽는자리 + 8 + lùb_INDEX * 8) == Iuchair_fiosrachadh) targaid_ADDRESS = suidhich_àireamh_shlàn(읽는자리 + 12 + lùb_INDEX * 8); }
                gluais_VALUE(ruith + targaid_ADDRESS); continue;
            }
            if (VALUE == 200) { gluais_VALUE(ruith + suidhich_àireamh_shlàn(ruith + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int nì_fiosrachadh = 빼기(2);
                if (VALUE == 195) 잠금풀기(nì_fiosrachadh);
                else if (!잠금얻기(nì_fiosrachadh) && !Mearachd) { 넣기(nì_fiosrachadh, 2); frèam_suidhich[frèam_INDEX] = ruith; }
                continue;
            }
            if (VALUE == 196) {
                int àithne_CODE = 명바(), cur_a_steach_suidhich = 명짧();
                if (àithne_CODE == 21 || àithne_CODE == 25) 지역읽기(cur_a_steach_suidhich, àithne_CODE == 21 ? 1 : 2);
                else if (àithne_CODE == 54 || àithne_CODE == 58) sgrìobh_ionadail(cur_a_steach_suidhich, àithne_CODE == 54 ? 1 : 2);
                else if (àithne_CODE == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(cur_a_steach_suidhich, 1); 넣기(빼기(1) + DELTA_VALUE, 1); sgrìobh_ionadail(cur_a_steach_suidhich, 1); }
                else fàilligeadh_VALUE("unsupported wide opcode");
                continue;
            }
            fàilligeadh_VALUE("unsupported bytecode");
        }
    }
    static int FIND_clas_deifinisean(int Ainm) {
        for (int lùb_INDEX = 0; lùb_INDEX < clas_deifinisean_COUNT; lùb_INDEX++) if (clas_deifinisean_ainm[lùb_INDEX] != 0 && 같은말(clas_deifinisean_ainm[lùb_INDEX], Ainm)) return lùb_INDEX;
        return luchd_clas_deifinisean(cunbhalachan_SMS(Ainm));
    }
    static int luchd_clas_deifinisean(int ainm_sreang) {
        if (!nì_VALUE(ainm_sreang, 1)) return -1;
        int faid_VALUE = 힙[ainm_sreang + 1];
        if (faid_VALUE < 1 || faid_VALUE > 505 || clas_deifinisean_COUNT == 16) { fàilligeadh_VALUE("class name/count limit"); return -1; }
        for (int lùb_INDEX = 0; lùb_INDEX < faid_VALUE; lùb_INDEX++) { int còd_a_charactair = 힙[ainm_sreang + 2 + lùb_INDEX]; faidhle_ainm_SMS[lùb_INDEX] = còd_a_charactair == '/' ? '.' : còd_a_charactair; }
        faidhle_ainm_SMS[faid_VALUE] = '.'; faidhle_ainm_SMS[faid_VALUE + 1] = 'c'; faidhle_ainm_SMS[faid_VALUE + 2] = 'l'; faidhle_ainm_SMS[faid_VALUE + 3] = 'a'; faidhle_ainm_SMS[faid_VALUE + 4] = 's'; faidhle_ainm_SMS[faid_VALUE + 5] = 's'; faidhle_ainm_SMS[faid_VALUE + 6] = 0;
        int atharraich_am_meud = cleachdaiche.파일읽기(faidhle_ainm_SMS, 임시파일);
        if (atharraich_am_meud < 0) { fàilligeadh_VALUE("ClassNotFoundException"); return -1; }
        int clas_deifinisean = clas_deifinisean_COUNT++; clas_deifinisean_atharraich_am_meud[clas_deifinisean] = atharraich_am_meud;
        for (int lùb_INDEX = 0; lùb_INDEX < atharraich_am_meud; lùb_INDEX++) faidhle[clas_deifinisean * 16384 + lùb_INDEX] = 임시파일[lùb_INDEX];
        클래스읽기(clas_deifinisean); if (Mearachd) return -1;
        int dearbh_dàta = cunbhalachan_SMS(clas_deifinisean_ainm[clas_deifinisean]);
        if (!글같음(dearbh_dàta, ainm_sreang, true)) { fàilligeadh_VALUE("class name does not match file"); return -1; }
        int 부모 = 종부모[clas_deifinisean];
        if (부모 != 0 && !Word_SMS(부모, "java/lang/Object") && !Word_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_clas_deifinisean(부모);
            if (Mearachd || 위 < 0) return -1;
            int 읽는자리 = 위, stèidse_COUNT = 0;
            while (읽는자리 >= 0 && stèidse_COUNT++ < 16) {
                if (읽는자리 == clas_deifinisean) { fàilligeadh_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = clas_slot_COUNT[위];
            for (int faidhle_INDEX = 0; faidhle_INDEX < slot_COUNT; faidhle_INDEX++) if (slot_sealbhadair[faidhle_INDEX] == clas_deifinisean && (slot_ceadan[faidhle_INDEX] & 8) == 0) slot_suidhich[faidhle_INDEX] += 시작변위;
            clas_slot_COUNT[clas_deifinisean] += 시작변위;
        }
        return clas_deifinisean;
    }
    static int 부모종(int clas_deifinisean) {
        int Ainm = 종부모[clas_deifinisean];
        for (int lùb_INDEX = 0; lùb_INDEX < clas_deifinisean_COUNT; lùb_INDEX++) if (Ainm != 0 && clas_deifinisean_ainm[lùb_INDEX] != 0 && 같은말(clas_deifinisean_ainm[lùb_INDEX], Ainm)) return lùb_INDEX;
        return -1;
    }
    static int FIND_dòigh(int clas_deifinisean, int Ainm, int fòrmat_VALUE) {
        for (int 깊이 = 0; clas_deifinisean >= 0 && 깊이 < 16; 깊이++, clas_deifinisean = 부모종(clas_deifinisean)) {
            for (int lùb_INDEX = 0; lùb_INDEX < dòigh_COUNT; lùb_INDEX++) if (dòigh_sealbhadair[lùb_INDEX] == clas_deifinisean && 같은말(dòigh_ainm_SMS[lùb_INDEX], Ainm) && 같은말(dòigh_TYPE[lùb_INDEX], fòrmat_VALUE)) return lùb_INDEX;
        }
        return -1;
    }
    static int ainm_dòigh(int clas_deifinisean, String Ainm, String fòrmat_VALUE) {
        for (int 깊이 = 0; clas_deifinisean >= 0 && 깊이 < 16; 깊이++, clas_deifinisean = 부모종(clas_deifinisean))
            for (int lùb_INDEX = 0; lùb_INDEX < dòigh_COUNT; lùb_INDEX++) if (dòigh_sealbhadair[lùb_INDEX] == clas_deifinisean && Word_SMS(dòigh_ainm_SMS[lùb_INDEX], Ainm) && Word_SMS(dòigh_TYPE[lùb_INDEX], fòrmat_VALUE)) return lùb_INDEX;
        return -1;
    }
    static int 형종류(int Ainm) { return faidhle[상가[Ainm]] == 'L' || faidhle[상가[Ainm]] == '[' ? 2 : 1; }
    static boolean ro_shuidhich(int clas_deifinisean, int àithne_Start) {
        if (clas_deifinisean < 0 || Mearachd) return false;
        if (clas_deifinisean_cor[clas_deifinisean] == 3) { fàilligeadh_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (clas_deifinisean_cor[clas_deifinisean] == 1 && clas_snàithlean[clas_deifinisean] != 현재가닥) { frèam_suidhich[frèam_INDEX] = àithne_Start; 바꿈요청 = true; return false; }
        if (clas_deifinisean_cor[clas_deifinisean] != 0) return true;
        int 위 = 부모종(clas_deifinisean);
        if (위 >= 0 && !ro_shuidhich(위, àithne_Start)) return false;
        clas_deifinisean_cor[clas_deifinisean] = 1; clas_snàithlean[clas_deifinisean] = 현재가닥;
        if (ro_shuidhich_clas_deifinisean[clas_deifinisean] != 0) {
            frèam_suidhich[frèam_INDEX] = àithne_Start;
            호출(ro_shuidhich_clas_deifinisean[clas_deifinisean] - 1); if (!Mearachd) ro_shuidhich_frèam[frèam_INDEX] = clas_deifinisean + 1;
            return false;
        }
        clas_deifinisean_cor[clas_deifinisean] = 2; return true;
    }
    static void 필드호출(int INDEX, int àithne, int ruith) {
        if (!seic_cunbhalachan(INDEX, 9)) return;
        int sealbhadair_VALUE = clas_ainm_SMS(상가[INDEX]), Ainm = fiosrachadh_ainm(cunbhalachan_SECOND_VALUE[INDEX]), fòrmat_VALUE = fiosrachadh_TYPE(cunbhalachan_SECOND_VALUE[INDEX]);
        if (Word_SMS(sealbhadair_VALUE, "java/lang/System") && (Word_SMS(Ainm, "out") || Word_SMS(Ainm, "err")) && Word_SMS(fòrmat_VALUE, "Ljava/io/PrintStream;") && àithne == 178) { 넣기(-1, 2); return; }
        int clas_deifinisean = FIND_clas_deifinisean(sealbhadair_VALUE); if (clas_deifinisean < 0 || Mearachd) return;
        int 찾음 = -1;
        for (int 읽는자리 = clas_deifinisean, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int faidhle_INDEX = 0; faidhle_INDEX < slot_COUNT; faidhle_INDEX++) if (slot_sealbhadair[faidhle_INDEX] == 읽는자리 && 같은말(slot_ainm[faidhle_INDEX], Ainm) && 같은말(slot_TYPE[faidhle_INDEX], fòrmat_VALUE)) 찾음 = faidhle_INDEX;
        if (찾음 < 0) { fàilligeadh_VALUE("NoSuchFieldError"); return; }
        boolean stadaigeach_VALUE = àithne == 178 || àithne == 179;
        if (stadaigeach_VALUE != ((slot_ceadan[찾음] & 8) != 0)) { fàilligeadh_VALUE("field static/instance mismatch"); return; }
        if (stadaigeach_VALUE && !ro_shuidhich(slot_sealbhadair[찾음], ruith)) return;
        int TYPE_VALUE = 형종류(fòrmat_VALUE), VALUE = 0;
        if (àithne == 179 || àithne == 181) VALUE = 빼기(TYPE_VALUE);
        if (stadaigeach_VALUE) { if (àithne == 178) 넣기(slot_dàta[찾음], TYPE_VALUE); else if (!Mearachd) slot_dàta[찾음] = VALUE; return; }
        int nì_fiosrachadh = 빼기(2);
        if (!객체유효(nì_fiosrachadh)) return;
        if (힙[nì_fiosrachadh] < 32 || !종포함(힙[nì_fiosrachadh] - 32, sealbhadair_VALUE)) { fàilligeadh_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = nì_fiosrachadh + 2 + slot_suidhich[찾음];
        if (àithne == 180) 넣기(힙[보관칸], TYPE_VALUE);
        else if (!Mearachd) { 힙[보관칸] = VALUE; 힙참조[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int clas_deifinisean, int Ainm) {
        for (int 중첩깊이 = 0; clas_deifinisean >= 0 && 중첩깊이 < 16; 중첩깊이++, clas_deifinisean = 부모종(clas_deifinisean)) {
            if (같은말(clas_deifinisean_ainm[clas_deifinisean], Ainm) || (종부모[clas_deifinisean] != 0 && 같은말(종부모[clas_deifinisean], Ainm))) return true;
            for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < clas_eadar_aghaidh_COUNT[clas_deifinisean]; Inner_Join_suidhich++) if (같은말(clas_eadar_aghaidh[clas_deifinisean * 16 + Inner_Join_suidhich], Ainm)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int baidht_dàta, boolean Slighe) {
        if (첫값 == baidht_dàta) return true;
        if (첫값 <= 0 || baidht_dàta <= 0 || 힙[첫값] != 1 || 힙[baidht_dàta] != 1 || 힙[첫값 + 1] != 힙[baidht_dàta + 1]) return false;
        for (int lùb_INDEX = 0; lùb_INDEX < 힙[첫값 + 1]; lùb_INDEX++) {
            int co_chomharra_x = 힙[첫값 + 2 + lùb_INDEX], 세로좌표 = 힙[baidht_dàta + 2 + lùb_INDEX];
            if (Slighe) { if (co_chomharra_x == '.') co_chomharra_x = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (co_chomharra_x != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int nì_fiosrachadh) {
        if (nì_fiosrachadh == 0) { fàilligeadh_VALUE("NullPointerException"); return false; }
        if (nì_fiosrachadh < 1 || nì_fiosrachadh >= 힙끝 || 힙폭[nì_fiosrachadh] < 2 || 힙[nì_fiosrachadh] == 0) { fàilligeadh_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void dìon_VALUE(int nì_fiosrachadh) {
        if (nì_fiosrachadh > 0 && nì_fiosrachadh < 힙끝 && 힙폭[nì_fiosrachadh] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = nì_fiosrachadh;
    }
    static void show_VALUE(int nì_fiosrachadh) {
        if (nì_fiosrachadh > 0 && nì_fiosrachadh < 힙끝 && 힙폭[nì_fiosrachadh] >= 2 && 힙[nì_fiosrachadh] != 0 && 힙표시[nì_fiosrachadh] == 0) {
            힙표시[nì_fiosrachadh] = 1; 표시대기[taisbean_COUNT++] = nì_fiosrachadh;
        }
    }
    static void 수거() {
        taisbean_COUNT = 0; cruinneachadh_COUNT++;
        for (int seic_suidhich = 1; seic_suidhich < 힙끝; seic_suidhich += 힙폭[seic_suidhich]) 힙표시[seic_suidhich] = 0;
        for (int lùb_INDEX = 0; lùb_INDEX < sreang_fiosrachadh.length; lùb_INDEX++) show_VALUE(sreang_fiosrachadh[lùb_INDEX]);
        for (int lùb_INDEX = 0; lùb_INDEX < slot_COUNT; lùb_INDEX++) if ((slot_ceadan[lùb_INDEX] & 8) != 0 && 형종류(slot_TYPE[lùb_INDEX]) == 2) show_VALUE(slot_dàta[lùb_INDEX]);
        for (int 임시값 = 0; 임시값 < snàithlean_COUNT; 임시값++) {
            show_VALUE(snàithlean_nì[임시값]); show_VALUE(snàithlean_targaid[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? frèam_INDEX : snàithlean_frèam[임시값];
            for (int faidhle_INDEX = 임시값 * 32; faidhle_INDEX <= 꼭대기자리; faidhle_INDEX++) {
                for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < 함수지역[frèam_dòigh[faidhle_INDEX]]; Inner_Join_suidhich++) if (ionadail_TYPE[faidhle_INDEX * 128 + Inner_Join_suidhich] == 2) show_VALUE(ionadail_VALUE[faidhle_INDEX * 128 + Inner_Join_suidhich]);
                for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < frèam_stac[faidhle_INDEX]; Inner_Join_suidhich++) if (스택형[faidhle_INDEX * 128 + Inner_Join_suidhich] == 2) show_VALUE(스택값[faidhle_INDEX * 128 + Inner_Join_suidhich]);
            }
        }
        for (int lùb_INDEX = 0; lùb_INDEX < 화면참조.length; lùb_INDEX++) show_VALUE(화면참조[lùb_INDEX]);
        for (int lùb_INDEX = 0; lùb_INDEX < 나중수; lùb_INDEX++) show_VALUE(나중실행[lùb_INDEX]);
        for (int lùb_INDEX = 0; lùb_INDEX < Store_àireamh_shlàn.length; lùb_INDEX++) show_VALUE(Store_àireamh_shlàn[lùb_INDEX]);
        for (int lùb_INDEX = 0; lùb_INDEX < clas_deifinisean_COUNT; lùb_INDEX++) show_VALUE(종잠금[lùb_INDEX]);
        for (int seic_suidhich = 1; seic_suidhich < 힙끝; seic_suidhich += 힙폭[seic_suidhich]) if (잠금깊이[seic_suidhich] > 0) show_VALUE(seic_suidhich);
        show_VALUE(던진객체);
        for (int lùb_INDEX = 0; lùb_INDEX < 잠시수; lùb_INDEX++) show_VALUE(잠시참조[lùb_INDEX]);
        while (taisbean_COUNT > 0) {
            int nì_fiosrachadh = 표시대기[--taisbean_COUNT], roinn_seòrsa_CODE = 힙[nì_fiosrachadh];
            for (int lùb_INDEX = nì_fiosrachadh + 2; lùb_INDEX < nì_fiosrachadh + 힙폭[nì_fiosrachadh]; lùb_INDEX++) if (roinn_seòrsa_CODE == 3 || roinn_seòrsa_CODE == 4 || 힙참조[lùb_INDEX] != 0) show_VALUE(힙[lùb_INDEX]);
        }
        for (int seic_suidhich = 1; seic_suidhich < 힙끝; seic_suidhich += 힙폭[seic_suidhich]) if (힙표시[seic_suidhich] == 0) 힙[seic_suidhich] = 0;
        for (int seic_suidhich = 1; seic_suidhich < 힙끝; seic_suidhich += 힙폭[seic_suidhich]) if (힙[seic_suidhich] == 0) {
            while (seic_suidhich + 힙폭[seic_suidhich] < 힙끝 && 힙[seic_suidhich + 힙폭[seic_suidhich]] == 0) { int air_adhart_suidhich = seic_suidhich + 힙폭[seic_suidhich]; 힙폭[seic_suidhich] += 힙폭[air_adhart_suidhich]; 힙폭[air_adhart_suidhich] = 0; }
            if (seic_suidhich + 힙폭[seic_suidhich] == 힙끝) { 힙끝 = seic_suidhich; break; }
        }
    }
    static int 새기억(int 종류, int faid_VALUE) {
        if (faid_VALUE < 0) { fàilligeadh_VALUE("NegativeArraySizeException"); return 0; }
        if (faid_VALUE > 힙.length - 3) { fàilligeadh_VALUE("object heap exhausted"); return 0; }
        int 필요수 = faid_VALUE + 2, nì_fiosrachadh = 0;
        if (필요수 <= 힙.length - 힙끝) { nì_fiosrachadh = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { nì_fiosrachadh = 읽는자리; break; }
            if (nì_fiosrachadh != 0) {
                int 남은길이 = 힙폭[nì_fiosrachadh] - 필요수;
                if (남은길이 >= 2) { 힙폭[nì_fiosrachadh + 필요수] = 남은길이; 힙[nì_fiosrachadh + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { nì_fiosrachadh = 힙끝; 힙끝 += 필요수; }
        }
        if (nì_fiosrachadh == 0) { fàilligeadh_VALUE("object heap exhausted"); return 0; }
        for (int lùb_INDEX = 0; lùb_INDEX < 필요수; lùb_INDEX++) { 힙[nì_fiosrachadh + lùb_INDEX] = 0; 힙참조[nì_fiosrachadh + lùb_INDEX] = 0; 힙폭[nì_fiosrachadh + lùb_INDEX] = 0; }
        ARRAY_eileamaid[nì_fiosrachadh] = 0;
        힙폭[nì_fiosrachadh] = 필요수; 힙[nì_fiosrachadh] = 종류; 힙[nì_fiosrachadh + 1] = faid_VALUE; dìon_VALUE(nì_fiosrachadh); return nì_fiosrachadh;
    }
    static int 예외종(String ainm_cunbhalachan) {
        if (자바도구.같음(ainm_cunbhalachan, "java/lang/Throwable")) return 1;
        if (자바도구.같음(ainm_cunbhalachan, "java/lang/Exception")) return 2;
        if (자바도구.같음(ainm_cunbhalachan, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(ainm_cunbhalachan, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(ainm_cunbhalachan, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(ainm_cunbhalachan, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(ainm_cunbhalachan, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(ainm_cunbhalachan, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(ainm_cunbhalachan, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(ainm_cunbhalachan, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(ainm_cunbhalachan, "java/io/IOException")) return 11;
        if (자바도구.같음(ainm_cunbhalachan, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(ainm_cunbhalachan, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(ainm_cunbhalachan, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(ainm_cunbhalachan, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int 예외상수(int Ainm) {
        for (int lùb_INDEX = 1; lùb_INDEX <= 41; lùb_INDEX++) if (Word_SMS(Ainm, 예외이름(lùb_INDEX))) return lùb_INDEX;
        return 0;
    }
    static String 예외이름(int cunntas_VALUE) {
        if (cunntas_VALUE == 40) return "java/lang/InterruptedException";
        if (cunntas_VALUE == 41) return "한국어/자체/대기중단예외";
        if (cunntas_VALUE == 39) return "java/net/SocketException";
        if (cunntas_VALUE == 20) return "한국어/자체/예외";
        if (cunntas_VALUE == 21) return "한국어/자체/실행예외";
        if (cunntas_VALUE == 22) return "한국어/자체/입출력예외";
        if (cunntas_VALUE == 23) return "한국어/자체/대기시간초과예외";
        if (cunntas_VALUE == 24) return "한국어/자체/주소확인예외";
        if (cunntas_VALUE == 25) return "한국어/자체/파일없음예외";
        if (cunntas_VALUE == 26) return "한국어/자체/통신예외";
        if (cunntas_VALUE == 27) return "한국어/자체/잘못된인수예외";
        if (cunntas_VALUE == 28) return "한국어/자체/숫자형식예외";
        if (cunntas_VALUE == 29) return "한국어/자체/범위예외";
        if (cunntas_VALUE == 30) return "한국어/자체/배열범위예외";
        if (cunntas_VALUE == 31) return "한국어/자체/문자열범위예외";
        if (cunntas_VALUE == 32) return "한국어/자체/빈참조예외";
        if (cunntas_VALUE == 33) return "한국어/자체/산술예외";
        if (cunntas_VALUE == 34) return "한국어/자체/상태예외";
        if (cunntas_VALUE == 35) return "한국어/자체/형변환예외";
        if (cunntas_VALUE == 36) return "한국어/자체/음수배열크기예외";
        if (cunntas_VALUE == 37) return "한국어/자체/ARRAY_Store_fàilligeadh";
        if (cunntas_VALUE == 38) return "한국어/자체/가닥상태예외";
        if (cunntas_VALUE == 1) return "java/lang/Throwable"; if (cunntas_VALUE == 2) return "java/lang/Exception";
        if (cunntas_VALUE == 3) return "java/lang/RuntimeException"; if (cunntas_VALUE == 4) return "java/lang/ArithmeticException";
        if (cunntas_VALUE == 5) return "java/lang/NullPointerException"; if (cunntas_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (cunntas_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (cunntas_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (cunntas_VALUE == 9) return "java/lang/IllegalArgumentException"; if (cunntas_VALUE == 10) return "java/lang/NumberFormatException";
        if (cunntas_VALUE == 11) return "java/io/IOException"; if (cunntas_VALUE == 12) return "java/io/FileNotFoundException";
        if (cunntas_VALUE == 17) return "java/lang/ArrayStoreException";
        if (cunntas_VALUE == 18) return "java/net/UnknownHostException";
        if (cunntas_VALUE == 19) return "java/net/SocketTimeoutException";
        if (cunntas_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (cunntas_VALUE == 13) return "java/lang/IllegalStateException"; if (cunntas_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int cunntas_VALUE) {
        if (cunntas_VALUE == 40) return 2;
        if (cunntas_VALUE == 41) return 40;
        if (cunntas_VALUE == 39) return 11;
        if (cunntas_VALUE == 1) return 0;
        if (cunntas_VALUE == 2) return 1;
        if (cunntas_VALUE == 3) return 2;
        if (cunntas_VALUE == 4) return 3;
        if (cunntas_VALUE == 5) return 3;
        if (cunntas_VALUE == 6) return 3;
        if (cunntas_VALUE == 7) return 6;
        if (cunntas_VALUE == 8) return 6;
        if (cunntas_VALUE == 9) return 3;
        if (cunntas_VALUE == 10) return 9;
        if (cunntas_VALUE == 11) return 2;
        if (cunntas_VALUE == 12) return 11;
        if (cunntas_VALUE == 13) return 3;
        if (cunntas_VALUE == 14) return 3;
        if (cunntas_VALUE == 15) return 3;
        if (cunntas_VALUE == 16) return 9;
        if (cunntas_VALUE == 17) return 3;
        if (cunntas_VALUE == 18) return 11;
        if (cunntas_VALUE == 19) return 11;
        if (cunntas_VALUE == 20) return 2;
        if (cunntas_VALUE == 21) return 3;
        if (cunntas_VALUE == 22) return 11;
        if (cunntas_VALUE == 23) return 22;
        if (cunntas_VALUE == 24) return 22;
        if (cunntas_VALUE == 25) return 22;
        if (cunntas_VALUE == 26) return 22;
        if (cunntas_VALUE == 27) return 9;
        if (cunntas_VALUE == 28) return 27;
        if (cunntas_VALUE == 29) return 6;
        if (cunntas_VALUE == 30) return 29;
        if (cunntas_VALUE == 31) return 29;
        if (cunntas_VALUE == 32) return 5;
        if (cunntas_VALUE == 33) return 4;
        if (cunntas_VALUE == 34) return 13;
        if (cunntas_VALUE == 35) return 14;
        if (cunntas_VALUE == 36) return 15;
        if (cunntas_VALUE == 37) return 17;
        if (cunntas_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int dearbh_VALUE, int 요구값) {
        for (int 깊이 = 0; dearbh_VALUE != 0 && 깊이 < 16; 깊이++, dearbh_VALUE = 예외부모(dearbh_VALUE))
            if (dearbh_VALUE == 요구값) return true;
        return false;
    }
    static void 예외던짐(int cunntas_VALUE, String LEUGHMI_fiosrachadh) {
        int nì_fiosrachadh = 새기억(9, 2); if (Mearachd) return;
        힙[nì_fiosrachadh + 2] = cunntas_VALUE; 힙[nì_fiosrachadh + 3] = òstair_caractar(LEUGHMI_fiosrachadh); 힙참조[nì_fiosrachadh + 3] = 1;
        던진객체 = nì_fiosrachadh; Mearachd = true;
    }
    static boolean 맞는객체(int nì_fiosrachadh, int Ainm) {
        if (nì_fiosrachadh == 0) return true;
        if (!객체유효(nì_fiosrachadh)) return false;
        int roinn_seòrsa_CODE = 힙[nì_fiosrachadh];
        if (Word_SMS(Ainm, "java/lang/Object")) return true;
        if (roinn_seòrsa_CODE >= 32) return 종포함(roinn_seòrsa_CODE - 32, Ainm);
        if (roinn_seòrsa_CODE == 9) { int targaid_ADDRESS = 예외상수(Ainm); return targaid_ADDRESS != 0 && 예외포함(힙[nì_fiosrachadh + 2], targaid_ADDRESS); }
        if (roinn_seòrsa_CODE == 1) return Word_SMS(Ainm, "java/lang/String") || Word_SMS(Ainm, "java/lang/CharSequence");
        if (roinn_seòrsa_CODE == 4) return Word_SMS(Ainm, "java/lang/StringBuilder") || Word_SMS(Ainm, "java/lang/CharSequence");
        if (roinn_seòrsa_CODE == 10) return Word_SMS(Ainm, "java/util/ArrayList") || Word_SMS(Ainm, "java/util/List");
        if (roinn_seòrsa_CODE == 11) return Word_SMS(Ainm, "java/util/HashMap") || Word_SMS(Ainm, "java/util/Map");
        if (roinn_seòrsa_CODE == 12) return Word_SMS(Ainm, "java/lang/Integer") || Word_SMS(Ainm, "java/lang/Number");
        if (roinn_seòrsa_CODE >= 24 && roinn_seòrsa_CODE <= 28 && 힙[nì_fiosrachadh + 13] != 0) return 한국어화면종(Ainm) == roinn_seòrsa_CODE || Word_SMS(Ainm, "한국어/자체/화면구성요소");
        if (roinn_seòrsa_CODE >= 24 && roinn_seòrsa_CODE <= 28) return (한국어화면종(Ainm) == 0 && 화면종(Ainm) == roinn_seòrsa_CODE) || Word_SMS(Ainm, "java/awt/Component") || Word_SMS(Ainm, "java/awt/Container") || Word_SMS(Ainm, "javax/swing/JComponent");
        if (roinn_seòrsa_CODE == 29) return Word_SMS(Ainm, 힙[nì_fiosrachadh + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (roinn_seòrsa_CODE == 30) return Word_SMS(Ainm, "java/awt/FlowLayout") || Word_SMS(Ainm, "java/awt/LayoutManager");
        if (roinn_seòrsa_CODE == 17) return Word_SMS(Ainm, "java/net/Socket");
        if (roinn_seòrsa_CODE == 18) return Word_SMS(Ainm, "java/net/ServerSocket");
        if (roinn_seòrsa_CODE == 19) return Word_SMS(Ainm, 힙[nì_fiosrachadh + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (roinn_seòrsa_CODE == 14) return Word_SMS(Ainm, "java/net/InetAddress");
        if (roinn_seòrsa_CODE == 15) return Word_SMS(Ainm, "java/net/DatagramSocket");
        if (roinn_seòrsa_CODE == 16) return Word_SMS(Ainm, "java/net/DatagramPacket");
        if (roinn_seòrsa_CODE == 13) return Word_SMS(Ainm, 힙[nì_fiosrachadh + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (roinn_seòrsa_CODE == 2) return Word_SMS(Ainm, "[I"); if (roinn_seòrsa_CODE == 20) return Word_SMS(Ainm, "[B"); if (roinn_seòrsa_CODE == 21) return Word_SMS(Ainm, "[Z");
        if (roinn_seòrsa_CODE == 22) return Word_SMS(Ainm, "[C"); if (roinn_seòrsa_CODE == 23) return Word_SMS(Ainm, "[S");
        if (roinn_seòrsa_CODE != 3) return false;
        if (Word_SMS(Ainm, "[Ljava/lang/Object;")) return true;
        int co_phàirt = ARRAY_eileamaid[nì_fiosrachadh];
        if (co_phàirt == -1) return Word_SMS(Ainm, "[Ljava/lang/String;") || Word_SMS(Ainm, "[Ljava/lang/CharSequence;");
        if (co_phàirt == 0) return false;
        if (배열종비교(co_phàirt, Ainm)) return true;
        if ((Word_SMS(co_phàirt, "java/lang/String") || Word_SMS(co_phàirt, "java/lang/StringBuilder")) && Word_SMS(Ainm, "[Ljava/lang/CharSequence;")) return true;
        for (int lùb_INDEX = 0; lùb_INDEX < clas_deifinisean_COUNT; lùb_INDEX++) if (같은말(clas_deifinisean_ainm[lùb_INDEX], co_phàirt)) {
            for (int còd_a_charactair = lùb_INDEX, 중첩깊이 = 0; còd_a_charactair >= 0 && 중첩깊이 < 16; 중첩깊이++, còd_a_charactair = 부모종(còd_a_charactair)) {
                if (배열종비교(종부모[còd_a_charactair], Ainm)) return true;
                for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < clas_eadar_aghaidh_COUNT[còd_a_charactair]; Inner_Join_suidhich++) if (배열종비교(clas_eadar_aghaidh[còd_a_charactair * 16 + Inner_Join_suidhich], Ainm)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int ainm_cunbhalachan, int 형식참조) {
        int seic_suidhich = 상가[형식참조], cur_a_steach_COUNT = cunbhalachan_SECOND_VALUE[형식참조];
        if (ainm_cunbhalachan == 0 || cur_a_steach_COUNT < 4 || faidhle[seic_suidhich] != '[' || faidhle[seic_suidhich + 1] != 'L' || faidhle[seic_suidhich + cur_a_steach_COUNT - 1] != ';' || cunbhalachan_SECOND_VALUE[ainm_cunbhalachan] != cur_a_steach_COUNT - 3) return false;
        for (int lùb_INDEX = 0; lùb_INDEX < cur_a_steach_COUNT - 3; lùb_INDEX++) if (faidhle[상가[ainm_cunbhalachan] + lùb_INDEX] != faidhle[seic_suidhich + 2 + lùb_INDEX]) return false;
        return true;
    }
    static void 예외처리() {
        if (던진객체 == 0) return;
        Mearachd = false;
        while (frèam_INDEX >= 현재가닥 * 32) {
            int faidhle_INDEX = frèam_dòigh[frèam_INDEX], 읽는자리 = frèam_treòrachadh[frèam_INDEX];
            for (int lùb_INDEX = 0; lùb_INDEX < 잡기수; lùb_INDEX++) if (잡기함수[lùb_INDEX] == faidhle_INDEX && 읽는자리 >= 잡기시작[lùb_INDEX] && 읽는자리 < 잡기끝[lùb_INDEX]
                && (잡기종[lùb_INDEX] == 0 || 맞는객체(던진객체, 잡기종[lùb_INDEX]))) {
                frèam_suidhich[frèam_INDEX] = 잡기위치[lùb_INDEX]; frèam_stac[frèam_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (ro_shuidhich_frèam[frèam_INDEX] != 0) clas_deifinisean_cor[ro_shuidhich_frèam[frèam_INDEX] - 1] = 3;
            if (틀잠금[frèam_INDEX] != 0) { 잠금풀기(틀잠금[frèam_INDEX]); 틀잠금[frèam_INDEX] = 0; }
            frèam_INDEX--;
        }
        cleachdaiche.sgrìobh("Uncaught ");
        if (힙[던진객체] == 9) { cleachdaiche.sgrìobh(예외이름(힙[던진객체 + 2])); cleachdaiche.sgrìobh(": "); sgrìobh_SMS(힙[던진객체 + 3]); }
        else cleachdaiche.sgrìobh("user exception");
        cleachdaiche.sgrìobh_caractar_VALUE(10); 던진객체 = 0; Mearachd = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void stac_treòrachadh(int àithne_CODE) {
        int 첫값 = 빼기(0), 첫형식 = return_TYPE;
        if (àithne_CODE == 87) return;
        if (àithne_CODE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int baidht_dàta = 빼기(0), SECOND_fòrmat = return_TYPE;
        if (àithne_CODE == 88) return;
        if (àithne_CODE == 90) { 넣기(첫값, 첫형식); 넣기(baidht_dàta, SECOND_fòrmat); 넣기(첫값, 첫형식); return; }
        if (àithne_CODE == 92) { 넣기(baidht_dàta, SECOND_fòrmat); 넣기(첫값, 첫형식); 넣기(baidht_dàta, SECOND_fòrmat); 넣기(첫값, 첫형식); return; }
        if (àithne_CODE == 95) { 넣기(첫값, 첫형식); 넣기(baidht_dàta, SECOND_fòrmat); return; }
        int còd_a_charactair = 빼기(0), 셋째형식 = return_TYPE;
        if (àithne_CODE == 91) { 넣기(첫값, 첫형식); 넣기(còd_a_charactair, 셋째형식); 넣기(baidht_dàta, SECOND_fòrmat); 넣기(첫값, 첫형식); return; }
        if (àithne_CODE == 93) { 넣기(baidht_dàta, SECOND_fòrmat); 넣기(첫값, 첫형식); 넣기(còd_a_charactair, 셋째형식); 넣기(baidht_dàta, SECOND_fòrmat); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = return_TYPE;
        넣기(baidht_dàta, SECOND_fòrmat); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(còd_a_charactair, 셋째형식); 넣기(baidht_dàta, SECOND_fòrmat); 넣기(첫값, 첫형식);
    }
    static void 새객체(int ainm_cunbhalachan, int 시작점) {
        int roinn_seòrsa_CODE = 0, 유효길이 = 0, 예외참조 = 예외상수(ainm_cunbhalachan);
        if (Word_SMS(ainm_cunbhalachan, "java/lang/StringBuilder")) { roinn_seòrsa_CODE = 4; 유효길이 = 1; }
        if (Word_SMS(ainm_cunbhalachan, "java/io/FileInputStream")) { roinn_seòrsa_CODE = 5; 유효길이 = 2; }
        if (Word_SMS(ainm_cunbhalachan, "java/io/FileOutputStream")) { roinn_seòrsa_CODE = 6; 유효길이 = 2; }
        if (예외참조 != 0) { roinn_seòrsa_CODE = 9; 유효길이 = 2; }
        if (Word_SMS(ainm_cunbhalachan, "java/util/ArrayList")) { roinn_seòrsa_CODE = 10; 유효길이 = 2; }
        if (Word_SMS(ainm_cunbhalachan, "java/util/HashMap")) { roinn_seòrsa_CODE = 11; 유효길이 = 2; }
        if (Word_SMS(ainm_cunbhalachan, "java/lang/Integer")) { roinn_seòrsa_CODE = 12; 유효길이 = 1; }
        if (Word_SMS(ainm_cunbhalachan, "java/net/Socket")) { roinn_seòrsa_CODE = 17; 유효길이 = 5; }
        if (Word_SMS(ainm_cunbhalachan, "java/net/ServerSocket")) { roinn_seòrsa_CODE = 18; 유효길이 = 5; }
        if (Word_SMS(ainm_cunbhalachan, "java/net/DatagramSocket")) { roinn_seòrsa_CODE = 15; 유효길이 = 3; }
        if (Word_SMS(ainm_cunbhalachan, "java/net/DatagramPacket")) { roinn_seòrsa_CODE = 16; 유효길이 = 4; }
        if (Word_SMS(ainm_cunbhalachan, "java/lang/Thread") || Word_SMS(ainm_cunbhalachan, "한국어/자체/작업가닥")) { roinn_seòrsa_CODE = 13; 유효길이 = 2; }
        if (Word_SMS(ainm_cunbhalachan, "java/lang/Object")) { roinn_seòrsa_CODE = 8; }
        if (roinn_seòrsa_CODE == 0 && 화면종(ainm_cunbhalachan) != 0) { roinn_seòrsa_CODE = 화면종(ainm_cunbhalachan); 유효길이 = 12; }
        if (roinn_seòrsa_CODE == 0) {
            int còd_a_charactair = FIND_clas_deifinisean(ainm_cunbhalachan); if (còd_a_charactair < 0 || Mearachd || !ro_shuidhich(còd_a_charactair, 시작점)) return;
            roinn_seòrsa_CODE = 32 + còd_a_charactair; 유효길이 = clas_slot_COUNT[còd_a_charactair];
        }
        int nì_fiosrachadh = sònraich_stòras(roinn_seòrsa_CODE, 유효길이); if (Mearachd) return;
        if (roinn_seòrsa_CODE == 13 && Word_SMS(ainm_cunbhalachan, "한국어/자체/작업가닥")) 힙[nì_fiosrachadh + 3] = 1;
        if (roinn_seòrsa_CODE >= 24 && roinn_seòrsa_CODE <= 28 && 한국어화면종(ainm_cunbhalachan) != 0) 힙[nì_fiosrachadh + 13] = 1;
        if (roinn_seòrsa_CODE == 5 || roinn_seòrsa_CODE == 6 || roinn_seòrsa_CODE == 15 || roinn_seòrsa_CODE == 17 || roinn_seòrsa_CODE == 18) 힙[nì_fiosrachadh + 2] = -1;
        if (roinn_seòrsa_CODE == 9) 힙[nì_fiosrachadh + 2] = 예외참조;
        넣기(nì_fiosrachadh, 2);
    }
    static boolean 값같음(int 첫값, int baidht_dàta) {
        if (첫값 == baidht_dàta) return true;
        if (첫값 == 0 || baidht_dàta == 0 || 첫값 < 0 || baidht_dàta < 0 || 첫값 >= 힙끝 || baidht_dàta >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[baidht_dàta] == 1) return 글같음(첫값, baidht_dàta, false);
        return 힙[첫값] == 12 && 힙[baidht_dàta] == 12 && 힙[첫값 + 2] == 힙[baidht_dàta + 2];
    }
    static int 글조각(int nì_fiosrachadh, int Start_suidhich, int crìochnaich_suidhich) {
        if (!nì_VALUE(nì_fiosrachadh, 1)) return 0;
        if (Start_suidhich < 0 || crìochnaich_suidhich < Start_suidhich || crìochnaich_suidhich > 힙[nì_fiosrachadh + 1]) { fàilligeadh_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = sònraich_stòras(1, crìochnaich_suidhich - Start_suidhich); if (Mearachd) return 0;
        for (int lùb_INDEX = Start_suidhich; lùb_INDEX < crìochnaich_suidhich; lùb_INDEX++) 힙[반환값 + 2 + lùb_INDEX - Start_suidhich] = 힙[nì_fiosrachadh + 2 + lùb_INDEX];
        return 반환값;
    }
    static int co_cheangal_SMS(int 첫값, int baidht_dàta) {
        if (!nì_VALUE(첫값, 1) || !nì_VALUE(baidht_dàta, 1)) return 0;
        int cur_a_steach_COUNT = 힙[첫값 + 1], dòigh_INDEX = 힙[baidht_dàta + 1], 반환값 = sònraich_stòras(1, cur_a_steach_COUNT + dòigh_INDEX); if (Mearachd) return 0;
        for (int lùb_INDEX = 0; lùb_INDEX < cur_a_steach_COUNT; lùb_INDEX++) 힙[반환값 + 2 + lùb_INDEX] = 힙[첫값 + 2 + lùb_INDEX];
        for (int lùb_INDEX = 0; lùb_INDEX < dòigh_INDEX; lùb_INDEX++) 힙[반환값 + 2 + cur_a_steach_COUNT + lùb_INDEX] = 힙[baidht_dàta + 2 + lùb_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int sealbhadair, int ainm_cunbhalachan, int 서술상수, int àithne_CODE) {
        if (Word_SMS(sealbhadair, "한국어/자체/실행인수") && àithne_CODE == 184) {
            if (Word_SMS(ainm_cunbhalachan, "nì_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(cleachdaiche.인수개수() - 1, 1); return true; }
            if (Word_SMS(ainm_cunbhalachan, "SMS") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= cleachdaiche.인수개수() - 1) 예외던짐(29, "gnìomhaich_àithne 인수 범위를 벗어났습니다");
                else 넣기(òstair_caractar(cleachdaiche.인수(순번 + 1)), 2);
                return true;
            }
            fàilligeadh_VALUE("지원하지 않는 한국어 gnìomhaich_àithne 인수 호출"); return true;
        }
        if (Word_SMS(sealbhadair, "한국어/자체/작업가닥")) { Pròiseas_snàithlean(ainm_cunbhalachan, 서술상수, àithne_CODE, true); return true; }
        if (한국어화면소유(sealbhadair)) { 한국어화면호출(sealbhadair, ainm_cunbhalachan, 서술상수, àithne_CODE); return true; }
        if (화면소유(sealbhadair)) { 화면호출(sealbhadair, ainm_cunbhalachan, 서술상수, àithne_CODE); return true; }
        if (Word_SMS(sealbhadair, "java/net/Socket") || Word_SMS(sealbhadair, "java/net/ServerSocket") || Word_SMS(sealbhadair, "java/io/InputStream") || Word_SMS(sealbhadair, "java/io/OutputStream")) { 흐름호출(sealbhadair, ainm_cunbhalachan, 서술상수, àithne_CODE); return true; }
        if (Word_SMS(sealbhadair, "한국어/자체/eitean_VALUE") && àithne_CODE == 184) {
            if (Word_SMS(ainm_cunbhalachan, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(cleachdaiche.화면너비(), 1); return true; }
            if (Word_SMS(ainm_cunbhalachan, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(cleachdaiche.화면높이(), 1); return true; }
            if (Word_SMS(ainm_cunbhalachan, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(cleachdaiche.밀리초(), 1); return true; }
            if (Word_SMS(ainm_cunbhalachan, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(cleachdaiche.그림대기(), 1); return true; }
            if (Word_SMS(ainm_cunbhalachan, "사각형") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), co_chomharra_x = 빼기(1); 넣기(cleachdaiche.사각형(co_chomharra_x, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(sealbhadair, "java/net/InetAddress") || Word_SMS(sealbhadair, "java/net/DatagramPacket") || Word_SMS(sealbhadair, "java/net/DatagramSocket")) { 통신호출(sealbhadair, ainm_cunbhalachan, 서술상수, àithne_CODE); return true; }
        if (Word_SMS(sealbhadair, "java/lang/Thread")) { 가닥호출(ainm_cunbhalachan, 서술상수, àithne_CODE); return true; }
        if (Word_SMS(sealbhadair, "java/lang/Object")) {
            if (Word_SMS(ainm_cunbhalachan, "<init>") && Word_SMS(서술상수, "()V") && àithne_CODE == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(ainm_cunbhalachan, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int baidht_dàta = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == baidht_dàta ? 1 : 0, 1); return true; }
        }
        if (예외상수(sealbhadair) != 0) {
            if (Word_SMS(ainm_cunbhalachan, "<init>") && àithne_CODE == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int brodadh = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), nì_fiosrachadh = 빼기(2);
                if (nì_VALUE(nì_fiosrachadh, 9)) { 힙[nì_fiosrachadh + 3] = brodadh; 힙참조[nì_fiosrachadh + 3] = 1; } return true;
            }
            if ((Word_SMS(ainm_cunbhalachan, "getMessage") || Word_SMS(ainm_cunbhalachan, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int nì_fiosrachadh = 빼기(2); if (nì_VALUE(nì_fiosrachadh, 9)) 넣기(힙[nì_fiosrachadh + 3], 2); return true; }
        }
        if (Word_SMS(sealbhadair, "java/lang/String")) {
            if (àithne_CODE == 182 && Word_SMS(ainm_cunbhalachan, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int còdachadh_ainm = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), nì_fiosrachadh = 빼기(2);
                if (!nì_VALUE(nì_fiosrachadh, 1)) return true;
                if (còdachadh_ainm != 0 && !글같음(còdachadh_ainm, òstair_caractar("UTF-8"), false) && !글같음(còdachadh_ainm, òstair_caractar("UTF8"), false) && !글같음(còdachadh_ainm, òstair_caractar("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int cur_a_steach_COUNT = 힙[nì_fiosrachadh + 1], 반환값 = sònraich_stòras(20, cur_a_steach_COUNT * 3), 사용수 = 0; if (Mearachd) return true;
                for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < cur_a_steach_COUNT; Inner_Join_suidhich++) {
                    int còd_a_charactair = 힙[nì_fiosrachadh + 2 + Inner_Join_suidhich];
                    if (còd_a_charactair >= 0xd800 && còd_a_charactair <= 0xdbff && Inner_Join_suidhich + 1 < cur_a_steach_COUNT && 힙[nì_fiosrachadh + 3 + Inner_Join_suidhich] >= 0xdc00 && 힙[nì_fiosrachadh + 3 + Inner_Join_suidhich] <= 0xdfff) còd_a_charactair = 0x10000 + ((còd_a_charactair - 0xd800) << 10) + 힙[nì_fiosrachadh + 2 + ++Inner_Join_suidhich] - 0xdc00;
                    else if (còd_a_charactair >= 0xd800 && còd_a_charactair <= 0xdfff) còd_a_charactair = '?';
                    if (còd_a_charactair < 128) 힙[반환값 + 2 + 사용수++] = còd_a_charactair;
                    else { int baidht_COUNT = còd_a_charactair < 2048 ? 2 : còd_a_charactair < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((baidht_COUNT == 2 ? 192 : baidht_COUNT == 3 ? 224 : 240) | còd_a_charactair >> (6 * (baidht_COUNT - 1))); for (int 비교자리 = baidht_COUNT - 1; 비교자리 > 0; 비교자리--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | còd_a_charactair >> (6 * (비교자리 - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (àithne_CODE == 184 && Word_SMS(ainm_cunbhalachan, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(figear_caractar(빼기(1)), 2); return true; }
            if (àithne_CODE != 182) return false;
            if (Word_SMS(ainm_cunbhalachan, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int baidht_dàta = 빼기(2), 첫값 = 빼기(2); if (nì_VALUE(첫값, 1)) 넣기(글같음(첫값, baidht_dàta, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(ainm_cunbhalachan, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (nì_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(ainm_cunbhalachan, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int crìochnaich_suidhich = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (nì_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? crìochnaich_suidhich : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(ainm_cunbhalachan, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int baidht_dàta = 빼기(2), 첫값 = 빼기(2); 넣기(co_cheangal_SMS(첫값, baidht_dàta), 2); return true; }
            if (Word_SMS(ainm_cunbhalachan, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), hais_VALUE = 0; if (nì_VALUE(첫값, 1)) { for (int lùb_INDEX = 0; lùb_INDEX < 힙[첫값 + 1]; lùb_INDEX++) hais_VALUE = hais_VALUE * 31 + 힙[첫값 + 2 + lùb_INDEX]; 넣기(hais_VALUE, 1); } return true; }
            if (Word_SMS(ainm_cunbhalachan, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (nì_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(sealbhadair, "java/lang/Integer")) {
            if (àithne_CODE == 184 && Word_SMS(ainm_cunbhalachan, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int dàta_VALUE = 빼기(1), nì_fiosrachadh = dàta_VALUE >= -128 && dàta_VALUE <= 127 ? Store_àireamh_shlàn[dàta_VALUE + 128] : 0; if (nì_fiosrachadh == 0) { nì_fiosrachadh = sònraich_stòras(12, 1); if (!Mearachd) { 힙[nì_fiosrachadh + 2] = dàta_VALUE; if (dàta_VALUE >= -128 && dàta_VALUE <= 127) Store_àireamh_shlàn[dàta_VALUE + 128] = nì_fiosrachadh; } } 넣기(nì_fiosrachadh, 2); return true; }
            if (àithne_CODE == 183 && Word_SMS(ainm_cunbhalachan, "<init>") && Word_SMS(서술상수, "(I)V")) { int dàta_VALUE = 빼기(1), nì_fiosrachadh = 빼기(2); if (nì_VALUE(nì_fiosrachadh, 12)) 힙[nì_fiosrachadh + 2] = dàta_VALUE; return true; }
            if (àithne_CODE == 182 && Word_SMS(ainm_cunbhalachan, "intValue") && Word_SMS(서술상수, "()I")) { int nì_fiosrachadh = 빼기(2); if (nì_VALUE(nì_fiosrachadh, 12)) 넣기(힙[nì_fiosrachadh + 2], 1); return true; }
            if (àithne_CODE == 184 && Word_SMS(ainm_cunbhalachan, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(figear_caractar(빼기(1)), 2); return true; }
        }
        if (Word_SMS(sealbhadair, "java/lang/Math") && àithne_CODE == 184) {
            if (Word_SMS(ainm_cunbhalachan, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(ainm_cunbhalachan, "min") || Word_SMS(ainm_cunbhalachan, "max")) && Word_SMS(서술상수, "(II)I")) { int baidht_dàta = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(ainm_cunbhalachan, "min") ? (첫값 < baidht_dàta ? 첫값 : baidht_dàta) : (첫값 > baidht_dàta ? 첫값 : baidht_dàta), 1); return true; }
        }
        if (Word_SMS(sealbhadair, "java/lang/System") && àithne_CODE == 184) {
            if (Word_SMS(ainm_cunbhalachan, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(ainm_cunbhalachan, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int cur_a_steach_COUNT = 빼기(1), ceann_uidhe_VALUE_INDEX = 빼기(1), baidht_dàta = 빼기(2), Start_suidhich = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(baidht_dàta)) {
                    int roinn_seòrsa_CODE = 힙[첫값];
                    if (힙[baidht_dàta] != roinn_seòrsa_CODE || (roinn_seòrsa_CODE != 2 && roinn_seòrsa_CODE != 3 && (roinn_seòrsa_CODE < 20 || roinn_seòrsa_CODE > 23))) fàilligeadh_VALUE("arraycopy type mismatch");
                    else if (cur_a_steach_COUNT < 0 || Start_suidhich < 0 || ceann_uidhe_VALUE_INDEX < 0 || Start_suidhich > 힙[첫값 + 1] - cur_a_steach_COUNT || ceann_uidhe_VALUE_INDEX > 힙[baidht_dàta + 1] - cur_a_steach_COUNT) fàilligeadh_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == baidht_dàta && ceann_uidhe_VALUE_INDEX > Start_suidhich) { for (int lùb_INDEX = cur_a_steach_COUNT - 1; lùb_INDEX >= 0; lùb_INDEX--) 힙[baidht_dàta + 2 + ceann_uidhe_VALUE_INDEX + lùb_INDEX] = 힙[첫값 + 2 + Start_suidhich + lùb_INDEX]; }
                    else { for (int lùb_INDEX = 0; lùb_INDEX < cur_a_steach_COUNT && !Mearachd; lùb_INDEX++) { int dàta_VALUE = 힙[첫값 + 2 + Start_suidhich + lùb_INDEX]; if (roinn_seòrsa_CODE != 3 || 배열저장가능(baidht_dàta, dàta_VALUE)) 힙[baidht_dàta + 2 + ceann_uidhe_VALUE_INDEX + lùb_INDEX] = dàta_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(sealbhadair, "java/util/ArrayList") || Word_SMS(sealbhadair, "java/util/List") || Word_SMS(sealbhadair, "java/util/HashMap") || Word_SMS(sealbhadair, "java/util/Map")) {
            모음호출(sealbhadair, ainm_cunbhalachan, 서술상수, àithne_CODE); return true;
        }
        return false;
    }
    static void 모음늘리기(int nì_fiosrachadh, int 필요수) {
        int 이전값 = 힙[nì_fiosrachadh + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int air_adhart_suidhich = 용량값 < 8 ? 8 : 용량값 * 2; if (air_adhart_suidhich < 필요수) air_adhart_suidhich = 필요수;
        int dàta_ARRAY = sònraich_stòras(3, air_adhart_suidhich); if (Mearachd) return;
        for (int lùb_INDEX = 0; lùb_INDEX < 용량값; lùb_INDEX++) 힙[dàta_ARRAY + 2 + lùb_INDEX] = 힙[이전값 + 2 + lùb_INDEX];
        힙[nì_fiosrachadh + 2] = dàta_ARRAY; 힙참조[nì_fiosrachadh + 2] = 1;
    }
    static void 모음호출(int sealbhadair, int ainm_cunbhalachan, int 서술상수, int àithne_CODE) {
        boolean 대응참조 = Word_SMS(sealbhadair, "java/util/HashMap") || Word_SMS(sealbhadair, "java/util/Map"); int roinn_seòrsa_CODE = 대응참조 ? 11 : 10;
        if (Word_SMS(ainm_cunbhalachan, "<init>") && àithne_CODE == 183 && Word_SMS(서술상수, "()V")) { int nì_fiosrachadh = 빼기(2); if (nì_VALUE(nì_fiosrachadh, roinn_seòrsa_CODE)) 모음늘리기(nì_fiosrachadh, 8); return; }
        if (àithne_CODE != 182 && àithne_CODE != 185) { fàilligeadh_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(ainm_cunbhalachan, "size") && Word_SMS(서술상수, "()I") || Word_SMS(ainm_cunbhalachan, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int nì_fiosrachadh = 빼기(2); if (nì_VALUE(nì_fiosrachadh, roinn_seòrsa_CODE)) 넣기(Word_SMS(ainm_cunbhalachan, "size") ? 힙[nì_fiosrachadh + 3] : 힙[nì_fiosrachadh + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(ainm_cunbhalachan, "clear") && Word_SMS(서술상수, "()V")) { int nì_fiosrachadh = 빼기(2); if (nì_VALUE(nì_fiosrachadh, roinn_seòrsa_CODE)) { int dàta_ARRAY = 힙[nì_fiosrachadh + 2]; for (int lùb_INDEX = 0; lùb_INDEX < 힙[dàta_ARRAY + 1]; lùb_INDEX++) 힙[dàta_ARRAY + 2 + lùb_INDEX] = 0; 힙[nì_fiosrachadh + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(ainm_cunbhalachan, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int dàta_VALUE = 빼기(2), nì_fiosrachadh = 빼기(2); if (!nì_VALUE(nì_fiosrachadh, 10)) return;
            int cur_a_steach_COUNT = 힙[nì_fiosrachadh + 3]; 모음늘리기(nì_fiosrachadh, cur_a_steach_COUNT + 1); if (!Mearachd) { 힙[힙[nì_fiosrachadh + 2] + 2 + cur_a_steach_COUNT] = dàta_VALUE; 힙[nì_fiosrachadh + 3] = cur_a_steach_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(ainm_cunbhalachan, "get") || Word_SMS(ainm_cunbhalachan, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(ainm_cunbhalachan, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Word_SMS(ainm_cunbhalachan, "set"); int dàta_VALUE = 지정여부 ? 빼기(2) : 0, cur_a_steach_suidhich = 빼기(1), nì_fiosrachadh = 빼기(2);
            if (!nì_VALUE(nì_fiosrachadh, 10)) return;
            int cur_a_steach_COUNT = 힙[nì_fiosrachadh + 3], dàta_ARRAY = 힙[nì_fiosrachadh + 2];
            if (cur_a_steach_suidhich < 0 || cur_a_steach_suidhich >= cur_a_steach_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[dàta_ARRAY + 2 + cur_a_steach_suidhich];
            if (지정여부) 힙[dàta_ARRAY + 2 + cur_a_steach_suidhich] = dàta_VALUE;
            if (Word_SMS(ainm_cunbhalachan, "remove")) { for (int lùb_INDEX = cur_a_steach_suidhich + 1; lùb_INDEX < cur_a_steach_COUNT; lùb_INDEX++) 힙[dàta_ARRAY + 1 + lùb_INDEX] = 힙[dàta_ARRAY + 2 + lùb_INDEX]; 힙[dàta_ARRAY + 1 + cur_a_steach_COUNT] = 0; 힙[nì_fiosrachadh + 3] = cur_a_steach_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(ainm_cunbhalachan, "get") || Word_SMS(ainm_cunbhalachan, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(ainm_cunbhalachan, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(ainm_cunbhalachan, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(ainm_cunbhalachan, "put"), thoir_air_falbh = Word_SMS(ainm_cunbhalachan, "remove");
            int dàta_VALUE = 넣기여부 ? 빼기(2) : 0, Iuchair_fiosrachadh = 빼기(2), nì_fiosrachadh = 빼기(2); if (!nì_VALUE(nì_fiosrachadh, 11)) return;
            int cur_a_steach_COUNT = 힙[nì_fiosrachadh + 3], dàta_ARRAY = 힙[nì_fiosrachadh + 2], 찾은여부 = -1;
            for (int lùb_INDEX = 0; lùb_INDEX < cur_a_steach_COUNT; lùb_INDEX++) if (값같음(Iuchair_fiosrachadh, 힙[dàta_ARRAY + 2 + 2 * lùb_INDEX])) { 찾은여부 = lùb_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[dàta_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(nì_fiosrachadh, (cur_a_steach_COUNT + 1) * 2); dàta_ARRAY = 힙[nì_fiosrachadh + 2]; 찾은여부 = cur_a_steach_COUNT; if (!Mearachd) 힙[nì_fiosrachadh + 3] = cur_a_steach_COUNT + 1; }
                if (!Mearachd) { 힙[dàta_ARRAY + 2 + 2 * 찾은여부] = Iuchair_fiosrachadh; 힙[dàta_ARRAY + 3 + 2 * 찾은여부] = dàta_VALUE; }
            }
            if (thoir_air_falbh && 찾은여부 >= 0) { for (int lùb_INDEX = 찾은여부 + 1; lùb_INDEX < cur_a_steach_COUNT; lùb_INDEX++) { 힙[dàta_ARRAY + 2 * lùb_INDEX] = 힙[dàta_ARRAY + 2 + 2 * lùb_INDEX]; 힙[dàta_ARRAY + 1 + 2 * lùb_INDEX] = 힙[dàta_ARRAY + 3 + 2 * lùb_INDEX]; } 힙[dàta_ARRAY + 2 * cur_a_steach_COUNT] = 0; 힙[dàta_ARRAY + 1 + 2 * cur_a_steach_COUNT] = 0; 힙[nì_fiosrachadh + 3] = cur_a_steach_COUNT - 1; }
            if (Word_SMS(ainm_cunbhalachan, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        fàilligeadh_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int nì_fiosrachadh) {
        if (!객체유효(nì_fiosrachadh)) return false;
        if (잠금깊이[nì_fiosrachadh] != 0 && 잠금주인[nì_fiosrachadh] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        잠금주인[nì_fiosrachadh] = 현재가닥 + 1; 잠금깊이[nì_fiosrachadh]++; return true;
    }
    static void 잠금풀기(int nì_fiosrachadh) {
        if (!객체유효(nì_fiosrachadh)) return;
        if (잠금깊이[nì_fiosrachadh] == 0 || 잠금주인[nì_fiosrachadh] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[nì_fiosrachadh] == 0) 잠금주인[nì_fiosrachadh] = 0;
    }
    static boolean SWITCH_snàithlean() {
        snàithlean_frèam[현재가닥] = frèam_INDEX;
        if (frèam_INDEX < 현재가닥 * 32) snàithlean_cor[현재가닥] = 3;
        for (int lùb_INDEX = 0; lùb_INDEX < snàithlean_COUNT; lùb_INDEX++) if (snàithlean_cor[lùb_INDEX] == 2 && snàithlean_cor[가닥대기[lùb_INDEX]] == 3) snàithlean_cor[lùb_INDEX] = 1;
        for (int lùb_INDEX = 1; lùb_INDEX <= snàithlean_COUNT; lùb_INDEX++) {
            int air_adhart_suidhich = (현재가닥 + lùb_INDEX) % snàithlean_COUNT;
            if (snàithlean_cor[air_adhart_suidhich] == 1) { 현재가닥 = air_adhart_suidhich; frèam_INDEX = snàithlean_frèam[air_adhart_suidhich]; 바꿈요청 = false; return true; }
        }
        for (int lùb_INDEX = 0; lùb_INDEX < snàithlean_COUNT; lùb_INDEX++) if (snàithlean_cor[lùb_INDEX] != 3) { fàilligeadh_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int ainm_cunbhalachan, int 서술상수, int àithne_CODE) { Pròiseas_snàithlean(ainm_cunbhalachan, 서술상수, àithne_CODE, false); }
    static void Pròiseas_snàithlean(int ainm_cunbhalachan, int 서술상수, int àithne_CODE, boolean 한국어) {
        if (àithne_CODE == 184 && Word_SMS(ainm_cunbhalachan, 한국어 ? "YIELD_saothair" : "yield") && Word_SMS(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (àithne_CODE == 184 && Word_SMS(ainm_cunbhalachan, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(snàithlean_nì[현재가닥], 2); return; }
        if (àithne_CODE == 183 && Word_SMS(ainm_cunbhalachan, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int targaid_ADDRESS = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), nì_fiosrachadh = 빼기(2);
            if (!객체유효(nì_fiosrachadh)) return;
            if (힙[nì_fiosrachadh] == 13) { 힙[nì_fiosrachadh + 2] = targaid_ADDRESS; 힙참조[nì_fiosrachadh + 2] = 1; }
            else if (targaid_ADDRESS != 0) fàilligeadh_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (àithne_CODE == 182 && (Word_SMS(ainm_cunbhalachan, 한국어 ? "Start_saothair" : "start") || Word_SMS(ainm_cunbhalachan, 한국어 ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || àithne_CODE == 182 && Word_SMS(ainm_cunbhalachan, 한국어 ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int nì_fiosrachadh = 빼기(2); if (!객체유효(nì_fiosrachadh)) return;
            int cunntas_VALUE = -1; for (int lùb_INDEX = 0; lùb_INDEX < snàithlean_COUNT; lùb_INDEX++) if (snàithlean_nì[lùb_INDEX] == nì_fiosrachadh) cunntas_VALUE = lùb_INDEX;
            if (Word_SMS(ainm_cunbhalachan, 한국어 ? "살아있는가" : "isAlive")) { 넣기(cunntas_VALUE >= 0 && snàithlean_cor[cunntas_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(ainm_cunbhalachan, 한국어 ? "기다리기" : "join")) { if (cunntas_VALUE >= 0 && snàithlean_cor[cunntas_VALUE] != 3) { 가닥대기[현재가닥] = cunntas_VALUE; snàithlean_cor[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (cunntas_VALUE >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (snàithlean_COUNT == 4) { fàilligeadh_VALUE("thread limit (4 including main)"); return; }
            int targaid_ADDRESS = 힙[nì_fiosrachadh] == 13 ? 힙[nì_fiosrachadh + 2] : nì_fiosrachadh;
            int faidhle_INDEX = targaid_ADDRESS > 0 && 힙[targaid_ADDRESS] >= 32 ? ainm_dòigh(힙[targaid_ADDRESS] - 32, 한국어 ? "Ruith" : "run", "()V") : -1;
            if (targaid_ADDRESS != 0 && faidhle_INDEX < 0) { fàilligeadh_VALUE("Runnable.run required"); return; }
            cunntas_VALUE = snàithlean_COUNT++; snàithlean_nì[cunntas_VALUE] = nì_fiosrachadh; snàithlean_targaid[cunntas_VALUE] = targaid_ADDRESS;
            int frèam = cunntas_VALUE * 32; snàithlean_frèam[cunntas_VALUE] = faidhle_INDEX < 0 ? frèam - 1 : frèam; snàithlean_cor[cunntas_VALUE] = faidhle_INDEX < 0 ? 3 : 1;
            if (faidhle_INDEX >= 0) { frèam_dòigh[frèam] = faidhle_INDEX; frèam_suidhich[frèam] = dòigh_Start[faidhle_INDEX]; ionadail_VALUE[frèam * 128] = targaid_ADDRESS; ionadail_TYPE[frèam * 128] = 2; }
            return;
        }
        fàilligeadh_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], ADDRESS_SMS = new int[16];
    static int ionadail_ADDRESS() { return ADDRESS_nì(0x7f000001); }
    static int ADDRESS_nì(int VALUE) { int nì_fiosrachadh = sònraich_stòras(14, 1); if (!Mearachd) 힙[nì_fiosrachadh + 2] = VALUE; return nì_fiosrachadh; }
    static int 주소해독(int nì_fiosrachadh) {
        if (nì_fiosrachadh == 0 || 글같음(nì_fiosrachadh, òstair_caractar("localhost"), false)) return 0x7f000001;
        if (!nì_VALUE(nì_fiosrachadh, 1)) return 0;
        int dàta_VALUE = 0, 총수 = 0, ADDRESS_baidht = 0, 자릿수 = 0, cur_a_steach_COUNT = 힙[nì_fiosrachadh + 1];
        for (int lùb_INDEX = 0; lùb_INDEX <= cur_a_steach_COUNT; lùb_INDEX++) {
            int còd_a_charactair = lùb_INDEX == cur_a_steach_COUNT ? '.' : 힙[nì_fiosrachadh + 2 + lùb_INDEX];
            if (còd_a_charactair == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } dàta_VALUE = dàta_VALUE << 8 | ADDRESS_baidht; 총수++; ADDRESS_baidht = 자릿수 = 0; }
            else { if (còd_a_charactair < '0' || còd_a_charactair > '9' || ++자릿수 > 3 || (ADDRESS_baidht = ADDRESS_baidht * 10 + còd_a_charactair - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return dàta_VALUE;
    }
    static int ADDRESS_caractar(int dàta_VALUE) {
        int cur_a_steach_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int ADDRESS_baidht = dàta_VALUE >>> 이동비트 & 255;
            if (ADDRESS_baidht >= 100) ADDRESS_SMS[cur_a_steach_COUNT++] = '0' + ADDRESS_baidht / 100;
            if (ADDRESS_baidht >= 10) ADDRESS_SMS[cur_a_steach_COUNT++] = '0' + ADDRESS_baidht / 10 % 10;
            ADDRESS_SMS[cur_a_steach_COUNT++] = '0' + ADDRESS_baidht % 10; if (이동비트 != 0) ADDRESS_SMS[cur_a_steach_COUNT++] = '.';
        }
        int nì_fiosrachadh = sònraich_stòras(1, cur_a_steach_COUNT); if (!Mearachd) for (int lùb_INDEX = 0; lùb_INDEX < cur_a_steach_COUNT; lùb_INDEX++) 힙[nì_fiosrachadh + 2 + lùb_INDEX] = ADDRESS_SMS[lùb_INDEX]; return nì_fiosrachadh;
    }
    static void 통신호출(int sealbhadair, int ainm_cunbhalachan, int 서술상수, int àithne_CODE) {
        if (Word_SMS(sealbhadair, "java/net/InetAddress")) {
            if (àithne_CODE == 184 && Word_SMS(ainm_cunbhalachan, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(ionadail_ADDRESS(), 2); return; }
            if (àithne_CODE == 184 && Word_SMS(ainm_cunbhalachan, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int dàta_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !Mearachd) 넣기(ADDRESS_nì(dàta_VALUE), 2); return;
            }
            if (àithne_CODE == 182 && Word_SMS(ainm_cunbhalachan, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int nì_fiosrachadh = 빼기(2); if (nì_VALUE(nì_fiosrachadh, 14)) 넣기(ADDRESS_caractar(힙[nì_fiosrachadh + 2]), 2); return; }
        }
        if (Word_SMS(sealbhadair, "java/net/DatagramPacket")) {
            if (àithne_CODE == 183 && Word_SMS(ainm_cunbhalachan, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean ceann_uidhe_VALUE_fiosrachadh = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = ceann_uidhe_VALUE_fiosrachadh ? 빼기(1) : 0, ADDRESS_fiosrachadh = ceann_uidhe_VALUE_fiosrachadh ? 빼기(2) : 0;
                int cur_a_steach_COUNT = 빼기(1), dàta_ARRAY = 빼기(2), nì_fiosrachadh = 빼기(2);
                if (!nì_VALUE(nì_fiosrachadh, 16) || !nì_VALUE(dàta_ARRAY, 20)) return;
                if (cur_a_steach_COUNT < 0 || cur_a_steach_COUNT > 힙[dàta_ARRAY + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (ADDRESS_fiosrachadh != 0 && !nì_VALUE(ADDRESS_fiosrachadh, 14)) return;
                힙[nì_fiosrachadh + 2] = dàta_ARRAY; 힙참조[nì_fiosrachadh + 2] = 1; 힙[nì_fiosrachadh + 3] = cur_a_steach_COUNT;
                힙[nì_fiosrachadh + 4] = ADDRESS_fiosrachadh; 힙참조[nì_fiosrachadh + 4] = 1; 힙[nì_fiosrachadh + 5] = 접속번호; return;
            }
            if (àithne_CODE == 182 && Word_SMS(ainm_cunbhalachan, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int cur_a_steach_COUNT = 빼기(1), nì_fiosrachadh = 빼기(2); if (!nì_VALUE(nì_fiosrachadh, 16)) return;
                if (cur_a_steach_COUNT < 0 || cur_a_steach_COUNT > 힙[힙[nì_fiosrachadh + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[nì_fiosrachadh + 3] = cur_a_steach_COUNT; return;
            }
            if (àithne_CODE == 182 && (Word_SMS(ainm_cunbhalachan, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(ainm_cunbhalachan, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(ainm_cunbhalachan, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(ainm_cunbhalachan, "getPort") && Word_SMS(서술상수, "()I"))) {
                int nì_fiosrachadh = 빼기(2); if (!nì_VALUE(nì_fiosrachadh, 16)) return;
                int cur_a_steach_suidhich = Word_SMS(ainm_cunbhalachan, "getData") ? 2 : Word_SMS(ainm_cunbhalachan, "getLength") ? 3 : Word_SMS(ainm_cunbhalachan, "getAddress") ? 4 : 5;
                넣기(힙[nì_fiosrachadh + cur_a_steach_suidhich], cur_a_steach_suidhich == 2 || cur_a_steach_suidhich == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(sealbhadair, "java/net/DatagramSocket")) {
            if (àithne_CODE == 183 && Word_SMS(ainm_cunbhalachan, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int 접속번호 = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), nì_fiosrachadh = 빼기(2); if (!nì_VALUE(nì_fiosrachadh, 15)) return;
                if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = cleachdaiche.fosgail_lìonra(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[nì_fiosrachadh + 2] = 열린파일번호; return;
            }
            if (àithne_CODE == 182 && Word_SMS(ainm_cunbhalachan, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), nì_fiosrachadh = 빼기(2); if (!nì_VALUE(nì_fiosrachadh, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[nì_fiosrachadh + 3] = 밀리초값; return;
            }
            if (àithne_CODE == 182 && Word_SMS(ainm_cunbhalachan, "getLocalPort") && Word_SMS(서술상수, "()I")) { int nì_fiosrachadh = 빼기(2); if (nì_VALUE(nì_fiosrachadh, 15)) 넣기(힙[nì_fiosrachadh + 2] < 0 ? -1 : cleachdaiche.lìonra_port(힙[nì_fiosrachadh + 2]), 1); return; }
            if (àithne_CODE == 182 && Word_SMS(ainm_cunbhalachan, "isClosed") && Word_SMS(서술상수, "()Z")) { int nì_fiosrachadh = 빼기(2); if (nì_VALUE(nì_fiosrachadh, 15)) 넣기(힙[nì_fiosrachadh + 2] < 0 ? 1 : 0, 1); return; }
            if (àithne_CODE == 182 && Word_SMS(ainm_cunbhalachan, "close") && Word_SMS(서술상수, "()V")) { int nì_fiosrachadh = 빼기(2); if (nì_VALUE(nì_fiosrachadh, 15) && 힙[nì_fiosrachadh + 2] >= 0) { cleachdaiche.파일서술자닫기(힙[nì_fiosrachadh + 2]); 힙[nì_fiosrachadh + 2] = -1; } return; }
            if (àithne_CODE == 182 && (Word_SMS(ainm_cunbhalachan, "send") || Word_SMS(ainm_cunbhalachan, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int 전문참조 = 빼기(2), nì_fiosrachadh = 빼기(2); if (!nì_VALUE(전문참조, 16) || !nì_VALUE(nì_fiosrachadh, 15)) return;
                int dàta_ARRAY = 힙[전문참조 + 2], 유효길이 = 힙[전문참조 + 3], 열린파일번호 = 힙[nì_fiosrachadh + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(ainm_cunbhalachan, "send")) {
                    if (!nì_VALUE(힙[전문참조 + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int lùb_INDEX = 0; lùb_INDEX < 유효길이; lùb_INDEX++) 통신임시[lùb_INDEX] = 힙[dàta_ARRAY + 2 + lùb_INDEX];
                    if (cleachdaiche.cuir_lìonra(열린파일번호, 힙[힙[전문참조 + 4] + 2], 힙[전문참조 + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int cur_a_steach_COUNT = cleachdaiche.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (cur_a_steach_COUNT == -11) {
                        int 현재시각 = cleachdaiche.밀리초();
                        if (힙[nì_fiosrachadh + 4] == 0) 힙[nì_fiosrachadh + 4] = 현재시각 + 1;
                        if (힙[nì_fiosrachadh + 3] > 0 && 현재시각 - (힙[nì_fiosrachadh + 4] - 1) >= 힙[nì_fiosrachadh + 3]) { 힙[nì_fiosrachadh + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(nì_fiosrachadh, 2); 넣기(전문참조, 2); frèam_suidhich[frèam_INDEX] = frèam_treòrachadh[frèam_INDEX]; 바꿈요청 = true; return;
                    }
                    힙[nì_fiosrachadh + 4] = 0;
                    if (cur_a_steach_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int lùb_INDEX = 0; lùb_INDEX < cur_a_steach_COUNT; lùb_INDEX++) 힙[dàta_ARRAY + 2 + lùb_INDEX] = (byte)통신임시[lùb_INDEX];
                    힙[전문참조 + 3] = cur_a_steach_COUNT; 힙[전문참조 + 4] = ADDRESS_nì(통신임시[513]); 힙참조[전문참조 + 4] = 1; 힙[전문참조 + 5] = 통신임시[512];
                }
                return;
            }
        }
        fàilligeadh_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int nì_fiosrachadh) {
        int 현재시각 = cleachdaiche.밀리초();
        if (힙[nì_fiosrachadh + 5] == 0) 힙[nì_fiosrachadh + 5] = 현재시각 + 1;
        if (힙[nì_fiosrachadh + 3] > 0 && 현재시각 - (힙[nì_fiosrachadh + 5] - 1) >= 힙[nì_fiosrachadh + 3]) { 힙[nì_fiosrachadh + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        frèam_suidhich[frèam_INDEX] = frèam_treòrachadh[frèam_INDEX]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int sealbhadair, int ainm_cunbhalachan, int 서술상수, int àithne_CODE) {
        boolean 수신쪽 = Word_SMS(sealbhadair, "java/net/ServerSocket"), sruth = Word_SMS(sealbhadair, "java/io/InputStream") || Word_SMS(sealbhadair, "java/io/OutputStream");
        if (!sruth && àithne_CODE == 183 && Word_SMS(ainm_cunbhalachan, "<init>")) {
            boolean 빈여부 = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && Word_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { fàilligeadh_VALUE("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), ADDRESS_fiosrachadh = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, nì_fiosrachadh = 빼기(2);
            if (!nì_VALUE(nì_fiosrachadh, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !nì_VALUE(ADDRESS_fiosrachadh, 14)) return;
            int lìonra_ADDRESS = 이름지정여부 ? 주소해독(ADDRESS_fiosrachadh) : 주소지정여부 ? 힙[ADDRESS_fiosrachadh + 2] : 0x7f000001;
            if (Mearachd || 던진객체 != 0) return;
            int 열린파일번호 = cleachdaiche.sruth_smachd(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? cleachdaiche.sruth_smachd(1, 열린파일번호, 접속번호) : cleachdaiche.CONNECT_sruth(열린파일번호, lìonra_ADDRESS, 접속번호);
            if (처리값 < 0) { cleachdaiche.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[nì_fiosrachadh + 2] = 열린파일번호; 힙[nì_fiosrachadh + 4] = 접속번호; 힙[nì_fiosrachadh + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!sruth && Word_SMS(ainm_cunbhalachan, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), nì_fiosrachadh = 빼기(2); if (!nì_VALUE(nì_fiosrachadh, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[nì_fiosrachadh + 3] = 밀리초값; return; }
        if (!sruth && Word_SMS(ainm_cunbhalachan, "close") && Word_SMS(서술상수, "()V")) { int nì_fiosrachadh = 빼기(2); if (nì_VALUE(nì_fiosrachadh, 수신쪽 ? 18 : 17) && 힙[nì_fiosrachadh + 2] >= 0) { cleachdaiche.파일서술자닫기(힙[nì_fiosrachadh + 2]); 힙[nì_fiosrachadh + 2] = -1; } return; }
        if (!sruth && (Word_SMS(ainm_cunbhalachan, "getLocalPort") || Word_SMS(ainm_cunbhalachan, "getPort") || Word_SMS(ainm_cunbhalachan, "isClosed") || Word_SMS(ainm_cunbhalachan, "isConnected"))) {
            int nì_fiosrachadh = 빼기(2); if (!nì_VALUE(nì_fiosrachadh, 수신쪽 ? 18 : 17)) return;
            넣기(Word_SMS(ainm_cunbhalachan, "isClosed") ? 힙[nì_fiosrachadh + 2] < 0 ? 1 : 0 : Word_SMS(ainm_cunbhalachan, "isConnected") ? 힙[nì_fiosrachadh + 6] : Word_SMS(ainm_cunbhalachan, "getPort") ? 힙[nì_fiosrachadh + 4] : 힙[nì_fiosrachadh + 2] < 0 ? -1 : cleachdaiche.sruth_smachd(4, 힙[nì_fiosrachadh + 2], 0), 1); return;
        }
        if (수신쪽 && Word_SMS(ainm_cunbhalachan, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int nì_fiosrachadh = 빼기(2); if (!nì_VALUE(nì_fiosrachadh, 18)) return; int 열린파일번호 = cleachdaiche.sruth_smachd(3, 힙[nì_fiosrachadh + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(nì_fiosrachadh)) 넣기(nì_fiosrachadh, 2); return; }
            힙[nì_fiosrachadh + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = sònraich_stòras(17, 5); if (Mearachd) { cleachdaiche.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = cleachdaiche.sruth_smachd(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !sruth && ((Word_SMS(ainm_cunbhalachan, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(ainm_cunbhalachan, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int nì_fiosrachadh = 빼기(2); if (!nì_VALUE(nì_fiosrachadh, 17)) return; if (힙[nì_fiosrachadh + 2] < 0 || 힙[nì_fiosrachadh + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = sònraich_stòras(19, 4); if (Mearachd) return; 힙[반환값 + 2] = nì_fiosrachadh; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(ainm_cunbhalachan, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (sruth) {
            boolean 읽기여부 = Word_SMS(ainm_cunbhalachan, "read"), 쓰기여부 = Word_SMS(ainm_cunbhalachan, "write"), bac = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), 부분배열여부 = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int cur_a_steach_COUNT = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, dàta_ARRAY = bac || 부분배열여부 ? 빼기(2) : 0;
            int dàta_VALUE = 쓰기여부 && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, nì_fiosrachadh = 빼기(2);
            if (!nì_VALUE(nì_fiosrachadh, 19)) return; int 부모참조 = 힙[nì_fiosrachadh + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(ainm_cunbhalachan, "close") && Word_SMS(서술상수, "()V")) { cleachdaiche.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Word_SMS(ainm_cunbhalachan, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[nì_fiosrachadh + 3] == 0)) { fàilligeadh_VALUE("unsupported stream operation"); return; }
            if (bac || 부분배열여부) { if (!nì_VALUE(dàta_ARRAY, 20)) return; if (bac) cur_a_steach_COUNT = 힙[dàta_ARRAY + 1]; if (시작변위 < 0 || cur_a_steach_COUNT < 0 || 시작변위 > 힙[dàta_ARRAY + 1] - cur_a_steach_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else cur_a_steach_COUNT = 1;
            if (cur_a_steach_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[nì_fiosrachadh + 4] : 0, 처리값 = 0;
            while (완료수 < cur_a_steach_COUNT) {
                처리값 = 읽기여부 ? cleachdaiche.파일한바이트읽기(열린파일번호) : cleachdaiche.파일한바이트쓰기(열린파일번호, bac || 부분배열여부 ? 힙[dàta_ARRAY + 2 + 시작변위 + 완료수] : dàta_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (bac || 부분배열여부)) 힙[dàta_ARRAY + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(bac || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[nì_fiosrachadh + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(nì_fiosrachadh, 2); if (bac || 부분배열여부) 넣기(dàta_ARRAY, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(cur_a_steach_COUNT, 1); } if (쓰기여부 && !(bac || 부분배열여부)) 넣기(dàta_VALUE, 1); } return;
            }
            힙[nì_fiosrachadh + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : bac || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        fàilligeadh_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int ainm_cunbhalachan) {
        if (Word_SMS(ainm_cunbhalachan, "한국어/자체/uinneag")) return 24;
        if (Word_SMS(ainm_cunbhalachan, "한국어/자체/bileag")) return 26;
        if (Word_SMS(ainm_cunbhalachan, "한국어/자체/putan")) return 27;
        if (Word_SMS(ainm_cunbhalachan, "한국어/자체/raon_teacsa")) return 28;
        if (Word_SMS(ainm_cunbhalachan, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int ainm_cunbhalachan) {
        return 한국어화면종(ainm_cunbhalachan) != 0 || Word_SMS(ainm_cunbhalachan, "한국어/자체/화면구성요소") || Word_SMS(ainm_cunbhalachan, "한국어/자체/tachartas_ciutha");
    }
    static int 화면종(int ainm_cunbhalachan) {
        int 한국어종 = 한국어화면종(ainm_cunbhalachan); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(ainm_cunbhalachan, "javax/swing/JFrame")) return 24;
        if (Word_SMS(ainm_cunbhalachan, "javax/swing/JPanel")) return 25;
        if (Word_SMS(ainm_cunbhalachan, "javax/swing/JLabel")) return 26;
        if (Word_SMS(ainm_cunbhalachan, "javax/swing/JButton")) return 27;
        if (Word_SMS(ainm_cunbhalachan, "javax/swing/JTextField")) return 28;
        if (Word_SMS(ainm_cunbhalachan, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(ainm_cunbhalachan, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int ainm_cunbhalachan) {
        return 화면종(ainm_cunbhalachan) != 0 || Word_SMS(ainm_cunbhalachan, "java/awt/Component") || Word_SMS(ainm_cunbhalachan, "java/awt/Container") || Word_SMS(ainm_cunbhalachan, "javax/swing/JComponent") || Word_SMS(ainm_cunbhalachan, "javax/swing/AbstractButton") || Word_SMS(ainm_cunbhalachan, "javax/swing/text/JTextComponent") || Word_SMS(ainm_cunbhalachan, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int nì_fiosrachadh) { if (!객체유효(nì_fiosrachadh)) return false; if (힙[nì_fiosrachadh] < 24 || 힙[nì_fiosrachadh] > 28) { fàilligeadh_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int nì_fiosrachadh, int SMS_fiosrachadh) {
        if (SMS_fiosrachadh != 0 && !nì_VALUE(SMS_fiosrachadh, 1)) return;
        int cur_a_steach_COUNT = SMS_fiosrachadh == 0 ? 0 : 힙[SMS_fiosrachadh + 1]; if (cur_a_steach_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int lùb_INDEX = 0; lùb_INDEX < cur_a_steach_COUNT; lùb_INDEX++) 화면글임시[lùb_INDEX] = 힙[SMS_fiosrachadh + 2 + lùb_INDEX];
        if (cleachdaiche.화면글(힙[nì_fiosrachadh + 2], 화면글임시, cur_a_steach_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[nì_fiosrachadh + 3] = SMS_fiosrachadh; 힙참조[nì_fiosrachadh + 3] = 1;
    }
    static int 화면문자읽기(int nì_fiosrachadh) {
        int cunntas_VALUE = 힙[nì_fiosrachadh + 2], cur_a_steach_COUNT = cleachdaiche.화면연결(8, cunntas_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (cur_a_steach_COUNT < 0) { fàilligeadh_VALUE("GUI text read failed"); return 0; }
        for (int lùb_INDEX = 0; lùb_INDEX < cur_a_steach_COUNT; lùb_INDEX++) { int 부호값 = cleachdaiche.화면연결(9, cunntas_VALUE, lùb_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = sònraich_stòras(1, 사용수); if (!Mearachd) for (int lùb_INDEX = 0; lùb_INDEX < 사용수; lùb_INDEX++) 힙[반환값 + 2 + lùb_INDEX] = 화면글임시[lùb_INDEX]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 eitean_VALUE 화면 기능에 연결한다. Swing nì_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int sealbhadair, int ainm_cunbhalachan, int 서술상수, int àithne_CODE) {
        if (Word_SMS(sealbhadair, "한국어/자체/tachartas_ciutha")) {
            if (àithne_CODE == 184 && Word_SMS(ainm_cunbhalachan, "나중에실행") && Word_SMS(서술상수, "(L한국어/자체/실행할일;)V")) {
                int saothair_gnìomh = 빼기(2); if (!객체유효(saothair_gnìomh)) return;
                if (나중수 == 8) { fàilligeadh_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = saothair_gnìomh; return;
            }
            if (àithne_CODE == 184 && Word_SMS(ainm_cunbhalachan, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            fàilligeadh_VALUE("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (Word_SMS(sealbhadair, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!nì_VALUE(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Word_SMS(ainm_cunbhalachan, "tachartas_tùs") && Word_SMS(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Word_SMS(ainm_cunbhalachan, "àithne_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Word_SMS(ainm_cunbhalachan, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else fàilligeadh_VALUE("지원하지 않는 한국어 Gnìomh 알림 호출"); return;
        }
        if (àithne_CODE == 183 && Word_SMS(ainm_cunbhalachan, "<init>")) {
            int 종류 = 한국어화면종(sealbhadair), 받이 = 0, 가로 = 0, inghearach_suidhich = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (cleachdaiche.화면너비() - 폭) / 2; inghearach_suidhich = (cleachdaiche.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); inghearach_suidhich = 빼기(1); 가로 = 빼기(1);
            } else { fàilligeadh_VALUE("지원하지 않는 한국어 화면 생성자"); return; }
            int SMS = 빼기(2), eileamaid_VALUE = 빼기(2); if (!화면객체(eileamaid_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || inghearach_suidhich < 0 || 폭 > cleachdaiche.화면너비() - 가로 || 높이 > cleachdaiche.화면높이() - inghearach_suidhich) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = cleachdaiche.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { fàilligeadh_VALUE("화면 eileamaid_VALUE 자리가 가득 찼습니다"); return; }
            힙[eileamaid_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = eileamaid_VALUE;
            힙[eileamaid_VALUE + 5] = 가로; 힙[eileamaid_VALUE + 6] = inghearach_suidhich; 힙[eileamaid_VALUE + 7] = 폭; 힙[eileamaid_VALUE + 8] = 높이; 힙[eileamaid_VALUE + 10] = 2;
            힙[eileamaid_VALUE + 4] = 받이; 힙참조[eileamaid_VALUE + 4] = 1; 힙[eileamaid_VALUE + 12] = 1;
            cleachdaiche.화면연결(1, INDEX, 가로, inghearach_suidhich, 폭, 높이);
            if (종류 == 24) cleachdaiche.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(eileamaid_VALUE, SMS); return;
        }
        if (àithne_CODE != 182) { fàilligeadh_VALUE("잘못된 한국어 화면 호출 àithne"); return; }
        if (Word_SMS(ainm_cunbhalachan, "sgrìobh_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int SMS = 빼기(2), eileamaid_VALUE = 빼기(2); if (화면객체(eileamaid_VALUE)) 화면문자설정(eileamaid_VALUE, SMS); return;
        }
        if (Word_SMS(ainm_cunbhalachan, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int eileamaid_VALUE = 빼기(2); if (화면객체(eileamaid_VALUE)) 넣기(화면문자읽기(eileamaid_VALUE), 2); return;
        }
        if (Word_SMS(ainm_cunbhalachan, "동작맡기기") && Word_SMS(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), eileamaid_VALUE = 빼기(2);
            if (화면객체(eileamaid_VALUE)) { 힙[eileamaid_VALUE + 4] = 받이; 힙참조[eileamaid_VALUE + 4] = 1; 힙[eileamaid_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(ainm_cunbhalachan, "cuir_ris_eileamaid") && Word_SMS(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int duine_cloinne_VALUE = 빼기(2), 부모 = 빼기(2); if (!화면객체(duine_cloinne_VALUE) || !화면객체(부모)) return;
            if (cleachdaiche.화면연결(2, 힙[부모 + 2], 힙[duine_cloinne_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[duine_cloinne_VALUE + 11] = 부모; 힙참조[duine_cloinne_VALUE + 11] = 1; return;
        }
        if (Word_SMS(ainm_cunbhalachan, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), inghearach_suidhich = 빼기(1), 가로 = 빼기(1), eileamaid_VALUE = 빼기(2); if (!화면객체(eileamaid_VALUE)) return;
            if (cleachdaiche.화면연결(1, 힙[eileamaid_VALUE + 2], 가로, inghearach_suidhich, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[eileamaid_VALUE + 5] = 가로; 힙[eileamaid_VALUE + 6] = inghearach_suidhich; 힙[eileamaid_VALUE + 7] = 폭; 힙[eileamaid_VALUE + 8] = 높이; return;
        }
        if ((Word_SMS(ainm_cunbhalachan, "show_uinneag") || Word_SMS(ainm_cunbhalachan, "dùin")) && Word_SMS(서술상수, "()V")) {
            boolean follaiseachd_VALUE = Word_SMS(ainm_cunbhalachan, "show_uinneag"); int eileamaid_VALUE = 빼기(2); if (!화면객체(eileamaid_VALUE)) return;
            if (cleachdaiche.화면연결(follaiseachd_VALUE ? 3 : 4, 힙[eileamaid_VALUE + 2], follaiseachd_VALUE ? 1 : 0, 0, 0, 0) < 0) { fàilligeadh_VALUE("화면은 eadar_ghnìomhach 명령에서 실행해야 합니다"); return; }
            힙[eileamaid_VALUE + 9] = follaiseachd_VALUE ? 1 : 0; return;
        }
        if (Word_SMS(ainm_cunbhalachan, "보이는가") && Word_SMS(서술상수, "()Z")) { int eileamaid_VALUE = 빼기(2); if (화면객체(eileamaid_VALUE)) 넣기(힙[eileamaid_VALUE + 9], 1); return; }
        fàilligeadh_VALUE("지원하지 않는 한국어 화면 dòigh_VALUE");
    }
    static void 화면호출(int sealbhadair, int ainm_cunbhalachan, int 서술상수, int àithne_CODE) {
        if (Word_SMS(sealbhadair, "javax/swing/SwingUtilities")) {
            if (àithne_CODE == 184 && Word_SMS(ainm_cunbhalachan, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int nì_fiosrachadh = 빼기(2); if (!객체유효(nì_fiosrachadh)) return; if (나중수 == 8) { fàilligeadh_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = nì_fiosrachadh; return; }
            if (àithne_CODE == 184 && Word_SMS(ainm_cunbhalachan, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            fàilligeadh_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(sealbhadair, "java/awt/event/ActionEvent")) {
            int nì_fiosrachadh = 빼기(2); if (!nì_VALUE(nì_fiosrachadh, 29)) return;
            if (Word_SMS(ainm_cunbhalachan, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[nì_fiosrachadh + 2], 2);
            else if (Word_SMS(ainm_cunbhalachan, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[nì_fiosrachadh + 2]), 2);
            else if (Word_SMS(ainm_cunbhalachan, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else fàilligeadh_VALUE("unsupported ActionEvent method"); return;
        }
        if (àithne_CODE == 183 && Word_SMS(ainm_cunbhalachan, "<init>")) {
            int COLUMNS = 0, SMS_fiosrachadh = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_fiosrachadh = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_fiosrachadh = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { fàilligeadh_VALUE("unsupported Swing constructor"); return; }
            int nì_fiosrachadh = 빼기(2); if (!객체유효(nì_fiosrachadh)) return;
            if (힙[nì_fiosrachadh] == 30) { fàilligeadh_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(nì_fiosrachadh) || COLUMNS < 0) return;
            int cunntas_VALUE = cleachdaiche.화면연결(0, 힙[nì_fiosrachadh] - 23, 0, 0, 0, 0);
            if (cunntas_VALUE < 1 || cunntas_VALUE > 32) { fàilligeadh_VALUE("GUI widget slots exhausted"); return; }
            힙[nì_fiosrachadh + 2] = cunntas_VALUE; 화면참조[cunntas_VALUE - 1] = nì_fiosrachadh; 힙[nì_fiosrachadh + 5] = 힙[nì_fiosrachadh] == 24 ? 130 : 16; 힙[nì_fiosrachadh + 6] = 힙[nì_fiosrachadh] == 24 ? 110 : 16;
            힙[nì_fiosrachadh + 7] = 힙[nì_fiosrachadh] == 24 ? 380 : 220; 힙[nì_fiosrachadh + 8] = 힙[nì_fiosrachadh] == 24 ? 240 : 28; 힙[nì_fiosrachadh + 10] = 1;
            화면문자설정(nì_fiosrachadh, SMS_fiosrachadh); return;
        }
        if (Word_SMS(ainm_cunbhalachan, "setText") || Word_SMS(ainm_cunbhalachan, "setTitle")) { int SMS_fiosrachadh = 빼기(2), nì_fiosrachadh = 빼기(2); if (화면객체(nì_fiosrachadh) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(nì_fiosrachadh, SMS_fiosrachadh); return; }
        if (Word_SMS(ainm_cunbhalachan, "getText") || Word_SMS(ainm_cunbhalachan, "getTitle")) { int nì_fiosrachadh = 빼기(2); if (화면객체(nì_fiosrachadh) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(nì_fiosrachadh), 2); return; }
        if (Word_SMS(ainm_cunbhalachan, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), nì_fiosrachadh = 빼기(2); if (화면객체(nì_fiosrachadh)) { 힙[nì_fiosrachadh + 4] = 수신참조; 힙참조[nì_fiosrachadh + 4] = 1; } return; }
        if (Word_SMS(ainm_cunbhalachan, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int nì_fiosrachadh = 빼기(2); if (화면객체(nì_fiosrachadh)) 넣기(nì_fiosrachadh, 2); return; }
        if (Word_SMS(ainm_cunbhalachan, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int co_dhealbhachd_fiosrachadh = 빼기(2), nì_fiosrachadh = 빼기(2); if (화면객체(nì_fiosrachadh) && co_dhealbhachd_fiosrachadh != 0) fàilligeadh_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(ainm_cunbhalachan, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean co_dhealbhachd_cumha = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (co_dhealbhachd_cumha) 빼기(2);
            int duine_cloinne_fiosrachadh = 빼기(2), nì_fiosrachadh = 빼기(2); if (!화면객체(duine_cloinne_fiosrachadh) || !화면객체(nì_fiosrachadh)) return;
            if (cleachdaiche.화면연결(2, 힙[nì_fiosrachadh + 2], 힙[duine_cloinne_fiosrachadh + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[duine_cloinne_fiosrachadh + 11] = nì_fiosrachadh; 힙참조[duine_cloinne_fiosrachadh + 11] = 1; if (!co_dhealbhachd_cumha) 넣기(duine_cloinne_fiosrachadh, 2); return;
        }
        if (Word_SMS(ainm_cunbhalachan, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), co_chomharra_x = 빼기(1), nì_fiosrachadh = 빼기(2); if (!화면객체(nì_fiosrachadh)) return;
            if (cleachdaiche.화면연결(1, 힙[nì_fiosrachadh + 2], co_chomharra_x, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[nì_fiosrachadh + 5] = co_chomharra_x; 힙[nì_fiosrachadh + 6] = 세로좌표; 힙[nì_fiosrachadh + 7] = 너비; 힙[nì_fiosrachadh + 8] = 높이; return;
        }
        if (Word_SMS(ainm_cunbhalachan, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), nì_fiosrachadh = 빼기(2); if (!화면객체(nì_fiosrachadh)) return;
            if (cleachdaiche.화면연결(1, 힙[nì_fiosrachadh + 2], 힙[nì_fiosrachadh + 5], 힙[nì_fiosrachadh + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[nì_fiosrachadh + 7] = 너비; 힙[nì_fiosrachadh + 8] = 높이; } return;
        }
        if (Word_SMS(ainm_cunbhalachan, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), nì_fiosrachadh = 빼기(2); if (!화면객체(nì_fiosrachadh)) return; if (상대배치 != 0) { fàilligeadh_VALUE("only screen centering supported"); return; } 힙[nì_fiosrachadh + 5] = (cleachdaiche.화면너비() - 힙[nì_fiosrachadh + 7]) / 2; 힙[nì_fiosrachadh + 6] = (cleachdaiche.화면높이() - 힙[nì_fiosrachadh + 8]) / 2; cleachdaiche.화면연결(1, 힙[nì_fiosrachadh + 2], 힙[nì_fiosrachadh + 5], 힙[nì_fiosrachadh + 6], 힙[nì_fiosrachadh + 7], 힙[nì_fiosrachadh + 8]); return; }
        if (Word_SMS(ainm_cunbhalachan, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int poileasaidh = 빼기(1), nì_fiosrachadh = 빼기(2); if (화면객체(nì_fiosrachadh)) { if (poileasaidh < 0 || poileasaidh > 3) 예외던짐(9, "close policy"); else { 힙[nì_fiosrachadh + 10] = poileasaidh; cleachdaiche.화면연결(7, 힙[nì_fiosrachadh + 2], poileasaidh, 0, 0, 0); } } return; }
        if (Word_SMS(ainm_cunbhalachan, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int dàta_VALUE = 빼기(1), nì_fiosrachadh = 빼기(2); if (화면객체(nì_fiosrachadh)) { int 처리값 = cleachdaiche.화면연결(3, 힙[nì_fiosrachadh + 2], dàta_VALUE, 0, 0, 0); if (처리값 < 0) fàilligeadh_VALUE("Swing requires a standalone interactive command"); else 힙[nì_fiosrachadh + 9] = dàta_VALUE; } return; }
        if (Word_SMS(ainm_cunbhalachan, "dispose") && Word_SMS(서술상수, "()V")) { int nì_fiosrachadh = 빼기(2); if (화면객체(nì_fiosrachadh)) { cleachdaiche.화면연결(4, 힙[nì_fiosrachadh + 2], 0, 0, 0, 0); 힙[nì_fiosrachadh + 9] = 0; } return; }
        if (Word_SMS(ainm_cunbhalachan, "repaint") || Word_SMS(ainm_cunbhalachan, "validate")) { int nì_fiosrachadh = 빼기(2); if (!화면객체(nì_fiosrachadh) || !Word_SMS(서술상수, "()V")) return; cleachdaiche.화면연결(1, 힙[nì_fiosrachadh + 2], 힙[nì_fiosrachadh + 5], 힙[nì_fiosrachadh + 6], 힙[nì_fiosrachadh + 7], 힙[nì_fiosrachadh + 8]); return; }
        if (Word_SMS(ainm_cunbhalachan, "isVisible") && Word_SMS(서술상수, "()Z")) { int nì_fiosrachadh = 빼기(2); if (화면객체(nì_fiosrachadh)) 넣기(힙[nì_fiosrachadh + 9], 1); return; }
        fàilligeadh_VALUE("unsupported Swing method (native subset)");
    }
    static void 사건실행(int targaid_ADDRESS, int 사건번호, boolean 한국어) {
        if (targaid_ADDRESS < 1 || 힙[targaid_ADDRESS] < 32) { fàilligeadh_VALUE("Java event listener required"); return; }
        int faidhle_INDEX = ainm_dòigh(힙[targaid_ADDRESS] - 32, 사건번호 == 0 ? (한국어 ? "Ruith" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (faidhle_INDEX < 0) { fàilligeadh_VALUE("event callback missing"); return; }
        현재가닥 = 0; snàithlean_COUNT = 1; frèam_INDEX = 0; snàithlean_cor[0] = 1; frèam_stac[0] = 0; 틀잠금[0] = ro_shuidhich_frèam[0] = 0; 바꿈요청 = false;
        for (int lùb_INDEX = 0; lùb_INDEX < 128; lùb_INDEX++) { ionadail_VALUE[lùb_INDEX] = ionadail_TYPE[lùb_INDEX] = 0; }
        frèam_dòigh[0] = faidhle_INDEX; frèam_suidhich[0] = dòigh_Start[faidhle_INDEX]; ionadail_VALUE[0] = targaid_ADDRESS; ionadail_TYPE[0] = 2;
        if (사건번호 != 0) { ionadail_VALUE[1] = 사건번호; ionadail_TYPE[1] = 2; }
        사건중 = true; gnìomhaich_àithne(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!Mearachd) {
            if (나중수 > 0) { int targaid_ADDRESS = 나중실행[0], 한국어 = 나중한국어[0]; for (int lùb_INDEX = 1; lùb_INDEX < 나중수; lùb_INDEX++) { 나중실행[lùb_INDEX - 1] = 나중실행[lùb_INDEX]; 나중한국어[lùb_INDEX - 1] = 나중한국어[lùb_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(targaid_ADDRESS, 0, 한국어 != 0); continue; }
            if (cleachdaiche.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = cleachdaiche.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { fàilligeadh_VALUE("GUI event I/O failed"); return; }
            int cunntas_VALUE = 사건번호 & 65535; if (cunntas_VALUE < 1 || cunntas_VALUE > 32) continue; int nì_fiosrachadh = 화면참조[cunntas_VALUE - 1]; if (nì_fiosrachadh == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[nì_fiosrachadh + 10] != 0) 힙[nì_fiosrachadh + 9] = 0;
                if (힙[nì_fiosrachadh + 10] == 3) for (int lùb_INDEX = 0; lùb_INDEX < 32; lùb_INDEX++) if (화면참조[lùb_INDEX] != 0 && 힙[화면참조[lùb_INDEX]] == 24) cleachdaiche.화면연결(4, lùb_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[nì_fiosrachadh + 4] != 0) {
                int LEUGHMI_fiosrachadh = sònraich_stòras(29, 2); if (Mearachd) return; 힙[LEUGHMI_fiosrachadh + 2] = nì_fiosrachadh; 힙[LEUGHMI_fiosrachadh + 3] = 힙[nì_fiosrachadh + 12]; 힙참조[LEUGHMI_fiosrachadh + 2] = 1; 사건실행(힙[nì_fiosrachadh + 4], LEUGHMI_fiosrachadh, 힙[nì_fiosrachadh + 12] != 0);
            }
        }
    }
    public static int ruith() {
        if (cleachdaiche.인수개수() == 1 && 자바도구.같음(cleachdaiche.인수(0), "-version")) {
            cleachdaiche.sgrìobh("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (cleachdaiche.인수개수() < 1) { cleachdaiche.sgrìobh("Usage: java CLASS [ARGS]\n"); return 2; }
        cur_a_steach_clas_deifinisean = luchd_clas_deifinisean(òstair_caractar(cleachdaiche.인수(0))); if (Mearachd || cur_a_steach_clas_deifinisean < 0) return 1;
        int cur_a_steach_puing_VALUE = ainm_dòigh(cur_a_steach_clas_deifinisean, "ruith", "()V");
        boolean 한국어진입 = cur_a_steach_puing_VALUE >= 0 && (dòigh_inntrigeadh[cur_a_steach_puing_VALUE] & 9) == 9;
        if (!한국어진입) cur_a_steach_puing_VALUE = ainm_dòigh(cur_a_steach_clas_deifinisean, "main", "([Ljava/lang/String;)V");
        if (cur_a_steach_puing_VALUE < 0 || (dòigh_inntrigeadh[cur_a_steach_puing_VALUE] & 9) != 9) fàilligeadh_VALUE("public static void ruith() or main(String[] args) required");
        if (Mearachd) return 1;
        int 인수 = sònraich_stòras(3, cleachdaiche.인수개수() - 1); ARRAY_eileamaid[인수] = -1;
        for (int 수 = 1; 수 < cleachdaiche.인수개수() && !Mearachd; 수++) 힙[인수 + 1 + 수] = òstair_caractar(cleachdaiche.인수(수));
        frèam_INDEX = 0; frèam_dòigh[0] = cur_a_steach_puing_VALUE; frèam_suidhich[0] = dòigh_Start[cur_a_steach_puing_VALUE]; ionadail_VALUE[0] = 한국어진입 ? 0 : 인수; ionadail_TYPE[0] = 한국어진입 ? 0 : 2;
        snàithlean_cor[0] = 1; snàithlean_nì[0] = sònraich_stòras(13, 2);
        gnìomhaich_àithne(); if (!Mearachd) 화면사건들(); return Mearachd ? 1 : 0;
    }
}
