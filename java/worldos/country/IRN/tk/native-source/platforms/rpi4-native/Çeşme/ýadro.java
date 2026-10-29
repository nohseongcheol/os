// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class ýadro {
    static int[] 작업횟수 = new int[3];
    static int[] 작업합 = new int[3];
    static int tabşyryk_tertip;
    static int tabşyryk_säwlik;
    static int 난수씨 = 17;

    static void barla(boolean şert, int indeks) {
        if (!şert) { 단말.Ýaz("FAIL "); 단말.수(indeks); 보드.Dur(indeks); }
    }
    static int şahalanma(int baha) {
        switch (baha) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int baha) {
        switch (baha) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] ARRAY_baha) { return ARRAY_baha; }
    static void 계산시험() {
        int baha = 난수씨;
        barla(baha * 7 - baha == 102 && baha / 3 == 5 && baha % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        barla(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        barla(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        barla((-baha >> 2) == -5 && (-baha >>> 2) == 1073741819 && (baha << 33) == 34, 4);
        barla((byte)(baha * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_baha = new int[5];
        for (int sikl_indeks = 0; sikl_indeks < ARRAY_baha.length; sikl_indeks++) ARRAY_baha[sikl_indeks] = sikl_indeks * baha;
        ARRAY_baha[2]++;
        barla(배열돌려주기(ARRAY_baha) == ARRAY_baha && ARRAY_baha[2] == 35 && ARRAY_baha[4] == 68, 6);
        barla(şahalanma(baha - 117) == 7 && şahalanma(baha - 15) == 9 && şahalanma(baha) == 3 && 촘촘분기(baha - 15) == 17, 7);
        String Metin = "한글 😀";
        barla(Metin.length() == 5 && Metin.charAt(0) == '한' && Metin.charAt(3) == 0xd83d, 8);
        barla(보드.CPU_rugsat_dereje() == 1, 9);
        단말.Ýaz("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int indeks) {
        // togtatmak_CPU 전후 ýerli_elýeterli_gor 변수가 보존되는지 검사: 각 작업은 독립된 kompýuter 스택을 쓴다.
        int ýerli_baha = indeks * 100;
        for (int sikl_indeks = 0; sikl_indeks < 10; sikl_indeks++) {
            if (tabşyryk_tertip % 2 + 1 != indeks) tabşyryk_säwlik++;
            tabşyryk_tertip++;
            ýerli_baha += sikl_indeks + indeks;
            작업합[indeks] = ýerli_baha;
            작업횟수[indeks]++;
            보드.togtatmak_CPU();
            if (ýerli_baha != 작업합[indeks]) tabşyryk_säwlik++;
        }
    }
    static void 작업시험() {
        tabşyryk_tertip = 0; tabşyryk_säwlik = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        barla(보드.döretmek_tabşyryk(1) == 0 && 보드.döretmek_tabşyryk(2) == 0, 20);
        int 회전 = 0;
        while (보드.tabşyryk_ýagdaý(1) != 0 || 보드.tabşyryk_ýagdaý(2) != 0) {
            보드.togtatmak_CPU();
            barla(++회전 < 100, 21);
        }
        barla(작업횟수[1] == 10 && 작업횟수[2] == 10 && tabşyryk_tertip == 20 && tabşyryk_säwlik == 0, 22);
        barla(작업합[1] == 155 && 작업합[2] == 265, 23);
        단말.Ýaz("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int 세로, int 너비, int 높이, int 색) {
        for (int 세로좌표 = 세로; 세로좌표 < 세로 + 높이; 세로좌표++)
            for (int x_koordinatasy = 가로; x_koordinatasy < 가로 + 너비; x_koordinatasy++) 보드.화면점(x_koordinatasy, 세로좌표, 색);
    }
    static void 화면() {
        if (보드.화면준비() == 0) { 단말.Ýaz("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.Ýaz("FRAMEBUFFER PASS "); 단말.수(보드.화면너비()); 단말.문자('x');
        단말.수(보드.화면높이()); 단말.Ýaz(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int 결과 = 보드.씨플러스시험();
        barla(결과 == 0, 100 + 결과);
        단말.Ýaz("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        barla(보드.derňe_ulanyjy_programma() == 0, 200);
        단말.Ýaz("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = 보드.işe_goýber_ulanyjy_programma(0);
        if (처음결과 != 0) { 단말.Ýaz("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        barla(처음결과 == 0, 201);
        단말.Ýaz("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int indeks = 0; indeks < 예상.length; indeks++) {
            단말.Ýaz("USER CHECK "); 단말.수(indeks); 단말.문자(10);
            int 결과 = 보드.işe_goýber_ulanyjy_programma(indeks + 1);
            if (결과 != 예상[indeks]) { 단말.Ýaz("USER RESULT "); 단말.수(결과); 단말.문자(10); }
            barla(결과 == 예상[indeks], 210 + indeks);
        }
        barla(보드.işe_goýber_ulanyjy_programma(0) == 0, 220);
        단말.Ýaz("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int 결과 = 보드.işe_goýber_ulanyjy_programma(9);
        if (결과 != 0) { 단말.Ýaz("UDP RESULT "); 단말.수(결과); 단말.문자(10); }
        barla(결과 == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Ýaz("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Ýaz("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Ýaz("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Ýaz("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Ýaz("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Bitir() {
        단말.Ýaz("WorldOS tk · tk · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Ýaz("NATIVE READY\n");
        명령해석기.ýerine_ýetir_buýruk();
    }
}
