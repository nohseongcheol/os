// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Scriere 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int lungime_VALUE = 0;
    static boolean 앞줄복귀 = false;
    static boolean linie_depășire = false;

    static boolean Comandă(String Nume) {
        if (lungime_VALUE < Nume.length()) return false;
        for (int INDEX = 0; INDEX < Nume.length(); INDEX++)
            if (입력[INDEX] != Nume.charAt(INDEX)) return false;
        return lungime_VALUE == Nume.length() || 입력[Nume.length()] == ' ';
    }

    static void afișa_ajutor() {
        SMS_Terminal.Scriere("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminal.Scriere("apps | run NAME [ARGS] | net\n");
        SMS_Terminal.Scriere("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminal.Scriere("sync (연결된 JKSTORE1 Store_VALUE 장치에 Fișier 보존)\n");
    }

    static void Proces_VALUE_intrare() {
        if (lungime_VALUE == 0) return;
        if (Comandă("help")) afișa_ajutor();
        else if (Comandă("sync")) {
            int KR = 파일보존.sincroniz();
            SMS_Terminal.Scriere("Sync: "); SMS_Terminal.수쓰기(KR); SMS_Terminal.문자(10);
        }
        else if (Comandă("ls")) Memorie_sistem_de_fișiere.intrare_Listă();
        else if (Comandă("edit")) Memorie_sistem_de_fișiere.Comandă(입력, 4, lungime_VALUE, 0);
        else if (Comandă("cat")) Memorie_sistem_de_fișiere.Comandă(입력, 3, lungime_VALUE, 1);
        else if (Comandă("rm")) Memorie_sistem_de_fișiere.Comandă(입력, 2, lungime_VALUE, 2);
        else if (Comandă("java") || Comandă("javac")) {
            int KR = 실행관리.executa_comandă(입력, 0, lungime_VALUE);
            SMS_Terminal.Scriere("Exit: "); SMS_Terminal.수쓰기(KR); SMS_Terminal.문자(10);
        }
        else if (Comandă("apps")) 실행관리.intrare_Listă();
        else if (Comandă("net")) rețea_Teanc.Stare_VALUE();
        else if (Comandă("run")) {
            int KR = 실행관리.executa_comandă(입력, 3, lungime_VALUE);
            SMS_Terminal.Scriere("Exit: "); SMS_Terminal.수쓰기(KR); SMS_Terminal.Scriere("\n");
        } else if (Comandă("info")) {
            SMS_Terminal.Scriere("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Comandă("mem")) {
            SMS_Terminal.Scriere("위쪽 Memorie_VALUE adresa_regiune(KiB): "); SMS_Terminal.수쓰기(Memorie_regiune.UPPER_Memorie_dimensiona());
            SMS_Terminal.Scriere("\n배열 동적 Memorie_VALUE adresa_regiune(byte_VALUE): "); SMS_Terminal.수쓰기(mobil_VALUE.ARRAY_consum());
            SMS_Terminal.Scriere(" / 262144\n작업 adresa_regiune secțiune_VALUE: "); SMS_Terminal.수쓰기(Memorie_regiune.사용개수());
            SMS_Terminal.Scriere(" / 8 (각 4096바이트)\n");
        } else if (Comandă("alloc")) {
            int INDEX = Memorie_regiune.aloca_Stocare();
            SMS_Terminal.Scriere("secțiune_VALUE INDEX: "); SMS_Terminal.수쓰기(INDEX); SMS_Terminal.Scriere("\n");
        } else if (Comandă("free")) {
            if (lungime_VALUE == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Terminal.Scriere(Memorie_regiune.restitui_KR(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 secțiune_VALUE\n");
            } else SMS_Terminal.Scriere("사용법: free 0..7\n");
        } else if (Comandă("echo")) {
            for (int INDEX = 5; INDEX < lungime_VALUE; INDEX++) SMS_Terminal.문자(입력[INDEX]);
            SMS_Terminal.문자(10);
        } else if (Comandă("clear")) SMS_Terminal.șterge_intrare();
        else if (Comandă("test")) nucleu.시험();
        else if (Comandă("halt")) {
            SMS_Terminal.Scriere("HALTED\n");
            mobil_VALUE.정지();
        } else SMS_Terminal.Scriere("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void accepta_AND_scriere(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_Terminal.문자(10);
            if (Memorie_sistem_de_fișiere.편집중) Memorie_sistem_de_fișiere.Editate_linie(입력, lungime_VALUE, linie_depășire);
            else Proces_VALUE_intrare();
            lungime_VALUE = 0;
            linie_depășire = false;
            SMS_Terminal.Scriere(Memorie_sistem_de_fișiere.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (lungime_VALUE > 0) {
                lungime_VALUE--;
                SMS_Terminal.직렬바이트(8); SMS_Terminal.직렬바이트(32); SMS_Terminal.직렬바이트(8);
                SMS_Terminal.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && lungime_VALUE < 입력.length) {
            입력[lungime_VALUE++] = VALUE;
            SMS_Terminal.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) linie_depășire = true;
    }

    static void Pornește() {
        afișa_ajutor();
        SMS_Terminal.Scriere("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_Terminal.직렬읽기();
            if (VALUE < 0) VALUE = tastatură.Citire();
            if (VALUE >= 0) accepta_AND_scriere(VALUE);
            else { rețea_Teanc.verifica(); mobil_VALUE.잠시양보(); }
        }
    }
}
