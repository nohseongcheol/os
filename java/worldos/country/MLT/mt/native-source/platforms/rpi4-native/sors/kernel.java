// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class kernel {
    static int[] 작업횟수 = new int[3];
    static int[] attività_SUM = new int[3];
    static int attività_ordni;
    static int attività_żball;
    static int 난수씨 = 17;

    static void vverifika(boolean kondizzjoni, int INDEX) {
        if (!kondizzjoni) { 단말.kiteb("FAIL "); 단말.수(INDEX); bord.waqqaf(INDEX); }
    }
    static int fergħa(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] ARRAY_VALUE) { return ARRAY_VALUE; }
    static void 계산시험() {
        int VALUE = 난수씨;
        vverifika(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        vverifika(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        vverifika(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        vverifika((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        vverifika((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_VALUE = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < ARRAY_VALUE.length; Loop_INDEX++) ARRAY_VALUE[Loop_INDEX] = Loop_INDEX * VALUE;
        ARRAY_VALUE[2]++;
        vverifika(배열돌려주기(ARRAY_VALUE) == ARRAY_VALUE && ARRAY_VALUE[2] == 35 && ARRAY_VALUE[4] == 68, 6);
        vverifika(fergħa(VALUE - 117) == 7 && fergħa(VALUE - 15) == 9 && fergħa(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String SMS = "한글 😀";
        vverifika(SMS.length() == 5 && SMS.charAt(0) == '한' && SMS.charAt(3) == 0xd83d, 8);
        vverifika(bord.CPU_permess_livell() == 1, 9);
        단말.kiteb("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_CPU 전후 lokali_ambitu 변수가 보존되는지 검사: 각 작업은 독립된 kompjuter 스택을 쓴다.
        int lokali_VALUE = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (attività_ordni % 2 + 1 != INDEX) attività_żball++;
            attività_ordni++;
            lokali_VALUE += Loop_INDEX + INDEX;
            attività_SUM[INDEX] = lokali_VALUE;
            작업횟수[INDEX]++;
            bord.YIELD_CPU();
            if (lokali_VALUE != attività_SUM[INDEX]) attività_żball++;
        }
    }
    static void 작업시험() {
        attività_ordni = 0; attività_żball = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        vverifika(bord.ħalaq_attività(1) == 0 && bord.ħalaq_attività(2) == 0, 20);
        int rotazzjoni_COUNT = 0;
        while (bord.attività_stat(1) != 0 || bord.attività_stat(2) != 0) {
            bord.YIELD_CPU();
            vverifika(++rotazzjoni_COUNT < 100, 21);
        }
        vverifika(작업횟수[1] == 10 && 작업횟수[2] == 10 && attività_ordni == 20 && attività_żball == 0, 22);
        vverifika(attività_SUM[1] == 155 && attività_SUM[2] == 265, 23);
        단말.kiteb("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int Vertikali_pożizzjoni, int 너비, int 높이, int 색) {
        for (int 세로좌표 = Vertikali_pożizzjoni; 세로좌표 < Vertikali_pożizzjoni + 높이; 세로좌표++)
            for (int koordinat_x = 가로; koordinat_x < 가로 + 너비; koordinat_x++) bord.화면점(koordinat_x, 세로좌표, 색);
    }
    static void 화면() {
        if (bord.화면준비() == 0) { 단말.kiteb("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, bord.화면너비(), bord.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.kiteb("FRAMEBUFFER PASS "); 단말.수(bord.화면너비()); 단말.문자('x');
        단말.수(bord.화면높이()); 단말.kiteb(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int miżura = bord.씨플러스시험();
        vverifika(miżura == 0, 100 + miżura);
        단말.kiteb("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        vverifika(bord.ċekk_utent_programm() == 0, 200);
        단말.kiteb("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = bord.serje_utent_programm(0);
        if (처음결과 != 0) { 단말.kiteb("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        vverifika(처음결과 == 0, 201);
        단말.kiteb("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.kiteb("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int miżura = bord.serje_utent_programm(INDEX + 1);
            if (miżura != 예상[INDEX]) { 단말.kiteb("USER RESULT "); 단말.수(miżura); 단말.문자(10); }
            vverifika(miżura == 예상[INDEX], 210 + INDEX);
        }
        vverifika(bord.serje_utent_programm(0) == 0, 220);
        단말.kiteb("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int miżura = bord.serje_utent_programm(9);
        if (miżura != 0) { 단말.kiteb("UDP RESULT "); 단말.수(miżura); 단말.문자(10); }
        vverifika(miżura == 0, 230);
    }
    static void msinfo32_exe() {
        단말.kiteb("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.kiteb("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.kiteb("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.kiteb("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.kiteb("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void serje() {
        단말.kiteb("WorldOS mt · mt · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.kiteb("NATIVE READY\n");
        명령해석기.eżegwixxa_kmand();
    }
}
