// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. faili/스택/Marejeleo/tawi 경계를 tekeleza_amri 중 검사한다. */
public final class 자바가상기계 {
    static int[] faili = new int[16 * 16384], 임시파일 = new int[16384], faili_jina_SMS = new int[512];
    static int[] kisobadilika_lebo = new int[8192], 상가 = new int[8192], 상나 = new int[8192], tungo_Marejeleo = new int[8192];
    static int[] mbinu_jina_SMS = new int[512], mbinu_aina = new int[512], mbinu_fikia = new int[512], mbinu_mmiliki = new int[512];
    static int[] mbinu_Anza = new int[512], mbinu_tamatia = new int[512], mbinu_Mpororo = new int[512], 함수지역 = new int[512];
    static int[] 함수인수수 = new int[512], mbinu_hoja_aina = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] jirani_thamani = new int[16384], jirani_aina = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] fremu_mbinu = new int[128], 틀위치 = new int[128], fremu_Mpororo = new int[128], fremu_agizo = new int[128], anzilisha_fremu = new int[128];
    static int[] tabaka_Ufafanuzi_jina = new int[16], tabaka_Ufafanuzi_panga_ukubwa = new int[16], 종부모 = new int[16], tabaka_Ufafanuzi_hali = new int[16], 종칸수 = new int[16], anzilisha_tabaka_Ufafanuzi = new int[16];
    static int[] tabaka_kiolesura = new int[16 * 16], 종접면수 = new int[16];
    static int[] Sloti_jina = new int[512], Sloti_aina = new int[512], Sloti_mmiliki = new int[512], Sloti_Vibali = new int[512], 칸위치 = new int[512], Sloti_data = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], ARRAY_elementi = new int[32768], Store_namba_kamili = new int[256];
    static int panga_ukubwa, 읽기위치, 함수수, tabaka_jina, fremu_kielezo = -1, 힙끝 = 1, 반환형;
    static int 종수, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, 표시수, 수거횟수;
    static int 현재가닥, 가닥수 = 1, ingizo_tabaka_Ufafanuzi;
    static int[] mtungo_fremu = new int[4], mtungo_hali = new int[4], mtungo_kipengee = new int[4], mtungo_lengo = new int[4], 가닥대기 = new int[4];
    static boolean kosa, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], tabaka_mtungo = new int[16];

    static void kushindwa_thamani(String Neno_SMS) {
        if (kosa) return;
        int kategoria_msimbo = 0;
        if (자바도구.같음(Neno_SMS, "ArithmeticException: / by zero")) kategoria_msimbo = 4;
        if (자바도구.같음(Neno_SMS, "NullPointerException") || 자바도구.같음(Neno_SMS, "null or invalid array")) kategoria_msimbo = 5;
        if (자바도구.같음(Neno_SMS, "ArrayIndexOutOfBoundsException")) kategoria_msimbo = 7;
        if (자바도구.같음(Neno_SMS, "StringIndexOutOfBoundsException")) kategoria_msimbo = 8;
        if (자바도구.같음(Neno_SMS, "NumberFormatException")) kategoria_msimbo = 10;
        if (자바도구.같음(Neno_SMS, "FileNotFoundException: file open failed")) kategoria_msimbo = 12;
        if (자바도구.같음(Neno_SMS, "IOException: stream closed") || 자바도구.같음(Neno_SMS, "IOException: read failed") || 자바도구.같음(Neno_SMS, "IOException: write failed")) kategoria_msimbo = 11;
        if (자바도구.같음(Neno_SMS, "ClassCastException")) kategoria_msimbo = 14;
        if (자바도구.같음(Neno_SMS, "NegativeArraySizeException")) kategoria_msimbo = 15;
        if (kategoria_msimbo != 0 && fremu_kielezo >= 0) { 예외던짐(kategoria_msimbo, Neno_SMS); return; }
        mtumiaji.andika("JVM error: "); mtumiaji.andika(Neno_SMS); mtumiaji.andika_kibambo_thamani(10); kosa = true;
    }
    static boolean dondoo(int endesha, int urefu_thamani) {
        if (endesha < 0 || endesha >= faili.length || urefu_thamani < 0) return false;
        int tabaka_Ufafanuzi = endesha / 16384;
        return endesha % 16384 <= tabaka_Ufafanuzi_panga_ukubwa[tabaka_Ufafanuzi] && urefu_thamani <= tabaka_Ufafanuzi_panga_ukubwa[tabaka_Ufafanuzi] - endesha % 16384;
    }
    static int baiti_thamani() {
        if (!dondoo(읽기위치, 1)) { kushindwa_thamani("truncated class file"); return 0; }
        return faili[읽기위치++];
    }
    static int 짧은수() { return baiti_thamani() << 8 | baiti_thamani(); }
    static int namba_kamili() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int urefu_thamani) { if (!dondoo(읽기위치, urefu_thamani)) kushindwa_thamani("invalid attribute size"); else 읽기위치 += urefu_thamani; }
    static boolean hundi_kisobadilika(int 수, int 종류) {
        if (수 <= 0 || 수 >= kisobadilika_lebo.length || kisobadilika_lebo[수] != 종류) { kushindwa_thamani("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int endesha, int urefu_thamani, String Neno_SMS) {
        if (!dondoo(endesha, urefu_thamani)) return false;
        int 읽는자리 = endesha, 끝 = endesha + urefu_thamani;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < Neno_SMS.length(); kitanzi_kielezo++) {
            int msimbo_wa_kibambo = Neno_SMS.charAt(kitanzi_kielezo);
            if (msimbo_wa_kibambo > 0 && msimbo_wa_kibambo < 128) { if (읽는자리 >= 끝 || faili[읽는자리++] != msimbo_wa_kibambo) return false; }
            else if (msimbo_wa_kibambo < 2048) {
                if (읽는자리 + 2 > 끝 || faili[읽는자리++] != (192 | (msimbo_wa_kibambo >> 6)) || faili[읽는자리++] != (128 | (msimbo_wa_kibambo & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || faili[읽는자리++] != (224 | (msimbo_wa_kibambo >> 12)) || faili[읽는자리++] != (128 | ((msimbo_wa_kibambo >> 6) & 63)) || faili[읽는자리++] != (128 | (msimbo_wa_kibambo & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Neno_SMS(int kisobadilika_thamani, String Neno_SMS) { return hundi_kisobadilika(kisobadilika_thamani, 1) && 구간(상가[kisobadilika_thamani], 상나[kisobadilika_thamani], Neno_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!hundi_kisobadilika(가, 1) || !hundi_kisobadilika(나, 1) || 상나[가] != 상나[나]) return false;
        for (int 수 = 0; 수 < 상나[가]; 수++) if (faili[상가[가] + 수] != faili[상가[나] + 수]) return false;
        return true;
    }
    static int tabaka_jina_SMS(int 수) { return hundi_kisobadilika(수, 7) && hundi_kisobadilika(상가[수], 1) ? 상가[수] : 0; }
    static int Marejeleo_jina(int 수) { return hundi_kisobadilika(수, 12) && hundi_kisobadilika(상가[수], 1) ? 상가[수] : 0; }
    static int Marejeleo_aina(int 수) { return hundi_kisobadilika(수, 12) && hundi_kisobadilika(상나[수], 1) ? 상나[수] : 0; }
    static int 서술형(int 끝, boolean tupu_aina) {
        if (읽기위치 >= 끝) { kushindwa_thamani("invalid descriptor"); return 0; }
        int thamani = baiti_thamani();
        if (thamani == 'V' && tupu_aina) return 0;
        if (thamani == 'I' || thamani == 'B' || thamani == 'C' || thamani == 'S' || thamani == 'Z') return 1;
        if (thamani == '[') { 서술형(끝, false); return 2; }
        if (thamani == 'L') {
            int endesha = 읽기위치;
            while (읽기위치 < 끝 && faili[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == endesha) kushindwa_thamani("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        kushindwa_thamani("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int KITENDAKAZI_thamani) {
        int 이전 = 읽기위치, 수 = mbinu_aina[KITENDAKAZI_thamani];
        if (!hundi_kisobadilika(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + 상나[수];
        if (baiti_thamani() != '(') kushindwa_thamani("invalid method descriptor");
        int 개수 = 0;
        while (!kosa && 읽기위치 < 끝 && faili[읽기위치] != ')') {
            if (개수 == 16) { kushindwa_thamani("too many method arguments"); break; }
            mbinu_hoja_aina[KITENDAKAZI_thamani * 16 + 개수++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || baiti_thamani() != ')') kushindwa_thamani("invalid method descriptor");
        함수반환[KITENDAKAZI_thamani] = 서술형(끝, true); 함수인수수[KITENDAKAZI_thamani] = 개수;
        if (읽기위치 != 끝) kushindwa_thamani("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int thamani = 짧은수(); return thamani == 0 ? 0 : 현재읽는종 * 512 + thamani; }
    static int 명상수() { return mbinu_mmiliki[fremu_mbinu[fremu_kielezo]] * 512 + 명짧(); }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !kosa; 수++) { hundi_kisobadilika(상번호(), 1); 건너(namba_kamili()); }
    }
    static int amri_urefu(int thamani) {
        if (thamani == 16 || thamani == 18 || thamani == 21 || thamani == 25 || thamani == 54 || thamani == 58 || thamani == 188) return 2;
        if (thamani == 17 || thamani == 19 || thamani == 132 || thamani >= 153 && thamani <= 167
            || thamani >= 178 && thamani <= 184 || thamani == 187 || thamani == 189 || thamani == 192 || thamani == 193 || thamani == 198 || thamani == 199) return 3;
        if (thamani == 185 || thamani == 200) return 5;
        if (thamani >= 0 && thamani <= 8 || thamani >= 26 && thamani <= 29 || thamani >= 42 && thamani <= 46 || thamani >= 50 && thamani <= 53
            || thamani >= 59 && thamani <= 62 || thamani >= 75 && thamani <= 79 || thamani >= 83 && thamani <= 95
            || thamani == 96 || thamani == 100 || thamani == 104 || thamani == 108 || thamani == 112 || thamani == 116
            || thamani == 120 || thamani == 122 || thamani == 124 || thamani == 126 || thamani == 128 || thamani == 130
            || thamani >= 145 && thamani <= 147 || thamani == 172 || thamani == 176 || thamani == 177 || thamani == 190 || thamani == 191
            || thamani == 194 || thamani == 195) return 1;
        return 0;
    }
    static int 위치정수(int 읽는자리) {
        if (!dondoo(읽는자리, 4)) { kushindwa_thamani("truncated bytecode operand"); return 0; }
        return faili[읽는자리] << 24 | faili[읽는자리 + 1] << 16 | faili[읽는자리 + 2] << 8 | faili[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int endesha, int 끝) {
        int thamani = faili[읽는자리], urefu_thamani = amri_urefu(thamani);
        if (thamani == 170 || thamani == 171) {
            int 기준자리 = 읽는자리 + 1;
            while ((기준자리 - endesha) % 4 != 0) 기준자리++;
            if (끝 - 기준자리 < (thamani == 170 ? 12 : 8)) return 0;
            int 항목수 = thamani == 170 ? 위치정수(기준자리 + 8) - 위치정수(기준자리 + 4) + 1 : 위치정수(기준자리 + 4);
            if (항목수 < 0 || 항목수 > 2048) return 0;
            urefu_thamani = 기준자리 - 읽는자리 + (thamani == 170 ? 12 + 4 * 항목수 : 8 + 8 * 항목수);
        }
        if (thamani == 196 && 읽는자리 + 1 < 끝) {
            int Neno_data = faili[읽는자리 + 1]; urefu_thamani = Neno_data == 132 ? 6 : (Neno_data == 21 || Neno_data == 25 || Neno_data == 54 || Neno_data == 58) ? 4 : 0;
        }
        return urefu_thamani > 0 && urefu_thamani <= 끝 - 읽는자리 ? urefu_thamani : 0;
    }
    static void hundi_fikio_thamani(int fikio_thamani, int KITENDAKAZI_thamani) {
        if (fikio_thamani < mbinu_Anza[KITENDAKAZI_thamani] || fikio_thamani >= mbinu_tamatia[KITENDAKAZI_thamani] || 경계[fikio_thamani] != KITENDAKAZI_thamani + 1) kushindwa_thamani("invalid branch target");
    }
    static void 클래스읽기(int tabaka_Ufafanuzi) {
        현재읽는종 = tabaka_Ufafanuzi; 읽기위치 = tabaka_Ufafanuzi * 16384; panga_ukubwa = 읽기위치 + tabaka_Ufafanuzi_panga_ukubwa[tabaka_Ufafanuzi];
        if (namba_kamili() != 0xcafebabe) { kushindwa_thamani("not a class file"); return; }
        int 부판 = 짧은수(), toleo_thamani = 짧은수();
        if (toleo_thamani < 45 || toleo_thamani > 52 || 부판 != 0) { kushindwa_thamani("supported class versions: 45..52, minor 0"); return; }
        int 상수수 = 짧은수(), 기준자리 = tabaka_Ufafanuzi * 512;
        if (상수수 < 1 || 상수수 > 512) { kushindwa_thamani("constant pool limit (511)"); return; }
        for (int 항목수 = 1; 항목수 < 상수수 && !kosa; 항목수++) {
            int 수 = 기준자리 + 항목수, 종류 = baiti_thamani(); kisobadilika_lebo[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = namba_kamili();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); 상나[수] = 상번호(); }
            else kushindwa_thamani("unsupported constant type");
        }
        int kibali_thamani = 짧은수();
        if ((kibali_thamani & (0x2000 | 0x4000)) != 0) kushindwa_thamani("annotation/enum class unsupported");
        tabaka_Ufafanuzi_jina[tabaka_Ufafanuzi] = tabaka_jina_SMS(상번호());
        종부모[tabaka_Ufafanuzi] = tabaka_jina_SMS(상번호());
        int 접면수 = 짧은수(); if (접면수 > 16) { kushindwa_thamani("interface count limit"); return; }
        종접면수[tabaka_Ufafanuzi] = 접면수;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 접면수; kitanzi_kielezo++) tabaka_kiolesura[tabaka_Ufafanuzi * 16 + kitanzi_kielezo] = tabaka_jina_SMS(상번호());
        int 필드수 = 짧은수();
        if (필드수 > 512 - 칸수) { kushindwa_thamani("field count limit (512)"); return; }
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 필드수 && !kosa; kitanzi_kielezo++) {
            int faili_kielezo = 칸수++; Sloti_mmiliki[faili_kielezo] = tabaka_Ufafanuzi; Sloti_Vibali[faili_kielezo] = 짧은수(); Sloti_jina[faili_kielezo] = 상번호(); Sloti_aina[faili_kielezo] = 상번호();
            hundi_kisobadilika(Sloti_jina[faili_kielezo], 1); hundi_kisobadilika(Sloti_aina[faili_kielezo], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[Sloti_aina[faili_kielezo]]; int kategoria_msimbo = 서술형(읽기위치 + 상나[Sloti_aina[faili_kielezo]], false); 읽기위치 = 보존값;
            if ((Sloti_Vibali[faili_kielezo] & 8) == 0) 칸위치[faili_kielezo] = 종칸수[tabaka_Ufafanuzi]++;
            int sifa_data = 짧은수();
            for (int 안쪽자리 = 0; 안쪽자리 < sifa_data && !kosa; 안쪽자리++) {
                int jina_kisobadilika = 상번호(), 유효길이 = namba_kamili();
                if (Neno_SMS(jina_kisobadilika, "ConstantValue") && 유효길이 == 2) {
                    int data_thamani = 상번호();
                    if (kategoria_msimbo == 1 && hundi_kisobadilika(data_thamani, 3)) Sloti_data[faili_kielezo] = 상가[data_thamani];
                    else if (kategoria_msimbo == 2 && hundi_kisobadilika(data_thamani, 8)) Sloti_data[faili_kielezo] = kisobadilika_SMS(상가[data_thamani]);
                } else 건너(유효길이);
            }
        }
        int 개수 = 짧은수();
        if (개수 > 512 - 함수수) { kushindwa_thamani("method count limit (512)"); return; }
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 개수 && !kosa; kitanzi_kielezo++) {
            int 수 = 함수수++; mbinu_mmiliki[수] = tabaka_Ufafanuzi;
            mbinu_fikia[수] = 짧은수(); mbinu_jina_SMS[수] = 상번호(); mbinu_aina[수] = 상번호();
            hundi_kisobadilika(mbinu_jina_SMS[수], 1); 서술읽기(수);
            if ((mbinu_fikia[수] & 8) == 0) {
                if (함수인수수[수] == 16) { kushindwa_thamani("too many instance method arguments"); return; }
                for (int 비교자리 = 함수인수수[수]; 비교자리 > 0; 비교자리--) mbinu_hoja_aina[수 * 16 + 비교자리] = mbinu_hoja_aina[수 * 16 + 비교자리 - 1];
                mbinu_hoja_aina[수 * 16] = 2; 함수인수수[수]++;
            }
            if ((mbinu_fikia[수] & 0x100) != 0) kushindwa_thamani("user native method unsupported");
            if (Neno_SMS(mbinu_jina_SMS[수], "<clinit>")) anzilisha_tabaka_Ufafanuzi[tabaka_Ufafanuzi] = 수 + 1;
            for (int mbele_thamani = 0; mbele_thamani < 수; mbele_thamani++) if (mbinu_mmiliki[mbele_thamani] == tabaka_Ufafanuzi && 같은말(mbinu_jina_SMS[mbele_thamani], mbinu_jina_SMS[수]) && 같은말(mbinu_aina[mbele_thamani], mbinu_aina[수])) kushindwa_thamani("duplicate method");
            int 속성수 = 짧은수();
            for (int sifa_thamani = 0; sifa_thamani < 속성수 && !kosa; sifa_thamani++) {
                int Jina = 상번호(), urefu_thamani = namba_kamili(), endesha = 읽기위치;
                if (!dondoo(endesha, urefu_thamani)) { kushindwa_thamani("truncated method attribute"); break; }
                if (Neno_SMS(Jina, "Code")) {
                    if (mbinu_Anza[수] != 0) kushindwa_thamani("duplicate Code attribute");
                    mbinu_Mpororo[수] = 짧은수(); 함수지역[수] = 짧은수(); int msimbo_urefu = namba_kamili();
                    if (mbinu_Mpororo[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || msimbo_urefu < 1 || msimbo_urefu > 8192) kushindwa_thamani("method memory limits exceeded");
                    mbinu_Anza[수] = 읽기위치; 건너(msimbo_urefu); mbinu_tamatia[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { kushindwa_thamani("exception table limit"); return; }
                    for (int 안쪽자리 = 0; 안쪽자리 < 잡는수; 안쪽자리++) {
                        int kosa_Marejeleo = 잡기수++; 잡기함수[kosa_Marejeleo] = 수;
                        잡기시작[kosa_Marejeleo] = mbinu_Anza[수] + 짧은수(); 잡기끝[kosa_Marejeleo] = mbinu_Anza[수] + 짧은수();
                        잡기위치[kosa_Marejeleo] = mbinu_Anza[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[kosa_Marejeleo] = 부호값 == 0 ? 0 : tabaka_jina_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != endesha + urefu_thamani) kushindwa_thamani("Code attribute size mismatch");
                } else 건너(urefu_thamani);
            }
            if ((mbinu_fikia[수] & 0x400) != 0) continue;
            if (mbinu_Anza[수] == 0) kushindwa_thamani("missing Code attribute");
            int Sloti_ingizo = mbinu_Anza[수];
            while (Sloti_ingizo < mbinu_tamatia[수] && !kosa) {
                int urefu_thamani = 길이읽기(Sloti_ingizo, mbinu_Anza[수], mbinu_tamatia[수]);
                if (urefu_thamani == 0) { kushindwa_thamani("unsupported or truncated bytecode"); break; }
                경계[Sloti_ingizo] = 수 + 1; Sloti_ingizo += urefu_thamani;
            }
            Sloti_ingizo = mbinu_Anza[수];
            while (Sloti_ingizo < mbinu_tamatia[수] && !kosa) {
                int thamani = faili[Sloti_ingizo];
                if (thamani >= 153 && thamani <= 167 || thamani == 198 || thamani == 199) hundi_fikio_thamani(Sloti_ingizo + (short)(faili[Sloti_ingizo + 1] << 8 | faili[Sloti_ingizo + 2]), 수);
                if (thamani == 200) hundi_fikio_thamani(Sloti_ingizo + 위치정수(Sloti_ingizo + 1), 수);
                if (thamani == 170 || thamani == 171) {
                    int 읽는자리 = Sloti_ingizo + 1; while ((읽는자리 - mbinu_Anza[수]) % 4 != 0) 읽는자리++;
                    hundi_fikio_thamani(Sloti_ingizo + 위치정수(읽는자리), 수);
                    int 항목수 = thamani == 170 ? 위치정수(읽는자리 + 8) - 위치정수(읽는자리 + 4) + 1 : 위치정수(읽는자리 + 4);
                    읽는자리 += thamani == 170 ? 12 : 8;
                    for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) hundi_fikio_thamani(Sloti_ingizo + 위치정수(읽는자리 + 안쪽자리 * (thamani == 170 ? 4 : 8) + (thamani == 170 ? 0 : 4)), 수);
                }
                Sloti_ingizo += 길이읽기(Sloti_ingizo, mbinu_Anza[수], mbinu_tamatia[수]);
            }
            for (int 안쪽자리 = 0; 안쪽자리 < 잡기수; 안쪽자리++) if (잡기함수[안쪽자리] == 수) {
                hundi_fikio_thamani(잡기시작[안쪽자리], 수); hundi_fikio_thamani(잡기위치[안쪽자리], 수);
                if (잡기끝[안쪽자리] != mbinu_tamatia[수]) hundi_fikio_thamani(잡기끝[안쪽자리], 수);
                if (잡기시작[안쪽자리] >= 잡기끝[안쪽자리]) kushindwa_thamani("invalid exception range");
            }
        }
        if (!kosa) 속성건너();
        if (읽기위치 != panga_ukubwa) kushindwa_thamani("extra class file data");
    }
    static int tengea_Hifadhi(int 종류, int urefu_thamani) { return 새기억(종류, urefu_thamani); }
    static boolean kipengee_thamani(int Marejeleo, int 종류) {
        if (!객체유효(Marejeleo)) return false;
        if (힙[Marejeleo] != 종류) { kushindwa_thamani("object type mismatch"); return false; }
        return true;
    }
    static int kisobadilika_SMS(int kielezo) {
        if (!hundi_kisobadilika(kielezo, 1)) return 0;
        if (tungo_Marejeleo[kielezo] != 0) return tungo_Marejeleo[kielezo];
        int Marejeleo = tengea_Hifadhi(1, 상나[kielezo]); if (kosa) return 0;
        int 끝 = 상가[kielezo] + 상나[kielezo], 수 = 상가[kielezo], urefu_thamani = 0;
        while (수 < 끝 && !kosa) {
            int thamani = faili[수++];
            if (thamani == 0) kushindwa_thamani("invalid modified UTF-8");
            else if (thamani >= 192 && thamani <= 223 && 수 < 끝) {
                int 다음 = faili[수++];
                if ((다음 & 192) != 128) kushindwa_thamani("invalid modified UTF-8");
                thamani = (thamani & 31) << 6 | 다음 & 63;
                if (thamani != 0 && thamani < 128) kushindwa_thamani("overlong modified UTF-8");
            } else if (thamani >= 224 && thamani <= 239 && 수 + 1 < 끝) {
                int 가 = faili[수++], 나 = faili[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) kushindwa_thamani("invalid modified UTF-8");
                thamani = (thamani & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (thamani < 2048) kushindwa_thamani("overlong modified UTF-8");
            } else if (thamani >= 128) kushindwa_thamani("invalid modified UTF-8");
            힙[Marejeleo + 2 + urefu_thamani++] = thamani;
        }
        힙[Marejeleo + 1] = urefu_thamani; tungo_Marejeleo[kielezo] = Marejeleo; return Marejeleo;
    }
    static int mwenyeji_kibambo(String thamani) {
        int Marejeleo = tengea_Hifadhi(1, thamani.length()); if (kosa) return 0;
        for (int 수 = 0; 수 < thamani.length(); 수++) 힙[Marejeleo + 2 + 수] = thamani.charAt(수);
        return Marejeleo;
    }
    static void andika_SMS(int Marejeleo) {
        if (Marejeleo == 0) { mtumiaji.andika("null"); return; }
        if (!kipengee_thamani(Marejeleo, 1)) return;
        for (int 수 = 0; 수 < 힙[Marejeleo + 1]; 수++) mtumiaji.andika_kibambo_thamani(힙[Marejeleo + 2 + 수]);
    }
    static int dijiti_kibambo(int thamani) {
        int Marejeleo = tengea_Hifadhi(1, 11); if (kosa) return 0;
        int urefu_thamani = 0;
        if (thamani < 0) 힙[Marejeleo + 2 + urefu_thamani++] = '-'; else thamani = -thamani;
        int 자리 = 1000000000; boolean endesha = false;
        while (자리 != 0) {
            int 수 = -(thamani / 자리);
            if (수 != 0 || endesha || 자리 == 1) { 힙[Marejeleo + 2 + urefu_thamani++] = '0' + 수; endesha = true; }
            thamani %= 자리; 자리 /= 10;
        }
        힙[Marejeleo + 1] = urefu_thamani; return Marejeleo;
    }
    static int 정수해독(int Marejeleo) {
        if (!kipengee_thamani(Marejeleo, 1)) return 0;
        int urefu_thamani = 힙[Marejeleo + 1], 수 = 0, thamani = 0; boolean 음수 = false;
        if (urefu_thamani > 0 && (힙[Marejeleo + 2] == '-' || 힙[Marejeleo + 2] == '+')) { 음수 = 힙[Marejeleo + 2] == '-'; 수++; }
        if (수 == urefu_thamani) kushindwa_thamani("NumberFormatException");
        for (; 수 < urefu_thamani && !kosa; 수++) {
            int dijiti_thamani = 힙[Marejeleo + 2 + 수] - '0';
            if (dijiti_thamani < 0 || dijiti_thamani > 9 || thamani < -214748364 || thamani == -214748364 && dijiti_thamani > (음수 ? 8 : 7)) kushindwa_thamani("NumberFormatException");
            thamani = thamani * 10 - dijiti_thamani;
        }
        return 음수 ? thamani : -thamani;
    }
    static void 넣기(int thamani, int aina_thamani) {
        if (kosa) return;
        if (fremu_kielezo < 0 || fremu_Mpororo[fremu_kielezo] >= mbinu_Mpororo[fremu_mbinu[fremu_kielezo]]) { kushindwa_thamani("operand stack overflow"); return; }
        int Sloti_ingizo = fremu_kielezo * 128 + fremu_Mpororo[fremu_kielezo]++; 스택값[Sloti_ingizo] = thamani; 스택형[Sloti_ingizo] = aina_thamani;
    }
    static int 빼기(int aina_thamani) {
        if (kosa) return 0;
        if (fremu_kielezo < 0 || fremu_Mpororo[fremu_kielezo] < 1) { kushindwa_thamani("operand stack underflow"); return 0; }
        int Sloti_ingizo = fremu_kielezo * 128 + --fremu_Mpororo[fremu_kielezo]; 반환형 = 스택형[Sloti_ingizo];
        if (aina_thamani != 0 && 반환형 != aina_thamani) kushindwa_thamani("operand type mismatch");
        if (반환형 == 2) linda_thamani(스택값[Sloti_ingizo]);
        return 스택값[Sloti_ingizo];
    }
    static void 지역읽기(int kielezo, int aina_thamani) {
        if (kielezo >= 함수지역[fremu_mbinu[fremu_kielezo]] || kielezo < 0 || jirani_aina[fremu_kielezo * 128 + kielezo] != aina_thamani) { kushindwa_thamani("invalid or uninitialized local"); return; }
        넣기(jirani_thamani[fremu_kielezo * 128 + kielezo], aina_thamani);
    }
    static void andika_jirani(int kielezo, int aina_thamani) {
        if (kielezo >= 함수지역[fremu_mbinu[fremu_kielezo]] || kielezo < 0) { kushindwa_thamani("local index out of range"); return; }
        int thamani = 빼기(aina_thamani); jirani_thamani[fremu_kielezo * 128 + kielezo] = thamani; jirani_aina[fremu_kielezo * 128 + kielezo] = aina_thamani;
    }
    static int 명바() {
        int 위치 = 틀위치[fremu_kielezo];
        if (위치 < mbinu_Anza[fremu_mbinu[fremu_kielezo]] || 위치 >= mbinu_tamatia[fremu_mbinu[fremu_kielezo]]) { kushindwa_thamani("instruction pointer out of range"); return 0; }
        틀위치[fremu_kielezo]++; return faili[위치];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void hamisha_thamani(int 위치) {
        int KITENDAKAZI_thamani = fremu_mbinu[fremu_kielezo];
        if (위치 < mbinu_Anza[KITENDAKAZI_thamani] || 위치 >= mbinu_tamatia[KITENDAKAZI_thamani] || 경계[위치] != KITENDAKAZI_thamani + 1) kushindwa_thamani("invalid branch target");
        else 틀위치[fremu_kielezo] = 위치;
    }
    static void 호출(int KITENDAKAZI_thamani) {
        if (fremu_kielezo % 32 == 31) { kushindwa_thamani("call stack limit (32)"); return; }
        int 다음 = fremu_kielezo + 1;
        for (int 수 = 0; 수 < 128; 수++) jirani_aina[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[KITENDAKAZI_thamani] - 1; 수 >= 0; 수--) {
            jirani_thamani[다음 * 128 + 수] = 빼기(mbinu_hoja_aina[KITENDAKAZI_thamani * 16 + 수]); jirani_aina[다음 * 128 + 수] = mbinu_hoja_aina[KITENDAKAZI_thamani * 16 + 수];
        }
        if (kosa) return;
        fremu_kielezo = 다음; anzilisha_fremu[fremu_kielezo] = 0; fremu_mbinu[fremu_kielezo] = KITENDAKAZI_thamani; 틀위치[fremu_kielezo] = mbinu_Anza[KITENDAKAZI_thamani]; fremu_Mpororo[fremu_kielezo] = 0;
    }
    static void 반환(int aina_thamani) {
        if (aina_thamani != 함수반환[fremu_mbinu[fremu_kielezo]]) { kushindwa_thamani("return type mismatch"); return; }
        int thamani = aina_thamani == 0 ? 0 : 빼기(aina_thamani);
        if (anzilisha_fremu[fremu_kielezo] != 0) tabaka_Ufafanuzi_hali[anzilisha_fremu[fremu_kielezo] - 1] = 2;
        if (틀잠금[fremu_kielezo] != 0) { 잠금풀기(틀잠금[fremu_kielezo]); 틀잠금[fremu_kielezo] = 0; }
        fremu_kielezo--; if (fremu_kielezo >= 현재가닥 * 32 && aina_thamani != 0) 넣기(thamani, aina_thamani);
    }
    static int[] Stream_faili_jina = new int[64];
    static void faili_Stream_ita(int mmiliki_thamani, int Jina, int umbiza_thamani, int amri) {
        boolean 출력 = Neno_SMS(mmiliki_thamani, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (amri == 183 && Neno_SMS(Jina, "<init>")) {
            boolean 이어 = false;
            if (출력 && Neno_SMS(umbiza_thamani, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Neno_SMS(umbiza_thamani, "(Ljava/lang/String;)V")) { kushindwa_thamani("unsupported file stream constructor"); return; }
            int faili_ingizo_jina = 빼기(2), Stream_thamani = 빼기(2);
            if (!kipengee_thamani(faili_ingizo_jina, 1) || !kipengee_thamani(Stream_thamani, 종류) || kosa) return;
            if (힙[Stream_thamani + 3] != 0) { kushindwa_thamani("file stream already initialized"); return; }
            int urefu_thamani = 힙[faili_ingizo_jina + 1];
            if (urefu_thamani < 1 || urefu_thamani > 63) { kushindwa_thamani("invalid file name length"); return; }
            for (int Sloti_ingizo = 0; Sloti_ingizo < urefu_thamani; Sloti_ingizo++) {
                int thamani = 힙[faili_ingizo_jina + 2 + Sloti_ingizo];
                if (thamani < 1) { kushindwa_thamani("invalid file stream path"); return; }
                Stream_faili_jina[Sloti_ingizo] = thamani;
            }
            Stream_faili_jina[urefu_thamani] = 0;
            int 서술자 = mtumiaji.파일서술자열기(Stream_faili_jina, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { kushindwa_thamani("FileNotFoundException: file open failed"); return; }
            힙[Stream_thamani + 2] = 서술자; 힙[Stream_thamani + 3] = 1;
            return;
        }
        if (amri != 182) { kushindwa_thamani("invalid file stream invocation"); return; }
        if ((출력 && Neno_SMS(Jina, "write") || !출력 && Neno_SMS(Jina, "read"))
            && (Neno_SMS(umbiza_thamani, 출력 ? "([B)V" : "([B)I") || Neno_SMS(umbiza_thamani, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean dondoo_thamani = Neno_SMS(umbiza_thamani, 출력 ? "([BII)V" : "([BII)I");
            int 항목수 = dondoo_thamani ? 빼기(1) : 0, 시작점 = dondoo_thamani ? 빼기(1) : 0, data_ARRAY = 빼기(2), kipengee_Marejeleo = 빼기(2);
            if (!kipengee_thamani(data_ARRAY, 20) || !kipengee_thamani(kipengee_Marejeleo, 종류)) return;
            if (!dondoo_thamani) 항목수 = 힙[data_ARRAY + 1];
            if (시작점 < 0 || 항목수 < 0 || 시작점 > 힙[data_ARRAY + 1] - 항목수) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[kipengee_Marejeleo + 3] == 0 || 힙[kipengee_Marejeleo + 2] < 0) { kushindwa_thamani("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < 항목수 && !kosa) {
                int 반환값 = 출력 ? mtumiaji.파일한바이트쓰기(힙[kipengee_Marejeleo + 2], 힙[data_ARRAY + 2 + 시작점 + 완료수]) : mtumiaji.파일한바이트읽기(힙[kipengee_Marejeleo + 2]);
                if (반환값 < 0) { kushindwa_thamani(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[data_ARRAY + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(항목수 != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Neno_SMS(Jina, "flush") && Neno_SMS(umbiza_thamani, "()V")) { int kipengee_Marejeleo = 빼기(2); if (kipengee_thamani(kipengee_Marejeleo, 종류) && 힙[kipengee_Marejeleo + 2] < 0) kushindwa_thamani("IOException: stream closed"); return; }
        int Kitendo = -1, thamani = 0;
        if (Neno_SMS(Jina, "close") && Neno_SMS(umbiza_thamani, "()V")) Kitendo = 0;
        if (!출력 && Neno_SMS(Jina, "read") && Neno_SMS(umbiza_thamani, "()I")) Kitendo = 1;
        if (출력 && Neno_SMS(Jina, "write") && Neno_SMS(umbiza_thamani, "(I)V")) { Kitendo = 2; thamani = 빼기(1); }
        if (Kitendo < 0) { kushindwa_thamani("unsupported file stream method"); return; }
        int Stream_thamani = 빼기(2);
        if (!kipengee_thamani(Stream_thamani, 종류) || kosa) return;
        if (힙[Stream_thamani + 3] == 0) { kushindwa_thamani("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_thamani + 2];
        if (Kitendo == 0) {
            if (서술자 >= 0 && mtumiaji.파일서술자닫기(서술자) < 0) kushindwa_thamani("IOException: close failed");
            힙[Stream_thamani + 2] = -1; return;
        }
        if (서술자 < 0) { kushindwa_thamani("IOException: stream closed"); return; }
        if (Kitendo == 1) {
            int 결과 = mtumiaji.파일한바이트읽기(서술자);
            if (결과 < -1) kushindwa_thamani("IOException: read failed"); else 넣기(결과 == 256 ? -1 : 결과, 1);
        } else if (mtumiaji.파일한바이트쓰기(서술자, thamani) != 1) kushindwa_thamani("IOException: write failed");
    }
    static void ita_mbinu(int kielezo, int amri) {
        if (kielezo <= 0 || kielezo >= kisobadilika_lebo.length || (kisobadilika_lebo[kielezo] != 10 && kisobadilika_lebo[kielezo] != 11)) { kushindwa_thamani("invalid method reference"); return; }
        int mmiliki_thamani = tabaka_jina_SMS(상가[kielezo]), Jina = Marejeleo_jina(상나[kielezo]), umbiza_thamani = Marejeleo_aina(상나[kielezo]);
        if (kosa) return;
        if (기본호출(mmiliki_thamani, Jina, umbiza_thamani, amri)) return;
        if (Neno_SMS(mmiliki_thamani, "java/io/FileInputStream") || Neno_SMS(mmiliki_thamani, "java/io/FileOutputStream")) {
            faili_Stream_ita(mmiliki_thamani, Jina, umbiza_thamani, amri); return;
        }
        if (amri == 184 && Neno_SMS(mmiliki_thamani, "java/lang/Integer") && Neno_SMS(Jina, "parseInt") && Neno_SMS(umbiza_thamani, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (amri == 182 && Neno_SMS(mmiliki_thamani, "java/io/PrintStream") && (Neno_SMS(Jina, "println") || Neno_SMS(Jina, "print"))) {
            int aina_thamani = 0, thamani = 0;
            if (Neno_SMS(umbiza_thamani, "(I)V")) { aina_thamani = 1; thamani = 빼기(1); }
            else if (Neno_SMS(umbiza_thamani, "(Z)V")) { aina_thamani = 2; thamani = 빼기(1); }
            else if (Neno_SMS(umbiza_thamani, "(C)V")) { aina_thamani = 3; thamani = 빼기(1); }
            else if (Neno_SMS(umbiza_thamani, "(Ljava/lang/String;)V")) { aina_thamani = 4; thamani = 빼기(2); }
            else if (!Neno_SMS(umbiza_thamani, "()V") || !Neno_SMS(Jina, "println")) kushindwa_thamani("unsupported print descriptor");
            if (빼기(2) != -1) kushindwa_thamani("invalid PrintStream receiver");
            if (kosa) return;
            if (aina_thamani == 1) 자바도구.수쓰기(thamani);
            if (aina_thamani == 2) mtumiaji.andika(thamani == 0 ? "false" : "true");
            if (aina_thamani == 3) mtumiaji.andika_kibambo_thamani(thamani & 65535);
            if (aina_thamani == 4) andika_SMS(thamani);
            if (Neno_SMS(Jina, "println")) mtumiaji.andika_kibambo_thamani(10);
            return;
        }
        if (amri == 182 && Neno_SMS(mmiliki_thamani, "java/lang/String")) {
            if (Neno_SMS(Jina, "length") && Neno_SMS(umbiza_thamani, "()I")) {
                int Marejeleo = 빼기(2); if (kipengee_thamani(Marejeleo, 1)) 넣기(힙[Marejeleo + 1], 1); return;
            }
            if (Neno_SMS(Jina, "charAt") && Neno_SMS(umbiza_thamani, "(I)C")) {
                int hati_chini_thamani = 빼기(1), Marejeleo = 빼기(2);
                if (kipengee_thamani(Marejeleo, 1)) {
                    if (hati_chini_thamani < 0 || hati_chini_thamani >= 힙[Marejeleo + 1]) kushindwa_thamani("StringIndexOutOfBoundsException"); else 넣기(힙[Marejeleo + 2 + hati_chini_thamani], 1);
                }
                return;
            }
        }
        if (Neno_SMS(mmiliki_thamani, "java/lang/StringBuilder")) {
            if (amri == 183 && Neno_SMS(Jina, "<init>") && Neno_SMS(umbiza_thamani, "()V")) { kipengee_thamani(빼기(2), 4); return; }
            if (amri == 182 && Neno_SMS(Jina, "toString") && Neno_SMS(umbiza_thamani, "()Ljava/lang/String;")) {
                int Marejeleo = 빼기(2); if (kipengee_thamani(Marejeleo, 4)) 넣기(힙[Marejeleo + 2] == 0 ? mwenyeji_kibambo("") : 힙[Marejeleo + 2], 2); return;
            }
            if (amri == 182 && Neno_SMS(Jina, "append")) {
                int SMS = 0;
                if (Neno_SMS(umbiza_thamani, "(I)Ljava/lang/StringBuilder;")) SMS = dijiti_kibambo(빼기(1));
                else if (Neno_SMS(umbiza_thamani, "(Z)Ljava/lang/StringBuilder;")) SMS = mwenyeji_kibambo(빼기(1) == 0 ? "false" : "true");
                else if (Neno_SMS(umbiza_thamani, "(C)Ljava/lang/StringBuilder;")) {
                    int thamani = 빼기(1); SMS = tengea_Hifadhi(1, 1); if (!kosa) 힙[SMS + 2] = thamani & 65535;
                }
                else if (Neno_SMS(umbiza_thamani, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { SMS = 빼기(2); if (SMS == 0) SMS = mwenyeji_kibambo("null"); }
                else { kushindwa_thamani("unsupported StringBuilder append"); return; }
                int Marejeleo = 빼기(2); if (!kipengee_thamani(Marejeleo, 4) || !kipengee_thamani(SMS, 1)) return;
                int mbele_thamani = 힙[Marejeleo + 2], mbele_thamani_urefu = mbele_thamani == 0 ? 0 : 힙[mbele_thamani + 1], Nyuma_thamani_urefu = 힙[SMS + 1];
                int 새글 = tengea_Hifadhi(1, mbele_thamani_urefu + Nyuma_thamani_urefu); if (kosa) return;
                for (int 수 = 0; 수 < mbele_thamani_urefu; 수++) 힙[새글 + 2 + 수] = 힙[mbele_thamani + 2 + 수];
                for (int 수 = 0; 수 < Nyuma_thamani_urefu; 수++) 힙[새글 + 2 + mbele_thamani_urefu + 수] = 힙[SMS + 2 + 수];
                힙[Marejeleo + 2] = 새글; 넣기(Marejeleo, 2); return;
            }
        }
        int tabaka_Ufafanuzi = gundua_tabaka_Ufafanuzi(mmiliki_thamani); if (tabaka_Ufafanuzi < 0 || kosa) return;
        int faili_kielezo = gundua_mbinu(tabaka_Ufafanuzi, Jina, umbiza_thamani);
        if (faili_kielezo < 0) {
            for (int msimbo_wa_kibambo = tabaka_Ufafanuzi, 항목수 = 0; msimbo_wa_kibambo >= 0 && 항목수 < 16; 항목수++, msimbo_wa_kibambo = 부모종(msimbo_wa_kibambo))
                if (Neno_SMS(종부모[msimbo_wa_kibambo], "java/lang/Thread")) { 가닥호출(Jina, umbiza_thamani, amri); return; }
            kushindwa_thamani("NoSuchMethodError"); return;
        }
        if (((mbinu_fikia[faili_kielezo] & 8) != 0) != (amri == 184)) { kushindwa_thamani("method static/instance mismatch"); return; }
        if (amri == 184) { if (!anzilisha(mbinu_mmiliki[faili_kielezo], fremu_agizo[fremu_kielezo])) return; }
        else {
            int 읽는자리 = fremu_Mpororo[fremu_kielezo] - 함수인수수[faili_kielezo];
            if (읽는자리 < 0 || 스택형[fremu_kielezo * 128 + 읽는자리] != 2) { kushindwa_thamani("invalid method receiver"); return; }
            int kipengee_Marejeleo = 스택값[fremu_kielezo * 128 + 읽는자리];
            if (!객체유효(kipengee_Marejeleo)) return;
            if (힙[kipengee_Marejeleo] < 32 || !종포함(힙[kipengee_Marejeleo] - 32, mmiliki_thamani)) { kushindwa_thamani("method receiver type mismatch"); return; }
            if (amri != 183) faili_kielezo = gundua_mbinu(힙[kipengee_Marejeleo] - 32, Jina, umbiza_thamani);
        }
        if (faili_kielezo < 0 || (mbinu_fikia[faili_kielezo] & 0x400) != 0) { kushindwa_thamani("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((mbinu_fikia[faili_kielezo] & 32) != 0) {
            if (amri == 184) { int msimbo_wa_kibambo = mbinu_mmiliki[faili_kielezo]; if (종잠금[msimbo_wa_kibambo] == 0) 종잠금[msimbo_wa_kibambo] = tengea_Hifadhi(8, 0); 잠금참조 = 종잠금[msimbo_wa_kibambo]; }
            else 잠금참조 = 스택값[fremu_kielezo * 128 + fremu_Mpororo[fremu_kielezo] - 함수인수수[faili_kielezo]];
            if (!잠금얻기(잠금참조)) { if (!kosa) 틀위치[fremu_kielezo] = fremu_agizo[fremu_kielezo]; return; }
        }
        호출(faili_kielezo); if (!kosa) 틀잠금[fremu_kielezo] = 잠금참조;
    }
    static boolean 배열저장가능(int ARRAY_Marejeleo, int data_thamani) {
        if (data_thamani == 0 || ARRAY_elementi[ARRAY_Marejeleo] == 0) return true;
        boolean 성공여부 = ARRAY_elementi[ARRAY_Marejeleo] == -1 ? (data_thamani > 0 && data_thamani < 힙끝 && 힙[data_thamani] == 1) : 맞는객체(data_thamani, ARRAY_elementi[ARRAY_Marejeleo]);
        if (!성공여부 && !kosa) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int ARRAY_Sloti(int Marejeleo, int hati_chini_thamani, int aina_thamani) {
        if (!kipengee_thamani(Marejeleo, aina_thamani)) return 0;
        if (hati_chini_thamani < 0 || hati_chini_thamani >= 힙[Marejeleo + 1]) { kushindwa_thamani("ArrayIndexOutOfBoundsException"); return 0; }
        return Marejeleo + 2 + hati_chini_thamani;
    }
    static void tekeleza_amri() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (kosa) { if (던진객체 != 0) kishiko_vighairi(); if (kosa || fremu_kielezo < 현재가닥 * 32) break; }
            if (fremu_kielezo < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!badili_mtungo()) break; 조각 = 100; }
            if (fremu_kielezo == 0 && tabaka_Ufafanuzi_hali[ingizo_tabaka_Ufafanuzi] != 2 && !anzilisha(ingizo_tabaka_Ufafanuzi, 틀위치[fremu_kielezo])) continue;
            if (fremu_kielezo == 현재가닥 * 32 && 현재가닥 != 0 && (mbinu_fikia[fremu_mbinu[fremu_kielezo]] & 32) != 0 && 틀잠금[fremu_kielezo] == 0) {
                int kipengee_Marejeleo = mtungo_lengo[현재가닥]; if (!잠금얻기(kipengee_Marejeleo)) { if (kosa) break; continue; } 틀잠금[fremu_kielezo] = kipengee_Marejeleo;
            }
            잠시수 = 0;
            if (--남음 == 0) { kushindwa_thamani("instruction limit (500000)"); break; }
            int endesha = 틀위치[fremu_kielezo]; fremu_agizo[fremu_kielezo] = endesha; int thamani = 명바();
            if (kosa) break;
            if (thamani == 0) continue;
            if (thamani == 1) { 넣기(0, 2); continue; }
            if (thamani >= 2 && thamani <= 8) { 넣기(thamani - 3, 1); continue; }
            if (thamani == 16) { 넣기((byte)명바(), 1); continue; }
            if (thamani == 17) { 넣기((short)명짧(), 1); continue; }
            if (thamani == 18 || thamani == 19) {
                int 수 = mbinu_mmiliki[fremu_mbinu[fremu_kielezo]] * 512 + (thamani == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= kisobadilika_lebo.length) kushindwa_thamani("invalid ldc constant");
                else if (kisobadilika_lebo[수] == 3) 넣기(상가[수], 1);
                else if (kisobadilika_lebo[수] == 8) 넣기(kisobadilika_SMS(상가[수]), 2);
                else kushindwa_thamani("unsupported ldc constant");
                continue;
            }
            if (thamani == 21 || thamani == 25) { 지역읽기(명바(), thamani == 21 ? 1 : 2); continue; }
            if (thamani >= 26 && thamani <= 29) { 지역읽기(thamani - 26, 1); continue; }
            if (thamani >= 42 && thamani <= 45) { 지역읽기(thamani - 42, 2); continue; }
            if (thamani == 54 || thamani == 58) { andika_jirani(명바(), thamani == 54 ? 1 : 2); continue; }
            if (thamani >= 59 && thamani <= 62) { andika_jirani(thamani - 59, 1); continue; }
            if (thamani >= 75 && thamani <= 78) { andika_jirani(thamani - 75, 2); continue; }
            if (thamani == 46 || thamani >= 50 && thamani <= 53) {
                int 항목자리 = 빼기(1), kipengee_Marejeleo = 빼기(2), kategoria_msimbo = thamani == 46 ? 2 : thamani == 50 ? 3 : thamani == 51 ? 20 : thamani == 52 ? 22 : 23;
                if (thamani == 51 && kipengee_Marejeleo > 0 && kipengee_Marejeleo < 힙끝 && 힙[kipengee_Marejeleo] == 21) kategoria_msimbo = 21;
                int 읽는자리 = ARRAY_Sloti(kipengee_Marejeleo, 항목자리, kategoria_msimbo); if (!kosa) 넣기(힙[읽는자리], thamani == 50 ? 2 : 1); continue;
            }
            if (thamani == 79 || thamani >= 83 && thamani <= 86) {
                int ingizo_Marejeleo = 빼기(thamani == 83 ? 2 : 1), 항목자리 = 빼기(1), kipengee_Marejeleo = 빼기(2), kategoria_msimbo = thamani == 79 ? 2 : thamani == 83 ? 3 : thamani == 84 ? 20 : thamani == 85 ? 22 : 23;
                if (thamani == 84 && kipengee_Marejeleo > 0 && kipengee_Marejeleo < 힙끝 && 힙[kipengee_Marejeleo] == 21) kategoria_msimbo = 21;
                int 읽는자리 = ARRAY_Sloti(kipengee_Marejeleo, 항목자리, kategoria_msimbo);
                if (!kosa && kategoria_msimbo == 3 && !배열저장가능(kipengee_Marejeleo, ingizo_Marejeleo)) continue;
                if (!kosa) 힙[읽는자리] = kategoria_msimbo == 20 ? (byte)ingizo_Marejeleo : kategoria_msimbo == 21 ? ingizo_Marejeleo & 1 : kategoria_msimbo == 22 ? (char)ingizo_Marejeleo : kategoria_msimbo == 23 ? (short)ingizo_Marejeleo : ingizo_Marejeleo;
                continue;
            }
            if (thamani >= 87 && thamani <= 95) { Mpororo_agizo(thamani); continue; }
            if (thamani == 96 || thamani == 100 || thamani == 104 || thamani == 108 || thamani == 112 || thamani == 120
                || thamani == 122 || thamani == 124 || thamani == 126 || thamani == 128 || thamani == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), 결과 = 0;
                if ((thamani == 108 || thamani == 112) && 나 == 0) { kushindwa_thamani("ArithmeticException: / by zero"); continue; }
                if (thamani == 96) 결과 = 가 + 나;
                if (thamani == 100) 결과 = 가 - 나;
                if (thamani == 104) 결과 = 가 * 나;
                if (thamani == 108) 결과 = 가 / 나;
                if (thamani == 112) 결과 = 가 % 나;
                if (thamani == 120) 결과 = 가 << 나;
                if (thamani == 122) 결과 = 가 >> 나;
                if (thamani == 124) 결과 = 가 >>> 나;
                if (thamani == 126) 결과 = 가 & 나;
                if (thamani == 128) 결과 = 가 | 나;
                if (thamani == 130) 결과 = 가 ^ 나;
                넣기(결과, 1); continue;
            }
            if (thamani == 116) { 넣기(-빼기(1), 1); continue; }
            if (thamani == 132) {
                int jirani_upeo = 명바(), 증분 = (byte)명바(); 지역읽기(jirani_upeo, 1); 넣기(빼기(1) + 증분, 1); andika_jirani(jirani_upeo, 1); continue;
            }
            if (thamani >= 145 && thamani <= 147) {
                int 수 = 빼기(1); 넣기(thamani == 145 ? (byte)수 : thamani == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (thamani >= 153 && thamani <= 167 || thamani == 198 || thamani == 199) {
                int fikio_thamani = endesha + (short)명짧(); boolean 갈까 = thamani == 167;
                if (thamani >= 153 && thamani <= 158) {
                    int 수 = 빼기(1); 갈까 = thamani == 153 ? 수 == 0 : thamani == 154 ? 수 != 0 : thamani == 155 ? 수 < 0 : thamani == 156 ? 수 >= 0 : thamani == 157 ? 수 > 0 : 수 <= 0;
                } else if (thamani >= 159 && thamani <= 166) {
                    int 나 = 빼기(thamani >= 165 ? 2 : 1), 가 = 빼기(thamani >= 165 ? 2 : 1);
                    갈까 = thamani == 159 || thamani == 165 ? 가 == 나 : thamani == 160 || thamani == 166 ? 가 != 나 : thamani == 161 ? 가 < 나 : thamani == 162 ? 가 >= 나 : thamani == 163 ? 가 > 나 : 가 <= 나;
                } else if (thamani == 198 || thamani == 199) { int 수 = 빼기(2); 갈까 = thamani == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) hamisha_thamani(fikio_thamani); continue;
            }
            if (thamani == 172 || thamani == 176 || thamani == 177) { 반환(thamani == 172 ? 1 : thamani == 176 ? 2 : 0); continue; }
            if (thamani >= 178 && thamani <= 181) { 필드호출(명상수(), thamani, endesha); continue; }
            if (thamani >= 182 && thamani <= 185) {
                int 부호값 = 명상수();
                if (thamani == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { kushindwa_thamani("invalid invokeinterface operands"); continue; } }
                ita_mbinu(부호값, thamani); continue;
            }
            if (thamani == 187) { 새객체(tabaka_jina_SMS(명상수()), endesha); continue; }
            if (thamani == 188 || thamani == 189) {
                int kategoria_msimbo = 3, kijenzi = 0;
                if (thamani == 188) { int 임시값 = 명바(); kategoria_msimbo = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else kijenzi = tabaka_jina_SMS(명상수());
                if (kategoria_msimbo == 0) { kushindwa_thamani("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), kipengee_Marejeleo = tengea_Hifadhi(kategoria_msimbo, 유효길이); if (!kosa) ARRAY_elementi[kipengee_Marejeleo] = kijenzi; 넣기(kipengee_Marejeleo, 2); continue;
            }
            if (thamani == 190) {
                int kipengee_Marejeleo = 빼기(2);
                if (객체유효(kipengee_Marejeleo)) { int 비교자리 = 힙[kipengee_Marejeleo]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) kushindwa_thamani("not an array"); else 넣기(힙[kipengee_Marejeleo + 1], 1); }
                continue;
            }
            if (thamani == 191) {
                int kipengee_Marejeleo = 빼기(2); if (객체유효(kipengee_Marejeleo)) { if (힙[kipengee_Marejeleo] != 9) kushindwa_thamani("athrow requires supported Throwable"); else { 던진객체 = kipengee_Marejeleo; kosa = true; } }
                continue;
            }
            if (thamani == 192 || thamani == 193) {
                int jina_kisobadilika = tabaka_jina_SMS(명상수()), kipengee_Marejeleo = 빼기(2); boolean 일치여부 = 맞는객체(kipengee_Marejeleo, jina_kisobadilika);
                if (thamani == 193) 넣기(kipengee_Marejeleo != 0 && 일치여부 ? 1 : 0, 1);
                else { if (!일치여부 && !kosa) kushindwa_thamani("ClassCastException"); 넣기(kipengee_Marejeleo, 2); }
                continue;
            }
            if (thamani == 170 || thamani == 171) {
                int 읽는자리 = endesha + 1, faili_kielezo = fremu_mbinu[fremu_kielezo], Kitufe_Marejeleo = 빼기(1);
                while ((읽는자리 - mbinu_Anza[faili_kielezo]) % 4 != 0) 읽는자리++;
                int lengo_anwani = 위치정수(읽는자리);
                if (thamani == 170) { int 낮은값 = 위치정수(읽는자리 + 4), 높은값 = 위치정수(읽는자리 + 8); if (Kitufe_Marejeleo >= 낮은값 && Kitufe_Marejeleo <= 높은값) lengo_anwani = 위치정수(읽는자리 + 12 + (Kitufe_Marejeleo - 낮은값) * 4); }
                else { int 총수 = 위치정수(읽는자리 + 4); for (int kitanzi_kielezo = 0; kitanzi_kielezo < 총수; kitanzi_kielezo++) if (위치정수(읽는자리 + 8 + kitanzi_kielezo * 8) == Kitufe_Marejeleo) lengo_anwani = 위치정수(읽는자리 + 12 + kitanzi_kielezo * 8); }
                hamisha_thamani(endesha + lengo_anwani); continue;
            }
            if (thamani == 200) { hamisha_thamani(endesha + 위치정수(endesha + 1)); continue; }
            if (thamani == 194 || thamani == 195) {
                int kipengee_Marejeleo = 빼기(2);
                if (thamani == 195) 잠금풀기(kipengee_Marejeleo);
                else if (!잠금얻기(kipengee_Marejeleo) && !kosa) { 넣기(kipengee_Marejeleo, 2); 틀위치[fremu_kielezo] = endesha; }
                continue;
            }
            if (thamani == 196) {
                int amri_msimbo = 명바(), 항목자리 = 명짧();
                if (amri_msimbo == 21 || amri_msimbo == 25) 지역읽기(항목자리, amri_msimbo == 21 ? 1 : 2);
                else if (amri_msimbo == 54 || amri_msimbo == 58) andika_jirani(항목자리, amri_msimbo == 54 ? 1 : 2);
                else if (amri_msimbo == 132) { int 변화량 = (short)명짧(); 지역읽기(항목자리, 1); 넣기(빼기(1) + 변화량, 1); andika_jirani(항목자리, 1); }
                else kushindwa_thamani("unsupported wide opcode");
                continue;
            }
            kushindwa_thamani("unsupported bytecode");
        }
    }
    static int gundua_tabaka_Ufafanuzi(int Jina) {
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 종수; kitanzi_kielezo++) if (tabaka_Ufafanuzi_jina[kitanzi_kielezo] != 0 && 같은말(tabaka_Ufafanuzi_jina[kitanzi_kielezo], Jina)) return kitanzi_kielezo;
        return pakia_tabaka_Ufafanuzi(kisobadilika_SMS(Jina));
    }
    static int pakia_tabaka_Ufafanuzi(int jina_tungo) {
        if (!kipengee_thamani(jina_tungo, 1)) return -1;
        int urefu_thamani = 힙[jina_tungo + 1];
        if (urefu_thamani < 1 || urefu_thamani > 505 || 종수 == 16) { kushindwa_thamani("class name/count limit"); return -1; }
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < urefu_thamani; kitanzi_kielezo++) { int msimbo_wa_kibambo = 힙[jina_tungo + 2 + kitanzi_kielezo]; faili_jina_SMS[kitanzi_kielezo] = msimbo_wa_kibambo == '/' ? '.' : msimbo_wa_kibambo; }
        faili_jina_SMS[urefu_thamani] = '.'; faili_jina_SMS[urefu_thamani + 1] = 'c'; faili_jina_SMS[urefu_thamani + 2] = 'l'; faili_jina_SMS[urefu_thamani + 3] = 'a'; faili_jina_SMS[urefu_thamani + 4] = 's'; faili_jina_SMS[urefu_thamani + 5] = 's'; faili_jina_SMS[urefu_thamani + 6] = 0;
        int panga_ukubwa = mtumiaji.파일읽기(faili_jina_SMS, 임시파일);
        if (panga_ukubwa < 0) { kushindwa_thamani("ClassNotFoundException"); return -1; }
        int tabaka_Ufafanuzi = 종수++; tabaka_Ufafanuzi_panga_ukubwa[tabaka_Ufafanuzi] = panga_ukubwa;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < panga_ukubwa; kitanzi_kielezo++) faili[tabaka_Ufafanuzi * 16384 + kitanzi_kielezo] = 임시파일[kitanzi_kielezo];
        클래스읽기(tabaka_Ufafanuzi); if (kosa) return -1;
        int halisi_data = kisobadilika_SMS(tabaka_Ufafanuzi_jina[tabaka_Ufafanuzi]);
        if (!글같음(halisi_data, jina_tungo, true)) { kushindwa_thamani("class name does not match file"); return -1; }
        int 부모 = 종부모[tabaka_Ufafanuzi];
        if (부모 != 0 && !Neno_SMS(부모, "java/lang/Object") && !Neno_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = gundua_tabaka_Ufafanuzi(부모);
            if (kosa || 위 < 0) return -1;
            int 읽는자리 = 위, 단계수 = 0;
            while (읽는자리 >= 0 && 단계수++ < 16) {
                if (읽는자리 == tabaka_Ufafanuzi) { kushindwa_thamani("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int faili_kielezo = 0; faili_kielezo < 칸수; faili_kielezo++) if (Sloti_mmiliki[faili_kielezo] == tabaka_Ufafanuzi && (Sloti_Vibali[faili_kielezo] & 8) == 0) 칸위치[faili_kielezo] += 시작변위;
            종칸수[tabaka_Ufafanuzi] += 시작변위;
        }
        return tabaka_Ufafanuzi;
    }
    static int 부모종(int tabaka_Ufafanuzi) {
        int Jina = 종부모[tabaka_Ufafanuzi];
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 종수; kitanzi_kielezo++) if (Jina != 0 && tabaka_Ufafanuzi_jina[kitanzi_kielezo] != 0 && 같은말(tabaka_Ufafanuzi_jina[kitanzi_kielezo], Jina)) return kitanzi_kielezo;
        return -1;
    }
    static int gundua_mbinu(int tabaka_Ufafanuzi, int Jina, int umbiza_thamani) {
        for (int 깊이 = 0; tabaka_Ufafanuzi >= 0 && 깊이 < 16; 깊이++, tabaka_Ufafanuzi = 부모종(tabaka_Ufafanuzi)) {
            for (int kitanzi_kielezo = 0; kitanzi_kielezo < 함수수; kitanzi_kielezo++) if (mbinu_mmiliki[kitanzi_kielezo] == tabaka_Ufafanuzi && 같은말(mbinu_jina_SMS[kitanzi_kielezo], Jina) && 같은말(mbinu_aina[kitanzi_kielezo], umbiza_thamani)) return kitanzi_kielezo;
        }
        return -1;
    }
    static int jina_mbinu(int tabaka_Ufafanuzi, String Jina, String umbiza_thamani) {
        for (int 깊이 = 0; tabaka_Ufafanuzi >= 0 && 깊이 < 16; 깊이++, tabaka_Ufafanuzi = 부모종(tabaka_Ufafanuzi))
            for (int kitanzi_kielezo = 0; kitanzi_kielezo < 함수수; kitanzi_kielezo++) if (mbinu_mmiliki[kitanzi_kielezo] == tabaka_Ufafanuzi && Neno_SMS(mbinu_jina_SMS[kitanzi_kielezo], Jina) && Neno_SMS(mbinu_aina[kitanzi_kielezo], umbiza_thamani)) return kitanzi_kielezo;
        return -1;
    }
    static int 형종류(int Jina) { return faili[상가[Jina]] == 'L' || faili[상가[Jina]] == '[' ? 2 : 1; }
    static boolean anzilisha(int tabaka_Ufafanuzi, int amri_Anza) {
        if (tabaka_Ufafanuzi < 0 || kosa) return false;
        if (tabaka_Ufafanuzi_hali[tabaka_Ufafanuzi] == 3) { kushindwa_thamani("NoClassDefFoundError: initialization failed"); return false; }
        if (tabaka_Ufafanuzi_hali[tabaka_Ufafanuzi] == 1 && tabaka_mtungo[tabaka_Ufafanuzi] != 현재가닥) { 틀위치[fremu_kielezo] = amri_Anza; 바꿈요청 = true; return false; }
        if (tabaka_Ufafanuzi_hali[tabaka_Ufafanuzi] != 0) return true;
        int 위 = 부모종(tabaka_Ufafanuzi);
        if (위 >= 0 && !anzilisha(위, amri_Anza)) return false;
        tabaka_Ufafanuzi_hali[tabaka_Ufafanuzi] = 1; tabaka_mtungo[tabaka_Ufafanuzi] = 현재가닥;
        if (anzilisha_tabaka_Ufafanuzi[tabaka_Ufafanuzi] != 0) {
            틀위치[fremu_kielezo] = amri_Anza;
            호출(anzilisha_tabaka_Ufafanuzi[tabaka_Ufafanuzi] - 1); if (!kosa) anzilisha_fremu[fremu_kielezo] = tabaka_Ufafanuzi + 1;
            return false;
        }
        tabaka_Ufafanuzi_hali[tabaka_Ufafanuzi] = 2; return true;
    }
    static void 필드호출(int kielezo, int amri, int endesha) {
        if (!hundi_kisobadilika(kielezo, 9)) return;
        int mmiliki_thamani = tabaka_jina_SMS(상가[kielezo]), Jina = Marejeleo_jina(상나[kielezo]), umbiza_thamani = Marejeleo_aina(상나[kielezo]);
        if (Neno_SMS(mmiliki_thamani, "java/lang/System") && (Neno_SMS(Jina, "out") || Neno_SMS(Jina, "err")) && Neno_SMS(umbiza_thamani, "Ljava/io/PrintStream;") && amri == 178) { 넣기(-1, 2); return; }
        int tabaka_Ufafanuzi = gundua_tabaka_Ufafanuzi(mmiliki_thamani); if (tabaka_Ufafanuzi < 0 || kosa) return;
        int 찾음 = -1;
        for (int 읽는자리 = tabaka_Ufafanuzi, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int faili_kielezo = 0; faili_kielezo < 칸수; faili_kielezo++) if (Sloti_mmiliki[faili_kielezo] == 읽는자리 && 같은말(Sloti_jina[faili_kielezo], Jina) && 같은말(Sloti_aina[faili_kielezo], umbiza_thamani)) 찾음 = faili_kielezo;
        if (찾음 < 0) { kushindwa_thamani("NoSuchFieldError"); return; }
        boolean tuli_thamani = amri == 178 || amri == 179;
        if (tuli_thamani != ((Sloti_Vibali[찾음] & 8) != 0)) { kushindwa_thamani("field static/instance mismatch"); return; }
        if (tuli_thamani && !anzilisha(Sloti_mmiliki[찾음], endesha)) return;
        int aina_thamani = 형종류(umbiza_thamani), thamani = 0;
        if (amri == 179 || amri == 181) thamani = 빼기(aina_thamani);
        if (tuli_thamani) { if (amri == 178) 넣기(Sloti_data[찾음], aina_thamani); else if (!kosa) Sloti_data[찾음] = thamani; return; }
        int kipengee_Marejeleo = 빼기(2);
        if (!객체유효(kipengee_Marejeleo)) return;
        if (힙[kipengee_Marejeleo] < 32 || !종포함(힙[kipengee_Marejeleo] - 32, mmiliki_thamani)) { kushindwa_thamani("field receiver type mismatch"); return; }
        int 보관칸 = kipengee_Marejeleo + 2 + 칸위치[찾음];
        if (amri == 180) 넣기(힙[보관칸], aina_thamani);
        else if (!kosa) { 힙[보관칸] = thamani; 힙참조[보관칸] = aina_thamani == 2 ? 1 : 0; }
    }
    static boolean 종포함(int tabaka_Ufafanuzi, int Jina) {
        for (int 중첩깊이 = 0; tabaka_Ufafanuzi >= 0 && 중첩깊이 < 16; 중첩깊이++, tabaka_Ufafanuzi = 부모종(tabaka_Ufafanuzi)) {
            if (같은말(tabaka_Ufafanuzi_jina[tabaka_Ufafanuzi], Jina) || (종부모[tabaka_Ufafanuzi] != 0 && 같은말(종부모[tabaka_Ufafanuzi], Jina))) return true;
            for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[tabaka_Ufafanuzi]; 안쪽자리++) if (같은말(tabaka_kiolesura[tabaka_Ufafanuzi * 16 + 안쪽자리], Jina)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int baiti_data, boolean njia) {
        if (첫값 == baiti_data) return true;
        if (첫값 <= 0 || baiti_data <= 0 || 힙[첫값] != 1 || 힙[baiti_data] != 1 || 힙[첫값 + 1] != 힙[baiti_data + 1]) return false;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 힙[첫값 + 1]; kitanzi_kielezo++) {
            int jira_x = 힙[첫값 + 2 + kitanzi_kielezo], Kitufe_cha_Y_kiratibu = 힙[baiti_data + 2 + kitanzi_kielezo];
            if (njia) { if (jira_x == '.') jira_x = '/'; if (Kitufe_cha_Y_kiratibu == '.') Kitufe_cha_Y_kiratibu = '/'; }
            if (jira_x != Kitufe_cha_Y_kiratibu) return false;
        }
        return true;
    }
    static boolean 객체유효(int kipengee_Marejeleo) {
        if (kipengee_Marejeleo == 0) { kushindwa_thamani("NullPointerException"); return false; }
        if (kipengee_Marejeleo < 1 || kipengee_Marejeleo >= 힙끝 || 힙폭[kipengee_Marejeleo] < 2 || 힙[kipengee_Marejeleo] == 0) { kushindwa_thamani("invalid object reference"); return false; }
        return true;
    }
    static void linda_thamani(int kipengee_Marejeleo) {
        if (kipengee_Marejeleo > 0 && kipengee_Marejeleo < 힙끝 && 힙폭[kipengee_Marejeleo] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = kipengee_Marejeleo;
    }
    static void onyesha_thamani(int kipengee_Marejeleo) {
        if (kipengee_Marejeleo > 0 && kipengee_Marejeleo < 힙끝 && 힙폭[kipengee_Marejeleo] >= 2 && 힙[kipengee_Marejeleo] != 0 && 힙표시[kipengee_Marejeleo] == 0) {
            힙표시[kipengee_Marejeleo] = 1; 표시대기[표시수++] = kipengee_Marejeleo;
        }
    }
    static void 수거() {
        표시수 = 0; 수거횟수++;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) 힙표시[검사자리] = 0;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < tungo_Marejeleo.length; kitanzi_kielezo++) onyesha_thamani(tungo_Marejeleo[kitanzi_kielezo]);
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 칸수; kitanzi_kielezo++) if ((Sloti_Vibali[kitanzi_kielezo] & 8) != 0 && 형종류(Sloti_aina[kitanzi_kielezo]) == 2) onyesha_thamani(Sloti_data[kitanzi_kielezo]);
        for (int 임시값 = 0; 임시값 < 가닥수; 임시값++) {
            onyesha_thamani(mtungo_kipengee[임시값]); onyesha_thamani(mtungo_lengo[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? fremu_kielezo : mtungo_fremu[임시값];
            for (int faili_kielezo = 임시값 * 32; faili_kielezo <= 꼭대기자리; faili_kielezo++) {
                for (int 안쪽자리 = 0; 안쪽자리 < 함수지역[fremu_mbinu[faili_kielezo]]; 안쪽자리++) if (jirani_aina[faili_kielezo * 128 + 안쪽자리] == 2) onyesha_thamani(jirani_thamani[faili_kielezo * 128 + 안쪽자리]);
                for (int 안쪽자리 = 0; 안쪽자리 < fremu_Mpororo[faili_kielezo]; 안쪽자리++) if (스택형[faili_kielezo * 128 + 안쪽자리] == 2) onyesha_thamani(스택값[faili_kielezo * 128 + 안쪽자리]);
            }
        }
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 화면참조.length; kitanzi_kielezo++) onyesha_thamani(화면참조[kitanzi_kielezo]);
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 나중수; kitanzi_kielezo++) onyesha_thamani(나중실행[kitanzi_kielezo]);
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < Store_namba_kamili.length; kitanzi_kielezo++) onyesha_thamani(Store_namba_kamili[kitanzi_kielezo]);
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 종수; kitanzi_kielezo++) onyesha_thamani(종잠금[kitanzi_kielezo]);
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (잠금깊이[검사자리] > 0) onyesha_thamani(검사자리);
        onyesha_thamani(던진객체);
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 잠시수; kitanzi_kielezo++) onyesha_thamani(잠시참조[kitanzi_kielezo]);
        while (표시수 > 0) {
            int kipengee_Marejeleo = 표시대기[--표시수], kategoria_msimbo = 힙[kipengee_Marejeleo];
            for (int kitanzi_kielezo = kipengee_Marejeleo + 2; kitanzi_kielezo < kipengee_Marejeleo + 힙폭[kipengee_Marejeleo]; kitanzi_kielezo++) if (kategoria_msimbo == 3 || kategoria_msimbo == 4 || 힙참조[kitanzi_kielezo] != 0) onyesha_thamani(힙[kitanzi_kielezo]);
        }
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙표시[검사자리] == 0) 힙[검사자리] = 0;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙[검사자리] == 0) {
            while (검사자리 + 힙폭[검사자리] < 힙끝 && 힙[검사자리 + 힙폭[검사자리]] == 0) { int 다음자리 = 검사자리 + 힙폭[검사자리]; 힙폭[검사자리] += 힙폭[다음자리]; 힙폭[다음자리] = 0; }
            if (검사자리 + 힙폭[검사자리] == 힙끝) { 힙끝 = 검사자리; break; }
        }
    }
    static int 새기억(int 종류, int urefu_thamani) {
        if (urefu_thamani < 0) { kushindwa_thamani("NegativeArraySizeException"); return 0; }
        if (urefu_thamani > 힙.length - 3) { kushindwa_thamani("object heap exhausted"); return 0; }
        int 필요수 = urefu_thamani + 2, kipengee_Marejeleo = 0;
        if (필요수 <= 힙.length - 힙끝) { kipengee_Marejeleo = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { kipengee_Marejeleo = 읽는자리; break; }
            if (kipengee_Marejeleo != 0) {
                int 남은길이 = 힙폭[kipengee_Marejeleo] - 필요수;
                if (남은길이 >= 2) { 힙폭[kipengee_Marejeleo + 필요수] = 남은길이; 힙[kipengee_Marejeleo + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { kipengee_Marejeleo = 힙끝; 힙끝 += 필요수; }
        }
        if (kipengee_Marejeleo == 0) { kushindwa_thamani("object heap exhausted"); return 0; }
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 필요수; kitanzi_kielezo++) { 힙[kipengee_Marejeleo + kitanzi_kielezo] = 0; 힙참조[kipengee_Marejeleo + kitanzi_kielezo] = 0; 힙폭[kipengee_Marejeleo + kitanzi_kielezo] = 0; }
        ARRAY_elementi[kipengee_Marejeleo] = 0;
        힙폭[kipengee_Marejeleo] = 필요수; 힙[kipengee_Marejeleo] = 종류; 힙[kipengee_Marejeleo + 1] = urefu_thamani; linda_thamani(kipengee_Marejeleo); return kipengee_Marejeleo;
    }
    static int vighairi_tabaka(String jina_kisobadilika) {
        if (자바도구.같음(jina_kisobadilika, "java/lang/Throwable")) return 1;
        if (자바도구.같음(jina_kisobadilika, "java/lang/Exception")) return 2;
        if (자바도구.같음(jina_kisobadilika, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(jina_kisobadilika, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(jina_kisobadilika, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(jina_kisobadilika, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(jina_kisobadilika, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(jina_kisobadilika, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(jina_kisobadilika, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(jina_kisobadilika, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(jina_kisobadilika, "java/io/IOException")) return 11;
        if (자바도구.같음(jina_kisobadilika, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(jina_kisobadilika, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(jina_kisobadilika, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(jina_kisobadilika, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int vighairi_kisobadilika(int Jina) {
        for (int kitanzi_kielezo = 1; kitanzi_kielezo <= 41; kitanzi_kielezo++) if (Neno_SMS(Jina, vighairi_jina(kitanzi_kielezo))) return kitanzi_kielezo;
        return 0;
    }
    static String vighairi_jina(int akaunti_thamani) {
        if (akaunti_thamani == 40) return "java/lang/InterruptedException";
        if (akaunti_thamani == 41) return "한국어/자체/대기중단예외";
        if (akaunti_thamani == 39) return "java/net/SocketException";
        if (akaunti_thamani == 20) return "한국어/자체/vighairi";
        if (akaunti_thamani == 21) return "한국어/자체/실행예외";
        if (akaunti_thamani == 22) return "한국어/자체/I_T_vighairi";
        if (akaunti_thamani == 23) return "한국어/자체/대기시간초과예외";
        if (akaunti_thamani == 24) return "한국어/자체/주소확인예외";
        if (akaunti_thamani == 25) return "한국어/자체/파일없음예외";
        if (akaunti_thamani == 26) return "한국어/자체/통신예외";
        if (akaunti_thamani == 27) return "한국어/자체/batili_hoja_vighairi";
        if (akaunti_thamani == 28) return "한국어/자체/숫자형식예외";
        if (akaunti_thamani == 29) return "한국어/자체/범위예외";
        if (akaunti_thamani == 30) return "한국어/자체/배열범위예외";
        if (akaunti_thamani == 31) return "한국어/자체/문자열범위예외";
        if (akaunti_thamani == 32) return "한국어/자체/batili_Marejeleo_vighairi";
        if (akaunti_thamani == 33) return "한국어/자체/산술예외";
        if (akaunti_thamani == 34) return "한국어/자체/hali_vighairi";
        if (akaunti_thamani == 35) return "한국어/자체/aina_cheza_vighairi";
        if (akaunti_thamani == 36) return "한국어/자체/음수배열크기예외";
        if (akaunti_thamani == 37) return "한국어/자체/ARRAY_Store_kushindwa";
        if (akaunti_thamani == 38) return "한국어/자체/mtungo_hali_vighairi";
        if (akaunti_thamani == 1) return "java/lang/Throwable"; if (akaunti_thamani == 2) return "java/lang/Exception";
        if (akaunti_thamani == 3) return "java/lang/RuntimeException"; if (akaunti_thamani == 4) return "java/lang/ArithmeticException";
        if (akaunti_thamani == 5) return "java/lang/NullPointerException"; if (akaunti_thamani == 6) return "java/lang/IndexOutOfBoundsException";
        if (akaunti_thamani == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (akaunti_thamani == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (akaunti_thamani == 9) return "java/lang/IllegalArgumentException"; if (akaunti_thamani == 10) return "java/lang/NumberFormatException";
        if (akaunti_thamani == 11) return "java/io/IOException"; if (akaunti_thamani == 12) return "java/io/FileNotFoundException";
        if (akaunti_thamani == 17) return "java/lang/ArrayStoreException";
        if (akaunti_thamani == 18) return "java/net/UnknownHostException";
        if (akaunti_thamani == 19) return "java/net/SocketTimeoutException";
        if (akaunti_thamani == 16) return "java/lang/IllegalThreadStateException";
        if (akaunti_thamani == 13) return "java/lang/IllegalStateException"; if (akaunti_thamani == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int akaunti_thamani) {
        if (akaunti_thamani == 40) return 2;
        if (akaunti_thamani == 41) return 40;
        if (akaunti_thamani == 39) return 11;
        if (akaunti_thamani == 1) return 0;
        if (akaunti_thamani == 2) return 1;
        if (akaunti_thamani == 3) return 2;
        if (akaunti_thamani == 4) return 3;
        if (akaunti_thamani == 5) return 3;
        if (akaunti_thamani == 6) return 3;
        if (akaunti_thamani == 7) return 6;
        if (akaunti_thamani == 8) return 6;
        if (akaunti_thamani == 9) return 3;
        if (akaunti_thamani == 10) return 9;
        if (akaunti_thamani == 11) return 2;
        if (akaunti_thamani == 12) return 11;
        if (akaunti_thamani == 13) return 3;
        if (akaunti_thamani == 14) return 3;
        if (akaunti_thamani == 15) return 3;
        if (akaunti_thamani == 16) return 9;
        if (akaunti_thamani == 17) return 3;
        if (akaunti_thamani == 18) return 11;
        if (akaunti_thamani == 19) return 11;
        if (akaunti_thamani == 20) return 2;
        if (akaunti_thamani == 21) return 3;
        if (akaunti_thamani == 22) return 11;
        if (akaunti_thamani == 23) return 22;
        if (akaunti_thamani == 24) return 22;
        if (akaunti_thamani == 25) return 22;
        if (akaunti_thamani == 26) return 22;
        if (akaunti_thamani == 27) return 9;
        if (akaunti_thamani == 28) return 27;
        if (akaunti_thamani == 29) return 6;
        if (akaunti_thamani == 30) return 29;
        if (akaunti_thamani == 31) return 29;
        if (akaunti_thamani == 32) return 5;
        if (akaunti_thamani == 33) return 4;
        if (akaunti_thamani == 34) return 13;
        if (akaunti_thamani == 35) return 14;
        if (akaunti_thamani == 36) return 15;
        if (akaunti_thamani == 37) return 17;
        if (akaunti_thamani == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int halisi_thamani, int 요구값) {
        for (int 깊이 = 0; halisi_thamani != 0 && 깊이 < 16; 깊이++, halisi_thamani = 예외부모(halisi_thamani))
            if (halisi_thamani == 요구값) return true;
        return false;
    }
    static void 예외던짐(int akaunti_thamani, String NISOME_Marejeleo) {
        int kipengee_Marejeleo = 새기억(9, 2); if (kosa) return;
        힙[kipengee_Marejeleo + 2] = akaunti_thamani; 힙[kipengee_Marejeleo + 3] = mwenyeji_kibambo(NISOME_Marejeleo); 힙참조[kipengee_Marejeleo + 3] = 1;
        던진객체 = kipengee_Marejeleo; kosa = true;
    }
    static boolean 맞는객체(int kipengee_Marejeleo, int Jina) {
        if (kipengee_Marejeleo == 0) return true;
        if (!객체유효(kipengee_Marejeleo)) return false;
        int kategoria_msimbo = 힙[kipengee_Marejeleo];
        if (Neno_SMS(Jina, "java/lang/Object")) return true;
        if (kategoria_msimbo >= 32) return 종포함(kategoria_msimbo - 32, Jina);
        if (kategoria_msimbo == 9) { int lengo_anwani = vighairi_kisobadilika(Jina); return lengo_anwani != 0 && 예외포함(힙[kipengee_Marejeleo + 2], lengo_anwani); }
        if (kategoria_msimbo == 1) return Neno_SMS(Jina, "java/lang/String") || Neno_SMS(Jina, "java/lang/CharSequence");
        if (kategoria_msimbo == 4) return Neno_SMS(Jina, "java/lang/StringBuilder") || Neno_SMS(Jina, "java/lang/CharSequence");
        if (kategoria_msimbo == 10) return Neno_SMS(Jina, "java/util/ArrayList") || Neno_SMS(Jina, "java/util/List");
        if (kategoria_msimbo == 11) return Neno_SMS(Jina, "java/util/HashMap") || Neno_SMS(Jina, "java/util/Map");
        if (kategoria_msimbo == 12) return Neno_SMS(Jina, "java/lang/Integer") || Neno_SMS(Jina, "java/lang/Number");
        if (kategoria_msimbo >= 24 && kategoria_msimbo <= 28 && 힙[kipengee_Marejeleo + 13] != 0) return 한국어화면종(Jina) == kategoria_msimbo || Neno_SMS(Jina, "한국어/자체/화면구성요소");
        if (kategoria_msimbo >= 24 && kategoria_msimbo <= 28) return (한국어화면종(Jina) == 0 && 화면종(Jina) == kategoria_msimbo) || Neno_SMS(Jina, "java/awt/Component") || Neno_SMS(Jina, "java/awt/Container") || Neno_SMS(Jina, "javax/swing/JComponent");
        if (kategoria_msimbo == 29) return Neno_SMS(Jina, 힙[kipengee_Marejeleo + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (kategoria_msimbo == 30) return Neno_SMS(Jina, "java/awt/FlowLayout") || Neno_SMS(Jina, "java/awt/LayoutManager");
        if (kategoria_msimbo == 17) return Neno_SMS(Jina, "java/net/Socket");
        if (kategoria_msimbo == 18) return Neno_SMS(Jina, "java/net/ServerSocket");
        if (kategoria_msimbo == 19) return Neno_SMS(Jina, 힙[kipengee_Marejeleo + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (kategoria_msimbo == 14) return Neno_SMS(Jina, "java/net/InetAddress");
        if (kategoria_msimbo == 15) return Neno_SMS(Jina, "java/net/DatagramSocket");
        if (kategoria_msimbo == 16) return Neno_SMS(Jina, "java/net/DatagramPacket");
        if (kategoria_msimbo == 13) return Neno_SMS(Jina, 힙[kipengee_Marejeleo + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (kategoria_msimbo == 2) return Neno_SMS(Jina, "[I"); if (kategoria_msimbo == 20) return Neno_SMS(Jina, "[B"); if (kategoria_msimbo == 21) return Neno_SMS(Jina, "[Z");
        if (kategoria_msimbo == 22) return Neno_SMS(Jina, "[C"); if (kategoria_msimbo == 23) return Neno_SMS(Jina, "[S");
        if (kategoria_msimbo != 3) return false;
        if (Neno_SMS(Jina, "[Ljava/lang/Object;")) return true;
        int kijenzi = ARRAY_elementi[kipengee_Marejeleo];
        if (kijenzi == -1) return Neno_SMS(Jina, "[Ljava/lang/String;") || Neno_SMS(Jina, "[Ljava/lang/CharSequence;");
        if (kijenzi == 0) return false;
        if (배열종비교(kijenzi, Jina)) return true;
        if ((Neno_SMS(kijenzi, "java/lang/String") || Neno_SMS(kijenzi, "java/lang/StringBuilder")) && Neno_SMS(Jina, "[Ljava/lang/CharSequence;")) return true;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 종수; kitanzi_kielezo++) if (같은말(tabaka_Ufafanuzi_jina[kitanzi_kielezo], kijenzi)) {
            for (int msimbo_wa_kibambo = kitanzi_kielezo, 중첩깊이 = 0; msimbo_wa_kibambo >= 0 && 중첩깊이 < 16; 중첩깊이++, msimbo_wa_kibambo = 부모종(msimbo_wa_kibambo)) {
                if (배열종비교(종부모[msimbo_wa_kibambo], Jina)) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[msimbo_wa_kibambo]; 안쪽자리++) if (배열종비교(tabaka_kiolesura[msimbo_wa_kibambo * 16 + 안쪽자리], Jina)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int jina_kisobadilika, int 형식참조) {
        int 검사자리 = 상가[형식참조], 항목수 = 상나[형식참조];
        if (jina_kisobadilika == 0 || 항목수 < 4 || faili[검사자리] != '[' || faili[검사자리 + 1] != 'L' || faili[검사자리 + 항목수 - 1] != ';' || 상나[jina_kisobadilika] != 항목수 - 3) return false;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 항목수 - 3; kitanzi_kielezo++) if (faili[상가[jina_kisobadilika] + kitanzi_kielezo] != faili[검사자리 + 2 + kitanzi_kielezo]) return false;
        return true;
    }
    static void kishiko_vighairi() {
        if (던진객체 == 0) return;
        kosa = false;
        while (fremu_kielezo >= 현재가닥 * 32) {
            int faili_kielezo = fremu_mbinu[fremu_kielezo], 읽는자리 = fremu_agizo[fremu_kielezo];
            for (int kitanzi_kielezo = 0; kitanzi_kielezo < 잡기수; kitanzi_kielezo++) if (잡기함수[kitanzi_kielezo] == faili_kielezo && 읽는자리 >= 잡기시작[kitanzi_kielezo] && 읽는자리 < 잡기끝[kitanzi_kielezo]
                && (잡기종[kitanzi_kielezo] == 0 || 맞는객체(던진객체, 잡기종[kitanzi_kielezo]))) {
                틀위치[fremu_kielezo] = 잡기위치[kitanzi_kielezo]; fremu_Mpororo[fremu_kielezo] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (anzilisha_fremu[fremu_kielezo] != 0) tabaka_Ufafanuzi_hali[anzilisha_fremu[fremu_kielezo] - 1] = 3;
            if (틀잠금[fremu_kielezo] != 0) { 잠금풀기(틀잠금[fremu_kielezo]); 틀잠금[fremu_kielezo] = 0; }
            fremu_kielezo--;
        }
        mtumiaji.andika("Uncaught ");
        if (힙[던진객체] == 9) { mtumiaji.andika(vighairi_jina(힙[던진객체 + 2])); mtumiaji.andika(": "); andika_SMS(힙[던진객체 + 3]); }
        else mtumiaji.andika("user exception");
        mtumiaji.andika_kibambo_thamani(10); 던진객체 = 0; kosa = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void Mpororo_agizo(int amri_msimbo) {
        int 첫값 = 빼기(0), 첫형식 = 반환형;
        if (amri_msimbo == 87) return;
        if (amri_msimbo == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int baiti_data = 빼기(0), 둘째형식 = 반환형;
        if (amri_msimbo == 88) return;
        if (amri_msimbo == 90) { 넣기(첫값, 첫형식); 넣기(baiti_data, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (amri_msimbo == 92) { 넣기(baiti_data, 둘째형식); 넣기(첫값, 첫형식); 넣기(baiti_data, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (amri_msimbo == 95) { 넣기(첫값, 첫형식); 넣기(baiti_data, 둘째형식); return; }
        int msimbo_wa_kibambo = 빼기(0), 셋째형식 = 반환형;
        if (amri_msimbo == 91) { 넣기(첫값, 첫형식); 넣기(msimbo_wa_kibambo, 셋째형식); 넣기(baiti_data, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (amri_msimbo == 93) { 넣기(baiti_data, 둘째형식); 넣기(첫값, 첫형식); 넣기(msimbo_wa_kibambo, 셋째형식); 넣기(baiti_data, 둘째형식); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = 반환형;
        넣기(baiti_data, 둘째형식); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(msimbo_wa_kibambo, 셋째형식); 넣기(baiti_data, 둘째형식); 넣기(첫값, 첫형식);
    }
    static void 새객체(int jina_kisobadilika, int 시작점) {
        int kategoria_msimbo = 0, 유효길이 = 0, vighairi_Marejeleo = vighairi_kisobadilika(jina_kisobadilika);
        if (Neno_SMS(jina_kisobadilika, "java/lang/StringBuilder")) { kategoria_msimbo = 4; 유효길이 = 1; }
        if (Neno_SMS(jina_kisobadilika, "java/io/FileInputStream")) { kategoria_msimbo = 5; 유효길이 = 2; }
        if (Neno_SMS(jina_kisobadilika, "java/io/FileOutputStream")) { kategoria_msimbo = 6; 유효길이 = 2; }
        if (vighairi_Marejeleo != 0) { kategoria_msimbo = 9; 유효길이 = 2; }
        if (Neno_SMS(jina_kisobadilika, "java/util/ArrayList")) { kategoria_msimbo = 10; 유효길이 = 2; }
        if (Neno_SMS(jina_kisobadilika, "java/util/HashMap")) { kategoria_msimbo = 11; 유효길이 = 2; }
        if (Neno_SMS(jina_kisobadilika, "java/lang/Integer")) { kategoria_msimbo = 12; 유효길이 = 1; }
        if (Neno_SMS(jina_kisobadilika, "java/net/Socket")) { kategoria_msimbo = 17; 유효길이 = 5; }
        if (Neno_SMS(jina_kisobadilika, "java/net/ServerSocket")) { kategoria_msimbo = 18; 유효길이 = 5; }
        if (Neno_SMS(jina_kisobadilika, "java/net/DatagramSocket")) { kategoria_msimbo = 15; 유효길이 = 3; }
        if (Neno_SMS(jina_kisobadilika, "java/net/DatagramPacket")) { kategoria_msimbo = 16; 유효길이 = 4; }
        if (Neno_SMS(jina_kisobadilika, "java/lang/Thread") || Neno_SMS(jina_kisobadilika, "한국어/자체/작업가닥")) { kategoria_msimbo = 13; 유효길이 = 2; }
        if (Neno_SMS(jina_kisobadilika, "java/lang/Object")) { kategoria_msimbo = 8; }
        if (kategoria_msimbo == 0 && 화면종(jina_kisobadilika) != 0) { kategoria_msimbo = 화면종(jina_kisobadilika); 유효길이 = 12; }
        if (kategoria_msimbo == 0) {
            int msimbo_wa_kibambo = gundua_tabaka_Ufafanuzi(jina_kisobadilika); if (msimbo_wa_kibambo < 0 || kosa || !anzilisha(msimbo_wa_kibambo, 시작점)) return;
            kategoria_msimbo = 32 + msimbo_wa_kibambo; 유효길이 = 종칸수[msimbo_wa_kibambo];
        }
        int kipengee_Marejeleo = tengea_Hifadhi(kategoria_msimbo, 유효길이); if (kosa) return;
        if (kategoria_msimbo == 13 && Neno_SMS(jina_kisobadilika, "한국어/자체/작업가닥")) 힙[kipengee_Marejeleo + 3] = 1;
        if (kategoria_msimbo >= 24 && kategoria_msimbo <= 28 && 한국어화면종(jina_kisobadilika) != 0) 힙[kipengee_Marejeleo + 13] = 1;
        if (kategoria_msimbo == 5 || kategoria_msimbo == 6 || kategoria_msimbo == 15 || kategoria_msimbo == 17 || kategoria_msimbo == 18) 힙[kipengee_Marejeleo + 2] = -1;
        if (kategoria_msimbo == 9) 힙[kipengee_Marejeleo + 2] = vighairi_Marejeleo;
        넣기(kipengee_Marejeleo, 2);
    }
    static boolean 값같음(int 첫값, int baiti_data) {
        if (첫값 == baiti_data) return true;
        if (첫값 == 0 || baiti_data == 0 || 첫값 < 0 || baiti_data < 0 || 첫값 >= 힙끝 || baiti_data >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[baiti_data] == 1) return 글같음(첫값, baiti_data, false);
        return 힙[첫값] == 12 && 힙[baiti_data] == 12 && 힙[첫값 + 2] == 힙[baiti_data + 2];
    }
    static int 글조각(int kipengee_Marejeleo, int 시작자리, int 끝자리) {
        if (!kipengee_thamani(kipengee_Marejeleo, 1)) return 0;
        if (시작자리 < 0 || 끝자리 < 시작자리 || 끝자리 > 힙[kipengee_Marejeleo + 1]) { kushindwa_thamani("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = tengea_Hifadhi(1, 끝자리 - 시작자리); if (kosa) return 0;
        for (int kitanzi_kielezo = 시작자리; kitanzi_kielezo < 끝자리; kitanzi_kielezo++) 힙[반환값 + 2 + kitanzi_kielezo - 시작자리] = 힙[kipengee_Marejeleo + 2 + kitanzi_kielezo];
        return 반환값;
    }
    static int jiunge_SMS(int 첫값, int baiti_data) {
        if (!kipengee_thamani(첫값, 1) || !kipengee_thamani(baiti_data, 1)) return 0;
        int 항목수 = 힙[첫값 + 1], mbinu_kielezo = 힙[baiti_data + 1], 반환값 = tengea_Hifadhi(1, 항목수 + mbinu_kielezo); if (kosa) return 0;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 항목수; kitanzi_kielezo++) 힙[반환값 + 2 + kitanzi_kielezo] = 힙[첫값 + 2 + kitanzi_kielezo];
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < mbinu_kielezo; kitanzi_kielezo++) 힙[반환값 + 2 + 항목수 + kitanzi_kielezo] = 힙[baiti_data + 2 + kitanzi_kielezo];
        return 반환값;
    }
    static boolean 기본호출(int mmiliki, int jina_kisobadilika, int 서술상수, int amri_msimbo) {
        if (Neno_SMS(mmiliki, "한국어/자체/실행인수") && amri_msimbo == 184) {
            if (Neno_SMS(jina_kisobadilika, "개수") && Neno_SMS(서술상수, "()I")) { 넣기(mtumiaji.인수개수() - 1, 1); return true; }
            if (Neno_SMS(jina_kisobadilika, "SMS") && Neno_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= mtumiaji.인수개수() - 1) 예외던짐(29, "tekeleza_amri 인수 범위를 벗어났습니다");
                else 넣기(mwenyeji_kibambo(mtumiaji.인수(순번 + 1)), 2);
                return true;
            }
            kushindwa_thamani("지원하지 않는 한국어 tekeleza_amri 인수 호출"); return true;
        }
        if (Neno_SMS(mmiliki, "한국어/자체/작업가닥")) { Mchakato_mtungo(jina_kisobadilika, 서술상수, amri_msimbo, true); return true; }
        if (한국어화면소유(mmiliki)) { 한국어화면호출(mmiliki, jina_kisobadilika, 서술상수, amri_msimbo); return true; }
        if (화면소유(mmiliki)) { 화면호출(mmiliki, jina_kisobadilika, 서술상수, amri_msimbo); return true; }
        if (Neno_SMS(mmiliki, "java/net/Socket") || Neno_SMS(mmiliki, "java/net/ServerSocket") || Neno_SMS(mmiliki, "java/io/InputStream") || Neno_SMS(mmiliki, "java/io/OutputStream")) { 흐름호출(mmiliki, jina_kisobadilika, 서술상수, amri_msimbo); return true; }
        if (Neno_SMS(mmiliki, "한국어/자체/kiini_thamani_0611a8a8") && amri_msimbo == 184) {
            if (Neno_SMS(jina_kisobadilika, "화면너비") && Neno_SMS(서술상수, "()I")) { 넣기(mtumiaji.화면너비(), 1); return true; }
            if (Neno_SMS(jina_kisobadilika, "화면높이") && Neno_SMS(서술상수, "()I")) { 넣기(mtumiaji.화면높이(), 1); return true; }
            if (Neno_SMS(jina_kisobadilika, "밀리초") && Neno_SMS(서술상수, "()I")) { 넣기(mtumiaji.밀리초(), 1); return true; }
            if (Neno_SMS(jina_kisobadilika, "그림대기") && Neno_SMS(서술상수, "()I")) { 넣기(mtumiaji.그림대기(), 1); return true; }
            if (Neno_SMS(jina_kisobadilika, "사각형") && Neno_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), Kitufe_cha_Y_kiratibu = 빼기(1), jira_x = 빼기(1); 넣기(mtumiaji.사각형(jira_x, Kitufe_cha_Y_kiratibu, 너비, 높이, 색상), 1); return true; }
        }
        if (Neno_SMS(mmiliki, "java/net/InetAddress") || Neno_SMS(mmiliki, "java/net/DatagramPacket") || Neno_SMS(mmiliki, "java/net/DatagramSocket")) { 통신호출(mmiliki, jina_kisobadilika, 서술상수, amri_msimbo); return true; }
        if (Neno_SMS(mmiliki, "java/lang/Thread")) { 가닥호출(jina_kisobadilika, 서술상수, amri_msimbo); return true; }
        if (Neno_SMS(mmiliki, "java/lang/Object")) {
            if (Neno_SMS(jina_kisobadilika, "<init>") && Neno_SMS(서술상수, "()V") && amri_msimbo == 183) { 객체유효(빼기(2)); return true; }
            if (Neno_SMS(jina_kisobadilika, "equals") && Neno_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int baiti_data = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == baiti_data ? 1 : 0, 1); return true; }
        }
        if (vighairi_kisobadilika(mmiliki) != 0) {
            if (Neno_SMS(jina_kisobadilika, "<init>") && amri_msimbo == 183 && (Neno_SMS(서술상수, "()V") || Neno_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int kisituo = Neno_SMS(서술상수, "()V") ? 0 : 빼기(2), kipengee_Marejeleo = 빼기(2);
                if (kipengee_thamani(kipengee_Marejeleo, 9)) { 힙[kipengee_Marejeleo + 3] = kisituo; 힙참조[kipengee_Marejeleo + 3] = 1; } return true;
            }
            if ((Neno_SMS(jina_kisobadilika, "getMessage") || Neno_SMS(jina_kisobadilika, "설명")) && Neno_SMS(서술상수, "()Ljava/lang/String;")) { int kipengee_Marejeleo = 빼기(2); if (kipengee_thamani(kipengee_Marejeleo, 9)) 넣기(힙[kipengee_Marejeleo + 3], 2); return true; }
        }
        if (Neno_SMS(mmiliki, "java/lang/String")) {
            if (amri_msimbo == 182 && Neno_SMS(jina_kisobadilika, "getBytes") && (Neno_SMS(서술상수, "()[B") || Neno_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int usimbaji_jina = Neno_SMS(서술상수, "()[B") ? 0 : 빼기(2), kipengee_Marejeleo = 빼기(2);
                if (!kipengee_thamani(kipengee_Marejeleo, 1)) return true;
                if (usimbaji_jina != 0 && !글같음(usimbaji_jina, mwenyeji_kibambo("UTF-8"), false) && !글같음(usimbaji_jina, mwenyeji_kibambo("UTF8"), false) && !글같음(usimbaji_jina, mwenyeji_kibambo("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int 항목수 = 힙[kipengee_Marejeleo + 1], 반환값 = tengea_Hifadhi(20, 항목수 * 3), 사용수 = 0; if (kosa) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) {
                    int msimbo_wa_kibambo = 힙[kipengee_Marejeleo + 2 + 안쪽자리];
                    if (msimbo_wa_kibambo >= 0xd800 && msimbo_wa_kibambo <= 0xdbff && 안쪽자리 + 1 < 항목수 && 힙[kipengee_Marejeleo + 3 + 안쪽자리] >= 0xdc00 && 힙[kipengee_Marejeleo + 3 + 안쪽자리] <= 0xdfff) msimbo_wa_kibambo = 0x10000 + ((msimbo_wa_kibambo - 0xd800) << 10) + 힙[kipengee_Marejeleo + 2 + ++안쪽자리] - 0xdc00;
                    else if (msimbo_wa_kibambo >= 0xd800 && msimbo_wa_kibambo <= 0xdfff) msimbo_wa_kibambo = '?';
                    if (msimbo_wa_kibambo < 128) 힙[반환값 + 2 + 사용수++] = msimbo_wa_kibambo;
                    else { int 바이트수 = msimbo_wa_kibambo < 2048 ? 2 : msimbo_wa_kibambo < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((바이트수 == 2 ? 192 : 바이트수 == 3 ? 224 : 240) | msimbo_wa_kibambo >> (6 * (바이트수 - 1))); for (int 비교자리 = 바이트수 - 1; 비교자리 > 0; 비교자리--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | msimbo_wa_kibambo >> (6 * (비교자리 - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (amri_msimbo == 184 && Neno_SMS(jina_kisobadilika, "valueOf") && Neno_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(dijiti_kibambo(빼기(1)), 2); return true; }
            if (amri_msimbo != 182) return false;
            if (Neno_SMS(jina_kisobadilika, "equals") && Neno_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int baiti_data = 빼기(2), 첫값 = 빼기(2); if (kipengee_thamani(첫값, 1)) 넣기(글같음(첫값, baiti_data, false) ? 1 : 0, 1); return true; }
            if (Neno_SMS(jina_kisobadilika, "isEmpty") && Neno_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (kipengee_thamani(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Neno_SMS(jina_kisobadilika, "substring") && (Neno_SMS(서술상수, "(I)Ljava/lang/String;") || Neno_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean 둘째값 = Neno_SMS(서술상수, "(II)Ljava/lang/String;"); int 끝자리 = 둘째값 ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (kipengee_thamani(첫값, 1)) 넣기(글조각(첫값, 시작점, 둘째값 ? 끝자리 : 힙[첫값 + 1]), 2); return true;
            }
            if (Neno_SMS(jina_kisobadilika, "concat") && Neno_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int baiti_data = 빼기(2), 첫값 = 빼기(2); 넣기(jiunge_SMS(첫값, baiti_data), 2); return true; }
            if (Neno_SMS(jina_kisobadilika, "hashCode") && Neno_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), kali_thamani = 0; if (kipengee_thamani(첫값, 1)) { for (int kitanzi_kielezo = 0; kitanzi_kielezo < 힙[첫값 + 1]; kitanzi_kielezo++) kali_thamani = kali_thamani * 31 + 힙[첫값 + 2 + kitanzi_kielezo]; 넣기(kali_thamani, 1); } return true; }
            if (Neno_SMS(jina_kisobadilika, "toString") && Neno_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (kipengee_thamani(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Neno_SMS(mmiliki, "java/lang/Integer")) {
            if (amri_msimbo == 184 && Neno_SMS(jina_kisobadilika, "valueOf") && Neno_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int data_thamani = 빼기(1), kipengee_Marejeleo = data_thamani >= -128 && data_thamani <= 127 ? Store_namba_kamili[data_thamani + 128] : 0; if (kipengee_Marejeleo == 0) { kipengee_Marejeleo = tengea_Hifadhi(12, 1); if (!kosa) { 힙[kipengee_Marejeleo + 2] = data_thamani; if (data_thamani >= -128 && data_thamani <= 127) Store_namba_kamili[data_thamani + 128] = kipengee_Marejeleo; } } 넣기(kipengee_Marejeleo, 2); return true; }
            if (amri_msimbo == 183 && Neno_SMS(jina_kisobadilika, "<init>") && Neno_SMS(서술상수, "(I)V")) { int data_thamani = 빼기(1), kipengee_Marejeleo = 빼기(2); if (kipengee_thamani(kipengee_Marejeleo, 12)) 힙[kipengee_Marejeleo + 2] = data_thamani; return true; }
            if (amri_msimbo == 182 && Neno_SMS(jina_kisobadilika, "intValue") && Neno_SMS(서술상수, "()I")) { int kipengee_Marejeleo = 빼기(2); if (kipengee_thamani(kipengee_Marejeleo, 12)) 넣기(힙[kipengee_Marejeleo + 2], 1); return true; }
            if (amri_msimbo == 184 && Neno_SMS(jina_kisobadilika, "toString") && Neno_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(dijiti_kibambo(빼기(1)), 2); return true; }
        }
        if (Neno_SMS(mmiliki, "java/lang/Math") && amri_msimbo == 184) {
            if (Neno_SMS(jina_kisobadilika, "abs") && Neno_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Neno_SMS(jina_kisobadilika, "min") || Neno_SMS(jina_kisobadilika, "max")) && Neno_SMS(서술상수, "(II)I")) { int baiti_data = 빼기(1), 첫값 = 빼기(1); 넣기(Neno_SMS(jina_kisobadilika, "min") ? (첫값 < baiti_data ? 첫값 : baiti_data) : (첫값 > baiti_data ? 첫값 : baiti_data), 1); return true; }
        }
        if (Neno_SMS(mmiliki, "java/lang/System") && amri_msimbo == 184) {
            if (Neno_SMS(jina_kisobadilika, "gc") && Neno_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Neno_SMS(jina_kisobadilika, "arraycopy") && Neno_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int 항목수 = 빼기(1), fikio_thamani_kielezo = 빼기(1), baiti_data = 빼기(2), 시작자리 = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(baiti_data)) {
                    int kategoria_msimbo = 힙[첫값];
                    if (힙[baiti_data] != kategoria_msimbo || (kategoria_msimbo != 2 && kategoria_msimbo != 3 && (kategoria_msimbo < 20 || kategoria_msimbo > 23))) kushindwa_thamani("arraycopy type mismatch");
                    else if (항목수 < 0 || 시작자리 < 0 || fikio_thamani_kielezo < 0 || 시작자리 > 힙[첫값 + 1] - 항목수 || fikio_thamani_kielezo > 힙[baiti_data + 1] - 항목수) kushindwa_thamani("ArrayIndexOutOfBoundsException");
                    else if (첫값 == baiti_data && fikio_thamani_kielezo > 시작자리) { for (int kitanzi_kielezo = 항목수 - 1; kitanzi_kielezo >= 0; kitanzi_kielezo--) 힙[baiti_data + 2 + fikio_thamani_kielezo + kitanzi_kielezo] = 힙[첫값 + 2 + 시작자리 + kitanzi_kielezo]; }
                    else { for (int kitanzi_kielezo = 0; kitanzi_kielezo < 항목수 && !kosa; kitanzi_kielezo++) { int data_thamani = 힙[첫값 + 2 + 시작자리 + kitanzi_kielezo]; if (kategoria_msimbo != 3 || 배열저장가능(baiti_data, data_thamani)) 힙[baiti_data + 2 + fikio_thamani_kielezo + kitanzi_kielezo] = data_thamani; } }
                }
                return true;
            }
        }
        if (Neno_SMS(mmiliki, "java/util/ArrayList") || Neno_SMS(mmiliki, "java/util/List") || Neno_SMS(mmiliki, "java/util/HashMap") || Neno_SMS(mmiliki, "java/util/Map")) {
            모음호출(mmiliki, jina_kisobadilika, 서술상수, amri_msimbo); return true;
        }
        return false;
    }
    static void 모음늘리기(int kipengee_Marejeleo, int 필요수) {
        int 이전값 = 힙[kipengee_Marejeleo + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int 다음자리 = 용량값 < 8 ? 8 : 용량값 * 2; if (다음자리 < 필요수) 다음자리 = 필요수;
        int data_ARRAY = tengea_Hifadhi(3, 다음자리); if (kosa) return;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 용량값; kitanzi_kielezo++) 힙[data_ARRAY + 2 + kitanzi_kielezo] = 힙[이전값 + 2 + kitanzi_kielezo];
        힙[kipengee_Marejeleo + 2] = data_ARRAY; 힙참조[kipengee_Marejeleo + 2] = 1;
    }
    static void 모음호출(int mmiliki, int jina_kisobadilika, int 서술상수, int amri_msimbo) {
        boolean 대응참조 = Neno_SMS(mmiliki, "java/util/HashMap") || Neno_SMS(mmiliki, "java/util/Map"); int kategoria_msimbo = 대응참조 ? 11 : 10;
        if (Neno_SMS(jina_kisobadilika, "<init>") && amri_msimbo == 183 && Neno_SMS(서술상수, "()V")) { int kipengee_Marejeleo = 빼기(2); if (kipengee_thamani(kipengee_Marejeleo, kategoria_msimbo)) 모음늘리기(kipengee_Marejeleo, 8); return; }
        if (amri_msimbo != 182 && amri_msimbo != 185) { kushindwa_thamani("invalid collection invocation"); return; }
        if (Neno_SMS(jina_kisobadilika, "size") && Neno_SMS(서술상수, "()I") || Neno_SMS(jina_kisobadilika, "isEmpty") && Neno_SMS(서술상수, "()Z")) {
            int kipengee_Marejeleo = 빼기(2); if (kipengee_thamani(kipengee_Marejeleo, kategoria_msimbo)) 넣기(Neno_SMS(jina_kisobadilika, "size") ? 힙[kipengee_Marejeleo + 3] : 힙[kipengee_Marejeleo + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Neno_SMS(jina_kisobadilika, "clear") && Neno_SMS(서술상수, "()V")) { int kipengee_Marejeleo = 빼기(2); if (kipengee_thamani(kipengee_Marejeleo, kategoria_msimbo)) { int data_ARRAY = 힙[kipengee_Marejeleo + 2]; for (int kitanzi_kielezo = 0; kitanzi_kielezo < 힙[data_ARRAY + 1]; kitanzi_kielezo++) 힙[data_ARRAY + 2 + kitanzi_kielezo] = 0; 힙[kipengee_Marejeleo + 3] = 0; } return; }
        if (!대응참조 && Neno_SMS(jina_kisobadilika, "add") && Neno_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int data_thamani = 빼기(2), kipengee_Marejeleo = 빼기(2); if (!kipengee_thamani(kipengee_Marejeleo, 10)) return;
            int 항목수 = 힙[kipengee_Marejeleo + 3]; 모음늘리기(kipengee_Marejeleo, 항목수 + 1); if (!kosa) { 힙[힙[kipengee_Marejeleo + 2] + 2 + 항목수] = data_thamani; 힙[kipengee_Marejeleo + 3] = 항목수 + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Neno_SMS(jina_kisobadilika, "get") || Neno_SMS(jina_kisobadilika, "remove")) && Neno_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Neno_SMS(jina_kisobadilika, "set") && Neno_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Neno_SMS(jina_kisobadilika, "set"); int data_thamani = 지정여부 ? 빼기(2) : 0, 항목자리 = 빼기(1), kipengee_Marejeleo = 빼기(2);
            if (!kipengee_thamani(kipengee_Marejeleo, 10)) return;
            int 항목수 = 힙[kipengee_Marejeleo + 3], data_ARRAY = 힙[kipengee_Marejeleo + 2];
            if (항목자리 < 0 || 항목자리 >= 항목수) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[data_ARRAY + 2 + 항목자리];
            if (지정여부) 힙[data_ARRAY + 2 + 항목자리] = data_thamani;
            if (Neno_SMS(jina_kisobadilika, "remove")) { for (int kitanzi_kielezo = 항목자리 + 1; kitanzi_kielezo < 항목수; kitanzi_kielezo++) 힙[data_ARRAY + 1 + kitanzi_kielezo] = 힙[data_ARRAY + 2 + kitanzi_kielezo]; 힙[data_ARRAY + 1 + 항목수] = 0; 힙[kipengee_Marejeleo + 3] = 항목수 - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Neno_SMS(jina_kisobadilika, "get") || Neno_SMS(jina_kisobadilika, "remove")) && Neno_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Neno_SMS(jina_kisobadilika, "put") && Neno_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Neno_SMS(jina_kisobadilika, "containsKey") && Neno_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Neno_SMS(jina_kisobadilika, "put"), ondoa = Neno_SMS(jina_kisobadilika, "remove");
            int data_thamani = 넣기여부 ? 빼기(2) : 0, Kitufe_Marejeleo = 빼기(2), kipengee_Marejeleo = 빼기(2); if (!kipengee_thamani(kipengee_Marejeleo, 11)) return;
            int 항목수 = 힙[kipengee_Marejeleo + 3], data_ARRAY = 힙[kipengee_Marejeleo + 2], 찾은여부 = -1;
            for (int kitanzi_kielezo = 0; kitanzi_kielezo < 항목수; kitanzi_kielezo++) if (값같음(Kitufe_Marejeleo, 힙[data_ARRAY + 2 + 2 * kitanzi_kielezo])) { 찾은여부 = kitanzi_kielezo; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[data_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(kipengee_Marejeleo, (항목수 + 1) * 2); data_ARRAY = 힙[kipengee_Marejeleo + 2]; 찾은여부 = 항목수; if (!kosa) 힙[kipengee_Marejeleo + 3] = 항목수 + 1; }
                if (!kosa) { 힙[data_ARRAY + 2 + 2 * 찾은여부] = Kitufe_Marejeleo; 힙[data_ARRAY + 3 + 2 * 찾은여부] = data_thamani; }
            }
            if (ondoa && 찾은여부 >= 0) { for (int kitanzi_kielezo = 찾은여부 + 1; kitanzi_kielezo < 항목수; kitanzi_kielezo++) { 힙[data_ARRAY + 2 * kitanzi_kielezo] = 힙[data_ARRAY + 2 + 2 * kitanzi_kielezo]; 힙[data_ARRAY + 1 + 2 * kitanzi_kielezo] = 힙[data_ARRAY + 3 + 2 * kitanzi_kielezo]; } 힙[data_ARRAY + 2 * 항목수] = 0; 힙[data_ARRAY + 1 + 2 * 항목수] = 0; 힙[kipengee_Marejeleo + 3] = 항목수 - 1; }
            if (Neno_SMS(jina_kisobadilika, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        kushindwa_thamani("unsupported collection method");
    }
    static boolean 잠금얻기(int kipengee_Marejeleo) {
        if (!객체유효(kipengee_Marejeleo)) return false;
        if (잠금깊이[kipengee_Marejeleo] != 0 && 잠금주인[kipengee_Marejeleo] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        잠금주인[kipengee_Marejeleo] = 현재가닥 + 1; 잠금깊이[kipengee_Marejeleo]++; return true;
    }
    static void 잠금풀기(int kipengee_Marejeleo) {
        if (!객체유효(kipengee_Marejeleo)) return;
        if (잠금깊이[kipengee_Marejeleo] == 0 || 잠금주인[kipengee_Marejeleo] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[kipengee_Marejeleo] == 0) 잠금주인[kipengee_Marejeleo] = 0;
    }
    static boolean badili_mtungo() {
        mtungo_fremu[현재가닥] = fremu_kielezo;
        if (fremu_kielezo < 현재가닥 * 32) mtungo_hali[현재가닥] = 3;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 가닥수; kitanzi_kielezo++) if (mtungo_hali[kitanzi_kielezo] == 2 && mtungo_hali[가닥대기[kitanzi_kielezo]] == 3) mtungo_hali[kitanzi_kielezo] = 1;
        for (int kitanzi_kielezo = 1; kitanzi_kielezo <= 가닥수; kitanzi_kielezo++) {
            int 다음자리 = (현재가닥 + kitanzi_kielezo) % 가닥수;
            if (mtungo_hali[다음자리] == 1) { 현재가닥 = 다음자리; fremu_kielezo = mtungo_fremu[다음자리]; 바꿈요청 = false; return true; }
        }
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 가닥수; kitanzi_kielezo++) if (mtungo_hali[kitanzi_kielezo] != 3) { kushindwa_thamani("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int jina_kisobadilika, int 서술상수, int amri_msimbo) { Mchakato_mtungo(jina_kisobadilika, 서술상수, amri_msimbo, false); }
    static void Mchakato_mtungo(int jina_kisobadilika, int 서술상수, int amri_msimbo, boolean 한국어) {
        if (amri_msimbo == 184 && Neno_SMS(jina_kisobadilika, 한국어 ? "ahirisha_kazi" : "yield") && Neno_SMS(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (amri_msimbo == 184 && Neno_SMS(jina_kisobadilika, "currentThread") && Neno_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(mtungo_kipengee[현재가닥], 2); return; }
        if (amri_msimbo == 183 && Neno_SMS(jina_kisobadilika, "<init>") && (Neno_SMS(서술상수, "()V") || Neno_SMS(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int lengo_anwani = Neno_SMS(서술상수, "()V") ? 0 : 빼기(2), kipengee_Marejeleo = 빼기(2);
            if (!객체유효(kipengee_Marejeleo)) return;
            if (힙[kipengee_Marejeleo] == 13) { 힙[kipengee_Marejeleo + 2] = lengo_anwani; 힙참조[kipengee_Marejeleo + 2] = 1; }
            else if (lengo_anwani != 0) kushindwa_thamani("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (amri_msimbo == 182 && (Neno_SMS(jina_kisobadilika, 한국어 ? "Anza_kazi" : "start") || Neno_SMS(jina_kisobadilika, 한국어 ? "기다리기" : "join")) && Neno_SMS(서술상수, "()V") || amri_msimbo == 182 && Neno_SMS(jina_kisobadilika, 한국어 ? "살아있는가" : "isAlive") && Neno_SMS(서술상수, "()Z")) {
            int kipengee_Marejeleo = 빼기(2); if (!객체유효(kipengee_Marejeleo)) return;
            int akaunti_thamani = -1; for (int kitanzi_kielezo = 0; kitanzi_kielezo < 가닥수; kitanzi_kielezo++) if (mtungo_kipengee[kitanzi_kielezo] == kipengee_Marejeleo) akaunti_thamani = kitanzi_kielezo;
            if (Neno_SMS(jina_kisobadilika, 한국어 ? "살아있는가" : "isAlive")) { 넣기(akaunti_thamani >= 0 && mtungo_hali[akaunti_thamani] != 3 ? 1 : 0, 1); return; }
            if (Neno_SMS(jina_kisobadilika, 한국어 ? "기다리기" : "join")) { if (akaunti_thamani >= 0 && mtungo_hali[akaunti_thamani] != 3) { 가닥대기[현재가닥] = akaunti_thamani; mtungo_hali[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (akaunti_thamani >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (가닥수 == 4) { kushindwa_thamani("thread limit (4 including main)"); return; }
            int lengo_anwani = 힙[kipengee_Marejeleo] == 13 ? 힙[kipengee_Marejeleo + 2] : kipengee_Marejeleo;
            int faili_kielezo = lengo_anwani > 0 && 힙[lengo_anwani] >= 32 ? jina_mbinu(힙[lengo_anwani] - 32, 한국어 ? "tekeleza_kazi" : "run", "()V") : -1;
            if (lengo_anwani != 0 && faili_kielezo < 0) { kushindwa_thamani("Runnable.run required"); return; }
            akaunti_thamani = 가닥수++; mtungo_kipengee[akaunti_thamani] = kipengee_Marejeleo; mtungo_lengo[akaunti_thamani] = lengo_anwani;
            int fremu = akaunti_thamani * 32; mtungo_fremu[akaunti_thamani] = faili_kielezo < 0 ? fremu - 1 : fremu; mtungo_hali[akaunti_thamani] = faili_kielezo < 0 ? 3 : 1;
            if (faili_kielezo >= 0) { fremu_mbinu[fremu] = faili_kielezo; 틀위치[fremu] = mbinu_Anza[faili_kielezo]; jirani_thamani[fremu * 128] = lengo_anwani; jirani_aina[fremu * 128] = 2; }
            return;
        }
        kushindwa_thamani("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], anwani_SMS = new int[16];
    static int jirani_anwani() { return anwani_kipengee(0x7f000001); }
    static int anwani_kipengee(int thamani) { int kipengee_Marejeleo = tengea_Hifadhi(14, 1); if (!kosa) 힙[kipengee_Marejeleo + 2] = thamani; return kipengee_Marejeleo; }
    static int 주소해독(int kipengee_Marejeleo) {
        if (kipengee_Marejeleo == 0 || 글같음(kipengee_Marejeleo, mwenyeji_kibambo("localhost"), false)) return 0x7f000001;
        if (!kipengee_thamani(kipengee_Marejeleo, 1)) return 0;
        int data_thamani = 0, 총수 = 0, anwani_baiti = 0, 자릿수 = 0, 항목수 = 힙[kipengee_Marejeleo + 1];
        for (int kitanzi_kielezo = 0; kitanzi_kielezo <= 항목수; kitanzi_kielezo++) {
            int msimbo_wa_kibambo = kitanzi_kielezo == 항목수 ? '.' : 힙[kipengee_Marejeleo + 2 + kitanzi_kielezo];
            if (msimbo_wa_kibambo == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } data_thamani = data_thamani << 8 | anwani_baiti; 총수++; anwani_baiti = 자릿수 = 0; }
            else { if (msimbo_wa_kibambo < '0' || msimbo_wa_kibambo > '9' || ++자릿수 > 3 || (anwani_baiti = anwani_baiti * 10 + msimbo_wa_kibambo - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return data_thamani;
    }
    static int anwani_kibambo(int data_thamani) {
        int 항목수 = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int anwani_baiti = data_thamani >>> 이동비트 & 255;
            if (anwani_baiti >= 100) anwani_SMS[항목수++] = '0' + anwani_baiti / 100;
            if (anwani_baiti >= 10) anwani_SMS[항목수++] = '0' + anwani_baiti / 10 % 10;
            anwani_SMS[항목수++] = '0' + anwani_baiti % 10; if (이동비트 != 0) anwani_SMS[항목수++] = '.';
        }
        int kipengee_Marejeleo = tengea_Hifadhi(1, 항목수); if (!kosa) for (int kitanzi_kielezo = 0; kitanzi_kielezo < 항목수; kitanzi_kielezo++) 힙[kipengee_Marejeleo + 2 + kitanzi_kielezo] = anwani_SMS[kitanzi_kielezo]; return kipengee_Marejeleo;
    }
    static void 통신호출(int mmiliki, int jina_kisobadilika, int 서술상수, int amri_msimbo) {
        if (Neno_SMS(mmiliki, "java/net/InetAddress")) {
            if (amri_msimbo == 184 && Neno_SMS(jina_kisobadilika, "getLoopbackAddress") && Neno_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(jirani_anwani(), 2); return; }
            if (amri_msimbo == 184 && Neno_SMS(jina_kisobadilika, "getByName") && Neno_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int data_thamani = 주소해독(빼기(2)); if (던진객체 == 0 && !kosa) 넣기(anwani_kipengee(data_thamani), 2); return;
            }
            if (amri_msimbo == 182 && Neno_SMS(jina_kisobadilika, "getHostAddress") && Neno_SMS(서술상수, "()Ljava/lang/String;")) { int kipengee_Marejeleo = 빼기(2); if (kipengee_thamani(kipengee_Marejeleo, 14)) 넣기(anwani_kibambo(힙[kipengee_Marejeleo + 2]), 2); return; }
        }
        if (Neno_SMS(mmiliki, "java/net/DatagramPacket")) {
            if (amri_msimbo == 183 && Neno_SMS(jina_kisobadilika, "<init>") && (Neno_SMS(서술상수, "([BI)V") || Neno_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean fikio_thamani_Marejeleo = Neno_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int namba_ya_kituo = fikio_thamani_Marejeleo ? 빼기(1) : 0, anwani_Marejeleo = fikio_thamani_Marejeleo ? 빼기(2) : 0;
                int 항목수 = 빼기(1), data_ARRAY = 빼기(2), kipengee_Marejeleo = 빼기(2);
                if (!kipengee_thamani(kipengee_Marejeleo, 16) || !kipengee_thamani(data_ARRAY, 20)) return;
                if (항목수 < 0 || 항목수 > 힙[data_ARRAY + 1] || namba_ya_kituo < 0 || namba_ya_kituo > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (anwani_Marejeleo != 0 && !kipengee_thamani(anwani_Marejeleo, 14)) return;
                힙[kipengee_Marejeleo + 2] = data_ARRAY; 힙참조[kipengee_Marejeleo + 2] = 1; 힙[kipengee_Marejeleo + 3] = 항목수;
                힙[kipengee_Marejeleo + 4] = anwani_Marejeleo; 힙참조[kipengee_Marejeleo + 4] = 1; 힙[kipengee_Marejeleo + 5] = namba_ya_kituo; return;
            }
            if (amri_msimbo == 182 && Neno_SMS(jina_kisobadilika, "setLength") && Neno_SMS(서술상수, "(I)V")) {
                int 항목수 = 빼기(1), kipengee_Marejeleo = 빼기(2); if (!kipengee_thamani(kipengee_Marejeleo, 16)) return;
                if (항목수 < 0 || 항목수 > 힙[힙[kipengee_Marejeleo + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[kipengee_Marejeleo + 3] = 항목수; return;
            }
            if (amri_msimbo == 182 && (Neno_SMS(jina_kisobadilika, "getData") && Neno_SMS(서술상수, "()[B") || Neno_SMS(jina_kisobadilika, "getLength") && Neno_SMS(서술상수, "()I") || Neno_SMS(jina_kisobadilika, "getAddress") && Neno_SMS(서술상수, "()Ljava/net/InetAddress;") || Neno_SMS(jina_kisobadilika, "getPort") && Neno_SMS(서술상수, "()I"))) {
                int kipengee_Marejeleo = 빼기(2); if (!kipengee_thamani(kipengee_Marejeleo, 16)) return;
                int 항목자리 = Neno_SMS(jina_kisobadilika, "getData") ? 2 : Neno_SMS(jina_kisobadilika, "getLength") ? 3 : Neno_SMS(jina_kisobadilika, "getAddress") ? 4 : 5;
                넣기(힙[kipengee_Marejeleo + 항목자리], 항목자리 == 2 || 항목자리 == 4 ? 2 : 1); return;
            }
        }
        if (Neno_SMS(mmiliki, "java/net/DatagramSocket")) {
            if (amri_msimbo == 183 && Neno_SMS(jina_kisobadilika, "<init>") && (Neno_SMS(서술상수, "()V") || Neno_SMS(서술상수, "(I)V"))) {
                int namba_ya_kituo = Neno_SMS(서술상수, "()V") ? 0 : 빼기(1), kipengee_Marejeleo = 빼기(2); if (!kipengee_thamani(kipengee_Marejeleo, 15)) return;
                if (namba_ya_kituo < 0 || namba_ya_kituo > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = mtumiaji.unda_Mtandao(namba_ya_kituo); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[kipengee_Marejeleo + 2] = 열린파일번호; return;
            }
            if (amri_msimbo == 182 && Neno_SMS(jina_kisobadilika, "setSoTimeout") && Neno_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), kipengee_Marejeleo = 빼기(2); if (!kipengee_thamani(kipengee_Marejeleo, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[kipengee_Marejeleo + 3] = 밀리초값; return;
            }
            if (amri_msimbo == 182 && Neno_SMS(jina_kisobadilika, "getLocalPort") && Neno_SMS(서술상수, "()I")) { int kipengee_Marejeleo = 빼기(2); if (kipengee_thamani(kipengee_Marejeleo, 15)) 넣기(힙[kipengee_Marejeleo + 2] < 0 ? -1 : mtumiaji.Mtandao_kituo(힙[kipengee_Marejeleo + 2]), 1); return; }
            if (amri_msimbo == 182 && Neno_SMS(jina_kisobadilika, "isClosed") && Neno_SMS(서술상수, "()Z")) { int kipengee_Marejeleo = 빼기(2); if (kipengee_thamani(kipengee_Marejeleo, 15)) 넣기(힙[kipengee_Marejeleo + 2] < 0 ? 1 : 0, 1); return; }
            if (amri_msimbo == 182 && Neno_SMS(jina_kisobadilika, "close") && Neno_SMS(서술상수, "()V")) { int kipengee_Marejeleo = 빼기(2); if (kipengee_thamani(kipengee_Marejeleo, 15) && 힙[kipengee_Marejeleo + 2] >= 0) { mtumiaji.파일서술자닫기(힙[kipengee_Marejeleo + 2]); 힙[kipengee_Marejeleo + 2] = -1; } return; }
            if (amri_msimbo == 182 && (Neno_SMS(jina_kisobadilika, "send") || Neno_SMS(jina_kisobadilika, "receive")) && Neno_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int pakiti = 빼기(2), kipengee_Marejeleo = 빼기(2); if (!kipengee_thamani(pakiti, 16) || !kipengee_thamani(kipengee_Marejeleo, 15)) return;
                int data_ARRAY = 힙[pakiti + 2], 유효길이 = 힙[pakiti + 3], 열린파일번호 = 힙[kipengee_Marejeleo + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Neno_SMS(jina_kisobadilika, "send")) {
                    if (!kipengee_thamani(힙[pakiti + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int kitanzi_kielezo = 0; kitanzi_kielezo < 유효길이; kitanzi_kielezo++) 통신임시[kitanzi_kielezo] = 힙[data_ARRAY + 2 + kitanzi_kielezo];
                    if (mtumiaji.tuma_Mtandao(열린파일번호, 힙[힙[pakiti + 4] + 2], 힙[pakiti + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int 항목수 = mtumiaji.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (항목수 == -11) {
                        int 현재시각 = mtumiaji.밀리초();
                        if (힙[kipengee_Marejeleo + 4] == 0) 힙[kipengee_Marejeleo + 4] = 현재시각 + 1;
                        if (힙[kipengee_Marejeleo + 3] > 0 && 현재시각 - (힙[kipengee_Marejeleo + 4] - 1) >= 힙[kipengee_Marejeleo + 3]) { 힙[kipengee_Marejeleo + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(kipengee_Marejeleo, 2); 넣기(pakiti, 2); 틀위치[fremu_kielezo] = fremu_agizo[fremu_kielezo]; 바꿈요청 = true; return;
                    }
                    힙[kipengee_Marejeleo + 4] = 0;
                    if (항목수 < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int kitanzi_kielezo = 0; kitanzi_kielezo < 항목수; kitanzi_kielezo++) 힙[data_ARRAY + 2 + kitanzi_kielezo] = (byte)통신임시[kitanzi_kielezo];
                    힙[pakiti + 3] = 항목수; 힙[pakiti + 4] = anwani_kipengee(통신임시[513]); 힙참조[pakiti + 4] = 1; 힙[pakiti + 5] = 통신임시[512];
                }
                return;
            }
        }
        kushindwa_thamani("unsupported java.net method");
    }
    static boolean 흐름대기(int kipengee_Marejeleo) {
        int 현재시각 = mtumiaji.밀리초();
        if (힙[kipengee_Marejeleo + 5] == 0) 힙[kipengee_Marejeleo + 5] = 현재시각 + 1;
        if (힙[kipengee_Marejeleo + 3] > 0 && 현재시각 - (힙[kipengee_Marejeleo + 5] - 1) >= 힙[kipengee_Marejeleo + 3]) { 힙[kipengee_Marejeleo + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        틀위치[fremu_kielezo] = fremu_agizo[fremu_kielezo]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int mmiliki, int jina_kisobadilika, int 서술상수, int amri_msimbo) {
        boolean 수신쪽 = Neno_SMS(mmiliki, "java/net/ServerSocket"), Stream = Neno_SMS(mmiliki, "java/io/InputStream") || Neno_SMS(mmiliki, "java/io/OutputStream");
        if (!Stream && amri_msimbo == 183 && Neno_SMS(jina_kisobadilika, "<init>")) {
            boolean teknolojia_ya_maelezo_tupu_hali = Neno_SMS(서술상수, "()V"), 이름지정여부 = Neno_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Neno_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(teknolojia_ya_maelezo_tupu_hali || 수신쪽 && Neno_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { kushindwa_thamani("unsupported socket constructor"); return; }
            int namba_ya_kituo = teknolojia_ya_maelezo_tupu_hali ? 0 : 빼기(1), anwani_Marejeleo = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, kipengee_Marejeleo = 빼기(2);
            if (!kipengee_thamani(kipengee_Marejeleo, 수신쪽 ? 18 : 17)) return;
            if (namba_ya_kituo < 0 || namba_ya_kituo > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !kipengee_thamani(anwani_Marejeleo, 14)) return;
            int Mtandao_anwani = 이름지정여부 ? 주소해독(anwani_Marejeleo) : 주소지정여부 ? 힙[anwani_Marejeleo + 2] : 0x7f000001;
            if (kosa || 던진객체 != 0) return;
            int 열린파일번호 = mtumiaji.Stream_udhibiti(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = teknolojia_ya_maelezo_tupu_hali ? 0 : 수신쪽 ? mtumiaji.Stream_udhibiti(1, 열린파일번호, namba_ya_kituo) : mtumiaji.UNGANISHA_Stream(열린파일번호, Mtandao_anwani, namba_ya_kituo);
            if (처리값 < 0) { mtumiaji.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[kipengee_Marejeleo + 2] = 열린파일번호; 힙[kipengee_Marejeleo + 4] = namba_ya_kituo; 힙[kipengee_Marejeleo + 6] = teknolojia_ya_maelezo_tupu_hali ? 0 : 1; return;
        }
        if (!Stream && Neno_SMS(jina_kisobadilika, "setSoTimeout") && Neno_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), kipengee_Marejeleo = 빼기(2); if (!kipengee_thamani(kipengee_Marejeleo, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[kipengee_Marejeleo + 3] = 밀리초값; return; }
        if (!Stream && Neno_SMS(jina_kisobadilika, "close") && Neno_SMS(서술상수, "()V")) { int kipengee_Marejeleo = 빼기(2); if (kipengee_thamani(kipengee_Marejeleo, 수신쪽 ? 18 : 17) && 힙[kipengee_Marejeleo + 2] >= 0) { mtumiaji.파일서술자닫기(힙[kipengee_Marejeleo + 2]); 힙[kipengee_Marejeleo + 2] = -1; } return; }
        if (!Stream && (Neno_SMS(jina_kisobadilika, "getLocalPort") || Neno_SMS(jina_kisobadilika, "getPort") || Neno_SMS(jina_kisobadilika, "isClosed") || Neno_SMS(jina_kisobadilika, "isConnected"))) {
            int kipengee_Marejeleo = 빼기(2); if (!kipengee_thamani(kipengee_Marejeleo, 수신쪽 ? 18 : 17)) return;
            넣기(Neno_SMS(jina_kisobadilika, "isClosed") ? 힙[kipengee_Marejeleo + 2] < 0 ? 1 : 0 : Neno_SMS(jina_kisobadilika, "isConnected") ? 힙[kipengee_Marejeleo + 6] : Neno_SMS(jina_kisobadilika, "getPort") ? 힙[kipengee_Marejeleo + 4] : 힙[kipengee_Marejeleo + 2] < 0 ? -1 : mtumiaji.Stream_udhibiti(4, 힙[kipengee_Marejeleo + 2], 0), 1); return;
        }
        if (수신쪽 && Neno_SMS(jina_kisobadilika, "accept") && Neno_SMS(서술상수, "()Ljava/net/Socket;")) {
            int kipengee_Marejeleo = 빼기(2); if (!kipengee_thamani(kipengee_Marejeleo, 18)) return; int 열린파일번호 = mtumiaji.Stream_udhibiti(3, 힙[kipengee_Marejeleo + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(kipengee_Marejeleo)) 넣기(kipengee_Marejeleo, 2); return; }
            힙[kipengee_Marejeleo + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = tengea_Hifadhi(17, 5); if (kosa) { mtumiaji.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = mtumiaji.Stream_udhibiti(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !Stream && ((Neno_SMS(jina_kisobadilika, "getInputStream") && Neno_SMS(서술상수, "()Ljava/io/InputStream;")) || (Neno_SMS(jina_kisobadilika, "getOutputStream") && Neno_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int kipengee_Marejeleo = 빼기(2); if (!kipengee_thamani(kipengee_Marejeleo, 17)) return; if (힙[kipengee_Marejeleo + 2] < 0 || 힙[kipengee_Marejeleo + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = tengea_Hifadhi(19, 4); if (kosa) return; 힙[반환값 + 2] = kipengee_Marejeleo; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Neno_SMS(jina_kisobadilika, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Neno_SMS(jina_kisobadilika, "read"), teknolojia_ya_maelezo_andika_upasuaji = Neno_SMS(jina_kisobadilika, "write"), zuia = Neno_SMS(서술상수, "([B)I") || Neno_SMS(서술상수, "([B)V"), teknolojia_ya_maelezo_SUBARRAY = Neno_SMS(서술상수, "([BII)I") || Neno_SMS(서술상수, "([BII)V");
            int 항목수 = teknolojia_ya_maelezo_SUBARRAY ? 빼기(1) : 0, 시작변위 = teknolojia_ya_maelezo_SUBARRAY ? 빼기(1) : 0, data_ARRAY = zuia || teknolojia_ya_maelezo_SUBARRAY ? 빼기(2) : 0;
            int data_thamani = teknolojia_ya_maelezo_andika_upasuaji && Neno_SMS(서술상수, "(I)V") ? 빼기(1) : 0, kipengee_Marejeleo = 빼기(2);
            if (!kipengee_thamani(kipengee_Marejeleo, 19)) return; int 부모참조 = 힙[kipengee_Marejeleo + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Neno_SMS(jina_kisobadilika, "close") && Neno_SMS(서술상수, "()V")) { mtumiaji.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Neno_SMS(jina_kisobadilika, "flush") && Neno_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !teknolojia_ya_maelezo_andika_upasuaji) || 읽기여부 != (힙[kipengee_Marejeleo + 3] == 0)) { kushindwa_thamani("unsupported stream operation"); return; }
            if (zuia || teknolojia_ya_maelezo_SUBARRAY) { if (!kipengee_thamani(data_ARRAY, 20)) return; if (zuia) 항목수 = 힙[data_ARRAY + 1]; if (시작변위 < 0 || 항목수 < 0 || 시작변위 > 힙[data_ARRAY + 1] - 항목수) { 예외던짐(6, "stream array bounds"); return; } }
            else 항목수 = 1;
            if (항목수 == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = teknolojia_ya_maelezo_andika_upasuaji ? 힙[kipengee_Marejeleo + 4] : 0, 처리값 = 0;
            while (완료수 < 항목수) {
                처리값 = 읽기여부 ? mtumiaji.파일한바이트읽기(열린파일번호) : mtumiaji.파일한바이트쓰기(열린파일번호, zuia || teknolojia_ya_maelezo_SUBARRAY ? 힙[data_ARRAY + 2 + 시작변위 + 완료수] : data_thamani);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (zuia || teknolojia_ya_maelezo_SUBARRAY)) 힙[data_ARRAY + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(zuia || teknolojia_ya_maelezo_SUBARRAY)) break;
            }
            if (처리값 == -11 && (teknolojia_ya_maelezo_andika_upasuaji || 완료수 == 0)) {
                힙[kipengee_Marejeleo + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(kipengee_Marejeleo, 2); if (zuia || teknolojia_ya_maelezo_SUBARRAY) 넣기(data_ARRAY, 2); if (teknolojia_ya_maelezo_SUBARRAY) { 넣기(시작변위, 1); 넣기(항목수, 1); } if (teknolojia_ya_maelezo_andika_upasuaji && !(zuia || teknolojia_ya_maelezo_SUBARRAY)) 넣기(data_thamani, 1); } return;
            }
            힙[kipengee_Marejeleo + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : zuia || teknolojia_ya_maelezo_SUBARRAY ? 완료수 : 처리값, 1); return;
        }
        kushindwa_thamani("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int jina_kisobadilika) {
        if (Neno_SMS(jina_kisobadilika, "한국어/자체/dirisha")) return 24;
        if (Neno_SMS(jina_kisobadilika, "한국어/자체/lebo")) return 26;
        if (Neno_SMS(jina_kisobadilika, "한국어/자체/kitufe")) return 27;
        if (Neno_SMS(jina_kisobadilika, "한국어/자체/SMS_uga")) return 28;
        if (Neno_SMS(jina_kisobadilika, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int jina_kisobadilika) {
        return 한국어화면종(jina_kisobadilika) != 0 || Neno_SMS(jina_kisobadilika, "한국어/자체/화면구성요소") || Neno_SMS(jina_kisobadilika, "한국어/자체/tukio_foleni");
    }
    static int 화면종(int jina_kisobadilika) {
        int 한국어종 = 한국어화면종(jina_kisobadilika); if (한국어종 != 0) return 한국어종;
        if (Neno_SMS(jina_kisobadilika, "javax/swing/JFrame")) return 24;
        if (Neno_SMS(jina_kisobadilika, "javax/swing/JPanel")) return 25;
        if (Neno_SMS(jina_kisobadilika, "javax/swing/JLabel")) return 26;
        if (Neno_SMS(jina_kisobadilika, "javax/swing/JButton")) return 27;
        if (Neno_SMS(jina_kisobadilika, "javax/swing/JTextField")) return 28;
        if (Neno_SMS(jina_kisobadilika, "java/awt/event/ActionEvent")) return 29;
        if (Neno_SMS(jina_kisobadilika, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int jina_kisobadilika) {
        return 화면종(jina_kisobadilika) != 0 || Neno_SMS(jina_kisobadilika, "java/awt/Component") || Neno_SMS(jina_kisobadilika, "java/awt/Container") || Neno_SMS(jina_kisobadilika, "javax/swing/JComponent") || Neno_SMS(jina_kisobadilika, "javax/swing/AbstractButton") || Neno_SMS(jina_kisobadilika, "javax/swing/text/JTextComponent") || Neno_SMS(jina_kisobadilika, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int kipengee_Marejeleo) { if (!객체유효(kipengee_Marejeleo)) return false; if (힙[kipengee_Marejeleo] < 24 || 힙[kipengee_Marejeleo] > 28) { kushindwa_thamani("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int kipengee_Marejeleo, int SMS_Marejeleo) {
        if (SMS_Marejeleo != 0 && !kipengee_thamani(SMS_Marejeleo, 1)) return;
        int 항목수 = SMS_Marejeleo == 0 ? 0 : 힙[SMS_Marejeleo + 1]; if (항목수 > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 항목수; kitanzi_kielezo++) 화면글임시[kitanzi_kielezo] = 힙[SMS_Marejeleo + 2 + kitanzi_kielezo];
        if (mtumiaji.화면글(힙[kipengee_Marejeleo + 2], 화면글임시, 항목수) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[kipengee_Marejeleo + 3] = SMS_Marejeleo; 힙참조[kipengee_Marejeleo + 3] = 1;
    }
    static int 화면문자읽기(int kipengee_Marejeleo) {
        int akaunti_thamani = 힙[kipengee_Marejeleo + 2], 항목수 = mtumiaji.화면연결(8, akaunti_thamani, 0, 0, 0, 0), 사용수 = 0;
        if (항목수 < 0) { kushindwa_thamani("GUI text read failed"); return 0; }
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 항목수; kitanzi_kielezo++) { int 부호값 = mtumiaji.화면연결(9, akaunti_thamani, kitanzi_kielezo, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = tengea_Hifadhi(1, 사용수); if (!kosa) for (int kitanzi_kielezo = 0; kitanzi_kielezo < 사용수; kitanzi_kielezo++) 힙[반환값 + 2 + kitanzi_kielezo] = 화면글임시[kitanzi_kielezo]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 kiini_thamani_0611a8a8 화면 기능에 연결한다. Swing kipengee_thamani/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int mmiliki, int jina_kisobadilika, int 서술상수, int amri_msimbo) {
        if (Neno_SMS(mmiliki, "한국어/자체/tukio_foleni")) {
            if (amri_msimbo == 184 && Neno_SMS(jina_kisobadilika, "나중에실행") && Neno_SMS(서술상수, "(L한국어/자체/실행할일;)V")) {
                int kazi_Kitendo = 빼기(2); if (!객체유효(kazi_Kitendo)) return;
                if (나중수 == 8) { kushindwa_thamani("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = kazi_Kitendo; return;
            }
            if (amri_msimbo == 184 && Neno_SMS(jina_kisobadilika, "사건처리중인가") && Neno_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            kushindwa_thamani("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (Neno_SMS(mmiliki, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!kipengee_thamani(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Neno_SMS(jina_kisobadilika, "tukio_chanzo") && Neno_SMS(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Neno_SMS(jina_kisobadilika, "amri_SMS") && Neno_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Neno_SMS(jina_kisobadilika, "kielezo") && Neno_SMS(서술상수, "()I")) 넣기(1001, 1);
            else kushindwa_thamani("지원하지 않는 한국어 Kitendo 알림 호출"); return;
        }
        if (amri_msimbo == 183 && Neno_SMS(jina_kisobadilika, "<init>")) {
            int 종류 = 한국어화면종(mmiliki), 받이 = 0, 가로 = 0, 세로 = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Neno_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (mtumiaji.화면너비() - 폭) / 2; 세로 = (mtumiaji.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Neno_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Neno_SMS(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); 세로 = 빼기(1); 가로 = 빼기(1);
            } else { kushindwa_thamani("지원하지 않는 한국어 화면 생성자"); return; }
            int SMS = 빼기(2), elementi_thamani = 빼기(2); if (!화면객체(elementi_thamani)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || 세로 < 0 || 폭 > mtumiaji.화면너비() - 가로 || 높이 > mtumiaji.화면높이() - 세로) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int kielezo = mtumiaji.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (kielezo < 1 || kielezo > 32) { kushindwa_thamani("화면 elementi_thamani 자리가 가득 찼습니다"); return; }
            힙[elementi_thamani + 2] = kielezo; 화면참조[kielezo - 1] = elementi_thamani;
            힙[elementi_thamani + 5] = 가로; 힙[elementi_thamani + 6] = 세로; 힙[elementi_thamani + 7] = 폭; 힙[elementi_thamani + 8] = 높이; 힙[elementi_thamani + 10] = 2;
            힙[elementi_thamani + 4] = 받이; 힙참조[elementi_thamani + 4] = 1; 힙[elementi_thamani + 12] = 1;
            mtumiaji.화면연결(1, kielezo, 가로, 세로, 폭, 높이);
            if (종류 == 24) mtumiaji.화면연결(7, kielezo, 2, 0, 0, 0);
            화면문자설정(elementi_thamani, SMS); return;
        }
        if (amri_msimbo != 182) { kushindwa_thamani("잘못된 한국어 화면 호출 amri"); return; }
        if (Neno_SMS(jina_kisobadilika, "andika_SMS") && Neno_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int SMS = 빼기(2), elementi_thamani = 빼기(2); if (화면객체(elementi_thamani)) 화면문자설정(elementi_thamani, SMS); return;
        }
        if (Neno_SMS(jina_kisobadilika, "글읽기") && Neno_SMS(서술상수, "()Ljava/lang/String;")) {
            int elementi_thamani = 빼기(2); if (화면객체(elementi_thamani)) 넣기(화면문자읽기(elementi_thamani), 2); return;
        }
        if (Neno_SMS(jina_kisobadilika, "동작맡기기") && Neno_SMS(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), elementi_thamani = 빼기(2);
            if (화면객체(elementi_thamani)) { 힙[elementi_thamani + 4] = 받이; 힙참조[elementi_thamani + 4] = 1; 힙[elementi_thamani + 12] = 1; } return;
        }
        if (Neno_SMS(jina_kisobadilika, "jumlisha_elementi") && Neno_SMS(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int mtoto_thamani = 빼기(2), 부모 = 빼기(2); if (!화면객체(mtoto_thamani) || !화면객체(부모)) return;
            if (mtumiaji.화면연결(2, 힙[부모 + 2], 힙[mtoto_thamani + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[mtoto_thamani + 11] = 부모; 힙참조[mtoto_thamani + 11] = 1; return;
        }
        if (Neno_SMS(jina_kisobadilika, "자리정하기") && Neno_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), 세로 = 빼기(1), 가로 = 빼기(1), elementi_thamani = 빼기(2); if (!화면객체(elementi_thamani)) return;
            if (mtumiaji.화면연결(1, 힙[elementi_thamani + 2], 가로, 세로, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[elementi_thamani + 5] = 가로; 힙[elementi_thamani + 6] = 세로; 힙[elementi_thamani + 7] = 폭; 힙[elementi_thamani + 8] = 높이; return;
        }
        if ((Neno_SMS(jina_kisobadilika, "onyesha_dirisha") || Neno_SMS(jina_kisobadilika, "funga")) && Neno_SMS(서술상수, "()V")) {
            boolean uonekanaji_thamani = Neno_SMS(jina_kisobadilika, "onyesha_dirisha"); int elementi_thamani = 빼기(2); if (!화면객체(elementi_thamani)) return;
            if (mtumiaji.화면연결(uonekanaji_thamani ? 3 : 4, 힙[elementi_thamani + 2], uonekanaji_thamani ? 1 : 0, 0, 0, 0) < 0) { kushindwa_thamani("화면은 ingiliani 명령에서 실행해야 합니다"); return; }
            힙[elementi_thamani + 9] = uonekanaji_thamani ? 1 : 0; return;
        }
        if (Neno_SMS(jina_kisobadilika, "보이는가") && Neno_SMS(서술상수, "()Z")) { int elementi_thamani = 빼기(2); if (화면객체(elementi_thamani)) 넣기(힙[elementi_thamani + 9], 1); return; }
        kushindwa_thamani("지원하지 않는 한국어 화면 mbinu_thamani");
    }
    static void 화면호출(int mmiliki, int jina_kisobadilika, int 서술상수, int amri_msimbo) {
        if (Neno_SMS(mmiliki, "javax/swing/SwingUtilities")) {
            if (amri_msimbo == 184 && Neno_SMS(jina_kisobadilika, "invokeLater") && Neno_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int kipengee_Marejeleo = 빼기(2); if (!객체유효(kipengee_Marejeleo)) return; if (나중수 == 8) { kushindwa_thamani("invokeLater queue full"); return; } 나중실행[나중수++] = kipengee_Marejeleo; return; }
            if (amri_msimbo == 184 && Neno_SMS(jina_kisobadilika, "isEventDispatchThread") && Neno_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            kushindwa_thamani("unsupported SwingUtilities method"); return;
        }
        if (Neno_SMS(mmiliki, "java/awt/event/ActionEvent")) {
            int kipengee_Marejeleo = 빼기(2); if (!kipengee_thamani(kipengee_Marejeleo, 29)) return;
            if (Neno_SMS(jina_kisobadilika, "getSource") && Neno_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[kipengee_Marejeleo + 2], 2);
            else if (Neno_SMS(jina_kisobadilika, "getActionCommand") && Neno_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[kipengee_Marejeleo + 2]), 2);
            else if (Neno_SMS(jina_kisobadilika, "getID") && Neno_SMS(서술상수, "()I")) 넣기(1001, 1);
            else kushindwa_thamani("unsupported ActionEvent method"); return;
        }
        if (amri_msimbo == 183 && Neno_SMS(jina_kisobadilika, "<init>")) {
            int 열수 = 0, SMS_Marejeleo = 0;
            if (Neno_SMS(서술상수, "(I)V")) 열수 = 빼기(1);
            else if (Neno_SMS(서술상수, "(Ljava/lang/String;I)V")) { 열수 = 빼기(1); SMS_Marejeleo = 빼기(2); }
            else if (Neno_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Marejeleo = 빼기(2);
            else if (Neno_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Neno_SMS(서술상수, "()V")) { kushindwa_thamani("unsupported Swing constructor"); return; }
            int kipengee_Marejeleo = 빼기(2); if (!객체유효(kipengee_Marejeleo)) return;
            if (힙[kipengee_Marejeleo] == 30) { kushindwa_thamani("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(kipengee_Marejeleo) || 열수 < 0) return;
            int akaunti_thamani = mtumiaji.화면연결(0, 힙[kipengee_Marejeleo] - 23, 0, 0, 0, 0);
            if (akaunti_thamani < 1 || akaunti_thamani > 32) { kushindwa_thamani("GUI widget slots exhausted"); return; }
            힙[kipengee_Marejeleo + 2] = akaunti_thamani; 화면참조[akaunti_thamani - 1] = kipengee_Marejeleo; 힙[kipengee_Marejeleo + 5] = 힙[kipengee_Marejeleo] == 24 ? 130 : 16; 힙[kipengee_Marejeleo + 6] = 힙[kipengee_Marejeleo] == 24 ? 110 : 16;
            힙[kipengee_Marejeleo + 7] = 힙[kipengee_Marejeleo] == 24 ? 380 : 220; 힙[kipengee_Marejeleo + 8] = 힙[kipengee_Marejeleo] == 24 ? 240 : 28; 힙[kipengee_Marejeleo + 10] = 1;
            화면문자설정(kipengee_Marejeleo, SMS_Marejeleo); return;
        }
        if (Neno_SMS(jina_kisobadilika, "setText") || Neno_SMS(jina_kisobadilika, "setTitle")) { int SMS_Marejeleo = 빼기(2), kipengee_Marejeleo = 빼기(2); if (화면객체(kipengee_Marejeleo) && Neno_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(kipengee_Marejeleo, SMS_Marejeleo); return; }
        if (Neno_SMS(jina_kisobadilika, "getText") || Neno_SMS(jina_kisobadilika, "getTitle")) { int kipengee_Marejeleo = 빼기(2); if (화면객체(kipengee_Marejeleo) && Neno_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(kipengee_Marejeleo), 2); return; }
        if (Neno_SMS(jina_kisobadilika, "addActionListener") && Neno_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), kipengee_Marejeleo = 빼기(2); if (화면객체(kipengee_Marejeleo)) { 힙[kipengee_Marejeleo + 4] = 수신참조; 힙참조[kipengee_Marejeleo + 4] = 1; } return; }
        if (Neno_SMS(jina_kisobadilika, "getContentPane") && Neno_SMS(서술상수, "()Ljava/awt/Container;")) { int kipengee_Marejeleo = 빼기(2); if (화면객체(kipengee_Marejeleo)) 넣기(kipengee_Marejeleo, 2); return; }
        if (Neno_SMS(jina_kisobadilika, "setLayout") && Neno_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Muundo_Marejeleo = 빼기(2), kipengee_Marejeleo = 빼기(2); if (화면객체(kipengee_Marejeleo) && Muundo_Marejeleo != 0) kushindwa_thamani("only absolute layout (null) is supported"); return; }
        if (Neno_SMS(jina_kisobadilika, "add") && (Neno_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Neno_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Muundo_sharti = Neno_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Muundo_sharti) 빼기(2);
            int mtoto_Marejeleo = 빼기(2), kipengee_Marejeleo = 빼기(2); if (!화면객체(mtoto_Marejeleo) || !화면객체(kipengee_Marejeleo)) return;
            if (mtumiaji.화면연결(2, 힙[kipengee_Marejeleo + 2], 힙[mtoto_Marejeleo + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[mtoto_Marejeleo + 11] = kipengee_Marejeleo; 힙참조[mtoto_Marejeleo + 11] = 1; if (!Muundo_sharti) 넣기(mtoto_Marejeleo, 2); return;
        }
        if (Neno_SMS(jina_kisobadilika, "setBounds") && Neno_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), Kitufe_cha_Y_kiratibu = 빼기(1), jira_x = 빼기(1), kipengee_Marejeleo = 빼기(2); if (!화면객체(kipengee_Marejeleo)) return;
            if (mtumiaji.화면연결(1, 힙[kipengee_Marejeleo + 2], jira_x, Kitufe_cha_Y_kiratibu, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[kipengee_Marejeleo + 5] = jira_x; 힙[kipengee_Marejeleo + 6] = Kitufe_cha_Y_kiratibu; 힙[kipengee_Marejeleo + 7] = 너비; 힙[kipengee_Marejeleo + 8] = 높이; return;
        }
        if (Neno_SMS(jina_kisobadilika, "setSize") && Neno_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), kipengee_Marejeleo = 빼기(2); if (!화면객체(kipengee_Marejeleo)) return;
            if (mtumiaji.화면연결(1, 힙[kipengee_Marejeleo + 2], 힙[kipengee_Marejeleo + 5], 힙[kipengee_Marejeleo + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[kipengee_Marejeleo + 7] = 너비; 힙[kipengee_Marejeleo + 8] = 높이; } return;
        }
        if (Neno_SMS(jina_kisobadilika, "setLocationRelativeTo") && Neno_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), kipengee_Marejeleo = 빼기(2); if (!화면객체(kipengee_Marejeleo)) return; if (상대배치 != 0) { kushindwa_thamani("only screen centering supported"); return; } 힙[kipengee_Marejeleo + 5] = (mtumiaji.화면너비() - 힙[kipengee_Marejeleo + 7]) / 2; 힙[kipengee_Marejeleo + 6] = (mtumiaji.화면높이() - 힙[kipengee_Marejeleo + 8]) / 2; mtumiaji.화면연결(1, 힙[kipengee_Marejeleo + 2], 힙[kipengee_Marejeleo + 5], 힙[kipengee_Marejeleo + 6], 힙[kipengee_Marejeleo + 7], 힙[kipengee_Marejeleo + 8]); return; }
        if (Neno_SMS(jina_kisobadilika, "setDefaultCloseOperation") && Neno_SMS(서술상수, "(I)V")) { int sera = 빼기(1), kipengee_Marejeleo = 빼기(2); if (화면객체(kipengee_Marejeleo)) { if (sera < 0 || sera > 3) 예외던짐(9, "close policy"); else { 힙[kipengee_Marejeleo + 10] = sera; mtumiaji.화면연결(7, 힙[kipengee_Marejeleo + 2], sera, 0, 0, 0); } } return; }
        if (Neno_SMS(jina_kisobadilika, "setVisible") && Neno_SMS(서술상수, "(Z)V")) { int data_thamani = 빼기(1), kipengee_Marejeleo = 빼기(2); if (화면객체(kipengee_Marejeleo)) { int 처리값 = mtumiaji.화면연결(3, 힙[kipengee_Marejeleo + 2], data_thamani, 0, 0, 0); if (처리값 < 0) kushindwa_thamani("Swing requires a standalone interactive command"); else 힙[kipengee_Marejeleo + 9] = data_thamani; } return; }
        if (Neno_SMS(jina_kisobadilika, "dispose") && Neno_SMS(서술상수, "()V")) { int kipengee_Marejeleo = 빼기(2); if (화면객체(kipengee_Marejeleo)) { mtumiaji.화면연결(4, 힙[kipengee_Marejeleo + 2], 0, 0, 0, 0); 힙[kipengee_Marejeleo + 9] = 0; } return; }
        if (Neno_SMS(jina_kisobadilika, "repaint") || Neno_SMS(jina_kisobadilika, "validate")) { int kipengee_Marejeleo = 빼기(2); if (!화면객체(kipengee_Marejeleo) || !Neno_SMS(서술상수, "()V")) return; mtumiaji.화면연결(1, 힙[kipengee_Marejeleo + 2], 힙[kipengee_Marejeleo + 5], 힙[kipengee_Marejeleo + 6], 힙[kipengee_Marejeleo + 7], 힙[kipengee_Marejeleo + 8]); return; }
        if (Neno_SMS(jina_kisobadilika, "isVisible") && Neno_SMS(서술상수, "()Z")) { int kipengee_Marejeleo = 빼기(2); if (화면객체(kipengee_Marejeleo)) 넣기(힙[kipengee_Marejeleo + 9], 1); return; }
        kushindwa_thamani("unsupported Swing method (native subset)");
    }
    static void 사건실행(int lengo_anwani, int 사건번호, boolean 한국어) {
        if (lengo_anwani < 1 || 힙[lengo_anwani] < 32) { kushindwa_thamani("Java event listener required"); return; }
        int faili_kielezo = jina_mbinu(힙[lengo_anwani] - 32, 사건번호 == 0 ? (한국어 ? "tekeleza_kazi" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (faili_kielezo < 0) { kushindwa_thamani("event callback missing"); return; }
        현재가닥 = 0; 가닥수 = 1; fremu_kielezo = 0; mtungo_hali[0] = 1; fremu_Mpororo[0] = 0; 틀잠금[0] = anzilisha_fremu[0] = 0; 바꿈요청 = false;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 128; kitanzi_kielezo++) { jirani_thamani[kitanzi_kielezo] = jirani_aina[kitanzi_kielezo] = 0; }
        fremu_mbinu[0] = faili_kielezo; 틀위치[0] = mbinu_Anza[faili_kielezo]; jirani_thamani[0] = lengo_anwani; jirani_aina[0] = 2;
        if (사건번호 != 0) { jirani_thamani[1] = 사건번호; jirani_aina[1] = 2; }
        사건중 = true; tekeleza_amri(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!kosa) {
            if (나중수 > 0) { int lengo_anwani = 나중실행[0], 한국어 = 나중한국어[0]; for (int kitanzi_kielezo = 1; kitanzi_kielezo < 나중수; kitanzi_kielezo++) { 나중실행[kitanzi_kielezo - 1] = 나중실행[kitanzi_kielezo]; 나중한국어[kitanzi_kielezo - 1] = 나중한국어[kitanzi_kielezo]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(lengo_anwani, 0, 한국어 != 0); continue; }
            if (mtumiaji.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = mtumiaji.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { kushindwa_thamani("GUI event I/O failed"); return; }
            int akaunti_thamani = 사건번호 & 65535; if (akaunti_thamani < 1 || akaunti_thamani > 32) continue; int kipengee_Marejeleo = 화면참조[akaunti_thamani - 1]; if (kipengee_Marejeleo == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[kipengee_Marejeleo + 10] != 0) 힙[kipengee_Marejeleo + 9] = 0;
                if (힙[kipengee_Marejeleo + 10] == 3) for (int kitanzi_kielezo = 0; kitanzi_kielezo < 32; kitanzi_kielezo++) if (화면참조[kitanzi_kielezo] != 0 && 힙[화면참조[kitanzi_kielezo]] == 24) mtumiaji.화면연결(4, kitanzi_kielezo + 1, 0, 0, 0, 0);
            } else if (힙[kipengee_Marejeleo + 4] != 0) {
                int NISOME_Marejeleo = tengea_Hifadhi(29, 2); if (kosa) return; 힙[NISOME_Marejeleo + 2] = kipengee_Marejeleo; 힙[NISOME_Marejeleo + 3] = 힙[kipengee_Marejeleo + 12]; 힙참조[NISOME_Marejeleo + 2] = 1; 사건실행(힙[kipengee_Marejeleo + 4], NISOME_Marejeleo, 힙[kipengee_Marejeleo + 12] != 0);
            }
        }
    }
    public static int endesha() {
        if (mtumiaji.인수개수() == 1 && 자바도구.같음(mtumiaji.인수(0), "-version")) {
            mtumiaji.andika("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (mtumiaji.인수개수() < 1) { mtumiaji.andika("Usage: java CLASS [ARGS]\n"); return 2; }
        ingizo_tabaka_Ufafanuzi = pakia_tabaka_Ufafanuzi(mwenyeji_kibambo(mtumiaji.인수(0))); if (kosa || ingizo_tabaka_Ufafanuzi < 0) return 1;
        int ingizo_pointi_thamani = jina_mbinu(ingizo_tabaka_Ufafanuzi, "endesha", "()V");
        boolean 한국어진입 = ingizo_pointi_thamani >= 0 && (mbinu_fikia[ingizo_pointi_thamani] & 9) == 9;
        if (!한국어진입) ingizo_pointi_thamani = jina_mbinu(ingizo_tabaka_Ufafanuzi, "main", "([Ljava/lang/String;)V");
        if (ingizo_pointi_thamani < 0 || (mbinu_fikia[ingizo_pointi_thamani] & 9) != 9) kushindwa_thamani("public static void endesha() or main(String[] args) required");
        if (kosa) return 1;
        int 인수 = tengea_Hifadhi(3, mtumiaji.인수개수() - 1); ARRAY_elementi[인수] = -1;
        for (int 수 = 1; 수 < mtumiaji.인수개수() && !kosa; 수++) 힙[인수 + 1 + 수] = mwenyeji_kibambo(mtumiaji.인수(수));
        fremu_kielezo = 0; fremu_mbinu[0] = ingizo_pointi_thamani; 틀위치[0] = mbinu_Anza[ingizo_pointi_thamani]; jirani_thamani[0] = 한국어진입 ? 0 : 인수; jirani_aina[0] = 한국어진입 ? 0 : 2;
        mtungo_hali[0] = 1; mtungo_kipengee[0] = tengea_Hifadhi(13, 2);
        tekeleza_amri(); if (!kosa) 화면사건들(); return kosa ? 1 : 0;
    }
}
