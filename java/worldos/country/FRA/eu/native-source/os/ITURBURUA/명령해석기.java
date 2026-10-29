// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Idatzi 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int luzera_balio = 0;
    static boolean 앞줄복귀 = false;
    static boolean 줄넘침 = false;

    static boolean Komandoa(String Izena) {
        if (luzera_balio < Izena.length()) return false;
        for (int INDIZE = 0; INDIZE < Izena.length(); INDIZE++)
            if (입력[INDIZE] != Izena.charAt(INDIZE)) return false;
        return luzera_balio == Izena.length() || 입력[Izena.length()] == ' ';
    }

    static void erakutsi_laguntza() {
        SMS_Terminal.Idatzi("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminal.Idatzi("apps | run NAME [ARGS] | net\n");
        SMS_Terminal.Idatzi("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminal.Idatzi("sync (연결된 JKSTORE1 Store_balio 장치에 Fitxategia 보존)\n");
    }

    static void prozesu_balio_sarrera() {
        if (luzera_balio == 0) return;
        if (Komandoa("help")) erakutsi_laguntza();
        else if (Komandoa("sync")) {
            int EMAITZA = 파일보존.sinkronizatu();
            SMS_Terminal.Idatzi("Sync: "); SMS_Terminal.수쓰기(EMAITZA); SMS_Terminal.문자(10);
        }
        else if (Komandoa("ls")) Memoria_fitxategi_sistema.sarrera_Zerrenda();
        else if (Komandoa("edit")) Memoria_fitxategi_sistema.Komandoa(입력, 4, luzera_balio, 0);
        else if (Komandoa("cat")) Memoria_fitxategi_sistema.Komandoa(입력, 3, luzera_balio, 1);
        else if (Komandoa("rm")) Memoria_fitxategi_sistema.Komandoa(입력, 2, luzera_balio, 2);
        else if (Komandoa("java") || Komandoa("javac")) {
            int EMAITZA = 실행관리.exekutatu_komando(입력, 0, luzera_balio);
            SMS_Terminal.Idatzi("Exit: "); SMS_Terminal.수쓰기(EMAITZA); SMS_Terminal.문자(10);
        }
        else if (Komandoa("apps")) 실행관리.sarrera_Zerrenda();
        else if (Komandoa("net")) sare_pila.Egoera_balio();
        else if (Komandoa("run")) {
            int EMAITZA = 실행관리.exekutatu_komando(입력, 3, luzera_balio);
            SMS_Terminal.Idatzi("Exit: "); SMS_Terminal.수쓰기(EMAITZA); SMS_Terminal.Idatzi("\n");
        } else if (Komandoa("info")) {
            SMS_Terminal.Idatzi("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Komandoa("mem")) {
            SMS_Terminal.Idatzi("위쪽 Memoria_balio 공간(KiB): "); SMS_Terminal.수쓰기(기억공간.위쪽기억크기());
            SMS_Terminal.Idatzi("\n배열 동적 Memoria_balio 공간(byte_balio): "); SMS_Terminal.수쓰기(gailu_balio.배열사용량());
            SMS_Terminal.Idatzi(" / 262144\n작업 공간 sekzio_balio: "); SMS_Terminal.수쓰기(기억공간.사용개수());
            SMS_Terminal.Idatzi(" / 8 (각 4096바이트)\n");
        } else if (Komandoa("alloc")) {
            int INDIZE = 기억공간.esleitu_biltegi();
            SMS_Terminal.Idatzi("sekzio_balio INDIZE: "); SMS_Terminal.수쓰기(INDIZE); SMS_Terminal.Idatzi("\n");
        } else if (Komandoa("free")) {
            if (luzera_balio == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Terminal.Idatzi(기억공간.itzuli_neurria(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 sekzio_balio\n");
            } else SMS_Terminal.Idatzi("사용법: free 0..7\n");
        } else if (Komandoa("echo")) {
            for (int INDIZE = 5; INDIZE < luzera_balio; INDIZE++) SMS_Terminal.문자(입력[INDIZE]);
            SMS_Terminal.문자(10);
        } else if (Komandoa("clear")) SMS_Terminal.ezabatu_sarrera();
        else if (Komandoa("test")) nukleo.시험();
        else if (Komandoa("halt")) {
            SMS_Terminal.Idatzi("HALTED\n");
            gailu_balio.정지();
        } else SMS_Terminal.Idatzi("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void onartu_ETA_idatzi(int balio) {
        if (balio == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = balio == 13;
        if (balio == 10 || balio == 13) {
            SMS_Terminal.문자(10);
            if (Memoria_fitxategi_sistema.편집중) Memoria_fitxategi_sistema.Editatutakoak_lerro(입력, luzera_balio, 줄넘침);
            else prozesu_balio_sarrera();
            luzera_balio = 0;
            줄넘침 = false;
            SMS_Terminal.Idatzi(Memoria_fitxategi_sistema.편집중 ? "...> " : "jkoros> ");
        } else if (balio == 8 || balio == 127) {
            if (luzera_balio > 0) {
                luzera_balio--;
                SMS_Terminal.직렬바이트(8); SMS_Terminal.직렬바이트(32); SMS_Terminal.직렬바이트(8);
                SMS_Terminal.화면문자(8);
            }
        } else if (balio >= 32 && balio < 127 && luzera_balio < 입력.length) {
            입력[luzera_balio++] = balio;
            SMS_Terminal.문자(balio);
        } else if (balio >= 32 && balio < 127) 줄넘침 = true;
    }

    static void Exekutatu_2() {
        erakutsi_laguntza();
        SMS_Terminal.Idatzi("READY\njkoros> ");
        while (true) {
            int balio = SMS_Terminal.직렬읽기();
            if (balio < 0) balio = teklatu.Irakurri();
            if (balio >= 0) onartu_ETA_idatzi(balio);
            else { sare_pila.egiaztatu(); gailu_balio.잠시양보(); }
        }
    }
}
