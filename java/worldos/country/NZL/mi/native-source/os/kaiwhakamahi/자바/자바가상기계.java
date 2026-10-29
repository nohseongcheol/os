// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Kōnae/스택/Pūranga_kōrero/peka 경계를 kawe_tono 중 검사한다. */
public final class 자바가상기계 {
    static int[] Kōnae = new int[16384], kōnae_ingoa_TEXT = new int[64];
    static int[] taimau_tūtohu = new int[512], 상가 = new int[512], taimau_SECOND_uara = new int[512], aho_Pūranga_kōrero = new int[512];
    static int[] aratuka_ingoa_TEXT = new int[32], aratuka_TYPE = new int[32], aratuka_uru = new int[32];
    static int[] aratuka_Start = new int[32], aratuka_mutu = new int[32], aratuka_Huinga = new int[32], 함수지역 = new int[32];
    static int[] aratuka_tohenga_COUNT = new int[32], aratuka_tohenga_TYPE = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] paetata_uara = new int[4096], paetata_TYPE = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] tāpare_aratuka = new int[32], tāpare_tūranga = new int[32], tāpare_Huinga = new int[32];
    static int[] 힙 = new int[8192];
    static int rahi, 읽기위치, taimau_COUNT, aratuka_COUNT, tauaha_ingoa, tāpare_INDEX = -1, 힙끝 = 1, 반환형;
    static boolean Pōhēhē;

    static void rahunga_uara(String Word_TEXT) {
        if (!Pōhēhē) { kaiwhakamahi.Tuhia("JVM error: "); kaiwhakamahi.Tuhia(Word_TEXT); kaiwhakamahi.tuhi_pūāhua_uara(10); }
        Pōhēhē = true;
    }
    static boolean topenga(int whakahaere, int roa_uara) { return whakahaere >= 0 && roa_uara >= 0 && whakahaere <= rahi - roa_uara; }
    static int paita_uara() {
        if (!topenga(읽기위치, 1)) { rahunga_uara("truncated class file"); return 0; }
        return Kōnae[읽기위치++];
    }
    static int 짧은수() { return paita_uara() << 8 | paita_uara(); }
    static int tau_tōpū() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int roa_uara) { if (!topenga(읽기위치, roa_uara)) rahunga_uara("invalid attribute size"); else 읽기위치 += roa_uara; }
    static boolean taki_taimau(int 수, int 종류) {
        if (수 <= 0 || 수 >= taimau_COUNT || taimau_tūtohu[수] != 종류) { rahunga_uara("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int whakahaere, int roa_uara, String Word_TEXT) {
        if (!topenga(whakahaere, roa_uara) || roa_uara != Word_TEXT.length()) return false;
        for (int 수 = 0; 수 < roa_uara; 수++) if (Kōnae[whakahaere + 수] != Word_TEXT.charAt(수)) return false;
        return true;
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
    static void 속성건너() {
        int tuemi_COUNT = 짧은수();
        for (int 수 = 0; 수 < tuemi_COUNT && !Pōhēhē; 수++) { taki_taimau(짧은수(), 1); 건너(tau_tōpū()); }
    }
    static int tono_roa(int uara) {
        if (uara == 16 || uara == 18 || uara == 21 || uara == 25 || uara == 54 || uara == 58 || uara == 188) return 2;
        if (uara == 17 || uara == 19 || uara == 132 || uara >= 153 && uara <= 167
            || uara >= 178 && uara <= 184 || uara == 187 || uara == 189 || uara == 192 || uara == 198 || uara == 199) return 3;
        if (uara >= 0 && uara <= 8 || uara >= 26 && uara <= 29 || uara >= 42 && uara <= 46 || uara == 50
            || uara >= 59 && uara <= 62 || uara >= 75 && uara <= 79 || uara == 83 || uara == 87 || uara == 89 || uara == 95
            || uara == 96 || uara == 100 || uara == 104 || uara == 108 || uara == 112 || uara == 116
            || uara == 120 || uara == 122 || uara == 124 || uara == 126 || uara == 128 || uara == 130
            || uara >= 145 && uara <= 147 || uara == 172 || uara == 176 || uara == 177 || uara == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (tau_tōpū() != 0xcafebabe) rahunga_uara("not a class file");
        int 부판 = 짧은수(), putanga_uara = 짧은수();
        if (putanga_uara < 45 || putanga_uara > 52 || 부판 != 0) rahunga_uara("supported class versions: 45..52, minor 0");
        taimau_COUNT = 짧은수();
        if (taimau_COUNT < 1 || taimau_COUNT > 512) { rahunga_uara("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < taimau_COUNT && !Pōhēhē; 수++) {
            int 종류 = paita_uara(); taimau_tūtohu[수] = 종류;
            if (종류 == 1) { taimau_SECOND_uara[수] = 짧은수(); 상가[수] = 읽기위치; 건너(taimau_SECOND_uara[수]); }
            else if (종류 == 3) 상가[수] = tau_tōpū();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); taimau_SECOND_uara[수] = 짧은수(); }
            else rahunga_uara("unsupported constant type");
        }
        int mana_uru_uara = 짧은수();
        if ((mana_uru_uara & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) rahunga_uara("unsupported class flags");
        tauaha_ingoa = tauaha_ingoa_TEXT(짧은수());
        if (!Word_TEXT(tauaha_ingoa_TEXT(짧은수()), "java/lang/Object")) rahunga_uara("inheritance unsupported");
        if (짧은수() != 0) rahunga_uara("interfaces unsupported");
        if (짧은수() != 0) rahunga_uara("fields unsupported");
        aratuka_COUNT = 짧은수();
        if (aratuka_COUNT < 1 || aratuka_COUNT > 32) { rahunga_uara("method count limit (32)"); return; }
        for (int 수 = 0; 수 < aratuka_COUNT && !Pōhēhē; 수++) {
            aratuka_uru[수] = 짧은수(); aratuka_ingoa_TEXT[수] = 짧은수(); aratuka_TYPE[수] = 짧은수();
            taki_taimau(aratuka_ingoa_TEXT[수], 1); 서술읽기(수);
            if ((aratuka_uru[수] & (0x100 | 0x400 | 0x20)) != 0) rahunga_uara("native, abstract and synchronized methods unsupported");
            if ((aratuka_uru[수] & 8) == 0 && !Word_TEXT(aratuka_ingoa_TEXT[수], "<init>")) rahunga_uara("instance methods unsupported");
            if (Word_TEXT(aratuka_ingoa_TEXT[수], "<clinit>")) rahunga_uara("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(aratuka_ingoa_TEXT[앞], aratuka_ingoa_TEXT[수]) && 같은말(aratuka_TYPE[앞], aratuka_TYPE[수])) rahunga_uara("duplicate method");
            int tuemi_COUNT = 짧은수();
            for (int huanga_uara = 0; huanga_uara < tuemi_COUNT && !Pōhēhē; huanga_uara++) {
                int Ingoa = 짧은수(), roa_uara = tau_tōpū(), whakahaere = 읽기위치;
                if (!topenga(whakahaere, roa_uara)) { rahunga_uara("truncated method attribute"); break; }
                if (Word_TEXT(Ingoa, "Code")) {
                    if (aratuka_Start[수] != 0) rahunga_uara("duplicate Code attribute");
                    aratuka_Huinga[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_roa = tau_tōpū();
                    if (aratuka_Huinga[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < aratuka_tohenga_COUNT[수]
                        || CODE_roa < 1 || CODE_roa > 8192) rahunga_uara("method memory limits exceeded");
                    aratuka_Start[수] = 읽기위치; 건너(CODE_roa); aratuka_mutu[수] = 읽기위치;
                    if (짧은수() != 0) rahunga_uara("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != whakahaere + roa_uara) rahunga_uara("Code attribute size mismatch");
                } else 건너(roa_uara);
            }
            if (aratuka_Start[수] == 0) rahunga_uara("missing Code attribute");
            int kāniwha_tāurunga = aratuka_Start[수];
            while (kāniwha_tāurunga < aratuka_mutu[수] && !Pōhēhē) {
                int roa_uara = tono_roa(Kōnae[kāniwha_tāurunga]);
                if (roa_uara == 0 || roa_uara > aratuka_mutu[수] - kāniwha_tāurunga) { rahunga_uara("unsupported or truncated bytecode"); break; }
                경계[kāniwha_tāurunga] = 수 + 1; kāniwha_tāurunga += roa_uara;
            }
            // 실행하지 않는 경로에도 잘못된 peka 목적지를 허용하지 않는다.
            kāniwha_tāurunga = aratuka_Start[수];
            while (kāniwha_tāurunga < aratuka_mutu[수] && !Pōhēhē) {
                int uara = Kōnae[kāniwha_tāurunga];
                if (uara >= 153 && uara <= 167 || uara == 198 || uara == 199) {
                    int ūnga_uara = kāniwha_tāurunga + (short)(Kōnae[kāniwha_tāurunga + 1] << 8 | Kōnae[kāniwha_tāurunga + 2]);
                    if (ūnga_uara < aratuka_Start[수] || ūnga_uara >= aratuka_mutu[수] || 경계[ūnga_uara] != 수 + 1) rahunga_uara("invalid branch target");
                }
                kāniwha_tāurunga += tono_roa(uara);
            }
        }
        if (!Pōhēhē) 속성건너();
        if (읽기위치 != rahi) rahunga_uara("extra class file data");
    }
    static int tiritiri_Rokiroki(int 종류, int roa_uara) {
        if (roa_uara < 0 || roa_uara > 힙.length - 힙끝 - 2) { rahunga_uara("object heap exhausted or negative array size"); return 0; }
        int Pūranga_kōrero = 힙끝; 힙끝 += roa_uara + 2; 힙[Pūranga_kōrero] = 종류; 힙[Pūranga_kōrero + 1] = roa_uara;
        return Pūranga_kōrero;
    }
    static boolean ahanoa_uara(int Pūranga_kōrero, int 종류) {
        if (Pūranga_kōrero < 1 || Pūranga_kōrero >= 힙끝 - 1 || 힙[Pūranga_kōrero] != 종류) { rahunga_uara("null or invalid object reference"); return false; }
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
        if (tāpare_INDEX == 31) { rahunga_uara("call stack limit (32)"); return; }
        int Panuku_tuemi = tāpare_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) paetata_TYPE[Panuku_tuemi * 128 + 수] = 0;
        for (int 수 = aratuka_tohenga_COUNT[TAUMAHI_uara] - 1; 수 >= 0; 수--) {
            paetata_uara[Panuku_tuemi * 128 + 수] = 빼기(aratuka_tohenga_TYPE[TAUMAHI_uara * 16 + 수]); paetata_TYPE[Panuku_tuemi * 128 + 수] = aratuka_tohenga_TYPE[TAUMAHI_uara * 16 + 수];
        }
        tāpare_INDEX = Panuku_tuemi; tāpare_aratuka[tāpare_INDEX] = TAUMAHI_uara; tāpare_tūranga[tāpare_INDEX] = aratuka_Start[TAUMAHI_uara]; tāpare_Huinga[tāpare_INDEX] = 0;
    }
    static void 반환(int TYPE_uara) {
        if (TYPE_uara != 함수반환[tāpare_aratuka[tāpare_INDEX]]) { rahunga_uara("return type mismatch"); return; }
        int uara = TYPE_uara == 0 ? 0 : 빼기(TYPE_uara);
        tāpare_INDEX--; if (tāpare_INDEX >= 0 && TYPE_uara != 0) 넣기(uara, TYPE_uara);
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
                if (uara < 1 || uara > 127) { rahunga_uara("file stream paths currently require ASCII"); return; }
                roma_kōnae_ingoa[kāniwha_tāurunga] = uara;
            }
            roma_kōnae_ingoa[roa_uara] = 0;
            int 서술자 = kaiwhakamahi.파일서술자열기(roma_kōnae_ingoa, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { rahunga_uara("FileNotFoundException: file open failed"); return; }
            힙[roma_uara + 2] = 서술자; 힙[roma_uara + 3] = 1;
            return;
        }
        if (tono != 182) { rahunga_uara("invalid file stream invocation"); return; }
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
            if (mēhua < -1) rahunga_uara("IOException: read failed"); else 넣기(mēhua, 1);
        } else if (kaiwhakamahi.파일한바이트쓰기(서술자, uara) != 1) rahunga_uara("IOException: write failed");
    }
    static void CALL_aratuka(int INDEX, int tono) {
        if (!taki_taimau(INDEX, 10)) return;
        int kaipupuri_uara = tauaha_ingoa_TEXT(상가[INDEX]), Ingoa = Pūranga_kōrero_ingoa(taimau_SECOND_uara[INDEX]), hōputu_uara = Pūranga_kōrero_TYPE(taimau_SECOND_uara[INDEX]);
        if (Pōhēhē) return;
        if (같은말(kaipupuri_uara, tauaha_ingoa)) {
            if (tono != 184) { rahunga_uara("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < aratuka_COUNT; 수++) if (같은말(Ingoa, aratuka_ingoa_TEXT[수]) && 같은말(hōputu_uara, aratuka_TYPE[수])) {
                if ((aratuka_uru[수] & 8) == 0) rahunga_uara("method is not static"); else 호출(수);
                return;
            }
            rahunga_uara("NoSuchMethodError"); return;
        }
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
        rahunga_uara("unsupported library method");
    }
    static int HUĀNGA_kāniwha(int Pūranga_kōrero, int hauraro_uara, int TYPE_uara) {
        if (!ahanoa_uara(Pūranga_kōrero, TYPE_uara)) return 0;
        if (hauraro_uara < 0 || hauraro_uara >= 힙[Pūranga_kōrero + 1]) { rahunga_uara("ArrayIndexOutOfBoundsException"); return 0; }
        return Pūranga_kōrero + 2 + hauraro_uara;
    }
    static void kawe_tono() {
        int 남음 = 500000;
        while (tāpare_INDEX >= 0 && !Pōhēhē) {
            if (--남음 == 0) { rahunga_uara("instruction limit (500000)"); break; }
            int whakahaere = tāpare_tūranga[tāpare_INDEX], uara = 명바();
            if (Pōhēhē) break;
            if (uara == 0) continue;
            if (uara == 1) { 넣기(0, 2); continue; }
            if (uara >= 2 && uara <= 8) { 넣기(uara - 3, 1); continue; }
            if (uara == 16) { 넣기((byte)명바(), 1); continue; }
            if (uara == 17) { 넣기((short)명짧(), 1); continue; }
            if (uara == 18 || uara == 19) {
                int 수 = uara == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= taimau_COUNT) rahunga_uara("invalid ldc constant");
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
            if (uara == 46 || uara == 50) {
                int hauraro_uara = 빼기(1), Pūranga_kōrero = 빼기(2), kāniwha_tāurunga = HUĀNGA_kāniwha(Pūranga_kōrero, hauraro_uara, uara == 46 ? 2 : 3);
                if (!Pōhēhē) 넣기(힙[kāniwha_tāurunga], uara == 46 ? 1 : 2); continue;
            }
            if (uara == 79 || uara == 83) {
                int tuemi_huānga = 빼기(uara == 79 ? 1 : 2), hauraro_uara = 빼기(1), Pūranga_kōrero = 빼기(2), kāniwha_tāurunga = HUĀNGA_kāniwha(Pūranga_kōrero, hauraro_uara, uara == 79 ? 2 : 3);
                if (uara == 83 && tuemi_huānga != 0) ahanoa_uara(tuemi_huānga, 1);
                if (!Pōhēhē) 힙[kāniwha_tāurunga] = tuemi_huānga; continue;
            }
            if (uara == 87) { 빼기(0); continue; }
            if (uara == 89) { int 가 = 빼기(0), TYPE_uara = 반환형; 넣기(가, TYPE_uara); 넣기(가, TYPE_uara); continue; }
            if (uara == 95) { int 가 = 빼기(0), 가형 = 반환형, 나 = 빼기(0), 나형 = 반환형; 넣기(가, 가형); 넣기(나, 나형); continue; }
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
            if (uara == 178) {
                int 수 = 명짧(); if (!taki_taimau(수, 9)) continue;
                if (!Word_TEXT(tauaha_ingoa_TEXT(상가[수]), "java/lang/System") || !Word_TEXT(Pūranga_kōrero_ingoa(taimau_SECOND_uara[수]), "out")
                    || !Word_TEXT(Pūranga_kōrero_TYPE(taimau_SECOND_uara[수]), "Ljava/io/PrintStream;")) rahunga_uara("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (uara == 182 || uara == 183 || uara == 184) { CALL_aratuka(명짧(), uara); continue; }
            if (uara == 187) {
                int Ingoa = tauaha_ingoa_TEXT(명짧());
                if (Word_TEXT(Ingoa, "java/lang/StringBuilder")) 넣기(tiritiri_Rokiroki(4, 1), 2);
                else if (Word_TEXT(Ingoa, "java/io/FileInputStream") || Word_TEXT(Ingoa, "java/io/FileOutputStream")) {
                    int Pūranga_kōrero = tiritiri_Rokiroki(Word_TEXT(Ingoa, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!Pōhēhē) { 힙[Pūranga_kōrero + 2] = -1; 넣기(Pūranga_kōrero, 2); }
                } else rahunga_uara("unsupported object construction");
                continue;
            }
            if (uara == 188 || uara == 189) {
                if (uara == 188) { if (명바() != 10) rahunga_uara("only int[] newarray is supported"); }
                else if (!Word_TEXT(tauaha_ingoa_TEXT(명짧()), "java/lang/String")) rahunga_uara("only String[] anewarray is supported");
                int roa_uara = 빼기(1); 넣기(tiritiri_Rokiroki(uara == 188 ? 2 : 3, roa_uara), 2); continue;
            }
            if (uara == 190) {
                int Pūranga_kōrero = 빼기(2);
                if (Pūranga_kōrero < 1 || Pūranga_kōrero >= 힙끝 - 1 || (힙[Pūranga_kōrero] != 2 && 힙[Pūranga_kōrero] != 3)) rahunga_uara("null or invalid array");
                else 넣기(힙[Pūranga_kōrero + 1], 1); continue;
            }
            if (uara == 192) {
                int Ingoa = tauaha_ingoa_TEXT(명짧()), Pūranga_kōrero = 빼기(2);
                if (!Word_TEXT(Ingoa, "java/lang/String")) rahunga_uara("unsupported checkcast");
                else if (Pūranga_kōrero != 0) ahanoa_uara(Pūranga_kōrero, 1);
                넣기(Pūranga_kōrero, 2); continue;
            }
            rahunga_uara("unsupported bytecode");
        }
    }
    public static int whakahaere() {
        if (kaiwhakamahi.인수개수() == 1 && 자바도구.같음(kaiwhakamahi.인수(0), "-version")) {
            kaiwhakamahi.Tuhia("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (kaiwhakamahi.인수개수() < 1) { kaiwhakamahi.Tuhia("Usage: java CLASS [ARGS]\n"); return 2; }
        int roa_uara = 자바도구.Ingoa(kōnae_ingoa_TEXT, kaiwhakamahi.인수(0));
        if (roa_uara < 1 || roa_uara > 57) { kaiwhakamahi.Tuhia("java: invalid class name\n"); return 2; }
        kōnae_ingoa_TEXT[roa_uara] = '.'; kōnae_ingoa_TEXT[roa_uara + 1] = 'c'; kōnae_ingoa_TEXT[roa_uara + 2] = 'l'; kōnae_ingoa_TEXT[roa_uara + 3] = 'a'; kōnae_ingoa_TEXT[roa_uara + 4] = 's'; kōnae_ingoa_TEXT[roa_uara + 5] = 's';
        rahi = kaiwhakamahi.파일읽기(kōnae_ingoa_TEXT, Kōnae);
        if (rahi < 0) { kaiwhakamahi.Tuhia("java: cannot read class: "); 자바도구.수쓰기(rahi); kaiwhakamahi.tuhi_pūāhua_uara(10); return 1; }
        클래스읽기(); if (Pōhēhē) return 1;
        int pūāhua_ingoa = taimau_TEXT(tauaha_ingoa);
        if (!Pōhēhē && 힙[pūāhua_ingoa + 1] != roa_uara) rahunga_uara("class name does not match file");
        for (int 수 = 0; 수 < roa_uara && !Pōhēhē; 수++) if (힙[pūāhua_ingoa + 2 + 수] != kōnae_ingoa_TEXT[수]) rahunga_uara("class name does not match file");
        int tāurunga_ira_uara = -1;
        for (int 수 = 0; 수 < aratuka_COUNT; 수++) if (Word_TEXT(aratuka_ingoa_TEXT[수], "main") && Word_TEXT(aratuka_TYPE[수], "([Ljava/lang/String;)V") && (aratuka_uru[수] & 9) == 9) tāurunga_ira_uara = 수;
        if (tāurunga_ira_uara < 0) rahunga_uara("public static void main(String[] args) required");
        if (Pōhēhē) return 1;
        int 인수 = tiritiri_Rokiroki(3, kaiwhakamahi.인수개수() - 1);
        for (int 수 = 1; 수 < kaiwhakamahi.인수개수() && !Pōhēhē; 수++) 힙[인수 + 1 + 수] = taurima_pūāhua(kaiwhakamahi.인수(수));
        tāpare_INDEX = 0; tāpare_aratuka[0] = tāurunga_ira_uara; tāpare_tūranga[0] = aratuka_Start[tāurunga_ira_uara]; paetata_uara[0] = 인수; paetata_TYPE[0] = 2;
        kawe_tono(); return Pōhēhē ? 1 : 0;
    }
}
