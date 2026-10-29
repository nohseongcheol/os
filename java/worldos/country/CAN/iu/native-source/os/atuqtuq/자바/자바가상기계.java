// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. ini/스택/참조/avalangajuq 경계를 실행 중 검사한다. */
public final class 자바가상기계 {
    static int[] ini = new int[16384], ini_atiq_titiqqaq = new int[64];
    static int[] surragunnangittuq_nalunaikkutaq = new int[512], 상가 = new int[512], 상나 = new int[512], 문자열참조 = new int[512];
    static int[] 함수명 = new int[32], 함수형 = new int[32], 함수권한 = new int[32];
    static int[] 함수시작 = new int[32], 함수끝 = new int[32], 함수스택 = new int[32], 함수지역 = new int[32];
    static int[] 함수인수수 = new int[32], 함수인수형 = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] tamaani_atuutilik = new int[4096], tamaani_qanuittuuninga = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] 틀함수 = new int[32], 틀위치 = new int[32], 틀스택 = new int[32];
    static int[] 힙 = new int[8192];
    static int anininga, 읽기위치, 상수수, 함수수, naliannuungavik_atiq, avalu_nalunaiqsimavik = -1, 힙끝 = 1, 반환형;
    static boolean tammarniq;

    static void itigaqtuq_atuutilik(String 말) {
        if (!tammarniq) { atuqtuq.titiraq("JVM error: "); atuqtuq.titiraq(말); atuqtuq.titiraq_immikkuuqtuq_atuutilik(10); }
        tammarniq = true;
    }
    static boolean Nakatigat(int 시작, int takininga_atuutilik) { return 시작 >= 0 && takininga_atuutilik >= 0 && 시작 <= anininga - takininga_atuutilik; }
    static int byte_atuutilik() {
        if (!Nakatigat(읽기위치, 1)) { itigaqtuq_atuutilik("truncated class file"); return 0; }
        return ini[읽기위치++];
    }
    static int 짧은수() { return byte_atuutilik() << 8 | byte_atuutilik(); }
    static int naasaut() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int takininga_atuutilik) { if (!Nakatigat(읽기위치, takininga_atuutilik)) itigaqtuq_atuutilik("invalid attribute size"); else 읽기위치 += takininga_atuutilik; }
    static boolean qaujigiarli_surragunnangittuq(int 수, int 종류) {
        if (수 <= 0 || 수 >= 상수수 || surragunnangittuq_nalunaikkutaq[수] != 종류) { itigaqtuq_atuutilik("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int 시작, int takininga_atuutilik, String 말) {
        if (!Nakatigat(시작, takininga_atuutilik) || takininga_atuutilik != 말.length()) return false;
        for (int 수 = 0; 수 < takininga_atuutilik; 수++) if (ini[시작 + 수] != 말.charAt(수)) return false;
        return true;
    }
    static boolean 말(int surragunnangittuq_atuutilik, String 말) { return qaujigiarli_surragunnangittuq(surragunnangittuq_atuutilik, 1) && 구간(상가[surragunnangittuq_atuutilik], 상나[surragunnangittuq_atuutilik], 말); }
    static boolean 같은말(int 가, int 나) {
        if (!qaujigiarli_surragunnangittuq(가, 1) || !qaujigiarli_surragunnangittuq(나, 1) || 상나[가] != 상나[나]) return false;
        for (int 수 = 0; 수 < 상나[가]; 수++) if (ini[상가[가] + 수] != ini[상가[나] + 수]) return false;
        return true;
    }
    static int naliannuungavik_atiq_titiqqaq(int 수) { return qaujigiarli_surragunnangittuq(수, 7) && qaujigiarli_surragunnangittuq(상가[수], 1) ? 상가[수] : 0; }
    static int 참조이름(int 수) { return qaujigiarli_surragunnangittuq(수, 12) && qaujigiarli_surragunnangittuq(상가[수], 1) ? 상가[수] : 0; }
    static int 참조형식(int 수) { return qaujigiarli_surragunnangittuq(수, 12) && qaujigiarli_surragunnangittuq(상나[수], 1) ? 상나[수] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (읽기위치 >= 끝) { itigaqtuq_atuutilik("invalid descriptor"); return 0; }
        int atuutilik = byte_atuutilik();
        if (atuutilik == 'V' && 빈형) return 0;
        if (atuutilik == 'I' || atuutilik == 'B' || atuutilik == 'C' || atuutilik == 'S' || atuutilik == 'Z') return 1;
        if (atuutilik == '[') { 서술형(끝, false); return 2; }
        if (atuutilik == 'L') {
            int 시작 = 읽기위치;
            while (읽기위치 < 끝 && ini[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == 시작) itigaqtuq_atuutilik("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        itigaqtuq_atuutilik("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int sugiakkannirut_atuutilik) {
        int 이전 = 읽기위치, 수 = 함수형[sugiakkannirut_atuutilik];
        if (!qaujigiarli_surragunnangittuq(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + 상나[수];
        if (byte_atuutilik() != '(') itigaqtuq_atuutilik("invalid method descriptor");
        int 개수 = 0;
        while (!tammarniq && 읽기위치 < 끝 && ini[읽기위치] != ')') {
            if (개수 == 16) { itigaqtuq_atuutilik("too many method arguments"); break; }
            함수인수형[sugiakkannirut_atuutilik * 16 + 개수++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || byte_atuutilik() != ')') itigaqtuq_atuutilik("invalid method descriptor");
        함수반환[sugiakkannirut_atuutilik] = 서술형(끝, true); 함수인수수[sugiakkannirut_atuutilik] = 개수;
        if (읽기위치 != 끝) itigaqtuq_atuutilik("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !tammarniq; 수++) { qaujigiarli_surragunnangittuq(짧은수(), 1); 건너(naasaut()); }
    }
    static int piqujijjut_takininga(int atuutilik) {
        if (atuutilik == 16 || atuutilik == 18 || atuutilik == 21 || atuutilik == 25 || atuutilik == 54 || atuutilik == 58 || atuutilik == 188) return 2;
        if (atuutilik == 17 || atuutilik == 19 || atuutilik == 132 || atuutilik >= 153 && atuutilik <= 167
            || atuutilik >= 178 && atuutilik <= 184 || atuutilik == 187 || atuutilik == 189 || atuutilik == 192 || atuutilik == 198 || atuutilik == 199) return 3;
        if (atuutilik >= 0 && atuutilik <= 8 || atuutilik >= 26 && atuutilik <= 29 || atuutilik >= 42 && atuutilik <= 46 || atuutilik == 50
            || atuutilik >= 59 && atuutilik <= 62 || atuutilik >= 75 && atuutilik <= 79 || atuutilik == 83 || atuutilik == 87 || atuutilik == 89 || atuutilik == 95
            || atuutilik == 96 || atuutilik == 100 || atuutilik == 104 || atuutilik == 108 || atuutilik == 112 || atuutilik == 116
            || atuutilik == 120 || atuutilik == 122 || atuutilik == 124 || atuutilik == 126 || atuutilik == 128 || atuutilik == 130
            || atuutilik >= 145 && atuutilik <= 147 || atuutilik == 172 || atuutilik == 176 || atuutilik == 177 || atuutilik == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (naasaut() != 0xcafebabe) itigaqtuq_atuutilik("not a class file");
        int 부판 = 짧은수(), imaittuuninga_atuutilik = 짧은수();
        if (imaittuuninga_atuutilik < 45 || imaittuuninga_atuutilik > 52 || 부판 != 0) itigaqtuq_atuutilik("supported class versions: 45..52, minor 0");
        상수수 = 짧은수();
        if (상수수 < 1 || 상수수 > 512) { itigaqtuq_atuutilik("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < 상수수 && !tammarniq; 수++) {
            int 종류 = byte_atuutilik(); surragunnangittuq_nalunaikkutaq[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = naasaut();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); 상나[수] = 짧은수(); }
            else itigaqtuq_atuutilik("unsupported constant type");
        }
        int pijunnaqtittijjut_atuutilik = 짧은수();
        if ((pijunnaqtittijjut_atuutilik & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) itigaqtuq_atuutilik("unsupported class flags");
        naliannuungavik_atiq = naliannuungavik_atiq_titiqqaq(짧은수());
        if (!말(naliannuungavik_atiq_titiqqaq(짧은수()), "java/lang/Object")) itigaqtuq_atuutilik("inheritance unsupported");
        if (짧은수() != 0) itigaqtuq_atuutilik("interfaces unsupported");
        if (짧은수() != 0) itigaqtuq_atuutilik("fields unsupported");
        함수수 = 짧은수();
        if (함수수 < 1 || 함수수 > 32) { itigaqtuq_atuutilik("method count limit (32)"); return; }
        for (int 수 = 0; 수 < 함수수 && !tammarniq; 수++) {
            함수권한[수] = 짧은수(); 함수명[수] = 짧은수(); 함수형[수] = 짧은수();
            qaujigiarli_surragunnangittuq(함수명[수], 1); 서술읽기(수);
            if ((함수권한[수] & (0x100 | 0x400 | 0x20)) != 0) itigaqtuq_atuutilik("native, abstract and synchronized methods unsupported");
            if ((함수권한[수] & 8) == 0 && !말(함수명[수], "<init>")) itigaqtuq_atuutilik("instance methods unsupported");
            if (말(함수명[수], "<clinit>")) itigaqtuq_atuutilik("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(함수명[앞], 함수명[수]) && 같은말(함수형[앞], 함수형[수])) itigaqtuq_atuutilik("duplicate method");
            int 개수 = 짧은수();
            for (int piuluqqutit_atuutilik = 0; piuluqqutit_atuutilik < 개수 && !tammarniq; piuluqqutit_atuutilik++) {
                int atiq = 짧은수(), takininga_atuutilik = naasaut(), 시작 = 읽기위치;
                if (!Nakatigat(시작, takininga_atuutilik)) { itigaqtuq_atuutilik("truncated method attribute"); break; }
                if (말(atiq, "Code")) {
                    if (함수시작[수] != 0) itigaqtuq_atuutilik("duplicate Code attribute");
                    함수스택[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = naasaut();
                    if (함수스택[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) itigaqtuq_atuutilik("method memory limits exceeded");
                    함수시작[수] = 읽기위치; 건너(코드길이); 함수끝[수] = 읽기위치;
                    if (짧은수() != 0) itigaqtuq_atuutilik("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != 시작 + takininga_atuutilik) itigaqtuq_atuutilik("Code attribute size mismatch");
                } else 건너(takininga_atuutilik);
            }
            if (함수시작[수] == 0) itigaqtuq_atuutilik("missing Code attribute");
            int 칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !tammarniq) {
                int takininga_atuutilik = piqujijjut_takininga(ini[칸]);
                if (takininga_atuutilik == 0 || takininga_atuutilik > 함수끝[수] - 칸) { itigaqtuq_atuutilik("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += takininga_atuutilik;
            }
            // 실행하지 않는 경로에도 잘못된 avalangajuq 목적지를 허용하지 않는다.
            칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !tammarniq) {
                int atuutilik = ini[칸];
                if (atuutilik >= 153 && atuutilik <= 167 || atuutilik == 198 || atuutilik == 199) {
                    int namunngarvik_atuutilik = 칸 + (short)(ini[칸 + 1] << 8 | ini[칸 + 2]);
                    if (namunngarvik_atuutilik < 함수시작[수] || namunngarvik_atuutilik >= 함수끝[수] || 경계[namunngarvik_atuutilik] != 수 + 1) itigaqtuq_atuutilik("invalid branch target");
                }
                칸 += piqujijjut_takininga(atuutilik);
            }
        }
        if (!tammarniq) 속성건너();
        if (읽기위치 != anininga) itigaqtuq_atuutilik("extra class file data");
    }
    static int 할당(int 종류, int takininga_atuutilik) {
        if (takininga_atuutilik < 0 || takininga_atuutilik > 힙.length - 힙끝 - 2) { itigaqtuq_atuutilik("object heap exhausted or negative array size"); return 0; }
        int 참조 = 힙끝; 힙끝 += takininga_atuutilik + 2; 힙[참조] = 종류; 힙[참조 + 1] = takininga_atuutilik;
        return 참조;
    }
    static boolean kisu_atuutilik(int 참조, int 종류) {
        if (참조 < 1 || 참조 >= 힙끝 - 1 || 힙[참조] != 종류) { itigaqtuq_atuutilik("null or invalid object reference"); return false; }
        return true;
    }
    static int surragunnangittuq_titiqqaq(int nalunaiqsimavik) {
        if (!qaujigiarli_surragunnangittuq(nalunaiqsimavik, 1)) return 0;
        if (문자열참조[nalunaiqsimavik] != 0) return 문자열참조[nalunaiqsimavik];
        int 참조 = 할당(1, 상나[nalunaiqsimavik]); if (tammarniq) return 0;
        int 끝 = 상가[nalunaiqsimavik] + 상나[nalunaiqsimavik], 수 = 상가[nalunaiqsimavik], takininga_atuutilik = 0;
        while (수 < 끝 && !tammarniq) {
            int atuutilik = ini[수++];
            if (atuutilik == 0) itigaqtuq_atuutilik("invalid modified UTF-8");
            else if (atuutilik >= 192 && atuutilik <= 223 && 수 < 끝) {
                int 다음 = ini[수++];
                if ((다음 & 192) != 128) itigaqtuq_atuutilik("invalid modified UTF-8");
                atuutilik = (atuutilik & 31) << 6 | 다음 & 63;
                if (atuutilik != 0 && atuutilik < 128) itigaqtuq_atuutilik("overlong modified UTF-8");
            } else if (atuutilik >= 224 && atuutilik <= 239 && 수 + 1 < 끝) {
                int 가 = ini[수++], 나 = ini[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) itigaqtuq_atuutilik("invalid modified UTF-8");
                atuutilik = (atuutilik & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (atuutilik < 2048) itigaqtuq_atuutilik("overlong modified UTF-8");
            } else if (atuutilik >= 128) itigaqtuq_atuutilik("invalid modified UTF-8");
            힙[참조 + 2 + takininga_atuutilik++] = atuutilik;
        }
        힙[참조 + 1] = takininga_atuutilik; 문자열참조[nalunaiqsimavik] = 참조; return 참조;
    }
    static int tuttarvik_immikkuuqtuq(String atuutilik) {
        int 참조 = 할당(1, atuutilik.length()); if (tammarniq) return 0;
        for (int 수 = 0; 수 < atuutilik.length(); 수++) 힙[참조 + 2 + 수] = atuutilik.charAt(수);
        return 참조;
    }
    static void titiraq_titiqqaq(int 참조) {
        if (참조 == 0) { atuqtuq.titiraq("null"); return; }
        if (!kisu_atuutilik(참조, 1)) return;
        for (int 수 = 0; 수 < 힙[참조 + 1]; 수++) atuqtuq.titiraq_immikkuuqtuq_atuutilik(힙[참조 + 2 + 수]);
    }
    static int 수문자(int atuutilik) {
        int 참조 = 할당(1, 11); if (tammarniq) return 0;
        int takininga_atuutilik = 0;
        if (atuutilik < 0) 힙[참조 + 2 + takininga_atuutilik++] = '-'; else atuutilik = -atuutilik;
        int 자리 = 1000000000; boolean 시작 = false;
        while (자리 != 0) {
            int 수 = -(atuutilik / 자리);
            if (수 != 0 || 시작 || 자리 == 1) { 힙[참조 + 2 + takininga_atuutilik++] = '0' + 수; 시작 = true; }
            atuutilik %= 자리; 자리 /= 10;
        }
        힙[참조 + 1] = takininga_atuutilik; return 참조;
    }
    static int 정수해독(int 참조) {
        if (!kisu_atuutilik(참조, 1)) return 0;
        int takininga_atuutilik = 힙[참조 + 1], 수 = 0, atuutilik = 0; boolean 음수 = false;
        if (takininga_atuutilik > 0 && (힙[참조 + 2] == '-' || 힙[참조 + 2] == '+')) { 음수 = 힙[참조 + 2] == '-'; 수++; }
        if (수 == takininga_atuutilik) itigaqtuq_atuutilik("NumberFormatException");
        for (; 수 < takininga_atuutilik && !tammarniq; 수++) {
            int 숫자 = 힙[참조 + 2 + 수] - '0';
            if (숫자 < 0 || 숫자 > 9 || atuutilik < -214748364 || atuutilik == -214748364 && 숫자 > (음수 ? 8 : 7)) itigaqtuq_atuutilik("NumberFormatException");
            atuutilik = atuutilik * 10 - 숫자;
        }
        return 음수 ? atuutilik : -atuutilik;
    }
    static void 넣기(int atuutilik, int qanuittuuninga_atuutilik) {
        if (tammarniq) return;
        if (avalu_nalunaiqsimavik < 0 || 틀스택[avalu_nalunaiqsimavik] >= 함수스택[틀함수[avalu_nalunaiqsimavik]]) { itigaqtuq_atuutilik("operand stack overflow"); return; }
        int 칸 = avalu_nalunaiqsimavik * 128 + 틀스택[avalu_nalunaiqsimavik]++; 스택값[칸] = atuutilik; 스택형[칸] = qanuittuuninga_atuutilik;
    }
    static int 빼기(int qanuittuuninga_atuutilik) {
        if (tammarniq) return 0;
        if (avalu_nalunaiqsimavik < 0 || 틀스택[avalu_nalunaiqsimavik] < 1) { itigaqtuq_atuutilik("operand stack underflow"); return 0; }
        int 칸 = avalu_nalunaiqsimavik * 128 + --틀스택[avalu_nalunaiqsimavik]; 반환형 = 스택형[칸];
        if (qanuittuuninga_atuutilik != 0 && 반환형 != qanuittuuninga_atuutilik) itigaqtuq_atuutilik("operand type mismatch");
        return 스택값[칸];
    }
    static void 지역읽기(int nalunaiqsimavik, int qanuittuuninga_atuutilik) {
        if (nalunaiqsimavik >= 함수지역[틀함수[avalu_nalunaiqsimavik]] || nalunaiqsimavik < 0 || tamaani_qanuittuuninga[avalu_nalunaiqsimavik * 128 + nalunaiqsimavik] != qanuittuuninga_atuutilik) { itigaqtuq_atuutilik("invalid or uninitialized local"); return; }
        넣기(tamaani_atuutilik[avalu_nalunaiqsimavik * 128 + nalunaiqsimavik], qanuittuuninga_atuutilik);
    }
    static void titiraq_tamaani(int nalunaiqsimavik, int qanuittuuninga_atuutilik) {
        if (nalunaiqsimavik >= 함수지역[틀함수[avalu_nalunaiqsimavik]] || nalunaiqsimavik < 0) { itigaqtuq_atuutilik("local index out of range"); return; }
        int atuutilik = 빼기(qanuittuuninga_atuutilik); tamaani_atuutilik[avalu_nalunaiqsimavik * 128 + nalunaiqsimavik] = atuutilik; tamaani_qanuittuuninga[avalu_nalunaiqsimavik * 128 + nalunaiqsimavik] = qanuittuuninga_atuutilik;
    }
    static int 명바() {
        int 위치 = 틀위치[avalu_nalunaiqsimavik];
        if (위치 < 함수시작[틀함수[avalu_nalunaiqsimavik]] || 위치 >= 함수끝[틀함수[avalu_nalunaiqsimavik]]) { itigaqtuq_atuutilik("instruction pointer out of range"); return 0; }
        틀위치[avalu_nalunaiqsimavik]++; return ini[위치];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void nuulli_atuutilik(int 위치) {
        int sugiakkannirut_atuutilik = 틀함수[avalu_nalunaiqsimavik];
        if (위치 < 함수시작[sugiakkannirut_atuutilik] || 위치 >= 함수끝[sugiakkannirut_atuutilik] || 경계[위치] != sugiakkannirut_atuutilik + 1) itigaqtuq_atuutilik("invalid branch target");
        else 틀위치[avalu_nalunaiqsimavik] = 위치;
    }
    static void 호출(int sugiakkannirut_atuutilik) {
        if (avalu_nalunaiqsimavik == 31) { itigaqtuq_atuutilik("call stack limit (32)"); return; }
        int 다음 = avalu_nalunaiqsimavik + 1;
        for (int 수 = 0; 수 < 128; 수++) tamaani_qanuittuuninga[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[sugiakkannirut_atuutilik] - 1; 수 >= 0; 수--) {
            tamaani_atuutilik[다음 * 128 + 수] = 빼기(함수인수형[sugiakkannirut_atuutilik * 16 + 수]); tamaani_qanuittuuninga[다음 * 128 + 수] = 함수인수형[sugiakkannirut_atuutilik * 16 + 수];
        }
        avalu_nalunaiqsimavik = 다음; 틀함수[avalu_nalunaiqsimavik] = sugiakkannirut_atuutilik; 틀위치[avalu_nalunaiqsimavik] = 함수시작[sugiakkannirut_atuutilik]; 틀스택[avalu_nalunaiqsimavik] = 0;
    }
    static void 반환(int qanuittuuninga_atuutilik) {
        if (qanuittuuninga_atuutilik != 함수반환[틀함수[avalu_nalunaiqsimavik]]) { itigaqtuq_atuutilik("return type mismatch"); return; }
        int atuutilik = qanuittuuninga_atuutilik == 0 ? 0 : 빼기(qanuittuuninga_atuutilik);
        avalu_nalunaiqsimavik--; if (avalu_nalunaiqsimavik >= 0 && qanuittuuninga_atuutilik != 0) 넣기(atuutilik, qanuittuuninga_atuutilik);
    }
    static int[] ingirrania_aulataup_ini_atiq = new int[64];
    static void ini_ingirrania_aulataup_Uqaalaniq(int 소유, int atiq, int aaqqisurli_atuutilik, int piqujijjut) {
        boolean 출력 = 말(소유, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (piqujijjut == 183 && 말(atiq, "<init>")) {
            boolean 이어 = false;
            if (출력 && 말(aaqqisurli_atuutilik, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!말(aaqqisurli_atuutilik, "(Ljava/lang/String;)V")) { itigaqtuq_atuutilik("unsupported file stream constructor"); return; }
            int ini_Iliniku_atiq = 빼기(2), ingirrania_aulataup_atuutilik = 빼기(2);
            if (!kisu_atuutilik(ini_Iliniku_atiq, 1) || !kisu_atuutilik(ingirrania_aulataup_atuutilik, 종류) || tammarniq) return;
            if (힙[ingirrania_aulataup_atuutilik + 3] != 0) { itigaqtuq_atuutilik("file stream already initialized"); return; }
            int takininga_atuutilik = 힙[ini_Iliniku_atiq + 1];
            if (takininga_atuutilik < 1 || takininga_atuutilik > 63) { itigaqtuq_atuutilik("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < takininga_atuutilik; 칸++) {
                int atuutilik = 힙[ini_Iliniku_atiq + 2 + 칸];
                if (atuutilik < 1 || atuutilik > 127) { itigaqtuq_atuutilik("file stream paths currently require ASCII"); return; }
                ingirrania_aulataup_ini_atiq[칸] = atuutilik;
            }
            ingirrania_aulataup_ini_atiq[takininga_atuutilik] = 0;
            int 서술자 = atuqtuq.파일서술자열기(ingirrania_aulataup_ini_atiq, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { itigaqtuq_atuutilik("FileNotFoundException: file open failed"); return; }
            힙[ingirrania_aulataup_atuutilik + 2] = 서술자; 힙[ingirrania_aulataup_atuutilik + 3] = 1;
            return;
        }
        if (piqujijjut != 182) { itigaqtuq_atuutilik("invalid file stream invocation"); return; }
        int sugiarut = -1, atuutilik = 0;
        if (말(atiq, "close") && 말(aaqqisurli_atuutilik, "()V")) sugiarut = 0;
        if (!출력 && 말(atiq, "read") && 말(aaqqisurli_atuutilik, "()I")) sugiarut = 1;
        if (출력 && 말(atiq, "write") && 말(aaqqisurli_atuutilik, "(I)V")) { sugiarut = 2; atuutilik = 빼기(1); }
        if (sugiarut < 0) { itigaqtuq_atuutilik("unsupported file stream method"); return; }
        int ingirrania_aulataup_atuutilik = 빼기(2);
        if (!kisu_atuutilik(ingirrania_aulataup_atuutilik, 종류) || tammarniq) return;
        if (힙[ingirrania_aulataup_atuutilik + 3] == 0) { itigaqtuq_atuutilik("uninitialized file stream"); return; }
        int 서술자 = 힙[ingirrania_aulataup_atuutilik + 2];
        if (sugiarut == 0) {
            if (서술자 >= 0 && atuqtuq.파일서술자닫기(서술자) < 0) itigaqtuq_atuutilik("IOException: close failed");
            힙[ingirrania_aulataup_atuutilik + 2] = -1; return;
        }
        if (서술자 < 0) { itigaqtuq_atuutilik("IOException: stream closed"); return; }
        if (sugiarut == 1) {
            int 결과 = atuqtuq.파일한바이트읽기(서술자);
            if (결과 < -1) itigaqtuq_atuutilik("IOException: read failed"); else 넣기(결과, 1);
        } else if (atuqtuq.파일한바이트쓰기(서술자, atuutilik) != 1) itigaqtuq_atuutilik("IOException: write failed");
    }
    static void 함수호출(int nalunaiqsimavik, int piqujijjut) {
        if (!qaujigiarli_surragunnangittuq(nalunaiqsimavik, 10)) return;
        int 소유 = naliannuungavik_atiq_titiqqaq(상가[nalunaiqsimavik]), atiq = 참조이름(상나[nalunaiqsimavik]), aaqqisurli_atuutilik = 참조형식(상나[nalunaiqsimavik]);
        if (tammarniq) return;
        if (같은말(소유, naliannuungavik_atiq)) {
            if (piqujijjut != 184) { itigaqtuq_atuutilik("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < 함수수; 수++) if (같은말(atiq, 함수명[수]) && 같은말(aaqqisurli_atuutilik, 함수형[수])) {
                if ((함수권한[수] & 8) == 0) itigaqtuq_atuutilik("method is not static"); else 호출(수);
                return;
            }
            itigaqtuq_atuutilik("NoSuchMethodError"); return;
        }
        if (말(소유, "java/io/FileInputStream") || 말(소유, "java/io/FileOutputStream")) {
            ini_ingirrania_aulataup_Uqaalaniq(소유, atiq, aaqqisurli_atuutilik, piqujijjut); return;
        }
        if (piqujijjut == 184 && 말(소유, "java/lang/Integer") && 말(atiq, "parseInt") && 말(aaqqisurli_atuutilik, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (piqujijjut == 182 && 말(소유, "java/io/PrintStream") && (말(atiq, "println") || 말(atiq, "print"))) {
            int qanuittuuninga_atuutilik = 0, atuutilik = 0;
            if (말(aaqqisurli_atuutilik, "(I)V")) { qanuittuuninga_atuutilik = 1; atuutilik = 빼기(1); }
            else if (말(aaqqisurli_atuutilik, "(Z)V")) { qanuittuuninga_atuutilik = 2; atuutilik = 빼기(1); }
            else if (말(aaqqisurli_atuutilik, "(C)V")) { qanuittuuninga_atuutilik = 3; atuutilik = 빼기(1); }
            else if (말(aaqqisurli_atuutilik, "(Ljava/lang/String;)V")) { qanuittuuninga_atuutilik = 4; atuutilik = 빼기(2); }
            else if (!말(aaqqisurli_atuutilik, "()V") || !말(atiq, "println")) itigaqtuq_atuutilik("unsupported print descriptor");
            if (빼기(2) != -1) itigaqtuq_atuutilik("invalid PrintStream receiver");
            if (tammarniq) return;
            if (qanuittuuninga_atuutilik == 1) 자바도구.수쓰기(atuutilik);
            if (qanuittuuninga_atuutilik == 2) atuqtuq.titiraq(atuutilik == 0 ? "false" : "true");
            if (qanuittuuninga_atuutilik == 3) atuqtuq.titiraq_immikkuuqtuq_atuutilik(atuutilik & 65535);
            if (qanuittuuninga_atuutilik == 4) titiraq_titiqqaq(atuutilik);
            if (말(atiq, "println")) atuqtuq.titiraq_immikkuuqtuq_atuutilik(10);
            return;
        }
        if (piqujijjut == 182 && 말(소유, "java/lang/String")) {
            if (말(atiq, "length") && 말(aaqqisurli_atuutilik, "()I")) {
                int 참조 = 빼기(2); if (kisu_atuutilik(참조, 1)) 넣기(힙[참조 + 1], 1); return;
            }
            if (말(atiq, "charAt") && 말(aaqqisurli_atuutilik, "(I)C")) {
                int qulikkanniagut_titiraqsimajuq_atuutilik = 빼기(1), 참조 = 빼기(2);
                if (kisu_atuutilik(참조, 1)) {
                    if (qulikkanniagut_titiraqsimajuq_atuutilik < 0 || qulikkanniagut_titiraqsimajuq_atuutilik >= 힙[참조 + 1]) itigaqtuq_atuutilik("StringIndexOutOfBoundsException"); else 넣기(힙[참조 + 2 + qulikkanniagut_titiraqsimajuq_atuutilik], 1);
                }
                return;
            }
        }
        if (말(소유, "java/lang/StringBuilder")) {
            if (piqujijjut == 183 && 말(atiq, "<init>") && 말(aaqqisurli_atuutilik, "()V")) { kisu_atuutilik(빼기(2), 4); return; }
            if (piqujijjut == 182 && 말(atiq, "toString") && 말(aaqqisurli_atuutilik, "()Ljava/lang/String;")) {
                int 참조 = 빼기(2); if (kisu_atuutilik(참조, 4)) 넣기(힙[참조 + 2] == 0 ? tuttarvik_immikkuuqtuq("") : 힙[참조 + 2], 2); return;
            }
            if (piqujijjut == 182 && 말(atiq, "append")) {
                int titiqqaq = 0;
                if (말(aaqqisurli_atuutilik, "(I)Ljava/lang/StringBuilder;")) titiqqaq = 수문자(빼기(1));
                else if (말(aaqqisurli_atuutilik, "(Z)Ljava/lang/StringBuilder;")) titiqqaq = tuttarvik_immikkuuqtuq(빼기(1) == 0 ? "false" : "true");
                else if (말(aaqqisurli_atuutilik, "(C)Ljava/lang/StringBuilder;")) {
                    int atuutilik = 빼기(1); titiqqaq = 할당(1, 1); if (!tammarniq) 힙[titiqqaq + 2] = atuutilik & 65535;
                }
                else if (말(aaqqisurli_atuutilik, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { titiqqaq = 빼기(2); if (titiqqaq == 0) titiqqaq = tuttarvik_immikkuuqtuq("null"); }
                else { itigaqtuq_atuutilik("unsupported StringBuilder append"); return; }
                int 참조 = 빼기(2); if (!kisu_atuutilik(참조, 4) || !kisu_atuutilik(titiqqaq, 1)) return;
                int 앞 = 힙[참조 + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], Utimut_atuutilik_takininga = 힙[titiqqaq + 1];
                int 새글 = 할당(1, 앞길이 + Utimut_atuutilik_takininga); if (tammarniq) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < Utimut_atuutilik_takininga; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[titiqqaq + 2 + 수];
                힙[참조 + 2] = 새글; 넣기(참조, 2); return;
            }
        }
        itigaqtuq_atuutilik("unsupported library method");
    }
    static int 배열칸(int 참조, int qulikkanniagut_titiraqsimajuq_atuutilik, int qanuittuuninga_atuutilik) {
        if (!kisu_atuutilik(참조, qanuittuuninga_atuutilik)) return 0;
        if (qulikkanniagut_titiraqsimajuq_atuutilik < 0 || qulikkanniagut_titiraqsimajuq_atuutilik >= 힙[참조 + 1]) { itigaqtuq_atuutilik("ArrayIndexOutOfBoundsException"); return 0; }
        return 참조 + 2 + qulikkanniagut_titiraqsimajuq_atuutilik;
    }
    static void 실행() {
        int 남음 = 500000;
        while (avalu_nalunaiqsimavik >= 0 && !tammarniq) {
            if (--남음 == 0) { itigaqtuq_atuutilik("instruction limit (500000)"); break; }
            int 시작 = 틀위치[avalu_nalunaiqsimavik], atuutilik = 명바();
            if (tammarniq) break;
            if (atuutilik == 0) continue;
            if (atuutilik == 1) { 넣기(0, 2); continue; }
            if (atuutilik >= 2 && atuutilik <= 8) { 넣기(atuutilik - 3, 1); continue; }
            if (atuutilik == 16) { 넣기((byte)명바(), 1); continue; }
            if (atuutilik == 17) { 넣기((short)명짧(), 1); continue; }
            if (atuutilik == 18 || atuutilik == 19) {
                int 수 = atuutilik == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= 상수수) itigaqtuq_atuutilik("invalid ldc constant");
                else if (surragunnangittuq_nalunaikkutaq[수] == 3) 넣기(상가[수], 1);
                else if (surragunnangittuq_nalunaikkutaq[수] == 8) 넣기(surragunnangittuq_titiqqaq(상가[수]), 2);
                else itigaqtuq_atuutilik("unsupported ldc constant");
                continue;
            }
            if (atuutilik == 21 || atuutilik == 25) { 지역읽기(명바(), atuutilik == 21 ? 1 : 2); continue; }
            if (atuutilik >= 26 && atuutilik <= 29) { 지역읽기(atuutilik - 26, 1); continue; }
            if (atuutilik >= 42 && atuutilik <= 45) { 지역읽기(atuutilik - 42, 2); continue; }
            if (atuutilik == 54 || atuutilik == 58) { titiraq_tamaani(명바(), atuutilik == 54 ? 1 : 2); continue; }
            if (atuutilik >= 59 && atuutilik <= 62) { titiraq_tamaani(atuutilik - 59, 1); continue; }
            if (atuutilik >= 75 && atuutilik <= 78) { titiraq_tamaani(atuutilik - 75, 2); continue; }
            if (atuutilik == 46 || atuutilik == 50) {
                int qulikkanniagut_titiraqsimajuq_atuutilik = 빼기(1), 참조 = 빼기(2), 칸 = 배열칸(참조, qulikkanniagut_titiraqsimajuq_atuutilik, atuutilik == 46 ? 2 : 3);
                if (!tammarniq) 넣기(힙[칸], atuutilik == 46 ? 1 : 2); continue;
            }
            if (atuutilik == 79 || atuutilik == 83) {
                int kisu_ilanga = 빼기(atuutilik == 79 ? 1 : 2), qulikkanniagut_titiraqsimajuq_atuutilik = 빼기(1), 참조 = 빼기(2), 칸 = 배열칸(참조, qulikkanniagut_titiraqsimajuq_atuutilik, atuutilik == 79 ? 2 : 3);
                if (atuutilik == 83 && kisu_ilanga != 0) kisu_atuutilik(kisu_ilanga, 1);
                if (!tammarniq) 힙[칸] = kisu_ilanga; continue;
            }
            if (atuutilik == 87) { 빼기(0); continue; }
            if (atuutilik == 89) { int 가 = 빼기(0), qanuittuuninga_atuutilik = 반환형; 넣기(가, qanuittuuninga_atuutilik); 넣기(가, qanuittuuninga_atuutilik); continue; }
            if (atuutilik == 95) { int 가 = 빼기(0), 가형 = 반환형, 나 = 빼기(0), 나형 = 반환형; 넣기(가, 가형); 넣기(나, 나형); continue; }
            if (atuutilik == 96 || atuutilik == 100 || atuutilik == 104 || atuutilik == 108 || atuutilik == 112 || atuutilik == 120
                || atuutilik == 122 || atuutilik == 124 || atuutilik == 126 || atuutilik == 128 || atuutilik == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), 결과 = 0;
                if ((atuutilik == 108 || atuutilik == 112) && 나 == 0) { itigaqtuq_atuutilik("ArithmeticException: / by zero"); continue; }
                if (atuutilik == 96) 결과 = 가 + 나;
                if (atuutilik == 100) 결과 = 가 - 나;
                if (atuutilik == 104) 결과 = 가 * 나;
                if (atuutilik == 108) 결과 = 가 / 나;
                if (atuutilik == 112) 결과 = 가 % 나;
                if (atuutilik == 120) 결과 = 가 << 나;
                if (atuutilik == 122) 결과 = 가 >> 나;
                if (atuutilik == 124) 결과 = 가 >>> 나;
                if (atuutilik == 126) 결과 = 가 & 나;
                if (atuutilik == 128) 결과 = 가 | 나;
                if (atuutilik == 130) 결과 = 가 ^ 나;
                넣기(결과, 1); continue;
            }
            if (atuutilik == 116) { 넣기(-빼기(1), 1); continue; }
            if (atuutilik == 132) {
                int tamaani_qinirvik = 명바(), 증분 = (byte)명바(); 지역읽기(tamaani_qinirvik, 1); 넣기(빼기(1) + 증분, 1); titiraq_tamaani(tamaani_qinirvik, 1); continue;
            }
            if (atuutilik >= 145 && atuutilik <= 147) {
                int 수 = 빼기(1); 넣기(atuutilik == 145 ? (byte)수 : atuutilik == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (atuutilik >= 153 && atuutilik <= 167 || atuutilik == 198 || atuutilik == 199) {
                int namunngarvik_atuutilik = 시작 + (short)명짧(); boolean 갈까 = atuutilik == 167;
                if (atuutilik >= 153 && atuutilik <= 158) {
                    int 수 = 빼기(1); 갈까 = atuutilik == 153 ? 수 == 0 : atuutilik == 154 ? 수 != 0 : atuutilik == 155 ? 수 < 0 : atuutilik == 156 ? 수 >= 0 : atuutilik == 157 ? 수 > 0 : 수 <= 0;
                } else if (atuutilik >= 159 && atuutilik <= 166) {
                    int 나 = 빼기(atuutilik >= 165 ? 2 : 1), 가 = 빼기(atuutilik >= 165 ? 2 : 1);
                    갈까 = atuutilik == 159 || atuutilik == 165 ? 가 == 나 : atuutilik == 160 || atuutilik == 166 ? 가 != 나 : atuutilik == 161 ? 가 < 나 : atuutilik == 162 ? 가 >= 나 : atuutilik == 163 ? 가 > 나 : 가 <= 나;
                } else if (atuutilik == 198 || atuutilik == 199) { int 수 = 빼기(2); 갈까 = atuutilik == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) nuulli_atuutilik(namunngarvik_atuutilik); continue;
            }
            if (atuutilik == 172 || atuutilik == 176 || atuutilik == 177) { 반환(atuutilik == 172 ? 1 : atuutilik == 176 ? 2 : 0); continue; }
            if (atuutilik == 178) {
                int 수 = 명짧(); if (!qaujigiarli_surragunnangittuq(수, 9)) continue;
                if (!말(naliannuungavik_atiq_titiqqaq(상가[수]), "java/lang/System") || !말(참조이름(상나[수]), "out")
                    || !말(참조형식(상나[수]), "Ljava/io/PrintStream;")) itigaqtuq_atuutilik("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (atuutilik == 182 || atuutilik == 183 || atuutilik == 184) { 함수호출(명짧(), atuutilik); continue; }
            if (atuutilik == 187) {
                int atiq = naliannuungavik_atiq_titiqqaq(명짧());
                if (말(atiq, "java/lang/StringBuilder")) 넣기(할당(4, 1), 2);
                else if (말(atiq, "java/io/FileInputStream") || 말(atiq, "java/io/FileOutputStream")) {
                    int 참조 = 할당(말(atiq, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!tammarniq) { 힙[참조 + 2] = -1; 넣기(참조, 2); }
                } else itigaqtuq_atuutilik("unsupported object construction");
                continue;
            }
            if (atuutilik == 188 || atuutilik == 189) {
                if (atuutilik == 188) { if (명바() != 10) itigaqtuq_atuutilik("only int[] newarray is supported"); }
                else if (!말(naliannuungavik_atiq_titiqqaq(명짧()), "java/lang/String")) itigaqtuq_atuutilik("only String[] anewarray is supported");
                int takininga_atuutilik = 빼기(1); 넣기(할당(atuutilik == 188 ? 2 : 3, takininga_atuutilik), 2); continue;
            }
            if (atuutilik == 190) {
                int 참조 = 빼기(2);
                if (참조 < 1 || 참조 >= 힙끝 - 1 || (힙[참조] != 2 && 힙[참조] != 3)) itigaqtuq_atuutilik("null or invalid array");
                else 넣기(힙[참조 + 1], 1); continue;
            }
            if (atuutilik == 192) {
                int atiq = naliannuungavik_atiq_titiqqaq(명짧()), 참조 = 빼기(2);
                if (!말(atiq, "java/lang/String")) itigaqtuq_atuutilik("unsupported checkcast");
                else if (참조 != 0) kisu_atuutilik(참조, 1);
                넣기(참조, 2); continue;
            }
            itigaqtuq_atuutilik("unsupported bytecode");
        }
    }
    public static int 시작() {
        if (atuqtuq.인수개수() == 1 && 자바도구.같음(atuqtuq.인수(0), "-version")) {
            atuqtuq.titiraq("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (atuqtuq.인수개수() < 1) { atuqtuq.titiraq("Usage: java CLASS [ARGS]\n"); return 2; }
        int takininga_atuutilik = 자바도구.atiq(ini_atiq_titiqqaq, atuqtuq.인수(0));
        if (takininga_atuutilik < 1 || takininga_atuutilik > 57) { atuqtuq.titiraq("java: invalid class name\n"); return 2; }
        ini_atiq_titiqqaq[takininga_atuutilik] = '.'; ini_atiq_titiqqaq[takininga_atuutilik + 1] = 'c'; ini_atiq_titiqqaq[takininga_atuutilik + 2] = 'l'; ini_atiq_titiqqaq[takininga_atuutilik + 3] = 'a'; ini_atiq_titiqqaq[takininga_atuutilik + 4] = 's'; ini_atiq_titiqqaq[takininga_atuutilik + 5] = 's';
        anininga = atuqtuq.파일읽기(ini_atiq_titiqqaq, ini);
        if (anininga < 0) { atuqtuq.titiraq("java: cannot read class: "); 자바도구.수쓰기(anininga); atuqtuq.titiraq_immikkuuqtuq_atuutilik(10); return 1; }
        클래스읽기(); if (tammarniq) return 1;
        int immikkuuqtuq_atiq = surragunnangittuq_titiqqaq(naliannuungavik_atiq);
        if (!tammarniq && 힙[immikkuuqtuq_atiq + 1] != takininga_atuutilik) itigaqtuq_atuutilik("class name does not match file");
        for (int 수 = 0; 수 < takininga_atuutilik && !tammarniq; 수++) if (힙[immikkuuqtuq_atiq + 2 + 수] != ini_atiq_titiqqaq[수]) itigaqtuq_atuutilik("class name does not match file");
        int Iliniku_puinti_atuutilik = -1;
        for (int 수 = 0; 수 < 함수수; 수++) if (말(함수명[수], "main") && 말(함수형[수], "([Ljava/lang/String;)V") && (함수권한[수] & 9) == 9) Iliniku_puinti_atuutilik = 수;
        if (Iliniku_puinti_atuutilik < 0) itigaqtuq_atuutilik("public static void main(String[] args) required");
        if (tammarniq) return 1;
        int 인수 = 할당(3, atuqtuq.인수개수() - 1);
        for (int 수 = 1; 수 < atuqtuq.인수개수() && !tammarniq; 수++) 힙[인수 + 1 + 수] = tuttarvik_immikkuuqtuq(atuqtuq.인수(수));
        avalu_nalunaiqsimavik = 0; 틀함수[0] = Iliniku_puinti_atuutilik; 틀위치[0] = 함수시작[Iliniku_puinti_atuutilik]; tamaani_atuutilik[0] = 인수; tamaani_qanuittuuninga[0] = 2;
        실행(); return tammarniq ? 1 : 0;
    }
}
