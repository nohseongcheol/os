// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class bërthamë {
    static int[] 작업횟수 = new int[3];
    static int[] detyrë_SUM = new int[3];
    static int detyrë_renditja;
    static int detyrë_gabim;
    static int 난수씨 = 17;

    static void verifikoj(boolean kusht, int INDEX) {
        if (!kusht) { 단말.Shkrimi("FAIL "); 단말.수(INDEX); panel.Ndalo(INDEX); }
    }
    static int degë(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] Kthe_ARRAY(int[] ARRAY_VALUE) { return ARRAY_VALUE; }
    static void 계산시험() {
        int VALUE = 난수씨;
        verifikoj(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        verifikoj(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        verifikoj(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        verifikoj((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        verifikoj((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_VALUE = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < ARRAY_VALUE.length; Loop_INDEX++) ARRAY_VALUE[Loop_INDEX] = Loop_INDEX * VALUE;
        ARRAY_VALUE[2]++;
        verifikoj(Kthe_ARRAY(ARRAY_VALUE) == ARRAY_VALUE && ARRAY_VALUE[2] == 35 && ARRAY_VALUE[4] == 68, 6);
        verifikoj(degë(VALUE - 117) == 7 && degë(VALUE - 15) == 9 && degë(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String Teksti = "한글 😀";
        verifikoj(Teksti.length() == 5 && Teksti.charAt(0) == '한' && Teksti.charAt(3) == 0xd83d, 8);
        verifikoj(panel.CPU_leje_nivel() == 1, 9);
        단말.Shkrimi("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_CPU 전후 lokal_fushë 변수가 보존되는지 검사: 각 작업은 독립된 makinë 스택을 쓴다.
        int lokal_VALUE = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (detyrë_renditja % 2 + 1 != INDEX) detyrë_gabim++;
            detyrë_renditja++;
            lokal_VALUE += Loop_INDEX + INDEX;
            detyrë_SUM[INDEX] = lokal_VALUE;
            작업횟수[INDEX]++;
            panel.YIELD_CPU();
            if (lokal_VALUE != detyrë_SUM[INDEX]) detyrë_gabim++;
        }
    }
    static void 작업시험() {
        detyrë_renditja = 0; detyrë_gabim = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        verifikoj(panel.Krijo_detyrë(1) == 0 && panel.Krijo_detyrë(2) == 0, 20);
        int rrotullim_COUNT = 0;
        while (panel.detyrë_status(1) != 0 || panel.detyrë_status(2) != 0) {
            panel.YIELD_CPU();
            verifikoj(++rrotullim_COUNT < 100, 21);
        }
        verifikoj(작업횟수[1] == 10 && 작업횟수[2] == 10 && detyrë_renditja == 20 && detyrë_gabim == 0, 22);
        verifikoj(detyrë_SUM[1] == 155 && detyrë_SUM[2] == 265, 23);
        단말.Shkrimi("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int Vertikal_pozicioni, int 너비, int 높이, int 색) {
        for (int Y_koordinatë = Vertikal_pozicioni; Y_koordinatë < Vertikal_pozicioni + 높이; Y_koordinatë++)
            for (int koordinata_x = 가로; koordinata_x < 가로 + 너비; koordinata_x++) panel.화면점(koordinata_x, Y_koordinatë, 색);
    }
    static void 화면() {
        if (panel.화면준비() == 0) { 단말.Shkrimi("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, panel.화면너비(), panel.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.Shkrimi("FRAMEBUFFER PASS "); 단말.수(panel.화면너비()); 단말.문자('x');
        단말.수(panel.화면높이()); 단말.Shkrimi(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int llogaritje = panel.씨플러스시험();
        verifikoj(llogaritje == 0, 100 + llogaritje);
        단말.Shkrimi("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        verifikoj(panel.çek_përdorues_program() == 0, 200);
        단말.Shkrimi("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = panel.varg_përdorues_program(0);
        if (처음결과 != 0) { 단말.Shkrimi("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        verifikoj(처음결과 == 0, 201);
        단말.Shkrimi("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Shkrimi("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int llogaritje = panel.varg_përdorues_program(INDEX + 1);
            if (llogaritje != 예상[INDEX]) { 단말.Shkrimi("USER RESULT "); 단말.수(llogaritje); 단말.문자(10); }
            verifikoj(llogaritje == 예상[INDEX], 210 + INDEX);
        }
        verifikoj(panel.varg_përdorues_program(0) == 0, 220);
        단말.Shkrimi("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int llogaritje = panel.varg_përdorues_program(9);
        if (llogaritje != 0) { 단말.Shkrimi("UDP RESULT "); 단말.수(llogaritje); 단말.문자(10); }
        verifikoj(llogaritje == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Shkrimi("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Shkrimi("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Shkrimi("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Shkrimi("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Shkrimi("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Ekzekuto() {
        단말.Shkrimi("WorldOS sq · sq · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Shkrimi("NATIVE READY\n");
        명령해석기.zbatoj_komandë();
    }
}
