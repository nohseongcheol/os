// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class intima {
    static int[] 작업횟수 = new int[3];
    static int[] 작업합 = new int[3];
    static int umukoro_umujyo;
    static int umukoro_ikosa;
    static int 난수씨 = 17;

    static void gusuzuma(boolean icyangombwa, int umugerekashakiro) {
        if (!icyangombwa) { 단말.kwandika("FAIL "); 단말.수(umugerekashakiro); 보드.Guhagarara(umugerekashakiro); }
    }
    static int ishami(int agaciro) {
        switch (agaciro) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int agaciro) {
        switch (agaciro) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] ARRAY_agaciro) { return ARRAY_agaciro; }
    static void 계산시험() {
        int agaciro = 난수씨;
        gusuzuma(agaciro * 7 - agaciro == 102 && agaciro / 3 == 5 && agaciro % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        gusuzuma(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        gusuzuma(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        gusuzuma((-agaciro >> 2) == -5 && (-agaciro >>> 2) == 1073741819 && (agaciro << 33) == 34, 4);
        gusuzuma((byte)(agaciro * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_agaciro = new int[5];
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < ARRAY_agaciro.length; gukora_mu_matsinda_umugerekashakiro++) ARRAY_agaciro[gukora_mu_matsinda_umugerekashakiro] = gukora_mu_matsinda_umugerekashakiro * agaciro;
        ARRAY_agaciro[2]++;
        gusuzuma(배열돌려주기(ARRAY_agaciro) == ARRAY_agaciro && ARRAY_agaciro[2] == 35 && ARRAY_agaciro[4] == 68, 6);
        gusuzuma(ishami(agaciro - 117) == 7 && ishami(agaciro - 15) == 9 && ishami(agaciro) == 3 && 촘촘분기(agaciro - 15) == 17, 7);
        String Umwandiko = "한글 😀";
        gusuzuma(Umwandiko.length() == 5 && Umwandiko.charAt(0) == '한' && Umwandiko.charAt(3) == 0xd83d, 8);
        gusuzuma(보드.시피유권한() == 1, 9);
        단말.kwandika("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int umugerekashakiro) {
        // gusubika_CPU 전후 mu_gace_urwego 변수가 보존되는지 검사: 각 작업은 독립된 imashini 스택을 쓴다.
        int mu_gace_agaciro = umugerekashakiro * 100;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 10; gukora_mu_matsinda_umugerekashakiro++) {
            if (umukoro_umujyo % 2 + 1 != umugerekashakiro) umukoro_ikosa++;
            umukoro_umujyo++;
            mu_gace_agaciro += gukora_mu_matsinda_umugerekashakiro + umugerekashakiro;
            작업합[umugerekashakiro] = mu_gace_agaciro;
            작업횟수[umugerekashakiro]++;
            보드.gusubika_CPU();
            if (mu_gace_agaciro != 작업합[umugerekashakiro]) umukoro_ikosa++;
        }
    }
    static void 작업시험() {
        umukoro_umujyo = 0; umukoro_ikosa = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        gusuzuma(보드.kurema_umukoro(1) == 0 && 보드.kurema_umukoro(2) == 0, 20);
        int 회전 = 0;
        while (보드.umukoro_imimerere(1) != 0 || 보드.umukoro_imimerere(2) != 0) {
            보드.gusubika_CPU();
            gusuzuma(++회전 < 100, 21);
        }
        gusuzuma(작업횟수[1] == 10 && 작업횟수[2] == 10 && umukoro_umujyo == 20 && umukoro_ikosa == 0, 22);
        gusuzuma(작업합[1] == 155 && 작업합[2] == 265, 23);
        단말.kwandika("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int 세로, int 너비, int 높이, int 색) {
        for (int 세로좌표 = 세로; 세로좌표 < 세로 + 높이; 세로좌표++)
            for (int Ihuza_rya_x = 가로; Ihuza_rya_x < 가로 + 너비; Ihuza_rya_x++) 보드.화면점(Ihuza_rya_x, 세로좌표, 색);
    }
    static void 화면() {
        if (보드.화면준비() == 0) { 단말.kwandika("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.kwandika("FRAMEBUFFER PASS "); 단말.수(보드.화면너비()); 단말.문자('x');
        단말.수(보드.화면높이()); 단말.kwandika(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int 결과 = 보드.씨플러스시험();
        gusuzuma(결과 == 0, 100 + 결과);
        단말.kwandika("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        gusuzuma(보드.sheki_ukoresha_porogaramu() == 0, 200);
        단말.kwandika("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = 보드.ihuriro_ukoresha_porogaramu(0);
        if (처음결과 != 0) { 단말.kwandika("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        gusuzuma(처음결과 == 0, 201);
        단말.kwandika("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int umugerekashakiro = 0; umugerekashakiro < 예상.length; umugerekashakiro++) {
            단말.kwandika("USER CHECK "); 단말.수(umugerekashakiro); 단말.문자(10);
            int 결과 = 보드.ihuriro_ukoresha_porogaramu(umugerekashakiro + 1);
            if (결과 != 예상[umugerekashakiro]) { 단말.kwandika("USER RESULT "); 단말.수(결과); 단말.문자(10); }
            gusuzuma(결과 == 예상[umugerekashakiro], 210 + umugerekashakiro);
        }
        gusuzuma(보드.ihuriro_ukoresha_porogaramu(0) == 0, 220);
        단말.kwandika("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int 결과 = 보드.ihuriro_ukoresha_porogaramu(9);
        if (결과 != 0) { 단말.kwandika("UDP RESULT "); 단말.수(결과); 단말.문자(10); }
        gusuzuma(결과 == 0, 230);
    }
    static void msinfo32_exe() {
        단말.kwandika("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.kwandika("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.kwandika("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.kwandika("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.kwandika("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void ihuriro() {
        단말.kwandika("WorldOS rw · Ikinyarwanda · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.kwandika("NATIVE READY\n");
        명령해석기.gukora_ibwiriza();
    }
}
