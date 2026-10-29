// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Kōnae/스택/Pūranga_kōrero/peka 경계를 kawe_tono 중 검사한다. */
public final class 자바가상기계 {
    static int[] Kōnae = new int[16 * 16384], 임시파일 = new int[16384], kōnae_ingoa_TEXT = new int[512];
    static int[] taimau_tūtohu = new int[8192], 상가 = new int[8192], taimau_SECOND_uara = new int[8192], aho_Pūranga_kōrero = new int[8192];
    static int[] aratuka_ingoa_TEXT = new int[512], aratuka_TYPE = new int[512], aratuka_uru = new int[512], aratuka_kaipupuri = new int[512];
    static int[] aratuka_Start = new int[512], aratuka_mutu = new int[512], aratuka_Huinga = new int[512], 함수지역 = new int[512];
    static int[] aratuka_tohenga_COUNT = new int[512], aratuka_tohenga_TYPE = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] paetata_uara = new int[16384], paetata_TYPE = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] tāpare_aratuka = new int[128], tāpare_tūranga = new int[128], tāpare_Huinga = new int[128], tāpare_tohutohu = new int[128], arawhiti_tāpare = new int[128];
    static int[] tauaha_Whakamāramatanga_ingoa = new int[16], tauaha_Whakamāramatanga_rahi = new int[16], 종부모 = new int[16], tauaha_Whakamāramatanga_tūnga = new int[16], tauaha_kāniwha_COUNT = new int[16], arawhiti_tauaha_Whakamāramatanga = new int[16];
    static int[] tauaha_atanga = new int[16 * 16], tauaha_atanga_COUNT = new int[16];
    static int[] kāniwha_ingoa = new int[512], kāniwha_TYPE = new int[512], kāniwha_kaipupuri = new int[512], kāniwha_whakaaetanga = new int[512], kāniwha_tūranga = new int[512], kāniwha_raraunga = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], HUĀNGA_huānga = new int[32768], Store_tau_tōpū = new int[256];
    static int rahi, 읽기위치, aratuka_COUNT, tauaha_ingoa, tāpare_INDEX = -1, 힙끝 = 1, 반환형;
    static int tauaha_Whakamāramatanga_COUNT, kāniwha_COUNT, 잡기수, 현재읽는종, 던진객체, 잠시수, whakaatu_COUNT, Kohinga_COUNT;
    static int 현재가닥, miro_COUNT = 1, tāurunga_tauaha_Whakamāramatanga;
    static int[] miro_tāpare = new int[4], miro_tūnga = new int[4], miro_ahanoa = new int[4], miro_ūnga = new int[4], 가닥대기 = new int[4];
    static boolean Pōhēhē, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], tauaha_miro = new int[16];

    static void rahunga_uara(String Word_TEXT) {
        if (Pōhēhē) return;
        int kāwai_CODE = 0;
        if (자바도구.같음(Word_TEXT, "ArithmeticException: / by zero")) kāwai_CODE = 4;
        if (자바도구.같음(Word_TEXT, "NullPointerException") || 자바도구.같음(Word_TEXT, "null or invalid array")) kāwai_CODE = 5;
        if (자바도구.같음(Word_TEXT, "ArrayIndexOutOfBoundsException")) kāwai_CODE = 7;
        if (자바도구.같음(Word_TEXT, "StringIndexOutOfBoundsException")) kāwai_CODE = 8;
        if (자바도구.같음(Word_TEXT, "NumberFormatException")) kāwai_CODE = 10;
        if (자바도구.같음(Word_TEXT, "FileNotFoundException: file open failed")) kāwai_CODE = 12;
        if (자바도구.같음(Word_TEXT, "IOException: stream closed") || 자바도구.같음(Word_TEXT, "IOException: read failed") || 자바도구.같음(Word_TEXT, "IOException: write failed")) kāwai_CODE = 11;
        if (자바도구.같음(Word_TEXT, "ClassCastException")) kāwai_CODE = 14;
        if (자바도구.같음(Word_TEXT, "NegativeArraySizeException")) kāwai_CODE = 15;
        if (kāwai_CODE != 0 && tāpare_INDEX >= 0) { 예외던짐(kāwai_CODE, Word_TEXT); return; }
        kaiwhakamahi.Tuhia("JVM error: "); kaiwhakamahi.Tuhia(Word_TEXT); kaiwhakamahi.tuhi_pūāhua_uara(10); Pōhēhē = true;
    }
    static boolean topenga(int whakahaere, int roa_uara) {
        if (whakahaere < 0 || whakahaere >= Kōnae.length || roa_uara < 0) return false;
        int tauaha_Whakamāramatanga = whakahaere / 16384;
        return whakahaere % 16384 <= tauaha_Whakamāramatanga_rahi[tauaha_Whakamāramatanga] && roa_uara <= tauaha_Whakamāramatanga_rahi[tauaha_Whakamāramatanga] - whakahaere % 16384;
    }
    static int paita_uara() {
        if (!topenga(읽기위치, 1)) { rahunga_uara("truncated class file"); return 0; }
        return Kōnae[읽기위치++];
    }
    static int 짧은수() { return paita_uara() << 8 | paita_uara(); }
    static int tau_tōpū() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int roa_uara) { if (!topenga(읽기위치, roa_uara)) rahunga_uara("invalid attribute size"); else 읽기위치 += roa_uara; }
    static boolean taki_taimau(int 수, int 종류) {
        if (수 <= 0 || 수 >= taimau_tūtohu.length || taimau_tūtohu[수] != 종류) { rahunga_uara("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int whakahaere, int roa_uara, String Word_TEXT) {
        if (!topenga(whakahaere, roa_uara)) return false;
        int 읽는자리 = whakahaere, 끝 = whakahaere + roa_uara;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_TEXT.length(); Loop_INDEX++) {
            int waehere_pūāhua = Word_TEXT.charAt(Loop_INDEX);
            if (waehere_pūāhua > 0 && waehere_pūāhua < 128) { if (읽는자리 >= 끝 || Kōnae[읽는자리++] != waehere_pūāhua) return false; }
            else if (waehere_pūāhua < 2048) {
                if (읽는자리 + 2 > 끝 || Kōnae[읽는자리++] != (192 | (waehere_pūāhua >> 6)) || Kōnae[읽는자리++] != (128 | (waehere_pūāhua & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Kōnae[읽는자리++] != (224 | (waehere_pūāhua >> 12)) || Kōnae[읽는자리++] != (128 | ((waehere_pūāhua >> 6) & 63)) || Kōnae[읽는자리++] != (128 | (waehere_pūāhua & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Word_TEXT(int taimau_uara, String Word_TEXT) { return taki_taimau(taimau_uara, 1) && 구간(상가[taimau_uara], taimau_SECOND_uara[taimau_uara], Word_TEXT); }
    static boolean 같은말(int 가, int 나) {
        if (!taki_taimau(가, 1) || !taki_taimau(나, 1) || taimau_SECOND_uara[가] != taimau_SECOND_uara[나]) return false;
        for (int 수 = 0; 수 < taimau_SECOND_uara[가]; 수++) if (Kōnae[상가[가] + 수] != Kōnae[상가[나] + 수]) return false;
        return true;
    }
    static int tauaha_ingoa_TEXT(int 수) { return taki_taimau(수, 7) && taki_taimau(상가[수], 1) ? 상가[수] : 0; }
    static int Pūranga_kōrero_ingoa(int 수) { return taki_taimau(수, 12) && taki_taimau(상가[수], 1) ? 상가[수] : 0; }
    static int Pūranga_kōrero_TYPE(int 수) { return taki_taimau(수, 12) && taki_taimau(taimau_SECOND_uara[수], 1) ? taimau_SECOND_uara[수] : 0; }
    static int 서술형(int 끝, boolean putua_TYPE) {
        if (읽기위치 >= 끝) { rahunga_uara("invalid descriptor"); return 0; }
        int uara = paita_uara();
        if (uara == 'V' && putua_TYPE) return 0;
        if (uara == 'I' || uara == 'B' || uara == 'C' || uara == 'S' || uara == 'Z') return 1;
        if (uara == '[') { 서술형(끝, false); return 2; }
        if (uara == 'L') {
            int whakahaere = 읽기위치;
            while (읽기위치 < 끝 && Kōnae[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == whakahaere) rahunga_uara("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        rahunga_uara("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int TAUMAHI_uara) {
        int 이전 = 읽기위치, 수 = aratuka_TYPE[TAUMAHI_uara];
        if (!taki_taimau(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + taimau_SECOND_uara[수];
        if (paita_uara() != '(') rahunga_uara("invalid method descriptor");
        int tuemi_COUNT = 0;
        while (!Pōhēhē && 읽기위치 < 끝 && Kōnae[읽기위치] != ')') {
            if (tuemi_COUNT == 16) { rahunga_uara("too many method arguments"); break; }
            aratuka_tohenga_TYPE[TAUMAHI_uara * 16 + tuemi_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || paita_uara() != ')') rahunga_uara("invalid method descriptor");
        함수반환[TAUMAHI_uara] = 서술형(끝, true); aratuka_tohenga_COUNT[TAUMAHI_uara] = tuemi_COUNT;
        if (읽기위치 != 끝) rahunga_uara("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int uara = 짧은수(); return uara == 0 ? 0 : 현재읽는종 * 512 + uara; }
    static int 명상수() { return aratuka_kaipupuri[tāpare_aratuka[tāpare_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int tuemi_COUNT = 짧은수();
        for (int 수 = 0; 수 < tuemi_COUNT && !Pōhēhē; 수++) { taki_taimau(상번호(), 1); 건너(tau_tōpū()); }
    }
    static int tono_roa(int uara) {
        if (uara == 16 || uara == 18 || uara == 21 || uara == 25 || uara == 54 || uara == 58 || uara == 188) return 2;
        if (uara == 17 || uara == 19 || uara == 132 || uara >= 153 && uara <= 167
            || uara >= 178 && uara <= 184 || uara == 187 || uara == 189 || uara == 192 || uara == 193 || uara == 198 || uara == 199) return 3;
        if (uara == 185 || uara == 200) return 5;
        if (uara >= 0 && uara <= 8 || uara >= 26 && uara <= 29 || uara >= 42 && uara <= 46 || uara >= 50 && uara <= 53
            || uara >= 59 && uara <= 62 || uara >= 75 && uara <= 79 || uara >= 83 && uara <= 95
            || uara == 96 || uara == 100 || uara == 104 || uara == 108 || uara == 112 || uara == 116
            || uara == 120 || uara == 122 || uara == 124 || uara == 126 || uara == 128 || uara == 130
            || uara >= 145 && uara <= 147 || uara == 172 || uara == 176 || uara == 177 || uara == 190 || uara == 191
            || uara == 194 || uara == 195) return 1;
        return 0;
    }
    static int tūranga_tau_tōpū(int 읽는자리) {
        if (!topenga(읽는자리, 4)) { rahunga_uara("truncated bytecode operand"); return 0; }
        return Kōnae[읽는자리] << 24 | Kōnae[읽는자리 + 1] << 16 | Kōnae[읽는자리 + 2] << 8 | Kōnae[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int whakahaere, int 끝) {
        int uara = Kōnae[읽는자리], roa_uara = tono_roa(uara);
        if (uara == 170 || uara == 171) {
            int BASE_tūranga = 읽는자리 + 1;
            while ((BASE_tūranga - whakahaere) % 4 != 0) BASE_tūranga++;
            if (끝 - BASE_tūranga < (uara == 170 ? 12 : 8)) return 0;
            int tāurunga_COUNT = uara == 170 ? tūranga_tau_tōpū(BASE_tūranga + 8) - tūranga_tau_tōpū(BASE_tūranga + 4) + 1 : tūranga_tau_tōpū(BASE_tūranga + 4);
            if (tāurunga_COUNT < 0 || tāurunga_COUNT > 2048) return 0;
            roa_uara = BASE_tūranga - 읽는자리 + (uara == 170 ? 12 + 4 * tāurunga_COUNT : 8 + 8 * tāurunga_COUNT);
        }
        if (uara == 196 && 읽는자리 + 1 < 끝) {
            int Word_raraunga = Kōnae[읽는자리 + 1]; roa_uara = Word_raraunga == 132 ? 6 : (Word_raraunga == 21 || Word_raraunga == 25 || Word_raraunga == 54 || Word_raraunga == 58) ? 4 : 0;
        }
        return roa_uara > 0 && roa_uara <= 끝 - 읽는자리 ? roa_uara : 0;
    }
    static void taki_ūnga_uara(int ūnga_uara, int TAUMAHI_uara) {
        if (ūnga_uara < aratuka_Start[TAUMAHI_uara] || ūnga_uara >= aratuka_mutu[TAUMAHI_uara] || 경계[ūnga_uara] != TAUMAHI_uara + 1) rahunga_uara("invalid branch target");
    }
    static void 클래스읽기(int tauaha_Whakamāramatanga) {
        현재읽는종 = tauaha_Whakamāramatanga; 읽기위치 = tauaha_Whakamāramatanga * 16384; rahi = 읽기위치 + tauaha_Whakamāramatanga_rahi[tauaha_Whakamāramatanga];
        if (tau_tōpū() != 0xcafebabe) { rahunga_uara("not a class file"); return; }
        int 부판 = 짧은수(), putanga_uara = 짧은수();
        if (putanga_uara < 45 || putanga_uara > 52 || 부판 != 0) { rahunga_uara("supported class versions: 45..52, minor 0"); return; }
        int taimau_COUNT = 짧은수(), BASE_tūranga = tauaha_Whakamāramatanga * 512;
        if (taimau_COUNT < 1 || taimau_COUNT > 512) { rahunga_uara("constant pool limit (511)"); return; }
        for (int tāurunga_COUNT = 1; tāurunga_COUNT < taimau_COUNT && !Pōhēhē; tāurunga_COUNT++) {
            int 수 = BASE_tūranga + tāurunga_COUNT, 종류 = paita_uara(); taimau_tūtohu[수] = 종류;
            if (종류 == 1) { taimau_SECOND_uara[수] = 짧은수(); 상가[수] = 읽기위치; 건너(taimau_SECOND_uara[수]); }
            else if (종류 == 3) 상가[수] = tau_tōpū();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); taimau_SECOND_uara[수] = 상번호(); }
            else rahunga_uara("unsupported constant type");
        }
        int mana_uru_uara = 짧은수();
        if ((mana_uru_uara & (0x2000 | 0x4000)) != 0) rahunga_uara("annotation/enum class unsupported");
        tauaha_Whakamāramatanga_ingoa[tauaha_Whakamāramatanga] = tauaha_ingoa_TEXT(상번호());
        종부모[tauaha_Whakamāramatanga] = tauaha_ingoa_TEXT(상번호());
        int atanga_COUNT = 짧은수(); if (atanga_COUNT > 16) { rahunga_uara("interface count limit"); return; }
        tauaha_atanga_COUNT[tauaha_Whakamāramatanga] = atanga_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < atanga_COUNT; Loop_INDEX++) tauaha_atanga[tauaha_Whakamāramatanga * 16 + Loop_INDEX] = tauaha_ingoa_TEXT(상번호());
        int āpure_COUNT = 짧은수();
        if (āpure_COUNT > 512 - kāniwha_COUNT) { rahunga_uara("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < āpure_COUNT && !Pōhēhē; Loop_INDEX++) {
            int kōnae_INDEX = kāniwha_COUNT++; kāniwha_kaipupuri[kōnae_INDEX] = tauaha_Whakamāramatanga; kāniwha_whakaaetanga[kōnae_INDEX] = 짧은수(); kāniwha_ingoa[kōnae_INDEX] = 상번호(); kāniwha_TYPE[kōnae_INDEX] = 상번호();
            taki_taimau(kāniwha_ingoa[kōnae_INDEX], 1); taki_taimau(kāniwha_TYPE[kōnae_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[kāniwha_TYPE[kōnae_INDEX]]; int kāwai_CODE = 서술형(읽기위치 + taimau_SECOND_uara[kāniwha_TYPE[kōnae_INDEX]], false); 읽기위치 = 보존값;
            if ((kāniwha_whakaaetanga[kōnae_INDEX] & 8) == 0) kāniwha_tūranga[kōnae_INDEX] = tauaha_kāniwha_COUNT[tauaha_Whakamāramatanga]++;
            int huanga_raraunga = 짧은수();
            for (int hono_roto_tūranga = 0; hono_roto_tūranga < huanga_raraunga && !Pōhēhē; hono_roto_tūranga++) {
                int ingoa_taimau = 상번호(), 유효길이 = tau_tōpū();
                if (Word_TEXT(ingoa_taimau, "ConstantValue") && 유효길이 == 2) {
                    int raraunga_uara = 상번호();
                    if (kāwai_CODE == 1 && taki_taimau(raraunga_uara, 3)) kāniwha_raraunga[kōnae_INDEX] = 상가[raraunga_uara];
                    else if (kāwai_CODE == 2 && taki_taimau(raraunga_uara, 8)) kāniwha_raraunga[kōnae_INDEX] = taimau_TEXT(상가[raraunga_uara]);
                } else 건너(유효길이);
            }
        }
        int tuemi_COUNT = 짧은수();
        if (tuemi_COUNT > 512 - aratuka_COUNT) { rahunga_uara("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < tuemi_COUNT && !Pōhēhē; Loop_INDEX++) {
            int 수 = aratuka_COUNT++; aratuka_kaipupuri[수] = tauaha_Whakamāramatanga;
            aratuka_uru[수] = 짧은수(); aratuka_ingoa_TEXT[수] = 상번호(); aratuka_TYPE[수] = 상번호();
            taki_taimau(aratuka_ingoa_TEXT[수], 1); 서술읽기(수);
            if ((aratuka_uru[수] & 8) == 0) {
                if (aratuka_tohenga_COUNT[수] == 16) { rahunga_uara("too many instance method arguments"); return; }
                for (int 비교자리 = aratuka_tohenga_COUNT[수]; 비교자리 > 0; 비교자리--) aratuka_tohenga_TYPE[수 * 16 + 비교자리] = aratuka_tohenga_TYPE[수 * 16 + 비교자리 - 1];
                aratuka_tohenga_TYPE[수 * 16] = 2; aratuka_tohenga_COUNT[수]++;
            }
            if ((aratuka_uru[수] & 0x100) != 0) rahunga_uara("user native method unsupported");
            if (Word_TEXT(aratuka_ingoa_TEXT[수], "<clinit>")) arawhiti_tauaha_Whakamāramatanga[tauaha_Whakamāramatanga] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (aratuka_kaipupuri[앞] == tauaha_Whakamāramatanga && 같은말(aratuka_ingoa_TEXT[앞], aratuka_ingoa_TEXT[수]) && 같은말(aratuka_TYPE[앞], aratuka_TYPE[수])) rahunga_uara("duplicate method");
            int huanga_COUNT = 짧은수();
            for (int huanga_uara = 0; huanga_uara < huanga_COUNT && !Pōhēhē; huanga_uara++) {
                int Ingoa = 상번호(), roa_uara = tau_tōpū(), whakahaere = 읽기위치;
                if (!topenga(whakahaere, roa_uara)) { rahunga_uara("truncated method attribute"); break; }
                if (Word_TEXT(Ingoa, "Code")) {
                    if (aratuka_Start[수] != 0) rahunga_uara("duplicate Code attribute");
                    aratuka_Huinga[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_roa = tau_tōpū();
                    if (aratuka_Huinga[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < aratuka_tohenga_COUNT[수]
                        || CODE_roa < 1 || CODE_roa > 8192) rahunga_uara("method memory limits exceeded");
                    aratuka_Start[수] = 읽기위치; 건너(CODE_roa); aratuka_mutu[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { rahunga_uara("exception table limit"); return; }
                    for (int hono_roto_tūranga = 0; hono_roto_tūranga < 잡는수; hono_roto_tūranga++) {
                        int hapa_Pūranga_kōrero = 잡기수++; 잡기함수[hapa_Pūranga_kōrero] = 수;
                        잡기시작[hapa_Pūranga_kōrero] = aratuka_Start[수] + 짧은수(); 잡기끝[hapa_Pūranga_kōrero] = aratuka_Start[수] + 짧은수();
                        잡기위치[hapa_Pūranga_kōrero] = aratuka_Start[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[hapa_Pūranga_kōrero] = 부호값 == 0 ? 0 : tauaha_ingoa_TEXT(부호값);
                    }
                    속성건너();
                    if (읽기위치 != whakahaere + roa_uara) rahunga_uara("Code attribute size mismatch");
                } else 건너(roa_uara);
            }
            if ((aratuka_uru[수] & 0x400) != 0) continue;
            if (aratuka_Start[수] == 0) rahunga_uara("missing Code attribute");
            int kāniwha_tāurunga = aratuka_Start[수];
            while (kāniwha_tāurunga < aratuka_mutu[수] && !Pōhēhē) {
                int roa_uara = 길이읽기(kāniwha_tāurunga, aratuka_Start[수], aratuka_mutu[수]);
                if (roa_uara == 0) { rahunga_uara("unsupported or truncated bytecode"); break; }
                경계[kāniwha_tāurunga] = 수 + 1; kāniwha_tāurunga += roa_uara;
            }
            kāniwha_tāurunga = aratuka_Start[수];
            while (kāniwha_tāurunga < aratuka_mutu[수] && !Pōhēhē) {
                int uara = Kōnae[kāniwha_tāurunga];
                if (uara >= 153 && uara <= 167 || uara == 198 || uara == 199) taki_ūnga_uara(kāniwha_tāurunga + (short)(Kōnae[kāniwha_tāurunga + 1] << 8 | Kōnae[kāniwha_tāurunga + 2]), 수);
                if (uara == 200) taki_ūnga_uara(kāniwha_tāurunga + tūranga_tau_tōpū(kāniwha_tāurunga + 1), 수);
                if (uara == 170 || uara == 171) {
                    int 읽는자리 = kāniwha_tāurunga + 1; while ((읽는자리 - aratuka_Start[수]) % 4 != 0) 읽는자리++;
                    taki_ūnga_uara(kāniwha_tāurunga + tūranga_tau_tōpū(읽는자리), 수);
                    int tāurunga_COUNT = uara == 170 ? tūranga_tau_tōpū(읽는자리 + 8) - tūranga_tau_tōpū(읽는자리 + 4) + 1 : tūranga_tau_tōpū(읽는자리 + 4);
                    읽는자리 += uara == 170 ? 12 : 8;
                    for (int hono_roto_tūranga = 0; hono_roto_tūranga < tāurunga_COUNT; hono_roto_tūranga++) taki_ūnga_uara(kāniwha_tāurunga + tūranga_tau_tōpū(읽는자리 + hono_roto_tūranga * (uara == 170 ? 4 : 8) + (uara == 170 ? 0 : 4)), 수);
                }
                kāniwha_tāurunga += 길이읽기(kāniwha_tāurunga, aratuka_Start[수], aratuka_mutu[수]);
            }
            for (int hono_roto_tūranga = 0; hono_roto_tūranga < 잡기수; hono_roto_tūranga++) if (잡기함수[hono_roto_tūranga] == 수) {
                taki_ūnga_uara(잡기시작[hono_roto_tūranga], 수); taki_ūnga_uara(잡기위치[hono_roto_tūranga], 수);
                if (잡기끝[hono_roto_tūranga] != aratuka_mutu[수]) taki_ūnga_uara(잡기끝[hono_roto_tūranga], 수);
                if (잡기시작[hono_roto_tūranga] >= 잡기끝[hono_roto_tūranga]) rahunga_uara("invalid exception range");
            }
        }
        if (!Pōhēhē) 속성건너();
        if (읽기위치 != rahi) rahunga_uara("extra class file data");
    }
    static int tiritiri_Rokiroki(int 종류, int roa_uara) { return 새기억(종류, roa_uara); }
    static boolean ahanoa_uara(int Pūranga_kōrero, int 종류) {
        if (!객체유효(Pūranga_kōrero)) return false;
        if (힙[Pūranga_kōrero] != 종류) { rahunga_uara("object type mismatch"); return false; }
        return true;
    }
    static int taimau_TEXT(int INDEX) {
        if (!taki_taimau(INDEX, 1)) return 0;
        if (aho_Pūranga_kōrero[INDEX] != 0) return aho_Pūranga_kōrero[INDEX];
        int Pūranga_kōrero = tiritiri_Rokiroki(1, taimau_SECOND_uara[INDEX]); if (Pōhēhē) return 0;
        int 끝 = 상가[INDEX] + taimau_SECOND_uara[INDEX], 수 = 상가[INDEX], roa_uara = 0;
        while (수 < 끝 && !Pōhēhē) {
            int uara = Kōnae[수++];
            if (uara == 0) rahunga_uara("invalid modified UTF-8");
            else if (uara >= 192 && uara <= 223 && 수 < 끝) {
                int Panuku_tuemi = Kōnae[수++];
                if ((Panuku_tuemi & 192) != 128) rahunga_uara("invalid modified UTF-8");
                uara = (uara & 31) << 6 | Panuku_tuemi & 63;
                if (uara != 0 && uara < 128) rahunga_uara("overlong modified UTF-8");
            } else if (uara >= 224 && uara <= 239 && 수 + 1 < 끝) {
                int 가 = Kōnae[수++], 나 = Kōnae[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) rahunga_uara("invalid modified UTF-8");
                uara = (uara & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (uara < 2048) rahunga_uara("overlong modified UTF-8");
            } else if (uara >= 128) rahunga_uara("invalid modified UTF-8");
            힙[Pūranga_kōrero + 2 + roa_uara++] = uara;
        }
        힙[Pūranga_kōrero + 1] = roa_uara; aho_Pūranga_kōrero[INDEX] = Pūranga_kōrero; return Pūranga_kōrero;
    }
    static int taurima_pūāhua(String uara) {
        int Pūranga_kōrero = tiritiri_Rokiroki(1, uara.length()); if (Pōhēhē) return 0;
        for (int 수 = 0; 수 < uara.length(); 수++) 힙[Pūranga_kōrero + 2 + 수] = uara.charAt(수);
        return Pūranga_kōrero;
    }
    static void tuhi_TEXT(int Pūranga_kōrero) {
        if (Pūranga_kōrero == 0) { kaiwhakamahi.Tuhia("null"); return; }
        if (!ahanoa_uara(Pūranga_kōrero, 1)) return;
        for (int 수 = 0; 수 < 힙[Pūranga_kōrero + 1]; 수++) kaiwhakamahi.tuhi_pūāhua_uara(힙[Pūranga_kōrero + 2 + 수]);
    }
    static int mati_pūāhua(int uara) {
        int Pūranga_kōrero = tiritiri_Rokiroki(1, 11); if (Pōhēhē) return 0;
        int roa_uara = 0;
        if (uara < 0) 힙[Pūranga_kōrero + 2 + roa_uara++] = '-'; else uara = -uara;
        int tūranga_INDEX = 1000000000; boolean whakahaere = false;
        while (tūranga_INDEX != 0) {
            int 수 = -(uara / tūranga_INDEX);
            if (수 != 0 || whakahaere || tūranga_INDEX == 1) { 힙[Pūranga_kōrero + 2 + roa_uara++] = '0' + 수; whakahaere = true; }
            uara %= tūranga_INDEX; tūranga_INDEX /= 10;
        }
        힙[Pūranga_kōrero + 1] = roa_uara; return Pūranga_kōrero;
    }
    static int 정수해독(int Pūranga_kōrero) {
        if (!ahanoa_uara(Pūranga_kōrero, 1)) return 0;
        int roa_uara = 힙[Pūranga_kōrero + 1], 수 = 0, uara = 0; boolean 음수 = false;
        if (roa_uara > 0 && (힙[Pūranga_kōrero + 2] == '-' || 힙[Pūranga_kōrero + 2] == '+')) { 음수 = 힙[Pūranga_kōrero + 2] == '-'; 수++; }
        if (수 == roa_uara) rahunga_uara("NumberFormatException");
        for (; 수 < roa_uara && !Pōhēhē; 수++) {
            int mati_uara = 힙[Pūranga_kōrero + 2 + 수] - '0';
            if (mati_uara < 0 || mati_uara > 9 || uara < -214748364 || uara == -214748364 && mati_uara > (음수 ? 8 : 7)) rahunga_uara("NumberFormatException");
            uara = uara * 10 - mati_uara;
        }
        return 음수 ? uara : -uara;
    }
    static void 넣기(int uara, int TYPE_uara) {
        if (Pōhēhē) return;
        if (tāpare_INDEX < 0 || tāpare_Huinga[tāpare_INDEX] >= aratuka_Huinga[tāpare_aratuka[tāpare_INDEX]]) { rahunga_uara("operand stack overflow"); return; }
        int kāniwha_tāurunga = tāpare_INDEX * 128 + tāpare_Huinga[tāpare_INDEX]++; 스택값[kāniwha_tāurunga] = uara; 스택형[kāniwha_tāurunga] = TYPE_uara;
    }
    static int 빼기(int TYPE_uara) {
        if (Pōhēhē) return 0;
        if (tāpare_INDEX < 0 || tāpare_Huinga[tāpare_INDEX] < 1) { rahunga_uara("operand stack underflow"); return 0; }
        int kāniwha_tāurunga = tāpare_INDEX * 128 + --tāpare_Huinga[tāpare_INDEX]; 반환형 = 스택형[kāniwha_tāurunga];
        if (TYPE_uara != 0 && 반환형 != TYPE_uara) rahunga_uara("operand type mismatch");
        if (반환형 == 2) pare_uara(스택값[kāniwha_tāurunga]);
        return 스택값[kāniwha_tāurunga];
    }
    static void 지역읽기(int INDEX, int TYPE_uara) {
        if (INDEX >= 함수지역[tāpare_aratuka[tāpare_INDEX]] || INDEX < 0 || paetata_TYPE[tāpare_INDEX * 128 + INDEX] != TYPE_uara) { rahunga_uara("invalid or uninitialized local"); return; }
        넣기(paetata_uara[tāpare_INDEX * 128 + INDEX], TYPE_uara);
    }
    static void tuhi_paetata(int INDEX, int TYPE_uara) {
        if (INDEX >= 함수지역[tāpare_aratuka[tāpare_INDEX]] || INDEX < 0) { rahunga_uara("local index out of range"); return; }
        int uara = 빼기(TYPE_uara); paetata_uara[tāpare_INDEX * 128 + INDEX] = uara; paetata_TYPE[tāpare_INDEX * 128 + INDEX] = TYPE_uara;
    }
    static int 명바() {
        int tūranga = tāpare_tūranga[tāpare_INDEX];
        if (tūranga < aratuka_Start[tāpare_aratuka[tāpare_INDEX]] || tūranga >= aratuka_mutu[tāpare_aratuka[tāpare_INDEX]]) { rahunga_uara("instruction pointer out of range"); return 0; }
        tāpare_tūranga[tāpare_INDEX]++; return Kōnae[tūranga];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void nuku_uara(int tūranga) {
        int TAUMAHI_uara = tāpare_aratuka[tāpare_INDEX];
        if (tūranga < aratuka_Start[TAUMAHI_uara] || tūranga >= aratuka_mutu[TAUMAHI_uara] || 경계[tūranga] != TAUMAHI_uara + 1) rahunga_uara("invalid branch target");
        else tāpare_tūranga[tāpare_INDEX] = tūranga;
    }
    static void 호출(int TAUMAHI_uara) {
        if (tāpare_INDEX % 32 == 31) { rahunga_uara("call stack limit (32)"); return; }
        int Panuku_tuemi = tāpare_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) paetata_TYPE[Panuku_tuemi * 128 + 수] = 0;
        for (int 수 = aratuka_tohenga_COUNT[TAUMAHI_uara] - 1; 수 >= 0; 수--) {
            paetata_uara[Panuku_tuemi * 128 + 수] = 빼기(aratuka_tohenga_TYPE[TAUMAHI_uara * 16 + 수]); paetata_TYPE[Panuku_tuemi * 128 + 수] = aratuka_tohenga_TYPE[TAUMAHI_uara * 16 + 수];
        }
        if (Pōhēhē) return;
        tāpare_INDEX = Panuku_tuemi; arawhiti_tāpare[tāpare_INDEX] = 0; tāpare_aratuka[tāpare_INDEX] = TAUMAHI_uara; tāpare_tūranga[tāpare_INDEX] = aratuka_Start[TAUMAHI_uara]; tāpare_Huinga[tāpare_INDEX] = 0;
    }
    static void 반환(int TYPE_uara) {
        if (TYPE_uara != 함수반환[tāpare_aratuka[tāpare_INDEX]]) { rahunga_uara("return type mismatch"); return; }
        int uara = TYPE_uara == 0 ? 0 : 빼기(TYPE_uara);
        if (arawhiti_tāpare[tāpare_INDEX] != 0) tauaha_Whakamāramatanga_tūnga[arawhiti_tāpare[tāpare_INDEX] - 1] = 2;
        if (틀잠금[tāpare_INDEX] != 0) { 잠금풀기(틀잠금[tāpare_INDEX]); 틀잠금[tāpare_INDEX] = 0; }
        tāpare_INDEX--; if (tāpare_INDEX >= 현재가닥 * 32 && TYPE_uara != 0) 넣기(uara, TYPE_uara);
    }
    static int[] roma_kōnae_ingoa = new int[64];
    static void kōnae_roma_CALL(int kaipupuri_uara, int Ingoa, int hōputu_uara, int tono) {
        boolean 출력 = Word_TEXT(kaipupuri_uara, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (tono == 183 && Word_TEXT(Ingoa, "<init>")) {
            boolean 이어 = false;
            if (출력 && Word_TEXT(hōputu_uara, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_TEXT(hōputu_uara, "(Ljava/lang/String;)V")) { rahunga_uara("unsupported file stream constructor"); return; }
            int kōnae_tāurunga_ingoa = 빼기(2), roma_uara = 빼기(2);
            if (!ahanoa_uara(kōnae_tāurunga_ingoa, 1) || !ahanoa_uara(roma_uara, 종류) || Pōhēhē) return;
            if (힙[roma_uara + 3] != 0) { rahunga_uara("file stream already initialized"); return; }
            int roa_uara = 힙[kōnae_tāurunga_ingoa + 1];
            if (roa_uara < 1 || roa_uara > 63) { rahunga_uara("invalid file name length"); return; }
            for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < roa_uara; kāniwha_tāurunga++) {
                int uara = 힙[kōnae_tāurunga_ingoa + 2 + kāniwha_tāurunga];
                if (uara < 1) { rahunga_uara("invalid file stream path"); return; }
                roma_kōnae_ingoa[kāniwha_tāurunga] = uara;
            }
            roma_kōnae_ingoa[roa_uara] = 0;
            int 서술자 = kaiwhakamahi.파일서술자열기(roma_kōnae_ingoa, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { rahunga_uara("FileNotFoundException: file open failed"); return; }
            힙[roma_uara + 2] = 서술자; 힙[roma_uara + 3] = 1;
            return;
        }
        if (tono != 182) { rahunga_uara("invalid file stream invocation"); return; }
        if ((출력 && Word_TEXT(Ingoa, "write") || !출력 && Word_TEXT(Ingoa, "read"))
            && (Word_TEXT(hōputu_uara, 출력 ? "([B)V" : "([B)I") || Word_TEXT(hōputu_uara, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean topenga_uara = Word_TEXT(hōputu_uara, 출력 ? "([BII)V" : "([BII)I");
            int tāurunga_COUNT = topenga_uara ? 빼기(1) : 0, 시작점 = topenga_uara ? 빼기(1) : 0, raraunga_HUĀNGA = 빼기(2), ahanoa_Pūranga_kōrero = 빼기(2);
            if (!ahanoa_uara(raraunga_HUĀNGA, 20) || !ahanoa_uara(ahanoa_Pūranga_kōrero, 종류)) return;
            if (!topenga_uara) tāurunga_COUNT = 힙[raraunga_HUĀNGA + 1];
            if (시작점 < 0 || tāurunga_COUNT < 0 || 시작점 > 힙[raraunga_HUĀNGA + 1] - tāurunga_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[ahanoa_Pūranga_kōrero + 3] == 0 || 힙[ahanoa_Pūranga_kōrero + 2] < 0) { rahunga_uara("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < tāurunga_COUNT && !Pōhēhē) {
                int 반환값 = 출력 ? kaiwhakamahi.파일한바이트쓰기(힙[ahanoa_Pūranga_kōrero + 2], 힙[raraunga_HUĀNGA + 2 + 시작점 + 완료수]) : kaiwhakamahi.파일한바이트읽기(힙[ahanoa_Pūranga_kōrero + 2]);
                if (반환값 < 0) { rahunga_uara(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[raraunga_HUĀNGA + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(tāurunga_COUNT != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Word_TEXT(Ingoa, "flush") && Word_TEXT(hōputu_uara, "()V")) { int ahanoa_Pūranga_kōrero = 빼기(2); if (ahanoa_uara(ahanoa_Pūranga_kōrero, 종류) && 힙[ahanoa_Pūranga_kōrero + 2] < 0) rahunga_uara("IOException: stream closed"); return; }
        int hohenga = -1, uara = 0;
        if (Word_TEXT(Ingoa, "close") && Word_TEXT(hōputu_uara, "()V")) hohenga = 0;
        if (!출력 && Word_TEXT(Ingoa, "read") && Word_TEXT(hōputu_uara, "()I")) hohenga = 1;
        if (출력 && Word_TEXT(Ingoa, "write") && Word_TEXT(hōputu_uara, "(I)V")) { hohenga = 2; uara = 빼기(1); }
        if (hohenga < 0) { rahunga_uara("unsupported file stream method"); return; }
        int roma_uara = 빼기(2);
        if (!ahanoa_uara(roma_uara, 종류) || Pōhēhē) return;
        if (힙[roma_uara + 3] == 0) { rahunga_uara("uninitialized file stream"); return; }
        int 서술자 = 힙[roma_uara + 2];
        if (hohenga == 0) {
            if (서술자 >= 0 && kaiwhakamahi.파일서술자닫기(서술자) < 0) rahunga_uara("IOException: close failed");
            힙[roma_uara + 2] = -1; return;
        }
        if (서술자 < 0) { rahunga_uara("IOException: stream closed"); return; }
        if (hohenga == 1) {
            int mēhua = kaiwhakamahi.파일한바이트읽기(서술자);
            if (mēhua < -1) rahunga_uara("IOException: read failed"); else 넣기(mēhua == 256 ? -1 : mēhua, 1);
        } else if (kaiwhakamahi.파일한바이트쓰기(서술자, uara) != 1) rahunga_uara("IOException: write failed");
    }
    static void CALL_aratuka(int INDEX, int tono) {
        if (INDEX <= 0 || INDEX >= taimau_tūtohu.length || (taimau_tūtohu[INDEX] != 10 && taimau_tūtohu[INDEX] != 11)) { rahunga_uara("invalid method reference"); return; }
        int kaipupuri_uara = tauaha_ingoa_TEXT(상가[INDEX]), Ingoa = Pūranga_kōrero_ingoa(taimau_SECOND_uara[INDEX]), hōputu_uara = Pūranga_kōrero_TYPE(taimau_SECOND_uara[INDEX]);
        if (Pōhēhē) return;
        if (기본호출(kaipupuri_uara, Ingoa, hōputu_uara, tono)) return;
        if (Word_TEXT(kaipupuri_uara, "java/io/FileInputStream") || Word_TEXT(kaipupuri_uara, "java/io/FileOutputStream")) {
            kōnae_roma_CALL(kaipupuri_uara, Ingoa, hōputu_uara, tono); return;
        }
        if (tono == 184 && Word_TEXT(kaipupuri_uara, "java/lang/Integer") && Word_TEXT(Ingoa, "parseInt") && Word_TEXT(hōputu_uara, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (tono == 182 && Word_TEXT(kaipupuri_uara, "java/io/PrintStream") && (Word_TEXT(Ingoa, "println") || Word_TEXT(Ingoa, "print"))) {
            int TYPE_uara = 0, uara = 0;
            if (Word_TEXT(hōputu_uara, "(I)V")) { TYPE_uara = 1; uara = 빼기(1); }
            else if (Word_TEXT(hōputu_uara, "(Z)V")) { TYPE_uara = 2; uara = 빼기(1); }
            else if (Word_TEXT(hōputu_uara, "(C)V")) { TYPE_uara = 3; uara = 빼기(1); }
            else if (Word_TEXT(hōputu_uara, "(Ljava/lang/String;)V")) { TYPE_uara = 4; uara = 빼기(2); }
            else if (!Word_TEXT(hōputu_uara, "()V") || !Word_TEXT(Ingoa, "println")) rahunga_uara("unsupported print descriptor");
            if (빼기(2) != -1) rahunga_uara("invalid PrintStream receiver");
            if (Pōhēhē) return;
            if (TYPE_uara == 1) 자바도구.수쓰기(uara);
            if (TYPE_uara == 2) kaiwhakamahi.Tuhia(uara == 0 ? "false" : "true");
            if (TYPE_uara == 3) kaiwhakamahi.tuhi_pūāhua_uara(uara & 65535);
            if (TYPE_uara == 4) tuhi_TEXT(uara);
            if (Word_TEXT(Ingoa, "println")) kaiwhakamahi.tuhi_pūāhua_uara(10);
            return;
        }
        if (tono == 182 && Word_TEXT(kaipupuri_uara, "java/lang/String")) {
            if (Word_TEXT(Ingoa, "length") && Word_TEXT(hōputu_uara, "()I")) {
                int Pūranga_kōrero = 빼기(2); if (ahanoa_uara(Pūranga_kōrero, 1)) 넣기(힙[Pūranga_kōrero + 1], 1); return;
            }
            if (Word_TEXT(Ingoa, "charAt") && Word_TEXT(hōputu_uara, "(I)C")) {
                int hauraro_uara = 빼기(1), Pūranga_kōrero = 빼기(2);
                if (ahanoa_uara(Pūranga_kōrero, 1)) {
                    if (hauraro_uara < 0 || hauraro_uara >= 힙[Pūranga_kōrero + 1]) rahunga_uara("StringIndexOutOfBoundsException"); else 넣기(힙[Pūranga_kōrero + 2 + hauraro_uara], 1);
                }
                return;
            }
        }
        if (Word_TEXT(kaipupuri_uara, "java/lang/StringBuilder")) {
            if (tono == 183 && Word_TEXT(Ingoa, "<init>") && Word_TEXT(hōputu_uara, "()V")) { ahanoa_uara(빼기(2), 4); return; }
            if (tono == 182 && Word_TEXT(Ingoa, "toString") && Word_TEXT(hōputu_uara, "()Ljava/lang/String;")) {
                int Pūranga_kōrero = 빼기(2); if (ahanoa_uara(Pūranga_kōrero, 4)) 넣기(힙[Pūranga_kōrero + 2] == 0 ? taurima_pūāhua("") : 힙[Pūranga_kōrero + 2], 2); return;
            }
            if (tono == 182 && Word_TEXT(Ingoa, "append")) {
                int Ngā_kupu = 0;
                if (Word_TEXT(hōputu_uara, "(I)Ljava/lang/StringBuilder;")) Ngā_kupu = mati_pūāhua(빼기(1));
                else if (Word_TEXT(hōputu_uara, "(Z)Ljava/lang/StringBuilder;")) Ngā_kupu = taurima_pūāhua(빼기(1) == 0 ? "false" : "true");
                else if (Word_TEXT(hōputu_uara, "(C)Ljava/lang/StringBuilder;")) {
                    int uara = 빼기(1); Ngā_kupu = tiritiri_Rokiroki(1, 1); if (!Pōhēhē) 힙[Ngā_kupu + 2] = uara & 65535;
                }
                else if (Word_TEXT(hōputu_uara, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Ngā_kupu = 빼기(2); if (Ngā_kupu == 0) Ngā_kupu = taurima_pūāhua("null"); }
                else { rahunga_uara("unsupported StringBuilder append"); return; }
                int Pūranga_kōrero = 빼기(2); if (!ahanoa_uara(Pūranga_kōrero, 4) || !ahanoa_uara(Ngā_kupu, 1)) return;
                int 앞 = 힙[Pūranga_kōrero + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], Hoki_uara_roa = 힙[Ngā_kupu + 1];
                int 새글 = tiritiri_Rokiroki(1, 앞길이 + Hoki_uara_roa); if (Pōhēhē) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < Hoki_uara_roa; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[Ngā_kupu + 2 + 수];
                힙[Pūranga_kōrero + 2] = 새글; 넣기(Pūranga_kōrero, 2); return;
            }
        }
        int tauaha_Whakamāramatanga = FIND_tauaha_Whakamāramatanga(kaipupuri_uara); if (tauaha_Whakamāramatanga < 0 || Pōhēhē) return;
        int kōnae_INDEX = FIND_aratuka(tauaha_Whakamāramatanga, Ingoa, hōputu_uara);
        if (kōnae_INDEX < 0) {
            for (int waehere_pūāhua = tauaha_Whakamāramatanga, tāurunga_COUNT = 0; waehere_pūāhua >= 0 && tāurunga_COUNT < 16; tāurunga_COUNT++, waehere_pūāhua = 부모종(waehere_pūāhua))
                if (Word_TEXT(종부모[waehere_pūāhua], "java/lang/Thread")) { 가닥호출(Ingoa, hōputu_uara, tono); return; }
            rahunga_uara("NoSuchMethodError"); return;
        }
        if (((aratuka_uru[kōnae_INDEX] & 8) != 0) != (tono == 184)) { rahunga_uara("method static/instance mismatch"); return; }
        if (tono == 184) { if (!arawhiti(aratuka_kaipupuri[kōnae_INDEX], tāpare_tohutohu[tāpare_INDEX])) return; }
        else {
            int 읽는자리 = tāpare_Huinga[tāpare_INDEX] - aratuka_tohenga_COUNT[kōnae_INDEX];
            if (읽는자리 < 0 || 스택형[tāpare_INDEX * 128 + 읽는자리] != 2) { rahunga_uara("invalid method receiver"); return; }
            int ahanoa_Pūranga_kōrero = 스택값[tāpare_INDEX * 128 + 읽는자리];
            if (!객체유효(ahanoa_Pūranga_kōrero)) return;
            if (힙[ahanoa_Pūranga_kōrero] < 32 || !종포함(힙[ahanoa_Pūranga_kōrero] - 32, kaipupuri_uara)) { rahunga_uara("method receiver type mismatch"); return; }
            if (tono != 183) kōnae_INDEX = FIND_aratuka(힙[ahanoa_Pūranga_kōrero] - 32, Ingoa, hōputu_uara);
        }
        if (kōnae_INDEX < 0 || (aratuka_uru[kōnae_INDEX] & 0x400) != 0) { rahunga_uara("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((aratuka_uru[kōnae_INDEX] & 32) != 0) {
            if (tono == 184) { int waehere_pūāhua = aratuka_kaipupuri[kōnae_INDEX]; if (종잠금[waehere_pūāhua] == 0) 종잠금[waehere_pūāhua] = tiritiri_Rokiroki(8, 0); 잠금참조 = 종잠금[waehere_pūāhua]; }
            else 잠금참조 = 스택값[tāpare_INDEX * 128 + tāpare_Huinga[tāpare_INDEX] - aratuka_tohenga_COUNT[kōnae_INDEX]];
            if (!잠금얻기(잠금참조)) { if (!Pōhēhē) tāpare_tūranga[tāpare_INDEX] = tāpare_tohutohu[tāpare_INDEX]; return; }
        }
        호출(kōnae_INDEX); if (!Pōhēhē) 틀잠금[tāpare_INDEX] = 잠금참조;
    }
    static boolean 배열저장가능(int HUĀNGA_Pūranga_kōrero, int raraunga_uara) {
        if (raraunga_uara == 0 || HUĀNGA_huānga[HUĀNGA_Pūranga_kōrero] == 0) return true;
        boolean 성공여부 = HUĀNGA_huānga[HUĀNGA_Pūranga_kōrero] == -1 ? (raraunga_uara > 0 && raraunga_uara < 힙끝 && 힙[raraunga_uara] == 1) : 맞는객체(raraunga_uara, HUĀNGA_huānga[HUĀNGA_Pūranga_kōrero]);
        if (!성공여부 && !Pōhēhē) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int HUĀNGA_kāniwha(int Pūranga_kōrero, int hauraro_uara, int TYPE_uara) {
        if (!ahanoa_uara(Pūranga_kōrero, TYPE_uara)) return 0;
        if (hauraro_uara < 0 || hauraro_uara >= 힙[Pūranga_kōrero + 1]) { rahunga_uara("ArrayIndexOutOfBoundsException"); return 0; }
        return Pūranga_kōrero + 2 + hauraro_uara;
    }
    static void kawe_tono() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (Pōhēhē) { if (던진객체 != 0) 예외처리(); if (Pōhēhē || tāpare_INDEX < 현재가닥 * 32) break; }
            if (tāpare_INDEX < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!SWITCH_miro()) break; 조각 = 100; }
            if (tāpare_INDEX == 0 && tauaha_Whakamāramatanga_tūnga[tāurunga_tauaha_Whakamāramatanga] != 2 && !arawhiti(tāurunga_tauaha_Whakamāramatanga, tāpare_tūranga[tāpare_INDEX])) continue;
            if (tāpare_INDEX == 현재가닥 * 32 && 현재가닥 != 0 && (aratuka_uru[tāpare_aratuka[tāpare_INDEX]] & 32) != 0 && 틀잠금[tāpare_INDEX] == 0) {
                int ahanoa_Pūranga_kōrero = miro_ūnga[현재가닥]; if (!잠금얻기(ahanoa_Pūranga_kōrero)) { if (Pōhēhē) break; continue; } 틀잠금[tāpare_INDEX] = ahanoa_Pūranga_kōrero;
            }
            잠시수 = 0;
            if (--남음 == 0) { rahunga_uara("instruction limit (500000)"); break; }
            int whakahaere = tāpare_tūranga[tāpare_INDEX]; tāpare_tohutohu[tāpare_INDEX] = whakahaere; int uara = 명바();
            if (Pōhēhē) break;
            if (uara == 0) continue;
            if (uara == 1) { 넣기(0, 2); continue; }
            if (uara >= 2 && uara <= 8) { 넣기(uara - 3, 1); continue; }
            if (uara == 16) { 넣기((byte)명바(), 1); continue; }
            if (uara == 17) { 넣기((short)명짧(), 1); continue; }
            if (uara == 18 || uara == 19) {
                int 수 = aratuka_kaipupuri[tāpare_aratuka[tāpare_INDEX]] * 512 + (uara == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= taimau_tūtohu.length) rahunga_uara("invalid ldc constant");
                else if (taimau_tūtohu[수] == 3) 넣기(상가[수], 1);
                else if (taimau_tūtohu[수] == 8) 넣기(taimau_TEXT(상가[수]), 2);
                else rahunga_uara("unsupported ldc constant");
                continue;
            }
            if (uara == 21 || uara == 25) { 지역읽기(명바(), uara == 21 ? 1 : 2); continue; }
            if (uara >= 26 && uara <= 29) { 지역읽기(uara - 26, 1); continue; }
            if (uara >= 42 && uara <= 45) { 지역읽기(uara - 42, 2); continue; }
            if (uara == 54 || uara == 58) { tuhi_paetata(명바(), uara == 54 ? 1 : 2); continue; }
            if (uara >= 59 && uara <= 62) { tuhi_paetata(uara - 59, 1); continue; }
            if (uara >= 75 && uara <= 78) { tuhi_paetata(uara - 75, 2); continue; }
            if (uara == 46 || uara >= 50 && uara <= 53) {
                int tāurunga_tūranga = 빼기(1), ahanoa_Pūranga_kōrero = 빼기(2), kāwai_CODE = uara == 46 ? 2 : uara == 50 ? 3 : uara == 51 ? 20 : uara == 52 ? 22 : 23;
                if (uara == 51 && ahanoa_Pūranga_kōrero > 0 && ahanoa_Pūranga_kōrero < 힙끝 && 힙[ahanoa_Pūranga_kōrero] == 21) kāwai_CODE = 21;
                int 읽는자리 = HUĀNGA_kāniwha(ahanoa_Pūranga_kōrero, tāurunga_tūranga, kāwai_CODE); if (!Pōhēhē) 넣기(힙[읽는자리], uara == 50 ? 2 : 1); continue;
            }
            if (uara == 79 || uara >= 83 && uara <= 86) {
                int tāurunga_Pūranga_kōrero = 빼기(uara == 83 ? 2 : 1), tāurunga_tūranga = 빼기(1), ahanoa_Pūranga_kōrero = 빼기(2), kāwai_CODE = uara == 79 ? 2 : uara == 83 ? 3 : uara == 84 ? 20 : uara == 85 ? 22 : 23;
                if (uara == 84 && ahanoa_Pūranga_kōrero > 0 && ahanoa_Pūranga_kōrero < 힙끝 && 힙[ahanoa_Pūranga_kōrero] == 21) kāwai_CODE = 21;
                int 읽는자리 = HUĀNGA_kāniwha(ahanoa_Pūranga_kōrero, tāurunga_tūranga, kāwai_CODE);
                if (!Pōhēhē && kāwai_CODE == 3 && !배열저장가능(ahanoa_Pūranga_kōrero, tāurunga_Pūranga_kōrero)) continue;
                if (!Pōhēhē) 힙[읽는자리] = kāwai_CODE == 20 ? (byte)tāurunga_Pūranga_kōrero : kāwai_CODE == 21 ? tāurunga_Pūranga_kōrero & 1 : kāwai_CODE == 22 ? (char)tāurunga_Pūranga_kōrero : kāwai_CODE == 23 ? (short)tāurunga_Pūranga_kōrero : tāurunga_Pūranga_kōrero;
                continue;
            }
            if (uara >= 87 && uara <= 95) { Huinga_tohutohu(uara); continue; }
            if (uara == 96 || uara == 100 || uara == 104 || uara == 108 || uara == 112 || uara == 120
                || uara == 122 || uara == 124 || uara == 126 || uara == 128 || uara == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), mēhua = 0;
                if ((uara == 108 || uara == 112) && 나 == 0) { rahunga_uara("ArithmeticException: / by zero"); continue; }
                if (uara == 96) mēhua = 가 + 나;
                if (uara == 100) mēhua = 가 - 나;
                if (uara == 104) mēhua = 가 * 나;
                if (uara == 108) mēhua = 가 / 나;
                if (uara == 112) mēhua = 가 % 나;
                if (uara == 120) mēhua = 가 << 나;
                if (uara == 122) mēhua = 가 >> 나;
                if (uara == 124) mēhua = 가 >>> 나;
                if (uara == 126) mēhua = 가 & 나;
                if (uara == 128) mēhua = 가 | 나;
                if (uara == 130) mēhua = 가 ^ 나;
                넣기(mēhua, 1); continue;
            }
            if (uara == 116) { 넣기(-빼기(1), 1); continue; }
            if (uara == 132) {
                int paetata_whānuitanga = 명바(), 증분 = (byte)명바(); 지역읽기(paetata_whānuitanga, 1); 넣기(빼기(1) + 증분, 1); tuhi_paetata(paetata_whānuitanga, 1); continue;
            }
            if (uara >= 145 && uara <= 147) {
                int 수 = 빼기(1); 넣기(uara == 145 ? (byte)수 : uara == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (uara >= 153 && uara <= 167 || uara == 198 || uara == 199) {
                int ūnga_uara = whakahaere + (short)명짧(); boolean 갈까 = uara == 167;
                if (uara >= 153 && uara <= 158) {
                    int 수 = 빼기(1); 갈까 = uara == 153 ? 수 == 0 : uara == 154 ? 수 != 0 : uara == 155 ? 수 < 0 : uara == 156 ? 수 >= 0 : uara == 157 ? 수 > 0 : 수 <= 0;
                } else if (uara >= 159 && uara <= 166) {
                    int 나 = 빼기(uara >= 165 ? 2 : 1), 가 = 빼기(uara >= 165 ? 2 : 1);
                    갈까 = uara == 159 || uara == 165 ? 가 == 나 : uara == 160 || uara == 166 ? 가 != 나 : uara == 161 ? 가 < 나 : uara == 162 ? 가 >= 나 : uara == 163 ? 가 > 나 : 가 <= 나;
                } else if (uara == 198 || uara == 199) { int 수 = 빼기(2); 갈까 = uara == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) nuku_uara(ūnga_uara); continue;
            }
            if (uara == 172 || uara == 176 || uara == 177) { 반환(uara == 172 ? 1 : uara == 176 ? 2 : 0); continue; }
            if (uara >= 178 && uara <= 181) { 필드호출(명상수(), uara, whakahaere); continue; }
            if (uara >= 182 && uara <= 185) {
                int 부호값 = 명상수();
                if (uara == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { rahunga_uara("invalid invokeinterface operands"); continue; } }
                CALL_aratuka(부호값, uara); continue;
            }
            if (uara == 187) { 새객체(tauaha_ingoa_TEXT(명상수()), whakahaere); continue; }
            if (uara == 188 || uara == 189) {
                int kāwai_CODE = 3, wae = 0;
                if (uara == 188) { int 임시값 = 명바(); kāwai_CODE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else wae = tauaha_ingoa_TEXT(명상수());
                if (kāwai_CODE == 0) { rahunga_uara("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), ahanoa_Pūranga_kōrero = tiritiri_Rokiroki(kāwai_CODE, 유효길이); if (!Pōhēhē) HUĀNGA_huānga[ahanoa_Pūranga_kōrero] = wae; 넣기(ahanoa_Pūranga_kōrero, 2); continue;
            }
            if (uara == 190) {
                int ahanoa_Pūranga_kōrero = 빼기(2);
                if (객체유효(ahanoa_Pūranga_kōrero)) { int 비교자리 = 힙[ahanoa_Pūranga_kōrero]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) rahunga_uara("not an array"); else 넣기(힙[ahanoa_Pūranga_kōrero + 1], 1); }
                continue;
            }
            if (uara == 191) {
                int ahanoa_Pūranga_kōrero = 빼기(2); if (객체유효(ahanoa_Pūranga_kōrero)) { if (힙[ahanoa_Pūranga_kōrero] != 9) rahunga_uara("athrow requires supported Throwable"); else { 던진객체 = ahanoa_Pūranga_kōrero; Pōhēhē = true; } }
                continue;
            }
            if (uara == 192 || uara == 193) {
                int ingoa_taimau = tauaha_ingoa_TEXT(명상수()), ahanoa_Pūranga_kōrero = 빼기(2); boolean MATCH = 맞는객체(ahanoa_Pūranga_kōrero, ingoa_taimau);
                if (uara == 193) 넣기(ahanoa_Pūranga_kōrero != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !Pōhēhē) rahunga_uara("ClassCastException"); 넣기(ahanoa_Pūranga_kōrero, 2); }
                continue;
            }
            if (uara == 170 || uara == 171) {
                int 읽는자리 = whakahaere + 1, kōnae_INDEX = tāpare_aratuka[tāpare_INDEX], kī_Pūranga_kōrero = 빼기(1);
                while ((읽는자리 - aratuka_Start[kōnae_INDEX]) % 4 != 0) 읽는자리++;
                int ūnga_ADDRESS = tūranga_tau_tōpū(읽는자리);
                if (uara == 170) { int 낮은값 = tūranga_tau_tōpū(읽는자리 + 4), 높은값 = tūranga_tau_tōpū(읽는자리 + 8); if (kī_Pūranga_kōrero >= 낮은값 && kī_Pūranga_kōrero <= 높은값) ūnga_ADDRESS = tūranga_tau_tōpū(읽는자리 + 12 + (kī_Pūranga_kōrero - 낮은값) * 4); }
                else { int 총수 = tūranga_tau_tōpū(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (tūranga_tau_tōpū(읽는자리 + 8 + Loop_INDEX * 8) == kī_Pūranga_kōrero) ūnga_ADDRESS = tūranga_tau_tōpū(읽는자리 + 12 + Loop_INDEX * 8); }
                nuku_uara(whakahaere + ūnga_ADDRESS); continue;
            }
            if (uara == 200) { nuku_uara(whakahaere + tūranga_tau_tōpū(whakahaere + 1)); continue; }
            if (uara == 194 || uara == 195) {
                int ahanoa_Pūranga_kōrero = 빼기(2);
                if (uara == 195) 잠금풀기(ahanoa_Pūranga_kōrero);
                else if (!잠금얻기(ahanoa_Pūranga_kōrero) && !Pōhēhē) { 넣기(ahanoa_Pūranga_kōrero, 2); tāpare_tūranga[tāpare_INDEX] = whakahaere; }
                continue;
            }
            if (uara == 196) {
                int tono_CODE = 명바(), tāurunga_tūranga = 명짧();
                if (tono_CODE == 21 || tono_CODE == 25) 지역읽기(tāurunga_tūranga, tono_CODE == 21 ? 1 : 2);
                else if (tono_CODE == 54 || tono_CODE == 58) tuhi_paetata(tāurunga_tūranga, tono_CODE == 54 ? 1 : 2);
                else if (tono_CODE == 132) { int DELTA_uara = (short)명짧(); 지역읽기(tāurunga_tūranga, 1); 넣기(빼기(1) + DELTA_uara, 1); tuhi_paetata(tāurunga_tūranga, 1); }
                else rahunga_uara("unsupported wide opcode");
                continue;
            }
            rahunga_uara("unsupported bytecode");
        }
    }
    static int FIND_tauaha_Whakamāramatanga(int Ingoa) {
        for (int Loop_INDEX = 0; Loop_INDEX < tauaha_Whakamāramatanga_COUNT; Loop_INDEX++) if (tauaha_Whakamāramatanga_ingoa[Loop_INDEX] != 0 && 같은말(tauaha_Whakamāramatanga_ingoa[Loop_INDEX], Ingoa)) return Loop_INDEX;
        return uta_tauaha_Whakamāramatanga(taimau_TEXT(Ingoa));
    }
    static int uta_tauaha_Whakamāramatanga(int ingoa_aho) {
        if (!ahanoa_uara(ingoa_aho, 1)) return -1;
        int roa_uara = 힙[ingoa_aho + 1];
        if (roa_uara < 1 || roa_uara > 505 || tauaha_Whakamāramatanga_COUNT == 16) { rahunga_uara("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < roa_uara; Loop_INDEX++) { int waehere_pūāhua = 힙[ingoa_aho + 2 + Loop_INDEX]; kōnae_ingoa_TEXT[Loop_INDEX] = waehere_pūāhua == '/' ? '.' : waehere_pūāhua; }
        kōnae_ingoa_TEXT[roa_uara] = '.'; kōnae_ingoa_TEXT[roa_uara + 1] = 'c'; kōnae_ingoa_TEXT[roa_uara + 2] = 'l'; kōnae_ingoa_TEXT[roa_uara + 3] = 'a'; kōnae_ingoa_TEXT[roa_uara + 4] = 's'; kōnae_ingoa_TEXT[roa_uara + 5] = 's'; kōnae_ingoa_TEXT[roa_uara + 6] = 0;
        int rahi = kaiwhakamahi.파일읽기(kōnae_ingoa_TEXT, 임시파일);
        if (rahi < 0) { rahunga_uara("ClassNotFoundException"); return -1; }
        int tauaha_Whakamāramatanga = tauaha_Whakamāramatanga_COUNT++; tauaha_Whakamāramatanga_rahi[tauaha_Whakamāramatanga] = rahi;
        for (int Loop_INDEX = 0; Loop_INDEX < rahi; Loop_INDEX++) Kōnae[tauaha_Whakamāramatanga * 16384 + Loop_INDEX] = 임시파일[Loop_INDEX];
        클래스읽기(tauaha_Whakamāramatanga); if (Pōhēhē) return -1;
        int tūturu_raraunga = taimau_TEXT(tauaha_Whakamāramatanga_ingoa[tauaha_Whakamāramatanga]);
        if (!글같음(tūturu_raraunga, ingoa_aho, true)) { rahunga_uara("class name does not match file"); return -1; }
        int 부모 = 종부모[tauaha_Whakamāramatanga];
        if (부모 != 0 && !Word_TEXT(부모, "java/lang/Object") && !Word_TEXT(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_tauaha_Whakamāramatanga(부모);
            if (Pōhēhē || 위 < 0) return -1;
            int 읽는자리 = 위, atamira_COUNT = 0;
            while (읽는자리 >= 0 && atamira_COUNT++ < 16) {
                if (읽는자리 == tauaha_Whakamāramatanga) { rahunga_uara("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = tauaha_kāniwha_COUNT[위];
            for (int kōnae_INDEX = 0; kōnae_INDEX < kāniwha_COUNT; kōnae_INDEX++) if (kāniwha_kaipupuri[kōnae_INDEX] == tauaha_Whakamāramatanga && (kāniwha_whakaaetanga[kōnae_INDEX] & 8) == 0) kāniwha_tūranga[kōnae_INDEX] += 시작변위;
            tauaha_kāniwha_COUNT[tauaha_Whakamāramatanga] += 시작변위;
        }
        return tauaha_Whakamāramatanga;
    }
    static int 부모종(int tauaha_Whakamāramatanga) {
        int Ingoa = 종부모[tauaha_Whakamāramatanga];
        for (int Loop_INDEX = 0; Loop_INDEX < tauaha_Whakamāramatanga_COUNT; Loop_INDEX++) if (Ingoa != 0 && tauaha_Whakamāramatanga_ingoa[Loop_INDEX] != 0 && 같은말(tauaha_Whakamāramatanga_ingoa[Loop_INDEX], Ingoa)) return Loop_INDEX;
        return -1;
    }
    static int FIND_aratuka(int tauaha_Whakamāramatanga, int Ingoa, int hōputu_uara) {
        for (int 깊이 = 0; tauaha_Whakamāramatanga >= 0 && 깊이 < 16; 깊이++, tauaha_Whakamāramatanga = 부모종(tauaha_Whakamāramatanga)) {
            for (int Loop_INDEX = 0; Loop_INDEX < aratuka_COUNT; Loop_INDEX++) if (aratuka_kaipupuri[Loop_INDEX] == tauaha_Whakamāramatanga && 같은말(aratuka_ingoa_TEXT[Loop_INDEX], Ingoa) && 같은말(aratuka_TYPE[Loop_INDEX], hōputu_uara)) return Loop_INDEX;
        }
        return -1;
    }
    static int ingoa_aratuka(int tauaha_Whakamāramatanga, String Ingoa, String hōputu_uara) {
        for (int 깊이 = 0; tauaha_Whakamāramatanga >= 0 && 깊이 < 16; 깊이++, tauaha_Whakamāramatanga = 부모종(tauaha_Whakamāramatanga))
            for (int Loop_INDEX = 0; Loop_INDEX < aratuka_COUNT; Loop_INDEX++) if (aratuka_kaipupuri[Loop_INDEX] == tauaha_Whakamāramatanga && Word_TEXT(aratuka_ingoa_TEXT[Loop_INDEX], Ingoa) && Word_TEXT(aratuka_TYPE[Loop_INDEX], hōputu_uara)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int Ingoa) { return Kōnae[상가[Ingoa]] == 'L' || Kōnae[상가[Ingoa]] == '[' ? 2 : 1; }
    static boolean arawhiti(int tauaha_Whakamāramatanga, int tono_Start) {
        if (tauaha_Whakamāramatanga < 0 || Pōhēhē) return false;
        if (tauaha_Whakamāramatanga_tūnga[tauaha_Whakamāramatanga] == 3) { rahunga_uara("NoClassDefFoundError: initialization failed"); return false; }
        if (tauaha_Whakamāramatanga_tūnga[tauaha_Whakamāramatanga] == 1 && tauaha_miro[tauaha_Whakamāramatanga] != 현재가닥) { tāpare_tūranga[tāpare_INDEX] = tono_Start; 바꿈요청 = true; return false; }
        if (tauaha_Whakamāramatanga_tūnga[tauaha_Whakamāramatanga] != 0) return true;
        int 위 = 부모종(tauaha_Whakamāramatanga);
        if (위 >= 0 && !arawhiti(위, tono_Start)) return false;
        tauaha_Whakamāramatanga_tūnga[tauaha_Whakamāramatanga] = 1; tauaha_miro[tauaha_Whakamāramatanga] = 현재가닥;
        if (arawhiti_tauaha_Whakamāramatanga[tauaha_Whakamāramatanga] != 0) {
            tāpare_tūranga[tāpare_INDEX] = tono_Start;
            호출(arawhiti_tauaha_Whakamāramatanga[tauaha_Whakamāramatanga] - 1); if (!Pōhēhē) arawhiti_tāpare[tāpare_INDEX] = tauaha_Whakamāramatanga + 1;
            return false;
        }
        tauaha_Whakamāramatanga_tūnga[tauaha_Whakamāramatanga] = 2; return true;
    }
    static void 필드호출(int INDEX, int tono, int whakahaere) {
        if (!taki_taimau(INDEX, 9)) return;
        int kaipupuri_uara = tauaha_ingoa_TEXT(상가[INDEX]), Ingoa = Pūranga_kōrero_ingoa(taimau_SECOND_uara[INDEX]), hōputu_uara = Pūranga_kōrero_TYPE(taimau_SECOND_uara[INDEX]);
        if (Word_TEXT(kaipupuri_uara, "java/lang/System") && (Word_TEXT(Ingoa, "out") || Word_TEXT(Ingoa, "err")) && Word_TEXT(hōputu_uara, "Ljava/io/PrintStream;") && tono == 178) { 넣기(-1, 2); return; }
        int tauaha_Whakamāramatanga = FIND_tauaha_Whakamāramatanga(kaipupuri_uara); if (tauaha_Whakamāramatanga < 0 || Pōhēhē) return;
        int 찾음 = -1;
        for (int 읽는자리 = tauaha_Whakamāramatanga, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int kōnae_INDEX = 0; kōnae_INDEX < kāniwha_COUNT; kōnae_INDEX++) if (kāniwha_kaipupuri[kōnae_INDEX] == 읽는자리 && 같은말(kāniwha_ingoa[kōnae_INDEX], Ingoa) && 같은말(kāniwha_TYPE[kōnae_INDEX], hōputu_uara)) 찾음 = kōnae_INDEX;
        if (찾음 < 0) { rahunga_uara("NoSuchFieldError"); return; }
        boolean pateko_uara = tono == 178 || tono == 179;
        if (pateko_uara != ((kāniwha_whakaaetanga[찾음] & 8) != 0)) { rahunga_uara("field static/instance mismatch"); return; }
        if (pateko_uara && !arawhiti(kāniwha_kaipupuri[찾음], whakahaere)) return;
        int TYPE_uara = 형종류(hōputu_uara), uara = 0;
        if (tono == 179 || tono == 181) uara = 빼기(TYPE_uara);
        if (pateko_uara) { if (tono == 178) 넣기(kāniwha_raraunga[찾음], TYPE_uara); else if (!Pōhēhē) kāniwha_raraunga[찾음] = uara; return; }
        int ahanoa_Pūranga_kōrero = 빼기(2);
        if (!객체유효(ahanoa_Pūranga_kōrero)) return;
        if (힙[ahanoa_Pūranga_kōrero] < 32 || !종포함(힙[ahanoa_Pūranga_kōrero] - 32, kaipupuri_uara)) { rahunga_uara("field receiver type mismatch"); return; }
        int 보관칸 = ahanoa_Pūranga_kōrero + 2 + kāniwha_tūranga[찾음];
        if (tono == 180) 넣기(힙[보관칸], TYPE_uara);
        else if (!Pōhēhē) { 힙[보관칸] = uara; 힙참조[보관칸] = TYPE_uara == 2 ? 1 : 0; }
    }
    static boolean 종포함(int tauaha_Whakamāramatanga, int Ingoa) {
        for (int 중첩깊이 = 0; tauaha_Whakamāramatanga >= 0 && 중첩깊이 < 16; 중첩깊이++, tauaha_Whakamāramatanga = 부모종(tauaha_Whakamāramatanga)) {
            if (같은말(tauaha_Whakamāramatanga_ingoa[tauaha_Whakamāramatanga], Ingoa) || (종부모[tauaha_Whakamāramatanga] != 0 && 같은말(종부모[tauaha_Whakamāramatanga], Ingoa))) return true;
            for (int hono_roto_tūranga = 0; hono_roto_tūranga < tauaha_atanga_COUNT[tauaha_Whakamāramatanga]; hono_roto_tūranga++) if (같은말(tauaha_atanga[tauaha_Whakamāramatanga * 16 + hono_roto_tūranga], Ingoa)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int paita_raraunga, boolean ara) {
        if (첫값 == paita_raraunga) return true;
        if (첫값 <= 0 || paita_raraunga <= 0 || 힙[첫값] != 1 || 힙[paita_raraunga] != 1 || 힙[첫값 + 1] != 힙[paita_raraunga + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) {
            int taunga_x = 힙[첫값 + 2 + Loop_INDEX], 세로좌표 = 힙[paita_raraunga + 2 + Loop_INDEX];
            if (ara) { if (taunga_x == '.') taunga_x = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (taunga_x != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int ahanoa_Pūranga_kōrero) {
        if (ahanoa_Pūranga_kōrero == 0) { rahunga_uara("NullPointerException"); return false; }
        if (ahanoa_Pūranga_kōrero < 1 || ahanoa_Pūranga_kōrero >= 힙끝 || 힙폭[ahanoa_Pūranga_kōrero] < 2 || 힙[ahanoa_Pūranga_kōrero] == 0) { rahunga_uara("invalid object reference"); return false; }
        return true;
    }
    static void pare_uara(int ahanoa_Pūranga_kōrero) {
        if (ahanoa_Pūranga_kōrero > 0 && ahanoa_Pūranga_kōrero < 힙끝 && 힙폭[ahanoa_Pūranga_kōrero] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = ahanoa_Pūranga_kōrero;
    }
    static void whakaatu_uara(int ahanoa_Pūranga_kōrero) {
        if (ahanoa_Pūranga_kōrero > 0 && ahanoa_Pūranga_kōrero < 힙끝 && 힙폭[ahanoa_Pūranga_kōrero] >= 2 && 힙[ahanoa_Pūranga_kōrero] != 0 && 힙표시[ahanoa_Pūranga_kōrero] == 0) {
            힙표시[ahanoa_Pūranga_kōrero] = 1; 표시대기[whakaatu_COUNT++] = ahanoa_Pūranga_kōrero;
        }
    }
    static void 수거() {
        whakaatu_COUNT = 0; Kohinga_COUNT++;
        for (int taki_tūranga = 1; taki_tūranga < 힙끝; taki_tūranga += 힙폭[taki_tūranga]) 힙표시[taki_tūranga] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < aho_Pūranga_kōrero.length; Loop_INDEX++) whakaatu_uara(aho_Pūranga_kōrero[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < kāniwha_COUNT; Loop_INDEX++) if ((kāniwha_whakaaetanga[Loop_INDEX] & 8) != 0 && 형종류(kāniwha_TYPE[Loop_INDEX]) == 2) whakaatu_uara(kāniwha_raraunga[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < miro_COUNT; 임시값++) {
            whakaatu_uara(miro_ahanoa[임시값]); whakaatu_uara(miro_ūnga[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? tāpare_INDEX : miro_tāpare[임시값];
            for (int kōnae_INDEX = 임시값 * 32; kōnae_INDEX <= 꼭대기자리; kōnae_INDEX++) {
                for (int hono_roto_tūranga = 0; hono_roto_tūranga < 함수지역[tāpare_aratuka[kōnae_INDEX]]; hono_roto_tūranga++) if (paetata_TYPE[kōnae_INDEX * 128 + hono_roto_tūranga] == 2) whakaatu_uara(paetata_uara[kōnae_INDEX * 128 + hono_roto_tūranga]);
                for (int hono_roto_tūranga = 0; hono_roto_tūranga < tāpare_Huinga[kōnae_INDEX]; hono_roto_tūranga++) if (스택형[kōnae_INDEX * 128 + hono_roto_tūranga] == 2) whakaatu_uara(스택값[kōnae_INDEX * 128 + hono_roto_tūranga]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) whakaatu_uara(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) whakaatu_uara(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_tau_tōpū.length; Loop_INDEX++) whakaatu_uara(Store_tau_tōpū[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < tauaha_Whakamāramatanga_COUNT; Loop_INDEX++) whakaatu_uara(종잠금[Loop_INDEX]);
        for (int taki_tūranga = 1; taki_tūranga < 힙끝; taki_tūranga += 힙폭[taki_tūranga]) if (잠금깊이[taki_tūranga] > 0) whakaatu_uara(taki_tūranga);
        whakaatu_uara(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) whakaatu_uara(잠시참조[Loop_INDEX]);
        while (whakaatu_COUNT > 0) {
            int ahanoa_Pūranga_kōrero = 표시대기[--whakaatu_COUNT], kāwai_CODE = 힙[ahanoa_Pūranga_kōrero];
            for (int Loop_INDEX = ahanoa_Pūranga_kōrero + 2; Loop_INDEX < ahanoa_Pūranga_kōrero + 힙폭[ahanoa_Pūranga_kōrero]; Loop_INDEX++) if (kāwai_CODE == 3 || kāwai_CODE == 4 || 힙참조[Loop_INDEX] != 0) whakaatu_uara(힙[Loop_INDEX]);
        }
        for (int taki_tūranga = 1; taki_tūranga < 힙끝; taki_tūranga += 힙폭[taki_tūranga]) if (힙표시[taki_tūranga] == 0) 힙[taki_tūranga] = 0;
        for (int taki_tūranga = 1; taki_tūranga < 힙끝; taki_tūranga += 힙폭[taki_tūranga]) if (힙[taki_tūranga] == 0) {
            while (taki_tūranga + 힙폭[taki_tūranga] < 힙끝 && 힙[taki_tūranga + 힙폭[taki_tūranga]] == 0) { int Panuku_tūranga = taki_tūranga + 힙폭[taki_tūranga]; 힙폭[taki_tūranga] += 힙폭[Panuku_tūranga]; 힙폭[Panuku_tūranga] = 0; }
            if (taki_tūranga + 힙폭[taki_tūranga] == 힙끝) { 힙끝 = taki_tūranga; break; }
        }
    }
    static int 새기억(int 종류, int roa_uara) {
        if (roa_uara < 0) { rahunga_uara("NegativeArraySizeException"); return 0; }
        if (roa_uara > 힙.length - 3) { rahunga_uara("object heap exhausted"); return 0; }
        int 필요수 = roa_uara + 2, ahanoa_Pūranga_kōrero = 0;
        if (필요수 <= 힙.length - 힙끝) { ahanoa_Pūranga_kōrero = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { ahanoa_Pūranga_kōrero = 읽는자리; break; }
            if (ahanoa_Pūranga_kōrero != 0) {
                int 남은길이 = 힙폭[ahanoa_Pūranga_kōrero] - 필요수;
                if (남은길이 >= 2) { 힙폭[ahanoa_Pūranga_kōrero + 필요수] = 남은길이; 힙[ahanoa_Pūranga_kōrero + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { ahanoa_Pūranga_kōrero = 힙끝; 힙끝 += 필요수; }
        }
        if (ahanoa_Pūranga_kōrero == 0) { rahunga_uara("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { 힙[ahanoa_Pūranga_kōrero + Loop_INDEX] = 0; 힙참조[ahanoa_Pūranga_kōrero + Loop_INDEX] = 0; 힙폭[ahanoa_Pūranga_kōrero + Loop_INDEX] = 0; }
        HUĀNGA_huānga[ahanoa_Pūranga_kōrero] = 0;
        힙폭[ahanoa_Pūranga_kōrero] = 필요수; 힙[ahanoa_Pūranga_kōrero] = 종류; 힙[ahanoa_Pūranga_kōrero + 1] = roa_uara; pare_uara(ahanoa_Pūranga_kōrero); return ahanoa_Pūranga_kōrero;
    }
    static int 예외종(String ingoa_taimau) {
        if (자바도구.같음(ingoa_taimau, "java/lang/Throwable")) return 1;
        if (자바도구.같음(ingoa_taimau, "java/lang/Exception")) return 2;
        if (자바도구.같음(ingoa_taimau, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(ingoa_taimau, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(ingoa_taimau, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(ingoa_taimau, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(ingoa_taimau, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(ingoa_taimau, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(ingoa_taimau, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(ingoa_taimau, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(ingoa_taimau, "java/io/IOException")) return 11;
        if (자바도구.같음(ingoa_taimau, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(ingoa_taimau, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(ingoa_taimau, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(ingoa_taimau, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int 예외상수(int Ingoa) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_TEXT(Ingoa, 예외이름(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String 예외이름(int pūkete_uara) {
        if (pūkete_uara == 40) return "java/lang/InterruptedException";
        if (pūkete_uara == 41) return "Reo_Māori/자체/대기중단예외";
        if (pūkete_uara == 39) return "java/net/SocketException";
        if (pūkete_uara == 20) return "Reo_Māori/자체/예외";
        if (pūkete_uara == 21) return "Reo_Māori/자체/실행예외";
        if (pūkete_uara == 22) return "Reo_Māori/자체/입출력예외";
        if (pūkete_uara == 23) return "Reo_Māori/자체/대기시간초과예외";
        if (pūkete_uara == 24) return "Reo_Māori/자체/주소확인예외";
        if (pūkete_uara == 25) return "Reo_Māori/자체/파일없음예외";
        if (pūkete_uara == 26) return "Reo_Māori/자체/통신예외";
        if (pūkete_uara == 27) return "Reo_Māori/자체/잘못된인수예외";
        if (pūkete_uara == 28) return "Reo_Māori/자체/숫자형식예외";
        if (pūkete_uara == 29) return "Reo_Māori/자체/범위예외";
        if (pūkete_uara == 30) return "Reo_Māori/자체/배열범위예외";
        if (pūkete_uara == 31) return "Reo_Māori/자체/문자열범위예외";
        if (pūkete_uara == 32) return "Reo_Māori/자체/빈참조예외";
        if (pūkete_uara == 33) return "Reo_Māori/자체/산술예외";
        if (pūkete_uara == 34) return "Reo_Māori/자체/상태예외";
        if (pūkete_uara == 35) return "Reo_Māori/자체/형변환예외";
        if (pūkete_uara == 36) return "Reo_Māori/자체/음수배열크기예외";
        if (pūkete_uara == 37) return "Reo_Māori/자체/HUĀNGA_Store_rahunga";
        if (pūkete_uara == 38) return "Reo_Māori/자체/가닥상태예외";
        if (pūkete_uara == 1) return "java/lang/Throwable"; if (pūkete_uara == 2) return "java/lang/Exception";
        if (pūkete_uara == 3) return "java/lang/RuntimeException"; if (pūkete_uara == 4) return "java/lang/ArithmeticException";
        if (pūkete_uara == 5) return "java/lang/NullPointerException"; if (pūkete_uara == 6) return "java/lang/IndexOutOfBoundsException";
        if (pūkete_uara == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (pūkete_uara == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (pūkete_uara == 9) return "java/lang/IllegalArgumentException"; if (pūkete_uara == 10) return "java/lang/NumberFormatException";
        if (pūkete_uara == 11) return "java/io/IOException"; if (pūkete_uara == 12) return "java/io/FileNotFoundException";
        if (pūkete_uara == 17) return "java/lang/ArrayStoreException";
        if (pūkete_uara == 18) return "java/net/UnknownHostException";
        if (pūkete_uara == 19) return "java/net/SocketTimeoutException";
        if (pūkete_uara == 16) return "java/lang/IllegalThreadStateException";
        if (pūkete_uara == 13) return "java/lang/IllegalStateException"; if (pūkete_uara == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int pūkete_uara) {
        if (pūkete_uara == 40) return 2;
        if (pūkete_uara == 41) return 40;
        if (pūkete_uara == 39) return 11;
        if (pūkete_uara == 1) return 0;
        if (pūkete_uara == 2) return 1;
        if (pūkete_uara == 3) return 2;
        if (pūkete_uara == 4) return 3;
        if (pūkete_uara == 5) return 3;
        if (pūkete_uara == 6) return 3;
        if (pūkete_uara == 7) return 6;
        if (pūkete_uara == 8) return 6;
        if (pūkete_uara == 9) return 3;
        if (pūkete_uara == 10) return 9;
        if (pūkete_uara == 11) return 2;
        if (pūkete_uara == 12) return 11;
        if (pūkete_uara == 13) return 3;
        if (pūkete_uara == 14) return 3;
        if (pūkete_uara == 15) return 3;
        if (pūkete_uara == 16) return 9;
        if (pūkete_uara == 17) return 3;
        if (pūkete_uara == 18) return 11;
        if (pūkete_uara == 19) return 11;
        if (pūkete_uara == 20) return 2;
        if (pūkete_uara == 21) return 3;
        if (pūkete_uara == 22) return 11;
        if (pūkete_uara == 23) return 22;
        if (pūkete_uara == 24) return 22;
        if (pūkete_uara == 25) return 22;
        if (pūkete_uara == 26) return 22;
        if (pūkete_uara == 27) return 9;
        if (pūkete_uara == 28) return 27;
        if (pūkete_uara == 29) return 6;
        if (pūkete_uara == 30) return 29;
        if (pūkete_uara == 31) return 29;
        if (pūkete_uara == 32) return 5;
        if (pūkete_uara == 33) return 4;
        if (pūkete_uara == 34) return 13;
        if (pūkete_uara == 35) return 14;
        if (pūkete_uara == 36) return 15;
        if (pūkete_uara == 37) return 17;
        if (pūkete_uara == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int tūturu_uara, int 요구값) {
        for (int 깊이 = 0; tūturu_uara != 0 && 깊이 < 16; 깊이++, tūturu_uara = 예외부모(tūturu_uara))
            if (tūturu_uara == 요구값) return true;
        return false;
    }
    static void 예외던짐(int pūkete_uara, String PĀNUIMAI_Pūranga_kōrero) {
        int ahanoa_Pūranga_kōrero = 새기억(9, 2); if (Pōhēhē) return;
        힙[ahanoa_Pūranga_kōrero + 2] = pūkete_uara; 힙[ahanoa_Pūranga_kōrero + 3] = taurima_pūāhua(PĀNUIMAI_Pūranga_kōrero); 힙참조[ahanoa_Pūranga_kōrero + 3] = 1;
        던진객체 = ahanoa_Pūranga_kōrero; Pōhēhē = true;
    }
    static boolean 맞는객체(int ahanoa_Pūranga_kōrero, int Ingoa) {
        if (ahanoa_Pūranga_kōrero == 0) return true;
        if (!객체유효(ahanoa_Pūranga_kōrero)) return false;
        int kāwai_CODE = 힙[ahanoa_Pūranga_kōrero];
        if (Word_TEXT(Ingoa, "java/lang/Object")) return true;
        if (kāwai_CODE >= 32) return 종포함(kāwai_CODE - 32, Ingoa);
        if (kāwai_CODE == 9) { int ūnga_ADDRESS = 예외상수(Ingoa); return ūnga_ADDRESS != 0 && 예외포함(힙[ahanoa_Pūranga_kōrero + 2], ūnga_ADDRESS); }
        if (kāwai_CODE == 1) return Word_TEXT(Ingoa, "java/lang/String") || Word_TEXT(Ingoa, "java/lang/CharSequence");
        if (kāwai_CODE == 4) return Word_TEXT(Ingoa, "java/lang/StringBuilder") || Word_TEXT(Ingoa, "java/lang/CharSequence");
        if (kāwai_CODE == 10) return Word_TEXT(Ingoa, "java/util/ArrayList") || Word_TEXT(Ingoa, "java/util/List");
        if (kāwai_CODE == 11) return Word_TEXT(Ingoa, "java/util/HashMap") || Word_TEXT(Ingoa, "java/util/Map");
        if (kāwai_CODE == 12) return Word_TEXT(Ingoa, "java/lang/Integer") || Word_TEXT(Ingoa, "java/lang/Number");
        if (kāwai_CODE >= 24 && kāwai_CODE <= 28 && 힙[ahanoa_Pūranga_kōrero + 13] != 0) return 한국어화면종(Ingoa) == kāwai_CODE || Word_TEXT(Ingoa, "Reo_Māori/자체/화면구성요소");
        if (kāwai_CODE >= 24 && kāwai_CODE <= 28) return (한국어화면종(Ingoa) == 0 && 화면종(Ingoa) == kāwai_CODE) || Word_TEXT(Ingoa, "java/awt/Component") || Word_TEXT(Ingoa, "java/awt/Container") || Word_TEXT(Ingoa, "javax/swing/JComponent");
        if (kāwai_CODE == 29) return Word_TEXT(Ingoa, 힙[ahanoa_Pūranga_kōrero + 3] != 0 ? "Reo_Māori/자체/동작알림" : "java/awt/event/ActionEvent");
        if (kāwai_CODE == 30) return Word_TEXT(Ingoa, "java/awt/FlowLayout") || Word_TEXT(Ingoa, "java/awt/LayoutManager");
        if (kāwai_CODE == 17) return Word_TEXT(Ingoa, "java/net/Socket");
        if (kāwai_CODE == 18) return Word_TEXT(Ingoa, "java/net/ServerSocket");
        if (kāwai_CODE == 19) return Word_TEXT(Ingoa, 힙[ahanoa_Pūranga_kōrero + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (kāwai_CODE == 14) return Word_TEXT(Ingoa, "java/net/InetAddress");
        if (kāwai_CODE == 15) return Word_TEXT(Ingoa, "java/net/DatagramSocket");
        if (kāwai_CODE == 16) return Word_TEXT(Ingoa, "java/net/DatagramPacket");
        if (kāwai_CODE == 13) return Word_TEXT(Ingoa, 힙[ahanoa_Pūranga_kōrero + 3] != 0 ? "Reo_Māori/자체/작업가닥" : "java/lang/Thread");
        if (kāwai_CODE == 2) return Word_TEXT(Ingoa, "[I"); if (kāwai_CODE == 20) return Word_TEXT(Ingoa, "[B"); if (kāwai_CODE == 21) return Word_TEXT(Ingoa, "[Z");
        if (kāwai_CODE == 22) return Word_TEXT(Ingoa, "[C"); if (kāwai_CODE == 23) return Word_TEXT(Ingoa, "[S");
        if (kāwai_CODE != 3) return false;
        if (Word_TEXT(Ingoa, "[Ljava/lang/Object;")) return true;
        int wae = HUĀNGA_huānga[ahanoa_Pūranga_kōrero];
        if (wae == -1) return Word_TEXT(Ingoa, "[Ljava/lang/String;") || Word_TEXT(Ingoa, "[Ljava/lang/CharSequence;");
        if (wae == 0) return false;
        if (배열종비교(wae, Ingoa)) return true;
        if ((Word_TEXT(wae, "java/lang/String") || Word_TEXT(wae, "java/lang/StringBuilder")) && Word_TEXT(Ingoa, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < tauaha_Whakamāramatanga_COUNT; Loop_INDEX++) if (같은말(tauaha_Whakamāramatanga_ingoa[Loop_INDEX], wae)) {
            for (int waehere_pūāhua = Loop_INDEX, 중첩깊이 = 0; waehere_pūāhua >= 0 && 중첩깊이 < 16; 중첩깊이++, waehere_pūāhua = 부모종(waehere_pūāhua)) {
                if (배열종비교(종부모[waehere_pūāhua], Ingoa)) return true;
                for (int hono_roto_tūranga = 0; hono_roto_tūranga < tauaha_atanga_COUNT[waehere_pūāhua]; hono_roto_tūranga++) if (배열종비교(tauaha_atanga[waehere_pūāhua * 16 + hono_roto_tūranga], Ingoa)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int ingoa_taimau, int 형식참조) {
        int taki_tūranga = 상가[형식참조], tāurunga_COUNT = taimau_SECOND_uara[형식참조];
        if (ingoa_taimau == 0 || tāurunga_COUNT < 4 || Kōnae[taki_tūranga] != '[' || Kōnae[taki_tūranga + 1] != 'L' || Kōnae[taki_tūranga + tāurunga_COUNT - 1] != ';' || taimau_SECOND_uara[ingoa_taimau] != tāurunga_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < tāurunga_COUNT - 3; Loop_INDEX++) if (Kōnae[상가[ingoa_taimau] + Loop_INDEX] != Kōnae[taki_tūranga + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void 예외처리() {
        if (던진객체 == 0) return;
        Pōhēhē = false;
        while (tāpare_INDEX >= 현재가닥 * 32) {
            int kōnae_INDEX = tāpare_aratuka[tāpare_INDEX], 읽는자리 = tāpare_tohutohu[tāpare_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == kōnae_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                tāpare_tūranga[tāpare_INDEX] = 잡기위치[Loop_INDEX]; tāpare_Huinga[tāpare_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (arawhiti_tāpare[tāpare_INDEX] != 0) tauaha_Whakamāramatanga_tūnga[arawhiti_tāpare[tāpare_INDEX] - 1] = 3;
            if (틀잠금[tāpare_INDEX] != 0) { 잠금풀기(틀잠금[tāpare_INDEX]); 틀잠금[tāpare_INDEX] = 0; }
            tāpare_INDEX--;
        }
        kaiwhakamahi.Tuhia("Uncaught ");
        if (힙[던진객체] == 9) { kaiwhakamahi.Tuhia(예외이름(힙[던진객체 + 2])); kaiwhakamahi.Tuhia(": "); tuhi_TEXT(힙[던진객체 + 3]); }
        else kaiwhakamahi.Tuhia("user exception");
        kaiwhakamahi.tuhi_pūāhua_uara(10); 던진객체 = 0; Pōhēhē = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void Huinga_tohutohu(int tono_CODE) {
        int 첫값 = 빼기(0), 첫형식 = 반환형;
        if (tono_CODE == 87) return;
        if (tono_CODE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int paita_raraunga = 빼기(0), SECOND_hōputu = 반환형;
        if (tono_CODE == 88) return;
        if (tono_CODE == 90) { 넣기(첫값, 첫형식); 넣기(paita_raraunga, SECOND_hōputu); 넣기(첫값, 첫형식); return; }
        if (tono_CODE == 92) { 넣기(paita_raraunga, SECOND_hōputu); 넣기(첫값, 첫형식); 넣기(paita_raraunga, SECOND_hōputu); 넣기(첫값, 첫형식); return; }
        if (tono_CODE == 95) { 넣기(첫값, 첫형식); 넣기(paita_raraunga, SECOND_hōputu); return; }
        int waehere_pūāhua = 빼기(0), 셋째형식 = 반환형;
        if (tono_CODE == 91) { 넣기(첫값, 첫형식); 넣기(waehere_pūāhua, 셋째형식); 넣기(paita_raraunga, SECOND_hōputu); 넣기(첫값, 첫형식); return; }
        if (tono_CODE == 93) { 넣기(paita_raraunga, SECOND_hōputu); 넣기(첫값, 첫형식); 넣기(waehere_pūāhua, 셋째형식); 넣기(paita_raraunga, SECOND_hōputu); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = 반환형;
        넣기(paita_raraunga, SECOND_hōputu); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(waehere_pūāhua, 셋째형식); 넣기(paita_raraunga, SECOND_hōputu); 넣기(첫값, 첫형식);
    }
    static void 새객체(int ingoa_taimau, int 시작점) {
        int kāwai_CODE = 0, 유효길이 = 0, 예외참조 = 예외상수(ingoa_taimau);
        if (Word_TEXT(ingoa_taimau, "java/lang/StringBuilder")) { kāwai_CODE = 4; 유효길이 = 1; }
        if (Word_TEXT(ingoa_taimau, "java/io/FileInputStream")) { kāwai_CODE = 5; 유효길이 = 2; }
        if (Word_TEXT(ingoa_taimau, "java/io/FileOutputStream")) { kāwai_CODE = 6; 유효길이 = 2; }
        if (예외참조 != 0) { kāwai_CODE = 9; 유효길이 = 2; }
        if (Word_TEXT(ingoa_taimau, "java/util/ArrayList")) { kāwai_CODE = 10; 유효길이 = 2; }
        if (Word_TEXT(ingoa_taimau, "java/util/HashMap")) { kāwai_CODE = 11; 유효길이 = 2; }
        if (Word_TEXT(ingoa_taimau, "java/lang/Integer")) { kāwai_CODE = 12; 유효길이 = 1; }
        if (Word_TEXT(ingoa_taimau, "java/net/Socket")) { kāwai_CODE = 17; 유효길이 = 5; }
        if (Word_TEXT(ingoa_taimau, "java/net/ServerSocket")) { kāwai_CODE = 18; 유효길이 = 5; }
        if (Word_TEXT(ingoa_taimau, "java/net/DatagramSocket")) { kāwai_CODE = 15; 유효길이 = 3; }
        if (Word_TEXT(ingoa_taimau, "java/net/DatagramPacket")) { kāwai_CODE = 16; 유효길이 = 4; }
        if (Word_TEXT(ingoa_taimau, "java/lang/Thread") || Word_TEXT(ingoa_taimau, "Reo_Māori/자체/작업가닥")) { kāwai_CODE = 13; 유효길이 = 2; }
        if (Word_TEXT(ingoa_taimau, "java/lang/Object")) { kāwai_CODE = 8; }
        if (kāwai_CODE == 0 && 화면종(ingoa_taimau) != 0) { kāwai_CODE = 화면종(ingoa_taimau); 유효길이 = 12; }
        if (kāwai_CODE == 0) {
            int waehere_pūāhua = FIND_tauaha_Whakamāramatanga(ingoa_taimau); if (waehere_pūāhua < 0 || Pōhēhē || !arawhiti(waehere_pūāhua, 시작점)) return;
            kāwai_CODE = 32 + waehere_pūāhua; 유효길이 = tauaha_kāniwha_COUNT[waehere_pūāhua];
        }
        int ahanoa_Pūranga_kōrero = tiritiri_Rokiroki(kāwai_CODE, 유효길이); if (Pōhēhē) return;
        if (kāwai_CODE == 13 && Word_TEXT(ingoa_taimau, "Reo_Māori/자체/작업가닥")) 힙[ahanoa_Pūranga_kōrero + 3] = 1;
        if (kāwai_CODE >= 24 && kāwai_CODE <= 28 && 한국어화면종(ingoa_taimau) != 0) 힙[ahanoa_Pūranga_kōrero + 13] = 1;
        if (kāwai_CODE == 5 || kāwai_CODE == 6 || kāwai_CODE == 15 || kāwai_CODE == 17 || kāwai_CODE == 18) 힙[ahanoa_Pūranga_kōrero + 2] = -1;
        if (kāwai_CODE == 9) 힙[ahanoa_Pūranga_kōrero + 2] = 예외참조;
        넣기(ahanoa_Pūranga_kōrero, 2);
    }
    static boolean 값같음(int 첫값, int paita_raraunga) {
        if (첫값 == paita_raraunga) return true;
        if (첫값 == 0 || paita_raraunga == 0 || 첫값 < 0 || paita_raraunga < 0 || 첫값 >= 힙끝 || paita_raraunga >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[paita_raraunga] == 1) return 글같음(첫값, paita_raraunga, false);
        return 힙[첫값] == 12 && 힙[paita_raraunga] == 12 && 힙[첫값 + 2] == 힙[paita_raraunga + 2];
    }
    static int 글조각(int ahanoa_Pūranga_kōrero, int Start_tūranga, int mutu_tūranga) {
        if (!ahanoa_uara(ahanoa_Pūranga_kōrero, 1)) return 0;
        if (Start_tūranga < 0 || mutu_tūranga < Start_tūranga || mutu_tūranga > 힙[ahanoa_Pūranga_kōrero + 1]) { rahunga_uara("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = tiritiri_Rokiroki(1, mutu_tūranga - Start_tūranga); if (Pōhēhē) return 0;
        for (int Loop_INDEX = Start_tūranga; Loop_INDEX < mutu_tūranga; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX - Start_tūranga] = 힙[ahanoa_Pūranga_kōrero + 2 + Loop_INDEX];
        return 반환값;
    }
    static int hono_TEXT(int 첫값, int paita_raraunga) {
        if (!ahanoa_uara(첫값, 1) || !ahanoa_uara(paita_raraunga, 1)) return 0;
        int tāurunga_COUNT = 힙[첫값 + 1], aratuka_INDEX = 힙[paita_raraunga + 1], 반환값 = tiritiri_Rokiroki(1, tāurunga_COUNT + aratuka_INDEX); if (Pōhēhē) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < tāurunga_COUNT; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 힙[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < aratuka_INDEX; Loop_INDEX++) 힙[반환값 + 2 + tāurunga_COUNT + Loop_INDEX] = 힙[paita_raraunga + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int kaipupuri, int ingoa_taimau, int 서술상수, int tono_CODE) {
        if (Word_TEXT(kaipupuri, "Reo_Māori/자체/실행인수") && tono_CODE == 184) {
            if (Word_TEXT(ingoa_taimau, "tuemi_COUNT") && Word_TEXT(서술상수, "()I")) { 넣기(kaiwhakamahi.인수개수() - 1, 1); return true; }
            if (Word_TEXT(ingoa_taimau, "Ngā_kupu") && Word_TEXT(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= kaiwhakamahi.인수개수() - 1) 예외던짐(29, "kawe_tono 인수 범위를 벗어났습니다");
                else 넣기(taurima_pūāhua(kaiwhakamahi.인수(순번 + 1)), 2);
                return true;
            }
            rahunga_uara("지원하지 않는 Reo_Māori kawe_tono 인수 호출"); return true;
        }
        if (Word_TEXT(kaipupuri, "Reo_Māori/자체/작업가닥")) { Hātepe_miro(ingoa_taimau, 서술상수, tono_CODE, true); return true; }
        if (한국어화면소유(kaipupuri)) { 한국어화면호출(kaipupuri, ingoa_taimau, 서술상수, tono_CODE); return true; }
        if (화면소유(kaipupuri)) { 화면호출(kaipupuri, ingoa_taimau, 서술상수, tono_CODE); return true; }
        if (Word_TEXT(kaipupuri, "java/net/Socket") || Word_TEXT(kaipupuri, "java/net/ServerSocket") || Word_TEXT(kaipupuri, "java/io/InputStream") || Word_TEXT(kaipupuri, "java/io/OutputStream")) { 흐름호출(kaipupuri, ingoa_taimau, 서술상수, tono_CODE); return true; }
        if (Word_TEXT(kaipupuri, "Reo_Māori/자체/kākano_uara_0611a8a8") && tono_CODE == 184) {
            if (Word_TEXT(ingoa_taimau, "화면너비") && Word_TEXT(서술상수, "()I")) { 넣기(kaiwhakamahi.화면너비(), 1); return true; }
            if (Word_TEXT(ingoa_taimau, "화면높이") && Word_TEXT(서술상수, "()I")) { 넣기(kaiwhakamahi.화면높이(), 1); return true; }
            if (Word_TEXT(ingoa_taimau, "밀리초") && Word_TEXT(서술상수, "()I")) { 넣기(kaiwhakamahi.밀리초(), 1); return true; }
            if (Word_TEXT(ingoa_taimau, "그림대기") && Word_TEXT(서술상수, "()I")) { 넣기(kaiwhakamahi.그림대기(), 1); return true; }
            if (Word_TEXT(ingoa_taimau, "사각형") && Word_TEXT(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), taunga_x = 빼기(1); 넣기(kaiwhakamahi.사각형(taunga_x, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_TEXT(kaipupuri, "java/net/InetAddress") || Word_TEXT(kaipupuri, "java/net/DatagramPacket") || Word_TEXT(kaipupuri, "java/net/DatagramSocket")) { 통신호출(kaipupuri, ingoa_taimau, 서술상수, tono_CODE); return true; }
        if (Word_TEXT(kaipupuri, "java/lang/Thread")) { 가닥호출(ingoa_taimau, 서술상수, tono_CODE); return true; }
        if (Word_TEXT(kaipupuri, "java/lang/Object")) {
            if (Word_TEXT(ingoa_taimau, "<init>") && Word_TEXT(서술상수, "()V") && tono_CODE == 183) { 객체유효(빼기(2)); return true; }
            if (Word_TEXT(ingoa_taimau, "equals") && Word_TEXT(서술상수, "(Ljava/lang/Object;)Z")) { int paita_raraunga = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == paita_raraunga ? 1 : 0, 1); return true; }
        }
        if (예외상수(kaipupuri) != 0) {
            if (Word_TEXT(ingoa_taimau, "<init>") && tono_CODE == 183 && (Word_TEXT(서술상수, "()V") || Word_TEXT(서술상수, "(Ljava/lang/String;)V"))) {
                int tohuaki = Word_TEXT(서술상수, "()V") ? 0 : 빼기(2), ahanoa_Pūranga_kōrero = 빼기(2);
                if (ahanoa_uara(ahanoa_Pūranga_kōrero, 9)) { 힙[ahanoa_Pūranga_kōrero + 3] = tohuaki; 힙참조[ahanoa_Pūranga_kōrero + 3] = 1; } return true;
            }
            if ((Word_TEXT(ingoa_taimau, "getMessage") || Word_TEXT(ingoa_taimau, "설명")) && Word_TEXT(서술상수, "()Ljava/lang/String;")) { int ahanoa_Pūranga_kōrero = 빼기(2); if (ahanoa_uara(ahanoa_Pūranga_kōrero, 9)) 넣기(힙[ahanoa_Pūranga_kōrero + 3], 2); return true; }
        }
        if (Word_TEXT(kaipupuri, "java/lang/String")) {
            if (tono_CODE == 182 && Word_TEXT(ingoa_taimau, "getBytes") && (Word_TEXT(서술상수, "()[B") || Word_TEXT(서술상수, "(Ljava/lang/String;)[B"))) {
                int whakawaehere_ingoa = Word_TEXT(서술상수, "()[B") ? 0 : 빼기(2), ahanoa_Pūranga_kōrero = 빼기(2);
                if (!ahanoa_uara(ahanoa_Pūranga_kōrero, 1)) return true;
                if (whakawaehere_ingoa != 0 && !글같음(whakawaehere_ingoa, taurima_pūāhua("UTF-8"), false) && !글같음(whakawaehere_ingoa, taurima_pūāhua("UTF8"), false) && !글같음(whakawaehere_ingoa, taurima_pūāhua("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int tāurunga_COUNT = 힙[ahanoa_Pūranga_kōrero + 1], 반환값 = tiritiri_Rokiroki(20, tāurunga_COUNT * 3), 사용수 = 0; if (Pōhēhē) return true;
                for (int hono_roto_tūranga = 0; hono_roto_tūranga < tāurunga_COUNT; hono_roto_tūranga++) {
                    int waehere_pūāhua = 힙[ahanoa_Pūranga_kōrero + 2 + hono_roto_tūranga];
                    if (waehere_pūāhua >= 0xd800 && waehere_pūāhua <= 0xdbff && hono_roto_tūranga + 1 < tāurunga_COUNT && 힙[ahanoa_Pūranga_kōrero + 3 + hono_roto_tūranga] >= 0xdc00 && 힙[ahanoa_Pūranga_kōrero + 3 + hono_roto_tūranga] <= 0xdfff) waehere_pūāhua = 0x10000 + ((waehere_pūāhua - 0xd800) << 10) + 힙[ahanoa_Pūranga_kōrero + 2 + ++hono_roto_tūranga] - 0xdc00;
                    else if (waehere_pūāhua >= 0xd800 && waehere_pūāhua <= 0xdfff) waehere_pūāhua = '?';
                    if (waehere_pūāhua < 128) 힙[반환값 + 2 + 사용수++] = waehere_pūāhua;
                    else { int paita_COUNT = waehere_pūāhua < 2048 ? 2 : waehere_pūāhua < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((paita_COUNT == 2 ? 192 : paita_COUNT == 3 ? 224 : 240) | waehere_pūāhua >> (6 * (paita_COUNT - 1))); for (int 비교자리 = paita_COUNT - 1; 비교자리 > 0; 비교자리--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | waehere_pūāhua >> (6 * (비교자리 - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (tono_CODE == 184 && Word_TEXT(ingoa_taimau, "valueOf") && Word_TEXT(서술상수, "(I)Ljava/lang/String;")) { 넣기(mati_pūāhua(빼기(1)), 2); return true; }
            if (tono_CODE != 182) return false;
            if (Word_TEXT(ingoa_taimau, "equals") && Word_TEXT(서술상수, "(Ljava/lang/Object;)Z")) { int paita_raraunga = 빼기(2), 첫값 = 빼기(2); if (ahanoa_uara(첫값, 1)) 넣기(글같음(첫값, paita_raraunga, false) ? 1 : 0, 1); return true; }
            if (Word_TEXT(ingoa_taimau, "isEmpty") && Word_TEXT(서술상수, "()Z")) { int 첫값 = 빼기(2); if (ahanoa_uara(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_TEXT(ingoa_taimau, "substring") && (Word_TEXT(서술상수, "(I)Ljava/lang/String;") || Word_TEXT(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_uara = Word_TEXT(서술상수, "(II)Ljava/lang/String;"); int mutu_tūranga = SECOND_uara ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (ahanoa_uara(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_uara ? mutu_tūranga : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_TEXT(ingoa_taimau, "concat") && Word_TEXT(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int paita_raraunga = 빼기(2), 첫값 = 빼기(2); 넣기(hono_TEXT(첫값, paita_raraunga), 2); return true; }
            if (Word_TEXT(ingoa_taimau, "hashCode") && Word_TEXT(서술상수, "()I")) { int 첫값 = 빼기(2), hash_uara = 0; if (ahanoa_uara(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) hash_uara = hash_uara * 31 + 힙[첫값 + 2 + Loop_INDEX]; 넣기(hash_uara, 1); } return true; }
            if (Word_TEXT(ingoa_taimau, "toString") && Word_TEXT(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (ahanoa_uara(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_TEXT(kaipupuri, "java/lang/Integer")) {
            if (tono_CODE == 184 && Word_TEXT(ingoa_taimau, "valueOf") && Word_TEXT(서술상수, "(I)Ljava/lang/Integer;")) { int raraunga_uara = 빼기(1), ahanoa_Pūranga_kōrero = raraunga_uara >= -128 && raraunga_uara <= 127 ? Store_tau_tōpū[raraunga_uara + 128] : 0; if (ahanoa_Pūranga_kōrero == 0) { ahanoa_Pūranga_kōrero = tiritiri_Rokiroki(12, 1); if (!Pōhēhē) { 힙[ahanoa_Pūranga_kōrero + 2] = raraunga_uara; if (raraunga_uara >= -128 && raraunga_uara <= 127) Store_tau_tōpū[raraunga_uara + 128] = ahanoa_Pūranga_kōrero; } } 넣기(ahanoa_Pūranga_kōrero, 2); return true; }
            if (tono_CODE == 183 && Word_TEXT(ingoa_taimau, "<init>") && Word_TEXT(서술상수, "(I)V")) { int raraunga_uara = 빼기(1), ahanoa_Pūranga_kōrero = 빼기(2); if (ahanoa_uara(ahanoa_Pūranga_kōrero, 12)) 힙[ahanoa_Pūranga_kōrero + 2] = raraunga_uara; return true; }
            if (tono_CODE == 182 && Word_TEXT(ingoa_taimau, "intValue") && Word_TEXT(서술상수, "()I")) { int ahanoa_Pūranga_kōrero = 빼기(2); if (ahanoa_uara(ahanoa_Pūranga_kōrero, 12)) 넣기(힙[ahanoa_Pūranga_kōrero + 2], 1); return true; }
            if (tono_CODE == 184 && Word_TEXT(ingoa_taimau, "toString") && Word_TEXT(서술상수, "(I)Ljava/lang/String;")) { 넣기(mati_pūāhua(빼기(1)), 2); return true; }
        }
        if (Word_TEXT(kaipupuri, "java/lang/Math") && tono_CODE == 184) {
            if (Word_TEXT(ingoa_taimau, "abs") && Word_TEXT(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_TEXT(ingoa_taimau, "min") || Word_TEXT(ingoa_taimau, "max")) && Word_TEXT(서술상수, "(II)I")) { int paita_raraunga = 빼기(1), 첫값 = 빼기(1); 넣기(Word_TEXT(ingoa_taimau, "min") ? (첫값 < paita_raraunga ? 첫값 : paita_raraunga) : (첫값 > paita_raraunga ? 첫값 : paita_raraunga), 1); return true; }
        }
        if (Word_TEXT(kaipupuri, "java/lang/System") && tono_CODE == 184) {
            if (Word_TEXT(ingoa_taimau, "gc") && Word_TEXT(서술상수, "()V")) { 수거(); return true; }
            if (Word_TEXT(ingoa_taimau, "arraycopy") && Word_TEXT(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int tāurunga_COUNT = 빼기(1), ūnga_uara_INDEX = 빼기(1), paita_raraunga = 빼기(2), Start_tūranga = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(paita_raraunga)) {
                    int kāwai_CODE = 힙[첫값];
                    if (힙[paita_raraunga] != kāwai_CODE || (kāwai_CODE != 2 && kāwai_CODE != 3 && (kāwai_CODE < 20 || kāwai_CODE > 23))) rahunga_uara("arraycopy type mismatch");
                    else if (tāurunga_COUNT < 0 || Start_tūranga < 0 || ūnga_uara_INDEX < 0 || Start_tūranga > 힙[첫값 + 1] - tāurunga_COUNT || ūnga_uara_INDEX > 힙[paita_raraunga + 1] - tāurunga_COUNT) rahunga_uara("ArrayIndexOutOfBoundsException");
                    else if (첫값 == paita_raraunga && ūnga_uara_INDEX > Start_tūranga) { for (int Loop_INDEX = tāurunga_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) 힙[paita_raraunga + 2 + ūnga_uara_INDEX + Loop_INDEX] = 힙[첫값 + 2 + Start_tūranga + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < tāurunga_COUNT && !Pōhēhē; Loop_INDEX++) { int raraunga_uara = 힙[첫값 + 2 + Start_tūranga + Loop_INDEX]; if (kāwai_CODE != 3 || 배열저장가능(paita_raraunga, raraunga_uara)) 힙[paita_raraunga + 2 + ūnga_uara_INDEX + Loop_INDEX] = raraunga_uara; } }
                }
                return true;
            }
        }
        if (Word_TEXT(kaipupuri, "java/util/ArrayList") || Word_TEXT(kaipupuri, "java/util/List") || Word_TEXT(kaipupuri, "java/util/HashMap") || Word_TEXT(kaipupuri, "java/util/Map")) {
            모음호출(kaipupuri, ingoa_taimau, 서술상수, tono_CODE); return true;
        }
        return false;
    }
    static void 모음늘리기(int ahanoa_Pūranga_kōrero, int 필요수) {
        int 이전값 = 힙[ahanoa_Pūranga_kōrero + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int Panuku_tūranga = 용량값 < 8 ? 8 : 용량값 * 2; if (Panuku_tūranga < 필요수) Panuku_tūranga = 필요수;
        int raraunga_HUĀNGA = tiritiri_Rokiroki(3, Panuku_tūranga); if (Pōhēhē) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 용량값; Loop_INDEX++) 힙[raraunga_HUĀNGA + 2 + Loop_INDEX] = 힙[이전값 + 2 + Loop_INDEX];
        힙[ahanoa_Pūranga_kōrero + 2] = raraunga_HUĀNGA; 힙참조[ahanoa_Pūranga_kōrero + 2] = 1;
    }
    static void 모음호출(int kaipupuri, int ingoa_taimau, int 서술상수, int tono_CODE) {
        boolean 대응참조 = Word_TEXT(kaipupuri, "java/util/HashMap") || Word_TEXT(kaipupuri, "java/util/Map"); int kāwai_CODE = 대응참조 ? 11 : 10;
        if (Word_TEXT(ingoa_taimau, "<init>") && tono_CODE == 183 && Word_TEXT(서술상수, "()V")) { int ahanoa_Pūranga_kōrero = 빼기(2); if (ahanoa_uara(ahanoa_Pūranga_kōrero, kāwai_CODE)) 모음늘리기(ahanoa_Pūranga_kōrero, 8); return; }
        if (tono_CODE != 182 && tono_CODE != 185) { rahunga_uara("invalid collection invocation"); return; }
        if (Word_TEXT(ingoa_taimau, "size") && Word_TEXT(서술상수, "()I") || Word_TEXT(ingoa_taimau, "isEmpty") && Word_TEXT(서술상수, "()Z")) {
            int ahanoa_Pūranga_kōrero = 빼기(2); if (ahanoa_uara(ahanoa_Pūranga_kōrero, kāwai_CODE)) 넣기(Word_TEXT(ingoa_taimau, "size") ? 힙[ahanoa_Pūranga_kōrero + 3] : 힙[ahanoa_Pūranga_kōrero + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_TEXT(ingoa_taimau, "clear") && Word_TEXT(서술상수, "()V")) { int ahanoa_Pūranga_kōrero = 빼기(2); if (ahanoa_uara(ahanoa_Pūranga_kōrero, kāwai_CODE)) { int raraunga_HUĀNGA = 힙[ahanoa_Pūranga_kōrero + 2]; for (int Loop_INDEX = 0; Loop_INDEX < 힙[raraunga_HUĀNGA + 1]; Loop_INDEX++) 힙[raraunga_HUĀNGA + 2 + Loop_INDEX] = 0; 힙[ahanoa_Pūranga_kōrero + 3] = 0; } return; }
        if (!대응참조 && Word_TEXT(ingoa_taimau, "add") && Word_TEXT(서술상수, "(Ljava/lang/Object;)Z")) {
            int raraunga_uara = 빼기(2), ahanoa_Pūranga_kōrero = 빼기(2); if (!ahanoa_uara(ahanoa_Pūranga_kōrero, 10)) return;
            int tāurunga_COUNT = 힙[ahanoa_Pūranga_kōrero + 3]; 모음늘리기(ahanoa_Pūranga_kōrero, tāurunga_COUNT + 1); if (!Pōhēhē) { 힙[힙[ahanoa_Pūranga_kōrero + 2] + 2 + tāurunga_COUNT] = raraunga_uara; 힙[ahanoa_Pūranga_kōrero + 3] = tāurunga_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_TEXT(ingoa_taimau, "get") || Word_TEXT(ingoa_taimau, "remove")) && Word_TEXT(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_TEXT(ingoa_taimau, "set") && Word_TEXT(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Word_TEXT(ingoa_taimau, "set"); int raraunga_uara = 지정여부 ? 빼기(2) : 0, tāurunga_tūranga = 빼기(1), ahanoa_Pūranga_kōrero = 빼기(2);
            if (!ahanoa_uara(ahanoa_Pūranga_kōrero, 10)) return;
            int tāurunga_COUNT = 힙[ahanoa_Pūranga_kōrero + 3], raraunga_HUĀNGA = 힙[ahanoa_Pūranga_kōrero + 2];
            if (tāurunga_tūranga < 0 || tāurunga_tūranga >= tāurunga_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[raraunga_HUĀNGA + 2 + tāurunga_tūranga];
            if (지정여부) 힙[raraunga_HUĀNGA + 2 + tāurunga_tūranga] = raraunga_uara;
            if (Word_TEXT(ingoa_taimau, "remove")) { for (int Loop_INDEX = tāurunga_tūranga + 1; Loop_INDEX < tāurunga_COUNT; Loop_INDEX++) 힙[raraunga_HUĀNGA + 1 + Loop_INDEX] = 힙[raraunga_HUĀNGA + 2 + Loop_INDEX]; 힙[raraunga_HUĀNGA + 1 + tāurunga_COUNT] = 0; 힙[ahanoa_Pūranga_kōrero + 3] = tāurunga_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_TEXT(ingoa_taimau, "get") || Word_TEXT(ingoa_taimau, "remove")) && Word_TEXT(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_TEXT(ingoa_taimau, "put") && Word_TEXT(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_TEXT(ingoa_taimau, "containsKey") && Word_TEXT(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_TEXT(ingoa_taimau, "put"), tango = Word_TEXT(ingoa_taimau, "remove");
            int raraunga_uara = 넣기여부 ? 빼기(2) : 0, kī_Pūranga_kōrero = 빼기(2), ahanoa_Pūranga_kōrero = 빼기(2); if (!ahanoa_uara(ahanoa_Pūranga_kōrero, 11)) return;
            int tāurunga_COUNT = 힙[ahanoa_Pūranga_kōrero + 3], raraunga_HUĀNGA = 힙[ahanoa_Pūranga_kōrero + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < tāurunga_COUNT; Loop_INDEX++) if (값같음(kī_Pūranga_kōrero, 힙[raraunga_HUĀNGA + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[raraunga_HUĀNGA + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(ahanoa_Pūranga_kōrero, (tāurunga_COUNT + 1) * 2); raraunga_HUĀNGA = 힙[ahanoa_Pūranga_kōrero + 2]; 찾은여부 = tāurunga_COUNT; if (!Pōhēhē) 힙[ahanoa_Pūranga_kōrero + 3] = tāurunga_COUNT + 1; }
                if (!Pōhēhē) { 힙[raraunga_HUĀNGA + 2 + 2 * 찾은여부] = kī_Pūranga_kōrero; 힙[raraunga_HUĀNGA + 3 + 2 * 찾은여부] = raraunga_uara; }
            }
            if (tango && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < tāurunga_COUNT; Loop_INDEX++) { 힙[raraunga_HUĀNGA + 2 * Loop_INDEX] = 힙[raraunga_HUĀNGA + 2 + 2 * Loop_INDEX]; 힙[raraunga_HUĀNGA + 1 + 2 * Loop_INDEX] = 힙[raraunga_HUĀNGA + 3 + 2 * Loop_INDEX]; } 힙[raraunga_HUĀNGA + 2 * tāurunga_COUNT] = 0; 힙[raraunga_HUĀNGA + 1 + 2 * tāurunga_COUNT] = 0; 힙[ahanoa_Pūranga_kōrero + 3] = tāurunga_COUNT - 1; }
            if (Word_TEXT(ingoa_taimau, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        rahunga_uara("unsupported collection method");
    }
    static boolean 잠금얻기(int ahanoa_Pūranga_kōrero) {
        if (!객체유효(ahanoa_Pūranga_kōrero)) return false;
        if (잠금깊이[ahanoa_Pūranga_kōrero] != 0 && 잠금주인[ahanoa_Pūranga_kōrero] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        잠금주인[ahanoa_Pūranga_kōrero] = 현재가닥 + 1; 잠금깊이[ahanoa_Pūranga_kōrero]++; return true;
    }
    static void 잠금풀기(int ahanoa_Pūranga_kōrero) {
        if (!객체유효(ahanoa_Pūranga_kōrero)) return;
        if (잠금깊이[ahanoa_Pūranga_kōrero] == 0 || 잠금주인[ahanoa_Pūranga_kōrero] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[ahanoa_Pūranga_kōrero] == 0) 잠금주인[ahanoa_Pūranga_kōrero] = 0;
    }
    static boolean SWITCH_miro() {
        miro_tāpare[현재가닥] = tāpare_INDEX;
        if (tāpare_INDEX < 현재가닥 * 32) miro_tūnga[현재가닥] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < miro_COUNT; Loop_INDEX++) if (miro_tūnga[Loop_INDEX] == 2 && miro_tūnga[가닥대기[Loop_INDEX]] == 3) miro_tūnga[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= miro_COUNT; Loop_INDEX++) {
            int Panuku_tūranga = (현재가닥 + Loop_INDEX) % miro_COUNT;
            if (miro_tūnga[Panuku_tūranga] == 1) { 현재가닥 = Panuku_tūranga; tāpare_INDEX = miro_tāpare[Panuku_tūranga]; 바꿈요청 = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < miro_COUNT; Loop_INDEX++) if (miro_tūnga[Loop_INDEX] != 3) { rahunga_uara("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int ingoa_taimau, int 서술상수, int tono_CODE) { Hātepe_miro(ingoa_taimau, 서술상수, tono_CODE, false); }
    static void Hātepe_miro(int ingoa_taimau, int 서술상수, int tono_CODE, boolean Reo_Māori) {
        if (tono_CODE == 184 && Word_TEXT(ingoa_taimau, Reo_Māori ? "YIELD_tūmahi" : "yield") && Word_TEXT(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (tono_CODE == 184 && Word_TEXT(ingoa_taimau, "currentThread") && Word_TEXT(서술상수, "()Ljava/lang/Thread;")) { 넣기(miro_ahanoa[현재가닥], 2); return; }
        if (tono_CODE == 183 && Word_TEXT(ingoa_taimau, "<init>") && (Word_TEXT(서술상수, "()V") || Word_TEXT(서술상수, Reo_Māori ? "(LReo_Māori/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int ūnga_ADDRESS = Word_TEXT(서술상수, "()V") ? 0 : 빼기(2), ahanoa_Pūranga_kōrero = 빼기(2);
            if (!객체유효(ahanoa_Pūranga_kōrero)) return;
            if (힙[ahanoa_Pūranga_kōrero] == 13) { 힙[ahanoa_Pūranga_kōrero + 2] = ūnga_ADDRESS; 힙참조[ahanoa_Pūranga_kōrero + 2] = 1; }
            else if (ūnga_ADDRESS != 0) rahunga_uara("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (tono_CODE == 182 && (Word_TEXT(ingoa_taimau, Reo_Māori ? "Start_tūmahi" : "start") || Word_TEXT(ingoa_taimau, Reo_Māori ? "기다리기" : "join")) && Word_TEXT(서술상수, "()V") || tono_CODE == 182 && Word_TEXT(ingoa_taimau, Reo_Māori ? "살아있는가" : "isAlive") && Word_TEXT(서술상수, "()Z")) {
            int ahanoa_Pūranga_kōrero = 빼기(2); if (!객체유효(ahanoa_Pūranga_kōrero)) return;
            int pūkete_uara = -1; for (int Loop_INDEX = 0; Loop_INDEX < miro_COUNT; Loop_INDEX++) if (miro_ahanoa[Loop_INDEX] == ahanoa_Pūranga_kōrero) pūkete_uara = Loop_INDEX;
            if (Word_TEXT(ingoa_taimau, Reo_Māori ? "살아있는가" : "isAlive")) { 넣기(pūkete_uara >= 0 && miro_tūnga[pūkete_uara] != 3 ? 1 : 0, 1); return; }
            if (Word_TEXT(ingoa_taimau, Reo_Māori ? "기다리기" : "join")) { if (pūkete_uara >= 0 && miro_tūnga[pūkete_uara] != 3) { 가닥대기[현재가닥] = pūkete_uara; miro_tūnga[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (pūkete_uara >= 0) { 예외던짐(Reo_Māori ? 38 : 16, "thread already started"); return; }
            if (miro_COUNT == 4) { rahunga_uara("thread limit (4 including main)"); return; }
            int ūnga_ADDRESS = 힙[ahanoa_Pūranga_kōrero] == 13 ? 힙[ahanoa_Pūranga_kōrero + 2] : ahanoa_Pūranga_kōrero;
            int kōnae_INDEX = ūnga_ADDRESS > 0 && 힙[ūnga_ADDRESS] >= 32 ? ingoa_aratuka(힙[ūnga_ADDRESS] - 32, Reo_Māori ? "kawe_tūmahi" : "run", "()V") : -1;
            if (ūnga_ADDRESS != 0 && kōnae_INDEX < 0) { rahunga_uara("Runnable.run required"); return; }
            pūkete_uara = miro_COUNT++; miro_ahanoa[pūkete_uara] = ahanoa_Pūranga_kōrero; miro_ūnga[pūkete_uara] = ūnga_ADDRESS;
            int tāpare = pūkete_uara * 32; miro_tāpare[pūkete_uara] = kōnae_INDEX < 0 ? tāpare - 1 : tāpare; miro_tūnga[pūkete_uara] = kōnae_INDEX < 0 ? 3 : 1;
            if (kōnae_INDEX >= 0) { tāpare_aratuka[tāpare] = kōnae_INDEX; tāpare_tūranga[tāpare] = aratuka_Start[kōnae_INDEX]; paetata_uara[tāpare * 128] = ūnga_ADDRESS; paetata_TYPE[tāpare * 128] = 2; }
            return;
        }
        rahunga_uara("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], ADDRESS_TEXT = new int[16];
    static int paetata_ADDRESS() { return ADDRESS_ahanoa(0x7f000001); }
    static int ADDRESS_ahanoa(int uara) { int ahanoa_Pūranga_kōrero = tiritiri_Rokiroki(14, 1); if (!Pōhēhē) 힙[ahanoa_Pūranga_kōrero + 2] = uara; return ahanoa_Pūranga_kōrero; }
    static int 주소해독(int ahanoa_Pūranga_kōrero) {
        if (ahanoa_Pūranga_kōrero == 0 || 글같음(ahanoa_Pūranga_kōrero, taurima_pūāhua("localhost"), false)) return 0x7f000001;
        if (!ahanoa_uara(ahanoa_Pūranga_kōrero, 1)) return 0;
        int raraunga_uara = 0, 총수 = 0, ADDRESS_paita = 0, 자릿수 = 0, tāurunga_COUNT = 힙[ahanoa_Pūranga_kōrero + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= tāurunga_COUNT; Loop_INDEX++) {
            int waehere_pūāhua = Loop_INDEX == tāurunga_COUNT ? '.' : 힙[ahanoa_Pūranga_kōrero + 2 + Loop_INDEX];
            if (waehere_pūāhua == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } raraunga_uara = raraunga_uara << 8 | ADDRESS_paita; 총수++; ADDRESS_paita = 자릿수 = 0; }
            else { if (waehere_pūāhua < '0' || waehere_pūāhua > '9' || ++자릿수 > 3 || (ADDRESS_paita = ADDRESS_paita * 10 + waehere_pūāhua - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return raraunga_uara;
    }
    static int ADDRESS_pūāhua(int raraunga_uara) {
        int tāurunga_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int ADDRESS_paita = raraunga_uara >>> 이동비트 & 255;
            if (ADDRESS_paita >= 100) ADDRESS_TEXT[tāurunga_COUNT++] = '0' + ADDRESS_paita / 100;
            if (ADDRESS_paita >= 10) ADDRESS_TEXT[tāurunga_COUNT++] = '0' + ADDRESS_paita / 10 % 10;
            ADDRESS_TEXT[tāurunga_COUNT++] = '0' + ADDRESS_paita % 10; if (이동비트 != 0) ADDRESS_TEXT[tāurunga_COUNT++] = '.';
        }
        int ahanoa_Pūranga_kōrero = tiritiri_Rokiroki(1, tāurunga_COUNT); if (!Pōhēhē) for (int Loop_INDEX = 0; Loop_INDEX < tāurunga_COUNT; Loop_INDEX++) 힙[ahanoa_Pūranga_kōrero + 2 + Loop_INDEX] = ADDRESS_TEXT[Loop_INDEX]; return ahanoa_Pūranga_kōrero;
    }
    static void 통신호출(int kaipupuri, int ingoa_taimau, int 서술상수, int tono_CODE) {
        if (Word_TEXT(kaipupuri, "java/net/InetAddress")) {
            if (tono_CODE == 184 && Word_TEXT(ingoa_taimau, "getLoopbackAddress") && Word_TEXT(서술상수, "()Ljava/net/InetAddress;")) { 넣기(paetata_ADDRESS(), 2); return; }
            if (tono_CODE == 184 && Word_TEXT(ingoa_taimau, "getByName") && Word_TEXT(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int raraunga_uara = 주소해독(빼기(2)); if (던진객체 == 0 && !Pōhēhē) 넣기(ADDRESS_ahanoa(raraunga_uara), 2); return;
            }
            if (tono_CODE == 182 && Word_TEXT(ingoa_taimau, "getHostAddress") && Word_TEXT(서술상수, "()Ljava/lang/String;")) { int ahanoa_Pūranga_kōrero = 빼기(2); if (ahanoa_uara(ahanoa_Pūranga_kōrero, 14)) 넣기(ADDRESS_pūāhua(힙[ahanoa_Pūranga_kōrero + 2]), 2); return; }
        }
        if (Word_TEXT(kaipupuri, "java/net/DatagramPacket")) {
            if (tono_CODE == 183 && Word_TEXT(ingoa_taimau, "<init>") && (Word_TEXT(서술상수, "([BI)V") || Word_TEXT(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean ūnga_uara_Pūranga_kōrero = Word_TEXT(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = ūnga_uara_Pūranga_kōrero ? 빼기(1) : 0, ADDRESS_Pūranga_kōrero = ūnga_uara_Pūranga_kōrero ? 빼기(2) : 0;
                int tāurunga_COUNT = 빼기(1), raraunga_HUĀNGA = 빼기(2), ahanoa_Pūranga_kōrero = 빼기(2);
                if (!ahanoa_uara(ahanoa_Pūranga_kōrero, 16) || !ahanoa_uara(raraunga_HUĀNGA, 20)) return;
                if (tāurunga_COUNT < 0 || tāurunga_COUNT > 힙[raraunga_HUĀNGA + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (ADDRESS_Pūranga_kōrero != 0 && !ahanoa_uara(ADDRESS_Pūranga_kōrero, 14)) return;
                힙[ahanoa_Pūranga_kōrero + 2] = raraunga_HUĀNGA; 힙참조[ahanoa_Pūranga_kōrero + 2] = 1; 힙[ahanoa_Pūranga_kōrero + 3] = tāurunga_COUNT;
                힙[ahanoa_Pūranga_kōrero + 4] = ADDRESS_Pūranga_kōrero; 힙참조[ahanoa_Pūranga_kōrero + 4] = 1; 힙[ahanoa_Pūranga_kōrero + 5] = 접속번호; return;
            }
            if (tono_CODE == 182 && Word_TEXT(ingoa_taimau, "setLength") && Word_TEXT(서술상수, "(I)V")) {
                int tāurunga_COUNT = 빼기(1), ahanoa_Pūranga_kōrero = 빼기(2); if (!ahanoa_uara(ahanoa_Pūranga_kōrero, 16)) return;
                if (tāurunga_COUNT < 0 || tāurunga_COUNT > 힙[힙[ahanoa_Pūranga_kōrero + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[ahanoa_Pūranga_kōrero + 3] = tāurunga_COUNT; return;
            }
            if (tono_CODE == 182 && (Word_TEXT(ingoa_taimau, "getData") && Word_TEXT(서술상수, "()[B") || Word_TEXT(ingoa_taimau, "getLength") && Word_TEXT(서술상수, "()I") || Word_TEXT(ingoa_taimau, "getAddress") && Word_TEXT(서술상수, "()Ljava/net/InetAddress;") || Word_TEXT(ingoa_taimau, "getPort") && Word_TEXT(서술상수, "()I"))) {
                int ahanoa_Pūranga_kōrero = 빼기(2); if (!ahanoa_uara(ahanoa_Pūranga_kōrero, 16)) return;
                int tāurunga_tūranga = Word_TEXT(ingoa_taimau, "getData") ? 2 : Word_TEXT(ingoa_taimau, "getLength") ? 3 : Word_TEXT(ingoa_taimau, "getAddress") ? 4 : 5;
                넣기(힙[ahanoa_Pūranga_kōrero + tāurunga_tūranga], tāurunga_tūranga == 2 || tāurunga_tūranga == 4 ? 2 : 1); return;
            }
        }
        if (Word_TEXT(kaipupuri, "java/net/DatagramSocket")) {
            if (tono_CODE == 183 && Word_TEXT(ingoa_taimau, "<init>") && (Word_TEXT(서술상수, "()V") || Word_TEXT(서술상수, "(I)V"))) {
                int 접속번호 = Word_TEXT(서술상수, "()V") ? 0 : 빼기(1), ahanoa_Pūranga_kōrero = 빼기(2); if (!ahanoa_uara(ahanoa_Pūranga_kōrero, 15)) return;
                if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = kaiwhakamahi.tiwhikete_whatunga(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[ahanoa_Pūranga_kōrero + 2] = 열린파일번호; return;
            }
            if (tono_CODE == 182 && Word_TEXT(ingoa_taimau, "setSoTimeout") && Word_TEXT(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), ahanoa_Pūranga_kōrero = 빼기(2); if (!ahanoa_uara(ahanoa_Pūranga_kōrero, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[ahanoa_Pūranga_kōrero + 3] = 밀리초값; return;
            }
            if (tono_CODE == 182 && Word_TEXT(ingoa_taimau, "getLocalPort") && Word_TEXT(서술상수, "()I")) { int ahanoa_Pūranga_kōrero = 빼기(2); if (ahanoa_uara(ahanoa_Pūranga_kōrero, 15)) 넣기(힙[ahanoa_Pūranga_kōrero + 2] < 0 ? -1 : kaiwhakamahi.whatunga_kawe(힙[ahanoa_Pūranga_kōrero + 2]), 1); return; }
            if (tono_CODE == 182 && Word_TEXT(ingoa_taimau, "isClosed") && Word_TEXT(서술상수, "()Z")) { int ahanoa_Pūranga_kōrero = 빼기(2); if (ahanoa_uara(ahanoa_Pūranga_kōrero, 15)) 넣기(힙[ahanoa_Pūranga_kōrero + 2] < 0 ? 1 : 0, 1); return; }
            if (tono_CODE == 182 && Word_TEXT(ingoa_taimau, "close") && Word_TEXT(서술상수, "()V")) { int ahanoa_Pūranga_kōrero = 빼기(2); if (ahanoa_uara(ahanoa_Pūranga_kōrero, 15) && 힙[ahanoa_Pūranga_kōrero + 2] >= 0) { kaiwhakamahi.파일서술자닫기(힙[ahanoa_Pūranga_kōrero + 2]); 힙[ahanoa_Pūranga_kōrero + 2] = -1; } return; }
            if (tono_CODE == 182 && (Word_TEXT(ingoa_taimau, "send") || Word_TEXT(ingoa_taimau, "receive")) && Word_TEXT(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int pākete = 빼기(2), ahanoa_Pūranga_kōrero = 빼기(2); if (!ahanoa_uara(pākete, 16) || !ahanoa_uara(ahanoa_Pūranga_kōrero, 15)) return;
                int raraunga_HUĀNGA = 힙[pākete + 2], 유효길이 = 힙[pākete + 3], 열린파일번호 = 힙[ahanoa_Pūranga_kōrero + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_TEXT(ingoa_taimau, "send")) {
                    if (!ahanoa_uara(힙[pākete + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = 힙[raraunga_HUĀNGA + 2 + Loop_INDEX];
                    if (kaiwhakamahi.tuku_whatunga(열린파일번호, 힙[힙[pākete + 4] + 2], 힙[pākete + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int tāurunga_COUNT = kaiwhakamahi.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (tāurunga_COUNT == -11) {
                        int 현재시각 = kaiwhakamahi.밀리초();
                        if (힙[ahanoa_Pūranga_kōrero + 4] == 0) 힙[ahanoa_Pūranga_kōrero + 4] = 현재시각 + 1;
                        if (힙[ahanoa_Pūranga_kōrero + 3] > 0 && 현재시각 - (힙[ahanoa_Pūranga_kōrero + 4] - 1) >= 힙[ahanoa_Pūranga_kōrero + 3]) { 힙[ahanoa_Pūranga_kōrero + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(ahanoa_Pūranga_kōrero, 2); 넣기(pākete, 2); tāpare_tūranga[tāpare_INDEX] = tāpare_tohutohu[tāpare_INDEX]; 바꿈요청 = true; return;
                    }
                    힙[ahanoa_Pūranga_kōrero + 4] = 0;
                    if (tāurunga_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < tāurunga_COUNT; Loop_INDEX++) 힙[raraunga_HUĀNGA + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    힙[pākete + 3] = tāurunga_COUNT; 힙[pākete + 4] = ADDRESS_ahanoa(통신임시[513]); 힙참조[pākete + 4] = 1; 힙[pākete + 5] = 통신임시[512];
                }
                return;
            }
        }
        rahunga_uara("unsupported java.net method");
    }
    static boolean 흐름대기(int ahanoa_Pūranga_kōrero) {
        int 현재시각 = kaiwhakamahi.밀리초();
        if (힙[ahanoa_Pūranga_kōrero + 5] == 0) 힙[ahanoa_Pūranga_kōrero + 5] = 현재시각 + 1;
        if (힙[ahanoa_Pūranga_kōrero + 3] > 0 && 현재시각 - (힙[ahanoa_Pūranga_kōrero + 5] - 1) >= 힙[ahanoa_Pūranga_kōrero + 3]) { 힙[ahanoa_Pūranga_kōrero + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        tāpare_tūranga[tāpare_INDEX] = tāpare_tohutohu[tāpare_INDEX]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int kaipupuri, int ingoa_taimau, int 서술상수, int tono_CODE) {
        boolean 수신쪽 = Word_TEXT(kaipupuri, "java/net/ServerSocket"), roma = Word_TEXT(kaipupuri, "java/io/InputStream") || Word_TEXT(kaipupuri, "java/io/OutputStream");
        if (!roma && tono_CODE == 183 && Word_TEXT(ingoa_taimau, "<init>")) {
            boolean 빈여부 = Word_TEXT(서술상수, "()V"), 이름지정여부 = Word_TEXT(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_TEXT(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && Word_TEXT(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { rahunga_uara("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), ADDRESS_Pūranga_kōrero = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, ahanoa_Pūranga_kōrero = 빼기(2);
            if (!ahanoa_uara(ahanoa_Pūranga_kōrero, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !ahanoa_uara(ADDRESS_Pūranga_kōrero, 14)) return;
            int whatunga_ADDRESS = 이름지정여부 ? 주소해독(ADDRESS_Pūranga_kōrero) : 주소지정여부 ? 힙[ADDRESS_Pūranga_kōrero + 2] : 0x7f000001;
            if (Pōhēhē || 던진객체 != 0) return;
            int 열린파일번호 = kaiwhakamahi.roma_mana(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? kaiwhakamahi.roma_mana(1, 열린파일번호, 접속번호) : kaiwhakamahi.TŪHONO_roma(열린파일번호, whatunga_ADDRESS, 접속번호);
            if (처리값 < 0) { kaiwhakamahi.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[ahanoa_Pūranga_kōrero + 2] = 열린파일번호; 힙[ahanoa_Pūranga_kōrero + 4] = 접속번호; 힙[ahanoa_Pūranga_kōrero + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!roma && Word_TEXT(ingoa_taimau, "setSoTimeout") && Word_TEXT(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), ahanoa_Pūranga_kōrero = 빼기(2); if (!ahanoa_uara(ahanoa_Pūranga_kōrero, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[ahanoa_Pūranga_kōrero + 3] = 밀리초값; return; }
        if (!roma && Word_TEXT(ingoa_taimau, "close") && Word_TEXT(서술상수, "()V")) { int ahanoa_Pūranga_kōrero = 빼기(2); if (ahanoa_uara(ahanoa_Pūranga_kōrero, 수신쪽 ? 18 : 17) && 힙[ahanoa_Pūranga_kōrero + 2] >= 0) { kaiwhakamahi.파일서술자닫기(힙[ahanoa_Pūranga_kōrero + 2]); 힙[ahanoa_Pūranga_kōrero + 2] = -1; } return; }
        if (!roma && (Word_TEXT(ingoa_taimau, "getLocalPort") || Word_TEXT(ingoa_taimau, "getPort") || Word_TEXT(ingoa_taimau, "isClosed") || Word_TEXT(ingoa_taimau, "isConnected"))) {
            int ahanoa_Pūranga_kōrero = 빼기(2); if (!ahanoa_uara(ahanoa_Pūranga_kōrero, 수신쪽 ? 18 : 17)) return;
            넣기(Word_TEXT(ingoa_taimau, "isClosed") ? 힙[ahanoa_Pūranga_kōrero + 2] < 0 ? 1 : 0 : Word_TEXT(ingoa_taimau, "isConnected") ? 힙[ahanoa_Pūranga_kōrero + 6] : Word_TEXT(ingoa_taimau, "getPort") ? 힙[ahanoa_Pūranga_kōrero + 4] : 힙[ahanoa_Pūranga_kōrero + 2] < 0 ? -1 : kaiwhakamahi.roma_mana(4, 힙[ahanoa_Pūranga_kōrero + 2], 0), 1); return;
        }
        if (수신쪽 && Word_TEXT(ingoa_taimau, "accept") && Word_TEXT(서술상수, "()Ljava/net/Socket;")) {
            int ahanoa_Pūranga_kōrero = 빼기(2); if (!ahanoa_uara(ahanoa_Pūranga_kōrero, 18)) return; int 열린파일번호 = kaiwhakamahi.roma_mana(3, 힙[ahanoa_Pūranga_kōrero + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(ahanoa_Pūranga_kōrero)) 넣기(ahanoa_Pūranga_kōrero, 2); return; }
            힙[ahanoa_Pūranga_kōrero + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = tiritiri_Rokiroki(17, 5); if (Pōhēhē) { kaiwhakamahi.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = kaiwhakamahi.roma_mana(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !roma && ((Word_TEXT(ingoa_taimau, "getInputStream") && Word_TEXT(서술상수, "()Ljava/io/InputStream;")) || (Word_TEXT(ingoa_taimau, "getOutputStream") && Word_TEXT(서술상수, "()Ljava/io/OutputStream;")))) {
            int ahanoa_Pūranga_kōrero = 빼기(2); if (!ahanoa_uara(ahanoa_Pūranga_kōrero, 17)) return; if (힙[ahanoa_Pūranga_kōrero + 2] < 0 || 힙[ahanoa_Pūranga_kōrero + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = tiritiri_Rokiroki(19, 4); if (Pōhēhē) return; 힙[반환값 + 2] = ahanoa_Pūranga_kōrero; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_TEXT(ingoa_taimau, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (roma) {
            boolean 읽기여부 = Word_TEXT(ingoa_taimau, "read"), 쓰기여부 = Word_TEXT(ingoa_taimau, "write"), aukati = Word_TEXT(서술상수, "([B)I") || Word_TEXT(서술상수, "([B)V"), 부분배열여부 = Word_TEXT(서술상수, "([BII)I") || Word_TEXT(서술상수, "([BII)V");
            int tāurunga_COUNT = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, raraunga_HUĀNGA = aukati || 부분배열여부 ? 빼기(2) : 0;
            int raraunga_uara = 쓰기여부 && Word_TEXT(서술상수, "(I)V") ? 빼기(1) : 0, ahanoa_Pūranga_kōrero = 빼기(2);
            if (!ahanoa_uara(ahanoa_Pūranga_kōrero, 19)) return; int 부모참조 = 힙[ahanoa_Pūranga_kōrero + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_TEXT(ingoa_taimau, "close") && Word_TEXT(서술상수, "()V")) { kaiwhakamahi.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Word_TEXT(ingoa_taimau, "flush") && Word_TEXT(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[ahanoa_Pūranga_kōrero + 3] == 0)) { rahunga_uara("unsupported stream operation"); return; }
            if (aukati || 부분배열여부) { if (!ahanoa_uara(raraunga_HUĀNGA, 20)) return; if (aukati) tāurunga_COUNT = 힙[raraunga_HUĀNGA + 1]; if (시작변위 < 0 || tāurunga_COUNT < 0 || 시작변위 > 힙[raraunga_HUĀNGA + 1] - tāurunga_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else tāurunga_COUNT = 1;
            if (tāurunga_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[ahanoa_Pūranga_kōrero + 4] : 0, 처리값 = 0;
            while (완료수 < tāurunga_COUNT) {
                처리값 = 읽기여부 ? kaiwhakamahi.파일한바이트읽기(열린파일번호) : kaiwhakamahi.파일한바이트쓰기(열린파일번호, aukati || 부분배열여부 ? 힙[raraunga_HUĀNGA + 2 + 시작변위 + 완료수] : raraunga_uara);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (aukati || 부분배열여부)) 힙[raraunga_HUĀNGA + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(aukati || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[ahanoa_Pūranga_kōrero + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(ahanoa_Pūranga_kōrero, 2); if (aukati || 부분배열여부) 넣기(raraunga_HUĀNGA, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(tāurunga_COUNT, 1); } if (쓰기여부 && !(aukati || 부분배열여부)) 넣기(raraunga_uara, 1); } return;
            }
            힙[ahanoa_Pūranga_kōrero + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : aukati || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        rahunga_uara("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int ingoa_taimau) {
        if (Word_TEXT(ingoa_taimau, "Reo_Māori/자체/matapihi")) return 24;
        if (Word_TEXT(ingoa_taimau, "Reo_Māori/자체/tapanga")) return 26;
        if (Word_TEXT(ingoa_taimau, "Reo_Māori/자체/pātene")) return 27;
        if (Word_TEXT(ingoa_taimau, "Reo_Māori/자체/āpure_kuputuhi")) return 28;
        if (Word_TEXT(ingoa_taimau, "Reo_Māori/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int ingoa_taimau) {
        return 한국어화면종(ingoa_taimau) != 0 || Word_TEXT(ingoa_taimau, "Reo_Māori/자체/화면구성요소") || Word_TEXT(ingoa_taimau, "Reo_Māori/자체/hui_tūtira");
    }
    static int 화면종(int ingoa_taimau) {
        int 한국어종 = 한국어화면종(ingoa_taimau); if (한국어종 != 0) return 한국어종;
        if (Word_TEXT(ingoa_taimau, "javax/swing/JFrame")) return 24;
        if (Word_TEXT(ingoa_taimau, "javax/swing/JPanel")) return 25;
        if (Word_TEXT(ingoa_taimau, "javax/swing/JLabel")) return 26;
        if (Word_TEXT(ingoa_taimau, "javax/swing/JButton")) return 27;
        if (Word_TEXT(ingoa_taimau, "javax/swing/JTextField")) return 28;
        if (Word_TEXT(ingoa_taimau, "java/awt/event/ActionEvent")) return 29;
        if (Word_TEXT(ingoa_taimau, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int ingoa_taimau) {
        return 화면종(ingoa_taimau) != 0 || Word_TEXT(ingoa_taimau, "java/awt/Component") || Word_TEXT(ingoa_taimau, "java/awt/Container") || Word_TEXT(ingoa_taimau, "javax/swing/JComponent") || Word_TEXT(ingoa_taimau, "javax/swing/AbstractButton") || Word_TEXT(ingoa_taimau, "javax/swing/text/JTextComponent") || Word_TEXT(ingoa_taimau, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int ahanoa_Pūranga_kōrero) { if (!객체유효(ahanoa_Pūranga_kōrero)) return false; if (힙[ahanoa_Pūranga_kōrero] < 24 || 힙[ahanoa_Pūranga_kōrero] > 28) { rahunga_uara("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int ahanoa_Pūranga_kōrero, int TEXT_Pūranga_kōrero) {
        if (TEXT_Pūranga_kōrero != 0 && !ahanoa_uara(TEXT_Pūranga_kōrero, 1)) return;
        int tāurunga_COUNT = TEXT_Pūranga_kōrero == 0 ? 0 : 힙[TEXT_Pūranga_kōrero + 1]; if (tāurunga_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < tāurunga_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = 힙[TEXT_Pūranga_kōrero + 2 + Loop_INDEX];
        if (kaiwhakamahi.화면글(힙[ahanoa_Pūranga_kōrero + 2], 화면글임시, tāurunga_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[ahanoa_Pūranga_kōrero + 3] = TEXT_Pūranga_kōrero; 힙참조[ahanoa_Pūranga_kōrero + 3] = 1;
    }
    static int 화면문자읽기(int ahanoa_Pūranga_kōrero) {
        int pūkete_uara = 힙[ahanoa_Pūranga_kōrero + 2], tāurunga_COUNT = kaiwhakamahi.화면연결(8, pūkete_uara, 0, 0, 0, 0), 사용수 = 0;
        if (tāurunga_COUNT < 0) { rahunga_uara("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < tāurunga_COUNT; Loop_INDEX++) { int 부호값 = kaiwhakamahi.화면연결(9, pūkete_uara, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = tiritiri_Rokiroki(1, 사용수); if (!Pōhēhē) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* Reo_Māori 객체를 직접 만들고 kākano_uara_0611a8a8 화면 기능에 연결한다. Swing ahanoa_uara/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int kaipupuri, int ingoa_taimau, int 서술상수, int tono_CODE) {
        if (Word_TEXT(kaipupuri, "Reo_Māori/자체/hui_tūtira")) {
            if (tono_CODE == 184 && Word_TEXT(ingoa_taimau, "나중에실행") && Word_TEXT(서술상수, "(LReo_Māori/자체/실행할일;)V")) {
                int tūmahi_hohenga = 빼기(2); if (!객체유효(tūmahi_hohenga)) return;
                if (나중수 == 8) { rahunga_uara("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = tūmahi_hohenga; return;
            }
            if (tono_CODE == 184 && Word_TEXT(ingoa_taimau, "사건처리중인가") && Word_TEXT(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            rahunga_uara("지원하지 않는 Reo_Māori 화면 일정 호출"); return;
        }
        if (Word_TEXT(kaipupuri, "Reo_Māori/자체/동작알림")) {
            int 알림 = 빼기(2); if (!ahanoa_uara(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Word_TEXT(ingoa_taimau, "hui_pūtake") && Word_TEXT(서술상수, "()LReo_Māori/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Word_TEXT(ingoa_taimau, "tono_TEXT") && Word_TEXT(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Word_TEXT(ingoa_taimau, "INDEX") && Word_TEXT(서술상수, "()I")) 넣기(1001, 1);
            else rahunga_uara("지원하지 않는 Reo_Māori hohenga 알림 호출"); return;
        }
        if (tono_CODE == 183 && Word_TEXT(ingoa_taimau, "<init>")) {
            int 종류 = 한국어화면종(kaipupuri), 받이 = 0, 가로 = 0, Poutū_tūranga = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_TEXT(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (kaiwhakamahi.화면너비() - 폭) / 2; Poutū_tūranga = (kaiwhakamahi.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_TEXT(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_TEXT(서술상수, "(Ljava/lang/String;IIIILReo_Māori/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); Poutū_tūranga = 빼기(1); 가로 = 빼기(1);
            } else { rahunga_uara("지원하지 않는 Reo_Māori 화면 생성자"); return; }
            int Ngā_kupu = 빼기(2), huānga_uara = 빼기(2); if (!화면객체(huānga_uara)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || Poutū_tūranga < 0 || 폭 > kaiwhakamahi.화면너비() - 가로 || 높이 > kaiwhakamahi.화면높이() - Poutū_tūranga) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = kaiwhakamahi.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { rahunga_uara("화면 huānga_uara 자리가 가득 찼습니다"); return; }
            힙[huānga_uara + 2] = INDEX; 화면참조[INDEX - 1] = huānga_uara;
            힙[huānga_uara + 5] = 가로; 힙[huānga_uara + 6] = Poutū_tūranga; 힙[huānga_uara + 7] = 폭; 힙[huānga_uara + 8] = 높이; 힙[huānga_uara + 10] = 2;
            힙[huānga_uara + 4] = 받이; 힙참조[huānga_uara + 4] = 1; 힙[huānga_uara + 12] = 1;
            kaiwhakamahi.화면연결(1, INDEX, 가로, Poutū_tūranga, 폭, 높이);
            if (종류 == 24) kaiwhakamahi.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(huānga_uara, Ngā_kupu); return;
        }
        if (tono_CODE != 182) { rahunga_uara("잘못된 Reo_Māori 화면 호출 tono"); return; }
        if (Word_TEXT(ingoa_taimau, "tuhi_TEXT") && Word_TEXT(서술상수, "(Ljava/lang/String;)V")) {
            int Ngā_kupu = 빼기(2), huānga_uara = 빼기(2); if (화면객체(huānga_uara)) 화면문자설정(huānga_uara, Ngā_kupu); return;
        }
        if (Word_TEXT(ingoa_taimau, "글읽기") && Word_TEXT(서술상수, "()Ljava/lang/String;")) {
            int huānga_uara = 빼기(2); if (화면객체(huānga_uara)) 넣기(화면문자읽기(huānga_uara), 2); return;
        }
        if (Word_TEXT(ingoa_taimau, "동작맡기기") && Word_TEXT(서술상수, "(LReo_Māori/자체/동작받이;)V")) {
            int 받이 = 빼기(2), huānga_uara = 빼기(2);
            if (화면객체(huānga_uara)) { 힙[huānga_uara + 4] = 받이; 힙참조[huānga_uara + 4] = 1; 힙[huānga_uara + 12] = 1; } return;
        }
        if (Word_TEXT(ingoa_taimau, "tāpiri_huānga") && Word_TEXT(서술상수, "(LReo_Māori/자체/화면구성요소;)V")) {
            int tamaiti_uara = 빼기(2), 부모 = 빼기(2); if (!화면객체(tamaiti_uara) || !화면객체(부모)) return;
            if (kaiwhakamahi.화면연결(2, 힙[부모 + 2], 힙[tamaiti_uara + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[tamaiti_uara + 11] = 부모; 힙참조[tamaiti_uara + 11] = 1; return;
        }
        if (Word_TEXT(ingoa_taimau, "자리정하기") && Word_TEXT(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), Poutū_tūranga = 빼기(1), 가로 = 빼기(1), huānga_uara = 빼기(2); if (!화면객체(huānga_uara)) return;
            if (kaiwhakamahi.화면연결(1, 힙[huānga_uara + 2], 가로, Poutū_tūranga, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[huānga_uara + 5] = 가로; 힙[huānga_uara + 6] = Poutū_tūranga; 힙[huānga_uara + 7] = 폭; 힙[huānga_uara + 8] = 높이; return;
        }
        if ((Word_TEXT(ingoa_taimau, "whakaatu_matapihi") || Word_TEXT(ingoa_taimau, "Kati")) && Word_TEXT(서술상수, "()V")) {
            boolean aritanga_uara = Word_TEXT(ingoa_taimau, "whakaatu_matapihi"); int huānga_uara = 빼기(2); if (!화면객체(huānga_uara)) return;
            if (kaiwhakamahi.화면연결(aritanga_uara ? 3 : 4, 힙[huānga_uara + 2], aritanga_uara ? 1 : 0, 0, 0, 0) < 0) { rahunga_uara("화면은 pāhekoheko 명령에서 실행해야 합니다"); return; }
            힙[huānga_uara + 9] = aritanga_uara ? 1 : 0; return;
        }
        if (Word_TEXT(ingoa_taimau, "보이는가") && Word_TEXT(서술상수, "()Z")) { int huānga_uara = 빼기(2); if (화면객체(huānga_uara)) 넣기(힙[huānga_uara + 9], 1); return; }
        rahunga_uara("지원하지 않는 Reo_Māori 화면 aratuka_uara");
    }
    static void 화면호출(int kaipupuri, int ingoa_taimau, int 서술상수, int tono_CODE) {
        if (Word_TEXT(kaipupuri, "javax/swing/SwingUtilities")) {
            if (tono_CODE == 184 && Word_TEXT(ingoa_taimau, "invokeLater") && Word_TEXT(서술상수, "(Ljava/lang/Runnable;)V")) { int ahanoa_Pūranga_kōrero = 빼기(2); if (!객체유효(ahanoa_Pūranga_kōrero)) return; if (나중수 == 8) { rahunga_uara("invokeLater queue full"); return; } 나중실행[나중수++] = ahanoa_Pūranga_kōrero; return; }
            if (tono_CODE == 184 && Word_TEXT(ingoa_taimau, "isEventDispatchThread") && Word_TEXT(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            rahunga_uara("unsupported SwingUtilities method"); return;
        }
        if (Word_TEXT(kaipupuri, "java/awt/event/ActionEvent")) {
            int ahanoa_Pūranga_kōrero = 빼기(2); if (!ahanoa_uara(ahanoa_Pūranga_kōrero, 29)) return;
            if (Word_TEXT(ingoa_taimau, "getSource") && Word_TEXT(서술상수, "()Ljava/lang/Object;")) 넣기(힙[ahanoa_Pūranga_kōrero + 2], 2);
            else if (Word_TEXT(ingoa_taimau, "getActionCommand") && Word_TEXT(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[ahanoa_Pūranga_kōrero + 2]), 2);
            else if (Word_TEXT(ingoa_taimau, "getID") && Word_TEXT(서술상수, "()I")) 넣기(1001, 1);
            else rahunga_uara("unsupported ActionEvent method"); return;
        }
        if (tono_CODE == 183 && Word_TEXT(ingoa_taimau, "<init>")) {
            int COLUMNS = 0, TEXT_Pūranga_kōrero = 0;
            if (Word_TEXT(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_TEXT(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); TEXT_Pūranga_kōrero = 빼기(2); }
            else if (Word_TEXT(서술상수, "(Ljava/lang/String;)V")) TEXT_Pūranga_kōrero = 빼기(2);
            else if (Word_TEXT(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_TEXT(서술상수, "()V")) { rahunga_uara("unsupported Swing constructor"); return; }
            int ahanoa_Pūranga_kōrero = 빼기(2); if (!객체유효(ahanoa_Pūranga_kōrero)) return;
            if (힙[ahanoa_Pūranga_kōrero] == 30) { rahunga_uara("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(ahanoa_Pūranga_kōrero) || COLUMNS < 0) return;
            int pūkete_uara = kaiwhakamahi.화면연결(0, 힙[ahanoa_Pūranga_kōrero] - 23, 0, 0, 0, 0);
            if (pūkete_uara < 1 || pūkete_uara > 32) { rahunga_uara("GUI widget slots exhausted"); return; }
            힙[ahanoa_Pūranga_kōrero + 2] = pūkete_uara; 화면참조[pūkete_uara - 1] = ahanoa_Pūranga_kōrero; 힙[ahanoa_Pūranga_kōrero + 5] = 힙[ahanoa_Pūranga_kōrero] == 24 ? 130 : 16; 힙[ahanoa_Pūranga_kōrero + 6] = 힙[ahanoa_Pūranga_kōrero] == 24 ? 110 : 16;
            힙[ahanoa_Pūranga_kōrero + 7] = 힙[ahanoa_Pūranga_kōrero] == 24 ? 380 : 220; 힙[ahanoa_Pūranga_kōrero + 8] = 힙[ahanoa_Pūranga_kōrero] == 24 ? 240 : 28; 힙[ahanoa_Pūranga_kōrero + 10] = 1;
            화면문자설정(ahanoa_Pūranga_kōrero, TEXT_Pūranga_kōrero); return;
        }
        if (Word_TEXT(ingoa_taimau, "setText") || Word_TEXT(ingoa_taimau, "setTitle")) { int TEXT_Pūranga_kōrero = 빼기(2), ahanoa_Pūranga_kōrero = 빼기(2); if (화면객체(ahanoa_Pūranga_kōrero) && Word_TEXT(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(ahanoa_Pūranga_kōrero, TEXT_Pūranga_kōrero); return; }
        if (Word_TEXT(ingoa_taimau, "getText") || Word_TEXT(ingoa_taimau, "getTitle")) { int ahanoa_Pūranga_kōrero = 빼기(2); if (화면객체(ahanoa_Pūranga_kōrero) && Word_TEXT(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(ahanoa_Pūranga_kōrero), 2); return; }
        if (Word_TEXT(ingoa_taimau, "addActionListener") && Word_TEXT(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), ahanoa_Pūranga_kōrero = 빼기(2); if (화면객체(ahanoa_Pūranga_kōrero)) { 힙[ahanoa_Pūranga_kōrero + 4] = 수신참조; 힙참조[ahanoa_Pūranga_kōrero + 4] = 1; } return; }
        if (Word_TEXT(ingoa_taimau, "getContentPane") && Word_TEXT(서술상수, "()Ljava/awt/Container;")) { int ahanoa_Pūranga_kōrero = 빼기(2); if (화면객체(ahanoa_Pūranga_kōrero)) 넣기(ahanoa_Pūranga_kōrero, 2); return; }
        if (Word_TEXT(ingoa_taimau, "setLayout") && Word_TEXT(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Tahora_Pūranga_kōrero = 빼기(2), ahanoa_Pūranga_kōrero = 빼기(2); if (화면객체(ahanoa_Pūranga_kōrero) && Tahora_Pūranga_kōrero != 0) rahunga_uara("only absolute layout (null) is supported"); return; }
        if (Word_TEXT(ingoa_taimau, "add") && (Word_TEXT(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_TEXT(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Tahora_here = Word_TEXT(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Tahora_here) 빼기(2);
            int tamaiti_Pūranga_kōrero = 빼기(2), ahanoa_Pūranga_kōrero = 빼기(2); if (!화면객체(tamaiti_Pūranga_kōrero) || !화면객체(ahanoa_Pūranga_kōrero)) return;
            if (kaiwhakamahi.화면연결(2, 힙[ahanoa_Pūranga_kōrero + 2], 힙[tamaiti_Pūranga_kōrero + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[tamaiti_Pūranga_kōrero + 11] = ahanoa_Pūranga_kōrero; 힙참조[tamaiti_Pūranga_kōrero + 11] = 1; if (!Tahora_here) 넣기(tamaiti_Pūranga_kōrero, 2); return;
        }
        if (Word_TEXT(ingoa_taimau, "setBounds") && Word_TEXT(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), taunga_x = 빼기(1), ahanoa_Pūranga_kōrero = 빼기(2); if (!화면객체(ahanoa_Pūranga_kōrero)) return;
            if (kaiwhakamahi.화면연결(1, 힙[ahanoa_Pūranga_kōrero + 2], taunga_x, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[ahanoa_Pūranga_kōrero + 5] = taunga_x; 힙[ahanoa_Pūranga_kōrero + 6] = 세로좌표; 힙[ahanoa_Pūranga_kōrero + 7] = 너비; 힙[ahanoa_Pūranga_kōrero + 8] = 높이; return;
        }
        if (Word_TEXT(ingoa_taimau, "setSize") && Word_TEXT(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), ahanoa_Pūranga_kōrero = 빼기(2); if (!화면객체(ahanoa_Pūranga_kōrero)) return;
            if (kaiwhakamahi.화면연결(1, 힙[ahanoa_Pūranga_kōrero + 2], 힙[ahanoa_Pūranga_kōrero + 5], 힙[ahanoa_Pūranga_kōrero + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[ahanoa_Pūranga_kōrero + 7] = 너비; 힙[ahanoa_Pūranga_kōrero + 8] = 높이; } return;
        }
        if (Word_TEXT(ingoa_taimau, "setLocationRelativeTo") && Word_TEXT(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), ahanoa_Pūranga_kōrero = 빼기(2); if (!화면객체(ahanoa_Pūranga_kōrero)) return; if (상대배치 != 0) { rahunga_uara("only screen centering supported"); return; } 힙[ahanoa_Pūranga_kōrero + 5] = (kaiwhakamahi.화면너비() - 힙[ahanoa_Pūranga_kōrero + 7]) / 2; 힙[ahanoa_Pūranga_kōrero + 6] = (kaiwhakamahi.화면높이() - 힙[ahanoa_Pūranga_kōrero + 8]) / 2; kaiwhakamahi.화면연결(1, 힙[ahanoa_Pūranga_kōrero + 2], 힙[ahanoa_Pūranga_kōrero + 5], 힙[ahanoa_Pūranga_kōrero + 6], 힙[ahanoa_Pūranga_kōrero + 7], 힙[ahanoa_Pūranga_kōrero + 8]); return; }
        if (Word_TEXT(ingoa_taimau, "setDefaultCloseOperation") && Word_TEXT(서술상수, "(I)V")) { int kaupapahere = 빼기(1), ahanoa_Pūranga_kōrero = 빼기(2); if (화면객체(ahanoa_Pūranga_kōrero)) { if (kaupapahere < 0 || kaupapahere > 3) 예외던짐(9, "close policy"); else { 힙[ahanoa_Pūranga_kōrero + 10] = kaupapahere; kaiwhakamahi.화면연결(7, 힙[ahanoa_Pūranga_kōrero + 2], kaupapahere, 0, 0, 0); } } return; }
        if (Word_TEXT(ingoa_taimau, "setVisible") && Word_TEXT(서술상수, "(Z)V")) { int raraunga_uara = 빼기(1), ahanoa_Pūranga_kōrero = 빼기(2); if (화면객체(ahanoa_Pūranga_kōrero)) { int 처리값 = kaiwhakamahi.화면연결(3, 힙[ahanoa_Pūranga_kōrero + 2], raraunga_uara, 0, 0, 0); if (처리값 < 0) rahunga_uara("Swing requires a standalone interactive command"); else 힙[ahanoa_Pūranga_kōrero + 9] = raraunga_uara; } return; }
        if (Word_TEXT(ingoa_taimau, "dispose") && Word_TEXT(서술상수, "()V")) { int ahanoa_Pūranga_kōrero = 빼기(2); if (화면객체(ahanoa_Pūranga_kōrero)) { kaiwhakamahi.화면연결(4, 힙[ahanoa_Pūranga_kōrero + 2], 0, 0, 0, 0); 힙[ahanoa_Pūranga_kōrero + 9] = 0; } return; }
        if (Word_TEXT(ingoa_taimau, "repaint") || Word_TEXT(ingoa_taimau, "validate")) { int ahanoa_Pūranga_kōrero = 빼기(2); if (!화면객체(ahanoa_Pūranga_kōrero) || !Word_TEXT(서술상수, "()V")) return; kaiwhakamahi.화면연결(1, 힙[ahanoa_Pūranga_kōrero + 2], 힙[ahanoa_Pūranga_kōrero + 5], 힙[ahanoa_Pūranga_kōrero + 6], 힙[ahanoa_Pūranga_kōrero + 7], 힙[ahanoa_Pūranga_kōrero + 8]); return; }
        if (Word_TEXT(ingoa_taimau, "isVisible") && Word_TEXT(서술상수, "()Z")) { int ahanoa_Pūranga_kōrero = 빼기(2); if (화면객체(ahanoa_Pūranga_kōrero)) 넣기(힙[ahanoa_Pūranga_kōrero + 9], 1); return; }
        rahunga_uara("unsupported Swing method (native subset)");
    }
    static void 사건실행(int ūnga_ADDRESS, int 사건번호, boolean Reo_Māori) {
        if (ūnga_ADDRESS < 1 || 힙[ūnga_ADDRESS] < 32) { rahunga_uara("Java event listener required"); return; }
        int kōnae_INDEX = ingoa_aratuka(힙[ūnga_ADDRESS] - 32, 사건번호 == 0 ? (Reo_Māori ? "kawe_tūmahi" : "run") : (Reo_Māori ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (Reo_Māori ? "(LReo_Māori/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (kōnae_INDEX < 0) { rahunga_uara("event callback missing"); return; }
        현재가닥 = 0; miro_COUNT = 1; tāpare_INDEX = 0; miro_tūnga[0] = 1; tāpare_Huinga[0] = 0; 틀잠금[0] = arawhiti_tāpare[0] = 0; 바꿈요청 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { paetata_uara[Loop_INDEX] = paetata_TYPE[Loop_INDEX] = 0; }
        tāpare_aratuka[0] = kōnae_INDEX; tāpare_tūranga[0] = aratuka_Start[kōnae_INDEX]; paetata_uara[0] = ūnga_ADDRESS; paetata_TYPE[0] = 2;
        if (사건번호 != 0) { paetata_uara[1] = 사건번호; paetata_TYPE[1] = 2; }
        사건중 = true; kawe_tono(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!Pōhēhē) {
            if (나중수 > 0) { int ūnga_ADDRESS = 나중실행[0], Reo_Māori = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(ūnga_ADDRESS, 0, Reo_Māori != 0); continue; }
            if (kaiwhakamahi.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = kaiwhakamahi.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { rahunga_uara("GUI event I/O failed"); return; }
            int pūkete_uara = 사건번호 & 65535; if (pūkete_uara < 1 || pūkete_uara > 32) continue; int ahanoa_Pūranga_kōrero = 화면참조[pūkete_uara - 1]; if (ahanoa_Pūranga_kōrero == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[ahanoa_Pūranga_kōrero + 10] != 0) 힙[ahanoa_Pūranga_kōrero + 9] = 0;
                if (힙[ahanoa_Pūranga_kōrero + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && 힙[화면참조[Loop_INDEX]] == 24) kaiwhakamahi.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[ahanoa_Pūranga_kōrero + 4] != 0) {
                int PĀNUIMAI_Pūranga_kōrero = tiritiri_Rokiroki(29, 2); if (Pōhēhē) return; 힙[PĀNUIMAI_Pūranga_kōrero + 2] = ahanoa_Pūranga_kōrero; 힙[PĀNUIMAI_Pūranga_kōrero + 3] = 힙[ahanoa_Pūranga_kōrero + 12]; 힙참조[PĀNUIMAI_Pūranga_kōrero + 2] = 1; 사건실행(힙[ahanoa_Pūranga_kōrero + 4], PĀNUIMAI_Pūranga_kōrero, 힙[ahanoa_Pūranga_kōrero + 12] != 0);
            }
        }
    }
    public static int whakahaere() {
        if (kaiwhakamahi.인수개수() == 1 && 자바도구.같음(kaiwhakamahi.인수(0), "-version")) {
            kaiwhakamahi.Tuhia("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (kaiwhakamahi.인수개수() < 1) { kaiwhakamahi.Tuhia("Usage: java CLASS [ARGS]\n"); return 2; }
        tāurunga_tauaha_Whakamāramatanga = uta_tauaha_Whakamāramatanga(taurima_pūāhua(kaiwhakamahi.인수(0))); if (Pōhēhē || tāurunga_tauaha_Whakamāramatanga < 0) return 1;
        int tāurunga_ira_uara = ingoa_aratuka(tāurunga_tauaha_Whakamāramatanga, "whakahaere", "()V");
        boolean 한국어진입 = tāurunga_ira_uara >= 0 && (aratuka_uru[tāurunga_ira_uara] & 9) == 9;
        if (!한국어진입) tāurunga_ira_uara = ingoa_aratuka(tāurunga_tauaha_Whakamāramatanga, "main", "([Ljava/lang/String;)V");
        if (tāurunga_ira_uara < 0 || (aratuka_uru[tāurunga_ira_uara] & 9) != 9) rahunga_uara("public static void whakahaere() or main(String[] args) required");
        if (Pōhēhē) return 1;
        int 인수 = tiritiri_Rokiroki(3, kaiwhakamahi.인수개수() - 1); HUĀNGA_huānga[인수] = -1;
        for (int 수 = 1; 수 < kaiwhakamahi.인수개수() && !Pōhēhē; 수++) 힙[인수 + 1 + 수] = taurima_pūāhua(kaiwhakamahi.인수(수));
        tāpare_INDEX = 0; tāpare_aratuka[0] = tāurunga_ira_uara; tāpare_tūranga[0] = aratuka_Start[tāurunga_ira_uara]; paetata_uara[0] = 한국어진입 ? 0 : 인수; paetata_TYPE[0] = 한국어진입 ? 0 : 2;
        miro_tūnga[0] = 1; miro_ahanoa[0] = tiritiri_Rokiroki(13, 2);
        kawe_tono(); if (!Pōhēhē) 화면사건들(); return Pōhēhē ? 1 : 0;
    }
}
