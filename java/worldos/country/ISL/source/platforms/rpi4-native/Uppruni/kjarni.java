// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** eigin Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class kjarni {
    static int[] 작업횟수 = new int[3];
    static int[] verk_SUM = new int[3];
    static int verk_röð;
    static int verk_villa;
    static int 난수씨 = 17;

    static void sannprófa(boolean skilyrði, int INDEX) {
        if (!skilyrði) { 단말.Skrift("FAIL "); 단말.númer(INDEX); bretti.Stopp(INDEX); }
    }
    static int grein(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] skila_ARRAY(int[] ARRAY_VALUE) { return ARRAY_VALUE; }
    static void 계산시험() {
        int VALUE = 난수씨;
        sannprófa(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        sannprófa(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        sannprófa(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        sannprófa((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        sannprófa((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_VALUE = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < ARRAY_VALUE.length; Loop_INDEX++) ARRAY_VALUE[Loop_INDEX] = Loop_INDEX * VALUE;
        ARRAY_VALUE[2]++;
        sannprófa(skila_ARRAY(ARRAY_VALUE) == ARRAY_VALUE && ARRAY_VALUE[2] == 35 && ARRAY_VALUE[4] == 68, 6);
        sannprófa(grein(VALUE - 117) == 7 && grein(VALUE - 15) == 9 && grein(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String Texti = "한글 😀";
        sannprófa(Texti.length() == 5 && Texti.charAt(0) == '한' && Texti.charAt(3) == 0xd83d, 8);
        sannprófa(bretti.örgjörvi_heimild_stig() == 1, 9);
        단말.Skrift("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_örgjörvi 전후 staðbundið_umfang 변수가 보존되는지 검사: 각 작업은 독립된 vél 스택을 쓴다.
        int staðbundið_VALUE = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (verk_röð % 2 + 1 != INDEX) verk_villa++;
            verk_röð++;
            staðbundið_VALUE += Loop_INDEX + INDEX;
            verk_SUM[INDEX] = staðbundið_VALUE;
            작업횟수[INDEX]++;
            bretti.YIELD_örgjörvi();
            if (staðbundið_VALUE != verk_SUM[INDEX]) verk_villa++;
        }
    }
    static void 작업시험() {
        verk_röð = 0; verk_villa = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        sannprófa(bretti.stofna_verk(1) == 0 && bretti.stofna_verk(2) == 0, 20);
        int snúningur_COUNT = 0;
        while (bretti.verk_staða(1) != 0 || bretti.verk_staða(2) != 0) {
            bretti.YIELD_örgjörvi();
            sannprófa(++snúningur_COUNT < 100, 21);
        }
        sannprófa(작업횟수[1] == 10 && 작업횟수[2] == 10 && verk_röð == 20 && verk_villa == 0, 22);
        sannprófa(verk_SUM[1] == 155 && verk_SUM[2] == 265, 23);
        단말.Skrift("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int Lóðrétt_staða, int 너비, int 높이, int 색) {
        for (int Y_hnit = Lóðrétt_staða; Y_hnit < Lóðrétt_staða + 높이; Y_hnit++)
            for (int x_hnit = 가로; x_hnit < 가로 + 너비; x_hnit++) bretti.화면점(x_hnit, Y_hnit, 색);
    }
    static void 화면() {
        if (bretti.화면준비() == 0) { 단말.Skrift("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, bretti.화면너비(), bretti.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.Skrift("FRAMEBUFFER PASS "); 단말.númer(bretti.화면너비()); 단말.문자('x');
        단말.númer(bretti.화면높이()); 단말.Skrift(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int NIÐURSTAÐA = bretti.씨플러스시험();
        sannprófa(NIÐURSTAÐA == 0, 100 + NIÐURSTAÐA);
        단말.Skrift("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        sannprófa(bretti.athuga_notandi_forrit() == 0, 200);
        단말.Skrift("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = bretti.runa_notandi_forrit(0);
        if (처음결과 != 0) { 단말.Skrift("USER DEMO RESULT "); 단말.númer(처음결과); 단말.문자(10); }
        sannprófa(처음결과 == 0, 201);
        단말.Skrift("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Skrift("USER CHECK "); 단말.númer(INDEX); 단말.문자(10);
            int NIÐURSTAÐA = bretti.runa_notandi_forrit(INDEX + 1);
            if (NIÐURSTAÐA != 예상[INDEX]) { 단말.Skrift("USER RESULT "); 단말.númer(NIÐURSTAÐA); 단말.문자(10); }
            sannprófa(NIÐURSTAÐA == 예상[INDEX], 210 + INDEX);
        }
        sannprófa(bretti.runa_notandi_forrit(0) == 0, 220);
        단말.Skrift("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int NIÐURSTAÐA = bretti.runa_notandi_forrit(9);
        if (NIÐURSTAÐA != 0) { 단말.Skrift("UDP RESULT "); 단말.númer(NIÐURSTAÐA); 단말.문자(10); }
        sannprófa(NIÐURSTAÐA == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Skrift("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Skrift("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Skrift("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Skrift("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Skrift("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Keyra_2() {
        단말.Skrift("WorldOS is · Íslenska · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Skrift("NATIVE READY\n");
        명령해석기.keyra_skipun();
    }
}
