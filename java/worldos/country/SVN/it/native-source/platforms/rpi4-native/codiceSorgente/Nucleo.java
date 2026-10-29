// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** nativo Java 커널의 Pi4 stato_iniziale 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class Nucleo {
    static int[] 작업횟수 = new int[3];
    static int[] task_SUM = new int[3];
    static int task_ordine;
    static int task_errore;
    static int casuale_seme = 17;

    static void verificare(boolean condizione, int INDICE) {
        if (!condizione) { 단말.Scrittura("FAIL "); 단말.numero(INDICE); scheda.Ferma(INDICE); }
    }
    static int ramo(int VALORE) {
        switch (VALORE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALORE) {
        switch (VALORE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] Reso_array(int[] array_VALORE) { return array_VALORE; }
    static void test_aritmetico() {
        int VALORE = casuale_seme;
        verificare(VALORE * 7 - VALORE == 102 && VALORE / 3 == 5 && VALORE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        verificare(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        verificare(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        verificare((-VALORE >> 2) == -5 && (-VALORE >>> 2) == 1073741819 && (VALORE << 33) == 34, 4);
        verificare((byte)(VALORE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] array_VALORE = new int[5];
        for (int Loop_INDICE = 0; Loop_INDICE < array_VALORE.length; Loop_INDICE++) array_VALORE[Loop_INDICE] = Loop_INDICE * VALORE;
        array_VALORE[2]++;
        verificare(Reso_array(array_VALORE) == array_VALORE && array_VALORE[2] == 35 && array_VALORE[4] == 68, 6);
        verificare(ramo(VALORE - 117) == 7 && ramo(VALORE - 15) == 9 && ramo(VALORE) == 3 && 촘촘분기(VALORE - 15) == 17, 7);
        String testo = "한글 😀";
        verificare(testo.length() == 5 && testo.charAt(0) == '한' && testo.charAt(3) == 0xd83d, 8);
        verificare(scheda.CPU_privilegio_livello() == 1, 9);
        단말.Scrittura("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDICE) {
        // REND_CPU 전후 locale_Scope 변수가 보존되는지 검사: 각 작업은 독립된 computer 스택을 쓴다.
        int locale_VALORE = INDICE * 100;
        for (int Loop_INDICE = 0; Loop_INDICE < 10; Loop_INDICE++) {
            if (task_ordine % 2 + 1 != INDICE) task_errore++;
            task_ordine++;
            locale_VALORE += Loop_INDICE + INDICE;
            task_SUM[INDICE] = locale_VALORE;
            작업횟수[INDICE]++;
            scheda.REND_CPU();
            if (locale_VALORE != task_SUM[INDICE]) task_errore++;
        }
    }
    static void test_Tasks() {
        task_ordine = 0; task_errore = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        verificare(scheda.Crea_task(1) == 0 && scheda.Crea_task(2) == 0, 20);
        int rotazione_CONTA_NUMERI = 0;
        while (scheda.task_Stato(1) != 0 || scheda.task_Stato(2) != 0) {
            scheda.REND_CPU();
            verificare(++rotazione_CONTA_NUMERI < 100, 21);
        }
        verificare(작업횟수[1] == 10 && 작업횟수[2] == 10 && task_ordine == 20 && task_errore == 0, 22);
        verificare(task_SUM[1] == 155 && task_SUM[2] == 265, 23);
        단말.Scrittura("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void rettangolo(int 가로, int Verticale_funzione, int 너비, int altezza_VALORE, int 색) {
        for (int Y_coordinata = Verticale_funzione; Y_coordinata < Verticale_funzione + altezza_VALORE; Y_coordinata++)
            for (int coordinata_x = 가로; coordinata_x < 가로 + 너비; coordinata_x++) scheda.화면점(coordinata_x, Y_coordinata, 색);
    }
    static void schermata() {
        if (scheda.Prepara_schermata() == 0) { 단말.Scrittura("FRAMEBUFFER unavailable\n"); return; }
        rettangolo(0, 0, scheda.화면너비(), scheda.schermata_altezza(), 0x302018);
        rettangolo(40, 40, 560, 400, 0xefe8e2);
        rettangolo(40, 40, 560, 40, 0x905020);
        rettangolo(60, 110, 240, 140, 0x90b050);
        rettangolo(320, 110, 260, 140, 0xd0a040);
        rettangolo(60, 290, 520, 120, 0xd8d0c8);
        단말.Scrittura("FRAMEBUFFER PASS "); 단말.numero(scheda.화면너비()); 단말.문자('x');
        단말.numero(scheda.schermata_altezza()); 단말.Scrittura(" RGB32 (drawing only)\n");
    }
    static void test_C() {
        int risultato = scheda.씨플러스시험();
        verificare(risultato == 0, 100 + risultato);
        단말.Scrittura("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        verificare(scheda.assegno_USER_app() == 0, 200);
        단말.Scrittura("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = scheda.eseguire_USER_app(0);
        if (처음결과 != 0) { 단말.Scrittura("USER DEMO RESULT "); 단말.numero(처음결과); 단말.문자(10); }
        verificare(처음결과 == 0, 201);
        단말.Scrittura("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDICE = 0; INDICE < 예상.length; INDICE++) {
            단말.Scrittura("USER CHECK "); 단말.numero(INDICE); 단말.문자(10);
            int risultato = scheda.eseguire_USER_app(INDICE + 1);
            if (risultato != 예상[INDICE]) { 단말.Scrittura("USER RESULT "); 단말.numero(risultato); 단말.문자(10); }
            verificare(risultato == 예상[INDICE], 210 + INDICE);
        }
        verificare(scheda.eseguire_USER_app(0) == 0, 220);
        단말.Scrittura("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void test_Rete() {
        int risultato = scheda.eseguire_USER_app(9);
        if (risultato != 0) { 단말.Scrittura("UDP RESULT "); 단말.numero(risultato); 단말.문자(10); }
        verificare(risultato == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Scrittura("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Scrittura("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Scrittura("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Scrittura("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Scrittura("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void avvia() {
        단말.Scrittura("WorldOS it · Ciao · 😀\n");
        test_aritmetico();
        test_C();
        test_Tasks();
        schermata();
        사용자시험();
        test_Rete();
        단말.Scrittura("NATIVE READY\n");
        InterpreteComandi.Esegui_comando();
    }
}
