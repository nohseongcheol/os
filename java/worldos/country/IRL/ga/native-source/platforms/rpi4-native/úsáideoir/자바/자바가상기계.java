// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Comhad/스택/Leabhair_thagartha/craobh 경계를 Rith_ordú 중 검사한다. */
public final class 자바가상기계 {
    static int[] Comhad = new int[16 * 16384], 임시파일 = new int[16384], comhad_ainm_SMS = new int[512];
    static int[] tairiseach_clib = new int[8192], 상가 = new int[8192], tairiseach_SECOND_VALUE = new int[8192], teaghrán_Leabhair_thagartha = new int[8192];
    static int[] modh_ainm_SMS = new int[512], modh_TYPE = new int[512], modh_rochtain = new int[512], modh_úinéir = new int[512];
    static int[] modh_Start = new int[512], modh_cuir_deireadh_le = new int[512], modh_Cruach = new int[512], 함수지역 = new int[512];
    static int[] modh_argóint_COUNT = new int[512], modh_argóint_TYPE = new int[8192], modh_return = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] logánta_VALUE = new int[16384], logánta_TYPE = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] fráma_modh = new int[128], fráma_suíomh = new int[128], fráma_Cruach = new int[128], fráma_treoir = new int[128], túsaigh_fráma = new int[128];
    static int[] aicme_Sainmhíniú_ainm = new int[16], aicme_Sainmhíniú_socraigh_méid = new int[16], 종부모 = new int[16], aicme_Sainmhíniú_staid = new int[16], aicme_spás_COUNT = new int[16], túsaigh_aicme_Sainmhíniú = new int[16];
    static int[] aicme_comhéadan = new int[16 * 16], aicme_comhéadan_COUNT = new int[16];
    static int[] spás_ainm = new int[512], spás_TYPE = new int[512], spás_úinéir = new int[512], spás_ceadanna_rochtana = new int[512], spás_suíomh = new int[512], spás_sonraí = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], ARRAY_eilimint = new int[32768], Store_slánuimhir = new int[256];
    static int Méid, 읽기위치, modh_COUNT, aicme_ainm, fráma_INDEX = -1, 힙끝 = 1, return_TYPE;
    static int aicme_Sainmhíniú_COUNT, spás_COUNT, 잡기수, 현재읽는종, 던진객체, 잠시수, taispeáin_COUNT, Bailiúchán_COUNT;
    static int 현재가닥, snáithe_COUNT = 1, iontráil_aicme_Sainmhíniú;
    static int[] snáithe_fráma = new int[4], snáithe_staid = new int[4], snáithe_oibiacht = new int[4], snáithe_sprioc = new int[4], 가닥대기 = new int[4];
    static boolean ERREÁID, athraigh_iarratas_HTTP;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], aicme_snáithe = new int[16];

    static void teip_VALUE(String Word_SMS) {
        if (ERREÁID) return;
        int catagóir_CODE = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) catagóir_CODE = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) catagóir_CODE = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) catagóir_CODE = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) catagóir_CODE = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) catagóir_CODE = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) catagóir_CODE = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) catagóir_CODE = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) catagóir_CODE = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) catagóir_CODE = 15;
        if (catagóir_CODE != 0 && fráma_INDEX >= 0) { 예외던짐(catagóir_CODE, Word_SMS); return; }
        úsáideoir.Scríobh("JVM error: "); úsáideoir.Scríobh(Word_SMS); úsáideoir.scríobh_carachtar_VALUE(10); ERREÁID = true;
    }
    static boolean gearrthóg(int Rith_2, int fad_VALUE) {
        if (Rith_2 < 0 || Rith_2 >= Comhad.length || fad_VALUE < 0) return false;
        int aicme_Sainmhíniú = Rith_2 / 16384;
        return Rith_2 % 16384 <= aicme_Sainmhíniú_socraigh_méid[aicme_Sainmhíniú] && fad_VALUE <= aicme_Sainmhíniú_socraigh_méid[aicme_Sainmhíniú] - Rith_2 % 16384;
    }
    static int beart_VALUE() {
        if (!gearrthóg(읽기위치, 1)) { teip_VALUE("truncated class file"); return 0; }
        return Comhad[읽기위치++];
    }
    static int 짧은수() { return beart_VALUE() << 8 | beart_VALUE(); }
    static int slánuimhir() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int fad_VALUE) { if (!gearrthóg(읽기위치, fad_VALUE)) teip_VALUE("invalid attribute size"); else 읽기위치 += fad_VALUE; }
    static boolean seic_tairiseach(int 수, int 종류) {
        if (수 <= 0 || 수 >= tairiseach_clib.length || tairiseach_clib[수] != 종류) { teip_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Rith_2, int fad_VALUE, String Word_SMS) {
        if (!gearrthóg(Rith_2, fad_VALUE)) return false;
        int 읽는자리 = Rith_2, 끝 = Rith_2 + fad_VALUE;
        for (int lúb_INDEX = 0; lúb_INDEX < Word_SMS.length(); lúb_INDEX++) {
            int pointe_cóid = Word_SMS.charAt(lúb_INDEX);
            if (pointe_cóid > 0 && pointe_cóid < 128) { if (읽는자리 >= 끝 || Comhad[읽는자리++] != pointe_cóid) return false; }
            else if (pointe_cóid < 2048) {
                if (읽는자리 + 2 > 끝 || Comhad[읽는자리++] != (192 | (pointe_cóid >> 6)) || Comhad[읽는자리++] != (128 | (pointe_cóid & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Comhad[읽는자리++] != (224 | (pointe_cóid >> 12)) || Comhad[읽는자리++] != (128 | ((pointe_cóid >> 6) & 63)) || Comhad[읽는자리++] != (128 | (pointe_cóid & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Word_SMS(int tairiseach_VALUE, String Word_SMS) { return seic_tairiseach(tairiseach_VALUE, 1) && 구간(상가[tairiseach_VALUE], tairiseach_SECOND_VALUE[tairiseach_VALUE], Word_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!seic_tairiseach(가, 1) || !seic_tairiseach(나, 1) || tairiseach_SECOND_VALUE[가] != tairiseach_SECOND_VALUE[나]) return false;
        for (int 수 = 0; 수 < tairiseach_SECOND_VALUE[가]; 수++) if (Comhad[상가[가] + 수] != Comhad[상가[나] + 수]) return false;
        return true;
    }
    static int aicme_ainm_SMS(int 수) { return seic_tairiseach(수, 7) && seic_tairiseach(상가[수], 1) ? 상가[수] : 0; }
    static int Leabhair_thagartha_ainm(int 수) { return seic_tairiseach(수, 12) && seic_tairiseach(상가[수], 1) ? 상가[수] : 0; }
    static int Leabhair_thagartha_TYPE(int 수) { return seic_tairiseach(수, 12) && seic_tairiseach(tairiseach_SECOND_VALUE[수], 1) ? tairiseach_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean folamh_TYPE) {
        if (읽기위치 >= 끝) { teip_VALUE("invalid descriptor"); return 0; }
        int VALUE = beart_VALUE();
        if (VALUE == 'V' && folamh_TYPE) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Rith_2 = 읽기위치;
            while (읽기위치 < 끝 && Comhad[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Rith_2) teip_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        teip_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int feidhm_VALUE) {
        int 이전 = 읽기위치, 수 = modh_TYPE[feidhm_VALUE];
        if (!seic_tairiseach(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + tairiseach_SECOND_VALUE[수];
        if (beart_VALUE() != '(') teip_VALUE("invalid method descriptor");
        int mír_COUNT = 0;
        while (!ERREÁID && 읽기위치 < 끝 && Comhad[읽기위치] != ')') {
            if (mír_COUNT == 16) { teip_VALUE("too many method arguments"); break; }
            modh_argóint_TYPE[feidhm_VALUE * 16 + mír_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || beart_VALUE() != ')') teip_VALUE("invalid method descriptor");
        modh_return[feidhm_VALUE] = 서술형(끝, true); modh_argóint_COUNT[feidhm_VALUE] = mír_COUNT;
        if (읽기위치 != 끝) teip_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return modh_úinéir[fráma_modh[fráma_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int mír_COUNT = 짧은수();
        for (int 수 = 0; 수 < mír_COUNT && !ERREÁID; 수++) { seic_tairiseach(상번호(), 1); 건너(slánuimhir()); }
    }
    static int ordú_fad(int VALUE) {
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
    static int suíomh_slánuimhir(int 읽는자리) {
        if (!gearrthóg(읽는자리, 4)) { teip_VALUE("truncated bytecode operand"); return 0; }
        return Comhad[읽는자리] << 24 | Comhad[읽는자리 + 1] << 16 | Comhad[읽는자리 + 2] << 8 | Comhad[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Rith_2, int 끝) {
        int VALUE = Comhad[읽는자리], fad_VALUE = ordú_fad(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_suíomh = 읽는자리 + 1;
            while ((BASE_suíomh - Rith_2) % 4 != 0) BASE_suíomh++;
            if (끝 - BASE_suíomh < (VALUE == 170 ? 12 : 8)) return 0;
            int iontráil_COUNT = VALUE == 170 ? suíomh_slánuimhir(BASE_suíomh + 8) - suíomh_slánuimhir(BASE_suíomh + 4) + 1 : suíomh_slánuimhir(BASE_suíomh + 4);
            if (iontráil_COUNT < 0 || iontráil_COUNT > 2048) return 0;
            fad_VALUE = BASE_suíomh - 읽는자리 + (VALUE == 170 ? 12 + 4 * iontráil_COUNT : 8 + 8 * iontráil_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_sonraí = Comhad[읽는자리 + 1]; fad_VALUE = Word_sonraí == 132 ? 6 : (Word_sonraí == 21 || Word_sonraí == 25 || Word_sonraí == 54 || Word_sonraí == 58) ? 4 : 0;
        }
        return fad_VALUE > 0 && fad_VALUE <= 끝 - 읽는자리 ? fad_VALUE : 0;
    }
    static void seic_sprioc_VALUE(int sprioc_VALUE, int feidhm_VALUE) {
        if (sprioc_VALUE < modh_Start[feidhm_VALUE] || sprioc_VALUE >= modh_cuir_deireadh_le[feidhm_VALUE] || 경계[sprioc_VALUE] != feidhm_VALUE + 1) teip_VALUE("invalid branch target");
    }
    static void 클래스읽기(int aicme_Sainmhíniú) {
        현재읽는종 = aicme_Sainmhíniú; 읽기위치 = aicme_Sainmhíniú * 16384; Méid = 읽기위치 + aicme_Sainmhíniú_socraigh_méid[aicme_Sainmhíniú];
        if (slánuimhir() != 0xcafebabe) { teip_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), leagan_VALUE = 짧은수();
        if (leagan_VALUE < 45 || leagan_VALUE > 52 || 부판 != 0) { teip_VALUE("supported class versions: 45..52, minor 0"); return; }
        int tairiseach_COUNT = 짧은수(), BASE_suíomh = aicme_Sainmhíniú * 512;
        if (tairiseach_COUNT < 1 || tairiseach_COUNT > 512) { teip_VALUE("constant pool limit (511)"); return; }
        for (int iontráil_COUNT = 1; iontráil_COUNT < tairiseach_COUNT && !ERREÁID; iontráil_COUNT++) {
            int 수 = BASE_suíomh + iontráil_COUNT, 종류 = beart_VALUE(); tairiseach_clib[수] = 종류;
            if (종류 == 1) { tairiseach_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(tairiseach_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = slánuimhir();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); tairiseach_SECOND_VALUE[수] = 상번호(); }
            else teip_VALUE("unsupported constant type");
        }
        int cead_VALUE = 짧은수();
        if ((cead_VALUE & (0x2000 | 0x4000)) != 0) teip_VALUE("annotation/enum class unsupported");
        aicme_Sainmhíniú_ainm[aicme_Sainmhíniú] = aicme_ainm_SMS(상번호());
        종부모[aicme_Sainmhíniú] = aicme_ainm_SMS(상번호());
        int comhéadan_COUNT = 짧은수(); if (comhéadan_COUNT > 16) { teip_VALUE("interface count limit"); return; }
        aicme_comhéadan_COUNT[aicme_Sainmhíniú] = comhéadan_COUNT;
        for (int lúb_INDEX = 0; lúb_INDEX < comhéadan_COUNT; lúb_INDEX++) aicme_comhéadan[aicme_Sainmhíniú * 16 + lúb_INDEX] = aicme_ainm_SMS(상번호());
        int réimse_COUNT = 짧은수();
        if (réimse_COUNT > 512 - spás_COUNT) { teip_VALUE("field count limit (512)"); return; }
        for (int lúb_INDEX = 0; lúb_INDEX < réimse_COUNT && !ERREÁID; lúb_INDEX++) {
            int comhad_INDEX = spás_COUNT++; spás_úinéir[comhad_INDEX] = aicme_Sainmhíniú; spás_ceadanna_rochtana[comhad_INDEX] = 짧은수(); spás_ainm[comhad_INDEX] = 상번호(); spás_TYPE[comhad_INDEX] = 상번호();
            seic_tairiseach(spás_ainm[comhad_INDEX], 1); seic_tairiseach(spás_TYPE[comhad_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[spás_TYPE[comhad_INDEX]]; int catagóir_CODE = 서술형(읽기위치 + tairiseach_SECOND_VALUE[spás_TYPE[comhad_INDEX]], false); 읽기위치 = 보존값;
            if ((spás_ceadanna_rochtana[comhad_INDEX] & 8) == 0) spás_suíomh[comhad_INDEX] = aicme_spás_COUNT[aicme_Sainmhíniú]++;
            int tréith_sonraí = 짧은수();
            for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < tréith_sonraí && !ERREÁID; comhcheangal_istigh_suíomh++) {
                int ainm_tairiseach = 상번호(), 유효길이 = slánuimhir();
                if (Word_SMS(ainm_tairiseach, "ConstantValue") && 유효길이 == 2) {
                    int sonraí_VALUE = 상번호();
                    if (catagóir_CODE == 1 && seic_tairiseach(sonraí_VALUE, 3)) spás_sonraí[comhad_INDEX] = 상가[sonraí_VALUE];
                    else if (catagóir_CODE == 2 && seic_tairiseach(sonraí_VALUE, 8)) spás_sonraí[comhad_INDEX] = tairiseach_SMS(상가[sonraí_VALUE]);
                } else 건너(유효길이);
            }
        }
        int mír_COUNT = 짧은수();
        if (mír_COUNT > 512 - modh_COUNT) { teip_VALUE("method count limit (512)"); return; }
        for (int lúb_INDEX = 0; lúb_INDEX < mír_COUNT && !ERREÁID; lúb_INDEX++) {
            int 수 = modh_COUNT++; modh_úinéir[수] = aicme_Sainmhíniú;
            modh_rochtain[수] = 짧은수(); modh_ainm_SMS[수] = 상번호(); modh_TYPE[수] = 상번호();
            seic_tairiseach(modh_ainm_SMS[수], 1); 서술읽기(수);
            if ((modh_rochtain[수] & 8) == 0) {
                if (modh_argóint_COUNT[수] == 16) { teip_VALUE("too many instance method arguments"); return; }
                for (int 비교자리 = modh_argóint_COUNT[수]; 비교자리 > 0; 비교자리--) modh_argóint_TYPE[수 * 16 + 비교자리] = modh_argóint_TYPE[수 * 16 + 비교자리 - 1];
                modh_argóint_TYPE[수 * 16] = 2; modh_argóint_COUNT[수]++;
            }
            if ((modh_rochtain[수] & 0x100) != 0) teip_VALUE("user native method unsupported");
            if (Word_SMS(modh_ainm_SMS[수], "<clinit>")) túsaigh_aicme_Sainmhíniú[aicme_Sainmhíniú] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (modh_úinéir[앞] == aicme_Sainmhíniú && 같은말(modh_ainm_SMS[앞], modh_ainm_SMS[수]) && 같은말(modh_TYPE[앞], modh_TYPE[수])) teip_VALUE("duplicate method");
            int tréith_COUNT = 짧은수();
            for (int tréith_VALUE = 0; tréith_VALUE < tréith_COUNT && !ERREÁID; tréith_VALUE++) {
                int Ainm = 상번호(), fad_VALUE = slánuimhir(), Rith_2 = 읽기위치;
                if (!gearrthóg(Rith_2, fad_VALUE)) { teip_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Ainm, "Code")) {
                    if (modh_Start[수] != 0) teip_VALUE("duplicate Code attribute");
                    modh_Cruach[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_fad = slánuimhir();
                    if (modh_Cruach[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < modh_argóint_COUNT[수]
                        || CODE_fad < 1 || CODE_fad > 8192) teip_VALUE("method memory limits exceeded");
                    modh_Start[수] = 읽기위치; 건너(CODE_fad); modh_cuir_deireadh_le[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { teip_VALUE("exception table limit"); return; }
                    for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < 잡는수; comhcheangal_istigh_suíomh++) {
                        int earráid_Leabhair_thagartha = 잡기수++; 잡기함수[earráid_Leabhair_thagartha] = 수;
                        잡기시작[earráid_Leabhair_thagartha] = modh_Start[수] + 짧은수(); 잡기끝[earráid_Leabhair_thagartha] = modh_Start[수] + 짧은수();
                        잡기위치[earráid_Leabhair_thagartha] = modh_Start[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[earráid_Leabhair_thagartha] = 부호값 == 0 ? 0 : aicme_ainm_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Rith_2 + fad_VALUE) teip_VALUE("Code attribute size mismatch");
                } else 건너(fad_VALUE);
            }
            if ((modh_rochtain[수] & 0x400) != 0) continue;
            if (modh_Start[수] == 0) teip_VALUE("missing Code attribute");
            int spás_iontráil = modh_Start[수];
            while (spás_iontráil < modh_cuir_deireadh_le[수] && !ERREÁID) {
                int fad_VALUE = 길이읽기(spás_iontráil, modh_Start[수], modh_cuir_deireadh_le[수]);
                if (fad_VALUE == 0) { teip_VALUE("unsupported or truncated bytecode"); break; }
                경계[spás_iontráil] = 수 + 1; spás_iontráil += fad_VALUE;
            }
            spás_iontráil = modh_Start[수];
            while (spás_iontráil < modh_cuir_deireadh_le[수] && !ERREÁID) {
                int VALUE = Comhad[spás_iontráil];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) seic_sprioc_VALUE(spás_iontráil + (short)(Comhad[spás_iontráil + 1] << 8 | Comhad[spás_iontráil + 2]), 수);
                if (VALUE == 200) seic_sprioc_VALUE(spás_iontráil + suíomh_slánuimhir(spás_iontráil + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = spás_iontráil + 1; while ((읽는자리 - modh_Start[수]) % 4 != 0) 읽는자리++;
                    seic_sprioc_VALUE(spás_iontráil + suíomh_slánuimhir(읽는자리), 수);
                    int iontráil_COUNT = VALUE == 170 ? suíomh_slánuimhir(읽는자리 + 8) - suíomh_slánuimhir(읽는자리 + 4) + 1 : suíomh_slánuimhir(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < iontráil_COUNT; comhcheangal_istigh_suíomh++) seic_sprioc_VALUE(spás_iontráil + suíomh_slánuimhir(읽는자리 + comhcheangal_istigh_suíomh * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                spás_iontráil += 길이읽기(spás_iontráil, modh_Start[수], modh_cuir_deireadh_le[수]);
            }
            for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < 잡기수; comhcheangal_istigh_suíomh++) if (잡기함수[comhcheangal_istigh_suíomh] == 수) {
                seic_sprioc_VALUE(잡기시작[comhcheangal_istigh_suíomh], 수); seic_sprioc_VALUE(잡기위치[comhcheangal_istigh_suíomh], 수);
                if (잡기끝[comhcheangal_istigh_suíomh] != modh_cuir_deireadh_le[수]) seic_sprioc_VALUE(잡기끝[comhcheangal_istigh_suíomh], 수);
                if (잡기시작[comhcheangal_istigh_suíomh] >= 잡기끝[comhcheangal_istigh_suíomh]) teip_VALUE("invalid exception range");
            }
        }
        if (!ERREÁID) 속성건너();
        if (읽기위치 != Méid) teip_VALUE("extra class file data");
    }
    static int leithdháil_Stóras(int 종류, int fad_VALUE) { return 새기억(종류, fad_VALUE); }
    static boolean oibiacht_VALUE(int Leabhair_thagartha, int 종류) {
        if (!객체유효(Leabhair_thagartha)) return false;
        if (힙[Leabhair_thagartha] != 종류) { teip_VALUE("object type mismatch"); return false; }
        return true;
    }
    static int tairiseach_SMS(int INDEX) {
        if (!seic_tairiseach(INDEX, 1)) return 0;
        if (teaghrán_Leabhair_thagartha[INDEX] != 0) return teaghrán_Leabhair_thagartha[INDEX];
        int Leabhair_thagartha = leithdháil_Stóras(1, tairiseach_SECOND_VALUE[INDEX]); if (ERREÁID) return 0;
        int 끝 = 상가[INDEX] + tairiseach_SECOND_VALUE[INDEX], 수 = 상가[INDEX], fad_VALUE = 0;
        while (수 < 끝 && !ERREÁID) {
            int VALUE = Comhad[수++];
            if (VALUE == 0) teip_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Ar_aghaidh_mír = Comhad[수++];
                if ((Ar_aghaidh_mír & 192) != 128) teip_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Ar_aghaidh_mír & 63;
                if (VALUE != 0 && VALUE < 128) teip_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = Comhad[수++], 나 = Comhad[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) teip_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (VALUE < 2048) teip_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) teip_VALUE("invalid modified UTF-8");
            힙[Leabhair_thagartha + 2 + fad_VALUE++] = VALUE;
        }
        힙[Leabhair_thagartha + 1] = fad_VALUE; teaghrán_Leabhair_thagartha[INDEX] = Leabhair_thagartha; return Leabhair_thagartha;
    }
    static int óstach_carachtar(String VALUE) {
        int Leabhair_thagartha = leithdháil_Stóras(1, VALUE.length()); if (ERREÁID) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) 힙[Leabhair_thagartha + 2 + 수] = VALUE.charAt(수);
        return Leabhair_thagartha;
    }
    static void scríobh_SMS(int Leabhair_thagartha) {
        if (Leabhair_thagartha == 0) { úsáideoir.Scríobh("null"); return; }
        if (!oibiacht_VALUE(Leabhair_thagartha, 1)) return;
        for (int 수 = 0; 수 < 힙[Leabhair_thagartha + 1]; 수++) úsáideoir.scríobh_carachtar_VALUE(힙[Leabhair_thagartha + 2 + 수]);
    }
    static int digit_carachtar(int VALUE) {
        int Leabhair_thagartha = leithdháil_Stóras(1, 11); if (ERREÁID) return 0;
        int fad_VALUE = 0;
        if (VALUE < 0) 힙[Leabhair_thagartha + 2 + fad_VALUE++] = '-'; else VALUE = -VALUE;
        int suíomh_INDEX = 1000000000; boolean Rith_2 = false;
        while (suíomh_INDEX != 0) {
            int 수 = -(VALUE / suíomh_INDEX);
            if (수 != 0 || Rith_2 || suíomh_INDEX == 1) { 힙[Leabhair_thagartha + 2 + fad_VALUE++] = '0' + 수; Rith_2 = true; }
            VALUE %= suíomh_INDEX; suíomh_INDEX /= 10;
        }
        힙[Leabhair_thagartha + 1] = fad_VALUE; return Leabhair_thagartha;
    }
    static int 정수해독(int Leabhair_thagartha) {
        if (!oibiacht_VALUE(Leabhair_thagartha, 1)) return 0;
        int fad_VALUE = 힙[Leabhair_thagartha + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (fad_VALUE > 0 && (힙[Leabhair_thagartha + 2] == '-' || 힙[Leabhair_thagartha + 2] == '+')) { 음수 = 힙[Leabhair_thagartha + 2] == '-'; 수++; }
        if (수 == fad_VALUE) teip_VALUE("NumberFormatException");
        for (; 수 < fad_VALUE && !ERREÁID; 수++) {
            int digit_VALUE = 힙[Leabhair_thagartha + 2 + 수] - '0';
            if (digit_VALUE < 0 || digit_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && digit_VALUE > (음수 ? 8 : 7)) teip_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - digit_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (ERREÁID) return;
        if (fráma_INDEX < 0 || fráma_Cruach[fráma_INDEX] >= modh_Cruach[fráma_modh[fráma_INDEX]]) { teip_VALUE("operand stack overflow"); return; }
        int spás_iontráil = fráma_INDEX * 128 + fráma_Cruach[fráma_INDEX]++; 스택값[spás_iontráil] = VALUE; 스택형[spás_iontráil] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (ERREÁID) return 0;
        if (fráma_INDEX < 0 || fráma_Cruach[fráma_INDEX] < 1) { teip_VALUE("operand stack underflow"); return 0; }
        int spás_iontráil = fráma_INDEX * 128 + --fráma_Cruach[fráma_INDEX]; return_TYPE = 스택형[spás_iontráil];
        if (TYPE_VALUE != 0 && return_TYPE != TYPE_VALUE) teip_VALUE("operand type mismatch");
        if (return_TYPE == 2) cosain_VALUE(스택값[spás_iontráil]);
        return 스택값[spás_iontráil];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[fráma_modh[fráma_INDEX]] || INDEX < 0 || logánta_TYPE[fráma_INDEX * 128 + INDEX] != TYPE_VALUE) { teip_VALUE("invalid or uninitialized local"); return; }
        넣기(logánta_VALUE[fráma_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void scríobh_logánta(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[fráma_modh[fráma_INDEX]] || INDEX < 0) { teip_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); logánta_VALUE[fráma_INDEX * 128 + INDEX] = VALUE; logánta_TYPE[fráma_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int suíomh = fráma_suíomh[fráma_INDEX];
        if (suíomh < modh_Start[fráma_modh[fráma_INDEX]] || suíomh >= modh_cuir_deireadh_le[fráma_modh[fráma_INDEX]]) { teip_VALUE("instruction pointer out of range"); return 0; }
        fráma_suíomh[fráma_INDEX]++; return Comhad[suíomh];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void bog_VALUE(int suíomh) {
        int feidhm_VALUE = fráma_modh[fráma_INDEX];
        if (suíomh < modh_Start[feidhm_VALUE] || suíomh >= modh_cuir_deireadh_le[feidhm_VALUE] || 경계[suíomh] != feidhm_VALUE + 1) teip_VALUE("invalid branch target");
        else fráma_suíomh[fráma_INDEX] = suíomh;
    }
    static void 호출(int feidhm_VALUE) {
        if (fráma_INDEX % 32 == 31) { teip_VALUE("call stack limit (32)"); return; }
        int Ar_aghaidh_mír = fráma_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) logánta_TYPE[Ar_aghaidh_mír * 128 + 수] = 0;
        for (int 수 = modh_argóint_COUNT[feidhm_VALUE] - 1; 수 >= 0; 수--) {
            logánta_VALUE[Ar_aghaidh_mír * 128 + 수] = 빼기(modh_argóint_TYPE[feidhm_VALUE * 16 + 수]); logánta_TYPE[Ar_aghaidh_mír * 128 + 수] = modh_argóint_TYPE[feidhm_VALUE * 16 + 수];
        }
        if (ERREÁID) return;
        fráma_INDEX = Ar_aghaidh_mír; túsaigh_fráma[fráma_INDEX] = 0; fráma_modh[fráma_INDEX] = feidhm_VALUE; fráma_suíomh[fráma_INDEX] = modh_Start[feidhm_VALUE]; fráma_Cruach[fráma_INDEX] = 0;
    }
    static void return_tomhas(int TYPE_VALUE) {
        if (TYPE_VALUE != modh_return[fráma_modh[fráma_INDEX]]) { teip_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (túsaigh_fráma[fráma_INDEX] != 0) aicme_Sainmhíniú_staid[túsaigh_fráma[fráma_INDEX] - 1] = 2;
        if (틀잠금[fráma_INDEX] != 0) { 잠금풀기(틀잠금[fráma_INDEX]); 틀잠금[fráma_INDEX] = 0; }
        fráma_INDEX--; if (fráma_INDEX >= 현재가닥 * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] sruth_comhad_ainm = new int[64];
    static void comhad_sruth_CALL(int úinéir_VALUE, int Ainm, int formáid_VALUE, int Ordú) {
        boolean Aschur = Word_SMS(úinéir_VALUE, "java/io/FileOutputStream");
        int 종류 = Aschur ? 6 : 5;
        if (Ordú == 183 && Word_SMS(Ainm, "<init>")) {
            boolean 이어 = false;
            if (Aschur && Word_SMS(formáid_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(formáid_VALUE, "(Ljava/lang/String;)V")) { teip_VALUE("unsupported file stream constructor"); return; }
            int comhad_iontráil_ainm = 빼기(2), sruth_VALUE = 빼기(2);
            if (!oibiacht_VALUE(comhad_iontráil_ainm, 1) || !oibiacht_VALUE(sruth_VALUE, 종류) || ERREÁID) return;
            if (힙[sruth_VALUE + 3] != 0) { teip_VALUE("file stream already initialized"); return; }
            int fad_VALUE = 힙[comhad_iontráil_ainm + 1];
            if (fad_VALUE < 1 || fad_VALUE > 63) { teip_VALUE("invalid file name length"); return; }
            for (int spás_iontráil = 0; spás_iontráil < fad_VALUE; spás_iontráil++) {
                int VALUE = 힙[comhad_iontráil_ainm + 2 + spás_iontráil];
                if (VALUE < 1) { teip_VALUE("invalid file stream path"); return; }
                sruth_comhad_ainm[spás_iontráil] = VALUE;
            }
            sruth_comhad_ainm[fad_VALUE] = 0;
            int 서술자 = úsáideoir.파일서술자열기(sruth_comhad_ainm, Aschur ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { teip_VALUE("FileNotFoundException: file open failed"); return; }
            힙[sruth_VALUE + 2] = 서술자; 힙[sruth_VALUE + 3] = 1;
            return;
        }
        if (Ordú != 182) { teip_VALUE("invalid file stream invocation"); return; }
        if ((Aschur && Word_SMS(Ainm, "write") || !Aschur && Word_SMS(Ainm, "read"))
            && (Word_SMS(formáid_VALUE, Aschur ? "([B)V" : "([B)I") || Word_SMS(formáid_VALUE, Aschur ? "([BII)V" : "([BII)I"))) {
            boolean gearrthóg_VALUE = Word_SMS(formáid_VALUE, Aschur ? "([BII)V" : "([BII)I");
            int iontráil_COUNT = gearrthóg_VALUE ? 빼기(1) : 0, 시작점 = gearrthóg_VALUE ? 빼기(1) : 0, sonraí_ARRAY = 빼기(2), oibiacht_Leabhair_thagartha = 빼기(2);
            if (!oibiacht_VALUE(sonraí_ARRAY, 20) || !oibiacht_VALUE(oibiacht_Leabhair_thagartha, 종류)) return;
            if (!gearrthóg_VALUE) iontráil_COUNT = 힙[sonraí_ARRAY + 1];
            if (시작점 < 0 || iontráil_COUNT < 0 || 시작점 > 힙[sonraí_ARRAY + 1] - iontráil_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[oibiacht_Leabhair_thagartha + 3] == 0 || 힙[oibiacht_Leabhair_thagartha + 2] < 0) { teip_VALUE("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < iontráil_COUNT && !ERREÁID) {
                int 반환값 = Aschur ? úsáideoir.파일한바이트쓰기(힙[oibiacht_Leabhair_thagartha + 2], 힙[sonraí_ARRAY + 2 + 시작점 + 완료수]) : úsáideoir.파일한바이트읽기(힙[oibiacht_Leabhair_thagartha + 2]);
                if (반환값 < 0) { teip_VALUE(Aschur ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Aschur && 반환값 == 256) break;
                if (!Aschur) 힙[sonraí_ARRAY + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!Aschur) 넣기(iontráil_COUNT != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (Aschur && Word_SMS(Ainm, "flush") && Word_SMS(formáid_VALUE, "()V")) { int oibiacht_Leabhair_thagartha = 빼기(2); if (oibiacht_VALUE(oibiacht_Leabhair_thagartha, 종류) && 힙[oibiacht_Leabhair_thagartha + 2] < 0) teip_VALUE("IOException: stream closed"); return; }
        int Gníomh = -1, VALUE = 0;
        if (Word_SMS(Ainm, "close") && Word_SMS(formáid_VALUE, "()V")) Gníomh = 0;
        if (!Aschur && Word_SMS(Ainm, "read") && Word_SMS(formáid_VALUE, "()I")) Gníomh = 1;
        if (Aschur && Word_SMS(Ainm, "write") && Word_SMS(formáid_VALUE, "(I)V")) { Gníomh = 2; VALUE = 빼기(1); }
        if (Gníomh < 0) { teip_VALUE("unsupported file stream method"); return; }
        int sruth_VALUE = 빼기(2);
        if (!oibiacht_VALUE(sruth_VALUE, 종류) || ERREÁID) return;
        if (힙[sruth_VALUE + 3] == 0) { teip_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[sruth_VALUE + 2];
        if (Gníomh == 0) {
            if (서술자 >= 0 && úsáideoir.파일서술자닫기(서술자) < 0) teip_VALUE("IOException: close failed");
            힙[sruth_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { teip_VALUE("IOException: stream closed"); return; }
        if (Gníomh == 1) {
            int tomhas = úsáideoir.파일한바이트읽기(서술자);
            if (tomhas < -1) teip_VALUE("IOException: read failed"); else 넣기(tomhas == 256 ? -1 : tomhas, 1);
        } else if (úsáideoir.파일한바이트쓰기(서술자, VALUE) != 1) teip_VALUE("IOException: write failed");
    }
    static void CALL_modh(int INDEX, int Ordú) {
        if (INDEX <= 0 || INDEX >= tairiseach_clib.length || (tairiseach_clib[INDEX] != 10 && tairiseach_clib[INDEX] != 11)) { teip_VALUE("invalid method reference"); return; }
        int úinéir_VALUE = aicme_ainm_SMS(상가[INDEX]), Ainm = Leabhair_thagartha_ainm(tairiseach_SECOND_VALUE[INDEX]), formáid_VALUE = Leabhair_thagartha_TYPE(tairiseach_SECOND_VALUE[INDEX]);
        if (ERREÁID) return;
        if (기본호출(úinéir_VALUE, Ainm, formáid_VALUE, Ordú)) return;
        if (Word_SMS(úinéir_VALUE, "java/io/FileInputStream") || Word_SMS(úinéir_VALUE, "java/io/FileOutputStream")) {
            comhad_sruth_CALL(úinéir_VALUE, Ainm, formáid_VALUE, Ordú); return;
        }
        if (Ordú == 184 && Word_SMS(úinéir_VALUE, "java/lang/Integer") && Word_SMS(Ainm, "parseInt") && Word_SMS(formáid_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Ordú == 182 && Word_SMS(úinéir_VALUE, "java/io/PrintStream") && (Word_SMS(Ainm, "println") || Word_SMS(Ainm, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_SMS(formáid_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_SMS(formáid_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_SMS(formáid_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_SMS(formáid_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_SMS(formáid_VALUE, "()V") || !Word_SMS(Ainm, "println")) teip_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) teip_VALUE("invalid PrintStream receiver");
            if (ERREÁID) return;
            if (TYPE_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (TYPE_VALUE == 2) úsáideoir.Scríobh(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) úsáideoir.scríobh_carachtar_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) scríobh_SMS(VALUE);
            if (Word_SMS(Ainm, "println")) úsáideoir.scríobh_carachtar_VALUE(10);
            return;
        }
        if (Ordú == 182 && Word_SMS(úinéir_VALUE, "java/lang/String")) {
            if (Word_SMS(Ainm, "length") && Word_SMS(formáid_VALUE, "()I")) {
                int Leabhair_thagartha = 빼기(2); if (oibiacht_VALUE(Leabhair_thagartha, 1)) 넣기(힙[Leabhair_thagartha + 1], 1); return;
            }
            if (Word_SMS(Ainm, "charAt") && Word_SMS(formáid_VALUE, "(I)C")) {
                int foscript_VALUE = 빼기(1), Leabhair_thagartha = 빼기(2);
                if (oibiacht_VALUE(Leabhair_thagartha, 1)) {
                    if (foscript_VALUE < 0 || foscript_VALUE >= 힙[Leabhair_thagartha + 1]) teip_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[Leabhair_thagartha + 2 + foscript_VALUE], 1);
                }
                return;
            }
        }
        if (Word_SMS(úinéir_VALUE, "java/lang/StringBuilder")) {
            if (Ordú == 183 && Word_SMS(Ainm, "<init>") && Word_SMS(formáid_VALUE, "()V")) { oibiacht_VALUE(빼기(2), 4); return; }
            if (Ordú == 182 && Word_SMS(Ainm, "toString") && Word_SMS(formáid_VALUE, "()Ljava/lang/String;")) {
                int Leabhair_thagartha = 빼기(2); if (oibiacht_VALUE(Leabhair_thagartha, 4)) 넣기(힙[Leabhair_thagartha + 2] == 0 ? óstach_carachtar("") : 힙[Leabhair_thagartha + 2], 2); return;
            }
            if (Ordú == 182 && Word_SMS(Ainm, "append")) {
                int Téacs = 0;
                if (Word_SMS(formáid_VALUE, "(I)Ljava/lang/StringBuilder;")) Téacs = digit_carachtar(빼기(1));
                else if (Word_SMS(formáid_VALUE, "(Z)Ljava/lang/StringBuilder;")) Téacs = óstach_carachtar(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(formáid_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Téacs = leithdháil_Stóras(1, 1); if (!ERREÁID) 힙[Téacs + 2] = VALUE & 65535;
                }
                else if (Word_SMS(formáid_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Téacs = 빼기(2); if (Téacs == 0) Téacs = óstach_carachtar("null"); }
                else { teip_VALUE("unsupported StringBuilder append"); return; }
                int Leabhair_thagartha = 빼기(2); if (!oibiacht_VALUE(Leabhair_thagartha, 4) || !oibiacht_VALUE(Téacs, 1)) return;
                int 앞 = 힙[Leabhair_thagartha + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], Siar_VALUE_fad = 힙[Téacs + 1];
                int 새글 = leithdháil_Stóras(1, 앞길이 + Siar_VALUE_fad); if (ERREÁID) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < Siar_VALUE_fad; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[Téacs + 2 + 수];
                힙[Leabhair_thagartha + 2] = 새글; 넣기(Leabhair_thagartha, 2); return;
            }
        }
        int aicme_Sainmhíniú = FIND_aicme_Sainmhíniú(úinéir_VALUE); if (aicme_Sainmhíniú < 0 || ERREÁID) return;
        int comhad_INDEX = FIND_modh(aicme_Sainmhíniú, Ainm, formáid_VALUE);
        if (comhad_INDEX < 0) {
            for (int pointe_cóid = aicme_Sainmhíniú, iontráil_COUNT = 0; pointe_cóid >= 0 && iontráil_COUNT < 16; iontráil_COUNT++, pointe_cóid = 부모종(pointe_cóid))
                if (Word_SMS(종부모[pointe_cóid], "java/lang/Thread")) { 가닥호출(Ainm, formáid_VALUE, Ordú); return; }
            teip_VALUE("NoSuchMethodError"); return;
        }
        if (((modh_rochtain[comhad_INDEX] & 8) != 0) != (Ordú == 184)) { teip_VALUE("method static/instance mismatch"); return; }
        if (Ordú == 184) { if (!túsaigh(modh_úinéir[comhad_INDEX], fráma_treoir[fráma_INDEX])) return; }
        else {
            int 읽는자리 = fráma_Cruach[fráma_INDEX] - modh_argóint_COUNT[comhad_INDEX];
            if (읽는자리 < 0 || 스택형[fráma_INDEX * 128 + 읽는자리] != 2) { teip_VALUE("invalid method receiver"); return; }
            int oibiacht_Leabhair_thagartha = 스택값[fráma_INDEX * 128 + 읽는자리];
            if (!객체유효(oibiacht_Leabhair_thagartha)) return;
            if (힙[oibiacht_Leabhair_thagartha] < 32 || !종포함(힙[oibiacht_Leabhair_thagartha] - 32, úinéir_VALUE)) { teip_VALUE("method receiver type mismatch"); return; }
            if (Ordú != 183) comhad_INDEX = FIND_modh(힙[oibiacht_Leabhair_thagartha] - 32, Ainm, formáid_VALUE);
        }
        if (comhad_INDEX < 0 || (modh_rochtain[comhad_INDEX] & 0x400) != 0) { teip_VALUE("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((modh_rochtain[comhad_INDEX] & 32) != 0) {
            if (Ordú == 184) { int pointe_cóid = modh_úinéir[comhad_INDEX]; if (종잠금[pointe_cóid] == 0) 종잠금[pointe_cóid] = leithdháil_Stóras(8, 0); 잠금참조 = 종잠금[pointe_cóid]; }
            else 잠금참조 = 스택값[fráma_INDEX * 128 + fráma_Cruach[fráma_INDEX] - modh_argóint_COUNT[comhad_INDEX]];
            if (!잠금얻기(잠금참조)) { if (!ERREÁID) fráma_suíomh[fráma_INDEX] = fráma_treoir[fráma_INDEX]; return; }
        }
        호출(comhad_INDEX); if (!ERREÁID) 틀잠금[fráma_INDEX] = 잠금참조;
    }
    static boolean 배열저장가능(int ARRAY_Leabhair_thagartha, int sonraí_VALUE) {
        if (sonraí_VALUE == 0 || ARRAY_eilimint[ARRAY_Leabhair_thagartha] == 0) return true;
        boolean 성공여부 = ARRAY_eilimint[ARRAY_Leabhair_thagartha] == -1 ? (sonraí_VALUE > 0 && sonraí_VALUE < 힙끝 && 힙[sonraí_VALUE] == 1) : 맞는객체(sonraí_VALUE, ARRAY_eilimint[ARRAY_Leabhair_thagartha]);
        if (!성공여부 && !ERREÁID) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int ARRAY_spás(int Leabhair_thagartha, int foscript_VALUE, int TYPE_VALUE) {
        if (!oibiacht_VALUE(Leabhair_thagartha, TYPE_VALUE)) return 0;
        if (foscript_VALUE < 0 || foscript_VALUE >= 힙[Leabhair_thagartha + 1]) { teip_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Leabhair_thagartha + 2 + foscript_VALUE;
    }
    static void Rith_ordú() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (ERREÁID) { if (던진객체 != 0) hanla_eisceacht(); if (ERREÁID || fráma_INDEX < 현재가닥 * 32) break; }
            if (fráma_INDEX < 현재가닥 * 32 || athraigh_iarratas_HTTP || --조각 == 0) { if (!SWITCH_snáithe()) break; 조각 = 100; }
            if (fráma_INDEX == 0 && aicme_Sainmhíniú_staid[iontráil_aicme_Sainmhíniú] != 2 && !túsaigh(iontráil_aicme_Sainmhíniú, fráma_suíomh[fráma_INDEX])) continue;
            if (fráma_INDEX == 현재가닥 * 32 && 현재가닥 != 0 && (modh_rochtain[fráma_modh[fráma_INDEX]] & 32) != 0 && 틀잠금[fráma_INDEX] == 0) {
                int oibiacht_Leabhair_thagartha = snáithe_sprioc[현재가닥]; if (!잠금얻기(oibiacht_Leabhair_thagartha)) { if (ERREÁID) break; continue; } 틀잠금[fráma_INDEX] = oibiacht_Leabhair_thagartha;
            }
            잠시수 = 0;
            if (--남음 == 0) { teip_VALUE("instruction limit (500000)"); break; }
            int Rith_2 = fráma_suíomh[fráma_INDEX]; fráma_treoir[fráma_INDEX] = Rith_2; int VALUE = 명바();
            if (ERREÁID) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = modh_úinéir[fráma_modh[fráma_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= tairiseach_clib.length) teip_VALUE("invalid ldc constant");
                else if (tairiseach_clib[수] == 3) 넣기(상가[수], 1);
                else if (tairiseach_clib[수] == 8) 넣기(tairiseach_SMS(상가[수]), 2);
                else teip_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { scríobh_logánta(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { scríobh_logánta(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { scríobh_logánta(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int iontráil_suíomh = 빼기(1), oibiacht_Leabhair_thagartha = 빼기(2), catagóir_CODE = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && oibiacht_Leabhair_thagartha > 0 && oibiacht_Leabhair_thagartha < 힙끝 && 힙[oibiacht_Leabhair_thagartha] == 21) catagóir_CODE = 21;
                int 읽는자리 = ARRAY_spás(oibiacht_Leabhair_thagartha, iontráil_suíomh, catagóir_CODE); if (!ERREÁID) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int iontráil_Leabhair_thagartha = 빼기(VALUE == 83 ? 2 : 1), iontráil_suíomh = 빼기(1), oibiacht_Leabhair_thagartha = 빼기(2), catagóir_CODE = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && oibiacht_Leabhair_thagartha > 0 && oibiacht_Leabhair_thagartha < 힙끝 && 힙[oibiacht_Leabhair_thagartha] == 21) catagóir_CODE = 21;
                int 읽는자리 = ARRAY_spás(oibiacht_Leabhair_thagartha, iontráil_suíomh, catagóir_CODE);
                if (!ERREÁID && catagóir_CODE == 3 && !배열저장가능(oibiacht_Leabhair_thagartha, iontráil_Leabhair_thagartha)) continue;
                if (!ERREÁID) 힙[읽는자리] = catagóir_CODE == 20 ? (byte)iontráil_Leabhair_thagartha : catagóir_CODE == 21 ? iontráil_Leabhair_thagartha & 1 : catagóir_CODE == 22 ? (char)iontráil_Leabhair_thagartha : catagóir_CODE == 23 ? (short)iontráil_Leabhair_thagartha : iontráil_Leabhair_thagartha;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { Cruach_treoir(VALUE); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), tomhas = 0;
                if ((VALUE == 108 || VALUE == 112) && 나 == 0) { teip_VALUE("ArithmeticException: / by zero"); continue; }
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
                int logánta_scóip = 명바(), 증분 = (byte)명바(); 지역읽기(logánta_scóip, 1); 넣기(빼기(1) + 증분, 1); scríobh_logánta(logánta_scóip, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int sprioc_VALUE = Rith_2 + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int 나 = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == 나 : VALUE == 160 || VALUE == 166 ? 가 != 나 : VALUE == 161 ? 가 < 나 : VALUE == 162 ? 가 >= 나 : VALUE == 163 ? 가 > 나 : 가 <= 나;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) bog_VALUE(sprioc_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { return_tomhas(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, Rith_2); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { teip_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_modh(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(aicme_ainm_SMS(명상수()), Rith_2); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int catagóir_CODE = 3, comhpháirt = 0;
                if (VALUE == 188) { int 임시값 = 명바(); catagóir_CODE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else comhpháirt = aicme_ainm_SMS(명상수());
                if (catagóir_CODE == 0) { teip_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), oibiacht_Leabhair_thagartha = leithdháil_Stóras(catagóir_CODE, 유효길이); if (!ERREÁID) ARRAY_eilimint[oibiacht_Leabhair_thagartha] = comhpháirt; 넣기(oibiacht_Leabhair_thagartha, 2); continue;
            }
            if (VALUE == 190) {
                int oibiacht_Leabhair_thagartha = 빼기(2);
                if (객체유효(oibiacht_Leabhair_thagartha)) { int 비교자리 = 힙[oibiacht_Leabhair_thagartha]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) teip_VALUE("not an array"); else 넣기(힙[oibiacht_Leabhair_thagartha + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int oibiacht_Leabhair_thagartha = 빼기(2); if (객체유효(oibiacht_Leabhair_thagartha)) { if (힙[oibiacht_Leabhair_thagartha] != 9) teip_VALUE("athrow requires supported Throwable"); else { 던진객체 = oibiacht_Leabhair_thagartha; ERREÁID = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int ainm_tairiseach = aicme_ainm_SMS(명상수()), oibiacht_Leabhair_thagartha = 빼기(2); boolean MATCH = 맞는객체(oibiacht_Leabhair_thagartha, ainm_tairiseach);
                if (VALUE == 193) 넣기(oibiacht_Leabhair_thagartha != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !ERREÁID) teip_VALUE("ClassCastException"); 넣기(oibiacht_Leabhair_thagartha, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = Rith_2 + 1, comhad_INDEX = fráma_modh[fráma_INDEX], eochair_Leabhair_thagartha = 빼기(1);
                while ((읽는자리 - modh_Start[comhad_INDEX]) % 4 != 0) 읽는자리++;
                int sprioc_ADDRESS = suíomh_slánuimhir(읽는자리);
                if (VALUE == 170) { int 낮은값 = suíomh_slánuimhir(읽는자리 + 4), 높은값 = suíomh_slánuimhir(읽는자리 + 8); if (eochair_Leabhair_thagartha >= 낮은값 && eochair_Leabhair_thagartha <= 높은값) sprioc_ADDRESS = suíomh_slánuimhir(읽는자리 + 12 + (eochair_Leabhair_thagartha - 낮은값) * 4); }
                else { int 총수 = suíomh_slánuimhir(읽는자리 + 4); for (int lúb_INDEX = 0; lúb_INDEX < 총수; lúb_INDEX++) if (suíomh_slánuimhir(읽는자리 + 8 + lúb_INDEX * 8) == eochair_Leabhair_thagartha) sprioc_ADDRESS = suíomh_slánuimhir(읽는자리 + 12 + lúb_INDEX * 8); }
                bog_VALUE(Rith_2 + sprioc_ADDRESS); continue;
            }
            if (VALUE == 200) { bog_VALUE(Rith_2 + suíomh_slánuimhir(Rith_2 + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int oibiacht_Leabhair_thagartha = 빼기(2);
                if (VALUE == 195) 잠금풀기(oibiacht_Leabhair_thagartha);
                else if (!잠금얻기(oibiacht_Leabhair_thagartha) && !ERREÁID) { 넣기(oibiacht_Leabhair_thagartha, 2); fráma_suíomh[fráma_INDEX] = Rith_2; }
                continue;
            }
            if (VALUE == 196) {
                int ordú_CODE = 명바(), iontráil_suíomh = 명짧();
                if (ordú_CODE == 21 || ordú_CODE == 25) 지역읽기(iontráil_suíomh, ordú_CODE == 21 ? 1 : 2);
                else if (ordú_CODE == 54 || ordú_CODE == 58) scríobh_logánta(iontráil_suíomh, ordú_CODE == 54 ? 1 : 2);
                else if (ordú_CODE == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(iontráil_suíomh, 1); 넣기(빼기(1) + DELTA_VALUE, 1); scríobh_logánta(iontráil_suíomh, 1); }
                else teip_VALUE("unsupported wide opcode");
                continue;
            }
            teip_VALUE("unsupported bytecode");
        }
    }
    static int FIND_aicme_Sainmhíniú(int Ainm) {
        for (int lúb_INDEX = 0; lúb_INDEX < aicme_Sainmhíniú_COUNT; lúb_INDEX++) if (aicme_Sainmhíniú_ainm[lúb_INDEX] != 0 && 같은말(aicme_Sainmhíniú_ainm[lúb_INDEX], Ainm)) return lúb_INDEX;
        return lódáil_aicme_Sainmhíniú(tairiseach_SMS(Ainm));
    }
    static int lódáil_aicme_Sainmhíniú(int ainm_teaghrán) {
        if (!oibiacht_VALUE(ainm_teaghrán, 1)) return -1;
        int fad_VALUE = 힙[ainm_teaghrán + 1];
        if (fad_VALUE < 1 || fad_VALUE > 505 || aicme_Sainmhíniú_COUNT == 16) { teip_VALUE("class name/count limit"); return -1; }
        for (int lúb_INDEX = 0; lúb_INDEX < fad_VALUE; lúb_INDEX++) { int pointe_cóid = 힙[ainm_teaghrán + 2 + lúb_INDEX]; comhad_ainm_SMS[lúb_INDEX] = pointe_cóid == '/' ? '.' : pointe_cóid; }
        comhad_ainm_SMS[fad_VALUE] = '.'; comhad_ainm_SMS[fad_VALUE + 1] = 'c'; comhad_ainm_SMS[fad_VALUE + 2] = 'l'; comhad_ainm_SMS[fad_VALUE + 3] = 'a'; comhad_ainm_SMS[fad_VALUE + 4] = 's'; comhad_ainm_SMS[fad_VALUE + 5] = 's'; comhad_ainm_SMS[fad_VALUE + 6] = 0;
        int Méid = úsáideoir.파일읽기(comhad_ainm_SMS, 임시파일);
        if (Méid < 0) { teip_VALUE("ClassNotFoundException"); return -1; }
        int aicme_Sainmhíniú = aicme_Sainmhíniú_COUNT++; aicme_Sainmhíniú_socraigh_méid[aicme_Sainmhíniú] = Méid;
        for (int lúb_INDEX = 0; lúb_INDEX < Méid; lúb_INDEX++) Comhad[aicme_Sainmhíniú * 16384 + lúb_INDEX] = 임시파일[lúb_INDEX];
        클래스읽기(aicme_Sainmhíniú); if (ERREÁID) return -1;
        int iarbhír_sonraí = tairiseach_SMS(aicme_Sainmhíniú_ainm[aicme_Sainmhíniú]);
        if (!글같음(iarbhír_sonraí, ainm_teaghrán, true)) { teip_VALUE("class name does not match file"); return -1; }
        int 부모 = 종부모[aicme_Sainmhíniú];
        if (부모 != 0 && !Word_SMS(부모, "java/lang/Object") && !Word_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_aicme_Sainmhíniú(부모);
            if (ERREÁID || 위 < 0) return -1;
            int 읽는자리 = 위, céim_COUNT = 0;
            while (읽는자리 >= 0 && céim_COUNT++ < 16) {
                if (읽는자리 == aicme_Sainmhíniú) { teip_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = aicme_spás_COUNT[위];
            for (int comhad_INDEX = 0; comhad_INDEX < spás_COUNT; comhad_INDEX++) if (spás_úinéir[comhad_INDEX] == aicme_Sainmhíniú && (spás_ceadanna_rochtana[comhad_INDEX] & 8) == 0) spás_suíomh[comhad_INDEX] += 시작변위;
            aicme_spás_COUNT[aicme_Sainmhíniú] += 시작변위;
        }
        return aicme_Sainmhíniú;
    }
    static int 부모종(int aicme_Sainmhíniú) {
        int Ainm = 종부모[aicme_Sainmhíniú];
        for (int lúb_INDEX = 0; lúb_INDEX < aicme_Sainmhíniú_COUNT; lúb_INDEX++) if (Ainm != 0 && aicme_Sainmhíniú_ainm[lúb_INDEX] != 0 && 같은말(aicme_Sainmhíniú_ainm[lúb_INDEX], Ainm)) return lúb_INDEX;
        return -1;
    }
    static int FIND_modh(int aicme_Sainmhíniú, int Ainm, int formáid_VALUE) {
        for (int 깊이 = 0; aicme_Sainmhíniú >= 0 && 깊이 < 16; 깊이++, aicme_Sainmhíniú = 부모종(aicme_Sainmhíniú)) {
            for (int lúb_INDEX = 0; lúb_INDEX < modh_COUNT; lúb_INDEX++) if (modh_úinéir[lúb_INDEX] == aicme_Sainmhíniú && 같은말(modh_ainm_SMS[lúb_INDEX], Ainm) && 같은말(modh_TYPE[lúb_INDEX], formáid_VALUE)) return lúb_INDEX;
        }
        return -1;
    }
    static int ainm_modh(int aicme_Sainmhíniú, String Ainm, String formáid_VALUE) {
        for (int 깊이 = 0; aicme_Sainmhíniú >= 0 && 깊이 < 16; 깊이++, aicme_Sainmhíniú = 부모종(aicme_Sainmhíniú))
            for (int lúb_INDEX = 0; lúb_INDEX < modh_COUNT; lúb_INDEX++) if (modh_úinéir[lúb_INDEX] == aicme_Sainmhíniú && Word_SMS(modh_ainm_SMS[lúb_INDEX], Ainm) && Word_SMS(modh_TYPE[lúb_INDEX], formáid_VALUE)) return lúb_INDEX;
        return -1;
    }
    static int 형종류(int Ainm) { return Comhad[상가[Ainm]] == 'L' || Comhad[상가[Ainm]] == '[' ? 2 : 1; }
    static boolean túsaigh(int aicme_Sainmhíniú, int ordú_Start) {
        if (aicme_Sainmhíniú < 0 || ERREÁID) return false;
        if (aicme_Sainmhíniú_staid[aicme_Sainmhíniú] == 3) { teip_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (aicme_Sainmhíniú_staid[aicme_Sainmhíniú] == 1 && aicme_snáithe[aicme_Sainmhíniú] != 현재가닥) { fráma_suíomh[fráma_INDEX] = ordú_Start; athraigh_iarratas_HTTP = true; return false; }
        if (aicme_Sainmhíniú_staid[aicme_Sainmhíniú] != 0) return true;
        int 위 = 부모종(aicme_Sainmhíniú);
        if (위 >= 0 && !túsaigh(위, ordú_Start)) return false;
        aicme_Sainmhíniú_staid[aicme_Sainmhíniú] = 1; aicme_snáithe[aicme_Sainmhíniú] = 현재가닥;
        if (túsaigh_aicme_Sainmhíniú[aicme_Sainmhíniú] != 0) {
            fráma_suíomh[fráma_INDEX] = ordú_Start;
            호출(túsaigh_aicme_Sainmhíniú[aicme_Sainmhíniú] - 1); if (!ERREÁID) túsaigh_fráma[fráma_INDEX] = aicme_Sainmhíniú + 1;
            return false;
        }
        aicme_Sainmhíniú_staid[aicme_Sainmhíniú] = 2; return true;
    }
    static void 필드호출(int INDEX, int Ordú, int Rith_2) {
        if (!seic_tairiseach(INDEX, 9)) return;
        int úinéir_VALUE = aicme_ainm_SMS(상가[INDEX]), Ainm = Leabhair_thagartha_ainm(tairiseach_SECOND_VALUE[INDEX]), formáid_VALUE = Leabhair_thagartha_TYPE(tairiseach_SECOND_VALUE[INDEX]);
        if (Word_SMS(úinéir_VALUE, "java/lang/System") && (Word_SMS(Ainm, "out") || Word_SMS(Ainm, "err")) && Word_SMS(formáid_VALUE, "Ljava/io/PrintStream;") && Ordú == 178) { 넣기(-1, 2); return; }
        int aicme_Sainmhíniú = FIND_aicme_Sainmhíniú(úinéir_VALUE); if (aicme_Sainmhíniú < 0 || ERREÁID) return;
        int 찾음 = -1;
        for (int 읽는자리 = aicme_Sainmhíniú, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int comhad_INDEX = 0; comhad_INDEX < spás_COUNT; comhad_INDEX++) if (spás_úinéir[comhad_INDEX] == 읽는자리 && 같은말(spás_ainm[comhad_INDEX], Ainm) && 같은말(spás_TYPE[comhad_INDEX], formáid_VALUE)) 찾음 = comhad_INDEX;
        if (찾음 < 0) { teip_VALUE("NoSuchFieldError"); return; }
        boolean statach_VALUE = Ordú == 178 || Ordú == 179;
        if (statach_VALUE != ((spás_ceadanna_rochtana[찾음] & 8) != 0)) { teip_VALUE("field static/instance mismatch"); return; }
        if (statach_VALUE && !túsaigh(spás_úinéir[찾음], Rith_2)) return;
        int TYPE_VALUE = 형종류(formáid_VALUE), VALUE = 0;
        if (Ordú == 179 || Ordú == 181) VALUE = 빼기(TYPE_VALUE);
        if (statach_VALUE) { if (Ordú == 178) 넣기(spás_sonraí[찾음], TYPE_VALUE); else if (!ERREÁID) spás_sonraí[찾음] = VALUE; return; }
        int oibiacht_Leabhair_thagartha = 빼기(2);
        if (!객체유효(oibiacht_Leabhair_thagartha)) return;
        if (힙[oibiacht_Leabhair_thagartha] < 32 || !종포함(힙[oibiacht_Leabhair_thagartha] - 32, úinéir_VALUE)) { teip_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = oibiacht_Leabhair_thagartha + 2 + spás_suíomh[찾음];
        if (Ordú == 180) 넣기(힙[보관칸], TYPE_VALUE);
        else if (!ERREÁID) { 힙[보관칸] = VALUE; 힙참조[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int aicme_Sainmhíniú, int Ainm) {
        for (int 중첩깊이 = 0; aicme_Sainmhíniú >= 0 && 중첩깊이 < 16; 중첩깊이++, aicme_Sainmhíniú = 부모종(aicme_Sainmhíniú)) {
            if (같은말(aicme_Sainmhíniú_ainm[aicme_Sainmhíniú], Ainm) || (종부모[aicme_Sainmhíniú] != 0 && 같은말(종부모[aicme_Sainmhíniú], Ainm))) return true;
            for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < aicme_comhéadan_COUNT[aicme_Sainmhíniú]; comhcheangal_istigh_suíomh++) if (같은말(aicme_comhéadan[aicme_Sainmhíniú * 16 + comhcheangal_istigh_suíomh], Ainm)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int beart_sonraí, boolean CONAIR) {
        if (첫값 == beart_sonraí) return true;
        if (첫값 <= 0 || beart_sonraí <= 0 || 힙[첫값] != 1 || 힙[beart_sonraí] != 1 || 힙[첫값 + 1] != 힙[beart_sonraí + 1]) return false;
        for (int lúb_INDEX = 0; lúb_INDEX < 힙[첫값 + 1]; lúb_INDEX++) {
            int x_chomhordanáid = 힙[첫값 + 2 + lúb_INDEX], 세로좌표 = 힙[beart_sonraí + 2 + lúb_INDEX];
            if (CONAIR) { if (x_chomhordanáid == '.') x_chomhordanáid = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (x_chomhordanáid != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int oibiacht_Leabhair_thagartha) {
        if (oibiacht_Leabhair_thagartha == 0) { teip_VALUE("NullPointerException"); return false; }
        if (oibiacht_Leabhair_thagartha < 1 || oibiacht_Leabhair_thagartha >= 힙끝 || 힙폭[oibiacht_Leabhair_thagartha] < 2 || 힙[oibiacht_Leabhair_thagartha] == 0) { teip_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void cosain_VALUE(int oibiacht_Leabhair_thagartha) {
        if (oibiacht_Leabhair_thagartha > 0 && oibiacht_Leabhair_thagartha < 힙끝 && 힙폭[oibiacht_Leabhair_thagartha] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = oibiacht_Leabhair_thagartha;
    }
    static void seó_VALUE(int oibiacht_Leabhair_thagartha) {
        if (oibiacht_Leabhair_thagartha > 0 && oibiacht_Leabhair_thagartha < 힙끝 && 힙폭[oibiacht_Leabhair_thagartha] >= 2 && 힙[oibiacht_Leabhair_thagartha] != 0 && 힙표시[oibiacht_Leabhair_thagartha] == 0) {
            힙표시[oibiacht_Leabhair_thagartha] = 1; 표시대기[taispeáin_COUNT++] = oibiacht_Leabhair_thagartha;
        }
    }
    static void 수거() {
        taispeáin_COUNT = 0; Bailiúchán_COUNT++;
        for (int seic_suíomh = 1; seic_suíomh < 힙끝; seic_suíomh += 힙폭[seic_suíomh]) 힙표시[seic_suíomh] = 0;
        for (int lúb_INDEX = 0; lúb_INDEX < teaghrán_Leabhair_thagartha.length; lúb_INDEX++) seó_VALUE(teaghrán_Leabhair_thagartha[lúb_INDEX]);
        for (int lúb_INDEX = 0; lúb_INDEX < spás_COUNT; lúb_INDEX++) if ((spás_ceadanna_rochtana[lúb_INDEX] & 8) != 0 && 형종류(spás_TYPE[lúb_INDEX]) == 2) seó_VALUE(spás_sonraí[lúb_INDEX]);
        for (int 임시값 = 0; 임시값 < snáithe_COUNT; 임시값++) {
            seó_VALUE(snáithe_oibiacht[임시값]); seó_VALUE(snáithe_sprioc[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? fráma_INDEX : snáithe_fráma[임시값];
            for (int comhad_INDEX = 임시값 * 32; comhad_INDEX <= 꼭대기자리; comhad_INDEX++) {
                for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < 함수지역[fráma_modh[comhad_INDEX]]; comhcheangal_istigh_suíomh++) if (logánta_TYPE[comhad_INDEX * 128 + comhcheangal_istigh_suíomh] == 2) seó_VALUE(logánta_VALUE[comhad_INDEX * 128 + comhcheangal_istigh_suíomh]);
                for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < fráma_Cruach[comhad_INDEX]; comhcheangal_istigh_suíomh++) if (스택형[comhad_INDEX * 128 + comhcheangal_istigh_suíomh] == 2) seó_VALUE(스택값[comhad_INDEX * 128 + comhcheangal_istigh_suíomh]);
            }
        }
        for (int lúb_INDEX = 0; lúb_INDEX < 화면참조.length; lúb_INDEX++) seó_VALUE(화면참조[lúb_INDEX]);
        for (int lúb_INDEX = 0; lúb_INDEX < 나중수; lúb_INDEX++) seó_VALUE(나중실행[lúb_INDEX]);
        for (int lúb_INDEX = 0; lúb_INDEX < Store_slánuimhir.length; lúb_INDEX++) seó_VALUE(Store_slánuimhir[lúb_INDEX]);
        for (int lúb_INDEX = 0; lúb_INDEX < aicme_Sainmhíniú_COUNT; lúb_INDEX++) seó_VALUE(종잠금[lúb_INDEX]);
        for (int seic_suíomh = 1; seic_suíomh < 힙끝; seic_suíomh += 힙폭[seic_suíomh]) if (잠금깊이[seic_suíomh] > 0) seó_VALUE(seic_suíomh);
        seó_VALUE(던진객체);
        for (int lúb_INDEX = 0; lúb_INDEX < 잠시수; lúb_INDEX++) seó_VALUE(잠시참조[lúb_INDEX]);
        while (taispeáin_COUNT > 0) {
            int oibiacht_Leabhair_thagartha = 표시대기[--taispeáin_COUNT], catagóir_CODE = 힙[oibiacht_Leabhair_thagartha];
            for (int lúb_INDEX = oibiacht_Leabhair_thagartha + 2; lúb_INDEX < oibiacht_Leabhair_thagartha + 힙폭[oibiacht_Leabhair_thagartha]; lúb_INDEX++) if (catagóir_CODE == 3 || catagóir_CODE == 4 || 힙참조[lúb_INDEX] != 0) seó_VALUE(힙[lúb_INDEX]);
        }
        for (int seic_suíomh = 1; seic_suíomh < 힙끝; seic_suíomh += 힙폭[seic_suíomh]) if (힙표시[seic_suíomh] == 0) 힙[seic_suíomh] = 0;
        for (int seic_suíomh = 1; seic_suíomh < 힙끝; seic_suíomh += 힙폭[seic_suíomh]) if (힙[seic_suíomh] == 0) {
            while (seic_suíomh + 힙폭[seic_suíomh] < 힙끝 && 힙[seic_suíomh + 힙폭[seic_suíomh]] == 0) { int Ar_aghaidh_suíomh = seic_suíomh + 힙폭[seic_suíomh]; 힙폭[seic_suíomh] += 힙폭[Ar_aghaidh_suíomh]; 힙폭[Ar_aghaidh_suíomh] = 0; }
            if (seic_suíomh + 힙폭[seic_suíomh] == 힙끝) { 힙끝 = seic_suíomh; break; }
        }
    }
    static int 새기억(int 종류, int fad_VALUE) {
        if (fad_VALUE < 0) { teip_VALUE("NegativeArraySizeException"); return 0; }
        if (fad_VALUE > 힙.length - 3) { teip_VALUE("object heap exhausted"); return 0; }
        int 필요수 = fad_VALUE + 2, oibiacht_Leabhair_thagartha = 0;
        if (필요수 <= 힙.length - 힙끝) { oibiacht_Leabhair_thagartha = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { oibiacht_Leabhair_thagartha = 읽는자리; break; }
            if (oibiacht_Leabhair_thagartha != 0) {
                int 남은길이 = 힙폭[oibiacht_Leabhair_thagartha] - 필요수;
                if (남은길이 >= 2) { 힙폭[oibiacht_Leabhair_thagartha + 필요수] = 남은길이; 힙[oibiacht_Leabhair_thagartha + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { oibiacht_Leabhair_thagartha = 힙끝; 힙끝 += 필요수; }
        }
        if (oibiacht_Leabhair_thagartha == 0) { teip_VALUE("object heap exhausted"); return 0; }
        for (int lúb_INDEX = 0; lúb_INDEX < 필요수; lúb_INDEX++) { 힙[oibiacht_Leabhair_thagartha + lúb_INDEX] = 0; 힙참조[oibiacht_Leabhair_thagartha + lúb_INDEX] = 0; 힙폭[oibiacht_Leabhair_thagartha + lúb_INDEX] = 0; }
        ARRAY_eilimint[oibiacht_Leabhair_thagartha] = 0;
        힙폭[oibiacht_Leabhair_thagartha] = 필요수; 힙[oibiacht_Leabhair_thagartha] = 종류; 힙[oibiacht_Leabhair_thagartha + 1] = fad_VALUE; cosain_VALUE(oibiacht_Leabhair_thagartha); return oibiacht_Leabhair_thagartha;
    }
    static int eisceacht_aicme(String ainm_tairiseach) {
        if (자바도구.같음(ainm_tairiseach, "java/lang/Throwable")) return 1;
        if (자바도구.같음(ainm_tairiseach, "java/lang/Exception")) return 2;
        if (자바도구.같음(ainm_tairiseach, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(ainm_tairiseach, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(ainm_tairiseach, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(ainm_tairiseach, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(ainm_tairiseach, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(ainm_tairiseach, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(ainm_tairiseach, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(ainm_tairiseach, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(ainm_tairiseach, "java/io/IOException")) return 11;
        if (자바도구.같음(ainm_tairiseach, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(ainm_tairiseach, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(ainm_tairiseach, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(ainm_tairiseach, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int eisceacht_tairiseach(int Ainm) {
        for (int lúb_INDEX = 1; lúb_INDEX <= 41; lúb_INDEX++) if (Word_SMS(Ainm, eisceacht_ainm(lúb_INDEX))) return lúb_INDEX;
        return 0;
    }
    static String eisceacht_ainm(int cuntas_VALUE) {
        if (cuntas_VALUE == 40) return "java/lang/InterruptedException";
        if (cuntas_VALUE == 41) return "Gaeilge/자체/대기중단예외";
        if (cuntas_VALUE == 39) return "java/net/SocketException";
        if (cuntas_VALUE == 20) return "Gaeilge/자체/eisceacht";
        if (cuntas_VALUE == 21) return "Gaeilge/자체/실행예외";
        if (cuntas_VALUE == 22) return "Gaeilge/자체/I_O_eisceacht";
        if (cuntas_VALUE == 23) return "Gaeilge/자체/대기시간초과예외";
        if (cuntas_VALUE == 24) return "Gaeilge/자체/ADDRESS_LOOKUP_eisceacht";
        if (cuntas_VALUE == 25) return "Gaeilge/자체/파일없음예외";
        if (cuntas_VALUE == 26) return "Gaeilge/자체/통신예외";
        if (cuntas_VALUE == 27) return "Gaeilge/자체/neamhbhailí_argóint_eisceacht";
        if (cuntas_VALUE == 28) return "Gaeilge/자체/숫자형식예외";
        if (cuntas_VALUE == 29) return "Gaeilge/자체/범위예외";
        if (cuntas_VALUE == 30) return "Gaeilge/자체/배열범위예외";
        if (cuntas_VALUE == 31) return "Gaeilge/자체/문자열범위예외";
        if (cuntas_VALUE == 32) return "Gaeilge/자체/NULL_Leabhair_thagartha_eisceacht";
        if (cuntas_VALUE == 33) return "Gaeilge/자체/산술예외";
        if (cuntas_VALUE == 34) return "Gaeilge/자체/staid_eisceacht";
        if (cuntas_VALUE == 35) return "Gaeilge/자체/TYPE_craol_eisceacht";
        if (cuntas_VALUE == 36) return "Gaeilge/자체/음수배열크기예외";
        if (cuntas_VALUE == 37) return "Gaeilge/자체/ARRAY_Store_teip";
        if (cuntas_VALUE == 38) return "Gaeilge/자체/snáithe_staid_eisceacht";
        if (cuntas_VALUE == 1) return "java/lang/Throwable"; if (cuntas_VALUE == 2) return "java/lang/Exception";
        if (cuntas_VALUE == 3) return "java/lang/RuntimeException"; if (cuntas_VALUE == 4) return "java/lang/ArithmeticException";
        if (cuntas_VALUE == 5) return "java/lang/NullPointerException"; if (cuntas_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (cuntas_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (cuntas_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (cuntas_VALUE == 9) return "java/lang/IllegalArgumentException"; if (cuntas_VALUE == 10) return "java/lang/NumberFormatException";
        if (cuntas_VALUE == 11) return "java/io/IOException"; if (cuntas_VALUE == 12) return "java/io/FileNotFoundException";
        if (cuntas_VALUE == 17) return "java/lang/ArrayStoreException";
        if (cuntas_VALUE == 18) return "java/net/UnknownHostException";
        if (cuntas_VALUE == 19) return "java/net/SocketTimeoutException";
        if (cuntas_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (cuntas_VALUE == 13) return "java/lang/IllegalStateException"; if (cuntas_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int cuntas_VALUE) {
        if (cuntas_VALUE == 40) return 2;
        if (cuntas_VALUE == 41) return 40;
        if (cuntas_VALUE == 39) return 11;
        if (cuntas_VALUE == 1) return 0;
        if (cuntas_VALUE == 2) return 1;
        if (cuntas_VALUE == 3) return 2;
        if (cuntas_VALUE == 4) return 3;
        if (cuntas_VALUE == 5) return 3;
        if (cuntas_VALUE == 6) return 3;
        if (cuntas_VALUE == 7) return 6;
        if (cuntas_VALUE == 8) return 6;
        if (cuntas_VALUE == 9) return 3;
        if (cuntas_VALUE == 10) return 9;
        if (cuntas_VALUE == 11) return 2;
        if (cuntas_VALUE == 12) return 11;
        if (cuntas_VALUE == 13) return 3;
        if (cuntas_VALUE == 14) return 3;
        if (cuntas_VALUE == 15) return 3;
        if (cuntas_VALUE == 16) return 9;
        if (cuntas_VALUE == 17) return 3;
        if (cuntas_VALUE == 18) return 11;
        if (cuntas_VALUE == 19) return 11;
        if (cuntas_VALUE == 20) return 2;
        if (cuntas_VALUE == 21) return 3;
        if (cuntas_VALUE == 22) return 11;
        if (cuntas_VALUE == 23) return 22;
        if (cuntas_VALUE == 24) return 22;
        if (cuntas_VALUE == 25) return 22;
        if (cuntas_VALUE == 26) return 22;
        if (cuntas_VALUE == 27) return 9;
        if (cuntas_VALUE == 28) return 27;
        if (cuntas_VALUE == 29) return 6;
        if (cuntas_VALUE == 30) return 29;
        if (cuntas_VALUE == 31) return 29;
        if (cuntas_VALUE == 32) return 5;
        if (cuntas_VALUE == 33) return 4;
        if (cuntas_VALUE == 34) return 13;
        if (cuntas_VALUE == 35) return 14;
        if (cuntas_VALUE == 36) return 15;
        if (cuntas_VALUE == 37) return 17;
        if (cuntas_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int iarbhír_VALUE, int 요구값) {
        for (int 깊이 = 0; iarbhír_VALUE != 0 && 깊이 < 16; 깊이++, iarbhír_VALUE = 예외부모(iarbhír_VALUE))
            if (iarbhír_VALUE == 요구값) return true;
        return false;
    }
    static void 예외던짐(int cuntas_VALUE, String LÉIGHMÉ_Leabhair_thagartha) {
        int oibiacht_Leabhair_thagartha = 새기억(9, 2); if (ERREÁID) return;
        힙[oibiacht_Leabhair_thagartha + 2] = cuntas_VALUE; 힙[oibiacht_Leabhair_thagartha + 3] = óstach_carachtar(LÉIGHMÉ_Leabhair_thagartha); 힙참조[oibiacht_Leabhair_thagartha + 3] = 1;
        던진객체 = oibiacht_Leabhair_thagartha; ERREÁID = true;
    }
    static boolean 맞는객체(int oibiacht_Leabhair_thagartha, int Ainm) {
        if (oibiacht_Leabhair_thagartha == 0) return true;
        if (!객체유효(oibiacht_Leabhair_thagartha)) return false;
        int catagóir_CODE = 힙[oibiacht_Leabhair_thagartha];
        if (Word_SMS(Ainm, "java/lang/Object")) return true;
        if (catagóir_CODE >= 32) return 종포함(catagóir_CODE - 32, Ainm);
        if (catagóir_CODE == 9) { int sprioc_ADDRESS = eisceacht_tairiseach(Ainm); return sprioc_ADDRESS != 0 && 예외포함(힙[oibiacht_Leabhair_thagartha + 2], sprioc_ADDRESS); }
        if (catagóir_CODE == 1) return Word_SMS(Ainm, "java/lang/String") || Word_SMS(Ainm, "java/lang/CharSequence");
        if (catagóir_CODE == 4) return Word_SMS(Ainm, "java/lang/StringBuilder") || Word_SMS(Ainm, "java/lang/CharSequence");
        if (catagóir_CODE == 10) return Word_SMS(Ainm, "java/util/ArrayList") || Word_SMS(Ainm, "java/util/List");
        if (catagóir_CODE == 11) return Word_SMS(Ainm, "java/util/HashMap") || Word_SMS(Ainm, "java/util/Map");
        if (catagóir_CODE == 12) return Word_SMS(Ainm, "java/lang/Integer") || Word_SMS(Ainm, "java/lang/Number");
        if (catagóir_CODE >= 24 && catagóir_CODE <= 28 && 힙[oibiacht_Leabhair_thagartha + 13] != 0) return 한국어화면종(Ainm) == catagóir_CODE || Word_SMS(Ainm, "Gaeilge/자체/화면구성요소");
        if (catagóir_CODE >= 24 && catagóir_CODE <= 28) return (한국어화면종(Ainm) == 0 && 화면종(Ainm) == catagóir_CODE) || Word_SMS(Ainm, "java/awt/Component") || Word_SMS(Ainm, "java/awt/Container") || Word_SMS(Ainm, "javax/swing/JComponent");
        if (catagóir_CODE == 29) return Word_SMS(Ainm, 힙[oibiacht_Leabhair_thagartha + 3] != 0 ? "Gaeilge/자체/동작알림" : "java/awt/event/ActionEvent");
        if (catagóir_CODE == 30) return Word_SMS(Ainm, "java/awt/FlowLayout") || Word_SMS(Ainm, "java/awt/LayoutManager");
        if (catagóir_CODE == 17) return Word_SMS(Ainm, "java/net/Socket");
        if (catagóir_CODE == 18) return Word_SMS(Ainm, "java/net/ServerSocket");
        if (catagóir_CODE == 19) return Word_SMS(Ainm, 힙[oibiacht_Leabhair_thagartha + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (catagóir_CODE == 14) return Word_SMS(Ainm, "java/net/InetAddress");
        if (catagóir_CODE == 15) return Word_SMS(Ainm, "java/net/DatagramSocket");
        if (catagóir_CODE == 16) return Word_SMS(Ainm, "java/net/DatagramPacket");
        if (catagóir_CODE == 13) return Word_SMS(Ainm, 힙[oibiacht_Leabhair_thagartha + 3] != 0 ? "Gaeilge/자체/작업가닥" : "java/lang/Thread");
        if (catagóir_CODE == 2) return Word_SMS(Ainm, "[I"); if (catagóir_CODE == 20) return Word_SMS(Ainm, "[B"); if (catagóir_CODE == 21) return Word_SMS(Ainm, "[Z");
        if (catagóir_CODE == 22) return Word_SMS(Ainm, "[C"); if (catagóir_CODE == 23) return Word_SMS(Ainm, "[S");
        if (catagóir_CODE != 3) return false;
        if (Word_SMS(Ainm, "[Ljava/lang/Object;")) return true;
        int comhpháirt = ARRAY_eilimint[oibiacht_Leabhair_thagartha];
        if (comhpháirt == -1) return Word_SMS(Ainm, "[Ljava/lang/String;") || Word_SMS(Ainm, "[Ljava/lang/CharSequence;");
        if (comhpháirt == 0) return false;
        if (배열종비교(comhpháirt, Ainm)) return true;
        if ((Word_SMS(comhpháirt, "java/lang/String") || Word_SMS(comhpháirt, "java/lang/StringBuilder")) && Word_SMS(Ainm, "[Ljava/lang/CharSequence;")) return true;
        for (int lúb_INDEX = 0; lúb_INDEX < aicme_Sainmhíniú_COUNT; lúb_INDEX++) if (같은말(aicme_Sainmhíniú_ainm[lúb_INDEX], comhpháirt)) {
            for (int pointe_cóid = lúb_INDEX, 중첩깊이 = 0; pointe_cóid >= 0 && 중첩깊이 < 16; 중첩깊이++, pointe_cóid = 부모종(pointe_cóid)) {
                if (배열종비교(종부모[pointe_cóid], Ainm)) return true;
                for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < aicme_comhéadan_COUNT[pointe_cóid]; comhcheangal_istigh_suíomh++) if (배열종비교(aicme_comhéadan[pointe_cóid * 16 + comhcheangal_istigh_suíomh], Ainm)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int ainm_tairiseach, int 형식참조) {
        int seic_suíomh = 상가[형식참조], iontráil_COUNT = tairiseach_SECOND_VALUE[형식참조];
        if (ainm_tairiseach == 0 || iontráil_COUNT < 4 || Comhad[seic_suíomh] != '[' || Comhad[seic_suíomh + 1] != 'L' || Comhad[seic_suíomh + iontráil_COUNT - 1] != ';' || tairiseach_SECOND_VALUE[ainm_tairiseach] != iontráil_COUNT - 3) return false;
        for (int lúb_INDEX = 0; lúb_INDEX < iontráil_COUNT - 3; lúb_INDEX++) if (Comhad[상가[ainm_tairiseach] + lúb_INDEX] != Comhad[seic_suíomh + 2 + lúb_INDEX]) return false;
        return true;
    }
    static void hanla_eisceacht() {
        if (던진객체 == 0) return;
        ERREÁID = false;
        while (fráma_INDEX >= 현재가닥 * 32) {
            int comhad_INDEX = fráma_modh[fráma_INDEX], 읽는자리 = fráma_treoir[fráma_INDEX];
            for (int lúb_INDEX = 0; lúb_INDEX < 잡기수; lúb_INDEX++) if (잡기함수[lúb_INDEX] == comhad_INDEX && 읽는자리 >= 잡기시작[lúb_INDEX] && 읽는자리 < 잡기끝[lúb_INDEX]
                && (잡기종[lúb_INDEX] == 0 || 맞는객체(던진객체, 잡기종[lúb_INDEX]))) {
                fráma_suíomh[fráma_INDEX] = 잡기위치[lúb_INDEX]; fráma_Cruach[fráma_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (túsaigh_fráma[fráma_INDEX] != 0) aicme_Sainmhíniú_staid[túsaigh_fráma[fráma_INDEX] - 1] = 3;
            if (틀잠금[fráma_INDEX] != 0) { 잠금풀기(틀잠금[fráma_INDEX]); 틀잠금[fráma_INDEX] = 0; }
            fráma_INDEX--;
        }
        úsáideoir.Scríobh("Uncaught ");
        if (힙[던진객체] == 9) { úsáideoir.Scríobh(eisceacht_ainm(힙[던진객체 + 2])); úsáideoir.Scríobh(": "); scríobh_SMS(힙[던진객체 + 3]); }
        else úsáideoir.Scríobh("user exception");
        úsáideoir.scríobh_carachtar_VALUE(10); 던진객체 = 0; ERREÁID = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void Cruach_treoir(int ordú_CODE) {
        int 첫값 = 빼기(0), 첫형식 = return_TYPE;
        if (ordú_CODE == 87) return;
        if (ordú_CODE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int beart_sonraí = 빼기(0), SECOND_formáid = return_TYPE;
        if (ordú_CODE == 88) return;
        if (ordú_CODE == 90) { 넣기(첫값, 첫형식); 넣기(beart_sonraí, SECOND_formáid); 넣기(첫값, 첫형식); return; }
        if (ordú_CODE == 92) { 넣기(beart_sonraí, SECOND_formáid); 넣기(첫값, 첫형식); 넣기(beart_sonraí, SECOND_formáid); 넣기(첫값, 첫형식); return; }
        if (ordú_CODE == 95) { 넣기(첫값, 첫형식); 넣기(beart_sonraí, SECOND_formáid); return; }
        int pointe_cóid = 빼기(0), 셋째형식 = return_TYPE;
        if (ordú_CODE == 91) { 넣기(첫값, 첫형식); 넣기(pointe_cóid, 셋째형식); 넣기(beart_sonraí, SECOND_formáid); 넣기(첫값, 첫형식); return; }
        if (ordú_CODE == 93) { 넣기(beart_sonraí, SECOND_formáid); 넣기(첫값, 첫형식); 넣기(pointe_cóid, 셋째형식); 넣기(beart_sonraí, SECOND_formáid); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = return_TYPE;
        넣기(beart_sonraí, SECOND_formáid); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(pointe_cóid, 셋째형식); 넣기(beart_sonraí, SECOND_formáid); 넣기(첫값, 첫형식);
    }
    static void 새객체(int ainm_tairiseach, int 시작점) {
        int catagóir_CODE = 0, 유효길이 = 0, eisceacht_Leabhair_thagartha = eisceacht_tairiseach(ainm_tairiseach);
        if (Word_SMS(ainm_tairiseach, "java/lang/StringBuilder")) { catagóir_CODE = 4; 유효길이 = 1; }
        if (Word_SMS(ainm_tairiseach, "java/io/FileInputStream")) { catagóir_CODE = 5; 유효길이 = 2; }
        if (Word_SMS(ainm_tairiseach, "java/io/FileOutputStream")) { catagóir_CODE = 6; 유효길이 = 2; }
        if (eisceacht_Leabhair_thagartha != 0) { catagóir_CODE = 9; 유효길이 = 2; }
        if (Word_SMS(ainm_tairiseach, "java/util/ArrayList")) { catagóir_CODE = 10; 유효길이 = 2; }
        if (Word_SMS(ainm_tairiseach, "java/util/HashMap")) { catagóir_CODE = 11; 유효길이 = 2; }
        if (Word_SMS(ainm_tairiseach, "java/lang/Integer")) { catagóir_CODE = 12; 유효길이 = 1; }
        if (Word_SMS(ainm_tairiseach, "java/net/Socket")) { catagóir_CODE = 17; 유효길이 = 5; }
        if (Word_SMS(ainm_tairiseach, "java/net/ServerSocket")) { catagóir_CODE = 18; 유효길이 = 5; }
        if (Word_SMS(ainm_tairiseach, "java/net/DatagramSocket")) { catagóir_CODE = 15; 유효길이 = 3; }
        if (Word_SMS(ainm_tairiseach, "java/net/DatagramPacket")) { catagóir_CODE = 16; 유효길이 = 4; }
        if (Word_SMS(ainm_tairiseach, "java/lang/Thread") || Word_SMS(ainm_tairiseach, "Gaeilge/자체/작업가닥")) { catagóir_CODE = 13; 유효길이 = 2; }
        if (Word_SMS(ainm_tairiseach, "java/lang/Object")) { catagóir_CODE = 8; }
        if (catagóir_CODE == 0 && 화면종(ainm_tairiseach) != 0) { catagóir_CODE = 화면종(ainm_tairiseach); 유효길이 = 12; }
        if (catagóir_CODE == 0) {
            int pointe_cóid = FIND_aicme_Sainmhíniú(ainm_tairiseach); if (pointe_cóid < 0 || ERREÁID || !túsaigh(pointe_cóid, 시작점)) return;
            catagóir_CODE = 32 + pointe_cóid; 유효길이 = aicme_spás_COUNT[pointe_cóid];
        }
        int oibiacht_Leabhair_thagartha = leithdháil_Stóras(catagóir_CODE, 유효길이); if (ERREÁID) return;
        if (catagóir_CODE == 13 && Word_SMS(ainm_tairiseach, "Gaeilge/자체/작업가닥")) 힙[oibiacht_Leabhair_thagartha + 3] = 1;
        if (catagóir_CODE >= 24 && catagóir_CODE <= 28 && 한국어화면종(ainm_tairiseach) != 0) 힙[oibiacht_Leabhair_thagartha + 13] = 1;
        if (catagóir_CODE == 5 || catagóir_CODE == 6 || catagóir_CODE == 15 || catagóir_CODE == 17 || catagóir_CODE == 18) 힙[oibiacht_Leabhair_thagartha + 2] = -1;
        if (catagóir_CODE == 9) 힙[oibiacht_Leabhair_thagartha + 2] = eisceacht_Leabhair_thagartha;
        넣기(oibiacht_Leabhair_thagartha, 2);
    }
    static boolean 값같음(int 첫값, int beart_sonraí) {
        if (첫값 == beart_sonraí) return true;
        if (첫값 == 0 || beart_sonraí == 0 || 첫값 < 0 || beart_sonraí < 0 || 첫값 >= 힙끝 || beart_sonraí >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[beart_sonraí] == 1) return 글같음(첫값, beart_sonraí, false);
        return 힙[첫값] == 12 && 힙[beart_sonraí] == 12 && 힙[첫값 + 2] == 힙[beart_sonraí + 2];
    }
    static int 글조각(int oibiacht_Leabhair_thagartha, int Start_suíomh, int cuir_deireadh_le_suíomh) {
        if (!oibiacht_VALUE(oibiacht_Leabhair_thagartha, 1)) return 0;
        if (Start_suíomh < 0 || cuir_deireadh_le_suíomh < Start_suíomh || cuir_deireadh_le_suíomh > 힙[oibiacht_Leabhair_thagartha + 1]) { teip_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = leithdháil_Stóras(1, cuir_deireadh_le_suíomh - Start_suíomh); if (ERREÁID) return 0;
        for (int lúb_INDEX = Start_suíomh; lúb_INDEX < cuir_deireadh_le_suíomh; lúb_INDEX++) 힙[반환값 + 2 + lúb_INDEX - Start_suíomh] = 힙[oibiacht_Leabhair_thagartha + 2 + lúb_INDEX];
        return 반환값;
    }
    static int comhcheangal_SMS(int 첫값, int beart_sonraí) {
        if (!oibiacht_VALUE(첫값, 1) || !oibiacht_VALUE(beart_sonraí, 1)) return 0;
        int iontráil_COUNT = 힙[첫값 + 1], modh_INDEX = 힙[beart_sonraí + 1], 반환값 = leithdháil_Stóras(1, iontráil_COUNT + modh_INDEX); if (ERREÁID) return 0;
        for (int lúb_INDEX = 0; lúb_INDEX < iontráil_COUNT; lúb_INDEX++) 힙[반환값 + 2 + lúb_INDEX] = 힙[첫값 + 2 + lúb_INDEX];
        for (int lúb_INDEX = 0; lúb_INDEX < modh_INDEX; lúb_INDEX++) 힙[반환값 + 2 + iontráil_COUNT + lúb_INDEX] = 힙[beart_sonraí + 2 + lúb_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int úinéir, int ainm_tairiseach, int 서술상수, int ordú_CODE) {
        if (Word_SMS(úinéir, "Gaeilge/자체/실행인수") && ordú_CODE == 184) {
            if (Word_SMS(ainm_tairiseach, "mír_COUNT") && Word_SMS(서술상수, "()I")) { 넣기(úsáideoir.인수개수() - 1, 1); return true; }
            if (Word_SMS(ainm_tairiseach, "Téacs") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= úsáideoir.인수개수() - 1) 예외던짐(29, "Rith_ordú Argóintí 범위를 벗어났습니다");
                else 넣기(óstach_carachtar(úsáideoir.Argóintí(순번 + 1)), 2);
                return true;
            }
            teip_VALUE("지원하지 않는 Gaeilge Rith_ordú Argóintí 호출"); return true;
        }
        if (Word_SMS(úinéir, "Gaeilge/자체/작업가닥")) { Próiseas_snáithe(ainm_tairiseach, 서술상수, ordú_CODE, true); return true; }
        if (한국어화면소유(úinéir)) { 한국어화면호출(úinéir, ainm_tairiseach, 서술상수, ordú_CODE); return true; }
        if (화면소유(úinéir)) { 화면호출(úinéir, ainm_tairiseach, 서술상수, ordú_CODE); return true; }
        if (Word_SMS(úinéir, "java/net/Socket") || Word_SMS(úinéir, "java/net/ServerSocket") || Word_SMS(úinéir, "java/io/InputStream") || Word_SMS(úinéir, "java/io/OutputStream")) { 흐름호출(úinéir, ainm_tairiseach, 서술상수, ordú_CODE); return true; }
        if (Word_SMS(úinéir, "Gaeilge/자체/eithne_VALUE") && ordú_CODE == 184) {
            if (Word_SMS(ainm_tairiseach, "화면너비") && Word_SMS(서술상수, "()I")) { 넣기(úsáideoir.화면너비(), 1); return true; }
            if (Word_SMS(ainm_tairiseach, "화면높이") && Word_SMS(서술상수, "()I")) { 넣기(úsáideoir.화면높이(), 1); return true; }
            if (Word_SMS(ainm_tairiseach, "밀리초") && Word_SMS(서술상수, "()I")) { 넣기(úsáideoir.밀리초(), 1); return true; }
            if (Word_SMS(ainm_tairiseach, "그림대기") && Word_SMS(서술상수, "()I")) { 넣기(úsáideoir.그림대기(), 1); return true; }
            if (Word_SMS(ainm_tairiseach, "사각형") && Word_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), x_chomhordanáid = 빼기(1); 넣기(úsáideoir.사각형(x_chomhordanáid, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_SMS(úinéir, "java/net/InetAddress") || Word_SMS(úinéir, "java/net/DatagramPacket") || Word_SMS(úinéir, "java/net/DatagramSocket")) { 통신호출(úinéir, ainm_tairiseach, 서술상수, ordú_CODE); return true; }
        if (Word_SMS(úinéir, "java/lang/Thread")) { 가닥호출(ainm_tairiseach, 서술상수, ordú_CODE); return true; }
        if (Word_SMS(úinéir, "java/lang/Object")) {
            if (Word_SMS(ainm_tairiseach, "<init>") && Word_SMS(서술상수, "()V") && ordú_CODE == 183) { 객체유효(빼기(2)); return true; }
            if (Word_SMS(ainm_tairiseach, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int beart_sonraí = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == beart_sonraí ? 1 : 0, 1); return true; }
        }
        if (eisceacht_tairiseach(úinéir) != 0) {
            if (Word_SMS(ainm_tairiseach, "<init>") && ordú_CODE == 183 && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int leid = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), oibiacht_Leabhair_thagartha = 빼기(2);
                if (oibiacht_VALUE(oibiacht_Leabhair_thagartha, 9)) { 힙[oibiacht_Leabhair_thagartha + 3] = leid; 힙참조[oibiacht_Leabhair_thagartha + 3] = 1; } return true;
            }
            if ((Word_SMS(ainm_tairiseach, "getMessage") || Word_SMS(ainm_tairiseach, "설명")) && Word_SMS(서술상수, "()Ljava/lang/String;")) { int oibiacht_Leabhair_thagartha = 빼기(2); if (oibiacht_VALUE(oibiacht_Leabhair_thagartha, 9)) 넣기(힙[oibiacht_Leabhair_thagartha + 3], 2); return true; }
        }
        if (Word_SMS(úinéir, "java/lang/String")) {
            if (ordú_CODE == 182 && Word_SMS(ainm_tairiseach, "getBytes") && (Word_SMS(서술상수, "()[B") || Word_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int ionchódú_ainm = Word_SMS(서술상수, "()[B") ? 0 : 빼기(2), oibiacht_Leabhair_thagartha = 빼기(2);
                if (!oibiacht_VALUE(oibiacht_Leabhair_thagartha, 1)) return true;
                if (ionchódú_ainm != 0 && !글같음(ionchódú_ainm, óstach_carachtar("UTF-8"), false) && !글같음(ionchódú_ainm, óstach_carachtar("UTF8"), false) && !글같음(ionchódú_ainm, óstach_carachtar("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int iontráil_COUNT = 힙[oibiacht_Leabhair_thagartha + 1], 반환값 = leithdháil_Stóras(20, iontráil_COUNT * 3), 사용수 = 0; if (ERREÁID) return true;
                for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < iontráil_COUNT; comhcheangal_istigh_suíomh++) {
                    int pointe_cóid = 힙[oibiacht_Leabhair_thagartha + 2 + comhcheangal_istigh_suíomh];
                    if (pointe_cóid >= 0xd800 && pointe_cóid <= 0xdbff && comhcheangal_istigh_suíomh + 1 < iontráil_COUNT && 힙[oibiacht_Leabhair_thagartha + 3 + comhcheangal_istigh_suíomh] >= 0xdc00 && 힙[oibiacht_Leabhair_thagartha + 3 + comhcheangal_istigh_suíomh] <= 0xdfff) pointe_cóid = 0x10000 + ((pointe_cóid - 0xd800) << 10) + 힙[oibiacht_Leabhair_thagartha + 2 + ++comhcheangal_istigh_suíomh] - 0xdc00;
                    else if (pointe_cóid >= 0xd800 && pointe_cóid <= 0xdfff) pointe_cóid = '?';
                    if (pointe_cóid < 128) 힙[반환값 + 2 + 사용수++] = pointe_cóid;
                    else { int beart_COUNT = pointe_cóid < 2048 ? 2 : pointe_cóid < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((beart_COUNT == 2 ? 192 : beart_COUNT == 3 ? 224 : 240) | pointe_cóid >> (6 * (beart_COUNT - 1))); for (int 비교자리 = beart_COUNT - 1; 비교자리 > 0; 비교자리--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | pointe_cóid >> (6 * (비교자리 - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (ordú_CODE == 184 && Word_SMS(ainm_tairiseach, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(digit_carachtar(빼기(1)), 2); return true; }
            if (ordú_CODE != 182) return false;
            if (Word_SMS(ainm_tairiseach, "equals") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int beart_sonraí = 빼기(2), 첫값 = 빼기(2); if (oibiacht_VALUE(첫값, 1)) 넣기(글같음(첫값, beart_sonraí, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(ainm_tairiseach, "isEmpty") && Word_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (oibiacht_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(ainm_tairiseach, "substring") && (Word_SMS(서술상수, "(I)Ljava/lang/String;") || Word_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_SMS(서술상수, "(II)Ljava/lang/String;"); int cuir_deireadh_le_suíomh = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (oibiacht_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? cuir_deireadh_le_suíomh : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(ainm_tairiseach, "concat") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int beart_sonraí = 빼기(2), 첫값 = 빼기(2); 넣기(comhcheangal_SMS(첫값, beart_sonraí), 2); return true; }
            if (Word_SMS(ainm_tairiseach, "hashCode") && Word_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), hais_VALUE = 0; if (oibiacht_VALUE(첫값, 1)) { for (int lúb_INDEX = 0; lúb_INDEX < 힙[첫값 + 1]; lúb_INDEX++) hais_VALUE = hais_VALUE * 31 + 힙[첫값 + 2 + lúb_INDEX]; 넣기(hais_VALUE, 1); } return true; }
            if (Word_SMS(ainm_tairiseach, "toString") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (oibiacht_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(úinéir, "java/lang/Integer")) {
            if (ordú_CODE == 184 && Word_SMS(ainm_tairiseach, "valueOf") && Word_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int sonraí_VALUE = 빼기(1), oibiacht_Leabhair_thagartha = sonraí_VALUE >= -128 && sonraí_VALUE <= 127 ? Store_slánuimhir[sonraí_VALUE + 128] : 0; if (oibiacht_Leabhair_thagartha == 0) { oibiacht_Leabhair_thagartha = leithdháil_Stóras(12, 1); if (!ERREÁID) { 힙[oibiacht_Leabhair_thagartha + 2] = sonraí_VALUE; if (sonraí_VALUE >= -128 && sonraí_VALUE <= 127) Store_slánuimhir[sonraí_VALUE + 128] = oibiacht_Leabhair_thagartha; } } 넣기(oibiacht_Leabhair_thagartha, 2); return true; }
            if (ordú_CODE == 183 && Word_SMS(ainm_tairiseach, "<init>") && Word_SMS(서술상수, "(I)V")) { int sonraí_VALUE = 빼기(1), oibiacht_Leabhair_thagartha = 빼기(2); if (oibiacht_VALUE(oibiacht_Leabhair_thagartha, 12)) 힙[oibiacht_Leabhair_thagartha + 2] = sonraí_VALUE; return true; }
            if (ordú_CODE == 182 && Word_SMS(ainm_tairiseach, "intValue") && Word_SMS(서술상수, "()I")) { int oibiacht_Leabhair_thagartha = 빼기(2); if (oibiacht_VALUE(oibiacht_Leabhair_thagartha, 12)) 넣기(힙[oibiacht_Leabhair_thagartha + 2], 1); return true; }
            if (ordú_CODE == 184 && Word_SMS(ainm_tairiseach, "toString") && Word_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(digit_carachtar(빼기(1)), 2); return true; }
        }
        if (Word_SMS(úinéir, "java/lang/Math") && ordú_CODE == 184) {
            if (Word_SMS(ainm_tairiseach, "abs") && Word_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(ainm_tairiseach, "min") || Word_SMS(ainm_tairiseach, "max")) && Word_SMS(서술상수, "(II)I")) { int beart_sonraí = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(ainm_tairiseach, "min") ? (첫값 < beart_sonraí ? 첫값 : beart_sonraí) : (첫값 > beart_sonraí ? 첫값 : beart_sonraí), 1); return true; }
        }
        if (Word_SMS(úinéir, "java/lang/System") && ordú_CODE == 184) {
            if (Word_SMS(ainm_tairiseach, "gc") && Word_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Word_SMS(ainm_tairiseach, "arraycopy") && Word_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int iontráil_COUNT = 빼기(1), sprioc_VALUE_INDEX = 빼기(1), beart_sonraí = 빼기(2), Start_suíomh = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(beart_sonraí)) {
                    int catagóir_CODE = 힙[첫값];
                    if (힙[beart_sonraí] != catagóir_CODE || (catagóir_CODE != 2 && catagóir_CODE != 3 && (catagóir_CODE < 20 || catagóir_CODE > 23))) teip_VALUE("arraycopy type mismatch");
                    else if (iontráil_COUNT < 0 || Start_suíomh < 0 || sprioc_VALUE_INDEX < 0 || Start_suíomh > 힙[첫값 + 1] - iontráil_COUNT || sprioc_VALUE_INDEX > 힙[beart_sonraí + 1] - iontráil_COUNT) teip_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == beart_sonraí && sprioc_VALUE_INDEX > Start_suíomh) { for (int lúb_INDEX = iontráil_COUNT - 1; lúb_INDEX >= 0; lúb_INDEX--) 힙[beart_sonraí + 2 + sprioc_VALUE_INDEX + lúb_INDEX] = 힙[첫값 + 2 + Start_suíomh + lúb_INDEX]; }
                    else { for (int lúb_INDEX = 0; lúb_INDEX < iontráil_COUNT && !ERREÁID; lúb_INDEX++) { int sonraí_VALUE = 힙[첫값 + 2 + Start_suíomh + lúb_INDEX]; if (catagóir_CODE != 3 || 배열저장가능(beart_sonraí, sonraí_VALUE)) 힙[beart_sonraí + 2 + sprioc_VALUE_INDEX + lúb_INDEX] = sonraí_VALUE; } }
                }
                return true;
            }
        }
        if (Word_SMS(úinéir, "java/util/ArrayList") || Word_SMS(úinéir, "java/util/List") || Word_SMS(úinéir, "java/util/HashMap") || Word_SMS(úinéir, "java/util/Map")) {
            모음호출(úinéir, ainm_tairiseach, 서술상수, ordú_CODE); return true;
        }
        return false;
    }
    static void 모음늘리기(int oibiacht_Leabhair_thagartha, int 필요수) {
        int 이전값 = 힙[oibiacht_Leabhair_thagartha + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int Ar_aghaidh_suíomh = 용량값 < 8 ? 8 : 용량값 * 2; if (Ar_aghaidh_suíomh < 필요수) Ar_aghaidh_suíomh = 필요수;
        int sonraí_ARRAY = leithdháil_Stóras(3, Ar_aghaidh_suíomh); if (ERREÁID) return;
        for (int lúb_INDEX = 0; lúb_INDEX < 용량값; lúb_INDEX++) 힙[sonraí_ARRAY + 2 + lúb_INDEX] = 힙[이전값 + 2 + lúb_INDEX];
        힙[oibiacht_Leabhair_thagartha + 2] = sonraí_ARRAY; 힙참조[oibiacht_Leabhair_thagartha + 2] = 1;
    }
    static void 모음호출(int úinéir, int ainm_tairiseach, int 서술상수, int ordú_CODE) {
        boolean 대응참조 = Word_SMS(úinéir, "java/util/HashMap") || Word_SMS(úinéir, "java/util/Map"); int catagóir_CODE = 대응참조 ? 11 : 10;
        if (Word_SMS(ainm_tairiseach, "<init>") && ordú_CODE == 183 && Word_SMS(서술상수, "()V")) { int oibiacht_Leabhair_thagartha = 빼기(2); if (oibiacht_VALUE(oibiacht_Leabhair_thagartha, catagóir_CODE)) 모음늘리기(oibiacht_Leabhair_thagartha, 8); return; }
        if (ordú_CODE != 182 && ordú_CODE != 185) { teip_VALUE("invalid collection invocation"); return; }
        if (Word_SMS(ainm_tairiseach, "size") && Word_SMS(서술상수, "()I") || Word_SMS(ainm_tairiseach, "isEmpty") && Word_SMS(서술상수, "()Z")) {
            int oibiacht_Leabhair_thagartha = 빼기(2); if (oibiacht_VALUE(oibiacht_Leabhair_thagartha, catagóir_CODE)) 넣기(Word_SMS(ainm_tairiseach, "size") ? 힙[oibiacht_Leabhair_thagartha + 3] : 힙[oibiacht_Leabhair_thagartha + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(ainm_tairiseach, "clear") && Word_SMS(서술상수, "()V")) { int oibiacht_Leabhair_thagartha = 빼기(2); if (oibiacht_VALUE(oibiacht_Leabhair_thagartha, catagóir_CODE)) { int sonraí_ARRAY = 힙[oibiacht_Leabhair_thagartha + 2]; for (int lúb_INDEX = 0; lúb_INDEX < 힙[sonraí_ARRAY + 1]; lúb_INDEX++) 힙[sonraí_ARRAY + 2 + lúb_INDEX] = 0; 힙[oibiacht_Leabhair_thagartha + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(ainm_tairiseach, "add") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int sonraí_VALUE = 빼기(2), oibiacht_Leabhair_thagartha = 빼기(2); if (!oibiacht_VALUE(oibiacht_Leabhair_thagartha, 10)) return;
            int iontráil_COUNT = 힙[oibiacht_Leabhair_thagartha + 3]; 모음늘리기(oibiacht_Leabhair_thagartha, iontráil_COUNT + 1); if (!ERREÁID) { 힙[힙[oibiacht_Leabhair_thagartha + 2] + 2 + iontráil_COUNT] = sonraí_VALUE; 힙[oibiacht_Leabhair_thagartha + 3] = iontráil_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(ainm_tairiseach, "get") || Word_SMS(ainm_tairiseach, "remove")) && Word_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(ainm_tairiseach, "set") && Word_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Word_SMS(ainm_tairiseach, "set"); int sonraí_VALUE = 지정여부 ? 빼기(2) : 0, iontráil_suíomh = 빼기(1), oibiacht_Leabhair_thagartha = 빼기(2);
            if (!oibiacht_VALUE(oibiacht_Leabhair_thagartha, 10)) return;
            int iontráil_COUNT = 힙[oibiacht_Leabhair_thagartha + 3], sonraí_ARRAY = 힙[oibiacht_Leabhair_thagartha + 2];
            if (iontráil_suíomh < 0 || iontráil_suíomh >= iontráil_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[sonraí_ARRAY + 2 + iontráil_suíomh];
            if (지정여부) 힙[sonraí_ARRAY + 2 + iontráil_suíomh] = sonraí_VALUE;
            if (Word_SMS(ainm_tairiseach, "remove")) { for (int lúb_INDEX = iontráil_suíomh + 1; lúb_INDEX < iontráil_COUNT; lúb_INDEX++) 힙[sonraí_ARRAY + 1 + lúb_INDEX] = 힙[sonraí_ARRAY + 2 + lúb_INDEX]; 힙[sonraí_ARRAY + 1 + iontráil_COUNT] = 0; 힙[oibiacht_Leabhair_thagartha + 3] = iontráil_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_SMS(ainm_tairiseach, "get") || Word_SMS(ainm_tairiseach, "remove")) && Word_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(ainm_tairiseach, "put") && Word_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(ainm_tairiseach, "containsKey") && Word_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(ainm_tairiseach, "put"), bain = Word_SMS(ainm_tairiseach, "remove");
            int sonraí_VALUE = 넣기여부 ? 빼기(2) : 0, eochair_Leabhair_thagartha = 빼기(2), oibiacht_Leabhair_thagartha = 빼기(2); if (!oibiacht_VALUE(oibiacht_Leabhair_thagartha, 11)) return;
            int iontráil_COUNT = 힙[oibiacht_Leabhair_thagartha + 3], sonraí_ARRAY = 힙[oibiacht_Leabhair_thagartha + 2], 찾은여부 = -1;
            for (int lúb_INDEX = 0; lúb_INDEX < iontráil_COUNT; lúb_INDEX++) if (값같음(eochair_Leabhair_thagartha, 힙[sonraí_ARRAY + 2 + 2 * lúb_INDEX])) { 찾은여부 = lúb_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[sonraí_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(oibiacht_Leabhair_thagartha, (iontráil_COUNT + 1) * 2); sonraí_ARRAY = 힙[oibiacht_Leabhair_thagartha + 2]; 찾은여부 = iontráil_COUNT; if (!ERREÁID) 힙[oibiacht_Leabhair_thagartha + 3] = iontráil_COUNT + 1; }
                if (!ERREÁID) { 힙[sonraí_ARRAY + 2 + 2 * 찾은여부] = eochair_Leabhair_thagartha; 힙[sonraí_ARRAY + 3 + 2 * 찾은여부] = sonraí_VALUE; }
            }
            if (bain && 찾은여부 >= 0) { for (int lúb_INDEX = 찾은여부 + 1; lúb_INDEX < iontráil_COUNT; lúb_INDEX++) { 힙[sonraí_ARRAY + 2 * lúb_INDEX] = 힙[sonraí_ARRAY + 2 + 2 * lúb_INDEX]; 힙[sonraí_ARRAY + 1 + 2 * lúb_INDEX] = 힙[sonraí_ARRAY + 3 + 2 * lúb_INDEX]; } 힙[sonraí_ARRAY + 2 * iontráil_COUNT] = 0; 힙[sonraí_ARRAY + 1 + 2 * iontráil_COUNT] = 0; 힙[oibiacht_Leabhair_thagartha + 3] = iontráil_COUNT - 1; }
            if (Word_SMS(ainm_tairiseach, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        teip_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int oibiacht_Leabhair_thagartha) {
        if (!객체유효(oibiacht_Leabhair_thagartha)) return false;
        if (잠금깊이[oibiacht_Leabhair_thagartha] != 0 && 잠금주인[oibiacht_Leabhair_thagartha] != 현재가닥 + 1) { athraigh_iarratas_HTTP = true; return false; }
        잠금주인[oibiacht_Leabhair_thagartha] = 현재가닥 + 1; 잠금깊이[oibiacht_Leabhair_thagartha]++; return true;
    }
    static void 잠금풀기(int oibiacht_Leabhair_thagartha) {
        if (!객체유효(oibiacht_Leabhair_thagartha)) return;
        if (잠금깊이[oibiacht_Leabhair_thagartha] == 0 || 잠금주인[oibiacht_Leabhair_thagartha] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[oibiacht_Leabhair_thagartha] == 0) 잠금주인[oibiacht_Leabhair_thagartha] = 0;
    }
    static boolean SWITCH_snáithe() {
        snáithe_fráma[현재가닥] = fráma_INDEX;
        if (fráma_INDEX < 현재가닥 * 32) snáithe_staid[현재가닥] = 3;
        for (int lúb_INDEX = 0; lúb_INDEX < snáithe_COUNT; lúb_INDEX++) if (snáithe_staid[lúb_INDEX] == 2 && snáithe_staid[가닥대기[lúb_INDEX]] == 3) snáithe_staid[lúb_INDEX] = 1;
        for (int lúb_INDEX = 1; lúb_INDEX <= snáithe_COUNT; lúb_INDEX++) {
            int Ar_aghaidh_suíomh = (현재가닥 + lúb_INDEX) % snáithe_COUNT;
            if (snáithe_staid[Ar_aghaidh_suíomh] == 1) { 현재가닥 = Ar_aghaidh_suíomh; fráma_INDEX = snáithe_fráma[Ar_aghaidh_suíomh]; athraigh_iarratas_HTTP = false; return true; }
        }
        for (int lúb_INDEX = 0; lúb_INDEX < snáithe_COUNT; lúb_INDEX++) if (snáithe_staid[lúb_INDEX] != 3) { teip_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int ainm_tairiseach, int 서술상수, int ordú_CODE) { Próiseas_snáithe(ainm_tairiseach, 서술상수, ordú_CODE, false); }
    static void Próiseas_snáithe(int ainm_tairiseach, int 서술상수, int ordú_CODE, boolean Gaeilge) {
        if (ordú_CODE == 184 && Word_SMS(ainm_tairiseach, Gaeilge ? "YIELD_tasc" : "yield") && Word_SMS(서술상수, "()V")) { athraigh_iarratas_HTTP = true; return; }
        if (ordú_CODE == 184 && Word_SMS(ainm_tairiseach, "currentThread") && Word_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(snáithe_oibiacht[현재가닥], 2); return; }
        if (ordú_CODE == 183 && Word_SMS(ainm_tairiseach, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, Gaeilge ? "(LGaeilge/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int sprioc_ADDRESS = Word_SMS(서술상수, "()V") ? 0 : 빼기(2), oibiacht_Leabhair_thagartha = 빼기(2);
            if (!객체유효(oibiacht_Leabhair_thagartha)) return;
            if (힙[oibiacht_Leabhair_thagartha] == 13) { 힙[oibiacht_Leabhair_thagartha + 2] = sprioc_ADDRESS; 힙참조[oibiacht_Leabhair_thagartha + 2] = 1; }
            else if (sprioc_ADDRESS != 0) teip_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (ordú_CODE == 182 && (Word_SMS(ainm_tairiseach, Gaeilge ? "Start_tasc" : "start") || Word_SMS(ainm_tairiseach, Gaeilge ? "기다리기" : "join")) && Word_SMS(서술상수, "()V") || ordú_CODE == 182 && Word_SMS(ainm_tairiseach, Gaeilge ? "살아있는가" : "isAlive") && Word_SMS(서술상수, "()Z")) {
            int oibiacht_Leabhair_thagartha = 빼기(2); if (!객체유효(oibiacht_Leabhair_thagartha)) return;
            int cuntas_VALUE = -1; for (int lúb_INDEX = 0; lúb_INDEX < snáithe_COUNT; lúb_INDEX++) if (snáithe_oibiacht[lúb_INDEX] == oibiacht_Leabhair_thagartha) cuntas_VALUE = lúb_INDEX;
            if (Word_SMS(ainm_tairiseach, Gaeilge ? "살아있는가" : "isAlive")) { 넣기(cuntas_VALUE >= 0 && snáithe_staid[cuntas_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(ainm_tairiseach, Gaeilge ? "기다리기" : "join")) { if (cuntas_VALUE >= 0 && snáithe_staid[cuntas_VALUE] != 3) { 가닥대기[현재가닥] = cuntas_VALUE; snáithe_staid[현재가닥] = 2; athraigh_iarratas_HTTP = true; } return; }
            if (cuntas_VALUE >= 0) { 예외던짐(Gaeilge ? 38 : 16, "thread already started"); return; }
            if (snáithe_COUNT == 4) { teip_VALUE("thread limit (4 including main)"); return; }
            int sprioc_ADDRESS = 힙[oibiacht_Leabhair_thagartha] == 13 ? 힙[oibiacht_Leabhair_thagartha + 2] : oibiacht_Leabhair_thagartha;
            int comhad_INDEX = sprioc_ADDRESS > 0 && 힙[sprioc_ADDRESS] >= 32 ? ainm_modh(힙[sprioc_ADDRESS] - 32, Gaeilge ? "Rith" : "run", "()V") : -1;
            if (sprioc_ADDRESS != 0 && comhad_INDEX < 0) { teip_VALUE("Runnable.run required"); return; }
            cuntas_VALUE = snáithe_COUNT++; snáithe_oibiacht[cuntas_VALUE] = oibiacht_Leabhair_thagartha; snáithe_sprioc[cuntas_VALUE] = sprioc_ADDRESS;
            int fráma = cuntas_VALUE * 32; snáithe_fráma[cuntas_VALUE] = comhad_INDEX < 0 ? fráma - 1 : fráma; snáithe_staid[cuntas_VALUE] = comhad_INDEX < 0 ? 3 : 1;
            if (comhad_INDEX >= 0) { fráma_modh[fráma] = comhad_INDEX; fráma_suíomh[fráma] = modh_Start[comhad_INDEX]; logánta_VALUE[fráma * 128] = sprioc_ADDRESS; logánta_TYPE[fráma * 128] = 2; }
            return;
        }
        teip_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], ADDRESS_SMS = new int[16];
    static int logánta_ADDRESS() { return ADDRESS_oibiacht(0x7f000001); }
    static int ADDRESS_oibiacht(int VALUE) { int oibiacht_Leabhair_thagartha = leithdháil_Stóras(14, 1); if (!ERREÁID) 힙[oibiacht_Leabhair_thagartha + 2] = VALUE; return oibiacht_Leabhair_thagartha; }
    static int 주소해독(int oibiacht_Leabhair_thagartha) {
        if (oibiacht_Leabhair_thagartha == 0 || 글같음(oibiacht_Leabhair_thagartha, óstach_carachtar("localhost"), false)) return 0x7f000001;
        if (!oibiacht_VALUE(oibiacht_Leabhair_thagartha, 1)) return 0;
        int sonraí_VALUE = 0, 총수 = 0, ADDRESS_beart = 0, 자릿수 = 0, iontráil_COUNT = 힙[oibiacht_Leabhair_thagartha + 1];
        for (int lúb_INDEX = 0; lúb_INDEX <= iontráil_COUNT; lúb_INDEX++) {
            int pointe_cóid = lúb_INDEX == iontráil_COUNT ? '.' : 힙[oibiacht_Leabhair_thagartha + 2 + lúb_INDEX];
            if (pointe_cóid == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } sonraí_VALUE = sonraí_VALUE << 8 | ADDRESS_beart; 총수++; ADDRESS_beart = 자릿수 = 0; }
            else { if (pointe_cóid < '0' || pointe_cóid > '9' || ++자릿수 > 3 || (ADDRESS_beart = ADDRESS_beart * 10 + pointe_cóid - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return sonraí_VALUE;
    }
    static int ADDRESS_carachtar(int sonraí_VALUE) {
        int iontráil_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int ADDRESS_beart = sonraí_VALUE >>> 이동비트 & 255;
            if (ADDRESS_beart >= 100) ADDRESS_SMS[iontráil_COUNT++] = '0' + ADDRESS_beart / 100;
            if (ADDRESS_beart >= 10) ADDRESS_SMS[iontráil_COUNT++] = '0' + ADDRESS_beart / 10 % 10;
            ADDRESS_SMS[iontráil_COUNT++] = '0' + ADDRESS_beart % 10; if (이동비트 != 0) ADDRESS_SMS[iontráil_COUNT++] = '.';
        }
        int oibiacht_Leabhair_thagartha = leithdháil_Stóras(1, iontráil_COUNT); if (!ERREÁID) for (int lúb_INDEX = 0; lúb_INDEX < iontráil_COUNT; lúb_INDEX++) 힙[oibiacht_Leabhair_thagartha + 2 + lúb_INDEX] = ADDRESS_SMS[lúb_INDEX]; return oibiacht_Leabhair_thagartha;
    }
    static void 통신호출(int úinéir, int ainm_tairiseach, int 서술상수, int ordú_CODE) {
        if (Word_SMS(úinéir, "java/net/InetAddress")) {
            if (ordú_CODE == 184 && Word_SMS(ainm_tairiseach, "getLoopbackAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(logánta_ADDRESS(), 2); return; }
            if (ordú_CODE == 184 && Word_SMS(ainm_tairiseach, "getByName") && Word_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int sonraí_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !ERREÁID) 넣기(ADDRESS_oibiacht(sonraí_VALUE), 2); return;
            }
            if (ordú_CODE == 182 && Word_SMS(ainm_tairiseach, "getHostAddress") && Word_SMS(서술상수, "()Ljava/lang/String;")) { int oibiacht_Leabhair_thagartha = 빼기(2); if (oibiacht_VALUE(oibiacht_Leabhair_thagartha, 14)) 넣기(ADDRESS_carachtar(힙[oibiacht_Leabhair_thagartha + 2]), 2); return; }
        }
        if (Word_SMS(úinéir, "java/net/DatagramPacket")) {
            if (ordú_CODE == 183 && Word_SMS(ainm_tairiseach, "<init>") && (Word_SMS(서술상수, "([BI)V") || Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean sprioc_VALUE_Leabhair_thagartha = Word_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int uimhir_phoirt = sprioc_VALUE_Leabhair_thagartha ? 빼기(1) : 0, ADDRESS_Leabhair_thagartha = sprioc_VALUE_Leabhair_thagartha ? 빼기(2) : 0;
                int iontráil_COUNT = 빼기(1), sonraí_ARRAY = 빼기(2), oibiacht_Leabhair_thagartha = 빼기(2);
                if (!oibiacht_VALUE(oibiacht_Leabhair_thagartha, 16) || !oibiacht_VALUE(sonraí_ARRAY, 20)) return;
                if (iontráil_COUNT < 0 || iontráil_COUNT > 힙[sonraí_ARRAY + 1] || uimhir_phoirt < 0 || uimhir_phoirt > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (ADDRESS_Leabhair_thagartha != 0 && !oibiacht_VALUE(ADDRESS_Leabhair_thagartha, 14)) return;
                힙[oibiacht_Leabhair_thagartha + 2] = sonraí_ARRAY; 힙참조[oibiacht_Leabhair_thagartha + 2] = 1; 힙[oibiacht_Leabhair_thagartha + 3] = iontráil_COUNT;
                힙[oibiacht_Leabhair_thagartha + 4] = ADDRESS_Leabhair_thagartha; 힙참조[oibiacht_Leabhair_thagartha + 4] = 1; 힙[oibiacht_Leabhair_thagartha + 5] = uimhir_phoirt; return;
            }
            if (ordú_CODE == 182 && Word_SMS(ainm_tairiseach, "setLength") && Word_SMS(서술상수, "(I)V")) {
                int iontráil_COUNT = 빼기(1), oibiacht_Leabhair_thagartha = 빼기(2); if (!oibiacht_VALUE(oibiacht_Leabhair_thagartha, 16)) return;
                if (iontráil_COUNT < 0 || iontráil_COUNT > 힙[힙[oibiacht_Leabhair_thagartha + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[oibiacht_Leabhair_thagartha + 3] = iontráil_COUNT; return;
            }
            if (ordú_CODE == 182 && (Word_SMS(ainm_tairiseach, "getData") && Word_SMS(서술상수, "()[B") || Word_SMS(ainm_tairiseach, "getLength") && Word_SMS(서술상수, "()I") || Word_SMS(ainm_tairiseach, "getAddress") && Word_SMS(서술상수, "()Ljava/net/InetAddress;") || Word_SMS(ainm_tairiseach, "getPort") && Word_SMS(서술상수, "()I"))) {
                int oibiacht_Leabhair_thagartha = 빼기(2); if (!oibiacht_VALUE(oibiacht_Leabhair_thagartha, 16)) return;
                int iontráil_suíomh = Word_SMS(ainm_tairiseach, "getData") ? 2 : Word_SMS(ainm_tairiseach, "getLength") ? 3 : Word_SMS(ainm_tairiseach, "getAddress") ? 4 : 5;
                넣기(힙[oibiacht_Leabhair_thagartha + iontráil_suíomh], iontráil_suíomh == 2 || iontráil_suíomh == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(úinéir, "java/net/DatagramSocket")) {
            if (ordú_CODE == 183 && Word_SMS(ainm_tairiseach, "<init>") && (Word_SMS(서술상수, "()V") || Word_SMS(서술상수, "(I)V"))) {
                int uimhir_phoirt = Word_SMS(서술상수, "()V") ? 0 : 빼기(1), oibiacht_Leabhair_thagartha = 빼기(2); if (!oibiacht_VALUE(oibiacht_Leabhair_thagartha, 15)) return;
                if (uimhir_phoirt < 0 || uimhir_phoirt > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = úsáideoir.oscail_Líonra(uimhir_phoirt); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[oibiacht_Leabhair_thagartha + 2] = 열린파일번호; return;
            }
            if (ordú_CODE == 182 && Word_SMS(ainm_tairiseach, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), oibiacht_Leabhair_thagartha = 빼기(2); if (!oibiacht_VALUE(oibiacht_Leabhair_thagartha, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[oibiacht_Leabhair_thagartha + 3] = 밀리초값; return;
            }
            if (ordú_CODE == 182 && Word_SMS(ainm_tairiseach, "getLocalPort") && Word_SMS(서술상수, "()I")) { int oibiacht_Leabhair_thagartha = 빼기(2); if (oibiacht_VALUE(oibiacht_Leabhair_thagartha, 15)) 넣기(힙[oibiacht_Leabhair_thagartha + 2] < 0 ? -1 : úsáideoir.Líonra_port(힙[oibiacht_Leabhair_thagartha + 2]), 1); return; }
            if (ordú_CODE == 182 && Word_SMS(ainm_tairiseach, "isClosed") && Word_SMS(서술상수, "()Z")) { int oibiacht_Leabhair_thagartha = 빼기(2); if (oibiacht_VALUE(oibiacht_Leabhair_thagartha, 15)) 넣기(힙[oibiacht_Leabhair_thagartha + 2] < 0 ? 1 : 0, 1); return; }
            if (ordú_CODE == 182 && Word_SMS(ainm_tairiseach, "close") && Word_SMS(서술상수, "()V")) { int oibiacht_Leabhair_thagartha = 빼기(2); if (oibiacht_VALUE(oibiacht_Leabhair_thagartha, 15) && 힙[oibiacht_Leabhair_thagartha + 2] >= 0) { úsáideoir.파일서술자닫기(힙[oibiacht_Leabhair_thagartha + 2]); 힙[oibiacht_Leabhair_thagartha + 2] = -1; } return; }
            if (ordú_CODE == 182 && (Word_SMS(ainm_tairiseach, "send") || Word_SMS(ainm_tairiseach, "receive")) && Word_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int paicéad = 빼기(2), oibiacht_Leabhair_thagartha = 빼기(2); if (!oibiacht_VALUE(paicéad, 16) || !oibiacht_VALUE(oibiacht_Leabhair_thagartha, 15)) return;
                int sonraí_ARRAY = 힙[paicéad + 2], 유효길이 = 힙[paicéad + 3], 열린파일번호 = 힙[oibiacht_Leabhair_thagartha + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(ainm_tairiseach, "send")) {
                    if (!oibiacht_VALUE(힙[paicéad + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int lúb_INDEX = 0; lúb_INDEX < 유효길이; lúb_INDEX++) 통신임시[lúb_INDEX] = 힙[sonraí_ARRAY + 2 + lúb_INDEX];
                    if (úsáideoir.seol_Líonra(열린파일번호, 힙[힙[paicéad + 4] + 2], 힙[paicéad + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int iontráil_COUNT = úsáideoir.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (iontráil_COUNT == -11) {
                        int 현재시각 = úsáideoir.밀리초();
                        if (힙[oibiacht_Leabhair_thagartha + 4] == 0) 힙[oibiacht_Leabhair_thagartha + 4] = 현재시각 + 1;
                        if (힙[oibiacht_Leabhair_thagartha + 3] > 0 && 현재시각 - (힙[oibiacht_Leabhair_thagartha + 4] - 1) >= 힙[oibiacht_Leabhair_thagartha + 3]) { 힙[oibiacht_Leabhair_thagartha + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(oibiacht_Leabhair_thagartha, 2); 넣기(paicéad, 2); fráma_suíomh[fráma_INDEX] = fráma_treoir[fráma_INDEX]; athraigh_iarratas_HTTP = true; return;
                    }
                    힙[oibiacht_Leabhair_thagartha + 4] = 0;
                    if (iontráil_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int lúb_INDEX = 0; lúb_INDEX < iontráil_COUNT; lúb_INDEX++) 힙[sonraí_ARRAY + 2 + lúb_INDEX] = (byte)통신임시[lúb_INDEX];
                    힙[paicéad + 3] = iontráil_COUNT; 힙[paicéad + 4] = ADDRESS_oibiacht(통신임시[513]); 힙참조[paicéad + 4] = 1; 힙[paicéad + 5] = 통신임시[512];
                }
                return;
            }
        }
        teip_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int oibiacht_Leabhair_thagartha) {
        int 현재시각 = úsáideoir.밀리초();
        if (힙[oibiacht_Leabhair_thagartha + 5] == 0) 힙[oibiacht_Leabhair_thagartha + 5] = 현재시각 + 1;
        if (힙[oibiacht_Leabhair_thagartha + 3] > 0 && 현재시각 - (힙[oibiacht_Leabhair_thagartha + 5] - 1) >= 힙[oibiacht_Leabhair_thagartha + 3]) { 힙[oibiacht_Leabhair_thagartha + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        fráma_suíomh[fráma_INDEX] = fráma_treoir[fráma_INDEX]; athraigh_iarratas_HTTP = true; return true;
    }
    static void 흐름호출(int úinéir, int ainm_tairiseach, int 서술상수, int ordú_CODE) {
        boolean 수신쪽 = Word_SMS(úinéir, "java/net/ServerSocket"), sruth = Word_SMS(úinéir, "java/io/InputStream") || Word_SMS(úinéir, "java/io/OutputStream");
        if (!sruth && ordú_CODE == 183 && Word_SMS(ainm_tairiseach, "<init>")) {
            boolean teicneolaíocht_faisnéise_folamh_staid = Word_SMS(서술상수, "()V"), 이름지정여부 = Word_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(teicneolaíocht_faisnéise_folamh_staid || 수신쪽 && Word_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { teip_VALUE("unsupported socket constructor"); return; }
            int uimhir_phoirt = teicneolaíocht_faisnéise_folamh_staid ? 0 : 빼기(1), ADDRESS_Leabhair_thagartha = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, oibiacht_Leabhair_thagartha = 빼기(2);
            if (!oibiacht_VALUE(oibiacht_Leabhair_thagartha, 수신쪽 ? 18 : 17)) return;
            if (uimhir_phoirt < 0 || uimhir_phoirt > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !oibiacht_VALUE(ADDRESS_Leabhair_thagartha, 14)) return;
            int Líonra_ADDRESS = 이름지정여부 ? 주소해독(ADDRESS_Leabhair_thagartha) : 주소지정여부 ? 힙[ADDRESS_Leabhair_thagartha + 2] : 0x7f000001;
            if (ERREÁID || 던진객체 != 0) return;
            int 열린파일번호 = úsáideoir.sruth_rialú(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = teicneolaíocht_faisnéise_folamh_staid ? 0 : 수신쪽 ? úsáideoir.sruth_rialú(1, 열린파일번호, uimhir_phoirt) : úsáideoir.nasc_sruth(열린파일번호, Líonra_ADDRESS, uimhir_phoirt);
            if (처리값 < 0) { úsáideoir.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[oibiacht_Leabhair_thagartha + 2] = 열린파일번호; 힙[oibiacht_Leabhair_thagartha + 4] = uimhir_phoirt; 힙[oibiacht_Leabhair_thagartha + 6] = teicneolaíocht_faisnéise_folamh_staid ? 0 : 1; return;
        }
        if (!sruth && Word_SMS(ainm_tairiseach, "setSoTimeout") && Word_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), oibiacht_Leabhair_thagartha = 빼기(2); if (!oibiacht_VALUE(oibiacht_Leabhair_thagartha, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[oibiacht_Leabhair_thagartha + 3] = 밀리초값; return; }
        if (!sruth && Word_SMS(ainm_tairiseach, "close") && Word_SMS(서술상수, "()V")) { int oibiacht_Leabhair_thagartha = 빼기(2); if (oibiacht_VALUE(oibiacht_Leabhair_thagartha, 수신쪽 ? 18 : 17) && 힙[oibiacht_Leabhair_thagartha + 2] >= 0) { úsáideoir.파일서술자닫기(힙[oibiacht_Leabhair_thagartha + 2]); 힙[oibiacht_Leabhair_thagartha + 2] = -1; } return; }
        if (!sruth && (Word_SMS(ainm_tairiseach, "getLocalPort") || Word_SMS(ainm_tairiseach, "getPort") || Word_SMS(ainm_tairiseach, "isClosed") || Word_SMS(ainm_tairiseach, "isConnected"))) {
            int oibiacht_Leabhair_thagartha = 빼기(2); if (!oibiacht_VALUE(oibiacht_Leabhair_thagartha, 수신쪽 ? 18 : 17)) return;
            넣기(Word_SMS(ainm_tairiseach, "isClosed") ? 힙[oibiacht_Leabhair_thagartha + 2] < 0 ? 1 : 0 : Word_SMS(ainm_tairiseach, "isConnected") ? 힙[oibiacht_Leabhair_thagartha + 6] : Word_SMS(ainm_tairiseach, "getPort") ? 힙[oibiacht_Leabhair_thagartha + 4] : 힙[oibiacht_Leabhair_thagartha + 2] < 0 ? -1 : úsáideoir.sruth_rialú(4, 힙[oibiacht_Leabhair_thagartha + 2], 0), 1); return;
        }
        if (수신쪽 && Word_SMS(ainm_tairiseach, "accept") && Word_SMS(서술상수, "()Ljava/net/Socket;")) {
            int oibiacht_Leabhair_thagartha = 빼기(2); if (!oibiacht_VALUE(oibiacht_Leabhair_thagartha, 18)) return; int 열린파일번호 = úsáideoir.sruth_rialú(3, 힙[oibiacht_Leabhair_thagartha + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(oibiacht_Leabhair_thagartha)) 넣기(oibiacht_Leabhair_thagartha, 2); return; }
            힙[oibiacht_Leabhair_thagartha + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = leithdháil_Stóras(17, 5); if (ERREÁID) { úsáideoir.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = úsáideoir.sruth_rialú(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !sruth && ((Word_SMS(ainm_tairiseach, "getInputStream") && Word_SMS(서술상수, "()Ljava/io/InputStream;")) || (Word_SMS(ainm_tairiseach, "getOutputStream") && Word_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int oibiacht_Leabhair_thagartha = 빼기(2); if (!oibiacht_VALUE(oibiacht_Leabhair_thagartha, 17)) return; if (힙[oibiacht_Leabhair_thagartha + 2] < 0 || 힙[oibiacht_Leabhair_thagartha + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = leithdháil_Stóras(19, 4); if (ERREÁID) return; 힙[반환값 + 2] = oibiacht_Leabhair_thagartha; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_SMS(ainm_tairiseach, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (sruth) {
            boolean 읽기여부 = Word_SMS(ainm_tairiseach, "read"), teicneolaíocht_faisnéise_scríobh_oibríocht = Word_SMS(ainm_tairiseach, "write"), bac = Word_SMS(서술상수, "([B)I") || Word_SMS(서술상수, "([B)V"), teicneolaíocht_faisnéise_SUBARRAY = Word_SMS(서술상수, "([BII)I") || Word_SMS(서술상수, "([BII)V");
            int iontráil_COUNT = teicneolaíocht_faisnéise_SUBARRAY ? 빼기(1) : 0, 시작변위 = teicneolaíocht_faisnéise_SUBARRAY ? 빼기(1) : 0, sonraí_ARRAY = bac || teicneolaíocht_faisnéise_SUBARRAY ? 빼기(2) : 0;
            int sonraí_VALUE = teicneolaíocht_faisnéise_scríobh_oibríocht && Word_SMS(서술상수, "(I)V") ? 빼기(1) : 0, oibiacht_Leabhair_thagartha = 빼기(2);
            if (!oibiacht_VALUE(oibiacht_Leabhair_thagartha, 19)) return; int 부모참조 = 힙[oibiacht_Leabhair_thagartha + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(ainm_tairiseach, "close") && Word_SMS(서술상수, "()V")) { úsáideoir.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Word_SMS(ainm_tairiseach, "flush") && Word_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !teicneolaíocht_faisnéise_scríobh_oibríocht) || 읽기여부 != (힙[oibiacht_Leabhair_thagartha + 3] == 0)) { teip_VALUE("unsupported stream operation"); return; }
            if (bac || teicneolaíocht_faisnéise_SUBARRAY) { if (!oibiacht_VALUE(sonraí_ARRAY, 20)) return; if (bac) iontráil_COUNT = 힙[sonraí_ARRAY + 1]; if (시작변위 < 0 || iontráil_COUNT < 0 || 시작변위 > 힙[sonraí_ARRAY + 1] - iontráil_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else iontráil_COUNT = 1;
            if (iontráil_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = teicneolaíocht_faisnéise_scríobh_oibríocht ? 힙[oibiacht_Leabhair_thagartha + 4] : 0, 처리값 = 0;
            while (완료수 < iontráil_COUNT) {
                처리값 = 읽기여부 ? úsáideoir.파일한바이트읽기(열린파일번호) : úsáideoir.파일한바이트쓰기(열린파일번호, bac || teicneolaíocht_faisnéise_SUBARRAY ? 힙[sonraí_ARRAY + 2 + 시작변위 + 완료수] : sonraí_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (bac || teicneolaíocht_faisnéise_SUBARRAY)) 힙[sonraí_ARRAY + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(bac || teicneolaíocht_faisnéise_SUBARRAY)) break;
            }
            if (처리값 == -11 && (teicneolaíocht_faisnéise_scríobh_oibríocht || 완료수 == 0)) {
                힙[oibiacht_Leabhair_thagartha + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(oibiacht_Leabhair_thagartha, 2); if (bac || teicneolaíocht_faisnéise_SUBARRAY) 넣기(sonraí_ARRAY, 2); if (teicneolaíocht_faisnéise_SUBARRAY) { 넣기(시작변위, 1); 넣기(iontráil_COUNT, 1); } if (teicneolaíocht_faisnéise_scríobh_oibríocht && !(bac || teicneolaíocht_faisnéise_SUBARRAY)) 넣기(sonraí_VALUE, 1); } return;
            }
            힙[oibiacht_Leabhair_thagartha + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : bac || teicneolaíocht_faisnéise_SUBARRAY ? 완료수 : 처리값, 1); return;
        }
        teip_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int ainm_tairiseach) {
        if (Word_SMS(ainm_tairiseach, "Gaeilge/자체/fuinneog")) return 24;
        if (Word_SMS(ainm_tairiseach, "Gaeilge/자체/Lipéad")) return 26;
        if (Word_SMS(ainm_tairiseach, "Gaeilge/자체/cnaipe")) return 27;
        if (Word_SMS(ainm_tairiseach, "Gaeilge/자체/réimse_téacs")) return 28;
        if (Word_SMS(ainm_tairiseach, "Gaeilge/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int ainm_tairiseach) {
        return 한국어화면종(ainm_tairiseach) != 0 || Word_SMS(ainm_tairiseach, "Gaeilge/자체/화면구성요소") || Word_SMS(ainm_tairiseach, "Gaeilge/자체/ócáid_scuaine");
    }
    static int 화면종(int ainm_tairiseach) {
        int 한국어종 = 한국어화면종(ainm_tairiseach); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(ainm_tairiseach, "javax/swing/JFrame")) return 24;
        if (Word_SMS(ainm_tairiseach, "javax/swing/JPanel")) return 25;
        if (Word_SMS(ainm_tairiseach, "javax/swing/JLabel")) return 26;
        if (Word_SMS(ainm_tairiseach, "javax/swing/JButton")) return 27;
        if (Word_SMS(ainm_tairiseach, "javax/swing/JTextField")) return 28;
        if (Word_SMS(ainm_tairiseach, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(ainm_tairiseach, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int ainm_tairiseach) {
        return 화면종(ainm_tairiseach) != 0 || Word_SMS(ainm_tairiseach, "java/awt/Component") || Word_SMS(ainm_tairiseach, "java/awt/Container") || Word_SMS(ainm_tairiseach, "javax/swing/JComponent") || Word_SMS(ainm_tairiseach, "javax/swing/AbstractButton") || Word_SMS(ainm_tairiseach, "javax/swing/text/JTextComponent") || Word_SMS(ainm_tairiseach, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int oibiacht_Leabhair_thagartha) { if (!객체유효(oibiacht_Leabhair_thagartha)) return false; if (힙[oibiacht_Leabhair_thagartha] < 24 || 힙[oibiacht_Leabhair_thagartha] > 28) { teip_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int oibiacht_Leabhair_thagartha, int SMS_Leabhair_thagartha) {
        if (SMS_Leabhair_thagartha != 0 && !oibiacht_VALUE(SMS_Leabhair_thagartha, 1)) return;
        int iontráil_COUNT = SMS_Leabhair_thagartha == 0 ? 0 : 힙[SMS_Leabhair_thagartha + 1]; if (iontráil_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int lúb_INDEX = 0; lúb_INDEX < iontráil_COUNT; lúb_INDEX++) 화면글임시[lúb_INDEX] = 힙[SMS_Leabhair_thagartha + 2 + lúb_INDEX];
        if (úsáideoir.화면글(힙[oibiacht_Leabhair_thagartha + 2], 화면글임시, iontráil_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[oibiacht_Leabhair_thagartha + 3] = SMS_Leabhair_thagartha; 힙참조[oibiacht_Leabhair_thagartha + 3] = 1;
    }
    static int 화면문자읽기(int oibiacht_Leabhair_thagartha) {
        int cuntas_VALUE = 힙[oibiacht_Leabhair_thagartha + 2], iontráil_COUNT = úsáideoir.화면연결(8, cuntas_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (iontráil_COUNT < 0) { teip_VALUE("GUI text read failed"); return 0; }
        for (int lúb_INDEX = 0; lúb_INDEX < iontráil_COUNT; lúb_INDEX++) { int 부호값 = úsáideoir.화면연결(9, cuntas_VALUE, lúb_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = leithdháil_Stóras(1, 사용수); if (!ERREÁID) for (int lúb_INDEX = 0; lúb_INDEX < 사용수; lúb_INDEX++) 힙[반환값 + 2 + lúb_INDEX] = 화면글임시[lúb_INDEX]; return 반환값;
    }
    /* Gaeilge 객체를 직접 만들고 eithne_VALUE 화면 기능에 연결한다. Swing oibiacht_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int úinéir, int ainm_tairiseach, int 서술상수, int ordú_CODE) {
        if (Word_SMS(úinéir, "Gaeilge/자체/ócáid_scuaine")) {
            if (ordú_CODE == 184 && Word_SMS(ainm_tairiseach, "나중에실행") && Word_SMS(서술상수, "(LGaeilge/자체/실행할일;)V")) {
                int tasc_gníomh = 빼기(2); if (!객체유효(tasc_gníomh)) return;
                if (나중수 == 8) { teip_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = tasc_gníomh; return;
            }
            if (ordú_CODE == 184 && Word_SMS(ainm_tairiseach, "사건처리중인가") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            teip_VALUE("지원하지 않는 Gaeilge 화면 일정 호출"); return;
        }
        if (Word_SMS(úinéir, "Gaeilge/자체/동작알림")) {
            int 알림 = 빼기(2); if (!oibiacht_VALUE(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Word_SMS(ainm_tairiseach, "ócáid_foinse") && Word_SMS(서술상수, "()LGaeilge/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Word_SMS(ainm_tairiseach, "ordú_SMS") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Word_SMS(ainm_tairiseach, "INDEX") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else teip_VALUE("지원하지 않는 Gaeilge Gníomh 알림 호출"); return;
        }
        if (ordú_CODE == 183 && Word_SMS(ainm_tairiseach, "<init>")) {
            int 종류 = 한국어화면종(úinéir), 받이 = 0, 가로 = 0, Ingearach_suíomh = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (úsáideoir.화면너비() - 폭) / 2; Ingearach_suíomh = (úsáideoir.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_SMS(서술상수, "(Ljava/lang/String;IIIILGaeilge/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Ingearach_suíomh = 빼기(1); 가로 = 빼기(1);
            } else { teip_VALUE("지원하지 않는 Gaeilge 화면 생성자"); return; }
            int Téacs = 빼기(2), eilimint_VALUE = 빼기(2); if (!화면객체(eilimint_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Ingearach_suíomh < 0 || 폭 > úsáideoir.화면너비() - 가로 || 높이 > úsáideoir.화면높이() - Ingearach_suíomh) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = úsáideoir.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { teip_VALUE("화면 eilimint_VALUE 자리가 가득 찼습니다"); return; }
            힙[eilimint_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = eilimint_VALUE;
            힙[eilimint_VALUE + 5] = 가로; 힙[eilimint_VALUE + 6] = Ingearach_suíomh; 힙[eilimint_VALUE + 7] = 폭; 힙[eilimint_VALUE + 8] = 높이; 힙[eilimint_VALUE + 10] = 2;
            힙[eilimint_VALUE + 4] = 받이; 힙참조[eilimint_VALUE + 4] = 1; 힙[eilimint_VALUE + 12] = 1;
            úsáideoir.화면연결(1, INDEX, 가로, Ingearach_suíomh, 폭, 높이);
            if (종류 == 24) úsáideoir.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(eilimint_VALUE, Téacs); return;
        }
        if (ordú_CODE != 182) { teip_VALUE("잘못된 Gaeilge 화면 호출 Ordú"); return; }
        if (Word_SMS(ainm_tairiseach, "scríobh_SMS") && Word_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Téacs = 빼기(2), eilimint_VALUE = 빼기(2); if (화면객체(eilimint_VALUE)) 화면문자설정(eilimint_VALUE, Téacs); return;
        }
        if (Word_SMS(ainm_tairiseach, "글읽기") && Word_SMS(서술상수, "()Ljava/lang/String;")) {
            int eilimint_VALUE = 빼기(2); if (화면객체(eilimint_VALUE)) 넣기(화면문자읽기(eilimint_VALUE), 2); return;
        }
        if (Word_SMS(ainm_tairiseach, "동작맡기기") && Word_SMS(서술상수, "(LGaeilge/자체/동작받이;)V")) {
            int 받이 = 빼기(2), eilimint_VALUE = 빼기(2);
            if (화면객체(eilimint_VALUE)) { 힙[eilimint_VALUE + 4] = 받이; 힙참조[eilimint_VALUE + 4] = 1; 힙[eilimint_VALUE + 12] = 1; } return;
        }
        if (Word_SMS(ainm_tairiseach, "cuir_le_eilimint") && Word_SMS(서술상수, "(LGaeilge/자체/화면구성요소;)V")) {
            int leanbh_VALUE = 빼기(2), 부모 = 빼기(2); if (!화면객체(leanbh_VALUE) || !화면객체(부모)) return;
            if (úsáideoir.화면연결(2, 힙[부모 + 2], 힙[leanbh_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[leanbh_VALUE + 11] = 부모; 힙참조[leanbh_VALUE + 11] = 1; return;
        }
        if (Word_SMS(ainm_tairiseach, "자리정하기") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Ingearach_suíomh = 빼기(1), 가로 = 빼기(1), eilimint_VALUE = 빼기(2); if (!화면객체(eilimint_VALUE)) return;
            if (úsáideoir.화면연결(1, 힙[eilimint_VALUE + 2], 가로, Ingearach_suíomh, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[eilimint_VALUE + 5] = 가로; 힙[eilimint_VALUE + 6] = Ingearach_suíomh; 힙[eilimint_VALUE + 7] = 폭; 힙[eilimint_VALUE + 8] = 높이; return;
        }
        if ((Word_SMS(ainm_tairiseach, "seó_fuinneog") || Word_SMS(ainm_tairiseach, "Dún")) && Word_SMS(서술상수, "()V")) {
            boolean infheictheacht_VALUE = Word_SMS(ainm_tairiseach, "seó_fuinneog"); int eilimint_VALUE = 빼기(2); if (!화면객체(eilimint_VALUE)) return;
            if (úsáideoir.화면연결(infheictheacht_VALUE ? 3 : 4, 힙[eilimint_VALUE + 2], infheictheacht_VALUE ? 1 : 0, 0, 0, 0) < 0) { teip_VALUE("화면은 idirghníomhach 명령에서 실행해야 합니다"); return; }
            힙[eilimint_VALUE + 9] = infheictheacht_VALUE ? 1 : 0; return;
        }
        if (Word_SMS(ainm_tairiseach, "보이는가") && Word_SMS(서술상수, "()Z")) { int eilimint_VALUE = 빼기(2); if (화면객체(eilimint_VALUE)) 넣기(힙[eilimint_VALUE + 9], 1); return; }
        teip_VALUE("지원하지 않는 Gaeilge 화면 modh_VALUE");
    }
    static void 화면호출(int úinéir, int ainm_tairiseach, int 서술상수, int ordú_CODE) {
        if (Word_SMS(úinéir, "javax/swing/SwingUtilities")) {
            if (ordú_CODE == 184 && Word_SMS(ainm_tairiseach, "invokeLater") && Word_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int oibiacht_Leabhair_thagartha = 빼기(2); if (!객체유효(oibiacht_Leabhair_thagartha)) return; if (나중수 == 8) { teip_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = oibiacht_Leabhair_thagartha; return; }
            if (ordú_CODE == 184 && Word_SMS(ainm_tairiseach, "isEventDispatchThread") && Word_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            teip_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(úinéir, "java/awt/event/ActionEvent")) {
            int oibiacht_Leabhair_thagartha = 빼기(2); if (!oibiacht_VALUE(oibiacht_Leabhair_thagartha, 29)) return;
            if (Word_SMS(ainm_tairiseach, "getSource") && Word_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[oibiacht_Leabhair_thagartha + 2], 2);
            else if (Word_SMS(ainm_tairiseach, "getActionCommand") && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[oibiacht_Leabhair_thagartha + 2]), 2);
            else if (Word_SMS(ainm_tairiseach, "getID") && Word_SMS(서술상수, "()I")) 넣기(1001, 1);
            else teip_VALUE("unsupported ActionEvent method"); return;
        }
        if (ordú_CODE == 183 && Word_SMS(ainm_tairiseach, "<init>")) {
            int COLUMNS = 0, SMS_Leabhair_thagartha = 0;
            if (Word_SMS(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_SMS(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); SMS_Leabhair_thagartha = 빼기(2); }
            else if (Word_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Leabhair_thagartha = 빼기(2);
            else if (Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(서술상수, "()V")) { teip_VALUE("unsupported Swing constructor"); return; }
            int oibiacht_Leabhair_thagartha = 빼기(2); if (!객체유효(oibiacht_Leabhair_thagartha)) return;
            if (힙[oibiacht_Leabhair_thagartha] == 30) { teip_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(oibiacht_Leabhair_thagartha) || COLUMNS < 0) return;
            int cuntas_VALUE = úsáideoir.화면연결(0, 힙[oibiacht_Leabhair_thagartha] - 23, 0, 0, 0, 0);
            if (cuntas_VALUE < 1 || cuntas_VALUE > 32) { teip_VALUE("GUI widget slots exhausted"); return; }
            힙[oibiacht_Leabhair_thagartha + 2] = cuntas_VALUE; 화면참조[cuntas_VALUE - 1] = oibiacht_Leabhair_thagartha; 힙[oibiacht_Leabhair_thagartha + 5] = 힙[oibiacht_Leabhair_thagartha] == 24 ? 130 : 16; 힙[oibiacht_Leabhair_thagartha + 6] = 힙[oibiacht_Leabhair_thagartha] == 24 ? 110 : 16;
            힙[oibiacht_Leabhair_thagartha + 7] = 힙[oibiacht_Leabhair_thagartha] == 24 ? 380 : 220; 힙[oibiacht_Leabhair_thagartha + 8] = 힙[oibiacht_Leabhair_thagartha] == 24 ? 240 : 28; 힙[oibiacht_Leabhair_thagartha + 10] = 1;
            화면문자설정(oibiacht_Leabhair_thagartha, SMS_Leabhair_thagartha); return;
        }
        if (Word_SMS(ainm_tairiseach, "setText") || Word_SMS(ainm_tairiseach, "setTitle")) { int SMS_Leabhair_thagartha = 빼기(2), oibiacht_Leabhair_thagartha = 빼기(2); if (화면객체(oibiacht_Leabhair_thagartha) && Word_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(oibiacht_Leabhair_thagartha, SMS_Leabhair_thagartha); return; }
        if (Word_SMS(ainm_tairiseach, "getText") || Word_SMS(ainm_tairiseach, "getTitle")) { int oibiacht_Leabhair_thagartha = 빼기(2); if (화면객체(oibiacht_Leabhair_thagartha) && Word_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(oibiacht_Leabhair_thagartha), 2); return; }
        if (Word_SMS(ainm_tairiseach, "addActionListener") && Word_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), oibiacht_Leabhair_thagartha = 빼기(2); if (화면객체(oibiacht_Leabhair_thagartha)) { 힙[oibiacht_Leabhair_thagartha + 4] = 수신참조; 힙참조[oibiacht_Leabhair_thagartha + 4] = 1; } return; }
        if (Word_SMS(ainm_tairiseach, "getContentPane") && Word_SMS(서술상수, "()Ljava/awt/Container;")) { int oibiacht_Leabhair_thagartha = 빼기(2); if (화면객체(oibiacht_Leabhair_thagartha)) 넣기(oibiacht_Leabhair_thagartha, 2); return; }
        if (Word_SMS(ainm_tairiseach, "setLayout") && Word_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int dáileadh_Leabhair_thagartha = 빼기(2), oibiacht_Leabhair_thagartha = 빼기(2); if (화면객체(oibiacht_Leabhair_thagartha) && dáileadh_Leabhair_thagartha != 0) teip_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(ainm_tairiseach, "add") && (Word_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean dáileadh_coinníoll = Word_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (dáileadh_coinníoll) 빼기(2);
            int leanbh_Leabhair_thagartha = 빼기(2), oibiacht_Leabhair_thagartha = 빼기(2); if (!화면객체(leanbh_Leabhair_thagartha) || !화면객체(oibiacht_Leabhair_thagartha)) return;
            if (úsáideoir.화면연결(2, 힙[oibiacht_Leabhair_thagartha + 2], 힙[leanbh_Leabhair_thagartha + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[leanbh_Leabhair_thagartha + 11] = oibiacht_Leabhair_thagartha; 힙참조[leanbh_Leabhair_thagartha + 11] = 1; if (!dáileadh_coinníoll) 넣기(leanbh_Leabhair_thagartha, 2); return;
        }
        if (Word_SMS(ainm_tairiseach, "setBounds") && Word_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), x_chomhordanáid = 빼기(1), oibiacht_Leabhair_thagartha = 빼기(2); if (!화면객체(oibiacht_Leabhair_thagartha)) return;
            if (úsáideoir.화면연결(1, 힙[oibiacht_Leabhair_thagartha + 2], x_chomhordanáid, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[oibiacht_Leabhair_thagartha + 5] = x_chomhordanáid; 힙[oibiacht_Leabhair_thagartha + 6] = 세로좌표; 힙[oibiacht_Leabhair_thagartha + 7] = 너비; 힙[oibiacht_Leabhair_thagartha + 8] = 높이; return;
        }
        if (Word_SMS(ainm_tairiseach, "setSize") && Word_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), oibiacht_Leabhair_thagartha = 빼기(2); if (!화면객체(oibiacht_Leabhair_thagartha)) return;
            if (úsáideoir.화면연결(1, 힙[oibiacht_Leabhair_thagartha + 2], 힙[oibiacht_Leabhair_thagartha + 5], 힙[oibiacht_Leabhair_thagartha + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[oibiacht_Leabhair_thagartha + 7] = 너비; 힙[oibiacht_Leabhair_thagartha + 8] = 높이; } return;
        }
        if (Word_SMS(ainm_tairiseach, "setLocationRelativeTo") && Word_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), oibiacht_Leabhair_thagartha = 빼기(2); if (!화면객체(oibiacht_Leabhair_thagartha)) return; if (상대배치 != 0) { teip_VALUE("only screen centering supported"); return; } 힙[oibiacht_Leabhair_thagartha + 5] = (úsáideoir.화면너비() - 힙[oibiacht_Leabhair_thagartha + 7]) / 2; 힙[oibiacht_Leabhair_thagartha + 6] = (úsáideoir.화면높이() - 힙[oibiacht_Leabhair_thagartha + 8]) / 2; úsáideoir.화면연결(1, 힙[oibiacht_Leabhair_thagartha + 2], 힙[oibiacht_Leabhair_thagartha + 5], 힙[oibiacht_Leabhair_thagartha + 6], 힙[oibiacht_Leabhair_thagartha + 7], 힙[oibiacht_Leabhair_thagartha + 8]); return; }
        if (Word_SMS(ainm_tairiseach, "setDefaultCloseOperation") && Word_SMS(서술상수, "(I)V")) { int polasaí = 빼기(1), oibiacht_Leabhair_thagartha = 빼기(2); if (화면객체(oibiacht_Leabhair_thagartha)) { if (polasaí < 0 || polasaí > 3) 예외던짐(9, "close policy"); else { 힙[oibiacht_Leabhair_thagartha + 10] = polasaí; úsáideoir.화면연결(7, 힙[oibiacht_Leabhair_thagartha + 2], polasaí, 0, 0, 0); } } return; }
        if (Word_SMS(ainm_tairiseach, "setVisible") && Word_SMS(서술상수, "(Z)V")) { int sonraí_VALUE = 빼기(1), oibiacht_Leabhair_thagartha = 빼기(2); if (화면객체(oibiacht_Leabhair_thagartha)) { int 처리값 = úsáideoir.화면연결(3, 힙[oibiacht_Leabhair_thagartha + 2], sonraí_VALUE, 0, 0, 0); if (처리값 < 0) teip_VALUE("Swing requires a standalone interactive command"); else 힙[oibiacht_Leabhair_thagartha + 9] = sonraí_VALUE; } return; }
        if (Word_SMS(ainm_tairiseach, "dispose") && Word_SMS(서술상수, "()V")) { int oibiacht_Leabhair_thagartha = 빼기(2); if (화면객체(oibiacht_Leabhair_thagartha)) { úsáideoir.화면연결(4, 힙[oibiacht_Leabhair_thagartha + 2], 0, 0, 0, 0); 힙[oibiacht_Leabhair_thagartha + 9] = 0; } return; }
        if (Word_SMS(ainm_tairiseach, "repaint") || Word_SMS(ainm_tairiseach, "validate")) { int oibiacht_Leabhair_thagartha = 빼기(2); if (!화면객체(oibiacht_Leabhair_thagartha) || !Word_SMS(서술상수, "()V")) return; úsáideoir.화면연결(1, 힙[oibiacht_Leabhair_thagartha + 2], 힙[oibiacht_Leabhair_thagartha + 5], 힙[oibiacht_Leabhair_thagartha + 6], 힙[oibiacht_Leabhair_thagartha + 7], 힙[oibiacht_Leabhair_thagartha + 8]); return; }
        if (Word_SMS(ainm_tairiseach, "isVisible") && Word_SMS(서술상수, "()Z")) { int oibiacht_Leabhair_thagartha = 빼기(2); if (화면객체(oibiacht_Leabhair_thagartha)) 넣기(힙[oibiacht_Leabhair_thagartha + 9], 1); return; }
        teip_VALUE("unsupported Swing method (native subset)");
    }
    static void 사건실행(int sprioc_ADDRESS, int 사건번호, boolean Gaeilge) {
        if (sprioc_ADDRESS < 1 || 힙[sprioc_ADDRESS] < 32) { teip_VALUE("Java event listener required"); return; }
        int comhad_INDEX = ainm_modh(힙[sprioc_ADDRESS] - 32, 사건번호 == 0 ? (Gaeilge ? "Rith" : "run") : (Gaeilge ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (Gaeilge ? "(LGaeilge/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (comhad_INDEX < 0) { teip_VALUE("event callback missing"); return; }
        현재가닥 = 0; snáithe_COUNT = 1; fráma_INDEX = 0; snáithe_staid[0] = 1; fráma_Cruach[0] = 0; 틀잠금[0] = túsaigh_fráma[0] = 0; athraigh_iarratas_HTTP = false;
        for (int lúb_INDEX = 0; lúb_INDEX < 128; lúb_INDEX++) { logánta_VALUE[lúb_INDEX] = logánta_TYPE[lúb_INDEX] = 0; }
        fráma_modh[0] = comhad_INDEX; fráma_suíomh[0] = modh_Start[comhad_INDEX]; logánta_VALUE[0] = sprioc_ADDRESS; logánta_TYPE[0] = 2;
        if (사건번호 != 0) { logánta_VALUE[1] = 사건번호; logánta_TYPE[1] = 2; }
        사건중 = true; Rith_ordú(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!ERREÁID) {
            if (나중수 > 0) { int sprioc_ADDRESS = 나중실행[0], Gaeilge = 나중한국어[0]; for (int lúb_INDEX = 1; lúb_INDEX < 나중수; lúb_INDEX++) { 나중실행[lúb_INDEX - 1] = 나중실행[lúb_INDEX]; 나중한국어[lúb_INDEX - 1] = 나중한국어[lúb_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(sprioc_ADDRESS, 0, Gaeilge != 0); continue; }
            if (úsáideoir.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = úsáideoir.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { teip_VALUE("GUI event I/O failed"); return; }
            int cuntas_VALUE = 사건번호 & 65535; if (cuntas_VALUE < 1 || cuntas_VALUE > 32) continue; int oibiacht_Leabhair_thagartha = 화면참조[cuntas_VALUE - 1]; if (oibiacht_Leabhair_thagartha == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[oibiacht_Leabhair_thagartha + 10] != 0) 힙[oibiacht_Leabhair_thagartha + 9] = 0;
                if (힙[oibiacht_Leabhair_thagartha + 10] == 3) for (int lúb_INDEX = 0; lúb_INDEX < 32; lúb_INDEX++) if (화면참조[lúb_INDEX] != 0 && 힙[화면참조[lúb_INDEX]] == 24) úsáideoir.화면연결(4, lúb_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[oibiacht_Leabhair_thagartha + 4] != 0) {
                int LÉIGHMÉ_Leabhair_thagartha = leithdháil_Stóras(29, 2); if (ERREÁID) return; 힙[LÉIGHMÉ_Leabhair_thagartha + 2] = oibiacht_Leabhair_thagartha; 힙[LÉIGHMÉ_Leabhair_thagartha + 3] = 힙[oibiacht_Leabhair_thagartha + 12]; 힙참조[LÉIGHMÉ_Leabhair_thagartha + 2] = 1; 사건실행(힙[oibiacht_Leabhair_thagartha + 4], LÉIGHMÉ_Leabhair_thagartha, 힙[oibiacht_Leabhair_thagartha + 12] != 0);
            }
        }
    }
    public static int Rith_2() {
        if (úsáideoir.인수개수() == 1 && 자바도구.같음(úsáideoir.Argóintí(0), "-version")) {
            úsáideoir.Scríobh("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (úsáideoir.인수개수() < 1) { úsáideoir.Scríobh("Usage: java CLASS [ARGS]\n"); return 2; }
        iontráil_aicme_Sainmhíniú = lódáil_aicme_Sainmhíniú(óstach_carachtar(úsáideoir.Argóintí(0))); if (ERREÁID || iontráil_aicme_Sainmhíniú < 0) return 1;
        int iontráil_pointe_VALUE = ainm_modh(iontráil_aicme_Sainmhíniú, "Rith_2", "()V");
        boolean 한국어진입 = iontráil_pointe_VALUE >= 0 && (modh_rochtain[iontráil_pointe_VALUE] & 9) == 9;
        if (!한국어진입) iontráil_pointe_VALUE = ainm_modh(iontráil_aicme_Sainmhíniú, "main", "([Ljava/lang/String;)V");
        if (iontráil_pointe_VALUE < 0 || (modh_rochtain[iontráil_pointe_VALUE] & 9) != 9) teip_VALUE("public static void Rith_2() or main(String[] args) required");
        if (ERREÁID) return 1;
        int Argóintí = leithdháil_Stóras(3, úsáideoir.인수개수() - 1); ARRAY_eilimint[Argóintí] = -1;
        for (int 수 = 1; 수 < úsáideoir.인수개수() && !ERREÁID; 수++) 힙[Argóintí + 1 + 수] = óstach_carachtar(úsáideoir.Argóintí(수));
        fráma_INDEX = 0; fráma_modh[0] = iontráil_pointe_VALUE; fráma_suíomh[0] = modh_Start[iontráil_pointe_VALUE]; logánta_VALUE[0] = 한국어진입 ? 0 : Argóintí; logánta_TYPE[0] = 한국어진입 ? 0 : 2;
        snáithe_staid[0] = 1; snáithe_oibiacht[0] = leithdháil_Stóras(13, 2);
        Rith_ordú(); if (!ERREÁID) 화면사건들(); return ERREÁID ? 1 : 0;
    }
}
