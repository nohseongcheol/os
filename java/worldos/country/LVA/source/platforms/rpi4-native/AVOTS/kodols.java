// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** savs Java 커널의 Pi4 sākumstāvoklis 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class kodols {
    static int[] 작업횟수 = new int[3];
    static int[] uzdevums_SUM = new int[3];
    static int uzdevums_secība;
    static int uzdevums_kļūda;
    static int nejaušs_dēstīt = 17;

    static void verificēt(boolean nosacījums, int INDEX) {
        if (!nosacījums) { 단말.Rakstīt("FAIL "); 단말.numurs(INDEX); Panelis.Pārtraukt(INDEX); }
    }
    static int zars(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] atdot_ARRAY(int[] ARRAY_VALUE) { return ARRAY_VALUE; }
    static void 계산시험() {
        int VALUE = nejaušs_dēstīt;
        verificēt(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        verificēt(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        verificēt(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        verificēt((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        verificēt((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_VALUE = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < ARRAY_VALUE.length; Loop_INDEX++) ARRAY_VALUE[Loop_INDEX] = Loop_INDEX * VALUE;
        ARRAY_VALUE[2]++;
        verificēt(atdot_ARRAY(ARRAY_VALUE) == ARRAY_VALUE && ARRAY_VALUE[2] == 35 && ARRAY_VALUE[4] == 68, 6);
        verificēt(zars(VALUE - 117) == 7 && zars(VALUE - 15) == 9 && zars(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String Teksts = "한글 😀";
        verificēt(Teksts.length() == 5 && Teksts.charAt(0) == '한' && Teksts.charAt(3) == 0xd83d, 8);
        verificēt(Panelis.centrālais_procesors_atļauja_līmenis() == 1, 9);
        단말.Rakstīt("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_apstrādātājs 전후 vietējs_Tvērums 변수가 보존되는지 검사: 각 작업은 독립된 mašīna 스택을 쓴다.
        int vietējs_VALUE = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (uzdevums_secība % 2 + 1 != INDEX) uzdevums_kļūda++;
            uzdevums_secība++;
            vietējs_VALUE += Loop_INDEX + INDEX;
            uzdevums_SUM[INDEX] = vietējs_VALUE;
            작업횟수[INDEX]++;
            Panelis.YIELD_apstrādātājs();
            if (vietējs_VALUE != uzdevums_SUM[INDEX]) uzdevums_kļūda++;
        }
    }
    static void 작업시험() {
        uzdevums_secība = 0; uzdevums_kļūda = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        verificēt(Panelis.atvērt_uzdevums(1) == 0 && Panelis.atvērt_uzdevums(2) == 0, 20);
        int pagriešana_COUNT = 0;
        while (Panelis.uzdevums_Statuss(1) != 0 || Panelis.uzdevums_Statuss(2) != 0) {
            Panelis.YIELD_apstrādātājs();
            verificēt(++pagriešana_COUNT < 100, 21);
        }
        verificēt(작업횟수[1] == 10 && 작업횟수[2] == 10 && uzdevums_secība == 20 && uzdevums_kļūda == 0, 22);
        verificēt(uzdevums_SUM[1] == 155 && uzdevums_SUM[2] == 265, 23);
        단말.Rakstīt("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void taisnstūris(int 가로, int vertikāle_amats, int 너비, int 높이, int 색) {
        for (int 세로좌표 = vertikāle_amats; 세로좌표 < vertikāle_amats + 높이; 세로좌표++)
            for (int x_koordināta = 가로; x_koordināta < 가로 + 너비; x_koordināta++) Panelis.화면점(x_koordināta, 세로좌표, 색);
    }
    static void 화면() {
        if (Panelis.화면준비() == 0) { 단말.Rakstīt("FRAMEBUFFER unavailable\n"); return; }
        taisnstūris(0, 0, Panelis.화면너비(), Panelis.화면높이(), 0x302018);
        taisnstūris(40, 40, 560, 400, 0xefe8e2);
        taisnstūris(40, 40, 560, 40, 0x905020);
        taisnstūris(60, 110, 240, 140, 0x90b050);
        taisnstūris(320, 110, 260, 140, 0xd0a040);
        taisnstūris(60, 290, 520, 120, 0xd8d0c8);
        단말.Rakstīt("FRAMEBUFFER PASS "); 단말.numurs(Panelis.화면너비()); 단말.문자('x');
        단말.numurs(Panelis.화면높이()); 단말.Rakstīt(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int mērs = Panelis.씨플러스시험();
        verificēt(mērs == 0, 100 + mērs);
        단말.Rakstīt("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        verificēt(Panelis.čeks_lietotājs_programma() == 0, 200);
        단말.Rakstīt("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = Panelis.virkne_lietotājs_programma(0);
        if (처음결과 != 0) { 단말.Rakstīt("USER DEMO RESULT "); 단말.numurs(처음결과); 단말.문자(10); }
        verificēt(처음결과 == 0, 201);
        단말.Rakstīt("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Rakstīt("USER CHECK "); 단말.numurs(INDEX); 단말.문자(10);
            int mērs = Panelis.virkne_lietotājs_programma(INDEX + 1);
            if (mērs != 예상[INDEX]) { 단말.Rakstīt("USER RESULT "); 단말.numurs(mērs); 단말.문자(10); }
            verificēt(mērs == 예상[INDEX], 210 + INDEX);
        }
        verificēt(Panelis.virkne_lietotājs_programma(0) == 0, 220);
        단말.Rakstīt("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int mērs = Panelis.virkne_lietotājs_programma(9);
        if (mērs != 0) { 단말.Rakstīt("UDP RESULT "); 단말.numurs(mērs); 단말.문자(10); }
        verificēt(mērs == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Rakstīt("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Rakstīt("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Rakstīt("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Rakstīt("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Rakstīt("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Palaist() {
        단말.Rakstīt("WorldOS lv · Latviešu · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Rakstīt("NATIVE READY\n");
        명령해석기.Izpildīt_komanda();
    }
}
