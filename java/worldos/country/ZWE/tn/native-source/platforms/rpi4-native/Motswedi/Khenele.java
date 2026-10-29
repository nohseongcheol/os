// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class Khenele {
    static int[] 작업횟수 = new int[3];
    static int[] 작업합 = new int[3];
    static int Tiro_thulaganyo;
    static int Tiro_phoso;
    static int 난수씨 = 17;

    static void netefatsa(boolean boemo, int tshupane) {
        if (!boemo) { 단말.kwala("FAIL "); 단말.수(tshupane); 보드.emisa(tshupane); }
    }
    static int lekala(int Boleng) {
        switch (Boleng) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int Boleng) {
        switch (Boleng) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] setlhopha_Boleng_ed437109) { return setlhopha_Boleng_ed437109; }
    static void 계산시험() {
        int Boleng = 난수씨;
        netefatsa(Boleng * 7 - Boleng == 102 && Boleng / 3 == 5 && Boleng % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        netefatsa(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        netefatsa(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        netefatsa((-Boleng >> 2) == -5 && (-Boleng >>> 2) == 1073741819 && (Boleng << 33) == 34, 4);
        netefatsa((byte)(Boleng * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] setlhopha_Boleng_ed437109 = new int[5];
        for (int lupu_tshupane = 0; lupu_tshupane < setlhopha_Boleng_ed437109.length; lupu_tshupane++) setlhopha_Boleng_ed437109[lupu_tshupane] = lupu_tshupane * Boleng;
        setlhopha_Boleng_ed437109[2]++;
        netefatsa(배열돌려주기(setlhopha_Boleng_ed437109) == setlhopha_Boleng_ed437109 && setlhopha_Boleng_ed437109[2] == 35 && setlhopha_Boleng_ed437109[4] == 68, 6);
        netefatsa(lekala(Boleng - 117) == 7 && lekala(Boleng - 15) == 9 && lekala(Boleng) == 3 && 촘촘분기(Boleng - 15) == 17, 7);
        String SMS = "한글 😀";
        netefatsa(SMS.length() == 5 && SMS.charAt(0) == '한' && SMS.charAt(3) == 0xd83d, 8);
        netefatsa(보드.CPU_tetla_Maemo() == 1, 9);
        단말.kwala("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int tshupane) {
        // emisa_ka_nakwana_CPU 전후 e_e_gaufi_Mothamo 변수가 보존되는지 검사: 각 작업은 독립된 motšhine 스택을 쓴다.
        int e_e_gaufi_Boleng = tshupane * 100;
        for (int lupu_tshupane = 0; lupu_tshupane < 10; lupu_tshupane++) {
            if (Tiro_thulaganyo % 2 + 1 != tshupane) Tiro_phoso++;
            Tiro_thulaganyo++;
            e_e_gaufi_Boleng += lupu_tshupane + tshupane;
            작업합[tshupane] = e_e_gaufi_Boleng;
            작업횟수[tshupane]++;
            보드.emisa_ka_nakwana_CPU();
            if (e_e_gaufi_Boleng != 작업합[tshupane]) Tiro_phoso++;
        }
    }
    static void 작업시험() {
        Tiro_thulaganyo = 0; Tiro_phoso = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        netefatsa(보드.tlhama_Tiro(1) == 0 && 보드.tlhama_Tiro(2) == 0, 20);
        int 회전 = 0;
        while (보드.Tiro_kemo(1) != 0 || 보드.Tiro_kemo(2) != 0) {
            보드.emisa_ka_nakwana_CPU();
            netefatsa(++회전 < 100, 21);
        }
        netefatsa(작업횟수[1] == 10 && 작업횟수[2] == 10 && Tiro_thulaganyo == 20 && Tiro_phoso == 0, 22);
        netefatsa(작업합[1] == 155 && 작업합[2] == 265, 23);
        단말.kwala("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int 세로, int 너비, int 높이, int 색) {
        for (int 세로좌표 = 세로; 세로좌표 < 세로 + 높이; 세로좌표++)
            for (int kgokagano_ya_x = 가로; kgokagano_ya_x < 가로 + 너비; kgokagano_ya_x++) 보드.화면점(kgokagano_ya_x, 세로좌표, 색);
    }
    static void 화면() {
        if (보드.화면준비() == 0) { 단말.kwala("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.kwala("FRAMEBUFFER PASS "); 단말.수(보드.화면너비()); 단말.문자('x');
        단말.수(보드.화면높이()); 단말.kwala(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int 결과 = 보드.씨플러스시험();
        netefatsa(결과 == 0, 100 + 결과);
        단말.kwala("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        netefatsa(보드.tlhola_modirisi_Tiriso() == 0, 200);
        단말.kwala("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = 보드.dirisa_modirisi_Tiriso(0);
        if (처음결과 != 0) { 단말.kwala("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        netefatsa(처음결과 == 0, 201);
        단말.kwala("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int tshupane = 0; tshupane < 예상.length; tshupane++) {
            단말.kwala("USER CHECK "); 단말.수(tshupane); 단말.문자(10);
            int 결과 = 보드.dirisa_modirisi_Tiriso(tshupane + 1);
            if (결과 != 예상[tshupane]) { 단말.kwala("USER RESULT "); 단말.수(결과); 단말.문자(10); }
            netefatsa(결과 == 예상[tshupane], 210 + tshupane);
        }
        netefatsa(보드.dirisa_modirisi_Tiriso(0) == 0, 220);
        단말.kwala("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int 결과 = 보드.dirisa_modirisi_Tiriso(9);
        if (결과 != 0) { 단말.kwala("UDP RESULT "); 단말.수(결과); 단말.문자(10); }
        netefatsa(결과 == 0, 230);
    }
    static void msinfo32_exe() {
        단말.kwala("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.kwala("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.kwala("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.kwala("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.kwala("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void dirisa() {
        단말.kwala("WorldOS tn · tn · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.kwala("NATIVE READY\n");
        명령해석기.diragatsa_Taelo();
    }
}
