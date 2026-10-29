// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class nüvə {
    static int[] 작업횟수 = new int[3];
    static int[] tapşırıq_SUM = new int[3];
    static int tapşırıq_ardıcıllıq;
    static int tapşırıq_səhv;
    static int 난수씨 = 17;

    static void yoxlamaq(boolean şərt, int INDEX) {
        if (!şərt) { 단말.Yazma("FAIL "); 단말.수(INDEX); lövhə.Dayan(INDEX); }
    }
    static int qol(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] geri_qaytarmaq_ARRAY(int[] ARRAY_VALUE) { return ARRAY_VALUE; }
    static void 계산시험() {
        int VALUE = 난수씨;
        yoxlamaq(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        yoxlamaq(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        yoxlamaq(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        yoxlamaq((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        yoxlamaq((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_VALUE = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < ARRAY_VALUE.length; Loop_INDEX++) ARRAY_VALUE[Loop_INDEX] = Loop_INDEX * VALUE;
        ARRAY_VALUE[2]++;
        yoxlamaq(geri_qaytarmaq_ARRAY(ARRAY_VALUE) == ARRAY_VALUE && ARRAY_VALUE[2] == 35 && ARRAY_VALUE[4] == 68, 6);
        yoxlamaq(qol(VALUE - 117) == 7 && qol(VALUE - 15) == 9 && qol(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String Mətn = "한글 😀";
        yoxlamaq(Mətn.length() == 5 && Mətn.charAt(0) == '한' && Mətn.charAt(3) == 0xd83d, 8);
        yoxlamaq(lövhə.CPU_icazə_səviyyə() == 1, 9);
        단말.Yazma("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_CPU 전후 lokal_miqyas 변수가 보존되는지 검사: 각 작업은 독립된 maşın 스택을 쓴다.
        int lokal_VALUE = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (tapşırıq_ardıcıllıq % 2 + 1 != INDEX) tapşırıq_səhv++;
            tapşırıq_ardıcıllıq++;
            lokal_VALUE += Loop_INDEX + INDEX;
            tapşırıq_SUM[INDEX] = lokal_VALUE;
            작업횟수[INDEX]++;
            lövhə.YIELD_CPU();
            if (lokal_VALUE != tapşırıq_SUM[INDEX]) tapşırıq_səhv++;
        }
    }
    static void 작업시험() {
        tapşırıq_ardıcıllıq = 0; tapşırıq_səhv = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        yoxlamaq(lövhə.yarat_tapşırıq(1) == 0 && lövhə.yarat_tapşırıq(2) == 0, 20);
        int fırlatma_COUNT = 0;
        while (lövhə.tapşırıq_vəziyyət(1) != 0 || lövhə.tapşırıq_vəziyyət(2) != 0) {
            lövhə.YIELD_CPU();
            yoxlamaq(++fırlatma_COUNT < 100, 21);
        }
        yoxlamaq(작업횟수[1] == 10 && 작업횟수[2] == 10 && tapşırıq_ardıcıllıq == 20 && tapşırıq_səhv == 0, 22);
        yoxlamaq(tapşırıq_SUM[1] == 155 && tapşırıq_SUM[2] == 265, 23);
        단말.Yazma("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int Şaquli_yerinə_qoymaq, int 너비, int 높이, int 색) {
        for (int Y_koordinat = Şaquli_yerinə_qoymaq; Y_koordinat < Şaquli_yerinə_qoymaq + 높이; Y_koordinat++)
            for (int x_koordinatı = 가로; x_koordinatı < 가로 + 너비; x_koordinatı++) lövhə.화면점(x_koordinatı, Y_koordinat, 색);
    }
    static void 화면() {
        if (lövhə.화면준비() == 0) { 단말.Yazma("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, lövhə.화면너비(), lövhə.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.Yazma("FRAMEBUFFER PASS "); 단말.수(lövhə.화면너비()); 단말.문자('x');
        단말.수(lövhə.화면높이()); 단말.Yazma(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int ölçü = lövhə.씨플러스시험();
        yoxlamaq(ölçü == 0, 100 + ölçü);
        단말.Yazma("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        yoxlamaq(lövhə.çek_istifadəçi_proqram() == 0, 200);
        단말.Yazma("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = lövhə.icra_istifadəçi_proqram(0);
        if (처음결과 != 0) { 단말.Yazma("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        yoxlamaq(처음결과 == 0, 201);
        단말.Yazma("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Yazma("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int ölçü = lövhə.icra_istifadəçi_proqram(INDEX + 1);
            if (ölçü != 예상[INDEX]) { 단말.Yazma("USER RESULT "); 단말.수(ölçü); 단말.문자(10); }
            yoxlamaq(ölçü == 예상[INDEX], 210 + INDEX);
        }
        yoxlamaq(lövhə.icra_istifadəçi_proqram(0) == 0, 220);
        단말.Yazma("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int ölçü = lövhə.icra_istifadəçi_proqram(9);
        if (ölçü != 0) { 단말.Yazma("UDP RESULT "); 단말.수(ölçü); 단말.문자(10); }
        yoxlamaq(ölçü == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Yazma("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Yazma("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Yazma("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Yazma("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Yazma("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void İcra_Et() {
        단말.Yazma("WorldOS az · az · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Yazma("NATIVE READY\n");
        명령해석기.icra_etmək_əmr();
    }
}
