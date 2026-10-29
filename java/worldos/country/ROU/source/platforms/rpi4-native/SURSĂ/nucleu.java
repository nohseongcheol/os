// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** propriu Java 커널의 Pi4 stare_inițială 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class nucleu {
    static int[] 작업횟수 = new int[3];
    static int[] sarcină_SUM = new int[3];
    static int sarcină_ordine;
    static int sarcină_eroare;
    static int aleator_adăugare_sursă = 17;

    static void verifica(boolean condiție, int INDEX) {
        if (!condiție) { 단말.Scriere("FAIL "); 단말.수(INDEX); Avizier.Oprește(INDEX); }
    }
    static int ramură(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] restitui_ARRAY(int[] ARRAY_VALUE) { return ARRAY_VALUE; }
    static void 계산시험() {
        int VALUE = aleator_adăugare_sursă;
        verifica(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        verifica(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        verifica(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        verifica((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        verifica((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_VALUE = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < ARRAY_VALUE.length; Loop_INDEX++) ARRAY_VALUE[Loop_INDEX] = Loop_INDEX * VALUE;
        ARRAY_VALUE[2]++;
        verifica(restitui_ARRAY(ARRAY_VALUE) == ARRAY_VALUE && ARRAY_VALUE[2] == 35 && ARRAY_VALUE[4] == 68, 6);
        verifica(ramură(VALUE - 117) == 7 && ramură(VALUE - 15) == 9 && ramură(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String SMS = "한글 😀";
        verifica(SMS.length() == 5 && SMS.charAt(0) == '한' && SMS.charAt(3) == 0xd83d, 8);
        verifica(Avizier.CPU_permisiune_nivel() == 1, 9);
        단말.Scriere("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_CPU 전후 local_gamă 변수가 보존되는지 검사: 각 작업은 독립된 mașină 스택을 쓴다.
        int local_VALUE = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (sarcină_ordine % 2 + 1 != INDEX) sarcină_eroare++;
            sarcină_ordine++;
            local_VALUE += Loop_INDEX + INDEX;
            sarcină_SUM[INDEX] = local_VALUE;
            작업횟수[INDEX]++;
            Avizier.YIELD_CPU();
            if (local_VALUE != sarcină_SUM[INDEX]) sarcină_eroare++;
        }
    }
    static void 작업시험() {
        sarcină_ordine = 0; sarcină_eroare = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        verifica(Avizier.crea_sarcină(1) == 0 && Avizier.crea_sarcină(2) == 0, 20);
        int rotație_COUNT = 0;
        while (Avizier.sarcină_Stare(1) != 0 || Avizier.sarcină_Stare(2) != 0) {
            Avizier.YIELD_CPU();
            verifica(++rotație_COUNT < 100, 21);
        }
        verifica(작업횟수[1] == 10 && 작업횟수[2] == 10 && sarcină_ordine == 20 && sarcină_eroare == 0, 22);
        verifica(sarcină_SUM[1] == 155 && sarcină_SUM[2] == 265, 23);
        단말.Scriere("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void dreptunghi(int 가로, int Verticală_poziție, int 너비, int 높이, int 색) {
        for (int 세로좌표 = Verticală_poziție; 세로좌표 < Verticală_poziție + 높이; 세로좌표++)
            for (int coordonata_X = 가로; coordonata_X < 가로 + 너비; coordonata_X++) Avizier.화면점(coordonata_X, 세로좌표, 색);
    }
    static void 화면() {
        if (Avizier.화면준비() == 0) { 단말.Scriere("FRAMEBUFFER unavailable\n"); return; }
        dreptunghi(0, 0, Avizier.화면너비(), Avizier.화면높이(), 0x302018);
        dreptunghi(40, 40, 560, 400, 0xefe8e2);
        dreptunghi(40, 40, 560, 40, 0x905020);
        dreptunghi(60, 110, 240, 140, 0x90b050);
        dreptunghi(320, 110, 260, 140, 0xd0a040);
        dreptunghi(60, 290, 520, 120, 0xd8d0c8);
        단말.Scriere("FRAMEBUFFER PASS "); 단말.수(Avizier.화면너비()); 단말.문자('x');
        단말.수(Avizier.화면높이()); 단말.Scriere(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int KR = Avizier.씨플러스시험();
        verifica(KR == 0, 100 + KR);
        단말.Scriere("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        verifica(Avizier.verifica_utilizator_program() == 0, 200);
        단말.Scriere("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = Avizier.rula_utilizator_program(0);
        if (처음결과 != 0) { 단말.Scriere("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        verifica(처음결과 == 0, 201);
        단말.Scriere("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Scriere("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int KR = Avizier.rula_utilizator_program(INDEX + 1);
            if (KR != 예상[INDEX]) { 단말.Scriere("USER RESULT "); 단말.수(KR); 단말.문자(10); }
            verifica(KR == 예상[INDEX], 210 + INDEX);
        }
        verifica(Avizier.rula_utilizator_program(0) == 0, 220);
        단말.Scriere("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int KR = Avizier.rula_utilizator_program(9);
        if (KR != 0) { 단말.Scriere("UDP RESULT "); 단말.수(KR); 단말.문자(10); }
        verifica(KR == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Scriere("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Scriere("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Scriere("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Scriere("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Scriere("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Pornește() {
        단말.Scriere("WorldOS ro · Română · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Scriere("NATIVE READY\n");
        명령해석기.executa_comandă();
    }
}
