// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. ini/스택/참조/avalangajuq 경계를 실행 중 검사한다. */
public final class 자바가상기계 {
    static int[] ini = new int[16 * 16384], 임시파일 = new int[16384], ini_atiq_titiqqaq = new int[512];
    static int[] surragunnangittuq_nalunaikkutaq = new int[8192], 상가 = new int[8192], 상나 = new int[8192], 문자열참조 = new int[8192];
    static int[] 함수명 = new int[512], 함수형 = new int[512], 함수권한 = new int[512], 함수주인 = new int[512];
    static int[] 함수시작 = new int[512], 함수끝 = new int[512], 함수스택 = new int[512], 함수지역 = new int[512];
    static int[] 함수인수수 = new int[512], 함수인수형 = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] tamaani_atuutilik = new int[16384], tamaani_qanuittuuninga = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] 틀함수 = new int[128], 틀위치 = new int[128], 틀스택 = new int[128], avalu_maligialiit = new int[128], aturunnaqsili_avalu = new int[128];
    static int[] 종이름 = new int[16], 종크기 = new int[16], 종부모 = new int[16], 종상태 = new int[16], 종칸수 = new int[16], 종초기화 = new int[16];
    static int[] naliannuungavik_saqqijaagaq = new int[16 * 16], 종접면수 = new int[16];
    static int[] 칸이름 = new int[512], 칸형 = new int[512], 칸주인 = new int[512], 칸권한 = new int[512], 칸위치 = new int[512], 칸값 = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], array_ilanga = new int[32768], tuqqurli_naasaut = new int[256];
    static int anininga, 읽기위치, 함수수, naliannuungavik_atiq, avalu_nalunaiqsimavik = -1, 힙끝 = 1, 반환형;
    static int 종수, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, 표시수, 수거횟수;
    static int 현재가닥, 가닥수 = 1, 시작종;
    static int[] aqqusiqtarvik_avalu = new int[4], aqqusiqtarvik_qanuilinganiq = new int[4], aqqusiqtarvik_kisu = new int[4], aqqusiqtarvik_turaagaq = new int[4], 가닥대기 = new int[4];
    static boolean tammarniq, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], naliannuungavik_aqqusiqtarvik = new int[16];

    static void itigaqtuq_atuutilik(String 말) {
        if (tammarniq) return;
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
        if (분류코드 != 0 && avalu_nalunaiqsimavik >= 0) { 예외던짐(분류코드, 말); return; }
        atuqtuq.titiraq("JVM error: "); atuqtuq.titiraq(말); atuqtuq.titiraq_immikkuuqtuq_atuutilik(10); tammarniq = true;
    }
    static boolean Nakatigat(int 시작, int takininga_atuutilik) {
        if (시작 < 0 || 시작 >= ini.length || takininga_atuutilik < 0) return false;
        int 종 = 시작 / 16384;
        return 시작 % 16384 <= 종크기[종] && takininga_atuutilik <= 종크기[종] - 시작 % 16384;
    }
    static int byte_atuutilik() {
        if (!Nakatigat(읽기위치, 1)) { itigaqtuq_atuutilik("truncated class file"); return 0; }
        return ini[읽기위치++];
    }
    static int 짧은수() { return byte_atuutilik() << 8 | byte_atuutilik(); }
    static int naasaut() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int takininga_atuutilik) { if (!Nakatigat(읽기위치, takininga_atuutilik)) itigaqtuq_atuutilik("invalid attribute size"); else 읽기위치 += takininga_atuutilik; }
    static boolean qaujigiarli_surragunnangittuq(int 수, int 종류) {
        if (수 <= 0 || 수 >= surragunnangittuq_nalunaikkutaq.length || surragunnangittuq_nalunaikkutaq[수] != 종류) { itigaqtuq_atuutilik("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int 시작, int takininga_atuutilik, String 말) {
        if (!Nakatigat(시작, takininga_atuutilik)) return false;
        int 읽는자리 = 시작, 끝 = 시작 + takininga_atuutilik;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 말.length(); piliqqittaajuq_nalunaiqsimavik++) {
            int immikkuuqtumut_nalunaikkut = 말.charAt(piliqqittaajuq_nalunaiqsimavik);
            if (immikkuuqtumut_nalunaikkut > 0 && immikkuuqtumut_nalunaikkut < 128) { if (읽는자리 >= 끝 || ini[읽는자리++] != immikkuuqtumut_nalunaikkut) return false; }
            else if (immikkuuqtumut_nalunaikkut < 2048) {
                if (읽는자리 + 2 > 끝 || ini[읽는자리++] != (192 | (immikkuuqtumut_nalunaikkut >> 6)) || ini[읽는자리++] != (128 | (immikkuuqtumut_nalunaikkut & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || ini[읽는자리++] != (224 | (immikkuuqtumut_nalunaikkut >> 12)) || ini[읽는자리++] != (128 | ((immikkuuqtumut_nalunaikkut >> 6) & 63)) || ini[읽는자리++] != (128 | (immikkuuqtumut_nalunaikkut & 63))) return false;
        }
        return 읽는자리 == 끝;
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
    static int 상번호() { int atuutilik = 짧은수(); return atuutilik == 0 ? 0 : 현재읽는종 * 512 + atuutilik; }
    static int 명상수() { return 함수주인[틀함수[avalu_nalunaiqsimavik]] * 512 + 명짧(); }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !tammarniq; 수++) { qaujigiarli_surragunnangittuq(상번호(), 1); 건너(naasaut()); }
    }
    static int piqujijjut_takininga(int atuutilik) {
        if (atuutilik == 16 || atuutilik == 18 || atuutilik == 21 || atuutilik == 25 || atuutilik == 54 || atuutilik == 58 || atuutilik == 188) return 2;
        if (atuutilik == 17 || atuutilik == 19 || atuutilik == 132 || atuutilik >= 153 && atuutilik <= 167
            || atuutilik >= 178 && atuutilik <= 184 || atuutilik == 187 || atuutilik == 189 || atuutilik == 192 || atuutilik == 193 || atuutilik == 198 || atuutilik == 199) return 3;
        if (atuutilik == 185 || atuutilik == 200) return 5;
        if (atuutilik >= 0 && atuutilik <= 8 || atuutilik >= 26 && atuutilik <= 29 || atuutilik >= 42 && atuutilik <= 46 || atuutilik >= 50 && atuutilik <= 53
            || atuutilik >= 59 && atuutilik <= 62 || atuutilik >= 75 && atuutilik <= 79 || atuutilik >= 83 && atuutilik <= 95
            || atuutilik == 96 || atuutilik == 100 || atuutilik == 104 || atuutilik == 108 || atuutilik == 112 || atuutilik == 116
            || atuutilik == 120 || atuutilik == 122 || atuutilik == 124 || atuutilik == 126 || atuutilik == 128 || atuutilik == 130
            || atuutilik >= 145 && atuutilik <= 147 || atuutilik == 172 || atuutilik == 176 || atuutilik == 177 || atuutilik == 190 || atuutilik == 191
            || atuutilik == 194 || atuutilik == 195) return 1;
        return 0;
    }
    static int 위치정수(int 읽는자리) {
        if (!Nakatigat(읽는자리, 4)) { itigaqtuq_atuutilik("truncated bytecode operand"); return 0; }
        return ini[읽는자리] << 24 | ini[읽는자리 + 1] << 16 | ini[읽는자리 + 2] << 8 | ini[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int 시작, int 끝) {
        int atuutilik = ini[읽는자리], takininga_atuutilik = piqujijjut_takininga(atuutilik);
        if (atuutilik == 170 || atuutilik == 171) {
            int 기준자리 = 읽는자리 + 1;
            while ((기준자리 - 시작) % 4 != 0) 기준자리++;
            if (끝 - 기준자리 < (atuutilik == 170 ? 12 : 8)) return 0;
            int 항목수 = atuutilik == 170 ? 위치정수(기준자리 + 8) - 위치정수(기준자리 + 4) + 1 : 위치정수(기준자리 + 4);
            if (항목수 < 0 || 항목수 > 2048) return 0;
            takininga_atuutilik = 기준자리 - 읽는자리 + (atuutilik == 170 ? 12 + 4 * 항목수 : 8 + 8 * 항목수);
        }
        if (atuutilik == 196 && 읽는자리 + 1 < 끝) {
            int 단어값 = ini[읽는자리 + 1]; takininga_atuutilik = 단어값 == 132 ? 6 : (단어값 == 21 || 단어값 == 25 || 단어값 == 54 || 단어값 == 58) ? 4 : 0;
        }
        return takininga_atuutilik > 0 && takininga_atuutilik <= 끝 - 읽는자리 ? takininga_atuutilik : 0;
    }
    static void qaujigiarli_namunngarvik_atuutilik(int namunngarvik_atuutilik, int sugiakkannirut_atuutilik) {
        if (namunngarvik_atuutilik < 함수시작[sugiakkannirut_atuutilik] || namunngarvik_atuutilik >= 함수끝[sugiakkannirut_atuutilik] || 경계[namunngarvik_atuutilik] != sugiakkannirut_atuutilik + 1) itigaqtuq_atuutilik("invalid branch target");
    }
    static void 클래스읽기(int 종) {
        현재읽는종 = 종; 읽기위치 = 종 * 16384; anininga = 읽기위치 + 종크기[종];
        if (naasaut() != 0xcafebabe) { itigaqtuq_atuutilik("not a class file"); return; }
        int 부판 = 짧은수(), imaittuuninga_atuutilik = 짧은수();
        if (imaittuuninga_atuutilik < 45 || imaittuuninga_atuutilik > 52 || 부판 != 0) { itigaqtuq_atuutilik("supported class versions: 45..52, minor 0"); return; }
        int 상수수 = 짧은수(), 기준자리 = 종 * 512;
        if (상수수 < 1 || 상수수 > 512) { itigaqtuq_atuutilik("constant pool limit (511)"); return; }
        for (int 항목수 = 1; 항목수 < 상수수 && !tammarniq; 항목수++) {
            int 수 = 기준자리 + 항목수, 종류 = byte_atuutilik(); surragunnangittuq_nalunaikkutaq[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = naasaut();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); 상나[수] = 상번호(); }
            else itigaqtuq_atuutilik("unsupported constant type");
        }
        int pijunnaqtittijjut_atuutilik = 짧은수();
        if ((pijunnaqtittijjut_atuutilik & (0x2000 | 0x4000)) != 0) itigaqtuq_atuutilik("annotation/enum class unsupported");
        종이름[종] = naliannuungavik_atiq_titiqqaq(상번호());
        종부모[종] = naliannuungavik_atiq_titiqqaq(상번호());
        int 접면수 = 짧은수(); if (접면수 > 16) { itigaqtuq_atuutilik("interface count limit"); return; }
        종접면수[종] = 접면수;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 접면수; piliqqittaajuq_nalunaiqsimavik++) naliannuungavik_saqqijaagaq[종 * 16 + piliqqittaajuq_nalunaiqsimavik] = naliannuungavik_atiq_titiqqaq(상번호());
        int 필드수 = 짧은수();
        if (필드수 > 512 - 칸수) { itigaqtuq_atuutilik("field count limit (512)"); return; }
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 필드수 && !tammarniq; piliqqittaajuq_nalunaiqsimavik++) {
            int ini_nalunaiqsimavik = 칸수++; 칸주인[ini_nalunaiqsimavik] = 종; 칸권한[ini_nalunaiqsimavik] = 짧은수(); 칸이름[ini_nalunaiqsimavik] = 상번호(); 칸형[ini_nalunaiqsimavik] = 상번호();
            qaujigiarli_surragunnangittuq(칸이름[ini_nalunaiqsimavik], 1); qaujigiarli_surragunnangittuq(칸형[ini_nalunaiqsimavik], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[칸형[ini_nalunaiqsimavik]]; int 분류코드 = 서술형(읽기위치 + 상나[칸형[ini_nalunaiqsimavik]], false); 읽기위치 = 보존값;
            if ((칸권한[ini_nalunaiqsimavik] & 8) == 0) 칸위치[ini_nalunaiqsimavik] = 종칸수[종]++;
            int piuluqqutit_titiqqat = 짧은수();
            for (int 안쪽자리 = 0; 안쪽자리 < piuluqqutit_titiqqat && !tammarniq; 안쪽자리++) {
                int atiq_surragunnangittuq = 상번호(), 유효길이 = naasaut();
                if (말(atiq_surragunnangittuq, "ConstantValue") && 유효길이 == 2) {
                    int titiqqat_atuutilik = 상번호();
                    if (분류코드 == 1 && qaujigiarli_surragunnangittuq(titiqqat_atuutilik, 3)) 칸값[ini_nalunaiqsimavik] = 상가[titiqqat_atuutilik];
                    else if (분류코드 == 2 && qaujigiarli_surragunnangittuq(titiqqat_atuutilik, 8)) 칸값[ini_nalunaiqsimavik] = surragunnangittuq_titiqqaq(상가[titiqqat_atuutilik]);
                } else 건너(유효길이);
            }
        }
        int 개수 = 짧은수();
        if (개수 > 512 - 함수수) { itigaqtuq_atuutilik("method count limit (512)"); return; }
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 개수 && !tammarniq; piliqqittaajuq_nalunaiqsimavik++) {
            int 수 = 함수수++; 함수주인[수] = 종;
            함수권한[수] = 짧은수(); 함수명[수] = 상번호(); 함수형[수] = 상번호();
            qaujigiarli_surragunnangittuq(함수명[수], 1); 서술읽기(수);
            if ((함수권한[수] & 8) == 0) {
                if (함수인수수[수] == 16) { itigaqtuq_atuutilik("too many instance method arguments"); return; }
                for (int 비교자리 = 함수인수수[수]; 비교자리 > 0; 비교자리--) 함수인수형[수 * 16 + 비교자리] = 함수인수형[수 * 16 + 비교자리 - 1];
                함수인수형[수 * 16] = 2; 함수인수수[수]++;
            }
            if ((함수권한[수] & 0x100) != 0) itigaqtuq_atuutilik("user native method unsupported");
            if (말(함수명[수], "<clinit>")) 종초기화[종] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (함수주인[앞] == 종 && 같은말(함수명[앞], 함수명[수]) && 같은말(함수형[앞], 함수형[수])) itigaqtuq_atuutilik("duplicate method");
            int 속성수 = 짧은수();
            for (int piuluqqutit_atuutilik = 0; piuluqqutit_atuutilik < 속성수 && !tammarniq; piuluqqutit_atuutilik++) {
                int atiq = 상번호(), takininga_atuutilik = naasaut(), 시작 = 읽기위치;
                if (!Nakatigat(시작, takininga_atuutilik)) { itigaqtuq_atuutilik("truncated method attribute"); break; }
                if (말(atiq, "Code")) {
                    if (함수시작[수] != 0) itigaqtuq_atuutilik("duplicate Code attribute");
                    함수스택[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = naasaut();
                    if (함수스택[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) itigaqtuq_atuutilik("method memory limits exceeded");
                    함수시작[수] = 읽기위치; 건너(코드길이); 함수끝[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { itigaqtuq_atuutilik("exception table limit"); return; }
                    for (int 안쪽자리 = 0; 안쪽자리 < 잡는수; 안쪽자리++) {
                        int 오류참조 = 잡기수++; 잡기함수[오류참조] = 수;
                        잡기시작[오류참조] = 함수시작[수] + 짧은수(); 잡기끝[오류참조] = 함수시작[수] + 짧은수();
                        잡기위치[오류참조] = 함수시작[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[오류참조] = 부호값 == 0 ? 0 : naliannuungavik_atiq_titiqqaq(부호값);
                    }
                    속성건너();
                    if (읽기위치 != 시작 + takininga_atuutilik) itigaqtuq_atuutilik("Code attribute size mismatch");
                } else 건너(takininga_atuutilik);
            }
            if ((함수권한[수] & 0x400) != 0) continue;
            if (함수시작[수] == 0) itigaqtuq_atuutilik("missing Code attribute");
            int 칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !tammarniq) {
                int takininga_atuutilik = 길이읽기(칸, 함수시작[수], 함수끝[수]);
                if (takininga_atuutilik == 0) { itigaqtuq_atuutilik("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += takininga_atuutilik;
            }
            칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !tammarniq) {
                int atuutilik = ini[칸];
                if (atuutilik >= 153 && atuutilik <= 167 || atuutilik == 198 || atuutilik == 199) qaujigiarli_namunngarvik_atuutilik(칸 + (short)(ini[칸 + 1] << 8 | ini[칸 + 2]), 수);
                if (atuutilik == 200) qaujigiarli_namunngarvik_atuutilik(칸 + 위치정수(칸 + 1), 수);
                if (atuutilik == 170 || atuutilik == 171) {
                    int 읽는자리 = 칸 + 1; while ((읽는자리 - 함수시작[수]) % 4 != 0) 읽는자리++;
                    qaujigiarli_namunngarvik_atuutilik(칸 + 위치정수(읽는자리), 수);
                    int 항목수 = atuutilik == 170 ? 위치정수(읽는자리 + 8) - 위치정수(읽는자리 + 4) + 1 : 위치정수(읽는자리 + 4);
                    읽는자리 += atuutilik == 170 ? 12 : 8;
                    for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) qaujigiarli_namunngarvik_atuutilik(칸 + 위치정수(읽는자리 + 안쪽자리 * (atuutilik == 170 ? 4 : 8) + (atuutilik == 170 ? 0 : 4)), 수);
                }
                칸 += 길이읽기(칸, 함수시작[수], 함수끝[수]);
            }
            for (int 안쪽자리 = 0; 안쪽자리 < 잡기수; 안쪽자리++) if (잡기함수[안쪽자리] == 수) {
                qaujigiarli_namunngarvik_atuutilik(잡기시작[안쪽자리], 수); qaujigiarli_namunngarvik_atuutilik(잡기위치[안쪽자리], 수);
                if (잡기끝[안쪽자리] != 함수끝[수]) qaujigiarli_namunngarvik_atuutilik(잡기끝[안쪽자리], 수);
                if (잡기시작[안쪽자리] >= 잡기끝[안쪽자리]) itigaqtuq_atuutilik("invalid exception range");
            }
        }
        if (!tammarniq) 속성건너();
        if (읽기위치 != anininga) itigaqtuq_atuutilik("extra class file data");
    }
    static int 할당(int 종류, int takininga_atuutilik) { return 새기억(종류, takininga_atuutilik); }
    static boolean kisu_atuutilik(int 참조, int 종류) {
        if (!객체유효(참조)) return false;
        if (힙[참조] != 종류) { itigaqtuq_atuutilik("object type mismatch"); return false; }
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
        if (반환형 == 2) pijjairli_atuutilik(스택값[칸]);
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
        if (avalu_nalunaiqsimavik % 32 == 31) { itigaqtuq_atuutilik("call stack limit (32)"); return; }
        int 다음 = avalu_nalunaiqsimavik + 1;
        for (int 수 = 0; 수 < 128; 수++) tamaani_qanuittuuninga[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[sugiakkannirut_atuutilik] - 1; 수 >= 0; 수--) {
            tamaani_atuutilik[다음 * 128 + 수] = 빼기(함수인수형[sugiakkannirut_atuutilik * 16 + 수]); tamaani_qanuittuuninga[다음 * 128 + 수] = 함수인수형[sugiakkannirut_atuutilik * 16 + 수];
        }
        if (tammarniq) return;
        avalu_nalunaiqsimavik = 다음; aturunnaqsili_avalu[avalu_nalunaiqsimavik] = 0; 틀함수[avalu_nalunaiqsimavik] = sugiakkannirut_atuutilik; 틀위치[avalu_nalunaiqsimavik] = 함수시작[sugiakkannirut_atuutilik]; 틀스택[avalu_nalunaiqsimavik] = 0;
    }
    static void 반환(int qanuittuuninga_atuutilik) {
        if (qanuittuuninga_atuutilik != 함수반환[틀함수[avalu_nalunaiqsimavik]]) { itigaqtuq_atuutilik("return type mismatch"); return; }
        int atuutilik = qanuittuuninga_atuutilik == 0 ? 0 : 빼기(qanuittuuninga_atuutilik);
        if (aturunnaqsili_avalu[avalu_nalunaiqsimavik] != 0) 종상태[aturunnaqsili_avalu[avalu_nalunaiqsimavik] - 1] = 2;
        if (틀잠금[avalu_nalunaiqsimavik] != 0) { 잠금풀기(틀잠금[avalu_nalunaiqsimavik]); 틀잠금[avalu_nalunaiqsimavik] = 0; }
        avalu_nalunaiqsimavik--; if (avalu_nalunaiqsimavik >= 현재가닥 * 32 && qanuittuuninga_atuutilik != 0) 넣기(atuutilik, qanuittuuninga_atuutilik);
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
                if (atuutilik < 1) { itigaqtuq_atuutilik("invalid file stream path"); return; }
                ingirrania_aulataup_ini_atiq[칸] = atuutilik;
            }
            ingirrania_aulataup_ini_atiq[takininga_atuutilik] = 0;
            int 서술자 = atuqtuq.파일서술자열기(ingirrania_aulataup_ini_atiq, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { itigaqtuq_atuutilik("FileNotFoundException: file open failed"); return; }
            힙[ingirrania_aulataup_atuutilik + 2] = 서술자; 힙[ingirrania_aulataup_atuutilik + 3] = 1;
            return;
        }
        if (piqujijjut != 182) { itigaqtuq_atuutilik("invalid file stream invocation"); return; }
        if ((출력 && 말(atiq, "write") || !출력 && 말(atiq, "read"))
            && (말(aaqqisurli_atuutilik, 출력 ? "([B)V" : "([B)I") || 말(aaqqisurli_atuutilik, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean Nakatigat_atuutilik = 말(aaqqisurli_atuutilik, 출력 ? "([BII)V" : "([BII)I");
            int 항목수 = Nakatigat_atuutilik ? 빼기(1) : 0, 시작점 = Nakatigat_atuutilik ? 빼기(1) : 0, titiqqat_array = 빼기(2), 객체참조 = 빼기(2);
            if (!kisu_atuutilik(titiqqat_array, 20) || !kisu_atuutilik(객체참조, 종류)) return;
            if (!Nakatigat_atuutilik) 항목수 = 힙[titiqqat_array + 1];
            if (시작점 < 0 || 항목수 < 0 || 시작점 > 힙[titiqqat_array + 1] - 항목수) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[객체참조 + 3] == 0 || 힙[객체참조 + 2] < 0) { itigaqtuq_atuutilik("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < 항목수 && !tammarniq) {
                int 반환값 = 출력 ? atuqtuq.파일한바이트쓰기(힙[객체참조 + 2], 힙[titiqqat_array + 2 + 시작점 + 완료수]) : atuqtuq.파일한바이트읽기(힙[객체참조 + 2]);
                if (반환값 < 0) { itigaqtuq_atuutilik(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[titiqqat_array + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(항목수 != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && 말(atiq, "flush") && 말(aaqqisurli_atuutilik, "()V")) { int 객체참조 = 빼기(2); if (kisu_atuutilik(객체참조, 종류) && 힙[객체참조 + 2] < 0) itigaqtuq_atuutilik("IOException: stream closed"); return; }
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
            if (결과 < -1) itigaqtuq_atuutilik("IOException: read failed"); else 넣기(결과 == 256 ? -1 : 결과, 1);
        } else if (atuqtuq.파일한바이트쓰기(서술자, atuutilik) != 1) itigaqtuq_atuutilik("IOException: write failed");
    }
    static void 함수호출(int nalunaiqsimavik, int piqujijjut) {
        if (nalunaiqsimavik <= 0 || nalunaiqsimavik >= surragunnangittuq_nalunaikkutaq.length || (surragunnangittuq_nalunaikkutaq[nalunaiqsimavik] != 10 && surragunnangittuq_nalunaikkutaq[nalunaiqsimavik] != 11)) { itigaqtuq_atuutilik("invalid method reference"); return; }
        int 소유 = naliannuungavik_atiq_titiqqaq(상가[nalunaiqsimavik]), atiq = 참조이름(상나[nalunaiqsimavik]), aaqqisurli_atuutilik = 참조형식(상나[nalunaiqsimavik]);
        if (tammarniq) return;
        if (기본호출(소유, atiq, aaqqisurli_atuutilik, piqujijjut)) return;
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
        int 종 = 종찾기(소유); if (종 < 0 || tammarniq) return;
        int ini_nalunaiqsimavik = 함수찾기(종, atiq, aaqqisurli_atuutilik);
        if (ini_nalunaiqsimavik < 0) {
            for (int immikkuuqtumut_nalunaikkut = 종, 항목수 = 0; immikkuuqtumut_nalunaikkut >= 0 && 항목수 < 16; 항목수++, immikkuuqtumut_nalunaikkut = 부모종(immikkuuqtumut_nalunaikkut))
                if (말(종부모[immikkuuqtumut_nalunaikkut], "java/lang/Thread")) { 가닥호출(atiq, aaqqisurli_atuutilik, piqujijjut); return; }
            itigaqtuq_atuutilik("NoSuchMethodError"); return;
        }
        if (((함수권한[ini_nalunaiqsimavik] & 8) != 0) != (piqujijjut == 184)) { itigaqtuq_atuutilik("method static/instance mismatch"); return; }
        if (piqujijjut == 184) { if (!aturunnaqsili(함수주인[ini_nalunaiqsimavik], avalu_maligialiit[avalu_nalunaiqsimavik])) return; }
        else {
            int 읽는자리 = 틀스택[avalu_nalunaiqsimavik] - 함수인수수[ini_nalunaiqsimavik];
            if (읽는자리 < 0 || 스택형[avalu_nalunaiqsimavik * 128 + 읽는자리] != 2) { itigaqtuq_atuutilik("invalid method receiver"); return; }
            int 객체참조 = 스택값[avalu_nalunaiqsimavik * 128 + 읽는자리];
            if (!객체유효(객체참조)) return;
            if (힙[객체참조] < 32 || !종포함(힙[객체참조] - 32, 소유)) { itigaqtuq_atuutilik("method receiver type mismatch"); return; }
            if (piqujijjut != 183) ini_nalunaiqsimavik = 함수찾기(힙[객체참조] - 32, atiq, aaqqisurli_atuutilik);
        }
        if (ini_nalunaiqsimavik < 0 || (함수권한[ini_nalunaiqsimavik] & 0x400) != 0) { itigaqtuq_atuutilik("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((함수권한[ini_nalunaiqsimavik] & 32) != 0) {
            if (piqujijjut == 184) { int immikkuuqtumut_nalunaikkut = 함수주인[ini_nalunaiqsimavik]; if (종잠금[immikkuuqtumut_nalunaikkut] == 0) 종잠금[immikkuuqtumut_nalunaikkut] = 할당(8, 0); 잠금참조 = 종잠금[immikkuuqtumut_nalunaikkut]; }
            else 잠금참조 = 스택값[avalu_nalunaiqsimavik * 128 + 틀스택[avalu_nalunaiqsimavik] - 함수인수수[ini_nalunaiqsimavik]];
            if (!잠금얻기(잠금참조)) { if (!tammarniq) 틀위치[avalu_nalunaiqsimavik] = avalu_maligialiit[avalu_nalunaiqsimavik]; return; }
        }
        호출(ini_nalunaiqsimavik); if (!tammarniq) 틀잠금[avalu_nalunaiqsimavik] = 잠금참조;
    }
    static boolean 배열저장가능(int 배열참조, int titiqqat_atuutilik) {
        if (titiqqat_atuutilik == 0 || array_ilanga[배열참조] == 0) return true;
        boolean 성공여부 = array_ilanga[배열참조] == -1 ? (titiqqat_atuutilik > 0 && titiqqat_atuutilik < 힙끝 && 힙[titiqqat_atuutilik] == 1) : 맞는객체(titiqqat_atuutilik, array_ilanga[배열참조]);
        if (!성공여부 && !tammarniq) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int 배열칸(int 참조, int qulikkanniagut_titiraqsimajuq_atuutilik, int qanuittuuninga_atuutilik) {
        if (!kisu_atuutilik(참조, qanuittuuninga_atuutilik)) return 0;
        if (qulikkanniagut_titiraqsimajuq_atuutilik < 0 || qulikkanniagut_titiraqsimajuq_atuutilik >= 힙[참조 + 1]) { itigaqtuq_atuutilik("ArrayIndexOutOfBoundsException"); return 0; }
        return 참조 + 2 + qulikkanniagut_titiraqsimajuq_atuutilik;
    }
    static void 실행() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (tammarniq) { if (던진객체 != 0) 예외처리(); if (tammarniq || avalu_nalunaiqsimavik < 현재가닥 * 32) break; }
            if (avalu_nalunaiqsimavik < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!kipulli_aqqusiqtarvik()) break; 조각 = 100; }
            if (avalu_nalunaiqsimavik == 0 && 종상태[시작종] != 2 && !aturunnaqsili(시작종, 틀위치[avalu_nalunaiqsimavik])) continue;
            if (avalu_nalunaiqsimavik == 현재가닥 * 32 && 현재가닥 != 0 && (함수권한[틀함수[avalu_nalunaiqsimavik]] & 32) != 0 && 틀잠금[avalu_nalunaiqsimavik] == 0) {
                int 객체참조 = aqqusiqtarvik_turaagaq[현재가닥]; if (!잠금얻기(객체참조)) { if (tammarniq) break; continue; } 틀잠금[avalu_nalunaiqsimavik] = 객체참조;
            }
            잠시수 = 0;
            if (--남음 == 0) { itigaqtuq_atuutilik("instruction limit (500000)"); break; }
            int 시작 = 틀위치[avalu_nalunaiqsimavik]; avalu_maligialiit[avalu_nalunaiqsimavik] = 시작; int atuutilik = 명바();
            if (tammarniq) break;
            if (atuutilik == 0) continue;
            if (atuutilik == 1) { 넣기(0, 2); continue; }
            if (atuutilik >= 2 && atuutilik <= 8) { 넣기(atuutilik - 3, 1); continue; }
            if (atuutilik == 16) { 넣기((byte)명바(), 1); continue; }
            if (atuutilik == 17) { 넣기((short)명짧(), 1); continue; }
            if (atuutilik == 18 || atuutilik == 19) {
                int 수 = 함수주인[틀함수[avalu_nalunaiqsimavik]] * 512 + (atuutilik == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= surragunnangittuq_nalunaikkutaq.length) itigaqtuq_atuutilik("invalid ldc constant");
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
            if (atuutilik == 46 || atuutilik >= 50 && atuutilik <= 53) {
                int 항목자리 = 빼기(1), 객체참조 = 빼기(2), 분류코드 = atuutilik == 46 ? 2 : atuutilik == 50 ? 3 : atuutilik == 51 ? 20 : atuutilik == 52 ? 22 : 23;
                if (atuutilik == 51 && 객체참조 > 0 && 객체참조 < 힙끝 && 힙[객체참조] == 21) 분류코드 = 21;
                int 읽는자리 = 배열칸(객체참조, 항목자리, 분류코드); if (!tammarniq) 넣기(힙[읽는자리], atuutilik == 50 ? 2 : 1); continue;
            }
            if (atuutilik == 79 || atuutilik >= 83 && atuutilik <= 86) {
                int 항목참조 = 빼기(atuutilik == 83 ? 2 : 1), 항목자리 = 빼기(1), 객체참조 = 빼기(2), 분류코드 = atuutilik == 79 ? 2 : atuutilik == 83 ? 3 : atuutilik == 84 ? 20 : atuutilik == 85 ? 22 : 23;
                if (atuutilik == 84 && 객체참조 > 0 && 객체참조 < 힙끝 && 힙[객체참조] == 21) 분류코드 = 21;
                int 읽는자리 = 배열칸(객체참조, 항목자리, 분류코드);
                if (!tammarniq && 분류코드 == 3 && !배열저장가능(객체참조, 항목참조)) continue;
                if (!tammarniq) 힙[읽는자리] = 분류코드 == 20 ? (byte)항목참조 : 분류코드 == 21 ? 항목참조 & 1 : 분류코드 == 22 ? (char)항목참조 : 분류코드 == 23 ? (short)항목참조 : 항목참조;
                continue;
            }
            if (atuutilik >= 87 && atuutilik <= 95) { 스택명령(atuutilik); continue; }
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
            if (atuutilik >= 178 && atuutilik <= 181) { 필드호출(명상수(), atuutilik, 시작); continue; }
            if (atuutilik >= 182 && atuutilik <= 185) {
                int 부호값 = 명상수();
                if (atuutilik == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { itigaqtuq_atuutilik("invalid invokeinterface operands"); continue; } }
                함수호출(부호값, atuutilik); continue;
            }
            if (atuutilik == 187) { 새객체(naliannuungavik_atiq_titiqqaq(명상수()), 시작); continue; }
            if (atuutilik == 188 || atuutilik == 189) {
                int 분류코드 = 3, Ilanga = 0;
                if (atuutilik == 188) { int 임시값 = 명바(); 분류코드 = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else Ilanga = naliannuungavik_atiq_titiqqaq(명상수());
                if (분류코드 == 0) { itigaqtuq_atuutilik("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), 객체참조 = 할당(분류코드, 유효길이); if (!tammarniq) array_ilanga[객체참조] = Ilanga; 넣기(객체참조, 2); continue;
            }
            if (atuutilik == 190) {
                int 객체참조 = 빼기(2);
                if (객체유효(객체참조)) { int 비교자리 = 힙[객체참조]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) itigaqtuq_atuutilik("not an array"); else 넣기(힙[객체참조 + 1], 1); }
                continue;
            }
            if (atuutilik == 191) {
                int 객체참조 = 빼기(2); if (객체유효(객체참조)) { if (힙[객체참조] != 9) itigaqtuq_atuutilik("athrow requires supported Throwable"); else { 던진객체 = 객체참조; tammarniq = true; } }
                continue;
            }
            if (atuutilik == 192 || atuutilik == 193) {
                int atiq_surragunnangittuq = naliannuungavik_atiq_titiqqaq(명상수()), 객체참조 = 빼기(2); boolean 일치여부 = 맞는객체(객체참조, atiq_surragunnangittuq);
                if (atuutilik == 193) 넣기(객체참조 != 0 && 일치여부 ? 1 : 0, 1);
                else { if (!일치여부 && !tammarniq) itigaqtuq_atuutilik("ClassCastException"); 넣기(객체참조, 2); }
                continue;
            }
            if (atuutilik == 170 || atuutilik == 171) {
                int 읽는자리 = 시작 + 1, ini_nalunaiqsimavik = 틀함수[avalu_nalunaiqsimavik], 키참조 = 빼기(1);
                while ((읽는자리 - 함수시작[ini_nalunaiqsimavik]) % 4 != 0) 읽는자리++;
                int turaagaq_turaarut = 위치정수(읽는자리);
                if (atuutilik == 170) { int 낮은값 = 위치정수(읽는자리 + 4), 높은값 = 위치정수(읽는자리 + 8); if (키참조 >= 낮은값 && 키참조 <= 높은값) turaagaq_turaarut = 위치정수(읽는자리 + 12 + (키참조 - 낮은값) * 4); }
                else { int 총수 = 위치정수(읽는자리 + 4); for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 총수; piliqqittaajuq_nalunaiqsimavik++) if (위치정수(읽는자리 + 8 + piliqqittaajuq_nalunaiqsimavik * 8) == 키참조) turaagaq_turaarut = 위치정수(읽는자리 + 12 + piliqqittaajuq_nalunaiqsimavik * 8); }
                nuulli_atuutilik(시작 + turaagaq_turaarut); continue;
            }
            if (atuutilik == 200) { nuulli_atuutilik(시작 + 위치정수(시작 + 1)); continue; }
            if (atuutilik == 194 || atuutilik == 195) {
                int 객체참조 = 빼기(2);
                if (atuutilik == 195) 잠금풀기(객체참조);
                else if (!잠금얻기(객체참조) && !tammarniq) { 넣기(객체참조, 2); 틀위치[avalu_nalunaiqsimavik] = 시작; }
                continue;
            }
            if (atuutilik == 196) {
                int 명령코드 = 명바(), 항목자리 = 명짧();
                if (명령코드 == 21 || 명령코드 == 25) 지역읽기(항목자리, 명령코드 == 21 ? 1 : 2);
                else if (명령코드 == 54 || 명령코드 == 58) titiraq_tamaani(항목자리, 명령코드 == 54 ? 1 : 2);
                else if (명령코드 == 132) { int 변화량 = (short)명짧(); 지역읽기(항목자리, 1); 넣기(빼기(1) + 변화량, 1); titiraq_tamaani(항목자리, 1); }
                else itigaqtuq_atuutilik("unsupported wide opcode");
                continue;
            }
            itigaqtuq_atuutilik("unsupported bytecode");
        }
    }
    static int 종찾기(int atiq) {
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 종수; piliqqittaajuq_nalunaiqsimavik++) if (종이름[piliqqittaajuq_nalunaiqsimavik] != 0 && 같은말(종이름[piliqqittaajuq_nalunaiqsimavik], atiq)) return piliqqittaajuq_nalunaiqsimavik;
        return 종적재(surragunnangittuq_titiqqaq(atiq));
    }
    static int 종적재(int atiq_qimiaq) {
        if (!kisu_atuutilik(atiq_qimiaq, 1)) return -1;
        int takininga_atuutilik = 힙[atiq_qimiaq + 1];
        if (takininga_atuutilik < 1 || takininga_atuutilik > 505 || 종수 == 16) { itigaqtuq_atuutilik("class name/count limit"); return -1; }
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < takininga_atuutilik; piliqqittaajuq_nalunaiqsimavik++) { int immikkuuqtumut_nalunaikkut = 힙[atiq_qimiaq + 2 + piliqqittaajuq_nalunaiqsimavik]; ini_atiq_titiqqaq[piliqqittaajuq_nalunaiqsimavik] = immikkuuqtumut_nalunaikkut == '/' ? '.' : immikkuuqtumut_nalunaikkut; }
        ini_atiq_titiqqaq[takininga_atuutilik] = '.'; ini_atiq_titiqqaq[takininga_atuutilik + 1] = 'c'; ini_atiq_titiqqaq[takininga_atuutilik + 2] = 'l'; ini_atiq_titiqqaq[takininga_atuutilik + 3] = 'a'; ini_atiq_titiqqaq[takininga_atuutilik + 4] = 's'; ini_atiq_titiqqaq[takininga_atuutilik + 5] = 's'; ini_atiq_titiqqaq[takininga_atuutilik + 6] = 0;
        int anininga = atuqtuq.파일읽기(ini_atiq_titiqqaq, 임시파일);
        if (anininga < 0) { itigaqtuq_atuutilik("ClassNotFoundException"); return -1; }
        int 종 = 종수++; 종크기[종] = anininga;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < anininga; piliqqittaajuq_nalunaiqsimavik++) ini[종 * 16384 + piliqqittaajuq_nalunaiqsimavik] = 임시파일[piliqqittaajuq_nalunaiqsimavik];
        클래스읽기(종); if (tammarniq) return -1;
        int taannallarik_titiqqat = surragunnangittuq_titiqqaq(종이름[종]);
        if (!글같음(taannallarik_titiqqat, atiq_qimiaq, true)) { itigaqtuq_atuutilik("class name does not match file"); return -1; }
        int 부모 = 종부모[종];
        if (부모 != 0 && !말(부모, "java/lang/Object") && !말(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = 종찾기(부모);
            if (tammarniq || 위 < 0) return -1;
            int 읽는자리 = 위, 단계수 = 0;
            while (읽는자리 >= 0 && 단계수++ < 16) {
                if (읽는자리 == 종) { itigaqtuq_atuutilik("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int ini_nalunaiqsimavik = 0; ini_nalunaiqsimavik < 칸수; ini_nalunaiqsimavik++) if (칸주인[ini_nalunaiqsimavik] == 종 && (칸권한[ini_nalunaiqsimavik] & 8) == 0) 칸위치[ini_nalunaiqsimavik] += 시작변위;
            종칸수[종] += 시작변위;
        }
        return 종;
    }
    static int 부모종(int 종) {
        int atiq = 종부모[종];
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 종수; piliqqittaajuq_nalunaiqsimavik++) if (atiq != 0 && 종이름[piliqqittaajuq_nalunaiqsimavik] != 0 && 같은말(종이름[piliqqittaajuq_nalunaiqsimavik], atiq)) return piliqqittaajuq_nalunaiqsimavik;
        return -1;
    }
    static int 함수찾기(int 종, int atiq, int aaqqisurli_atuutilik) {
        for (int 깊이 = 0; 종 >= 0 && 깊이 < 16; 깊이++, 종 = 부모종(종)) {
            for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 함수수; piliqqittaajuq_nalunaiqsimavik++) if (함수주인[piliqqittaajuq_nalunaiqsimavik] == 종 && 같은말(함수명[piliqqittaajuq_nalunaiqsimavik], atiq) && 같은말(함수형[piliqqittaajuq_nalunaiqsimavik], aaqqisurli_atuutilik)) return piliqqittaajuq_nalunaiqsimavik;
        }
        return -1;
    }
    static int 이름함수(int 종, String atiq, String aaqqisurli_atuutilik) {
        for (int 깊이 = 0; 종 >= 0 && 깊이 < 16; 깊이++, 종 = 부모종(종))
            for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 함수수; piliqqittaajuq_nalunaiqsimavik++) if (함수주인[piliqqittaajuq_nalunaiqsimavik] == 종 && 말(함수명[piliqqittaajuq_nalunaiqsimavik], atiq) && 말(함수형[piliqqittaajuq_nalunaiqsimavik], aaqqisurli_atuutilik)) return piliqqittaajuq_nalunaiqsimavik;
        return -1;
    }
    static int 형종류(int atiq) { return ini[상가[atiq]] == 'L' || ini[상가[atiq]] == '[' ? 2 : 1; }
    static boolean aturunnaqsili(int 종, int piqujijjut_pigiarli) {
        if (종 < 0 || tammarniq) return false;
        if (종상태[종] == 3) { itigaqtuq_atuutilik("NoClassDefFoundError: initialization failed"); return false; }
        if (종상태[종] == 1 && naliannuungavik_aqqusiqtarvik[종] != 현재가닥) { 틀위치[avalu_nalunaiqsimavik] = piqujijjut_pigiarli; 바꿈요청 = true; return false; }
        if (종상태[종] != 0) return true;
        int 위 = 부모종(종);
        if (위 >= 0 && !aturunnaqsili(위, piqujijjut_pigiarli)) return false;
        종상태[종] = 1; naliannuungavik_aqqusiqtarvik[종] = 현재가닥;
        if (종초기화[종] != 0) {
            틀위치[avalu_nalunaiqsimavik] = piqujijjut_pigiarli;
            호출(종초기화[종] - 1); if (!tammarniq) aturunnaqsili_avalu[avalu_nalunaiqsimavik] = 종 + 1;
            return false;
        }
        종상태[종] = 2; return true;
    }
    static void 필드호출(int nalunaiqsimavik, int piqujijjut, int 시작) {
        if (!qaujigiarli_surragunnangittuq(nalunaiqsimavik, 9)) return;
        int 소유 = naliannuungavik_atiq_titiqqaq(상가[nalunaiqsimavik]), atiq = 참조이름(상나[nalunaiqsimavik]), aaqqisurli_atuutilik = 참조형식(상나[nalunaiqsimavik]);
        if (말(소유, "java/lang/System") && (말(atiq, "out") || 말(atiq, "err")) && 말(aaqqisurli_atuutilik, "Ljava/io/PrintStream;") && piqujijjut == 178) { 넣기(-1, 2); return; }
        int 종 = 종찾기(소유); if (종 < 0 || tammarniq) return;
        int 찾음 = -1;
        for (int 읽는자리 = 종, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int ini_nalunaiqsimavik = 0; ini_nalunaiqsimavik < 칸수; ini_nalunaiqsimavik++) if (칸주인[ini_nalunaiqsimavik] == 읽는자리 && 같은말(칸이름[ini_nalunaiqsimavik], atiq) && 같은말(칸형[ini_nalunaiqsimavik], aaqqisurli_atuutilik)) 찾음 = ini_nalunaiqsimavik;
        if (찾음 < 0) { itigaqtuq_atuutilik("NoSuchFieldError"); return; }
        boolean surravviqanngittuq_atuutilik = piqujijjut == 178 || piqujijjut == 179;
        if (surravviqanngittuq_atuutilik != ((칸권한[찾음] & 8) != 0)) { itigaqtuq_atuutilik("field static/instance mismatch"); return; }
        if (surravviqanngittuq_atuutilik && !aturunnaqsili(칸주인[찾음], 시작)) return;
        int qanuittuuninga_atuutilik = 형종류(aaqqisurli_atuutilik), atuutilik = 0;
        if (piqujijjut == 179 || piqujijjut == 181) atuutilik = 빼기(qanuittuuninga_atuutilik);
        if (surravviqanngittuq_atuutilik) { if (piqujijjut == 178) 넣기(칸값[찾음], qanuittuuninga_atuutilik); else if (!tammarniq) 칸값[찾음] = atuutilik; return; }
        int 객체참조 = 빼기(2);
        if (!객체유효(객체참조)) return;
        if (힙[객체참조] < 32 || !종포함(힙[객체참조] - 32, 소유)) { itigaqtuq_atuutilik("field receiver type mismatch"); return; }
        int 보관칸 = 객체참조 + 2 + 칸위치[찾음];
        if (piqujijjut == 180) 넣기(힙[보관칸], qanuittuuninga_atuutilik);
        else if (!tammarniq) { 힙[보관칸] = atuutilik; 힙참조[보관칸] = qanuittuuninga_atuutilik == 2 ? 1 : 0; }
    }
    static boolean 종포함(int 종, int atiq) {
        for (int 중첩깊이 = 0; 종 >= 0 && 중첩깊이 < 16; 중첩깊이++, 종 = 부모종(종)) {
            if (같은말(종이름[종], atiq) || (종부모[종] != 0 && 같은말(종부모[종], atiq))) return true;
            for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[종]; 안쪽자리++) if (같은말(naliannuungavik_saqqijaagaq[종 * 16 + 안쪽자리], atiq)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int byte_titiqqat, boolean aqqut) {
        if (첫값 == byte_titiqqat) return true;
        if (첫값 <= 0 || byte_titiqqat <= 0 || 힙[첫값] != 1 || 힙[byte_titiqqat] != 1 || 힙[첫값 + 1] != 힙[byte_titiqqat + 1]) return false;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 힙[첫값 + 1]; piliqqittaajuq_nalunaiqsimavik++) {
            int 가로좌표 = 힙[첫값 + 2 + piliqqittaajuq_nalunaiqsimavik], 세로좌표 = 힙[byte_titiqqat + 2 + piliqqittaajuq_nalunaiqsimavik];
            if (aqqut) { if (가로좌표 == '.') 가로좌표 = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (가로좌표 != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int 객체참조) {
        if (객체참조 == 0) { itigaqtuq_atuutilik("NullPointerException"); return false; }
        if (객체참조 < 1 || 객체참조 >= 힙끝 || 힙폭[객체참조] < 2 || 힙[객체참조] == 0) { itigaqtuq_atuutilik("invalid object reference"); return false; }
        return true;
    }
    static void pijjairli_atuutilik(int 객체참조) {
        if (객체참조 > 0 && 객체참조 < 힙끝 && 힙폭[객체참조] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = 객체참조;
    }
    static void saqqilli_atuutilik(int 객체참조) {
        if (객체참조 > 0 && 객체참조 < 힙끝 && 힙폭[객체참조] >= 2 && 힙[객체참조] != 0 && 힙표시[객체참조] == 0) {
            힙표시[객체참조] = 1; 표시대기[표시수++] = 객체참조;
        }
    }
    static void 수거() {
        표시수 = 0; 수거횟수++;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) 힙표시[검사자리] = 0;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 문자열참조.length; piliqqittaajuq_nalunaiqsimavik++) saqqilli_atuutilik(문자열참조[piliqqittaajuq_nalunaiqsimavik]);
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 칸수; piliqqittaajuq_nalunaiqsimavik++) if ((칸권한[piliqqittaajuq_nalunaiqsimavik] & 8) != 0 && 형종류(칸형[piliqqittaajuq_nalunaiqsimavik]) == 2) saqqilli_atuutilik(칸값[piliqqittaajuq_nalunaiqsimavik]);
        for (int 임시값 = 0; 임시값 < 가닥수; 임시값++) {
            saqqilli_atuutilik(aqqusiqtarvik_kisu[임시값]); saqqilli_atuutilik(aqqusiqtarvik_turaagaq[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? avalu_nalunaiqsimavik : aqqusiqtarvik_avalu[임시값];
            for (int ini_nalunaiqsimavik = 임시값 * 32; ini_nalunaiqsimavik <= 꼭대기자리; ini_nalunaiqsimavik++) {
                for (int 안쪽자리 = 0; 안쪽자리 < 함수지역[틀함수[ini_nalunaiqsimavik]]; 안쪽자리++) if (tamaani_qanuittuuninga[ini_nalunaiqsimavik * 128 + 안쪽자리] == 2) saqqilli_atuutilik(tamaani_atuutilik[ini_nalunaiqsimavik * 128 + 안쪽자리]);
                for (int 안쪽자리 = 0; 안쪽자리 < 틀스택[ini_nalunaiqsimavik]; 안쪽자리++) if (스택형[ini_nalunaiqsimavik * 128 + 안쪽자리] == 2) saqqilli_atuutilik(스택값[ini_nalunaiqsimavik * 128 + 안쪽자리]);
            }
        }
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 화면참조.length; piliqqittaajuq_nalunaiqsimavik++) saqqilli_atuutilik(화면참조[piliqqittaajuq_nalunaiqsimavik]);
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 나중수; piliqqittaajuq_nalunaiqsimavik++) saqqilli_atuutilik(나중실행[piliqqittaajuq_nalunaiqsimavik]);
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < tuqqurli_naasaut.length; piliqqittaajuq_nalunaiqsimavik++) saqqilli_atuutilik(tuqqurli_naasaut[piliqqittaajuq_nalunaiqsimavik]);
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 종수; piliqqittaajuq_nalunaiqsimavik++) saqqilli_atuutilik(종잠금[piliqqittaajuq_nalunaiqsimavik]);
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (잠금깊이[검사자리] > 0) saqqilli_atuutilik(검사자리);
        saqqilli_atuutilik(던진객체);
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 잠시수; piliqqittaajuq_nalunaiqsimavik++) saqqilli_atuutilik(잠시참조[piliqqittaajuq_nalunaiqsimavik]);
        while (표시수 > 0) {
            int 객체참조 = 표시대기[--표시수], 분류코드 = 힙[객체참조];
            for (int piliqqittaajuq_nalunaiqsimavik = 객체참조 + 2; piliqqittaajuq_nalunaiqsimavik < 객체참조 + 힙폭[객체참조]; piliqqittaajuq_nalunaiqsimavik++) if (분류코드 == 3 || 분류코드 == 4 || 힙참조[piliqqittaajuq_nalunaiqsimavik] != 0) saqqilli_atuutilik(힙[piliqqittaajuq_nalunaiqsimavik]);
        }
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙표시[검사자리] == 0) 힙[검사자리] = 0;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙[검사자리] == 0) {
            while (검사자리 + 힙폭[검사자리] < 힙끝 && 힙[검사자리 + 힙폭[검사자리]] == 0) { int 다음자리 = 검사자리 + 힙폭[검사자리]; 힙폭[검사자리] += 힙폭[다음자리]; 힙폭[다음자리] = 0; }
            if (검사자리 + 힙폭[검사자리] == 힙끝) { 힙끝 = 검사자리; break; }
        }
    }
    static int 새기억(int 종류, int takininga_atuutilik) {
        if (takininga_atuutilik < 0) { itigaqtuq_atuutilik("NegativeArraySizeException"); return 0; }
        if (takininga_atuutilik > 힙.length - 3) { itigaqtuq_atuutilik("object heap exhausted"); return 0; }
        int 필요수 = takininga_atuutilik + 2, 객체참조 = 0;
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
        if (객체참조 == 0) { itigaqtuq_atuutilik("object heap exhausted"); return 0; }
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 필요수; piliqqittaajuq_nalunaiqsimavik++) { 힙[객체참조 + piliqqittaajuq_nalunaiqsimavik] = 0; 힙참조[객체참조 + piliqqittaajuq_nalunaiqsimavik] = 0; 힙폭[객체참조 + piliqqittaajuq_nalunaiqsimavik] = 0; }
        array_ilanga[객체참조] = 0;
        힙폭[객체참조] = 필요수; 힙[객체참조] = 종류; 힙[객체참조 + 1] = takininga_atuutilik; pijjairli_atuutilik(객체참조); return 객체참조;
    }
    static int 예외종(String atiq_surragunnangittuq) {
        if (자바도구.같음(atiq_surragunnangittuq, "java/lang/Throwable")) return 1;
        if (자바도구.같음(atiq_surragunnangittuq, "java/lang/Exception")) return 2;
        if (자바도구.같음(atiq_surragunnangittuq, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(atiq_surragunnangittuq, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(atiq_surragunnangittuq, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(atiq_surragunnangittuq, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(atiq_surragunnangittuq, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(atiq_surragunnangittuq, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(atiq_surragunnangittuq, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(atiq_surragunnangittuq, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(atiq_surragunnangittuq, "java/io/IOException")) return 11;
        if (자바도구.같음(atiq_surragunnangittuq, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(atiq_surragunnangittuq, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(atiq_surragunnangittuq, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(atiq_surragunnangittuq, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int 예외상수(int atiq) {
        for (int piliqqittaajuq_nalunaiqsimavik = 1; piliqqittaajuq_nalunaiqsimavik <= 41; piliqqittaajuq_nalunaiqsimavik++) if (말(atiq, 예외이름(piliqqittaajuq_nalunaiqsimavik))) return piliqqittaajuq_nalunaiqsimavik;
        return 0;
    }
    static String 예외이름(int piqaut_atuutilik) {
        if (piqaut_atuutilik == 40) return "java/lang/InterruptedException";
        if (piqaut_atuutilik == 41) return "한국어/자체/대기중단예외";
        if (piqaut_atuutilik == 39) return "java/net/SocketException";
        if (piqaut_atuutilik == 20) return "한국어/자체/예외";
        if (piqaut_atuutilik == 21) return "한국어/자체/실행예외";
        if (piqaut_atuutilik == 22) return "한국어/자체/입출력예외";
        if (piqaut_atuutilik == 23) return "한국어/자체/대기시간초과예외";
        if (piqaut_atuutilik == 24) return "한국어/자체/주소확인예외";
        if (piqaut_atuutilik == 25) return "한국어/자체/파일없음예외";
        if (piqaut_atuutilik == 26) return "한국어/자체/통신예외";
        if (piqaut_atuutilik == 27) return "한국어/자체/잘못된인수예외";
        if (piqaut_atuutilik == 28) return "한국어/자체/숫자형식예외";
        if (piqaut_atuutilik == 29) return "한국어/자체/범위예외";
        if (piqaut_atuutilik == 30) return "한국어/자체/배열범위예외";
        if (piqaut_atuutilik == 31) return "한국어/자체/문자열범위예외";
        if (piqaut_atuutilik == 32) return "한국어/자체/빈참조예외";
        if (piqaut_atuutilik == 33) return "한국어/자체/산술예외";
        if (piqaut_atuutilik == 34) return "한국어/자체/상태예외";
        if (piqaut_atuutilik == 35) return "한국어/자체/형변환예외";
        if (piqaut_atuutilik == 36) return "한국어/자체/음수배열크기예외";
        if (piqaut_atuutilik == 37) return "한국어/자체/array_tuqqurli_itigaqtuq";
        if (piqaut_atuutilik == 38) return "한국어/자체/가닥상태예외";
        if (piqaut_atuutilik == 1) return "java/lang/Throwable"; if (piqaut_atuutilik == 2) return "java/lang/Exception";
        if (piqaut_atuutilik == 3) return "java/lang/RuntimeException"; if (piqaut_atuutilik == 4) return "java/lang/ArithmeticException";
        if (piqaut_atuutilik == 5) return "java/lang/NullPointerException"; if (piqaut_atuutilik == 6) return "java/lang/IndexOutOfBoundsException";
        if (piqaut_atuutilik == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (piqaut_atuutilik == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (piqaut_atuutilik == 9) return "java/lang/IllegalArgumentException"; if (piqaut_atuutilik == 10) return "java/lang/NumberFormatException";
        if (piqaut_atuutilik == 11) return "java/io/IOException"; if (piqaut_atuutilik == 12) return "java/io/FileNotFoundException";
        if (piqaut_atuutilik == 17) return "java/lang/ArrayStoreException";
        if (piqaut_atuutilik == 18) return "java/net/UnknownHostException";
        if (piqaut_atuutilik == 19) return "java/net/SocketTimeoutException";
        if (piqaut_atuutilik == 16) return "java/lang/IllegalThreadStateException";
        if (piqaut_atuutilik == 13) return "java/lang/IllegalStateException"; if (piqaut_atuutilik == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int piqaut_atuutilik) {
        if (piqaut_atuutilik == 40) return 2;
        if (piqaut_atuutilik == 41) return 40;
        if (piqaut_atuutilik == 39) return 11;
        if (piqaut_atuutilik == 1) return 0;
        if (piqaut_atuutilik == 2) return 1;
        if (piqaut_atuutilik == 3) return 2;
        if (piqaut_atuutilik == 4) return 3;
        if (piqaut_atuutilik == 5) return 3;
        if (piqaut_atuutilik == 6) return 3;
        if (piqaut_atuutilik == 7) return 6;
        if (piqaut_atuutilik == 8) return 6;
        if (piqaut_atuutilik == 9) return 3;
        if (piqaut_atuutilik == 10) return 9;
        if (piqaut_atuutilik == 11) return 2;
        if (piqaut_atuutilik == 12) return 11;
        if (piqaut_atuutilik == 13) return 3;
        if (piqaut_atuutilik == 14) return 3;
        if (piqaut_atuutilik == 15) return 3;
        if (piqaut_atuutilik == 16) return 9;
        if (piqaut_atuutilik == 17) return 3;
        if (piqaut_atuutilik == 18) return 11;
        if (piqaut_atuutilik == 19) return 11;
        if (piqaut_atuutilik == 20) return 2;
        if (piqaut_atuutilik == 21) return 3;
        if (piqaut_atuutilik == 22) return 11;
        if (piqaut_atuutilik == 23) return 22;
        if (piqaut_atuutilik == 24) return 22;
        if (piqaut_atuutilik == 25) return 22;
        if (piqaut_atuutilik == 26) return 22;
        if (piqaut_atuutilik == 27) return 9;
        if (piqaut_atuutilik == 28) return 27;
        if (piqaut_atuutilik == 29) return 6;
        if (piqaut_atuutilik == 30) return 29;
        if (piqaut_atuutilik == 31) return 29;
        if (piqaut_atuutilik == 32) return 5;
        if (piqaut_atuutilik == 33) return 4;
        if (piqaut_atuutilik == 34) return 13;
        if (piqaut_atuutilik == 35) return 14;
        if (piqaut_atuutilik == 36) return 15;
        if (piqaut_atuutilik == 37) return 17;
        if (piqaut_atuutilik == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int taannallarik_atuutilik, int 요구값) {
        for (int 깊이 = 0; taannallarik_atuutilik != 0 && 깊이 < 16; 깊이++, taannallarik_atuutilik = 예외부모(taannallarik_atuutilik))
            if (taannallarik_atuutilik == 요구값) return true;
        return false;
    }
    static void 예외던짐(int piqaut_atuutilik, String 안내참조) {
        int 객체참조 = 새기억(9, 2); if (tammarniq) return;
        힙[객체참조 + 2] = piqaut_atuutilik; 힙[객체참조 + 3] = tuttarvik_immikkuuqtuq(안내참조); 힙참조[객체참조 + 3] = 1;
        던진객체 = 객체참조; tammarniq = true;
    }
    static boolean 맞는객체(int 객체참조, int atiq) {
        if (객체참조 == 0) return true;
        if (!객체유효(객체참조)) return false;
        int 분류코드 = 힙[객체참조];
        if (말(atiq, "java/lang/Object")) return true;
        if (분류코드 >= 32) return 종포함(분류코드 - 32, atiq);
        if (분류코드 == 9) { int turaagaq_turaarut = 예외상수(atiq); return turaagaq_turaarut != 0 && 예외포함(힙[객체참조 + 2], turaagaq_turaarut); }
        if (분류코드 == 1) return 말(atiq, "java/lang/String") || 말(atiq, "java/lang/CharSequence");
        if (분류코드 == 4) return 말(atiq, "java/lang/StringBuilder") || 말(atiq, "java/lang/CharSequence");
        if (분류코드 == 10) return 말(atiq, "java/util/ArrayList") || 말(atiq, "java/util/List");
        if (분류코드 == 11) return 말(atiq, "java/util/HashMap") || 말(atiq, "java/util/Map");
        if (분류코드 == 12) return 말(atiq, "java/lang/Integer") || 말(atiq, "java/lang/Number");
        if (분류코드 >= 24 && 분류코드 <= 28 && 힙[객체참조 + 13] != 0) return 한국어화면종(atiq) == 분류코드 || 말(atiq, "한국어/자체/화면구성요소");
        if (분류코드 >= 24 && 분류코드 <= 28) return (한국어화면종(atiq) == 0 && 화면종(atiq) == 분류코드) || 말(atiq, "java/awt/Component") || 말(atiq, "java/awt/Container") || 말(atiq, "javax/swing/JComponent");
        if (분류코드 == 29) return 말(atiq, 힙[객체참조 + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (분류코드 == 30) return 말(atiq, "java/awt/FlowLayout") || 말(atiq, "java/awt/LayoutManager");
        if (분류코드 == 17) return 말(atiq, "java/net/Socket");
        if (분류코드 == 18) return 말(atiq, "java/net/ServerSocket");
        if (분류코드 == 19) return 말(atiq, 힙[객체참조 + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (분류코드 == 14) return 말(atiq, "java/net/InetAddress");
        if (분류코드 == 15) return 말(atiq, "java/net/DatagramSocket");
        if (분류코드 == 16) return 말(atiq, "java/net/DatagramPacket");
        if (분류코드 == 13) return 말(atiq, 힙[객체참조 + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (분류코드 == 2) return 말(atiq, "[I"); if (분류코드 == 20) return 말(atiq, "[B"); if (분류코드 == 21) return 말(atiq, "[Z");
        if (분류코드 == 22) return 말(atiq, "[C"); if (분류코드 == 23) return 말(atiq, "[S");
        if (분류코드 != 3) return false;
        if (말(atiq, "[Ljava/lang/Object;")) return true;
        int Ilanga = array_ilanga[객체참조];
        if (Ilanga == -1) return 말(atiq, "[Ljava/lang/String;") || 말(atiq, "[Ljava/lang/CharSequence;");
        if (Ilanga == 0) return false;
        if (배열종비교(Ilanga, atiq)) return true;
        if ((말(Ilanga, "java/lang/String") || 말(Ilanga, "java/lang/StringBuilder")) && 말(atiq, "[Ljava/lang/CharSequence;")) return true;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 종수; piliqqittaajuq_nalunaiqsimavik++) if (같은말(종이름[piliqqittaajuq_nalunaiqsimavik], Ilanga)) {
            for (int immikkuuqtumut_nalunaikkut = piliqqittaajuq_nalunaiqsimavik, 중첩깊이 = 0; immikkuuqtumut_nalunaikkut >= 0 && 중첩깊이 < 16; 중첩깊이++, immikkuuqtumut_nalunaikkut = 부모종(immikkuuqtumut_nalunaikkut)) {
                if (배열종비교(종부모[immikkuuqtumut_nalunaikkut], atiq)) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[immikkuuqtumut_nalunaikkut]; 안쪽자리++) if (배열종비교(naliannuungavik_saqqijaagaq[immikkuuqtumut_nalunaikkut * 16 + 안쪽자리], atiq)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int atiq_surragunnangittuq, int 형식참조) {
        int 검사자리 = 상가[형식참조], 항목수 = 상나[형식참조];
        if (atiq_surragunnangittuq == 0 || 항목수 < 4 || ini[검사자리] != '[' || ini[검사자리 + 1] != 'L' || ini[검사자리 + 항목수 - 1] != ';' || 상나[atiq_surragunnangittuq] != 항목수 - 3) return false;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 항목수 - 3; piliqqittaajuq_nalunaiqsimavik++) if (ini[상가[atiq_surragunnangittuq] + piliqqittaajuq_nalunaiqsimavik] != ini[검사자리 + 2 + piliqqittaajuq_nalunaiqsimavik]) return false;
        return true;
    }
    static void 예외처리() {
        if (던진객체 == 0) return;
        tammarniq = false;
        while (avalu_nalunaiqsimavik >= 현재가닥 * 32) {
            int ini_nalunaiqsimavik = 틀함수[avalu_nalunaiqsimavik], 읽는자리 = avalu_maligialiit[avalu_nalunaiqsimavik];
            for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 잡기수; piliqqittaajuq_nalunaiqsimavik++) if (잡기함수[piliqqittaajuq_nalunaiqsimavik] == ini_nalunaiqsimavik && 읽는자리 >= 잡기시작[piliqqittaajuq_nalunaiqsimavik] && 읽는자리 < 잡기끝[piliqqittaajuq_nalunaiqsimavik]
                && (잡기종[piliqqittaajuq_nalunaiqsimavik] == 0 || 맞는객체(던진객체, 잡기종[piliqqittaajuq_nalunaiqsimavik]))) {
                틀위치[avalu_nalunaiqsimavik] = 잡기위치[piliqqittaajuq_nalunaiqsimavik]; 틀스택[avalu_nalunaiqsimavik] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (aturunnaqsili_avalu[avalu_nalunaiqsimavik] != 0) 종상태[aturunnaqsili_avalu[avalu_nalunaiqsimavik] - 1] = 3;
            if (틀잠금[avalu_nalunaiqsimavik] != 0) { 잠금풀기(틀잠금[avalu_nalunaiqsimavik]); 틀잠금[avalu_nalunaiqsimavik] = 0; }
            avalu_nalunaiqsimavik--;
        }
        atuqtuq.titiraq("Uncaught ");
        if (힙[던진객체] == 9) { atuqtuq.titiraq(예외이름(힙[던진객체 + 2])); atuqtuq.titiraq(": "); titiraq_titiqqaq(힙[던진객체 + 3]); }
        else atuqtuq.titiraq("user exception");
        atuqtuq.titiraq_immikkuuqtuq_atuutilik(10); 던진객체 = 0; tammarniq = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void 스택명령(int 명령코드) {
        int 첫값 = 빼기(0), 첫형식 = 반환형;
        if (명령코드 == 87) return;
        if (명령코드 == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int byte_titiqqat = 빼기(0), 둘째형식 = 반환형;
        if (명령코드 == 88) return;
        if (명령코드 == 90) { 넣기(첫값, 첫형식); 넣기(byte_titiqqat, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 92) { 넣기(byte_titiqqat, 둘째형식); 넣기(첫값, 첫형식); 넣기(byte_titiqqat, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 95) { 넣기(첫값, 첫형식); 넣기(byte_titiqqat, 둘째형식); return; }
        int immikkuuqtumut_nalunaikkut = 빼기(0), 셋째형식 = 반환형;
        if (명령코드 == 91) { 넣기(첫값, 첫형식); 넣기(immikkuuqtumut_nalunaikkut, 셋째형식); 넣기(byte_titiqqat, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 93) { 넣기(byte_titiqqat, 둘째형식); 넣기(첫값, 첫형식); 넣기(immikkuuqtumut_nalunaikkut, 셋째형식); 넣기(byte_titiqqat, 둘째형식); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = 반환형;
        넣기(byte_titiqqat, 둘째형식); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(immikkuuqtumut_nalunaikkut, 셋째형식); 넣기(byte_titiqqat, 둘째형식); 넣기(첫값, 첫형식);
    }
    static void 새객체(int atiq_surragunnangittuq, int 시작점) {
        int 분류코드 = 0, 유효길이 = 0, 예외참조 = 예외상수(atiq_surragunnangittuq);
        if (말(atiq_surragunnangittuq, "java/lang/StringBuilder")) { 분류코드 = 4; 유효길이 = 1; }
        if (말(atiq_surragunnangittuq, "java/io/FileInputStream")) { 분류코드 = 5; 유효길이 = 2; }
        if (말(atiq_surragunnangittuq, "java/io/FileOutputStream")) { 분류코드 = 6; 유효길이 = 2; }
        if (예외참조 != 0) { 분류코드 = 9; 유효길이 = 2; }
        if (말(atiq_surragunnangittuq, "java/util/ArrayList")) { 분류코드 = 10; 유효길이 = 2; }
        if (말(atiq_surragunnangittuq, "java/util/HashMap")) { 분류코드 = 11; 유효길이 = 2; }
        if (말(atiq_surragunnangittuq, "java/lang/Integer")) { 분류코드 = 12; 유효길이 = 1; }
        if (말(atiq_surragunnangittuq, "java/net/Socket")) { 분류코드 = 17; 유효길이 = 5; }
        if (말(atiq_surragunnangittuq, "java/net/ServerSocket")) { 분류코드 = 18; 유효길이 = 5; }
        if (말(atiq_surragunnangittuq, "java/net/DatagramSocket")) { 분류코드 = 15; 유효길이 = 3; }
        if (말(atiq_surragunnangittuq, "java/net/DatagramPacket")) { 분류코드 = 16; 유효길이 = 4; }
        if (말(atiq_surragunnangittuq, "java/lang/Thread") || 말(atiq_surragunnangittuq, "한국어/자체/작업가닥")) { 분류코드 = 13; 유효길이 = 2; }
        if (말(atiq_surragunnangittuq, "java/lang/Object")) { 분류코드 = 8; }
        if (분류코드 == 0 && 화면종(atiq_surragunnangittuq) != 0) { 분류코드 = 화면종(atiq_surragunnangittuq); 유효길이 = 12; }
        if (분류코드 == 0) {
            int immikkuuqtumut_nalunaikkut = 종찾기(atiq_surragunnangittuq); if (immikkuuqtumut_nalunaikkut < 0 || tammarniq || !aturunnaqsili(immikkuuqtumut_nalunaikkut, 시작점)) return;
            분류코드 = 32 + immikkuuqtumut_nalunaikkut; 유효길이 = 종칸수[immikkuuqtumut_nalunaikkut];
        }
        int 객체참조 = 할당(분류코드, 유효길이); if (tammarniq) return;
        if (분류코드 == 13 && 말(atiq_surragunnangittuq, "한국어/자체/작업가닥")) 힙[객체참조 + 3] = 1;
        if (분류코드 >= 24 && 분류코드 <= 28 && 한국어화면종(atiq_surragunnangittuq) != 0) 힙[객체참조 + 13] = 1;
        if (분류코드 == 5 || 분류코드 == 6 || 분류코드 == 15 || 분류코드 == 17 || 분류코드 == 18) 힙[객체참조 + 2] = -1;
        if (분류코드 == 9) 힙[객체참조 + 2] = 예외참조;
        넣기(객체참조, 2);
    }
    static boolean 값같음(int 첫값, int byte_titiqqat) {
        if (첫값 == byte_titiqqat) return true;
        if (첫값 == 0 || byte_titiqqat == 0 || 첫값 < 0 || byte_titiqqat < 0 || 첫값 >= 힙끝 || byte_titiqqat >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[byte_titiqqat] == 1) return 글같음(첫값, byte_titiqqat, false);
        return 힙[첫값] == 12 && 힙[byte_titiqqat] == 12 && 힙[첫값 + 2] == 힙[byte_titiqqat + 2];
    }
    static int 글조각(int 객체참조, int 시작자리, int 끝자리) {
        if (!kisu_atuutilik(객체참조, 1)) return 0;
        if (시작자리 < 0 || 끝자리 < 시작자리 || 끝자리 > 힙[객체참조 + 1]) { itigaqtuq_atuutilik("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = 할당(1, 끝자리 - 시작자리); if (tammarniq) return 0;
        for (int piliqqittaajuq_nalunaiqsimavik = 시작자리; piliqqittaajuq_nalunaiqsimavik < 끝자리; piliqqittaajuq_nalunaiqsimavik++) 힙[반환값 + 2 + piliqqittaajuq_nalunaiqsimavik - 시작자리] = 힙[객체참조 + 2 + piliqqittaajuq_nalunaiqsimavik];
        return 반환값;
    }
    static int ilauvigili_titiqqaq(int 첫값, int byte_titiqqat) {
        if (!kisu_atuutilik(첫값, 1) || !kisu_atuutilik(byte_titiqqat, 1)) return 0;
        int 항목수 = 힙[첫값 + 1], 함수번호 = 힙[byte_titiqqat + 1], 반환값 = 할당(1, 항목수 + 함수번호); if (tammarniq) return 0;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 항목수; piliqqittaajuq_nalunaiqsimavik++) 힙[반환값 + 2 + piliqqittaajuq_nalunaiqsimavik] = 힙[첫값 + 2 + piliqqittaajuq_nalunaiqsimavik];
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 함수번호; piliqqittaajuq_nalunaiqsimavik++) 힙[반환값 + 2 + 항목수 + piliqqittaajuq_nalunaiqsimavik] = 힙[byte_titiqqat + 2 + piliqqittaajuq_nalunaiqsimavik];
        return 반환값;
    }
    static boolean 기본호출(int 소유종, int atiq_surragunnangittuq, int 서술상수, int 명령코드) {
        if (말(소유종, "한국어/자체/실행인수") && 명령코드 == 184) {
            if (말(atiq_surragunnangittuq, "개수") && 말(서술상수, "()I")) { 넣기(atuqtuq.인수개수() - 1, 1); return true; }
            if (말(atiq_surragunnangittuq, "titiqqaq") && 말(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= atuqtuq.인수개수() - 1) 예외던짐(29, "실행 인수 범위를 벗어났습니다");
                else 넣기(tuttarvik_immikkuuqtuq(atuqtuq.인수(순번 + 1)), 2);
                return true;
            }
            itigaqtuq_atuutilik("지원하지 않는 한국어 실행 인수 호출"); return true;
        }
        if (말(소유종, "한국어/자체/작업가닥")) { Pivallianiq_aqqusiqtarvik(atiq_surragunnangittuq, 서술상수, 명령코드, true); return true; }
        if (한국어화면소유(소유종)) { 한국어화면호출(소유종, atiq_surragunnangittuq, 서술상수, 명령코드); return true; }
        if (화면소유(소유종)) { 화면호출(소유종, atiq_surragunnangittuq, 서술상수, 명령코드); return true; }
        if (말(소유종, "java/net/Socket") || 말(소유종, "java/net/ServerSocket") || 말(소유종, "java/io/InputStream") || 말(소유종, "java/io/OutputStream")) { 흐름호출(소유종, atiq_surragunnangittuq, 서술상수, 명령코드); return true; }
        if (말(소유종, "한국어/자체/kernel_atuutilik") && 명령코드 == 184) {
            if (말(atiq_surragunnangittuq, "화면너비") && 말(서술상수, "()I")) { 넣기(atuqtuq.화면너비(), 1); return true; }
            if (말(atiq_surragunnangittuq, "화면높이") && 말(서술상수, "()I")) { 넣기(atuqtuq.화면높이(), 1); return true; }
            if (말(atiq_surragunnangittuq, "밀리초") && 말(서술상수, "()I")) { 넣기(atuqtuq.밀리초(), 1); return true; }
            if (말(atiq_surragunnangittuq, "그림대기") && 말(서술상수, "()I")) { 넣기(atuqtuq.그림대기(), 1); return true; }
            if (말(atiq_surragunnangittuq, "사각형") && 말(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), 가로좌표 = 빼기(1); 넣기(atuqtuq.사각형(가로좌표, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (말(소유종, "java/net/InetAddress") || 말(소유종, "java/net/DatagramPacket") || 말(소유종, "java/net/DatagramSocket")) { 통신호출(소유종, atiq_surragunnangittuq, 서술상수, 명령코드); return true; }
        if (말(소유종, "java/lang/Thread")) { 가닥호출(atiq_surragunnangittuq, 서술상수, 명령코드); return true; }
        if (말(소유종, "java/lang/Object")) {
            if (말(atiq_surragunnangittuq, "<init>") && 말(서술상수, "()V") && 명령코드 == 183) { 객체유효(빼기(2)); return true; }
            if (말(atiq_surragunnangittuq, "equals") && 말(서술상수, "(Ljava/lang/Object;)Z")) { int byte_titiqqat = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == byte_titiqqat ? 1 : 0, 1); return true; }
        }
        if (예외상수(소유종) != 0) {
            if (말(atiq_surragunnangittuq, "<init>") && 명령코드 == 183 && (말(서술상수, "()V") || 말(서술상수, "(Ljava/lang/String;)V"))) {
                int inattijjut = 말(서술상수, "()V") ? 0 : 빼기(2), 객체참조 = 빼기(2);
                if (kisu_atuutilik(객체참조, 9)) { 힙[객체참조 + 3] = inattijjut; 힙참조[객체참조 + 3] = 1; } return true;
            }
            if ((말(atiq_surragunnangittuq, "getMessage") || 말(atiq_surragunnangittuq, "설명")) && 말(서술상수, "()Ljava/lang/String;")) { int 객체참조 = 빼기(2); if (kisu_atuutilik(객체참조, 9)) 넣기(힙[객체참조 + 3], 2); return true; }
        }
        if (말(소유종, "java/lang/String")) {
            if (명령코드 == 182 && 말(atiq_surragunnangittuq, "getBytes") && (말(서술상수, "()[B") || 말(서술상수, "(Ljava/lang/String;)[B"))) {
                int tukiniktiri_atiq = 말(서술상수, "()[B") ? 0 : 빼기(2), 객체참조 = 빼기(2);
                if (!kisu_atuutilik(객체참조, 1)) return true;
                if (tukiniktiri_atiq != 0 && !글같음(tukiniktiri_atiq, tuttarvik_immikkuuqtuq("UTF-8"), false) && !글같음(tukiniktiri_atiq, tuttarvik_immikkuuqtuq("UTF8"), false) && !글같음(tukiniktiri_atiq, tuttarvik_immikkuuqtuq("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int 항목수 = 힙[객체참조 + 1], 반환값 = 할당(20, 항목수 * 3), 사용수 = 0; if (tammarniq) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) {
                    int immikkuuqtumut_nalunaikkut = 힙[객체참조 + 2 + 안쪽자리];
                    if (immikkuuqtumut_nalunaikkut >= 0xd800 && immikkuuqtumut_nalunaikkut <= 0xdbff && 안쪽자리 + 1 < 항목수 && 힙[객체참조 + 3 + 안쪽자리] >= 0xdc00 && 힙[객체참조 + 3 + 안쪽자리] <= 0xdfff) immikkuuqtumut_nalunaikkut = 0x10000 + ((immikkuuqtumut_nalunaikkut - 0xd800) << 10) + 힙[객체참조 + 2 + ++안쪽자리] - 0xdc00;
                    else if (immikkuuqtumut_nalunaikkut >= 0xd800 && immikkuuqtumut_nalunaikkut <= 0xdfff) immikkuuqtumut_nalunaikkut = '?';
                    if (immikkuuqtumut_nalunaikkut < 128) 힙[반환값 + 2 + 사용수++] = immikkuuqtumut_nalunaikkut;
                    else { int 바이트수 = immikkuuqtumut_nalunaikkut < 2048 ? 2 : immikkuuqtumut_nalunaikkut < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((바이트수 == 2 ? 192 : 바이트수 == 3 ? 224 : 240) | immikkuuqtumut_nalunaikkut >> (6 * (바이트수 - 1))); for (int 비교자리 = 바이트수 - 1; 비교자리 > 0; 비교자리--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | immikkuuqtumut_nalunaikkut >> (6 * (비교자리 - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (명령코드 == 184 && 말(atiq_surragunnangittuq, "valueOf") && 말(서술상수, "(I)Ljava/lang/String;")) { 넣기(수문자(빼기(1)), 2); return true; }
            if (명령코드 != 182) return false;
            if (말(atiq_surragunnangittuq, "equals") && 말(서술상수, "(Ljava/lang/Object;)Z")) { int byte_titiqqat = 빼기(2), 첫값 = 빼기(2); if (kisu_atuutilik(첫값, 1)) 넣기(글같음(첫값, byte_titiqqat, false) ? 1 : 0, 1); return true; }
            if (말(atiq_surragunnangittuq, "isEmpty") && 말(서술상수, "()Z")) { int 첫값 = 빼기(2); if (kisu_atuutilik(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (말(atiq_surragunnangittuq, "substring") && (말(서술상수, "(I)Ljava/lang/String;") || 말(서술상수, "(II)Ljava/lang/String;"))) {
                boolean 둘째값 = 말(서술상수, "(II)Ljava/lang/String;"); int 끝자리 = 둘째값 ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (kisu_atuutilik(첫값, 1)) 넣기(글조각(첫값, 시작점, 둘째값 ? 끝자리 : 힙[첫값 + 1]), 2); return true;
            }
            if (말(atiq_surragunnangittuq, "concat") && 말(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int byte_titiqqat = 빼기(2), 첫값 = 빼기(2); 넣기(ilauvigili_titiqqaq(첫값, byte_titiqqat), 2); return true; }
            if (말(atiq_surragunnangittuq, "hashCode") && 말(서술상수, "()I")) { int 첫값 = 빼기(2), 해시값 = 0; if (kisu_atuutilik(첫값, 1)) { for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 힙[첫값 + 1]; piliqqittaajuq_nalunaiqsimavik++) 해시값 = 해시값 * 31 + 힙[첫값 + 2 + piliqqittaajuq_nalunaiqsimavik]; 넣기(해시값, 1); } return true; }
            if (말(atiq_surragunnangittuq, "toString") && 말(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (kisu_atuutilik(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (말(소유종, "java/lang/Integer")) {
            if (명령코드 == 184 && 말(atiq_surragunnangittuq, "valueOf") && 말(서술상수, "(I)Ljava/lang/Integer;")) { int titiqqat_atuutilik = 빼기(1), 객체참조 = titiqqat_atuutilik >= -128 && titiqqat_atuutilik <= 127 ? tuqqurli_naasaut[titiqqat_atuutilik + 128] : 0; if (객체참조 == 0) { 객체참조 = 할당(12, 1); if (!tammarniq) { 힙[객체참조 + 2] = titiqqat_atuutilik; if (titiqqat_atuutilik >= -128 && titiqqat_atuutilik <= 127) tuqqurli_naasaut[titiqqat_atuutilik + 128] = 객체참조; } } 넣기(객체참조, 2); return true; }
            if (명령코드 == 183 && 말(atiq_surragunnangittuq, "<init>") && 말(서술상수, "(I)V")) { int titiqqat_atuutilik = 빼기(1), 객체참조 = 빼기(2); if (kisu_atuutilik(객체참조, 12)) 힙[객체참조 + 2] = titiqqat_atuutilik; return true; }
            if (명령코드 == 182 && 말(atiq_surragunnangittuq, "intValue") && 말(서술상수, "()I")) { int 객체참조 = 빼기(2); if (kisu_atuutilik(객체참조, 12)) 넣기(힙[객체참조 + 2], 1); return true; }
            if (명령코드 == 184 && 말(atiq_surragunnangittuq, "toString") && 말(서술상수, "(I)Ljava/lang/String;")) { 넣기(수문자(빼기(1)), 2); return true; }
        }
        if (말(소유종, "java/lang/Math") && 명령코드 == 184) {
            if (말(atiq_surragunnangittuq, "abs") && 말(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((말(atiq_surragunnangittuq, "min") || 말(atiq_surragunnangittuq, "max")) && 말(서술상수, "(II)I")) { int byte_titiqqat = 빼기(1), 첫값 = 빼기(1); 넣기(말(atiq_surragunnangittuq, "min") ? (첫값 < byte_titiqqat ? 첫값 : byte_titiqqat) : (첫값 > byte_titiqqat ? 첫값 : byte_titiqqat), 1); return true; }
        }
        if (말(소유종, "java/lang/System") && 명령코드 == 184) {
            if (말(atiq_surragunnangittuq, "gc") && 말(서술상수, "()V")) { 수거(); return true; }
            if (말(atiq_surragunnangittuq, "arraycopy") && 말(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int 항목수 = 빼기(1), namunngarvik_atuutilik_nalunaiqsimavik = 빼기(1), byte_titiqqat = 빼기(2), 시작자리 = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(byte_titiqqat)) {
                    int 분류코드 = 힙[첫값];
                    if (힙[byte_titiqqat] != 분류코드 || (분류코드 != 2 && 분류코드 != 3 && (분류코드 < 20 || 분류코드 > 23))) itigaqtuq_atuutilik("arraycopy type mismatch");
                    else if (항목수 < 0 || 시작자리 < 0 || namunngarvik_atuutilik_nalunaiqsimavik < 0 || 시작자리 > 힙[첫값 + 1] - 항목수 || namunngarvik_atuutilik_nalunaiqsimavik > 힙[byte_titiqqat + 1] - 항목수) itigaqtuq_atuutilik("ArrayIndexOutOfBoundsException");
                    else if (첫값 == byte_titiqqat && namunngarvik_atuutilik_nalunaiqsimavik > 시작자리) { for (int piliqqittaajuq_nalunaiqsimavik = 항목수 - 1; piliqqittaajuq_nalunaiqsimavik >= 0; piliqqittaajuq_nalunaiqsimavik--) 힙[byte_titiqqat + 2 + namunngarvik_atuutilik_nalunaiqsimavik + piliqqittaajuq_nalunaiqsimavik] = 힙[첫값 + 2 + 시작자리 + piliqqittaajuq_nalunaiqsimavik]; }
                    else { for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 항목수 && !tammarniq; piliqqittaajuq_nalunaiqsimavik++) { int titiqqat_atuutilik = 힙[첫값 + 2 + 시작자리 + piliqqittaajuq_nalunaiqsimavik]; if (분류코드 != 3 || 배열저장가능(byte_titiqqat, titiqqat_atuutilik)) 힙[byte_titiqqat + 2 + namunngarvik_atuutilik_nalunaiqsimavik + piliqqittaajuq_nalunaiqsimavik] = titiqqat_atuutilik; } }
                }
                return true;
            }
        }
        if (말(소유종, "java/util/ArrayList") || 말(소유종, "java/util/List") || 말(소유종, "java/util/HashMap") || 말(소유종, "java/util/Map")) {
            모음호출(소유종, atiq_surragunnangittuq, 서술상수, 명령코드); return true;
        }
        return false;
    }
    static void 모음늘리기(int 객체참조, int 필요수) {
        int 이전값 = 힙[객체참조 + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int 다음자리 = 용량값 < 8 ? 8 : 용량값 * 2; if (다음자리 < 필요수) 다음자리 = 필요수;
        int titiqqat_array = 할당(3, 다음자리); if (tammarniq) return;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 용량값; piliqqittaajuq_nalunaiqsimavik++) 힙[titiqqat_array + 2 + piliqqittaajuq_nalunaiqsimavik] = 힙[이전값 + 2 + piliqqittaajuq_nalunaiqsimavik];
        힙[객체참조 + 2] = titiqqat_array; 힙참조[객체참조 + 2] = 1;
    }
    static void 모음호출(int 소유종, int atiq_surragunnangittuq, int 서술상수, int 명령코드) {
        boolean 대응참조 = 말(소유종, "java/util/HashMap") || 말(소유종, "java/util/Map"); int 분류코드 = 대응참조 ? 11 : 10;
        if (말(atiq_surragunnangittuq, "<init>") && 명령코드 == 183 && 말(서술상수, "()V")) { int 객체참조 = 빼기(2); if (kisu_atuutilik(객체참조, 분류코드)) 모음늘리기(객체참조, 8); return; }
        if (명령코드 != 182 && 명령코드 != 185) { itigaqtuq_atuutilik("invalid collection invocation"); return; }
        if (말(atiq_surragunnangittuq, "size") && 말(서술상수, "()I") || 말(atiq_surragunnangittuq, "isEmpty") && 말(서술상수, "()Z")) {
            int 객체참조 = 빼기(2); if (kisu_atuutilik(객체참조, 분류코드)) 넣기(말(atiq_surragunnangittuq, "size") ? 힙[객체참조 + 3] : 힙[객체참조 + 3] == 0 ? 1 : 0, 1); return;
        }
        if (말(atiq_surragunnangittuq, "clear") && 말(서술상수, "()V")) { int 객체참조 = 빼기(2); if (kisu_atuutilik(객체참조, 분류코드)) { int titiqqat_array = 힙[객체참조 + 2]; for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 힙[titiqqat_array + 1]; piliqqittaajuq_nalunaiqsimavik++) 힙[titiqqat_array + 2 + piliqqittaajuq_nalunaiqsimavik] = 0; 힙[객체참조 + 3] = 0; } return; }
        if (!대응참조 && 말(atiq_surragunnangittuq, "add") && 말(서술상수, "(Ljava/lang/Object;)Z")) {
            int titiqqat_atuutilik = 빼기(2), 객체참조 = 빼기(2); if (!kisu_atuutilik(객체참조, 10)) return;
            int 항목수 = 힙[객체참조 + 3]; 모음늘리기(객체참조, 항목수 + 1); if (!tammarniq) { 힙[힙[객체참조 + 2] + 2 + 항목수] = titiqqat_atuutilik; 힙[객체참조 + 3] = 항목수 + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (말(atiq_surragunnangittuq, "get") || 말(atiq_surragunnangittuq, "remove")) && 말(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && 말(atiq_surragunnangittuq, "set") && 말(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = 말(atiq_surragunnangittuq, "set"); int titiqqat_atuutilik = 지정여부 ? 빼기(2) : 0, 항목자리 = 빼기(1), 객체참조 = 빼기(2);
            if (!kisu_atuutilik(객체참조, 10)) return;
            int 항목수 = 힙[객체참조 + 3], titiqqat_array = 힙[객체참조 + 2];
            if (항목자리 < 0 || 항목자리 >= 항목수) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[titiqqat_array + 2 + 항목자리];
            if (지정여부) 힙[titiqqat_array + 2 + 항목자리] = titiqqat_atuutilik;
            if (말(atiq_surragunnangittuq, "remove")) { for (int piliqqittaajuq_nalunaiqsimavik = 항목자리 + 1; piliqqittaajuq_nalunaiqsimavik < 항목수; piliqqittaajuq_nalunaiqsimavik++) 힙[titiqqat_array + 1 + piliqqittaajuq_nalunaiqsimavik] = 힙[titiqqat_array + 2 + piliqqittaajuq_nalunaiqsimavik]; 힙[titiqqat_array + 1 + 항목수] = 0; 힙[객체참조 + 3] = 항목수 - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (말(atiq_surragunnangittuq, "get") || 말(atiq_surragunnangittuq, "remove")) && 말(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && 말(atiq_surragunnangittuq, "put") && 말(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && 말(atiq_surragunnangittuq, "containsKey") && 말(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = 말(atiq_surragunnangittuq, "put"), sanirvalli = 말(atiq_surragunnangittuq, "remove");
            int titiqqat_atuutilik = 넣기여부 ? 빼기(2) : 0, 키참조 = 빼기(2), 객체참조 = 빼기(2); if (!kisu_atuutilik(객체참조, 11)) return;
            int 항목수 = 힙[객체참조 + 3], titiqqat_array = 힙[객체참조 + 2], 찾은여부 = -1;
            for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 항목수; piliqqittaajuq_nalunaiqsimavik++) if (값같음(키참조, 힙[titiqqat_array + 2 + 2 * piliqqittaajuq_nalunaiqsimavik])) { 찾은여부 = piliqqittaajuq_nalunaiqsimavik; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[titiqqat_array + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(객체참조, (항목수 + 1) * 2); titiqqat_array = 힙[객체참조 + 2]; 찾은여부 = 항목수; if (!tammarniq) 힙[객체참조 + 3] = 항목수 + 1; }
                if (!tammarniq) { 힙[titiqqat_array + 2 + 2 * 찾은여부] = 키참조; 힙[titiqqat_array + 3 + 2 * 찾은여부] = titiqqat_atuutilik; }
            }
            if (sanirvalli && 찾은여부 >= 0) { for (int piliqqittaajuq_nalunaiqsimavik = 찾은여부 + 1; piliqqittaajuq_nalunaiqsimavik < 항목수; piliqqittaajuq_nalunaiqsimavik++) { 힙[titiqqat_array + 2 * piliqqittaajuq_nalunaiqsimavik] = 힙[titiqqat_array + 2 + 2 * piliqqittaajuq_nalunaiqsimavik]; 힙[titiqqat_array + 1 + 2 * piliqqittaajuq_nalunaiqsimavik] = 힙[titiqqat_array + 3 + 2 * piliqqittaajuq_nalunaiqsimavik]; } 힙[titiqqat_array + 2 * 항목수] = 0; 힙[titiqqat_array + 1 + 2 * 항목수] = 0; 힙[객체참조 + 3] = 항목수 - 1; }
            if (말(atiq_surragunnangittuq, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        itigaqtuq_atuutilik("unsupported collection method");
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
    static boolean kipulli_aqqusiqtarvik() {
        aqqusiqtarvik_avalu[현재가닥] = avalu_nalunaiqsimavik;
        if (avalu_nalunaiqsimavik < 현재가닥 * 32) aqqusiqtarvik_qanuilinganiq[현재가닥] = 3;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 가닥수; piliqqittaajuq_nalunaiqsimavik++) if (aqqusiqtarvik_qanuilinganiq[piliqqittaajuq_nalunaiqsimavik] == 2 && aqqusiqtarvik_qanuilinganiq[가닥대기[piliqqittaajuq_nalunaiqsimavik]] == 3) aqqusiqtarvik_qanuilinganiq[piliqqittaajuq_nalunaiqsimavik] = 1;
        for (int piliqqittaajuq_nalunaiqsimavik = 1; piliqqittaajuq_nalunaiqsimavik <= 가닥수; piliqqittaajuq_nalunaiqsimavik++) {
            int 다음자리 = (현재가닥 + piliqqittaajuq_nalunaiqsimavik) % 가닥수;
            if (aqqusiqtarvik_qanuilinganiq[다음자리] == 1) { 현재가닥 = 다음자리; avalu_nalunaiqsimavik = aqqusiqtarvik_avalu[다음자리]; 바꿈요청 = false; return true; }
        }
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 가닥수; piliqqittaajuq_nalunaiqsimavik++) if (aqqusiqtarvik_qanuilinganiq[piliqqittaajuq_nalunaiqsimavik] != 3) { itigaqtuq_atuutilik("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int atiq_surragunnangittuq, int 서술상수, int 명령코드) { Pivallianiq_aqqusiqtarvik(atiq_surragunnangittuq, 서술상수, 명령코드, false); }
    static void Pivallianiq_aqqusiqtarvik(int atiq_surragunnangittuq, int 서술상수, int 명령코드, boolean 한국어) {
        if (명령코드 == 184 && 말(atiq_surragunnangittuq, 한국어 ? "양보하기" : "yield") && 말(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (명령코드 == 184 && 말(atiq_surragunnangittuq, "currentThread") && 말(서술상수, "()Ljava/lang/Thread;")) { 넣기(aqqusiqtarvik_kisu[현재가닥], 2); return; }
        if (명령코드 == 183 && 말(atiq_surragunnangittuq, "<init>") && (말(서술상수, "()V") || 말(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int turaagaq_turaarut = 말(서술상수, "()V") ? 0 : 빼기(2), 객체참조 = 빼기(2);
            if (!객체유효(객체참조)) return;
            if (힙[객체참조] == 13) { 힙[객체참조 + 2] = turaagaq_turaarut; 힙참조[객체참조 + 2] = 1; }
            else if (turaagaq_turaarut != 0) itigaqtuq_atuutilik("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (명령코드 == 182 && (말(atiq_surragunnangittuq, 한국어 ? "pigiarli_sujassaq" : "start") || 말(atiq_surragunnangittuq, 한국어 ? "기다리기" : "join")) && 말(서술상수, "()V") || 명령코드 == 182 && 말(atiq_surragunnangittuq, 한국어 ? "살아있는가" : "isAlive") && 말(서술상수, "()Z")) {
            int 객체참조 = 빼기(2); if (!객체유효(객체참조)) return;
            int piqaut_atuutilik = -1; for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 가닥수; piliqqittaajuq_nalunaiqsimavik++) if (aqqusiqtarvik_kisu[piliqqittaajuq_nalunaiqsimavik] == 객체참조) piqaut_atuutilik = piliqqittaajuq_nalunaiqsimavik;
            if (말(atiq_surragunnangittuq, 한국어 ? "살아있는가" : "isAlive")) { 넣기(piqaut_atuutilik >= 0 && aqqusiqtarvik_qanuilinganiq[piqaut_atuutilik] != 3 ? 1 : 0, 1); return; }
            if (말(atiq_surragunnangittuq, 한국어 ? "기다리기" : "join")) { if (piqaut_atuutilik >= 0 && aqqusiqtarvik_qanuilinganiq[piqaut_atuutilik] != 3) { 가닥대기[현재가닥] = piqaut_atuutilik; aqqusiqtarvik_qanuilinganiq[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (piqaut_atuutilik >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (가닥수 == 4) { itigaqtuq_atuutilik("thread limit (4 including main)"); return; }
            int turaagaq_turaarut = 힙[객체참조] == 13 ? 힙[객체참조 + 2] : 객체참조;
            int ini_nalunaiqsimavik = turaagaq_turaarut > 0 && 힙[turaagaq_turaarut] >= 32 ? 이름함수(힙[turaagaq_turaarut] - 32, 한국어 ? "실행하기" : "run", "()V") : -1;
            if (turaagaq_turaarut != 0 && ini_nalunaiqsimavik < 0) { itigaqtuq_atuutilik("Runnable.run required"); return; }
            piqaut_atuutilik = 가닥수++; aqqusiqtarvik_kisu[piqaut_atuutilik] = 객체참조; aqqusiqtarvik_turaagaq[piqaut_atuutilik] = turaagaq_turaarut;
            int avalu = piqaut_atuutilik * 32; aqqusiqtarvik_avalu[piqaut_atuutilik] = ini_nalunaiqsimavik < 0 ? avalu - 1 : avalu; aqqusiqtarvik_qanuilinganiq[piqaut_atuutilik] = ini_nalunaiqsimavik < 0 ? 3 : 1;
            if (ini_nalunaiqsimavik >= 0) { 틀함수[avalu] = ini_nalunaiqsimavik; 틀위치[avalu] = 함수시작[ini_nalunaiqsimavik]; tamaani_atuutilik[avalu * 128] = turaagaq_turaarut; tamaani_qanuittuuninga[avalu * 128] = 2; }
            return;
        }
        itigaqtuq_atuutilik("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], turaarut_titiqqaq = new int[16];
    static int tamaani_turaarut() { return turaarut_kisu(0x7f000001); }
    static int turaarut_kisu(int atuutilik) { int 객체참조 = 할당(14, 1); if (!tammarniq) 힙[객체참조 + 2] = atuutilik; return 객체참조; }
    static int 주소해독(int 객체참조) {
        if (객체참조 == 0 || 글같음(객체참조, tuttarvik_immikkuuqtuq("localhost"), false)) return 0x7f000001;
        if (!kisu_atuutilik(객체참조, 1)) return 0;
        int titiqqat_atuutilik = 0, 총수 = 0, turaarut_byte = 0, 자릿수 = 0, 항목수 = 힙[객체참조 + 1];
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik <= 항목수; piliqqittaajuq_nalunaiqsimavik++) {
            int immikkuuqtumut_nalunaikkut = piliqqittaajuq_nalunaiqsimavik == 항목수 ? '.' : 힙[객체참조 + 2 + piliqqittaajuq_nalunaiqsimavik];
            if (immikkuuqtumut_nalunaikkut == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } titiqqat_atuutilik = titiqqat_atuutilik << 8 | turaarut_byte; 총수++; turaarut_byte = 자릿수 = 0; }
            else { if (immikkuuqtumut_nalunaikkut < '0' || immikkuuqtumut_nalunaikkut > '9' || ++자릿수 > 3 || (turaarut_byte = turaarut_byte * 10 + immikkuuqtumut_nalunaikkut - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return titiqqat_atuutilik;
    }
    static int turaarut_immikkuuqtuq(int titiqqat_atuutilik) {
        int 항목수 = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int turaarut_byte = titiqqat_atuutilik >>> 이동비트 & 255;
            if (turaarut_byte >= 100) turaarut_titiqqaq[항목수++] = '0' + turaarut_byte / 100;
            if (turaarut_byte >= 10) turaarut_titiqqaq[항목수++] = '0' + turaarut_byte / 10 % 10;
            turaarut_titiqqaq[항목수++] = '0' + turaarut_byte % 10; if (이동비트 != 0) turaarut_titiqqaq[항목수++] = '.';
        }
        int 객체참조 = 할당(1, 항목수); if (!tammarniq) for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 항목수; piliqqittaajuq_nalunaiqsimavik++) 힙[객체참조 + 2 + piliqqittaajuq_nalunaiqsimavik] = turaarut_titiqqaq[piliqqittaajuq_nalunaiqsimavik]; return 객체참조;
    }
    static void 통신호출(int 소유종, int atiq_surragunnangittuq, int 서술상수, int 명령코드) {
        if (말(소유종, "java/net/InetAddress")) {
            if (명령코드 == 184 && 말(atiq_surragunnangittuq, "getLoopbackAddress") && 말(서술상수, "()Ljava/net/InetAddress;")) { 넣기(tamaani_turaarut(), 2); return; }
            if (명령코드 == 184 && 말(atiq_surragunnangittuq, "getByName") && 말(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int titiqqat_atuutilik = 주소해독(빼기(2)); if (던진객체 == 0 && !tammarniq) 넣기(turaarut_kisu(titiqqat_atuutilik), 2); return;
            }
            if (명령코드 == 182 && 말(atiq_surragunnangittuq, "getHostAddress") && 말(서술상수, "()Ljava/lang/String;")) { int 객체참조 = 빼기(2); if (kisu_atuutilik(객체참조, 14)) 넣기(turaarut_immikkuuqtuq(힙[객체참조 + 2]), 2); return; }
        }
        if (말(소유종, "java/net/DatagramPacket")) {
            if (명령코드 == 183 && 말(atiq_surragunnangittuq, "<init>") && (말(서술상수, "([BI)V") || 말(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean 목적참조 = 말(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = 목적참조 ? 빼기(1) : 0, 주소참조 = 목적참조 ? 빼기(2) : 0;
                int 항목수 = 빼기(1), titiqqat_array = 빼기(2), 객체참조 = 빼기(2);
                if (!kisu_atuutilik(객체참조, 16) || !kisu_atuutilik(titiqqat_array, 20)) return;
                if (항목수 < 0 || 항목수 > 힙[titiqqat_array + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (주소참조 != 0 && !kisu_atuutilik(주소참조, 14)) return;
                힙[객체참조 + 2] = titiqqat_array; 힙참조[객체참조 + 2] = 1; 힙[객체참조 + 3] = 항목수;
                힙[객체참조 + 4] = 주소참조; 힙참조[객체참조 + 4] = 1; 힙[객체참조 + 5] = 접속번호; return;
            }
            if (명령코드 == 182 && 말(atiq_surragunnangittuq, "setLength") && 말(서술상수, "(I)V")) {
                int 항목수 = 빼기(1), 객체참조 = 빼기(2); if (!kisu_atuutilik(객체참조, 16)) return;
                if (항목수 < 0 || 항목수 > 힙[힙[객체참조 + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[객체참조 + 3] = 항목수; return;
            }
            if (명령코드 == 182 && (말(atiq_surragunnangittuq, "getData") && 말(서술상수, "()[B") || 말(atiq_surragunnangittuq, "getLength") && 말(서술상수, "()I") || 말(atiq_surragunnangittuq, "getAddress") && 말(서술상수, "()Ljava/net/InetAddress;") || 말(atiq_surragunnangittuq, "getPort") && 말(서술상수, "()I"))) {
                int 객체참조 = 빼기(2); if (!kisu_atuutilik(객체참조, 16)) return;
                int 항목자리 = 말(atiq_surragunnangittuq, "getData") ? 2 : 말(atiq_surragunnangittuq, "getLength") ? 3 : 말(atiq_surragunnangittuq, "getAddress") ? 4 : 5;
                넣기(힙[객체참조 + 항목자리], 항목자리 == 2 || 항목자리 == 4 ? 2 : 1); return;
            }
        }
        if (말(소유종, "java/net/DatagramSocket")) {
            if (명령코드 == 183 && 말(atiq_surragunnangittuq, "<init>") && (말(서술상수, "()V") || 말(서술상수, "(I)V"))) {
                int 접속번호 = 말(서술상수, "()V") ? 0 : 빼기(1), 객체참조 = 빼기(2); if (!kisu_atuutilik(객체참조, 15)) return;
                if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = atuqtuq.matuirli_Kasuqatigiitsimajut(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[객체참조 + 2] = 열린파일번호; return;
            }
            if (명령코드 == 182 && 말(atiq_surragunnangittuq, "setSoTimeout") && 말(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), 객체참조 = 빼기(2); if (!kisu_atuutilik(객체참조, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[객체참조 + 3] = 밀리초값; return;
            }
            if (명령코드 == 182 && 말(atiq_surragunnangittuq, "getLocalPort") && 말(서술상수, "()I")) { int 객체참조 = 빼기(2); if (kisu_atuutilik(객체참조, 15)) 넣기(힙[객체참조 + 2] < 0 ? -1 : atuqtuq.Kasuqatigiitsimajut_kapputigaq(힙[객체참조 + 2]), 1); return; }
            if (명령코드 == 182 && 말(atiq_surragunnangittuq, "isClosed") && 말(서술상수, "()Z")) { int 객체참조 = 빼기(2); if (kisu_atuutilik(객체참조, 15)) 넣기(힙[객체참조 + 2] < 0 ? 1 : 0, 1); return; }
            if (명령코드 == 182 && 말(atiq_surragunnangittuq, "close") && 말(서술상수, "()V")) { int 객체참조 = 빼기(2); if (kisu_atuutilik(객체참조, 15) && 힙[객체참조 + 2] >= 0) { atuqtuq.파일서술자닫기(힙[객체참조 + 2]); 힙[객체참조 + 2] = -1; } return; }
            if (명령코드 == 182 && (말(atiq_surragunnangittuq, "send") || 말(atiq_surragunnangittuq, "receive")) && 말(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int 전문참조 = 빼기(2), 객체참조 = 빼기(2); if (!kisu_atuutilik(전문참조, 16) || !kisu_atuutilik(객체참조, 15)) return;
                int titiqqat_array = 힙[전문참조 + 2], 유효길이 = 힙[전문참조 + 3], 열린파일번호 = 힙[객체참조 + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (말(atiq_surragunnangittuq, "send")) {
                    if (!kisu_atuutilik(힙[전문참조 + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 유효길이; piliqqittaajuq_nalunaiqsimavik++) 통신임시[piliqqittaajuq_nalunaiqsimavik] = 힙[titiqqat_array + 2 + piliqqittaajuq_nalunaiqsimavik];
                    if (atuqtuq.nassiutili_Kasuqatigiitsimajut(열린파일번호, 힙[힙[전문참조 + 4] + 2], 힙[전문참조 + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int 항목수 = atuqtuq.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (항목수 == -11) {
                        int 현재시각 = atuqtuq.밀리초();
                        if (힙[객체참조 + 4] == 0) 힙[객체참조 + 4] = 현재시각 + 1;
                        if (힙[객체참조 + 3] > 0 && 현재시각 - (힙[객체참조 + 4] - 1) >= 힙[객체참조 + 3]) { 힙[객체참조 + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(객체참조, 2); 넣기(전문참조, 2); 틀위치[avalu_nalunaiqsimavik] = avalu_maligialiit[avalu_nalunaiqsimavik]; 바꿈요청 = true; return;
                    }
                    힙[객체참조 + 4] = 0;
                    if (항목수 < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 항목수; piliqqittaajuq_nalunaiqsimavik++) 힙[titiqqat_array + 2 + piliqqittaajuq_nalunaiqsimavik] = (byte)통신임시[piliqqittaajuq_nalunaiqsimavik];
                    힙[전문참조 + 3] = 항목수; 힙[전문참조 + 4] = turaarut_kisu(통신임시[513]); 힙참조[전문참조 + 4] = 1; 힙[전문참조 + 5] = 통신임시[512];
                }
                return;
            }
        }
        itigaqtuq_atuutilik("unsupported java.net method");
    }
    static boolean 흐름대기(int 객체참조) {
        int 현재시각 = atuqtuq.밀리초();
        if (힙[객체참조 + 5] == 0) 힙[객체참조 + 5] = 현재시각 + 1;
        if (힙[객체참조 + 3] > 0 && 현재시각 - (힙[객체참조 + 5] - 1) >= 힙[객체참조 + 3]) { 힙[객체참조 + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        틀위치[avalu_nalunaiqsimavik] = avalu_maligialiit[avalu_nalunaiqsimavik]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int 소유종, int atiq_surragunnangittuq, int 서술상수, int 명령코드) {
        boolean 수신쪽 = 말(소유종, "java/net/ServerSocket"), ingirrania_aulataup = 말(소유종, "java/io/InputStream") || 말(소유종, "java/io/OutputStream");
        if (!ingirrania_aulataup && 명령코드 == 183 && 말(atiq_surragunnangittuq, "<init>")) {
            boolean 빈여부 = 말(서술상수, "()V"), 이름지정여부 = 말(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = 말(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && 말(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { itigaqtuq_atuutilik("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), 주소참조 = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, 객체참조 = 빼기(2);
            if (!kisu_atuutilik(객체참조, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !kisu_atuutilik(주소참조, 14)) return;
            int Kasuqatigiitsimajut_turaarut = 이름지정여부 ? 주소해독(주소참조) : 주소지정여부 ? 힙[주소참조 + 2] : 0x7f000001;
            if (tammarniq || 던진객체 != 0) return;
            int 열린파일번호 = atuqtuq.ingirrania_aulataup_aulattivik(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? atuqtuq.ingirrania_aulataup_aulattivik(1, 열린파일번호, 접속번호) : atuqtuq.kasurli_ingirrania_aulataup(열린파일번호, Kasuqatigiitsimajut_turaarut, 접속번호);
            if (처리값 < 0) { atuqtuq.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[객체참조 + 2] = 열린파일번호; 힙[객체참조 + 4] = 접속번호; 힙[객체참조 + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!ingirrania_aulataup && 말(atiq_surragunnangittuq, "setSoTimeout") && 말(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), 객체참조 = 빼기(2); if (!kisu_atuutilik(객체참조, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[객체참조 + 3] = 밀리초값; return; }
        if (!ingirrania_aulataup && 말(atiq_surragunnangittuq, "close") && 말(서술상수, "()V")) { int 객체참조 = 빼기(2); if (kisu_atuutilik(객체참조, 수신쪽 ? 18 : 17) && 힙[객체참조 + 2] >= 0) { atuqtuq.파일서술자닫기(힙[객체참조 + 2]); 힙[객체참조 + 2] = -1; } return; }
        if (!ingirrania_aulataup && (말(atiq_surragunnangittuq, "getLocalPort") || 말(atiq_surragunnangittuq, "getPort") || 말(atiq_surragunnangittuq, "isClosed") || 말(atiq_surragunnangittuq, "isConnected"))) {
            int 객체참조 = 빼기(2); if (!kisu_atuutilik(객체참조, 수신쪽 ? 18 : 17)) return;
            넣기(말(atiq_surragunnangittuq, "isClosed") ? 힙[객체참조 + 2] < 0 ? 1 : 0 : 말(atiq_surragunnangittuq, "isConnected") ? 힙[객체참조 + 6] : 말(atiq_surragunnangittuq, "getPort") ? 힙[객체참조 + 4] : 힙[객체참조 + 2] < 0 ? -1 : atuqtuq.ingirrania_aulataup_aulattivik(4, 힙[객체참조 + 2], 0), 1); return;
        }
        if (수신쪽 && 말(atiq_surragunnangittuq, "accept") && 말(서술상수, "()Ljava/net/Socket;")) {
            int 객체참조 = 빼기(2); if (!kisu_atuutilik(객체참조, 18)) return; int 열린파일번호 = atuqtuq.ingirrania_aulataup_aulattivik(3, 힙[객체참조 + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(객체참조)) 넣기(객체참조, 2); return; }
            힙[객체참조 + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = 할당(17, 5); if (tammarniq) { atuqtuq.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = atuqtuq.ingirrania_aulataup_aulattivik(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !ingirrania_aulataup && ((말(atiq_surragunnangittuq, "getInputStream") && 말(서술상수, "()Ljava/io/InputStream;")) || (말(atiq_surragunnangittuq, "getOutputStream") && 말(서술상수, "()Ljava/io/OutputStream;")))) {
            int 객체참조 = 빼기(2); if (!kisu_atuutilik(객체참조, 17)) return; if (힙[객체참조 + 2] < 0 || 힙[객체참조 + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = 할당(19, 4); if (tammarniq) return; 힙[반환값 + 2] = 객체참조; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = 말(atiq_surragunnangittuq, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (ingirrania_aulataup) {
            boolean 읽기여부 = 말(atiq_surragunnangittuq, "read"), 쓰기여부 = 말(atiq_surragunnangittuq, "write"), sapummili = 말(서술상수, "([B)I") || 말(서술상수, "([B)V"), 부분배열여부 = 말(서술상수, "([BII)I") || 말(서술상수, "([BII)V");
            int 항목수 = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, titiqqat_array = sapummili || 부분배열여부 ? 빼기(2) : 0;
            int titiqqat_atuutilik = 쓰기여부 && 말(서술상수, "(I)V") ? 빼기(1) : 0, 객체참조 = 빼기(2);
            if (!kisu_atuutilik(객체참조, 19)) return; int 부모참조 = 힙[객체참조 + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (말(atiq_surragunnangittuq, "close") && 말(서술상수, "()V")) { atuqtuq.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (말(atiq_surragunnangittuq, "flush") && 말(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[객체참조 + 3] == 0)) { itigaqtuq_atuutilik("unsupported stream operation"); return; }
            if (sapummili || 부분배열여부) { if (!kisu_atuutilik(titiqqat_array, 20)) return; if (sapummili) 항목수 = 힙[titiqqat_array + 1]; if (시작변위 < 0 || 항목수 < 0 || 시작변위 > 힙[titiqqat_array + 1] - 항목수) { 예외던짐(6, "stream array bounds"); return; } }
            else 항목수 = 1;
            if (항목수 == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[객체참조 + 4] : 0, 처리값 = 0;
            while (완료수 < 항목수) {
                처리값 = 읽기여부 ? atuqtuq.파일한바이트읽기(열린파일번호) : atuqtuq.파일한바이트쓰기(열린파일번호, sapummili || 부분배열여부 ? 힙[titiqqat_array + 2 + 시작변위 + 완료수] : titiqqat_atuutilik);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (sapummili || 부분배열여부)) 힙[titiqqat_array + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(sapummili || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[객체참조 + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(객체참조, 2); if (sapummili || 부분배열여부) 넣기(titiqqat_array, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(항목수, 1); } if (쓰기여부 && !(sapummili || 부분배열여부)) 넣기(titiqqat_atuutilik, 1); } return;
            }
            힙[객체참조 + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : sapummili || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        itigaqtuq_atuutilik("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int atiq_surragunnangittuq) {
        if (말(atiq_surragunnangittuq, "한국어/자체/igalaangujaq")) return 24;
        if (말(atiq_surragunnangittuq, "한국어/자체/nalunairli")) return 26;
        if (말(atiq_surragunnangittuq, "한국어/자체/tikkuagaq")) return 27;
        if (말(atiq_surragunnangittuq, "한국어/자체/titiqqaq_kisumuungavik")) return 28;
        if (말(atiq_surragunnangittuq, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int atiq_surragunnangittuq) {
        return 한국어화면종(atiq_surragunnangittuq) != 0 || 말(atiq_surragunnangittuq, "한국어/자체/화면구성요소") || 말(atiq_surragunnangittuq, "한국어/자체/piniku_utaqqivik");
    }
    static int 화면종(int atiq_surragunnangittuq) {
        int 한국어종 = 한국어화면종(atiq_surragunnangittuq); if (한국어종 != 0) return 한국어종;
        if (말(atiq_surragunnangittuq, "javax/swing/JFrame")) return 24;
        if (말(atiq_surragunnangittuq, "javax/swing/JPanel")) return 25;
        if (말(atiq_surragunnangittuq, "javax/swing/JLabel")) return 26;
        if (말(atiq_surragunnangittuq, "javax/swing/JButton")) return 27;
        if (말(atiq_surragunnangittuq, "javax/swing/JTextField")) return 28;
        if (말(atiq_surragunnangittuq, "java/awt/event/ActionEvent")) return 29;
        if (말(atiq_surragunnangittuq, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int atiq_surragunnangittuq) {
        return 화면종(atiq_surragunnangittuq) != 0 || 말(atiq_surragunnangittuq, "java/awt/Component") || 말(atiq_surragunnangittuq, "java/awt/Container") || 말(atiq_surragunnangittuq, "javax/swing/JComponent") || 말(atiq_surragunnangittuq, "javax/swing/AbstractButton") || 말(atiq_surragunnangittuq, "javax/swing/text/JTextComponent") || 말(atiq_surragunnangittuq, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int 객체참조) { if (!객체유효(객체참조)) return false; if (힙[객체참조] < 24 || 힙[객체참조] > 28) { itigaqtuq_atuutilik("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int 객체참조, int 글참조) {
        if (글참조 != 0 && !kisu_atuutilik(글참조, 1)) return;
        int 항목수 = 글참조 == 0 ? 0 : 힙[글참조 + 1]; if (항목수 > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 항목수; piliqqittaajuq_nalunaiqsimavik++) 화면글임시[piliqqittaajuq_nalunaiqsimavik] = 힙[글참조 + 2 + piliqqittaajuq_nalunaiqsimavik];
        if (atuqtuq.화면글(힙[객체참조 + 2], 화면글임시, 항목수) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[객체참조 + 3] = 글참조; 힙참조[객체참조 + 3] = 1;
    }
    static int 화면문자읽기(int 객체참조) {
        int piqaut_atuutilik = 힙[객체참조 + 2], 항목수 = atuqtuq.화면연결(8, piqaut_atuutilik, 0, 0, 0, 0), 사용수 = 0;
        if (항목수 < 0) { itigaqtuq_atuutilik("GUI text read failed"); return 0; }
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 항목수; piliqqittaajuq_nalunaiqsimavik++) { int 부호값 = atuqtuq.화면연결(9, piqaut_atuutilik, piliqqittaajuq_nalunaiqsimavik, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = 할당(1, 사용수); if (!tammarniq) for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 사용수; piliqqittaajuq_nalunaiqsimavik++) 힙[반환값 + 2 + piliqqittaajuq_nalunaiqsimavik] = 화면글임시[piliqqittaajuq_nalunaiqsimavik]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 kernel_atuutilik 화면 기능에 연결한다. Swing kisu_atuutilik/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int 소유종, int atiq_surragunnangittuq, int 서술상수, int 명령코드) {
        if (말(소유종, "한국어/자체/piniku_utaqqivik")) {
            if (명령코드 == 184 && 말(atiq_surragunnangittuq, "나중에실행") && 말(서술상수, "(L한국어/자체/실행할일;)V")) {
                int sujassaq_sugiarut = 빼기(2); if (!객체유효(sujassaq_sugiarut)) return;
                if (나중수 == 8) { itigaqtuq_atuutilik("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = sujassaq_sugiarut; return;
            }
            if (명령코드 == 184 && 말(atiq_surragunnangittuq, "사건처리중인가") && 말(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            itigaqtuq_atuutilik("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (말(소유종, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!kisu_atuutilik(알림, 29) || 힙[알림 + 3] == 0) return;
            if (말(atiq_surragunnangittuq, "piniku_pivviujuq") && 말(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (말(atiq_surragunnangittuq, "piqujijjut_titiqqaq") && 말(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (말(atiq_surragunnangittuq, "nalunaiqsimavik") && 말(서술상수, "()I")) 넣기(1001, 1);
            else itigaqtuq_atuutilik("지원하지 않는 한국어 sugiarut 알림 호출"); return;
        }
        if (명령코드 == 183 && 말(atiq_surragunnangittuq, "<init>")) {
            int 종류 = 한국어화면종(소유종), 받이 = 0, 가로 = 0, 세로 = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && 말(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (atuqtuq.화면너비() - 폭) / 2; 세로 = (atuqtuq.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && 말(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && 말(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); 세로 = 빼기(1); 가로 = 빼기(1);
            } else { itigaqtuq_atuutilik("지원하지 않는 한국어 화면 생성자"); return; }
            int titiqqaq = 빼기(2), ilanga_atuutilik = 빼기(2); if (!화면객체(ilanga_atuutilik)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || 세로 < 0 || 폭 > atuqtuq.화면너비() - 가로 || 높이 > atuqtuq.화면높이() - 세로) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int nalunaiqsimavik = atuqtuq.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (nalunaiqsimavik < 1 || nalunaiqsimavik > 32) { itigaqtuq_atuutilik("화면 ilanga_atuutilik 자리가 가득 찼습니다"); return; }
            힙[ilanga_atuutilik + 2] = nalunaiqsimavik; 화면참조[nalunaiqsimavik - 1] = ilanga_atuutilik;
            힙[ilanga_atuutilik + 5] = 가로; 힙[ilanga_atuutilik + 6] = 세로; 힙[ilanga_atuutilik + 7] = 폭; 힙[ilanga_atuutilik + 8] = 높이; 힙[ilanga_atuutilik + 10] = 2;
            힙[ilanga_atuutilik + 4] = 받이; 힙참조[ilanga_atuutilik + 4] = 1; 힙[ilanga_atuutilik + 12] = 1;
            atuqtuq.화면연결(1, nalunaiqsimavik, 가로, 세로, 폭, 높이);
            if (종류 == 24) atuqtuq.화면연결(7, nalunaiqsimavik, 2, 0, 0, 0);
            화면문자설정(ilanga_atuutilik, titiqqaq); return;
        }
        if (명령코드 != 182) { itigaqtuq_atuutilik("잘못된 한국어 화면 호출 piqujijjut"); return; }
        if (말(atiq_surragunnangittuq, "titiraq_titiqqaq") && 말(서술상수, "(Ljava/lang/String;)V")) {
            int titiqqaq = 빼기(2), ilanga_atuutilik = 빼기(2); if (화면객체(ilanga_atuutilik)) 화면문자설정(ilanga_atuutilik, titiqqaq); return;
        }
        if (말(atiq_surragunnangittuq, "글읽기") && 말(서술상수, "()Ljava/lang/String;")) {
            int ilanga_atuutilik = 빼기(2); if (화면객체(ilanga_atuutilik)) 넣기(화면문자읽기(ilanga_atuutilik), 2); return;
        }
        if (말(atiq_surragunnangittuq, "동작맡기기") && 말(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), ilanga_atuutilik = 빼기(2);
            if (화면객체(ilanga_atuutilik)) { 힙[ilanga_atuutilik + 4] = 받이; 힙참조[ilanga_atuutilik + 4] = 1; 힙[ilanga_atuutilik + 12] = 1; } return;
        }
        if (말(atiq_surragunnangittuq, "ilali_ilanga") && 말(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int surusiq_atuutilik = 빼기(2), 부모 = 빼기(2); if (!화면객체(surusiq_atuutilik) || !화면객체(부모)) return;
            if (atuqtuq.화면연결(2, 힙[부모 + 2], 힙[surusiq_atuutilik + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[surusiq_atuutilik + 11] = 부모; 힙참조[surusiq_atuutilik + 11] = 1; return;
        }
        if (말(atiq_surragunnangittuq, "자리정하기") && 말(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), 세로 = 빼기(1), 가로 = 빼기(1), ilanga_atuutilik = 빼기(2); if (!화면객체(ilanga_atuutilik)) return;
            if (atuqtuq.화면연결(1, 힙[ilanga_atuutilik + 2], 가로, 세로, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[ilanga_atuutilik + 5] = 가로; 힙[ilanga_atuutilik + 6] = 세로; 힙[ilanga_atuutilik + 7] = 폭; 힙[ilanga_atuutilik + 8] = 높이; return;
        }
        if ((말(atiq_surragunnangittuq, "saqqilli_igalaangujaq") || 말(atiq_surragunnangittuq, "matuli")) && 말(서술상수, "()V")) {
            boolean takutsauninga_atuutilik = 말(atiq_surragunnangittuq, "saqqilli_igalaangujaq"); int ilanga_atuutilik = 빼기(2); if (!화면객체(ilanga_atuutilik)) return;
            if (atuqtuq.화면연결(takutsauninga_atuutilik ? 3 : 4, 힙[ilanga_atuutilik + 2], takutsauninga_atuutilik ? 1 : 0, 0, 0, 0) < 0) { itigaqtuq_atuutilik("화면은 ilaliujjarvilik 명령에서 실행해야 합니다"); return; }
            힙[ilanga_atuutilik + 9] = takutsauninga_atuutilik ? 1 : 0; return;
        }
        if (말(atiq_surragunnangittuq, "보이는가") && 말(서술상수, "()Z")) { int ilanga_atuutilik = 빼기(2); if (화면객체(ilanga_atuutilik)) 넣기(힙[ilanga_atuutilik + 9], 1); return; }
        itigaqtuq_atuutilik("지원하지 않는 한국어 화면 메서드");
    }
    static void 화면호출(int 소유종, int atiq_surragunnangittuq, int 서술상수, int 명령코드) {
        if (말(소유종, "javax/swing/SwingUtilities")) {
            if (명령코드 == 184 && 말(atiq_surragunnangittuq, "invokeLater") && 말(서술상수, "(Ljava/lang/Runnable;)V")) { int 객체참조 = 빼기(2); if (!객체유효(객체참조)) return; if (나중수 == 8) { itigaqtuq_atuutilik("invokeLater queue full"); return; } 나중실행[나중수++] = 객체참조; return; }
            if (명령코드 == 184 && 말(atiq_surragunnangittuq, "isEventDispatchThread") && 말(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            itigaqtuq_atuutilik("unsupported SwingUtilities method"); return;
        }
        if (말(소유종, "java/awt/event/ActionEvent")) {
            int 객체참조 = 빼기(2); if (!kisu_atuutilik(객체참조, 29)) return;
            if (말(atiq_surragunnangittuq, "getSource") && 말(서술상수, "()Ljava/lang/Object;")) 넣기(힙[객체참조 + 2], 2);
            else if (말(atiq_surragunnangittuq, "getActionCommand") && 말(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[객체참조 + 2]), 2);
            else if (말(atiq_surragunnangittuq, "getID") && 말(서술상수, "()I")) 넣기(1001, 1);
            else itigaqtuq_atuutilik("unsupported ActionEvent method"); return;
        }
        if (명령코드 == 183 && 말(atiq_surragunnangittuq, "<init>")) {
            int 열수 = 0, 글참조 = 0;
            if (말(서술상수, "(I)V")) 열수 = 빼기(1);
            else if (말(서술상수, "(Ljava/lang/String;I)V")) { 열수 = 빼기(1); 글참조 = 빼기(2); }
            else if (말(서술상수, "(Ljava/lang/String;)V")) 글참조 = 빼기(2);
            else if (말(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!말(서술상수, "()V")) { itigaqtuq_atuutilik("unsupported Swing constructor"); return; }
            int 객체참조 = 빼기(2); if (!객체유효(객체참조)) return;
            if (힙[객체참조] == 30) { itigaqtuq_atuutilik("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(객체참조) || 열수 < 0) return;
            int piqaut_atuutilik = atuqtuq.화면연결(0, 힙[객체참조] - 23, 0, 0, 0, 0);
            if (piqaut_atuutilik < 1 || piqaut_atuutilik > 32) { itigaqtuq_atuutilik("GUI widget slots exhausted"); return; }
            힙[객체참조 + 2] = piqaut_atuutilik; 화면참조[piqaut_atuutilik - 1] = 객체참조; 힙[객체참조 + 5] = 힙[객체참조] == 24 ? 130 : 16; 힙[객체참조 + 6] = 힙[객체참조] == 24 ? 110 : 16;
            힙[객체참조 + 7] = 힙[객체참조] == 24 ? 380 : 220; 힙[객체참조 + 8] = 힙[객체참조] == 24 ? 240 : 28; 힙[객체참조 + 10] = 1;
            화면문자설정(객체참조, 글참조); return;
        }
        if (말(atiq_surragunnangittuq, "setText") || 말(atiq_surragunnangittuq, "setTitle")) { int 글참조 = 빼기(2), 객체참조 = 빼기(2); if (화면객체(객체참조) && 말(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(객체참조, 글참조); return; }
        if (말(atiq_surragunnangittuq, "getText") || 말(atiq_surragunnangittuq, "getTitle")) { int 객체참조 = 빼기(2); if (화면객체(객체참조) && 말(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(객체참조), 2); return; }
        if (말(atiq_surragunnangittuq, "addActionListener") && 말(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), 객체참조 = 빼기(2); if (화면객체(객체참조)) { 힙[객체참조 + 4] = 수신참조; 힙참조[객체참조 + 4] = 1; } return; }
        if (말(atiq_surragunnangittuq, "getContentPane") && 말(서술상수, "()Ljava/awt/Container;")) { int 객체참조 = 빼기(2); if (화면객체(객체참조)) 넣기(객체참조, 2); return; }
        if (말(atiq_surragunnangittuq, "setLayout") && 말(서술상수, "(Ljava/awt/LayoutManager;)V")) { int 배치참조 = 빼기(2), 객체참조 = 빼기(2); if (화면객체(객체참조) && 배치참조 != 0) itigaqtuq_atuutilik("only absolute layout (null) is supported"); return; }
        if (말(atiq_surragunnangittuq, "add") && (말(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || 말(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean ilinganinga_qanuinniq = 말(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (ilinganinga_qanuinniq) 빼기(2);
            int 자식참조 = 빼기(2), 객체참조 = 빼기(2); if (!화면객체(자식참조) || !화면객체(객체참조)) return;
            if (atuqtuq.화면연결(2, 힙[객체참조 + 2], 힙[자식참조 + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[자식참조 + 11] = 객체참조; 힙참조[자식참조 + 11] = 1; if (!ilinganinga_qanuinniq) 넣기(자식참조, 2); return;
        }
        if (말(atiq_surragunnangittuq, "setBounds") && 말(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), 가로좌표 = 빼기(1), 객체참조 = 빼기(2); if (!화면객체(객체참조)) return;
            if (atuqtuq.화면연결(1, 힙[객체참조 + 2], 가로좌표, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[객체참조 + 5] = 가로좌표; 힙[객체참조 + 6] = 세로좌표; 힙[객체참조 + 7] = 너비; 힙[객체참조 + 8] = 높이; return;
        }
        if (말(atiq_surragunnangittuq, "setSize") && 말(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 객체참조 = 빼기(2); if (!화면객체(객체참조)) return;
            if (atuqtuq.화면연결(1, 힙[객체참조 + 2], 힙[객체참조 + 5], 힙[객체참조 + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[객체참조 + 7] = 너비; 힙[객체참조 + 8] = 높이; } return;
        }
        if (말(atiq_surragunnangittuq, "setLocationRelativeTo") && 말(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), 객체참조 = 빼기(2); if (!화면객체(객체참조)) return; if (상대배치 != 0) { itigaqtuq_atuutilik("only screen centering supported"); return; } 힙[객체참조 + 5] = (atuqtuq.화면너비() - 힙[객체참조 + 7]) / 2; 힙[객체참조 + 6] = (atuqtuq.화면높이() - 힙[객체참조 + 8]) / 2; atuqtuq.화면연결(1, 힙[객체참조 + 2], 힙[객체참조 + 5], 힙[객체참조 + 6], 힙[객체참조 + 7], 힙[객체참조 + 8]); return; }
        if (말(atiq_surragunnangittuq, "setDefaultCloseOperation") && 말(서술상수, "(I)V")) { int 종료정책 = 빼기(1), 객체참조 = 빼기(2); if (화면객체(객체참조)) { if (종료정책 < 0 || 종료정책 > 3) 예외던짐(9, "close policy"); else { 힙[객체참조 + 10] = 종료정책; atuqtuq.화면연결(7, 힙[객체참조 + 2], 종료정책, 0, 0, 0); } } return; }
        if (말(atiq_surragunnangittuq, "setVisible") && 말(서술상수, "(Z)V")) { int titiqqat_atuutilik = 빼기(1), 객체참조 = 빼기(2); if (화면객체(객체참조)) { int 처리값 = atuqtuq.화면연결(3, 힙[객체참조 + 2], titiqqat_atuutilik, 0, 0, 0); if (처리값 < 0) itigaqtuq_atuutilik("Swing requires a standalone interactive command"); else 힙[객체참조 + 9] = titiqqat_atuutilik; } return; }
        if (말(atiq_surragunnangittuq, "dispose") && 말(서술상수, "()V")) { int 객체참조 = 빼기(2); if (화면객체(객체참조)) { atuqtuq.화면연결(4, 힙[객체참조 + 2], 0, 0, 0, 0); 힙[객체참조 + 9] = 0; } return; }
        if (말(atiq_surragunnangittuq, "repaint") || 말(atiq_surragunnangittuq, "validate")) { int 객체참조 = 빼기(2); if (!화면객체(객체참조) || !말(서술상수, "()V")) return; atuqtuq.화면연결(1, 힙[객체참조 + 2], 힙[객체참조 + 5], 힙[객체참조 + 6], 힙[객체참조 + 7], 힙[객체참조 + 8]); return; }
        if (말(atiq_surragunnangittuq, "isVisible") && 말(서술상수, "()Z")) { int 객체참조 = 빼기(2); if (화면객체(객체참조)) 넣기(힙[객체참조 + 9], 1); return; }
        itigaqtuq_atuutilik("unsupported Swing method (native subset)");
    }
    static void 사건실행(int turaagaq_turaarut, int 사건번호, boolean 한국어) {
        if (turaagaq_turaarut < 1 || 힙[turaagaq_turaarut] < 32) { itigaqtuq_atuutilik("Java event listener required"); return; }
        int ini_nalunaiqsimavik = 이름함수(힙[turaagaq_turaarut] - 32, 사건번호 == 0 ? (한국어 ? "실행하기" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (ini_nalunaiqsimavik < 0) { itigaqtuq_atuutilik("event callback missing"); return; }
        현재가닥 = 0; 가닥수 = 1; avalu_nalunaiqsimavik = 0; aqqusiqtarvik_qanuilinganiq[0] = 1; 틀스택[0] = 0; 틀잠금[0] = aturunnaqsili_avalu[0] = 0; 바꿈요청 = false;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 128; piliqqittaajuq_nalunaiqsimavik++) { tamaani_atuutilik[piliqqittaajuq_nalunaiqsimavik] = tamaani_qanuittuuninga[piliqqittaajuq_nalunaiqsimavik] = 0; }
        틀함수[0] = ini_nalunaiqsimavik; 틀위치[0] = 함수시작[ini_nalunaiqsimavik]; tamaani_atuutilik[0] = turaagaq_turaarut; tamaani_qanuittuuninga[0] = 2;
        if (사건번호 != 0) { tamaani_atuutilik[1] = 사건번호; tamaani_qanuittuuninga[1] = 2; }
        사건중 = true; 실행(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!tammarniq) {
            if (나중수 > 0) { int turaagaq_turaarut = 나중실행[0], 한국어 = 나중한국어[0]; for (int piliqqittaajuq_nalunaiqsimavik = 1; piliqqittaajuq_nalunaiqsimavik < 나중수; piliqqittaajuq_nalunaiqsimavik++) { 나중실행[piliqqittaajuq_nalunaiqsimavik - 1] = 나중실행[piliqqittaajuq_nalunaiqsimavik]; 나중한국어[piliqqittaajuq_nalunaiqsimavik - 1] = 나중한국어[piliqqittaajuq_nalunaiqsimavik]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(turaagaq_turaarut, 0, 한국어 != 0); continue; }
            if (atuqtuq.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = atuqtuq.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { itigaqtuq_atuutilik("GUI event I/O failed"); return; }
            int piqaut_atuutilik = 사건번호 & 65535; if (piqaut_atuutilik < 1 || piqaut_atuutilik > 32) continue; int 객체참조 = 화면참조[piqaut_atuutilik - 1]; if (객체참조 == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[객체참조 + 10] != 0) 힙[객체참조 + 9] = 0;
                if (힙[객체참조 + 10] == 3) for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 32; piliqqittaajuq_nalunaiqsimavik++) if (화면참조[piliqqittaajuq_nalunaiqsimavik] != 0 && 힙[화면참조[piliqqittaajuq_nalunaiqsimavik]] == 24) atuqtuq.화면연결(4, piliqqittaajuq_nalunaiqsimavik + 1, 0, 0, 0, 0);
            } else if (힙[객체참조 + 4] != 0) {
                int 안내참조 = 할당(29, 2); if (tammarniq) return; 힙[안내참조 + 2] = 객체참조; 힙[안내참조 + 3] = 힙[객체참조 + 12]; 힙참조[안내참조 + 2] = 1; 사건실행(힙[객체참조 + 4], 안내참조, 힙[객체참조 + 12] != 0);
            }
        }
    }
    public static int 시작() {
        if (atuqtuq.인수개수() == 1 && 자바도구.같음(atuqtuq.인수(0), "-version")) {
            atuqtuq.titiraq("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (atuqtuq.인수개수() < 1) { atuqtuq.titiraq("Usage: java CLASS [ARGS]\n"); return 2; }
        시작종 = 종적재(tuttarvik_immikkuuqtuq(atuqtuq.인수(0))); if (tammarniq || 시작종 < 0) return 1;
        int Iliniku_puinti_atuutilik = 이름함수(시작종, "시작", "()V");
        boolean 한국어진입 = Iliniku_puinti_atuutilik >= 0 && (함수권한[Iliniku_puinti_atuutilik] & 9) == 9;
        if (!한국어진입) Iliniku_puinti_atuutilik = 이름함수(시작종, "main", "([Ljava/lang/String;)V");
        if (Iliniku_puinti_atuutilik < 0 || (함수권한[Iliniku_puinti_atuutilik] & 9) != 9) itigaqtuq_atuutilik("public static void 시작() or main(String[] args) required");
        if (tammarniq) return 1;
        int 인수 = 할당(3, atuqtuq.인수개수() - 1); array_ilanga[인수] = -1;
        for (int 수 = 1; 수 < atuqtuq.인수개수() && !tammarniq; 수++) 힙[인수 + 1 + 수] = tuttarvik_immikkuuqtuq(atuqtuq.인수(수));
        avalu_nalunaiqsimavik = 0; 틀함수[0] = Iliniku_puinti_atuutilik; 틀위치[0] = 함수시작[Iliniku_puinti_atuutilik]; tamaani_atuutilik[0] = 한국어진입 ? 0 : 인수; tamaani_qanuittuuninga[0] = 한국어진입 ? 0 : 2;
        aqqusiqtarvik_qanuilinganiq[0] = 1; aqqusiqtarvik_kisu[0] = 할당(13, 2);
        실행(); if (!tammarniq) 화면사건들(); return tammarniq ? 1 : 0;
    }
}
