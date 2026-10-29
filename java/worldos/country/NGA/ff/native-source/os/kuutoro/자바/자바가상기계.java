// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. fiilde/스택/참조/분기 경계를 실행 중 검사한다. */
public final class 자바가상기계 {
    static int[] fiilde = new int[16384], fiilde_innde_binndi = new int[64];
    static int[] 상종류 = new int[512], 상가 = new int[512], 상나 = new int[512], 문자열참조 = new int[512];
    static int[] 함수명 = new int[32], 함수형 = new int[32], 함수권한 = new int[32];
    static int[] 함수시작 = new int[32], 함수끝 = new int[32], 함수스택 = new int[32], 함수지역 = new int[32];
    static int[] 함수인수수 = new int[32], 함수인수형 = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] nokkuwal_njaru = new int[4096], 지역형 = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] 틀함수 = new int[32], 틀위치 = new int[32], 틀스택 = new int[32];
    static int[] 힙 = new int[8192];
    static int waylude_etannde, 읽기위치, 상수수, 함수수, fedde_innde, taƴtinnde_joopirdu = -1, 힙끝 = 1, 반환형;
    static boolean juumre;

    static void ella_njaru(String 말) {
        if (!juumre) { kuutoro.winndude("JVM error: "); kuutoro.winndude(말); kuutoro.winndude_alkulal_njaru(10); }
        juumre = true;
    }
    static boolean kilip(int huutoraade, int njuuteendi_njaru) { return huutoraade >= 0 && njuuteendi_njaru >= 0 && huutoraade <= waylude_etannde - njuuteendi_njaru; }
    static int oktee_njaru() {
        if (!kilip(읽기위치, 1)) { ella_njaru("truncated class file"); return 0; }
        return fiilde[읽기위치++];
    }
    static int 짧은수() { return oktee_njaru() << 8 | oktee_njaru(); }
    static int 정수() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int njuuteendi_njaru) { if (!kilip(읽기위치, njuuteendi_njaru)) ella_njaru("invalid attribute size"); else 읽기위치 += njuuteendi_njaru; }
    static boolean 상검사(int 수, int 종류) {
        if (수 <= 0 || 수 >= 상수수 || 상종류[수] != 종류) { ella_njaru("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int huutoraade, int njuuteendi_njaru, String 말) {
        if (!kilip(huutoraade, njuuteendi_njaru) || njuuteendi_njaru != 말.length()) return false;
        for (int 수 = 0; 수 < njuuteendi_njaru; 수++) if (fiilde[huutoraade + 수] != 말.charAt(수)) return false;
        return true;
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
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !juumre; 수++) { 상검사(짧은수(), 1); 건너(정수()); }
    }
    static int ginol_njuuteendi(int njaru) {
        if (njaru == 16 || njaru == 18 || njaru == 21 || njaru == 25 || njaru == 54 || njaru == 58 || njaru == 188) return 2;
        if (njaru == 17 || njaru == 19 || njaru == 132 || njaru >= 153 && njaru <= 167
            || njaru >= 178 && njaru <= 184 || njaru == 187 || njaru == 189 || njaru == 192 || njaru == 198 || njaru == 199) return 3;
        if (njaru >= 0 && njaru <= 8 || njaru >= 26 && njaru <= 29 || njaru >= 42 && njaru <= 46 || njaru == 50
            || njaru >= 59 && njaru <= 62 || njaru >= 75 && njaru <= 79 || njaru == 83 || njaru == 87 || njaru == 89 || njaru == 95
            || njaru == 96 || njaru == 100 || njaru == 104 || njaru == 108 || njaru == 112 || njaru == 116
            || njaru == 120 || njaru == 122 || njaru == 124 || njaru == 126 || njaru == 128 || njaru == 130
            || njaru >= 145 && njaru <= 147 || njaru == 172 || njaru == 176 || njaru == 177 || njaru == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (정수() != 0xcafebabe) ella_njaru("not a class file");
        int 부판 = 짧은수(), yamre_njaru = 짧은수();
        if (yamre_njaru < 45 || yamre_njaru > 52 || 부판 != 0) ella_njaru("supported class versions: 45..52, minor 0");
        상수수 = 짧은수();
        if (상수수 < 1 || 상수수 > 512) { ella_njaru("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < 상수수 && !juumre; 수++) {
            int 종류 = oktee_njaru(); 상종류[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = 정수();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); 상나[수] = 짧은수(); }
            else ella_njaru("unsupported constant type");
        }
        int 권한 = 짧은수();
        if ((권한 & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) ella_njaru("unsupported class flags");
        fedde_innde = fedde_innde_binndi(짧은수());
        if (!말(fedde_innde_binndi(짧은수()), "java/lang/Object")) ella_njaru("inheritance unsupported");
        if (짧은수() != 0) ella_njaru("interfaces unsupported");
        if (짧은수() != 0) ella_njaru("fields unsupported");
        함수수 = 짧은수();
        if (함수수 < 1 || 함수수 > 32) { ella_njaru("method count limit (32)"); return; }
        for (int 수 = 0; 수 < 함수수 && !juumre; 수++) {
            함수권한[수] = 짧은수(); 함수명[수] = 짧은수(); 함수형[수] = 짧은수();
            상검사(함수명[수], 1); 서술읽기(수);
            if ((함수권한[수] & (0x100 | 0x400 | 0x20)) != 0) ella_njaru("native, abstract and synchronized methods unsupported");
            if ((함수권한[수] & 8) == 0 && !말(함수명[수], "<init>")) ella_njaru("instance methods unsupported");
            if (말(함수명[수], "<clinit>")) ella_njaru("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(함수명[앞], 함수명[수]) && 같은말(함수형[앞], 함수형[수])) ella_njaru("duplicate method");
            int 개수 = 짧은수();
            for (int mbaadi_njaru = 0; mbaadi_njaru < 개수 && !juumre; mbaadi_njaru++) {
                int innde = 짧은수(), njuuteendi_njaru = 정수(), huutoraade = 읽기위치;
                if (!kilip(huutoraade, njuuteendi_njaru)) { ella_njaru("truncated method attribute"); break; }
                if (말(innde, "Code")) {
                    if (함수시작[수] != 0) ella_njaru("duplicate Code attribute");
                    함수스택[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = 정수();
                    if (함수스택[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) ella_njaru("method memory limits exceeded");
                    함수시작[수] = 읽기위치; 건너(코드길이); 함수끝[수] = 읽기위치;
                    if (짧은수() != 0) ella_njaru("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != huutoraade + njuuteendi_njaru) ella_njaru("Code attribute size mismatch");
                } else 건너(njuuteendi_njaru);
            }
            if (함수시작[수] == 0) ella_njaru("missing Code attribute");
            int 칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !juumre) {
                int njuuteendi_njaru = ginol_njuuteendi(fiilde[칸]);
                if (njuuteendi_njaru == 0 || njuuteendi_njaru > 함수끝[수] - 칸) { ella_njaru("unsupported or truncated bytecode"); break; }
                경계[칸] = 수 + 1; 칸 += njuuteendi_njaru;
            }
            // 실행하지 않는 경로에도 잘못된 분기 목적지를 허용하지 않는다.
            칸 = 함수시작[수];
            while (칸 < 함수끝[수] && !juumre) {
                int njaru = fiilde[칸];
                if (njaru >= 153 && njaru <= 167 || njaru == 198 || njaru == 199) {
                    int tiindaare_njaru = 칸 + (short)(fiilde[칸 + 1] << 8 | fiilde[칸 + 2]);
                    if (tiindaare_njaru < 함수시작[수] || tiindaare_njaru >= 함수끝[수] || 경계[tiindaare_njaru] != 수 + 1) ella_njaru("invalid branch target");
                }
                칸 += ginol_njuuteendi(njaru);
            }
        }
        if (!juumre) 속성건너();
        if (읽기위치 != waylude_etannde) ella_njaru("extra class file data");
    }
    static int 할당(int 종류, int njuuteendi_njaru) {
        if (njuuteendi_njaru < 0 || njuuteendi_njaru > 힙.length - 힙끝 - 2) { ella_njaru("object heap exhausted or negative array size"); return 0; }
        int 참조 = 힙끝; 힙끝 += njuuteendi_njaru + 2; 힙[참조] = 종류; 힙[참조 + 1] = njuuteendi_njaru;
        return 참조;
    }
    static boolean huunde_njaru(int 참조, int 종류) {
        if (참조 < 1 || 참조 >= 힙끝 - 1 || 힙[참조] != 종류) { ella_njaru("null or invalid object reference"); return false; }
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
        if (taƴtinnde_joopirdu == 31) { ella_njaru("call stack limit (32)"); return; }
        int 다음 = taƴtinnde_joopirdu + 1;
        for (int 수 = 0; 수 < 128; 수++) 지역형[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[juɓɓol_njaru] - 1; 수 >= 0; 수--) {
            nokkuwal_njaru[다음 * 128 + 수] = 빼기(함수인수형[juɓɓol_njaru * 16 + 수]); 지역형[다음 * 128 + 수] = 함수인수형[juɓɓol_njaru * 16 + 수];
        }
        taƴtinnde_joopirdu = 다음; 틀함수[taƴtinnde_joopirdu] = juɓɓol_njaru; 틀위치[taƴtinnde_joopirdu] = 함수시작[juɓɓol_njaru]; 틀스택[taƴtinnde_joopirdu] = 0;
    }
    static void 반환(int 형) {
        if (형 != 함수반환[틀함수[taƴtinnde_joopirdu]]) { ella_njaru("return type mismatch"); return; }
        int njaru = 형 == 0 ? 0 : 빼기(형);
        taƴtinnde_joopirdu--; if (taƴtinnde_joopirdu >= 0 && 형 != 0) 넣기(njaru, 형);
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
                if (njaru < 1 || njaru > 127) { ella_njaru("file stream paths currently require ASCII"); return; }
                waraango_fiilde_innde[칸] = njaru;
            }
            waraango_fiilde_innde[njuuteendi_njaru] = 0;
            int 서술자 = kuutoro.파일서술자열기(waraango_fiilde_innde, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { ella_njaru("FileNotFoundException: file open failed"); return; }
            힙[waraango_njaru + 2] = 서술자; 힙[waraango_njaru + 3] = 1;
            return;
        }
        if (ginol != 182) { ella_njaru("invalid file stream invocation"); return; }
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
            if (결과 < -1) ella_njaru("IOException: read failed"); else 넣기(결과, 1);
        } else if (kuutoro.파일한바이트쓰기(서술자, njaru) != 1) ella_njaru("IOException: write failed");
    }
    static void 함수호출(int joopirdu, int ginol) {
        if (!상검사(joopirdu, 10)) return;
        int 소유 = fedde_innde_binndi(상가[joopirdu]), innde = 참조이름(상나[joopirdu]), formaa_njaru = 참조형식(상나[joopirdu]);
        if (juumre) return;
        if (같은말(소유, fedde_innde)) {
            if (ginol != 184) { ella_njaru("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < 함수수; 수++) if (같은말(innde, 함수명[수]) && 같은말(formaa_njaru, 함수형[수])) {
                if ((함수권한[수] & 8) == 0) ella_njaru("method is not static"); else 호출(수);
                return;
            }
            ella_njaru("NoSuchMethodError"); return;
        }
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
        ella_njaru("unsupported library method");
    }
    static int 배열칸(int 참조, int limtoore_sakkiinde_njaru, int 형) {
        if (!huunde_njaru(참조, 형)) return 0;
        if (limtoore_sakkiinde_njaru < 0 || limtoore_sakkiinde_njaru >= 힙[참조 + 1]) { ella_njaru("ArrayIndexOutOfBoundsException"); return 0; }
        return 참조 + 2 + limtoore_sakkiinde_njaru;
    }
    static void 실행() {
        int 남음 = 500000;
        while (taƴtinnde_joopirdu >= 0 && !juumre) {
            if (--남음 == 0) { ella_njaru("instruction limit (500000)"); break; }
            int huutoraade = 틀위치[taƴtinnde_joopirdu], njaru = 명바();
            if (juumre) break;
            if (njaru == 0) continue;
            if (njaru == 1) { 넣기(0, 2); continue; }
            if (njaru >= 2 && njaru <= 8) { 넣기(njaru - 3, 1); continue; }
            if (njaru == 16) { 넣기((byte)명바(), 1); continue; }
            if (njaru == 17) { 넣기((short)명짧(), 1); continue; }
            if (njaru == 18 || njaru == 19) {
                int 수 = njaru == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= 상수수) ella_njaru("invalid ldc constant");
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
            if (njaru == 46 || njaru == 50) {
                int limtoore_sakkiinde_njaru = 빼기(1), 참조 = 빼기(2), 칸 = 배열칸(참조, limtoore_sakkiinde_njaru, njaru == 46 ? 2 : 3);
                if (!juumre) 넣기(힙[칸], njaru == 46 ? 1 : 2); continue;
            }
            if (njaru == 79 || njaru == 83) {
                int geɗal_geɗel = 빼기(njaru == 79 ? 1 : 2), limtoore_sakkiinde_njaru = 빼기(1), 참조 = 빼기(2), 칸 = 배열칸(참조, limtoore_sakkiinde_njaru, njaru == 79 ? 2 : 3);
                if (njaru == 83 && geɗal_geɗel != 0) huunde_njaru(geɗal_geɗel, 1);
                if (!juumre) 힙[칸] = geɗal_geɗel; continue;
            }
            if (njaru == 87) { 빼기(0); continue; }
            if (njaru == 89) { int 가 = 빼기(0), 형 = 반환형; 넣기(가, 형); 넣기(가, 형); continue; }
            if (njaru == 95) { int 가 = 빼기(0), 가형 = 반환형, 나 = 빼기(0), 나형 = 반환형; 넣기(가, 가형); 넣기(나, 나형); continue; }
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
            if (njaru == 178) {
                int 수 = 명짧(); if (!상검사(수, 9)) continue;
                if (!말(fedde_innde_binndi(상가[수]), "java/lang/System") || !말(참조이름(상나[수]), "out")
                    || !말(참조형식(상나[수]), "Ljava/io/PrintStream;")) ella_njaru("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (njaru == 182 || njaru == 183 || njaru == 184) { 함수호출(명짧(), njaru); continue; }
            if (njaru == 187) {
                int innde = fedde_innde_binndi(명짧());
                if (말(innde, "java/lang/StringBuilder")) 넣기(할당(4, 1), 2);
                else if (말(innde, "java/io/FileInputStream") || 말(innde, "java/io/FileOutputStream")) {
                    int 참조 = 할당(말(innde, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!juumre) { 힙[참조 + 2] = -1; 넣기(참조, 2); }
                } else ella_njaru("unsupported object construction");
                continue;
            }
            if (njaru == 188 || njaru == 189) {
                if (njaru == 188) { if (명바() != 10) ella_njaru("only int[] newarray is supported"); }
                else if (!말(fedde_innde_binndi(명짧()), "java/lang/String")) ella_njaru("only String[] anewarray is supported");
                int njuuteendi_njaru = 빼기(1); 넣기(할당(njaru == 188 ? 2 : 3, njuuteendi_njaru), 2); continue;
            }
            if (njaru == 190) {
                int 참조 = 빼기(2);
                if (참조 < 1 || 참조 >= 힙끝 - 1 || (힙[참조] != 2 && 힙[참조] != 3)) ella_njaru("null or invalid array");
                else 넣기(힙[참조 + 1], 1); continue;
            }
            if (njaru == 192) {
                int innde = fedde_innde_binndi(명짧()), 참조 = 빼기(2);
                if (!말(innde, "java/lang/String")) ella_njaru("unsupported checkcast");
                else if (참조 != 0) huunde_njaru(참조, 1);
                넣기(참조, 2); continue;
            }
            ella_njaru("unsupported bytecode");
        }
    }
    public static int huutoraade() {
        if (kuutoro.인수개수() == 1 && 자바도구.같음(kuutoro.인수(0), "-version")) {
            kuutoro.winndude("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (kuutoro.인수개수() < 1) { kuutoro.winndude("Usage: java CLASS [ARGS]\n"); return 2; }
        int njuuteendi_njaru = 자바도구.innde(fiilde_innde_binndi, kuutoro.인수(0));
        if (njuuteendi_njaru < 1 || njuuteendi_njaru > 57) { kuutoro.winndude("java: invalid class name\n"); return 2; }
        fiilde_innde_binndi[njuuteendi_njaru] = '.'; fiilde_innde_binndi[njuuteendi_njaru + 1] = 'c'; fiilde_innde_binndi[njuuteendi_njaru + 2] = 'l'; fiilde_innde_binndi[njuuteendi_njaru + 3] = 'a'; fiilde_innde_binndi[njuuteendi_njaru + 4] = 's'; fiilde_innde_binndi[njuuteendi_njaru + 5] = 's';
        waylude_etannde = kuutoro.파일읽기(fiilde_innde_binndi, fiilde);
        if (waylude_etannde < 0) { kuutoro.winndude("java: cannot read class: "); 자바도구.수쓰기(waylude_etannde); kuutoro.winndude_alkulal_njaru(10); return 1; }
        클래스읽기(); if (juumre) return 1;
        int alkulal_innde = 상문자(fedde_innde);
        if (!juumre && 힙[alkulal_innde + 1] != njuuteendi_njaru) ella_njaru("class name does not match file");
        for (int 수 = 0; 수 < njuuteendi_njaru && !juumre; 수++) if (힙[alkulal_innde + 2 + 수] != fiilde_innde_binndi[수]) ella_njaru("class name does not match file");
        int naatnugol_toɓɓere_njaru = -1;
        for (int 수 = 0; 수 < 함수수; 수++) if (말(함수명[수], "main") && 말(함수형[수], "([Ljava/lang/String;)V") && (함수권한[수] & 9) == 9) naatnugol_toɓɓere_njaru = 수;
        if (naatnugol_toɓɓere_njaru < 0) ella_njaru("public static void main(String[] args) required");
        if (juumre) return 1;
        int 인수 = 할당(3, kuutoro.인수개수() - 1);
        for (int 수 = 1; 수 < kuutoro.인수개수() && !juumre; 수++) 힙[인수 + 1 + 수] = njaatigi_alkulal(kuutoro.인수(수));
        taƴtinnde_joopirdu = 0; 틀함수[0] = naatnugol_toɓɓere_njaru; 틀위치[0] = 함수시작[naatnugol_toɓɓere_njaru]; nokkuwal_njaru[0] = 인수; 지역형[0] = 2;
        실행(); return juumre ? 1 : 0;
    }
}
