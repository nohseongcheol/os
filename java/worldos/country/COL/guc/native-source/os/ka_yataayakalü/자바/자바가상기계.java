// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. anaajaalaa/스택/참조/분기 경계를 실행 중 검사한다. */
public final class 자바가상기계 {
    static int[] anaajaalaa = new int[16384], 파일명 = new int[64];
    static int[] waneepiajutu_akanüliajia = new int[512], 상가 = new int[512], 상나 = new int[512], 문자열참조 = new int[512];
    static int[] 함수명 = new int[32], 함수형 = new int[32], 함수권한 = new int[32];
    static int[] 함수시작 = new int[32], 함수끝 = new int[32], 함수스택 = new int[32], 함수지역 = new int[32];
    static int[] 함수인수수 = new int[32], 함수인수형 = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] 지역값 = new int[4096], 지역형 = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] 틀함수 = new int[32], 틀위치 = new int[32], 틀스택 = new int[32];
    static int[] 힙 = new int[8192];
    static int 크기, 읽기위치, 상수수, 함수수, 클래스명, otpünaa_ee_iyatialujuna = -1, 힙끝 = 1, 반환형;
    static boolean ajachitia;

    static void ajachitia_ajutuu(String 말) {
        if (!ajachitia) { ka_yataayakalü.ashajaa("JVM error: "); ka_yataayakalü.ashajaa(말); ka_yataayakalü.ashajaa_jeerü_ajutuu(10); }
        ajachitia = true;
    }
    static boolean külipü_ayaakuaapijana(int 시작, int akaliaa_ajutuu) { return 시작 >= 0 && akaliaa_ajutuu >= 0 && 시작 <= 크기 - akaliaa_ajutuu; }
    static int waai_ajutuu() {
        if (!külipü_ayaakuaapijana(읽기위치, 1)) { ajachitia_ajutuu("truncated class file"); return 0; }
        return anaajaalaa[읽기위치++];
    }
    static int 짧은수() { return waai_ajutuu() << 8 | waai_ajutuu(); }
    static int waneepiasü() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int akaliaa_ajutuu) { if (!külipü_ayaakuaapijana(읽기위치, akaliaa_ajutuu)) ajachitia_ajutuu("invalid attribute size"); else 읽기위치 += akaliaa_ajutuu; }
    static boolean cheeke_waneepiajutu(int 수, int 종류) {
        if (수 <= 0 || 수 >= 상수수 || waneepiajutu_akanüliajia[수] != 종류) { ajachitia_ajutuu("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int 시작, int akaliaa_ajutuu, String 말) {
        if (!külipü_ayaakuaapijana(시작, akaliaa_ajutuu) || akaliaa_ajutuu != 말.length()) return false;
        for (int 수 = 0; 수 < akaliaa_ajutuu; 수++) if (anaajaalaa[시작 + 수] != 말.charAt(수)) return false;
        return true;
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
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !ajachitia; 수++) { cheeke_waneepiajutu(짧은수(), 1); 건너(waneepiasü()); }
    }
    static int aluwataaya_akaliaa(int ajutuu) {
        if (ajutuu == 16 || ajutuu == 18 || ajutuu == 21 || ajutuu == 25 || ajutuu == 54 || ajutuu == 58 || ajutuu == 188) return 2;
        if (ajutuu == 17 || ajutuu == 19 || ajutuu == 132 || ajutuu >= 153 && ajutuu <= 167
            || ajutuu >= 178 && ajutuu <= 184 || ajutuu == 187 || ajutuu == 189 || ajutuu == 192 || ajutuu == 198 || ajutuu == 199) return 3;
        if (ajutuu >= 0 && ajutuu <= 8 || ajutuu >= 26 && ajutuu <= 29 || ajutuu >= 42 && ajutuu <= 46 || ajutuu == 50
            || ajutuu >= 59 && ajutuu <= 62 || ajutuu >= 75 && ajutuu <= 79 || ajutuu == 83 || ajutuu == 87 || ajutuu == 89 || ajutuu == 95
            || ajutuu == 96 || ajutuu == 100 || ajutuu == 104 || ajutuu == 108 || ajutuu == 112 || ajutuu == 116
            || ajutuu == 120 || ajutuu == 122 || ajutuu == 124 || ajutuu == 126 || ajutuu == 128 || ajutuu == 130
            || ajutuu >= 145 && ajutuu <= 147 || ajutuu == 172 || ajutuu == 176 || ajutuu == 177 || ajutuu == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (waneepiasü() != 0xcafebabe) ajachitia_ajutuu("not a class file");
        int 부판 = 짧은수(), 판 = 짧은수();
        if (판 < 45 || 판 > 52 || 부판 != 0) ajachitia_ajutuu("supported class versions: 45..52, minor 0");
        상수수 = 짧은수();
        if (상수수 < 1 || 상수수 > 512) { ajachitia_ajutuu("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < 상수수 && !ajachitia; 수++) {
            int 종류 = waai_ajutuu(); waneepiajutu_akanüliajia[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = waneepiasü();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); 상나[수] = 짧은수(); }
            else ajachitia_ajutuu("unsupported constant type");
        }
        int 권한 = 짧은수();
        if ((권한 & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) ajachitia_ajutuu("unsupported class flags");
        클래스명 = 클래스문자(짧은수());
        if (!말(클래스문자(짧은수()), "java/lang/Object")) ajachitia_ajutuu("inheritance unsupported");
        if (짧은수() != 0) ajachitia_ajutuu("interfaces unsupported");
        if (짧은수() != 0) ajachitia_ajutuu("fields unsupported");
        함수수 = 짧은수();
        if (함수수 < 1 || 함수수 > 32) { ajachitia_ajutuu("method count limit (32)"); return; }
        for (int 수 = 0; 수 < 함수수 && !ajachitia; 수++) {
            함수권한[수] = 짧은수(); 함수명[수] = 짧은수(); 함수형[수] = 짧은수();
            cheeke_waneepiajutu(함수명[수], 1); 서술읽기(수);
            if ((함수권한[수] & (0x100 | 0x400 | 0x20)) != 0) ajachitia_ajutuu("native, abstract and synchronized methods unsupported");
            if ((함수권한[수] & 8) == 0 && !말(함수명[수], "<init>")) ajachitia_ajutuu("instance methods unsupported");
            if (말(함수명[수], "<clinit>")) ajachitia_ajutuu("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(함수명[앞], 함수명[수]) && 같은말(함수형[앞], 함수형[수])) ajachitia_ajutuu("duplicate method");
            int 개수 = 짧은수();
            for (int anaajaalaakua_ipa_ajutuu = 0; anaajaalaakua_ipa_ajutuu < 개수 && !ajachitia; anaajaalaakua_ipa_ajutuu++) {
                int 이름 = 짧은수(), akaliaa_ajutuu = waneepiasü(), 시작 = 읽기위치;
                if (!külipü_ayaakuaapijana(시작, akaliaa_ajutuu)) { ajachitia_ajutuu("truncated method attribute"); break; }
                if (말(이름, "Code")) {
                    if (함수시작[수] != 0) ajachitia_ajutuu("duplicate Code attribute");
                    함수스택[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = waneepiasü();
                    if (함수스택[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) ajachitia_ajutuu("method memory limits exceeded");
                    함수시작[수] = 읽기위치; 건너(코드길이); 함수끝[수] = 읽기위치;
                    if (짧은수() != 0) ajachitia_ajutuu("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != 시작 + akaliaa_ajutuu) ajachitia_ajutuu("Code attribute size mismatch");
                } else 건너(akaliaa_ajutuu);
            }
            if (함수시작[수] == 0) ajachitia_ajutuu("missing Code attribute");
            int 칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !ajachitia) {
                int akaliaa_ajutuu = aluwataaya_akaliaa(anaajaalaa[칸]);
                if (akaliaa_ajutuu == 0 || akaliaa_ajutuu > 함수끝[수] - 칸) { ajachitia_ajutuu("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += akaliaa_ajutuu;
            }
            // 실행하지 않는 경로에도 잘못된 분기 목적지를 허용하지 않는다.
            칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !ajachitia) {
                int ajutuu = anaajaalaa[칸];
                if (ajutuu >= 153 && ajutuu <= 167 || ajutuu == 198 || ajutuu == 199) {
                    int jalamüinjatü_ajutuu = 칸 + (short)(anaajaalaa[칸 + 1] << 8 | anaajaalaa[칸 + 2]);
                    if (jalamüinjatü_ajutuu < 함수시작[수] || jalamüinjatü_ajutuu >= 함수끝[수] || 경계[jalamüinjatü_ajutuu] != 수 + 1) ajachitia_ajutuu("invalid branch target");
                }
                칸 += aluwataaya_akaliaa(ajutuu);
            }
        }
        if (!ajachitia) 속성건너();
        if (읽기위치 != 크기) ajachitia_ajutuu("extra class file data");
    }
    static int 할당(int 종류, int akaliaa_ajutuu) {
        if (akaliaa_ajutuu < 0 || akaliaa_ajutuu > 힙.length - 힙끝 - 2) { ajachitia_ajutuu("object heap exhausted or negative array size"); return 0; }
        int 참조 = 힙끝; 힙끝 += akaliaa_ajutuu + 2; 힙[참조] = 종류; 힙[참조 + 1] = akaliaa_ajutuu;
        return 참조;
    }
    static boolean 객체(int 참조, int 종류) {
        if (참조 < 1 || 참조 >= 힙끝 - 1 || 힙[참조] != 종류) { ajachitia_ajutuu("null or invalid object reference"); return false; }
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
        if (otpünaa_ee_iyatialujuna == 31) { ajachitia_ajutuu("call stack limit (32)"); return; }
        int 다음 = otpünaa_ee_iyatialujuna + 1;
        for (int 수 = 0; 수 < 128; 수++) 지역형[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[함수] - 1; 수 >= 0; 수--) {
            지역값[다음 * 128 + 수] = 빼기(함수인수형[함수 * 16 + 수]); 지역형[다음 * 128 + 수] = 함수인수형[함수 * 16 + 수];
        }
        otpünaa_ee_iyatialujuna = 다음; 틀함수[otpünaa_ee_iyatialujuna] = 함수; 틀위치[otpünaa_ee_iyatialujuna] = 함수시작[함수]; 틀스택[otpünaa_ee_iyatialujuna] = 0;
    }
    static void 반환(int 형) {
        if (형 != 함수반환[틀함수[otpünaa_ee_iyatialujuna]]) { ajachitia_ajutuu("return type mismatch"); return; }
        int ajutuu = 형 == 0 ? 0 : 빼기(형);
        otpünaa_ee_iyatialujuna--; if (otpünaa_ee_iyatialujuna >= 0 && 형 != 0) 넣기(ajutuu, 형);
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
                if (ajutuu < 1 || ajutuu > 127) { ajachitia_ajutuu("file stream paths currently require ASCII"); return; }
                흐름파일이름[칸] = ajutuu;
            }
            흐름파일이름[akaliaa_ajutuu] = 0;
            int 서술자 = ka_yataayakalü.파일서술자열기(흐름파일이름, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { ajachitia_ajutuu("FileNotFoundException: file open failed"); return; }
            힙[palantüsü_ajutuu + 2] = 서술자; 힙[palantüsü_ajutuu + 3] = 1;
            return;
        }
        if (aluwataaya != 182) { ajachitia_ajutuu("invalid file stream invocation"); return; }
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
            if (결과 < -1) ajachitia_ajutuu("IOException: read failed"); else 넣기(결과, 1);
        } else if (ka_yataayakalü.파일한바이트쓰기(서술자, ajutuu) != 1) ajachitia_ajutuu("IOException: write failed");
    }
    static void 함수호출(int ee_iyatialujuna, int aluwataaya) {
        if (!cheeke_waneepiajutu(ee_iyatialujuna, 10)) return;
        int 소유 = 클래스문자(상가[ee_iyatialujuna]), 이름 = 참조이름(상나[ee_iyatialujuna]), akua_ipaa_ajutuu = 참조형식(상나[ee_iyatialujuna]);
        if (ajachitia) return;
        if (같은말(소유, 클래스명)) {
            if (aluwataaya != 184) { ajachitia_ajutuu("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < 함수수; 수++) if (같은말(이름, 함수명[수]) && 같은말(akua_ipaa_ajutuu, 함수형[수])) {
                if ((함수권한[수] & 8) == 0) ajachitia_ajutuu("method is not static"); else 호출(수);
                return;
            }
            ajachitia_ajutuu("NoSuchMethodError"); return;
        }
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
        ajachitia_ajutuu("unsupported library method");
    }
    static int 배열칸(int 참조, int 첨자, int 형) {
        if (!객체(참조, 형)) return 0;
        if (첨자 < 0 || 첨자 >= 힙[참조 + 1]) { ajachitia_ajutuu("ArrayIndexOutOfBoundsException"); return 0; }
        return 참조 + 2 + 첨자;
    }
    static void 실행() {
        int 남음 = 500000;
        while (otpünaa_ee_iyatialujuna >= 0 && !ajachitia) {
            if (--남음 == 0) { ajachitia_ajutuu("instruction limit (500000)"); break; }
            int 시작 = 틀위치[otpünaa_ee_iyatialujuna], ajutuu = 명바();
            if (ajachitia) break;
            if (ajutuu == 0) continue;
            if (ajutuu == 1) { 넣기(0, 2); continue; }
            if (ajutuu >= 2 && ajutuu <= 8) { 넣기(ajutuu - 3, 1); continue; }
            if (ajutuu == 16) { 넣기((byte)명바(), 1); continue; }
            if (ajutuu == 17) { 넣기((short)명짧(), 1); continue; }
            if (ajutuu == 18 || ajutuu == 19) {
                int 수 = ajutuu == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= 상수수) ajachitia_ajutuu("invalid ldc constant");
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
            if (ajutuu == 46 || ajutuu == 50) {
                int 첨자 = 빼기(1), 참조 = 빼기(2), 칸 = 배열칸(참조, 첨자, ajutuu == 46 ? 2 : 3);
                if (!ajachitia) 넣기(힙[칸], ajutuu == 46 ? 1 : 2); continue;
            }
            if (ajutuu == 79 || ajutuu == 83) {
                int apüshii_apüshii = 빼기(ajutuu == 79 ? 1 : 2), 첨자 = 빼기(1), 참조 = 빼기(2), 칸 = 배열칸(참조, 첨자, ajutuu == 79 ? 2 : 3);
                if (ajutuu == 83 && apüshii_apüshii != 0) 객체(apüshii_apüshii, 1);
                if (!ajachitia) 힙[칸] = apüshii_apüshii; continue;
            }
            if (ajutuu == 87) { 빼기(0); continue; }
            if (ajutuu == 89) { int 가 = 빼기(0), 형 = 반환형; 넣기(가, 형); 넣기(가, 형); continue; }
            if (ajutuu == 95) { int 가 = 빼기(0), 가형 = 반환형, 나 = 빼기(0), 나형 = 반환형; 넣기(가, 가형); 넣기(나, 나형); continue; }
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
            if (ajutuu == 178) {
                int 수 = 명짧(); if (!cheeke_waneepiajutu(수, 9)) continue;
                if (!말(클래스문자(상가[수]), "java/lang/System") || !말(참조이름(상나[수]), "out")
                    || !말(참조형식(상나[수]), "Ljava/io/PrintStream;")) ajachitia_ajutuu("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (ajutuu == 182 || ajutuu == 183 || ajutuu == 184) { 함수호출(명짧(), ajutuu); continue; }
            if (ajutuu == 187) {
                int 이름 = 클래스문자(명짧());
                if (말(이름, "java/lang/StringBuilder")) 넣기(할당(4, 1), 2);
                else if (말(이름, "java/io/FileInputStream") || 말(이름, "java/io/FileOutputStream")) {
                    int 참조 = 할당(말(이름, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!ajachitia) { 힙[참조 + 2] = -1; 넣기(참조, 2); }
                } else ajachitia_ajutuu("unsupported object construction");
                continue;
            }
            if (ajutuu == 188 || ajutuu == 189) {
                if (ajutuu == 188) { if (명바() != 10) ajachitia_ajutuu("only int[] newarray is supported"); }
                else if (!말(클래스문자(명짧()), "java/lang/String")) ajachitia_ajutuu("only String[] anewarray is supported");
                int akaliaa_ajutuu = 빼기(1); 넣기(할당(ajutuu == 188 ? 2 : 3, akaliaa_ajutuu), 2); continue;
            }
            if (ajutuu == 190) {
                int 참조 = 빼기(2);
                if (참조 < 1 || 참조 >= 힙끝 - 1 || (힙[참조] != 2 && 힙[참조] != 3)) ajachitia_ajutuu("null or invalid array");
                else 넣기(힙[참조 + 1], 1); continue;
            }
            if (ajutuu == 192) {
                int 이름 = 클래스문자(명짧()), 참조 = 빼기(2);
                if (!말(이름, "java/lang/String")) ajachitia_ajutuu("unsupported checkcast");
                else if (참조 != 0) 객체(참조, 1);
                넣기(참조, 2); continue;
            }
            ajachitia_ajutuu("unsupported bytecode");
        }
    }
    public static int 시작() {
        if (ka_yataayakalü.인수개수() == 1 && 자바도구.같음(ka_yataayakalü.인수(0), "-version")) {
            ka_yataayakalü.ashajaa("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (ka_yataayakalü.인수개수() < 1) { ka_yataayakalü.ashajaa("Usage: java CLASS [ARGS]\n"); return 2; }
        int akaliaa_ajutuu = 자바도구.이름(파일명, ka_yataayakalü.인수(0));
        if (akaliaa_ajutuu < 1 || akaliaa_ajutuu > 57) { ka_yataayakalü.ashajaa("java: invalid class name\n"); return 2; }
        파일명[akaliaa_ajutuu] = '.'; 파일명[akaliaa_ajutuu + 1] = 'c'; 파일명[akaliaa_ajutuu + 2] = 'l'; 파일명[akaliaa_ajutuu + 3] = 'a'; 파일명[akaliaa_ajutuu + 4] = 's'; 파일명[akaliaa_ajutuu + 5] = 's';
        크기 = ka_yataayakalü.파일읽기(파일명, anaajaalaa);
        if (크기 < 0) { ka_yataayakalü.ashajaa("java: cannot read class: "); 자바도구.수쓰기(크기); ka_yataayakalü.ashajaa_jeerü_ajutuu(10); return 1; }
        클래스읽기(); if (ajachitia) return 1;
        int 문자이름 = 상문자(클래스명);
        if (!ajachitia && 힙[문자이름 + 1] != akaliaa_ajutuu) ajachitia_ajutuu("class name does not match file");
        for (int 수 = 0; 수 < akaliaa_ajutuu && !ajachitia; 수++) if (힙[문자이름 + 2 + 수] != 파일명[수]) ajachitia_ajutuu("class name does not match file");
        int ekeroliaa_o_uchikanain_ajutuu = -1;
        for (int 수 = 0; 수 < 함수수; 수++) if (말(함수명[수], "main") && 말(함수형[수], "([Ljava/lang/String;)V") && (함수권한[수] & 9) == 9) ekeroliaa_o_uchikanain_ajutuu = 수;
        if (ekeroliaa_o_uchikanain_ajutuu < 0) ajachitia_ajutuu("public static void main(String[] args) required");
        if (ajachitia) return 1;
        int 인수 = 할당(3, ka_yataayakalü.인수개수() - 1);
        for (int 수 = 1; 수 < ka_yataayakalü.인수개수() && !ajachitia; 수++) 힙[인수 + 1 + 수] = epiajatü_jeerü(ka_yataayakalü.인수(수));
        otpünaa_ee_iyatialujuna = 0; 틀함수[0] = ekeroliaa_o_uchikanain_ajutuu; 틀위치[0] = 함수시작[ekeroliaa_o_uchikanain_ajutuu]; 지역값[0] = 인수; 지역형[0] = 2;
        실행(); return ajachitia ? 1 : 0;
    }
}
