// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class ikheneli {
    static int[] 작업횟수 = new int[3];
    static int[] 작업합 = new int[3];
    static int umsebenzi_ulandelelwano;
    static int umsebenzi_impazamo;
    static int 난수씨 = 17;

    static void ngqinisisa(boolean imo, int indeksa) {
        if (!imo) { 단말.Bhala("FAIL "); 단말.수(indeksa); 보드.Yima(indeksa); }
    }
    static int isebe(int ixabiso) {
        switch (ixabiso) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int ixabiso) {
        switch (ixabiso) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] ULUHLU_ixabiso) { return ULUHLU_ixabiso; }
    static void 계산시험() {
        int ixabiso = 난수씨;
        ngqinisisa(ixabiso * 7 - ixabiso == 102 && ixabiso / 3 == 5 && ixabiso % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        ngqinisisa(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        ngqinisisa(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        ngqinisisa((-ixabiso >> 2) == -5 && (-ixabiso >>> 2) == 1073741819 && (ixabiso << 33) == 34, 4);
        ngqinisisa((byte)(ixabiso * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ULUHLU_ixabiso = new int[5];
        for (int iluphu_indeksa = 0; iluphu_indeksa < ULUHLU_ixabiso.length; iluphu_indeksa++) ULUHLU_ixabiso[iluphu_indeksa] = iluphu_indeksa * ixabiso;
        ULUHLU_ixabiso[2]++;
        ngqinisisa(배열돌려주기(ULUHLU_ixabiso) == ULUHLU_ixabiso && ULUHLU_ixabiso[2] == 35 && ULUHLU_ixabiso[4] == 68, 6);
        ngqinisisa(isebe(ixabiso - 117) == 7 && isebe(ixabiso - 15) == 9 && isebe(ixabiso) == 3 && 촘촘분기(ixabiso - 15) == 17, 7);
        String Umbhalo = "한글 😀";
        ngqinisisa(Umbhalo.length() == 5 && Umbhalo.charAt(0) == '한' && Umbhalo.charAt(3) == 0xd83d, 8);
        ngqinisisa(보드.i_CPU_imvume_inqanaba() == 1, 9);
        단말.Bhala("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int indeksa) {
        // misa_okwexeshana_i_CPU 전후 eyale_ndawo_umda 변수가 보존되는지 검사: 각 작업은 독립된 umatshini 스택을 쓴다.
        int eyale_ndawo_ixabiso = indeksa * 100;
        for (int iluphu_indeksa = 0; iluphu_indeksa < 10; iluphu_indeksa++) {
            if (umsebenzi_ulandelelwano % 2 + 1 != indeksa) umsebenzi_impazamo++;
            umsebenzi_ulandelelwano++;
            eyale_ndawo_ixabiso += iluphu_indeksa + indeksa;
            작업합[indeksa] = eyale_ndawo_ixabiso;
            작업횟수[indeksa]++;
            보드.misa_okwexeshana_i_CPU();
            if (eyale_ndawo_ixabiso != 작업합[indeksa]) umsebenzi_impazamo++;
        }
    }
    static void 작업시험() {
        umsebenzi_ulandelelwano = 0; umsebenzi_impazamo = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        ngqinisisa(보드.yila_umsebenzi(1) == 0 && 보드.yila_umsebenzi(2) == 0, 20);
        int 회전 = 0;
        while (보드.umsebenzi_imo(1) != 0 || 보드.umsebenzi_imo(2) != 0) {
            보드.misa_okwexeshana_i_CPU();
            ngqinisisa(++회전 < 100, 21);
        }
        ngqinisisa(작업횟수[1] == 10 && 작업횟수[2] == 10 && umsebenzi_ulandelelwano == 20 && umsebenzi_impazamo == 0, 22);
        ngqinisisa(작업합[1] == 155 && 작업합[2] == 265, 23);
        단말.Bhala("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int 세로, int 너비, int 높이, int 색) {
        for (int 세로좌표 = 세로; 세로좌표 < 세로 + 높이; 세로좌표++)
            for (int isilungelelanisi_x = 가로; isilungelelanisi_x < 가로 + 너비; isilungelelanisi_x++) 보드.화면점(isilungelelanisi_x, 세로좌표, 색);
    }
    static void 화면() {
        if (보드.화면준비() == 0) { 단말.Bhala("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.Bhala("FRAMEBUFFER PASS "); 단말.수(보드.화면너비()); 단말.문자('x');
        단말.수(보드.화면높이()); 단말.Bhala(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int 결과 = 보드.씨플러스시험();
        ngqinisisa(결과 == 0, 100 + 결과);
        단말.Bhala("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        ngqinisisa(보드.jonga_umsebenzisi_inkqubo() == 0, 200);
        단말.Bhala("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = 보드.i_run_umsebenzisi_inkqubo(0);
        if (처음결과 != 0) { 단말.Bhala("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        ngqinisisa(처음결과 == 0, 201);
        단말.Bhala("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int indeksa = 0; indeksa < 예상.length; indeksa++) {
            단말.Bhala("USER CHECK "); 단말.수(indeksa); 단말.문자(10);
            int 결과 = 보드.i_run_umsebenzisi_inkqubo(indeksa + 1);
            if (결과 != 예상[indeksa]) { 단말.Bhala("USER RESULT "); 단말.수(결과); 단말.문자(10); }
            ngqinisisa(결과 == 예상[indeksa], 210 + indeksa);
        }
        ngqinisisa(보드.i_run_umsebenzisi_inkqubo(0) == 0, 220);
        단말.Bhala("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int 결과 = 보드.i_run_umsebenzisi_inkqubo(9);
        if (결과 != 0) { 단말.Bhala("UDP RESULT "); 단말.수(결과); 단말.문자(10); }
        ngqinisisa(결과 == 0, 230);
    }
    static void i_msinfo32_exe() {
        단말.Bhala("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Bhala("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Bhala("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Bhala("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Bhala("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Phumeza() {
        단말.Bhala("WorldOS xh · xh · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Bhala("NATIVE READY\n");
        명령해석기.ukwenza_umyalelo();
    }
}
