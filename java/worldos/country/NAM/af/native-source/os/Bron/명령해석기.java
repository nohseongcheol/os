// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Skryf 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int lengte_VALUE = 0;
    static boolean 앞줄복귀 = false;
    static boolean lyn_oorloop = false;

    static boolean Opdrag(String Naam) {
        if (lengte_VALUE < Naam.length()) return false;
        for (int INDEX = 0; INDEX < Naam.length(); INDEX++)
            if (입력[INDEX] != Naam.charAt(INDEX)) return false;
        return lengte_VALUE == Naam.length() || 입력[Naam.length()] == ' ';
    }

    static void wys_hulp() {
        SMS_Terminaal.Skryf("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminaal.Skryf("apps | run NAME [ARGS] | net\n");
        SMS_Terminaal.Skryf("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminaal.Skryf("sync (연결된 JKSTORE1 bêre_VALUE 장치에 Lêer 보존)\n");
    }

    static void Proses_VALUE_inskrywing() {
        if (lengte_VALUE == 0) return;
        if (Opdrag("help")) wys_hulp();
        else if (Opdrag("sync")) {
            int maatreël = 파일보존.sinc();
            SMS_Terminaal.Skryf("Sync: "); SMS_Terminaal.수쓰기(maatreël); SMS_Terminaal.문자(10);
        }
        else if (Opdrag("ls")) Geheue_lêerstelsel.inskrywing_Lys();
        else if (Opdrag("edit")) Geheue_lêerstelsel.Opdrag(입력, 4, lengte_VALUE, 0);
        else if (Opdrag("cat")) Geheue_lêerstelsel.Opdrag(입력, 3, lengte_VALUE, 1);
        else if (Opdrag("rm")) Geheue_lêerstelsel.Opdrag(입력, 2, lengte_VALUE, 2);
        else if (Opdrag("java") || Opdrag("javac")) {
            int maatreël = 실행관리.uitvoer_bevel(입력, 0, lengte_VALUE);
            SMS_Terminaal.Skryf("Exit: "); SMS_Terminaal.수쓰기(maatreël); SMS_Terminaal.문자(10);
        }
        else if (Opdrag("apps")) 실행관리.inskrywing_Lys();
        else if (Opdrag("net")) Netwerk_Stapel.stand_VALUE();
        else if (Opdrag("run")) {
            int maatreël = 실행관리.uitvoer_bevel(입력, 3, lengte_VALUE);
            SMS_Terminaal.Skryf("Exit: "); SMS_Terminaal.수쓰기(maatreël); SMS_Terminaal.Skryf("\n");
        } else if (Opdrag("info")) {
            SMS_Terminaal.Skryf("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Opdrag("mem")) {
            SMS_Terminaal.Skryf("위쪽 Geheue_VALUE 공간(KiB): "); SMS_Terminaal.수쓰기(기억공간.UPPER_Geheue_verstel());
            SMS_Terminaal.Skryf("\n배열 동적 Geheue_VALUE 공간(greep_VALUE): "); SMS_Terminaal.수쓰기(mobiel_VALUE.배열사용량());
            SMS_Terminaal.Skryf(" / 262144\n작업 공간 seksie_VALUE: "); SMS_Terminaal.수쓰기(기억공간.사용개수());
            SMS_Terminaal.Skryf(" / 8 (각 4096바이트)\n");
        } else if (Opdrag("alloc")) {
            int INDEX = 기억공간.toewys_Berging();
            SMS_Terminaal.Skryf("seksie_VALUE INDEX: "); SMS_Terminaal.수쓰기(INDEX); SMS_Terminaal.Skryf("\n");
        } else if (Opdrag("free")) {
            if (lengte_VALUE == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Terminaal.Skryf(기억공간.teruggee_maatreël(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 seksie_VALUE\n");
            } else SMS_Terminaal.Skryf("사용법: free 0..7\n");
        } else if (Opdrag("echo")) {
            for (int INDEX = 5; INDEX < lengte_VALUE; INDEX++) SMS_Terminaal.문자(입력[INDEX]);
            SMS_Terminaal.문자(10);
        } else if (Opdrag("clear")) SMS_Terminaal.vee_uit_inskrywing();
        else if (Opdrag("test")) kern.시험();
        else if (Opdrag("halt")) {
            SMS_Terminaal.Skryf("HALTED\n");
            mobiel_VALUE.정지();
        } else SMS_Terminaal.Skryf("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void aanvaar_AND_skryf(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_Terminaal.문자(10);
            if (Geheue_lêerstelsel.편집중) Geheue_lêerstelsel.편집줄(입력, lengte_VALUE, lyn_oorloop);
            else Proses_VALUE_inskrywing();
            lengte_VALUE = 0;
            lyn_oorloop = false;
            SMS_Terminaal.Skryf(Geheue_lêerstelsel.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (lengte_VALUE > 0) {
                lengte_VALUE--;
                SMS_Terminaal.직렬바이트(8); SMS_Terminaal.직렬바이트(32); SMS_Terminaal.직렬바이트(8);
                SMS_Terminaal.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && lengte_VALUE < 입력.length) {
            입력[lengte_VALUE++] = VALUE;
            SMS_Terminaal.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) lyn_oorloop = true;
    }

    static void Loop() {
        wys_hulp();
        SMS_Terminaal.Skryf("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_Terminaal.직렬읽기();
            if (VALUE < 0) VALUE = sleutelbord.Lees();
            if (VALUE >= 0) aanvaar_AND_skryf(VALUE);
            else { Netwerk_Stapel.verifieer(); mobiel_VALUE.잠시양보(); }
        }
    }
}
