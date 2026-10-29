// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class eithne {
    static int[] 작업횟수 = new int[3];
    static int[] tasc_SUM = new int[3];
    static int tasc_ord;
    static int tasc_earráid;
    static int 난수씨 = 17;

    static void fíoraigh(boolean coinníoll, int INDEX) {
        if (!coinníoll) { 단말.Scríobh("FAIL "); 단말.수(INDEX); clár.Stad(INDEX); }
    }
    static int craobh(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] return_ARRAY(int[] ARRAY_VALUE) { return ARRAY_VALUE; }
    static void 계산시험() {
        int VALUE = 난수씨;
        fíoraigh(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        fíoraigh(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        fíoraigh(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        fíoraigh((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        fíoraigh((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_VALUE = new int[5];
        for (int lúb_INDEX = 0; lúb_INDEX < ARRAY_VALUE.length; lúb_INDEX++) ARRAY_VALUE[lúb_INDEX] = lúb_INDEX * VALUE;
        ARRAY_VALUE[2]++;
        fíoraigh(return_ARRAY(ARRAY_VALUE) == ARRAY_VALUE && ARRAY_VALUE[2] == 35 && ARRAY_VALUE[4] == 68, 6);
        fíoraigh(craobh(VALUE - 117) == 7 && craobh(VALUE - 15) == 9 && craobh(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String Téacs = "한글 😀";
        fíoraigh(Téacs.length() == 5 && Téacs.charAt(0) == '한' && Téacs.charAt(3) == 0xd83d, 8);
        fíoraigh(clár.CPU_cead_leibhéal() == 1, 9);
        단말.Scríobh("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_CPU 전후 logánta_scóip 변수가 보존되는지 검사: 각 작업은 독립된 meaisín 스택을 쓴다.
        int logánta_VALUE = INDEX * 100;
        for (int lúb_INDEX = 0; lúb_INDEX < 10; lúb_INDEX++) {
            if (tasc_ord % 2 + 1 != INDEX) tasc_earráid++;
            tasc_ord++;
            logánta_VALUE += lúb_INDEX + INDEX;
            tasc_SUM[INDEX] = logánta_VALUE;
            작업횟수[INDEX]++;
            clár.YIELD_CPU();
            if (logánta_VALUE != tasc_SUM[INDEX]) tasc_earráid++;
        }
    }
    static void 작업시험() {
        tasc_ord = 0; tasc_earráid = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        fíoraigh(clár.Create_tasc(1) == 0 && clár.Create_tasc(2) == 0, 20);
        int rothlú_COUNT = 0;
        while (clár.tasc_staid(1) != 0 || clár.tasc_staid(2) != 0) {
            clár.YIELD_CPU();
            fíoraigh(++rothlú_COUNT < 100, 21);
        }
        fíoraigh(작업횟수[1] == 10 && 작업횟수[2] == 10 && tasc_ord == 20 && tasc_earráid == 0, 22);
        fíoraigh(tasc_SUM[1] == 155 && tasc_SUM[2] == 265, 23);
        단말.Scríobh("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int Ingearach_suíomh, int 너비, int 높이, int 색) {
        for (int 세로좌표 = Ingearach_suíomh; 세로좌표 < Ingearach_suíomh + 높이; 세로좌표++)
            for (int x_chomhordanáid = 가로; x_chomhordanáid < 가로 + 너비; x_chomhordanáid++) clár.화면점(x_chomhordanáid, 세로좌표, 색);
    }
    static void 화면() {
        if (clár.화면준비() == 0) { 단말.Scríobh("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, clár.화면너비(), clár.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.Scríobh("FRAMEBUFFER PASS "); 단말.수(clár.화면너비()); 단말.문자('x');
        단말.수(clár.화면높이()); 단말.Scríobh(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int tomhas = clár.씨플러스시험();
        fíoraigh(tomhas == 0, 100 + tomhas);
        단말.Scríobh("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        fíoraigh(clár.seic_úsáideoir_clár() == 0, 200);
        단말.Scríobh("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = clár.rith_úsáideoir_clár(0);
        if (처음결과 != 0) { 단말.Scríobh("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        fíoraigh(처음결과 == 0, 201);
        단말.Scríobh("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Scríobh("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int tomhas = clár.rith_úsáideoir_clár(INDEX + 1);
            if (tomhas != 예상[INDEX]) { 단말.Scríobh("USER RESULT "); 단말.수(tomhas); 단말.문자(10); }
            fíoraigh(tomhas == 예상[INDEX], 210 + INDEX);
        }
        fíoraigh(clár.rith_úsáideoir_clár(0) == 0, 220);
        단말.Scríobh("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int tomhas = clár.rith_úsáideoir_clár(9);
        if (tomhas != 0) { 단말.Scríobh("UDP RESULT "); 단말.수(tomhas); 단말.문자(10); }
        fíoraigh(tomhas == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Scríobh("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Scríobh("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Scríobh("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Scríobh("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Scríobh("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Rith_2() {
        단말.Scríobh("WorldOS ga · ga · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Scríobh("NATIVE READY\n");
        명령해석기.Rith_ordú();
    }
}
