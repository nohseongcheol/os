// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 schreiwen 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int Längt_VALUE = 0;
    static boolean 앞줄복귀 = false;
    static boolean Zeil_Iwwerlaf = false;

    static boolean Befeel(String Numm) {
        if (Längt_VALUE < Numm.length()) return false;
        for (int INDEX = 0; INDEX < Numm.length(); INDEX++)
            if (입력[INDEX] != Numm.charAt(INDEX)) return false;
        return Längt_VALUE == Numm.length() || 입력[Numm.length()] == ' ';
    }

    static void Show_Hëllef() {
        SMS_Terminal.schreiwen("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminal.schreiwen("apps | run NAME [ARGS] | net\n");
        SMS_Terminal.schreiwen("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminal.schreiwen("sync (연결된 JKSTORE1 Store_VALUE 장치에 Fichier 보존)\n");
    }

    static void Prozess_VALUE_Agab() {
        if (Längt_VALUE == 0) return;
        if (Befeel("help")) Show_Hëllef();
        else if (Befeel("sync")) {
            int Mooss = 파일보존.synchroniséieren();
            SMS_Terminal.schreiwen("Sync: "); SMS_Terminal.수쓰기(Mooss); SMS_Terminal.문자(10);
        }
        else if (Befeel("ls")) Späicher_Fichierssystem.Agab_Lëscht();
        else if (Befeel("edit")) Späicher_Fichierssystem.Befeel(입력, 4, Längt_VALUE, 0);
        else if (Befeel("cat")) Späicher_Fichierssystem.Befeel(입력, 3, Längt_VALUE, 1);
        else if (Befeel("rm")) Späicher_Fichierssystem.Befeel(입력, 2, Längt_VALUE, 2);
        else if (Befeel("java") || Befeel("javac")) {
            int Mooss = 실행관리.ausféieren_Befeel(입력, 0, Längt_VALUE);
            SMS_Terminal.schreiwen("Exit: "); SMS_Terminal.수쓰기(Mooss); SMS_Terminal.문자(10);
        }
        else if (Befeel("apps")) 실행관리.Agab_Lëscht();
        else if (Befeel("net")) Reseau_Stapel.Status_VALUE();
        else if (Befeel("run")) {
            int Mooss = 실행관리.ausféieren_Befeel(입력, 3, Längt_VALUE);
            SMS_Terminal.schreiwen("Exit: "); SMS_Terminal.수쓰기(Mooss); SMS_Terminal.schreiwen("\n");
        } else if (Befeel("info")) {
            SMS_Terminal.schreiwen("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Befeel("mem")) {
            SMS_Terminal.schreiwen("위쪽 Späicher_VALUE 공간(KiB): "); SMS_Terminal.수쓰기(기억공간.UPPER_Späicher_d_Gréisst_veränneren());
            SMS_Terminal.schreiwen("\n배열 동적 Späicher_VALUE 공간(Byte_VALUE): "); SMS_Terminal.수쓰기(Mobil_VALUE.ARRAY_Usage());
            SMS_Terminal.schreiwen(" / 262144\n작업 공간 Beräich_VALUE: "); SMS_Terminal.수쓰기(기억공간.사용개수());
            SMS_Terminal.schreiwen(" / 8 (각 4096바이트)\n");
        } else if (Befeel("alloc")) {
            int INDEX = 기억공간.zouweisen_Späicher();
            SMS_Terminal.schreiwen("Beräich_VALUE INDEX: "); SMS_Terminal.수쓰기(INDEX); SMS_Terminal.schreiwen("\n");
        } else if (Befeel("free")) {
            if (Längt_VALUE == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Terminal.schreiwen(기억공간.반환(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 Beräich_VALUE\n");
            } else SMS_Terminal.schreiwen("사용법: free 0..7\n");
        } else if (Befeel("echo")) {
            for (int INDEX = 5; INDEX < Längt_VALUE; INDEX++) SMS_Terminal.문자(입력[INDEX]);
            SMS_Terminal.문자(10);
        } else if (Befeel("clear")) SMS_Terminal.지우기();
        else if (Befeel("test")) Kernel.시험();
        else if (Befeel("halt")) {
            SMS_Terminal.schreiwen("HALTED\n");
            Mobil_VALUE.정지();
        } else SMS_Terminal.schreiwen("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void acceptéieren_AND_schreiwen(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_Terminal.문자(10);
            if (Späicher_Fichierssystem.편집중) Späicher_Fichierssystem.편집줄(입력, Längt_VALUE, Zeil_Iwwerlaf);
            else Prozess_VALUE_Agab();
            Längt_VALUE = 0;
            Zeil_Iwwerlaf = false;
            SMS_Terminal.schreiwen(Späicher_Fichierssystem.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (Längt_VALUE > 0) {
                Längt_VALUE--;
                SMS_Terminal.직렬바이트(8); SMS_Terminal.직렬바이트(32); SMS_Terminal.직렬바이트(8);
                SMS_Terminal.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && Längt_VALUE < 입력.length) {
            입력[Längt_VALUE++] = VALUE;
            SMS_Terminal.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) Zeil_Iwwerlaf = true;
    }

    static void Laf() {
        Show_Hëllef();
        SMS_Terminal.schreiwen("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_Terminal.직렬읽기();
            if (VALUE < 0) VALUE = Tastatur.읽기();
            if (VALUE >= 0) acceptéieren_AND_schreiwen(VALUE);
            else { Reseau_Stapel.verifizéieren(); Mobil_VALUE.잠시양보(); }
        }
    }
}
