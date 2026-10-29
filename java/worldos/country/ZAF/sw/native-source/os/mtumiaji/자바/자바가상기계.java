// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. faili/스택/Marejeleo/tawi 경계를 tekeleza_amri 중 검사한다. */
public final class 자바가상기계 {
    static int[] faili = new int[16384], faili_jina_SMS = new int[64];
    static int[] kisobadilika_lebo = new int[512], 상가 = new int[512], 상나 = new int[512], tungo_Marejeleo = new int[512];
    static int[] mbinu_jina_SMS = new int[32], mbinu_aina = new int[32], mbinu_fikia = new int[32];
    static int[] mbinu_Anza = new int[32], mbinu_tamatia = new int[32], mbinu_Mpororo = new int[32], 함수지역 = new int[32];
    static int[] 함수인수수 = new int[32], mbinu_hoja_aina = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] jirani_thamani = new int[4096], jirani_aina = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] fremu_mbinu = new int[32], 틀위치 = new int[32], fremu_Mpororo = new int[32];
    static int[] 힙 = new int[8192];
    static int panga_ukubwa, 읽기위치, 상수수, 함수수, tabaka_jina, fremu_kielezo = -1, 힙끝 = 1, 반환형;
    static boolean kosa;

    static void kushindwa_thamani(String Neno_SMS) {
        if (!kosa) { mtumiaji.andika("JVM error: "); mtumiaji.andika(Neno_SMS); mtumiaji.andika_kibambo_thamani(10); }
        kosa = true;
    }
    static boolean dondoo(int endesha, int urefu_thamani) { return endesha >= 0 && urefu_thamani >= 0 && endesha <= panga_ukubwa - urefu_thamani; }
    static int baiti_thamani() {
        if (!dondoo(읽기위치, 1)) { kushindwa_thamani("truncated class file"); return 0; }
        return faili[읽기위치++];
    }
    static int 짧은수() { return baiti_thamani() << 8 | baiti_thamani(); }
    static int namba_kamili() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int urefu_thamani) { if (!dondoo(읽기위치, urefu_thamani)) kushindwa_thamani("invalid attribute size"); else 읽기위치 += urefu_thamani; }
    static boolean hundi_kisobadilika(int 수, int 종류) {
        if (수 <= 0 || 수 >= 상수수 || kisobadilika_lebo[수] != 종류) { kushindwa_thamani("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int endesha, int urefu_thamani, String Neno_SMS) {
        if (!dondoo(endesha, urefu_thamani) || urefu_thamani != Neno_SMS.length()) return false;
        for (int 수 = 0; 수 < urefu_thamani; 수++) if (faili[endesha + 수] != Neno_SMS.charAt(수)) return false;
        return true;
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
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !kosa; 수++) { hundi_kisobadilika(짧은수(), 1); 건너(namba_kamili()); }
    }
    static int amri_urefu(int thamani) {
        if (thamani == 16 || thamani == 18 || thamani == 21 || thamani == 25 || thamani == 54 || thamani == 58 || thamani == 188) return 2;
        if (thamani == 17 || thamani == 19 || thamani == 132 || thamani >= 153 && thamani <= 167
            || thamani >= 178 && thamani <= 184 || thamani == 187 || thamani == 189 || thamani == 192 || thamani == 198 || thamani == 199) return 3;
        if (thamani >= 0 && thamani <= 8 || thamani >= 26 && thamani <= 29 || thamani >= 42 && thamani <= 46 || thamani == 50
            || thamani >= 59 && thamani <= 62 || thamani >= 75 && thamani <= 79 || thamani == 83 || thamani == 87 || thamani == 89 || thamani == 95
            || thamani == 96 || thamani == 100 || thamani == 104 || thamani == 108 || thamani == 112 || thamani == 116
            || thamani == 120 || thamani == 122 || thamani == 124 || thamani == 126 || thamani == 128 || thamani == 130
            || thamani >= 145 && thamani <= 147 || thamani == 172 || thamani == 176 || thamani == 177 || thamani == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (namba_kamili() != 0xcafebabe) kushindwa_thamani("not a class file");
        int 부판 = 짧은수(), toleo_thamani = 짧은수();
        if (toleo_thamani < 45 || toleo_thamani > 52 || 부판 != 0) kushindwa_thamani("supported class versions: 45..52, minor 0");
        상수수 = 짧은수();
        if (상수수 < 1 || 상수수 > 512) { kushindwa_thamani("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < 상수수 && !kosa; 수++) {
            int 종류 = baiti_thamani(); kisobadilika_lebo[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = namba_kamili();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); 상나[수] = 짧은수(); }
            else kushindwa_thamani("unsupported constant type");
        }
        int kibali_thamani = 짧은수();
        if ((kibali_thamani & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) kushindwa_thamani("unsupported class flags");
        tabaka_jina = tabaka_jina_SMS(짧은수());
        if (!Neno_SMS(tabaka_jina_SMS(짧은수()), "java/lang/Object")) kushindwa_thamani("inheritance unsupported");
        if (짧은수() != 0) kushindwa_thamani("interfaces unsupported");
        if (짧은수() != 0) kushindwa_thamani("fields unsupported");
        함수수 = 짧은수();
        if (함수수 < 1 || 함수수 > 32) { kushindwa_thamani("method count limit (32)"); return; }
        for (int 수 = 0; 수 < 함수수 && !kosa; 수++) {
            mbinu_fikia[수] = 짧은수(); mbinu_jina_SMS[수] = 짧은수(); mbinu_aina[수] = 짧은수();
            hundi_kisobadilika(mbinu_jina_SMS[수], 1); 서술읽기(수);
            if ((mbinu_fikia[수] & (0x100 | 0x400 | 0x20)) != 0) kushindwa_thamani("native, abstract and synchronized methods unsupported");
            if ((mbinu_fikia[수] & 8) == 0 && !Neno_SMS(mbinu_jina_SMS[수], "<init>")) kushindwa_thamani("instance methods unsupported");
            if (Neno_SMS(mbinu_jina_SMS[수], "<clinit>")) kushindwa_thamani("class initializers unsupported");
            for (int mbele_thamani = 0; mbele_thamani < 수; mbele_thamani++) if (같은말(mbinu_jina_SMS[mbele_thamani], mbinu_jina_SMS[수]) && 같은말(mbinu_aina[mbele_thamani], mbinu_aina[수])) kushindwa_thamani("duplicate method");
            int 개수 = 짧은수();
            for (int sifa_thamani = 0; sifa_thamani < 개수 && !kosa; sifa_thamani++) {
                int Jina = 짧은수(), urefu_thamani = namba_kamili(), endesha = 읽기위치;
                if (!dondoo(endesha, urefu_thamani)) { kushindwa_thamani("truncated method attribute"); break; }
                if (Neno_SMS(Jina, "Code")) {
                    if (mbinu_Anza[수] != 0) kushindwa_thamani("duplicate Code attribute");
                    mbinu_Mpororo[수] = 짧은수(); 함수지역[수] = 짧은수(); int msimbo_urefu = namba_kamili();
                    if (mbinu_Mpororo[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || msimbo_urefu < 1 || msimbo_urefu > 8192) kushindwa_thamani("method memory limits exceeded");
                    mbinu_Anza[수] = 읽기위치; 건너(msimbo_urefu); mbinu_tamatia[수] = 읽기위치;
                    if (짧은수() != 0) kushindwa_thamani("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != endesha + urefu_thamani) kushindwa_thamani("Code attribute size mismatch");
                } else 건너(urefu_thamani);
            }
            if (mbinu_Anza[수] == 0) kushindwa_thamani("missing Code attribute");
            int Sloti_ingizo = mbinu_Anza[수];
            while (Sloti_ingizo < mbinu_tamatia[수] && !kosa) {
                int urefu_thamani = amri_urefu(faili[Sloti_ingizo]);
                if (urefu_thamani == 0 || urefu_thamani > mbinu_tamatia[수] - Sloti_ingizo) { kushindwa_thamani("unsupported or truncated bytecode"); break; }
                경계[Sloti_ingizo] = 수 + 1; Sloti_ingizo += urefu_thamani;
            }
            // 실행하지 않는 경로에도 잘못된 tawi 목적지를 허용하지 않는다.
            Sloti_ingizo = mbinu_Anza[수];
            while (Sloti_ingizo < mbinu_tamatia[수] && !kosa) {
                int thamani = faili[Sloti_ingizo];
                if (thamani >= 153 && thamani <= 167 || thamani == 198 || thamani == 199) {
                    int fikio_thamani = Sloti_ingizo + (short)(faili[Sloti_ingizo + 1] << 8 | faili[Sloti_ingizo + 2]);
                    if (fikio_thamani < mbinu_Anza[수] || fikio_thamani >= mbinu_tamatia[수] || 경계[fikio_thamani] != 수 + 1) kushindwa_thamani("invalid branch target");
                }
                Sloti_ingizo += amri_urefu(thamani);
            }
        }
        if (!kosa) 속성건너();
        if (읽기위치 != panga_ukubwa) kushindwa_thamani("extra class file data");
    }
    static int tengea_Hifadhi(int 종류, int urefu_thamani) {
        if (urefu_thamani < 0 || urefu_thamani > 힙.length - 힙끝 - 2) { kushindwa_thamani("object heap exhausted or negative array size"); return 0; }
        int Marejeleo = 힙끝; 힙끝 += urefu_thamani + 2; 힙[Marejeleo] = 종류; 힙[Marejeleo + 1] = urefu_thamani;
        return Marejeleo;
    }
    static boolean kipengee_thamani(int Marejeleo, int 종류) {
        if (Marejeleo < 1 || Marejeleo >= 힙끝 - 1 || 힙[Marejeleo] != 종류) { kushindwa_thamani("null or invalid object reference"); return false; }
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
        if (fremu_kielezo == 31) { kushindwa_thamani("call stack limit (32)"); return; }
        int 다음 = fremu_kielezo + 1;
        for (int 수 = 0; 수 < 128; 수++) jirani_aina[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[KITENDAKAZI_thamani] - 1; 수 >= 0; 수--) {
            jirani_thamani[다음 * 128 + 수] = 빼기(mbinu_hoja_aina[KITENDAKAZI_thamani * 16 + 수]); jirani_aina[다음 * 128 + 수] = mbinu_hoja_aina[KITENDAKAZI_thamani * 16 + 수];
        }
        fremu_kielezo = 다음; fremu_mbinu[fremu_kielezo] = KITENDAKAZI_thamani; 틀위치[fremu_kielezo] = mbinu_Anza[KITENDAKAZI_thamani]; fremu_Mpororo[fremu_kielezo] = 0;
    }
    static void 반환(int aina_thamani) {
        if (aina_thamani != 함수반환[fremu_mbinu[fremu_kielezo]]) { kushindwa_thamani("return type mismatch"); return; }
        int thamani = aina_thamani == 0 ? 0 : 빼기(aina_thamani);
        fremu_kielezo--; if (fremu_kielezo >= 0 && aina_thamani != 0) 넣기(thamani, aina_thamani);
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
                if (thamani < 1 || thamani > 127) { kushindwa_thamani("file stream paths currently require ASCII"); return; }
                Stream_faili_jina[Sloti_ingizo] = thamani;
            }
            Stream_faili_jina[urefu_thamani] = 0;
            int 서술자 = mtumiaji.파일서술자열기(Stream_faili_jina, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { kushindwa_thamani("FileNotFoundException: file open failed"); return; }
            힙[Stream_thamani + 2] = 서술자; 힙[Stream_thamani + 3] = 1;
            return;
        }
        if (amri != 182) { kushindwa_thamani("invalid file stream invocation"); return; }
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
            if (결과 < -1) kushindwa_thamani("IOException: read failed"); else 넣기(결과, 1);
        } else if (mtumiaji.파일한바이트쓰기(서술자, thamani) != 1) kushindwa_thamani("IOException: write failed");
    }
    static void ita_mbinu(int kielezo, int amri) {
        if (!hundi_kisobadilika(kielezo, 10)) return;
        int mmiliki_thamani = tabaka_jina_SMS(상가[kielezo]), Jina = Marejeleo_jina(상나[kielezo]), umbiza_thamani = Marejeleo_aina(상나[kielezo]);
        if (kosa) return;
        if (같은말(mmiliki_thamani, tabaka_jina)) {
            if (amri != 184) { kushindwa_thamani("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < 함수수; 수++) if (같은말(Jina, mbinu_jina_SMS[수]) && 같은말(umbiza_thamani, mbinu_aina[수])) {
                if ((mbinu_fikia[수] & 8) == 0) kushindwa_thamani("method is not static"); else 호출(수);
                return;
            }
            kushindwa_thamani("NoSuchMethodError"); return;
        }
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
        kushindwa_thamani("unsupported library method");
    }
    static int ARRAY_Sloti(int Marejeleo, int hati_chini_thamani, int aina_thamani) {
        if (!kipengee_thamani(Marejeleo, aina_thamani)) return 0;
        if (hati_chini_thamani < 0 || hati_chini_thamani >= 힙[Marejeleo + 1]) { kushindwa_thamani("ArrayIndexOutOfBoundsException"); return 0; }
        return Marejeleo + 2 + hati_chini_thamani;
    }
    static void tekeleza_amri() {
        int 남음 = 500000;
        while (fremu_kielezo >= 0 && !kosa) {
            if (--남음 == 0) { kushindwa_thamani("instruction limit (500000)"); break; }
            int endesha = 틀위치[fremu_kielezo], thamani = 명바();
            if (kosa) break;
            if (thamani == 0) continue;
            if (thamani == 1) { 넣기(0, 2); continue; }
            if (thamani >= 2 && thamani <= 8) { 넣기(thamani - 3, 1); continue; }
            if (thamani == 16) { 넣기((byte)명바(), 1); continue; }
            if (thamani == 17) { 넣기((short)명짧(), 1); continue; }
            if (thamani == 18 || thamani == 19) {
                int 수 = thamani == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= 상수수) kushindwa_thamani("invalid ldc constant");
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
            if (thamani == 46 || thamani == 50) {
                int hati_chini_thamani = 빼기(1), Marejeleo = 빼기(2), Sloti_ingizo = ARRAY_Sloti(Marejeleo, hati_chini_thamani, thamani == 46 ? 2 : 3);
                if (!kosa) 넣기(힙[Sloti_ingizo], thamani == 46 ? 1 : 2); continue;
            }
            if (thamani == 79 || thamani == 83) {
                int kipengee_elementi = 빼기(thamani == 79 ? 1 : 2), hati_chini_thamani = 빼기(1), Marejeleo = 빼기(2), Sloti_ingizo = ARRAY_Sloti(Marejeleo, hati_chini_thamani, thamani == 79 ? 2 : 3);
                if (thamani == 83 && kipengee_elementi != 0) kipengee_thamani(kipengee_elementi, 1);
                if (!kosa) 힙[Sloti_ingizo] = kipengee_elementi; continue;
            }
            if (thamani == 87) { 빼기(0); continue; }
            if (thamani == 89) { int 가 = 빼기(0), aina_thamani = 반환형; 넣기(가, aina_thamani); 넣기(가, aina_thamani); continue; }
            if (thamani == 95) { int 가 = 빼기(0), 가형 = 반환형, 나 = 빼기(0), 나형 = 반환형; 넣기(가, 가형); 넣기(나, 나형); continue; }
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
            if (thamani == 178) {
                int 수 = 명짧(); if (!hundi_kisobadilika(수, 9)) continue;
                if (!Neno_SMS(tabaka_jina_SMS(상가[수]), "java/lang/System") || !Neno_SMS(Marejeleo_jina(상나[수]), "out")
                    || !Neno_SMS(Marejeleo_aina(상나[수]), "Ljava/io/PrintStream;")) kushindwa_thamani("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (thamani == 182 || thamani == 183 || thamani == 184) { ita_mbinu(명짧(), thamani); continue; }
            if (thamani == 187) {
                int Jina = tabaka_jina_SMS(명짧());
                if (Neno_SMS(Jina, "java/lang/StringBuilder")) 넣기(tengea_Hifadhi(4, 1), 2);
                else if (Neno_SMS(Jina, "java/io/FileInputStream") || Neno_SMS(Jina, "java/io/FileOutputStream")) {
                    int Marejeleo = tengea_Hifadhi(Neno_SMS(Jina, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!kosa) { 힙[Marejeleo + 2] = -1; 넣기(Marejeleo, 2); }
                } else kushindwa_thamani("unsupported object construction");
                continue;
            }
            if (thamani == 188 || thamani == 189) {
                if (thamani == 188) { if (명바() != 10) kushindwa_thamani("only int[] newarray is supported"); }
                else if (!Neno_SMS(tabaka_jina_SMS(명짧()), "java/lang/String")) kushindwa_thamani("only String[] anewarray is supported");
                int urefu_thamani = 빼기(1); 넣기(tengea_Hifadhi(thamani == 188 ? 2 : 3, urefu_thamani), 2); continue;
            }
            if (thamani == 190) {
                int Marejeleo = 빼기(2);
                if (Marejeleo < 1 || Marejeleo >= 힙끝 - 1 || (힙[Marejeleo] != 2 && 힙[Marejeleo] != 3)) kushindwa_thamani("null or invalid array");
                else 넣기(힙[Marejeleo + 1], 1); continue;
            }
            if (thamani == 192) {
                int Jina = tabaka_jina_SMS(명짧()), Marejeleo = 빼기(2);
                if (!Neno_SMS(Jina, "java/lang/String")) kushindwa_thamani("unsupported checkcast");
                else if (Marejeleo != 0) kipengee_thamani(Marejeleo, 1);
                넣기(Marejeleo, 2); continue;
            }
            kushindwa_thamani("unsupported bytecode");
        }
    }
    public static int endesha() {
        if (mtumiaji.인수개수() == 1 && 자바도구.같음(mtumiaji.인수(0), "-version")) {
            mtumiaji.andika("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (mtumiaji.인수개수() < 1) { mtumiaji.andika("Usage: java CLASS [ARGS]\n"); return 2; }
        int urefu_thamani = 자바도구.Jina(faili_jina_SMS, mtumiaji.인수(0));
        if (urefu_thamani < 1 || urefu_thamani > 57) { mtumiaji.andika("java: invalid class name\n"); return 2; }
        faili_jina_SMS[urefu_thamani] = '.'; faili_jina_SMS[urefu_thamani + 1] = 'c'; faili_jina_SMS[urefu_thamani + 2] = 'l'; faili_jina_SMS[urefu_thamani + 3] = 'a'; faili_jina_SMS[urefu_thamani + 4] = 's'; faili_jina_SMS[urefu_thamani + 5] = 's';
        panga_ukubwa = mtumiaji.파일읽기(faili_jina_SMS, faili);
        if (panga_ukubwa < 0) { mtumiaji.andika("java: cannot read class: "); 자바도구.수쓰기(panga_ukubwa); mtumiaji.andika_kibambo_thamani(10); return 1; }
        클래스읽기(); if (kosa) return 1;
        int kibambo_jina = kisobadilika_SMS(tabaka_jina);
        if (!kosa && 힙[kibambo_jina + 1] != urefu_thamani) kushindwa_thamani("class name does not match file");
        for (int 수 = 0; 수 < urefu_thamani && !kosa; 수++) if (힙[kibambo_jina + 2 + 수] != faili_jina_SMS[수]) kushindwa_thamani("class name does not match file");
        int ingizo_pointi_thamani = -1;
        for (int 수 = 0; 수 < 함수수; 수++) if (Neno_SMS(mbinu_jina_SMS[수], "main") && Neno_SMS(mbinu_aina[수], "([Ljava/lang/String;)V") && (mbinu_fikia[수] & 9) == 9) ingizo_pointi_thamani = 수;
        if (ingizo_pointi_thamani < 0) kushindwa_thamani("public static void main(String[] args) required");
        if (kosa) return 1;
        int 인수 = tengea_Hifadhi(3, mtumiaji.인수개수() - 1);
        for (int 수 = 1; 수 < mtumiaji.인수개수() && !kosa; 수++) 힙[인수 + 1 + 수] = mwenyeji_kibambo(mtumiaji.인수(수));
        fremu_kielezo = 0; fremu_mbinu[0] = ingizo_pointi_thamani; 틀위치[0] = mbinu_Anza[ingizo_pointi_thamani]; jirani_thamani[0] = 인수; jirani_aina[0] = 2;
        tekeleza_amri(); return kosa ? 1 : 0;
    }
}
