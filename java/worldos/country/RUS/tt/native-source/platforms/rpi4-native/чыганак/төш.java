// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class төш {
    static int[] 작업횟수 = new int[3];
    static int[] мәсьәлә_SUM = new int[3];
    static int мәсьәлә_тәртипкә_салу;
    static int мәсьәлә_хата;
    static int 난수씨 = 17;

    static void раслау(boolean шарт, int INDEX) {
        if (!шарт) { 단말.язу("FAIL "); 단말.수(INDEX); такта.туктату(INDEX); }
    }
    static int тармак(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] кайтару_МАССИВ(int[] МАССИВ_VALUE) { return МАССИВ_VALUE; }
    static void 계산시험() {
        int VALUE = 난수씨;
        раслау(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        раслау(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        раслау(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        раслау((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        раслау((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] МАССИВ_VALUE = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < МАССИВ_VALUE.length; Loop_INDEX++) МАССИВ_VALUE[Loop_INDEX] = Loop_INDEX * VALUE;
        МАССИВ_VALUE[2]++;
        раслау(кайтару_МАССИВ(МАССИВ_VALUE) == МАССИВ_VALUE && МАССИВ_VALUE[2] == 35 && МАССИВ_VALUE[4] == 68, 6);
        раслау(тармак(VALUE - 117) == 7 && тармак(VALUE - 15) == 9 && тармак(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String Mäten = "한글 😀";
        раслау(Mäten.length() == 5 && Mäten.charAt(0) == '한' && Mäten.charAt(3) == 0xd83d, 8);
        раслау(такта.процессор_рөхсәтләр_дәрәҗә() == 1, 9);
        단말.язу("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_процессор 전후 локаль_даирә 변수가 보존되는지 검사: 각 작업은 독립된 машина 스택을 쓴다.
        int локаль_VALUE = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (мәсьәлә_тәртипкә_салу % 2 + 1 != INDEX) мәсьәлә_хата++;
            мәсьәлә_тәртипкә_салу++;
            локаль_VALUE += Loop_INDEX + INDEX;
            мәсьәлә_SUM[INDEX] = локаль_VALUE;
            작업횟수[INDEX]++;
            такта.YIELD_процессор();
            if (локаль_VALUE != мәсьәлә_SUM[INDEX]) мәсьәлә_хата++;
        }
    }
    static void 작업시험() {
        мәсьәлә_тәртипкә_салу = 0; мәсьәлә_хата = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        раслау(такта.Төзү_мәсьәлә(1) == 0 && такта.Төзү_мәсьәлә(2) == 0, 20);
        int әйләндерү_COUNT = 0;
        while (такта.мәсьәлә_халәт(1) != 0 || такта.мәсьәлә_халәт(2) != 0) {
            такта.YIELD_процессор();
            раслау(++әйләндерү_COUNT < 100, 21);
        }
        раслау(작업횟수[1] == 10 && 작업횟수[2] == 10 && мәсьәлә_тәртипкә_салу == 20 && мәсьәлә_хата == 0, 22);
        раслау(мәсьәлә_SUM[1] == 155 && мәсьәлә_SUM[2] == 265, 23);
        단말.язу("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int Вертикаль_урнаштыру, int 너비, int 높이, int 색) {
        for (int 세로좌표 = Вертикаль_урнаштыру; 세로좌표 < Вертикаль_урнаштыру + 높이; 세로좌표++)
            for (int X_координатасы = 가로; X_координатасы < 가로 + 너비; X_координатасы++) такта.화면점(X_координатасы, 세로좌표, 색);
    }
    static void 화면() {
        if (такта.화면준비() == 0) { 단말.язу("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, такта.화면너비(), такта.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.язу("FRAMEBUFFER PASS "); 단말.수(такта.화면너비()); 단말.문자('x');
        단말.수(такта.화면높이()); 단말.язу(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int үлчәм = такта.씨플러스시험();
        раслау(үлчәм == 0, 100 + үлчәм);
        단말.язу("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        раслау(такта.чек_кулланучы_кушымта() == 0, 200);
        단말.язу("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = такта.эшләтү_кулланучы_кушымта(0);
        if (처음결과 != 0) { 단말.язу("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        раслау(처음결과 == 0, 201);
        단말.язу("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.язу("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int үлчәм = такта.эшләтү_кулланучы_кушымта(INDEX + 1);
            if (үлчәм != 예상[INDEX]) { 단말.язу("USER RESULT "); 단말.수(үлчәм); 단말.문자(10); }
            раслау(үлчәм == 예상[INDEX], 210 + INDEX);
        }
        раслау(такта.эшләтү_кулланучы_кушымта(0) == 0, 220);
        단말.язу("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int үлчәм = такта.эшләтү_кулланучы_кушымта(9);
        if (үлчәм != 0) { 단말.язу("UDP RESULT "); 단말.수(үлчәм); 단말.문자(10); }
        раслау(үлчәм == 0, 230);
    }
    static void msinfo32_exe() {
        단말.язу("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.язу("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.язу("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.язу("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.язу("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void эшләтү() {
        단말.язу("WorldOS tt · tt · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.язу("NATIVE READY\n");
        명령해석기.үтәргә_команда();
    }
}
