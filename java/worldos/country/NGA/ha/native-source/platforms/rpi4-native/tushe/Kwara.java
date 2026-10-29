// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class Kwara {
    static int[] 작업횟수 = new int[3];
    static int[] 작업합 = new int[3];
    static int aiki_Hanyar_jejjerawa;
    static int aiki_Kuskure;
    static int 난수씨 = 17;

    static void Tabbatar_da(boolean Yanayi, int Indes) {
        if (!Yanayi) { 단말.Yi_Rubutu("FAIL "); 단말.수(Indes); 보드.Tsai_da(Indes); }
    }
    static int Reshe(int Daraja) {
        switch (Daraja) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int Daraja) {
        switch (Daraja) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] TSARI_Daraja) { return TSARI_Daraja; }
    static void 계산시험() {
        int Daraja = 난수씨;
        Tabbatar_da(Daraja * 7 - Daraja == 102 && Daraja / 3 == 5 && Daraja % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        Tabbatar_da(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        Tabbatar_da(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        Tabbatar_da((-Daraja >> 2) == -5 && (-Daraja >>> 2) == 1073741819 && (Daraja << 33) == 34, 4);
        Tabbatar_da((byte)(Daraja * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] TSARI_Daraja = new int[5];
        for (int Warware_Indes = 0; Warware_Indes < TSARI_Daraja.length; Warware_Indes++) TSARI_Daraja[Warware_Indes] = Warware_Indes * Daraja;
        TSARI_Daraja[2]++;
        Tabbatar_da(배열돌려주기(TSARI_Daraja) == TSARI_Daraja && TSARI_Daraja[2] == 35 && TSARI_Daraja[4] == 68, 6);
        Tabbatar_da(Reshe(Daraja - 117) == 7 && Reshe(Daraja - 15) == 9 && Reshe(Daraja) == 3 && 촘촘분기(Daraja - 15) == 17, 7);
        String SMS = "한글 😀";
        Tabbatar_da(SMS.length() == 5 && SMS.charAt(0) == '한' && SMS.charAt(3) == 0xd83d, 8);
        Tabbatar_da(보드.CPU_izini_mataki() == 1, 9);
        단말.Yi_Rubutu("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int Indes) {
        // ɗan_tsai_da_CPU 전후 na_gida_Kima 변수가 보존되는지 검사: 각 작업은 독립된 na_ura_mai_kwakwalwa 스택을 쓴다.
        int na_gida_Daraja = Indes * 100;
        for (int Warware_Indes = 0; Warware_Indes < 10; Warware_Indes++) {
            if (aiki_Hanyar_jejjerawa % 2 + 1 != Indes) aiki_Kuskure++;
            aiki_Hanyar_jejjerawa++;
            na_gida_Daraja += Warware_Indes + Indes;
            작업합[Indes] = na_gida_Daraja;
            작업횟수[Indes]++;
            보드.ɗan_tsai_da_CPU();
            if (na_gida_Daraja != 작업합[Indes]) aiki_Kuskure++;
        }
    }
    static void 작업시험() {
        aiki_Hanyar_jejjerawa = 0; aiki_Kuskure = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        Tabbatar_da(보드.ƙirƙíra_aiki(1) == 0 && 보드.ƙirƙíra_aiki(2) == 0, 20);
        int 회전 = 0;
        while (보드.aiki_Matsayi(1) != 0 || 보드.aiki_Matsayi(2) != 0) {
            보드.ɗan_tsai_da_CPU();
            Tabbatar_da(++회전 < 100, 21);
        }
        Tabbatar_da(작업횟수[1] == 10 && 작업횟수[2] == 10 && aiki_Hanyar_jejjerawa == 20 && aiki_Kuskure == 0, 22);
        Tabbatar_da(작업합[1] == 155 && 작업합[2] == 265, 23);
        단말.Yi_Rubutu("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int 세로, int 너비, int 높이, int 색) {
        for (int Maɓallin_Y_Mai_tsarawa = 세로; Maɓallin_Y_Mai_tsarawa < 세로 + 높이; Maɓallin_Y_Mai_tsarawa++)
            for (int gamayyar_x = 가로; gamayyar_x < 가로 + 너비; gamayyar_x++) 보드.화면점(gamayyar_x, Maɓallin_Y_Mai_tsarawa, 색);
    }
    static void 화면() {
        if (보드.화면준비() == 0) { 단말.Yi_Rubutu("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.Yi_Rubutu("FRAMEBUFFER PASS "); 단말.수(보드.화면너비()); 단말.문자('x');
        단말.수(보드.화면높이()); 단말.Yi_Rubutu(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int 결과 = 보드.씨플러스시험();
        Tabbatar_da(결과 == 0, 100 + 결과);
        단말.Yi_Rubutu("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        Tabbatar_da(보드.Bincika_Mai_anfani_da_kwamfuta_Shiri() == 0, 200);
        단말.Yi_Rubutu("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = 보드.Gudanar_da_Mai_anfani_da_kwamfuta_Shiri(0);
        if (처음결과 != 0) { 단말.Yi_Rubutu("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        Tabbatar_da(처음결과 == 0, 201);
        단말.Yi_Rubutu("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int Indes = 0; Indes < 예상.length; Indes++) {
            단말.Yi_Rubutu("USER CHECK "); 단말.수(Indes); 단말.문자(10);
            int 결과 = 보드.Gudanar_da_Mai_anfani_da_kwamfuta_Shiri(Indes + 1);
            if (결과 != 예상[Indes]) { 단말.Yi_Rubutu("USER RESULT "); 단말.수(결과); 단말.문자(10); }
            Tabbatar_da(결과 == 예상[Indes], 210 + Indes);
        }
        Tabbatar_da(보드.Gudanar_da_Mai_anfani_da_kwamfuta_Shiri(0) == 0, 220);
        단말.Yi_Rubutu("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int 결과 = 보드.Gudanar_da_Mai_anfani_da_kwamfuta_Shiri(9);
        if (결과 != 0) { 단말.Yi_Rubutu("UDP RESULT "); 단말.수(결과); 단말.문자(10); }
        Tabbatar_da(결과 == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Yi_Rubutu("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Yi_Rubutu("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Yi_Rubutu("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Yi_Rubutu("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Yi_Rubutu("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Tafiyar_da() {
        단말.Yi_Rubutu("WorldOS ha · ha · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Yi_Rubutu("NATIVE READY\n");
        명령해석기.gudanar_Umarni();
    }
}
