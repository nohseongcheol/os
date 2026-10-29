// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Shkrimi 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int gjatësi_VALUE = 0;
    static boolean 앞줄복귀 = false;
    static boolean linjë_tejkalim = false;

    static boolean Komanda(String Emër) {
        if (gjatësi_VALUE < Emër.length()) return false;
        for (int INDEX = 0; INDEX < Emër.length(); INDEX++)
            if (입력[INDEX] != Emër.charAt(INDEX)) return false;
        return gjatësi_VALUE == Emër.length() || 입력[Emër.length()] == ' ';
    }

    static void shfaq_ndihmë() {
        SMS_Terminali.Shkrimi("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminali.Shkrimi("apps | run NAME [ARGS] | net\n");
        SMS_Terminali.Shkrimi("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminali.Shkrimi("sync (연결된 JKSTORE1 Store_VALUE 장치에 Kartelë 보존)\n");
    }

    static void Proces_VALUE_futje() {
        if (gjatësi_VALUE == 0) return;
        if (Komanda("help")) shfaq_ndihmë();
        else if (Komanda("sync")) {
            int llogaritje = 파일보존.sinkronizoj();
            SMS_Terminali.Shkrimi("Sync: "); SMS_Terminali.수쓰기(llogaritje); SMS_Terminali.문자(10);
        }
        else if (Komanda("ls")) Memorie_sistemi_i_skedarëve.futje_Listë();
        else if (Komanda("edit")) Memorie_sistemi_i_skedarëve.Komanda(입력, 4, gjatësi_VALUE, 0);
        else if (Komanda("cat")) Memorie_sistemi_i_skedarëve.Komanda(입력, 3, gjatësi_VALUE, 1);
        else if (Komanda("rm")) Memorie_sistemi_i_skedarëve.Komanda(입력, 2, gjatësi_VALUE, 2);
        else if (Komanda("java") || Komanda("javac")) {
            int llogaritje = 실행관리.zbatoj_komandë(입력, 0, gjatësi_VALUE);
            SMS_Terminali.Shkrimi("Exit: "); SMS_Terminali.수쓰기(llogaritje); SMS_Terminali.문자(10);
        }
        else if (Komanda("apps")) 실행관리.futje_Listë();
        else if (Komanda("net")) rrjet_Stivë.status_VALUE();
        else if (Komanda("run")) {
            int llogaritje = 실행관리.zbatoj_komandë(입력, 3, gjatësi_VALUE);
            SMS_Terminali.Shkrimi("Exit: "); SMS_Terminali.수쓰기(llogaritje); SMS_Terminali.Shkrimi("\n");
        } else if (Komanda("info")) {
            SMS_Terminali.Shkrimi("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Komanda("mem")) {
            SMS_Terminali.Shkrimi("위쪽 Memorie_VALUE 공간(KiB): "); SMS_Terminali.수쓰기(기억공간.UPPER_Memorie_ndryshoj_përmasat());
            SMS_Terminali.Shkrimi("\n배열 동적 Memorie_VALUE 공간(bajt_VALUE): "); SMS_Terminali.수쓰기(pajisje_VALUE.ARRAY_përdorim());
            SMS_Terminali.Shkrimi(" / 262144\n작업 공간 seksion_VALUE: "); SMS_Terminali.수쓰기(기억공간.사용개수());
            SMS_Terminali.Shkrimi(" / 8 (각 4096바이트)\n");
        } else if (Komanda("alloc")) {
            int INDEX = 기억공간.caktoj_hapësira_ruajtëse();
            SMS_Terminali.Shkrimi("seksion_VALUE INDEX: "); SMS_Terminali.수쓰기(INDEX); SMS_Terminali.Shkrimi("\n");
        } else if (Komanda("free")) {
            if (gjatësi_VALUE == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Terminali.Shkrimi(기억공간.Kthe_llogaritje(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 seksion_VALUE\n");
            } else SMS_Terminali.Shkrimi("사용법: free 0..7\n");
        } else if (Komanda("echo")) {
            for (int INDEX = 5; INDEX < gjatësi_VALUE; INDEX++) SMS_Terminali.문자(입력[INDEX]);
            SMS_Terminali.문자(10);
        } else if (Komanda("clear")) SMS_Terminali.spastroj_futje();
        else if (Komanda("test")) bërthamë.시험();
        else if (Komanda("halt")) {
            SMS_Terminali.Shkrimi("HALTED\n");
            pajisje_VALUE.정지();
        } else SMS_Terminali.Shkrimi("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void prano_AND_shkruaj(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_Terminali.문자(10);
            if (Memorie_sistemi_i_skedarëve.편집중) Memorie_sistemi_i_skedarëve.편집줄(입력, gjatësi_VALUE, linjë_tejkalim);
            else Proces_VALUE_futje();
            gjatësi_VALUE = 0;
            linjë_tejkalim = false;
            SMS_Terminali.Shkrimi(Memorie_sistemi_i_skedarëve.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (gjatësi_VALUE > 0) {
                gjatësi_VALUE--;
                SMS_Terminali.직렬바이트(8); SMS_Terminali.직렬바이트(32); SMS_Terminali.직렬바이트(8);
                SMS_Terminali.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && gjatësi_VALUE < 입력.length) {
            입력[gjatësi_VALUE++] = VALUE;
            SMS_Terminali.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) linjë_tejkalim = true;
    }

    static void Ekzekuto() {
        shfaq_ndihmë();
        SMS_Terminali.Shkrimi("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_Terminali.직렬읽기();
            if (VALUE < 0) VALUE = tastiera.Leximi();
            if (VALUE >= 0) prano_AND_shkruaj(VALUE);
            else { rrjet_Stivë.verifikoj(); pajisje_VALUE.잠시양보(); }
        }
    }
}
