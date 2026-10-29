// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Skriv 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int lengd_VALUE = 0;
    static boolean 앞줄복귀 = false;
    static boolean line_overflyt = false;

    static boolean Kommando(String Namn) {
        if (lengd_VALUE < Namn.length()) return false;
        for (int INDEX = 0; INDEX < Namn.length(); INDEX++)
            if (입력[INDEX] != Namn.charAt(INDEX)) return false;
        return lengd_VALUE == Namn.length() || 입력[Namn.length()] == ' ';
    }

    static void vise_hjelp() {
        SMS_Terminal.Skriv("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminal.Skriv("apps | run NAME [ARGS] | net\n");
        SMS_Terminal.Skriv("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminal.Skriv("sync (연결된 JKSTORE1 Store_VALUE 장치에 Fil 보존)\n");
    }

    static void Prosess_VALUE_oppføring() {
        if (lengd_VALUE == 0) return;
        if (Kommando("help")) vise_hjelp();
        else if (Kommando("sync")) {
            int forretningsmål = 파일보존.synkronisere();
            SMS_Terminal.Skriv("Sync: "); SMS_Terminal.수쓰기(forretningsmål); SMS_Terminal.문자(10);
        }
        else if (Kommando("ls")) Minne_filsystem.oppføring_Liste();
        else if (Kommando("edit")) Minne_filsystem.Kommando(입력, 4, lengd_VALUE, 0);
        else if (Kommando("cat")) Minne_filsystem.Kommando(입력, 3, lengd_VALUE, 1);
        else if (Kommando("rm")) Minne_filsystem.Kommando(입력, 2, lengd_VALUE, 2);
        else if (Kommando("java") || Kommando("javac")) {
            int forretningsmål = 실행관리.Utfør_kommando(입력, 0, lengd_VALUE);
            SMS_Terminal.Skriv("Exit: "); SMS_Terminal.수쓰기(forretningsmål); SMS_Terminal.문자(10);
        }
        else if (Kommando("apps")) 실행관리.oppføring_Liste();
        else if (Kommando("net")) Nettverk_Stabel.status_VALUE();
        else if (Kommando("run")) {
            int forretningsmål = 실행관리.Utfør_kommando(입력, 3, lengd_VALUE);
            SMS_Terminal.Skriv("Exit: "); SMS_Terminal.수쓰기(forretningsmål); SMS_Terminal.Skriv("\n");
        } else if (Kommando("info")) {
            SMS_Terminal.Skriv("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Kommando("mem")) {
            SMS_Terminal.Skriv("위쪽 Minne_VALUE 공간(KiB): "); SMS_Terminal.수쓰기(기억공간.UPPER_Minne_endre_storleik());
            SMS_Terminal.Skriv("\n배열 동적 Minne_VALUE 공간(byte_VALUE): "); SMS_Terminal.수쓰기(mobil_VALUE.ARRAY_bruk());
            SMS_Terminal.Skriv(" / 262144\n작업 공간 del_VALUE: "); SMS_Terminal.수쓰기(기억공간.사용개수());
            SMS_Terminal.Skriv(" / 8 (각 4096바이트)\n");
        } else if (Kommando("alloc")) {
            int INDEX = 기억공간.tildele_Lagring();
            SMS_Terminal.Skriv("del_VALUE INDEX: "); SMS_Terminal.수쓰기(INDEX); SMS_Terminal.Skriv("\n");
        } else if (Kommando("free")) {
            if (lengd_VALUE == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Terminal.Skriv(기억공간.levere_tilbake_forretningsmål(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 del_VALUE\n");
            } else SMS_Terminal.Skriv("사용법: free 0..7\n");
        } else if (Kommando("echo")) {
            for (int INDEX = 5; INDEX < lengd_VALUE; INDEX++) SMS_Terminal.문자(입력[INDEX]);
            SMS_Terminal.문자(10);
        } else if (Kommando("clear")) SMS_Terminal.지우기();
        else if (Kommando("test")) kjerne.시험();
        else if (Kommando("halt")) {
            SMS_Terminal.Skriv("HALTED\n");
            mobil_VALUE.정지();
        } else SMS_Terminal.Skriv("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void godta_AND_skrive(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_Terminal.문자(10);
            if (Minne_filsystem.편집중) Minne_filsystem.Redigert_line(입력, lengd_VALUE, line_overflyt);
            else Prosess_VALUE_oppføring();
            lengd_VALUE = 0;
            line_overflyt = false;
            SMS_Terminal.Skriv(Minne_filsystem.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (lengd_VALUE > 0) {
                lengd_VALUE--;
                SMS_Terminal.직렬바이트(8); SMS_Terminal.직렬바이트(32); SMS_Terminal.직렬바이트(8);
                SMS_Terminal.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && lengd_VALUE < 입력.length) {
            입력[lengd_VALUE++] = VALUE;
            SMS_Terminal.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) line_overflyt = true;
    }

    static void Køyr_2() {
        vise_hjelp();
        SMS_Terminal.Skriv("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_Terminal.직렬읽기();
            if (VALUE < 0) VALUE = tastatur.Les();
            if (VALUE >= 0) godta_AND_skrive(VALUE);
            else { Nettverk_Stabel.stadfeste(); mobil_VALUE.잠시양보(); }
        }
    }
}
