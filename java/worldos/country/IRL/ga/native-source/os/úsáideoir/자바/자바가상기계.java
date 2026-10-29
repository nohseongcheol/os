// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Comhad/스택/Leabhair_thagartha/craobh 경계를 Rith_ordú 중 검사한다. */
public final class 자바가상기계 {
    static int[] Comhad = new int[16384], comhad_ainm_SMS = new int[64];
    static int[] tairiseach_clib = new int[512], 상가 = new int[512], tairiseach_SECOND_VALUE = new int[512], teaghrán_Leabhair_thagartha = new int[512];
    static int[] modh_ainm_SMS = new int[32], modh_TYPE = new int[32], modh_rochtain = new int[32];
    static int[] modh_Start = new int[32], modh_cuir_deireadh_le = new int[32], modh_Cruach = new int[32], 함수지역 = new int[32];
    static int[] modh_argóint_COUNT = new int[32], modh_argóint_TYPE = new int[512], modh_return = new int[32];
    static int[] 경계 = new int[16384];
    static int[] logánta_VALUE = new int[4096], logánta_TYPE = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] fráma_modh = new int[32], fráma_suíomh = new int[32], fráma_Cruach = new int[32];
    static int[] 힙 = new int[8192];
    static int Méid, 읽기위치, tairiseach_COUNT, modh_COUNT, aicme_ainm, fráma_INDEX = -1, 힙끝 = 1, return_TYPE;
    static boolean ERREÁID;

    static void teip_VALUE(String Word_SMS) {
        if (!ERREÁID) { úsáideoir.Scríobh("JVM error: "); úsáideoir.Scríobh(Word_SMS); úsáideoir.scríobh_carachtar_VALUE(10); }
        ERREÁID = true;
    }
    static boolean gearrthóg(int Rith_2, int fad_VALUE) { return Rith_2 >= 0 && fad_VALUE >= 0 && Rith_2 <= Méid - fad_VALUE; }
    static int beart_VALUE() {
        if (!gearrthóg(읽기위치, 1)) { teip_VALUE("truncated class file"); return 0; }
        return Comhad[읽기위치++];
    }
    static int 짧은수() { return beart_VALUE() << 8 | beart_VALUE(); }
    static int slánuimhir() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int fad_VALUE) { if (!gearrthóg(읽기위치, fad_VALUE)) teip_VALUE("invalid attribute size"); else 읽기위치 += fad_VALUE; }
    static boolean seic_tairiseach(int 수, int 종류) {
        if (수 <= 0 || 수 >= tairiseach_COUNT || tairiseach_clib[수] != 종류) { teip_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Rith_2, int fad_VALUE, String Word_SMS) {
        if (!gearrthóg(Rith_2, fad_VALUE) || fad_VALUE != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < fad_VALUE; 수++) if (Comhad[Rith_2 + 수] != Word_SMS.charAt(수)) return false;
        return true;
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
    static void 속성건너() {
        int mír_COUNT = 짧은수();
        for (int 수 = 0; 수 < mír_COUNT && !ERREÁID; 수++) { seic_tairiseach(짧은수(), 1); 건너(slánuimhir()); }
    }
    static int ordú_fad(int VALUE) {
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
        if (slánuimhir() != 0xcafebabe) teip_VALUE("not a class file");
        int 부판 = 짧은수(), leagan_VALUE = 짧은수();
        if (leagan_VALUE < 45 || leagan_VALUE > 52 || 부판 != 0) teip_VALUE("supported class versions: 45..52, minor 0");
        tairiseach_COUNT = 짧은수();
        if (tairiseach_COUNT < 1 || tairiseach_COUNT > 512) { teip_VALUE("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < tairiseach_COUNT && !ERREÁID; 수++) {
            int 종류 = beart_VALUE(); tairiseach_clib[수] = 종류;
            if (종류 == 1) { tairiseach_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(tairiseach_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = slánuimhir();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); tairiseach_SECOND_VALUE[수] = 짧은수(); }
            else teip_VALUE("unsupported constant type");
        }
        int cead_VALUE = 짧은수();
        if ((cead_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) teip_VALUE("unsupported class flags");
        aicme_ainm = aicme_ainm_SMS(짧은수());
        if (!Word_SMS(aicme_ainm_SMS(짧은수()), "java/lang/Object")) teip_VALUE("inheritance unsupported");
        if (짧은수() != 0) teip_VALUE("interfaces unsupported");
        if (짧은수() != 0) teip_VALUE("fields unsupported");
        modh_COUNT = 짧은수();
        if (modh_COUNT < 1 || modh_COUNT > 32) { teip_VALUE("method count limit (32)"); return; }
        for (int 수 = 0; 수 < modh_COUNT && !ERREÁID; 수++) {
            modh_rochtain[수] = 짧은수(); modh_ainm_SMS[수] = 짧은수(); modh_TYPE[수] = 짧은수();
            seic_tairiseach(modh_ainm_SMS[수], 1); 서술읽기(수);
            if ((modh_rochtain[수] & (0x100 | 0x400 | 0x20)) != 0) teip_VALUE("native, abstract and synchronized methods unsupported");
            if ((modh_rochtain[수] & 8) == 0 && !Word_SMS(modh_ainm_SMS[수], "<init>")) teip_VALUE("instance methods unsupported");
            if (Word_SMS(modh_ainm_SMS[수], "<clinit>")) teip_VALUE("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(modh_ainm_SMS[앞], modh_ainm_SMS[수]) && 같은말(modh_TYPE[앞], modh_TYPE[수])) teip_VALUE("duplicate method");
            int mír_COUNT = 짧은수();
            for (int tréith_VALUE = 0; tréith_VALUE < mír_COUNT && !ERREÁID; tréith_VALUE++) {
                int Ainm = 짧은수(), fad_VALUE = slánuimhir(), Rith_2 = 읽기위치;
                if (!gearrthóg(Rith_2, fad_VALUE)) { teip_VALUE("truncated method attribute"); break; }
                if (Word_SMS(Ainm, "Code")) {
                    if (modh_Start[수] != 0) teip_VALUE("duplicate Code attribute");
                    modh_Cruach[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_fad = slánuimhir();
                    if (modh_Cruach[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < modh_argóint_COUNT[수]
                        || CODE_fad < 1 || CODE_fad > 8192) teip_VALUE("method memory limits exceeded");
                    modh_Start[수] = 읽기위치; 건너(CODE_fad); modh_cuir_deireadh_le[수] = 읽기위치;
                    if (짧은수() != 0) teip_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Rith_2 + fad_VALUE) teip_VALUE("Code attribute size mismatch");
                } else 건너(fad_VALUE);
            }
            if (modh_Start[수] == 0) teip_VALUE("missing Code attribute");
            int spás_iontráil = modh_Start[수];
            while (spás_iontráil < modh_cuir_deireadh_le[수] && !ERREÁID) {
                int fad_VALUE = ordú_fad(Comhad[spás_iontráil]);
                if (fad_VALUE == 0 || fad_VALUE > modh_cuir_deireadh_le[수] - spás_iontráil) { teip_VALUE("unsupported or truncated bytecode"); break; }
                경계[spás_iontráil] = 수 + 1; spás_iontráil += fad_VALUE;
            }
            // 실행하지 않는 경로에도 잘못된 craobh 목적지를 허용하지 않는다.
            spás_iontráil = modh_Start[수];
            while (spás_iontráil < modh_cuir_deireadh_le[수] && !ERREÁID) {
                int VALUE = Comhad[spás_iontráil];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int sprioc_VALUE = spás_iontráil + (short)(Comhad[spás_iontráil + 1] << 8 | Comhad[spás_iontráil + 2]);
                    if (sprioc_VALUE < modh_Start[수] || sprioc_VALUE >= modh_cuir_deireadh_le[수] || 경계[sprioc_VALUE] != 수 + 1) teip_VALUE("invalid branch target");
                }
                spás_iontráil += ordú_fad(VALUE);
            }
        }
        if (!ERREÁID) 속성건너();
        if (읽기위치 != Méid) teip_VALUE("extra class file data");
    }
    static int leithdháil_Stóras(int 종류, int fad_VALUE) {
        if (fad_VALUE < 0 || fad_VALUE > 힙.length - 힙끝 - 2) { teip_VALUE("object heap exhausted or negative array size"); return 0; }
        int Leabhair_thagartha = 힙끝; 힙끝 += fad_VALUE + 2; 힙[Leabhair_thagartha] = 종류; 힙[Leabhair_thagartha + 1] = fad_VALUE;
        return Leabhair_thagartha;
    }
    static boolean oibiacht_VALUE(int Leabhair_thagartha, int 종류) {
        if (Leabhair_thagartha < 1 || Leabhair_thagartha >= 힙끝 - 1 || 힙[Leabhair_thagartha] != 종류) { teip_VALUE("null or invalid object reference"); return false; }
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
        if (fráma_INDEX == 31) { teip_VALUE("call stack limit (32)"); return; }
        int Ar_aghaidh_mír = fráma_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) logánta_TYPE[Ar_aghaidh_mír * 128 + 수] = 0;
        for (int 수 = modh_argóint_COUNT[feidhm_VALUE] - 1; 수 >= 0; 수--) {
            logánta_VALUE[Ar_aghaidh_mír * 128 + 수] = 빼기(modh_argóint_TYPE[feidhm_VALUE * 16 + 수]); logánta_TYPE[Ar_aghaidh_mír * 128 + 수] = modh_argóint_TYPE[feidhm_VALUE * 16 + 수];
        }
        fráma_INDEX = Ar_aghaidh_mír; fráma_modh[fráma_INDEX] = feidhm_VALUE; fráma_suíomh[fráma_INDEX] = modh_Start[feidhm_VALUE]; fráma_Cruach[fráma_INDEX] = 0;
    }
    static void return_tomhas(int TYPE_VALUE) {
        if (TYPE_VALUE != modh_return[fráma_modh[fráma_INDEX]]) { teip_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        fráma_INDEX--; if (fráma_INDEX >= 0 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
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
                if (VALUE < 1 || VALUE > 127) { teip_VALUE("file stream paths currently require ASCII"); return; }
                sruth_comhad_ainm[spás_iontráil] = VALUE;
            }
            sruth_comhad_ainm[fad_VALUE] = 0;
            int 서술자 = úsáideoir.파일서술자열기(sruth_comhad_ainm, Aschur ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { teip_VALUE("FileNotFoundException: file open failed"); return; }
            힙[sruth_VALUE + 2] = 서술자; 힙[sruth_VALUE + 3] = 1;
            return;
        }
        if (Ordú != 182) { teip_VALUE("invalid file stream invocation"); return; }
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
            if (tomhas < -1) teip_VALUE("IOException: read failed"); else 넣기(tomhas, 1);
        } else if (úsáideoir.파일한바이트쓰기(서술자, VALUE) != 1) teip_VALUE("IOException: write failed");
    }
    static void CALL_modh(int INDEX, int Ordú) {
        if (!seic_tairiseach(INDEX, 10)) return;
        int úinéir_VALUE = aicme_ainm_SMS(상가[INDEX]), Ainm = Leabhair_thagartha_ainm(tairiseach_SECOND_VALUE[INDEX]), formáid_VALUE = Leabhair_thagartha_TYPE(tairiseach_SECOND_VALUE[INDEX]);
        if (ERREÁID) return;
        if (같은말(úinéir_VALUE, aicme_ainm)) {
            if (Ordú != 184) { teip_VALUE("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < modh_COUNT; 수++) if (같은말(Ainm, modh_ainm_SMS[수]) && 같은말(formáid_VALUE, modh_TYPE[수])) {
                if ((modh_rochtain[수] & 8) == 0) teip_VALUE("method is not static"); else 호출(수);
                return;
            }
            teip_VALUE("NoSuchMethodError"); return;
        }
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
        teip_VALUE("unsupported library method");
    }
    static int ARRAY_spás(int Leabhair_thagartha, int foscript_VALUE, int TYPE_VALUE) {
        if (!oibiacht_VALUE(Leabhair_thagartha, TYPE_VALUE)) return 0;
        if (foscript_VALUE < 0 || foscript_VALUE >= 힙[Leabhair_thagartha + 1]) { teip_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Leabhair_thagartha + 2 + foscript_VALUE;
    }
    static void Rith_ordú() {
        int 남음 = 500000;
        while (fráma_INDEX >= 0 && !ERREÁID) {
            if (--남음 == 0) { teip_VALUE("instruction limit (500000)"); break; }
            int Rith_2 = fráma_suíomh[fráma_INDEX], VALUE = 명바();
            if (ERREÁID) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = VALUE == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= tairiseach_COUNT) teip_VALUE("invalid ldc constant");
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
            if (VALUE == 46 || VALUE == 50) {
                int foscript_VALUE = 빼기(1), Leabhair_thagartha = 빼기(2), spás_iontráil = ARRAY_spás(Leabhair_thagartha, foscript_VALUE, VALUE == 46 ? 2 : 3);
                if (!ERREÁID) 넣기(힙[spás_iontráil], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int mír_eilimint = 빼기(VALUE == 79 ? 1 : 2), foscript_VALUE = 빼기(1), Leabhair_thagartha = 빼기(2), spás_iontráil = ARRAY_spás(Leabhair_thagartha, foscript_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && mír_eilimint != 0) oibiacht_VALUE(mír_eilimint, 1);
                if (!ERREÁID) 힙[spás_iontráil] = mír_eilimint; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), TYPE_VALUE = return_TYPE; 넣기(가, TYPE_VALUE); 넣기(가, TYPE_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = return_TYPE, 나 = 빼기(0), 나형 = return_TYPE; 넣기(가, 가형); 넣기(나, 나형); continue; }
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
            if (VALUE == 178) {
                int 수 = 명짧(); if (!seic_tairiseach(수, 9)) continue;
                if (!Word_SMS(aicme_ainm_SMS(상가[수]), "java/lang/System") || !Word_SMS(Leabhair_thagartha_ainm(tairiseach_SECOND_VALUE[수]), "out")
                    || !Word_SMS(Leabhair_thagartha_TYPE(tairiseach_SECOND_VALUE[수]), "Ljava/io/PrintStream;")) teip_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_modh(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int Ainm = aicme_ainm_SMS(명짧());
                if (Word_SMS(Ainm, "java/lang/StringBuilder")) 넣기(leithdháil_Stóras(4, 1), 2);
                else if (Word_SMS(Ainm, "java/io/FileInputStream") || Word_SMS(Ainm, "java/io/FileOutputStream")) {
                    int Leabhair_thagartha = leithdháil_Stóras(Word_SMS(Ainm, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!ERREÁID) { 힙[Leabhair_thagartha + 2] = -1; 넣기(Leabhair_thagartha, 2); }
                } else teip_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) teip_VALUE("only int[] newarray is supported"); }
                else if (!Word_SMS(aicme_ainm_SMS(명짧()), "java/lang/String")) teip_VALUE("only String[] anewarray is supported");
                int fad_VALUE = 빼기(1); 넣기(leithdháil_Stóras(VALUE == 188 ? 2 : 3, fad_VALUE), 2); continue;
            }
            if (VALUE == 190) {
                int Leabhair_thagartha = 빼기(2);
                if (Leabhair_thagartha < 1 || Leabhair_thagartha >= 힙끝 - 1 || (힙[Leabhair_thagartha] != 2 && 힙[Leabhair_thagartha] != 3)) teip_VALUE("null or invalid array");
                else 넣기(힙[Leabhair_thagartha + 1], 1); continue;
            }
            if (VALUE == 192) {
                int Ainm = aicme_ainm_SMS(명짧()), Leabhair_thagartha = 빼기(2);
                if (!Word_SMS(Ainm, "java/lang/String")) teip_VALUE("unsupported checkcast");
                else if (Leabhair_thagartha != 0) oibiacht_VALUE(Leabhair_thagartha, 1);
                넣기(Leabhair_thagartha, 2); continue;
            }
            teip_VALUE("unsupported bytecode");
        }
    }
    public static int Rith_2() {
        if (úsáideoir.인수개수() == 1 && 자바도구.같음(úsáideoir.Argóintí(0), "-version")) {
            úsáideoir.Scríobh("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (úsáideoir.인수개수() < 1) { úsáideoir.Scríobh("Usage: java CLASS [ARGS]\n"); return 2; }
        int fad_VALUE = 자바도구.Ainm(comhad_ainm_SMS, úsáideoir.Argóintí(0));
        if (fad_VALUE < 1 || fad_VALUE > 57) { úsáideoir.Scríobh("java: invalid class name\n"); return 2; }
        comhad_ainm_SMS[fad_VALUE] = '.'; comhad_ainm_SMS[fad_VALUE + 1] = 'c'; comhad_ainm_SMS[fad_VALUE + 2] = 'l'; comhad_ainm_SMS[fad_VALUE + 3] = 'a'; comhad_ainm_SMS[fad_VALUE + 4] = 's'; comhad_ainm_SMS[fad_VALUE + 5] = 's';
        Méid = úsáideoir.파일읽기(comhad_ainm_SMS, Comhad);
        if (Méid < 0) { úsáideoir.Scríobh("java: cannot read class: "); 자바도구.수쓰기(Méid); úsáideoir.scríobh_carachtar_VALUE(10); return 1; }
        클래스읽기(); if (ERREÁID) return 1;
        int carachtar_ainm = tairiseach_SMS(aicme_ainm);
        if (!ERREÁID && 힙[carachtar_ainm + 1] != fad_VALUE) teip_VALUE("class name does not match file");
        for (int 수 = 0; 수 < fad_VALUE && !ERREÁID; 수++) if (힙[carachtar_ainm + 2 + 수] != comhad_ainm_SMS[수]) teip_VALUE("class name does not match file");
        int iontráil_pointe_VALUE = -1;
        for (int 수 = 0; 수 < modh_COUNT; 수++) if (Word_SMS(modh_ainm_SMS[수], "main") && Word_SMS(modh_TYPE[수], "([Ljava/lang/String;)V") && (modh_rochtain[수] & 9) == 9) iontráil_pointe_VALUE = 수;
        if (iontráil_pointe_VALUE < 0) teip_VALUE("public static void main(String[] args) required");
        if (ERREÁID) return 1;
        int Argóintí = leithdháil_Stóras(3, úsáideoir.인수개수() - 1);
        for (int 수 = 1; 수 < úsáideoir.인수개수() && !ERREÁID; 수++) 힙[Argóintí + 1 + 수] = óstach_carachtar(úsáideoir.Argóintí(수));
        fráma_INDEX = 0; fráma_modh[0] = iontráil_pointe_VALUE; fráma_suíomh[0] = modh_Start[iontráil_pointe_VALUE]; logánta_VALUE[0] = Argóintí; logánta_TYPE[0] = 2;
        Rith_ordú(); return ERREÁID ? 1 : 0;
    }
}
