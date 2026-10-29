// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Idosiye/스택/Indanga/ishami 경계를 gukora_ibwiriza 중 검사한다. */
public final class 자바가상기계 {
    static int[] Idosiye = new int[16 * 16384], 임시파일 = new int[16384], dosiye_izina_SMS = new int[512];
    static int[] kidahinduka_Akarango = new int[8192], 상가 = new int[8192], 상나 = new int[8192], igicenteruro_Indanga = new int[8192];
    static int[] uburyo_izina_SMS = new int[512], 함수형 = new int[512], uburyo_kwinjira = new int[512], uburyo_nyirayo = new int[512];
    static int[] uburyo_Itangira = new int[512], uburyo_kurangiza = new int[512], uburyo_Ikirundo = new int[512], 함수지역 = new int[512];
    static int[] 함수인수수 = new int[512], 함수인수형 = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] mu_gace_agaciro = new int[16384], 지역형 = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] ikadiri_uburyo = new int[128], 틀위치 = new int[128], ikadiri_Ikirundo = new int[128], ikadiri_ibwiriza = new int[128], gutangiza_ikadiri = new int[128];
    static int[] icyiciro_Igisobanuro_izina = new int[16], icyiciro_Igisobanuro_ingano = new int[16], 종부모 = new int[16], icyiciro_Igisobanuro_imimerere = new int[16], 종칸수 = new int[16], gutangiza_icyiciro_Igisobanuro = new int[16];
    static int[] icyiciro_irebero = new int[16 * 16], 종접면수 = new int[16];
    static int[] umwanya_izina = new int[512], 칸형 = new int[512], umwanya_nyirayo = new int[512], umwanya_impushya = new int[512], 칸위치 = new int[512], umwanya_amakurushingiro = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], ARRAY_ikintu = new int[32768], Store_umubare_wuzuye = new int[256];
    static int Ingano, 읽기위치, 함수수, icyiciro_izina, ikadiri_umugerekashakiro = -1, 힙끝 = 1, 반환형;
    static int 종수, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, 표시수, 수거횟수;
    static int 현재가닥, 가닥수 = 1, icyinjizwa_icyiciro_Igisobanuro;
    static int[] mugenaporogaramu_ikadiri = new int[4], mugenaporogaramu_imimerere = new int[4], mugenaporogaramu_ikintu = new int[4], mugenaporogaramu_gusimbuza_igishya = new int[4], 가닥대기 = new int[4];
    static boolean IKOSA, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], icyiciro_mugenaporogaramu = new int[16];

    static void kudakora_agaciro(String Ijambo_SMS) {
        if (IKOSA) return;
        int 분류코드 = 0;
        if (자바도구.같음(Ijambo_SMS, "ArithmeticException: / by zero")) 분류코드 = 4;
        if (자바도구.같음(Ijambo_SMS, "NullPointerException") || 자바도구.같음(Ijambo_SMS, "null or invalid array")) 분류코드 = 5;
        if (자바도구.같음(Ijambo_SMS, "ArrayIndexOutOfBoundsException")) 분류코드 = 7;
        if (자바도구.같음(Ijambo_SMS, "StringIndexOutOfBoundsException")) 분류코드 = 8;
        if (자바도구.같음(Ijambo_SMS, "NumberFormatException")) 분류코드 = 10;
        if (자바도구.같음(Ijambo_SMS, "FileNotFoundException: file open failed")) 분류코드 = 12;
        if (자바도구.같음(Ijambo_SMS, "IOException: stream closed") || 자바도구.같음(Ijambo_SMS, "IOException: read failed") || 자바도구.같음(Ijambo_SMS, "IOException: write failed")) 분류코드 = 11;
        if (자바도구.같음(Ijambo_SMS, "ClassCastException")) 분류코드 = 14;
        if (자바도구.같음(Ijambo_SMS, "NegativeArraySizeException")) 분류코드 = 15;
        if (분류코드 != 0 && ikadiri_umugerekashakiro >= 0) { 예외던짐(분류코드, Ijambo_SMS); return; }
        ukoresha.kwandika("JVM error: "); ukoresha.kwandika(Ijambo_SMS); ukoresha.kwandika_inyuguti_agaciro(10); IKOSA = true;
    }
    static boolean kiripu(int ihuriro, int uburebure_agaciro) {
        if (ihuriro < 0 || ihuriro >= Idosiye.length || uburebure_agaciro < 0) return false;
        int icyiciro_Igisobanuro = ihuriro / 16384;
        return ihuriro % 16384 <= icyiciro_Igisobanuro_ingano[icyiciro_Igisobanuro] && uburebure_agaciro <= icyiciro_Igisobanuro_ingano[icyiciro_Igisobanuro] - ihuriro % 16384;
    }
    static int bayiti_agaciro() {
        if (!kiripu(읽기위치, 1)) { kudakora_agaciro("truncated class file"); return 0; }
        return Idosiye[읽기위치++];
    }
    static int 짧은수() { return bayiti_agaciro() << 8 | bayiti_agaciro(); }
    static int umubare_wuzuye() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int uburebure_agaciro) { if (!kiripu(읽기위치, uburebure_agaciro)) kudakora_agaciro("invalid attribute size"); else 읽기위치 += uburebure_agaciro; }
    static boolean sheki_kidahinduka(int 수, int 종류) {
        if (수 <= 0 || 수 >= kidahinduka_Akarango.length || kidahinduka_Akarango[수] != 종류) { kudakora_agaciro("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int ihuriro, int uburebure_agaciro, String Ijambo_SMS) {
        if (!kiripu(ihuriro, uburebure_agaciro)) return false;
        int 읽는자리 = ihuriro, 끝 = ihuriro + uburebure_agaciro;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < Ijambo_SMS.length(); gukora_mu_matsinda_umugerekashakiro++) {
            int 문자값 = Ijambo_SMS.charAt(gukora_mu_matsinda_umugerekashakiro);
            if (문자값 > 0 && 문자값 < 128) { if (읽는자리 >= 끝 || Idosiye[읽는자리++] != 문자값) return false; }
            else if (문자값 < 2048) {
                if (읽는자리 + 2 > 끝 || Idosiye[읽는자리++] != (192 | (문자값 >> 6)) || Idosiye[읽는자리++] != (128 | (문자값 & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Idosiye[읽는자리++] != (224 | (문자값 >> 12)) || Idosiye[읽는자리++] != (128 | ((문자값 >> 6) & 63)) || Idosiye[읽는자리++] != (128 | (문자값 & 63))) return false;
        }
        return 읽는자리 == 끝;
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
    static int 상번호() { int agaciro = 짧은수(); return agaciro == 0 ? 0 : 현재읽는종 * 512 + agaciro; }
    static int 명상수() { return uburyo_nyirayo[ikadiri_uburyo[ikadiri_umugerekashakiro]] * 512 + 명짧(); }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !IKOSA; 수++) { sheki_kidahinduka(상번호(), 1); 건너(umubare_wuzuye()); }
    }
    static int ibwiriza_uburebure(int agaciro) {
        if (agaciro == 16 || agaciro == 18 || agaciro == 21 || agaciro == 25 || agaciro == 54 || agaciro == 58 || agaciro == 188) return 2;
        if (agaciro == 17 || agaciro == 19 || agaciro == 132 || agaciro >= 153 && agaciro <= 167
            || agaciro >= 178 && agaciro <= 184 || agaciro == 187 || agaciro == 189 || agaciro == 192 || agaciro == 193 || agaciro == 198 || agaciro == 199) return 3;
        if (agaciro == 185 || agaciro == 200) return 5;
        if (agaciro >= 0 && agaciro <= 8 || agaciro >= 26 && agaciro <= 29 || agaciro >= 42 && agaciro <= 46 || agaciro >= 50 && agaciro <= 53
            || agaciro >= 59 && agaciro <= 62 || agaciro >= 75 && agaciro <= 79 || agaciro >= 83 && agaciro <= 95
            || agaciro == 96 || agaciro == 100 || agaciro == 104 || agaciro == 108 || agaciro == 112 || agaciro == 116
            || agaciro == 120 || agaciro == 122 || agaciro == 124 || agaciro == 126 || agaciro == 128 || agaciro == 130
            || agaciro >= 145 && agaciro <= 147 || agaciro == 172 || agaciro == 176 || agaciro == 177 || agaciro == 190 || agaciro == 191
            || agaciro == 194 || agaciro == 195) return 1;
        return 0;
    }
    static int 위치정수(int 읽는자리) {
        if (!kiripu(읽는자리, 4)) { kudakora_agaciro("truncated bytecode operand"); return 0; }
        return Idosiye[읽는자리] << 24 | Idosiye[읽는자리 + 1] << 16 | Idosiye[읽는자리 + 2] << 8 | Idosiye[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int ihuriro, int 끝) {
        int agaciro = Idosiye[읽는자리], uburebure_agaciro = ibwiriza_uburebure(agaciro);
        if (agaciro == 170 || agaciro == 171) {
            int 기준자리 = 읽는자리 + 1;
            while ((기준자리 - ihuriro) % 4 != 0) 기준자리++;
            if (끝 - 기준자리 < (agaciro == 170 ? 12 : 8)) return 0;
            int 항목수 = agaciro == 170 ? 위치정수(기준자리 + 8) - 위치정수(기준자리 + 4) + 1 : 위치정수(기준자리 + 4);
            if (항목수 < 0 || 항목수 > 2048) return 0;
            uburebure_agaciro = 기준자리 - 읽는자리 + (agaciro == 170 ? 12 + 4 * 항목수 : 8 + 8 * 항목수);
        }
        if (agaciro == 196 && 읽는자리 + 1 < 끝) {
            int Ijambo_amakurushingiro = Idosiye[읽는자리 + 1]; uburebure_agaciro = Ijambo_amakurushingiro == 132 ? 6 : (Ijambo_amakurushingiro == 21 || Ijambo_amakurushingiro == 25 || Ijambo_amakurushingiro == 54 || Ijambo_amakurushingiro == 58) ? 4 : 0;
        }
        return uburebure_agaciro > 0 && uburebure_agaciro <= 끝 - 읽는자리 ? uburebure_agaciro : 0;
    }
    static void sheki_aho_ijya_agaciro(int aho_ijya_agaciro, int FUNCTION_agaciro) {
        if (aho_ijya_agaciro < uburyo_Itangira[FUNCTION_agaciro] || aho_ijya_agaciro >= uburyo_kurangiza[FUNCTION_agaciro] || 경계[aho_ijya_agaciro] != FUNCTION_agaciro + 1) kudakora_agaciro("invalid branch target");
    }
    static void 클래스읽기(int icyiciro_Igisobanuro) {
        현재읽는종 = icyiciro_Igisobanuro; 읽기위치 = icyiciro_Igisobanuro * 16384; Ingano = 읽기위치 + icyiciro_Igisobanuro_ingano[icyiciro_Igisobanuro];
        if (umubare_wuzuye() != 0xcafebabe) { kudakora_agaciro("not a class file"); return; }
        int 부판 = 짧은수(), verisiyo_agaciro = 짧은수();
        if (verisiyo_agaciro < 45 || verisiyo_agaciro > 52 || 부판 != 0) { kudakora_agaciro("supported class versions: 45..52, minor 0"); return; }
        int 상수수 = 짧은수(), 기준자리 = icyiciro_Igisobanuro * 512;
        if (상수수 < 1 || 상수수 > 512) { kudakora_agaciro("constant pool limit (511)"); return; }
        for (int 항목수 = 1; 항목수 < 상수수 && !IKOSA; 항목수++) {
            int 수 = 기준자리 + 항목수, 종류 = bayiti_agaciro(); kidahinduka_Akarango[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = umubare_wuzuye();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); 상나[수] = 상번호(); }
            else kudakora_agaciro("unsupported constant type");
        }
        int 권한 = 짧은수();
        if ((권한 & (0x2000 | 0x4000)) != 0) kudakora_agaciro("annotation/enum class unsupported");
        icyiciro_Igisobanuro_izina[icyiciro_Igisobanuro] = icyiciro_izina_SMS(상번호());
        종부모[icyiciro_Igisobanuro] = icyiciro_izina_SMS(상번호());
        int 접면수 = 짧은수(); if (접면수 > 16) { kudakora_agaciro("interface count limit"); return; }
        종접면수[icyiciro_Igisobanuro] = 접면수;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 접면수; gukora_mu_matsinda_umugerekashakiro++) icyiciro_irebero[icyiciro_Igisobanuro * 16 + gukora_mu_matsinda_umugerekashakiro] = icyiciro_izina_SMS(상번호());
        int 필드수 = 짧은수();
        if (필드수 > 512 - 칸수) { kudakora_agaciro("field count limit (512)"); return; }
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 필드수 && !IKOSA; gukora_mu_matsinda_umugerekashakiro++) {
            int dosiye_umugerekashakiro = 칸수++; umwanya_nyirayo[dosiye_umugerekashakiro] = icyiciro_Igisobanuro; umwanya_impushya[dosiye_umugerekashakiro] = 짧은수(); umwanya_izina[dosiye_umugerekashakiro] = 상번호(); 칸형[dosiye_umugerekashakiro] = 상번호();
            sheki_kidahinduka(umwanya_izina[dosiye_umugerekashakiro], 1); sheki_kidahinduka(칸형[dosiye_umugerekashakiro], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[칸형[dosiye_umugerekashakiro]]; int 분류코드 = 서술형(읽기위치 + 상나[칸형[dosiye_umugerekashakiro]], false); 읽기위치 = 보존값;
            if ((umwanya_impushya[dosiye_umugerekashakiro] & 8) == 0) 칸위치[dosiye_umugerekashakiro] = 종칸수[icyiciro_Igisobanuro]++;
            int ikiranga_amakurushingiro = 짧은수();
            for (int 안쪽자리 = 0; 안쪽자리 < ikiranga_amakurushingiro && !IKOSA; 안쪽자리++) {
                int izina_kidahinduka = 상번호(), 유효길이 = umubare_wuzuye();
                if (Ijambo_SMS(izina_kidahinduka, "ConstantValue") && 유효길이 == 2) {
                    int amakurushingiro_agaciro = 상번호();
                    if (분류코드 == 1 && sheki_kidahinduka(amakurushingiro_agaciro, 3)) umwanya_amakurushingiro[dosiye_umugerekashakiro] = 상가[amakurushingiro_agaciro];
                    else if (분류코드 == 2 && sheki_kidahinduka(amakurushingiro_agaciro, 8)) umwanya_amakurushingiro[dosiye_umugerekashakiro] = kidahinduka_SMS(상가[amakurushingiro_agaciro]);
                } else 건너(유효길이);
            }
        }
        int 개수 = 짧은수();
        if (개수 > 512 - 함수수) { kudakora_agaciro("method count limit (512)"); return; }
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 개수 && !IKOSA; gukora_mu_matsinda_umugerekashakiro++) {
            int 수 = 함수수++; uburyo_nyirayo[수] = icyiciro_Igisobanuro;
            uburyo_kwinjira[수] = 짧은수(); uburyo_izina_SMS[수] = 상번호(); 함수형[수] = 상번호();
            sheki_kidahinduka(uburyo_izina_SMS[수], 1); 서술읽기(수);
            if ((uburyo_kwinjira[수] & 8) == 0) {
                if (함수인수수[수] == 16) { kudakora_agaciro("too many instance method arguments"); return; }
                for (int 비교자리 = 함수인수수[수]; 비교자리 > 0; 비교자리--) 함수인수형[수 * 16 + 비교자리] = 함수인수형[수 * 16 + 비교자리 - 1];
                함수인수형[수 * 16] = 2; 함수인수수[수]++;
            }
            if ((uburyo_kwinjira[수] & 0x100) != 0) kudakora_agaciro("user native method unsupported");
            if (Ijambo_SMS(uburyo_izina_SMS[수], "<clinit>")) gutangiza_icyiciro_Igisobanuro[icyiciro_Igisobanuro] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (uburyo_nyirayo[앞] == icyiciro_Igisobanuro && 같은말(uburyo_izina_SMS[앞], uburyo_izina_SMS[수]) && 같은말(함수형[앞], 함수형[수])) kudakora_agaciro("duplicate method");
            int 속성수 = 짧은수();
            for (int ikiranga_agaciro = 0; ikiranga_agaciro < 속성수 && !IKOSA; ikiranga_agaciro++) {
                int Izina = 상번호(), uburebure_agaciro = umubare_wuzuye(), ihuriro = 읽기위치;
                if (!kiripu(ihuriro, uburebure_agaciro)) { kudakora_agaciro("truncated method attribute"); break; }
                if (Ijambo_SMS(Izina, "Code")) {
                    if (uburyo_Itangira[수] != 0) kudakora_agaciro("duplicate Code attribute");
                    uburyo_Ikirundo[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = umubare_wuzuye();
                    if (uburyo_Ikirundo[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) kudakora_agaciro("method memory limits exceeded");
                    uburyo_Itangira[수] = 읽기위치; 건너(코드길이); uburyo_kurangiza[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { kudakora_agaciro("exception table limit"); return; }
                    for (int 안쪽자리 = 0; 안쪽자리 < 잡는수; 안쪽자리++) {
                        int ikosa_Indanga = 잡기수++; 잡기함수[ikosa_Indanga] = 수;
                        잡기시작[ikosa_Indanga] = uburyo_Itangira[수] + 짧은수(); 잡기끝[ikosa_Indanga] = uburyo_Itangira[수] + 짧은수();
                        잡기위치[ikosa_Indanga] = uburyo_Itangira[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[ikosa_Indanga] = 부호값 == 0 ? 0 : icyiciro_izina_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != ihuriro + uburebure_agaciro) kudakora_agaciro("Code attribute size mismatch");
                } else 건너(uburebure_agaciro);
            }
            if ((uburyo_kwinjira[수] & 0x400) != 0) continue;
            if (uburyo_Itangira[수] == 0) kudakora_agaciro("missing Code attribute");
            int umwanya_icyinjizwa = uburyo_Itangira[수];
            while (umwanya_icyinjizwa < uburyo_kurangiza[수] && !IKOSA) {
                int uburebure_agaciro = 길이읽기(umwanya_icyinjizwa, uburyo_Itangira[수], uburyo_kurangiza[수]);
                if (uburebure_agaciro == 0) { kudakora_agaciro("unsupported or truncated bytecode"); break; }
                경계[umwanya_icyinjizwa] = 수 + 1; umwanya_icyinjizwa += uburebure_agaciro;
            }
            umwanya_icyinjizwa = uburyo_Itangira[수];
            while (umwanya_icyinjizwa < uburyo_kurangiza[수] && !IKOSA) {
                int agaciro = Idosiye[umwanya_icyinjizwa];
                if (agaciro >= 153 && agaciro <= 167 || agaciro == 198 || agaciro == 199) sheki_aho_ijya_agaciro(umwanya_icyinjizwa + (short)(Idosiye[umwanya_icyinjizwa + 1] << 8 | Idosiye[umwanya_icyinjizwa + 2]), 수);
                if (agaciro == 200) sheki_aho_ijya_agaciro(umwanya_icyinjizwa + 위치정수(umwanya_icyinjizwa + 1), 수);
                if (agaciro == 170 || agaciro == 171) {
                    int 읽는자리 = umwanya_icyinjizwa + 1; while ((읽는자리 - uburyo_Itangira[수]) % 4 != 0) 읽는자리++;
                    sheki_aho_ijya_agaciro(umwanya_icyinjizwa + 위치정수(읽는자리), 수);
                    int 항목수 = agaciro == 170 ? 위치정수(읽는자리 + 8) - 위치정수(읽는자리 + 4) + 1 : 위치정수(읽는자리 + 4);
                    읽는자리 += agaciro == 170 ? 12 : 8;
                    for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) sheki_aho_ijya_agaciro(umwanya_icyinjizwa + 위치정수(읽는자리 + 안쪽자리 * (agaciro == 170 ? 4 : 8) + (agaciro == 170 ? 0 : 4)), 수);
                }
                umwanya_icyinjizwa += 길이읽기(umwanya_icyinjizwa, uburyo_Itangira[수], uburyo_kurangiza[수]);
            }
            for (int 안쪽자리 = 0; 안쪽자리 < 잡기수; 안쪽자리++) if (잡기함수[안쪽자리] == 수) {
                sheki_aho_ijya_agaciro(잡기시작[안쪽자리], 수); sheki_aho_ijya_agaciro(잡기위치[안쪽자리], 수);
                if (잡기끝[안쪽자리] != uburyo_kurangiza[수]) sheki_aho_ijya_agaciro(잡기끝[안쪽자리], 수);
                if (잡기시작[안쪽자리] >= 잡기끝[안쪽자리]) kudakora_agaciro("invalid exception range");
            }
        }
        if (!IKOSA) 속성건너();
        if (읽기위치 != Ingano) kudakora_agaciro("extra class file data");
    }
    static int kugenera_Ububiko(int 종류, int uburebure_agaciro) { return 새기억(종류, uburebure_agaciro); }
    static boolean ikintu_agaciro_2ed200e9(int Indanga, int 종류) {
        if (!객체유효(Indanga)) return false;
        if (힙[Indanga] != 종류) { kudakora_agaciro("object type mismatch"); return false; }
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
        if (반환형 == 2) kurinda_agaciro(스택값[umwanya_icyinjizwa]);
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
        if (ikadiri_umugerekashakiro % 32 == 31) { kudakora_agaciro("call stack limit (32)"); return; }
        int 다음 = ikadiri_umugerekashakiro + 1;
        for (int 수 = 0; 수 < 128; 수++) 지역형[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[FUNCTION_agaciro] - 1; 수 >= 0; 수--) {
            mu_gace_agaciro[다음 * 128 + 수] = 빼기(함수인수형[FUNCTION_agaciro * 16 + 수]); 지역형[다음 * 128 + 수] = 함수인수형[FUNCTION_agaciro * 16 + 수];
        }
        if (IKOSA) return;
        ikadiri_umugerekashakiro = 다음; gutangiza_ikadiri[ikadiri_umugerekashakiro] = 0; ikadiri_uburyo[ikadiri_umugerekashakiro] = FUNCTION_agaciro; 틀위치[ikadiri_umugerekashakiro] = uburyo_Itangira[FUNCTION_agaciro]; ikadiri_Ikirundo[ikadiri_umugerekashakiro] = 0;
    }
    static void 반환(int 형) {
        if (형 != 함수반환[ikadiri_uburyo[ikadiri_umugerekashakiro]]) { kudakora_agaciro("return type mismatch"); return; }
        int agaciro = 형 == 0 ? 0 : 빼기(형);
        if (gutangiza_ikadiri[ikadiri_umugerekashakiro] != 0) icyiciro_Igisobanuro_imimerere[gutangiza_ikadiri[ikadiri_umugerekashakiro] - 1] = 2;
        if (틀잠금[ikadiri_umugerekashakiro] != 0) { 잠금풀기(틀잠금[ikadiri_umugerekashakiro]); 틀잠금[ikadiri_umugerekashakiro] = 0; }
        ikadiri_umugerekashakiro--; if (ikadiri_umugerekashakiro >= 현재가닥 * 32 && 형 != 0) 넣기(agaciro, 형);
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
                if (agaciro < 1) { kudakora_agaciro("invalid file stream path"); return; }
                Stream_dosiye_izina[umwanya_icyinjizwa] = agaciro;
            }
            Stream_dosiye_izina[uburebure_agaciro] = 0;
            int 서술자 = ukoresha.파일서술자열기(Stream_dosiye_izina, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { kudakora_agaciro("FileNotFoundException: file open failed"); return; }
            힙[Stream_agaciro + 2] = 서술자; 힙[Stream_agaciro + 3] = 1;
            return;
        }
        if (Icyo_wifuza != 182) { kudakora_agaciro("invalid file stream invocation"); return; }
        if ((출력 && Ijambo_SMS(Izina, "write") || !출력 && Ijambo_SMS(Izina, "read"))
            && (Ijambo_SMS(imiterere_agaciro, 출력 ? "([B)V" : "([B)I") || Ijambo_SMS(imiterere_agaciro, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean kiripu_agaciro = Ijambo_SMS(imiterere_agaciro, 출력 ? "([BII)V" : "([BII)I");
            int 항목수 = kiripu_agaciro ? 빼기(1) : 0, 시작점 = kiripu_agaciro ? 빼기(1) : 0, amakurushingiro_ARRAY = 빼기(2), ikintu_Indanga = 빼기(2);
            if (!ikintu_agaciro_2ed200e9(amakurushingiro_ARRAY, 20) || !ikintu_agaciro_2ed200e9(ikintu_Indanga, 종류)) return;
            if (!kiripu_agaciro) 항목수 = 힙[amakurushingiro_ARRAY + 1];
            if (시작점 < 0 || 항목수 < 0 || 시작점 > 힙[amakurushingiro_ARRAY + 1] - 항목수) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[ikintu_Indanga + 3] == 0 || 힙[ikintu_Indanga + 2] < 0) { kudakora_agaciro("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < 항목수 && !IKOSA) {
                int 반환값 = 출력 ? ukoresha.파일한바이트쓰기(힙[ikintu_Indanga + 2], 힙[amakurushingiro_ARRAY + 2 + 시작점 + 완료수]) : ukoresha.파일한바이트읽기(힙[ikintu_Indanga + 2]);
                if (반환값 < 0) { kudakora_agaciro(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[amakurushingiro_ARRAY + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(항목수 != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Ijambo_SMS(Izina, "flush") && Ijambo_SMS(imiterere_agaciro, "()V")) { int ikintu_Indanga = 빼기(2); if (ikintu_agaciro_2ed200e9(ikintu_Indanga, 종류) && 힙[ikintu_Indanga + 2] < 0) kudakora_agaciro("IOException: stream closed"); return; }
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
            if (결과 < -1) kudakora_agaciro("IOException: read failed"); else 넣기(결과 == 256 ? -1 : 결과, 1);
        } else if (ukoresha.파일한바이트쓰기(서술자, agaciro) != 1) kudakora_agaciro("IOException: write failed");
    }
    static void Hamagara_uburyo(int umugerekashakiro, int Icyo_wifuza) {
        if (umugerekashakiro <= 0 || umugerekashakiro >= kidahinduka_Akarango.length || (kidahinduka_Akarango[umugerekashakiro] != 10 && kidahinduka_Akarango[umugerekashakiro] != 11)) { kudakora_agaciro("invalid method reference"); return; }
        int nyirayo_agaciro = icyiciro_izina_SMS(상가[umugerekashakiro]), Izina = Indanga_izina(상나[umugerekashakiro]), imiterere_agaciro = 참조형식(상나[umugerekashakiro]);
        if (IKOSA) return;
        if (기본호출(nyirayo_agaciro, Izina, imiterere_agaciro, Icyo_wifuza)) return;
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
        int icyiciro_Igisobanuro = gushaka_icyiciro_Igisobanuro(nyirayo_agaciro); if (icyiciro_Igisobanuro < 0 || IKOSA) return;
        int dosiye_umugerekashakiro = gushaka_uburyo(icyiciro_Igisobanuro, Izina, imiterere_agaciro);
        if (dosiye_umugerekashakiro < 0) {
            for (int 문자값 = icyiciro_Igisobanuro, 항목수 = 0; 문자값 >= 0 && 항목수 < 16; 항목수++, 문자값 = 부모종(문자값))
                if (Ijambo_SMS(종부모[문자값], "java/lang/Thread")) { 가닥호출(Izina, imiterere_agaciro, Icyo_wifuza); return; }
            kudakora_agaciro("NoSuchMethodError"); return;
        }
        if (((uburyo_kwinjira[dosiye_umugerekashakiro] & 8) != 0) != (Icyo_wifuza == 184)) { kudakora_agaciro("method static/instance mismatch"); return; }
        if (Icyo_wifuza == 184) { if (!gutangiza(uburyo_nyirayo[dosiye_umugerekashakiro], ikadiri_ibwiriza[ikadiri_umugerekashakiro])) return; }
        else {
            int 읽는자리 = ikadiri_Ikirundo[ikadiri_umugerekashakiro] - 함수인수수[dosiye_umugerekashakiro];
            if (읽는자리 < 0 || 스택형[ikadiri_umugerekashakiro * 128 + 읽는자리] != 2) { kudakora_agaciro("invalid method receiver"); return; }
            int ikintu_Indanga = 스택값[ikadiri_umugerekashakiro * 128 + 읽는자리];
            if (!객체유효(ikintu_Indanga)) return;
            if (힙[ikintu_Indanga] < 32 || !종포함(힙[ikintu_Indanga] - 32, nyirayo_agaciro)) { kudakora_agaciro("method receiver type mismatch"); return; }
            if (Icyo_wifuza != 183) dosiye_umugerekashakiro = gushaka_uburyo(힙[ikintu_Indanga] - 32, Izina, imiterere_agaciro);
        }
        if (dosiye_umugerekashakiro < 0 || (uburyo_kwinjira[dosiye_umugerekashakiro] & 0x400) != 0) { kudakora_agaciro("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((uburyo_kwinjira[dosiye_umugerekashakiro] & 32) != 0) {
            if (Icyo_wifuza == 184) { int 문자값 = uburyo_nyirayo[dosiye_umugerekashakiro]; if (종잠금[문자값] == 0) 종잠금[문자값] = kugenera_Ububiko(8, 0); 잠금참조 = 종잠금[문자값]; }
            else 잠금참조 = 스택값[ikadiri_umugerekashakiro * 128 + ikadiri_Ikirundo[ikadiri_umugerekashakiro] - 함수인수수[dosiye_umugerekashakiro]];
            if (!잠금얻기(잠금참조)) { if (!IKOSA) 틀위치[ikadiri_umugerekashakiro] = ikadiri_ibwiriza[ikadiri_umugerekashakiro]; return; }
        }
        호출(dosiye_umugerekashakiro); if (!IKOSA) 틀잠금[ikadiri_umugerekashakiro] = 잠금참조;
    }
    static boolean 배열저장가능(int ARRAY_Indanga, int amakurushingiro_agaciro) {
        if (amakurushingiro_agaciro == 0 || ARRAY_ikintu[ARRAY_Indanga] == 0) return true;
        boolean 성공여부 = ARRAY_ikintu[ARRAY_Indanga] == -1 ? (amakurushingiro_agaciro > 0 && amakurushingiro_agaciro < 힙끝 && 힙[amakurushingiro_agaciro] == 1) : 맞는객체(amakurushingiro_agaciro, ARRAY_ikintu[ARRAY_Indanga]);
        if (!성공여부 && !IKOSA) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int ARRAY_umwanya(int Indanga, int injyesi_agaciro, int 형) {
        if (!ikintu_agaciro_2ed200e9(Indanga, 형)) return 0;
        if (injyesi_agaciro < 0 || injyesi_agaciro >= 힙[Indanga + 1]) { kudakora_agaciro("ArrayIndexOutOfBoundsException"); return 0; }
        return Indanga + 2 + injyesi_agaciro;
    }
    static void gukora_ibwiriza() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (IKOSA) { if (던진객체 != 0) 예외처리(); if (IKOSA || ikadiri_umugerekashakiro < 현재가닥 * 32) break; }
            if (ikadiri_umugerekashakiro < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!guhinduranya_mugenaporogaramu()) break; 조각 = 100; }
            if (ikadiri_umugerekashakiro == 0 && icyiciro_Igisobanuro_imimerere[icyinjizwa_icyiciro_Igisobanuro] != 2 && !gutangiza(icyinjizwa_icyiciro_Igisobanuro, 틀위치[ikadiri_umugerekashakiro])) continue;
            if (ikadiri_umugerekashakiro == 현재가닥 * 32 && 현재가닥 != 0 && (uburyo_kwinjira[ikadiri_uburyo[ikadiri_umugerekashakiro]] & 32) != 0 && 틀잠금[ikadiri_umugerekashakiro] == 0) {
                int ikintu_Indanga = mugenaporogaramu_gusimbuza_igishya[현재가닥]; if (!잠금얻기(ikintu_Indanga)) { if (IKOSA) break; continue; } 틀잠금[ikadiri_umugerekashakiro] = ikintu_Indanga;
            }
            잠시수 = 0;
            if (--남음 == 0) { kudakora_agaciro("instruction limit (500000)"); break; }
            int ihuriro = 틀위치[ikadiri_umugerekashakiro]; ikadiri_ibwiriza[ikadiri_umugerekashakiro] = ihuriro; int agaciro = 명바();
            if (IKOSA) break;
            if (agaciro == 0) continue;
            if (agaciro == 1) { 넣기(0, 2); continue; }
            if (agaciro >= 2 && agaciro <= 8) { 넣기(agaciro - 3, 1); continue; }
            if (agaciro == 16) { 넣기((byte)명바(), 1); continue; }
            if (agaciro == 17) { 넣기((short)명짧(), 1); continue; }
            if (agaciro == 18 || agaciro == 19) {
                int 수 = uburyo_nyirayo[ikadiri_uburyo[ikadiri_umugerekashakiro]] * 512 + (agaciro == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= kidahinduka_Akarango.length) kudakora_agaciro("invalid ldc constant");
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
            if (agaciro == 46 || agaciro >= 50 && agaciro <= 53) {
                int 항목자리 = 빼기(1), ikintu_Indanga = 빼기(2), 분류코드 = agaciro == 46 ? 2 : agaciro == 50 ? 3 : agaciro == 51 ? 20 : agaciro == 52 ? 22 : 23;
                if (agaciro == 51 && ikintu_Indanga > 0 && ikintu_Indanga < 힙끝 && 힙[ikintu_Indanga] == 21) 분류코드 = 21;
                int 읽는자리 = ARRAY_umwanya(ikintu_Indanga, 항목자리, 분류코드); if (!IKOSA) 넣기(힙[읽는자리], agaciro == 50 ? 2 : 1); continue;
            }
            if (agaciro == 79 || agaciro >= 83 && agaciro <= 86) {
                int icyinjizwa_Indanga = 빼기(agaciro == 83 ? 2 : 1), 항목자리 = 빼기(1), ikintu_Indanga = 빼기(2), 분류코드 = agaciro == 79 ? 2 : agaciro == 83 ? 3 : agaciro == 84 ? 20 : agaciro == 85 ? 22 : 23;
                if (agaciro == 84 && ikintu_Indanga > 0 && ikintu_Indanga < 힙끝 && 힙[ikintu_Indanga] == 21) 분류코드 = 21;
                int 읽는자리 = ARRAY_umwanya(ikintu_Indanga, 항목자리, 분류코드);
                if (!IKOSA && 분류코드 == 3 && !배열저장가능(ikintu_Indanga, icyinjizwa_Indanga)) continue;
                if (!IKOSA) 힙[읽는자리] = 분류코드 == 20 ? (byte)icyinjizwa_Indanga : 분류코드 == 21 ? icyinjizwa_Indanga & 1 : 분류코드 == 22 ? (char)icyinjizwa_Indanga : 분류코드 == 23 ? (short)icyinjizwa_Indanga : icyinjizwa_Indanga;
                continue;
            }
            if (agaciro >= 87 && agaciro <= 95) { Ikirundo_ibwiriza(agaciro); continue; }
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
            if (agaciro >= 178 && agaciro <= 181) { 필드호출(명상수(), agaciro, ihuriro); continue; }
            if (agaciro >= 182 && agaciro <= 185) {
                int 부호값 = 명상수();
                if (agaciro == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { kudakora_agaciro("invalid invokeinterface operands"); continue; } }
                Hamagara_uburyo(부호값, agaciro); continue;
            }
            if (agaciro == 187) { 새객체(icyiciro_izina_SMS(명상수()), ihuriro); continue; }
            if (agaciro == 188 || agaciro == 189) {
                int 분류코드 = 3, ikigize = 0;
                if (agaciro == 188) { int 임시값 = 명바(); 분류코드 = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else ikigize = icyiciro_izina_SMS(명상수());
                if (분류코드 == 0) { kudakora_agaciro("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), ikintu_Indanga = kugenera_Ububiko(분류코드, 유효길이); if (!IKOSA) ARRAY_ikintu[ikintu_Indanga] = ikigize; 넣기(ikintu_Indanga, 2); continue;
            }
            if (agaciro == 190) {
                int ikintu_Indanga = 빼기(2);
                if (객체유효(ikintu_Indanga)) { int 비교자리 = 힙[ikintu_Indanga]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) kudakora_agaciro("not an array"); else 넣기(힙[ikintu_Indanga + 1], 1); }
                continue;
            }
            if (agaciro == 191) {
                int ikintu_Indanga = 빼기(2); if (객체유효(ikintu_Indanga)) { if (힙[ikintu_Indanga] != 9) kudakora_agaciro("athrow requires supported Throwable"); else { 던진객체 = ikintu_Indanga; IKOSA = true; } }
                continue;
            }
            if (agaciro == 192 || agaciro == 193) {
                int izina_kidahinduka = icyiciro_izina_SMS(명상수()), ikintu_Indanga = 빼기(2); boolean 일치여부 = 맞는객체(ikintu_Indanga, izina_kidahinduka);
                if (agaciro == 193) 넣기(ikintu_Indanga != 0 && 일치여부 ? 1 : 0, 1);
                else { if (!일치여부 && !IKOSA) kudakora_agaciro("ClassCastException"); 넣기(ikintu_Indanga, 2); }
                continue;
            }
            if (agaciro == 170 || agaciro == 171) {
                int 읽는자리 = ihuriro + 1, dosiye_umugerekashakiro = ikadiri_uburyo[ikadiri_umugerekashakiro], buto_Indanga = 빼기(1);
                while ((읽는자리 - uburyo_Itangira[dosiye_umugerekashakiro]) % 4 != 0) 읽는자리++;
                int gusimbuza_igishya_aderesi = 위치정수(읽는자리);
                if (agaciro == 170) { int 낮은값 = 위치정수(읽는자리 + 4), 높은값 = 위치정수(읽는자리 + 8); if (buto_Indanga >= 낮은값 && buto_Indanga <= 높은값) gusimbuza_igishya_aderesi = 위치정수(읽는자리 + 12 + (buto_Indanga - 낮은값) * 4); }
                else { int 총수 = 위치정수(읽는자리 + 4); for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 총수; gukora_mu_matsinda_umugerekashakiro++) if (위치정수(읽는자리 + 8 + gukora_mu_matsinda_umugerekashakiro * 8) == buto_Indanga) gusimbuza_igishya_aderesi = 위치정수(읽는자리 + 12 + gukora_mu_matsinda_umugerekashakiro * 8); }
                kwimura_agaciro(ihuriro + gusimbuza_igishya_aderesi); continue;
            }
            if (agaciro == 200) { kwimura_agaciro(ihuriro + 위치정수(ihuriro + 1)); continue; }
            if (agaciro == 194 || agaciro == 195) {
                int ikintu_Indanga = 빼기(2);
                if (agaciro == 195) 잠금풀기(ikintu_Indanga);
                else if (!잠금얻기(ikintu_Indanga) && !IKOSA) { 넣기(ikintu_Indanga, 2); 틀위치[ikadiri_umugerekashakiro] = ihuriro; }
                continue;
            }
            if (agaciro == 196) {
                int 명령코드 = 명바(), 항목자리 = 명짧();
                if (명령코드 == 21 || 명령코드 == 25) 지역읽기(항목자리, 명령코드 == 21 ? 1 : 2);
                else if (명령코드 == 54 || 명령코드 == 58) kwandika_mu_gace(항목자리, 명령코드 == 54 ? 1 : 2);
                else if (명령코드 == 132) { int 변화량 = (short)명짧(); 지역읽기(항목자리, 1); 넣기(빼기(1) + 변화량, 1); kwandika_mu_gace(항목자리, 1); }
                else kudakora_agaciro("unsupported wide opcode");
                continue;
            }
            kudakora_agaciro("unsupported bytecode");
        }
    }
    static int gushaka_icyiciro_Igisobanuro(int Izina) {
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 종수; gukora_mu_matsinda_umugerekashakiro++) if (icyiciro_Igisobanuro_izina[gukora_mu_matsinda_umugerekashakiro] != 0 && 같은말(icyiciro_Igisobanuro_izina[gukora_mu_matsinda_umugerekashakiro], Izina)) return gukora_mu_matsinda_umugerekashakiro;
        return gufunguka_icyiciro_Igisobanuro(kidahinduka_SMS(Izina));
    }
    static int gufunguka_icyiciro_Igisobanuro(int izina_igicenteruro) {
        if (!ikintu_agaciro_2ed200e9(izina_igicenteruro, 1)) return -1;
        int uburebure_agaciro = 힙[izina_igicenteruro + 1];
        if (uburebure_agaciro < 1 || uburebure_agaciro > 505 || 종수 == 16) { kudakora_agaciro("class name/count limit"); return -1; }
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < uburebure_agaciro; gukora_mu_matsinda_umugerekashakiro++) { int 문자값 = 힙[izina_igicenteruro + 2 + gukora_mu_matsinda_umugerekashakiro]; dosiye_izina_SMS[gukora_mu_matsinda_umugerekashakiro] = 문자값 == '/' ? '.' : 문자값; }
        dosiye_izina_SMS[uburebure_agaciro] = '.'; dosiye_izina_SMS[uburebure_agaciro + 1] = 'c'; dosiye_izina_SMS[uburebure_agaciro + 2] = 'l'; dosiye_izina_SMS[uburebure_agaciro + 3] = 'a'; dosiye_izina_SMS[uburebure_agaciro + 4] = 's'; dosiye_izina_SMS[uburebure_agaciro + 5] = 's'; dosiye_izina_SMS[uburebure_agaciro + 6] = 0;
        int Ingano = ukoresha.파일읽기(dosiye_izina_SMS, 임시파일);
        if (Ingano < 0) { kudakora_agaciro("ClassNotFoundException"); return -1; }
        int icyiciro_Igisobanuro = 종수++; icyiciro_Igisobanuro_ingano[icyiciro_Igisobanuro] = Ingano;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < Ingano; gukora_mu_matsinda_umugerekashakiro++) Idosiye[icyiciro_Igisobanuro * 16384 + gukora_mu_matsinda_umugerekashakiro] = 임시파일[gukora_mu_matsinda_umugerekashakiro];
        클래스읽기(icyiciro_Igisobanuro); if (IKOSA) return -1;
        int nyakuri_amakurushingiro = kidahinduka_SMS(icyiciro_Igisobanuro_izina[icyiciro_Igisobanuro]);
        if (!글같음(nyakuri_amakurushingiro, izina_igicenteruro, true)) { kudakora_agaciro("class name does not match file"); return -1; }
        int 부모 = 종부모[icyiciro_Igisobanuro];
        if (부모 != 0 && !Ijambo_SMS(부모, "java/lang/Object") && !Ijambo_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = gushaka_icyiciro_Igisobanuro(부모);
            if (IKOSA || 위 < 0) return -1;
            int 읽는자리 = 위, 단계수 = 0;
            while (읽는자리 >= 0 && 단계수++ < 16) {
                if (읽는자리 == icyiciro_Igisobanuro) { kudakora_agaciro("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int dosiye_umugerekashakiro = 0; dosiye_umugerekashakiro < 칸수; dosiye_umugerekashakiro++) if (umwanya_nyirayo[dosiye_umugerekashakiro] == icyiciro_Igisobanuro && (umwanya_impushya[dosiye_umugerekashakiro] & 8) == 0) 칸위치[dosiye_umugerekashakiro] += 시작변위;
            종칸수[icyiciro_Igisobanuro] += 시작변위;
        }
        return icyiciro_Igisobanuro;
    }
    static int 부모종(int icyiciro_Igisobanuro) {
        int Izina = 종부모[icyiciro_Igisobanuro];
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 종수; gukora_mu_matsinda_umugerekashakiro++) if (Izina != 0 && icyiciro_Igisobanuro_izina[gukora_mu_matsinda_umugerekashakiro] != 0 && 같은말(icyiciro_Igisobanuro_izina[gukora_mu_matsinda_umugerekashakiro], Izina)) return gukora_mu_matsinda_umugerekashakiro;
        return -1;
    }
    static int gushaka_uburyo(int icyiciro_Igisobanuro, int Izina, int imiterere_agaciro) {
        for (int 깊이 = 0; icyiciro_Igisobanuro >= 0 && 깊이 < 16; 깊이++, icyiciro_Igisobanuro = 부모종(icyiciro_Igisobanuro)) {
            for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 함수수; gukora_mu_matsinda_umugerekashakiro++) if (uburyo_nyirayo[gukora_mu_matsinda_umugerekashakiro] == icyiciro_Igisobanuro && 같은말(uburyo_izina_SMS[gukora_mu_matsinda_umugerekashakiro], Izina) && 같은말(함수형[gukora_mu_matsinda_umugerekashakiro], imiterere_agaciro)) return gukora_mu_matsinda_umugerekashakiro;
        }
        return -1;
    }
    static int izina_uburyo(int icyiciro_Igisobanuro, String Izina, String imiterere_agaciro) {
        for (int 깊이 = 0; icyiciro_Igisobanuro >= 0 && 깊이 < 16; 깊이++, icyiciro_Igisobanuro = 부모종(icyiciro_Igisobanuro))
            for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 함수수; gukora_mu_matsinda_umugerekashakiro++) if (uburyo_nyirayo[gukora_mu_matsinda_umugerekashakiro] == icyiciro_Igisobanuro && Ijambo_SMS(uburyo_izina_SMS[gukora_mu_matsinda_umugerekashakiro], Izina) && Ijambo_SMS(함수형[gukora_mu_matsinda_umugerekashakiro], imiterere_agaciro)) return gukora_mu_matsinda_umugerekashakiro;
        return -1;
    }
    static int 형종류(int Izina) { return Idosiye[상가[Izina]] == 'L' || Idosiye[상가[Izina]] == '[' ? 2 : 1; }
    static boolean gutangiza(int icyiciro_Igisobanuro, int ibwiriza_Itangira) {
        if (icyiciro_Igisobanuro < 0 || IKOSA) return false;
        if (icyiciro_Igisobanuro_imimerere[icyiciro_Igisobanuro] == 3) { kudakora_agaciro("NoClassDefFoundError: initialization failed"); return false; }
        if (icyiciro_Igisobanuro_imimerere[icyiciro_Igisobanuro] == 1 && icyiciro_mugenaporogaramu[icyiciro_Igisobanuro] != 현재가닥) { 틀위치[ikadiri_umugerekashakiro] = ibwiriza_Itangira; 바꿈요청 = true; return false; }
        if (icyiciro_Igisobanuro_imimerere[icyiciro_Igisobanuro] != 0) return true;
        int 위 = 부모종(icyiciro_Igisobanuro);
        if (위 >= 0 && !gutangiza(위, ibwiriza_Itangira)) return false;
        icyiciro_Igisobanuro_imimerere[icyiciro_Igisobanuro] = 1; icyiciro_mugenaporogaramu[icyiciro_Igisobanuro] = 현재가닥;
        if (gutangiza_icyiciro_Igisobanuro[icyiciro_Igisobanuro] != 0) {
            틀위치[ikadiri_umugerekashakiro] = ibwiriza_Itangira;
            호출(gutangiza_icyiciro_Igisobanuro[icyiciro_Igisobanuro] - 1); if (!IKOSA) gutangiza_ikadiri[ikadiri_umugerekashakiro] = icyiciro_Igisobanuro + 1;
            return false;
        }
        icyiciro_Igisobanuro_imimerere[icyiciro_Igisobanuro] = 2; return true;
    }
    static void 필드호출(int umugerekashakiro, int Icyo_wifuza, int ihuriro) {
        if (!sheki_kidahinduka(umugerekashakiro, 9)) return;
        int nyirayo_agaciro = icyiciro_izina_SMS(상가[umugerekashakiro]), Izina = Indanga_izina(상나[umugerekashakiro]), imiterere_agaciro = 참조형식(상나[umugerekashakiro]);
        if (Ijambo_SMS(nyirayo_agaciro, "java/lang/System") && (Ijambo_SMS(Izina, "out") || Ijambo_SMS(Izina, "err")) && Ijambo_SMS(imiterere_agaciro, "Ljava/io/PrintStream;") && Icyo_wifuza == 178) { 넣기(-1, 2); return; }
        int icyiciro_Igisobanuro = gushaka_icyiciro_Igisobanuro(nyirayo_agaciro); if (icyiciro_Igisobanuro < 0 || IKOSA) return;
        int 찾음 = -1;
        for (int 읽는자리 = icyiciro_Igisobanuro, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int dosiye_umugerekashakiro = 0; dosiye_umugerekashakiro < 칸수; dosiye_umugerekashakiro++) if (umwanya_nyirayo[dosiye_umugerekashakiro] == 읽는자리 && 같은말(umwanya_izina[dosiye_umugerekashakiro], Izina) && 같은말(칸형[dosiye_umugerekashakiro], imiterere_agaciro)) 찾음 = dosiye_umugerekashakiro;
        if (찾음 < 0) { kudakora_agaciro("NoSuchFieldError"); return; }
        boolean kitayega_agaciro = Icyo_wifuza == 178 || Icyo_wifuza == 179;
        if (kitayega_agaciro != ((umwanya_impushya[찾음] & 8) != 0)) { kudakora_agaciro("field static/instance mismatch"); return; }
        if (kitayega_agaciro && !gutangiza(umwanya_nyirayo[찾음], ihuriro)) return;
        int 형 = 형종류(imiterere_agaciro), agaciro = 0;
        if (Icyo_wifuza == 179 || Icyo_wifuza == 181) agaciro = 빼기(형);
        if (kitayega_agaciro) { if (Icyo_wifuza == 178) 넣기(umwanya_amakurushingiro[찾음], 형); else if (!IKOSA) umwanya_amakurushingiro[찾음] = agaciro; return; }
        int ikintu_Indanga = 빼기(2);
        if (!객체유효(ikintu_Indanga)) return;
        if (힙[ikintu_Indanga] < 32 || !종포함(힙[ikintu_Indanga] - 32, nyirayo_agaciro)) { kudakora_agaciro("field receiver type mismatch"); return; }
        int 보관칸 = ikintu_Indanga + 2 + 칸위치[찾음];
        if (Icyo_wifuza == 180) 넣기(힙[보관칸], 형);
        else if (!IKOSA) { 힙[보관칸] = agaciro; 힙참조[보관칸] = 형 == 2 ? 1 : 0; }
    }
    static boolean 종포함(int icyiciro_Igisobanuro, int Izina) {
        for (int 중첩깊이 = 0; icyiciro_Igisobanuro >= 0 && 중첩깊이 < 16; 중첩깊이++, icyiciro_Igisobanuro = 부모종(icyiciro_Igisobanuro)) {
            if (같은말(icyiciro_Igisobanuro_izina[icyiciro_Igisobanuro], Izina) || (종부모[icyiciro_Igisobanuro] != 0 && 같은말(종부모[icyiciro_Igisobanuro], Izina))) return true;
            for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[icyiciro_Igisobanuro]; 안쪽자리++) if (같은말(icyiciro_irebero[icyiciro_Igisobanuro * 16 + 안쪽자리], Izina)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int bayiti_amakurushingiro, boolean Inzira) {
        if (첫값 == bayiti_amakurushingiro) return true;
        if (첫값 <= 0 || bayiti_amakurushingiro <= 0 || 힙[첫값] != 1 || 힙[bayiti_amakurushingiro] != 1 || 힙[첫값 + 1] != 힙[bayiti_amakurushingiro + 1]) return false;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 힙[첫값 + 1]; gukora_mu_matsinda_umugerekashakiro++) {
            int Ihuza_rya_x = 힙[첫값 + 2 + gukora_mu_matsinda_umugerekashakiro], 세로좌표 = 힙[bayiti_amakurushingiro + 2 + gukora_mu_matsinda_umugerekashakiro];
            if (Inzira) { if (Ihuza_rya_x == '.') Ihuza_rya_x = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (Ihuza_rya_x != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int ikintu_Indanga) {
        if (ikintu_Indanga == 0) { kudakora_agaciro("NullPointerException"); return false; }
        if (ikintu_Indanga < 1 || ikintu_Indanga >= 힙끝 || 힙폭[ikintu_Indanga] < 2 || 힙[ikintu_Indanga] == 0) { kudakora_agaciro("invalid object reference"); return false; }
        return true;
    }
    static void kurinda_agaciro(int ikintu_Indanga) {
        if (ikintu_Indanga > 0 && ikintu_Indanga < 힙끝 && 힙폭[ikintu_Indanga] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = ikintu_Indanga;
    }
    static void kugaragaza_agaciro(int ikintu_Indanga) {
        if (ikintu_Indanga > 0 && ikintu_Indanga < 힙끝 && 힙폭[ikintu_Indanga] >= 2 && 힙[ikintu_Indanga] != 0 && 힙표시[ikintu_Indanga] == 0) {
            힙표시[ikintu_Indanga] = 1; 표시대기[표시수++] = ikintu_Indanga;
        }
    }
    static void 수거() {
        표시수 = 0; 수거횟수++;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) 힙표시[검사자리] = 0;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < igicenteruro_Indanga.length; gukora_mu_matsinda_umugerekashakiro++) kugaragaza_agaciro(igicenteruro_Indanga[gukora_mu_matsinda_umugerekashakiro]);
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 칸수; gukora_mu_matsinda_umugerekashakiro++) if ((umwanya_impushya[gukora_mu_matsinda_umugerekashakiro] & 8) != 0 && 형종류(칸형[gukora_mu_matsinda_umugerekashakiro]) == 2) kugaragaza_agaciro(umwanya_amakurushingiro[gukora_mu_matsinda_umugerekashakiro]);
        for (int 임시값 = 0; 임시값 < 가닥수; 임시값++) {
            kugaragaza_agaciro(mugenaporogaramu_ikintu[임시값]); kugaragaza_agaciro(mugenaporogaramu_gusimbuza_igishya[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? ikadiri_umugerekashakiro : mugenaporogaramu_ikadiri[임시값];
            for (int dosiye_umugerekashakiro = 임시값 * 32; dosiye_umugerekashakiro <= 꼭대기자리; dosiye_umugerekashakiro++) {
                for (int 안쪽자리 = 0; 안쪽자리 < 함수지역[ikadiri_uburyo[dosiye_umugerekashakiro]]; 안쪽자리++) if (지역형[dosiye_umugerekashakiro * 128 + 안쪽자리] == 2) kugaragaza_agaciro(mu_gace_agaciro[dosiye_umugerekashakiro * 128 + 안쪽자리]);
                for (int 안쪽자리 = 0; 안쪽자리 < ikadiri_Ikirundo[dosiye_umugerekashakiro]; 안쪽자리++) if (스택형[dosiye_umugerekashakiro * 128 + 안쪽자리] == 2) kugaragaza_agaciro(스택값[dosiye_umugerekashakiro * 128 + 안쪽자리]);
            }
        }
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 화면참조.length; gukora_mu_matsinda_umugerekashakiro++) kugaragaza_agaciro(화면참조[gukora_mu_matsinda_umugerekashakiro]);
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 나중수; gukora_mu_matsinda_umugerekashakiro++) kugaragaza_agaciro(나중실행[gukora_mu_matsinda_umugerekashakiro]);
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < Store_umubare_wuzuye.length; gukora_mu_matsinda_umugerekashakiro++) kugaragaza_agaciro(Store_umubare_wuzuye[gukora_mu_matsinda_umugerekashakiro]);
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 종수; gukora_mu_matsinda_umugerekashakiro++) kugaragaza_agaciro(종잠금[gukora_mu_matsinda_umugerekashakiro]);
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (잠금깊이[검사자리] > 0) kugaragaza_agaciro(검사자리);
        kugaragaza_agaciro(던진객체);
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 잠시수; gukora_mu_matsinda_umugerekashakiro++) kugaragaza_agaciro(잠시참조[gukora_mu_matsinda_umugerekashakiro]);
        while (표시수 > 0) {
            int ikintu_Indanga = 표시대기[--표시수], 분류코드 = 힙[ikintu_Indanga];
            for (int gukora_mu_matsinda_umugerekashakiro = ikintu_Indanga + 2; gukora_mu_matsinda_umugerekashakiro < ikintu_Indanga + 힙폭[ikintu_Indanga]; gukora_mu_matsinda_umugerekashakiro++) if (분류코드 == 3 || 분류코드 == 4 || 힙참조[gukora_mu_matsinda_umugerekashakiro] != 0) kugaragaza_agaciro(힙[gukora_mu_matsinda_umugerekashakiro]);
        }
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙표시[검사자리] == 0) 힙[검사자리] = 0;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙[검사자리] == 0) {
            while (검사자리 + 힙폭[검사자리] < 힙끝 && 힙[검사자리 + 힙폭[검사자리]] == 0) { int 다음자리 = 검사자리 + 힙폭[검사자리]; 힙폭[검사자리] += 힙폭[다음자리]; 힙폭[다음자리] = 0; }
            if (검사자리 + 힙폭[검사자리] == 힙끝) { 힙끝 = 검사자리; break; }
        }
    }
    static int 새기억(int 종류, int uburebure_agaciro) {
        if (uburebure_agaciro < 0) { kudakora_agaciro("NegativeArraySizeException"); return 0; }
        if (uburebure_agaciro > 힙.length - 3) { kudakora_agaciro("object heap exhausted"); return 0; }
        int 필요수 = uburebure_agaciro + 2, ikintu_Indanga = 0;
        if (필요수 <= 힙.length - 힙끝) { ikintu_Indanga = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { ikintu_Indanga = 읽는자리; break; }
            if (ikintu_Indanga != 0) {
                int 남은길이 = 힙폭[ikintu_Indanga] - 필요수;
                if (남은길이 >= 2) { 힙폭[ikintu_Indanga + 필요수] = 남은길이; 힙[ikintu_Indanga + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { ikintu_Indanga = 힙끝; 힙끝 += 필요수; }
        }
        if (ikintu_Indanga == 0) { kudakora_agaciro("object heap exhausted"); return 0; }
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 필요수; gukora_mu_matsinda_umugerekashakiro++) { 힙[ikintu_Indanga + gukora_mu_matsinda_umugerekashakiro] = 0; 힙참조[ikintu_Indanga + gukora_mu_matsinda_umugerekashakiro] = 0; 힙폭[ikintu_Indanga + gukora_mu_matsinda_umugerekashakiro] = 0; }
        ARRAY_ikintu[ikintu_Indanga] = 0;
        힙폭[ikintu_Indanga] = 필요수; 힙[ikintu_Indanga] = 종류; 힙[ikintu_Indanga + 1] = uburebure_agaciro; kurinda_agaciro(ikintu_Indanga); return ikintu_Indanga;
    }
    static int 예외종(String izina_kidahinduka) {
        if (자바도구.같음(izina_kidahinduka, "java/lang/Throwable")) return 1;
        if (자바도구.같음(izina_kidahinduka, "java/lang/Exception")) return 2;
        if (자바도구.같음(izina_kidahinduka, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(izina_kidahinduka, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(izina_kidahinduka, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(izina_kidahinduka, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(izina_kidahinduka, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(izina_kidahinduka, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(izina_kidahinduka, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(izina_kidahinduka, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(izina_kidahinduka, "java/io/IOException")) return 11;
        if (자바도구.같음(izina_kidahinduka, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(izina_kidahinduka, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(izina_kidahinduka, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(izina_kidahinduka, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int 예외상수(int Izina) {
        for (int gukora_mu_matsinda_umugerekashakiro = 1; gukora_mu_matsinda_umugerekashakiro <= 41; gukora_mu_matsinda_umugerekashakiro++) if (Ijambo_SMS(Izina, 예외이름(gukora_mu_matsinda_umugerekashakiro))) return gukora_mu_matsinda_umugerekashakiro;
        return 0;
    }
    static String 예외이름(int konti_agaciro) {
        if (konti_agaciro == 40) return "java/lang/InterruptedException";
        if (konti_agaciro == 41) return "Ikinyarwanda/자체/대기중단예외";
        if (konti_agaciro == 39) return "java/net/SocketException";
        if (konti_agaciro == 20) return "Ikinyarwanda/자체/예외";
        if (konti_agaciro == 21) return "Ikinyarwanda/자체/실행예외";
        if (konti_agaciro == 22) return "Ikinyarwanda/자체/입출력예외";
        if (konti_agaciro == 23) return "Ikinyarwanda/자체/대기시간초과예외";
        if (konti_agaciro == 24) return "Ikinyarwanda/자체/주소확인예외";
        if (konti_agaciro == 25) return "Ikinyarwanda/자체/파일없음예외";
        if (konti_agaciro == 26) return "Ikinyarwanda/자체/통신예외";
        if (konti_agaciro == 27) return "Ikinyarwanda/자체/잘못된인수예외";
        if (konti_agaciro == 28) return "Ikinyarwanda/자체/숫자형식예외";
        if (konti_agaciro == 29) return "Ikinyarwanda/자체/범위예외";
        if (konti_agaciro == 30) return "Ikinyarwanda/자체/배열범위예외";
        if (konti_agaciro == 31) return "Ikinyarwanda/자체/문자열범위예외";
        if (konti_agaciro == 32) return "Ikinyarwanda/자체/빈참조예외";
        if (konti_agaciro == 33) return "Ikinyarwanda/자체/산술예외";
        if (konti_agaciro == 34) return "Ikinyarwanda/자체/상태예외";
        if (konti_agaciro == 35) return "Ikinyarwanda/자체/형변환예외";
        if (konti_agaciro == 36) return "Ikinyarwanda/자체/음수배열크기예외";
        if (konti_agaciro == 37) return "Ikinyarwanda/자체/ARRAY_Store_kudakora";
        if (konti_agaciro == 38) return "Ikinyarwanda/자체/가닥상태예외";
        if (konti_agaciro == 1) return "java/lang/Throwable"; if (konti_agaciro == 2) return "java/lang/Exception";
        if (konti_agaciro == 3) return "java/lang/RuntimeException"; if (konti_agaciro == 4) return "java/lang/ArithmeticException";
        if (konti_agaciro == 5) return "java/lang/NullPointerException"; if (konti_agaciro == 6) return "java/lang/IndexOutOfBoundsException";
        if (konti_agaciro == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (konti_agaciro == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (konti_agaciro == 9) return "java/lang/IllegalArgumentException"; if (konti_agaciro == 10) return "java/lang/NumberFormatException";
        if (konti_agaciro == 11) return "java/io/IOException"; if (konti_agaciro == 12) return "java/io/FileNotFoundException";
        if (konti_agaciro == 17) return "java/lang/ArrayStoreException";
        if (konti_agaciro == 18) return "java/net/UnknownHostException";
        if (konti_agaciro == 19) return "java/net/SocketTimeoutException";
        if (konti_agaciro == 16) return "java/lang/IllegalThreadStateException";
        if (konti_agaciro == 13) return "java/lang/IllegalStateException"; if (konti_agaciro == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int konti_agaciro) {
        if (konti_agaciro == 40) return 2;
        if (konti_agaciro == 41) return 40;
        if (konti_agaciro == 39) return 11;
        if (konti_agaciro == 1) return 0;
        if (konti_agaciro == 2) return 1;
        if (konti_agaciro == 3) return 2;
        if (konti_agaciro == 4) return 3;
        if (konti_agaciro == 5) return 3;
        if (konti_agaciro == 6) return 3;
        if (konti_agaciro == 7) return 6;
        if (konti_agaciro == 8) return 6;
        if (konti_agaciro == 9) return 3;
        if (konti_agaciro == 10) return 9;
        if (konti_agaciro == 11) return 2;
        if (konti_agaciro == 12) return 11;
        if (konti_agaciro == 13) return 3;
        if (konti_agaciro == 14) return 3;
        if (konti_agaciro == 15) return 3;
        if (konti_agaciro == 16) return 9;
        if (konti_agaciro == 17) return 3;
        if (konti_agaciro == 18) return 11;
        if (konti_agaciro == 19) return 11;
        if (konti_agaciro == 20) return 2;
        if (konti_agaciro == 21) return 3;
        if (konti_agaciro == 22) return 11;
        if (konti_agaciro == 23) return 22;
        if (konti_agaciro == 24) return 22;
        if (konti_agaciro == 25) return 22;
        if (konti_agaciro == 26) return 22;
        if (konti_agaciro == 27) return 9;
        if (konti_agaciro == 28) return 27;
        if (konti_agaciro == 29) return 6;
        if (konti_agaciro == 30) return 29;
        if (konti_agaciro == 31) return 29;
        if (konti_agaciro == 32) return 5;
        if (konti_agaciro == 33) return 4;
        if (konti_agaciro == 34) return 13;
        if (konti_agaciro == 35) return 14;
        if (konti_agaciro == 36) return 15;
        if (konti_agaciro == 37) return 17;
        if (konti_agaciro == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int nyakuri_agaciro, int 요구값) {
        for (int 깊이 = 0; nyakuri_agaciro != 0 && 깊이 < 16; 깊이++, nyakuri_agaciro = 예외부모(nyakuri_agaciro))
            if (nyakuri_agaciro == 요구값) return true;
        return false;
    }
    static void 예외던짐(int konti_agaciro, String NSOMA_Indanga) {
        int ikintu_Indanga = 새기억(9, 2); if (IKOSA) return;
        힙[ikintu_Indanga + 2] = konti_agaciro; 힙[ikintu_Indanga + 3] = gucumbikira_inyuguti(NSOMA_Indanga); 힙참조[ikintu_Indanga + 3] = 1;
        던진객체 = ikintu_Indanga; IKOSA = true;
    }
    static boolean 맞는객체(int ikintu_Indanga, int Izina) {
        if (ikintu_Indanga == 0) return true;
        if (!객체유효(ikintu_Indanga)) return false;
        int 분류코드 = 힙[ikintu_Indanga];
        if (Ijambo_SMS(Izina, "java/lang/Object")) return true;
        if (분류코드 >= 32) return 종포함(분류코드 - 32, Izina);
        if (분류코드 == 9) { int gusimbuza_igishya_aderesi = 예외상수(Izina); return gusimbuza_igishya_aderesi != 0 && 예외포함(힙[ikintu_Indanga + 2], gusimbuza_igishya_aderesi); }
        if (분류코드 == 1) return Ijambo_SMS(Izina, "java/lang/String") || Ijambo_SMS(Izina, "java/lang/CharSequence");
        if (분류코드 == 4) return Ijambo_SMS(Izina, "java/lang/StringBuilder") || Ijambo_SMS(Izina, "java/lang/CharSequence");
        if (분류코드 == 10) return Ijambo_SMS(Izina, "java/util/ArrayList") || Ijambo_SMS(Izina, "java/util/List");
        if (분류코드 == 11) return Ijambo_SMS(Izina, "java/util/HashMap") || Ijambo_SMS(Izina, "java/util/Map");
        if (분류코드 == 12) return Ijambo_SMS(Izina, "java/lang/Integer") || Ijambo_SMS(Izina, "java/lang/Number");
        if (분류코드 >= 24 && 분류코드 <= 28 && 힙[ikintu_Indanga + 13] != 0) return 한국어화면종(Izina) == 분류코드 || Ijambo_SMS(Izina, "Ikinyarwanda/자체/화면구성요소");
        if (분류코드 >= 24 && 분류코드 <= 28) return (한국어화면종(Izina) == 0 && 화면종(Izina) == 분류코드) || Ijambo_SMS(Izina, "java/awt/Component") || Ijambo_SMS(Izina, "java/awt/Container") || Ijambo_SMS(Izina, "javax/swing/JComponent");
        if (분류코드 == 29) return Ijambo_SMS(Izina, 힙[ikintu_Indanga + 3] != 0 ? "Ikinyarwanda/자체/동작알림" : "java/awt/event/ActionEvent");
        if (분류코드 == 30) return Ijambo_SMS(Izina, "java/awt/FlowLayout") || Ijambo_SMS(Izina, "java/awt/LayoutManager");
        if (분류코드 == 17) return Ijambo_SMS(Izina, "java/net/Socket");
        if (분류코드 == 18) return Ijambo_SMS(Izina, "java/net/ServerSocket");
        if (분류코드 == 19) return Ijambo_SMS(Izina, 힙[ikintu_Indanga + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (분류코드 == 14) return Ijambo_SMS(Izina, "java/net/InetAddress");
        if (분류코드 == 15) return Ijambo_SMS(Izina, "java/net/DatagramSocket");
        if (분류코드 == 16) return Ijambo_SMS(Izina, "java/net/DatagramPacket");
        if (분류코드 == 13) return Ijambo_SMS(Izina, 힙[ikintu_Indanga + 3] != 0 ? "Ikinyarwanda/자체/작업가닥" : "java/lang/Thread");
        if (분류코드 == 2) return Ijambo_SMS(Izina, "[I"); if (분류코드 == 20) return Ijambo_SMS(Izina, "[B"); if (분류코드 == 21) return Ijambo_SMS(Izina, "[Z");
        if (분류코드 == 22) return Ijambo_SMS(Izina, "[C"); if (분류코드 == 23) return Ijambo_SMS(Izina, "[S");
        if (분류코드 != 3) return false;
        if (Ijambo_SMS(Izina, "[Ljava/lang/Object;")) return true;
        int ikigize = ARRAY_ikintu[ikintu_Indanga];
        if (ikigize == -1) return Ijambo_SMS(Izina, "[Ljava/lang/String;") || Ijambo_SMS(Izina, "[Ljava/lang/CharSequence;");
        if (ikigize == 0) return false;
        if (배열종비교(ikigize, Izina)) return true;
        if ((Ijambo_SMS(ikigize, "java/lang/String") || Ijambo_SMS(ikigize, "java/lang/StringBuilder")) && Ijambo_SMS(Izina, "[Ljava/lang/CharSequence;")) return true;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 종수; gukora_mu_matsinda_umugerekashakiro++) if (같은말(icyiciro_Igisobanuro_izina[gukora_mu_matsinda_umugerekashakiro], ikigize)) {
            for (int 문자값 = gukora_mu_matsinda_umugerekashakiro, 중첩깊이 = 0; 문자값 >= 0 && 중첩깊이 < 16; 중첩깊이++, 문자값 = 부모종(문자값)) {
                if (배열종비교(종부모[문자값], Izina)) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[문자값]; 안쪽자리++) if (배열종비교(icyiciro_irebero[문자값 * 16 + 안쪽자리], Izina)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int izina_kidahinduka, int 형식참조) {
        int 검사자리 = 상가[형식참조], 항목수 = 상나[형식참조];
        if (izina_kidahinduka == 0 || 항목수 < 4 || Idosiye[검사자리] != '[' || Idosiye[검사자리 + 1] != 'L' || Idosiye[검사자리 + 항목수 - 1] != ';' || 상나[izina_kidahinduka] != 항목수 - 3) return false;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 항목수 - 3; gukora_mu_matsinda_umugerekashakiro++) if (Idosiye[상가[izina_kidahinduka] + gukora_mu_matsinda_umugerekashakiro] != Idosiye[검사자리 + 2 + gukora_mu_matsinda_umugerekashakiro]) return false;
        return true;
    }
    static void 예외처리() {
        if (던진객체 == 0) return;
        IKOSA = false;
        while (ikadiri_umugerekashakiro >= 현재가닥 * 32) {
            int dosiye_umugerekashakiro = ikadiri_uburyo[ikadiri_umugerekashakiro], 읽는자리 = ikadiri_ibwiriza[ikadiri_umugerekashakiro];
            for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 잡기수; gukora_mu_matsinda_umugerekashakiro++) if (잡기함수[gukora_mu_matsinda_umugerekashakiro] == dosiye_umugerekashakiro && 읽는자리 >= 잡기시작[gukora_mu_matsinda_umugerekashakiro] && 읽는자리 < 잡기끝[gukora_mu_matsinda_umugerekashakiro]
                && (잡기종[gukora_mu_matsinda_umugerekashakiro] == 0 || 맞는객체(던진객체, 잡기종[gukora_mu_matsinda_umugerekashakiro]))) {
                틀위치[ikadiri_umugerekashakiro] = 잡기위치[gukora_mu_matsinda_umugerekashakiro]; ikadiri_Ikirundo[ikadiri_umugerekashakiro] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (gutangiza_ikadiri[ikadiri_umugerekashakiro] != 0) icyiciro_Igisobanuro_imimerere[gutangiza_ikadiri[ikadiri_umugerekashakiro] - 1] = 3;
            if (틀잠금[ikadiri_umugerekashakiro] != 0) { 잠금풀기(틀잠금[ikadiri_umugerekashakiro]); 틀잠금[ikadiri_umugerekashakiro] = 0; }
            ikadiri_umugerekashakiro--;
        }
        ukoresha.kwandika("Uncaught ");
        if (힙[던진객체] == 9) { ukoresha.kwandika(예외이름(힙[던진객체 + 2])); ukoresha.kwandika(": "); kwandika_SMS(힙[던진객체 + 3]); }
        else ukoresha.kwandika("user exception");
        ukoresha.kwandika_inyuguti_agaciro(10); 던진객체 = 0; IKOSA = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void Ikirundo_ibwiriza(int 명령코드) {
        int 첫값 = 빼기(0), 첫형식 = 반환형;
        if (명령코드 == 87) return;
        if (명령코드 == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int bayiti_amakurushingiro = 빼기(0), 둘째형식 = 반환형;
        if (명령코드 == 88) return;
        if (명령코드 == 90) { 넣기(첫값, 첫형식); 넣기(bayiti_amakurushingiro, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 92) { 넣기(bayiti_amakurushingiro, 둘째형식); 넣기(첫값, 첫형식); 넣기(bayiti_amakurushingiro, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 95) { 넣기(첫값, 첫형식); 넣기(bayiti_amakurushingiro, 둘째형식); return; }
        int 문자값 = 빼기(0), 셋째형식 = 반환형;
        if (명령코드 == 91) { 넣기(첫값, 첫형식); 넣기(문자값, 셋째형식); 넣기(bayiti_amakurushingiro, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 93) { 넣기(bayiti_amakurushingiro, 둘째형식); 넣기(첫값, 첫형식); 넣기(문자값, 셋째형식); 넣기(bayiti_amakurushingiro, 둘째형식); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = 반환형;
        넣기(bayiti_amakurushingiro, 둘째형식); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(문자값, 셋째형식); 넣기(bayiti_amakurushingiro, 둘째형식); 넣기(첫값, 첫형식);
    }
    static void 새객체(int izina_kidahinduka, int 시작점) {
        int 분류코드 = 0, 유효길이 = 0, 예외참조 = 예외상수(izina_kidahinduka);
        if (Ijambo_SMS(izina_kidahinduka, "java/lang/StringBuilder")) { 분류코드 = 4; 유효길이 = 1; }
        if (Ijambo_SMS(izina_kidahinduka, "java/io/FileInputStream")) { 분류코드 = 5; 유효길이 = 2; }
        if (Ijambo_SMS(izina_kidahinduka, "java/io/FileOutputStream")) { 분류코드 = 6; 유효길이 = 2; }
        if (예외참조 != 0) { 분류코드 = 9; 유효길이 = 2; }
        if (Ijambo_SMS(izina_kidahinduka, "java/util/ArrayList")) { 분류코드 = 10; 유효길이 = 2; }
        if (Ijambo_SMS(izina_kidahinduka, "java/util/HashMap")) { 분류코드 = 11; 유효길이 = 2; }
        if (Ijambo_SMS(izina_kidahinduka, "java/lang/Integer")) { 분류코드 = 12; 유효길이 = 1; }
        if (Ijambo_SMS(izina_kidahinduka, "java/net/Socket")) { 분류코드 = 17; 유효길이 = 5; }
        if (Ijambo_SMS(izina_kidahinduka, "java/net/ServerSocket")) { 분류코드 = 18; 유효길이 = 5; }
        if (Ijambo_SMS(izina_kidahinduka, "java/net/DatagramSocket")) { 분류코드 = 15; 유효길이 = 3; }
        if (Ijambo_SMS(izina_kidahinduka, "java/net/DatagramPacket")) { 분류코드 = 16; 유효길이 = 4; }
        if (Ijambo_SMS(izina_kidahinduka, "java/lang/Thread") || Ijambo_SMS(izina_kidahinduka, "Ikinyarwanda/자체/작업가닥")) { 분류코드 = 13; 유효길이 = 2; }
        if (Ijambo_SMS(izina_kidahinduka, "java/lang/Object")) { 분류코드 = 8; }
        if (분류코드 == 0 && 화면종(izina_kidahinduka) != 0) { 분류코드 = 화면종(izina_kidahinduka); 유효길이 = 12; }
        if (분류코드 == 0) {
            int 문자값 = gushaka_icyiciro_Igisobanuro(izina_kidahinduka); if (문자값 < 0 || IKOSA || !gutangiza(문자값, 시작점)) return;
            분류코드 = 32 + 문자값; 유효길이 = 종칸수[문자값];
        }
        int ikintu_Indanga = kugenera_Ububiko(분류코드, 유효길이); if (IKOSA) return;
        if (분류코드 == 13 && Ijambo_SMS(izina_kidahinduka, "Ikinyarwanda/자체/작업가닥")) 힙[ikintu_Indanga + 3] = 1;
        if (분류코드 >= 24 && 분류코드 <= 28 && 한국어화면종(izina_kidahinduka) != 0) 힙[ikintu_Indanga + 13] = 1;
        if (분류코드 == 5 || 분류코드 == 6 || 분류코드 == 15 || 분류코드 == 17 || 분류코드 == 18) 힙[ikintu_Indanga + 2] = -1;
        if (분류코드 == 9) 힙[ikintu_Indanga + 2] = 예외참조;
        넣기(ikintu_Indanga, 2);
    }
    static boolean 값같음(int 첫값, int bayiti_amakurushingiro) {
        if (첫값 == bayiti_amakurushingiro) return true;
        if (첫값 == 0 || bayiti_amakurushingiro == 0 || 첫값 < 0 || bayiti_amakurushingiro < 0 || 첫값 >= 힙끝 || bayiti_amakurushingiro >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[bayiti_amakurushingiro] == 1) return 글같음(첫값, bayiti_amakurushingiro, false);
        return 힙[첫값] == 12 && 힙[bayiti_amakurushingiro] == 12 && 힙[첫값 + 2] == 힙[bayiti_amakurushingiro + 2];
    }
    static int 글조각(int ikintu_Indanga, int 시작자리, int 끝자리) {
        if (!ikintu_agaciro_2ed200e9(ikintu_Indanga, 1)) return 0;
        if (시작자리 < 0 || 끝자리 < 시작자리 || 끝자리 > 힙[ikintu_Indanga + 1]) { kudakora_agaciro("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = kugenera_Ububiko(1, 끝자리 - 시작자리); if (IKOSA) return 0;
        for (int gukora_mu_matsinda_umugerekashakiro = 시작자리; gukora_mu_matsinda_umugerekashakiro < 끝자리; gukora_mu_matsinda_umugerekashakiro++) 힙[반환값 + 2 + gukora_mu_matsinda_umugerekashakiro - 시작자리] = 힙[ikintu_Indanga + 2 + gukora_mu_matsinda_umugerekashakiro];
        return 반환값;
    }
    static int ihuza_SMS(int 첫값, int bayiti_amakurushingiro) {
        if (!ikintu_agaciro_2ed200e9(첫값, 1) || !ikintu_agaciro_2ed200e9(bayiti_amakurushingiro, 1)) return 0;
        int 항목수 = 힙[첫값 + 1], uburyo_umugerekashakiro = 힙[bayiti_amakurushingiro + 1], 반환값 = kugenera_Ububiko(1, 항목수 + uburyo_umugerekashakiro); if (IKOSA) return 0;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 항목수; gukora_mu_matsinda_umugerekashakiro++) 힙[반환값 + 2 + gukora_mu_matsinda_umugerekashakiro] = 힙[첫값 + 2 + gukora_mu_matsinda_umugerekashakiro];
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < uburyo_umugerekashakiro; gukora_mu_matsinda_umugerekashakiro++) 힙[반환값 + 2 + 항목수 + gukora_mu_matsinda_umugerekashakiro] = 힙[bayiti_amakurushingiro + 2 + gukora_mu_matsinda_umugerekashakiro];
        return 반환값;
    }
    static boolean 기본호출(int nyirayo, int izina_kidahinduka, int 서술상수, int 명령코드) {
        if (Ijambo_SMS(nyirayo, "Ikinyarwanda/자체/실행인수") && 명령코드 == 184) {
            if (Ijambo_SMS(izina_kidahinduka, "개수") && Ijambo_SMS(서술상수, "()I")) { 넣기(ukoresha.인수개수() - 1, 1); return true; }
            if (Ijambo_SMS(izina_kidahinduka, "Umwandiko") && Ijambo_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= ukoresha.인수개수() - 1) 예외던짐(29, "gukora_ibwiriza 인수 범위를 벗어났습니다");
                else 넣기(gucumbikira_inyuguti(ukoresha.인수(순번 + 1)), 2);
                return true;
            }
            kudakora_agaciro("지원하지 않는 Ikinyarwanda gukora_ibwiriza 인수 호출"); return true;
        }
        if (Ijambo_SMS(nyirayo, "Ikinyarwanda/자체/작업가닥")) { Inzira_mugenaporogaramu(izina_kidahinduka, 서술상수, 명령코드, true); return true; }
        if (한국어화면소유(nyirayo)) { 한국어화면호출(nyirayo, izina_kidahinduka, 서술상수, 명령코드); return true; }
        if (화면소유(nyirayo)) { 화면호출(nyirayo, izina_kidahinduka, 서술상수, 명령코드); return true; }
        if (Ijambo_SMS(nyirayo, "java/net/Socket") || Ijambo_SMS(nyirayo, "java/net/ServerSocket") || Ijambo_SMS(nyirayo, "java/io/InputStream") || Ijambo_SMS(nyirayo, "java/io/OutputStream")) { 흐름호출(nyirayo, izina_kidahinduka, 서술상수, 명령코드); return true; }
        if (Ijambo_SMS(nyirayo, "Ikinyarwanda/자체/intima_agaciro") && 명령코드 == 184) {
            if (Ijambo_SMS(izina_kidahinduka, "화면너비") && Ijambo_SMS(서술상수, "()I")) { 넣기(ukoresha.화면너비(), 1); return true; }
            if (Ijambo_SMS(izina_kidahinduka, "화면높이") && Ijambo_SMS(서술상수, "()I")) { 넣기(ukoresha.화면높이(), 1); return true; }
            if (Ijambo_SMS(izina_kidahinduka, "밀리초") && Ijambo_SMS(서술상수, "()I")) { 넣기(ukoresha.밀리초(), 1); return true; }
            if (Ijambo_SMS(izina_kidahinduka, "그림대기") && Ijambo_SMS(서술상수, "()I")) { 넣기(ukoresha.그림대기(), 1); return true; }
            if (Ijambo_SMS(izina_kidahinduka, "사각형") && Ijambo_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), Ihuza_rya_x = 빼기(1); 넣기(ukoresha.사각형(Ihuza_rya_x, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Ijambo_SMS(nyirayo, "java/net/InetAddress") || Ijambo_SMS(nyirayo, "java/net/DatagramPacket") || Ijambo_SMS(nyirayo, "java/net/DatagramSocket")) { 통신호출(nyirayo, izina_kidahinduka, 서술상수, 명령코드); return true; }
        if (Ijambo_SMS(nyirayo, "java/lang/Thread")) { 가닥호출(izina_kidahinduka, 서술상수, 명령코드); return true; }
        if (Ijambo_SMS(nyirayo, "java/lang/Object")) {
            if (Ijambo_SMS(izina_kidahinduka, "<init>") && Ijambo_SMS(서술상수, "()V") && 명령코드 == 183) { 객체유효(빼기(2)); return true; }
            if (Ijambo_SMS(izina_kidahinduka, "equals") && Ijambo_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bayiti_amakurushingiro = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == bayiti_amakurushingiro ? 1 : 0, 1); return true; }
        }
        if (예외상수(nyirayo) != 0) {
            if (Ijambo_SMS(izina_kidahinduka, "<init>") && 명령코드 == 183 && (Ijambo_SMS(서술상수, "()V") || Ijambo_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int integuza = Ijambo_SMS(서술상수, "()V") ? 0 : 빼기(2), ikintu_Indanga = 빼기(2);
                if (ikintu_agaciro_2ed200e9(ikintu_Indanga, 9)) { 힙[ikintu_Indanga + 3] = integuza; 힙참조[ikintu_Indanga + 3] = 1; } return true;
            }
            if ((Ijambo_SMS(izina_kidahinduka, "getMessage") || Ijambo_SMS(izina_kidahinduka, "설명")) && Ijambo_SMS(서술상수, "()Ljava/lang/String;")) { int ikintu_Indanga = 빼기(2); if (ikintu_agaciro_2ed200e9(ikintu_Indanga, 9)) 넣기(힙[ikintu_Indanga + 3], 2); return true; }
        }
        if (Ijambo_SMS(nyirayo, "java/lang/String")) {
            if (명령코드 == 182 && Ijambo_SMS(izina_kidahinduka, "getBytes") && (Ijambo_SMS(서술상수, "()[B") || Ijambo_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int gusobeka_izina = Ijambo_SMS(서술상수, "()[B") ? 0 : 빼기(2), ikintu_Indanga = 빼기(2);
                if (!ikintu_agaciro_2ed200e9(ikintu_Indanga, 1)) return true;
                if (gusobeka_izina != 0 && !글같음(gusobeka_izina, gucumbikira_inyuguti("UTF-8"), false) && !글같음(gusobeka_izina, gucumbikira_inyuguti("UTF8"), false) && !글같음(gusobeka_izina, gucumbikira_inyuguti("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int 항목수 = 힙[ikintu_Indanga + 1], 반환값 = kugenera_Ububiko(20, 항목수 * 3), 사용수 = 0; if (IKOSA) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) {
                    int 문자값 = 힙[ikintu_Indanga + 2 + 안쪽자리];
                    if (문자값 >= 0xd800 && 문자값 <= 0xdbff && 안쪽자리 + 1 < 항목수 && 힙[ikintu_Indanga + 3 + 안쪽자리] >= 0xdc00 && 힙[ikintu_Indanga + 3 + 안쪽자리] <= 0xdfff) 문자값 = 0x10000 + ((문자값 - 0xd800) << 10) + 힙[ikintu_Indanga + 2 + ++안쪽자리] - 0xdc00;
                    else if (문자값 >= 0xd800 && 문자값 <= 0xdfff) 문자값 = '?';
                    if (문자값 < 128) 힙[반환값 + 2 + 사용수++] = 문자값;
                    else { int 바이트수 = 문자값 < 2048 ? 2 : 문자값 < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((바이트수 == 2 ? 192 : 바이트수 == 3 ? 224 : 240) | 문자값 >> (6 * (바이트수 - 1))); for (int 비교자리 = 바이트수 - 1; 비교자리 > 0; 비교자리--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | 문자값 >> (6 * (비교자리 - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (명령코드 == 184 && Ijambo_SMS(izina_kidahinduka, "valueOf") && Ijambo_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(umubare_inyuguti(빼기(1)), 2); return true; }
            if (명령코드 != 182) return false;
            if (Ijambo_SMS(izina_kidahinduka, "equals") && Ijambo_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int bayiti_amakurushingiro = 빼기(2), 첫값 = 빼기(2); if (ikintu_agaciro_2ed200e9(첫값, 1)) 넣기(글같음(첫값, bayiti_amakurushingiro, false) ? 1 : 0, 1); return true; }
            if (Ijambo_SMS(izina_kidahinduka, "isEmpty") && Ijambo_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (ikintu_agaciro_2ed200e9(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Ijambo_SMS(izina_kidahinduka, "substring") && (Ijambo_SMS(서술상수, "(I)Ljava/lang/String;") || Ijambo_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean 둘째값 = Ijambo_SMS(서술상수, "(II)Ljava/lang/String;"); int 끝자리 = 둘째값 ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (ikintu_agaciro_2ed200e9(첫값, 1)) 넣기(글조각(첫값, 시작점, 둘째값 ? 끝자리 : 힙[첫값 + 1]), 2); return true;
            }
            if (Ijambo_SMS(izina_kidahinduka, "concat") && Ijambo_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int bayiti_amakurushingiro = 빼기(2), 첫값 = 빼기(2); 넣기(ihuza_SMS(첫값, bayiti_amakurushingiro), 2); return true; }
            if (Ijambo_SMS(izina_kidahinduka, "hashCode") && Ijambo_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), hashi_agaciro = 0; if (ikintu_agaciro_2ed200e9(첫값, 1)) { for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 힙[첫값 + 1]; gukora_mu_matsinda_umugerekashakiro++) hashi_agaciro = hashi_agaciro * 31 + 힙[첫값 + 2 + gukora_mu_matsinda_umugerekashakiro]; 넣기(hashi_agaciro, 1); } return true; }
            if (Ijambo_SMS(izina_kidahinduka, "toString") && Ijambo_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (ikintu_agaciro_2ed200e9(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Ijambo_SMS(nyirayo, "java/lang/Integer")) {
            if (명령코드 == 184 && Ijambo_SMS(izina_kidahinduka, "valueOf") && Ijambo_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int amakurushingiro_agaciro = 빼기(1), ikintu_Indanga = amakurushingiro_agaciro >= -128 && amakurushingiro_agaciro <= 127 ? Store_umubare_wuzuye[amakurushingiro_agaciro + 128] : 0; if (ikintu_Indanga == 0) { ikintu_Indanga = kugenera_Ububiko(12, 1); if (!IKOSA) { 힙[ikintu_Indanga + 2] = amakurushingiro_agaciro; if (amakurushingiro_agaciro >= -128 && amakurushingiro_agaciro <= 127) Store_umubare_wuzuye[amakurushingiro_agaciro + 128] = ikintu_Indanga; } } 넣기(ikintu_Indanga, 2); return true; }
            if (명령코드 == 183 && Ijambo_SMS(izina_kidahinduka, "<init>") && Ijambo_SMS(서술상수, "(I)V")) { int amakurushingiro_agaciro = 빼기(1), ikintu_Indanga = 빼기(2); if (ikintu_agaciro_2ed200e9(ikintu_Indanga, 12)) 힙[ikintu_Indanga + 2] = amakurushingiro_agaciro; return true; }
            if (명령코드 == 182 && Ijambo_SMS(izina_kidahinduka, "intValue") && Ijambo_SMS(서술상수, "()I")) { int ikintu_Indanga = 빼기(2); if (ikintu_agaciro_2ed200e9(ikintu_Indanga, 12)) 넣기(힙[ikintu_Indanga + 2], 1); return true; }
            if (명령코드 == 184 && Ijambo_SMS(izina_kidahinduka, "toString") && Ijambo_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(umubare_inyuguti(빼기(1)), 2); return true; }
        }
        if (Ijambo_SMS(nyirayo, "java/lang/Math") && 명령코드 == 184) {
            if (Ijambo_SMS(izina_kidahinduka, "abs") && Ijambo_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Ijambo_SMS(izina_kidahinduka, "min") || Ijambo_SMS(izina_kidahinduka, "max")) && Ijambo_SMS(서술상수, "(II)I")) { int bayiti_amakurushingiro = 빼기(1), 첫값 = 빼기(1); 넣기(Ijambo_SMS(izina_kidahinduka, "min") ? (첫값 < bayiti_amakurushingiro ? 첫값 : bayiti_amakurushingiro) : (첫값 > bayiti_amakurushingiro ? 첫값 : bayiti_amakurushingiro), 1); return true; }
        }
        if (Ijambo_SMS(nyirayo, "java/lang/System") && 명령코드 == 184) {
            if (Ijambo_SMS(izina_kidahinduka, "gc") && Ijambo_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Ijambo_SMS(izina_kidahinduka, "arraycopy") && Ijambo_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int 항목수 = 빼기(1), aho_ijya_agaciro_umugerekashakiro = 빼기(1), bayiti_amakurushingiro = 빼기(2), 시작자리 = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(bayiti_amakurushingiro)) {
                    int 분류코드 = 힙[첫값];
                    if (힙[bayiti_amakurushingiro] != 분류코드 || (분류코드 != 2 && 분류코드 != 3 && (분류코드 < 20 || 분류코드 > 23))) kudakora_agaciro("arraycopy type mismatch");
                    else if (항목수 < 0 || 시작자리 < 0 || aho_ijya_agaciro_umugerekashakiro < 0 || 시작자리 > 힙[첫값 + 1] - 항목수 || aho_ijya_agaciro_umugerekashakiro > 힙[bayiti_amakurushingiro + 1] - 항목수) kudakora_agaciro("ArrayIndexOutOfBoundsException");
                    else if (첫값 == bayiti_amakurushingiro && aho_ijya_agaciro_umugerekashakiro > 시작자리) { for (int gukora_mu_matsinda_umugerekashakiro = 항목수 - 1; gukora_mu_matsinda_umugerekashakiro >= 0; gukora_mu_matsinda_umugerekashakiro--) 힙[bayiti_amakurushingiro + 2 + aho_ijya_agaciro_umugerekashakiro + gukora_mu_matsinda_umugerekashakiro] = 힙[첫값 + 2 + 시작자리 + gukora_mu_matsinda_umugerekashakiro]; }
                    else { for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 항목수 && !IKOSA; gukora_mu_matsinda_umugerekashakiro++) { int amakurushingiro_agaciro = 힙[첫값 + 2 + 시작자리 + gukora_mu_matsinda_umugerekashakiro]; if (분류코드 != 3 || 배열저장가능(bayiti_amakurushingiro, amakurushingiro_agaciro)) 힙[bayiti_amakurushingiro + 2 + aho_ijya_agaciro_umugerekashakiro + gukora_mu_matsinda_umugerekashakiro] = amakurushingiro_agaciro; } }
                }
                return true;
            }
        }
        if (Ijambo_SMS(nyirayo, "java/util/ArrayList") || Ijambo_SMS(nyirayo, "java/util/List") || Ijambo_SMS(nyirayo, "java/util/HashMap") || Ijambo_SMS(nyirayo, "java/util/Map")) {
            모음호출(nyirayo, izina_kidahinduka, 서술상수, 명령코드); return true;
        }
        return false;
    }
    static void 모음늘리기(int ikintu_Indanga, int 필요수) {
        int 이전값 = 힙[ikintu_Indanga + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int 다음자리 = 용량값 < 8 ? 8 : 용량값 * 2; if (다음자리 < 필요수) 다음자리 = 필요수;
        int amakurushingiro_ARRAY = kugenera_Ububiko(3, 다음자리); if (IKOSA) return;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 용량값; gukora_mu_matsinda_umugerekashakiro++) 힙[amakurushingiro_ARRAY + 2 + gukora_mu_matsinda_umugerekashakiro] = 힙[이전값 + 2 + gukora_mu_matsinda_umugerekashakiro];
        힙[ikintu_Indanga + 2] = amakurushingiro_ARRAY; 힙참조[ikintu_Indanga + 2] = 1;
    }
    static void 모음호출(int nyirayo, int izina_kidahinduka, int 서술상수, int 명령코드) {
        boolean 대응참조 = Ijambo_SMS(nyirayo, "java/util/HashMap") || Ijambo_SMS(nyirayo, "java/util/Map"); int 분류코드 = 대응참조 ? 11 : 10;
        if (Ijambo_SMS(izina_kidahinduka, "<init>") && 명령코드 == 183 && Ijambo_SMS(서술상수, "()V")) { int ikintu_Indanga = 빼기(2); if (ikintu_agaciro_2ed200e9(ikintu_Indanga, 분류코드)) 모음늘리기(ikintu_Indanga, 8); return; }
        if (명령코드 != 182 && 명령코드 != 185) { kudakora_agaciro("invalid collection invocation"); return; }
        if (Ijambo_SMS(izina_kidahinduka, "size") && Ijambo_SMS(서술상수, "()I") || Ijambo_SMS(izina_kidahinduka, "isEmpty") && Ijambo_SMS(서술상수, "()Z")) {
            int ikintu_Indanga = 빼기(2); if (ikintu_agaciro_2ed200e9(ikintu_Indanga, 분류코드)) 넣기(Ijambo_SMS(izina_kidahinduka, "size") ? 힙[ikintu_Indanga + 3] : 힙[ikintu_Indanga + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Ijambo_SMS(izina_kidahinduka, "clear") && Ijambo_SMS(서술상수, "()V")) { int ikintu_Indanga = 빼기(2); if (ikintu_agaciro_2ed200e9(ikintu_Indanga, 분류코드)) { int amakurushingiro_ARRAY = 힙[ikintu_Indanga + 2]; for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 힙[amakurushingiro_ARRAY + 1]; gukora_mu_matsinda_umugerekashakiro++) 힙[amakurushingiro_ARRAY + 2 + gukora_mu_matsinda_umugerekashakiro] = 0; 힙[ikintu_Indanga + 3] = 0; } return; }
        if (!대응참조 && Ijambo_SMS(izina_kidahinduka, "add") && Ijambo_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int amakurushingiro_agaciro = 빼기(2), ikintu_Indanga = 빼기(2); if (!ikintu_agaciro_2ed200e9(ikintu_Indanga, 10)) return;
            int 항목수 = 힙[ikintu_Indanga + 3]; 모음늘리기(ikintu_Indanga, 항목수 + 1); if (!IKOSA) { 힙[힙[ikintu_Indanga + 2] + 2 + 항목수] = amakurushingiro_agaciro; 힙[ikintu_Indanga + 3] = 항목수 + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Ijambo_SMS(izina_kidahinduka, "get") || Ijambo_SMS(izina_kidahinduka, "remove")) && Ijambo_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Ijambo_SMS(izina_kidahinduka, "set") && Ijambo_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Ijambo_SMS(izina_kidahinduka, "set"); int amakurushingiro_agaciro = 지정여부 ? 빼기(2) : 0, 항목자리 = 빼기(1), ikintu_Indanga = 빼기(2);
            if (!ikintu_agaciro_2ed200e9(ikintu_Indanga, 10)) return;
            int 항목수 = 힙[ikintu_Indanga + 3], amakurushingiro_ARRAY = 힙[ikintu_Indanga + 2];
            if (항목자리 < 0 || 항목자리 >= 항목수) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[amakurushingiro_ARRAY + 2 + 항목자리];
            if (지정여부) 힙[amakurushingiro_ARRAY + 2 + 항목자리] = amakurushingiro_agaciro;
            if (Ijambo_SMS(izina_kidahinduka, "remove")) { for (int gukora_mu_matsinda_umugerekashakiro = 항목자리 + 1; gukora_mu_matsinda_umugerekashakiro < 항목수; gukora_mu_matsinda_umugerekashakiro++) 힙[amakurushingiro_ARRAY + 1 + gukora_mu_matsinda_umugerekashakiro] = 힙[amakurushingiro_ARRAY + 2 + gukora_mu_matsinda_umugerekashakiro]; 힙[amakurushingiro_ARRAY + 1 + 항목수] = 0; 힙[ikintu_Indanga + 3] = 항목수 - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Ijambo_SMS(izina_kidahinduka, "get") || Ijambo_SMS(izina_kidahinduka, "remove")) && Ijambo_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Ijambo_SMS(izina_kidahinduka, "put") && Ijambo_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Ijambo_SMS(izina_kidahinduka, "containsKey") && Ijambo_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Ijambo_SMS(izina_kidahinduka, "put"), gukuramo = Ijambo_SMS(izina_kidahinduka, "remove");
            int amakurushingiro_agaciro = 넣기여부 ? 빼기(2) : 0, buto_Indanga = 빼기(2), ikintu_Indanga = 빼기(2); if (!ikintu_agaciro_2ed200e9(ikintu_Indanga, 11)) return;
            int 항목수 = 힙[ikintu_Indanga + 3], amakurushingiro_ARRAY = 힙[ikintu_Indanga + 2], 찾은여부 = -1;
            for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 항목수; gukora_mu_matsinda_umugerekashakiro++) if (값같음(buto_Indanga, 힙[amakurushingiro_ARRAY + 2 + 2 * gukora_mu_matsinda_umugerekashakiro])) { 찾은여부 = gukora_mu_matsinda_umugerekashakiro; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[amakurushingiro_ARRAY + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(ikintu_Indanga, (항목수 + 1) * 2); amakurushingiro_ARRAY = 힙[ikintu_Indanga + 2]; 찾은여부 = 항목수; if (!IKOSA) 힙[ikintu_Indanga + 3] = 항목수 + 1; }
                if (!IKOSA) { 힙[amakurushingiro_ARRAY + 2 + 2 * 찾은여부] = buto_Indanga; 힙[amakurushingiro_ARRAY + 3 + 2 * 찾은여부] = amakurushingiro_agaciro; }
            }
            if (gukuramo && 찾은여부 >= 0) { for (int gukora_mu_matsinda_umugerekashakiro = 찾은여부 + 1; gukora_mu_matsinda_umugerekashakiro < 항목수; gukora_mu_matsinda_umugerekashakiro++) { 힙[amakurushingiro_ARRAY + 2 * gukora_mu_matsinda_umugerekashakiro] = 힙[amakurushingiro_ARRAY + 2 + 2 * gukora_mu_matsinda_umugerekashakiro]; 힙[amakurushingiro_ARRAY + 1 + 2 * gukora_mu_matsinda_umugerekashakiro] = 힙[amakurushingiro_ARRAY + 3 + 2 * gukora_mu_matsinda_umugerekashakiro]; } 힙[amakurushingiro_ARRAY + 2 * 항목수] = 0; 힙[amakurushingiro_ARRAY + 1 + 2 * 항목수] = 0; 힙[ikintu_Indanga + 3] = 항목수 - 1; }
            if (Ijambo_SMS(izina_kidahinduka, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        kudakora_agaciro("unsupported collection method");
    }
    static boolean 잠금얻기(int ikintu_Indanga) {
        if (!객체유효(ikintu_Indanga)) return false;
        if (잠금깊이[ikintu_Indanga] != 0 && 잠금주인[ikintu_Indanga] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        잠금주인[ikintu_Indanga] = 현재가닥 + 1; 잠금깊이[ikintu_Indanga]++; return true;
    }
    static void 잠금풀기(int ikintu_Indanga) {
        if (!객체유효(ikintu_Indanga)) return;
        if (잠금깊이[ikintu_Indanga] == 0 || 잠금주인[ikintu_Indanga] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[ikintu_Indanga] == 0) 잠금주인[ikintu_Indanga] = 0;
    }
    static boolean guhinduranya_mugenaporogaramu() {
        mugenaporogaramu_ikadiri[현재가닥] = ikadiri_umugerekashakiro;
        if (ikadiri_umugerekashakiro < 현재가닥 * 32) mugenaporogaramu_imimerere[현재가닥] = 3;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 가닥수; gukora_mu_matsinda_umugerekashakiro++) if (mugenaporogaramu_imimerere[gukora_mu_matsinda_umugerekashakiro] == 2 && mugenaporogaramu_imimerere[가닥대기[gukora_mu_matsinda_umugerekashakiro]] == 3) mugenaporogaramu_imimerere[gukora_mu_matsinda_umugerekashakiro] = 1;
        for (int gukora_mu_matsinda_umugerekashakiro = 1; gukora_mu_matsinda_umugerekashakiro <= 가닥수; gukora_mu_matsinda_umugerekashakiro++) {
            int 다음자리 = (현재가닥 + gukora_mu_matsinda_umugerekashakiro) % 가닥수;
            if (mugenaporogaramu_imimerere[다음자리] == 1) { 현재가닥 = 다음자리; ikadiri_umugerekashakiro = mugenaporogaramu_ikadiri[다음자리]; 바꿈요청 = false; return true; }
        }
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 가닥수; gukora_mu_matsinda_umugerekashakiro++) if (mugenaporogaramu_imimerere[gukora_mu_matsinda_umugerekashakiro] != 3) { kudakora_agaciro("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int izina_kidahinduka, int 서술상수, int 명령코드) { Inzira_mugenaporogaramu(izina_kidahinduka, 서술상수, 명령코드, false); }
    static void Inzira_mugenaporogaramu(int izina_kidahinduka, int 서술상수, int 명령코드, boolean Ikinyarwanda) {
        if (명령코드 == 184 && Ijambo_SMS(izina_kidahinduka, Ikinyarwanda ? "gusubika_umukoro" : "yield") && Ijambo_SMS(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (명령코드 == 184 && Ijambo_SMS(izina_kidahinduka, "currentThread") && Ijambo_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(mugenaporogaramu_ikintu[현재가닥], 2); return; }
        if (명령코드 == 183 && Ijambo_SMS(izina_kidahinduka, "<init>") && (Ijambo_SMS(서술상수, "()V") || Ijambo_SMS(서술상수, Ikinyarwanda ? "(LIkinyarwanda/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int gusimbuza_igishya_aderesi = Ijambo_SMS(서술상수, "()V") ? 0 : 빼기(2), ikintu_Indanga = 빼기(2);
            if (!객체유효(ikintu_Indanga)) return;
            if (힙[ikintu_Indanga] == 13) { 힙[ikintu_Indanga + 2] = gusimbuza_igishya_aderesi; 힙참조[ikintu_Indanga + 2] = 1; }
            else if (gusimbuza_igishya_aderesi != 0) kudakora_agaciro("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (명령코드 == 182 && (Ijambo_SMS(izina_kidahinduka, Ikinyarwanda ? "Itangira_umukoro" : "start") || Ijambo_SMS(izina_kidahinduka, Ikinyarwanda ? "기다리기" : "join")) && Ijambo_SMS(서술상수, "()V") || 명령코드 == 182 && Ijambo_SMS(izina_kidahinduka, Ikinyarwanda ? "살아있는가" : "isAlive") && Ijambo_SMS(서술상수, "()Z")) {
            int ikintu_Indanga = 빼기(2); if (!객체유효(ikintu_Indanga)) return;
            int konti_agaciro = -1; for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 가닥수; gukora_mu_matsinda_umugerekashakiro++) if (mugenaporogaramu_ikintu[gukora_mu_matsinda_umugerekashakiro] == ikintu_Indanga) konti_agaciro = gukora_mu_matsinda_umugerekashakiro;
            if (Ijambo_SMS(izina_kidahinduka, Ikinyarwanda ? "살아있는가" : "isAlive")) { 넣기(konti_agaciro >= 0 && mugenaporogaramu_imimerere[konti_agaciro] != 3 ? 1 : 0, 1); return; }
            if (Ijambo_SMS(izina_kidahinduka, Ikinyarwanda ? "기다리기" : "join")) { if (konti_agaciro >= 0 && mugenaporogaramu_imimerere[konti_agaciro] != 3) { 가닥대기[현재가닥] = konti_agaciro; mugenaporogaramu_imimerere[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (konti_agaciro >= 0) { 예외던짐(Ikinyarwanda ? 38 : 16, "thread already started"); return; }
            if (가닥수 == 4) { kudakora_agaciro("thread limit (4 including main)"); return; }
            int gusimbuza_igishya_aderesi = 힙[ikintu_Indanga] == 13 ? 힙[ikintu_Indanga + 2] : ikintu_Indanga;
            int dosiye_umugerekashakiro = gusimbuza_igishya_aderesi > 0 && 힙[gusimbuza_igishya_aderesi] >= 32 ? izina_uburyo(힙[gusimbuza_igishya_aderesi] - 32, Ikinyarwanda ? "gukora_umukoro" : "run", "()V") : -1;
            if (gusimbuza_igishya_aderesi != 0 && dosiye_umugerekashakiro < 0) { kudakora_agaciro("Runnable.run required"); return; }
            konti_agaciro = 가닥수++; mugenaporogaramu_ikintu[konti_agaciro] = ikintu_Indanga; mugenaporogaramu_gusimbuza_igishya[konti_agaciro] = gusimbuza_igishya_aderesi;
            int ikadiri = konti_agaciro * 32; mugenaporogaramu_ikadiri[konti_agaciro] = dosiye_umugerekashakiro < 0 ? ikadiri - 1 : ikadiri; mugenaporogaramu_imimerere[konti_agaciro] = dosiye_umugerekashakiro < 0 ? 3 : 1;
            if (dosiye_umugerekashakiro >= 0) { ikadiri_uburyo[ikadiri] = dosiye_umugerekashakiro; 틀위치[ikadiri] = uburyo_Itangira[dosiye_umugerekashakiro]; mu_gace_agaciro[ikadiri * 128] = gusimbuza_igishya_aderesi; 지역형[ikadiri * 128] = 2; }
            return;
        }
        kudakora_agaciro("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], aderesi_SMS = new int[16];
    static int mu_gace_aderesi() { return aderesi_ikintu(0x7f000001); }
    static int aderesi_ikintu(int agaciro) { int ikintu_Indanga = kugenera_Ububiko(14, 1); if (!IKOSA) 힙[ikintu_Indanga + 2] = agaciro; return ikintu_Indanga; }
    static int 주소해독(int ikintu_Indanga) {
        if (ikintu_Indanga == 0 || 글같음(ikintu_Indanga, gucumbikira_inyuguti("localhost"), false)) return 0x7f000001;
        if (!ikintu_agaciro_2ed200e9(ikintu_Indanga, 1)) return 0;
        int amakurushingiro_agaciro = 0, 총수 = 0, aderesi_bayiti = 0, 자릿수 = 0, 항목수 = 힙[ikintu_Indanga + 1];
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro <= 항목수; gukora_mu_matsinda_umugerekashakiro++) {
            int 문자값 = gukora_mu_matsinda_umugerekashakiro == 항목수 ? '.' : 힙[ikintu_Indanga + 2 + gukora_mu_matsinda_umugerekashakiro];
            if (문자값 == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } amakurushingiro_agaciro = amakurushingiro_agaciro << 8 | aderesi_bayiti; 총수++; aderesi_bayiti = 자릿수 = 0; }
            else { if (문자값 < '0' || 문자값 > '9' || ++자릿수 > 3 || (aderesi_bayiti = aderesi_bayiti * 10 + 문자값 - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return amakurushingiro_agaciro;
    }
    static int aderesi_inyuguti(int amakurushingiro_agaciro) {
        int 항목수 = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int aderesi_bayiti = amakurushingiro_agaciro >>> 이동비트 & 255;
            if (aderesi_bayiti >= 100) aderesi_SMS[항목수++] = '0' + aderesi_bayiti / 100;
            if (aderesi_bayiti >= 10) aderesi_SMS[항목수++] = '0' + aderesi_bayiti / 10 % 10;
            aderesi_SMS[항목수++] = '0' + aderesi_bayiti % 10; if (이동비트 != 0) aderesi_SMS[항목수++] = '.';
        }
        int ikintu_Indanga = kugenera_Ububiko(1, 항목수); if (!IKOSA) for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 항목수; gukora_mu_matsinda_umugerekashakiro++) 힙[ikintu_Indanga + 2 + gukora_mu_matsinda_umugerekashakiro] = aderesi_SMS[gukora_mu_matsinda_umugerekashakiro]; return ikintu_Indanga;
    }
    static void 통신호출(int nyirayo, int izina_kidahinduka, int 서술상수, int 명령코드) {
        if (Ijambo_SMS(nyirayo, "java/net/InetAddress")) {
            if (명령코드 == 184 && Ijambo_SMS(izina_kidahinduka, "getLoopbackAddress") && Ijambo_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(mu_gace_aderesi(), 2); return; }
            if (명령코드 == 184 && Ijambo_SMS(izina_kidahinduka, "getByName") && Ijambo_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int amakurushingiro_agaciro = 주소해독(빼기(2)); if (던진객체 == 0 && !IKOSA) 넣기(aderesi_ikintu(amakurushingiro_agaciro), 2); return;
            }
            if (명령코드 == 182 && Ijambo_SMS(izina_kidahinduka, "getHostAddress") && Ijambo_SMS(서술상수, "()Ljava/lang/String;")) { int ikintu_Indanga = 빼기(2); if (ikintu_agaciro_2ed200e9(ikintu_Indanga, 14)) 넣기(aderesi_inyuguti(힙[ikintu_Indanga + 2]), 2); return; }
        }
        if (Ijambo_SMS(nyirayo, "java/net/DatagramPacket")) {
            if (명령코드 == 183 && Ijambo_SMS(izina_kidahinduka, "<init>") && (Ijambo_SMS(서술상수, "([BI)V") || Ijambo_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean aho_ijya_agaciro_Indanga = Ijambo_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = aho_ijya_agaciro_Indanga ? 빼기(1) : 0, aderesi_Indanga = aho_ijya_agaciro_Indanga ? 빼기(2) : 0;
                int 항목수 = 빼기(1), amakurushingiro_ARRAY = 빼기(2), ikintu_Indanga = 빼기(2);
                if (!ikintu_agaciro_2ed200e9(ikintu_Indanga, 16) || !ikintu_agaciro_2ed200e9(amakurushingiro_ARRAY, 20)) return;
                if (항목수 < 0 || 항목수 > 힙[amakurushingiro_ARRAY + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (aderesi_Indanga != 0 && !ikintu_agaciro_2ed200e9(aderesi_Indanga, 14)) return;
                힙[ikintu_Indanga + 2] = amakurushingiro_ARRAY; 힙참조[ikintu_Indanga + 2] = 1; 힙[ikintu_Indanga + 3] = 항목수;
                힙[ikintu_Indanga + 4] = aderesi_Indanga; 힙참조[ikintu_Indanga + 4] = 1; 힙[ikintu_Indanga + 5] = 접속번호; return;
            }
            if (명령코드 == 182 && Ijambo_SMS(izina_kidahinduka, "setLength") && Ijambo_SMS(서술상수, "(I)V")) {
                int 항목수 = 빼기(1), ikintu_Indanga = 빼기(2); if (!ikintu_agaciro_2ed200e9(ikintu_Indanga, 16)) return;
                if (항목수 < 0 || 항목수 > 힙[힙[ikintu_Indanga + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[ikintu_Indanga + 3] = 항목수; return;
            }
            if (명령코드 == 182 && (Ijambo_SMS(izina_kidahinduka, "getData") && Ijambo_SMS(서술상수, "()[B") || Ijambo_SMS(izina_kidahinduka, "getLength") && Ijambo_SMS(서술상수, "()I") || Ijambo_SMS(izina_kidahinduka, "getAddress") && Ijambo_SMS(서술상수, "()Ljava/net/InetAddress;") || Ijambo_SMS(izina_kidahinduka, "getPort") && Ijambo_SMS(서술상수, "()I"))) {
                int ikintu_Indanga = 빼기(2); if (!ikintu_agaciro_2ed200e9(ikintu_Indanga, 16)) return;
                int 항목자리 = Ijambo_SMS(izina_kidahinduka, "getData") ? 2 : Ijambo_SMS(izina_kidahinduka, "getLength") ? 3 : Ijambo_SMS(izina_kidahinduka, "getAddress") ? 4 : 5;
                넣기(힙[ikintu_Indanga + 항목자리], 항목자리 == 2 || 항목자리 == 4 ? 2 : 1); return;
            }
        }
        if (Ijambo_SMS(nyirayo, "java/net/DatagramSocket")) {
            if (명령코드 == 183 && Ijambo_SMS(izina_kidahinduka, "<init>") && (Ijambo_SMS(서술상수, "()V") || Ijambo_SMS(서술상수, "(I)V"))) {
                int 접속번호 = Ijambo_SMS(서술상수, "()V") ? 0 : 빼기(1), ikintu_Indanga = 빼기(2); if (!ikintu_agaciro_2ed200e9(ikintu_Indanga, 15)) return;
                if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = ukoresha.kurema_Urusobemiyoboro(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[ikintu_Indanga + 2] = 열린파일번호; return;
            }
            if (명령코드 == 182 && Ijambo_SMS(izina_kidahinduka, "setSoTimeout") && Ijambo_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), ikintu_Indanga = 빼기(2); if (!ikintu_agaciro_2ed200e9(ikintu_Indanga, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[ikintu_Indanga + 3] = 밀리초값; return;
            }
            if (명령코드 == 182 && Ijambo_SMS(izina_kidahinduka, "getLocalPort") && Ijambo_SMS(서술상수, "()I")) { int ikintu_Indanga = 빼기(2); if (ikintu_agaciro_2ed200e9(ikintu_Indanga, 15)) 넣기(힙[ikintu_Indanga + 2] < 0 ? -1 : ukoresha.Urusobemiyoboro_poti(힙[ikintu_Indanga + 2]), 1); return; }
            if (명령코드 == 182 && Ijambo_SMS(izina_kidahinduka, "isClosed") && Ijambo_SMS(서술상수, "()Z")) { int ikintu_Indanga = 빼기(2); if (ikintu_agaciro_2ed200e9(ikintu_Indanga, 15)) 넣기(힙[ikintu_Indanga + 2] < 0 ? 1 : 0, 1); return; }
            if (명령코드 == 182 && Ijambo_SMS(izina_kidahinduka, "close") && Ijambo_SMS(서술상수, "()V")) { int ikintu_Indanga = 빼기(2); if (ikintu_agaciro_2ed200e9(ikintu_Indanga, 15) && 힙[ikintu_Indanga + 2] >= 0) { ukoresha.파일서술자닫기(힙[ikintu_Indanga + 2]); 힙[ikintu_Indanga + 2] = -1; } return; }
            if (명령코드 == 182 && (Ijambo_SMS(izina_kidahinduka, "send") || Ijambo_SMS(izina_kidahinduka, "receive")) && Ijambo_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int ipaki_5cd5338b = 빼기(2), ikintu_Indanga = 빼기(2); if (!ikintu_agaciro_2ed200e9(ipaki_5cd5338b, 16) || !ikintu_agaciro_2ed200e9(ikintu_Indanga, 15)) return;
                int amakurushingiro_ARRAY = 힙[ipaki_5cd5338b + 2], 유효길이 = 힙[ipaki_5cd5338b + 3], 열린파일번호 = 힙[ikintu_Indanga + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Ijambo_SMS(izina_kidahinduka, "send")) {
                    if (!ikintu_agaciro_2ed200e9(힙[ipaki_5cd5338b + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 유효길이; gukora_mu_matsinda_umugerekashakiro++) 통신임시[gukora_mu_matsinda_umugerekashakiro] = 힙[amakurushingiro_ARRAY + 2 + gukora_mu_matsinda_umugerekashakiro];
                    if (ukoresha.kohereza_Urusobemiyoboro(열린파일번호, 힙[힙[ipaki_5cd5338b + 4] + 2], 힙[ipaki_5cd5338b + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int 항목수 = ukoresha.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (항목수 == -11) {
                        int 현재시각 = ukoresha.밀리초();
                        if (힙[ikintu_Indanga + 4] == 0) 힙[ikintu_Indanga + 4] = 현재시각 + 1;
                        if (힙[ikintu_Indanga + 3] > 0 && 현재시각 - (힙[ikintu_Indanga + 4] - 1) >= 힙[ikintu_Indanga + 3]) { 힙[ikintu_Indanga + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(ikintu_Indanga, 2); 넣기(ipaki_5cd5338b, 2); 틀위치[ikadiri_umugerekashakiro] = ikadiri_ibwiriza[ikadiri_umugerekashakiro]; 바꿈요청 = true; return;
                    }
                    힙[ikintu_Indanga + 4] = 0;
                    if (항목수 < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 항목수; gukora_mu_matsinda_umugerekashakiro++) 힙[amakurushingiro_ARRAY + 2 + gukora_mu_matsinda_umugerekashakiro] = (byte)통신임시[gukora_mu_matsinda_umugerekashakiro];
                    힙[ipaki_5cd5338b + 3] = 항목수; 힙[ipaki_5cd5338b + 4] = aderesi_ikintu(통신임시[513]); 힙참조[ipaki_5cd5338b + 4] = 1; 힙[ipaki_5cd5338b + 5] = 통신임시[512];
                }
                return;
            }
        }
        kudakora_agaciro("unsupported java.net method");
    }
    static boolean 흐름대기(int ikintu_Indanga) {
        int 현재시각 = ukoresha.밀리초();
        if (힙[ikintu_Indanga + 5] == 0) 힙[ikintu_Indanga + 5] = 현재시각 + 1;
        if (힙[ikintu_Indanga + 3] > 0 && 현재시각 - (힙[ikintu_Indanga + 5] - 1) >= 힙[ikintu_Indanga + 3]) { 힙[ikintu_Indanga + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        틀위치[ikadiri_umugerekashakiro] = ikadiri_ibwiriza[ikadiri_umugerekashakiro]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int nyirayo, int izina_kidahinduka, int 서술상수, int 명령코드) {
        boolean 수신쪽 = Ijambo_SMS(nyirayo, "java/net/ServerSocket"), Stream = Ijambo_SMS(nyirayo, "java/io/InputStream") || Ijambo_SMS(nyirayo, "java/io/OutputStream");
        if (!Stream && 명령코드 == 183 && Ijambo_SMS(izina_kidahinduka, "<init>")) {
            boolean 빈여부 = Ijambo_SMS(서술상수, "()V"), 이름지정여부 = Ijambo_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Ijambo_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && Ijambo_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { kudakora_agaciro("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), aderesi_Indanga = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, ikintu_Indanga = 빼기(2);
            if (!ikintu_agaciro_2ed200e9(ikintu_Indanga, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !ikintu_agaciro_2ed200e9(aderesi_Indanga, 14)) return;
            int Urusobemiyoboro_aderesi = 이름지정여부 ? 주소해독(aderesi_Indanga) : 주소지정여부 ? 힙[aderesi_Indanga + 2] : 0x7f000001;
            if (IKOSA || 던진객체 != 0) return;
            int 열린파일번호 = ukoresha.Stream_icunga(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? ukoresha.Stream_icunga(1, 열린파일번호, 접속번호) : ukoresha.Guhuza_Stream(열린파일번호, Urusobemiyoboro_aderesi, 접속번호);
            if (처리값 < 0) { ukoresha.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[ikintu_Indanga + 2] = 열린파일번호; 힙[ikintu_Indanga + 4] = 접속번호; 힙[ikintu_Indanga + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!Stream && Ijambo_SMS(izina_kidahinduka, "setSoTimeout") && Ijambo_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), ikintu_Indanga = 빼기(2); if (!ikintu_agaciro_2ed200e9(ikintu_Indanga, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[ikintu_Indanga + 3] = 밀리초값; return; }
        if (!Stream && Ijambo_SMS(izina_kidahinduka, "close") && Ijambo_SMS(서술상수, "()V")) { int ikintu_Indanga = 빼기(2); if (ikintu_agaciro_2ed200e9(ikintu_Indanga, 수신쪽 ? 18 : 17) && 힙[ikintu_Indanga + 2] >= 0) { ukoresha.파일서술자닫기(힙[ikintu_Indanga + 2]); 힙[ikintu_Indanga + 2] = -1; } return; }
        if (!Stream && (Ijambo_SMS(izina_kidahinduka, "getLocalPort") || Ijambo_SMS(izina_kidahinduka, "getPort") || Ijambo_SMS(izina_kidahinduka, "isClosed") || Ijambo_SMS(izina_kidahinduka, "isConnected"))) {
            int ikintu_Indanga = 빼기(2); if (!ikintu_agaciro_2ed200e9(ikintu_Indanga, 수신쪽 ? 18 : 17)) return;
            넣기(Ijambo_SMS(izina_kidahinduka, "isClosed") ? 힙[ikintu_Indanga + 2] < 0 ? 1 : 0 : Ijambo_SMS(izina_kidahinduka, "isConnected") ? 힙[ikintu_Indanga + 6] : Ijambo_SMS(izina_kidahinduka, "getPort") ? 힙[ikintu_Indanga + 4] : 힙[ikintu_Indanga + 2] < 0 ? -1 : ukoresha.Stream_icunga(4, 힙[ikintu_Indanga + 2], 0), 1); return;
        }
        if (수신쪽 && Ijambo_SMS(izina_kidahinduka, "accept") && Ijambo_SMS(서술상수, "()Ljava/net/Socket;")) {
            int ikintu_Indanga = 빼기(2); if (!ikintu_agaciro_2ed200e9(ikintu_Indanga, 18)) return; int 열린파일번호 = ukoresha.Stream_icunga(3, 힙[ikintu_Indanga + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(ikintu_Indanga)) 넣기(ikintu_Indanga, 2); return; }
            힙[ikintu_Indanga + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = kugenera_Ububiko(17, 5); if (IKOSA) { ukoresha.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = ukoresha.Stream_icunga(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !Stream && ((Ijambo_SMS(izina_kidahinduka, "getInputStream") && Ijambo_SMS(서술상수, "()Ljava/io/InputStream;")) || (Ijambo_SMS(izina_kidahinduka, "getOutputStream") && Ijambo_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int ikintu_Indanga = 빼기(2); if (!ikintu_agaciro_2ed200e9(ikintu_Indanga, 17)) return; if (힙[ikintu_Indanga + 2] < 0 || 힙[ikintu_Indanga + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = kugenera_Ububiko(19, 4); if (IKOSA) return; 힙[반환값 + 2] = ikintu_Indanga; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Ijambo_SMS(izina_kidahinduka, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Ijambo_SMS(izina_kidahinduka, "read"), 쓰기여부 = Ijambo_SMS(izina_kidahinduka, "write"), guheza = Ijambo_SMS(서술상수, "([B)I") || Ijambo_SMS(서술상수, "([B)V"), 부분배열여부 = Ijambo_SMS(서술상수, "([BII)I") || Ijambo_SMS(서술상수, "([BII)V");
            int 항목수 = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, amakurushingiro_ARRAY = guheza || 부분배열여부 ? 빼기(2) : 0;
            int amakurushingiro_agaciro = 쓰기여부 && Ijambo_SMS(서술상수, "(I)V") ? 빼기(1) : 0, ikintu_Indanga = 빼기(2);
            if (!ikintu_agaciro_2ed200e9(ikintu_Indanga, 19)) return; int 부모참조 = 힙[ikintu_Indanga + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Ijambo_SMS(izina_kidahinduka, "close") && Ijambo_SMS(서술상수, "()V")) { ukoresha.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Ijambo_SMS(izina_kidahinduka, "flush") && Ijambo_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[ikintu_Indanga + 3] == 0)) { kudakora_agaciro("unsupported stream operation"); return; }
            if (guheza || 부분배열여부) { if (!ikintu_agaciro_2ed200e9(amakurushingiro_ARRAY, 20)) return; if (guheza) 항목수 = 힙[amakurushingiro_ARRAY + 1]; if (시작변위 < 0 || 항목수 < 0 || 시작변위 > 힙[amakurushingiro_ARRAY + 1] - 항목수) { 예외던짐(6, "stream array bounds"); return; } }
            else 항목수 = 1;
            if (항목수 == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[ikintu_Indanga + 4] : 0, 처리값 = 0;
            while (완료수 < 항목수) {
                처리값 = 읽기여부 ? ukoresha.파일한바이트읽기(열린파일번호) : ukoresha.파일한바이트쓰기(열린파일번호, guheza || 부분배열여부 ? 힙[amakurushingiro_ARRAY + 2 + 시작변위 + 완료수] : amakurushingiro_agaciro);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (guheza || 부분배열여부)) 힙[amakurushingiro_ARRAY + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(guheza || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[ikintu_Indanga + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(ikintu_Indanga, 2); if (guheza || 부분배열여부) 넣기(amakurushingiro_ARRAY, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(항목수, 1); } if (쓰기여부 && !(guheza || 부분배열여부)) 넣기(amakurushingiro_agaciro, 1); } return;
            }
            힙[ikintu_Indanga + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : guheza || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        kudakora_agaciro("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int izina_kidahinduka) {
        if (Ijambo_SMS(izina_kidahinduka, "Ikinyarwanda/자체/idirishya")) return 24;
        if (Ijambo_SMS(izina_kidahinduka, "Ikinyarwanda/자체/Akarango")) return 26;
        if (Ijambo_SMS(izina_kidahinduka, "Ikinyarwanda/자체/buto")) return 27;
        if (Ijambo_SMS(izina_kidahinduka, "Ikinyarwanda/자체/SMS_umwanya")) return 28;
        if (Ijambo_SMS(izina_kidahinduka, "Ikinyarwanda/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int izina_kidahinduka) {
        return 한국어화면종(izina_kidahinduka) != 0 || Ijambo_SMS(izina_kidahinduka, "Ikinyarwanda/자체/화면구성요소") || Ijambo_SMS(izina_kidahinduka, "Ikinyarwanda/자체/icyabaye_umurongo_utegererezwaho");
    }
    static int 화면종(int izina_kidahinduka) {
        int 한국어종 = 한국어화면종(izina_kidahinduka); if (한국어종 != 0) return 한국어종;
        if (Ijambo_SMS(izina_kidahinduka, "javax/swing/JFrame")) return 24;
        if (Ijambo_SMS(izina_kidahinduka, "javax/swing/JPanel")) return 25;
        if (Ijambo_SMS(izina_kidahinduka, "javax/swing/JLabel")) return 26;
        if (Ijambo_SMS(izina_kidahinduka, "javax/swing/JButton")) return 27;
        if (Ijambo_SMS(izina_kidahinduka, "javax/swing/JTextField")) return 28;
        if (Ijambo_SMS(izina_kidahinduka, "java/awt/event/ActionEvent")) return 29;
        if (Ijambo_SMS(izina_kidahinduka, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int izina_kidahinduka) {
        return 화면종(izina_kidahinduka) != 0 || Ijambo_SMS(izina_kidahinduka, "java/awt/Component") || Ijambo_SMS(izina_kidahinduka, "java/awt/Container") || Ijambo_SMS(izina_kidahinduka, "javax/swing/JComponent") || Ijambo_SMS(izina_kidahinduka, "javax/swing/AbstractButton") || Ijambo_SMS(izina_kidahinduka, "javax/swing/text/JTextComponent") || Ijambo_SMS(izina_kidahinduka, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int ikintu_Indanga) { if (!객체유효(ikintu_Indanga)) return false; if (힙[ikintu_Indanga] < 24 || 힙[ikintu_Indanga] > 28) { kudakora_agaciro("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int ikintu_Indanga, int SMS_Indanga) {
        if (SMS_Indanga != 0 && !ikintu_agaciro_2ed200e9(SMS_Indanga, 1)) return;
        int 항목수 = SMS_Indanga == 0 ? 0 : 힙[SMS_Indanga + 1]; if (항목수 > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 항목수; gukora_mu_matsinda_umugerekashakiro++) 화면글임시[gukora_mu_matsinda_umugerekashakiro] = 힙[SMS_Indanga + 2 + gukora_mu_matsinda_umugerekashakiro];
        if (ukoresha.화면글(힙[ikintu_Indanga + 2], 화면글임시, 항목수) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[ikintu_Indanga + 3] = SMS_Indanga; 힙참조[ikintu_Indanga + 3] = 1;
    }
    static int 화면문자읽기(int ikintu_Indanga) {
        int konti_agaciro = 힙[ikintu_Indanga + 2], 항목수 = ukoresha.화면연결(8, konti_agaciro, 0, 0, 0, 0), 사용수 = 0;
        if (항목수 < 0) { kudakora_agaciro("GUI text read failed"); return 0; }
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 항목수; gukora_mu_matsinda_umugerekashakiro++) { int 부호값 = ukoresha.화면연결(9, konti_agaciro, gukora_mu_matsinda_umugerekashakiro, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = kugenera_Ububiko(1, 사용수); if (!IKOSA) for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 사용수; gukora_mu_matsinda_umugerekashakiro++) 힙[반환값 + 2 + gukora_mu_matsinda_umugerekashakiro] = 화면글임시[gukora_mu_matsinda_umugerekashakiro]; return 반환값;
    }
    /* Ikinyarwanda 객체를 직접 만들고 intima_agaciro 화면 기능에 연결한다. Swing ikintu_agaciro_2ed200e9/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int nyirayo, int izina_kidahinduka, int 서술상수, int 명령코드) {
        if (Ijambo_SMS(nyirayo, "Ikinyarwanda/자체/icyabaye_umurongo_utegererezwaho")) {
            if (명령코드 == 184 && Ijambo_SMS(izina_kidahinduka, "나중에실행") && Ijambo_SMS(서술상수, "(LIkinyarwanda/자체/실행할일;)V")) {
                int umukoro_igikorwa = 빼기(2); if (!객체유효(umukoro_igikorwa)) return;
                if (나중수 == 8) { kudakora_agaciro("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = umukoro_igikorwa; return;
            }
            if (명령코드 == 184 && Ijambo_SMS(izina_kidahinduka, "사건처리중인가") && Ijambo_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            kudakora_agaciro("지원하지 않는 Ikinyarwanda 화면 일정 호출"); return;
        }
        if (Ijambo_SMS(nyirayo, "Ikinyarwanda/자체/동작알림")) {
            int 알림 = 빼기(2); if (!ikintu_agaciro_2ed200e9(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Ijambo_SMS(izina_kidahinduka, "icyabaye_inkomoko") && Ijambo_SMS(서술상수, "()LIkinyarwanda/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Ijambo_SMS(izina_kidahinduka, "ibwiriza_SMS") && Ijambo_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Ijambo_SMS(izina_kidahinduka, "umugerekashakiro") && Ijambo_SMS(서술상수, "()I")) 넣기(1001, 1);
            else kudakora_agaciro("지원하지 않는 Ikinyarwanda Igikorwa 알림 호출"); return;
        }
        if (명령코드 == 183 && Ijambo_SMS(izina_kidahinduka, "<init>")) {
            int 종류 = 한국어화면종(nyirayo), 받이 = 0, 가로 = 0, 세로 = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Ijambo_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (ukoresha.화면너비() - 폭) / 2; 세로 = (ukoresha.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Ijambo_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Ijambo_SMS(서술상수, "(Ljava/lang/String;IIIILIkinyarwanda/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); 세로 = 빼기(1); 가로 = 빼기(1);
            } else { kudakora_agaciro("지원하지 않는 Ikinyarwanda 화면 생성자"); return; }
            int Umwandiko = 빼기(2), ikintu_agaciro = 빼기(2); if (!화면객체(ikintu_agaciro)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || 세로 < 0 || 폭 > ukoresha.화면너비() - 가로 || 높이 > ukoresha.화면높이() - 세로) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int umugerekashakiro = ukoresha.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (umugerekashakiro < 1 || umugerekashakiro > 32) { kudakora_agaciro("화면 ikintu_agaciro 자리가 가득 찼습니다"); return; }
            힙[ikintu_agaciro + 2] = umugerekashakiro; 화면참조[umugerekashakiro - 1] = ikintu_agaciro;
            힙[ikintu_agaciro + 5] = 가로; 힙[ikintu_agaciro + 6] = 세로; 힙[ikintu_agaciro + 7] = 폭; 힙[ikintu_agaciro + 8] = 높이; 힙[ikintu_agaciro + 10] = 2;
            힙[ikintu_agaciro + 4] = 받이; 힙참조[ikintu_agaciro + 4] = 1; 힙[ikintu_agaciro + 12] = 1;
            ukoresha.화면연결(1, umugerekashakiro, 가로, 세로, 폭, 높이);
            if (종류 == 24) ukoresha.화면연결(7, umugerekashakiro, 2, 0, 0, 0);
            화면문자설정(ikintu_agaciro, Umwandiko); return;
        }
        if (명령코드 != 182) { kudakora_agaciro("잘못된 Ikinyarwanda 화면 호출 Icyo_wifuza"); return; }
        if (Ijambo_SMS(izina_kidahinduka, "kwandika_SMS") && Ijambo_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Umwandiko = 빼기(2), ikintu_agaciro = 빼기(2); if (화면객체(ikintu_agaciro)) 화면문자설정(ikintu_agaciro, Umwandiko); return;
        }
        if (Ijambo_SMS(izina_kidahinduka, "글읽기") && Ijambo_SMS(서술상수, "()Ljava/lang/String;")) {
            int ikintu_agaciro = 빼기(2); if (화면객체(ikintu_agaciro)) 넣기(화면문자읽기(ikintu_agaciro), 2); return;
        }
        if (Ijambo_SMS(izina_kidahinduka, "동작맡기기") && Ijambo_SMS(서술상수, "(LIkinyarwanda/자체/동작받이;)V")) {
            int 받이 = 빼기(2), ikintu_agaciro = 빼기(2);
            if (화면객체(ikintu_agaciro)) { 힙[ikintu_agaciro + 4] = 받이; 힙참조[ikintu_agaciro + 4] = 1; 힙[ikintu_agaciro + 12] = 1; } return;
        }
        if (Ijambo_SMS(izina_kidahinduka, "kongeraho_ikintu") && Ijambo_SMS(서술상수, "(LIkinyarwanda/자체/화면구성요소;)V")) {
            int ishami_agaciro_b642f4b4 = 빼기(2), 부모 = 빼기(2); if (!화면객체(ishami_agaciro_b642f4b4) || !화면객체(부모)) return;
            if (ukoresha.화면연결(2, 힙[부모 + 2], 힙[ishami_agaciro_b642f4b4 + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[ishami_agaciro_b642f4b4 + 11] = 부모; 힙참조[ishami_agaciro_b642f4b4 + 11] = 1; return;
        }
        if (Ijambo_SMS(izina_kidahinduka, "자리정하기") && Ijambo_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), 세로 = 빼기(1), 가로 = 빼기(1), ikintu_agaciro = 빼기(2); if (!화면객체(ikintu_agaciro)) return;
            if (ukoresha.화면연결(1, 힙[ikintu_agaciro + 2], 가로, 세로, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[ikintu_agaciro + 5] = 가로; 힙[ikintu_agaciro + 6] = 세로; 힙[ikintu_agaciro + 7] = 폭; 힙[ikintu_agaciro + 8] = 높이; return;
        }
        if ((Ijambo_SMS(izina_kidahinduka, "kugaragaza_idirishya") || Ijambo_SMS(izina_kidahinduka, "Gufunga")) && Ijambo_SMS(서술상수, "()V")) {
            boolean ukuboneka_agaciro = Ijambo_SMS(izina_kidahinduka, "kugaragaza_idirishya"); int ikintu_agaciro = 빼기(2); if (!화면객체(ikintu_agaciro)) return;
            if (ukoresha.화면연결(ukuboneka_agaciro ? 3 : 4, 힙[ikintu_agaciro + 2], ukuboneka_agaciro ? 1 : 0, 0, 0, 0) < 0) { kudakora_agaciro("화면은 interfacebikorana 명령에서 실행해야 합니다"); return; }
            힙[ikintu_agaciro + 9] = ukuboneka_agaciro ? 1 : 0; return;
        }
        if (Ijambo_SMS(izina_kidahinduka, "보이는가") && Ijambo_SMS(서술상수, "()Z")) { int ikintu_agaciro = 빼기(2); if (화면객체(ikintu_agaciro)) 넣기(힙[ikintu_agaciro + 9], 1); return; }
        kudakora_agaciro("지원하지 않는 Ikinyarwanda 화면 uburyo_agaciro");
    }
    static void 화면호출(int nyirayo, int izina_kidahinduka, int 서술상수, int 명령코드) {
        if (Ijambo_SMS(nyirayo, "javax/swing/SwingUtilities")) {
            if (명령코드 == 184 && Ijambo_SMS(izina_kidahinduka, "invokeLater") && Ijambo_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int ikintu_Indanga = 빼기(2); if (!객체유효(ikintu_Indanga)) return; if (나중수 == 8) { kudakora_agaciro("invokeLater queue full"); return; } 나중실행[나중수++] = ikintu_Indanga; return; }
            if (명령코드 == 184 && Ijambo_SMS(izina_kidahinduka, "isEventDispatchThread") && Ijambo_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            kudakora_agaciro("unsupported SwingUtilities method"); return;
        }
        if (Ijambo_SMS(nyirayo, "java/awt/event/ActionEvent")) {
            int ikintu_Indanga = 빼기(2); if (!ikintu_agaciro_2ed200e9(ikintu_Indanga, 29)) return;
            if (Ijambo_SMS(izina_kidahinduka, "getSource") && Ijambo_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[ikintu_Indanga + 2], 2);
            else if (Ijambo_SMS(izina_kidahinduka, "getActionCommand") && Ijambo_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[ikintu_Indanga + 2]), 2);
            else if (Ijambo_SMS(izina_kidahinduka, "getID") && Ijambo_SMS(서술상수, "()I")) 넣기(1001, 1);
            else kudakora_agaciro("unsupported ActionEvent method"); return;
        }
        if (명령코드 == 183 && Ijambo_SMS(izina_kidahinduka, "<init>")) {
            int 열수 = 0, SMS_Indanga = 0;
            if (Ijambo_SMS(서술상수, "(I)V")) 열수 = 빼기(1);
            else if (Ijambo_SMS(서술상수, "(Ljava/lang/String;I)V")) { 열수 = 빼기(1); SMS_Indanga = 빼기(2); }
            else if (Ijambo_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Indanga = 빼기(2);
            else if (Ijambo_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Ijambo_SMS(서술상수, "()V")) { kudakora_agaciro("unsupported Swing constructor"); return; }
            int ikintu_Indanga = 빼기(2); if (!객체유효(ikintu_Indanga)) return;
            if (힙[ikintu_Indanga] == 30) { kudakora_agaciro("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(ikintu_Indanga) || 열수 < 0) return;
            int konti_agaciro = ukoresha.화면연결(0, 힙[ikintu_Indanga] - 23, 0, 0, 0, 0);
            if (konti_agaciro < 1 || konti_agaciro > 32) { kudakora_agaciro("GUI widget slots exhausted"); return; }
            힙[ikintu_Indanga + 2] = konti_agaciro; 화면참조[konti_agaciro - 1] = ikintu_Indanga; 힙[ikintu_Indanga + 5] = 힙[ikintu_Indanga] == 24 ? 130 : 16; 힙[ikintu_Indanga + 6] = 힙[ikintu_Indanga] == 24 ? 110 : 16;
            힙[ikintu_Indanga + 7] = 힙[ikintu_Indanga] == 24 ? 380 : 220; 힙[ikintu_Indanga + 8] = 힙[ikintu_Indanga] == 24 ? 240 : 28; 힙[ikintu_Indanga + 10] = 1;
            화면문자설정(ikintu_Indanga, SMS_Indanga); return;
        }
        if (Ijambo_SMS(izina_kidahinduka, "setText") || Ijambo_SMS(izina_kidahinduka, "setTitle")) { int SMS_Indanga = 빼기(2), ikintu_Indanga = 빼기(2); if (화면객체(ikintu_Indanga) && Ijambo_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(ikintu_Indanga, SMS_Indanga); return; }
        if (Ijambo_SMS(izina_kidahinduka, "getText") || Ijambo_SMS(izina_kidahinduka, "getTitle")) { int ikintu_Indanga = 빼기(2); if (화면객체(ikintu_Indanga) && Ijambo_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(ikintu_Indanga), 2); return; }
        if (Ijambo_SMS(izina_kidahinduka, "addActionListener") && Ijambo_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), ikintu_Indanga = 빼기(2); if (화면객체(ikintu_Indanga)) { 힙[ikintu_Indanga + 4] = 수신참조; 힙참조[ikintu_Indanga + 4] = 1; } return; }
        if (Ijambo_SMS(izina_kidahinduka, "getContentPane") && Ijambo_SMS(서술상수, "()Ljava/awt/Container;")) { int ikintu_Indanga = 빼기(2); if (화면객체(ikintu_Indanga)) 넣기(ikintu_Indanga, 2); return; }
        if (Ijambo_SMS(izina_kidahinduka, "setLayout") && Ijambo_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Imimerere_Indanga = 빼기(2), ikintu_Indanga = 빼기(2); if (화면객체(ikintu_Indanga) && Imimerere_Indanga != 0) kudakora_agaciro("only absolute layout (null) is supported"); return; }
        if (Ijambo_SMS(izina_kidahinduka, "add") && (Ijambo_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Ijambo_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Imimerere_icyangombwa = Ijambo_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Imimerere_icyangombwa) 빼기(2);
            int ishami_Indanga = 빼기(2), ikintu_Indanga = 빼기(2); if (!화면객체(ishami_Indanga) || !화면객체(ikintu_Indanga)) return;
            if (ukoresha.화면연결(2, 힙[ikintu_Indanga + 2], 힙[ishami_Indanga + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[ishami_Indanga + 11] = ikintu_Indanga; 힙참조[ishami_Indanga + 11] = 1; if (!Imimerere_icyangombwa) 넣기(ishami_Indanga, 2); return;
        }
        if (Ijambo_SMS(izina_kidahinduka, "setBounds") && Ijambo_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), Ihuza_rya_x = 빼기(1), ikintu_Indanga = 빼기(2); if (!화면객체(ikintu_Indanga)) return;
            if (ukoresha.화면연결(1, 힙[ikintu_Indanga + 2], Ihuza_rya_x, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[ikintu_Indanga + 5] = Ihuza_rya_x; 힙[ikintu_Indanga + 6] = 세로좌표; 힙[ikintu_Indanga + 7] = 너비; 힙[ikintu_Indanga + 8] = 높이; return;
        }
        if (Ijambo_SMS(izina_kidahinduka, "setSize") && Ijambo_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), ikintu_Indanga = 빼기(2); if (!화면객체(ikintu_Indanga)) return;
            if (ukoresha.화면연결(1, 힙[ikintu_Indanga + 2], 힙[ikintu_Indanga + 5], 힙[ikintu_Indanga + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[ikintu_Indanga + 7] = 너비; 힙[ikintu_Indanga + 8] = 높이; } return;
        }
        if (Ijambo_SMS(izina_kidahinduka, "setLocationRelativeTo") && Ijambo_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), ikintu_Indanga = 빼기(2); if (!화면객체(ikintu_Indanga)) return; if (상대배치 != 0) { kudakora_agaciro("only screen centering supported"); return; } 힙[ikintu_Indanga + 5] = (ukoresha.화면너비() - 힙[ikintu_Indanga + 7]) / 2; 힙[ikintu_Indanga + 6] = (ukoresha.화면높이() - 힙[ikintu_Indanga + 8]) / 2; ukoresha.화면연결(1, 힙[ikintu_Indanga + 2], 힙[ikintu_Indanga + 5], 힙[ikintu_Indanga + 6], 힙[ikintu_Indanga + 7], 힙[ikintu_Indanga + 8]); return; }
        if (Ijambo_SMS(izina_kidahinduka, "setDefaultCloseOperation") && Ijambo_SMS(서술상수, "(I)V")) { int ingamba = 빼기(1), ikintu_Indanga = 빼기(2); if (화면객체(ikintu_Indanga)) { if (ingamba < 0 || ingamba > 3) 예외던짐(9, "close policy"); else { 힙[ikintu_Indanga + 10] = ingamba; ukoresha.화면연결(7, 힙[ikintu_Indanga + 2], ingamba, 0, 0, 0); } } return; }
        if (Ijambo_SMS(izina_kidahinduka, "setVisible") && Ijambo_SMS(서술상수, "(Z)V")) { int amakurushingiro_agaciro = 빼기(1), ikintu_Indanga = 빼기(2); if (화면객체(ikintu_Indanga)) { int 처리값 = ukoresha.화면연결(3, 힙[ikintu_Indanga + 2], amakurushingiro_agaciro, 0, 0, 0); if (처리값 < 0) kudakora_agaciro("Swing requires a standalone interactive command"); else 힙[ikintu_Indanga + 9] = amakurushingiro_agaciro; } return; }
        if (Ijambo_SMS(izina_kidahinduka, "dispose") && Ijambo_SMS(서술상수, "()V")) { int ikintu_Indanga = 빼기(2); if (화면객체(ikintu_Indanga)) { ukoresha.화면연결(4, 힙[ikintu_Indanga + 2], 0, 0, 0, 0); 힙[ikintu_Indanga + 9] = 0; } return; }
        if (Ijambo_SMS(izina_kidahinduka, "repaint") || Ijambo_SMS(izina_kidahinduka, "validate")) { int ikintu_Indanga = 빼기(2); if (!화면객체(ikintu_Indanga) || !Ijambo_SMS(서술상수, "()V")) return; ukoresha.화면연결(1, 힙[ikintu_Indanga + 2], 힙[ikintu_Indanga + 5], 힙[ikintu_Indanga + 6], 힙[ikintu_Indanga + 7], 힙[ikintu_Indanga + 8]); return; }
        if (Ijambo_SMS(izina_kidahinduka, "isVisible") && Ijambo_SMS(서술상수, "()Z")) { int ikintu_Indanga = 빼기(2); if (화면객체(ikintu_Indanga)) 넣기(힙[ikintu_Indanga + 9], 1); return; }
        kudakora_agaciro("unsupported Swing method (native subset)");
    }
    static void 사건실행(int gusimbuza_igishya_aderesi, int 사건번호, boolean Ikinyarwanda) {
        if (gusimbuza_igishya_aderesi < 1 || 힙[gusimbuza_igishya_aderesi] < 32) { kudakora_agaciro("Java event listener required"); return; }
        int dosiye_umugerekashakiro = izina_uburyo(힙[gusimbuza_igishya_aderesi] - 32, 사건번호 == 0 ? (Ikinyarwanda ? "gukora_umukoro" : "run") : (Ikinyarwanda ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (Ikinyarwanda ? "(LIkinyarwanda/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (dosiye_umugerekashakiro < 0) { kudakora_agaciro("event callback missing"); return; }
        현재가닥 = 0; 가닥수 = 1; ikadiri_umugerekashakiro = 0; mugenaporogaramu_imimerere[0] = 1; ikadiri_Ikirundo[0] = 0; 틀잠금[0] = gutangiza_ikadiri[0] = 0; 바꿈요청 = false;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 128; gukora_mu_matsinda_umugerekashakiro++) { mu_gace_agaciro[gukora_mu_matsinda_umugerekashakiro] = 지역형[gukora_mu_matsinda_umugerekashakiro] = 0; }
        ikadiri_uburyo[0] = dosiye_umugerekashakiro; 틀위치[0] = uburyo_Itangira[dosiye_umugerekashakiro]; mu_gace_agaciro[0] = gusimbuza_igishya_aderesi; 지역형[0] = 2;
        if (사건번호 != 0) { mu_gace_agaciro[1] = 사건번호; 지역형[1] = 2; }
        사건중 = true; gukora_ibwiriza(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!IKOSA) {
            if (나중수 > 0) { int gusimbuza_igishya_aderesi = 나중실행[0], Ikinyarwanda = 나중한국어[0]; for (int gukora_mu_matsinda_umugerekashakiro = 1; gukora_mu_matsinda_umugerekashakiro < 나중수; gukora_mu_matsinda_umugerekashakiro++) { 나중실행[gukora_mu_matsinda_umugerekashakiro - 1] = 나중실행[gukora_mu_matsinda_umugerekashakiro]; 나중한국어[gukora_mu_matsinda_umugerekashakiro - 1] = 나중한국어[gukora_mu_matsinda_umugerekashakiro]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(gusimbuza_igishya_aderesi, 0, Ikinyarwanda != 0); continue; }
            if (ukoresha.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = ukoresha.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { kudakora_agaciro("GUI event I/O failed"); return; }
            int konti_agaciro = 사건번호 & 65535; if (konti_agaciro < 1 || konti_agaciro > 32) continue; int ikintu_Indanga = 화면참조[konti_agaciro - 1]; if (ikintu_Indanga == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[ikintu_Indanga + 10] != 0) 힙[ikintu_Indanga + 9] = 0;
                if (힙[ikintu_Indanga + 10] == 3) for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 32; gukora_mu_matsinda_umugerekashakiro++) if (화면참조[gukora_mu_matsinda_umugerekashakiro] != 0 && 힙[화면참조[gukora_mu_matsinda_umugerekashakiro]] == 24) ukoresha.화면연결(4, gukora_mu_matsinda_umugerekashakiro + 1, 0, 0, 0, 0);
            } else if (힙[ikintu_Indanga + 4] != 0) {
                int NSOMA_Indanga = kugenera_Ububiko(29, 2); if (IKOSA) return; 힙[NSOMA_Indanga + 2] = ikintu_Indanga; 힙[NSOMA_Indanga + 3] = 힙[ikintu_Indanga + 12]; 힙참조[NSOMA_Indanga + 2] = 1; 사건실행(힙[ikintu_Indanga + 4], NSOMA_Indanga, 힙[ikintu_Indanga + 12] != 0);
            }
        }
    }
    public static int ihuriro() {
        if (ukoresha.인수개수() == 1 && 자바도구.같음(ukoresha.인수(0), "-version")) {
            ukoresha.kwandika("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (ukoresha.인수개수() < 1) { ukoresha.kwandika("Usage: java CLASS [ARGS]\n"); return 2; }
        icyinjizwa_icyiciro_Igisobanuro = gufunguka_icyiciro_Igisobanuro(gucumbikira_inyuguti(ukoresha.인수(0))); if (IKOSA || icyinjizwa_icyiciro_Igisobanuro < 0) return 1;
        int icyinjizwa_inota_agaciro = izina_uburyo(icyinjizwa_icyiciro_Igisobanuro, "ihuriro", "()V");
        boolean 한국어진입 = icyinjizwa_inota_agaciro >= 0 && (uburyo_kwinjira[icyinjizwa_inota_agaciro] & 9) == 9;
        if (!한국어진입) icyinjizwa_inota_agaciro = izina_uburyo(icyinjizwa_icyiciro_Igisobanuro, "main", "([Ljava/lang/String;)V");
        if (icyinjizwa_inota_agaciro < 0 || (uburyo_kwinjira[icyinjizwa_inota_agaciro] & 9) != 9) kudakora_agaciro("public static void ihuriro() or main(String[] args) required");
        if (IKOSA) return 1;
        int 인수 = kugenera_Ububiko(3, ukoresha.인수개수() - 1); ARRAY_ikintu[인수] = -1;
        for (int 수 = 1; 수 < ukoresha.인수개수() && !IKOSA; 수++) 힙[인수 + 1 + 수] = gucumbikira_inyuguti(ukoresha.인수(수));
        ikadiri_umugerekashakiro = 0; ikadiri_uburyo[0] = icyinjizwa_inota_agaciro; 틀위치[0] = uburyo_Itangira[icyinjizwa_inota_agaciro]; mu_gace_agaciro[0] = 한국어진입 ? 0 : 인수; 지역형[0] = 한국어진입 ? 0 : 2;
        mugenaporogaramu_imimerere[0] = 1; mugenaporogaramu_ikintu[0] = kugenera_Ububiko(13, 2);
        gukora_ibwiriza(); if (!IKOSA) 화면사건들(); return IKOSA ? 1 : 0;
    }
}
