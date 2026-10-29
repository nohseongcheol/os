// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** savas Java 커널의 Pi4 pradinė_būsena 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class branduolys {
    static int[] 작업횟수 = new int[3];
    static int[] užduotis_SUM = new int[3];
    static int užduotis_tvarka;
    static int 작업오류;
    static int atsitiktinis_pirminė_reikšmė = 17;

    static void patvirtinti(boolean sąlyga, int INDEX) {
        if (!sąlyga) { 단말.Rašymas("FAIL "); 단말.numeris(INDEX); Lenta.Sustabdyti(INDEX); }
    }
    static int šaka(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] grąžinti_ARRAY(int[] ARRAY_VALUE) { return ARRAY_VALUE; }
    static void 계산시험() {
        int VALUE = atsitiktinis_pirminė_reikšmė;
        patvirtinti(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        patvirtinti(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        patvirtinti(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        patvirtinti((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        patvirtinti((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_VALUE = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < ARRAY_VALUE.length; Loop_INDEX++) ARRAY_VALUE[Loop_INDEX] = Loop_INDEX * VALUE;
        ARRAY_VALUE[2]++;
        patvirtinti(grąžinti_ARRAY(ARRAY_VALUE) == ARRAY_VALUE && ARRAY_VALUE[2] == 35 && ARRAY_VALUE[4] == 68, 6);
        patvirtinti(šaka(VALUE - 117) == 7 && šaka(VALUE - 15) == 9 && šaka(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String Tekstas = "한글 😀";
        patvirtinti(Tekstas.length() == 5 && Tekstas.charAt(0) == '한' && Tekstas.charAt(3) == 0xd83d, 8);
        patvirtinti(Lenta.CPU_teisė_lygis() == 1, 9);
        단말.Rašymas("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_CPU 전후 vietinis_Aprėptis 변수가 보존되는지 검사: 각 작업은 독립된 mašina 스택을 쓴다.
        int vietinis_VALUE = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (užduotis_tvarka % 2 + 1 != INDEX) 작업오류++;
            užduotis_tvarka++;
            vietinis_VALUE += Loop_INDEX + INDEX;
            užduotis_SUM[INDEX] = vietinis_VALUE;
            작업횟수[INDEX]++;
            Lenta.YIELD_CPU();
            if (vietinis_VALUE != užduotis_SUM[INDEX]) 작업오류++;
        }
    }
    static void 작업시험() {
        užduotis_tvarka = 0; 작업오류 = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        patvirtinti(Lenta.kurti_užduotis(1) == 0 && Lenta.kurti_užduotis(2) == 0, 20);
        int sukimas_COUNT = 0;
        while (Lenta.užduotis_Būsena(1) != 0 || Lenta.užduotis_Būsena(2) != 0) {
            Lenta.YIELD_CPU();
            patvirtinti(++sukimas_COUNT < 100, 21);
        }
        patvirtinti(작업횟수[1] == 10 && 작업횟수[2] == 10 && užduotis_tvarka == 20 && 작업오류 == 0, 22);
        patvirtinti(užduotis_SUM[1] == 155 && užduotis_SUM[2] == 265, 23);
        단말.Rašymas("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void stačiakampis(int 가로, int segmentas_padėtis, int 너비, int 높이, int 색) {
        for (int 세로좌표 = segmentas_padėtis; 세로좌표 < segmentas_padėtis + 높이; 세로좌표++)
            for (int x_koordinatė = 가로; x_koordinatė < 가로 + 너비; x_koordinatė++) Lenta.화면점(x_koordinatė, 세로좌표, 색);
    }
    static void 화면() {
        if (Lenta.화면준비() == 0) { 단말.Rašymas("FRAMEBUFFER unavailable\n"); return; }
        stačiakampis(0, 0, Lenta.화면너비(), Lenta.화면높이(), 0x302018);
        stačiakampis(40, 40, 560, 400, 0xefe8e2);
        stačiakampis(40, 40, 560, 40, 0x905020);
        stačiakampis(60, 110, 240, 140, 0x90b050);
        stačiakampis(320, 110, 260, 140, 0xd0a040);
        stačiakampis(60, 290, 520, 120, 0xd8d0c8);
        단말.Rašymas("FRAMEBUFFER PASS "); 단말.numeris(Lenta.화면너비()); 단말.문자('x');
        단말.numeris(Lenta.화면높이()); 단말.Rašymas(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int REZULTATAS = Lenta.씨플러스시험();
        patvirtinti(REZULTATAS == 0, 100 + REZULTATAS);
        단말.Rašymas("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        patvirtinti(Lenta.čekis_naudotojas_programa() == 0, 200);
        단말.Rašymas("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = Lenta.vykdyti_naudotojas_programa(0);
        if (처음결과 != 0) { 단말.Rašymas("USER DEMO RESULT "); 단말.numeris(처음결과); 단말.문자(10); }
        patvirtinti(처음결과 == 0, 201);
        단말.Rašymas("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Rašymas("USER CHECK "); 단말.numeris(INDEX); 단말.문자(10);
            int REZULTATAS = Lenta.vykdyti_naudotojas_programa(INDEX + 1);
            if (REZULTATAS != 예상[INDEX]) { 단말.Rašymas("USER RESULT "); 단말.numeris(REZULTATAS); 단말.문자(10); }
            patvirtinti(REZULTATAS == 예상[INDEX], 210 + INDEX);
        }
        patvirtinti(Lenta.vykdyti_naudotojas_programa(0) == 0, 220);
        단말.Rašymas("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int REZULTATAS = Lenta.vykdyti_naudotojas_programa(9);
        if (REZULTATAS != 0) { 단말.Rašymas("UDP RESULT "); 단말.numeris(REZULTATAS); 단말.문자(10); }
        patvirtinti(REZULTATAS == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Rašymas("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Rašymas("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Rašymas("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Rašymas("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Rašymas("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Paleisti() {
        단말.Rašymas("WorldOS lt · lt · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Rašymas("NATIVE READY\n");
        명령해석기.Vykdyti_komanda();
    }
}
