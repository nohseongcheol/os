// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. anaajaalaa/스택/참조/분기 경계를 실행 중 검사한다. */
public final class 자바가상기계 {
    static int[] anaajaalaa = new int[16 * 16384], 임시파일 = new int[16384], 파일명 = new int[512];
    static int[] waneepiajutu_akanüliajia = new int[8192], 상가 = new int[8192], 상나 = new int[8192], 문자열참조 = new int[8192];
    static int[] 함수명 = new int[512], 함수형 = new int[512], 함수권한 = new int[512], 함수주인 = new int[512];
    static int[] 함수시작 = new int[512], 함수끝 = new int[512], 함수스택 = new int[512], 함수지역 = new int[512];
    static int[] 함수인수수 = new int[512], 함수인수형 = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] 지역값 = new int[16384], 지역형 = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] 틀함수 = new int[128], 틀위치 = new int[128], 틀스택 = new int[128], otpünaa_aluwataaya = new int[128], anaajaa_otpünaa = new int[128];
    static int[] 종이름 = new int[16], 종크기 = new int[16], 종부모 = new int[16], 종상태 = new int[16], 종칸수 = new int[16], 종초기화 = new int[16];
    static int[] akotchijuushi_po_upünawaa = new int[16 * 16], 종접면수 = new int[16];
    static int[] 칸이름 = new int[512], 칸형 = new int[512], 칸주인 = new int[512], 칸권한 = new int[512], 칸위치 = new int[512], 칸값 = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], matüriisü_apüshii = new int[32768], 정수저장 = new int[256];
    static int 크기, 읽기위치, 함수수, 클래스명, otpünaa_ee_iyatialujuna = -1, 힙끝 = 1, 반환형;
    static int 종수, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, 표시수, 수거횟수;
    static int 현재가닥, 가닥수 = 1, 시작종;
    static int[] akumajia_ipa_otpünaa = new int[4], akumajia_ipa_jamakua_iparülein = new int[4], 가닥객체 = new int[4], 가닥대상 = new int[4], 가닥대기 = new int[4];
    static boolean ajachitia, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], akotchijuushi_akumajia_ipa = new int[16];

    static void ajachitia_ajutuu(String 말) {
        if (ajachitia) return;
        int 분류코드 = 0;
        if (자바도구.같음(말, "ArithmeticException: / by zero")) 분류코드 = 4;
        if (자바도구.같음(말, "NullPointerException") || 자바도구.같음(말, "null or invalid array")) 분류코드 = 5;
        if (자바도구.같음(말, "ArrayIndexOutOfBoundsException")) 분류코드 = 7;
        if (자바도구.같음(말, "StringIndexOutOfBoundsException")) 분류코드 = 8;
        if (자바도구.같음(말, "NumberFormatException")) 분류코드 = 10;
        if (자바도구.같음(말, "FileNotFoundException: file open failed")) 분류코드 = 12;
        if (자바도구.같음(말, "IOException: stream closed") || 자바도구.같음(말, "IOException: read failed") || 자바도구.같음(말, "IOException: write failed")) 분류코드 = 11;
        if (자바도구.같음(말, "ClassCastException")) 분류코드 = 14;
        if (자바도구.같음(말, "NegativeArraySizeException")) 분류코드 = 15;
        if (분류코드 != 0 && otpünaa_ee_iyatialujuna >= 0) { 예외던짐(분류코드, 말); return; }
        ka_yataayakalü.ashajaa("JVM error: "); ka_yataayakalü.ashajaa(말); ka_yataayakalü.ashajaa_jeerü_ajutuu(10); ajachitia = true;
    }
    static boolean külipü_ayaakuaapijana(int 시작, int akaliaa_ajutuu) {
        if (시작 < 0 || 시작 >= anaajaalaa.length || akaliaa_ajutuu < 0) return false;
        int 종 = 시작 / 16384;
        return 시작 % 16384 <= 종크기[종] && akaliaa_ajutuu <= 종크기[종] - 시작 % 16384;
    }
    static int waai_ajutuu() {
        if (!külipü_ayaakuaapijana(읽기위치, 1)) { ajachitia_ajutuu("truncated class file"); return 0; }
        return anaajaalaa[읽기위치++];
    }
    static int 짧은수() { return waai_ajutuu() << 8 | waai_ajutuu(); }
    static int waneepiasü() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int akaliaa_ajutuu) { if (!külipü_ayaakuaapijana(읽기위치, akaliaa_ajutuu)) ajachitia_ajutuu("invalid attribute size"); else 읽기위치 += akaliaa_ajutuu; }
    static boolean cheeke_waneepiajutu(int 수, int 종류) {
        if (수 <= 0 || 수 >= waneepiajutu_akanüliajia.length || waneepiajutu_akanüliajia[수] != 종류) { ajachitia_ajutuu("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int 시작, int akaliaa_ajutuu, String 말) {
        if (!külipü_ayaakuaapijana(시작, akaliaa_ajutuu)) return false;
        int 읽는자리 = 시작, 끝 = 시작 + akaliaa_ajutuu;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 말.length(); eitawaakualü_ee_iyatialujuna++) {
            int 문자값 = 말.charAt(eitawaakualü_ee_iyatialujuna);
            if (문자값 > 0 && 문자값 < 128) { if (읽는자리 >= 끝 || anaajaalaa[읽는자리++] != 문자값) return false; }
            else if (문자값 < 2048) {
                if (읽는자리 + 2 > 끝 || anaajaalaa[읽는자리++] != (192 | (문자값 >> 6)) || anaajaalaa[읽는자리++] != (128 | (문자값 & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || anaajaalaa[읽는자리++] != (224 | (문자값 >> 12)) || anaajaalaa[읽는자리++] != (128 | ((문자값 >> 6) & 63)) || anaajaalaa[읽는자리++] != (128 | (문자값 & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean 말(int waneepiajutu_ajutuu, String 말) { return cheeke_waneepiajutu(waneepiajutu_ajutuu, 1) && 구간(상가[waneepiajutu_ajutuu], 상나[waneepiajutu_ajutuu], 말); }
    static boolean 같은말(int 가, int 나) {
        if (!cheeke_waneepiajutu(가, 1) || !cheeke_waneepiajutu(나, 1) || 상나[가] != 상나[나]) return false;
        for (int 수 = 0; 수 < 상나[가]; 수++) if (anaajaalaa[상가[가] + 수] != anaajaalaa[상가[나] + 수]) return false;
        return true;
    }
    static int 클래스문자(int 수) { return cheeke_waneepiajutu(수, 7) && cheeke_waneepiajutu(상가[수], 1) ? 상가[수] : 0; }
    static int 참조이름(int 수) { return cheeke_waneepiajutu(수, 12) && cheeke_waneepiajutu(상가[수], 1) ? 상가[수] : 0; }
    static int 참조형식(int 수) { return cheeke_waneepiajutu(수, 12) && cheeke_waneepiajutu(상나[수], 1) ? 상나[수] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (읽기위치 >= 끝) { ajachitia_ajutuu("invalid descriptor"); return 0; }
        int ajutuu = waai_ajutuu();
        if (ajutuu == 'V' && 빈형) return 0;
        if (ajutuu == 'I' || ajutuu == 'B' || ajutuu == 'C' || ajutuu == 'S' || ajutuu == 'Z') return 1;
        if (ajutuu == '[') { 서술형(끝, false); return 2; }
        if (ajutuu == 'L') {
            int 시작 = 읽기위치;
            while (읽기위치 < 끝 && anaajaalaa[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == 시작) ajachitia_ajutuu("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        ajachitia_ajutuu("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int 함수) {
        int 이전 = 읽기위치, 수 = 함수형[함수];
        if (!cheeke_waneepiajutu(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + 상나[수];
        if (waai_ajutuu() != '(') ajachitia_ajutuu("invalid method descriptor");
        int 개수 = 0;
        while (!ajachitia && 읽기위치 < 끝 && anaajaalaa[읽기위치] != ')') {
            if (개수 == 16) { ajachitia_ajutuu("too many method arguments"); break; }
            함수인수형[함수 * 16 + 개수++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || waai_ajutuu() != ')') ajachitia_ajutuu("invalid method descriptor");
        함수반환[함수] = 서술형(끝, true); 함수인수수[함수] = 개수;
        if (읽기위치 != 끝) ajachitia_ajutuu("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int ajutuu = 짧은수(); return ajutuu == 0 ? 0 : 현재읽는종 * 512 + ajutuu; }
    static int 명상수() { return 함수주인[틀함수[otpünaa_ee_iyatialujuna]] * 512 + 명짧(); }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !ajachitia; 수++) { cheeke_waneepiajutu(상번호(), 1); 건너(waneepiasü()); }
    }
    static int aluwataaya_akaliaa(int ajutuu) {
        if (ajutuu == 16 || ajutuu == 18 || ajutuu == 21 || ajutuu == 25 || ajutuu == 54 || ajutuu == 58 || ajutuu == 188) return 2;
        if (ajutuu == 17 || ajutuu == 19 || ajutuu == 132 || ajutuu >= 153 && ajutuu <= 167
            || ajutuu >= 178 && ajutuu <= 184 || ajutuu == 187 || ajutuu == 189 || ajutuu == 192 || ajutuu == 193 || ajutuu == 198 || ajutuu == 199) return 3;
        if (ajutuu == 185 || ajutuu == 200) return 5;
        if (ajutuu >= 0 && ajutuu <= 8 || ajutuu >= 26 && ajutuu <= 29 || ajutuu >= 42 && ajutuu <= 46 || ajutuu >= 50 && ajutuu <= 53
            || ajutuu >= 59 && ajutuu <= 62 || ajutuu >= 75 && ajutuu <= 79 || ajutuu >= 83 && ajutuu <= 95
            || ajutuu == 96 || ajutuu == 100 || ajutuu == 104 || ajutuu == 108 || ajutuu == 112 || ajutuu == 116
            || ajutuu == 120 || ajutuu == 122 || ajutuu == 124 || ajutuu == 126 || ajutuu == 128 || ajutuu == 130
            || ajutuu >= 145 && ajutuu <= 147 || ajutuu == 172 || ajutuu == 176 || ajutuu == 177 || ajutuu == 190 || ajutuu == 191
            || ajutuu == 194 || ajutuu == 195) return 1;
        return 0;
    }
    static int 위치정수(int 읽는자리) {
        if (!külipü_ayaakuaapijana(읽는자리, 4)) { ajachitia_ajutuu("truncated bytecode operand"); return 0; }
        return anaajaalaa[읽는자리] << 24 | anaajaalaa[읽는자리 + 1] << 16 | anaajaalaa[읽는자리 + 2] << 8 | anaajaalaa[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int 시작, int 끝) {
        int ajutuu = anaajaalaa[읽는자리], akaliaa_ajutuu = aluwataaya_akaliaa(ajutuu);
        if (ajutuu == 170 || ajutuu == 171) {
            int 기준자리 = 읽는자리 + 1;
            while ((기준자리 - 시작) % 4 != 0) 기준자리++;
            if (끝 - 기준자리 < (ajutuu == 170 ? 12 : 8)) return 0;
            int 항목수 = ajutuu == 170 ? 위치정수(기준자리 + 8) - 위치정수(기준자리 + 4) + 1 : 위치정수(기준자리 + 4);
            if (항목수 < 0 || 항목수 > 2048) return 0;
            akaliaa_ajutuu = 기준자리 - 읽는자리 + (ajutuu == 170 ? 12 + 4 * 항목수 : 8 + 8 * 항목수);
        }
        if (ajutuu == 196 && 읽는자리 + 1 < 끝) {
            int 단어값 = anaajaalaa[읽는자리 + 1]; akaliaa_ajutuu = 단어값 == 132 ? 6 : (단어값 == 21 || 단어값 == 25 || 단어값 == 54 || 단어값 == 58) ? 4 : 0;
        }
        return akaliaa_ajutuu > 0 && akaliaa_ajutuu <= 끝 - 읽는자리 ? akaliaa_ajutuu : 0;
    }
    static void cheeke_jalamüinjatü_ajutuu(int jalamüinjatü_ajutuu, int 함수) {
        if (jalamüinjatü_ajutuu < 함수시작[함수] || jalamüinjatü_ajutuu >= 함수끝[함수] || 경계[jalamüinjatü_ajutuu] != 함수 + 1) ajachitia_ajutuu("invalid branch target");
    }
    static void 클래스읽기(int 종) {
        현재읽는종 = 종; 읽기위치 = 종 * 16384; 크기 = 읽기위치 + 종크기[종];
        if (waneepiasü() != 0xcafebabe) { ajachitia_ajutuu("not a class file"); return; }
        int 부판 = 짧은수(), 판 = 짧은수();
        if (판 < 45 || 판 > 52 || 부판 != 0) { ajachitia_ajutuu("supported class versions: 45..52, minor 0"); return; }
        int 상수수 = 짧은수(), 기준자리 = 종 * 512;
        if (상수수 < 1 || 상수수 > 512) { ajachitia_ajutuu("constant pool limit (511)"); return; }
        for (int 항목수 = 1; 항목수 < 상수수 && !ajachitia; 항목수++) {
            int 수 = 기준자리 + 항목수, 종류 = waai_ajutuu(); waneepiajutu_akanüliajia[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = waneepiasü();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); 상나[수] = 상번호(); }
            else ajachitia_ajutuu("unsupported constant type");
        }
        int 권한 = 짧은수();
        if ((권한 & (0x2000 | 0x4000)) != 0) ajachitia_ajutuu("annotation/enum class unsupported");
        종이름[종] = 클래스문자(상번호());
        종부모[종] = 클래스문자(상번호());
        int 접면수 = 짧은수(); if (접면수 > 16) { ajachitia_ajutuu("interface count limit"); return; }
        종접면수[종] = 접면수;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 접면수; eitawaakualü_ee_iyatialujuna++) akotchijuushi_po_upünawaa[종 * 16 + eitawaakualü_ee_iyatialujuna] = 클래스문자(상번호());
        int 필드수 = 짧은수();
        if (필드수 > 512 - 칸수) { ajachitia_ajutuu("field count limit (512)"); return; }
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 필드수 && !ajachitia; eitawaakualü_ee_iyatialujuna++) {
            int anaajaalaa_ee_iyatialujuna = 칸수++; 칸주인[anaajaalaa_ee_iyatialujuna] = 종; 칸권한[anaajaalaa_ee_iyatialujuna] = 짧은수(); 칸이름[anaajaalaa_ee_iyatialujuna] = 상번호(); 칸형[anaajaalaa_ee_iyatialujuna] = 상번호();
            cheeke_waneepiajutu(칸이름[anaajaalaa_ee_iyatialujuna], 1); cheeke_waneepiajutu(칸형[anaajaalaa_ee_iyatialujuna], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[칸형[anaajaalaa_ee_iyatialujuna]]; int 분류코드 = 서술형(읽기위치 + 상나[칸형[anaajaalaa_ee_iyatialujuna]], false); 읽기위치 = 보존값;
            if ((칸권한[anaajaalaa_ee_iyatialujuna] & 8) == 0) 칸위치[anaajaalaa_ee_iyatialujuna] = 종칸수[종]++;
            int anaajaalaakua_ipa_atijaaya = 짧은수();
            for (int 안쪽자리 = 0; 안쪽자리 < anaajaalaakua_ipa_atijaaya && !ajachitia; 안쪽자리++) {
                int 이름상수 = 상번호(), 유효길이 = waneepiasü();
                if (말(이름상수, "ConstantValue") && 유효길이 == 2) {
                    int atijaaya_ajutuu = 상번호();
                    if (분류코드 == 1 && cheeke_waneepiajutu(atijaaya_ajutuu, 3)) 칸값[anaajaalaa_ee_iyatialujuna] = 상가[atijaaya_ajutuu];
                    else if (분류코드 == 2 && cheeke_waneepiajutu(atijaaya_ajutuu, 8)) 칸값[anaajaalaa_ee_iyatialujuna] = 상문자(상가[atijaaya_ajutuu]);
                } else 건너(유효길이);
            }
        }
        int 개수 = 짧은수();
        if (개수 > 512 - 함수수) { ajachitia_ajutuu("method count limit (512)"); return; }
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 개수 && !ajachitia; eitawaakualü_ee_iyatialujuna++) {
            int 수 = 함수수++; 함수주인[수] = 종;
            함수권한[수] = 짧은수(); 함수명[수] = 상번호(); 함수형[수] = 상번호();
            cheeke_waneepiajutu(함수명[수], 1); 서술읽기(수);
            if ((함수권한[수] & 8) == 0) {
                if (함수인수수[수] == 16) { ajachitia_ajutuu("too many instance method arguments"); return; }
                for (int 비교자리 = 함수인수수[수]; 비교자리 > 0; 비교자리--) 함수인수형[수 * 16 + 비교자리] = 함수인수형[수 * 16 + 비교자리 - 1];
                함수인수형[수 * 16] = 2; 함수인수수[수]++;
            }
            if ((함수권한[수] & 0x100) != 0) ajachitia_ajutuu("user native method unsupported");
            if (말(함수명[수], "<clinit>")) 종초기화[종] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (함수주인[앞] == 종 && 같은말(함수명[앞], 함수명[수]) && 같은말(함수형[앞], 함수형[수])) ajachitia_ajutuu("duplicate method");
            int 속성수 = 짧은수();
            for (int anaajaalaakua_ipa_ajutuu = 0; anaajaalaakua_ipa_ajutuu < 속성수 && !ajachitia; anaajaalaakua_ipa_ajutuu++) {
                int 이름 = 상번호(), akaliaa_ajutuu = waneepiasü(), 시작 = 읽기위치;
                if (!külipü_ayaakuaapijana(시작, akaliaa_ajutuu)) { ajachitia_ajutuu("truncated method attribute"); break; }
                if (말(이름, "Code")) {
                    if (함수시작[수] != 0) ajachitia_ajutuu("duplicate Code attribute");
                    함수스택[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = waneepiasü();
                    if (함수스택[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) ajachitia_ajutuu("method memory limits exceeded");
                    함수시작[수] = 읽기위치; 건너(코드길이); 함수끝[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { ajachitia_ajutuu("exception table limit"); return; }
                    for (int 안쪽자리 = 0; 안쪽자리 < 잡는수; 안쪽자리++) {
                        int 오류참조 = 잡기수++; 잡기함수[오류참조] = 수;
                        잡기시작[오류참조] = 함수시작[수] + 짧은수(); 잡기끝[오류참조] = 함수시작[수] + 짧은수();
                        잡기위치[오류참조] = 함수시작[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[오류참조] = 부호값 == 0 ? 0 : 클래스문자(부호값);
                    }
                    속성건너();
                    if (읽기위치 != 시작 + akaliaa_ajutuu) ajachitia_ajutuu("Code attribute size mismatch");
                } else 건너(akaliaa_ajutuu);
            }
            if ((함수권한[수] & 0x400) != 0) continue;
            if (함수시작[수] == 0) ajachitia_ajutuu("missing Code attribute");
            int 칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !ajachitia) {
                int akaliaa_ajutuu = 길이읽기(칸, 함수시작[수], 함수끝[수]);
                if (akaliaa_ajutuu == 0) { ajachitia_ajutuu("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += akaliaa_ajutuu;
            }
            칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !ajachitia) {
                int ajutuu = anaajaalaa[칸];
                if (ajutuu >= 153 && ajutuu <= 167 || ajutuu == 198 || ajutuu == 199) cheeke_jalamüinjatü_ajutuu(칸 + (short)(anaajaalaa[칸 + 1] << 8 | anaajaalaa[칸 + 2]), 수);
                if (ajutuu == 200) cheeke_jalamüinjatü_ajutuu(칸 + 위치정수(칸 + 1), 수);
                if (ajutuu == 170 || ajutuu == 171) {
                    int 읽는자리 = 칸 + 1; while ((읽는자리 - 함수시작[수]) % 4 != 0) 읽는자리++;
                    cheeke_jalamüinjatü_ajutuu(칸 + 위치정수(읽는자리), 수);
                    int 항목수 = ajutuu == 170 ? 위치정수(읽는자리 + 8) - 위치정수(읽는자리 + 4) + 1 : 위치정수(읽는자리 + 4);
                    읽는자리 += ajutuu == 170 ? 12 : 8;
                    for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) cheeke_jalamüinjatü_ajutuu(칸 + 위치정수(읽는자리 + 안쪽자리 * (ajutuu == 170 ? 4 : 8) + (ajutuu == 170 ? 0 : 4)), 수);
                }
                칸 += 길이읽기(칸, 함수시작[수], 함수끝[수]);
            }
            for (int 안쪽자리 = 0; 안쪽자리 < 잡기수; 안쪽자리++) if (잡기함수[안쪽자리] == 수) {
                cheeke_jalamüinjatü_ajutuu(잡기시작[안쪽자리], 수); cheeke_jalamüinjatü_ajutuu(잡기위치[안쪽자리], 수);
                if (잡기끝[안쪽자리] != 함수끝[수]) cheeke_jalamüinjatü_ajutuu(잡기끝[안쪽자리], 수);
                if (잡기시작[안쪽자리] >= 잡기끝[안쪽자리]) ajachitia_ajutuu("invalid exception range");
            }
        }
        if (!ajachitia) 속성건너();
        if (읽기위치 != 크기) ajachitia_ajutuu("extra class file data");
    }
    static int 할당(int 종류, int akaliaa_ajutuu) { return 새기억(종류, akaliaa_ajutuu); }
    static boolean 객체(int 참조, int 종류) {
        if (!객체유효(참조)) return false;
        if (힙[참조] != 종류) { ajachitia_ajutuu("object type mismatch"); return false; }
        return true;
    }
    static int 상문자(int ee_iyatialujuna) {
        if (!cheeke_waneepiajutu(ee_iyatialujuna, 1)) return 0;
        if (문자열참조[ee_iyatialujuna] != 0) return 문자열참조[ee_iyatialujuna];
        int 참조 = 할당(1, 상나[ee_iyatialujuna]); if (ajachitia) return 0;
        int 끝 = 상가[ee_iyatialujuna] + 상나[ee_iyatialujuna], 수 = 상가[ee_iyatialujuna], akaliaa_ajutuu = 0;
        while (수 < 끝 && !ajachitia) {
            int ajutuu = anaajaalaa[수++];
            if (ajutuu == 0) ajachitia_ajutuu("invalid modified UTF-8");
            else if (ajutuu >= 192 && ajutuu <= 223 && 수 < 끝) {
                int 다음 = anaajaalaa[수++];
                if ((다음 & 192) != 128) ajachitia_ajutuu("invalid modified UTF-8");
                ajutuu = (ajutuu & 31) << 6 | 다음 & 63;
                if (ajutuu != 0 && ajutuu < 128) ajachitia_ajutuu("overlong modified UTF-8");
            } else if (ajutuu >= 224 && ajutuu <= 239 && 수 + 1 < 끝) {
                int 가 = anaajaalaa[수++], 나 = anaajaalaa[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) ajachitia_ajutuu("invalid modified UTF-8");
                ajutuu = (ajutuu & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (ajutuu < 2048) ajachitia_ajutuu("overlong modified UTF-8");
            } else if (ajutuu >= 128) ajachitia_ajutuu("invalid modified UTF-8");
            힙[참조 + 2 + akaliaa_ajutuu++] = ajutuu;
        }
        힙[참조 + 1] = akaliaa_ajutuu; 문자열참조[ee_iyatialujuna] = 참조; return 참조;
    }
    static int epiajatü_jeerü(String ajutuu) {
        int 참조 = 할당(1, ajutuu.length()); if (ajachitia) return 0;
        for (int 수 = 0; 수 < ajutuu.length(); 수++) 힙[참조 + 2 + 수] = ajutuu.charAt(수);
        return 참조;
    }
    static void 글쓰기(int 참조) {
        if (참조 == 0) { ka_yataayakalü.ashajaa("null"); return; }
        if (!객체(참조, 1)) return;
        for (int 수 = 0; 수 < 힙[참조 + 1]; 수++) ka_yataayakalü.ashajaa_jeerü_ajutuu(힙[참조 + 2 + 수]);
    }
    static int 수문자(int ajutuu) {
        int 참조 = 할당(1, 11); if (ajachitia) return 0;
        int akaliaa_ajutuu = 0;
        if (ajutuu < 0) 힙[참조 + 2 + akaliaa_ajutuu++] = '-'; else ajutuu = -ajutuu;
        int 자리 = 1000000000; boolean 시작 = false;
        while (자리 != 0) {
            int 수 = -(ajutuu / 자리);
            if (수 != 0 || 시작 || 자리 == 1) { 힙[참조 + 2 + akaliaa_ajutuu++] = '0' + 수; 시작 = true; }
            ajutuu %= 자리; 자리 /= 10;
        }
        힙[참조 + 1] = akaliaa_ajutuu; return 참조;
    }
    static int 정수해독(int 참조) {
        if (!객체(참조, 1)) return 0;
        int akaliaa_ajutuu = 힙[참조 + 1], 수 = 0, ajutuu = 0; boolean 음수 = false;
        if (akaliaa_ajutuu > 0 && (힙[참조 + 2] == '-' || 힙[참조 + 2] == '+')) { 음수 = 힙[참조 + 2] == '-'; 수++; }
        if (수 == akaliaa_ajutuu) ajachitia_ajutuu("NumberFormatException");
        for (; 수 < akaliaa_ajutuu && !ajachitia; 수++) {
            int 숫자 = 힙[참조 + 2 + 수] - '0';
            if (숫자 < 0 || 숫자 > 9 || ajutuu < -214748364 || ajutuu == -214748364 && 숫자 > (음수 ? 8 : 7)) ajachitia_ajutuu("NumberFormatException");
            ajutuu = ajutuu * 10 - 숫자;
        }
        return 음수 ? ajutuu : -ajutuu;
    }
    static void 넣기(int ajutuu, int 형) {
        if (ajachitia) return;
        if (otpünaa_ee_iyatialujuna < 0 || 틀스택[otpünaa_ee_iyatialujuna] >= 함수스택[틀함수[otpünaa_ee_iyatialujuna]]) { ajachitia_ajutuu("operand stack overflow"); return; }
        int 칸 = otpünaa_ee_iyatialujuna * 128 + 틀스택[otpünaa_ee_iyatialujuna]++; 스택값[칸] = ajutuu; 스택형[칸] = 형;
    }
    static int 빼기(int 형) {
        if (ajachitia) return 0;
        if (otpünaa_ee_iyatialujuna < 0 || 틀스택[otpünaa_ee_iyatialujuna] < 1) { ajachitia_ajutuu("operand stack underflow"); return 0; }
        int 칸 = otpünaa_ee_iyatialujuna * 128 + --틀스택[otpünaa_ee_iyatialujuna]; 반환형 = 스택형[칸];
        if (형 != 0 && 반환형 != 형) ajachitia_ajutuu("operand type mismatch");
        if (반환형 == 2) aa_inmajaa_ajutuu(스택값[칸]);
        return 스택값[칸];
    }
    static void 지역읽기(int ee_iyatialujuna, int 형) {
        if (ee_iyatialujuna >= 함수지역[틀함수[otpünaa_ee_iyatialujuna]] || ee_iyatialujuna < 0 || 지역형[otpünaa_ee_iyatialujuna * 128 + ee_iyatialujuna] != 형) { ajachitia_ajutuu("invalid or uninitialized local"); return; }
        넣기(지역값[otpünaa_ee_iyatialujuna * 128 + ee_iyatialujuna], 형);
    }
    static void 지역쓰기(int ee_iyatialujuna, int 형) {
        if (ee_iyatialujuna >= 함수지역[틀함수[otpünaa_ee_iyatialujuna]] || ee_iyatialujuna < 0) { ajachitia_ajutuu("local index out of range"); return; }
        int ajutuu = 빼기(형); 지역값[otpünaa_ee_iyatialujuna * 128 + ee_iyatialujuna] = ajutuu; 지역형[otpünaa_ee_iyatialujuna * 128 + ee_iyatialujuna] = 형;
    }
    static int 명바() {
        int 위치 = 틀위치[otpünaa_ee_iyatialujuna];
        if (위치 < 함수시작[틀함수[otpünaa_ee_iyatialujuna]] || 위치 >= 함수끝[틀함수[otpünaa_ee_iyatialujuna]]) { ajachitia_ajutuu("instruction pointer out of range"); return 0; }
        틀위치[otpünaa_ee_iyatialujuna]++; return anaajaalaa[위치];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void 이동(int 위치) {
        int 함수 = 틀함수[otpünaa_ee_iyatialujuna];
        if (위치 < 함수시작[함수] || 위치 >= 함수끝[함수] || 경계[위치] != 함수 + 1) ajachitia_ajutuu("invalid branch target");
        else 틀위치[otpünaa_ee_iyatialujuna] = 위치;
    }
    static void 호출(int 함수) {
        if (otpünaa_ee_iyatialujuna % 32 == 31) { ajachitia_ajutuu("call stack limit (32)"); return; }
        int 다음 = otpünaa_ee_iyatialujuna + 1;
        for (int 수 = 0; 수 < 128; 수++) 지역형[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[함수] - 1; 수 >= 0; 수--) {
            지역값[다음 * 128 + 수] = 빼기(함수인수형[함수 * 16 + 수]); 지역형[다음 * 128 + 수] = 함수인수형[함수 * 16 + 수];
        }
        if (ajachitia) return;
        otpünaa_ee_iyatialujuna = 다음; anaajaa_otpünaa[otpünaa_ee_iyatialujuna] = 0; 틀함수[otpünaa_ee_iyatialujuna] = 함수; 틀위치[otpünaa_ee_iyatialujuna] = 함수시작[함수]; 틀스택[otpünaa_ee_iyatialujuna] = 0;
    }
    static void 반환(int 형) {
        if (형 != 함수반환[틀함수[otpünaa_ee_iyatialujuna]]) { ajachitia_ajutuu("return type mismatch"); return; }
        int ajutuu = 형 == 0 ? 0 : 빼기(형);
        if (anaajaa_otpünaa[otpünaa_ee_iyatialujuna] != 0) 종상태[anaajaa_otpünaa[otpünaa_ee_iyatialujuna] - 1] = 2;
        if (틀잠금[otpünaa_ee_iyatialujuna] != 0) { 잠금풀기(틀잠금[otpünaa_ee_iyatialujuna]); 틀잠금[otpünaa_ee_iyatialujuna] = 0; }
        otpünaa_ee_iyatialujuna--; if (otpünaa_ee_iyatialujuna >= 현재가닥 * 32 && 형 != 0) 넣기(ajutuu, 형);
    }
    static int[] 흐름파일이름 = new int[64];
    static void anaajaalaa_palantüsü_ounekaa(int 소유, int 이름, int akua_ipaa_ajutuu, int aluwataaya) {
        boolean 출력 = 말(소유, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (aluwataaya == 183 && 말(이름, "<init>")) {
            boolean 이어 = false;
            if (출력 && 말(akua_ipaa_ajutuu, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!말(akua_ipaa_ajutuu, "(Ljava/lang/String;)V")) { ajachitia_ajutuu("unsupported file stream constructor"); return; }
            int 파일이름 = 빼기(2), palantüsü_ajutuu = 빼기(2);
            if (!객체(파일이름, 1) || !객체(palantüsü_ajutuu, 종류) || ajachitia) return;
            if (힙[palantüsü_ajutuu + 3] != 0) { ajachitia_ajutuu("file stream already initialized"); return; }
            int akaliaa_ajutuu = 힙[파일이름 + 1];
            if (akaliaa_ajutuu < 1 || akaliaa_ajutuu > 63) { ajachitia_ajutuu("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < akaliaa_ajutuu; 칸++) {
                int ajutuu = 힙[파일이름 + 2 + 칸];
                if (ajutuu < 1) { ajachitia_ajutuu("invalid file stream path"); return; }
                흐름파일이름[칸] = ajutuu;
            }
            흐름파일이름[akaliaa_ajutuu] = 0;
            int 서술자 = ka_yataayakalü.파일서술자열기(흐름파일이름, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { ajachitia_ajutuu("FileNotFoundException: file open failed"); return; }
            힙[palantüsü_ajutuu + 2] = 서술자; 힙[palantüsü_ajutuu + 3] = 1;
            return;
        }
        if (aluwataaya != 182) { ajachitia_ajutuu("invalid file stream invocation"); return; }
        if ((출력 && 말(이름, "write") || !출력 && 말(이름, "read"))
            && (말(akua_ipaa_ajutuu, 출력 ? "([B)V" : "([B)I") || 말(akua_ipaa_ajutuu, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean külipü_ayaakuaapijana_ajutuu = 말(akua_ipaa_ajutuu, 출력 ? "([BII)V" : "([BII)I");
            int 항목수 = külipü_ayaakuaapijana_ajutuu ? 빼기(1) : 0, 시작점 = külipü_ayaakuaapijana_ajutuu ? 빼기(1) : 0, atijaaya_matüriisü = 빼기(2), 객체참조 = 빼기(2);
            if (!객체(atijaaya_matüriisü, 20) || !객체(객체참조, 종류)) return;
            if (!külipü_ayaakuaapijana_ajutuu) 항목수 = 힙[atijaaya_matüriisü + 1];
            if (시작점 < 0 || 항목수 < 0 || 시작점 > 힙[atijaaya_matüriisü + 1] - 항목수) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[객체참조 + 3] == 0 || 힙[객체참조 + 2] < 0) { ajachitia_ajutuu("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < 항목수 && !ajachitia) {
                int 반환값 = 출력 ? ka_yataayakalü.파일한바이트쓰기(힙[객체참조 + 2], 힙[atijaaya_matüriisü + 2 + 시작점 + 완료수]) : ka_yataayakalü.파일한바이트읽기(힙[객체참조 + 2]);
                if (반환값 < 0) { ajachitia_ajutuu(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[atijaaya_matüriisü + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(항목수 != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && 말(이름, "flush") && 말(akua_ipaa_ajutuu, "()V")) { int 객체참조 = 빼기(2); if (객체(객체참조, 종류) && 힙[객체참조 + 2] < 0) ajachitia_ajutuu("IOException: stream closed"); return; }
        int aa_inra_awai = -1, ajutuu = 0;
        if (말(이름, "close") && 말(akua_ipaa_ajutuu, "()V")) aa_inra_awai = 0;
        if (!출력 && 말(이름, "read") && 말(akua_ipaa_ajutuu, "()I")) aa_inra_awai = 1;
        if (출력 && 말(이름, "write") && 말(akua_ipaa_ajutuu, "(I)V")) { aa_inra_awai = 2; ajutuu = 빼기(1); }
        if (aa_inra_awai < 0) { ajachitia_ajutuu("unsupported file stream method"); return; }
        int palantüsü_ajutuu = 빼기(2);
        if (!객체(palantüsü_ajutuu, 종류) || ajachitia) return;
        if (힙[palantüsü_ajutuu + 3] == 0) { ajachitia_ajutuu("uninitialized file stream"); return; }
        int 서술자 = 힙[palantüsü_ajutuu + 2];
        if (aa_inra_awai == 0) {
            if (서술자 >= 0 && ka_yataayakalü.파일서술자닫기(서술자) < 0) ajachitia_ajutuu("IOException: close failed");
            힙[palantüsü_ajutuu + 2] = -1; return;
        }
        if (서술자 < 0) { ajachitia_ajutuu("IOException: stream closed"); return; }
        if (aa_inra_awai == 1) {
            int 결과 = ka_yataayakalü.파일한바이트읽기(서술자);
            if (결과 < -1) ajachitia_ajutuu("IOException: read failed"); else 넣기(결과 == 256 ? -1 : 결과, 1);
        } else if (ka_yataayakalü.파일한바이트쓰기(서술자, ajutuu) != 1) ajachitia_ajutuu("IOException: write failed");
    }
    static void 함수호출(int ee_iyatialujuna, int aluwataaya) {
        if (ee_iyatialujuna <= 0 || ee_iyatialujuna >= waneepiajutu_akanüliajia.length || (waneepiajutu_akanüliajia[ee_iyatialujuna] != 10 && waneepiajutu_akanüliajia[ee_iyatialujuna] != 11)) { ajachitia_ajutuu("invalid method reference"); return; }
        int 소유 = 클래스문자(상가[ee_iyatialujuna]), 이름 = 참조이름(상나[ee_iyatialujuna]), akua_ipaa_ajutuu = 참조형식(상나[ee_iyatialujuna]);
        if (ajachitia) return;
        if (기본호출(소유, 이름, akua_ipaa_ajutuu, aluwataaya)) return;
        if (말(소유, "java/io/FileInputStream") || 말(소유, "java/io/FileOutputStream")) {
            anaajaalaa_palantüsü_ounekaa(소유, 이름, akua_ipaa_ajutuu, aluwataaya); return;
        }
        if (aluwataaya == 184 && 말(소유, "java/lang/Integer") && 말(이름, "parseInt") && 말(akua_ipaa_ajutuu, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (aluwataaya == 182 && 말(소유, "java/io/PrintStream") && (말(이름, "println") || 말(이름, "print"))) {
            int 형 = 0, ajutuu = 0;
            if (말(akua_ipaa_ajutuu, "(I)V")) { 형 = 1; ajutuu = 빼기(1); }
            else if (말(akua_ipaa_ajutuu, "(Z)V")) { 형 = 2; ajutuu = 빼기(1); }
            else if (말(akua_ipaa_ajutuu, "(C)V")) { 형 = 3; ajutuu = 빼기(1); }
            else if (말(akua_ipaa_ajutuu, "(Ljava/lang/String;)V")) { 형 = 4; ajutuu = 빼기(2); }
            else if (!말(akua_ipaa_ajutuu, "()V") || !말(이름, "println")) ajachitia_ajutuu("unsupported print descriptor");
            if (빼기(2) != -1) ajachitia_ajutuu("invalid PrintStream receiver");
            if (ajachitia) return;
            if (형 == 1) 자바도구.수쓰기(ajutuu);
            if (형 == 2) ka_yataayakalü.ashajaa(ajutuu == 0 ? "false" : "true");
            if (형 == 3) ka_yataayakalü.ashajaa_jeerü_ajutuu(ajutuu & 65535);
            if (형 == 4) 글쓰기(ajutuu);
            if (말(이름, "println")) ka_yataayakalü.ashajaa_jeerü_ajutuu(10);
            return;
        }
        if (aluwataaya == 182 && 말(소유, "java/lang/String")) {
            if (말(이름, "length") && 말(akua_ipaa_ajutuu, "()I")) {
                int 참조 = 빼기(2); if (객체(참조, 1)) 넣기(힙[참조 + 1], 1); return;
            }
            if (말(이름, "charAt") && 말(akua_ipaa_ajutuu, "(I)C")) {
                int 첨자 = 빼기(1), 참조 = 빼기(2);
                if (객체(참조, 1)) {
                    if (첨자 < 0 || 첨자 >= 힙[참조 + 1]) ajachitia_ajutuu("StringIndexOutOfBoundsException"); else 넣기(힙[참조 + 2 + 첨자], 1);
                }
                return;
            }
        }
        if (말(소유, "java/lang/StringBuilder")) {
            if (aluwataaya == 183 && 말(이름, "<init>") && 말(akua_ipaa_ajutuu, "()V")) { 객체(빼기(2), 4); return; }
            if (aluwataaya == 182 && 말(이름, "toString") && 말(akua_ipaa_ajutuu, "()Ljava/lang/String;")) {
                int 참조 = 빼기(2); if (객체(참조, 4)) 넣기(힙[참조 + 2] == 0 ? epiajatü_jeerü("") : 힙[참조 + 2], 2); return;
            }
            if (aluwataaya == 182 && 말(이름, "append")) {
                int 글 = 0;
                if (말(akua_ipaa_ajutuu, "(I)Ljava/lang/StringBuilder;")) 글 = 수문자(빼기(1));
                else if (말(akua_ipaa_ajutuu, "(Z)Ljava/lang/StringBuilder;")) 글 = epiajatü_jeerü(빼기(1) == 0 ? "false" : "true");
                else if (말(akua_ipaa_ajutuu, "(C)Ljava/lang/StringBuilder;")) {
                    int ajutuu = 빼기(1); 글 = 할당(1, 1); if (!ajachitia) 힙[글 + 2] = ajutuu & 65535;
                }
                else if (말(akua_ipaa_ajutuu, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { 글 = 빼기(2); if (글 == 0) 글 = epiajatü_jeerü("null"); }
                else { ajachitia_ajutuu("unsupported StringBuilder append"); return; }
                int 참조 = 빼기(2); if (!객체(참조, 4) || !객체(글, 1)) return;
                int 앞 = 힙[참조 + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], 뒤길이 = 힙[글 + 1];
                int 새글 = 할당(1, 앞길이 + 뒤길이); if (ajachitia) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < 뒤길이; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[글 + 2 + 수];
                힙[참조 + 2] = 새글; 넣기(참조, 2); return;
            }
        }
        int 종 = 종찾기(소유); if (종 < 0 || ajachitia) return;
        int anaajaalaa_ee_iyatialujuna = 함수찾기(종, 이름, akua_ipaa_ajutuu);
        if (anaajaalaa_ee_iyatialujuna < 0) {
            for (int 문자값 = 종, 항목수 = 0; 문자값 >= 0 && 항목수 < 16; 항목수++, 문자값 = 부모종(문자값))
                if (말(종부모[문자값], "java/lang/Thread")) { 가닥호출(이름, akua_ipaa_ajutuu, aluwataaya); return; }
            ajachitia_ajutuu("NoSuchMethodError"); return;
        }
        if (((함수권한[anaajaalaa_ee_iyatialujuna] & 8) != 0) != (aluwataaya == 184)) { ajachitia_ajutuu("method static/instance mismatch"); return; }
        if (aluwataaya == 184) { if (!anaajaa(함수주인[anaajaalaa_ee_iyatialujuna], otpünaa_aluwataaya[otpünaa_ee_iyatialujuna])) return; }
        else {
            int 읽는자리 = 틀스택[otpünaa_ee_iyatialujuna] - 함수인수수[anaajaalaa_ee_iyatialujuna];
            if (읽는자리 < 0 || 스택형[otpünaa_ee_iyatialujuna * 128 + 읽는자리] != 2) { ajachitia_ajutuu("invalid method receiver"); return; }
            int 객체참조 = 스택값[otpünaa_ee_iyatialujuna * 128 + 읽는자리];
            if (!객체유효(객체참조)) return;
            if (힙[객체참조] < 32 || !종포함(힙[객체참조] - 32, 소유)) { ajachitia_ajutuu("method receiver type mismatch"); return; }
            if (aluwataaya != 183) anaajaalaa_ee_iyatialujuna = 함수찾기(힙[객체참조] - 32, 이름, akua_ipaa_ajutuu);
        }
        if (anaajaalaa_ee_iyatialujuna < 0 || (함수권한[anaajaalaa_ee_iyatialujuna] & 0x400) != 0) { ajachitia_ajutuu("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((함수권한[anaajaalaa_ee_iyatialujuna] & 32) != 0) {
            if (aluwataaya == 184) { int 문자값 = 함수주인[anaajaalaa_ee_iyatialujuna]; if (종잠금[문자값] == 0) 종잠금[문자값] = 할당(8, 0); 잠금참조 = 종잠금[문자값]; }
            else 잠금참조 = 스택값[otpünaa_ee_iyatialujuna * 128 + 틀스택[otpünaa_ee_iyatialujuna] - 함수인수수[anaajaalaa_ee_iyatialujuna]];
            if (!잠금얻기(잠금참조)) { if (!ajachitia) 틀위치[otpünaa_ee_iyatialujuna] = otpünaa_aluwataaya[otpünaa_ee_iyatialujuna]; return; }
        }
        호출(anaajaalaa_ee_iyatialujuna); if (!ajachitia) 틀잠금[otpünaa_ee_iyatialujuna] = 잠금참조;
    }
    static boolean 배열저장가능(int 배열참조, int atijaaya_ajutuu) {
        if (atijaaya_ajutuu == 0 || matüriisü_apüshii[배열참조] == 0) return true;
        boolean 성공여부 = matüriisü_apüshii[배열참조] == -1 ? (atijaaya_ajutuu > 0 && atijaaya_ajutuu < 힙끝 && 힙[atijaaya_ajutuu] == 1) : 맞는객체(atijaaya_ajutuu, matüriisü_apüshii[배열참조]);
        if (!성공여부 && !ajachitia) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int 배열칸(int 참조, int 첨자, int 형) {
        if (!객체(참조, 형)) return 0;
        if (첨자 < 0 || 첨자 >= 힙[참조 + 1]) { ajachitia_ajutuu("ArrayIndexOutOfBoundsException"); return 0; }
        return 참조 + 2 + 첨자;
    }
    static void 실행() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (ajachitia) { if (던진객체 != 0) 예외처리(); if (ajachitia || otpünaa_ee_iyatialujuna < 현재가닥 * 32) break; }
            if (otpünaa_ee_iyatialujuna < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!가닥바꾸기()) break; 조각 = 100; }
            if (otpünaa_ee_iyatialujuna == 0 && 종상태[시작종] != 2 && !anaajaa(시작종, 틀위치[otpünaa_ee_iyatialujuna])) continue;
            if (otpünaa_ee_iyatialujuna == 현재가닥 * 32 && 현재가닥 != 0 && (함수권한[틀함수[otpünaa_ee_iyatialujuna]] & 32) != 0 && 틀잠금[otpünaa_ee_iyatialujuna] == 0) {
                int 객체참조 = 가닥대상[현재가닥]; if (!잠금얻기(객체참조)) { if (ajachitia) break; continue; } 틀잠금[otpünaa_ee_iyatialujuna] = 객체참조;
            }
            잠시수 = 0;
            if (--남음 == 0) { ajachitia_ajutuu("instruction limit (500000)"); break; }
            int 시작 = 틀위치[otpünaa_ee_iyatialujuna]; otpünaa_aluwataaya[otpünaa_ee_iyatialujuna] = 시작; int ajutuu = 명바();
            if (ajachitia) break;
            if (ajutuu == 0) continue;
            if (ajutuu == 1) { 넣기(0, 2); continue; }
            if (ajutuu >= 2 && ajutuu <= 8) { 넣기(ajutuu - 3, 1); continue; }
            if (ajutuu == 16) { 넣기((byte)명바(), 1); continue; }
            if (ajutuu == 17) { 넣기((short)명짧(), 1); continue; }
            if (ajutuu == 18 || ajutuu == 19) {
                int 수 = 함수주인[틀함수[otpünaa_ee_iyatialujuna]] * 512 + (ajutuu == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= waneepiajutu_akanüliajia.length) ajachitia_ajutuu("invalid ldc constant");
                else if (waneepiajutu_akanüliajia[수] == 3) 넣기(상가[수], 1);
                else if (waneepiajutu_akanüliajia[수] == 8) 넣기(상문자(상가[수]), 2);
                else ajachitia_ajutuu("unsupported ldc constant");
                continue;
            }
            if (ajutuu == 21 || ajutuu == 25) { 지역읽기(명바(), ajutuu == 21 ? 1 : 2); continue; }
            if (ajutuu >= 26 && ajutuu <= 29) { 지역읽기(ajutuu - 26, 1); continue; }
            if (ajutuu >= 42 && ajutuu <= 45) { 지역읽기(ajutuu - 42, 2); continue; }
            if (ajutuu == 54 || ajutuu == 58) { 지역쓰기(명바(), ajutuu == 54 ? 1 : 2); continue; }
            if (ajutuu >= 59 && ajutuu <= 62) { 지역쓰기(ajutuu - 59, 1); continue; }
            if (ajutuu >= 75 && ajutuu <= 78) { 지역쓰기(ajutuu - 75, 2); continue; }
            if (ajutuu == 46 || ajutuu >= 50 && ajutuu <= 53) {
                int 항목자리 = 빼기(1), 객체참조 = 빼기(2), 분류코드 = ajutuu == 46 ? 2 : ajutuu == 50 ? 3 : ajutuu == 51 ? 20 : ajutuu == 52 ? 22 : 23;
                if (ajutuu == 51 && 객체참조 > 0 && 객체참조 < 힙끝 && 힙[객체참조] == 21) 분류코드 = 21;
                int 읽는자리 = 배열칸(객체참조, 항목자리, 분류코드); if (!ajachitia) 넣기(힙[읽는자리], ajutuu == 50 ? 2 : 1); continue;
            }
            if (ajutuu == 79 || ajutuu >= 83 && ajutuu <= 86) {
                int 항목참조 = 빼기(ajutuu == 83 ? 2 : 1), 항목자리 = 빼기(1), 객체참조 = 빼기(2), 분류코드 = ajutuu == 79 ? 2 : ajutuu == 83 ? 3 : ajutuu == 84 ? 20 : ajutuu == 85 ? 22 : 23;
                if (ajutuu == 84 && 객체참조 > 0 && 객체참조 < 힙끝 && 힙[객체참조] == 21) 분류코드 = 21;
                int 읽는자리 = 배열칸(객체참조, 항목자리, 분류코드);
                if (!ajachitia && 분류코드 == 3 && !배열저장가능(객체참조, 항목참조)) continue;
                if (!ajachitia) 힙[읽는자리] = 분류코드 == 20 ? (byte)항목참조 : 분류코드 == 21 ? 항목참조 & 1 : 분류코드 == 22 ? (char)항목참조 : 분류코드 == 23 ? (short)항목참조 : 항목참조;
                continue;
            }
            if (ajutuu >= 87 && ajutuu <= 95) { 스택명령(ajutuu); continue; }
            if (ajutuu == 96 || ajutuu == 100 || ajutuu == 104 || ajutuu == 108 || ajutuu == 112 || ajutuu == 120
                || ajutuu == 122 || ajutuu == 124 || ajutuu == 126 || ajutuu == 128 || ajutuu == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), 결과 = 0;
                if ((ajutuu == 108 || ajutuu == 112) && 나 == 0) { ajachitia_ajutuu("ArithmeticException: / by zero"); continue; }
                if (ajutuu == 96) 결과 = 가 + 나;
                if (ajutuu == 100) 결과 = 가 - 나;
                if (ajutuu == 104) 결과 = 가 * 나;
                if (ajutuu == 108) 결과 = 가 / 나;
                if (ajutuu == 112) 결과 = 가 % 나;
                if (ajutuu == 120) 결과 = 가 << 나;
                if (ajutuu == 122) 결과 = 가 >> 나;
                if (ajutuu == 124) 결과 = 가 >>> 나;
                if (ajutuu == 126) 결과 = 가 & 나;
                if (ajutuu == 128) 결과 = 가 | 나;
                if (ajutuu == 130) 결과 = 가 ^ 나;
                넣기(결과, 1); continue;
            }
            if (ajutuu == 116) { 넣기(-빼기(1), 1); continue; }
            if (ajutuu == 132) {
                int 지역 = 명바(), 증분 = (byte)명바(); 지역읽기(지역, 1); 넣기(빼기(1) + 증분, 1); 지역쓰기(지역, 1); continue;
            }
            if (ajutuu >= 145 && ajutuu <= 147) {
                int 수 = 빼기(1); 넣기(ajutuu == 145 ? (byte)수 : ajutuu == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (ajutuu >= 153 && ajutuu <= 167 || ajutuu == 198 || ajutuu == 199) {
                int jalamüinjatü_ajutuu = 시작 + (short)명짧(); boolean 갈까 = ajutuu == 167;
                if (ajutuu >= 153 && ajutuu <= 158) {
                    int 수 = 빼기(1); 갈까 = ajutuu == 153 ? 수 == 0 : ajutuu == 154 ? 수 != 0 : ajutuu == 155 ? 수 < 0 : ajutuu == 156 ? 수 >= 0 : ajutuu == 157 ? 수 > 0 : 수 <= 0;
                } else if (ajutuu >= 159 && ajutuu <= 166) {
                    int 나 = 빼기(ajutuu >= 165 ? 2 : 1), 가 = 빼기(ajutuu >= 165 ? 2 : 1);
                    갈까 = ajutuu == 159 || ajutuu == 165 ? 가 == 나 : ajutuu == 160 || ajutuu == 166 ? 가 != 나 : ajutuu == 161 ? 가 < 나 : ajutuu == 162 ? 가 >= 나 : ajutuu == 163 ? 가 > 나 : 가 <= 나;
                } else if (ajutuu == 198 || ajutuu == 199) { int 수 = 빼기(2); 갈까 = ajutuu == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) 이동(jalamüinjatü_ajutuu); continue;
            }
            if (ajutuu == 172 || ajutuu == 176 || ajutuu == 177) { 반환(ajutuu == 172 ? 1 : ajutuu == 176 ? 2 : 0); continue; }
            if (ajutuu >= 178 && ajutuu <= 181) { 필드호출(명상수(), ajutuu, 시작); continue; }
            if (ajutuu >= 182 && ajutuu <= 185) {
                int 부호값 = 명상수();
                if (ajutuu == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { ajachitia_ajutuu("invalid invokeinterface operands"); continue; } }
                함수호출(부호값, ajutuu); continue;
            }
            if (ajutuu == 187) { 새객체(클래스문자(명상수()), 시작); continue; }
            if (ajutuu == 188 || ajutuu == 189) {
                int 분류코드 = 3, apüshii = 0;
                if (ajutuu == 188) { int 임시값 = 명바(); 분류코드 = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else apüshii = 클래스문자(명상수());
                if (분류코드 == 0) { ajachitia_ajutuu("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), 객체참조 = 할당(분류코드, 유효길이); if (!ajachitia) matüriisü_apüshii[객체참조] = apüshii; 넣기(객체참조, 2); continue;
            }
            if (ajutuu == 190) {
                int 객체참조 = 빼기(2);
                if (객체유효(객체참조)) { int 비교자리 = 힙[객체참조]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) ajachitia_ajutuu("not an array"); else 넣기(힙[객체참조 + 1], 1); }
                continue;
            }
            if (ajutuu == 191) {
                int 객체참조 = 빼기(2); if (객체유효(객체참조)) { if (힙[객체참조] != 9) ajachitia_ajutuu("athrow requires supported Throwable"); else { 던진객체 = 객체참조; ajachitia = true; } }
                continue;
            }
            if (ajutuu == 192 || ajutuu == 193) {
                int 이름상수 = 클래스문자(명상수()), 객체참조 = 빼기(2); boolean 일치여부 = 맞는객체(객체참조, 이름상수);
                if (ajutuu == 193) 넣기(객체참조 != 0 && 일치여부 ? 1 : 0, 1);
                else { if (!일치여부 && !ajachitia) ajachitia_ajutuu("ClassCastException"); 넣기(객체참조, 2); }
                continue;
            }
            if (ajutuu == 170 || ajutuu == 171) {
                int 읽는자리 = 시작 + 1, anaajaalaa_ee_iyatialujuna = 틀함수[otpünaa_ee_iyatialujuna], 키참조 = 빼기(1);
                while ((읽는자리 - 함수시작[anaajaalaa_ee_iyatialujuna]) % 4 != 0) 읽는자리++;
                int 대상값 = 위치정수(읽는자리);
                if (ajutuu == 170) { int 낮은값 = 위치정수(읽는자리 + 4), 높은값 = 위치정수(읽는자리 + 8); if (키참조 >= 낮은값 && 키참조 <= 높은값) 대상값 = 위치정수(읽는자리 + 12 + (키참조 - 낮은값) * 4); }
                else { int 총수 = 위치정수(읽는자리 + 4); for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 총수; eitawaakualü_ee_iyatialujuna++) if (위치정수(읽는자리 + 8 + eitawaakualü_ee_iyatialujuna * 8) == 키참조) 대상값 = 위치정수(읽는자리 + 12 + eitawaakualü_ee_iyatialujuna * 8); }
                이동(시작 + 대상값); continue;
            }
            if (ajutuu == 200) { 이동(시작 + 위치정수(시작 + 1)); continue; }
            if (ajutuu == 194 || ajutuu == 195) {
                int 객체참조 = 빼기(2);
                if (ajutuu == 195) 잠금풀기(객체참조);
                else if (!잠금얻기(객체참조) && !ajachitia) { 넣기(객체참조, 2); 틀위치[otpünaa_ee_iyatialujuna] = 시작; }
                continue;
            }
            if (ajutuu == 196) {
                int 명령코드 = 명바(), 항목자리 = 명짧();
                if (명령코드 == 21 || 명령코드 == 25) 지역읽기(항목자리, 명령코드 == 21 ? 1 : 2);
                else if (명령코드 == 54 || 명령코드 == 58) 지역쓰기(항목자리, 명령코드 == 54 ? 1 : 2);
                else if (명령코드 == 132) { int 변화량 = (short)명짧(); 지역읽기(항목자리, 1); 넣기(빼기(1) + 변화량, 1); 지역쓰기(항목자리, 1); }
                else ajachitia_ajutuu("unsupported wide opcode");
                continue;
            }
            ajachitia_ajutuu("unsupported bytecode");
        }
    }
    static int 종찾기(int 이름) {
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 종수; eitawaakualü_ee_iyatialujuna++) if (종이름[eitawaakualü_ee_iyatialujuna] != 0 && 같은말(종이름[eitawaakualü_ee_iyatialujuna], 이름)) return eitawaakualü_ee_iyatialujuna;
        return 종적재(상문자(이름));
    }
    static int 종적재(int 이름글) {
        if (!객체(이름글, 1)) return -1;
        int akaliaa_ajutuu = 힙[이름글 + 1];
        if (akaliaa_ajutuu < 1 || akaliaa_ajutuu > 505 || 종수 == 16) { ajachitia_ajutuu("class name/count limit"); return -1; }
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < akaliaa_ajutuu; eitawaakualü_ee_iyatialujuna++) { int 문자값 = 힙[이름글 + 2 + eitawaakualü_ee_iyatialujuna]; 파일명[eitawaakualü_ee_iyatialujuna] = 문자값 == '/' ? '.' : 문자값; }
        파일명[akaliaa_ajutuu] = '.'; 파일명[akaliaa_ajutuu + 1] = 'c'; 파일명[akaliaa_ajutuu + 2] = 'l'; 파일명[akaliaa_ajutuu + 3] = 'a'; 파일명[akaliaa_ajutuu + 4] = 's'; 파일명[akaliaa_ajutuu + 5] = 's'; 파일명[akaliaa_ajutuu + 6] = 0;
        int 크기 = ka_yataayakalü.파일읽기(파일명, 임시파일);
        if (크기 < 0) { ajachitia_ajutuu("ClassNotFoundException"); return -1; }
        int 종 = 종수++; 종크기[종] = 크기;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 크기; eitawaakualü_ee_iyatialujuna++) anaajaalaa[종 * 16384 + eitawaakualü_ee_iyatialujuna] = 임시파일[eitawaakualü_ee_iyatialujuna];
        클래스읽기(종); if (ajachitia) return -1;
        int 실제 = 상문자(종이름[종]);
        if (!글같음(실제, 이름글, true)) { ajachitia_ajutuu("class name does not match file"); return -1; }
        int 부모 = 종부모[종];
        if (부모 != 0 && !말(부모, "java/lang/Object") && !말(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = 종찾기(부모);
            if (ajachitia || 위 < 0) return -1;
            int 읽는자리 = 위, 단계수 = 0;
            while (읽는자리 >= 0 && 단계수++ < 16) {
                if (읽는자리 == 종) { ajachitia_ajutuu("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int anaajaalaa_ee_iyatialujuna = 0; anaajaalaa_ee_iyatialujuna < 칸수; anaajaalaa_ee_iyatialujuna++) if (칸주인[anaajaalaa_ee_iyatialujuna] == 종 && (칸권한[anaajaalaa_ee_iyatialujuna] & 8) == 0) 칸위치[anaajaalaa_ee_iyatialujuna] += 시작변위;
            종칸수[종] += 시작변위;
        }
        return 종;
    }
    static int 부모종(int 종) {
        int 이름 = 종부모[종];
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 종수; eitawaakualü_ee_iyatialujuna++) if (이름 != 0 && 종이름[eitawaakualü_ee_iyatialujuna] != 0 && 같은말(종이름[eitawaakualü_ee_iyatialujuna], 이름)) return eitawaakualü_ee_iyatialujuna;
        return -1;
    }
    static int 함수찾기(int 종, int 이름, int akua_ipaa_ajutuu) {
        for (int 깊이 = 0; 종 >= 0 && 깊이 < 16; 깊이++, 종 = 부모종(종)) {
            for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 함수수; eitawaakualü_ee_iyatialujuna++) if (함수주인[eitawaakualü_ee_iyatialujuna] == 종 && 같은말(함수명[eitawaakualü_ee_iyatialujuna], 이름) && 같은말(함수형[eitawaakualü_ee_iyatialujuna], akua_ipaa_ajutuu)) return eitawaakualü_ee_iyatialujuna;
        }
        return -1;
    }
    static int 이름함수(int 종, String 이름, String akua_ipaa_ajutuu) {
        for (int 깊이 = 0; 종 >= 0 && 깊이 < 16; 깊이++, 종 = 부모종(종))
            for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 함수수; eitawaakualü_ee_iyatialujuna++) if (함수주인[eitawaakualü_ee_iyatialujuna] == 종 && 말(함수명[eitawaakualü_ee_iyatialujuna], 이름) && 말(함수형[eitawaakualü_ee_iyatialujuna], akua_ipaa_ajutuu)) return eitawaakualü_ee_iyatialujuna;
        return -1;
    }
    static int 형종류(int 이름) { return anaajaalaa[상가[이름]] == 'L' || anaajaalaa[상가[이름]] == '[' ? 2 : 1; }
    static boolean anaajaa(int 종, int aluwataaya_achuwalaa) {
        if (종 < 0 || ajachitia) return false;
        if (종상태[종] == 3) { ajachitia_ajutuu("NoClassDefFoundError: initialization failed"); return false; }
        if (종상태[종] == 1 && akotchijuushi_akumajia_ipa[종] != 현재가닥) { 틀위치[otpünaa_ee_iyatialujuna] = aluwataaya_achuwalaa; 바꿈요청 = true; return false; }
        if (종상태[종] != 0) return true;
        int 위 = 부모종(종);
        if (위 >= 0 && !anaajaa(위, aluwataaya_achuwalaa)) return false;
        종상태[종] = 1; akotchijuushi_akumajia_ipa[종] = 현재가닥;
        if (종초기화[종] != 0) {
            틀위치[otpünaa_ee_iyatialujuna] = aluwataaya_achuwalaa;
            호출(종초기화[종] - 1); if (!ajachitia) anaajaa_otpünaa[otpünaa_ee_iyatialujuna] = 종 + 1;
            return false;
        }
        종상태[종] = 2; return true;
    }
    static void 필드호출(int ee_iyatialujuna, int aluwataaya, int 시작) {
        if (!cheeke_waneepiajutu(ee_iyatialujuna, 9)) return;
        int 소유 = 클래스문자(상가[ee_iyatialujuna]), 이름 = 참조이름(상나[ee_iyatialujuna]), akua_ipaa_ajutuu = 참조형식(상나[ee_iyatialujuna]);
        if (말(소유, "java/lang/System") && (말(이름, "out") || 말(이름, "err")) && 말(akua_ipaa_ajutuu, "Ljava/io/PrintStream;") && aluwataaya == 178) { 넣기(-1, 2); return; }
        int 종 = 종찾기(소유); if (종 < 0 || ajachitia) return;
        int 찾음 = -1;
        for (int 읽는자리 = 종, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int anaajaalaa_ee_iyatialujuna = 0; anaajaalaa_ee_iyatialujuna < 칸수; anaajaalaa_ee_iyatialujuna++) if (칸주인[anaajaalaa_ee_iyatialujuna] == 읽는자리 && 같은말(칸이름[anaajaalaa_ee_iyatialujuna], 이름) && 같은말(칸형[anaajaalaa_ee_iyatialujuna], akua_ipaa_ajutuu)) 찾음 = anaajaalaa_ee_iyatialujuna;
        if (찾음 < 0) { ajachitia_ajutuu("NoSuchFieldError"); return; }
        boolean jimatüsü_ajutuu = aluwataaya == 178 || aluwataaya == 179;
        if (jimatüsü_ajutuu != ((칸권한[찾음] & 8) != 0)) { ajachitia_ajutuu("field static/instance mismatch"); return; }
        if (jimatüsü_ajutuu && !anaajaa(칸주인[찾음], 시작)) return;
        int 형 = 형종류(akua_ipaa_ajutuu), ajutuu = 0;
        if (aluwataaya == 179 || aluwataaya == 181) ajutuu = 빼기(형);
        if (jimatüsü_ajutuu) { if (aluwataaya == 178) 넣기(칸값[찾음], 형); else if (!ajachitia) 칸값[찾음] = ajutuu; return; }
        int 객체참조 = 빼기(2);
        if (!객체유효(객체참조)) return;
        if (힙[객체참조] < 32 || !종포함(힙[객체참조] - 32, 소유)) { ajachitia_ajutuu("field receiver type mismatch"); return; }
        int 보관칸 = 객체참조 + 2 + 칸위치[찾음];
        if (aluwataaya == 180) 넣기(힙[보관칸], 형);
        else if (!ajachitia) { 힙[보관칸] = ajutuu; 힙참조[보관칸] = 형 == 2 ? 1 : 0; }
    }
    static boolean 종포함(int 종, int 이름) {
        for (int 중첩깊이 = 0; 종 >= 0 && 중첩깊이 < 16; 중첩깊이++, 종 = 부모종(종)) {
            if (같은말(종이름[종], 이름) || (종부모[종] != 0 && 같은말(종부모[종], 이름))) return true;
            for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[종]; 안쪽자리++) if (같은말(akotchijuushi_po_upünawaa[종 * 16 + 안쪽자리], 이름)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int waai_atijaaya, boolean wopu_a_ttaaleemüin) {
        if (첫값 == waai_atijaaya) return true;
        if (첫값 <= 0 || waai_atijaaya <= 0 || 힙[첫값] != 1 || 힙[waai_atijaaya] != 1 || 힙[첫값 + 1] != 힙[waai_atijaaya + 1]) return false;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 힙[첫값 + 1]; eitawaakualü_ee_iyatialujuna++) {
            int 가로좌표 = 힙[첫값 + 2 + eitawaakualü_ee_iyatialujuna], 세로좌표 = 힙[waai_atijaaya + 2 + eitawaakualü_ee_iyatialujuna];
            if (wopu_a_ttaaleemüin) { if (가로좌표 == '.') 가로좌표 = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (가로좌표 != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int 객체참조) {
        if (객체참조 == 0) { ajachitia_ajutuu("NullPointerException"); return false; }
        if (객체참조 < 1 || 객체참조 >= 힙끝 || 힙폭[객체참조] < 2 || 힙[객체참조] == 0) { ajachitia_ajutuu("invalid object reference"); return false; }
        return true;
    }
    static void aa_inmajaa_ajutuu(int 객체참조) {
        if (객체참조 > 0 && 객체참조 < 힙끝 && 힙폭[객체참조] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = 객체참조;
    }
    static void 표시(int 객체참조) {
        if (객체참조 > 0 && 객체참조 < 힙끝 && 힙폭[객체참조] >= 2 && 힙[객체참조] != 0 && 힙표시[객체참조] == 0) {
            힙표시[객체참조] = 1; 표시대기[표시수++] = 객체참조;
        }
    }
    static void 수거() {
        표시수 = 0; 수거횟수++;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) 힙표시[검사자리] = 0;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 문자열참조.length; eitawaakualü_ee_iyatialujuna++) 표시(문자열참조[eitawaakualü_ee_iyatialujuna]);
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 칸수; eitawaakualü_ee_iyatialujuna++) if ((칸권한[eitawaakualü_ee_iyatialujuna] & 8) != 0 && 형종류(칸형[eitawaakualü_ee_iyatialujuna]) == 2) 표시(칸값[eitawaakualü_ee_iyatialujuna]);
        for (int 임시값 = 0; 임시값 < 가닥수; 임시값++) {
            표시(가닥객체[임시값]); 표시(가닥대상[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? otpünaa_ee_iyatialujuna : akumajia_ipa_otpünaa[임시값];
            for (int anaajaalaa_ee_iyatialujuna = 임시값 * 32; anaajaalaa_ee_iyatialujuna <= 꼭대기자리; anaajaalaa_ee_iyatialujuna++) {
                for (int 안쪽자리 = 0; 안쪽자리 < 함수지역[틀함수[anaajaalaa_ee_iyatialujuna]]; 안쪽자리++) if (지역형[anaajaalaa_ee_iyatialujuna * 128 + 안쪽자리] == 2) 표시(지역값[anaajaalaa_ee_iyatialujuna * 128 + 안쪽자리]);
                for (int 안쪽자리 = 0; 안쪽자리 < 틀스택[anaajaalaa_ee_iyatialujuna]; 안쪽자리++) if (스택형[anaajaalaa_ee_iyatialujuna * 128 + 안쪽자리] == 2) 표시(스택값[anaajaalaa_ee_iyatialujuna * 128 + 안쪽자리]);
            }
        }
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 화면참조.length; eitawaakualü_ee_iyatialujuna++) 표시(화면참조[eitawaakualü_ee_iyatialujuna]);
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 나중수; eitawaakualü_ee_iyatialujuna++) 표시(나중실행[eitawaakualü_ee_iyatialujuna]);
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 정수저장.length; eitawaakualü_ee_iyatialujuna++) 표시(정수저장[eitawaakualü_ee_iyatialujuna]);
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 종수; eitawaakualü_ee_iyatialujuna++) 표시(종잠금[eitawaakualü_ee_iyatialujuna]);
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (잠금깊이[검사자리] > 0) 표시(검사자리);
        표시(던진객체);
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 잠시수; eitawaakualü_ee_iyatialujuna++) 표시(잠시참조[eitawaakualü_ee_iyatialujuna]);
        while (표시수 > 0) {
            int 객체참조 = 표시대기[--표시수], 분류코드 = 힙[객체참조];
            for (int eitawaakualü_ee_iyatialujuna = 객체참조 + 2; eitawaakualü_ee_iyatialujuna < 객체참조 + 힙폭[객체참조]; eitawaakualü_ee_iyatialujuna++) if (분류코드 == 3 || 분류코드 == 4 || 힙참조[eitawaakualü_ee_iyatialujuna] != 0) 표시(힙[eitawaakualü_ee_iyatialujuna]);
        }
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙표시[검사자리] == 0) 힙[검사자리] = 0;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙[검사자리] == 0) {
            while (검사자리 + 힙폭[검사자리] < 힙끝 && 힙[검사자리 + 힙폭[검사자리]] == 0) { int 다음자리 = 검사자리 + 힙폭[검사자리]; 힙폭[검사자리] += 힙폭[다음자리]; 힙폭[다음자리] = 0; }
            if (검사자리 + 힙폭[검사자리] == 힙끝) { 힙끝 = 검사자리; break; }
        }
    }
    static int 새기억(int 종류, int akaliaa_ajutuu) {
        if (akaliaa_ajutuu < 0) { ajachitia_ajutuu("NegativeArraySizeException"); return 0; }
        if (akaliaa_ajutuu > 힙.length - 3) { ajachitia_ajutuu("object heap exhausted"); return 0; }
        int 필요수 = akaliaa_ajutuu + 2, 객체참조 = 0;
        if (필요수 <= 힙.length - 힙끝) { 객체참조 = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { 객체참조 = 읽는자리; break; }
            if (객체참조 != 0) {
                int 남은길이 = 힙폭[객체참조] - 필요수;
                if (남은길이 >= 2) { 힙폭[객체참조 + 필요수] = 남은길이; 힙[객체참조 + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { 객체참조 = 힙끝; 힙끝 += 필요수; }
        }
        if (객체참조 == 0) { ajachitia_ajutuu("object heap exhausted"); return 0; }
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 필요수; eitawaakualü_ee_iyatialujuna++) { 힙[객체참조 + eitawaakualü_ee_iyatialujuna] = 0; 힙참조[객체참조 + eitawaakualü_ee_iyatialujuna] = 0; 힙폭[객체참조 + eitawaakualü_ee_iyatialujuna] = 0; }
        matüriisü_apüshii[객체참조] = 0;
        힙폭[객체참조] = 필요수; 힙[객체참조] = 종류; 힙[객체참조 + 1] = akaliaa_ajutuu; aa_inmajaa_ajutuu(객체참조); return 객체참조;
    }
    static int 예외종(String 이름상수) {
        if (자바도구.같음(이름상수, "java/lang/Throwable")) return 1;
        if (자바도구.같음(이름상수, "java/lang/Exception")) return 2;
        if (자바도구.같음(이름상수, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(이름상수, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(이름상수, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(이름상수, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(이름상수, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(이름상수, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(이름상수, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(이름상수, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(이름상수, "java/io/IOException")) return 11;
        if (자바도구.같음(이름상수, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(이름상수, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(이름상수, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(이름상수, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int 예외상수(int 이름) {
        for (int eitawaakualü_ee_iyatialujuna = 1; eitawaakualü_ee_iyatialujuna <= 41; eitawaakualü_ee_iyatialujuna++) if (말(이름, 예외이름(eitawaakualü_ee_iyatialujuna))) return eitawaakualü_ee_iyatialujuna;
        return 0;
    }
    static String 예외이름(int ayaawatiaayaa_ajutuu) {
        if (ayaawatiaayaa_ajutuu == 40) return "java/lang/InterruptedException";
        if (ayaawatiaayaa_ajutuu == 41) return "한국어/자체/대기중단예외";
        if (ayaawatiaayaa_ajutuu == 39) return "java/net/SocketException";
        if (ayaawatiaayaa_ajutuu == 20) return "한국어/자체/예외";
        if (ayaawatiaayaa_ajutuu == 21) return "한국어/자체/실행예외";
        if (ayaawatiaayaa_ajutuu == 22) return "한국어/자체/입출력예외";
        if (ayaawatiaayaa_ajutuu == 23) return "한국어/자체/대기시간초과예외";
        if (ayaawatiaayaa_ajutuu == 24) return "한국어/자체/주소확인예외";
        if (ayaawatiaayaa_ajutuu == 25) return "한국어/자체/파일없음예외";
        if (ayaawatiaayaa_ajutuu == 26) return "한국어/자체/통신예외";
        if (ayaawatiaayaa_ajutuu == 27) return "한국어/자체/잘못된인수예외";
        if (ayaawatiaayaa_ajutuu == 28) return "한국어/자체/숫자형식예외";
        if (ayaawatiaayaa_ajutuu == 29) return "한국어/자체/범위예외";
        if (ayaawatiaayaa_ajutuu == 30) return "한국어/자체/배열범위예외";
        if (ayaawatiaayaa_ajutuu == 31) return "한국어/자체/문자열범위예외";
        if (ayaawatiaayaa_ajutuu == 32) return "한국어/자체/빈참조예외";
        if (ayaawatiaayaa_ajutuu == 33) return "한국어/자체/산술예외";
        if (ayaawatiaayaa_ajutuu == 34) return "한국어/자체/상태예외";
        if (ayaawatiaayaa_ajutuu == 35) return "한국어/자체/형변환예외";
        if (ayaawatiaayaa_ajutuu == 36) return "한국어/자체/음수배열크기예외";
        if (ayaawatiaayaa_ajutuu == 37) return "한국어/자체/배열저장예외";
        if (ayaawatiaayaa_ajutuu == 38) return "한국어/자체/가닥상태예외";
        if (ayaawatiaayaa_ajutuu == 1) return "java/lang/Throwable"; if (ayaawatiaayaa_ajutuu == 2) return "java/lang/Exception";
        if (ayaawatiaayaa_ajutuu == 3) return "java/lang/RuntimeException"; if (ayaawatiaayaa_ajutuu == 4) return "java/lang/ArithmeticException";
        if (ayaawatiaayaa_ajutuu == 5) return "java/lang/NullPointerException"; if (ayaawatiaayaa_ajutuu == 6) return "java/lang/IndexOutOfBoundsException";
        if (ayaawatiaayaa_ajutuu == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (ayaawatiaayaa_ajutuu == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (ayaawatiaayaa_ajutuu == 9) return "java/lang/IllegalArgumentException"; if (ayaawatiaayaa_ajutuu == 10) return "java/lang/NumberFormatException";
        if (ayaawatiaayaa_ajutuu == 11) return "java/io/IOException"; if (ayaawatiaayaa_ajutuu == 12) return "java/io/FileNotFoundException";
        if (ayaawatiaayaa_ajutuu == 17) return "java/lang/ArrayStoreException";
        if (ayaawatiaayaa_ajutuu == 18) return "java/net/UnknownHostException";
        if (ayaawatiaayaa_ajutuu == 19) return "java/net/SocketTimeoutException";
        if (ayaawatiaayaa_ajutuu == 16) return "java/lang/IllegalThreadStateException";
        if (ayaawatiaayaa_ajutuu == 13) return "java/lang/IllegalStateException"; if (ayaawatiaayaa_ajutuu == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int ayaawatiaayaa_ajutuu) {
        if (ayaawatiaayaa_ajutuu == 40) return 2;
        if (ayaawatiaayaa_ajutuu == 41) return 40;
        if (ayaawatiaayaa_ajutuu == 39) return 11;
        if (ayaawatiaayaa_ajutuu == 1) return 0;
        if (ayaawatiaayaa_ajutuu == 2) return 1;
        if (ayaawatiaayaa_ajutuu == 3) return 2;
        if (ayaawatiaayaa_ajutuu == 4) return 3;
        if (ayaawatiaayaa_ajutuu == 5) return 3;
        if (ayaawatiaayaa_ajutuu == 6) return 3;
        if (ayaawatiaayaa_ajutuu == 7) return 6;
        if (ayaawatiaayaa_ajutuu == 8) return 6;
        if (ayaawatiaayaa_ajutuu == 9) return 3;
        if (ayaawatiaayaa_ajutuu == 10) return 9;
        if (ayaawatiaayaa_ajutuu == 11) return 2;
        if (ayaawatiaayaa_ajutuu == 12) return 11;
        if (ayaawatiaayaa_ajutuu == 13) return 3;
        if (ayaawatiaayaa_ajutuu == 14) return 3;
        if (ayaawatiaayaa_ajutuu == 15) return 3;
        if (ayaawatiaayaa_ajutuu == 16) return 9;
        if (ayaawatiaayaa_ajutuu == 17) return 3;
        if (ayaawatiaayaa_ajutuu == 18) return 11;
        if (ayaawatiaayaa_ajutuu == 19) return 11;
        if (ayaawatiaayaa_ajutuu == 20) return 2;
        if (ayaawatiaayaa_ajutuu == 21) return 3;
        if (ayaawatiaayaa_ajutuu == 22) return 11;
        if (ayaawatiaayaa_ajutuu == 23) return 22;
        if (ayaawatiaayaa_ajutuu == 24) return 22;
        if (ayaawatiaayaa_ajutuu == 25) return 22;
        if (ayaawatiaayaa_ajutuu == 26) return 22;
        if (ayaawatiaayaa_ajutuu == 27) return 9;
        if (ayaawatiaayaa_ajutuu == 28) return 27;
        if (ayaawatiaayaa_ajutuu == 29) return 6;
        if (ayaawatiaayaa_ajutuu == 30) return 29;
        if (ayaawatiaayaa_ajutuu == 31) return 29;
        if (ayaawatiaayaa_ajutuu == 32) return 5;
        if (ayaawatiaayaa_ajutuu == 33) return 4;
        if (ayaawatiaayaa_ajutuu == 34) return 13;
        if (ayaawatiaayaa_ajutuu == 35) return 14;
        if (ayaawatiaayaa_ajutuu == 36) return 15;
        if (ayaawatiaayaa_ajutuu == 37) return 17;
        if (ayaawatiaayaa_ajutuu == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int 실제값, int 요구값) {
        for (int 깊이 = 0; 실제값 != 0 && 깊이 < 16; 깊이++, 실제값 = 예외부모(실제값))
            if (실제값 == 요구값) return true;
        return false;
    }
    static void 예외던짐(int ayaawatiaayaa_ajutuu, String 안내참조) {
        int 객체참조 = 새기억(9, 2); if (ajachitia) return;
        힙[객체참조 + 2] = ayaawatiaayaa_ajutuu; 힙[객체참조 + 3] = epiajatü_jeerü(안내참조); 힙참조[객체참조 + 3] = 1;
        던진객체 = 객체참조; ajachitia = true;
    }
    static boolean 맞는객체(int 객체참조, int 이름) {
        if (객체참조 == 0) return true;
        if (!객체유효(객체참조)) return false;
        int 분류코드 = 힙[객체참조];
        if (말(이름, "java/lang/Object")) return true;
        if (분류코드 >= 32) return 종포함(분류코드 - 32, 이름);
        if (분류코드 == 9) { int 대상값 = 예외상수(이름); return 대상값 != 0 && 예외포함(힙[객체참조 + 2], 대상값); }
        if (분류코드 == 1) return 말(이름, "java/lang/String") || 말(이름, "java/lang/CharSequence");
        if (분류코드 == 4) return 말(이름, "java/lang/StringBuilder") || 말(이름, "java/lang/CharSequence");
        if (분류코드 == 10) return 말(이름, "java/util/ArrayList") || 말(이름, "java/util/List");
        if (분류코드 == 11) return 말(이름, "java/util/HashMap") || 말(이름, "java/util/Map");
        if (분류코드 == 12) return 말(이름, "java/lang/Integer") || 말(이름, "java/lang/Number");
        if (분류코드 >= 24 && 분류코드 <= 28 && 힙[객체참조 + 13] != 0) return 한국어화면종(이름) == 분류코드 || 말(이름, "한국어/자체/화면구성요소");
        if (분류코드 >= 24 && 분류코드 <= 28) return (한국어화면종(이름) == 0 && 화면종(이름) == 분류코드) || 말(이름, "java/awt/Component") || 말(이름, "java/awt/Container") || 말(이름, "javax/swing/JComponent");
        if (분류코드 == 29) return 말(이름, 힙[객체참조 + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (분류코드 == 30) return 말(이름, "java/awt/FlowLayout") || 말(이름, "java/awt/LayoutManager");
        if (분류코드 == 17) return 말(이름, "java/net/Socket");
        if (분류코드 == 18) return 말(이름, "java/net/ServerSocket");
        if (분류코드 == 19) return 말(이름, 힙[객체참조 + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (분류코드 == 14) return 말(이름, "java/net/InetAddress");
        if (분류코드 == 15) return 말(이름, "java/net/DatagramSocket");
        if (분류코드 == 16) return 말(이름, "java/net/DatagramPacket");
        if (분류코드 == 13) return 말(이름, 힙[객체참조 + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (분류코드 == 2) return 말(이름, "[I"); if (분류코드 == 20) return 말(이름, "[B"); if (분류코드 == 21) return 말(이름, "[Z");
        if (분류코드 == 22) return 말(이름, "[C"); if (분류코드 == 23) return 말(이름, "[S");
        if (분류코드 != 3) return false;
        if (말(이름, "[Ljava/lang/Object;")) return true;
        int apüshii = matüriisü_apüshii[객체참조];
        if (apüshii == -1) return 말(이름, "[Ljava/lang/String;") || 말(이름, "[Ljava/lang/CharSequence;");
        if (apüshii == 0) return false;
        if (배열종비교(apüshii, 이름)) return true;
        if ((말(apüshii, "java/lang/String") || 말(apüshii, "java/lang/StringBuilder")) && 말(이름, "[Ljava/lang/CharSequence;")) return true;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 종수; eitawaakualü_ee_iyatialujuna++) if (같은말(종이름[eitawaakualü_ee_iyatialujuna], apüshii)) {
            for (int 문자값 = eitawaakualü_ee_iyatialujuna, 중첩깊이 = 0; 문자값 >= 0 && 중첩깊이 < 16; 중첩깊이++, 문자값 = 부모종(문자값)) {
                if (배열종비교(종부모[문자값], 이름)) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[문자값]; 안쪽자리++) if (배열종비교(akotchijuushi_po_upünawaa[문자값 * 16 + 안쪽자리], 이름)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int 이름상수, int 형식참조) {
        int 검사자리 = 상가[형식참조], 항목수 = 상나[형식참조];
        if (이름상수 == 0 || 항목수 < 4 || anaajaalaa[검사자리] != '[' || anaajaalaa[검사자리 + 1] != 'L' || anaajaalaa[검사자리 + 항목수 - 1] != ';' || 상나[이름상수] != 항목수 - 3) return false;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 항목수 - 3; eitawaakualü_ee_iyatialujuna++) if (anaajaalaa[상가[이름상수] + eitawaakualü_ee_iyatialujuna] != anaajaalaa[검사자리 + 2 + eitawaakualü_ee_iyatialujuna]) return false;
        return true;
    }
    static void 예외처리() {
        if (던진객체 == 0) return;
        ajachitia = false;
        while (otpünaa_ee_iyatialujuna >= 현재가닥 * 32) {
            int anaajaalaa_ee_iyatialujuna = 틀함수[otpünaa_ee_iyatialujuna], 읽는자리 = otpünaa_aluwataaya[otpünaa_ee_iyatialujuna];
            for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 잡기수; eitawaakualü_ee_iyatialujuna++) if (잡기함수[eitawaakualü_ee_iyatialujuna] == anaajaalaa_ee_iyatialujuna && 읽는자리 >= 잡기시작[eitawaakualü_ee_iyatialujuna] && 읽는자리 < 잡기끝[eitawaakualü_ee_iyatialujuna]
                && (잡기종[eitawaakualü_ee_iyatialujuna] == 0 || 맞는객체(던진객체, 잡기종[eitawaakualü_ee_iyatialujuna]))) {
                틀위치[otpünaa_ee_iyatialujuna] = 잡기위치[eitawaakualü_ee_iyatialujuna]; 틀스택[otpünaa_ee_iyatialujuna] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (anaajaa_otpünaa[otpünaa_ee_iyatialujuna] != 0) 종상태[anaajaa_otpünaa[otpünaa_ee_iyatialujuna] - 1] = 3;
            if (틀잠금[otpünaa_ee_iyatialujuna] != 0) { 잠금풀기(틀잠금[otpünaa_ee_iyatialujuna]); 틀잠금[otpünaa_ee_iyatialujuna] = 0; }
            otpünaa_ee_iyatialujuna--;
        }
        ka_yataayakalü.ashajaa("Uncaught ");
        if (힙[던진객체] == 9) { ka_yataayakalü.ashajaa(예외이름(힙[던진객체 + 2])); ka_yataayakalü.ashajaa(": "); 글쓰기(힙[던진객체 + 3]); }
        else ka_yataayakalü.ashajaa("user exception");
        ka_yataayakalü.ashajaa_jeerü_ajutuu(10); 던진객체 = 0; ajachitia = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void 스택명령(int 명령코드) {
        int 첫값 = 빼기(0), 첫형식 = 반환형;
        if (명령코드 == 87) return;
        if (명령코드 == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int waai_atijaaya = 빼기(0), 둘째형식 = 반환형;
        if (명령코드 == 88) return;
        if (명령코드 == 90) { 넣기(첫값, 첫형식); 넣기(waai_atijaaya, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 92) { 넣기(waai_atijaaya, 둘째형식); 넣기(첫값, 첫형식); 넣기(waai_atijaaya, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 95) { 넣기(첫값, 첫형식); 넣기(waai_atijaaya, 둘째형식); return; }
        int 문자값 = 빼기(0), 셋째형식 = 반환형;
        if (명령코드 == 91) { 넣기(첫값, 첫형식); 넣기(문자값, 셋째형식); 넣기(waai_atijaaya, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 93) { 넣기(waai_atijaaya, 둘째형식); 넣기(첫값, 첫형식); 넣기(문자값, 셋째형식); 넣기(waai_atijaaya, 둘째형식); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = 반환형;
        넣기(waai_atijaaya, 둘째형식); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(문자값, 셋째형식); 넣기(waai_atijaaya, 둘째형식); 넣기(첫값, 첫형식);
    }
    static void 새객체(int 이름상수, int 시작점) {
        int 분류코드 = 0, 유효길이 = 0, 예외참조 = 예외상수(이름상수);
        if (말(이름상수, "java/lang/StringBuilder")) { 분류코드 = 4; 유효길이 = 1; }
        if (말(이름상수, "java/io/FileInputStream")) { 분류코드 = 5; 유효길이 = 2; }
        if (말(이름상수, "java/io/FileOutputStream")) { 분류코드 = 6; 유효길이 = 2; }
        if (예외참조 != 0) { 분류코드 = 9; 유효길이 = 2; }
        if (말(이름상수, "java/util/ArrayList")) { 분류코드 = 10; 유효길이 = 2; }
        if (말(이름상수, "java/util/HashMap")) { 분류코드 = 11; 유효길이 = 2; }
        if (말(이름상수, "java/lang/Integer")) { 분류코드 = 12; 유효길이 = 1; }
        if (말(이름상수, "java/net/Socket")) { 분류코드 = 17; 유효길이 = 5; }
        if (말(이름상수, "java/net/ServerSocket")) { 분류코드 = 18; 유효길이 = 5; }
        if (말(이름상수, "java/net/DatagramSocket")) { 분류코드 = 15; 유효길이 = 3; }
        if (말(이름상수, "java/net/DatagramPacket")) { 분류코드 = 16; 유효길이 = 4; }
        if (말(이름상수, "java/lang/Thread") || 말(이름상수, "한국어/자체/작업가닥")) { 분류코드 = 13; 유효길이 = 2; }
        if (말(이름상수, "java/lang/Object")) { 분류코드 = 8; }
        if (분류코드 == 0 && 화면종(이름상수) != 0) { 분류코드 = 화면종(이름상수); 유효길이 = 12; }
        if (분류코드 == 0) {
            int 문자값 = 종찾기(이름상수); if (문자값 < 0 || ajachitia || !anaajaa(문자값, 시작점)) return;
            분류코드 = 32 + 문자값; 유효길이 = 종칸수[문자값];
        }
        int 객체참조 = 할당(분류코드, 유효길이); if (ajachitia) return;
        if (분류코드 == 13 && 말(이름상수, "한국어/자체/작업가닥")) 힙[객체참조 + 3] = 1;
        if (분류코드 >= 24 && 분류코드 <= 28 && 한국어화면종(이름상수) != 0) 힙[객체참조 + 13] = 1;
        if (분류코드 == 5 || 분류코드 == 6 || 분류코드 == 15 || 분류코드 == 17 || 분류코드 == 18) 힙[객체참조 + 2] = -1;
        if (분류코드 == 9) 힙[객체참조 + 2] = 예외참조;
        넣기(객체참조, 2);
    }
    static boolean 값같음(int 첫값, int waai_atijaaya) {
        if (첫값 == waai_atijaaya) return true;
        if (첫값 == 0 || waai_atijaaya == 0 || 첫값 < 0 || waai_atijaaya < 0 || 첫값 >= 힙끝 || waai_atijaaya >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[waai_atijaaya] == 1) return 글같음(첫값, waai_atijaaya, false);
        return 힙[첫값] == 12 && 힙[waai_atijaaya] == 12 && 힙[첫값 + 2] == 힙[waai_atijaaya + 2];
    }
    static int 글조각(int 객체참조, int 시작자리, int 끝자리) {
        if (!객체(객체참조, 1)) return 0;
        if (시작자리 < 0 || 끝자리 < 시작자리 || 끝자리 > 힙[객체참조 + 1]) { ajachitia_ajutuu("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = 할당(1, 끝자리 - 시작자리); if (ajachitia) return 0;
        for (int eitawaakualü_ee_iyatialujuna = 시작자리; eitawaakualü_ee_iyatialujuna < 끝자리; eitawaakualü_ee_iyatialujuna++) 힙[반환값 + 2 + eitawaakualü_ee_iyatialujuna - 시작자리] = 힙[객체참조 + 2 + eitawaakualü_ee_iyatialujuna];
        return 반환값;
    }
    static int 글합치기(int 첫값, int waai_atijaaya) {
        if (!객체(첫값, 1) || !객체(waai_atijaaya, 1)) return 0;
        int 항목수 = 힙[첫값 + 1], 함수번호 = 힙[waai_atijaaya + 1], 반환값 = 할당(1, 항목수 + 함수번호); if (ajachitia) return 0;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 항목수; eitawaakualü_ee_iyatialujuna++) 힙[반환값 + 2 + eitawaakualü_ee_iyatialujuna] = 힙[첫값 + 2 + eitawaakualü_ee_iyatialujuna];
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 함수번호; eitawaakualü_ee_iyatialujuna++) 힙[반환값 + 2 + 항목수 + eitawaakualü_ee_iyatialujuna] = 힙[waai_atijaaya + 2 + eitawaakualü_ee_iyatialujuna];
        return 반환값;
    }
    static boolean 기본호출(int 소유종, int 이름상수, int 서술상수, int 명령코드) {
        if (말(소유종, "한국어/자체/실행인수") && 명령코드 == 184) {
            if (말(이름상수, "개수") && 말(서술상수, "()I")) { 넣기(ka_yataayakalü.인수개수() - 1, 1); return true; }
            if (말(이름상수, "글") && 말(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= ka_yataayakalü.인수개수() - 1) 예외던짐(29, "실행 인수 범위를 벗어났습니다");
                else 넣기(epiajatü_jeerü(ka_yataayakalü.인수(순번 + 1)), 2);
                return true;
            }
            ajachitia_ajutuu("지원하지 않는 한국어 실행 인수 호출"); return true;
        }
        if (말(소유종, "한국어/자체/작업가닥")) { 가닥처리(이름상수, 서술상수, 명령코드, true); return true; }
        if (한국어화면소유(소유종)) { 한국어화면호출(소유종, 이름상수, 서술상수, 명령코드); return true; }
        if (화면소유(소유종)) { 화면호출(소유종, 이름상수, 서술상수, 명령코드); return true; }
        if (말(소유종, "java/net/Socket") || 말(소유종, "java/net/ServerSocket") || 말(소유종, "java/io/InputStream") || 말(소유종, "java/io/OutputStream")) { 흐름호출(소유종, 이름상수, 서술상수, 명령코드); return true; }
        if (말(소유종, "한국어/자체/keetnerü_ajutuu") && 명령코드 == 184) {
            if (말(이름상수, "화면너비") && 말(서술상수, "()I")) { 넣기(ka_yataayakalü.화면너비(), 1); return true; }
            if (말(이름상수, "화면높이") && 말(서술상수, "()I")) { 넣기(ka_yataayakalü.화면높이(), 1); return true; }
            if (말(이름상수, "밀리초") && 말(서술상수, "()I")) { 넣기(ka_yataayakalü.밀리초(), 1); return true; }
            if (말(이름상수, "그림대기") && 말(서술상수, "()I")) { 넣기(ka_yataayakalü.그림대기(), 1); return true; }
            if (말(이름상수, "사각형") && 말(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), 가로좌표 = 빼기(1); 넣기(ka_yataayakalü.사각형(가로좌표, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (말(소유종, "java/net/InetAddress") || 말(소유종, "java/net/DatagramPacket") || 말(소유종, "java/net/DatagramSocket")) { 통신호출(소유종, 이름상수, 서술상수, 명령코드); return true; }
        if (말(소유종, "java/lang/Thread")) { 가닥호출(이름상수, 서술상수, 명령코드); return true; }
        if (말(소유종, "java/lang/Object")) {
            if (말(이름상수, "<init>") && 말(서술상수, "()V") && 명령코드 == 183) { 객체유효(빼기(2)); return true; }
            if (말(이름상수, "equals") && 말(서술상수, "(Ljava/lang/Object;)Z")) { int waai_atijaaya = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == waai_atijaaya ? 1 : 0, 1); return true; }
        }
        if (예외상수(소유종) != 0) {
            if (말(이름상수, "<init>") && 명령코드 == 183 && (말(서술상수, "()V") || 말(서술상수, "(Ljava/lang/String;)V"))) {
                int a_atapajülü = 말(서술상수, "()V") ? 0 : 빼기(2), 객체참조 = 빼기(2);
                if (객체(객체참조, 9)) { 힙[객체참조 + 3] = a_atapajülü; 힙참조[객체참조 + 3] = 1; } return true;
            }
            if ((말(이름상수, "getMessage") || 말(이름상수, "설명")) && 말(서술상수, "()Ljava/lang/String;")) { int 객체참조 = 빼기(2); if (객체(객체참조, 9)) 넣기(힙[객체참조 + 3], 2); return true; }
        }
        if (말(소유종, "java/lang/String")) {
            if (명령코드 == 182 && 말(이름상수, "getBytes") && (말(서술상수, "()[B") || 말(서술상수, "(Ljava/lang/String;)[B"))) {
                int 부호화이름 = 말(서술상수, "()[B") ? 0 : 빼기(2), 객체참조 = 빼기(2);
                if (!객체(객체참조, 1)) return true;
                if (부호화이름 != 0 && !글같음(부호화이름, epiajatü_jeerü("UTF-8"), false) && !글같음(부호화이름, epiajatü_jeerü("UTF8"), false) && !글같음(부호화이름, epiajatü_jeerü("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int 항목수 = 힙[객체참조 + 1], 반환값 = 할당(20, 항목수 * 3), 사용수 = 0; if (ajachitia) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) {
                    int 문자값 = 힙[객체참조 + 2 + 안쪽자리];
                    if (문자값 >= 0xd800 && 문자값 <= 0xdbff && 안쪽자리 + 1 < 항목수 && 힙[객체참조 + 3 + 안쪽자리] >= 0xdc00 && 힙[객체참조 + 3 + 안쪽자리] <= 0xdfff) 문자값 = 0x10000 + ((문자값 - 0xd800) << 10) + 힙[객체참조 + 2 + ++안쪽자리] - 0xdc00;
                    else if (문자값 >= 0xd800 && 문자값 <= 0xdfff) 문자값 = '?';
                    if (문자값 < 128) 힙[반환값 + 2 + 사용수++] = 문자값;
                    else { int 바이트수 = 문자값 < 2048 ? 2 : 문자값 < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((바이트수 == 2 ? 192 : 바이트수 == 3 ? 224 : 240) | 문자값 >> (6 * (바이트수 - 1))); for (int 비교자리 = 바이트수 - 1; 비교자리 > 0; 비교자리--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | 문자값 >> (6 * (비교자리 - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (명령코드 == 184 && 말(이름상수, "valueOf") && 말(서술상수, "(I)Ljava/lang/String;")) { 넣기(수문자(빼기(1)), 2); return true; }
            if (명령코드 != 182) return false;
            if (말(이름상수, "equals") && 말(서술상수, "(Ljava/lang/Object;)Z")) { int waai_atijaaya = 빼기(2), 첫값 = 빼기(2); if (객체(첫값, 1)) 넣기(글같음(첫값, waai_atijaaya, false) ? 1 : 0, 1); return true; }
            if (말(이름상수, "isEmpty") && 말(서술상수, "()Z")) { int 첫값 = 빼기(2); if (객체(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (말(이름상수, "substring") && (말(서술상수, "(I)Ljava/lang/String;") || 말(서술상수, "(II)Ljava/lang/String;"))) {
                boolean 둘째값 = 말(서술상수, "(II)Ljava/lang/String;"); int 끝자리 = 둘째값 ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (객체(첫값, 1)) 넣기(글조각(첫값, 시작점, 둘째값 ? 끝자리 : 힙[첫값 + 1]), 2); return true;
            }
            if (말(이름상수, "concat") && 말(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int waai_atijaaya = 빼기(2), 첫값 = 빼기(2); 넣기(글합치기(첫값, waai_atijaaya), 2); return true; }
            if (말(이름상수, "hashCode") && 말(서술상수, "()I")) { int 첫값 = 빼기(2), 해시값 = 0; if (객체(첫값, 1)) { for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 힙[첫값 + 1]; eitawaakualü_ee_iyatialujuna++) 해시값 = 해시값 * 31 + 힙[첫값 + 2 + eitawaakualü_ee_iyatialujuna]; 넣기(해시값, 1); } return true; }
            if (말(이름상수, "toString") && 말(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (객체(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (말(소유종, "java/lang/Integer")) {
            if (명령코드 == 184 && 말(이름상수, "valueOf") && 말(서술상수, "(I)Ljava/lang/Integer;")) { int atijaaya_ajutuu = 빼기(1), 객체참조 = atijaaya_ajutuu >= -128 && atijaaya_ajutuu <= 127 ? 정수저장[atijaaya_ajutuu + 128] : 0; if (객체참조 == 0) { 객체참조 = 할당(12, 1); if (!ajachitia) { 힙[객체참조 + 2] = atijaaya_ajutuu; if (atijaaya_ajutuu >= -128 && atijaaya_ajutuu <= 127) 정수저장[atijaaya_ajutuu + 128] = 객체참조; } } 넣기(객체참조, 2); return true; }
            if (명령코드 == 183 && 말(이름상수, "<init>") && 말(서술상수, "(I)V")) { int atijaaya_ajutuu = 빼기(1), 객체참조 = 빼기(2); if (객체(객체참조, 12)) 힙[객체참조 + 2] = atijaaya_ajutuu; return true; }
            if (명령코드 == 182 && 말(이름상수, "intValue") && 말(서술상수, "()I")) { int 객체참조 = 빼기(2); if (객체(객체참조, 12)) 넣기(힙[객체참조 + 2], 1); return true; }
            if (명령코드 == 184 && 말(이름상수, "toString") && 말(서술상수, "(I)Ljava/lang/String;")) { 넣기(수문자(빼기(1)), 2); return true; }
        }
        if (말(소유종, "java/lang/Math") && 명령코드 == 184) {
            if (말(이름상수, "abs") && 말(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((말(이름상수, "min") || 말(이름상수, "max")) && 말(서술상수, "(II)I")) { int waai_atijaaya = 빼기(1), 첫값 = 빼기(1); 넣기(말(이름상수, "min") ? (첫값 < waai_atijaaya ? 첫값 : waai_atijaaya) : (첫값 > waai_atijaaya ? 첫값 : waai_atijaaya), 1); return true; }
        }
        if (말(소유종, "java/lang/System") && 명령코드 == 184) {
            if (말(이름상수, "gc") && 말(서술상수, "()V")) { 수거(); return true; }
            if (말(이름상수, "arraycopy") && 말(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int 항목수 = 빼기(1), jalamüinjatü_ajutuu_ee_iyatialujuna = 빼기(1), waai_atijaaya = 빼기(2), 시작자리 = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(waai_atijaaya)) {
                    int 분류코드 = 힙[첫값];
                    if (힙[waai_atijaaya] != 분류코드 || (분류코드 != 2 && 분류코드 != 3 && (분류코드 < 20 || 분류코드 > 23))) ajachitia_ajutuu("arraycopy type mismatch");
                    else if (항목수 < 0 || 시작자리 < 0 || jalamüinjatü_ajutuu_ee_iyatialujuna < 0 || 시작자리 > 힙[첫값 + 1] - 항목수 || jalamüinjatü_ajutuu_ee_iyatialujuna > 힙[waai_atijaaya + 1] - 항목수) ajachitia_ajutuu("ArrayIndexOutOfBoundsException");
                    else if (첫값 == waai_atijaaya && jalamüinjatü_ajutuu_ee_iyatialujuna > 시작자리) { for (int eitawaakualü_ee_iyatialujuna = 항목수 - 1; eitawaakualü_ee_iyatialujuna >= 0; eitawaakualü_ee_iyatialujuna--) 힙[waai_atijaaya + 2 + jalamüinjatü_ajutuu_ee_iyatialujuna + eitawaakualü_ee_iyatialujuna] = 힙[첫값 + 2 + 시작자리 + eitawaakualü_ee_iyatialujuna]; }
                    else { for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 항목수 && !ajachitia; eitawaakualü_ee_iyatialujuna++) { int atijaaya_ajutuu = 힙[첫값 + 2 + 시작자리 + eitawaakualü_ee_iyatialujuna]; if (분류코드 != 3 || 배열저장가능(waai_atijaaya, atijaaya_ajutuu)) 힙[waai_atijaaya + 2 + jalamüinjatü_ajutuu_ee_iyatialujuna + eitawaakualü_ee_iyatialujuna] = atijaaya_ajutuu; } }
                }
                return true;
            }
        }
        if (말(소유종, "java/util/ArrayList") || 말(소유종, "java/util/List") || 말(소유종, "java/util/HashMap") || 말(소유종, "java/util/Map")) {
            모음호출(소유종, 이름상수, 서술상수, 명령코드); return true;
        }
        return false;
    }
    static void 모음늘리기(int 객체참조, int 필요수) {
        int 이전값 = 힙[객체참조 + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int 다음자리 = 용량값 < 8 ? 8 : 용량값 * 2; if (다음자리 < 필요수) 다음자리 = 필요수;
        int atijaaya_matüriisü = 할당(3, 다음자리); if (ajachitia) return;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 용량값; eitawaakualü_ee_iyatialujuna++) 힙[atijaaya_matüriisü + 2 + eitawaakualü_ee_iyatialujuna] = 힙[이전값 + 2 + eitawaakualü_ee_iyatialujuna];
        힙[객체참조 + 2] = atijaaya_matüriisü; 힙참조[객체참조 + 2] = 1;
    }
    static void 모음호출(int 소유종, int 이름상수, int 서술상수, int 명령코드) {
        boolean 대응참조 = 말(소유종, "java/util/HashMap") || 말(소유종, "java/util/Map"); int 분류코드 = 대응참조 ? 11 : 10;
        if (말(이름상수, "<init>") && 명령코드 == 183 && 말(서술상수, "()V")) { int 객체참조 = 빼기(2); if (객체(객체참조, 분류코드)) 모음늘리기(객체참조, 8); return; }
        if (명령코드 != 182 && 명령코드 != 185) { ajachitia_ajutuu("invalid collection invocation"); return; }
        if (말(이름상수, "size") && 말(서술상수, "()I") || 말(이름상수, "isEmpty") && 말(서술상수, "()Z")) {
            int 객체참조 = 빼기(2); if (객체(객체참조, 분류코드)) 넣기(말(이름상수, "size") ? 힙[객체참조 + 3] : 힙[객체참조 + 3] == 0 ? 1 : 0, 1); return;
        }
        if (말(이름상수, "clear") && 말(서술상수, "()V")) { int 객체참조 = 빼기(2); if (객체(객체참조, 분류코드)) { int atijaaya_matüriisü = 힙[객체참조 + 2]; for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 힙[atijaaya_matüriisü + 1]; eitawaakualü_ee_iyatialujuna++) 힙[atijaaya_matüriisü + 2 + eitawaakualü_ee_iyatialujuna] = 0; 힙[객체참조 + 3] = 0; } return; }
        if (!대응참조 && 말(이름상수, "add") && 말(서술상수, "(Ljava/lang/Object;)Z")) {
            int atijaaya_ajutuu = 빼기(2), 객체참조 = 빼기(2); if (!객체(객체참조, 10)) return;
            int 항목수 = 힙[객체참조 + 3]; 모음늘리기(객체참조, 항목수 + 1); if (!ajachitia) { 힙[힙[객체참조 + 2] + 2 + 항목수] = atijaaya_ajutuu; 힙[객체참조 + 3] = 항목수 + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (말(이름상수, "get") || 말(이름상수, "remove")) && 말(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && 말(이름상수, "set") && 말(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = 말(이름상수, "set"); int atijaaya_ajutuu = 지정여부 ? 빼기(2) : 0, 항목자리 = 빼기(1), 객체참조 = 빼기(2);
            if (!객체(객체참조, 10)) return;
            int 항목수 = 힙[객체참조 + 3], atijaaya_matüriisü = 힙[객체참조 + 2];
            if (항목자리 < 0 || 항목자리 >= 항목수) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[atijaaya_matüriisü + 2 + 항목자리];
            if (지정여부) 힙[atijaaya_matüriisü + 2 + 항목자리] = atijaaya_ajutuu;
            if (말(이름상수, "remove")) { for (int eitawaakualü_ee_iyatialujuna = 항목자리 + 1; eitawaakualü_ee_iyatialujuna < 항목수; eitawaakualü_ee_iyatialujuna++) 힙[atijaaya_matüriisü + 1 + eitawaakualü_ee_iyatialujuna] = 힙[atijaaya_matüriisü + 2 + eitawaakualü_ee_iyatialujuna]; 힙[atijaaya_matüriisü + 1 + 항목수] = 0; 힙[객체참조 + 3] = 항목수 - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (말(이름상수, "get") || 말(이름상수, "remove")) && 말(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && 말(이름상수, "put") && 말(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && 말(이름상수, "containsKey") && 말(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = 말(이름상수, "put"), 제거여부 = 말(이름상수, "remove");
            int atijaaya_ajutuu = 넣기여부 ? 빼기(2) : 0, 키참조 = 빼기(2), 객체참조 = 빼기(2); if (!객체(객체참조, 11)) return;
            int 항목수 = 힙[객체참조 + 3], atijaaya_matüriisü = 힙[객체참조 + 2], 찾은여부 = -1;
            for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 항목수; eitawaakualü_ee_iyatialujuna++) if (값같음(키참조, 힙[atijaaya_matüriisü + 2 + 2 * eitawaakualü_ee_iyatialujuna])) { 찾은여부 = eitawaakualü_ee_iyatialujuna; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[atijaaya_matüriisü + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(객체참조, (항목수 + 1) * 2); atijaaya_matüriisü = 힙[객체참조 + 2]; 찾은여부 = 항목수; if (!ajachitia) 힙[객체참조 + 3] = 항목수 + 1; }
                if (!ajachitia) { 힙[atijaaya_matüriisü + 2 + 2 * 찾은여부] = 키참조; 힙[atijaaya_matüriisü + 3 + 2 * 찾은여부] = atijaaya_ajutuu; }
            }
            if (제거여부 && 찾은여부 >= 0) { for (int eitawaakualü_ee_iyatialujuna = 찾은여부 + 1; eitawaakualü_ee_iyatialujuna < 항목수; eitawaakualü_ee_iyatialujuna++) { 힙[atijaaya_matüriisü + 2 * eitawaakualü_ee_iyatialujuna] = 힙[atijaaya_matüriisü + 2 + 2 * eitawaakualü_ee_iyatialujuna]; 힙[atijaaya_matüriisü + 1 + 2 * eitawaakualü_ee_iyatialujuna] = 힙[atijaaya_matüriisü + 3 + 2 * eitawaakualü_ee_iyatialujuna]; } 힙[atijaaya_matüriisü + 2 * 항목수] = 0; 힙[atijaaya_matüriisü + 1 + 2 * 항목수] = 0; 힙[객체참조 + 3] = 항목수 - 1; }
            if (말(이름상수, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        ajachitia_ajutuu("unsupported collection method");
    }
    static boolean 잠금얻기(int 객체참조) {
        if (!객체유효(객체참조)) return false;
        if (잠금깊이[객체참조] != 0 && 잠금주인[객체참조] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        잠금주인[객체참조] = 현재가닥 + 1; 잠금깊이[객체참조]++; return true;
    }
    static void 잠금풀기(int 객체참조) {
        if (!객체유효(객체참조)) return;
        if (잠금깊이[객체참조] == 0 || 잠금주인[객체참조] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[객체참조] == 0) 잠금주인[객체참조] = 0;
    }
    static boolean 가닥바꾸기() {
        akumajia_ipa_otpünaa[현재가닥] = otpünaa_ee_iyatialujuna;
        if (otpünaa_ee_iyatialujuna < 현재가닥 * 32) akumajia_ipa_jamakua_iparülein[현재가닥] = 3;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 가닥수; eitawaakualü_ee_iyatialujuna++) if (akumajia_ipa_jamakua_iparülein[eitawaakualü_ee_iyatialujuna] == 2 && akumajia_ipa_jamakua_iparülein[가닥대기[eitawaakualü_ee_iyatialujuna]] == 3) akumajia_ipa_jamakua_iparülein[eitawaakualü_ee_iyatialujuna] = 1;
        for (int eitawaakualü_ee_iyatialujuna = 1; eitawaakualü_ee_iyatialujuna <= 가닥수; eitawaakualü_ee_iyatialujuna++) {
            int 다음자리 = (현재가닥 + eitawaakualü_ee_iyatialujuna) % 가닥수;
            if (akumajia_ipa_jamakua_iparülein[다음자리] == 1) { 현재가닥 = 다음자리; otpünaa_ee_iyatialujuna = akumajia_ipa_otpünaa[다음자리]; 바꿈요청 = false; return true; }
        }
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 가닥수; eitawaakualü_ee_iyatialujuna++) if (akumajia_ipa_jamakua_iparülein[eitawaakualü_ee_iyatialujuna] != 3) { ajachitia_ajutuu("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int 이름상수, int 서술상수, int 명령코드) { 가닥처리(이름상수, 서술상수, 명령코드, false); }
    static void 가닥처리(int 이름상수, int 서술상수, int 명령코드, boolean 한국어) {
        if (명령코드 == 184 && 말(이름상수, 한국어 ? "양보하기" : "yield") && 말(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (명령코드 == 184 && 말(이름상수, "currentThread") && 말(서술상수, "()Ljava/lang/Thread;")) { 넣기(가닥객체[현재가닥], 2); return; }
        if (명령코드 == 183 && 말(이름상수, "<init>") && (말(서술상수, "()V") || 말(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int 대상값 = 말(서술상수, "()V") ? 0 : 빼기(2), 객체참조 = 빼기(2);
            if (!객체유효(객체참조)) return;
            if (힙[객체참조] == 13) { 힙[객체참조 + 2] = 대상값; 힙참조[객체참조 + 2] = 1; }
            else if (대상값 != 0) ajachitia_ajutuu("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (명령코드 == 182 && (말(이름상수, 한국어 ? "achuwalaa_aa_innajatü" : "start") || 말(이름상수, 한국어 ? "기다리기" : "join")) && 말(서술상수, "()V") || 명령코드 == 182 && 말(이름상수, 한국어 ? "살아있는가" : "isAlive") && 말(서술상수, "()Z")) {
            int 객체참조 = 빼기(2); if (!객체유효(객체참조)) return;
            int ayaawatiaayaa_ajutuu = -1; for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 가닥수; eitawaakualü_ee_iyatialujuna++) if (가닥객체[eitawaakualü_ee_iyatialujuna] == 객체참조) ayaawatiaayaa_ajutuu = eitawaakualü_ee_iyatialujuna;
            if (말(이름상수, 한국어 ? "살아있는가" : "isAlive")) { 넣기(ayaawatiaayaa_ajutuu >= 0 && akumajia_ipa_jamakua_iparülein[ayaawatiaayaa_ajutuu] != 3 ? 1 : 0, 1); return; }
            if (말(이름상수, 한국어 ? "기다리기" : "join")) { if (ayaawatiaayaa_ajutuu >= 0 && akumajia_ipa_jamakua_iparülein[ayaawatiaayaa_ajutuu] != 3) { 가닥대기[현재가닥] = ayaawatiaayaa_ajutuu; akumajia_ipa_jamakua_iparülein[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (ayaawatiaayaa_ajutuu >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (가닥수 == 4) { ajachitia_ajutuu("thread limit (4 including main)"); return; }
            int 대상값 = 힙[객체참조] == 13 ? 힙[객체참조 + 2] : 객체참조;
            int anaajaalaa_ee_iyatialujuna = 대상값 > 0 && 힙[대상값] >= 32 ? 이름함수(힙[대상값] - 32, 한국어 ? "실행하기" : "run", "()V") : -1;
            if (대상값 != 0 && anaajaalaa_ee_iyatialujuna < 0) { ajachitia_ajutuu("Runnable.run required"); return; }
            ayaawatiaayaa_ajutuu = 가닥수++; 가닥객체[ayaawatiaayaa_ajutuu] = 객체참조; 가닥대상[ayaawatiaayaa_ajutuu] = 대상값;
            int otpünaa = ayaawatiaayaa_ajutuu * 32; akumajia_ipa_otpünaa[ayaawatiaayaa_ajutuu] = anaajaalaa_ee_iyatialujuna < 0 ? otpünaa - 1 : otpünaa; akumajia_ipa_jamakua_iparülein[ayaawatiaayaa_ajutuu] = anaajaalaa_ee_iyatialujuna < 0 ? 3 : 1;
            if (anaajaalaa_ee_iyatialujuna >= 0) { 틀함수[otpünaa] = anaajaalaa_ee_iyatialujuna; 틀위치[otpünaa] = 함수시작[anaajaalaa_ee_iyatialujuna]; 지역값[otpünaa * 128] = 대상값; 지역형[otpünaa * 128] = 2; }
            return;
        }
        ajachitia_ajutuu("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], 주소글 = new int[16];
    static int 지역주소() { return 주소객체(0x7f000001); }
    static int 주소객체(int ajutuu) { int 객체참조 = 할당(14, 1); if (!ajachitia) 힙[객체참조 + 2] = ajutuu; return 객체참조; }
    static int 주소해독(int 객체참조) {
        if (객체참조 == 0 || 글같음(객체참조, epiajatü_jeerü("localhost"), false)) return 0x7f000001;
        if (!객체(객체참조, 1)) return 0;
        int atijaaya_ajutuu = 0, 총수 = 0, ejepüsee_waai = 0, 자릿수 = 0, 항목수 = 힙[객체참조 + 1];
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna <= 항목수; eitawaakualü_ee_iyatialujuna++) {
            int 문자값 = eitawaakualü_ee_iyatialujuna == 항목수 ? '.' : 힙[객체참조 + 2 + eitawaakualü_ee_iyatialujuna];
            if (문자값 == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } atijaaya_ajutuu = atijaaya_ajutuu << 8 | ejepüsee_waai; 총수++; ejepüsee_waai = 자릿수 = 0; }
            else { if (문자값 < '0' || 문자값 > '9' || ++자릿수 > 3 || (ejepüsee_waai = ejepüsee_waai * 10 + 문자값 - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return atijaaya_ajutuu;
    }
    static int ejepüsee_jeerü(int atijaaya_ajutuu) {
        int 항목수 = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int ejepüsee_waai = atijaaya_ajutuu >>> 이동비트 & 255;
            if (ejepüsee_waai >= 100) 주소글[항목수++] = '0' + ejepüsee_waai / 100;
            if (ejepüsee_waai >= 10) 주소글[항목수++] = '0' + ejepüsee_waai / 10 % 10;
            주소글[항목수++] = '0' + ejepüsee_waai % 10; if (이동비트 != 0) 주소글[항목수++] = '.';
        }
        int 객체참조 = 할당(1, 항목수); if (!ajachitia) for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 항목수; eitawaakualü_ee_iyatialujuna++) 힙[객체참조 + 2 + eitawaakualü_ee_iyatialujuna] = 주소글[eitawaakualü_ee_iyatialujuna]; return 객체참조;
    }
    static void 통신호출(int 소유종, int 이름상수, int 서술상수, int 명령코드) {
        if (말(소유종, "java/net/InetAddress")) {
            if (명령코드 == 184 && 말(이름상수, "getLoopbackAddress") && 말(서술상수, "()Ljava/net/InetAddress;")) { 넣기(지역주소(), 2); return; }
            if (명령코드 == 184 && 말(이름상수, "getByName") && 말(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int atijaaya_ajutuu = 주소해독(빼기(2)); if (던진객체 == 0 && !ajachitia) 넣기(주소객체(atijaaya_ajutuu), 2); return;
            }
            if (명령코드 == 182 && 말(이름상수, "getHostAddress") && 말(서술상수, "()Ljava/lang/String;")) { int 객체참조 = 빼기(2); if (객체(객체참조, 14)) 넣기(ejepüsee_jeerü(힙[객체참조 + 2]), 2); return; }
        }
        if (말(소유종, "java/net/DatagramPacket")) {
            if (명령코드 == 183 && 말(이름상수, "<init>") && (말(서술상수, "([BI)V") || 말(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean 목적참조 = 말(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = 목적참조 ? 빼기(1) : 0, 주소참조 = 목적참조 ? 빼기(2) : 0;
                int 항목수 = 빼기(1), atijaaya_matüriisü = 빼기(2), 객체참조 = 빼기(2);
                if (!객체(객체참조, 16) || !객체(atijaaya_matüriisü, 20)) return;
                if (항목수 < 0 || 항목수 > 힙[atijaaya_matüriisü + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (주소참조 != 0 && !객체(주소참조, 14)) return;
                힙[객체참조 + 2] = atijaaya_matüriisü; 힙참조[객체참조 + 2] = 1; 힙[객체참조 + 3] = 항목수;
                힙[객체참조 + 4] = 주소참조; 힙참조[객체참조 + 4] = 1; 힙[객체참조 + 5] = 접속번호; return;
            }
            if (명령코드 == 182 && 말(이름상수, "setLength") && 말(서술상수, "(I)V")) {
                int 항목수 = 빼기(1), 객체참조 = 빼기(2); if (!객체(객체참조, 16)) return;
                if (항목수 < 0 || 항목수 > 힙[힙[객체참조 + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[객체참조 + 3] = 항목수; return;
            }
            if (명령코드 == 182 && (말(이름상수, "getData") && 말(서술상수, "()[B") || 말(이름상수, "getLength") && 말(서술상수, "()I") || 말(이름상수, "getAddress") && 말(서술상수, "()Ljava/net/InetAddress;") || 말(이름상수, "getPort") && 말(서술상수, "()I"))) {
                int 객체참조 = 빼기(2); if (!객체(객체참조, 16)) return;
                int 항목자리 = 말(이름상수, "getData") ? 2 : 말(이름상수, "getLength") ? 3 : 말(이름상수, "getAddress") ? 4 : 5;
                넣기(힙[객체참조 + 항목자리], 항목자리 == 2 || 항목자리 == 4 ? 2 : 1); return;
            }
        }
        if (말(소유종, "java/net/DatagramSocket")) {
            if (명령코드 == 183 && 말(이름상수, "<init>") && (말(서술상수, "()V") || 말(서술상수, "(I)V"))) {
                int 접속번호 = 말(서술상수, "()V") ? 0 : 빼기(1), 객체참조 = 빼기(2); if (!객체(객체참조, 15)) return;
                if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = ka_yataayakalü.통신열기(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[객체참조 + 2] = 열린파일번호; return;
            }
            if (명령코드 == 182 && 말(이름상수, "setSoTimeout") && 말(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), 객체참조 = 빼기(2); if (!객체(객체참조, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[객체참조 + 3] = 밀리초값; return;
            }
            if (명령코드 == 182 && 말(이름상수, "getLocalPort") && 말(서술상수, "()I")) { int 객체참조 = 빼기(2); if (객체(객체참조, 15)) 넣기(힙[객체참조 + 2] < 0 ? -1 : ka_yataayakalü.kusu_outtülee(힙[객체참조 + 2]), 1); return; }
            if (명령코드 == 182 && 말(이름상수, "isClosed") && 말(서술상수, "()Z")) { int 객체참조 = 빼기(2); if (객체(객체참조, 15)) 넣기(힙[객체참조 + 2] < 0 ? 1 : 0, 1); return; }
            if (명령코드 == 182 && 말(이름상수, "close") && 말(서술상수, "()V")) { int 객체참조 = 빼기(2); if (객체(객체참조, 15) && 힙[객체참조 + 2] >= 0) { ka_yataayakalü.파일서술자닫기(힙[객체참조 + 2]); 힙[객체참조 + 2] = -1; } return; }
            if (명령코드 == 182 && (말(이름상수, "send") || 말(이름상수, "receive")) && 말(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int 전문참조 = 빼기(2), 객체참조 = 빼기(2); if (!객체(전문참조, 16) || !객체(객체참조, 15)) return;
                int atijaaya_matüriisü = 힙[전문참조 + 2], 유효길이 = 힙[전문참조 + 3], 열린파일번호 = 힙[객체참조 + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (말(이름상수, "send")) {
                    if (!객체(힙[전문참조 + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 유효길이; eitawaakualü_ee_iyatialujuna++) 통신임시[eitawaakualü_ee_iyatialujuna] = 힙[atijaaya_matüriisü + 2 + eitawaakualü_ee_iyatialujuna];
                    if (ka_yataayakalü.ajütaa_kusu(열린파일번호, 힙[힙[전문참조 + 4] + 2], 힙[전문참조 + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int 항목수 = ka_yataayakalü.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (항목수 == -11) {
                        int 현재시각 = ka_yataayakalü.밀리초();
                        if (힙[객체참조 + 4] == 0) 힙[객체참조 + 4] = 현재시각 + 1;
                        if (힙[객체참조 + 3] > 0 && 현재시각 - (힙[객체참조 + 4] - 1) >= 힙[객체참조 + 3]) { 힙[객체참조 + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(객체참조, 2); 넣기(전문참조, 2); 틀위치[otpünaa_ee_iyatialujuna] = otpünaa_aluwataaya[otpünaa_ee_iyatialujuna]; 바꿈요청 = true; return;
                    }
                    힙[객체참조 + 4] = 0;
                    if (항목수 < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 항목수; eitawaakualü_ee_iyatialujuna++) 힙[atijaaya_matüriisü + 2 + eitawaakualü_ee_iyatialujuna] = (byte)통신임시[eitawaakualü_ee_iyatialujuna];
                    힙[전문참조 + 3] = 항목수; 힙[전문참조 + 4] = 주소객체(통신임시[513]); 힙참조[전문참조 + 4] = 1; 힙[전문참조 + 5] = 통신임시[512];
                }
                return;
            }
        }
        ajachitia_ajutuu("unsupported java.net method");
    }
    static boolean 흐름대기(int 객체참조) {
        int 현재시각 = ka_yataayakalü.밀리초();
        if (힙[객체참조 + 5] == 0) 힙[객체참조 + 5] = 현재시각 + 1;
        if (힙[객체참조 + 3] > 0 && 현재시각 - (힙[객체참조 + 5] - 1) >= 힙[객체참조 + 3]) { 힙[객체참조 + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        틀위치[otpünaa_ee_iyatialujuna] = otpünaa_aluwataaya[otpünaa_ee_iyatialujuna]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int 소유종, int 이름상수, int 서술상수, int 명령코드) {
        boolean 수신쪽 = 말(소유종, "java/net/ServerSocket"), palantüsü = 말(소유종, "java/io/InputStream") || 말(소유종, "java/io/OutputStream");
        if (!palantüsü && 명령코드 == 183 && 말(이름상수, "<init>")) {
            boolean 빈여부 = 말(서술상수, "()V"), 이름지정여부 = 말(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = 말(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && 말(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { ajachitia_ajutuu("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), 주소참조 = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, 객체참조 = 빼기(2);
            if (!객체(객체참조, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !객체(주소참조, 14)) return;
            int kusu_ejepüsee = 이름지정여부 ? 주소해독(주소참조) : 주소지정여부 ? 힙[주소참조 + 2] : 0x7f000001;
            if (ajachitia || 던진객체 != 0) return;
            int 열린파일번호 = ka_yataayakalü.palantüsü_aa_inmajia(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? ka_yataayakalü.palantüsü_aa_inmajia(1, 열린파일번호, 접속번호) : ka_yataayakalü.a_ataa_palantüsü(열린파일번호, kusu_ejepüsee, 접속번호);
            if (처리값 < 0) { ka_yataayakalü.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[객체참조 + 2] = 열린파일번호; 힙[객체참조 + 4] = 접속번호; 힙[객체참조 + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!palantüsü && 말(이름상수, "setSoTimeout") && 말(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), 객체참조 = 빼기(2); if (!객체(객체참조, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[객체참조 + 3] = 밀리초값; return; }
        if (!palantüsü && 말(이름상수, "close") && 말(서술상수, "()V")) { int 객체참조 = 빼기(2); if (객체(객체참조, 수신쪽 ? 18 : 17) && 힙[객체참조 + 2] >= 0) { ka_yataayakalü.파일서술자닫기(힙[객체참조 + 2]); 힙[객체참조 + 2] = -1; } return; }
        if (!palantüsü && (말(이름상수, "getLocalPort") || 말(이름상수, "getPort") || 말(이름상수, "isClosed") || 말(이름상수, "isConnected"))) {
            int 객체참조 = 빼기(2); if (!객체(객체참조, 수신쪽 ? 18 : 17)) return;
            넣기(말(이름상수, "isClosed") ? 힙[객체참조 + 2] < 0 ? 1 : 0 : 말(이름상수, "isConnected") ? 힙[객체참조 + 6] : 말(이름상수, "getPort") ? 힙[객체참조 + 4] : 힙[객체참조 + 2] < 0 ? -1 : ka_yataayakalü.palantüsü_aa_inmajia(4, 힙[객체참조 + 2], 0), 1); return;
        }
        if (수신쪽 && 말(이름상수, "accept") && 말(서술상수, "()Ljava/net/Socket;")) {
            int 객체참조 = 빼기(2); if (!객체(객체참조, 18)) return; int 열린파일번호 = ka_yataayakalü.palantüsü_aa_inmajia(3, 힙[객체참조 + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(객체참조)) 넣기(객체참조, 2); return; }
            힙[객체참조 + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = 할당(17, 5); if (ajachitia) { ka_yataayakalü.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = ka_yataayakalü.palantüsü_aa_inmajia(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !palantüsü && ((말(이름상수, "getInputStream") && 말(서술상수, "()Ljava/io/InputStream;")) || (말(이름상수, "getOutputStream") && 말(서술상수, "()Ljava/io/OutputStream;")))) {
            int 객체참조 = 빼기(2); if (!객체(객체참조, 17)) return; if (힙[객체참조 + 2] < 0 || 힙[객체참조 + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = 할당(19, 4); if (ajachitia) return; 힙[반환값 + 2] = 객체참조; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = 말(이름상수, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (palantüsü) {
            boolean 읽기여부 = 말(이름상수, "read"), 쓰기여부 = 말(이름상수, "write"), 배열여부 = 말(서술상수, "([B)I") || 말(서술상수, "([B)V"), 부분배열여부 = 말(서술상수, "([BII)I") || 말(서술상수, "([BII)V");
            int 항목수 = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, atijaaya_matüriisü = 배열여부 || 부분배열여부 ? 빼기(2) : 0;
            int atijaaya_ajutuu = 쓰기여부 && 말(서술상수, "(I)V") ? 빼기(1) : 0, 객체참조 = 빼기(2);
            if (!객체(객체참조, 19)) return; int 부모참조 = 힙[객체참조 + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (말(이름상수, "close") && 말(서술상수, "()V")) { ka_yataayakalü.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (말(이름상수, "flush") && 말(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[객체참조 + 3] == 0)) { ajachitia_ajutuu("unsupported stream operation"); return; }
            if (배열여부 || 부분배열여부) { if (!객체(atijaaya_matüriisü, 20)) return; if (배열여부) 항목수 = 힙[atijaaya_matüriisü + 1]; if (시작변위 < 0 || 항목수 < 0 || 시작변위 > 힙[atijaaya_matüriisü + 1] - 항목수) { 예외던짐(6, "stream array bounds"); return; } }
            else 항목수 = 1;
            if (항목수 == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[객체참조 + 4] : 0, 처리값 = 0;
            while (완료수 < 항목수) {
                처리값 = 읽기여부 ? ka_yataayakalü.파일한바이트읽기(열린파일번호) : ka_yataayakalü.파일한바이트쓰기(열린파일번호, 배열여부 || 부분배열여부 ? 힙[atijaaya_matüriisü + 2 + 시작변위 + 완료수] : atijaaya_ajutuu);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (배열여부 || 부분배열여부)) 힙[atijaaya_matüriisü + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(배열여부 || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[객체참조 + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(객체참조, 2); if (배열여부 || 부분배열여부) 넣기(atijaaya_matüriisü, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(항목수, 1); } if (쓰기여부 && !(배열여부 || 부분배열여부)) 넣기(atijaaya_ajutuu, 1); } return;
            }
            힙[객체참조 + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : 배열여부 || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        ajachitia_ajutuu("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int 이름상수) {
        if (말(이름상수, "한국어/자체/analaaya")) return 24;
        if (말(이름상수, "한국어/자체/akanüliajaa")) return 26;
        if (말(이름상수, "한국어/자체/ajüttülee")) return 27;
        if (말(이름상수, "한국어/자체/입력칸")) return 28;
        if (말(이름상수, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int 이름상수) {
        return 한국어화면종(이름상수) != 0 || 말(이름상수, "한국어/자체/화면구성요소") || 말(이름상수, "한국어/자체/kasachiki_a_atapajüsüirua");
    }
    static int 화면종(int 이름상수) {
        int 한국어종 = 한국어화면종(이름상수); if (한국어종 != 0) return 한국어종;
        if (말(이름상수, "javax/swing/JFrame")) return 24;
        if (말(이름상수, "javax/swing/JPanel")) return 25;
        if (말(이름상수, "javax/swing/JLabel")) return 26;
        if (말(이름상수, "javax/swing/JButton")) return 27;
        if (말(이름상수, "javax/swing/JTextField")) return 28;
        if (말(이름상수, "java/awt/event/ActionEvent")) return 29;
        if (말(이름상수, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int 이름상수) {
        return 화면종(이름상수) != 0 || 말(이름상수, "java/awt/Component") || 말(이름상수, "java/awt/Container") || 말(이름상수, "javax/swing/JComponent") || 말(이름상수, "javax/swing/AbstractButton") || 말(이름상수, "javax/swing/text/JTextComponent") || 말(이름상수, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int 객체참조) { if (!객체유효(객체참조)) return false; if (힙[객체참조] < 24 || 힙[객체참조] > 28) { ajachitia_ajutuu("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int 객체참조, int 글참조) {
        if (글참조 != 0 && !객체(글참조, 1)) return;
        int 항목수 = 글참조 == 0 ? 0 : 힙[글참조 + 1]; if (항목수 > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 항목수; eitawaakualü_ee_iyatialujuna++) 화면글임시[eitawaakualü_ee_iyatialujuna] = 힙[글참조 + 2 + eitawaakualü_ee_iyatialujuna];
        if (ka_yataayakalü.화면글(힙[객체참조 + 2], 화면글임시, 항목수) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[객체참조 + 3] = 글참조; 힙참조[객체참조 + 3] = 1;
    }
    static int 화면문자읽기(int 객체참조) {
        int ayaawatiaayaa_ajutuu = 힙[객체참조 + 2], 항목수 = ka_yataayakalü.화면연결(8, ayaawatiaayaa_ajutuu, 0, 0, 0, 0), 사용수 = 0;
        if (항목수 < 0) { ajachitia_ajutuu("GUI text read failed"); return 0; }
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 항목수; eitawaakualü_ee_iyatialujuna++) { int 부호값 = ka_yataayakalü.화면연결(9, ayaawatiaayaa_ajutuu, eitawaakualü_ee_iyatialujuna, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = 할당(1, 사용수); if (!ajachitia) for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 사용수; eitawaakualü_ee_iyatialujuna++) 힙[반환값 + 2 + eitawaakualü_ee_iyatialujuna] = 화면글임시[eitawaakualü_ee_iyatialujuna]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 keetnerü_ajutuu 화면 기능에 연결한다. Swing 객체/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int 소유종, int 이름상수, int 서술상수, int 명령코드) {
        if (말(소유종, "한국어/자체/kasachiki_a_atapajüsüirua")) {
            if (명령코드 == 184 && 말(이름상수, "나중에실행") && 말(서술상수, "(L한국어/자체/실행할일;)V")) {
                int aa_innajatü_aa_inra_awai = 빼기(2); if (!객체유효(aa_innajatü_aa_inra_awai)) return;
                if (나중수 == 8) { ajachitia_ajutuu("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = aa_innajatü_aa_inra_awai; return;
            }
            if (명령코드 == 184 && 말(이름상수, "사건처리중인가") && 말(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            ajachitia_ajutuu("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (말(소유종, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!객체(알림, 29) || 힙[알림 + 3] == 0) return;
            if (말(이름상수, "kasachiki_eejeejetülein") && 말(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (말(이름상수, "명령글") && 말(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (말(이름상수, "ee_iyatialujuna") && 말(서술상수, "()I")) 넣기(1001, 1);
            else ajachitia_ajutuu("지원하지 않는 한국어 aa_inra_awai 알림 호출"); return;
        }
        if (명령코드 == 183 && 말(이름상수, "<init>")) {
            int 종류 = 한국어화면종(소유종), 받이 = 0, 가로 = 0, 세로 = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && 말(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (ka_yataayakalü.화면너비() - 폭) / 2; 세로 = (ka_yataayakalü.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && 말(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && 말(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); 세로 = 빼기(1); 가로 = 빼기(1);
            } else { ajachitia_ajutuu("지원하지 않는 한국어 화면 생성자"); return; }
            int 글 = 빼기(2), apüshii_ajutuu = 빼기(2); if (!화면객체(apüshii_ajutuu)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || 세로 < 0 || 폭 > ka_yataayakalü.화면너비() - 가로 || 높이 > ka_yataayakalü.화면높이() - 세로) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int ee_iyatialujuna = ka_yataayakalü.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (ee_iyatialujuna < 1 || ee_iyatialujuna > 32) { ajachitia_ajutuu("화면 apüshii_ajutuu 자리가 가득 찼습니다"); return; }
            힙[apüshii_ajutuu + 2] = ee_iyatialujuna; 화면참조[ee_iyatialujuna - 1] = apüshii_ajutuu;
            힙[apüshii_ajutuu + 5] = 가로; 힙[apüshii_ajutuu + 6] = 세로; 힙[apüshii_ajutuu + 7] = 폭; 힙[apüshii_ajutuu + 8] = 높이; 힙[apüshii_ajutuu + 10] = 2;
            힙[apüshii_ajutuu + 4] = 받이; 힙참조[apüshii_ajutuu + 4] = 1; 힙[apüshii_ajutuu + 12] = 1;
            ka_yataayakalü.화면연결(1, ee_iyatialujuna, 가로, 세로, 폭, 높이);
            if (종류 == 24) ka_yataayakalü.화면연결(7, ee_iyatialujuna, 2, 0, 0, 0);
            화면문자설정(apüshii_ajutuu, 글); return;
        }
        if (명령코드 != 182) { ajachitia_ajutuu("잘못된 한국어 화면 호출 aluwataaya"); return; }
        if (말(이름상수, "글쓰기") && 말(서술상수, "(Ljava/lang/String;)V")) {
            int 글 = 빼기(2), apüshii_ajutuu = 빼기(2); if (화면객체(apüshii_ajutuu)) 화면문자설정(apüshii_ajutuu, 글); return;
        }
        if (말(이름상수, "글읽기") && 말(서술상수, "()Ljava/lang/String;")) {
            int apüshii_ajutuu = 빼기(2); if (화면객체(apüshii_ajutuu)) 넣기(화면문자읽기(apüshii_ajutuu), 2); return;
        }
        if (말(이름상수, "동작맡기기") && 말(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), apüshii_ajutuu = 빼기(2);
            if (화면객체(apüshii_ajutuu)) { 힙[apüshii_ajutuu + 4] = 받이; 힙참조[apüshii_ajutuu + 4] = 1; 힙[apüshii_ajutuu + 12] = 1; } return;
        }
        if (말(이름상수, "담기") && 말(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int apüshii_achiiruajatü_ajutuu = 빼기(2), 부모 = 빼기(2); if (!화면객체(apüshii_achiiruajatü_ajutuu) || !화면객체(부모)) return;
            if (ka_yataayakalü.화면연결(2, 힙[부모 + 2], 힙[apüshii_achiiruajatü_ajutuu + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[apüshii_achiiruajatü_ajutuu + 11] = 부모; 힙참조[apüshii_achiiruajatü_ajutuu + 11] = 1; return;
        }
        if (말(이름상수, "자리정하기") && 말(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), 세로 = 빼기(1), 가로 = 빼기(1), apüshii_ajutuu = 빼기(2); if (!화면객체(apüshii_ajutuu)) return;
            if (ka_yataayakalü.화면연결(1, 힙[apüshii_ajutuu + 2], 가로, 세로, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[apüshii_ajutuu + 5] = 가로; 힙[apüshii_ajutuu + 6] = 세로; 힙[apüshii_ajutuu + 7] = 폭; 힙[apüshii_ajutuu + 8] = 높이; return;
        }
        if ((말(이름상수, "보이기") || 말(이름상수, "asürülaa")) && 말(서술상수, "()V")) {
            boolean ko_upa_awaa_ajutuu = 말(이름상수, "보이기"); int apüshii_ajutuu = 빼기(2); if (!화면객체(apüshii_ajutuu)) return;
            if (ka_yataayakalü.화면연결(ko_upa_awaa_ajutuu ? 3 : 4, 힙[apüshii_ajutuu + 2], ko_upa_awaa_ajutuu ? 1 : 0, 0, 0, 0) < 0) { ajachitia_ajutuu("화면은 atütüjiraaya 명령에서 실행해야 합니다"); return; }
            힙[apüshii_ajutuu + 9] = ko_upa_awaa_ajutuu ? 1 : 0; return;
        }
        if (말(이름상수, "보이는가") && 말(서술상수, "()Z")) { int apüshii_ajutuu = 빼기(2); if (화면객체(apüshii_ajutuu)) 넣기(힙[apüshii_ajutuu + 9], 1); return; }
        ajachitia_ajutuu("지원하지 않는 한국어 화면 메서드");
    }
    static void 화면호출(int 소유종, int 이름상수, int 서술상수, int 명령코드) {
        if (말(소유종, "javax/swing/SwingUtilities")) {
            if (명령코드 == 184 && 말(이름상수, "invokeLater") && 말(서술상수, "(Ljava/lang/Runnable;)V")) { int 객체참조 = 빼기(2); if (!객체유효(객체참조)) return; if (나중수 == 8) { ajachitia_ajutuu("invokeLater queue full"); return; } 나중실행[나중수++] = 객체참조; return; }
            if (명령코드 == 184 && 말(이름상수, "isEventDispatchThread") && 말(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            ajachitia_ajutuu("unsupported SwingUtilities method"); return;
        }
        if (말(소유종, "java/awt/event/ActionEvent")) {
            int 객체참조 = 빼기(2); if (!객체(객체참조, 29)) return;
            if (말(이름상수, "getSource") && 말(서술상수, "()Ljava/lang/Object;")) 넣기(힙[객체참조 + 2], 2);
            else if (말(이름상수, "getActionCommand") && 말(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[객체참조 + 2]), 2);
            else if (말(이름상수, "getID") && 말(서술상수, "()I")) 넣기(1001, 1);
            else ajachitia_ajutuu("unsupported ActionEvent method"); return;
        }
        if (명령코드 == 183 && 말(이름상수, "<init>")) {
            int 열수 = 0, 글참조 = 0;
            if (말(서술상수, "(I)V")) 열수 = 빼기(1);
            else if (말(서술상수, "(Ljava/lang/String;I)V")) { 열수 = 빼기(1); 글참조 = 빼기(2); }
            else if (말(서술상수, "(Ljava/lang/String;)V")) 글참조 = 빼기(2);
            else if (말(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!말(서술상수, "()V")) { ajachitia_ajutuu("unsupported Swing constructor"); return; }
            int 객체참조 = 빼기(2); if (!객체유효(객체참조)) return;
            if (힙[객체참조] == 30) { ajachitia_ajutuu("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(객체참조) || 열수 < 0) return;
            int ayaawatiaayaa_ajutuu = ka_yataayakalü.화면연결(0, 힙[객체참조] - 23, 0, 0, 0, 0);
            if (ayaawatiaayaa_ajutuu < 1 || ayaawatiaayaa_ajutuu > 32) { ajachitia_ajutuu("GUI widget slots exhausted"); return; }
            힙[객체참조 + 2] = ayaawatiaayaa_ajutuu; 화면참조[ayaawatiaayaa_ajutuu - 1] = 객체참조; 힙[객체참조 + 5] = 힙[객체참조] == 24 ? 130 : 16; 힙[객체참조 + 6] = 힙[객체참조] == 24 ? 110 : 16;
            힙[객체참조 + 7] = 힙[객체참조] == 24 ? 380 : 220; 힙[객체참조 + 8] = 힙[객체참조] == 24 ? 240 : 28; 힙[객체참조 + 10] = 1;
            화면문자설정(객체참조, 글참조); return;
        }
        if (말(이름상수, "setText") || 말(이름상수, "setTitle")) { int 글참조 = 빼기(2), 객체참조 = 빼기(2); if (화면객체(객체참조) && 말(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(객체참조, 글참조); return; }
        if (말(이름상수, "getText") || 말(이름상수, "getTitle")) { int 객체참조 = 빼기(2); if (화면객체(객체참조) && 말(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(객체참조), 2); return; }
        if (말(이름상수, "addActionListener") && 말(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), 객체참조 = 빼기(2); if (화면객체(객체참조)) { 힙[객체참조 + 4] = 수신참조; 힙참조[객체참조 + 4] = 1; } return; }
        if (말(이름상수, "getContentPane") && 말(서술상수, "()Ljava/awt/Container;")) { int 객체참조 = 빼기(2); if (화면객체(객체참조)) 넣기(객체참조, 2); return; }
        if (말(이름상수, "setLayout") && 말(서술상수, "(Ljava/awt/LayoutManager;)V")) { int 배치참조 = 빼기(2), 객체참조 = 빼기(2); if (화면객체(객체참조) && 배치참조 != 0) ajachitia_ajutuu("only absolute layout (null) is supported"); return; }
        if (말(이름상수, "add") && (말(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || 말(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean akumajiakuai_pa_mülein = 말(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (akumajiakuai_pa_mülein) 빼기(2);
            int 자식참조 = 빼기(2), 객체참조 = 빼기(2); if (!화면객체(자식참조) || !화면객체(객체참조)) return;
            if (ka_yataayakalü.화면연결(2, 힙[객체참조 + 2], 힙[자식참조 + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[자식참조 + 11] = 객체참조; 힙참조[자식참조 + 11] = 1; if (!akumajiakuai_pa_mülein) 넣기(자식참조, 2); return;
        }
        if (말(이름상수, "setBounds") && 말(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), 가로좌표 = 빼기(1), 객체참조 = 빼기(2); if (!화면객체(객체참조)) return;
            if (ka_yataayakalü.화면연결(1, 힙[객체참조 + 2], 가로좌표, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[객체참조 + 5] = 가로좌표; 힙[객체참조 + 6] = 세로좌표; 힙[객체참조 + 7] = 너비; 힙[객체참조 + 8] = 높이; return;
        }
        if (말(이름상수, "setSize") && 말(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 객체참조 = 빼기(2); if (!화면객체(객체참조)) return;
            if (ka_yataayakalü.화면연결(1, 힙[객체참조 + 2], 힙[객체참조 + 5], 힙[객체참조 + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[객체참조 + 7] = 너비; 힙[객체참조 + 8] = 높이; } return;
        }
        if (말(이름상수, "setLocationRelativeTo") && 말(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), 객체참조 = 빼기(2); if (!화면객체(객체참조)) return; if (상대배치 != 0) { ajachitia_ajutuu("only screen centering supported"); return; } 힙[객체참조 + 5] = (ka_yataayakalü.화면너비() - 힙[객체참조 + 7]) / 2; 힙[객체참조 + 6] = (ka_yataayakalü.화면높이() - 힙[객체참조 + 8]) / 2; ka_yataayakalü.화면연결(1, 힙[객체참조 + 2], 힙[객체참조 + 5], 힙[객체참조 + 6], 힙[객체참조 + 7], 힙[객체참조 + 8]); return; }
        if (말(이름상수, "setDefaultCloseOperation") && 말(서술상수, "(I)V")) { int 종료정책 = 빼기(1), 객체참조 = 빼기(2); if (화면객체(객체참조)) { if (종료정책 < 0 || 종료정책 > 3) 예외던짐(9, "close policy"); else { 힙[객체참조 + 10] = 종료정책; ka_yataayakalü.화면연결(7, 힙[객체참조 + 2], 종료정책, 0, 0, 0); } } return; }
        if (말(이름상수, "setVisible") && 말(서술상수, "(Z)V")) { int atijaaya_ajutuu = 빼기(1), 객체참조 = 빼기(2); if (화면객체(객체참조)) { int 처리값 = ka_yataayakalü.화면연결(3, 힙[객체참조 + 2], atijaaya_ajutuu, 0, 0, 0); if (처리값 < 0) ajachitia_ajutuu("Swing requires a standalone interactive command"); else 힙[객체참조 + 9] = atijaaya_ajutuu; } return; }
        if (말(이름상수, "dispose") && 말(서술상수, "()V")) { int 객체참조 = 빼기(2); if (화면객체(객체참조)) { ka_yataayakalü.화면연결(4, 힙[객체참조 + 2], 0, 0, 0, 0); 힙[객체참조 + 9] = 0; } return; }
        if (말(이름상수, "repaint") || 말(이름상수, "validate")) { int 객체참조 = 빼기(2); if (!화면객체(객체참조) || !말(서술상수, "()V")) return; ka_yataayakalü.화면연결(1, 힙[객체참조 + 2], 힙[객체참조 + 5], 힙[객체참조 + 6], 힙[객체참조 + 7], 힙[객체참조 + 8]); return; }
        if (말(이름상수, "isVisible") && 말(서술상수, "()Z")) { int 객체참조 = 빼기(2); if (화면객체(객체참조)) 넣기(힙[객체참조 + 9], 1); return; }
        ajachitia_ajutuu("unsupported Swing method (native subset)");
    }
    static void 사건실행(int 대상값, int 사건번호, boolean 한국어) {
        if (대상값 < 1 || 힙[대상값] < 32) { ajachitia_ajutuu("Java event listener required"); return; }
        int anaajaalaa_ee_iyatialujuna = 이름함수(힙[대상값] - 32, 사건번호 == 0 ? (한국어 ? "실행하기" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (anaajaalaa_ee_iyatialujuna < 0) { ajachitia_ajutuu("event callback missing"); return; }
        현재가닥 = 0; 가닥수 = 1; otpünaa_ee_iyatialujuna = 0; akumajia_ipa_jamakua_iparülein[0] = 1; 틀스택[0] = 0; 틀잠금[0] = anaajaa_otpünaa[0] = 0; 바꿈요청 = false;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 128; eitawaakualü_ee_iyatialujuna++) { 지역값[eitawaakualü_ee_iyatialujuna] = 지역형[eitawaakualü_ee_iyatialujuna] = 0; }
        틀함수[0] = anaajaalaa_ee_iyatialujuna; 틀위치[0] = 함수시작[anaajaalaa_ee_iyatialujuna]; 지역값[0] = 대상값; 지역형[0] = 2;
        if (사건번호 != 0) { 지역값[1] = 사건번호; 지역형[1] = 2; }
        사건중 = true; 실행(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!ajachitia) {
            if (나중수 > 0) { int 대상값 = 나중실행[0], 한국어 = 나중한국어[0]; for (int eitawaakualü_ee_iyatialujuna = 1; eitawaakualü_ee_iyatialujuna < 나중수; eitawaakualü_ee_iyatialujuna++) { 나중실행[eitawaakualü_ee_iyatialujuna - 1] = 나중실행[eitawaakualü_ee_iyatialujuna]; 나중한국어[eitawaakualü_ee_iyatialujuna - 1] = 나중한국어[eitawaakualü_ee_iyatialujuna]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(대상값, 0, 한국어 != 0); continue; }
            if (ka_yataayakalü.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = ka_yataayakalü.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { ajachitia_ajutuu("GUI event I/O failed"); return; }
            int ayaawatiaayaa_ajutuu = 사건번호 & 65535; if (ayaawatiaayaa_ajutuu < 1 || ayaawatiaayaa_ajutuu > 32) continue; int 객체참조 = 화면참조[ayaawatiaayaa_ajutuu - 1]; if (객체참조 == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[객체참조 + 10] != 0) 힙[객체참조 + 9] = 0;
                if (힙[객체참조 + 10] == 3) for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 32; eitawaakualü_ee_iyatialujuna++) if (화면참조[eitawaakualü_ee_iyatialujuna] != 0 && 힙[화면참조[eitawaakualü_ee_iyatialujuna]] == 24) ka_yataayakalü.화면연결(4, eitawaakualü_ee_iyatialujuna + 1, 0, 0, 0, 0);
            } else if (힙[객체참조 + 4] != 0) {
                int 안내참조 = 할당(29, 2); if (ajachitia) return; 힙[안내참조 + 2] = 객체참조; 힙[안내참조 + 3] = 힙[객체참조 + 12]; 힙참조[안내참조 + 2] = 1; 사건실행(힙[객체참조 + 4], 안내참조, 힙[객체참조 + 12] != 0);
            }
        }
    }
    public static int 시작() {
        if (ka_yataayakalü.인수개수() == 1 && 자바도구.같음(ka_yataayakalü.인수(0), "-version")) {
            ka_yataayakalü.ashajaa("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (ka_yataayakalü.인수개수() < 1) { ka_yataayakalü.ashajaa("Usage: java CLASS [ARGS]\n"); return 2; }
        시작종 = 종적재(epiajatü_jeerü(ka_yataayakalü.인수(0))); if (ajachitia || 시작종 < 0) return 1;
        int ekeroliaa_o_uchikanain_ajutuu = 이름함수(시작종, "시작", "()V");
        boolean 한국어진입 = ekeroliaa_o_uchikanain_ajutuu >= 0 && (함수권한[ekeroliaa_o_uchikanain_ajutuu] & 9) == 9;
        if (!한국어진입) ekeroliaa_o_uchikanain_ajutuu = 이름함수(시작종, "main", "([Ljava/lang/String;)V");
        if (ekeroliaa_o_uchikanain_ajutuu < 0 || (함수권한[ekeroliaa_o_uchikanain_ajutuu] & 9) != 9) ajachitia_ajutuu("public static void 시작() or main(String[] args) required");
        if (ajachitia) return 1;
        int 인수 = 할당(3, ka_yataayakalü.인수개수() - 1); matüriisü_apüshii[인수] = -1;
        for (int 수 = 1; 수 < ka_yataayakalü.인수개수() && !ajachitia; 수++) 힙[인수 + 1 + 수] = epiajatü_jeerü(ka_yataayakalü.인수(수));
        otpünaa_ee_iyatialujuna = 0; 틀함수[0] = ekeroliaa_o_uchikanain_ajutuu; 틀위치[0] = 함수시작[ekeroliaa_o_uchikanain_ajutuu]; 지역값[0] = 한국어진입 ? 0 : 인수; 지역형[0] = 한국어진입 ? 0 : 2;
        akumajia_ipa_jamakua_iparülein[0] = 1; 가닥객체[0] = 할당(13, 2);
        실행(); if (!ajachitia) 화면사건들(); return ajachitia ? 1 : 0;
    }
}
