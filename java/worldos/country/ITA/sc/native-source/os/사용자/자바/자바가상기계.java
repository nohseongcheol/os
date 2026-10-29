// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. 파일/스택/참조/분기 경계를 실행 중 검사한다. */
public final class 자바가상기계 {
    static int[] 파일 = new int[16384], 파일명 = new int[64];
    static int[] 상종류 = new int[512], 상가 = new int[512], 상나 = new int[512], 문자열참조 = new int[512];
    static int[] 함수명 = new int[32], 함수형 = new int[32], 함수권한 = new int[32];
    static int[] 함수시작 = new int[32], 함수끝 = new int[32], 함수스택 = new int[32], 함수지역 = new int[32];
    static int[] 함수인수수 = new int[32], 함수인수형 = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] 지역값 = new int[4096], 지역형 = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] 틀함수 = new int[32], 틀위치 = new int[32], 틀스택 = new int[32];
    static int[] 힙 = new int[8192];
    static int Mannària, 읽기위치, 상수수, 함수수, 클래스명, 틀 = -1, 힙끝 = 1, 반환형;
    static boolean 오류;

    static void 실패(String 말) {
        if (!오류) { 사용자.쓰기("JVM error: "); 사용자.쓰기(말); 사용자.문자쓰기(10); }
        오류 = true;
    }
    static boolean 범위(int 시작, int 길이) { return 시작 >= 0 && 길이 >= 0 && 시작 <= Mannària - 길이; }
    static int 바이트() {
        if (!범위(읽기위치, 1)) { 실패("truncated class file"); return 0; }
        return 파일[읽기위치++];
    }
    static int 짧은수() { return 바이트() << 8 | 바이트(); }
    static int 정수() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int 길이) { if (!범위(읽기위치, 길이)) 실패("invalid attribute size"); else 읽기위치 += 길이; }
    static boolean 상검사(int 수, int 종류) {
        if (수 <= 0 || 수 >= 상수수 || 상종류[수] != 종류) { 실패("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int 시작, int 길이, String 말) {
        if (!범위(시작, 길이) || 길이 != 말.length()) return false;
        for (int 수 = 0; 수 < 길이; 수++) if (파일[시작 + 수] != 말.charAt(수)) return false;
        return true;
    }
    static boolean 말(int 상수, String 말) { return 상검사(상수, 1) && 구간(상가[상수], 상나[상수], 말); }
    static boolean 같은말(int 가, int 나) {
        if (!상검사(가, 1) || !상검사(나, 1) || 상나[가] != 상나[나]) return false;
        for (int 수 = 0; 수 < 상나[가]; 수++) if (파일[상가[가] + 수] != 파일[상가[나] + 수]) return false;
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
            int 시작 = 읽기위치;
            while (읽기위치 < 끝 && 파일[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == 시작) 실패("invalid reference descriptor");
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
        while (!오류 && 읽기위치 < 끝 && 파일[읽기위치] != ')') {
            if (개수 == 16) { 실패("too many method arguments"); break; }
            함수인수형[함수 * 16 + 개수++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || 바이트() != ')') 실패("invalid method descriptor");
        함수반환[함수] = 서술형(끝, true); 함수인수수[함수] = 개수;
        if (읽기위치 != 끝) 실패("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !오류; 수++) { 상검사(짧은수(), 1); 건너(정수()); }
    }
    static int 명령길이(int 값) {
        if (값 == 16 || 값 == 18 || 값 == 21 || 값 == 25 || 값 == 54 || 값 == 58 || 값 == 188) return 2;
        if (값 == 17 || 값 == 19 || 값 == 132 || 값 >= 153 && 값 <= 167
            || 값 >= 178 && 값 <= 184 || 값 == 187 || 값 == 189 || 값 == 192 || 값 == 198 || 값 == 199) return 3;
        if (값 >= 0 && 값 <= 8 || 값 >= 26 && 값 <= 29 || 값 >= 42 && 값 <= 46 || 값 == 50
            || 값 >= 59 && 값 <= 62 || 값 >= 75 && 값 <= 79 || 값 == 83 || 값 == 87 || 값 == 89 || 값 == 95
            || 값 == 96 || 값 == 100 || 값 == 104 || 값 == 108 || 값 == 112 || 값 == 116
            || 값 == 120 || 값 == 122 || 값 == 124 || 값 == 126 || 값 == 128 || 값 == 130
            || 값 >= 145 && 값 <= 147 || 값 == 172 || 값 == 176 || 값 == 177 || 값 == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (정수() != 0xcafebabe) 실패("not a class file");
        int 부판 = 짧은수(), 판 = 짧은수();
        if (판 < 45 || 판 > 52 || 부판 != 0) 실패("supported class versions: 45..52, minor 0");
        상수수 = 짧은수();
        if (상수수 < 1 || 상수수 > 512) { 실패("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < 상수수 && !오류; 수++) {
            int 종류 = 바이트(); 상종류[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = 정수();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); 상나[수] = 짧은수(); }
            else 실패("unsupported constant type");
        }
        int 권한 = 짧은수();
        if ((권한 & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) 실패("unsupported class flags");
        클래스명 = 클래스문자(짧은수());
        if (!말(클래스문자(짧은수()), "java/lang/Object")) 실패("inheritance unsupported");
        if (짧은수() != 0) 실패("interfaces unsupported");
        if (짧은수() != 0) 실패("fields unsupported");
        함수수 = 짧은수();
        if (함수수 < 1 || 함수수 > 32) { 실패("method count limit (32)"); return; }
        for (int 수 = 0; 수 < 함수수 && !오류; 수++) {
            함수권한[수] = 짧은수(); 함수명[수] = 짧은수(); 함수형[수] = 짧은수();
            상검사(함수명[수], 1); 서술읽기(수);
            if ((함수권한[수] & (0x100 | 0x400 | 0x20)) != 0) 실패("native, abstract and synchronized methods unsupported");
            if ((함수권한[수] & 8) == 0 && !말(함수명[수], "<init>")) 실패("instance methods unsupported");
            if (말(함수명[수], "<clinit>")) 실패("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(함수명[앞], 함수명[수]) && 같은말(함수형[앞], 함수형[수])) 실패("duplicate method");
            int 개수 = 짧은수();
            for (int 속성 = 0; 속성 < 개수 && !오류; 속성++) {
                int Nùmene = 짧은수(), 길이 = 정수(), 시작 = 읽기위치;
                if (!범위(시작, 길이)) { 실패("truncated method attribute"); break; }
                if (말(Nùmene, "Code")) {
                    if (함수시작[수] != 0) 실패("duplicate Code attribute");
                    함수스택[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = 정수();
                    if (함수스택[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) 실패("method memory limits exceeded");
                    함수시작[수] = 읽기위치; 건너(코드길이); 함수끝[수] = 읽기위치;
                    if (짧은수() != 0) 실패("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != 시작 + 길이) 실패("Code attribute size mismatch");
                } else 건너(길이);
            }
            if (함수시작[수] == 0) 실패("missing Code attribute");
            int 칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !오류) {
                int 길이 = 명령길이(파일[칸]);
                if (길이 == 0 || 길이 > 함수끝[수] - 칸) { 실패("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += 길이;
            }
            // 실행하지 않는 경로에도 잘못된 분기 목적지를 허용하지 않는다.
            칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !오류) {
                int 값 = 파일[칸];
                if (값 >= 153 && 값 <= 167 || 값 == 198 || 값 == 199) {
                    int 목적 = 칸 + (short)(파일[칸 + 1] << 8 | 파일[칸 + 2]);
                    if (목적 < 함수시작[수] || 목적 >= 함수끝[수] || 경계[목적] != 수 + 1) 실패("invalid branch target");
                }
                칸 += 명령길이(값);
            }
        }
        if (!오류) 속성건너();
        if (읽기위치 != Mannària) 실패("extra class file data");
    }
    static int 할당(int 종류, int 길이) {
        if (길이 < 0 || 길이 > 힙.length - 힙끝 - 2) { 실패("object heap exhausted or negative array size"); return 0; }
        int 참조 = 힙끝; 힙끝 += 길이 + 2; 힙[참조] = 종류; 힙[참조 + 1] = 길이;
        return 참조;
    }
    static boolean 객체(int 참조, int 종류) {
        if (참조 < 1 || 참조 >= 힙끝 - 1 || 힙[참조] != 종류) { 실패("null or invalid object reference"); return false; }
        return true;
    }
    static int 상문자(int 번호) {
        if (!상검사(번호, 1)) return 0;
        if (문자열참조[번호] != 0) return 문자열참조[번호];
        int 참조 = 할당(1, 상나[번호]); if (오류) return 0;
        int 끝 = 상가[번호] + 상나[번호], 수 = 상가[번호], 길이 = 0;
        while (수 < 끝 && !오류) {
            int 값 = 파일[수++];
            if (값 == 0) 실패("invalid modified UTF-8");
            else if (값 >= 192 && 값 <= 223 && 수 < 끝) {
                int 다음 = 파일[수++];
                if ((다음 & 192) != 128) 실패("invalid modified UTF-8");
                값 = (값 & 31) << 6 | 다음 & 63;
                if (값 != 0 && 값 < 128) 실패("overlong modified UTF-8");
            } else if (값 >= 224 && 값 <= 239 && 수 + 1 < 끝) {
                int 가 = 파일[수++], 나 = 파일[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) 실패("invalid modified UTF-8");
                값 = (값 & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (값 < 2048) 실패("overlong modified UTF-8");
            } else if (값 >= 128) 실패("invalid modified UTF-8");
            힙[참조 + 2 + 길이++] = 값;
        }
        힙[참조 + 1] = 길이; 문자열참조[번호] = 참조; return 참조;
    }
    static int 호스트문자(String 값) {
        int 참조 = 할당(1, 값.length()); if (오류) return 0;
        for (int 수 = 0; 수 < 값.length(); 수++) 힙[참조 + 2 + 수] = 값.charAt(수);
        return 참조;
    }
    static void 글쓰기(int 참조) {
        if (참조 == 0) { 사용자.쓰기("null"); return; }
        if (!객체(참조, 1)) return;
        for (int 수 = 0; 수 < 힙[참조 + 1]; 수++) 사용자.문자쓰기(힙[참조 + 2 + 수]);
    }
    static int 수문자(int 값) {
        int 참조 = 할당(1, 11); if (오류) return 0;
        int 길이 = 0;
        if (값 < 0) 힙[참조 + 2 + 길이++] = '-'; else 값 = -값;
        int 자리 = 1000000000; boolean 시작 = false;
        while (자리 != 0) {
            int 수 = -(값 / 자리);
            if (수 != 0 || 시작 || 자리 == 1) { 힙[참조 + 2 + 길이++] = '0' + 수; 시작 = true; }
            값 %= 자리; 자리 /= 10;
        }
        힙[참조 + 1] = 길이; return 참조;
    }
    static int 정수해독(int 참조) {
        if (!객체(참조, 1)) return 0;
        int 길이 = 힙[참조 + 1], 수 = 0, 값 = 0; boolean 음수 = false;
        if (길이 > 0 && (힙[참조 + 2] == '-' || 힙[참조 + 2] == '+')) { 음수 = 힙[참조 + 2] == '-'; 수++; }
        if (수 == 길이) 실패("NumberFormatException");
        for (; 수 < 길이 && !오류; 수++) {
            int 숫자 = 힙[참조 + 2 + 수] - '0';
            if (숫자 < 0 || 숫자 > 9 || 값 < -214748364 || 값 == -214748364 && 숫자 > (음수 ? 8 : 7)) 실패("NumberFormatException");
            값 = 값 * 10 - 숫자;
        }
        return 음수 ? 값 : -값;
    }
    static void 넣기(int 값, int 형) {
        if (오류) return;
        if (틀 < 0 || 틀스택[틀] >= 함수스택[틀함수[틀]]) { 실패("operand stack overflow"); return; }
        int 칸 = 틀 * 128 + 틀스택[틀]++; 스택값[칸] = 값; 스택형[칸] = 형;
    }
    static int 빼기(int 형) {
        if (오류) return 0;
        if (틀 < 0 || 틀스택[틀] < 1) { 실패("operand stack underflow"); return 0; }
        int 칸 = 틀 * 128 + --틀스택[틀]; 반환형 = 스택형[칸];
        if (형 != 0 && 반환형 != 형) 실패("operand type mismatch");
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
        틀위치[틀]++; return 파일[위치];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void 이동(int 위치) {
        int 함수 = 틀함수[틀];
        if (위치 < 함수시작[함수] || 위치 >= 함수끝[함수] || 경계[위치] != 함수 + 1) 실패("invalid branch target");
        else 틀위치[틀] = 위치;
    }
    static void 호출(int 함수) {
        if (틀 == 31) { 실패("call stack limit (32)"); return; }
        int 다음 = 틀 + 1;
        for (int 수 = 0; 수 < 128; 수++) 지역형[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[함수] - 1; 수 >= 0; 수--) {
            지역값[다음 * 128 + 수] = 빼기(함수인수형[함수 * 16 + 수]); 지역형[다음 * 128 + 수] = 함수인수형[함수 * 16 + 수];
        }
        틀 = 다음; 틀함수[틀] = 함수; 틀위치[틀] = 함수시작[함수]; 틀스택[틀] = 0;
    }
    static void 반환(int 형) {
        if (형 != 함수반환[틀함수[틀]]) { 실패("return type mismatch"); return; }
        int 값 = 형 == 0 ? 0 : 빼기(형);
        틀--; if (틀 >= 0 && 형 != 0) 넣기(값, 형);
    }
    static int[] 흐름파일이름 = new int[64];
    static void 파일흐름호출(int 소유, int Nùmene, int 형식, int 명령) {
        boolean 출력 = 말(소유, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (명령 == 183 && 말(Nùmene, "<init>")) {
            boolean 이어 = false;
            if (출력 && 말(형식, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!말(형식, "(Ljava/lang/String;)V")) { 실패("unsupported file stream constructor"); return; }
            int 파일이름 = 빼기(2), 흐름 = 빼기(2);
            if (!객체(파일이름, 1) || !객체(흐름, 종류) || 오류) return;
            if (힙[흐름 + 3] != 0) { 실패("file stream already initialized"); return; }
            int 길이 = 힙[파일이름 + 1];
            if (길이 < 1 || 길이 > 63) { 실패("invalid file name length"); return; }
            for (int 칸 = 0; 칸 < 길이; 칸++) {
                int 값 = 힙[파일이름 + 2 + 칸];
                if (값 < 1 || 값 > 127) { 실패("file stream paths currently require ASCII"); return; }
                흐름파일이름[칸] = 값;
            }
            흐름파일이름[길이] = 0;
            int 서술자 = 사용자.파일서술자열기(흐름파일이름, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { 실패("FileNotFoundException: file open failed"); return; }
            힙[흐름 + 2] = 서술자; 힙[흐름 + 3] = 1;
            return;
        }
        if (명령 != 182) { 실패("invalid file stream invocation"); return; }
        int 동작 = -1, 값 = 0;
        if (말(Nùmene, "close") && 말(형식, "()V")) 동작 = 0;
        if (!출력 && 말(Nùmene, "read") && 말(형식, "()I")) 동작 = 1;
        if (출력 && 말(Nùmene, "write") && 말(형식, "(I)V")) { 동작 = 2; 값 = 빼기(1); }
        if (동작 < 0) { 실패("unsupported file stream method"); return; }
        int 흐름 = 빼기(2);
        if (!객체(흐름, 종류) || 오류) return;
        if (힙[흐름 + 3] == 0) { 실패("uninitialized file stream"); return; }
        int 서술자 = 힙[흐름 + 2];
        if (동작 == 0) {
            if (서술자 >= 0 && 사용자.파일서술자닫기(서술자) < 0) 실패("IOException: close failed");
            힙[흐름 + 2] = -1; return;
        }
        if (서술자 < 0) { 실패("IOException: stream closed"); return; }
        if (동작 == 1) {
            int 결과 = 사용자.파일한바이트읽기(서술자);
            if (결과 < -1) 실패("IOException: read failed"); else 넣기(결과, 1);
        } else if (사용자.파일한바이트쓰기(서술자, 값) != 1) 실패("IOException: write failed");
    }
    static void 함수호출(int 번호, int 명령) {
        if (!상검사(번호, 10)) return;
        int 소유 = 클래스문자(상가[번호]), Nùmene = 참조이름(상나[번호]), 형식 = 참조형식(상나[번호]);
        if (오류) return;
        if (같은말(소유, 클래스명)) {
            if (명령 != 184) { 실패("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < 함수수; 수++) if (같은말(Nùmene, 함수명[수]) && 같은말(형식, 함수형[수])) {
                if ((함수권한[수] & 8) == 0) 실패("method is not static"); else 호출(수);
                return;
            }
            실패("NoSuchMethodError"); return;
        }
        if (말(소유, "java/io/FileInputStream") || 말(소유, "java/io/FileOutputStream")) {
            파일흐름호출(소유, Nùmene, 형식, 명령); return;
        }
        if (명령 == 184 && 말(소유, "java/lang/Integer") && 말(Nùmene, "parseInt") && 말(형식, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (명령 == 182 && 말(소유, "java/io/PrintStream") && (말(Nùmene, "println") || 말(Nùmene, "print"))) {
            int 형 = 0, 값 = 0;
            if (말(형식, "(I)V")) { 형 = 1; 값 = 빼기(1); }
            else if (말(형식, "(Z)V")) { 형 = 2; 값 = 빼기(1); }
            else if (말(형식, "(C)V")) { 형 = 3; 값 = 빼기(1); }
            else if (말(형식, "(Ljava/lang/String;)V")) { 형 = 4; 값 = 빼기(2); }
            else if (!말(형식, "()V") || !말(Nùmene, "println")) 실패("unsupported print descriptor");
            if (빼기(2) != -1) 실패("invalid PrintStream receiver");
            if (오류) return;
            if (형 == 1) 자바도구.수쓰기(값);
            if (형 == 2) 사용자.쓰기(값 == 0 ? "false" : "true");
            if (형 == 3) 사용자.문자쓰기(값 & 65535);
            if (형 == 4) 글쓰기(값);
            if (말(Nùmene, "println")) 사용자.문자쓰기(10);
            return;
        }
        if (명령 == 182 && 말(소유, "java/lang/String")) {
            if (말(Nùmene, "length") && 말(형식, "()I")) {
                int 참조 = 빼기(2); if (객체(참조, 1)) 넣기(힙[참조 + 1], 1); return;
            }
            if (말(Nùmene, "charAt") && 말(형식, "(I)C")) {
                int 첨자 = 빼기(1), 참조 = 빼기(2);
                if (객체(참조, 1)) {
                    if (첨자 < 0 || 첨자 >= 힙[참조 + 1]) 실패("StringIndexOutOfBoundsException"); else 넣기(힙[참조 + 2 + 첨자], 1);
                }
                return;
            }
        }
        if (말(소유, "java/lang/StringBuilder")) {
            if (명령 == 183 && 말(Nùmene, "<init>") && 말(형식, "()V")) { 객체(빼기(2), 4); return; }
            if (명령 == 182 && 말(Nùmene, "toString") && 말(형식, "()Ljava/lang/String;")) {
                int 참조 = 빼기(2); if (객체(참조, 4)) 넣기(힙[참조 + 2] == 0 ? 호스트문자("") : 힙[참조 + 2], 2); return;
            }
            if (명령 == 182 && 말(Nùmene, "append")) {
                int Testu = 0;
                if (말(형식, "(I)Ljava/lang/StringBuilder;")) Testu = 수문자(빼기(1));
                else if (말(형식, "(Z)Ljava/lang/StringBuilder;")) Testu = 호스트문자(빼기(1) == 0 ? "false" : "true");
                else if (말(형식, "(C)Ljava/lang/StringBuilder;")) {
                    int 값 = 빼기(1); Testu = 할당(1, 1); if (!오류) 힙[Testu + 2] = 값 & 65535;
                }
                else if (말(형식, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Testu = 빼기(2); if (Testu == 0) Testu = 호스트문자("null"); }
                else { 실패("unsupported StringBuilder append"); return; }
                int 참조 = 빼기(2); if (!객체(참조, 4) || !객체(Testu, 1)) return;
                int 앞 = 힙[참조 + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], 뒤길이 = 힙[Testu + 1];
                int 새글 = 할당(1, 앞길이 + 뒤길이); if (오류) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < 뒤길이; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[Testu + 2 + 수];
                힙[참조 + 2] = 새글; 넣기(참조, 2); return;
            }
        }
        실패("unsupported library method");
    }
    static int 배열칸(int 참조, int 첨자, int 형) {
        if (!객체(참조, 형)) return 0;
        if (첨자 < 0 || 첨자 >= 힙[참조 + 1]) { 실패("ArrayIndexOutOfBoundsException"); return 0; }
        return 참조 + 2 + 첨자;
    }
    static void 실행() {
        int 남음 = 500000;
        while (틀 >= 0 && !오류) {
            if (--남음 == 0) { 실패("instruction limit (500000)"); break; }
            int 시작 = 틀위치[틀], 값 = 명바();
            if (오류) break;
            if (값 == 0) continue;
            if (값 == 1) { 넣기(0, 2); continue; }
            if (값 >= 2 && 값 <= 8) { 넣기(값 - 3, 1); continue; }
            if (값 == 16) { 넣기((byte)명바(), 1); continue; }
            if (값 == 17) { 넣기((short)명짧(), 1); continue; }
            if (값 == 18 || 값 == 19) {
                int 수 = 값 == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= 상수수) 실패("invalid ldc constant");
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
            if (값 == 46 || 값 == 50) {
                int 첨자 = 빼기(1), 참조 = 빼기(2), 칸 = 배열칸(참조, 첨자, 값 == 46 ? 2 : 3);
                if (!오류) 넣기(힙[칸], 값 == 46 ? 1 : 2); continue;
            }
            if (값 == 79 || 값 == 83) {
                int 원소 = 빼기(값 == 79 ? 1 : 2), 첨자 = 빼기(1), 참조 = 빼기(2), 칸 = 배열칸(참조, 첨자, 값 == 79 ? 2 : 3);
                if (값 == 83 && 원소 != 0) 객체(원소, 1);
                if (!오류) 힙[칸] = 원소; continue;
            }
            if (값 == 87) { 빼기(0); continue; }
            if (값 == 89) { int 가 = 빼기(0), 형 = 반환형; 넣기(가, 형); 넣기(가, 형); continue; }
            if (값 == 95) { int 가 = 빼기(0), 가형 = 반환형, 나 = 빼기(0), 나형 = 반환형; 넣기(가, 가형); 넣기(나, 나형); continue; }
            if (값 == 96 || 값 == 100 || 값 == 104 || 값 == 108 || 값 == 112 || 값 == 120
                || 값 == 122 || 값 == 124 || 값 == 126 || 값 == 128 || 값 == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), 결과 = 0;
                if ((값 == 108 || 값 == 112) && 나 == 0) { 실패("ArithmeticException: / by zero"); continue; }
                if (값 == 96) 결과 = 가 + 나;
                if (값 == 100) 결과 = 가 - 나;
                if (값 == 104) 결과 = 가 * 나;
                if (값 == 108) 결과 = 가 / 나;
                if (값 == 112) 결과 = 가 % 나;
                if (값 == 120) 결과 = 가 << 나;
                if (값 == 122) 결과 = 가 >> 나;
                if (값 == 124) 결과 = 가 >>> 나;
                if (값 == 126) 결과 = 가 & 나;
                if (값 == 128) 결과 = 가 | 나;
                if (값 == 130) 결과 = 가 ^ 나;
                넣기(결과, 1); continue;
            }
            if (값 == 116) { 넣기(-빼기(1), 1); continue; }
            if (값 == 132) {
                int 지역 = 명바(), 증분 = (byte)명바(); 지역읽기(지역, 1); 넣기(빼기(1) + 증분, 1); 지역쓰기(지역, 1); continue;
            }
            if (값 >= 145 && 값 <= 147) {
                int 수 = 빼기(1); 넣기(값 == 145 ? (byte)수 : 값 == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (값 >= 153 && 값 <= 167 || 값 == 198 || 값 == 199) {
                int 목적 = 시작 + (short)명짧(); boolean 갈까 = 값 == 167;
                if (값 >= 153 && 값 <= 158) {
                    int 수 = 빼기(1); 갈까 = 값 == 153 ? 수 == 0 : 값 == 154 ? 수 != 0 : 값 == 155 ? 수 < 0 : 값 == 156 ? 수 >= 0 : 값 == 157 ? 수 > 0 : 수 <= 0;
                } else if (값 >= 159 && 값 <= 166) {
                    int 나 = 빼기(값 >= 165 ? 2 : 1), 가 = 빼기(값 >= 165 ? 2 : 1);
                    갈까 = 값 == 159 || 값 == 165 ? 가 == 나 : 값 == 160 || 값 == 166 ? 가 != 나 : 값 == 161 ? 가 < 나 : 값 == 162 ? 가 >= 나 : 값 == 163 ? 가 > 나 : 가 <= 나;
                } else if (값 == 198 || 값 == 199) { int 수 = 빼기(2); 갈까 = 값 == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) 이동(목적); continue;
            }
            if (값 == 172 || 값 == 176 || 값 == 177) { 반환(값 == 172 ? 1 : 값 == 176 ? 2 : 0); continue; }
            if (값 == 178) {
                int 수 = 명짧(); if (!상검사(수, 9)) continue;
                if (!말(클래스문자(상가[수]), "java/lang/System") || !말(참조이름(상나[수]), "out")
                    || !말(참조형식(상나[수]), "Ljava/io/PrintStream;")) 실패("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (값 == 182 || 값 == 183 || 값 == 184) { 함수호출(명짧(), 값); continue; }
            if (값 == 187) {
                int Nùmene = 클래스문자(명짧());
                if (말(Nùmene, "java/lang/StringBuilder")) 넣기(할당(4, 1), 2);
                else if (말(Nùmene, "java/io/FileInputStream") || 말(Nùmene, "java/io/FileOutputStream")) {
                    int 참조 = 할당(말(Nùmene, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!오류) { 힙[참조 + 2] = -1; 넣기(참조, 2); }
                } else 실패("unsupported object construction");
                continue;
            }
            if (값 == 188 || 값 == 189) {
                if (값 == 188) { if (명바() != 10) 실패("only int[] newarray is supported"); }
                else if (!말(클래스문자(명짧()), "java/lang/String")) 실패("only String[] anewarray is supported");
                int 길이 = 빼기(1); 넣기(할당(값 == 188 ? 2 : 3, 길이), 2); continue;
            }
            if (값 == 190) {
                int 참조 = 빼기(2);
                if (참조 < 1 || 참조 >= 힙끝 - 1 || (힙[참조] != 2 && 힙[참조] != 3)) 실패("null or invalid array");
                else 넣기(힙[참조 + 1], 1); continue;
            }
            if (값 == 192) {
                int Nùmene = 클래스문자(명짧()), 참조 = 빼기(2);
                if (!말(Nùmene, "java/lang/String")) 실패("unsupported checkcast");
                else if (참조 != 0) 객체(참조, 1);
                넣기(참조, 2); continue;
            }
            실패("unsupported bytecode");
        }
    }
    public static int 시작() {
        if (사용자.인수개수() == 1 && 자바도구.같음(사용자.인수(0), "-version")) {
            사용자.쓰기("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (사용자.인수개수() < 1) { 사용자.쓰기("Usage: java CLASS [ARGS]\n"); return 2; }
        int 길이 = 자바도구.Nùmene(파일명, 사용자.인수(0));
        if (길이 < 1 || 길이 > 57) { 사용자.쓰기("java: invalid class name\n"); return 2; }
        파일명[길이] = '.'; 파일명[길이 + 1] = 'c'; 파일명[길이 + 2] = 'l'; 파일명[길이 + 3] = 'a'; 파일명[길이 + 4] = 's'; 파일명[길이 + 5] = 's';
        Mannària = 사용자.파일읽기(파일명, 파일);
        if (Mannària < 0) { 사용자.쓰기("java: cannot read class: "); 자바도구.수쓰기(Mannària); 사용자.문자쓰기(10); return 1; }
        클래스읽기(); if (오류) return 1;
        int 문자이름 = 상문자(클래스명);
        if (!오류 && 힙[문자이름 + 1] != 길이) 실패("class name does not match file");
        for (int 수 = 0; 수 < 길이 && !오류; 수++) if (힙[문자이름 + 2 + 수] != 파일명[수]) 실패("class name does not match file");
        int 진입 = -1;
        for (int 수 = 0; 수 < 함수수; 수++) if (말(함수명[수], "main") && 말(함수형[수], "([Ljava/lang/String;)V") && (함수권한[수] & 9) == 9) 진입 = 수;
        if (진입 < 0) 실패("public static void main(String[] args) required");
        if (오류) return 1;
        int 인수 = 할당(3, 사용자.인수개수() - 1);
        for (int 수 = 1; 수 < 사용자.인수개수() && !오류; 수++) 힙[인수 + 1 + 수] = 호스트문자(사용자.인수(수));
        틀 = 0; 틀함수[0] = 진입; 틀위치[0] = 함수시작[진입]; 지역값[0] = 인수; 지역형[0] = 2;
        실행(); return 오류 ? 1 : 0;
    }
}
