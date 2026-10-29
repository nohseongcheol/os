// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Scríobh 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int fad_VALUE = 0;
    static boolean 앞줄복귀 = false;
    static boolean líne_róshreabhadh = false;

    static boolean Ordú(String Ainm) {
        if (fad_VALUE < Ainm.length()) return false;
        for (int INDEX = 0; INDEX < Ainm.length(); INDEX++)
            if (입력[INDEX] != Ainm.charAt(INDEX)) return false;
        return fad_VALUE == Ainm.length() || 입력[Ainm.length()] == ' ';
    }

    static void seó_cabhair() {
        SMS_Teirminéal.Scríobh("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Teirminéal.Scríobh("apps | run NAME [ARGS] | net\n");
        SMS_Teirminéal.Scríobh("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Teirminéal.Scríobh("sync (연결된 JKSTORE1 Store_VALUE 장치에 Comhad 보존)\n");
    }

    static void Próiseas_VALUE_iontráil() {
        if (fad_VALUE == 0) return;
        if (Ordú("help")) seó_cabhair();
        else if (Ordú("sync")) {
            int tomhas = 파일보존.sioncronaigh();
            SMS_Teirminéal.Scríobh("Sync: "); SMS_Teirminéal.수쓰기(tomhas); SMS_Teirminéal.문자(10);
        }
        else if (Ordú("ls")) Cuimhne_córas_comhad.iontráil_Liosta();
        else if (Ordú("edit")) Cuimhne_córas_comhad.Ordú(입력, 4, fad_VALUE, 0);
        else if (Ordú("cat")) Cuimhne_córas_comhad.Ordú(입력, 3, fad_VALUE, 1);
        else if (Ordú("rm")) Cuimhne_córas_comhad.Ordú(입력, 2, fad_VALUE, 2);
        else if (Ordú("java") || Ordú("javac")) {
            int tomhas = 실행관리.Rith_ordú(입력, 0, fad_VALUE);
            SMS_Teirminéal.Scríobh("Exit: "); SMS_Teirminéal.수쓰기(tomhas); SMS_Teirminéal.문자(10);
        }
        else if (Ordú("apps")) 실행관리.iontráil_Liosta();
        else if (Ordú("net")) Líonra_Cruach.staid_VALUE();
        else if (Ordú("run")) {
            int tomhas = 실행관리.Rith_ordú(입력, 3, fad_VALUE);
            SMS_Teirminéal.Scríobh("Exit: "); SMS_Teirminéal.수쓰기(tomhas); SMS_Teirminéal.Scríobh("\n");
        } else if (Ordú("info")) {
            SMS_Teirminéal.Scríobh("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Ordú("mem")) {
            SMS_Teirminéal.Scríobh("위쪽 Cuimhne_VALUE 공간(KiB): "); SMS_Teirminéal.수쓰기(기억공간.UPPER_Cuimhne_socraigh_méid());
            SMS_Teirminéal.Scríobh("\n배열 동적 Cuimhne_VALUE 공간(beart_VALUE): "); SMS_Teirminéal.수쓰기(gléas_VALUE.ARRAY_úsáid());
            SMS_Teirminéal.Scríobh(" / 262144\n작업 공간 rannán_VALUE: "); SMS_Teirminéal.수쓰기(기억공간.사용개수());
            SMS_Teirminéal.Scríobh(" / 8 (각 4096바이트)\n");
        } else if (Ordú("alloc")) {
            int INDEX = 기억공간.leithdháil_Stóras();
            SMS_Teirminéal.Scríobh("rannán_VALUE INDEX: "); SMS_Teirminéal.수쓰기(INDEX); SMS_Teirminéal.Scríobh("\n");
        } else if (Ordú("free")) {
            if (fad_VALUE == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Teirminéal.Scríobh(기억공간.return_tomhas(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 rannán_VALUE\n");
            } else SMS_Teirminéal.Scríobh("사용법: free 0..7\n");
        } else if (Ordú("echo")) {
            for (int INDEX = 5; INDEX < fad_VALUE; INDEX++) SMS_Teirminéal.문자(입력[INDEX]);
            SMS_Teirminéal.문자(10);
        } else if (Ordú("clear")) SMS_Teirminéal.지우기();
        else if (Ordú("test")) eithne.시험();
        else if (Ordú("halt")) {
            SMS_Teirminéal.Scríobh("HALTED\n");
            gléas_VALUE.정지();
        } else SMS_Teirminéal.Scríobh("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void glac_le_AND_scríobh(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_Teirminéal.문자(10);
            if (Cuimhne_córas_comhad.편집중) Cuimhne_córas_comhad.편집줄(입력, fad_VALUE, líne_róshreabhadh);
            else Próiseas_VALUE_iontráil();
            fad_VALUE = 0;
            líne_róshreabhadh = false;
            SMS_Teirminéal.Scríobh(Cuimhne_córas_comhad.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (fad_VALUE > 0) {
                fad_VALUE--;
                SMS_Teirminéal.직렬바이트(8); SMS_Teirminéal.직렬바이트(32); SMS_Teirminéal.직렬바이트(8);
                SMS_Teirminéal.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && fad_VALUE < 입력.length) {
            입력[fad_VALUE++] = VALUE;
            SMS_Teirminéal.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) líne_róshreabhadh = true;
    }

    static void Rith_2() {
        seó_cabhair();
        SMS_Teirminéal.Scríobh("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_Teirminéal.직렬읽기();
            if (VALUE < 0) VALUE = méarchlár.Léigh();
            if (VALUE >= 0) glac_le_AND_scríobh(VALUE);
            else { Líonra_Cruach.fíoraigh(); gléas_VALUE.잠시양보(); }
        }
    }
}
