// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class Kernel {
    static int[] 작업횟수 = new int[3];
    static int[] To_do_SUM = new int[3];
    static int To_do_Reiefolleg;
    static int To_do_Feeler;
    static int 난수씨 = 17;

    static void verifizéieren(boolean Bedéngung, int INDEX) {
        if (!Bedéngung) { 단말.schreiwen("FAIL "); 단말.수(INDEX); Board.Stoppen(INDEX); }
    }
    static int Branche(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] ARRAY_VALUE) { return ARRAY_VALUE; }
    static void 계산시험() {
        int VALUE = 난수씨;
        verifizéieren(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        verifizéieren(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        verifizéieren(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        verifizéieren((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        verifizéieren((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_VALUE = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < ARRAY_VALUE.length; Loop_INDEX++) ARRAY_VALUE[Loop_INDEX] = Loop_INDEX * VALUE;
        ARRAY_VALUE[2]++;
        verifizéieren(배열돌려주기(ARRAY_VALUE) == ARRAY_VALUE && ARRAY_VALUE[2] == 35 && ARRAY_VALUE[4] == 68, 6);
        verifizéieren(Branche(VALUE - 117) == 7 && Branche(VALUE - 15) == 9 && Branche(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String SMS = "한글 😀";
        verifizéieren(SMS.length() == 5 && SMS.charAt(0) == '한' && SMS.charAt(3) == 0xd83d, 8);
        verifizéieren(Board.CPU_Geneemegung_Niveau() == 1, 9);
        단말.schreiwen("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_CPU 전후 lokal_Beräich 변수가 보존되는지 검사: 각 작업은 독립된 Computer 스택을 쓴다.
        int lokal_VALUE = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (To_do_Reiefolleg % 2 + 1 != INDEX) To_do_Feeler++;
            To_do_Reiefolleg++;
            lokal_VALUE += Loop_INDEX + INDEX;
            To_do_SUM[INDEX] = lokal_VALUE;
            작업횟수[INDEX]++;
            Board.YIELD_CPU();
            if (lokal_VALUE != To_do_SUM[INDEX]) To_do_Feeler++;
        }
    }
    static void 작업시험() {
        To_do_Reiefolleg = 0; To_do_Feeler = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        verifizéieren(Board.Create_To_do(1) == 0 && Board.Create_To_do(2) == 0, 20);
        int Rotatioun_COUNT = 0;
        while (Board.To_do_Status(1) != 0 || Board.To_do_Status(2) != 0) {
            Board.YIELD_CPU();
            verifizéieren(++Rotatioun_COUNT < 100, 21);
        }
        verifizéieren(작업횟수[1] == 10 && 작업횟수[2] == 10 && To_do_Reiefolleg == 20 && To_do_Feeler == 0, 22);
        verifizéieren(To_do_SUM[1] == 155 && To_do_SUM[2] == 265, 23);
        단말.schreiwen("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int Vertikal_positionéieren, int 너비, int 높이, int 색) {
        for (int 세로좌표 = Vertikal_positionéieren; 세로좌표 < Vertikal_positionéieren + 높이; 세로좌표++)
            for (int X_Koordinat = 가로; X_Koordinat < 가로 + 너비; X_Koordinat++) Board.화면점(X_Koordinat, 세로좌표, 색);
    }
    static void 화면() {
        if (Board.화면준비() == 0) { 단말.schreiwen("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, Board.화면너비(), Board.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.schreiwen("FRAMEBUFFER PASS "); 단말.수(Board.화면너비()); 단말.문자('x');
        단말.수(Board.화면높이()); 단말.schreiwen(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int Mooss = Board.씨플러스시험();
        verifizéieren(Mooss == 0, 100 + Mooss);
        단말.schreiwen("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        verifizéieren(Board.Scheck_Benotzer_App() == 0, 200);
        단말.schreiwen("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = Board.Laf_Benotzer_App(0);
        if (처음결과 != 0) { 단말.schreiwen("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        verifizéieren(처음결과 == 0, 201);
        단말.schreiwen("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.schreiwen("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int Mooss = Board.Laf_Benotzer_App(INDEX + 1);
            if (Mooss != 예상[INDEX]) { 단말.schreiwen("USER RESULT "); 단말.수(Mooss); 단말.문자(10); }
            verifizéieren(Mooss == 예상[INDEX], 210 + INDEX);
        }
        verifizéieren(Board.Laf_Benotzer_App(0) == 0, 220);
        단말.schreiwen("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int Mooss = Board.Laf_Benotzer_App(9);
        if (Mooss != 0) { 단말.schreiwen("UDP RESULT "); 단말.수(Mooss); 단말.문자(10); }
        verifizéieren(Mooss == 0, 230);
    }
    static void msinfo32_exe() {
        단말.schreiwen("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.schreiwen("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.schreiwen("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.schreiwen("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.schreiwen("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Laf() {
        단말.schreiwen("WorldOS lb · lb · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.schreiwen("NATIVE READY\n");
        명령해석기.ausféieren_Befeel();
    }
}
