// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** lastno Java 커널의 Pi4 začetno_stanje 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class jedro {
    static int[] 작업횟수 = new int[3];
    static int[] opravek_SUM = new int[3];
    static int opravek_naročilo;
    static int 작업오류;
    static int 난수씨 = 17;

    static void 확인(boolean pogoj, int INDEX) {
        if (!pogoj) { 단말.Pisanje("FAIL "); 단말.수(INDEX); Tabla.Zaustavi(INDEX); }
    }
    static int veja(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] vrni_ARRAY(int[] ARRAY_VALUE) { return ARRAY_VALUE; }
    static void 계산시험() {
        int VALUE = 난수씨;
        확인(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        확인(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        확인(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        확인((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        확인((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_VALUE = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < ARRAY_VALUE.length; Loop_INDEX++) ARRAY_VALUE[Loop_INDEX] = Loop_INDEX * VALUE;
        ARRAY_VALUE[2]++;
        확인(vrni_ARRAY(ARRAY_VALUE) == ARRAY_VALUE && ARRAY_VALUE[2] == 35 && ARRAY_VALUE[4] == 68, 6);
        확인(veja(VALUE - 117) == 7 && veja(VALUE - 15) == 9 && veja(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String Besedilo = "한글 😀";
        확인(Besedilo.length() == 5 && Besedilo.charAt(0) == '한' && Besedilo.charAt(3) == 0xd83d, 8);
        확인(Tabla.CPE_pravica_raven() == 1, 9);
        단말.Pisanje("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_CPE 전후 lokalen_krajeven_obseg 변수가 보존되는지 검사: 각 작업은 독립된 računalnik 스택을 쓴다.
        int lokalen_krajeven_VALUE = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (opravek_naročilo % 2 + 1 != INDEX) 작업오류++;
            opravek_naročilo++;
            lokalen_krajeven_VALUE += Loop_INDEX + INDEX;
            opravek_SUM[INDEX] = lokalen_krajeven_VALUE;
            작업횟수[INDEX]++;
            Tabla.YIELD_CPE();
            if (lokalen_krajeven_VALUE != opravek_SUM[INDEX]) 작업오류++;
        }
    }
    static void preskusiti_Tasks() {
        opravek_naročilo = 0; 작업오류 = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        확인(Tabla.Ustvari_opravek(1) == 0 && Tabla.Ustvari_opravek(2) == 0, 20);
        int sukanje_COUNT = 0;
        while (Tabla.opravek_stanje(1) != 0 || Tabla.opravek_stanje(2) != 0) {
            Tabla.YIELD_CPE();
            확인(++sukanje_COUNT < 100, 21);
        }
        확인(작업횟수[1] == 10 && 작업횟수[2] == 10 && opravek_naročilo == 20 && 작업오류 == 0, 22);
        확인(opravek_SUM[1] == 155 && opravek_SUM[2] == 265, 23);
        단말.Pisanje("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void pravokotnik(int 가로, int Navpično_položaj, int 너비, int višina_VALUE, int 색) {
        for (int 세로좌표 = Navpično_položaj; 세로좌표 < Navpično_položaj + višina_VALUE; 세로좌표++)
            for (int koordinata_x = 가로; koordinata_x < 가로 + 너비; koordinata_x++) Tabla.화면점(koordinata_x, 세로좌표, 색);
    }
    static void 화면() {
        if (Tabla.화면준비() == 0) { 단말.Pisanje("FRAMEBUFFER unavailable\n"); return; }
        pravokotnik(0, 0, Tabla.화면너비(), Tabla.화면높이(), 0x302018);
        pravokotnik(40, 40, 560, 400, 0xefe8e2);
        pravokotnik(40, 40, 560, 40, 0x905020);
        pravokotnik(60, 110, 240, 140, 0x90b050);
        pravokotnik(320, 110, 260, 140, 0xd0a040);
        pravokotnik(60, 290, 520, 120, 0xd8d0c8);
        단말.Pisanje("FRAMEBUFFER PASS "); 단말.수(Tabla.화면너비()); 단말.문자('x');
        단말.수(Tabla.화면높이()); 단말.Pisanje(" RGB32 (drawing only)\n");
    }
    static void preskusiti_C() {
        int REZULTAT = Tabla.씨플러스시험();
        확인(REZULTAT == 0, 100 + REZULTAT);
        단말.Pisanje("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        확인(Tabla.preveriti_uporabnik_aplikacija() == 0, 200);
        단말.Pisanje("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = Tabla.izvajati_uporabnik_aplikacija(0);
        if (처음결과 != 0) { 단말.Pisanje("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        확인(처음결과 == 0, 201);
        단말.Pisanje("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Pisanje("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int REZULTAT = Tabla.izvajati_uporabnik_aplikacija(INDEX + 1);
            if (REZULTAT != 예상[INDEX]) { 단말.Pisanje("USER RESULT "); 단말.수(REZULTAT); 단말.문자(10); }
            확인(REZULTAT == 예상[INDEX], 210 + INDEX);
        }
        확인(Tabla.izvajati_uporabnik_aplikacija(0) == 0, 220);
        단말.Pisanje("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void preskusiti_Uporaba_omrežij() {
        int REZULTAT = Tabla.izvajati_uporabnik_aplikacija(9);
        if (REZULTAT != 0) { 단말.Pisanje("UDP RESULT "); 단말.수(REZULTAT); 단말.문자(10); }
        확인(REZULTAT == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Pisanje("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Pisanje("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Pisanje("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Pisanje("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Pisanje("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Zaženi() {
        단말.Pisanje("WorldOS sl · slovenščina · 😀\n");
        계산시험();
        preskusiti_C();
        preskusiti_Tasks();
        화면();
        사용자시험();
        preskusiti_Uporaba_omrežij();
        단말.Pisanje("NATIVE READY\n");
        명령해석기.Izvedi_ukaz();
    }
}
