// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Fayiro/스택/참조/분기 경계를 실행 중 검사한다. */
public final class 자바가상기계 {
    static int[] Fayiro = new int[16 * 16384], 임시파일 = new int[16384], 파일명 = new int[512];
    static int[] 상종류 = new int[8192], 상가 = new int[8192], 상나 = new int[8192], 문자열참조 = new int[8192];
    static int[] 함수명 = new int[512], 함수형 = new int[512], 함수권한 = new int[512], 함수주인 = new int[512];
    static int[] 함수시작 = new int[512], 함수끝 = new int[512], 함수스택 = new int[512], 함수지역 = new int[512];
    static int[] 함수인수수 = new int[512], 함수인수형 = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] 지역값 = new int[16384], 지역형 = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] 틀함수 = new int[128], 틀위치 = new int[128], 틀스택 = new int[128], 틀명령 = new int[128], 틀초기화 = new int[128];
    static int[] 종이름 = new int[16], 종크기 = new int[16], 종부모 = new int[16], 종상태 = new int[16], 종칸수 = new int[16], 종초기화 = new int[16];
    static int[] 종접면 = new int[16 * 16], 종접면수 = new int[16];
    static int[] 칸이름 = new int[512], 칸형 = new int[512], 칸주인 = new int[512], 칸권한 = new int[512], 칸위치 = new int[512], 칸값 = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], 배열원소 = new int[32768], 정수저장 = new int[256];
    static int Bunene, 읽기위치, 함수수, 클래스명, 틀 = -1, 힙끝 = 1, 반환형;
    static int 종수, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, 표시수, 수거횟수;
    static int 현재가닥, 가닥수 = 1, 시작종;
    static int[] 가닥틀 = new int[4], 가닥상태 = new int[4], 가닥객체 = new int[4], 가닥대상 = new int[4], 가닥대기 = new int[4];
    static boolean Kiremya, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], 종가닥 = new int[16];

    static void 실패(String 말) {
        if (Kiremya) return;
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
        if (분류코드 != 0 && 틀 >= 0) { 예외던짐(분류코드, 말); return; }
        사용자.쓰기("JVM error: "); 사용자.쓰기(말); 사용자.문자쓰기(10); Kiremya = true;
    }
    static boolean 범위(int Tandika, int 길이) {
        if (Tandika < 0 || Tandika >= Fayiro.length || 길이 < 0) return false;
        int 종 = Tandika / 16384;
        return Tandika % 16384 <= 종크기[종] && 길이 <= 종크기[종] - Tandika % 16384;
    }
    static int 바이트() {
        if (!범위(읽기위치, 1)) { 실패("truncated class file"); return 0; }
        return Fayiro[읽기위치++];
    }
    static int 짧은수() { return 바이트() << 8 | 바이트(); }
    static int 정수() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int 길이) { if (!범위(읽기위치, 길이)) 실패("invalid attribute size"); else 읽기위치 += 길이; }
    static boolean 상검사(int 수, int 종류) {
        if (수 <= 0 || 수 >= 상종류.length || 상종류[수] != 종류) { 실패("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Tandika, int 길이, String 말) {
        if (!범위(Tandika, 길이)) return false;
        int 읽는자리 = Tandika, 끝 = Tandika + 길이;
        for (int 반복자리 = 0; 반복자리 < 말.length(); 반복자리++) {
            int 문자값 = 말.charAt(반복자리);
            if (문자값 > 0 && 문자값 < 128) { if (읽는자리 >= 끝 || Fayiro[읽는자리++] != 문자값) return false; }
            else if (문자값 < 2048) {
                if (읽는자리 + 2 > 끝 || Fayiro[읽는자리++] != (192 | (문자값 >> 6)) || Fayiro[읽는자리++] != (128 | (문자값 & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Fayiro[읽는자리++] != (224 | (문자값 >> 12)) || Fayiro[읽는자리++] != (128 | ((문자값 >> 6) & 63)) || Fayiro[읽는자리++] != (128 | (문자값 & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean 말(int 상수, String 말) { return 상검사(상수, 1) && 구간(상가[상수], 상나[상수], 말); }
    static boolean 같은말(int 가, int 나) {
        if (!상검사(가, 1) || !상검사(나, 1) || 상나[가] != 상나[나]) return false;
        for (int 수 = 0; 수 < 상나[가]; 수++) if (Fayiro[상가[가] + 수] != Fayiro[상가[나] + 수]) return false;
        return true;
    }
    static int 클래스문자(int 수) { return 상검사(수, 7) && 상검사(상가[수], 1) ? 상가[수] : 0; }
    static int 참조이름(int 수) { return 상검사(수, 12) && 상검사(상가[수], 1) ? 상가[수] : 0; }
    static int 참조형식(int 수) { return 상검사(수, 12) && 상검사(상나[수], 1) ? 상나[수] : 0; }
    static int 서술형(int 끝, boolean 빈형) {
        if (읽기위치 >= 끝) { 실패("invalid descriptor"); return 0; }
        int 값 = 바이트();
        if (값 == 'V' && 빈형) return 0;
        if (값 == 'I' || 값 == 'B' || 값 == 'C' || 값 == 'S' || 값 == 'Z') return 1;
        if (값 == '[') { 서술형(끝, false); return 2; }
        if (값 == 'L') {
            int Tandika = 읽기위치;
            while (읽기위치 < 끝 && Fayiro[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Tandika) 실패("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        실패("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int 함수) {
        int 이전 = 읽기위치, 수 = 함수형[함수];
        if (!상검사(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + 상나[수];
        if (바이트() != '(') 실패("invalid method descriptor");
        int 개수 = 0;
        while (!Kiremya && 읽기위치 < 끝 && Fayiro[읽기위치] != ')') {
            if (개수 == 16) { 실패("too many method arguments"); break; }
            함수인수형[함수 * 16 + 개수++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || 바이트() != ')') 실패("invalid method descriptor");
        함수반환[함수] = 서술형(끝, true); 함수인수수[함수] = 개수;
        if (읽기위치 != 끝) 실패("invalid method descriptor");
        읽기위치 = 이전;
    }
    static int 상번호() { int 값 = 짧은수(); return 값 == 0 ? 0 : 현재읽는종 * 512 + 값; }
    static int 명상수() { return 함수주인[틀함수[틀]] * 512 + 명짧(); }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !Kiremya; 수++) { 상검사(상번호(), 1); 건너(정수()); }
    }
    static int 명령길이(int 값) {
        if (값 == 16 || 값 == 18 || 값 == 21 || 값 == 25 || 값 == 54 || 값 == 58 || 값 == 188) return 2;
        if (값 == 17 || 값 == 19 || 값 == 132 || 값 >= 153 && 값 <= 167
            || 값 >= 178 && 값 <= 184 || 값 == 187 || 값 == 189 || 값 == 192 || 값 == 193 || 값 == 198 || 값 == 199) return 3;
        if (값 == 185 || 값 == 200) return 5;
        if (값 >= 0 && 값 <= 8 || 값 >= 26 && 값 <= 29 || 값 >= 42 && 값 <= 46 || 값 >= 50 && 값 <= 53
            || 값 >= 59 && 값 <= 62 || 값 >= 75 && 값 <= 79 || 값 >= 83 && 값 <= 95
            || 값 == 96 || 값 == 100 || 값 == 104 || 값 == 108 || 값 == 112 || 값 == 116
            || 값 == 120 || 값 == 122 || 값 == 124 || 값 == 126 || 값 == 128 || 값 == 130
            || 값 >= 145 && 값 <= 147 || 값 == 172 || 값 == 176 || 값 == 177 || 값 == 190 || 값 == 191
            || 값 == 194 || 값 == 195) return 1;
        return 0;
    }
    static int 위치정수(int 읽는자리) {
        if (!범위(읽는자리, 4)) { 실패("truncated bytecode operand"); return 0; }
        return Fayiro[읽는자리] << 24 | Fayiro[읽는자리 + 1] << 16 | Fayiro[읽는자리 + 2] << 8 | Fayiro[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Tandika, int 끝) {
        int 값 = Fayiro[읽는자리], 길이 = 명령길이(값);
        if (값 == 170 || 값 == 171) {
            int 기준자리 = 읽는자리 + 1;
            while ((기준자리 - Tandika) % 4 != 0) 기준자리++;
            if (끝 - 기준자리 < (값 == 170 ? 12 : 8)) return 0;
            int 항목수 = 값 == 170 ? 위치정수(기준자리 + 8) - 위치정수(기준자리 + 4) + 1 : 위치정수(기준자리 + 4);
            if (항목수 < 0 || 항목수 > 2048) return 0;
            길이 = 기준자리 - 읽는자리 + (값 == 170 ? 12 + 4 * 항목수 : 8 + 8 * 항목수);
        }
        if (값 == 196 && 읽는자리 + 1 < 끝) {
            int 단어값 = Fayiro[읽는자리 + 1]; 길이 = 단어값 == 132 ? 6 : (단어값 == 21 || 단어값 == 25 || 단어값 == 54 || 단어값 == 58) ? 4 : 0;
        }
        return 길이 > 0 && 길이 <= 끝 - 읽는자리 ? 길이 : 0;
    }
    static void 목적검사(int 목적, int 함수) {
        if (목적 < 함수시작[함수] || 목적 >= 함수끝[함수] || 경계[목적] != 함수 + 1) 실패("invalid branch target");
    }
    static void 클래스읽기(int 종) {
        현재읽는종 = 종; 읽기위치 = 종 * 16384; Bunene = 읽기위치 + 종크기[종];
        if (정수() != 0xcafebabe) { 실패("not a class file"); return; }
        int 부판 = 짧은수(), 판 = 짧은수();
        if (판 < 45 || 판 > 52 || 부판 != 0) { 실패("supported class versions: 45..52, minor 0"); return; }
        int 상수수 = 짧은수(), 기준자리 = 종 * 512;
        if (상수수 < 1 || 상수수 > 512) { 실패("constant pool limit (511)"); return; }
        for (int 항목수 = 1; 항목수 < 상수수 && !Kiremya; 항목수++) {
            int 수 = 기준자리 + 항목수, 종류 = 바이트(); 상종류[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = 정수();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); 상나[수] = 상번호(); }
            else 실패("unsupported constant type");
        }
        int 권한 = 짧은수();
        if ((권한 & (0x2000 | 0x4000)) != 0) 실패("annotation/enum class unsupported");
        종이름[종] = 클래스문자(상번호());
        종부모[종] = 클래스문자(상번호());
        int 접면수 = 짧은수(); if (접면수 > 16) { 실패("interface count limit"); return; }
        종접면수[종] = 접면수;
        for (int 반복자리 = 0; 반복자리 < 접면수; 반복자리++) 종접면[종 * 16 + 반복자리] = 클래스문자(상번호());
        int 필드수 = 짧은수();
        if (필드수 > 512 - 칸수) { 실패("field count limit (512)"); return; }
        for (int 반복자리 = 0; 반복자리 < 필드수 && !Kiremya; 반복자리++) {
            int 파일번호 = 칸수++; 칸주인[파일번호] = 종; 칸권한[파일번호] = 짧은수(); 칸이름[파일번호] = 상번호(); 칸형[파일번호] = 상번호();
            상검사(칸이름[파일번호], 1); 상검사(칸형[파일번호], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[칸형[파일번호]]; int 분류코드 = 서술형(읽기위치 + 상나[칸형[파일번호]], false); 읽기위치 = 보존값;
            if ((칸권한[파일번호] & 8) == 0) 칸위치[파일번호] = 종칸수[종]++;
            int 속성값 = 짧은수();
            for (int 안쪽자리 = 0; 안쪽자리 < 속성값 && !Kiremya; 안쪽자리++) {
                int 이름상수 = 상번호(), 유효길이 = 정수();
                if (말(이름상수, "ConstantValue") && 유효길이 == 2) {
                    int 자료값 = 상번호();
                    if (분류코드 == 1 && 상검사(자료값, 3)) 칸값[파일번호] = 상가[자료값];
                    else if (분류코드 == 2 && 상검사(자료값, 8)) 칸값[파일번호] = 상문자(상가[자료값]);
                } else 건너(유효길이);
            }
        }
        int 개수 = 짧은수();
        if (개수 > 512 - 함수수) { 실패("method count limit (512)"); return; }
        for (int 반복자리 = 0; 반복자리 < 개수 && !Kiremya; 반복자리++) {
            int 수 = 함수수++; 함수주인[수] = 종;
            함수권한[수] = 짧은수(); 함수명[수] = 상번호(); 함수형[수] = 상번호();
            상검사(함수명[수], 1); 서술읽기(수);
            if ((함수권한[수] & 8) == 0) {
                if (함수인수수[수] == 16) { 실패("too many instance method arguments"); return; }
                for (int 비교자리 = 함수인수수[수]; 비교자리 > 0; 비교자리--) 함수인수형[수 * 16 + 비교자리] = 함수인수형[수 * 16 + 비교자리 - 1];
                함수인수형[수 * 16] = 2; 함수인수수[수]++;
            }
            if ((함수권한[수] & 0x100) != 0) 실패("user native method unsupported");
            if (말(함수명[수], "<clinit>")) 종초기화[종] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (함수주인[앞] == 종 && 같은말(함수명[앞], 함수명[수]) && 같은말(함수형[앞], 함수형[수])) 실패("duplicate method");
            int 속성수 = 짧은수();
            for (int 속성 = 0; 속성 < 속성수 && !Kiremya; 속성++) {
                int Linnya = 상번호(), 길이 = 정수(), Tandika = 읽기위치;
                if (!범위(Tandika, 길이)) { 실패("truncated method attribute"); break; }
                if (말(Linnya, "Code")) {
                    if (함수시작[수] != 0) 실패("duplicate Code attribute");
                    함수스택[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = 정수();
                    if (함수스택[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) 실패("method memory limits exceeded");
                    함수시작[수] = 읽기위치; 건너(코드길이); 함수끝[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { 실패("exception table limit"); return; }
                    for (int 안쪽자리 = 0; 안쪽자리 < 잡는수; 안쪽자리++) {
                        int 오류참조 = 잡기수++; 잡기함수[오류참조] = 수;
                        잡기시작[오류참조] = 함수시작[수] + 짧은수(); 잡기끝[오류참조] = 함수시작[수] + 짧은수();
                        잡기위치[오류참조] = 함수시작[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[오류참조] = 부호값 == 0 ? 0 : 클래스문자(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Tandika + 길이) 실패("Code attribute size mismatch");
                } else 건너(길이);
            }
            if ((함수권한[수] & 0x400) != 0) continue;
            if (함수시작[수] == 0) 실패("missing Code attribute");
            int 칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !Kiremya) {
                int 길이 = 길이읽기(칸, 함수시작[수], 함수끝[수]);
                if (길이 == 0) { 실패("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += 길이;
            }
            칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !Kiremya) {
                int 값 = Fayiro[칸];
                if (값 >= 153 && 값 <= 167 || 값 == 198 || 값 == 199) 목적검사(칸 + (short)(Fayiro[칸 + 1] << 8 | Fayiro[칸 + 2]), 수);
                if (값 == 200) 목적검사(칸 + 위치정수(칸 + 1), 수);
                if (값 == 170 || 값 == 171) {
                    int 읽는자리 = 칸 + 1; while ((읽는자리 - 함수시작[수]) % 4 != 0) 읽는자리++;
                    목적검사(칸 + 위치정수(읽는자리), 수);
                    int 항목수 = 값 == 170 ? 위치정수(읽는자리 + 8) - 위치정수(읽는자리 + 4) + 1 : 위치정수(읽는자리 + 4);
                    읽는자리 += 값 == 170 ? 12 : 8;
                    for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) 목적검사(칸 + 위치정수(읽는자리 + 안쪽자리 * (값 == 170 ? 4 : 8) + (값 == 170 ? 0 : 4)), 수);
                }
                칸 += 길이읽기(칸, 함수시작[수], 함수끝[수]);
            }
            for (int 안쪽자리 = 0; 안쪽자리 < 잡기수; 안쪽자리++) if (잡기함수[안쪽자리] == 수) {
                목적검사(잡기시작[안쪽자리], 수); 목적검사(잡기위치[안쪽자리], 수);
                if (잡기끝[안쪽자리] != 함수끝[수]) 목적검사(잡기끝[안쪽자리], 수);
                if (잡기시작[안쪽자리] >= 잡기끝[안쪽자리]) 실패("invalid exception range");
            }
        }
        if (!Kiremya) 속성건너();
        if (읽기위치 != Bunene) 실패("extra class file data");
    }
    static int 할당(int 종류, int 길이) { return 새기억(종류, 길이); }
    static boolean 객체(int 참조, int 종류) {
        if (!객체유효(참조)) return false;
        if (힙[참조] != 종류) { 실패("object type mismatch"); return false; }
        return true;
    }
    static int 상문자(int 번호) {
        if (!상검사(번호, 1)) return 0;
        if (문자열참조[번호] != 0) return 문자열참조[번호];
        int 참조 = 할당(1, 상나[번호]); if (Kiremya) return 0;
        int 끝 = 상가[번호] + 상나[번호], 수 = 상가[번호], 길이 = 0;
        while (수 < 끝 && !Kiremya) {
            int 값 = Fayiro[수++];
            if (값 == 0) 실패("invalid modified UTF-8");
            else if (값 >= 192 && 값 <= 223 && 수 < 끝) {
                int 다음 = Fayiro[수++];
                if ((다음 & 192) != 128) 실패("invalid modified UTF-8");
                값 = (값 & 31) << 6 | 다음 & 63;
                if (값 != 0 && 값 < 128) 실패("overlong modified UTF-8");
            } else if (값 >= 224 && 값 <= 239 && 수 + 1 < 끝) {
                int 가 = Fayiro[수++], 나 = Fayiro[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) 실패("invalid modified UTF-8");
                값 = (값 & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (값 < 2048) 실패("overlong modified UTF-8");
            } else if (값 >= 128) 실패("invalid modified UTF-8");
            힙[참조 + 2 + 길이++] = 값;
        }
        힙[참조 + 1] = 길이; 문자열참조[번호] = 참조; return 참조;
    }
    static int 호스트문자(String 값) {
        int 참조 = 할당(1, 값.length()); if (Kiremya) return 0;
        for (int 수 = 0; 수 < 값.length(); 수++) 힙[참조 + 2 + 수] = 값.charAt(수);
        return 참조;
    }
    static void 글쓰기(int 참조) {
        if (참조 == 0) { 사용자.쓰기("null"); return; }
        if (!객체(참조, 1)) return;
        for (int 수 = 0; 수 < 힙[참조 + 1]; 수++) 사용자.문자쓰기(힙[참조 + 2 + 수]);
    }
    static int 수문자(int 값) {
        int 참조 = 할당(1, 11); if (Kiremya) return 0;
        int 길이 = 0;
        if (값 < 0) 힙[참조 + 2 + 길이++] = '-'; else 값 = -값;
        int 자리 = 1000000000; boolean Tandika = false;
        while (자리 != 0) {
            int 수 = -(값 / 자리);
            if (수 != 0 || Tandika || 자리 == 1) { 힙[참조 + 2 + 길이++] = '0' + 수; Tandika = true; }
            값 %= 자리; 자리 /= 10;
        }
        힙[참조 + 1] = 길이; return 참조;
    }
    static int 정수해독(int 참조) {
        if (!객체(참조, 1)) return 0;
        int 길이 = 힙[참조 + 1], 수 = 0, 값 = 0; boolean 음수 = false;
        if (길이 > 0 && (힙[참조 + 2] == '-' || 힙[참조 + 2] == '+')) { 음수 = 힙[참조 + 2] == '-'; 수++; }
        if (수 == 길이) 실패("NumberFormatException");
        for (; 수 < 길이 && !Kiremya; 수++) {
            int 숫자 = 힙[참조 + 2 + 수] - '0';
            if (숫자 < 0 || 숫자 > 9 || 값 < -214748364 || 값 == -214748364 && 숫자 > (음수 ? 8 : 7)) 실패("NumberFormatException");
            값 = 값 * 10 - 숫자;
        }
        return 음수 ? 값 : -값;
    }
    static void 넣기(int 값, int 형) {
        if (Kiremya) return;
        if (틀 < 0 || 틀스택[틀] >= 함수스택[틀함수[틀]]) { 실패("operand stack overflow"); return; }
        int 칸 = 틀 * 128 + 틀스택[틀]++; 스택값[칸] = 값; 스택형[칸] = 형;
    }
    static int 빼기(int 형) {
        if (Kiremya) return 0;
        if (틀 < 0 || 틀스택[틀] < 1) { 실패("operand stack underflow"); return 0; }
        int 칸 = 틀 * 128 + --틀스택[틀]; 반환형 = 스택형[칸];
        if (형 != 0 && 반환형 != 형) 실패("operand type mismatch");
        if (반환형 == 2) 보호(스택값[칸]);
        return 스택값[칸];
    }
    static void 지역읽기(int 번호, int 형) {
        if (번호 >= 함수지역[틀함수[틀]] || 번호 < 0 || 지역형[틀 * 128 + 번호] != 형) { 실패("invalid or uninitialized local"); return; }
        넣기(지역값[틀 * 128 + 번호], 형);
    }
    static void 지역쓰기(int 번호, int 형) {
        if (번호 >= 함수지역[틀함수[틀]] || 번호 < 0) { 실패("local index out of range"); return; }
        int 값 = 빼기(형); 지역값[틀 * 128 + 번호] = 값; 지역형[틀 * 128 + 번호] = 형;
    }
    static int 명바() {
        int 위치 = 틀위치[틀];
        if (위치 < 함수시작[틀함수[틀]] || 위치 >= 함수끝[틀함수[틀]]) { 실패("instruction pointer out of range"); return 0; }
        틀위치[틀]++; return Fayiro[위치];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void 이동(int 위치) {
        int 함수 = 틀함수[틀];
        if (위치 < 함수시작[함수] || 위치 >= 함수끝[함수] || 경계[위치] != 함수 + 1) 실패("invalid branch target");
        else 틀위치[틀] = 위치;
    }
    static void 호출(int 함수) {
        if (틀 % 32 == 31) { 실패("call stack limit (32)"); return; }
        int 다음 = 틀 + 1;
        for (int 수 = 0; 수 < 128; 수++) 지역형[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[함수] - 1; 수 >= 0; 수--) {
            지역값[다음 * 128 + 수] = 빼기(함수인수형[함수 * 16 + 수]); 지역형[다음 * 128 + 수] = 함수인수형[함수 * 16 + 수];
        }
        if (Kiremya) return;
        틀 = 다음; 틀초기화[틀] = 0; 틀함수[틀] = 함수; 틀위치[틀] = 함수시작[함수]; 틀스택[틀] = 0;
    }
    static void 반환(int 형) {
        if (형 != 함수반환[틀함수[틀]]) { 실패("return type mismatch"); return; }
        int 값 = 형 == 0 ? 0 : 빼기(형);
        if (틀초기화[틀] != 0) 종상태[틀초기화[틀] - 1] = 2;
        if (틀잠금[틀] != 0) { 잠금풀기(틀잠금[틀]); 틀잠금[틀] = 0; }
        틀--; if (틀 >= 현재가닥 * 32 && 형 != 0) 넣기(값, 형);
    }
    static int[] 흐름파일이름 = new int[64];
    static void 파일흐름호출(int 소유, int Linnya, int 형식, int Mulimu) {
        boolean 출력 = 말(소유, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (Mulimu == 183 && 말(Linnya, "<init>")) {
            boolean 이어 = false;
            if (출력 && 말(형식, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!말(형식, "(Ljava/lang/String;)V")) { 실패("unsupported file stream constructor"); return; }
            int 파일이름 = 빼기(2), 흐름 = 빼기(2);
            if (!객체(파일이름, 1) || !객체(흐름, 종류) || Kiremya) return;
            if (힙[흐름 + 3] != 0) { 실패("file stream already initialized"); return; }
            int 길이 = 힙[파일이름 + 1];
            if (길이 < 1 || 길이 > 63) { 실패("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < 길이; 칸++) {
                int 값 = 힙[파일이름 + 2 + 칸];
                if (값 < 1) { 실패("invalid file stream path"); return; }
                흐름파일이름[칸] = 값;
            }
            흐름파일이름[길이] = 0;
            int 서술자 = 사용자.파일서술자열기(흐름파일이름, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { 실패("FileNotFoundException: file open failed"); return; }
            힙[흐름 + 2] = 서술자; 힙[흐름 + 3] = 1;
            return;
        }
        if (Mulimu != 182) { 실패("invalid file stream invocation"); return; }
        if ((출력 && 말(Linnya, "write") || !출력 && 말(Linnya, "read"))
            && (말(형식, 출력 ? "([B)V" : "([B)I") || 말(형식, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean 범위값 = 말(형식, 출력 ? "([BII)V" : "([BII)I");
            int 항목수 = 범위값 ? 빼기(1) : 0, 시작점 = 범위값 ? 빼기(1) : 0, 자료배열 = 빼기(2), 객체참조 = 빼기(2);
            if (!객체(자료배열, 20) || !객체(객체참조, 종류)) return;
            if (!범위값) 항목수 = 힙[자료배열 + 1];
            if (시작점 < 0 || 항목수 < 0 || 시작점 > 힙[자료배열 + 1] - 항목수) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[객체참조 + 3] == 0 || 힙[객체참조 + 2] < 0) { 실패("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < 항목수 && !Kiremya) {
                int 반환값 = 출력 ? 사용자.파일한바이트쓰기(힙[객체참조 + 2], 힙[자료배열 + 2 + 시작점 + 완료수]) : 사용자.파일한바이트읽기(힙[객체참조 + 2]);
                if (반환값 < 0) { 실패(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[자료배열 + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(항목수 != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && 말(Linnya, "flush") && 말(형식, "()V")) { int 객체참조 = 빼기(2); if (객체(객체참조, 종류) && 힙[객체참조 + 2] < 0) 실패("IOException: stream closed"); return; }
        int 동작 = -1, 값 = 0;
        if (말(Linnya, "close") && 말(형식, "()V")) 동작 = 0;
        if (!출력 && 말(Linnya, "read") && 말(형식, "()I")) 동작 = 1;
        if (출력 && 말(Linnya, "write") && 말(형식, "(I)V")) { 동작 = 2; 값 = 빼기(1); }
        if (동작 < 0) { 실패("unsupported file stream method"); return; }
        int 흐름 = 빼기(2);
        if (!객체(흐름, 종류) || Kiremya) return;
        if (힙[흐름 + 3] == 0) { 실패("uninitialized file stream"); return; }
        int 서술자 = 힙[흐름 + 2];
        if (동작 == 0) {
            if (서술자 >= 0 && 사용자.파일서술자닫기(서술자) < 0) 실패("IOException: close failed");
            힙[흐름 + 2] = -1; return;
        }
        if (서술자 < 0) { 실패("IOException: stream closed"); return; }
        if (동작 == 1) {
            int KIGENDERWA = 사용자.파일한바이트읽기(서술자);
            if (KIGENDERWA < -1) 실패("IOException: read failed"); else 넣기(KIGENDERWA == 256 ? -1 : KIGENDERWA, 1);
        } else if (사용자.파일한바이트쓰기(서술자, 값) != 1) 실패("IOException: write failed");
    }
    static void 함수호출(int 번호, int Mulimu) {
        if (번호 <= 0 || 번호 >= 상종류.length || (상종류[번호] != 10 && 상종류[번호] != 11)) { 실패("invalid method reference"); return; }
        int 소유 = 클래스문자(상가[번호]), Linnya = 참조이름(상나[번호]), 형식 = 참조형식(상나[번호]);
        if (Kiremya) return;
        if (기본호출(소유, Linnya, 형식, Mulimu)) return;
        if (말(소유, "java/io/FileInputStream") || 말(소유, "java/io/FileOutputStream")) {
            파일흐름호출(소유, Linnya, 형식, Mulimu); return;
        }
        if (Mulimu == 184 && 말(소유, "java/lang/Integer") && 말(Linnya, "parseInt") && 말(형식, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Mulimu == 182 && 말(소유, "java/io/PrintStream") && (말(Linnya, "println") || 말(Linnya, "print"))) {
            int 형 = 0, 값 = 0;
            if (말(형식, "(I)V")) { 형 = 1; 값 = 빼기(1); }
            else if (말(형식, "(Z)V")) { 형 = 2; 값 = 빼기(1); }
            else if (말(형식, "(C)V")) { 형 = 3; 값 = 빼기(1); }
            else if (말(형식, "(Ljava/lang/String;)V")) { 형 = 4; 값 = 빼기(2); }
            else if (!말(형식, "()V") || !말(Linnya, "println")) 실패("unsupported print descriptor");
            if (빼기(2) != -1) 실패("invalid PrintStream receiver");
            if (Kiremya) return;
            if (형 == 1) 자바도구.수쓰기(값);
            if (형 == 2) 사용자.쓰기(값 == 0 ? "false" : "true");
            if (형 == 3) 사용자.문자쓰기(값 & 65535);
            if (형 == 4) 글쓰기(값);
            if (말(Linnya, "println")) 사용자.문자쓰기(10);
            return;
        }
        if (Mulimu == 182 && 말(소유, "java/lang/String")) {
            if (말(Linnya, "length") && 말(형식, "()I")) {
                int 참조 = 빼기(2); if (객체(참조, 1)) 넣기(힙[참조 + 1], 1); return;
            }
            if (말(Linnya, "charAt") && 말(형식, "(I)C")) {
                int 첨자 = 빼기(1), 참조 = 빼기(2);
                if (객체(참조, 1)) {
                    if (첨자 < 0 || 첨자 >= 힙[참조 + 1]) 실패("StringIndexOutOfBoundsException"); else 넣기(힙[참조 + 2 + 첨자], 1);
                }
                return;
            }
        }
        if (말(소유, "java/lang/StringBuilder")) {
            if (Mulimu == 183 && 말(Linnya, "<init>") && 말(형식, "()V")) { 객체(빼기(2), 4); return; }
            if (Mulimu == 182 && 말(Linnya, "toString") && 말(형식, "()Ljava/lang/String;")) {
                int 참조 = 빼기(2); if (객체(참조, 4)) 넣기(힙[참조 + 2] == 0 ? 호스트문자("") : 힙[참조 + 2], 2); return;
            }
            if (Mulimu == 182 && 말(Linnya, "append")) {
                int Bigambo = 0;
                if (말(형식, "(I)Ljava/lang/StringBuilder;")) Bigambo = 수문자(빼기(1));
                else if (말(형식, "(Z)Ljava/lang/StringBuilder;")) Bigambo = 호스트문자(빼기(1) == 0 ? "false" : "true");
                else if (말(형식, "(C)Ljava/lang/StringBuilder;")) {
                    int 값 = 빼기(1); Bigambo = 할당(1, 1); if (!Kiremya) 힙[Bigambo + 2] = 값 & 65535;
                }
                else if (말(형식, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Bigambo = 빼기(2); if (Bigambo == 0) Bigambo = 호스트문자("null"); }
                else { 실패("unsupported StringBuilder append"); return; }
                int 참조 = 빼기(2); if (!객체(참조, 4) || !객체(Bigambo, 1)) return;
                int 앞 = 힙[참조 + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], 뒤길이 = 힙[Bigambo + 1];
                int 새글 = 할당(1, 앞길이 + 뒤길이); if (Kiremya) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < 뒤길이; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[Bigambo + 2 + 수];
                힙[참조 + 2] = 새글; 넣기(참조, 2); return;
            }
        }
        int 종 = 종찾기(소유); if (종 < 0 || Kiremya) return;
        int 파일번호 = 함수찾기(종, Linnya, 형식);
        if (파일번호 < 0) {
            for (int 문자값 = 종, 항목수 = 0; 문자값 >= 0 && 항목수 < 16; 항목수++, 문자값 = 부모종(문자값))
                if (말(종부모[문자값], "java/lang/Thread")) { 가닥호출(Linnya, 형식, Mulimu); return; }
            실패("NoSuchMethodError"); return;
        }
        if (((함수권한[파일번호] & 8) != 0) != (Mulimu == 184)) { 실패("method static/instance mismatch"); return; }
        if (Mulimu == 184) { if (!초기화(함수주인[파일번호], 틀명령[틀])) return; }
        else {
            int 읽는자리 = 틀스택[틀] - 함수인수수[파일번호];
            if (읽는자리 < 0 || 스택형[틀 * 128 + 읽는자리] != 2) { 실패("invalid method receiver"); return; }
            int 객체참조 = 스택값[틀 * 128 + 읽는자리];
            if (!객체유효(객체참조)) return;
            if (힙[객체참조] < 32 || !종포함(힙[객체참조] - 32, 소유)) { 실패("method receiver type mismatch"); return; }
            if (Mulimu != 183) 파일번호 = 함수찾기(힙[객체참조] - 32, Linnya, 형식);
        }
        if (파일번호 < 0 || (함수권한[파일번호] & 0x400) != 0) { 실패("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((함수권한[파일번호] & 32) != 0) {
            if (Mulimu == 184) { int 문자값 = 함수주인[파일번호]; if (종잠금[문자값] == 0) 종잠금[문자값] = 할당(8, 0); 잠금참조 = 종잠금[문자값]; }
            else 잠금참조 = 스택값[틀 * 128 + 틀스택[틀] - 함수인수수[파일번호]];
            if (!잠금얻기(잠금참조)) { if (!Kiremya) 틀위치[틀] = 틀명령[틀]; return; }
        }
        호출(파일번호); if (!Kiremya) 틀잠금[틀] = 잠금참조;
    }
    static boolean 배열저장가능(int 배열참조, int 자료값) {
        if (자료값 == 0 || 배열원소[배열참조] == 0) return true;
        boolean 성공여부 = 배열원소[배열참조] == -1 ? (자료값 > 0 && 자료값 < 힙끝 && 힙[자료값] == 1) : 맞는객체(자료값, 배열원소[배열참조]);
        if (!성공여부 && !Kiremya) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int 배열칸(int 참조, int 첨자, int 형) {
        if (!객체(참조, 형)) return 0;
        if (첨자 < 0 || 첨자 >= 힙[참조 + 1]) { 실패("ArrayIndexOutOfBoundsException"); return 0; }
        return 참조 + 2 + 첨자;
    }
    static void 실행() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (Kiremya) { if (던진객체 != 0) 예외처리(); if (Kiremya || 틀 < 현재가닥 * 32) break; }
            if (틀 < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!가닥바꾸기()) break; 조각 = 100; }
            if (틀 == 0 && 종상태[시작종] != 2 && !초기화(시작종, 틀위치[틀])) continue;
            if (틀 == 현재가닥 * 32 && 현재가닥 != 0 && (함수권한[틀함수[틀]] & 32) != 0 && 틀잠금[틀] == 0) {
                int 객체참조 = 가닥대상[현재가닥]; if (!잠금얻기(객체참조)) { if (Kiremya) break; continue; } 틀잠금[틀] = 객체참조;
            }
            잠시수 = 0;
            if (--남음 == 0) { 실패("instruction limit (500000)"); break; }
            int Tandika = 틀위치[틀]; 틀명령[틀] = Tandika; int 값 = 명바();
            if (Kiremya) break;
            if (값 == 0) continue;
            if (값 == 1) { 넣기(0, 2); continue; }
            if (값 >= 2 && 값 <= 8) { 넣기(값 - 3, 1); continue; }
            if (값 == 16) { 넣기((byte)명바(), 1); continue; }
            if (값 == 17) { 넣기((short)명짧(), 1); continue; }
            if (값 == 18 || 값 == 19) {
                int 수 = 함수주인[틀함수[틀]] * 512 + (값 == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= 상종류.length) 실패("invalid ldc constant");
                else if (상종류[수] == 3) 넣기(상가[수], 1);
                else if (상종류[수] == 8) 넣기(상문자(상가[수]), 2);
                else 실패("unsupported ldc constant");
                continue;
            }
            if (값 == 21 || 값 == 25) { 지역읽기(명바(), 값 == 21 ? 1 : 2); continue; }
            if (값 >= 26 && 값 <= 29) { 지역읽기(값 - 26, 1); continue; }
            if (값 >= 42 && 값 <= 45) { 지역읽기(값 - 42, 2); continue; }
            if (값 == 54 || 값 == 58) { 지역쓰기(명바(), 값 == 54 ? 1 : 2); continue; }
            if (값 >= 59 && 값 <= 62) { 지역쓰기(값 - 59, 1); continue; }
            if (값 >= 75 && 값 <= 78) { 지역쓰기(값 - 75, 2); continue; }
            if (값 == 46 || 값 >= 50 && 값 <= 53) {
                int 항목자리 = 빼기(1), 객체참조 = 빼기(2), 분류코드 = 값 == 46 ? 2 : 값 == 50 ? 3 : 값 == 51 ? 20 : 값 == 52 ? 22 : 23;
                if (값 == 51 && 객체참조 > 0 && 객체참조 < 힙끝 && 힙[객체참조] == 21) 분류코드 = 21;
                int 읽는자리 = 배열칸(객체참조, 항목자리, 분류코드); if (!Kiremya) 넣기(힙[읽는자리], 값 == 50 ? 2 : 1); continue;
            }
            if (값 == 79 || 값 >= 83 && 값 <= 86) {
                int 항목참조 = 빼기(값 == 83 ? 2 : 1), 항목자리 = 빼기(1), 객체참조 = 빼기(2), 분류코드 = 값 == 79 ? 2 : 값 == 83 ? 3 : 값 == 84 ? 20 : 값 == 85 ? 22 : 23;
                if (값 == 84 && 객체참조 > 0 && 객체참조 < 힙끝 && 힙[객체참조] == 21) 분류코드 = 21;
                int 읽는자리 = 배열칸(객체참조, 항목자리, 분류코드);
                if (!Kiremya && 분류코드 == 3 && !배열저장가능(객체참조, 항목참조)) continue;
                if (!Kiremya) 힙[읽는자리] = 분류코드 == 20 ? (byte)항목참조 : 분류코드 == 21 ? 항목참조 & 1 : 분류코드 == 22 ? (char)항목참조 : 분류코드 == 23 ? (short)항목참조 : 항목참조;
                continue;
            }
            if (값 >= 87 && 값 <= 95) { 스택명령(값); continue; }
            if (값 == 96 || 값 == 100 || 값 == 104 || 값 == 108 || 값 == 112 || 값 == 120
                || 값 == 122 || 값 == 124 || 값 == 126 || 값 == 128 || 값 == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), KIGENDERWA = 0;
                if ((값 == 108 || 값 == 112) && 나 == 0) { 실패("ArithmeticException: / by zero"); continue; }
                if (값 == 96) KIGENDERWA = 가 + 나;
                if (값 == 100) KIGENDERWA = 가 - 나;
                if (값 == 104) KIGENDERWA = 가 * 나;
                if (값 == 108) KIGENDERWA = 가 / 나;
                if (값 == 112) KIGENDERWA = 가 % 나;
                if (값 == 120) KIGENDERWA = 가 << 나;
                if (값 == 122) KIGENDERWA = 가 >> 나;
                if (값 == 124) KIGENDERWA = 가 >>> 나;
                if (값 == 126) KIGENDERWA = 가 & 나;
                if (값 == 128) KIGENDERWA = 가 | 나;
                if (값 == 130) KIGENDERWA = 가 ^ 나;
                넣기(KIGENDERWA, 1); continue;
            }
            if (값 == 116) { 넣기(-빼기(1), 1); continue; }
            if (값 == 132) {
                int 지역 = 명바(), 증분 = (byte)명바(); 지역읽기(지역, 1); 넣기(빼기(1) + 증분, 1); 지역쓰기(지역, 1); continue;
            }
            if (값 >= 145 && 값 <= 147) {
                int 수 = 빼기(1); 넣기(값 == 145 ? (byte)수 : 값 == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (값 >= 153 && 값 <= 167 || 값 == 198 || 값 == 199) {
                int 목적 = Tandika + (short)명짧(); boolean 갈까 = 값 == 167;
                if (값 >= 153 && 값 <= 158) {
                    int 수 = 빼기(1); 갈까 = 값 == 153 ? 수 == 0 : 값 == 154 ? 수 != 0 : 값 == 155 ? 수 < 0 : 값 == 156 ? 수 >= 0 : 값 == 157 ? 수 > 0 : 수 <= 0;
                } else if (값 >= 159 && 값 <= 166) {
                    int 나 = 빼기(값 >= 165 ? 2 : 1), 가 = 빼기(값 >= 165 ? 2 : 1);
                    갈까 = 값 == 159 || 값 == 165 ? 가 == 나 : 값 == 160 || 값 == 166 ? 가 != 나 : 값 == 161 ? 가 < 나 : 값 == 162 ? 가 >= 나 : 값 == 163 ? 가 > 나 : 가 <= 나;
                } else if (값 == 198 || 값 == 199) { int 수 = 빼기(2); 갈까 = 값 == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) 이동(목적); continue;
            }
            if (값 == 172 || 값 == 176 || 값 == 177) { 반환(값 == 172 ? 1 : 값 == 176 ? 2 : 0); continue; }
            if (값 >= 178 && 값 <= 181) { 필드호출(명상수(), 값, Tandika); continue; }
            if (값 >= 182 && 값 <= 185) {
                int 부호값 = 명상수();
                if (값 == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { 실패("invalid invokeinterface operands"); continue; } }
                함수호출(부호값, 값); continue;
            }
            if (값 == 187) { 새객체(클래스문자(명상수()), Tandika); continue; }
            if (값 == 188 || 값 == 189) {
                int 분류코드 = 3, 원소형식 = 0;
                if (값 == 188) { int 임시값 = 명바(); 분류코드 = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else 원소형식 = 클래스문자(명상수());
                if (분류코드 == 0) { 실패("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), 객체참조 = 할당(분류코드, 유효길이); if (!Kiremya) 배열원소[객체참조] = 원소형식; 넣기(객체참조, 2); continue;
            }
            if (값 == 190) {
                int 객체참조 = 빼기(2);
                if (객체유효(객체참조)) { int 비교자리 = 힙[객체참조]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) 실패("not an array"); else 넣기(힙[객체참조 + 1], 1); }
                continue;
            }
            if (값 == 191) {
                int 객체참조 = 빼기(2); if (객체유효(객체참조)) { if (힙[객체참조] != 9) 실패("athrow requires supported Throwable"); else { 던진객체 = 객체참조; Kiremya = true; } }
                continue;
            }
            if (값 == 192 || 값 == 193) {
                int 이름상수 = 클래스문자(명상수()), 객체참조 = 빼기(2); boolean 일치여부 = 맞는객체(객체참조, 이름상수);
                if (값 == 193) 넣기(객체참조 != 0 && 일치여부 ? 1 : 0, 1);
                else { if (!일치여부 && !Kiremya) 실패("ClassCastException"); 넣기(객체참조, 2); }
                continue;
            }
            if (값 == 170 || 값 == 171) {
                int 읽는자리 = Tandika + 1, 파일번호 = 틀함수[틀], 키참조 = 빼기(1);
                while ((읽는자리 - 함수시작[파일번호]) % 4 != 0) 읽는자리++;
                int 대상값 = 위치정수(읽는자리);
                if (값 == 170) { int 낮은값 = 위치정수(읽는자리 + 4), 높은값 = 위치정수(읽는자리 + 8); if (키참조 >= 낮은값 && 키참조 <= 높은값) 대상값 = 위치정수(읽는자리 + 12 + (키참조 - 낮은값) * 4); }
                else { int 총수 = 위치정수(읽는자리 + 4); for (int 반복자리 = 0; 반복자리 < 총수; 반복자리++) if (위치정수(읽는자리 + 8 + 반복자리 * 8) == 키참조) 대상값 = 위치정수(읽는자리 + 12 + 반복자리 * 8); }
                이동(Tandika + 대상값); continue;
            }
            if (값 == 200) { 이동(Tandika + 위치정수(Tandika + 1)); continue; }
            if (값 == 194 || 값 == 195) {
                int 객체참조 = 빼기(2);
                if (값 == 195) 잠금풀기(객체참조);
                else if (!잠금얻기(객체참조) && !Kiremya) { 넣기(객체참조, 2); 틀위치[틀] = Tandika; }
                continue;
            }
            if (값 == 196) {
                int 명령코드 = 명바(), 항목자리 = 명짧();
                if (명령코드 == 21 || 명령코드 == 25) 지역읽기(항목자리, 명령코드 == 21 ? 1 : 2);
                else if (명령코드 == 54 || 명령코드 == 58) 지역쓰기(항목자리, 명령코드 == 54 ? 1 : 2);
                else if (명령코드 == 132) { int 변화량 = (short)명짧(); 지역읽기(항목자리, 1); 넣기(빼기(1) + 변화량, 1); 지역쓰기(항목자리, 1); }
                else 실패("unsupported wide opcode");
                continue;
            }
            실패("unsupported bytecode");
        }
    }
    static int 종찾기(int Linnya) {
        for (int 반복자리 = 0; 반복자리 < 종수; 반복자리++) if (종이름[반복자리] != 0 && 같은말(종이름[반복자리], Linnya)) return 반복자리;
        return 종적재(상문자(Linnya));
    }
    static int 종적재(int 이름글) {
        if (!객체(이름글, 1)) return -1;
        int 길이 = 힙[이름글 + 1];
        if (길이 < 1 || 길이 > 505 || 종수 == 16) { 실패("class name/count limit"); return -1; }
        for (int 반복자리 = 0; 반복자리 < 길이; 반복자리++) { int 문자값 = 힙[이름글 + 2 + 반복자리]; 파일명[반복자리] = 문자값 == '/' ? '.' : 문자값; }
        파일명[길이] = '.'; 파일명[길이 + 1] = 'c'; 파일명[길이 + 2] = 'l'; 파일명[길이 + 3] = 'a'; 파일명[길이 + 4] = 's'; 파일명[길이 + 5] = 's'; 파일명[길이 + 6] = 0;
        int Bunene = 사용자.파일읽기(파일명, 임시파일);
        if (Bunene < 0) { 실패("ClassNotFoundException"); return -1; }
        int 종 = 종수++; 종크기[종] = Bunene;
        for (int 반복자리 = 0; 반복자리 < Bunene; 반복자리++) Fayiro[종 * 16384 + 반복자리] = 임시파일[반복자리];
        클래스읽기(종); if (Kiremya) return -1;
        int 실제 = 상문자(종이름[종]);
        if (!글같음(실제, 이름글, true)) { 실패("class name does not match file"); return -1; }
        int 부모 = 종부모[종];
        if (부모 != 0 && !말(부모, "java/lang/Object") && !말(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = 종찾기(부모);
            if (Kiremya || 위 < 0) return -1;
            int 읽는자리 = 위, 단계수 = 0;
            while (읽는자리 >= 0 && 단계수++ < 16) {
                if (읽는자리 == 종) { 실패("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int 파일번호 = 0; 파일번호 < 칸수; 파일번호++) if (칸주인[파일번호] == 종 && (칸권한[파일번호] & 8) == 0) 칸위치[파일번호] += 시작변위;
            종칸수[종] += 시작변위;
        }
        return 종;
    }
    static int 부모종(int 종) {
        int Linnya = 종부모[종];
        for (int 반복자리 = 0; 반복자리 < 종수; 반복자리++) if (Linnya != 0 && 종이름[반복자리] != 0 && 같은말(종이름[반복자리], Linnya)) return 반복자리;
        return -1;
    }
    static int 함수찾기(int 종, int Linnya, int 형식) {
        for (int 깊이 = 0; 종 >= 0 && 깊이 < 16; 깊이++, 종 = 부모종(종)) {
            for (int 반복자리 = 0; 반복자리 < 함수수; 반복자리++) if (함수주인[반복자리] == 종 && 같은말(함수명[반복자리], Linnya) && 같은말(함수형[반복자리], 형식)) return 반복자리;
        }
        return -1;
    }
    static int 이름함수(int 종, String Linnya, String 형식) {
        for (int 깊이 = 0; 종 >= 0 && 깊이 < 16; 깊이++, 종 = 부모종(종))
            for (int 반복자리 = 0; 반복자리 < 함수수; 반복자리++) if (함수주인[반복자리] == 종 && 말(함수명[반복자리], Linnya) && 말(함수형[반복자리], 형식)) return 반복자리;
        return -1;
    }
    static int 형종류(int Linnya) { return Fayiro[상가[Linnya]] == 'L' || Fayiro[상가[Linnya]] == '[' ? 2 : 1; }
    static boolean 초기화(int 종, int 명령시작) {
        if (종 < 0 || Kiremya) return false;
        if (종상태[종] == 3) { 실패("NoClassDefFoundError: initialization failed"); return false; }
        if (종상태[종] == 1 && 종가닥[종] != 현재가닥) { 틀위치[틀] = 명령시작; 바꿈요청 = true; return false; }
        if (종상태[종] != 0) return true;
        int 위 = 부모종(종);
        if (위 >= 0 && !초기화(위, 명령시작)) return false;
        종상태[종] = 1; 종가닥[종] = 현재가닥;
        if (종초기화[종] != 0) {
            틀위치[틀] = 명령시작;
            호출(종초기화[종] - 1); if (!Kiremya) 틀초기화[틀] = 종 + 1;
            return false;
        }
        종상태[종] = 2; return true;
    }
    static void 필드호출(int 번호, int Mulimu, int Tandika) {
        if (!상검사(번호, 9)) return;
        int 소유 = 클래스문자(상가[번호]), Linnya = 참조이름(상나[번호]), 형식 = 참조형식(상나[번호]);
        if (말(소유, "java/lang/System") && (말(Linnya, "out") || 말(Linnya, "err")) && 말(형식, "Ljava/io/PrintStream;") && Mulimu == 178) { 넣기(-1, 2); return; }
        int 종 = 종찾기(소유); if (종 < 0 || Kiremya) return;
        int 찾음 = -1;
        for (int 읽는자리 = 종, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int 파일번호 = 0; 파일번호 < 칸수; 파일번호++) if (칸주인[파일번호] == 읽는자리 && 같은말(칸이름[파일번호], Linnya) && 같은말(칸형[파일번호], 형식)) 찾음 = 파일번호;
        if (찾음 < 0) { 실패("NoSuchFieldError"); return; }
        boolean 정적 = Mulimu == 178 || Mulimu == 179;
        if (정적 != ((칸권한[찾음] & 8) != 0)) { 실패("field static/instance mismatch"); return; }
        if (정적 && !초기화(칸주인[찾음], Tandika)) return;
        int 형 = 형종류(형식), 값 = 0;
        if (Mulimu == 179 || Mulimu == 181) 값 = 빼기(형);
        if (정적) { if (Mulimu == 178) 넣기(칸값[찾음], 형); else if (!Kiremya) 칸값[찾음] = 값; return; }
        int 객체참조 = 빼기(2);
        if (!객체유효(객체참조)) return;
        if (힙[객체참조] < 32 || !종포함(힙[객체참조] - 32, 소유)) { 실패("field receiver type mismatch"); return; }
        int 보관칸 = 객체참조 + 2 + 칸위치[찾음];
        if (Mulimu == 180) 넣기(힙[보관칸], 형);
        else if (!Kiremya) { 힙[보관칸] = 값; 힙참조[보관칸] = 형 == 2 ? 1 : 0; }
    }
    static boolean 종포함(int 종, int Linnya) {
        for (int 중첩깊이 = 0; 종 >= 0 && 중첩깊이 < 16; 중첩깊이++, 종 = 부모종(종)) {
            if (같은말(종이름[종], Linnya) || (종부모[종] != 0 && 같은말(종부모[종], Linnya))) return true;
            for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[종]; 안쪽자리++) if (같은말(종접면[종 * 16 + 안쪽자리], Linnya)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int 바이트값, boolean 경로) {
        if (첫값 == 바이트값) return true;
        if (첫값 <= 0 || 바이트값 <= 0 || 힙[첫값] != 1 || 힙[바이트값] != 1 || 힙[첫값 + 1] != 힙[바이트값 + 1]) return false;
        for (int 반복자리 = 0; 반복자리 < 힙[첫값 + 1]; 반복자리++) {
            int 가로좌표 = 힙[첫값 + 2 + 반복자리], 세로좌표 = 힙[바이트값 + 2 + 반복자리];
            if (경로) { if (가로좌표 == '.') 가로좌표 = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (가로좌표 != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int 객체참조) {
        if (객체참조 == 0) { 실패("NullPointerException"); return false; }
        if (객체참조 < 1 || 객체참조 >= 힙끝 || 힙폭[객체참조] < 2 || 힙[객체참조] == 0) { 실패("invalid object reference"); return false; }
        return true;
    }
    static void 보호(int 객체참조) {
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
        for (int 반복자리 = 0; 반복자리 < 문자열참조.length; 반복자리++) 표시(문자열참조[반복자리]);
        for (int 반복자리 = 0; 반복자리 < 칸수; 반복자리++) if ((칸권한[반복자리] & 8) != 0 && 형종류(칸형[반복자리]) == 2) 표시(칸값[반복자리]);
        for (int 임시값 = 0; 임시값 < 가닥수; 임시값++) {
            표시(가닥객체[임시값]); 표시(가닥대상[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? 틀 : 가닥틀[임시값];
            for (int 파일번호 = 임시값 * 32; 파일번호 <= 꼭대기자리; 파일번호++) {
                for (int 안쪽자리 = 0; 안쪽자리 < 함수지역[틀함수[파일번호]]; 안쪽자리++) if (지역형[파일번호 * 128 + 안쪽자리] == 2) 표시(지역값[파일번호 * 128 + 안쪽자리]);
                for (int 안쪽자리 = 0; 안쪽자리 < 틀스택[파일번호]; 안쪽자리++) if (스택형[파일번호 * 128 + 안쪽자리] == 2) 표시(스택값[파일번호 * 128 + 안쪽자리]);
            }
        }
        for (int 반복자리 = 0; 반복자리 < 화면참조.length; 반복자리++) 표시(화면참조[반복자리]);
        for (int 반복자리 = 0; 반복자리 < 나중수; 반복자리++) 표시(나중실행[반복자리]);
        for (int 반복자리 = 0; 반복자리 < 정수저장.length; 반복자리++) 표시(정수저장[반복자리]);
        for (int 반복자리 = 0; 반복자리 < 종수; 반복자리++) 표시(종잠금[반복자리]);
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (잠금깊이[검사자리] > 0) 표시(검사자리);
        표시(던진객체);
        for (int 반복자리 = 0; 반복자리 < 잠시수; 반복자리++) 표시(잠시참조[반복자리]);
        while (표시수 > 0) {
            int 객체참조 = 표시대기[--표시수], 분류코드 = 힙[객체참조];
            for (int 반복자리 = 객체참조 + 2; 반복자리 < 객체참조 + 힙폭[객체참조]; 반복자리++) if (분류코드 == 3 || 분류코드 == 4 || 힙참조[반복자리] != 0) 표시(힙[반복자리]);
        }
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙표시[검사자리] == 0) 힙[검사자리] = 0;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙[검사자리] == 0) {
            while (검사자리 + 힙폭[검사자리] < 힙끝 && 힙[검사자리 + 힙폭[검사자리]] == 0) { int 다음자리 = 검사자리 + 힙폭[검사자리]; 힙폭[검사자리] += 힙폭[다음자리]; 힙폭[다음자리] = 0; }
            if (검사자리 + 힙폭[검사자리] == 힙끝) { 힙끝 = 검사자리; break; }
        }
    }
    static int 새기억(int 종류, int 길이) {
        if (길이 < 0) { 실패("NegativeArraySizeException"); return 0; }
        if (길이 > 힙.length - 3) { 실패("object heap exhausted"); return 0; }
        int 필요수 = 길이 + 2, 객체참조 = 0;
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
        if (객체참조 == 0) { 실패("object heap exhausted"); return 0; }
        for (int 반복자리 = 0; 반복자리 < 필요수; 반복자리++) { 힙[객체참조 + 반복자리] = 0; 힙참조[객체참조 + 반복자리] = 0; 힙폭[객체참조 + 반복자리] = 0; }
        배열원소[객체참조] = 0;
        힙폭[객체참조] = 필요수; 힙[객체참조] = 종류; 힙[객체참조 + 1] = 길이; 보호(객체참조); return 객체참조;
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
    static int 예외상수(int Linnya) {
        for (int 반복자리 = 1; 반복자리 <= 41; 반복자리++) if (말(Linnya, 예외이름(반복자리))) return 반복자리;
        return 0;
    }
    static String 예외이름(int 식별값) {
        if (식별값 == 40) return "java/lang/InterruptedException";
        if (식별값 == 41) return "한국어/자체/대기중단예외";
        if (식별값 == 39) return "java/net/SocketException";
        if (식별값 == 20) return "한국어/자체/예외";
        if (식별값 == 21) return "한국어/자체/실행예외";
        if (식별값 == 22) return "한국어/자체/입출력예외";
        if (식별값 == 23) return "한국어/자체/대기시간초과예외";
        if (식별값 == 24) return "한국어/자체/주소확인예외";
        if (식별값 == 25) return "한국어/자체/파일없음예외";
        if (식별값 == 26) return "한국어/자체/통신예외";
        if (식별값 == 27) return "한국어/자체/잘못된인수예외";
        if (식별값 == 28) return "한국어/자체/숫자형식예외";
        if (식별값 == 29) return "한국어/자체/범위예외";
        if (식별값 == 30) return "한국어/자체/배열범위예외";
        if (식별값 == 31) return "한국어/자체/문자열범위예외";
        if (식별값 == 32) return "한국어/자체/빈참조예외";
        if (식별값 == 33) return "한국어/자체/산술예외";
        if (식별값 == 34) return "한국어/자체/상태예외";
        if (식별값 == 35) return "한국어/자체/형변환예외";
        if (식별값 == 36) return "한국어/자체/음수배열크기예외";
        if (식별값 == 37) return "한국어/자체/배열저장예외";
        if (식별값 == 38) return "한국어/자체/가닥상태예외";
        if (식별값 == 1) return "java/lang/Throwable"; if (식별값 == 2) return "java/lang/Exception";
        if (식별값 == 3) return "java/lang/RuntimeException"; if (식별값 == 4) return "java/lang/ArithmeticException";
        if (식별값 == 5) return "java/lang/NullPointerException"; if (식별값 == 6) return "java/lang/IndexOutOfBoundsException";
        if (식별값 == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (식별값 == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (식별값 == 9) return "java/lang/IllegalArgumentException"; if (식별값 == 10) return "java/lang/NumberFormatException";
        if (식별값 == 11) return "java/io/IOException"; if (식별값 == 12) return "java/io/FileNotFoundException";
        if (식별값 == 17) return "java/lang/ArrayStoreException";
        if (식별값 == 18) return "java/net/UnknownHostException";
        if (식별값 == 19) return "java/net/SocketTimeoutException";
        if (식별값 == 16) return "java/lang/IllegalThreadStateException";
        if (식별값 == 13) return "java/lang/IllegalStateException"; if (식별값 == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int 식별값) {
        if (식별값 == 40) return 2;
        if (식별값 == 41) return 40;
        if (식별값 == 39) return 11;
        if (식별값 == 1) return 0;
        if (식별값 == 2) return 1;
        if (식별값 == 3) return 2;
        if (식별값 == 4) return 3;
        if (식별값 == 5) return 3;
        if (식별값 == 6) return 3;
        if (식별값 == 7) return 6;
        if (식별값 == 8) return 6;
        if (식별값 == 9) return 3;
        if (식별값 == 10) return 9;
        if (식별값 == 11) return 2;
        if (식별값 == 12) return 11;
        if (식별값 == 13) return 3;
        if (식별값 == 14) return 3;
        if (식별값 == 15) return 3;
        if (식별값 == 16) return 9;
        if (식별값 == 17) return 3;
        if (식별값 == 18) return 11;
        if (식별값 == 19) return 11;
        if (식별값 == 20) return 2;
        if (식별값 == 21) return 3;
        if (식별값 == 22) return 11;
        if (식별값 == 23) return 22;
        if (식별값 == 24) return 22;
        if (식별값 == 25) return 22;
        if (식별값 == 26) return 22;
        if (식별값 == 27) return 9;
        if (식별값 == 28) return 27;
        if (식별값 == 29) return 6;
        if (식별값 == 30) return 29;
        if (식별값 == 31) return 29;
        if (식별값 == 32) return 5;
        if (식별값 == 33) return 4;
        if (식별값 == 34) return 13;
        if (식별값 == 35) return 14;
        if (식별값 == 36) return 15;
        if (식별값 == 37) return 17;
        if (식별값 == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int 실제값, int 요구값) {
        for (int 깊이 = 0; 실제값 != 0 && 깊이 < 16; 깊이++, 실제값 = 예외부모(실제값))
            if (실제값 == 요구값) return true;
        return false;
    }
    static void 예외던짐(int 식별값, String 안내참조) {
        int 객체참조 = 새기억(9, 2); if (Kiremya) return;
        힙[객체참조 + 2] = 식별값; 힙[객체참조 + 3] = 호스트문자(안내참조); 힙참조[객체참조 + 3] = 1;
        던진객체 = 객체참조; Kiremya = true;
    }
    static boolean 맞는객체(int 객체참조, int Linnya) {
        if (객체참조 == 0) return true;
        if (!객체유효(객체참조)) return false;
        int 분류코드 = 힙[객체참조];
        if (말(Linnya, "java/lang/Object")) return true;
        if (분류코드 >= 32) return 종포함(분류코드 - 32, Linnya);
        if (분류코드 == 9) { int 대상값 = 예외상수(Linnya); return 대상값 != 0 && 예외포함(힙[객체참조 + 2], 대상값); }
        if (분류코드 == 1) return 말(Linnya, "java/lang/String") || 말(Linnya, "java/lang/CharSequence");
        if (분류코드 == 4) return 말(Linnya, "java/lang/StringBuilder") || 말(Linnya, "java/lang/CharSequence");
        if (분류코드 == 10) return 말(Linnya, "java/util/ArrayList") || 말(Linnya, "java/util/List");
        if (분류코드 == 11) return 말(Linnya, "java/util/HashMap") || 말(Linnya, "java/util/Map");
        if (분류코드 == 12) return 말(Linnya, "java/lang/Integer") || 말(Linnya, "java/lang/Number");
        if (분류코드 >= 24 && 분류코드 <= 28 && 힙[객체참조 + 13] != 0) return 한국어화면종(Linnya) == 분류코드 || 말(Linnya, "한국어/자체/화면구성요소");
        if (분류코드 >= 24 && 분류코드 <= 28) return (한국어화면종(Linnya) == 0 && 화면종(Linnya) == 분류코드) || 말(Linnya, "java/awt/Component") || 말(Linnya, "java/awt/Container") || 말(Linnya, "javax/swing/JComponent");
        if (분류코드 == 29) return 말(Linnya, 힙[객체참조 + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (분류코드 == 30) return 말(Linnya, "java/awt/FlowLayout") || 말(Linnya, "java/awt/LayoutManager");
        if (분류코드 == 17) return 말(Linnya, "java/net/Socket");
        if (분류코드 == 18) return 말(Linnya, "java/net/ServerSocket");
        if (분류코드 == 19) return 말(Linnya, 힙[객체참조 + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (분류코드 == 14) return 말(Linnya, "java/net/InetAddress");
        if (분류코드 == 15) return 말(Linnya, "java/net/DatagramSocket");
        if (분류코드 == 16) return 말(Linnya, "java/net/DatagramPacket");
        if (분류코드 == 13) return 말(Linnya, 힙[객체참조 + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (분류코드 == 2) return 말(Linnya, "[I"); if (분류코드 == 20) return 말(Linnya, "[B"); if (분류코드 == 21) return 말(Linnya, "[Z");
        if (분류코드 == 22) return 말(Linnya, "[C"); if (분류코드 == 23) return 말(Linnya, "[S");
        if (분류코드 != 3) return false;
        if (말(Linnya, "[Ljava/lang/Object;")) return true;
        int 원소형식 = 배열원소[객체참조];
        if (원소형식 == -1) return 말(Linnya, "[Ljava/lang/String;") || 말(Linnya, "[Ljava/lang/CharSequence;");
        if (원소형식 == 0) return false;
        if (배열종비교(원소형식, Linnya)) return true;
        if ((말(원소형식, "java/lang/String") || 말(원소형식, "java/lang/StringBuilder")) && 말(Linnya, "[Ljava/lang/CharSequence;")) return true;
        for (int 반복자리 = 0; 반복자리 < 종수; 반복자리++) if (같은말(종이름[반복자리], 원소형식)) {
            for (int 문자값 = 반복자리, 중첩깊이 = 0; 문자값 >= 0 && 중첩깊이 < 16; 중첩깊이++, 문자값 = 부모종(문자값)) {
                if (배열종비교(종부모[문자값], Linnya)) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[문자값]; 안쪽자리++) if (배열종비교(종접면[문자값 * 16 + 안쪽자리], Linnya)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int 이름상수, int 형식참조) {
        int 검사자리 = 상가[형식참조], 항목수 = 상나[형식참조];
        if (이름상수 == 0 || 항목수 < 4 || Fayiro[검사자리] != '[' || Fayiro[검사자리 + 1] != 'L' || Fayiro[검사자리 + 항목수 - 1] != ';' || 상나[이름상수] != 항목수 - 3) return false;
        for (int 반복자리 = 0; 반복자리 < 항목수 - 3; 반복자리++) if (Fayiro[상가[이름상수] + 반복자리] != Fayiro[검사자리 + 2 + 반복자리]) return false;
        return true;
    }
    static void 예외처리() {
        if (던진객체 == 0) return;
        Kiremya = false;
        while (틀 >= 현재가닥 * 32) {
            int 파일번호 = 틀함수[틀], 읽는자리 = 틀명령[틀];
            for (int 반복자리 = 0; 반복자리 < 잡기수; 반복자리++) if (잡기함수[반복자리] == 파일번호 && 읽는자리 >= 잡기시작[반복자리] && 읽는자리 < 잡기끝[반복자리]
                && (잡기종[반복자리] == 0 || 맞는객체(던진객체, 잡기종[반복자리]))) {
                틀위치[틀] = 잡기위치[반복자리]; 틀스택[틀] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (틀초기화[틀] != 0) 종상태[틀초기화[틀] - 1] = 3;
            if (틀잠금[틀] != 0) { 잠금풀기(틀잠금[틀]); 틀잠금[틀] = 0; }
            틀--;
        }
        사용자.쓰기("Uncaught ");
        if (힙[던진객체] == 9) { 사용자.쓰기(예외이름(힙[던진객체 + 2])); 사용자.쓰기(": "); 글쓰기(힙[던진객체 + 3]); }
        else 사용자.쓰기("user exception");
        사용자.문자쓰기(10); 던진객체 = 0; Kiremya = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void 스택명령(int 명령코드) {
        int 첫값 = 빼기(0), 첫형식 = 반환형;
        if (명령코드 == 87) return;
        if (명령코드 == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int 바이트값 = 빼기(0), 둘째형식 = 반환형;
        if (명령코드 == 88) return;
        if (명령코드 == 90) { 넣기(첫값, 첫형식); 넣기(바이트값, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 92) { 넣기(바이트값, 둘째형식); 넣기(첫값, 첫형식); 넣기(바이트값, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 95) { 넣기(첫값, 첫형식); 넣기(바이트값, 둘째형식); return; }
        int 문자값 = 빼기(0), 셋째형식 = 반환형;
        if (명령코드 == 91) { 넣기(첫값, 첫형식); 넣기(문자값, 셋째형식); 넣기(바이트값, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 93) { 넣기(바이트값, 둘째형식); 넣기(첫값, 첫형식); 넣기(문자값, 셋째형식); 넣기(바이트값, 둘째형식); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = 반환형;
        넣기(바이트값, 둘째형식); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(문자값, 셋째형식); 넣기(바이트값, 둘째형식); 넣기(첫값, 첫형식);
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
            int 문자값 = 종찾기(이름상수); if (문자값 < 0 || Kiremya || !초기화(문자값, 시작점)) return;
            분류코드 = 32 + 문자값; 유효길이 = 종칸수[문자값];
        }
        int 객체참조 = 할당(분류코드, 유효길이); if (Kiremya) return;
        if (분류코드 == 13 && 말(이름상수, "한국어/자체/작업가닥")) 힙[객체참조 + 3] = 1;
        if (분류코드 >= 24 && 분류코드 <= 28 && 한국어화면종(이름상수) != 0) 힙[객체참조 + 13] = 1;
        if (분류코드 == 5 || 분류코드 == 6 || 분류코드 == 15 || 분류코드 == 17 || 분류코드 == 18) 힙[객체참조 + 2] = -1;
        if (분류코드 == 9) 힙[객체참조 + 2] = 예외참조;
        넣기(객체참조, 2);
    }
    static boolean 값같음(int 첫값, int 바이트값) {
        if (첫값 == 바이트값) return true;
        if (첫값 == 0 || 바이트값 == 0 || 첫값 < 0 || 바이트값 < 0 || 첫값 >= 힙끝 || 바이트값 >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[바이트값] == 1) return 글같음(첫값, 바이트값, false);
        return 힙[첫값] == 12 && 힙[바이트값] == 12 && 힙[첫값 + 2] == 힙[바이트값 + 2];
    }
    static int 글조각(int 객체참조, int 시작자리, int 끝자리) {
        if (!객체(객체참조, 1)) return 0;
        if (시작자리 < 0 || 끝자리 < 시작자리 || 끝자리 > 힙[객체참조 + 1]) { 실패("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = 할당(1, 끝자리 - 시작자리); if (Kiremya) return 0;
        for (int 반복자리 = 시작자리; 반복자리 < 끝자리; 반복자리++) 힙[반환값 + 2 + 반복자리 - 시작자리] = 힙[객체참조 + 2 + 반복자리];
        return 반환값;
    }
    static int 글합치기(int 첫값, int 바이트값) {
        if (!객체(첫값, 1) || !객체(바이트값, 1)) return 0;
        int 항목수 = 힙[첫값 + 1], 함수번호 = 힙[바이트값 + 1], 반환값 = 할당(1, 항목수 + 함수번호); if (Kiremya) return 0;
        for (int 반복자리 = 0; 반복자리 < 항목수; 반복자리++) 힙[반환값 + 2 + 반복자리] = 힙[첫값 + 2 + 반복자리];
        for (int 반복자리 = 0; 반복자리 < 함수번호; 반복자리++) 힙[반환값 + 2 + 항목수 + 반복자리] = 힙[바이트값 + 2 + 반복자리];
        return 반환값;
    }
    static boolean 기본호출(int 소유종, int 이름상수, int 서술상수, int 명령코드) {
        if (말(소유종, "한국어/자체/실행인수") && 명령코드 == 184) {
            if (말(이름상수, "개수") && 말(서술상수, "()I")) { 넣기(사용자.인수개수() - 1, 1); return true; }
            if (말(이름상수, "Bigambo") && 말(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= 사용자.인수개수() - 1) 예외던짐(29, "실행 인수 범위를 벗어났습니다");
                else 넣기(호스트문자(사용자.인수(순번 + 1)), 2);
                return true;
            }
            실패("지원하지 않는 한국어 실행 인수 호출"); return true;
        }
        if (말(소유종, "한국어/자체/작업가닥")) { 가닥처리(이름상수, 서술상수, 명령코드, true); return true; }
        if (한국어화면소유(소유종)) { 한국어화면호출(소유종, 이름상수, 서술상수, 명령코드); return true; }
        if (화면소유(소유종)) { 화면호출(소유종, 이름상수, 서술상수, 명령코드); return true; }
        if (말(소유종, "java/net/Socket") || 말(소유종, "java/net/ServerSocket") || 말(소유종, "java/io/InputStream") || 말(소유종, "java/io/OutputStream")) { 흐름호출(소유종, 이름상수, 서술상수, 명령코드); return true; }
        if (말(소유종, "한국어/자체/커널") && 명령코드 == 184) {
            if (말(이름상수, "화면너비") && 말(서술상수, "()I")) { 넣기(사용자.화면너비(), 1); return true; }
            if (말(이름상수, "화면높이") && 말(서술상수, "()I")) { 넣기(사용자.화면높이(), 1); return true; }
            if (말(이름상수, "밀리초") && 말(서술상수, "()I")) { 넣기(사용자.밀리초(), 1); return true; }
            if (말(이름상수, "그림대기") && 말(서술상수, "()I")) { 넣기(사용자.그림대기(), 1); return true; }
            if (말(이름상수, "사각형") && 말(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), 가로좌표 = 빼기(1); 넣기(사용자.사각형(가로좌표, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (말(소유종, "java/net/InetAddress") || 말(소유종, "java/net/DatagramPacket") || 말(소유종, "java/net/DatagramSocket")) { 통신호출(소유종, 이름상수, 서술상수, 명령코드); return true; }
        if (말(소유종, "java/lang/Thread")) { 가닥호출(이름상수, 서술상수, 명령코드); return true; }
        if (말(소유종, "java/lang/Object")) {
            if (말(이름상수, "<init>") && 말(서술상수, "()V") && 명령코드 == 183) { 객체유효(빼기(2)); return true; }
            if (말(이름상수, "equals") && 말(서술상수, "(Ljava/lang/Object;)Z")) { int 바이트값 = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == 바이트값 ? 1 : 0, 1); return true; }
        }
        if (예외상수(소유종) != 0) {
            if (말(이름상수, "<init>") && 명령코드 == 183 && (말(서술상수, "()V") || 말(서술상수, "(Ljava/lang/String;)V"))) {
                int 안내문 = 말(서술상수, "()V") ? 0 : 빼기(2), 객체참조 = 빼기(2);
                if (객체(객체참조, 9)) { 힙[객체참조 + 3] = 안내문; 힙참조[객체참조 + 3] = 1; } return true;
            }
            if ((말(이름상수, "getMessage") || 말(이름상수, "설명")) && 말(서술상수, "()Ljava/lang/String;")) { int 객체참조 = 빼기(2); if (객체(객체참조, 9)) 넣기(힙[객체참조 + 3], 2); return true; }
        }
        if (말(소유종, "java/lang/String")) {
            if (명령코드 == 182 && 말(이름상수, "getBytes") && (말(서술상수, "()[B") || 말(서술상수, "(Ljava/lang/String;)[B"))) {
                int 부호화이름 = 말(서술상수, "()[B") ? 0 : 빼기(2), 객체참조 = 빼기(2);
                if (!객체(객체참조, 1)) return true;
                if (부호화이름 != 0 && !글같음(부호화이름, 호스트문자("UTF-8"), false) && !글같음(부호화이름, 호스트문자("UTF8"), false) && !글같음(부호화이름, 호스트문자("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int 항목수 = 힙[객체참조 + 1], 반환값 = 할당(20, 항목수 * 3), 사용수 = 0; if (Kiremya) return true;
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
            if (말(이름상수, "equals") && 말(서술상수, "(Ljava/lang/Object;)Z")) { int 바이트값 = 빼기(2), 첫값 = 빼기(2); if (객체(첫값, 1)) 넣기(글같음(첫값, 바이트값, false) ? 1 : 0, 1); return true; }
            if (말(이름상수, "isEmpty") && 말(서술상수, "()Z")) { int 첫값 = 빼기(2); if (객체(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (말(이름상수, "substring") && (말(서술상수, "(I)Ljava/lang/String;") || 말(서술상수, "(II)Ljava/lang/String;"))) {
                boolean 둘째값 = 말(서술상수, "(II)Ljava/lang/String;"); int 끝자리 = 둘째값 ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (객체(첫값, 1)) 넣기(글조각(첫값, 시작점, 둘째값 ? 끝자리 : 힙[첫값 + 1]), 2); return true;
            }
            if (말(이름상수, "concat") && 말(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int 바이트값 = 빼기(2), 첫값 = 빼기(2); 넣기(글합치기(첫값, 바이트값), 2); return true; }
            if (말(이름상수, "hashCode") && 말(서술상수, "()I")) { int 첫값 = 빼기(2), 해시값 = 0; if (객체(첫값, 1)) { for (int 반복자리 = 0; 반복자리 < 힙[첫값 + 1]; 반복자리++) 해시값 = 해시값 * 31 + 힙[첫값 + 2 + 반복자리]; 넣기(해시값, 1); } return true; }
            if (말(이름상수, "toString") && 말(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (객체(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (말(소유종, "java/lang/Integer")) {
            if (명령코드 == 184 && 말(이름상수, "valueOf") && 말(서술상수, "(I)Ljava/lang/Integer;")) { int 자료값 = 빼기(1), 객체참조 = 자료값 >= -128 && 자료값 <= 127 ? 정수저장[자료값 + 128] : 0; if (객체참조 == 0) { 객체참조 = 할당(12, 1); if (!Kiremya) { 힙[객체참조 + 2] = 자료값; if (자료값 >= -128 && 자료값 <= 127) 정수저장[자료값 + 128] = 객체참조; } } 넣기(객체참조, 2); return true; }
            if (명령코드 == 183 && 말(이름상수, "<init>") && 말(서술상수, "(I)V")) { int 자료값 = 빼기(1), 객체참조 = 빼기(2); if (객체(객체참조, 12)) 힙[객체참조 + 2] = 자료값; return true; }
            if (명령코드 == 182 && 말(이름상수, "intValue") && 말(서술상수, "()I")) { int 객체참조 = 빼기(2); if (객체(객체참조, 12)) 넣기(힙[객체참조 + 2], 1); return true; }
            if (명령코드 == 184 && 말(이름상수, "toString") && 말(서술상수, "(I)Ljava/lang/String;")) { 넣기(수문자(빼기(1)), 2); return true; }
        }
        if (말(소유종, "java/lang/Math") && 명령코드 == 184) {
            if (말(이름상수, "abs") && 말(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((말(이름상수, "min") || 말(이름상수, "max")) && 말(서술상수, "(II)I")) { int 바이트값 = 빼기(1), 첫값 = 빼기(1); 넣기(말(이름상수, "min") ? (첫값 < 바이트값 ? 첫값 : 바이트값) : (첫값 > 바이트값 ? 첫값 : 바이트값), 1); return true; }
        }
        if (말(소유종, "java/lang/System") && 명령코드 == 184) {
            if (말(이름상수, "gc") && 말(서술상수, "()V")) { 수거(); return true; }
            if (말(이름상수, "arraycopy") && 말(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int 항목수 = 빼기(1), 목적자리 = 빼기(1), 바이트값 = 빼기(2), 시작자리 = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(바이트값)) {
                    int 분류코드 = 힙[첫값];
                    if (힙[바이트값] != 분류코드 || (분류코드 != 2 && 분류코드 != 3 && (분류코드 < 20 || 분류코드 > 23))) 실패("arraycopy type mismatch");
                    else if (항목수 < 0 || 시작자리 < 0 || 목적자리 < 0 || 시작자리 > 힙[첫값 + 1] - 항목수 || 목적자리 > 힙[바이트값 + 1] - 항목수) 실패("ArrayIndexOutOfBoundsException");
                    else if (첫값 == 바이트값 && 목적자리 > 시작자리) { for (int 반복자리 = 항목수 - 1; 반복자리 >= 0; 반복자리--) 힙[바이트값 + 2 + 목적자리 + 반복자리] = 힙[첫값 + 2 + 시작자리 + 반복자리]; }
                    else { for (int 반복자리 = 0; 반복자리 < 항목수 && !Kiremya; 반복자리++) { int 자료값 = 힙[첫값 + 2 + 시작자리 + 반복자리]; if (분류코드 != 3 || 배열저장가능(바이트값, 자료값)) 힙[바이트값 + 2 + 목적자리 + 반복자리] = 자료값; } }
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
        int 자료배열 = 할당(3, 다음자리); if (Kiremya) return;
        for (int 반복자리 = 0; 반복자리 < 용량값; 반복자리++) 힙[자료배열 + 2 + 반복자리] = 힙[이전값 + 2 + 반복자리];
        힙[객체참조 + 2] = 자료배열; 힙참조[객체참조 + 2] = 1;
    }
    static void 모음호출(int 소유종, int 이름상수, int 서술상수, int 명령코드) {
        boolean 대응참조 = 말(소유종, "java/util/HashMap") || 말(소유종, "java/util/Map"); int 분류코드 = 대응참조 ? 11 : 10;
        if (말(이름상수, "<init>") && 명령코드 == 183 && 말(서술상수, "()V")) { int 객체참조 = 빼기(2); if (객체(객체참조, 분류코드)) 모음늘리기(객체참조, 8); return; }
        if (명령코드 != 182 && 명령코드 != 185) { 실패("invalid collection invocation"); return; }
        if (말(이름상수, "size") && 말(서술상수, "()I") || 말(이름상수, "isEmpty") && 말(서술상수, "()Z")) {
            int 객체참조 = 빼기(2); if (객체(객체참조, 분류코드)) 넣기(말(이름상수, "size") ? 힙[객체참조 + 3] : 힙[객체참조 + 3] == 0 ? 1 : 0, 1); return;
        }
        if (말(이름상수, "clear") && 말(서술상수, "()V")) { int 객체참조 = 빼기(2); if (객체(객체참조, 분류코드)) { int 자료배열 = 힙[객체참조 + 2]; for (int 반복자리 = 0; 반복자리 < 힙[자료배열 + 1]; 반복자리++) 힙[자료배열 + 2 + 반복자리] = 0; 힙[객체참조 + 3] = 0; } return; }
        if (!대응참조 && 말(이름상수, "add") && 말(서술상수, "(Ljava/lang/Object;)Z")) {
            int 자료값 = 빼기(2), 객체참조 = 빼기(2); if (!객체(객체참조, 10)) return;
            int 항목수 = 힙[객체참조 + 3]; 모음늘리기(객체참조, 항목수 + 1); if (!Kiremya) { 힙[힙[객체참조 + 2] + 2 + 항목수] = 자료값; 힙[객체참조 + 3] = 항목수 + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (말(이름상수, "get") || 말(이름상수, "remove")) && 말(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && 말(이름상수, "set") && 말(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = 말(이름상수, "set"); int 자료값 = 지정여부 ? 빼기(2) : 0, 항목자리 = 빼기(1), 객체참조 = 빼기(2);
            if (!객체(객체참조, 10)) return;
            int 항목수 = 힙[객체참조 + 3], 자료배열 = 힙[객체참조 + 2];
            if (항목자리 < 0 || 항목자리 >= 항목수) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[자료배열 + 2 + 항목자리];
            if (지정여부) 힙[자료배열 + 2 + 항목자리] = 자료값;
            if (말(이름상수, "remove")) { for (int 반복자리 = 항목자리 + 1; 반복자리 < 항목수; 반복자리++) 힙[자료배열 + 1 + 반복자리] = 힙[자료배열 + 2 + 반복자리]; 힙[자료배열 + 1 + 항목수] = 0; 힙[객체참조 + 3] = 항목수 - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (말(이름상수, "get") || 말(이름상수, "remove")) && 말(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && 말(이름상수, "put") && 말(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && 말(이름상수, "containsKey") && 말(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = 말(이름상수, "put"), 제거여부 = 말(이름상수, "remove");
            int 자료값 = 넣기여부 ? 빼기(2) : 0, 키참조 = 빼기(2), 객체참조 = 빼기(2); if (!객체(객체참조, 11)) return;
            int 항목수 = 힙[객체참조 + 3], 자료배열 = 힙[객체참조 + 2], 찾은여부 = -1;
            for (int 반복자리 = 0; 반복자리 < 항목수; 반복자리++) if (값같음(키참조, 힙[자료배열 + 2 + 2 * 반복자리])) { 찾은여부 = 반복자리; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[자료배열 + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(객체참조, (항목수 + 1) * 2); 자료배열 = 힙[객체참조 + 2]; 찾은여부 = 항목수; if (!Kiremya) 힙[객체참조 + 3] = 항목수 + 1; }
                if (!Kiremya) { 힙[자료배열 + 2 + 2 * 찾은여부] = 키참조; 힙[자료배열 + 3 + 2 * 찾은여부] = 자료값; }
            }
            if (제거여부 && 찾은여부 >= 0) { for (int 반복자리 = 찾은여부 + 1; 반복자리 < 항목수; 반복자리++) { 힙[자료배열 + 2 * 반복자리] = 힙[자료배열 + 2 + 2 * 반복자리]; 힙[자료배열 + 1 + 2 * 반복자리] = 힙[자료배열 + 3 + 2 * 반복자리]; } 힙[자료배열 + 2 * 항목수] = 0; 힙[자료배열 + 1 + 2 * 항목수] = 0; 힙[객체참조 + 3] = 항목수 - 1; }
            if (말(이름상수, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        실패("unsupported collection method");
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
        가닥틀[현재가닥] = 틀;
        if (틀 < 현재가닥 * 32) 가닥상태[현재가닥] = 3;
        for (int 반복자리 = 0; 반복자리 < 가닥수; 반복자리++) if (가닥상태[반복자리] == 2 && 가닥상태[가닥대기[반복자리]] == 3) 가닥상태[반복자리] = 1;
        for (int 반복자리 = 1; 반복자리 <= 가닥수; 반복자리++) {
            int 다음자리 = (현재가닥 + 반복자리) % 가닥수;
            if (가닥상태[다음자리] == 1) { 현재가닥 = 다음자리; 틀 = 가닥틀[다음자리]; 바꿈요청 = false; return true; }
        }
        for (int 반복자리 = 0; 반복자리 < 가닥수; 반복자리++) if (가닥상태[반복자리] != 3) { 실패("thread deadlock"); return false; }
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
            else if (대상값 != 0) 실패("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (명령코드 == 182 && (말(이름상수, 한국어 ? "시작하기" : "start") || 말(이름상수, 한국어 ? "기다리기" : "join")) && 말(서술상수, "()V") || 명령코드 == 182 && 말(이름상수, 한국어 ? "살아있는가" : "isAlive") && 말(서술상수, "()Z")) {
            int 객체참조 = 빼기(2); if (!객체유효(객체참조)) return;
            int 식별값 = -1; for (int 반복자리 = 0; 반복자리 < 가닥수; 반복자리++) if (가닥객체[반복자리] == 객체참조) 식별값 = 반복자리;
            if (말(이름상수, 한국어 ? "살아있는가" : "isAlive")) { 넣기(식별값 >= 0 && 가닥상태[식별값] != 3 ? 1 : 0, 1); return; }
            if (말(이름상수, 한국어 ? "기다리기" : "join")) { if (식별값 >= 0 && 가닥상태[식별값] != 3) { 가닥대기[현재가닥] = 식별값; 가닥상태[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (식별값 >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (가닥수 == 4) { 실패("thread limit (4 including main)"); return; }
            int 대상값 = 힙[객체참조] == 13 ? 힙[객체참조 + 2] : 객체참조;
            int 파일번호 = 대상값 > 0 && 힙[대상값] >= 32 ? 이름함수(힙[대상값] - 32, 한국어 ? "실행하기" : "run", "()V") : -1;
            if (대상값 != 0 && 파일번호 < 0) { 실패("Runnable.run required"); return; }
            식별값 = 가닥수++; 가닥객체[식별값] = 객체참조; 가닥대상[식별값] = 대상값;
            int 호출틀 = 식별값 * 32; 가닥틀[식별값] = 파일번호 < 0 ? 호출틀 - 1 : 호출틀; 가닥상태[식별값] = 파일번호 < 0 ? 3 : 1;
            if (파일번호 >= 0) { 틀함수[호출틀] = 파일번호; 틀위치[호출틀] = 함수시작[파일번호]; 지역값[호출틀 * 128] = 대상값; 지역형[호출틀 * 128] = 2; }
            return;
        }
        실패("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], 주소글 = new int[16];
    static int 지역주소() { return 주소객체(0x7f000001); }
    static int 주소객체(int 값) { int 객체참조 = 할당(14, 1); if (!Kiremya) 힙[객체참조 + 2] = 값; return 객체참조; }
    static int 주소해독(int 객체참조) {
        if (객체참조 == 0 || 글같음(객체참조, 호스트문자("localhost"), false)) return 0x7f000001;
        if (!객체(객체참조, 1)) return 0;
        int 자료값 = 0, 총수 = 0, 주소바이트 = 0, 자릿수 = 0, 항목수 = 힙[객체참조 + 1];
        for (int 반복자리 = 0; 반복자리 <= 항목수; 반복자리++) {
            int 문자값 = 반복자리 == 항목수 ? '.' : 힙[객체참조 + 2 + 반복자리];
            if (문자값 == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } 자료값 = 자료값 << 8 | 주소바이트; 총수++; 주소바이트 = 자릿수 = 0; }
            else { if (문자값 < '0' || 문자값 > '9' || ++자릿수 > 3 || (주소바이트 = 주소바이트 * 10 + 문자값 - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return 자료값;
    }
    static int 주소문자(int 자료값) {
        int 항목수 = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int 주소바이트 = 자료값 >>> 이동비트 & 255;
            if (주소바이트 >= 100) 주소글[항목수++] = '0' + 주소바이트 / 100;
            if (주소바이트 >= 10) 주소글[항목수++] = '0' + 주소바이트 / 10 % 10;
            주소글[항목수++] = '0' + 주소바이트 % 10; if (이동비트 != 0) 주소글[항목수++] = '.';
        }
        int 객체참조 = 할당(1, 항목수); if (!Kiremya) for (int 반복자리 = 0; 반복자리 < 항목수; 반복자리++) 힙[객체참조 + 2 + 반복자리] = 주소글[반복자리]; return 객체참조;
    }
    static void 통신호출(int 소유종, int 이름상수, int 서술상수, int 명령코드) {
        if (말(소유종, "java/net/InetAddress")) {
            if (명령코드 == 184 && 말(이름상수, "getLoopbackAddress") && 말(서술상수, "()Ljava/net/InetAddress;")) { 넣기(지역주소(), 2); return; }
            if (명령코드 == 184 && 말(이름상수, "getByName") && 말(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int 자료값 = 주소해독(빼기(2)); if (던진객체 == 0 && !Kiremya) 넣기(주소객체(자료값), 2); return;
            }
            if (명령코드 == 182 && 말(이름상수, "getHostAddress") && 말(서술상수, "()Ljava/lang/String;")) { int 객체참조 = 빼기(2); if (객체(객체참조, 14)) 넣기(주소문자(힙[객체참조 + 2]), 2); return; }
        }
        if (말(소유종, "java/net/DatagramPacket")) {
            if (명령코드 == 183 && 말(이름상수, "<init>") && (말(서술상수, "([BI)V") || 말(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean 목적참조 = 말(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = 목적참조 ? 빼기(1) : 0, 주소참조 = 목적참조 ? 빼기(2) : 0;
                int 항목수 = 빼기(1), 자료배열 = 빼기(2), 객체참조 = 빼기(2);
                if (!객체(객체참조, 16) || !객체(자료배열, 20)) return;
                if (항목수 < 0 || 항목수 > 힙[자료배열 + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (주소참조 != 0 && !객체(주소참조, 14)) return;
                힙[객체참조 + 2] = 자료배열; 힙참조[객체참조 + 2] = 1; 힙[객체참조 + 3] = 항목수;
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
                int 열린파일번호 = 사용자.통신열기(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[객체참조 + 2] = 열린파일번호; return;
            }
            if (명령코드 == 182 && 말(이름상수, "setSoTimeout") && 말(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), 객체참조 = 빼기(2); if (!객체(객체참조, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[객체참조 + 3] = 밀리초값; return;
            }
            if (명령코드 == 182 && 말(이름상수, "getLocalPort") && 말(서술상수, "()I")) { int 객체참조 = 빼기(2); if (객체(객체참조, 15)) 넣기(힙[객체참조 + 2] < 0 ? -1 : 사용자.통신창구(힙[객체참조 + 2]), 1); return; }
            if (명령코드 == 182 && 말(이름상수, "isClosed") && 말(서술상수, "()Z")) { int 객체참조 = 빼기(2); if (객체(객체참조, 15)) 넣기(힙[객체참조 + 2] < 0 ? 1 : 0, 1); return; }
            if (명령코드 == 182 && 말(이름상수, "close") && 말(서술상수, "()V")) { int 객체참조 = 빼기(2); if (객체(객체참조, 15) && 힙[객체참조 + 2] >= 0) { 사용자.파일서술자닫기(힙[객체참조 + 2]); 힙[객체참조 + 2] = -1; } return; }
            if (명령코드 == 182 && (말(이름상수, "send") || 말(이름상수, "receive")) && 말(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int 전문참조 = 빼기(2), 객체참조 = 빼기(2); if (!객체(전문참조, 16) || !객체(객체참조, 15)) return;
                int 자료배열 = 힙[전문참조 + 2], 유효길이 = 힙[전문참조 + 3], 열린파일번호 = 힙[객체참조 + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (말(이름상수, "send")) {
                    if (!객체(힙[전문참조 + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int 반복자리 = 0; 반복자리 < 유효길이; 반복자리++) 통신임시[반복자리] = 힙[자료배열 + 2 + 반복자리];
                    if (사용자.통신보내기(열린파일번호, 힙[힙[전문참조 + 4] + 2], 힙[전문참조 + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int 항목수 = 사용자.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (항목수 == -11) {
                        int 현재시각 = 사용자.밀리초();
                        if (힙[객체참조 + 4] == 0) 힙[객체참조 + 4] = 현재시각 + 1;
                        if (힙[객체참조 + 3] > 0 && 현재시각 - (힙[객체참조 + 4] - 1) >= 힙[객체참조 + 3]) { 힙[객체참조 + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(객체참조, 2); 넣기(전문참조, 2); 틀위치[틀] = 틀명령[틀]; 바꿈요청 = true; return;
                    }
                    힙[객체참조 + 4] = 0;
                    if (항목수 < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int 반복자리 = 0; 반복자리 < 항목수; 반복자리++) 힙[자료배열 + 2 + 반복자리] = (byte)통신임시[반복자리];
                    힙[전문참조 + 3] = 항목수; 힙[전문참조 + 4] = 주소객체(통신임시[513]); 힙참조[전문참조 + 4] = 1; 힙[전문참조 + 5] = 통신임시[512];
                }
                return;
            }
        }
        실패("unsupported java.net method");
    }
    static boolean 흐름대기(int 객체참조) {
        int 현재시각 = 사용자.밀리초();
        if (힙[객체참조 + 5] == 0) 힙[객체참조 + 5] = 현재시각 + 1;
        if (힙[객체참조 + 3] > 0 && 현재시각 - (힙[객체참조 + 5] - 1) >= 힙[객체참조 + 3]) { 힙[객체참조 + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        틀위치[틀] = 틀명령[틀]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int 소유종, int 이름상수, int 서술상수, int 명령코드) {
        boolean 수신쪽 = 말(소유종, "java/net/ServerSocket"), 흐름여부 = 말(소유종, "java/io/InputStream") || 말(소유종, "java/io/OutputStream");
        if (!흐름여부 && 명령코드 == 183 && 말(이름상수, "<init>")) {
            boolean 빈여부 = 말(서술상수, "()V"), 이름지정여부 = 말(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = 말(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && 말(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { 실패("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), 주소참조 = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, 객체참조 = 빼기(2);
            if (!객체(객체참조, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !객체(주소참조, 14)) return;
            int 망주소 = 이름지정여부 ? 주소해독(주소참조) : 주소지정여부 ? 힙[주소참조 + 2] : 0x7f000001;
            if (Kiremya || 던진객체 != 0) return;
            int 열린파일번호 = 사용자.흐름제어(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? 사용자.흐름제어(1, 열린파일번호, 접속번호) : 사용자.흐름연결(열린파일번호, 망주소, 접속번호);
            if (처리값 < 0) { 사용자.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[객체참조 + 2] = 열린파일번호; 힙[객체참조 + 4] = 접속번호; 힙[객체참조 + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!흐름여부 && 말(이름상수, "setSoTimeout") && 말(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), 객체참조 = 빼기(2); if (!객체(객체참조, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[객체참조 + 3] = 밀리초값; return; }
        if (!흐름여부 && 말(이름상수, "close") && 말(서술상수, "()V")) { int 객체참조 = 빼기(2); if (객체(객체참조, 수신쪽 ? 18 : 17) && 힙[객체참조 + 2] >= 0) { 사용자.파일서술자닫기(힙[객체참조 + 2]); 힙[객체참조 + 2] = -1; } return; }
        if (!흐름여부 && (말(이름상수, "getLocalPort") || 말(이름상수, "getPort") || 말(이름상수, "isClosed") || 말(이름상수, "isConnected"))) {
            int 객체참조 = 빼기(2); if (!객체(객체참조, 수신쪽 ? 18 : 17)) return;
            넣기(말(이름상수, "isClosed") ? 힙[객체참조 + 2] < 0 ? 1 : 0 : 말(이름상수, "isConnected") ? 힙[객체참조 + 6] : 말(이름상수, "getPort") ? 힙[객체참조 + 4] : 힙[객체참조 + 2] < 0 ? -1 : 사용자.흐름제어(4, 힙[객체참조 + 2], 0), 1); return;
        }
        if (수신쪽 && 말(이름상수, "accept") && 말(서술상수, "()Ljava/net/Socket;")) {
            int 객체참조 = 빼기(2); if (!객체(객체참조, 18)) return; int 열린파일번호 = 사용자.흐름제어(3, 힙[객체참조 + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(객체참조)) 넣기(객체참조, 2); return; }
            힙[객체참조 + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = 할당(17, 5); if (Kiremya) { 사용자.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = 사용자.흐름제어(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !흐름여부 && ((말(이름상수, "getInputStream") && 말(서술상수, "()Ljava/io/InputStream;")) || (말(이름상수, "getOutputStream") && 말(서술상수, "()Ljava/io/OutputStream;")))) {
            int 객체참조 = 빼기(2); if (!객체(객체참조, 17)) return; if (힙[객체참조 + 2] < 0 || 힙[객체참조 + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = 할당(19, 4); if (Kiremya) return; 힙[반환값 + 2] = 객체참조; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = 말(이름상수, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (흐름여부) {
            boolean 읽기여부 = 말(이름상수, "read"), 쓰기여부 = 말(이름상수, "write"), 배열여부 = 말(서술상수, "([B)I") || 말(서술상수, "([B)V"), 부분배열여부 = 말(서술상수, "([BII)I") || 말(서술상수, "([BII)V");
            int 항목수 = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, 자료배열 = 배열여부 || 부분배열여부 ? 빼기(2) : 0;
            int 자료값 = 쓰기여부 && 말(서술상수, "(I)V") ? 빼기(1) : 0, 객체참조 = 빼기(2);
            if (!객체(객체참조, 19)) return; int 부모참조 = 힙[객체참조 + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (말(이름상수, "close") && 말(서술상수, "()V")) { 사용자.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (말(이름상수, "flush") && 말(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[객체참조 + 3] == 0)) { 실패("unsupported stream operation"); return; }
            if (배열여부 || 부분배열여부) { if (!객체(자료배열, 20)) return; if (배열여부) 항목수 = 힙[자료배열 + 1]; if (시작변위 < 0 || 항목수 < 0 || 시작변위 > 힙[자료배열 + 1] - 항목수) { 예외던짐(6, "stream array bounds"); return; } }
            else 항목수 = 1;
            if (항목수 == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[객체참조 + 4] : 0, 처리값 = 0;
            while (완료수 < 항목수) {
                처리값 = 읽기여부 ? 사용자.파일한바이트읽기(열린파일번호) : 사용자.파일한바이트쓰기(열린파일번호, 배열여부 || 부분배열여부 ? 힙[자료배열 + 2 + 시작변위 + 완료수] : 자료값);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (배열여부 || 부분배열여부)) 힙[자료배열 + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(배열여부 || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[객체참조 + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(객체참조, 2); if (배열여부 || 부분배열여부) 넣기(자료배열, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(항목수, 1); } if (쓰기여부 && !(배열여부 || 부분배열여부)) 넣기(자료값, 1); } return;
            }
            힙[객체참조 + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : 배열여부 || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        실패("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int 이름상수) {
        if (말(이름상수, "한국어/자체/창")) return 24;
        if (말(이름상수, "한국어/자체/Bulambe")) return 26;
        if (말(이름상수, "한국어/자체/ppeesa")) return 27;
        if (말(이름상수, "한국어/자체/입력칸")) return 28;
        if (말(이름상수, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int 이름상수) {
        return 한국어화면종(이름상수) != 0 || 말(이름상수, "한국어/자체/화면구성요소") || 말(이름상수, "한국어/자체/화면일정");
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
    static boolean 화면객체(int 객체참조) { if (!객체유효(객체참조)) return false; if (힙[객체참조] < 24 || 힙[객체참조] > 28) { 실패("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int 객체참조, int 글참조) {
        if (글참조 != 0 && !객체(글참조, 1)) return;
        int 항목수 = 글참조 == 0 ? 0 : 힙[글참조 + 1]; if (항목수 > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int 반복자리 = 0; 반복자리 < 항목수; 반복자리++) 화면글임시[반복자리] = 힙[글참조 + 2 + 반복자리];
        if (사용자.화면글(힙[객체참조 + 2], 화면글임시, 항목수) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[객체참조 + 3] = 글참조; 힙참조[객체참조 + 3] = 1;
    }
    static int 화면문자읽기(int 객체참조) {
        int 식별값 = 힙[객체참조 + 2], 항목수 = 사용자.화면연결(8, 식별값, 0, 0, 0, 0), 사용수 = 0;
        if (항목수 < 0) { 실패("GUI text read failed"); return 0; }
        for (int 반복자리 = 0; 반복자리 < 항목수; 반복자리++) { int 부호값 = 사용자.화면연결(9, 식별값, 반복자리, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = 할당(1, 사용수); if (!Kiremya) for (int 반복자리 = 0; 반복자리 < 사용수; 반복자리++) 힙[반환값 + 2 + 반복자리] = 화면글임시[반복자리]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 커널 화면 기능에 연결한다. Swing 객체/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int 소유종, int 이름상수, int 서술상수, int 명령코드) {
        if (말(소유종, "한국어/자체/화면일정")) {
            if (명령코드 == 184 && 말(이름상수, "나중에실행") && 말(서술상수, "(L한국어/자체/실행할일;)V")) {
                int 할일 = 빼기(2); if (!객체유효(할일)) return;
                if (나중수 == 8) { 실패("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = 할일; return;
            }
            if (명령코드 == 184 && 말(이름상수, "사건처리중인가") && 말(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            실패("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (말(소유종, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!객체(알림, 29) || 힙[알림 + 3] == 0) return;
            if (말(이름상수, "일어난곳") && 말(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (말(이름상수, "명령글") && 말(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (말(이름상수, "번호") && 말(서술상수, "()I")) 넣기(1001, 1);
            else 실패("지원하지 않는 한국어 동작 알림 호출"); return;
        }
        if (명령코드 == 183 && 말(이름상수, "<init>")) {
            int 종류 = 한국어화면종(소유종), 받이 = 0, 가로 = 0, 세로 = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && 말(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (사용자.화면너비() - 폭) / 2; 세로 = (사용자.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && 말(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && 말(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); 세로 = 빼기(1); 가로 = 빼기(1);
            } else { 실패("지원하지 않는 한국어 화면 생성자"); return; }
            int Bigambo = 빼기(2), 요소 = 빼기(2); if (!화면객체(요소)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || 세로 < 0 || 폭 > 사용자.화면너비() - 가로 || 높이 > 사용자.화면높이() - 세로) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int 번호 = 사용자.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (번호 < 1 || 번호 > 32) { 실패("화면 요소 자리가 가득 찼습니다"); return; }
            힙[요소 + 2] = 번호; 화면참조[번호 - 1] = 요소;
            힙[요소 + 5] = 가로; 힙[요소 + 6] = 세로; 힙[요소 + 7] = 폭; 힙[요소 + 8] = 높이; 힙[요소 + 10] = 2;
            힙[요소 + 4] = 받이; 힙참조[요소 + 4] = 1; 힙[요소 + 12] = 1;
            사용자.화면연결(1, 번호, 가로, 세로, 폭, 높이);
            if (종류 == 24) 사용자.화면연결(7, 번호, 2, 0, 0, 0);
            화면문자설정(요소, Bigambo); return;
        }
        if (명령코드 != 182) { 실패("잘못된 한국어 화면 호출 Mulimu"); return; }
        if (말(이름상수, "글쓰기") && 말(서술상수, "(Ljava/lang/String;)V")) {
            int Bigambo = 빼기(2), 요소 = 빼기(2); if (화면객체(요소)) 화면문자설정(요소, Bigambo); return;
        }
        if (말(이름상수, "글읽기") && 말(서술상수, "()Ljava/lang/String;")) {
            int 요소 = 빼기(2); if (화면객체(요소)) 넣기(화면문자읽기(요소), 2); return;
        }
        if (말(이름상수, "동작맡기기") && 말(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), 요소 = 빼기(2);
            if (화면객체(요소)) { 힙[요소 + 4] = 받이; 힙참조[요소 + 4] = 1; 힙[요소 + 12] = 1; } return;
        }
        if (말(이름상수, "담기") && 말(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int 자식 = 빼기(2), 부모 = 빼기(2); if (!화면객체(자식) || !화면객체(부모)) return;
            if (사용자.화면연결(2, 힙[부모 + 2], 힙[자식 + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[자식 + 11] = 부모; 힙참조[자식 + 11] = 1; return;
        }
        if (말(이름상수, "자리정하기") && 말(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), 세로 = 빼기(1), 가로 = 빼기(1), 요소 = 빼기(2); if (!화면객체(요소)) return;
            if (사용자.화면연결(1, 힙[요소 + 2], 가로, 세로, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[요소 + 5] = 가로; 힙[요소 + 6] = 세로; 힙[요소 + 7] = 폭; 힙[요소 + 8] = 높이; return;
        }
        if ((말(이름상수, "보이기") || 말(이름상수, "Bikka")) && 말(서술상수, "()V")) {
            boolean 보임 = 말(이름상수, "보이기"); int 요소 = 빼기(2); if (!화면객체(요소)) return;
            if (사용자.화면연결(보임 ? 3 : 4, 힙[요소 + 2], 보임 ? 1 : 0, 0, 0, 0) < 0) { 실패("화면은 대화형 명령에서 실행해야 합니다"); return; }
            힙[요소 + 9] = 보임 ? 1 : 0; return;
        }
        if (말(이름상수, "보이는가") && 말(서술상수, "()Z")) { int 요소 = 빼기(2); if (화면객체(요소)) 넣기(힙[요소 + 9], 1); return; }
        실패("지원하지 않는 한국어 화면 메서드");
    }
    static void 화면호출(int 소유종, int 이름상수, int 서술상수, int 명령코드) {
        if (말(소유종, "javax/swing/SwingUtilities")) {
            if (명령코드 == 184 && 말(이름상수, "invokeLater") && 말(서술상수, "(Ljava/lang/Runnable;)V")) { int 객체참조 = 빼기(2); if (!객체유효(객체참조)) return; if (나중수 == 8) { 실패("invokeLater queue full"); return; } 나중실행[나중수++] = 객체참조; return; }
            if (명령코드 == 184 && 말(이름상수, "isEventDispatchThread") && 말(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            실패("unsupported SwingUtilities method"); return;
        }
        if (말(소유종, "java/awt/event/ActionEvent")) {
            int 객체참조 = 빼기(2); if (!객체(객체참조, 29)) return;
            if (말(이름상수, "getSource") && 말(서술상수, "()Ljava/lang/Object;")) 넣기(힙[객체참조 + 2], 2);
            else if (말(이름상수, "getActionCommand") && 말(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[객체참조 + 2]), 2);
            else if (말(이름상수, "getID") && 말(서술상수, "()I")) 넣기(1001, 1);
            else 실패("unsupported ActionEvent method"); return;
        }
        if (명령코드 == 183 && 말(이름상수, "<init>")) {
            int 열수 = 0, 글참조 = 0;
            if (말(서술상수, "(I)V")) 열수 = 빼기(1);
            else if (말(서술상수, "(Ljava/lang/String;I)V")) { 열수 = 빼기(1); 글참조 = 빼기(2); }
            else if (말(서술상수, "(Ljava/lang/String;)V")) 글참조 = 빼기(2);
            else if (말(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!말(서술상수, "()V")) { 실패("unsupported Swing constructor"); return; }
            int 객체참조 = 빼기(2); if (!객체유효(객체참조)) return;
            if (힙[객체참조] == 30) { 실패("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(객체참조) || 열수 < 0) return;
            int 식별값 = 사용자.화면연결(0, 힙[객체참조] - 23, 0, 0, 0, 0);
            if (식별값 < 1 || 식별값 > 32) { 실패("GUI widget slots exhausted"); return; }
            힙[객체참조 + 2] = 식별값; 화면참조[식별값 - 1] = 객체참조; 힙[객체참조 + 5] = 힙[객체참조] == 24 ? 130 : 16; 힙[객체참조 + 6] = 힙[객체참조] == 24 ? 110 : 16;
            힙[객체참조 + 7] = 힙[객체참조] == 24 ? 380 : 220; 힙[객체참조 + 8] = 힙[객체참조] == 24 ? 240 : 28; 힙[객체참조 + 10] = 1;
            화면문자설정(객체참조, 글참조); return;
        }
        if (말(이름상수, "setText") || 말(이름상수, "setTitle")) { int 글참조 = 빼기(2), 객체참조 = 빼기(2); if (화면객체(객체참조) && 말(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(객체참조, 글참조); return; }
        if (말(이름상수, "getText") || 말(이름상수, "getTitle")) { int 객체참조 = 빼기(2); if (화면객체(객체참조) && 말(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(객체참조), 2); return; }
        if (말(이름상수, "addActionListener") && 말(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), 객체참조 = 빼기(2); if (화면객체(객체참조)) { 힙[객체참조 + 4] = 수신참조; 힙참조[객체참조 + 4] = 1; } return; }
        if (말(이름상수, "getContentPane") && 말(서술상수, "()Ljava/awt/Container;")) { int 객체참조 = 빼기(2); if (화면객체(객체참조)) 넣기(객체참조, 2); return; }
        if (말(이름상수, "setLayout") && 말(서술상수, "(Ljava/awt/LayoutManager;)V")) { int 배치참조 = 빼기(2), 객체참조 = 빼기(2); if (화면객체(객체참조) && 배치참조 != 0) 실패("only absolute layout (null) is supported"); return; }
        if (말(이름상수, "add") && (말(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || 말(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean 배치조건 = 말(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (배치조건) 빼기(2);
            int 자식참조 = 빼기(2), 객체참조 = 빼기(2); if (!화면객체(자식참조) || !화면객체(객체참조)) return;
            if (사용자.화면연결(2, 힙[객체참조 + 2], 힙[자식참조 + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[자식참조 + 11] = 객체참조; 힙참조[자식참조 + 11] = 1; if (!배치조건) 넣기(자식참조, 2); return;
        }
        if (말(이름상수, "setBounds") && 말(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), 가로좌표 = 빼기(1), 객체참조 = 빼기(2); if (!화면객체(객체참조)) return;
            if (사용자.화면연결(1, 힙[객체참조 + 2], 가로좌표, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[객체참조 + 5] = 가로좌표; 힙[객체참조 + 6] = 세로좌표; 힙[객체참조 + 7] = 너비; 힙[객체참조 + 8] = 높이; return;
        }
        if (말(이름상수, "setSize") && 말(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 객체참조 = 빼기(2); if (!화면객체(객체참조)) return;
            if (사용자.화면연결(1, 힙[객체참조 + 2], 힙[객체참조 + 5], 힙[객체참조 + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[객체참조 + 7] = 너비; 힙[객체참조 + 8] = 높이; } return;
        }
        if (말(이름상수, "setLocationRelativeTo") && 말(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), 객체참조 = 빼기(2); if (!화면객체(객체참조)) return; if (상대배치 != 0) { 실패("only screen centering supported"); return; } 힙[객체참조 + 5] = (사용자.화면너비() - 힙[객체참조 + 7]) / 2; 힙[객체참조 + 6] = (사용자.화면높이() - 힙[객체참조 + 8]) / 2; 사용자.화면연결(1, 힙[객체참조 + 2], 힙[객체참조 + 5], 힙[객체참조 + 6], 힙[객체참조 + 7], 힙[객체참조 + 8]); return; }
        if (말(이름상수, "setDefaultCloseOperation") && 말(서술상수, "(I)V")) { int 종료정책 = 빼기(1), 객체참조 = 빼기(2); if (화면객체(객체참조)) { if (종료정책 < 0 || 종료정책 > 3) 예외던짐(9, "close policy"); else { 힙[객체참조 + 10] = 종료정책; 사용자.화면연결(7, 힙[객체참조 + 2], 종료정책, 0, 0, 0); } } return; }
        if (말(이름상수, "setVisible") && 말(서술상수, "(Z)V")) { int 자료값 = 빼기(1), 객체참조 = 빼기(2); if (화면객체(객체참조)) { int 처리값 = 사용자.화면연결(3, 힙[객체참조 + 2], 자료값, 0, 0, 0); if (처리값 < 0) 실패("Swing requires a standalone interactive command"); else 힙[객체참조 + 9] = 자료값; } return; }
        if (말(이름상수, "dispose") && 말(서술상수, "()V")) { int 객체참조 = 빼기(2); if (화면객체(객체참조)) { 사용자.화면연결(4, 힙[객체참조 + 2], 0, 0, 0, 0); 힙[객체참조 + 9] = 0; } return; }
        if (말(이름상수, "repaint") || 말(이름상수, "validate")) { int 객체참조 = 빼기(2); if (!화면객체(객체참조) || !말(서술상수, "()V")) return; 사용자.화면연결(1, 힙[객체참조 + 2], 힙[객체참조 + 5], 힙[객체참조 + 6], 힙[객체참조 + 7], 힙[객체참조 + 8]); return; }
        if (말(이름상수, "isVisible") && 말(서술상수, "()Z")) { int 객체참조 = 빼기(2); if (화면객체(객체참조)) 넣기(힙[객체참조 + 9], 1); return; }
        실패("unsupported Swing method (native subset)");
    }
    static void 사건실행(int 대상값, int 사건번호, boolean 한국어) {
        if (대상값 < 1 || 힙[대상값] < 32) { 실패("Java event listener required"); return; }
        int 파일번호 = 이름함수(힙[대상값] - 32, 사건번호 == 0 ? (한국어 ? "실행하기" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (파일번호 < 0) { 실패("event callback missing"); return; }
        현재가닥 = 0; 가닥수 = 1; 틀 = 0; 가닥상태[0] = 1; 틀스택[0] = 0; 틀잠금[0] = 틀초기화[0] = 0; 바꿈요청 = false;
        for (int 반복자리 = 0; 반복자리 < 128; 반복자리++) { 지역값[반복자리] = 지역형[반복자리] = 0; }
        틀함수[0] = 파일번호; 틀위치[0] = 함수시작[파일번호]; 지역값[0] = 대상값; 지역형[0] = 2;
        if (사건번호 != 0) { 지역값[1] = 사건번호; 지역형[1] = 2; }
        사건중 = true; 실행(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!Kiremya) {
            if (나중수 > 0) { int 대상값 = 나중실행[0], 한국어 = 나중한국어[0]; for (int 반복자리 = 1; 반복자리 < 나중수; 반복자리++) { 나중실행[반복자리 - 1] = 나중실행[반복자리]; 나중한국어[반복자리 - 1] = 나중한국어[반복자리]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(대상값, 0, 한국어 != 0); continue; }
            if (사용자.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = 사용자.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { 실패("GUI event I/O failed"); return; }
            int 식별값 = 사건번호 & 65535; if (식별값 < 1 || 식별값 > 32) continue; int 객체참조 = 화면참조[식별값 - 1]; if (객체참조 == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[객체참조 + 10] != 0) 힙[객체참조 + 9] = 0;
                if (힙[객체참조 + 10] == 3) for (int 반복자리 = 0; 반복자리 < 32; 반복자리++) if (화면참조[반복자리] != 0 && 힙[화면참조[반복자리]] == 24) 사용자.화면연결(4, 반복자리 + 1, 0, 0, 0, 0);
            } else if (힙[객체참조 + 4] != 0) {
                int 안내참조 = 할당(29, 2); if (Kiremya) return; 힙[안내참조 + 2] = 객체참조; 힙[안내참조 + 3] = 힙[객체참조 + 12]; 힙참조[안내참조 + 2] = 1; 사건실행(힙[객체참조 + 4], 안내참조, 힙[객체참조 + 12] != 0);
            }
        }
    }
    public static int Tandika() {
        if (사용자.인수개수() == 1 && 자바도구.같음(사용자.인수(0), "-version")) {
            사용자.쓰기("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (사용자.인수개수() < 1) { 사용자.쓰기("Usage: java CLASS [ARGS]\n"); return 2; }
        시작종 = 종적재(호스트문자(사용자.인수(0))); if (Kiremya || 시작종 < 0) return 1;
        int 진입 = 이름함수(시작종, "Tandika", "()V");
        boolean 한국어진입 = 진입 >= 0 && (함수권한[진입] & 9) == 9;
        if (!한국어진입) 진입 = 이름함수(시작종, "main", "([Ljava/lang/String;)V");
        if (진입 < 0 || (함수권한[진입] & 9) != 9) 실패("public static void Tandika() or main(String[] args) required");
        if (Kiremya) return 1;
        int 인수 = 할당(3, 사용자.인수개수() - 1); 배열원소[인수] = -1;
        for (int 수 = 1; 수 < 사용자.인수개수() && !Kiremya; 수++) 힙[인수 + 1 + 수] = 호스트문자(사용자.인수(수));
        틀 = 0; 틀함수[0] = 진입; 틀위치[0] = 함수시작[진입]; 지역값[0] = 한국어진입 ? 0 : 인수; 지역형[0] = 한국어진입 ? 0 : 2;
        가닥상태[0] = 1; 가닥객체[0] = 할당(13, 2);
        실행(); if (!Kiremya) 화면사건들(); return Kiremya ? 1 : 0;
    }
}
