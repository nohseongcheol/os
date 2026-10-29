// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. fiilde/스택/참조/분기 경계를 실행 중 검사한다. */
public final class 자바가상기계 {
    static int[] fiilde = new int[16 * 16384], 임시파일 = new int[16384], fiilde_innde_binndi = new int[512];
    static int[] 상종류 = new int[8192], 상가 = new int[8192], 상나 = new int[8192], 문자열참조 = new int[8192];
    static int[] 함수명 = new int[512], 함수형 = new int[512], 함수권한 = new int[512], 함수주인 = new int[512];
    static int[] 함수시작 = new int[512], 함수끝 = new int[512], 함수스택 = new int[512], 함수지역 = new int[512];
    static int[] 함수인수수 = new int[512], 함수인수형 = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] nokkuwal_njaru = new int[16384], 지역형 = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] 틀함수 = new int[128], 틀위치 = new int[128], 틀스택 = new int[128], taƴtinnde_yamiroore = new int[128], ɓamtinde_taƴtinnde = new int[128];
    static int[] 종이름 = new int[16], 종크기 = new int[16], 종부모 = new int[16], 종상태 = new int[16], 종칸수 = new int[16], 종초기화 = new int[16];
    static int[] fedde_jokkondirgal = new int[16 * 16], 종접면수 = new int[16];
    static int[] 칸이름 = new int[512], 칸형 = new int[512], 칸주인 = new int[512], 칸권한 = new int[512], 칸위치 = new int[512], 칸값 = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], 배열원소 = new int[32768], 정수저장 = new int[256];
    static int waylude_etannde, 읽기위치, 함수수, fedde_innde, taƴtinnde_joopirdu = -1, 힙끝 = 1, 반환형;
    static int 종수, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, 표시수, 수거횟수;
    static int 현재가닥, 가닥수 = 1, 시작종;
    static int[] piilol_taƴtinnde = new int[4], piilol_ngonka = new int[4], piilol_huunde = new int[4], piilol_faandaare = new int[4], 가닥대기 = new int[4];
    static boolean juumre, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], fedde_piilol = new int[16];

    static void ella_njaru(String 말) {
        if (juumre) return;
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
        if (분류코드 != 0 && taƴtinnde_joopirdu >= 0) { 예외던짐(분류코드, 말); return; }
        kuutoro.winndude("JVM error: "); kuutoro.winndude(말); kuutoro.winndude_alkulal_njaru(10); juumre = true;
    }
    static boolean kilip(int huutoraade, int njuuteendi_njaru) {
        if (huutoraade < 0 || huutoraade >= fiilde.length || njuuteendi_njaru < 0) return false;
        int 종 = huutoraade / 16384;
        return huutoraade % 16384 <= 종크기[종] && njuuteendi_njaru <= 종크기[종] - huutoraade % 16384;
    }
    static int oktee_njaru() {
        if (!kilip(읽기위치, 1)) { ella_njaru("truncated class file"); return 0; }
        return fiilde[읽기위치++];
    }
    static int 짧은수() { return oktee_njaru() << 8 | oktee_njaru(); }
    static int 정수() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int njuuteendi_njaru) { if (!kilip(읽기위치, njuuteendi_njaru)) ella_njaru("invalid attribute size"); else 읽기위치 += njuuteendi_njaru; }
    static boolean 상검사(int 수, int 종류) {
        if (수 <= 0 || 수 >= 상종류.length || 상종류[수] != 종류) { ella_njaru("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int huutoraade, int njuuteendi_njaru, String 말) {
        if (!kilip(huutoraade, njuuteendi_njaru)) return false;
        int 읽는자리 = huutoraade, 끝 = huutoraade + njuuteendi_njaru;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 말.length(); kowal_joopirdu++) {
            int 문자값 = 말.charAt(kowal_joopirdu);
            if (문자값 > 0 && 문자값 < 128) { if (읽는자리 >= 끝 || fiilde[읽는자리++] != 문자값) return false; }
            else if (문자값 < 2048) {
                if (읽는자리 + 2 > 끝 || fiilde[읽는자리++] != (192 | (문자값 >> 6)) || fiilde[읽는자리++] != (128 | (문자값 & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || fiilde[읽는자리++] != (224 | (문자값 >> 12)) || fiilde[읽는자리++] != (128 | ((문자값 >> 6) & 63)) || fiilde[읽는자리++] != (128 | (문자값 & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean 말(int 상수, String 말) { return 상검사(상수, 1) && 구간(상가[상수], 상나[상수], 말); }
    static boolean 같은말(int 가, int 나) {
        if (!상검사(가, 1) || !상검사(나, 1) || 상나[가] != 상나[나]) return false;
        for (int 수 = 0; 수 < 상나[가]; 수++) if (fiilde[상가[가] + 수] != fiilde[상가[나] + 수]) return false;
        return true;
    }
    static int fedde_innde_binndi(int 수) { return 상검사(수, 7) && 상검사(상가[수], 1) ? 상가[수] : 0; }
    static int 참조이름(int 수) { return 상검사(수, 12) && 상검사(상가[수], 1) ? 상가[수] : 0; }
    static int 참조형식(int 수) { return 상검사(수, 12) && 상검사(상나[수], 1) ? 상나[수] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (읽기위치 >= 끝) { ella_njaru("invalid descriptor"); return 0; }
        int njaru = oktee_njaru();
        if (njaru == 'V' && 빈형) return 0;
        if (njaru == 'I' || njaru == 'B' || njaru == 'C' || njaru == 'S' || njaru == 'Z') return 1;
        if (njaru == '[') { 서술형(끝, false); return 2; }
        if (njaru == 'L') {
            int huutoraade = 읽기위치;
            while (읽기위치 < 끝 && fiilde[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == huutoraade) ella_njaru("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        ella_njaru("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int juɓɓol_njaru) {
        int 이전 = 읽기위치, 수 = 함수형[juɓɓol_njaru];
        if (!상검사(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + 상나[수];
        if (oktee_njaru() != '(') ella_njaru("invalid method descriptor");
        int 개수 = 0;
        while (!juumre && 읽기위치 < 끝 && fiilde[읽기위치] != ')') {
            if (개수 == 16) { ella_njaru("too many method arguments"); break; }
            함수인수형[juɓɓol_njaru * 16 + 개수++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || oktee_njaru() != ')') ella_njaru("invalid method descriptor");
        함수반환[juɓɓol_njaru] = 서술형(끝, true); 함수인수수[juɓɓol_njaru] = 개수;
        if (읽기위치 != 끝) ella_njaru("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int njaru = 짧은수(); return njaru == 0 ? 0 : 현재읽는종 * 512 + njaru; }
    static int 명상수() { return 함수주인[틀함수[taƴtinnde_joopirdu]] * 512 + 명짧(); }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !juumre; 수++) { 상검사(상번호(), 1); 건너(정수()); }
    }
    static int ginol_njuuteendi(int njaru) {
        if (njaru == 16 || njaru == 18 || njaru == 21 || njaru == 25 || njaru == 54 || njaru == 58 || njaru == 188) return 2;
        if (njaru == 17 || njaru == 19 || njaru == 132 || njaru >= 153 && njaru <= 167
            || njaru >= 178 && njaru <= 184 || njaru == 187 || njaru == 189 || njaru == 192 || njaru == 193 || njaru == 198 || njaru == 199) return 3;
        if (njaru == 185 || njaru == 200) return 5;
        if (njaru >= 0 && njaru <= 8 || njaru >= 26 && njaru <= 29 || njaru >= 42 && njaru <= 46 || njaru >= 50 && njaru <= 53
            || njaru >= 59 && njaru <= 62 || njaru >= 75 && njaru <= 79 || njaru >= 83 && njaru <= 95
            || njaru == 96 || njaru == 100 || njaru == 104 || njaru == 108 || njaru == 112 || njaru == 116
            || njaru == 120 || njaru == 122 || njaru == 124 || njaru == 126 || njaru == 128 || njaru == 130
            || njaru >= 145 && njaru <= 147 || njaru == 172 || njaru == 176 || njaru == 177 || njaru == 190 || njaru == 191
            || njaru == 194 || njaru == 195) return 1;
        return 0;
    }
    static int 위치정수(int 읽는자리) {
        if (!kilip(읽는자리, 4)) { ella_njaru("truncated bytecode operand"); return 0; }
        return fiilde[읽는자리] << 24 | fiilde[읽는자리 + 1] << 16 | fiilde[읽는자리 + 2] << 8 | fiilde[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int huutoraade, int 끝) {
        int njaru = fiilde[읽는자리], njuuteendi_njaru = ginol_njuuteendi(njaru);
        if (njaru == 170 || njaru == 171) {
            int 기준자리 = 읽는자리 + 1;
            while ((기준자리 - huutoraade) % 4 != 0) 기준자리++;
            if (끝 - 기준자리 < (njaru == 170 ? 12 : 8)) return 0;
            int 항목수 = njaru == 170 ? 위치정수(기준자리 + 8) - 위치정수(기준자리 + 4) + 1 : 위치정수(기준자리 + 4);
            if (항목수 < 0 || 항목수 > 2048) return 0;
            njuuteendi_njaru = 기준자리 - 읽는자리 + (njaru == 170 ? 12 + 4 * 항목수 : 8 + 8 * 항목수);
        }
        if (njaru == 196 && 읽는자리 + 1 < 끝) {
            int 단어값 = fiilde[읽는자리 + 1]; njuuteendi_njaru = 단어값 == 132 ? 6 : (단어값 == 21 || 단어값 == 25 || 단어값 == 54 || 단어값 == 58) ? 4 : 0;
        }
        return njuuteendi_njaru > 0 && njuuteendi_njaru <= 끝 - 읽는자리 ? njuuteendi_njaru : 0;
    }
    static void sek_tiindaare_njaru(int tiindaare_njaru, int juɓɓol_njaru) {
        if (tiindaare_njaru < 함수시작[juɓɓol_njaru] || tiindaare_njaru >= 함수끝[juɓɓol_njaru] || 경계[tiindaare_njaru] != juɓɓol_njaru + 1) ella_njaru("invalid branch target");
    }
    static void 클래스읽기(int 종) {
        현재읽는종 = 종; 읽기위치 = 종 * 16384; waylude_etannde = 읽기위치 + 종크기[종];
        if (정수() != 0xcafebabe) { ella_njaru("not a class file"); return; }
        int 부판 = 짧은수(), yamre_njaru = 짧은수();
        if (yamre_njaru < 45 || yamre_njaru > 52 || 부판 != 0) { ella_njaru("supported class versions: 45..52, minor 0"); return; }
        int 상수수 = 짧은수(), 기준자리 = 종 * 512;
        if (상수수 < 1 || 상수수 > 512) { ella_njaru("constant pool limit (511)"); return; }
        for (int 항목수 = 1; 항목수 < 상수수 && !juumre; 항목수++) {
            int 수 = 기준자리 + 항목수, 종류 = oktee_njaru(); 상종류[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = 정수();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); 상나[수] = 상번호(); }
            else ella_njaru("unsupported constant type");
        }
        int 권한 = 짧은수();
        if ((권한 & (0x2000 | 0x4000)) != 0) ella_njaru("annotation/enum class unsupported");
        종이름[종] = fedde_innde_binndi(상번호());
        종부모[종] = fedde_innde_binndi(상번호());
        int 접면수 = 짧은수(); if (접면수 > 16) { ella_njaru("interface count limit"); return; }
        종접면수[종] = 접면수;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 접면수; kowal_joopirdu++) fedde_jokkondirgal[종 * 16 + kowal_joopirdu] = fedde_innde_binndi(상번호());
        int 필드수 = 짧은수();
        if (필드수 > 512 - 칸수) { ella_njaru("field count limit (512)"); return; }
        for (int kowal_joopirdu = 0; kowal_joopirdu < 필드수 && !juumre; kowal_joopirdu++) {
            int fiilde_joopirdu = 칸수++; 칸주인[fiilde_joopirdu] = 종; 칸권한[fiilde_joopirdu] = 짧은수(); 칸이름[fiilde_joopirdu] = 상번호(); 칸형[fiilde_joopirdu] = 상번호();
            상검사(칸이름[fiilde_joopirdu], 1); 상검사(칸형[fiilde_joopirdu], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[칸형[fiilde_joopirdu]]; int 분류코드 = 서술형(읽기위치 + 상나[칸형[fiilde_joopirdu]], false); 읽기위치 = 보존값;
            if ((칸권한[fiilde_joopirdu] & 8) == 0) 칸위치[fiilde_joopirdu] = 종칸수[종]++;
            int mbaadi_keɓe = 짧은수();
            for (int 안쪽자리 = 0; 안쪽자리 < mbaadi_keɓe && !juumre; 안쪽자리++) {
                int 이름상수 = 상번호(), 유효길이 = 정수();
                if (말(이름상수, "ConstantValue") && 유효길이 == 2) {
                    int keɓe_njaru = 상번호();
                    if (분류코드 == 1 && 상검사(keɓe_njaru, 3)) 칸값[fiilde_joopirdu] = 상가[keɓe_njaru];
                    else if (분류코드 == 2 && 상검사(keɓe_njaru, 8)) 칸값[fiilde_joopirdu] = 상문자(상가[keɓe_njaru]);
                } else 건너(유효길이);
            }
        }
        int 개수 = 짧은수();
        if (개수 > 512 - 함수수) { ella_njaru("method count limit (512)"); return; }
        for (int kowal_joopirdu = 0; kowal_joopirdu < 개수 && !juumre; kowal_joopirdu++) {
            int 수 = 함수수++; 함수주인[수] = 종;
            함수권한[수] = 짧은수(); 함수명[수] = 상번호(); 함수형[수] = 상번호();
            상검사(함수명[수], 1); 서술읽기(수);
            if ((함수권한[수] & 8) == 0) {
                if (함수인수수[수] == 16) { ella_njaru("too many instance method arguments"); return; }
                for (int 비교자리 = 함수인수수[수]; 비교자리 > 0; 비교자리--) 함수인수형[수 * 16 + 비교자리] = 함수인수형[수 * 16 + 비교자리 - 1];
                함수인수형[수 * 16] = 2; 함수인수수[수]++;
            }
            if ((함수권한[수] & 0x100) != 0) ella_njaru("user native method unsupported");
            if (말(함수명[수], "<clinit>")) 종초기화[종] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (함수주인[앞] == 종 && 같은말(함수명[앞], 함수명[수]) && 같은말(함수형[앞], 함수형[수])) ella_njaru("duplicate method");
            int 속성수 = 짧은수();
            for (int mbaadi_njaru = 0; mbaadi_njaru < 속성수 && !juumre; mbaadi_njaru++) {
                int innde = 상번호(), njuuteendi_njaru = 정수(), huutoraade = 읽기위치;
                if (!kilip(huutoraade, njuuteendi_njaru)) { ella_njaru("truncated method attribute"); break; }
                if (말(innde, "Code")) {
                    if (함수시작[수] != 0) ella_njaru("duplicate Code attribute");
                    함수스택[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = 정수();
                    if (함수스택[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) ella_njaru("method memory limits exceeded");
                    함수시작[수] = 읽기위치; 건너(코드길이); 함수끝[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { ella_njaru("exception table limit"); return; }
                    for (int 안쪽자리 = 0; 안쪽자리 < 잡는수; 안쪽자리++) {
                        int 오류참조 = 잡기수++; 잡기함수[오류참조] = 수;
                        잡기시작[오류참조] = 함수시작[수] + 짧은수(); 잡기끝[오류참조] = 함수시작[수] + 짧은수();
                        잡기위치[오류참조] = 함수시작[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[오류참조] = 부호값 == 0 ? 0 : fedde_innde_binndi(부호값);
                    }
                    속성건너();
                    if (읽기위치 != huutoraade + njuuteendi_njaru) ella_njaru("Code attribute size mismatch");
                } else 건너(njuuteendi_njaru);
            }
            if ((함수권한[수] & 0x400) != 0) continue;
            if (함수시작[수] == 0) ella_njaru("missing Code attribute");
            int 칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !juumre) {
                int njuuteendi_njaru = 길이읽기(칸, 함수시작[수], 함수끝[수]);
                if (njuuteendi_njaru == 0) { ella_njaru("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += njuuteendi_njaru;
            }
            칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !juumre) {
                int njaru = fiilde[칸];
                if (njaru >= 153 && njaru <= 167 || njaru == 198 || njaru == 199) sek_tiindaare_njaru(칸 + (short)(fiilde[칸 + 1] << 8 | fiilde[칸 + 2]), 수);
                if (njaru == 200) sek_tiindaare_njaru(칸 + 위치정수(칸 + 1), 수);
                if (njaru == 170 || njaru == 171) {
                    int 읽는자리 = 칸 + 1; while ((읽는자리 - 함수시작[수]) % 4 != 0) 읽는자리++;
                    sek_tiindaare_njaru(칸 + 위치정수(읽는자리), 수);
                    int 항목수 = njaru == 170 ? 위치정수(읽는자리 + 8) - 위치정수(읽는자리 + 4) + 1 : 위치정수(읽는자리 + 4);
                    읽는자리 += njaru == 170 ? 12 : 8;
                    for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) sek_tiindaare_njaru(칸 + 위치정수(읽는자리 + 안쪽자리 * (njaru == 170 ? 4 : 8) + (njaru == 170 ? 0 : 4)), 수);
                }
                칸 += 길이읽기(칸, 함수시작[수], 함수끝[수]);
            }
            for (int 안쪽자리 = 0; 안쪽자리 < 잡기수; 안쪽자리++) if (잡기함수[안쪽자리] == 수) {
                sek_tiindaare_njaru(잡기시작[안쪽자리], 수); sek_tiindaare_njaru(잡기위치[안쪽자리], 수);
                if (잡기끝[안쪽자리] != 함수끝[수]) sek_tiindaare_njaru(잡기끝[안쪽자리], 수);
                if (잡기시작[안쪽자리] >= 잡기끝[안쪽자리]) ella_njaru("invalid exception range");
            }
        }
        if (!juumre) 속성건너();
        if (읽기위치 != waylude_etannde) ella_njaru("extra class file data");
    }
    static int 할당(int 종류, int njuuteendi_njaru) { return 새기억(종류, njuuteendi_njaru); }
    static boolean huunde_njaru(int 참조, int 종류) {
        if (!객체유효(참조)) return false;
        if (힙[참조] != 종류) { ella_njaru("object type mismatch"); return false; }
        return true;
    }
    static int 상문자(int joopirdu) {
        if (!상검사(joopirdu, 1)) return 0;
        if (문자열참조[joopirdu] != 0) return 문자열참조[joopirdu];
        int 참조 = 할당(1, 상나[joopirdu]); if (juumre) return 0;
        int 끝 = 상가[joopirdu] + 상나[joopirdu], 수 = 상가[joopirdu], njuuteendi_njaru = 0;
        while (수 < 끝 && !juumre) {
            int njaru = fiilde[수++];
            if (njaru == 0) ella_njaru("invalid modified UTF-8");
            else if (njaru >= 192 && njaru <= 223 && 수 < 끝) {
                int 다음 = fiilde[수++];
                if ((다음 & 192) != 128) ella_njaru("invalid modified UTF-8");
                njaru = (njaru & 31) << 6 | 다음 & 63;
                if (njaru != 0 && njaru < 128) ella_njaru("overlong modified UTF-8");
            } else if (njaru >= 224 && njaru <= 239 && 수 + 1 < 끝) {
                int 가 = fiilde[수++], 나 = fiilde[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) ella_njaru("invalid modified UTF-8");
                njaru = (njaru & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (njaru < 2048) ella_njaru("overlong modified UTF-8");
            } else if (njaru >= 128) ella_njaru("invalid modified UTF-8");
            힙[참조 + 2 + njuuteendi_njaru++] = njaru;
        }
        힙[참조 + 1] = njuuteendi_njaru; 문자열참조[joopirdu] = 참조; return 참조;
    }
    static int njaatigi_alkulal(String njaru) {
        int 참조 = 할당(1, njaru.length()); if (juumre) return 0;
        for (int 수 = 0; 수 < njaru.length(); 수++) 힙[참조 + 2 + 수] = njaru.charAt(수);
        return 참조;
    }
    static void winndude_binndi(int 참조) {
        if (참조 == 0) { kuutoro.winndude("null"); return; }
        if (!huunde_njaru(참조, 1)) return;
        for (int 수 = 0; 수 < 힙[참조 + 1]; 수++) kuutoro.winndude_alkulal_njaru(힙[참조 + 2 + 수]);
    }
    static int 수문자(int njaru) {
        int 참조 = 할당(1, 11); if (juumre) return 0;
        int njuuteendi_njaru = 0;
        if (njaru < 0) 힙[참조 + 2 + njuuteendi_njaru++] = '-'; else njaru = -njaru;
        int 자리 = 1000000000; boolean huutoraade = false;
        while (자리 != 0) {
            int 수 = -(njaru / 자리);
            if (수 != 0 || huutoraade || 자리 == 1) { 힙[참조 + 2 + njuuteendi_njaru++] = '0' + 수; huutoraade = true; }
            njaru %= 자리; 자리 /= 10;
        }
        힙[참조 + 1] = njuuteendi_njaru; return 참조;
    }
    static int 정수해독(int 참조) {
        if (!huunde_njaru(참조, 1)) return 0;
        int njuuteendi_njaru = 힙[참조 + 1], 수 = 0, njaru = 0; boolean 음수 = false;
        if (njuuteendi_njaru > 0 && (힙[참조 + 2] == '-' || 힙[참조 + 2] == '+')) { 음수 = 힙[참조 + 2] == '-'; 수++; }
        if (수 == njuuteendi_njaru) ella_njaru("NumberFormatException");
        for (; 수 < njuuteendi_njaru && !juumre; 수++) {
            int 숫자 = 힙[참조 + 2 + 수] - '0';
            if (숫자 < 0 || 숫자 > 9 || njaru < -214748364 || njaru == -214748364 && 숫자 > (음수 ? 8 : 7)) ella_njaru("NumberFormatException");
            njaru = njaru * 10 - 숫자;
        }
        return 음수 ? njaru : -njaru;
    }
    static void 넣기(int njaru, int 형) {
        if (juumre) return;
        if (taƴtinnde_joopirdu < 0 || 틀스택[taƴtinnde_joopirdu] >= 함수스택[틀함수[taƴtinnde_joopirdu]]) { ella_njaru("operand stack overflow"); return; }
        int 칸 = taƴtinnde_joopirdu * 128 + 틀스택[taƴtinnde_joopirdu]++; 스택값[칸] = njaru; 스택형[칸] = 형;
    }
    static int 빼기(int 형) {
        if (juumre) return 0;
        if (taƴtinnde_joopirdu < 0 || 틀스택[taƴtinnde_joopirdu] < 1) { ella_njaru("operand stack underflow"); return 0; }
        int 칸 = taƴtinnde_joopirdu * 128 + --틀스택[taƴtinnde_joopirdu]; 반환형 = 스택형[칸];
        if (형 != 0 && 반환형 != 형) ella_njaru("operand type mismatch");
        if (반환형 == 2) suurde_njaru(스택값[칸]);
        return 스택값[칸];
    }
    static void 지역읽기(int joopirdu, int 형) {
        if (joopirdu >= 함수지역[틀함수[taƴtinnde_joopirdu]] || joopirdu < 0 || 지역형[taƴtinnde_joopirdu * 128 + joopirdu] != 형) { ella_njaru("invalid or uninitialized local"); return; }
        넣기(nokkuwal_njaru[taƴtinnde_joopirdu * 128 + joopirdu], 형);
    }
    static void winndude_nokkuwal(int joopirdu, int 형) {
        if (joopirdu >= 함수지역[틀함수[taƴtinnde_joopirdu]] || joopirdu < 0) { ella_njaru("local index out of range"); return; }
        int njaru = 빼기(형); nokkuwal_njaru[taƴtinnde_joopirdu * 128 + joopirdu] = njaru; 지역형[taƴtinnde_joopirdu * 128 + joopirdu] = 형;
    }
    static int 명바() {
        int 위치 = 틀위치[taƴtinnde_joopirdu];
        if (위치 < 함수시작[틀함수[taƴtinnde_joopirdu]] || 위치 >= 함수끝[틀함수[taƴtinnde_joopirdu]]) { ella_njaru("instruction pointer out of range"); return 0; }
        틀위치[taƴtinnde_joopirdu]++; return fiilde[위치];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void dirtinde_njaru(int 위치) {
        int juɓɓol_njaru = 틀함수[taƴtinnde_joopirdu];
        if (위치 < 함수시작[juɓɓol_njaru] || 위치 >= 함수끝[juɓɓol_njaru] || 경계[위치] != juɓɓol_njaru + 1) ella_njaru("invalid branch target");
        else 틀위치[taƴtinnde_joopirdu] = 위치;
    }
    static void 호출(int juɓɓol_njaru) {
        if (taƴtinnde_joopirdu % 32 == 31) { ella_njaru("call stack limit (32)"); return; }
        int 다음 = taƴtinnde_joopirdu + 1;
        for (int 수 = 0; 수 < 128; 수++) 지역형[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[juɓɓol_njaru] - 1; 수 >= 0; 수--) {
            nokkuwal_njaru[다음 * 128 + 수] = 빼기(함수인수형[juɓɓol_njaru * 16 + 수]); 지역형[다음 * 128 + 수] = 함수인수형[juɓɓol_njaru * 16 + 수];
        }
        if (juumre) return;
        taƴtinnde_joopirdu = 다음; ɓamtinde_taƴtinnde[taƴtinnde_joopirdu] = 0; 틀함수[taƴtinnde_joopirdu] = juɓɓol_njaru; 틀위치[taƴtinnde_joopirdu] = 함수시작[juɓɓol_njaru]; 틀스택[taƴtinnde_joopirdu] = 0;
    }
    static void 반환(int 형) {
        if (형 != 함수반환[틀함수[taƴtinnde_joopirdu]]) { ella_njaru("return type mismatch"); return; }
        int njaru = 형 == 0 ? 0 : 빼기(형);
        if (ɓamtinde_taƴtinnde[taƴtinnde_joopirdu] != 0) 종상태[ɓamtinde_taƴtinnde[taƴtinnde_joopirdu] - 1] = 2;
        if (틀잠금[taƴtinnde_joopirdu] != 0) { 잠금풀기(틀잠금[taƴtinnde_joopirdu]); 틀잠금[taƴtinnde_joopirdu] = 0; }
        taƴtinnde_joopirdu--; if (taƴtinnde_joopirdu >= 현재가닥 * 32 && 형 != 0) 넣기(njaru, 형);
    }
    static int[] waraango_fiilde_innde = new int[64];
    static void fiilde_waraango_noddude(int 소유, int innde, int formaa_njaru, int ginol) {
        boolean 출력 = 말(소유, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (ginol == 183 && 말(innde, "<init>")) {
            boolean 이어 = false;
            if (출력 && 말(formaa_njaru, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!말(formaa_njaru, "(Ljava/lang/String;)V")) { ella_njaru("unsupported file stream constructor"); return; }
            int fiilde_naatnugol_innde = 빼기(2), waraango_njaru = 빼기(2);
            if (!huunde_njaru(fiilde_naatnugol_innde, 1) || !huunde_njaru(waraango_njaru, 종류) || juumre) return;
            if (힙[waraango_njaru + 3] != 0) { ella_njaru("file stream already initialized"); return; }
            int njuuteendi_njaru = 힙[fiilde_naatnugol_innde + 1];
            if (njuuteendi_njaru < 1 || njuuteendi_njaru > 63) { ella_njaru("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < njuuteendi_njaru; 칸++) {
                int njaru = 힙[fiilde_naatnugol_innde + 2 + 칸];
                if (njaru < 1) { ella_njaru("invalid file stream path"); return; }
                waraango_fiilde_innde[칸] = njaru;
            }
            waraango_fiilde_innde[njuuteendi_njaru] = 0;
            int 서술자 = kuutoro.파일서술자열기(waraango_fiilde_innde, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { ella_njaru("FileNotFoundException: file open failed"); return; }
            힙[waraango_njaru + 2] = 서술자; 힙[waraango_njaru + 3] = 1;
            return;
        }
        if (ginol != 182) { ella_njaru("invalid file stream invocation"); return; }
        if ((출력 && 말(innde, "write") || !출력 && 말(innde, "read"))
            && (말(formaa_njaru, 출력 ? "([B)V" : "([B)I") || 말(formaa_njaru, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean kilip_njaru = 말(formaa_njaru, 출력 ? "([BII)V" : "([BII)I");
            int 항목수 = kilip_njaru ? 빼기(1) : 0, 시작점 = kilip_njaru ? 빼기(1) : 0, 자료배열 = 빼기(2), 객체참조 = 빼기(2);
            if (!huunde_njaru(자료배열, 20) || !huunde_njaru(객체참조, 종류)) return;
            if (!kilip_njaru) 항목수 = 힙[자료배열 + 1];
            if (시작점 < 0 || 항목수 < 0 || 시작점 > 힙[자료배열 + 1] - 항목수) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[객체참조 + 3] == 0 || 힙[객체참조 + 2] < 0) { ella_njaru("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < 항목수 && !juumre) {
                int 반환값 = 출력 ? kuutoro.파일한바이트쓰기(힙[객체참조 + 2], 힙[자료배열 + 2 + 시작점 + 완료수]) : kuutoro.파일한바이트읽기(힙[객체참조 + 2]);
                if (반환값 < 0) { ella_njaru(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[자료배열 + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(항목수 != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && 말(innde, "flush") && 말(formaa_njaru, "()V")) { int 객체참조 = 빼기(2); if (huunde_njaru(객체참조, 종류) && 힙[객체참조 + 2] < 0) ella_njaru("IOException: stream closed"); return; }
        int gollal = -1, njaru = 0;
        if (말(innde, "close") && 말(formaa_njaru, "()V")) gollal = 0;
        if (!출력 && 말(innde, "read") && 말(formaa_njaru, "()I")) gollal = 1;
        if (출력 && 말(innde, "write") && 말(formaa_njaru, "(I)V")) { gollal = 2; njaru = 빼기(1); }
        if (gollal < 0) { ella_njaru("unsupported file stream method"); return; }
        int waraango_njaru = 빼기(2);
        if (!huunde_njaru(waraango_njaru, 종류) || juumre) return;
        if (힙[waraango_njaru + 3] == 0) { ella_njaru("uninitialized file stream"); return; }
        int 서술자 = 힙[waraango_njaru + 2];
        if (gollal == 0) {
            if (서술자 >= 0 && kuutoro.파일서술자닫기(서술자) < 0) ella_njaru("IOException: close failed");
            힙[waraango_njaru + 2] = -1; return;
        }
        if (서술자 < 0) { ella_njaru("IOException: stream closed"); return; }
        if (gollal == 1) {
            int 결과 = kuutoro.파일한바이트읽기(서술자);
            if (결과 < -1) ella_njaru("IOException: read failed"); else 넣기(결과 == 256 ? -1 : 결과, 1);
        } else if (kuutoro.파일한바이트쓰기(서술자, njaru) != 1) ella_njaru("IOException: write failed");
    }
    static void 함수호출(int joopirdu, int ginol) {
        if (joopirdu <= 0 || joopirdu >= 상종류.length || (상종류[joopirdu] != 10 && 상종류[joopirdu] != 11)) { ella_njaru("invalid method reference"); return; }
        int 소유 = fedde_innde_binndi(상가[joopirdu]), innde = 참조이름(상나[joopirdu]), formaa_njaru = 참조형식(상나[joopirdu]);
        if (juumre) return;
        if (기본호출(소유, innde, formaa_njaru, ginol)) return;
        if (말(소유, "java/io/FileInputStream") || 말(소유, "java/io/FileOutputStream")) {
            fiilde_waraango_noddude(소유, innde, formaa_njaru, ginol); return;
        }
        if (ginol == 184 && 말(소유, "java/lang/Integer") && 말(innde, "parseInt") && 말(formaa_njaru, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (ginol == 182 && 말(소유, "java/io/PrintStream") && (말(innde, "println") || 말(innde, "print"))) {
            int 형 = 0, njaru = 0;
            if (말(formaa_njaru, "(I)V")) { 형 = 1; njaru = 빼기(1); }
            else if (말(formaa_njaru, "(Z)V")) { 형 = 2; njaru = 빼기(1); }
            else if (말(formaa_njaru, "(C)V")) { 형 = 3; njaru = 빼기(1); }
            else if (말(formaa_njaru, "(Ljava/lang/String;)V")) { 형 = 4; njaru = 빼기(2); }
            else if (!말(formaa_njaru, "()V") || !말(innde, "println")) ella_njaru("unsupported print descriptor");
            if (빼기(2) != -1) ella_njaru("invalid PrintStream receiver");
            if (juumre) return;
            if (형 == 1) 자바도구.수쓰기(njaru);
            if (형 == 2) kuutoro.winndude(njaru == 0 ? "false" : "true");
            if (형 == 3) kuutoro.winndude_alkulal_njaru(njaru & 65535);
            if (형 == 4) winndude_binndi(njaru);
            if (말(innde, "println")) kuutoro.winndude_alkulal_njaru(10);
            return;
        }
        if (ginol == 182 && 말(소유, "java/lang/String")) {
            if (말(innde, "length") && 말(formaa_njaru, "()I")) {
                int 참조 = 빼기(2); if (huunde_njaru(참조, 1)) 넣기(힙[참조 + 1], 1); return;
            }
            if (말(innde, "charAt") && 말(formaa_njaru, "(I)C")) {
                int limtoore_sakkiinde_njaru = 빼기(1), 참조 = 빼기(2);
                if (huunde_njaru(참조, 1)) {
                    if (limtoore_sakkiinde_njaru < 0 || limtoore_sakkiinde_njaru >= 힙[참조 + 1]) ella_njaru("StringIndexOutOfBoundsException"); else 넣기(힙[참조 + 2 + limtoore_sakkiinde_njaru], 1);
                }
                return;
            }
        }
        if (말(소유, "java/lang/StringBuilder")) {
            if (ginol == 183 && 말(innde, "<init>") && 말(formaa_njaru, "()V")) { huunde_njaru(빼기(2), 4); return; }
            if (ginol == 182 && 말(innde, "toString") && 말(formaa_njaru, "()Ljava/lang/String;")) {
                int 참조 = 빼기(2); if (huunde_njaru(참조, 4)) 넣기(힙[참조 + 2] == 0 ? njaatigi_alkulal("") : 힙[참조 + 2], 2); return;
            }
            if (ginol == 182 && 말(innde, "append")) {
                int binndi = 0;
                if (말(formaa_njaru, "(I)Ljava/lang/StringBuilder;")) binndi = 수문자(빼기(1));
                else if (말(formaa_njaru, "(Z)Ljava/lang/StringBuilder;")) binndi = njaatigi_alkulal(빼기(1) == 0 ? "false" : "true");
                else if (말(formaa_njaru, "(C)Ljava/lang/StringBuilder;")) {
                    int njaru = 빼기(1); binndi = 할당(1, 1); if (!juumre) 힙[binndi + 2] = njaru & 65535;
                }
                else if (말(formaa_njaru, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { binndi = 빼기(2); if (binndi == 0) binndi = njaatigi_alkulal("null"); }
                else { ella_njaru("unsupported StringBuilder append"); return; }
                int 참조 = 빼기(2); if (!huunde_njaru(참조, 4) || !huunde_njaru(binndi, 1)) return;
                int 앞 = 힙[참조 + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], Caggal_njaru_njuuteendi = 힙[binndi + 1];
                int 새글 = 할당(1, 앞길이 + Caggal_njaru_njuuteendi); if (juumre) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < Caggal_njaru_njuuteendi; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[binndi + 2 + 수];
                힙[참조 + 2] = 새글; 넣기(참조, 2); return;
            }
        }
        int 종 = 종찾기(소유); if (종 < 0 || juumre) return;
        int fiilde_joopirdu = 함수찾기(종, innde, formaa_njaru);
        if (fiilde_joopirdu < 0) {
            for (int 문자값 = 종, 항목수 = 0; 문자값 >= 0 && 항목수 < 16; 항목수++, 문자값 = 부모종(문자값))
                if (말(종부모[문자값], "java/lang/Thread")) { 가닥호출(innde, formaa_njaru, ginol); return; }
            ella_njaru("NoSuchMethodError"); return;
        }
        if (((함수권한[fiilde_joopirdu] & 8) != 0) != (ginol == 184)) { ella_njaru("method static/instance mismatch"); return; }
        if (ginol == 184) { if (!ɓamtinde(함수주인[fiilde_joopirdu], taƴtinnde_yamiroore[taƴtinnde_joopirdu])) return; }
        else {
            int 읽는자리 = 틀스택[taƴtinnde_joopirdu] - 함수인수수[fiilde_joopirdu];
            if (읽는자리 < 0 || 스택형[taƴtinnde_joopirdu * 128 + 읽는자리] != 2) { ella_njaru("invalid method receiver"); return; }
            int 객체참조 = 스택값[taƴtinnde_joopirdu * 128 + 읽는자리];
            if (!객체유효(객체참조)) return;
            if (힙[객체참조] < 32 || !종포함(힙[객체참조] - 32, 소유)) { ella_njaru("method receiver type mismatch"); return; }
            if (ginol != 183) fiilde_joopirdu = 함수찾기(힙[객체참조] - 32, innde, formaa_njaru);
        }
        if (fiilde_joopirdu < 0 || (함수권한[fiilde_joopirdu] & 0x400) != 0) { ella_njaru("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((함수권한[fiilde_joopirdu] & 32) != 0) {
            if (ginol == 184) { int 문자값 = 함수주인[fiilde_joopirdu]; if (종잠금[문자값] == 0) 종잠금[문자값] = 할당(8, 0); 잠금참조 = 종잠금[문자값]; }
            else 잠금참조 = 스택값[taƴtinnde_joopirdu * 128 + 틀스택[taƴtinnde_joopirdu] - 함수인수수[fiilde_joopirdu]];
            if (!잠금얻기(잠금참조)) { if (!juumre) 틀위치[taƴtinnde_joopirdu] = taƴtinnde_yamiroore[taƴtinnde_joopirdu]; return; }
        }
        호출(fiilde_joopirdu); if (!juumre) 틀잠금[taƴtinnde_joopirdu] = 잠금참조;
    }
    static boolean 배열저장가능(int 배열참조, int keɓe_njaru) {
        if (keɓe_njaru == 0 || 배열원소[배열참조] == 0) return true;
        boolean 성공여부 = 배열원소[배열참조] == -1 ? (keɓe_njaru > 0 && keɓe_njaru < 힙끝 && 힙[keɓe_njaru] == 1) : 맞는객체(keɓe_njaru, 배열원소[배열참조]);
        if (!성공여부 && !juumre) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int 배열칸(int 참조, int limtoore_sakkiinde_njaru, int 형) {
        if (!huunde_njaru(참조, 형)) return 0;
        if (limtoore_sakkiinde_njaru < 0 || limtoore_sakkiinde_njaru >= 힙[참조 + 1]) { ella_njaru("ArrayIndexOutOfBoundsException"); return 0; }
        return 참조 + 2 + limtoore_sakkiinde_njaru;
    }
    static void 실행() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (juumre) { if (던진객체 != 0) 예외처리(); if (juumre || taƴtinnde_joopirdu < 현재가닥 * 32) break; }
            if (taƴtinnde_joopirdu < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!waylude_piilol()) break; 조각 = 100; }
            if (taƴtinnde_joopirdu == 0 && 종상태[시작종] != 2 && !ɓamtinde(시작종, 틀위치[taƴtinnde_joopirdu])) continue;
            if (taƴtinnde_joopirdu == 현재가닥 * 32 && 현재가닥 != 0 && (함수권한[틀함수[taƴtinnde_joopirdu]] & 32) != 0 && 틀잠금[taƴtinnde_joopirdu] == 0) {
                int 객체참조 = piilol_faandaare[현재가닥]; if (!잠금얻기(객체참조)) { if (juumre) break; continue; } 틀잠금[taƴtinnde_joopirdu] = 객체참조;
            }
            잠시수 = 0;
            if (--남음 == 0) { ella_njaru("instruction limit (500000)"); break; }
            int huutoraade = 틀위치[taƴtinnde_joopirdu]; taƴtinnde_yamiroore[taƴtinnde_joopirdu] = huutoraade; int njaru = 명바();
            if (juumre) break;
            if (njaru == 0) continue;
            if (njaru == 1) { 넣기(0, 2); continue; }
            if (njaru >= 2 && njaru <= 8) { 넣기(njaru - 3, 1); continue; }
            if (njaru == 16) { 넣기((byte)명바(), 1); continue; }
            if (njaru == 17) { 넣기((short)명짧(), 1); continue; }
            if (njaru == 18 || njaru == 19) {
                int 수 = 함수주인[틀함수[taƴtinnde_joopirdu]] * 512 + (njaru == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= 상종류.length) ella_njaru("invalid ldc constant");
                else if (상종류[수] == 3) 넣기(상가[수], 1);
                else if (상종류[수] == 8) 넣기(상문자(상가[수]), 2);
                else ella_njaru("unsupported ldc constant");
                continue;
            }
            if (njaru == 21 || njaru == 25) { 지역읽기(명바(), njaru == 21 ? 1 : 2); continue; }
            if (njaru >= 26 && njaru <= 29) { 지역읽기(njaru - 26, 1); continue; }
            if (njaru >= 42 && njaru <= 45) { 지역읽기(njaru - 42, 2); continue; }
            if (njaru == 54 || njaru == 58) { winndude_nokkuwal(명바(), njaru == 54 ? 1 : 2); continue; }
            if (njaru >= 59 && njaru <= 62) { winndude_nokkuwal(njaru - 59, 1); continue; }
            if (njaru >= 75 && njaru <= 78) { winndude_nokkuwal(njaru - 75, 2); continue; }
            if (njaru == 46 || njaru >= 50 && njaru <= 53) {
                int 항목자리 = 빼기(1), 객체참조 = 빼기(2), 분류코드 = njaru == 46 ? 2 : njaru == 50 ? 3 : njaru == 51 ? 20 : njaru == 52 ? 22 : 23;
                if (njaru == 51 && 객체참조 > 0 && 객체참조 < 힙끝 && 힙[객체참조] == 21) 분류코드 = 21;
                int 읽는자리 = 배열칸(객체참조, 항목자리, 분류코드); if (!juumre) 넣기(힙[읽는자리], njaru == 50 ? 2 : 1); continue;
            }
            if (njaru == 79 || njaru >= 83 && njaru <= 86) {
                int 항목참조 = 빼기(njaru == 83 ? 2 : 1), 항목자리 = 빼기(1), 객체참조 = 빼기(2), 분류코드 = njaru == 79 ? 2 : njaru == 83 ? 3 : njaru == 84 ? 20 : njaru == 85 ? 22 : 23;
                if (njaru == 84 && 객체참조 > 0 && 객체참조 < 힙끝 && 힙[객체참조] == 21) 분류코드 = 21;
                int 읽는자리 = 배열칸(객체참조, 항목자리, 분류코드);
                if (!juumre && 분류코드 == 3 && !배열저장가능(객체참조, 항목참조)) continue;
                if (!juumre) 힙[읽는자리] = 분류코드 == 20 ? (byte)항목참조 : 분류코드 == 21 ? 항목참조 & 1 : 분류코드 == 22 ? (char)항목참조 : 분류코드 == 23 ? (short)항목참조 : 항목참조;
                continue;
            }
            if (njaru >= 87 && njaru <= 95) { 스택명령(njaru); continue; }
            if (njaru == 96 || njaru == 100 || njaru == 104 || njaru == 108 || njaru == 112 || njaru == 120
                || njaru == 122 || njaru == 124 || njaru == 126 || njaru == 128 || njaru == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), 결과 = 0;
                if ((njaru == 108 || njaru == 112) && 나 == 0) { ella_njaru("ArithmeticException: / by zero"); continue; }
                if (njaru == 96) 결과 = 가 + 나;
                if (njaru == 100) 결과 = 가 - 나;
                if (njaru == 104) 결과 = 가 * 나;
                if (njaru == 108) 결과 = 가 / 나;
                if (njaru == 112) 결과 = 가 % 나;
                if (njaru == 120) 결과 = 가 << 나;
                if (njaru == 122) 결과 = 가 >> 나;
                if (njaru == 124) 결과 = 가 >>> 나;
                if (njaru == 126) 결과 = 가 & 나;
                if (njaru == 128) 결과 = 가 | 나;
                if (njaru == 130) 결과 = 가 ^ 나;
                넣기(결과, 1); continue;
            }
            if (njaru == 116) { 넣기(-빼기(1), 1); continue; }
            if (njaru == 132) {
                int nokkuwal_njaajeendi = 명바(), 증분 = (byte)명바(); 지역읽기(nokkuwal_njaajeendi, 1); 넣기(빼기(1) + 증분, 1); winndude_nokkuwal(nokkuwal_njaajeendi, 1); continue;
            }
            if (njaru >= 145 && njaru <= 147) {
                int 수 = 빼기(1); 넣기(njaru == 145 ? (byte)수 : njaru == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (njaru >= 153 && njaru <= 167 || njaru == 198 || njaru == 199) {
                int tiindaare_njaru = huutoraade + (short)명짧(); boolean 갈까 = njaru == 167;
                if (njaru >= 153 && njaru <= 158) {
                    int 수 = 빼기(1); 갈까 = njaru == 153 ? 수 == 0 : njaru == 154 ? 수 != 0 : njaru == 155 ? 수 < 0 : njaru == 156 ? 수 >= 0 : njaru == 157 ? 수 > 0 : 수 <= 0;
                } else if (njaru >= 159 && njaru <= 166) {
                    int 나 = 빼기(njaru >= 165 ? 2 : 1), 가 = 빼기(njaru >= 165 ? 2 : 1);
                    갈까 = njaru == 159 || njaru == 165 ? 가 == 나 : njaru == 160 || njaru == 166 ? 가 != 나 : njaru == 161 ? 가 < 나 : njaru == 162 ? 가 >= 나 : njaru == 163 ? 가 > 나 : 가 <= 나;
                } else if (njaru == 198 || njaru == 199) { int 수 = 빼기(2); 갈까 = njaru == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) dirtinde_njaru(tiindaare_njaru); continue;
            }
            if (njaru == 172 || njaru == 176 || njaru == 177) { 반환(njaru == 172 ? 1 : njaru == 176 ? 2 : 0); continue; }
            if (njaru >= 178 && njaru <= 181) { 필드호출(명상수(), njaru, huutoraade); continue; }
            if (njaru >= 182 && njaru <= 185) {
                int 부호값 = 명상수();
                if (njaru == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { ella_njaru("invalid invokeinterface operands"); continue; } }
                함수호출(부호값, njaru); continue;
            }
            if (njaru == 187) { 새객체(fedde_innde_binndi(명상수()), huutoraade); continue; }
            if (njaru == 188 || njaru == 189) {
                int 분류코드 = 3, komponal = 0;
                if (njaru == 188) { int 임시값 = 명바(); 분류코드 = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else komponal = fedde_innde_binndi(명상수());
                if (분류코드 == 0) { ella_njaru("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), 객체참조 = 할당(분류코드, 유효길이); if (!juumre) 배열원소[객체참조] = komponal; 넣기(객체참조, 2); continue;
            }
            if (njaru == 190) {
                int 객체참조 = 빼기(2);
                if (객체유효(객체참조)) { int 비교자리 = 힙[객체참조]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) ella_njaru("not an array"); else 넣기(힙[객체참조 + 1], 1); }
                continue;
            }
            if (njaru == 191) {
                int 객체참조 = 빼기(2); if (객체유효(객체참조)) { if (힙[객체참조] != 9) ella_njaru("athrow requires supported Throwable"); else { 던진객체 = 객체참조; juumre = true; } }
                continue;
            }
            if (njaru == 192 || njaru == 193) {
                int 이름상수 = fedde_innde_binndi(명상수()), 객체참조 = 빼기(2); boolean 일치여부 = 맞는객체(객체참조, 이름상수);
                if (njaru == 193) 넣기(객체참조 != 0 && 일치여부 ? 1 : 0, 1);
                else { if (!일치여부 && !juumre) ella_njaru("ClassCastException"); 넣기(객체참조, 2); }
                continue;
            }
            if (njaru == 170 || njaru == 171) {
                int 읽는자리 = huutoraade + 1, fiilde_joopirdu = 틀함수[taƴtinnde_joopirdu], 키참조 = 빼기(1);
                while ((읽는자리 - 함수시작[fiilde_joopirdu]) % 4 != 0) 읽는자리++;
                int faandaare_ñiiɓirde = 위치정수(읽는자리);
                if (njaru == 170) { int 낮은값 = 위치정수(읽는자리 + 4), 높은값 = 위치정수(읽는자리 + 8); if (키참조 >= 낮은값 && 키참조 <= 높은값) faandaare_ñiiɓirde = 위치정수(읽는자리 + 12 + (키참조 - 낮은값) * 4); }
                else { int 총수 = 위치정수(읽는자리 + 4); for (int kowal_joopirdu = 0; kowal_joopirdu < 총수; kowal_joopirdu++) if (위치정수(읽는자리 + 8 + kowal_joopirdu * 8) == 키참조) faandaare_ñiiɓirde = 위치정수(읽는자리 + 12 + kowal_joopirdu * 8); }
                dirtinde_njaru(huutoraade + faandaare_ñiiɓirde); continue;
            }
            if (njaru == 200) { dirtinde_njaru(huutoraade + 위치정수(huutoraade + 1)); continue; }
            if (njaru == 194 || njaru == 195) {
                int 객체참조 = 빼기(2);
                if (njaru == 195) 잠금풀기(객체참조);
                else if (!잠금얻기(객체참조) && !juumre) { 넣기(객체참조, 2); 틀위치[taƴtinnde_joopirdu] = huutoraade; }
                continue;
            }
            if (njaru == 196) {
                int 명령코드 = 명바(), 항목자리 = 명짧();
                if (명령코드 == 21 || 명령코드 == 25) 지역읽기(항목자리, 명령코드 == 21 ? 1 : 2);
                else if (명령코드 == 54 || 명령코드 == 58) winndude_nokkuwal(항목자리, 명령코드 == 54 ? 1 : 2);
                else if (명령코드 == 132) { int 변화량 = (short)명짧(); 지역읽기(항목자리, 1); 넣기(빼기(1) + 변화량, 1); winndude_nokkuwal(항목자리, 1); }
                else ella_njaru("unsupported wide opcode");
                continue;
            }
            ella_njaru("unsupported bytecode");
        }
    }
    static int 종찾기(int innde) {
        for (int kowal_joopirdu = 0; kowal_joopirdu < 종수; kowal_joopirdu++) if (종이름[kowal_joopirdu] != 0 && 같은말(종이름[kowal_joopirdu], innde)) return kowal_joopirdu;
        return 종적재(상문자(innde));
    }
    static int 종적재(int innde_ɓoggol) {
        if (!huunde_njaru(innde_ɓoggol, 1)) return -1;
        int njuuteendi_njaru = 힙[innde_ɓoggol + 1];
        if (njuuteendi_njaru < 1 || njuuteendi_njaru > 505 || 종수 == 16) { ella_njaru("class name/count limit"); return -1; }
        for (int kowal_joopirdu = 0; kowal_joopirdu < njuuteendi_njaru; kowal_joopirdu++) { int 문자값 = 힙[innde_ɓoggol + 2 + kowal_joopirdu]; fiilde_innde_binndi[kowal_joopirdu] = 문자값 == '/' ? '.' : 문자값; }
        fiilde_innde_binndi[njuuteendi_njaru] = '.'; fiilde_innde_binndi[njuuteendi_njaru + 1] = 'c'; fiilde_innde_binndi[njuuteendi_njaru + 2] = 'l'; fiilde_innde_binndi[njuuteendi_njaru + 3] = 'a'; fiilde_innde_binndi[njuuteendi_njaru + 4] = 's'; fiilde_innde_binndi[njuuteendi_njaru + 5] = 's'; fiilde_innde_binndi[njuuteendi_njaru + 6] = 0;
        int waylude_etannde = kuutoro.파일읽기(fiilde_innde_binndi, 임시파일);
        if (waylude_etannde < 0) { ella_njaru("ClassNotFoundException"); return -1; }
        int 종 = 종수++; 종크기[종] = waylude_etannde;
        for (int kowal_joopirdu = 0; kowal_joopirdu < waylude_etannde; kowal_joopirdu++) fiilde[종 * 16384 + kowal_joopirdu] = 임시파일[kowal_joopirdu];
        클래스읽기(종); if (juumre) return -1;
        int laatii_keɓe = 상문자(종이름[종]);
        if (!글같음(laatii_keɓe, innde_ɓoggol, true)) { ella_njaru("class name does not match file"); return -1; }
        int 부모 = 종부모[종];
        if (부모 != 0 && !말(부모, "java/lang/Object") && !말(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = 종찾기(부모);
            if (juumre || 위 < 0) return -1;
            int 읽는자리 = 위, 단계수 = 0;
            while (읽는자리 >= 0 && 단계수++ < 16) {
                if (읽는자리 == 종) { ella_njaru("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int fiilde_joopirdu = 0; fiilde_joopirdu < 칸수; fiilde_joopirdu++) if (칸주인[fiilde_joopirdu] == 종 && (칸권한[fiilde_joopirdu] & 8) == 0) 칸위치[fiilde_joopirdu] += 시작변위;
            종칸수[종] += 시작변위;
        }
        return 종;
    }
    static int 부모종(int 종) {
        int innde = 종부모[종];
        for (int kowal_joopirdu = 0; kowal_joopirdu < 종수; kowal_joopirdu++) if (innde != 0 && 종이름[kowal_joopirdu] != 0 && 같은말(종이름[kowal_joopirdu], innde)) return kowal_joopirdu;
        return -1;
    }
    static int 함수찾기(int 종, int innde, int formaa_njaru) {
        for (int 깊이 = 0; 종 >= 0 && 깊이 < 16; 깊이++, 종 = 부모종(종)) {
            for (int kowal_joopirdu = 0; kowal_joopirdu < 함수수; kowal_joopirdu++) if (함수주인[kowal_joopirdu] == 종 && 같은말(함수명[kowal_joopirdu], innde) && 같은말(함수형[kowal_joopirdu], formaa_njaru)) return kowal_joopirdu;
        }
        return -1;
    }
    static int 이름함수(int 종, String innde, String formaa_njaru) {
        for (int 깊이 = 0; 종 >= 0 && 깊이 < 16; 깊이++, 종 = 부모종(종))
            for (int kowal_joopirdu = 0; kowal_joopirdu < 함수수; kowal_joopirdu++) if (함수주인[kowal_joopirdu] == 종 && 말(함수명[kowal_joopirdu], innde) && 말(함수형[kowal_joopirdu], formaa_njaru)) return kowal_joopirdu;
        return -1;
    }
    static int 형종류(int innde) { return fiilde[상가[innde]] == 'L' || fiilde[상가[innde]] == '[' ? 2 : 1; }
    static boolean ɓamtinde(int 종, int ginol_huɓɓude) {
        if (종 < 0 || juumre) return false;
        if (종상태[종] == 3) { ella_njaru("NoClassDefFoundError: initialization failed"); return false; }
        if (종상태[종] == 1 && fedde_piilol[종] != 현재가닥) { 틀위치[taƴtinnde_joopirdu] = ginol_huɓɓude; 바꿈요청 = true; return false; }
        if (종상태[종] != 0) return true;
        int 위 = 부모종(종);
        if (위 >= 0 && !ɓamtinde(위, ginol_huɓɓude)) return false;
        종상태[종] = 1; fedde_piilol[종] = 현재가닥;
        if (종초기화[종] != 0) {
            틀위치[taƴtinnde_joopirdu] = ginol_huɓɓude;
            호출(종초기화[종] - 1); if (!juumre) ɓamtinde_taƴtinnde[taƴtinnde_joopirdu] = 종 + 1;
            return false;
        }
        종상태[종] = 2; return true;
    }
    static void 필드호출(int joopirdu, int ginol, int huutoraade) {
        if (!상검사(joopirdu, 9)) return;
        int 소유 = fedde_innde_binndi(상가[joopirdu]), innde = 참조이름(상나[joopirdu]), formaa_njaru = 참조형식(상나[joopirdu]);
        if (말(소유, "java/lang/System") && (말(innde, "out") || 말(innde, "err")) && 말(formaa_njaru, "Ljava/io/PrintStream;") && ginol == 178) { 넣기(-1, 2); return; }
        int 종 = 종찾기(소유); if (종 < 0 || juumre) return;
        int 찾음 = -1;
        for (int 읽는자리 = 종, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int fiilde_joopirdu = 0; fiilde_joopirdu < 칸수; fiilde_joopirdu++) if (칸주인[fiilde_joopirdu] == 읽는자리 && 같은말(칸이름[fiilde_joopirdu], innde) && 같은말(칸형[fiilde_joopirdu], formaa_njaru)) 찾음 = fiilde_joopirdu;
        if (찾음 < 0) { ella_njaru("NoSuchFieldError"); return; }
        boolean ñiiɓ_njaru = ginol == 178 || ginol == 179;
        if (ñiiɓ_njaru != ((칸권한[찾음] & 8) != 0)) { ella_njaru("field static/instance mismatch"); return; }
        if (ñiiɓ_njaru && !ɓamtinde(칸주인[찾음], huutoraade)) return;
        int 형 = 형종류(formaa_njaru), njaru = 0;
        if (ginol == 179 || ginol == 181) njaru = 빼기(형);
        if (ñiiɓ_njaru) { if (ginol == 178) 넣기(칸값[찾음], 형); else if (!juumre) 칸값[찾음] = njaru; return; }
        int 객체참조 = 빼기(2);
        if (!객체유효(객체참조)) return;
        if (힙[객체참조] < 32 || !종포함(힙[객체참조] - 32, 소유)) { ella_njaru("field receiver type mismatch"); return; }
        int 보관칸 = 객체참조 + 2 + 칸위치[찾음];
        if (ginol == 180) 넣기(힙[보관칸], 형);
        else if (!juumre) { 힙[보관칸] = njaru; 힙참조[보관칸] = 형 == 2 ? 1 : 0; }
    }
    static boolean 종포함(int 종, int innde) {
        for (int 중첩깊이 = 0; 종 >= 0 && 중첩깊이 < 16; 중첩깊이++, 종 = 부모종(종)) {
            if (같은말(종이름[종], innde) || (종부모[종] != 0 && 같은말(종부모[종], innde))) return true;
            for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[종]; 안쪽자리++) if (같은말(fedde_jokkondirgal[종 * 16 + 안쪽자리], innde)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int oktee_keɓe, boolean laawol) {
        if (첫값 == oktee_keɓe) return true;
        if (첫값 <= 0 || oktee_keɓe <= 0 || 힙[첫값] != 1 || 힙[oktee_keɓe] != 1 || 힙[첫값 + 1] != 힙[oktee_keɓe + 1]) return false;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 힙[첫값 + 1]; kowal_joopirdu++) {
            int 가로좌표 = 힙[첫값 + 2 + kowal_joopirdu], 세로좌표 = 힙[oktee_keɓe + 2 + kowal_joopirdu];
            if (laawol) { if (가로좌표 == '.') 가로좌표 = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (가로좌표 != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int 객체참조) {
        if (객체참조 == 0) { ella_njaru("NullPointerException"); return false; }
        if (객체참조 < 1 || 객체참조 >= 힙끝 || 힙폭[객체참조] < 2 || 힙[객체참조] == 0) { ella_njaru("invalid object reference"); return false; }
        return true;
    }
    static void suurde_njaru(int 객체참조) {
        if (객체참조 > 0 && 객체참조 < 힙끝 && 힙폭[객체참조] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = 객체참조;
    }
    static void hollirde_njaru(int 객체참조) {
        if (객체참조 > 0 && 객체참조 < 힙끝 && 힙폭[객체참조] >= 2 && 힙[객체참조] != 0 && 힙표시[객체참조] == 0) {
            힙표시[객체참조] = 1; 표시대기[표시수++] = 객체참조;
        }
    }
    static void 수거() {
        표시수 = 0; 수거횟수++;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) 힙표시[검사자리] = 0;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 문자열참조.length; kowal_joopirdu++) hollirde_njaru(문자열참조[kowal_joopirdu]);
        for (int kowal_joopirdu = 0; kowal_joopirdu < 칸수; kowal_joopirdu++) if ((칸권한[kowal_joopirdu] & 8) != 0 && 형종류(칸형[kowal_joopirdu]) == 2) hollirde_njaru(칸값[kowal_joopirdu]);
        for (int 임시값 = 0; 임시값 < 가닥수; 임시값++) {
            hollirde_njaru(piilol_huunde[임시값]); hollirde_njaru(piilol_faandaare[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? taƴtinnde_joopirdu : piilol_taƴtinnde[임시값];
            for (int fiilde_joopirdu = 임시값 * 32; fiilde_joopirdu <= 꼭대기자리; fiilde_joopirdu++) {
                for (int 안쪽자리 = 0; 안쪽자리 < 함수지역[틀함수[fiilde_joopirdu]]; 안쪽자리++) if (지역형[fiilde_joopirdu * 128 + 안쪽자리] == 2) hollirde_njaru(nokkuwal_njaru[fiilde_joopirdu * 128 + 안쪽자리]);
                for (int 안쪽자리 = 0; 안쪽자리 < 틀스택[fiilde_joopirdu]; 안쪽자리++) if (스택형[fiilde_joopirdu * 128 + 안쪽자리] == 2) hollirde_njaru(스택값[fiilde_joopirdu * 128 + 안쪽자리]);
            }
        }
        for (int kowal_joopirdu = 0; kowal_joopirdu < 화면참조.length; kowal_joopirdu++) hollirde_njaru(화면참조[kowal_joopirdu]);
        for (int kowal_joopirdu = 0; kowal_joopirdu < 나중수; kowal_joopirdu++) hollirde_njaru(나중실행[kowal_joopirdu]);
        for (int kowal_joopirdu = 0; kowal_joopirdu < 정수저장.length; kowal_joopirdu++) hollirde_njaru(정수저장[kowal_joopirdu]);
        for (int kowal_joopirdu = 0; kowal_joopirdu < 종수; kowal_joopirdu++) hollirde_njaru(종잠금[kowal_joopirdu]);
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (잠금깊이[검사자리] > 0) hollirde_njaru(검사자리);
        hollirde_njaru(던진객체);
        for (int kowal_joopirdu = 0; kowal_joopirdu < 잠시수; kowal_joopirdu++) hollirde_njaru(잠시참조[kowal_joopirdu]);
        while (표시수 > 0) {
            int 객체참조 = 표시대기[--표시수], 분류코드 = 힙[객체참조];
            for (int kowal_joopirdu = 객체참조 + 2; kowal_joopirdu < 객체참조 + 힙폭[객체참조]; kowal_joopirdu++) if (분류코드 == 3 || 분류코드 == 4 || 힙참조[kowal_joopirdu] != 0) hollirde_njaru(힙[kowal_joopirdu]);
        }
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙표시[검사자리] == 0) 힙[검사자리] = 0;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙[검사자리] == 0) {
            while (검사자리 + 힙폭[검사자리] < 힙끝 && 힙[검사자리 + 힙폭[검사자리]] == 0) { int 다음자리 = 검사자리 + 힙폭[검사자리]; 힙폭[검사자리] += 힙폭[다음자리]; 힙폭[다음자리] = 0; }
            if (검사자리 + 힙폭[검사자리] == 힙끝) { 힙끝 = 검사자리; break; }
        }
    }
    static int 새기억(int 종류, int njuuteendi_njaru) {
        if (njuuteendi_njaru < 0) { ella_njaru("NegativeArraySizeException"); return 0; }
        if (njuuteendi_njaru > 힙.length - 3) { ella_njaru("object heap exhausted"); return 0; }
        int 필요수 = njuuteendi_njaru + 2, 객체참조 = 0;
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
        if (객체참조 == 0) { ella_njaru("object heap exhausted"); return 0; }
        for (int kowal_joopirdu = 0; kowal_joopirdu < 필요수; kowal_joopirdu++) { 힙[객체참조 + kowal_joopirdu] = 0; 힙참조[객체참조 + kowal_joopirdu] = 0; 힙폭[객체참조 + kowal_joopirdu] = 0; }
        배열원소[객체참조] = 0;
        힙폭[객체참조] = 필요수; 힙[객체참조] = 종류; 힙[객체참조 + 1] = njuuteendi_njaru; suurde_njaru(객체참조); return 객체참조;
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
    static int 예외상수(int innde) {
        for (int kowal_joopirdu = 1; kowal_joopirdu <= 41; kowal_joopirdu++) if (말(innde, 예외이름(kowal_joopirdu))) return kowal_joopirdu;
        return 0;
    }
    static String 예외이름(int konte_njaru) {
        if (konte_njaru == 40) return "java/lang/InterruptedException";
        if (konte_njaru == 41) return "한국어/자체/대기중단예외";
        if (konte_njaru == 39) return "java/net/SocketException";
        if (konte_njaru == 20) return "한국어/자체/예외";
        if (konte_njaru == 21) return "한국어/자체/실행예외";
        if (konte_njaru == 22) return "한국어/자체/입출력예외";
        if (konte_njaru == 23) return "한국어/자체/대기시간초과예외";
        if (konte_njaru == 24) return "한국어/자체/주소확인예외";
        if (konte_njaru == 25) return "한국어/자체/파일없음예외";
        if (konte_njaru == 26) return "한국어/자체/통신예외";
        if (konte_njaru == 27) return "한국어/자체/잘못된인수예외";
        if (konte_njaru == 28) return "한국어/자체/숫자형식예외";
        if (konte_njaru == 29) return "한국어/자체/범위예외";
        if (konte_njaru == 30) return "한국어/자체/배열범위예외";
        if (konte_njaru == 31) return "한국어/자체/문자열범위예외";
        if (konte_njaru == 32) return "한국어/자체/빈참조예외";
        if (konte_njaru == 33) return "한국어/자체/산술예외";
        if (konte_njaru == 34) return "한국어/자체/상태예외";
        if (konte_njaru == 35) return "한국어/자체/형변환예외";
        if (konte_njaru == 36) return "한국어/자체/음수배열크기예외";
        if (konte_njaru == 37) return "한국어/자체/배열저장예외";
        if (konte_njaru == 38) return "한국어/자체/가닥상태예외";
        if (konte_njaru == 1) return "java/lang/Throwable"; if (konte_njaru == 2) return "java/lang/Exception";
        if (konte_njaru == 3) return "java/lang/RuntimeException"; if (konte_njaru == 4) return "java/lang/ArithmeticException";
        if (konte_njaru == 5) return "java/lang/NullPointerException"; if (konte_njaru == 6) return "java/lang/IndexOutOfBoundsException";
        if (konte_njaru == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (konte_njaru == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (konte_njaru == 9) return "java/lang/IllegalArgumentException"; if (konte_njaru == 10) return "java/lang/NumberFormatException";
        if (konte_njaru == 11) return "java/io/IOException"; if (konte_njaru == 12) return "java/io/FileNotFoundException";
        if (konte_njaru == 17) return "java/lang/ArrayStoreException";
        if (konte_njaru == 18) return "java/net/UnknownHostException";
        if (konte_njaru == 19) return "java/net/SocketTimeoutException";
        if (konte_njaru == 16) return "java/lang/IllegalThreadStateException";
        if (konte_njaru == 13) return "java/lang/IllegalStateException"; if (konte_njaru == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int konte_njaru) {
        if (konte_njaru == 40) return 2;
        if (konte_njaru == 41) return 40;
        if (konte_njaru == 39) return 11;
        if (konte_njaru == 1) return 0;
        if (konte_njaru == 2) return 1;
        if (konte_njaru == 3) return 2;
        if (konte_njaru == 4) return 3;
        if (konte_njaru == 5) return 3;
        if (konte_njaru == 6) return 3;
        if (konte_njaru == 7) return 6;
        if (konte_njaru == 8) return 6;
        if (konte_njaru == 9) return 3;
        if (konte_njaru == 10) return 9;
        if (konte_njaru == 11) return 2;
        if (konte_njaru == 12) return 11;
        if (konte_njaru == 13) return 3;
        if (konte_njaru == 14) return 3;
        if (konte_njaru == 15) return 3;
        if (konte_njaru == 16) return 9;
        if (konte_njaru == 17) return 3;
        if (konte_njaru == 18) return 11;
        if (konte_njaru == 19) return 11;
        if (konte_njaru == 20) return 2;
        if (konte_njaru == 21) return 3;
        if (konte_njaru == 22) return 11;
        if (konte_njaru == 23) return 22;
        if (konte_njaru == 24) return 22;
        if (konte_njaru == 25) return 22;
        if (konte_njaru == 26) return 22;
        if (konte_njaru == 27) return 9;
        if (konte_njaru == 28) return 27;
        if (konte_njaru == 29) return 6;
        if (konte_njaru == 30) return 29;
        if (konte_njaru == 31) return 29;
        if (konte_njaru == 32) return 5;
        if (konte_njaru == 33) return 4;
        if (konte_njaru == 34) return 13;
        if (konte_njaru == 35) return 14;
        if (konte_njaru == 36) return 15;
        if (konte_njaru == 37) return 17;
        if (konte_njaru == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int laatii_njaru, int 요구값) {
        for (int 깊이 = 0; laatii_njaru != 0 && 깊이 < 16; 깊이++, laatii_njaru = 예외부모(laatii_njaru))
            if (laatii_njaru == 요구값) return true;
        return false;
    }
    static void 예외던짐(int konte_njaru, String 안내참조) {
        int 객체참조 = 새기억(9, 2); if (juumre) return;
        힙[객체참조 + 2] = konte_njaru; 힙[객체참조 + 3] = njaatigi_alkulal(안내참조); 힙참조[객체참조 + 3] = 1;
        던진객체 = 객체참조; juumre = true;
    }
    static boolean 맞는객체(int 객체참조, int innde) {
        if (객체참조 == 0) return true;
        if (!객체유효(객체참조)) return false;
        int 분류코드 = 힙[객체참조];
        if (말(innde, "java/lang/Object")) return true;
        if (분류코드 >= 32) return 종포함(분류코드 - 32, innde);
        if (분류코드 == 9) { int faandaare_ñiiɓirde = 예외상수(innde); return faandaare_ñiiɓirde != 0 && 예외포함(힙[객체참조 + 2], faandaare_ñiiɓirde); }
        if (분류코드 == 1) return 말(innde, "java/lang/String") || 말(innde, "java/lang/CharSequence");
        if (분류코드 == 4) return 말(innde, "java/lang/StringBuilder") || 말(innde, "java/lang/CharSequence");
        if (분류코드 == 10) return 말(innde, "java/util/ArrayList") || 말(innde, "java/util/List");
        if (분류코드 == 11) return 말(innde, "java/util/HashMap") || 말(innde, "java/util/Map");
        if (분류코드 == 12) return 말(innde, "java/lang/Integer") || 말(innde, "java/lang/Number");
        if (분류코드 >= 24 && 분류코드 <= 28 && 힙[객체참조 + 13] != 0) return 한국어화면종(innde) == 분류코드 || 말(innde, "한국어/자체/화면구성요소");
        if (분류코드 >= 24 && 분류코드 <= 28) return (한국어화면종(innde) == 0 && 화면종(innde) == 분류코드) || 말(innde, "java/awt/Component") || 말(innde, "java/awt/Container") || 말(innde, "javax/swing/JComponent");
        if (분류코드 == 29) return 말(innde, 힙[객체참조 + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (분류코드 == 30) return 말(innde, "java/awt/FlowLayout") || 말(innde, "java/awt/LayoutManager");
        if (분류코드 == 17) return 말(innde, "java/net/Socket");
        if (분류코드 == 18) return 말(innde, "java/net/ServerSocket");
        if (분류코드 == 19) return 말(innde, 힙[객체참조 + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (분류코드 == 14) return 말(innde, "java/net/InetAddress");
        if (분류코드 == 15) return 말(innde, "java/net/DatagramSocket");
        if (분류코드 == 16) return 말(innde, "java/net/DatagramPacket");
        if (분류코드 == 13) return 말(innde, 힙[객체참조 + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (분류코드 == 2) return 말(innde, "[I"); if (분류코드 == 20) return 말(innde, "[B"); if (분류코드 == 21) return 말(innde, "[Z");
        if (분류코드 == 22) return 말(innde, "[C"); if (분류코드 == 23) return 말(innde, "[S");
        if (분류코드 != 3) return false;
        if (말(innde, "[Ljava/lang/Object;")) return true;
        int komponal = 배열원소[객체참조];
        if (komponal == -1) return 말(innde, "[Ljava/lang/String;") || 말(innde, "[Ljava/lang/CharSequence;");
        if (komponal == 0) return false;
        if (배열종비교(komponal, innde)) return true;
        if ((말(komponal, "java/lang/String") || 말(komponal, "java/lang/StringBuilder")) && 말(innde, "[Ljava/lang/CharSequence;")) return true;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 종수; kowal_joopirdu++) if (같은말(종이름[kowal_joopirdu], komponal)) {
            for (int 문자값 = kowal_joopirdu, 중첩깊이 = 0; 문자값 >= 0 && 중첩깊이 < 16; 중첩깊이++, 문자값 = 부모종(문자값)) {
                if (배열종비교(종부모[문자값], innde)) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[문자값]; 안쪽자리++) if (배열종비교(fedde_jokkondirgal[문자값 * 16 + 안쪽자리], innde)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int 이름상수, int 형식참조) {
        int 검사자리 = 상가[형식참조], 항목수 = 상나[형식참조];
        if (이름상수 == 0 || 항목수 < 4 || fiilde[검사자리] != '[' || fiilde[검사자리 + 1] != 'L' || fiilde[검사자리 + 항목수 - 1] != ';' || 상나[이름상수] != 항목수 - 3) return false;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 항목수 - 3; kowal_joopirdu++) if (fiilde[상가[이름상수] + kowal_joopirdu] != fiilde[검사자리 + 2 + kowal_joopirdu]) return false;
        return true;
    }
    static void 예외처리() {
        if (던진객체 == 0) return;
        juumre = false;
        while (taƴtinnde_joopirdu >= 현재가닥 * 32) {
            int fiilde_joopirdu = 틀함수[taƴtinnde_joopirdu], 읽는자리 = taƴtinnde_yamiroore[taƴtinnde_joopirdu];
            for (int kowal_joopirdu = 0; kowal_joopirdu < 잡기수; kowal_joopirdu++) if (잡기함수[kowal_joopirdu] == fiilde_joopirdu && 읽는자리 >= 잡기시작[kowal_joopirdu] && 읽는자리 < 잡기끝[kowal_joopirdu]
                && (잡기종[kowal_joopirdu] == 0 || 맞는객체(던진객체, 잡기종[kowal_joopirdu]))) {
                틀위치[taƴtinnde_joopirdu] = 잡기위치[kowal_joopirdu]; 틀스택[taƴtinnde_joopirdu] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (ɓamtinde_taƴtinnde[taƴtinnde_joopirdu] != 0) 종상태[ɓamtinde_taƴtinnde[taƴtinnde_joopirdu] - 1] = 3;
            if (틀잠금[taƴtinnde_joopirdu] != 0) { 잠금풀기(틀잠금[taƴtinnde_joopirdu]); 틀잠금[taƴtinnde_joopirdu] = 0; }
            taƴtinnde_joopirdu--;
        }
        kuutoro.winndude("Uncaught ");
        if (힙[던진객체] == 9) { kuutoro.winndude(예외이름(힙[던진객체 + 2])); kuutoro.winndude(": "); winndude_binndi(힙[던진객체 + 3]); }
        else kuutoro.winndude("user exception");
        kuutoro.winndude_alkulal_njaru(10); 던진객체 = 0; juumre = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void 스택명령(int 명령코드) {
        int 첫값 = 빼기(0), 첫형식 = 반환형;
        if (명령코드 == 87) return;
        if (명령코드 == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int oktee_keɓe = 빼기(0), 둘째형식 = 반환형;
        if (명령코드 == 88) return;
        if (명령코드 == 90) { 넣기(첫값, 첫형식); 넣기(oktee_keɓe, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 92) { 넣기(oktee_keɓe, 둘째형식); 넣기(첫값, 첫형식); 넣기(oktee_keɓe, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 95) { 넣기(첫값, 첫형식); 넣기(oktee_keɓe, 둘째형식); return; }
        int 문자값 = 빼기(0), 셋째형식 = 반환형;
        if (명령코드 == 91) { 넣기(첫값, 첫형식); 넣기(문자값, 셋째형식); 넣기(oktee_keɓe, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 93) { 넣기(oktee_keɓe, 둘째형식); 넣기(첫값, 첫형식); 넣기(문자값, 셋째형식); 넣기(oktee_keɓe, 둘째형식); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = 반환형;
        넣기(oktee_keɓe, 둘째형식); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(문자값, 셋째형식); 넣기(oktee_keɓe, 둘째형식); 넣기(첫값, 첫형식);
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
            int 문자값 = 종찾기(이름상수); if (문자값 < 0 || juumre || !ɓamtinde(문자값, 시작점)) return;
            분류코드 = 32 + 문자값; 유효길이 = 종칸수[문자값];
        }
        int 객체참조 = 할당(분류코드, 유효길이); if (juumre) return;
        if (분류코드 == 13 && 말(이름상수, "한국어/자체/작업가닥")) 힙[객체참조 + 3] = 1;
        if (분류코드 >= 24 && 분류코드 <= 28 && 한국어화면종(이름상수) != 0) 힙[객체참조 + 13] = 1;
        if (분류코드 == 5 || 분류코드 == 6 || 분류코드 == 15 || 분류코드 == 17 || 분류코드 == 18) 힙[객체참조 + 2] = -1;
        if (분류코드 == 9) 힙[객체참조 + 2] = 예외참조;
        넣기(객체참조, 2);
    }
    static boolean 값같음(int 첫값, int oktee_keɓe) {
        if (첫값 == oktee_keɓe) return true;
        if (첫값 == 0 || oktee_keɓe == 0 || 첫값 < 0 || oktee_keɓe < 0 || 첫값 >= 힙끝 || oktee_keɓe >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[oktee_keɓe] == 1) return 글같음(첫값, oktee_keɓe, false);
        return 힙[첫값] == 12 && 힙[oktee_keɓe] == 12 && 힙[첫값 + 2] == 힙[oktee_keɓe + 2];
    }
    static int 글조각(int 객체참조, int 시작자리, int 끝자리) {
        if (!huunde_njaru(객체참조, 1)) return 0;
        if (시작자리 < 0 || 끝자리 < 시작자리 || 끝자리 > 힙[객체참조 + 1]) { ella_njaru("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = 할당(1, 끝자리 - 시작자리); if (juumre) return 0;
        for (int kowal_joopirdu = 시작자리; kowal_joopirdu < 끝자리; kowal_joopirdu++) 힙[반환값 + 2 + kowal_joopirdu - 시작자리] = 힙[객체참조 + 2 + kowal_joopirdu];
        return 반환값;
    }
    static int jokkunde_binndi(int 첫값, int oktee_keɓe) {
        if (!huunde_njaru(첫값, 1) || !huunde_njaru(oktee_keɓe, 1)) return 0;
        int 항목수 = 힙[첫값 + 1], 함수번호 = 힙[oktee_keɓe + 1], 반환값 = 할당(1, 항목수 + 함수번호); if (juumre) return 0;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 항목수; kowal_joopirdu++) 힙[반환값 + 2 + kowal_joopirdu] = 힙[첫값 + 2 + kowal_joopirdu];
        for (int kowal_joopirdu = 0; kowal_joopirdu < 함수번호; kowal_joopirdu++) 힙[반환값 + 2 + 항목수 + kowal_joopirdu] = 힙[oktee_keɓe + 2 + kowal_joopirdu];
        return 반환값;
    }
    static boolean 기본호출(int 소유종, int 이름상수, int 서술상수, int 명령코드) {
        if (말(소유종, "한국어/자체/실행인수") && 명령코드 == 184) {
            if (말(이름상수, "개수") && 말(서술상수, "()I")) { 넣기(kuutoro.인수개수() - 1, 1); return true; }
            if (말(이름상수, "binndi") && 말(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= kuutoro.인수개수() - 1) 예외던짐(29, "실행 인수 범위를 벗어났습니다");
                else 넣기(njaatigi_alkulal(kuutoro.인수(순번 + 1)), 2);
                return true;
            }
            ella_njaru("지원하지 않는 한국어 실행 인수 호출"); return true;
        }
        if (말(소유종, "한국어/자체/작업가닥")) { Yuɓɓo_golle_piilol(이름상수, 서술상수, 명령코드, true); return true; }
        if (한국어화면소유(소유종)) { 한국어화면호출(소유종, 이름상수, 서술상수, 명령코드); return true; }
        if (화면소유(소유종)) { 화면호출(소유종, 이름상수, 서술상수, 명령코드); return true; }
        if (말(소유종, "java/net/Socket") || 말(소유종, "java/net/ServerSocket") || 말(소유종, "java/io/InputStream") || 말(소유종, "java/io/OutputStream")) { 흐름호출(소유종, 이름상수, 서술상수, 명령코드); return true; }
        if (말(소유종, "한국어/자체/aaluude_njaru") && 명령코드 == 184) {
            if (말(이름상수, "화면너비") && 말(서술상수, "()I")) { 넣기(kuutoro.화면너비(), 1); return true; }
            if (말(이름상수, "화면높이") && 말(서술상수, "()I")) { 넣기(kuutoro.화면높이(), 1); return true; }
            if (말(이름상수, "밀리초") && 말(서술상수, "()I")) { 넣기(kuutoro.밀리초(), 1); return true; }
            if (말(이름상수, "그림대기") && 말(서술상수, "()I")) { 넣기(kuutoro.그림대기(), 1); return true; }
            if (말(이름상수, "사각형") && 말(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), 가로좌표 = 빼기(1); 넣기(kuutoro.사각형(가로좌표, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (말(소유종, "java/net/InetAddress") || 말(소유종, "java/net/DatagramPacket") || 말(소유종, "java/net/DatagramSocket")) { 통신호출(소유종, 이름상수, 서술상수, 명령코드); return true; }
        if (말(소유종, "java/lang/Thread")) { 가닥호출(이름상수, 서술상수, 명령코드); return true; }
        if (말(소유종, "java/lang/Object")) {
            if (말(이름상수, "<init>") && 말(서술상수, "()V") && 명령코드 == 183) { 객체유효(빼기(2)); return true; }
            if (말(이름상수, "equals") && 말(서술상수, "(Ljava/lang/Object;)Z")) { int oktee_keɓe = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == oktee_keɓe ? 1 : 0, 1); return true; }
        }
        if (예외상수(소유종) != 0) {
            if (말(이름상수, "<init>") && 명령코드 == 183 && (말(서술상수, "()V") || 말(서술상수, "(Ljava/lang/String;)V"))) {
                int hirjinaango = 말(서술상수, "()V") ? 0 : 빼기(2), 객체참조 = 빼기(2);
                if (huunde_njaru(객체참조, 9)) { 힙[객체참조 + 3] = hirjinaango; 힙참조[객체참조 + 3] = 1; } return true;
            }
            if ((말(이름상수, "getMessage") || 말(이름상수, "설명")) && 말(서술상수, "()Ljava/lang/String;")) { int 객체참조 = 빼기(2); if (huunde_njaru(객체참조, 9)) 넣기(힙[객체참조 + 3], 2); return true; }
        }
        if (말(소유종, "java/lang/String")) {
            if (명령코드 == 182 && 말(이름상수, "getBytes") && (말(서술상수, "()[B") || 말(서술상수, "(Ljava/lang/String;)[B"))) {
                int dokkagol_innde = 말(서술상수, "()[B") ? 0 : 빼기(2), 객체참조 = 빼기(2);
                if (!huunde_njaru(객체참조, 1)) return true;
                if (dokkagol_innde != 0 && !글같음(dokkagol_innde, njaatigi_alkulal("UTF-8"), false) && !글같음(dokkagol_innde, njaatigi_alkulal("UTF8"), false) && !글같음(dokkagol_innde, njaatigi_alkulal("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int 항목수 = 힙[객체참조 + 1], 반환값 = 할당(20, 항목수 * 3), 사용수 = 0; if (juumre) return true;
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
            if (말(이름상수, "equals") && 말(서술상수, "(Ljava/lang/Object;)Z")) { int oktee_keɓe = 빼기(2), 첫값 = 빼기(2); if (huunde_njaru(첫값, 1)) 넣기(글같음(첫값, oktee_keɓe, false) ? 1 : 0, 1); return true; }
            if (말(이름상수, "isEmpty") && 말(서술상수, "()Z")) { int 첫값 = 빼기(2); if (huunde_njaru(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (말(이름상수, "substring") && (말(서술상수, "(I)Ljava/lang/String;") || 말(서술상수, "(II)Ljava/lang/String;"))) {
                boolean 둘째값 = 말(서술상수, "(II)Ljava/lang/String;"); int 끝자리 = 둘째값 ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (huunde_njaru(첫값, 1)) 넣기(글조각(첫값, 시작점, 둘째값 ? 끝자리 : 힙[첫값 + 1]), 2); return true;
            }
            if (말(이름상수, "concat") && 말(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int oktee_keɓe = 빼기(2), 첫값 = 빼기(2); 넣기(jokkunde_binndi(첫값, oktee_keɓe), 2); return true; }
            if (말(이름상수, "hashCode") && 말(서술상수, "()I")) { int 첫값 = 빼기(2), 해시값 = 0; if (huunde_njaru(첫값, 1)) { for (int kowal_joopirdu = 0; kowal_joopirdu < 힙[첫값 + 1]; kowal_joopirdu++) 해시값 = 해시값 * 31 + 힙[첫값 + 2 + kowal_joopirdu]; 넣기(해시값, 1); } return true; }
            if (말(이름상수, "toString") && 말(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (huunde_njaru(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (말(소유종, "java/lang/Integer")) {
            if (명령코드 == 184 && 말(이름상수, "valueOf") && 말(서술상수, "(I)Ljava/lang/Integer;")) { int keɓe_njaru = 빼기(1), 객체참조 = keɓe_njaru >= -128 && keɓe_njaru <= 127 ? 정수저장[keɓe_njaru + 128] : 0; if (객체참조 == 0) { 객체참조 = 할당(12, 1); if (!juumre) { 힙[객체참조 + 2] = keɓe_njaru; if (keɓe_njaru >= -128 && keɓe_njaru <= 127) 정수저장[keɓe_njaru + 128] = 객체참조; } } 넣기(객체참조, 2); return true; }
            if (명령코드 == 183 && 말(이름상수, "<init>") && 말(서술상수, "(I)V")) { int keɓe_njaru = 빼기(1), 객체참조 = 빼기(2); if (huunde_njaru(객체참조, 12)) 힙[객체참조 + 2] = keɓe_njaru; return true; }
            if (명령코드 == 182 && 말(이름상수, "intValue") && 말(서술상수, "()I")) { int 객체참조 = 빼기(2); if (huunde_njaru(객체참조, 12)) 넣기(힙[객체참조 + 2], 1); return true; }
            if (명령코드 == 184 && 말(이름상수, "toString") && 말(서술상수, "(I)Ljava/lang/String;")) { 넣기(수문자(빼기(1)), 2); return true; }
        }
        if (말(소유종, "java/lang/Math") && 명령코드 == 184) {
            if (말(이름상수, "abs") && 말(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((말(이름상수, "min") || 말(이름상수, "max")) && 말(서술상수, "(II)I")) { int oktee_keɓe = 빼기(1), 첫값 = 빼기(1); 넣기(말(이름상수, "min") ? (첫값 < oktee_keɓe ? 첫값 : oktee_keɓe) : (첫값 > oktee_keɓe ? 첫값 : oktee_keɓe), 1); return true; }
        }
        if (말(소유종, "java/lang/System") && 명령코드 == 184) {
            if (말(이름상수, "gc") && 말(서술상수, "()V")) { 수거(); return true; }
            if (말(이름상수, "arraycopy") && 말(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int 항목수 = 빼기(1), tiindaare_njaru_joopirdu = 빼기(1), oktee_keɓe = 빼기(2), 시작자리 = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(oktee_keɓe)) {
                    int 분류코드 = 힙[첫값];
                    if (힙[oktee_keɓe] != 분류코드 || (분류코드 != 2 && 분류코드 != 3 && (분류코드 < 20 || 분류코드 > 23))) ella_njaru("arraycopy type mismatch");
                    else if (항목수 < 0 || 시작자리 < 0 || tiindaare_njaru_joopirdu < 0 || 시작자리 > 힙[첫값 + 1] - 항목수 || tiindaare_njaru_joopirdu > 힙[oktee_keɓe + 1] - 항목수) ella_njaru("ArrayIndexOutOfBoundsException");
                    else if (첫값 == oktee_keɓe && tiindaare_njaru_joopirdu > 시작자리) { for (int kowal_joopirdu = 항목수 - 1; kowal_joopirdu >= 0; kowal_joopirdu--) 힙[oktee_keɓe + 2 + tiindaare_njaru_joopirdu + kowal_joopirdu] = 힙[첫값 + 2 + 시작자리 + kowal_joopirdu]; }
                    else { for (int kowal_joopirdu = 0; kowal_joopirdu < 항목수 && !juumre; kowal_joopirdu++) { int keɓe_njaru = 힙[첫값 + 2 + 시작자리 + kowal_joopirdu]; if (분류코드 != 3 || 배열저장가능(oktee_keɓe, keɓe_njaru)) 힙[oktee_keɓe + 2 + tiindaare_njaru_joopirdu + kowal_joopirdu] = keɓe_njaru; } }
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
        int 자료배열 = 할당(3, 다음자리); if (juumre) return;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 용량값; kowal_joopirdu++) 힙[자료배열 + 2 + kowal_joopirdu] = 힙[이전값 + 2 + kowal_joopirdu];
        힙[객체참조 + 2] = 자료배열; 힙참조[객체참조 + 2] = 1;
    }
    static void 모음호출(int 소유종, int 이름상수, int 서술상수, int 명령코드) {
        boolean 대응참조 = 말(소유종, "java/util/HashMap") || 말(소유종, "java/util/Map"); int 분류코드 = 대응참조 ? 11 : 10;
        if (말(이름상수, "<init>") && 명령코드 == 183 && 말(서술상수, "()V")) { int 객체참조 = 빼기(2); if (huunde_njaru(객체참조, 분류코드)) 모음늘리기(객체참조, 8); return; }
        if (명령코드 != 182 && 명령코드 != 185) { ella_njaru("invalid collection invocation"); return; }
        if (말(이름상수, "size") && 말(서술상수, "()I") || 말(이름상수, "isEmpty") && 말(서술상수, "()Z")) {
            int 객체참조 = 빼기(2); if (huunde_njaru(객체참조, 분류코드)) 넣기(말(이름상수, "size") ? 힙[객체참조 + 3] : 힙[객체참조 + 3] == 0 ? 1 : 0, 1); return;
        }
        if (말(이름상수, "clear") && 말(서술상수, "()V")) { int 객체참조 = 빼기(2); if (huunde_njaru(객체참조, 분류코드)) { int 자료배열 = 힙[객체참조 + 2]; for (int kowal_joopirdu = 0; kowal_joopirdu < 힙[자료배열 + 1]; kowal_joopirdu++) 힙[자료배열 + 2 + kowal_joopirdu] = 0; 힙[객체참조 + 3] = 0; } return; }
        if (!대응참조 && 말(이름상수, "add") && 말(서술상수, "(Ljava/lang/Object;)Z")) {
            int keɓe_njaru = 빼기(2), 객체참조 = 빼기(2); if (!huunde_njaru(객체참조, 10)) return;
            int 항목수 = 힙[객체참조 + 3]; 모음늘리기(객체참조, 항목수 + 1); if (!juumre) { 힙[힙[객체참조 + 2] + 2 + 항목수] = keɓe_njaru; 힙[객체참조 + 3] = 항목수 + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (말(이름상수, "get") || 말(이름상수, "remove")) && 말(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && 말(이름상수, "set") && 말(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = 말(이름상수, "set"); int keɓe_njaru = 지정여부 ? 빼기(2) : 0, 항목자리 = 빼기(1), 객체참조 = 빼기(2);
            if (!huunde_njaru(객체참조, 10)) return;
            int 항목수 = 힙[객체참조 + 3], 자료배열 = 힙[객체참조 + 2];
            if (항목자리 < 0 || 항목자리 >= 항목수) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[자료배열 + 2 + 항목자리];
            if (지정여부) 힙[자료배열 + 2 + 항목자리] = keɓe_njaru;
            if (말(이름상수, "remove")) { for (int kowal_joopirdu = 항목자리 + 1; kowal_joopirdu < 항목수; kowal_joopirdu++) 힙[자료배열 + 1 + kowal_joopirdu] = 힙[자료배열 + 2 + kowal_joopirdu]; 힙[자료배열 + 1 + 항목수] = 0; 힙[객체참조 + 3] = 항목수 - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (말(이름상수, "get") || 말(이름상수, "remove")) && 말(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && 말(이름상수, "put") && 말(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && 말(이름상수, "containsKey") && 말(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = 말(이름상수, "put"), ittude = 말(이름상수, "remove");
            int keɓe_njaru = 넣기여부 ? 빼기(2) : 0, 키참조 = 빼기(2), 객체참조 = 빼기(2); if (!huunde_njaru(객체참조, 11)) return;
            int 항목수 = 힙[객체참조 + 3], 자료배열 = 힙[객체참조 + 2], 찾은여부 = -1;
            for (int kowal_joopirdu = 0; kowal_joopirdu < 항목수; kowal_joopirdu++) if (값같음(키참조, 힙[자료배열 + 2 + 2 * kowal_joopirdu])) { 찾은여부 = kowal_joopirdu; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[자료배열 + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(객체참조, (항목수 + 1) * 2); 자료배열 = 힙[객체참조 + 2]; 찾은여부 = 항목수; if (!juumre) 힙[객체참조 + 3] = 항목수 + 1; }
                if (!juumre) { 힙[자료배열 + 2 + 2 * 찾은여부] = 키참조; 힙[자료배열 + 3 + 2 * 찾은여부] = keɓe_njaru; }
            }
            if (ittude && 찾은여부 >= 0) { for (int kowal_joopirdu = 찾은여부 + 1; kowal_joopirdu < 항목수; kowal_joopirdu++) { 힙[자료배열 + 2 * kowal_joopirdu] = 힙[자료배열 + 2 + 2 * kowal_joopirdu]; 힙[자료배열 + 1 + 2 * kowal_joopirdu] = 힙[자료배열 + 3 + 2 * kowal_joopirdu]; } 힙[자료배열 + 2 * 항목수] = 0; 힙[자료배열 + 1 + 2 * 항목수] = 0; 힙[객체참조 + 3] = 항목수 - 1; }
            if (말(이름상수, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        ella_njaru("unsupported collection method");
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
    static boolean waylude_piilol() {
        piilol_taƴtinnde[현재가닥] = taƴtinnde_joopirdu;
        if (taƴtinnde_joopirdu < 현재가닥 * 32) piilol_ngonka[현재가닥] = 3;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 가닥수; kowal_joopirdu++) if (piilol_ngonka[kowal_joopirdu] == 2 && piilol_ngonka[가닥대기[kowal_joopirdu]] == 3) piilol_ngonka[kowal_joopirdu] = 1;
        for (int kowal_joopirdu = 1; kowal_joopirdu <= 가닥수; kowal_joopirdu++) {
            int 다음자리 = (현재가닥 + kowal_joopirdu) % 가닥수;
            if (piilol_ngonka[다음자리] == 1) { 현재가닥 = 다음자리; taƴtinnde_joopirdu = piilol_taƴtinnde[다음자리]; 바꿈요청 = false; return true; }
        }
        for (int kowal_joopirdu = 0; kowal_joopirdu < 가닥수; kowal_joopirdu++) if (piilol_ngonka[kowal_joopirdu] != 3) { ella_njaru("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int 이름상수, int 서술상수, int 명령코드) { Yuɓɓo_golle_piilol(이름상수, 서술상수, 명령코드, false); }
    static void Yuɓɓo_golle_piilol(int 이름상수, int 서술상수, int 명령코드, boolean 한국어) {
        if (명령코드 == 184 && 말(이름상수, 한국어 ? "양보하기" : "yield") && 말(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (명령코드 == 184 && 말(이름상수, "currentThread") && 말(서술상수, "()Ljava/lang/Thread;")) { 넣기(piilol_huunde[현재가닥], 2); return; }
        if (명령코드 == 183 && 말(이름상수, "<init>") && (말(서술상수, "()V") || 말(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int faandaare_ñiiɓirde = 말(서술상수, "()V") ? 0 : 빼기(2), 객체참조 = 빼기(2);
            if (!객체유효(객체참조)) return;
            if (힙[객체참조] == 13) { 힙[객체참조 + 2] = faandaare_ñiiɓirde; 힙참조[객체참조 + 2] = 1; }
            else if (faandaare_ñiiɓirde != 0) ella_njaru("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (명령코드 == 182 && (말(이름상수, 한국어 ? "huɓɓude_golle" : "start") || 말(이름상수, 한국어 ? "기다리기" : "join")) && 말(서술상수, "()V") || 명령코드 == 182 && 말(이름상수, 한국어 ? "살아있는가" : "isAlive") && 말(서술상수, "()Z")) {
            int 객체참조 = 빼기(2); if (!객체유효(객체참조)) return;
            int konte_njaru = -1; for (int kowal_joopirdu = 0; kowal_joopirdu < 가닥수; kowal_joopirdu++) if (piilol_huunde[kowal_joopirdu] == 객체참조) konte_njaru = kowal_joopirdu;
            if (말(이름상수, 한국어 ? "살아있는가" : "isAlive")) { 넣기(konte_njaru >= 0 && piilol_ngonka[konte_njaru] != 3 ? 1 : 0, 1); return; }
            if (말(이름상수, 한국어 ? "기다리기" : "join")) { if (konte_njaru >= 0 && piilol_ngonka[konte_njaru] != 3) { 가닥대기[현재가닥] = konte_njaru; piilol_ngonka[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (konte_njaru >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (가닥수 == 4) { ella_njaru("thread limit (4 including main)"); return; }
            int faandaare_ñiiɓirde = 힙[객체참조] == 13 ? 힙[객체참조 + 2] : 객체참조;
            int fiilde_joopirdu = faandaare_ñiiɓirde > 0 && 힙[faandaare_ñiiɓirde] >= 32 ? 이름함수(힙[faandaare_ñiiɓirde] - 32, 한국어 ? "실행하기" : "run", "()V") : -1;
            if (faandaare_ñiiɓirde != 0 && fiilde_joopirdu < 0) { ella_njaru("Runnable.run required"); return; }
            konte_njaru = 가닥수++; piilol_huunde[konte_njaru] = 객체참조; piilol_faandaare[konte_njaru] = faandaare_ñiiɓirde;
            int taƴtinnde = konte_njaru * 32; piilol_taƴtinnde[konte_njaru] = fiilde_joopirdu < 0 ? taƴtinnde - 1 : taƴtinnde; piilol_ngonka[konte_njaru] = fiilde_joopirdu < 0 ? 3 : 1;
            if (fiilde_joopirdu >= 0) { 틀함수[taƴtinnde] = fiilde_joopirdu; 틀위치[taƴtinnde] = 함수시작[fiilde_joopirdu]; nokkuwal_njaru[taƴtinnde * 128] = faandaare_ñiiɓirde; 지역형[taƴtinnde * 128] = 2; }
            return;
        }
        ella_njaru("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], ñiiɓirde_binndi = new int[16];
    static int nokkuwal_ñiiɓirde() { return ñiiɓirde_huunde(0x7f000001); }
    static int ñiiɓirde_huunde(int njaru) { int 객체참조 = 할당(14, 1); if (!juumre) 힙[객체참조 + 2] = njaru; return 객체참조; }
    static int 주소해독(int 객체참조) {
        if (객체참조 == 0 || 글같음(객체참조, njaatigi_alkulal("localhost"), false)) return 0x7f000001;
        if (!huunde_njaru(객체참조, 1)) return 0;
        int keɓe_njaru = 0, 총수 = 0, ñiiɓirde_oktee = 0, 자릿수 = 0, 항목수 = 힙[객체참조 + 1];
        for (int kowal_joopirdu = 0; kowal_joopirdu <= 항목수; kowal_joopirdu++) {
            int 문자값 = kowal_joopirdu == 항목수 ? '.' : 힙[객체참조 + 2 + kowal_joopirdu];
            if (문자값 == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } keɓe_njaru = keɓe_njaru << 8 | ñiiɓirde_oktee; 총수++; ñiiɓirde_oktee = 자릿수 = 0; }
            else { if (문자값 < '0' || 문자값 > '9' || ++자릿수 > 3 || (ñiiɓirde_oktee = ñiiɓirde_oktee * 10 + 문자값 - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return keɓe_njaru;
    }
    static int ñiiɓirde_alkulal(int keɓe_njaru) {
        int 항목수 = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int ñiiɓirde_oktee = keɓe_njaru >>> 이동비트 & 255;
            if (ñiiɓirde_oktee >= 100) ñiiɓirde_binndi[항목수++] = '0' + ñiiɓirde_oktee / 100;
            if (ñiiɓirde_oktee >= 10) ñiiɓirde_binndi[항목수++] = '0' + ñiiɓirde_oktee / 10 % 10;
            ñiiɓirde_binndi[항목수++] = '0' + ñiiɓirde_oktee % 10; if (이동비트 != 0) ñiiɓirde_binndi[항목수++] = '.';
        }
        int 객체참조 = 할당(1, 항목수); if (!juumre) for (int kowal_joopirdu = 0; kowal_joopirdu < 항목수; kowal_joopirdu++) 힙[객체참조 + 2 + kowal_joopirdu] = ñiiɓirde_binndi[kowal_joopirdu]; return 객체참조;
    }
    static void 통신호출(int 소유종, int 이름상수, int 서술상수, int 명령코드) {
        if (말(소유종, "java/net/InetAddress")) {
            if (명령코드 == 184 && 말(이름상수, "getLoopbackAddress") && 말(서술상수, "()Ljava/net/InetAddress;")) { 넣기(nokkuwal_ñiiɓirde(), 2); return; }
            if (명령코드 == 184 && 말(이름상수, "getByName") && 말(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int keɓe_njaru = 주소해독(빼기(2)); if (던진객체 == 0 && !juumre) 넣기(ñiiɓirde_huunde(keɓe_njaru), 2); return;
            }
            if (명령코드 == 182 && 말(이름상수, "getHostAddress") && 말(서술상수, "()Ljava/lang/String;")) { int 객체참조 = 빼기(2); if (huunde_njaru(객체참조, 14)) 넣기(ñiiɓirde_alkulal(힙[객체참조 + 2]), 2); return; }
        }
        if (말(소유종, "java/net/DatagramPacket")) {
            if (명령코드 == 183 && 말(이름상수, "<init>") && (말(서술상수, "([BI)V") || 말(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean 목적참조 = 말(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = 목적참조 ? 빼기(1) : 0, 주소참조 = 목적참조 ? 빼기(2) : 0;
                int 항목수 = 빼기(1), 자료배열 = 빼기(2), 객체참조 = 빼기(2);
                if (!huunde_njaru(객체참조, 16) || !huunde_njaru(자료배열, 20)) return;
                if (항목수 < 0 || 항목수 > 힙[자료배열 + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (주소참조 != 0 && !huunde_njaru(주소참조, 14)) return;
                힙[객체참조 + 2] = 자료배열; 힙참조[객체참조 + 2] = 1; 힙[객체참조 + 3] = 항목수;
                힙[객체참조 + 4] = 주소참조; 힙참조[객체참조 + 4] = 1; 힙[객체참조 + 5] = 접속번호; return;
            }
            if (명령코드 == 182 && 말(이름상수, "setLength") && 말(서술상수, "(I)V")) {
                int 항목수 = 빼기(1), 객체참조 = 빼기(2); if (!huunde_njaru(객체참조, 16)) return;
                if (항목수 < 0 || 항목수 > 힙[힙[객체참조 + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[객체참조 + 3] = 항목수; return;
            }
            if (명령코드 == 182 && (말(이름상수, "getData") && 말(서술상수, "()[B") || 말(이름상수, "getLength") && 말(서술상수, "()I") || 말(이름상수, "getAddress") && 말(서술상수, "()Ljava/net/InetAddress;") || 말(이름상수, "getPort") && 말(서술상수, "()I"))) {
                int 객체참조 = 빼기(2); if (!huunde_njaru(객체참조, 16)) return;
                int 항목자리 = 말(이름상수, "getData") ? 2 : 말(이름상수, "getLength") ? 3 : 말(이름상수, "getAddress") ? 4 : 5;
                넣기(힙[객체참조 + 항목자리], 항목자리 == 2 || 항목자리 == 4 ? 2 : 1); return;
            }
        }
        if (말(소유종, "java/net/DatagramSocket")) {
            if (명령코드 == 183 && 말(이름상수, "<init>") && (말(서술상수, "()V") || 말(서술상수, "(I)V"))) {
                int 접속번호 = 말(서술상수, "()V") ? 0 : 빼기(1), 객체참조 = 빼기(2); if (!huunde_njaru(객체참조, 15)) return;
                if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = kuutoro.udditde_laylaytol(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[객체참조 + 2] = 열린파일번호; return;
            }
            if (명령코드 == 182 && 말(이름상수, "setSoTimeout") && 말(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), 객체참조 = 빼기(2); if (!huunde_njaru(객체참조, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[객체참조 + 3] = 밀리초값; return;
            }
            if (명령코드 == 182 && 말(이름상수, "getLocalPort") && 말(서술상수, "()I")) { int 객체참조 = 빼기(2); if (huunde_njaru(객체참조, 15)) 넣기(힙[객체참조 + 2] < 0 ? -1 : kuutoro.laylaytol_poor(힙[객체참조 + 2]), 1); return; }
            if (명령코드 == 182 && 말(이름상수, "isClosed") && 말(서술상수, "()Z")) { int 객체참조 = 빼기(2); if (huunde_njaru(객체참조, 15)) 넣기(힙[객체참조 + 2] < 0 ? 1 : 0, 1); return; }
            if (명령코드 == 182 && 말(이름상수, "close") && 말(서술상수, "()V")) { int 객체참조 = 빼기(2); if (huunde_njaru(객체참조, 15) && 힙[객체참조 + 2] >= 0) { kuutoro.파일서술자닫기(힙[객체참조 + 2]); 힙[객체참조 + 2] = -1; } return; }
            if (명령코드 == 182 && (말(이름상수, "send") || 말(이름상수, "receive")) && 말(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int 전문참조 = 빼기(2), 객체참조 = 빼기(2); if (!huunde_njaru(전문참조, 16) || !huunde_njaru(객체참조, 15)) return;
                int 자료배열 = 힙[전문참조 + 2], 유효길이 = 힙[전문참조 + 3], 열린파일번호 = 힙[객체참조 + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (말(이름상수, "send")) {
                    if (!huunde_njaru(힙[전문참조 + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int kowal_joopirdu = 0; kowal_joopirdu < 유효길이; kowal_joopirdu++) 통신임시[kowal_joopirdu] = 힙[자료배열 + 2 + kowal_joopirdu];
                    if (kuutoro.neldude_laylaytol(열린파일번호, 힙[힙[전문참조 + 4] + 2], 힙[전문참조 + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int 항목수 = kuutoro.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (항목수 == -11) {
                        int 현재시각 = kuutoro.밀리초();
                        if (힙[객체참조 + 4] == 0) 힙[객체참조 + 4] = 현재시각 + 1;
                        if (힙[객체참조 + 3] > 0 && 현재시각 - (힙[객체참조 + 4] - 1) >= 힙[객체참조 + 3]) { 힙[객체참조 + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(객체참조, 2); 넣기(전문참조, 2); 틀위치[taƴtinnde_joopirdu] = taƴtinnde_yamiroore[taƴtinnde_joopirdu]; 바꿈요청 = true; return;
                    }
                    힙[객체참조 + 4] = 0;
                    if (항목수 < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int kowal_joopirdu = 0; kowal_joopirdu < 항목수; kowal_joopirdu++) 힙[자료배열 + 2 + kowal_joopirdu] = (byte)통신임시[kowal_joopirdu];
                    힙[전문참조 + 3] = 항목수; 힙[전문참조 + 4] = ñiiɓirde_huunde(통신임시[513]); 힙참조[전문참조 + 4] = 1; 힙[전문참조 + 5] = 통신임시[512];
                }
                return;
            }
        }
        ella_njaru("unsupported java.net method");
    }
    static boolean 흐름대기(int 객체참조) {
        int 현재시각 = kuutoro.밀리초();
        if (힙[객체참조 + 5] == 0) 힙[객체참조 + 5] = 현재시각 + 1;
        if (힙[객체참조 + 3] > 0 && 현재시각 - (힙[객체참조 + 5] - 1) >= 힙[객체참조 + 3]) { 힙[객체참조 + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        틀위치[taƴtinnde_joopirdu] = taƴtinnde_yamiroore[taƴtinnde_joopirdu]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int 소유종, int 이름상수, int 서술상수, int 명령코드) {
        boolean 수신쪽 = 말(소유종, "java/net/ServerSocket"), waraango = 말(소유종, "java/io/InputStream") || 말(소유종, "java/io/OutputStream");
        if (!waraango && 명령코드 == 183 && 말(이름상수, "<init>")) {
            boolean 빈여부 = 말(서술상수, "()V"), 이름지정여부 = 말(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = 말(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && 말(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { ella_njaru("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), 주소참조 = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, 객체참조 = 빼기(2);
            if (!huunde_njaru(객체참조, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !huunde_njaru(주소참조, 14)) return;
            int laylaytol_ñiiɓirde = 이름지정여부 ? 주소해독(주소참조) : 주소지정여부 ? 힙[주소참조 + 2] : 0x7f000001;
            if (juumre || 던진객체 != 0) return;
            int 열린파일번호 = kuutoro.waraango_yuurnitorde(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? kuutoro.waraango_yuurnitorde(1, 열린파일번호, 접속번호) : kuutoro.seŋaade_waraango(열린파일번호, laylaytol_ñiiɓirde, 접속번호);
            if (처리값 < 0) { kuutoro.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[객체참조 + 2] = 열린파일번호; 힙[객체참조 + 4] = 접속번호; 힙[객체참조 + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!waraango && 말(이름상수, "setSoTimeout") && 말(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), 객체참조 = 빼기(2); if (!huunde_njaru(객체참조, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[객체참조 + 3] = 밀리초값; return; }
        if (!waraango && 말(이름상수, "close") && 말(서술상수, "()V")) { int 객체참조 = 빼기(2); if (huunde_njaru(객체참조, 수신쪽 ? 18 : 17) && 힙[객체참조 + 2] >= 0) { kuutoro.파일서술자닫기(힙[객체참조 + 2]); 힙[객체참조 + 2] = -1; } return; }
        if (!waraango && (말(이름상수, "getLocalPort") || 말(이름상수, "getPort") || 말(이름상수, "isClosed") || 말(이름상수, "isConnected"))) {
            int 객체참조 = 빼기(2); if (!huunde_njaru(객체참조, 수신쪽 ? 18 : 17)) return;
            넣기(말(이름상수, "isClosed") ? 힙[객체참조 + 2] < 0 ? 1 : 0 : 말(이름상수, "isConnected") ? 힙[객체참조 + 6] : 말(이름상수, "getPort") ? 힙[객체참조 + 4] : 힙[객체참조 + 2] < 0 ? -1 : kuutoro.waraango_yuurnitorde(4, 힙[객체참조 + 2], 0), 1); return;
        }
        if (수신쪽 && 말(이름상수, "accept") && 말(서술상수, "()Ljava/net/Socket;")) {
            int 객체참조 = 빼기(2); if (!huunde_njaru(객체참조, 18)) return; int 열린파일번호 = kuutoro.waraango_yuurnitorde(3, 힙[객체참조 + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(객체참조)) 넣기(객체참조, 2); return; }
            힙[객체참조 + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = 할당(17, 5); if (juumre) { kuutoro.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = kuutoro.waraango_yuurnitorde(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !waraango && ((말(이름상수, "getInputStream") && 말(서술상수, "()Ljava/io/InputStream;")) || (말(이름상수, "getOutputStream") && 말(서술상수, "()Ljava/io/OutputStream;")))) {
            int 객체참조 = 빼기(2); if (!huunde_njaru(객체참조, 17)) return; if (힙[객체참조 + 2] < 0 || 힙[객체참조 + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = 할당(19, 4); if (juumre) return; 힙[반환값 + 2] = 객체참조; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = 말(이름상수, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (waraango) {
            boolean 읽기여부 = 말(이름상수, "read"), 쓰기여부 = 말(이름상수, "write"), 배열여부 = 말(서술상수, "([B)I") || 말(서술상수, "([B)V"), 부분배열여부 = 말(서술상수, "([BII)I") || 말(서술상수, "([BII)V");
            int 항목수 = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, 자료배열 = 배열여부 || 부분배열여부 ? 빼기(2) : 0;
            int keɓe_njaru = 쓰기여부 && 말(서술상수, "(I)V") ? 빼기(1) : 0, 객체참조 = 빼기(2);
            if (!huunde_njaru(객체참조, 19)) return; int 부모참조 = 힙[객체참조 + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (말(이름상수, "close") && 말(서술상수, "()V")) { kuutoro.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (말(이름상수, "flush") && 말(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[객체참조 + 3] == 0)) { ella_njaru("unsupported stream operation"); return; }
            if (배열여부 || 부분배열여부) { if (!huunde_njaru(자료배열, 20)) return; if (배열여부) 항목수 = 힙[자료배열 + 1]; if (시작변위 < 0 || 항목수 < 0 || 시작변위 > 힙[자료배열 + 1] - 항목수) { 예외던짐(6, "stream array bounds"); return; } }
            else 항목수 = 1;
            if (항목수 == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[객체참조 + 4] : 0, 처리값 = 0;
            while (완료수 < 항목수) {
                처리값 = 읽기여부 ? kuutoro.파일한바이트읽기(열린파일번호) : kuutoro.파일한바이트쓰기(열린파일번호, 배열여부 || 부분배열여부 ? 힙[자료배열 + 2 + 시작변위 + 완료수] : keɓe_njaru);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (배열여부 || 부분배열여부)) 힙[자료배열 + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(배열여부 || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[객체참조 + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(객체참조, 2); if (배열여부 || 부분배열여부) 넣기(자료배열, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(항목수, 1); } if (쓰기여부 && !(배열여부 || 부분배열여부)) 넣기(keɓe_njaru, 1); } return;
            }
            힙[객체참조 + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : 배열여부 || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        ella_njaru("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int 이름상수) {
        if (말(이름상수, "한국어/자체/falanteere")) return 24;
        if (말(이름상수, "한국어/자체/tinndinoore")) return 26;
        if (말(이름상수, "한국어/자체/feɗoode")) return 27;
        if (말(이름상수, "한국어/자체/binndi_suudu")) return 28;
        if (말(이름상수, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int 이름상수) {
        return 한국어화면종(이름상수) != 0 || 말(이름상수, "한국어/자체/화면구성요소") || 말(이름상수, "한국어/자체/saɗteende_lappol");
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
    static boolean 화면객체(int 객체참조) { if (!객체유효(객체참조)) return false; if (힙[객체참조] < 24 || 힙[객체참조] > 28) { ella_njaru("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int 객체참조, int 글참조) {
        if (글참조 != 0 && !huunde_njaru(글참조, 1)) return;
        int 항목수 = 글참조 == 0 ? 0 : 힙[글참조 + 1]; if (항목수 > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int kowal_joopirdu = 0; kowal_joopirdu < 항목수; kowal_joopirdu++) 화면글임시[kowal_joopirdu] = 힙[글참조 + 2 + kowal_joopirdu];
        if (kuutoro.화면글(힙[객체참조 + 2], 화면글임시, 항목수) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[객체참조 + 3] = 글참조; 힙참조[객체참조 + 3] = 1;
    }
    static int 화면문자읽기(int 객체참조) {
        int konte_njaru = 힙[객체참조 + 2], 항목수 = kuutoro.화면연결(8, konte_njaru, 0, 0, 0, 0), 사용수 = 0;
        if (항목수 < 0) { ella_njaru("GUI text read failed"); return 0; }
        for (int kowal_joopirdu = 0; kowal_joopirdu < 항목수; kowal_joopirdu++) { int 부호값 = kuutoro.화면연결(9, konte_njaru, kowal_joopirdu, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = 할당(1, 사용수); if (!juumre) for (int kowal_joopirdu = 0; kowal_joopirdu < 사용수; kowal_joopirdu++) 힙[반환값 + 2 + kowal_joopirdu] = 화면글임시[kowal_joopirdu]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 aaluude_njaru 화면 기능에 연결한다. Swing huunde_njaru/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int 소유종, int 이름상수, int 서술상수, int 명령코드) {
        if (말(소유종, "한국어/자체/saɗteende_lappol")) {
            if (명령코드 == 184 && 말(이름상수, "나중에실행") && 말(서술상수, "(L한국어/자체/실행할일;)V")) {
                int golle_gollal = 빼기(2); if (!객체유효(golle_gollal)) return;
                if (나중수 == 8) { ella_njaru("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = golle_gollal; return;
            }
            if (명령코드 == 184 && 말(이름상수, "사건처리중인가") && 말(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            ella_njaru("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (말(소유종, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!huunde_njaru(알림, 29) || 힙[알림 + 3] == 0) return;
            if (말(이름상수, "saɗteende_sewnde") && 말(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (말(이름상수, "ginol_binndi") && 말(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (말(이름상수, "joopirdu") && 말(서술상수, "()I")) 넣기(1001, 1);
            else ella_njaru("지원하지 않는 한국어 gollal 알림 호출"); return;
        }
        if (명령코드 == 183 && 말(이름상수, "<init>")) {
            int 종류 = 한국어화면종(소유종), 받이 = 0, 가로 = 0, 세로 = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && 말(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (kuutoro.화면너비() - 폭) / 2; 세로 = (kuutoro.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && 말(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && 말(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); 세로 = 빼기(1); 가로 = 빼기(1);
            } else { ella_njaru("지원하지 않는 한국어 화면 생성자"); return; }
            int binndi = 빼기(2), geɗel_njaru = 빼기(2); if (!화면객체(geɗel_njaru)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || 세로 < 0 || 폭 > kuutoro.화면너비() - 가로 || 높이 > kuutoro.화면높이() - 세로) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int joopirdu = kuutoro.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (joopirdu < 1 || joopirdu > 32) { ella_njaru("화면 geɗel_njaru 자리가 가득 찼습니다"); return; }
            힙[geɗel_njaru + 2] = joopirdu; 화면참조[joopirdu - 1] = geɗel_njaru;
            힙[geɗel_njaru + 5] = 가로; 힙[geɗel_njaru + 6] = 세로; 힙[geɗel_njaru + 7] = 폭; 힙[geɗel_njaru + 8] = 높이; 힙[geɗel_njaru + 10] = 2;
            힙[geɗel_njaru + 4] = 받이; 힙참조[geɗel_njaru + 4] = 1; 힙[geɗel_njaru + 12] = 1;
            kuutoro.화면연결(1, joopirdu, 가로, 세로, 폭, 높이);
            if (종류 == 24) kuutoro.화면연결(7, joopirdu, 2, 0, 0, 0);
            화면문자설정(geɗel_njaru, binndi); return;
        }
        if (명령코드 != 182) { ella_njaru("잘못된 한국어 화면 호출 ginol"); return; }
        if (말(이름상수, "winndude_binndi") && 말(서술상수, "(Ljava/lang/String;)V")) {
            int binndi = 빼기(2), geɗel_njaru = 빼기(2); if (화면객체(geɗel_njaru)) 화면문자설정(geɗel_njaru, binndi); return;
        }
        if (말(이름상수, "글읽기") && 말(서술상수, "()Ljava/lang/String;")) {
            int geɗel_njaru = 빼기(2); if (화면객체(geɗel_njaru)) 넣기(화면문자읽기(geɗel_njaru), 2); return;
        }
        if (말(이름상수, "동작맡기기") && 말(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), geɗel_njaru = 빼기(2);
            if (화면객체(geɗel_njaru)) { 힙[geɗel_njaru + 4] = 받이; 힙참조[geɗel_njaru + 4] = 1; 힙[geɗel_njaru + 12] = 1; } return;
        }
        if (말(이름상수, "ɓeydude_geɗel") && 말(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int 자식 = 빼기(2), 부모 = 빼기(2); if (!화면객체(자식) || !화면객체(부모)) return;
            if (kuutoro.화면연결(2, 힙[부모 + 2], 힙[자식 + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[자식 + 11] = 부모; 힙참조[자식 + 11] = 1; return;
        }
        if (말(이름상수, "자리정하기") && 말(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), 세로 = 빼기(1), 가로 = 빼기(1), geɗel_njaru = 빼기(2); if (!화면객체(geɗel_njaru)) return;
            if (kuutoro.화면연결(1, 힙[geɗel_njaru + 2], 가로, 세로, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[geɗel_njaru + 5] = 가로; 힙[geɗel_njaru + 6] = 세로; 힙[geɗel_njaru + 7] = 폭; 힙[geɗel_njaru + 8] = 높이; return;
        }
        if ((말(이름상수, "hollirde_falanteere") || 말(이름상수, "uddude")) && 말(서술상수, "()V")) {
            boolean jiitinigol_njaru = 말(이름상수, "hollirde_falanteere"); int geɗel_njaru = 빼기(2); if (!화면객체(geɗel_njaru)) return;
            if (kuutoro.화면연결(jiitinigol_njaru ? 3 : 4, 힙[geɗel_njaru + 2], jiitinigol_njaru ? 1 : 0, 0, 0, 0) < 0) { ella_njaru("화면은 jokkondirtoo 명령에서 실행해야 합니다"); return; }
            힙[geɗel_njaru + 9] = jiitinigol_njaru ? 1 : 0; return;
        }
        if (말(이름상수, "보이는가") && 말(서술상수, "()Z")) { int geɗel_njaru = 빼기(2); if (화면객체(geɗel_njaru)) 넣기(힙[geɗel_njaru + 9], 1); return; }
        ella_njaru("지원하지 않는 한국어 화면 메서드");
    }
    static void 화면호출(int 소유종, int 이름상수, int 서술상수, int 명령코드) {
        if (말(소유종, "javax/swing/SwingUtilities")) {
            if (명령코드 == 184 && 말(이름상수, "invokeLater") && 말(서술상수, "(Ljava/lang/Runnable;)V")) { int 객체참조 = 빼기(2); if (!객체유효(객체참조)) return; if (나중수 == 8) { ella_njaru("invokeLater queue full"); return; } 나중실행[나중수++] = 객체참조; return; }
            if (명령코드 == 184 && 말(이름상수, "isEventDispatchThread") && 말(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            ella_njaru("unsupported SwingUtilities method"); return;
        }
        if (말(소유종, "java/awt/event/ActionEvent")) {
            int 객체참조 = 빼기(2); if (!huunde_njaru(객체참조, 29)) return;
            if (말(이름상수, "getSource") && 말(서술상수, "()Ljava/lang/Object;")) 넣기(힙[객체참조 + 2], 2);
            else if (말(이름상수, "getActionCommand") && 말(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[객체참조 + 2]), 2);
            else if (말(이름상수, "getID") && 말(서술상수, "()I")) 넣기(1001, 1);
            else ella_njaru("unsupported ActionEvent method"); return;
        }
        if (명령코드 == 183 && 말(이름상수, "<init>")) {
            int 열수 = 0, 글참조 = 0;
            if (말(서술상수, "(I)V")) 열수 = 빼기(1);
            else if (말(서술상수, "(Ljava/lang/String;I)V")) { 열수 = 빼기(1); 글참조 = 빼기(2); }
            else if (말(서술상수, "(Ljava/lang/String;)V")) 글참조 = 빼기(2);
            else if (말(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!말(서술상수, "()V")) { ella_njaru("unsupported Swing constructor"); return; }
            int 객체참조 = 빼기(2); if (!객체유효(객체참조)) return;
            if (힙[객체참조] == 30) { ella_njaru("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(객체참조) || 열수 < 0) return;
            int konte_njaru = kuutoro.화면연결(0, 힙[객체참조] - 23, 0, 0, 0, 0);
            if (konte_njaru < 1 || konte_njaru > 32) { ella_njaru("GUI widget slots exhausted"); return; }
            힙[객체참조 + 2] = konte_njaru; 화면참조[konte_njaru - 1] = 객체참조; 힙[객체참조 + 5] = 힙[객체참조] == 24 ? 130 : 16; 힙[객체참조 + 6] = 힙[객체참조] == 24 ? 110 : 16;
            힙[객체참조 + 7] = 힙[객체참조] == 24 ? 380 : 220; 힙[객체참조 + 8] = 힙[객체참조] == 24 ? 240 : 28; 힙[객체참조 + 10] = 1;
            화면문자설정(객체참조, 글참조); return;
        }
        if (말(이름상수, "setText") || 말(이름상수, "setTitle")) { int 글참조 = 빼기(2), 객체참조 = 빼기(2); if (화면객체(객체참조) && 말(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(객체참조, 글참조); return; }
        if (말(이름상수, "getText") || 말(이름상수, "getTitle")) { int 객체참조 = 빼기(2); if (화면객체(객체참조) && 말(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(객체참조), 2); return; }
        if (말(이름상수, "addActionListener") && 말(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), 객체참조 = 빼기(2); if (화면객체(객체참조)) { 힙[객체참조 + 4] = 수신참조; 힙참조[객체참조 + 4] = 1; } return; }
        if (말(이름상수, "getContentPane") && 말(서술상수, "()Ljava/awt/Container;")) { int 객체참조 = 빼기(2); if (화면객체(객체참조)) 넣기(객체참조, 2); return; }
        if (말(이름상수, "setLayout") && 말(서술상수, "(Ljava/awt/LayoutManager;)V")) { int 배치참조 = 빼기(2), 객체참조 = 빼기(2); if (화면객체(객체참조) && 배치참조 != 0) ella_njaru("only absolute layout (null) is supported"); return; }
        if (말(이름상수, "add") && (말(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || 말(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean lelngo_ngonka = 말(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (lelngo_ngonka) 빼기(2);
            int 자식참조 = 빼기(2), 객체참조 = 빼기(2); if (!화면객체(자식참조) || !화면객체(객체참조)) return;
            if (kuutoro.화면연결(2, 힙[객체참조 + 2], 힙[자식참조 + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[자식참조 + 11] = 객체참조; 힙참조[자식참조 + 11] = 1; if (!lelngo_ngonka) 넣기(자식참조, 2); return;
        }
        if (말(이름상수, "setBounds") && 말(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), 가로좌표 = 빼기(1), 객체참조 = 빼기(2); if (!화면객체(객체참조)) return;
            if (kuutoro.화면연결(1, 힙[객체참조 + 2], 가로좌표, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[객체참조 + 5] = 가로좌표; 힙[객체참조 + 6] = 세로좌표; 힙[객체참조 + 7] = 너비; 힙[객체참조 + 8] = 높이; return;
        }
        if (말(이름상수, "setSize") && 말(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 객체참조 = 빼기(2); if (!화면객체(객체참조)) return;
            if (kuutoro.화면연결(1, 힙[객체참조 + 2], 힙[객체참조 + 5], 힙[객체참조 + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[객체참조 + 7] = 너비; 힙[객체참조 + 8] = 높이; } return;
        }
        if (말(이름상수, "setLocationRelativeTo") && 말(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), 객체참조 = 빼기(2); if (!화면객체(객체참조)) return; if (상대배치 != 0) { ella_njaru("only screen centering supported"); return; } 힙[객체참조 + 5] = (kuutoro.화면너비() - 힙[객체참조 + 7]) / 2; 힙[객체참조 + 6] = (kuutoro.화면높이() - 힙[객체참조 + 8]) / 2; kuutoro.화면연결(1, 힙[객체참조 + 2], 힙[객체참조 + 5], 힙[객체참조 + 6], 힙[객체참조 + 7], 힙[객체참조 + 8]); return; }
        if (말(이름상수, "setDefaultCloseOperation") && 말(서술상수, "(I)V")) { int 종료정책 = 빼기(1), 객체참조 = 빼기(2); if (화면객체(객체참조)) { if (종료정책 < 0 || 종료정책 > 3) 예외던짐(9, "close policy"); else { 힙[객체참조 + 10] = 종료정책; kuutoro.화면연결(7, 힙[객체참조 + 2], 종료정책, 0, 0, 0); } } return; }
        if (말(이름상수, "setVisible") && 말(서술상수, "(Z)V")) { int keɓe_njaru = 빼기(1), 객체참조 = 빼기(2); if (화면객체(객체참조)) { int 처리값 = kuutoro.화면연결(3, 힙[객체참조 + 2], keɓe_njaru, 0, 0, 0); if (처리값 < 0) ella_njaru("Swing requires a standalone interactive command"); else 힙[객체참조 + 9] = keɓe_njaru; } return; }
        if (말(이름상수, "dispose") && 말(서술상수, "()V")) { int 객체참조 = 빼기(2); if (화면객체(객체참조)) { kuutoro.화면연결(4, 힙[객체참조 + 2], 0, 0, 0, 0); 힙[객체참조 + 9] = 0; } return; }
        if (말(이름상수, "repaint") || 말(이름상수, "validate")) { int 객체참조 = 빼기(2); if (!화면객체(객체참조) || !말(서술상수, "()V")) return; kuutoro.화면연결(1, 힙[객체참조 + 2], 힙[객체참조 + 5], 힙[객체참조 + 6], 힙[객체참조 + 7], 힙[객체참조 + 8]); return; }
        if (말(이름상수, "isVisible") && 말(서술상수, "()Z")) { int 객체참조 = 빼기(2); if (화면객체(객체참조)) 넣기(힙[객체참조 + 9], 1); return; }
        ella_njaru("unsupported Swing method (native subset)");
    }
    static void 사건실행(int faandaare_ñiiɓirde, int 사건번호, boolean 한국어) {
        if (faandaare_ñiiɓirde < 1 || 힙[faandaare_ñiiɓirde] < 32) { ella_njaru("Java event listener required"); return; }
        int fiilde_joopirdu = 이름함수(힙[faandaare_ñiiɓirde] - 32, 사건번호 == 0 ? (한국어 ? "실행하기" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (fiilde_joopirdu < 0) { ella_njaru("event callback missing"); return; }
        현재가닥 = 0; 가닥수 = 1; taƴtinnde_joopirdu = 0; piilol_ngonka[0] = 1; 틀스택[0] = 0; 틀잠금[0] = ɓamtinde_taƴtinnde[0] = 0; 바꿈요청 = false;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 128; kowal_joopirdu++) { nokkuwal_njaru[kowal_joopirdu] = 지역형[kowal_joopirdu] = 0; }
        틀함수[0] = fiilde_joopirdu; 틀위치[0] = 함수시작[fiilde_joopirdu]; nokkuwal_njaru[0] = faandaare_ñiiɓirde; 지역형[0] = 2;
        if (사건번호 != 0) { nokkuwal_njaru[1] = 사건번호; 지역형[1] = 2; }
        사건중 = true; 실행(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!juumre) {
            if (나중수 > 0) { int faandaare_ñiiɓirde = 나중실행[0], 한국어 = 나중한국어[0]; for (int kowal_joopirdu = 1; kowal_joopirdu < 나중수; kowal_joopirdu++) { 나중실행[kowal_joopirdu - 1] = 나중실행[kowal_joopirdu]; 나중한국어[kowal_joopirdu - 1] = 나중한국어[kowal_joopirdu]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(faandaare_ñiiɓirde, 0, 한국어 != 0); continue; }
            if (kuutoro.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = kuutoro.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { ella_njaru("GUI event I/O failed"); return; }
            int konte_njaru = 사건번호 & 65535; if (konte_njaru < 1 || konte_njaru > 32) continue; int 객체참조 = 화면참조[konte_njaru - 1]; if (객체참조 == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[객체참조 + 10] != 0) 힙[객체참조 + 9] = 0;
                if (힙[객체참조 + 10] == 3) for (int kowal_joopirdu = 0; kowal_joopirdu < 32; kowal_joopirdu++) if (화면참조[kowal_joopirdu] != 0 && 힙[화면참조[kowal_joopirdu]] == 24) kuutoro.화면연결(4, kowal_joopirdu + 1, 0, 0, 0, 0);
            } else if (힙[객체참조 + 4] != 0) {
                int 안내참조 = 할당(29, 2); if (juumre) return; 힙[안내참조 + 2] = 객체참조; 힙[안내참조 + 3] = 힙[객체참조 + 12]; 힙참조[안내참조 + 2] = 1; 사건실행(힙[객체참조 + 4], 안내참조, 힙[객체참조 + 12] != 0);
            }
        }
    }
    public static int huutoraade() {
        if (kuutoro.인수개수() == 1 && 자바도구.같음(kuutoro.인수(0), "-version")) {
            kuutoro.winndude("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (kuutoro.인수개수() < 1) { kuutoro.winndude("Usage: java CLASS [ARGS]\n"); return 2; }
        시작종 = 종적재(njaatigi_alkulal(kuutoro.인수(0))); if (juumre || 시작종 < 0) return 1;
        int naatnugol_toɓɓere_njaru = 이름함수(시작종, "huutoraade", "()V");
        boolean 한국어진입 = naatnugol_toɓɓere_njaru >= 0 && (함수권한[naatnugol_toɓɓere_njaru] & 9) == 9;
        if (!한국어진입) naatnugol_toɓɓere_njaru = 이름함수(시작종, "main", "([Ljava/lang/String;)V");
        if (naatnugol_toɓɓere_njaru < 0 || (함수권한[naatnugol_toɓɓere_njaru] & 9) != 9) ella_njaru("public static void huutoraade() or main(String[] args) required");
        if (juumre) return 1;
        int 인수 = 할당(3, kuutoro.인수개수() - 1); 배열원소[인수] = -1;
        for (int 수 = 1; 수 < kuutoro.인수개수() && !juumre; 수++) 힙[인수 + 1 + 수] = njaatigi_alkulal(kuutoro.인수(수));
        taƴtinnde_joopirdu = 0; 틀함수[0] = naatnugol_toɓɓere_njaru; 틀위치[0] = 함수시작[naatnugol_toɓɓere_njaru]; nokkuwal_njaru[0] = 한국어진입 ? 0 : 인수; 지역형[0] = 한국어진입 ? 0 : 2;
        piilol_ngonka[0] = 1; piilol_huunde[0] = 할당(13, 2);
        실행(); if (!juumre) 화면사건들(); return juumre ? 1 : 0;
    }
}
