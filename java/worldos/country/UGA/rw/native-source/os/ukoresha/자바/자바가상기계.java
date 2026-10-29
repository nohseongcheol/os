// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Idosiye/스택/Indanga/ishami 경계를 gukora_ibwiriza 중 검사한다. */
public final class 자바가상기계 {
    static int[] Idosiye = new int[16384], dosiye_izina_SMS = new int[64];
    static int[] kidahinduka_Akarango = new int[512], 상가 = new int[512], 상나 = new int[512], igicenteruro_Indanga = new int[512];
    static int[] uburyo_izina_SMS = new int[32], 함수형 = new int[32], uburyo_kwinjira = new int[32];
    static int[] uburyo_Itangira = new int[32], uburyo_kurangiza = new int[32], uburyo_Ikirundo = new int[32], 함수지역 = new int[32];
    static int[] 함수인수수 = new int[32], 함수인수형 = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] mu_gace_agaciro = new int[4096], 지역형 = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] ikadiri_uburyo = new int[32], 틀위치 = new int[32], ikadiri_Ikirundo = new int[32];
    static int[] 힙 = new int[8192];
    static int Ingano, 읽기위치, 상수수, 함수수, icyiciro_izina, ikadiri_umugerekashakiro = -1, 힙끝 = 1, 반환형;
    static boolean IKOSA;

    static void kudakora_agaciro(String Ijambo_SMS) {
        if (!IKOSA) { ukoresha.kwandika("JVM error: "); ukoresha.kwandika(Ijambo_SMS); ukoresha.kwandika_inyuguti_agaciro(10); }
        IKOSA = true;
    }
    static boolean kiripu(int ihuriro, int uburebure_agaciro) { return ihuriro >= 0 && uburebure_agaciro >= 0 && ihuriro <= Ingano - uburebure_agaciro; }
    static int bayiti_agaciro() {
        if (!kiripu(읽기위치, 1)) { kudakora_agaciro("truncated class file"); return 0; }
        return Idosiye[읽기위치++];
    }
    static int 짧은수() { return bayiti_agaciro() << 8 | bayiti_agaciro(); }
    static int umubare_wuzuye() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int uburebure_agaciro) { if (!kiripu(읽기위치, uburebure_agaciro)) kudakora_agaciro("invalid attribute size"); else 읽기위치 += uburebure_agaciro; }
    static boolean sheki_kidahinduka(int 수, int 종류) {
        if (수 <= 0 || 수 >= 상수수 || kidahinduka_Akarango[수] != 종류) { kudakora_agaciro("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int ihuriro, int uburebure_agaciro, String Ijambo_SMS) {
        if (!kiripu(ihuriro, uburebure_agaciro) || uburebure_agaciro != Ijambo_SMS.length()) return false;
        for (int 수 = 0; 수 < uburebure_agaciro; 수++) if (Idosiye[ihuriro + 수] != Ijambo_SMS.charAt(수)) return false;
        return true;
    }
    static boolean Ijambo_SMS(int kidahinduka_agaciro, String Ijambo_SMS) { return sheki_kidahinduka(kidahinduka_agaciro, 1) && 구간(상가[kidahinduka_agaciro], 상나[kidahinduka_agaciro], Ijambo_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!sheki_kidahinduka(가, 1) || !sheki_kidahinduka(나, 1) || 상나[가] != 상나[나]) return false;
        for (int 수 = 0; 수 < 상나[가]; 수++) if (Idosiye[상가[가] + 수] != Idosiye[상가[나] + 수]) return false;
        return true;
    }
    static int icyiciro_izina_SMS(int 수) { return sheki_kidahinduka(수, 7) && sheki_kidahinduka(상가[수], 1) ? 상가[수] : 0; }
    static int Indanga_izina(int 수) { return sheki_kidahinduka(수, 12) && sheki_kidahinduka(상가[수], 1) ? 상가[수] : 0; }
    static int 참조형식(int 수) { return sheki_kidahinduka(수, 12) && sheki_kidahinduka(상나[수], 1) ? 상나[수] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (읽기위치 >= 끝) { kudakora_agaciro("invalid descriptor"); return 0; }
        int agaciro = bayiti_agaciro();
        if (agaciro == 'V' && 빈형) return 0;
        if (agaciro == 'I' || agaciro == 'B' || agaciro == 'C' || agaciro == 'S' || agaciro == 'Z') return 1;
        if (agaciro == '[') { 서술형(끝, false); return 2; }
        if (agaciro == 'L') {
            int ihuriro = 읽기위치;
            while (읽기위치 < 끝 && Idosiye[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == ihuriro) kudakora_agaciro("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        kudakora_agaciro("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNCTION_agaciro) {
        int 이전 = 읽기위치, 수 = 함수형[FUNCTION_agaciro];
        if (!sheki_kidahinduka(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + 상나[수];
        if (bayiti_agaciro() != '(') kudakora_agaciro("invalid method descriptor");
        int 개수 = 0;
        while (!IKOSA && 읽기위치 < 끝 && Idosiye[읽기위치] != ')') {
            if (개수 == 16) { kudakora_agaciro("too many method arguments"); break; }
            함수인수형[FUNCTION_agaciro * 16 + 개수++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || bayiti_agaciro() != ')') kudakora_agaciro("invalid method descriptor");
        함수반환[FUNCTION_agaciro] = 서술형(끝, true); 함수인수수[FUNCTION_agaciro] = 개수;
        if (읽기위치 != 끝) kudakora_agaciro("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !IKOSA; 수++) { sheki_kidahinduka(짧은수(), 1); 건너(umubare_wuzuye()); }
    }
    static int ibwiriza_uburebure(int agaciro) {
        if (agaciro == 16 || agaciro == 18 || agaciro == 21 || agaciro == 25 || agaciro == 54 || agaciro == 58 || agaciro == 188) return 2;
        if (agaciro == 17 || agaciro == 19 || agaciro == 132 || agaciro >= 153 && agaciro <= 167
            || agaciro >= 178 && agaciro <= 184 || agaciro == 187 || agaciro == 189 || agaciro == 192 || agaciro == 198 || agaciro == 199) return 3;
        if (agaciro >= 0 && agaciro <= 8 || agaciro >= 26 && agaciro <= 29 || agaciro >= 42 && agaciro <= 46 || agaciro == 50
            || agaciro >= 59 && agaciro <= 62 || agaciro >= 75 && agaciro <= 79 || agaciro == 83 || agaciro == 87 || agaciro == 89 || agaciro == 95
            || agaciro == 96 || agaciro == 100 || agaciro == 104 || agaciro == 108 || agaciro == 112 || agaciro == 116
            || agaciro == 120 || agaciro == 122 || agaciro == 124 || agaciro == 126 || agaciro == 128 || agaciro == 130
            || agaciro >= 145 && agaciro <= 147 || agaciro == 172 || agaciro == 176 || agaciro == 177 || agaciro == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (umubare_wuzuye() != 0xcafebabe) kudakora_agaciro("not a class file");
        int 부판 = 짧은수(), verisiyo_agaciro = 짧은수();
        if (verisiyo_agaciro < 45 || verisiyo_agaciro > 52 || 부판 != 0) kudakora_agaciro("supported class versions: 45..52, minor 0");
        상수수 = 짧은수();
        if (상수수 < 1 || 상수수 > 512) { kudakora_agaciro("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < 상수수 && !IKOSA; 수++) {
            int 종류 = bayiti_agaciro(); kidahinduka_Akarango[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = umubare_wuzuye();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); 상나[수] = 짧은수(); }
            else kudakora_agaciro("unsupported constant type");
        }
        int 권한 = 짧은수();
        if ((권한 & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) kudakora_agaciro("unsupported class flags");
        icyiciro_izina = icyiciro_izina_SMS(짧은수());
        if (!Ijambo_SMS(icyiciro_izina_SMS(짧은수()), "java/lang/Object")) kudakora_agaciro("inheritance unsupported");
        if (짧은수() != 0) kudakora_agaciro("interfaces unsupported");
        if (짧은수() != 0) kudakora_agaciro("fields unsupported");
        함수수 = 짧은수();
        if (함수수 < 1 || 함수수 > 32) { kudakora_agaciro("method count limit (32)"); return; }
        for (int 수 = 0; 수 < 함수수 && !IKOSA; 수++) {
            uburyo_kwinjira[수] = 짧은수(); uburyo_izina_SMS[수] = 짧은수(); 함수형[수] = 짧은수();
            sheki_kidahinduka(uburyo_izina_SMS[수], 1); 서술읽기(수);
            if ((uburyo_kwinjira[수] & (0x100 | 0x400 | 0x20)) != 0) kudakora_agaciro("native, abstract and synchronized methods unsupported");
            if ((uburyo_kwinjira[수] & 8) == 0 && !Ijambo_SMS(uburyo_izina_SMS[수], "<init>")) kudakora_agaciro("instance methods unsupported");
            if (Ijambo_SMS(uburyo_izina_SMS[수], "<clinit>")) kudakora_agaciro("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(uburyo_izina_SMS[앞], uburyo_izina_SMS[수]) && 같은말(함수형[앞], 함수형[수])) kudakora_agaciro("duplicate method");
            int 개수 = 짧은수();
            for (int ikiranga_agaciro = 0; ikiranga_agaciro < 개수 && !IKOSA; ikiranga_agaciro++) {
                int Izina = 짧은수(), uburebure_agaciro = umubare_wuzuye(), ihuriro = 읽기위치;
                if (!kiripu(ihuriro, uburebure_agaciro)) { kudakora_agaciro("truncated method attribute"); break; }
                if (Ijambo_SMS(Izina, "Code")) {
                    if (uburyo_Itangira[수] != 0) kudakora_agaciro("duplicate Code attribute");
                    uburyo_Ikirundo[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = umubare_wuzuye();
                    if (uburyo_Ikirundo[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) kudakora_agaciro("method memory limits exceeded");
                    uburyo_Itangira[수] = 읽기위치; 건너(코드길이); uburyo_kurangiza[수] = 읽기위치;
                    if (짧은수() != 0) kudakora_agaciro("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != ihuriro + uburebure_agaciro) kudakora_agaciro("Code attribute size mismatch");
                } else 건너(uburebure_agaciro);
            }
            if (uburyo_Itangira[수] == 0) kudakora_agaciro("missing Code attribute");
            int umwanya_icyinjizwa = uburyo_Itangira[수];
            while (umwanya_icyinjizwa < uburyo_kurangiza[수] && !IKOSA) {
                int uburebure_agaciro = ibwiriza_uburebure(Idosiye[umwanya_icyinjizwa]);
                if (uburebure_agaciro == 0 || uburebure_agaciro > uburyo_kurangiza[수] - umwanya_icyinjizwa) { kudakora_agaciro("unsupported or truncated bytecode"); break; }
                경계[umwanya_icyinjizwa] = 수 + 1; umwanya_icyinjizwa += uburebure_agaciro;
            }
            // 실행하지 않는 경로에도 잘못된 ishami 목적지를 허용하지 않는다.
            umwanya_icyinjizwa = uburyo_Itangira[수];
            while (umwanya_icyinjizwa < uburyo_kurangiza[수] && !IKOSA) {
                int agaciro = Idosiye[umwanya_icyinjizwa];
                if (agaciro >= 153 && agaciro <= 167 || agaciro == 198 || agaciro == 199) {
                    int aho_ijya_agaciro = umwanya_icyinjizwa + (short)(Idosiye[umwanya_icyinjizwa + 1] << 8 | Idosiye[umwanya_icyinjizwa + 2]);
                    if (aho_ijya_agaciro < uburyo_Itangira[수] || aho_ijya_agaciro >= uburyo_kurangiza[수] || 경계[aho_ijya_agaciro] != 수 + 1) kudakora_agaciro("invalid branch target");
                }
                umwanya_icyinjizwa += ibwiriza_uburebure(agaciro);
            }
        }
        if (!IKOSA) 속성건너();
        if (읽기위치 != Ingano) kudakora_agaciro("extra class file data");
    }
    static int kugenera_Ububiko(int 종류, int uburebure_agaciro) {
        if (uburebure_agaciro < 0 || uburebure_agaciro > 힙.length - 힙끝 - 2) { kudakora_agaciro("object heap exhausted or negative array size"); return 0; }
        int Indanga = 힙끝; 힙끝 += uburebure_agaciro + 2; 힙[Indanga] = 종류; 힙[Indanga + 1] = uburebure_agaciro;
        return Indanga;
    }
    static boolean ikintu_agaciro_2ed200e9(int Indanga, int 종류) {
        if (Indanga < 1 || Indanga >= 힙끝 - 1 || 힙[Indanga] != 종류) { kudakora_agaciro("null or invalid object reference"); return false; }
        return true;
    }
    static int kidahinduka_SMS(int umugerekashakiro) {
        if (!sheki_kidahinduka(umugerekashakiro, 1)) return 0;
        if (igicenteruro_Indanga[umugerekashakiro] != 0) return igicenteruro_Indanga[umugerekashakiro];
        int Indanga = kugenera_Ububiko(1, 상나[umugerekashakiro]); if (IKOSA) return 0;
        int 끝 = 상가[umugerekashakiro] + 상나[umugerekashakiro], 수 = 상가[umugerekashakiro], uburebure_agaciro = 0;
        while (수 < 끝 && !IKOSA) {
            int agaciro = Idosiye[수++];
            if (agaciro == 0) kudakora_agaciro("invalid modified UTF-8");
            else if (agaciro >= 192 && agaciro <= 223 && 수 < 끝) {
                int 다음 = Idosiye[수++];
                if ((다음 & 192) != 128) kudakora_agaciro("invalid modified UTF-8");
                agaciro = (agaciro & 31) << 6 | 다음 & 63;
                if (agaciro != 0 && agaciro < 128) kudakora_agaciro("overlong modified UTF-8");
            } else if (agaciro >= 224 && agaciro <= 239 && 수 + 1 < 끝) {
                int 가 = Idosiye[수++], 나 = Idosiye[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) kudakora_agaciro("invalid modified UTF-8");
                agaciro = (agaciro & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (agaciro < 2048) kudakora_agaciro("overlong modified UTF-8");
            } else if (agaciro >= 128) kudakora_agaciro("invalid modified UTF-8");
            힙[Indanga + 2 + uburebure_agaciro++] = agaciro;
        }
        힙[Indanga + 1] = uburebure_agaciro; igicenteruro_Indanga[umugerekashakiro] = Indanga; return Indanga;
    }
    static int gucumbikira_inyuguti(String agaciro) {
        int Indanga = kugenera_Ububiko(1, agaciro.length()); if (IKOSA) return 0;
        for (int 수 = 0; 수 < agaciro.length(); 수++) 힙[Indanga + 2 + 수] = agaciro.charAt(수);
        return Indanga;
    }
    static void kwandika_SMS(int Indanga) {
        if (Indanga == 0) { ukoresha.kwandika("null"); return; }
        if (!ikintu_agaciro_2ed200e9(Indanga, 1)) return;
        for (int 수 = 0; 수 < 힙[Indanga + 1]; 수++) ukoresha.kwandika_inyuguti_agaciro(힙[Indanga + 2 + 수]);
    }
    static int umubare_inyuguti(int agaciro) {
        int Indanga = kugenera_Ububiko(1, 11); if (IKOSA) return 0;
        int uburebure_agaciro = 0;
        if (agaciro < 0) 힙[Indanga + 2 + uburebure_agaciro++] = '-'; else agaciro = -agaciro;
        int 자리 = 1000000000; boolean ihuriro = false;
        while (자리 != 0) {
            int 수 = -(agaciro / 자리);
            if (수 != 0 || ihuriro || 자리 == 1) { 힙[Indanga + 2 + uburebure_agaciro++] = '0' + 수; ihuriro = true; }
            agaciro %= 자리; 자리 /= 10;
        }
        힙[Indanga + 1] = uburebure_agaciro; return Indanga;
    }
    static int 정수해독(int Indanga) {
        if (!ikintu_agaciro_2ed200e9(Indanga, 1)) return 0;
        int uburebure_agaciro = 힙[Indanga + 1], 수 = 0, agaciro = 0; boolean 음수 = false;
        if (uburebure_agaciro > 0 && (힙[Indanga + 2] == '-' || 힙[Indanga + 2] == '+')) { 음수 = 힙[Indanga + 2] == '-'; 수++; }
        if (수 == uburebure_agaciro) kudakora_agaciro("NumberFormatException");
        for (; 수 < uburebure_agaciro && !IKOSA; 수++) {
            int umubare_agaciro = 힙[Indanga + 2 + 수] - '0';
            if (umubare_agaciro < 0 || umubare_agaciro > 9 || agaciro < -214748364 || agaciro == -214748364 && umubare_agaciro > (음수 ? 8 : 7)) kudakora_agaciro("NumberFormatException");
            agaciro = agaciro * 10 - umubare_agaciro;
        }
        return 음수 ? agaciro : -agaciro;
    }
    static void 넣기(int agaciro, int 형) {
        if (IKOSA) return;
        if (ikadiri_umugerekashakiro < 0 || ikadiri_Ikirundo[ikadiri_umugerekashakiro] >= uburyo_Ikirundo[ikadiri_uburyo[ikadiri_umugerekashakiro]]) { kudakora_agaciro("operand stack overflow"); return; }
        int umwanya_icyinjizwa = ikadiri_umugerekashakiro * 128 + ikadiri_Ikirundo[ikadiri_umugerekashakiro]++; 스택값[umwanya_icyinjizwa] = agaciro; 스택형[umwanya_icyinjizwa] = 형;
    }
    static int 빼기(int 형) {
        if (IKOSA) return 0;
        if (ikadiri_umugerekashakiro < 0 || ikadiri_Ikirundo[ikadiri_umugerekashakiro] < 1) { kudakora_agaciro("operand stack underflow"); return 0; }
        int umwanya_icyinjizwa = ikadiri_umugerekashakiro * 128 + --ikadiri_Ikirundo[ikadiri_umugerekashakiro]; 반환형 = 스택형[umwanya_icyinjizwa];
        if (형 != 0 && 반환형 != 형) kudakora_agaciro("operand type mismatch");
        return 스택값[umwanya_icyinjizwa];
    }
    static void 지역읽기(int umugerekashakiro, int 형) {
        if (umugerekashakiro >= 함수지역[ikadiri_uburyo[ikadiri_umugerekashakiro]] || umugerekashakiro < 0 || 지역형[ikadiri_umugerekashakiro * 128 + umugerekashakiro] != 형) { kudakora_agaciro("invalid or uninitialized local"); return; }
        넣기(mu_gace_agaciro[ikadiri_umugerekashakiro * 128 + umugerekashakiro], 형);
    }
    static void kwandika_mu_gace(int umugerekashakiro, int 형) {
        if (umugerekashakiro >= 함수지역[ikadiri_uburyo[ikadiri_umugerekashakiro]] || umugerekashakiro < 0) { kudakora_agaciro("local index out of range"); return; }
        int agaciro = 빼기(형); mu_gace_agaciro[ikadiri_umugerekashakiro * 128 + umugerekashakiro] = agaciro; 지역형[ikadiri_umugerekashakiro * 128 + umugerekashakiro] = 형;
    }
    static int 명바() {
        int 위치 = 틀위치[ikadiri_umugerekashakiro];
        if (위치 < uburyo_Itangira[ikadiri_uburyo[ikadiri_umugerekashakiro]] || 위치 >= uburyo_kurangiza[ikadiri_uburyo[ikadiri_umugerekashakiro]]) { kudakora_agaciro("instruction pointer out of range"); return 0; }
        틀위치[ikadiri_umugerekashakiro]++; return Idosiye[위치];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void kwimura_agaciro(int 위치) {
        int FUNCTION_agaciro = ikadiri_uburyo[ikadiri_umugerekashakiro];
        if (위치 < uburyo_Itangira[FUNCTION_agaciro] || 위치 >= uburyo_kurangiza[FUNCTION_agaciro] || 경계[위치] != FUNCTION_agaciro + 1) kudakora_agaciro("invalid branch target");
        else 틀위치[ikadiri_umugerekashakiro] = 위치;
    }
    static void 호출(int FUNCTION_agaciro) {
        if (ikadiri_umugerekashakiro == 31) { kudakora_agaciro("call stack limit (32)"); return; }
        int 다음 = ikadiri_umugerekashakiro + 1;
        for (int 수 = 0; 수 < 128; 수++) 지역형[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[FUNCTION_agaciro] - 1; 수 >= 0; 수--) {
            mu_gace_agaciro[다음 * 128 + 수] = 빼기(함수인수형[FUNCTION_agaciro * 16 + 수]); 지역형[다음 * 128 + 수] = 함수인수형[FUNCTION_agaciro * 16 + 수];
        }
        ikadiri_umugerekashakiro = 다음; ikadiri_uburyo[ikadiri_umugerekashakiro] = FUNCTION_agaciro; 틀위치[ikadiri_umugerekashakiro] = uburyo_Itangira[FUNCTION_agaciro]; ikadiri_Ikirundo[ikadiri_umugerekashakiro] = 0;
    }
    static void 반환(int 형) {
        if (형 != 함수반환[ikadiri_uburyo[ikadiri_umugerekashakiro]]) { kudakora_agaciro("return type mismatch"); return; }
        int agaciro = 형 == 0 ? 0 : 빼기(형);
        ikadiri_umugerekashakiro--; if (ikadiri_umugerekashakiro >= 0 && 형 != 0) 넣기(agaciro, 형);
    }
    static int[] Stream_dosiye_izina = new int[64];
    static void dosiye_Stream_Hamagara(int nyirayo_agaciro, int Izina, int imiterere_agaciro, int Icyo_wifuza) {
        boolean 출력 = Ijambo_SMS(nyirayo_agaciro, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (Icyo_wifuza == 183 && Ijambo_SMS(Izina, "<init>")) {
            boolean 이어 = false;
            if (출력 && Ijambo_SMS(imiterere_agaciro, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Ijambo_SMS(imiterere_agaciro, "(Ljava/lang/String;)V")) { kudakora_agaciro("unsupported file stream constructor"); return; }
            int dosiye_icyinjizwa_izina = 빼기(2), Stream_agaciro = 빼기(2);
            if (!ikintu_agaciro_2ed200e9(dosiye_icyinjizwa_izina, 1) || !ikintu_agaciro_2ed200e9(Stream_agaciro, 종류) || IKOSA) return;
            if (힙[Stream_agaciro + 3] != 0) { kudakora_agaciro("file stream already initialized"); return; }
            int uburebure_agaciro = 힙[dosiye_icyinjizwa_izina + 1];
            if (uburebure_agaciro < 1 || uburebure_agaciro > 63) { kudakora_agaciro("invalid file name length"); return; }
            for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < uburebure_agaciro; umwanya_icyinjizwa++) {
                int agaciro = 힙[dosiye_icyinjizwa_izina + 2 + umwanya_icyinjizwa];
                if (agaciro < 1 || agaciro > 127) { kudakora_agaciro("file stream paths currently require ASCII"); return; }
                Stream_dosiye_izina[umwanya_icyinjizwa] = agaciro;
            }
            Stream_dosiye_izina[uburebure_agaciro] = 0;
            int 서술자 = ukoresha.파일서술자열기(Stream_dosiye_izina, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { kudakora_agaciro("FileNotFoundException: file open failed"); return; }
            힙[Stream_agaciro + 2] = 서술자; 힙[Stream_agaciro + 3] = 1;
            return;
        }
        if (Icyo_wifuza != 182) { kudakora_agaciro("invalid file stream invocation"); return; }
        int Igikorwa = -1, agaciro = 0;
        if (Ijambo_SMS(Izina, "close") && Ijambo_SMS(imiterere_agaciro, "()V")) Igikorwa = 0;
        if (!출력 && Ijambo_SMS(Izina, "read") && Ijambo_SMS(imiterere_agaciro, "()I")) Igikorwa = 1;
        if (출력 && Ijambo_SMS(Izina, "write") && Ijambo_SMS(imiterere_agaciro, "(I)V")) { Igikorwa = 2; agaciro = 빼기(1); }
        if (Igikorwa < 0) { kudakora_agaciro("unsupported file stream method"); return; }
        int Stream_agaciro = 빼기(2);
        if (!ikintu_agaciro_2ed200e9(Stream_agaciro, 종류) || IKOSA) return;
        if (힙[Stream_agaciro + 3] == 0) { kudakora_agaciro("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_agaciro + 2];
        if (Igikorwa == 0) {
            if (서술자 >= 0 && ukoresha.파일서술자닫기(서술자) < 0) kudakora_agaciro("IOException: close failed");
            힙[Stream_agaciro + 2] = -1; return;
        }
        if (서술자 < 0) { kudakora_agaciro("IOException: stream closed"); return; }
        if (Igikorwa == 1) {
            int 결과 = ukoresha.파일한바이트읽기(서술자);
            if (결과 < -1) kudakora_agaciro("IOException: read failed"); else 넣기(결과, 1);
        } else if (ukoresha.파일한바이트쓰기(서술자, agaciro) != 1) kudakora_agaciro("IOException: write failed");
    }
    static void Hamagara_uburyo(int umugerekashakiro, int Icyo_wifuza) {
        if (!sheki_kidahinduka(umugerekashakiro, 10)) return;
        int nyirayo_agaciro = icyiciro_izina_SMS(상가[umugerekashakiro]), Izina = Indanga_izina(상나[umugerekashakiro]), imiterere_agaciro = 참조형식(상나[umugerekashakiro]);
        if (IKOSA) return;
        if (같은말(nyirayo_agaciro, icyiciro_izina)) {
            if (Icyo_wifuza != 184) { kudakora_agaciro("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < 함수수; 수++) if (같은말(Izina, uburyo_izina_SMS[수]) && 같은말(imiterere_agaciro, 함수형[수])) {
                if ((uburyo_kwinjira[수] & 8) == 0) kudakora_agaciro("method is not static"); else 호출(수);
                return;
            }
            kudakora_agaciro("NoSuchMethodError"); return;
        }
        if (Ijambo_SMS(nyirayo_agaciro, "java/io/FileInputStream") || Ijambo_SMS(nyirayo_agaciro, "java/io/FileOutputStream")) {
            dosiye_Stream_Hamagara(nyirayo_agaciro, Izina, imiterere_agaciro, Icyo_wifuza); return;
        }
        if (Icyo_wifuza == 184 && Ijambo_SMS(nyirayo_agaciro, "java/lang/Integer") && Ijambo_SMS(Izina, "parseInt") && Ijambo_SMS(imiterere_agaciro, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Icyo_wifuza == 182 && Ijambo_SMS(nyirayo_agaciro, "java/io/PrintStream") && (Ijambo_SMS(Izina, "println") || Ijambo_SMS(Izina, "print"))) {
            int 형 = 0, agaciro = 0;
            if (Ijambo_SMS(imiterere_agaciro, "(I)V")) { 형 = 1; agaciro = 빼기(1); }
            else if (Ijambo_SMS(imiterere_agaciro, "(Z)V")) { 형 = 2; agaciro = 빼기(1); }
            else if (Ijambo_SMS(imiterere_agaciro, "(C)V")) { 형 = 3; agaciro = 빼기(1); }
            else if (Ijambo_SMS(imiterere_agaciro, "(Ljava/lang/String;)V")) { 형 = 4; agaciro = 빼기(2); }
            else if (!Ijambo_SMS(imiterere_agaciro, "()V") || !Ijambo_SMS(Izina, "println")) kudakora_agaciro("unsupported print descriptor");
            if (빼기(2) != -1) kudakora_agaciro("invalid PrintStream receiver");
            if (IKOSA) return;
            if (형 == 1) 자바도구.수쓰기(agaciro);
            if (형 == 2) ukoresha.kwandika(agaciro == 0 ? "false" : "true");
            if (형 == 3) ukoresha.kwandika_inyuguti_agaciro(agaciro & 65535);
            if (형 == 4) kwandika_SMS(agaciro);
            if (Ijambo_SMS(Izina, "println")) ukoresha.kwandika_inyuguti_agaciro(10);
            return;
        }
        if (Icyo_wifuza == 182 && Ijambo_SMS(nyirayo_agaciro, "java/lang/String")) {
            if (Ijambo_SMS(Izina, "length") && Ijambo_SMS(imiterere_agaciro, "()I")) {
                int Indanga = 빼기(2); if (ikintu_agaciro_2ed200e9(Indanga, 1)) 넣기(힙[Indanga + 1], 1); return;
            }
            if (Ijambo_SMS(Izina, "charAt") && Ijambo_SMS(imiterere_agaciro, "(I)C")) {
                int injyesi_agaciro = 빼기(1), Indanga = 빼기(2);
                if (ikintu_agaciro_2ed200e9(Indanga, 1)) {
                    if (injyesi_agaciro < 0 || injyesi_agaciro >= 힙[Indanga + 1]) kudakora_agaciro("StringIndexOutOfBoundsException"); else 넣기(힙[Indanga + 2 + injyesi_agaciro], 1);
                }
                return;
            }
        }
        if (Ijambo_SMS(nyirayo_agaciro, "java/lang/StringBuilder")) {
            if (Icyo_wifuza == 183 && Ijambo_SMS(Izina, "<init>") && Ijambo_SMS(imiterere_agaciro, "()V")) { ikintu_agaciro_2ed200e9(빼기(2), 4); return; }
            if (Icyo_wifuza == 182 && Ijambo_SMS(Izina, "toString") && Ijambo_SMS(imiterere_agaciro, "()Ljava/lang/String;")) {
                int Indanga = 빼기(2); if (ikintu_agaciro_2ed200e9(Indanga, 4)) 넣기(힙[Indanga + 2] == 0 ? gucumbikira_inyuguti("") : 힙[Indanga + 2], 2); return;
            }
            if (Icyo_wifuza == 182 && Ijambo_SMS(Izina, "append")) {
                int Umwandiko = 0;
                if (Ijambo_SMS(imiterere_agaciro, "(I)Ljava/lang/StringBuilder;")) Umwandiko = umubare_inyuguti(빼기(1));
                else if (Ijambo_SMS(imiterere_agaciro, "(Z)Ljava/lang/StringBuilder;")) Umwandiko = gucumbikira_inyuguti(빼기(1) == 0 ? "false" : "true");
                else if (Ijambo_SMS(imiterere_agaciro, "(C)Ljava/lang/StringBuilder;")) {
                    int agaciro = 빼기(1); Umwandiko = kugenera_Ububiko(1, 1); if (!IKOSA) 힙[Umwandiko + 2] = agaciro & 65535;
                }
                else if (Ijambo_SMS(imiterere_agaciro, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Umwandiko = 빼기(2); if (Umwandiko == 0) Umwandiko = gucumbikira_inyuguti("null"); }
                else { kudakora_agaciro("unsupported StringBuilder append"); return; }
                int Indanga = 빼기(2); if (!ikintu_agaciro_2ed200e9(Indanga, 4) || !ikintu_agaciro_2ed200e9(Umwandiko, 1)) return;
                int 앞 = 힙[Indanga + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], Ikibanza_agaciro_uburebure = 힙[Umwandiko + 1];
                int 새글 = kugenera_Ububiko(1, 앞길이 + Ikibanza_agaciro_uburebure); if (IKOSA) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < Ikibanza_agaciro_uburebure; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[Umwandiko + 2 + 수];
                힙[Indanga + 2] = 새글; 넣기(Indanga, 2); return;
            }
        }
        kudakora_agaciro("unsupported library method");
    }
    static int ARRAY_umwanya(int Indanga, int injyesi_agaciro, int 형) {
        if (!ikintu_agaciro_2ed200e9(Indanga, 형)) return 0;
        if (injyesi_agaciro < 0 || injyesi_agaciro >= 힙[Indanga + 1]) { kudakora_agaciro("ArrayIndexOutOfBoundsException"); return 0; }
        return Indanga + 2 + injyesi_agaciro;
    }
    static void gukora_ibwiriza() {
        int 남음 = 500000;
        while (ikadiri_umugerekashakiro >= 0 && !IKOSA) {
            if (--남음 == 0) { kudakora_agaciro("instruction limit (500000)"); break; }
            int ihuriro = 틀위치[ikadiri_umugerekashakiro], agaciro = 명바();
            if (IKOSA) break;
            if (agaciro == 0) continue;
            if (agaciro == 1) { 넣기(0, 2); continue; }
            if (agaciro >= 2 && agaciro <= 8) { 넣기(agaciro - 3, 1); continue; }
            if (agaciro == 16) { 넣기((byte)명바(), 1); continue; }
            if (agaciro == 17) { 넣기((short)명짧(), 1); continue; }
            if (agaciro == 18 || agaciro == 19) {
                int 수 = agaciro == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= 상수수) kudakora_agaciro("invalid ldc constant");
                else if (kidahinduka_Akarango[수] == 3) 넣기(상가[수], 1);
                else if (kidahinduka_Akarango[수] == 8) 넣기(kidahinduka_SMS(상가[수]), 2);
                else kudakora_agaciro("unsupported ldc constant");
                continue;
            }
            if (agaciro == 21 || agaciro == 25) { 지역읽기(명바(), agaciro == 21 ? 1 : 2); continue; }
            if (agaciro >= 26 && agaciro <= 29) { 지역읽기(agaciro - 26, 1); continue; }
            if (agaciro >= 42 && agaciro <= 45) { 지역읽기(agaciro - 42, 2); continue; }
            if (agaciro == 54 || agaciro == 58) { kwandika_mu_gace(명바(), agaciro == 54 ? 1 : 2); continue; }
            if (agaciro >= 59 && agaciro <= 62) { kwandika_mu_gace(agaciro - 59, 1); continue; }
            if (agaciro >= 75 && agaciro <= 78) { kwandika_mu_gace(agaciro - 75, 2); continue; }
            if (agaciro == 46 || agaciro == 50) {
                int injyesi_agaciro = 빼기(1), Indanga = 빼기(2), umwanya_icyinjizwa = ARRAY_umwanya(Indanga, injyesi_agaciro, agaciro == 46 ? 2 : 3);
                if (!IKOSA) 넣기(힙[umwanya_icyinjizwa], agaciro == 46 ? 1 : 2); continue;
            }
            if (agaciro == 79 || agaciro == 83) {
                int igice_ikintu = 빼기(agaciro == 79 ? 1 : 2), injyesi_agaciro = 빼기(1), Indanga = 빼기(2), umwanya_icyinjizwa = ARRAY_umwanya(Indanga, injyesi_agaciro, agaciro == 79 ? 2 : 3);
                if (agaciro == 83 && igice_ikintu != 0) ikintu_agaciro_2ed200e9(igice_ikintu, 1);
                if (!IKOSA) 힙[umwanya_icyinjizwa] = igice_ikintu; continue;
            }
            if (agaciro == 87) { 빼기(0); continue; }
            if (agaciro == 89) { int 가 = 빼기(0), 형 = 반환형; 넣기(가, 형); 넣기(가, 형); continue; }
            if (agaciro == 95) { int 가 = 빼기(0), 가형 = 반환형, 나 = 빼기(0), 나형 = 반환형; 넣기(가, 가형); 넣기(나, 나형); continue; }
            if (agaciro == 96 || agaciro == 100 || agaciro == 104 || agaciro == 108 || agaciro == 112 || agaciro == 120
                || agaciro == 122 || agaciro == 124 || agaciro == 126 || agaciro == 128 || agaciro == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), 결과 = 0;
                if ((agaciro == 108 || agaciro == 112) && 나 == 0) { kudakora_agaciro("ArithmeticException: / by zero"); continue; }
                if (agaciro == 96) 결과 = 가 + 나;
                if (agaciro == 100) 결과 = 가 - 나;
                if (agaciro == 104) 결과 = 가 * 나;
                if (agaciro == 108) 결과 = 가 / 나;
                if (agaciro == 112) 결과 = 가 % 나;
                if (agaciro == 120) 결과 = 가 << 나;
                if (agaciro == 122) 결과 = 가 >> 나;
                if (agaciro == 124) 결과 = 가 >>> 나;
                if (agaciro == 126) 결과 = 가 & 나;
                if (agaciro == 128) 결과 = 가 | 나;
                if (agaciro == 130) 결과 = 가 ^ 나;
                넣기(결과, 1); continue;
            }
            if (agaciro == 116) { 넣기(-빼기(1), 1); continue; }
            if (agaciro == 132) {
                int mu_gace_urwego = 명바(), 증분 = (byte)명바(); 지역읽기(mu_gace_urwego, 1); 넣기(빼기(1) + 증분, 1); kwandika_mu_gace(mu_gace_urwego, 1); continue;
            }
            if (agaciro >= 145 && agaciro <= 147) {
                int 수 = 빼기(1); 넣기(agaciro == 145 ? (byte)수 : agaciro == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (agaciro >= 153 && agaciro <= 167 || agaciro == 198 || agaciro == 199) {
                int aho_ijya_agaciro = ihuriro + (short)명짧(); boolean 갈까 = agaciro == 167;
                if (agaciro >= 153 && agaciro <= 158) {
                    int 수 = 빼기(1); 갈까 = agaciro == 153 ? 수 == 0 : agaciro == 154 ? 수 != 0 : agaciro == 155 ? 수 < 0 : agaciro == 156 ? 수 >= 0 : agaciro == 157 ? 수 > 0 : 수 <= 0;
                } else if (agaciro >= 159 && agaciro <= 166) {
                    int 나 = 빼기(agaciro >= 165 ? 2 : 1), 가 = 빼기(agaciro >= 165 ? 2 : 1);
                    갈까 = agaciro == 159 || agaciro == 165 ? 가 == 나 : agaciro == 160 || agaciro == 166 ? 가 != 나 : agaciro == 161 ? 가 < 나 : agaciro == 162 ? 가 >= 나 : agaciro == 163 ? 가 > 나 : 가 <= 나;
                } else if (agaciro == 198 || agaciro == 199) { int 수 = 빼기(2); 갈까 = agaciro == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) kwimura_agaciro(aho_ijya_agaciro); continue;
            }
            if (agaciro == 172 || agaciro == 176 || agaciro == 177) { 반환(agaciro == 172 ? 1 : agaciro == 176 ? 2 : 0); continue; }
            if (agaciro == 178) {
                int 수 = 명짧(); if (!sheki_kidahinduka(수, 9)) continue;
                if (!Ijambo_SMS(icyiciro_izina_SMS(상가[수]), "java/lang/System") || !Ijambo_SMS(Indanga_izina(상나[수]), "out")
                    || !Ijambo_SMS(참조형식(상나[수]), "Ljava/io/PrintStream;")) kudakora_agaciro("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (agaciro == 182 || agaciro == 183 || agaciro == 184) { Hamagara_uburyo(명짧(), agaciro); continue; }
            if (agaciro == 187) {
                int Izina = icyiciro_izina_SMS(명짧());
                if (Ijambo_SMS(Izina, "java/lang/StringBuilder")) 넣기(kugenera_Ububiko(4, 1), 2);
                else if (Ijambo_SMS(Izina, "java/io/FileInputStream") || Ijambo_SMS(Izina, "java/io/FileOutputStream")) {
                    int Indanga = kugenera_Ububiko(Ijambo_SMS(Izina, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!IKOSA) { 힙[Indanga + 2] = -1; 넣기(Indanga, 2); }
                } else kudakora_agaciro("unsupported object construction");
                continue;
            }
            if (agaciro == 188 || agaciro == 189) {
                if (agaciro == 188) { if (명바() != 10) kudakora_agaciro("only int[] newarray is supported"); }
                else if (!Ijambo_SMS(icyiciro_izina_SMS(명짧()), "java/lang/String")) kudakora_agaciro("only String[] anewarray is supported");
                int uburebure_agaciro = 빼기(1); 넣기(kugenera_Ububiko(agaciro == 188 ? 2 : 3, uburebure_agaciro), 2); continue;
            }
            if (agaciro == 190) {
                int Indanga = 빼기(2);
                if (Indanga < 1 || Indanga >= 힙끝 - 1 || (힙[Indanga] != 2 && 힙[Indanga] != 3)) kudakora_agaciro("null or invalid array");
                else 넣기(힙[Indanga + 1], 1); continue;
            }
            if (agaciro == 192) {
                int Izina = icyiciro_izina_SMS(명짧()), Indanga = 빼기(2);
                if (!Ijambo_SMS(Izina, "java/lang/String")) kudakora_agaciro("unsupported checkcast");
                else if (Indanga != 0) ikintu_agaciro_2ed200e9(Indanga, 1);
                넣기(Indanga, 2); continue;
            }
            kudakora_agaciro("unsupported bytecode");
        }
    }
    public static int ihuriro() {
        if (ukoresha.인수개수() == 1 && 자바도구.같음(ukoresha.인수(0), "-version")) {
            ukoresha.kwandika("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (ukoresha.인수개수() < 1) { ukoresha.kwandika("Usage: java CLASS [ARGS]\n"); return 2; }
        int uburebure_agaciro = 자바도구.Izina(dosiye_izina_SMS, ukoresha.인수(0));
        if (uburebure_agaciro < 1 || uburebure_agaciro > 57) { ukoresha.kwandika("java: invalid class name\n"); return 2; }
        dosiye_izina_SMS[uburebure_agaciro] = '.'; dosiye_izina_SMS[uburebure_agaciro + 1] = 'c'; dosiye_izina_SMS[uburebure_agaciro + 2] = 'l'; dosiye_izina_SMS[uburebure_agaciro + 3] = 'a'; dosiye_izina_SMS[uburebure_agaciro + 4] = 's'; dosiye_izina_SMS[uburebure_agaciro + 5] = 's';
        Ingano = ukoresha.파일읽기(dosiye_izina_SMS, Idosiye);
        if (Ingano < 0) { ukoresha.kwandika("java: cannot read class: "); 자바도구.수쓰기(Ingano); ukoresha.kwandika_inyuguti_agaciro(10); return 1; }
        클래스읽기(); if (IKOSA) return 1;
        int inyuguti_izina = kidahinduka_SMS(icyiciro_izina);
        if (!IKOSA && 힙[inyuguti_izina + 1] != uburebure_agaciro) kudakora_agaciro("class name does not match file");
        for (int 수 = 0; 수 < uburebure_agaciro && !IKOSA; 수++) if (힙[inyuguti_izina + 2 + 수] != dosiye_izina_SMS[수]) kudakora_agaciro("class name does not match file");
        int icyinjizwa_inota_agaciro = -1;
        for (int 수 = 0; 수 < 함수수; 수++) if (Ijambo_SMS(uburyo_izina_SMS[수], "main") && Ijambo_SMS(함수형[수], "([Ljava/lang/String;)V") && (uburyo_kwinjira[수] & 9) == 9) icyinjizwa_inota_agaciro = 수;
        if (icyinjizwa_inota_agaciro < 0) kudakora_agaciro("public static void main(String[] args) required");
        if (IKOSA) return 1;
        int 인수 = kugenera_Ububiko(3, ukoresha.인수개수() - 1);
        for (int 수 = 1; 수 < ukoresha.인수개수() && !IKOSA; 수++) 힙[인수 + 1 + 수] = gucumbikira_inyuguti(ukoresha.인수(수));
        ikadiri_umugerekashakiro = 0; ikadiri_uburyo[0] = icyinjizwa_inota_agaciro; 틀위치[0] = uburyo_Itangira[icyinjizwa_inota_agaciro]; mu_gace_agaciro[0] = 인수; 지역형[0] = 2;
        gukora_ibwiriza(); return IKOSA ? 1 : 0;
    }
}
