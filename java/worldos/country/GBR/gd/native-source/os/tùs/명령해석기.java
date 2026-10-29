// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 sgrìobh 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int faid_VALUE = 0;
    static boolean 앞줄복귀 = false;
    static boolean loidhne_taomadh = false;

    static boolean àithne(String Ainm) {
        if (faid_VALUE < Ainm.length()) return false;
        for (int INDEX = 0; INDEX < Ainm.length(); INDEX++)
            if (입력[INDEX] != Ainm.charAt(INDEX)) return false;
        return faid_VALUE == Ainm.length() || 입력[Ainm.length()] == ' ';
    }

    static void show_cuideachadh() {
        SMS_tèirmineal.sgrìobh("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_tèirmineal.sgrìobh("apps | run NAME [ARGS] | net\n");
        SMS_tèirmineal.sgrìobh("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_tèirmineal.sgrìobh("sync (연결된 JKSTORE1 Store_VALUE 장치에 faidhle 보존)\n");
    }

    static void Pròiseas_VALUE_cur_a_steach() {
        if (faid_VALUE == 0) return;
        if (àithne("help")) show_cuideachadh();
        else if (àithne("sync")) {
            int tomhas = 파일보존.sioncronaich();
            SMS_tèirmineal.sgrìobh("Sync: "); SMS_tèirmineal.수쓰기(tomhas); SMS_tèirmineal.문자(10);
        }
        else if (àithne("ls")) cuimhne_siostam_fhaidhlichean.cur_a_steach_Liosta();
        else if (àithne("edit")) cuimhne_siostam_fhaidhlichean.àithne(입력, 4, faid_VALUE, 0);
        else if (àithne("cat")) cuimhne_siostam_fhaidhlichean.àithne(입력, 3, faid_VALUE, 1);
        else if (àithne("rm")) cuimhne_siostam_fhaidhlichean.àithne(입력, 2, faid_VALUE, 2);
        else if (àithne("java") || àithne("javac")) {
            int tomhas = 실행관리.gnìomhaich_àithne(입력, 0, faid_VALUE);
            SMS_tèirmineal.sgrìobh("Exit: "); SMS_tèirmineal.수쓰기(tomhas); SMS_tèirmineal.문자(10);
        }
        else if (àithne("apps")) 실행관리.cur_a_steach_Liosta();
        else if (àithne("net")) lìonra_stac.cor_VALUE();
        else if (àithne("run")) {
            int tomhas = 실행관리.gnìomhaich_àithne(입력, 3, faid_VALUE);
            SMS_tèirmineal.sgrìobh("Exit: "); SMS_tèirmineal.수쓰기(tomhas); SMS_tèirmineal.sgrìobh("\n");
        } else if (àithne("info")) {
            SMS_tèirmineal.sgrìobh("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (àithne("mem")) {
            SMS_tèirmineal.sgrìobh("위쪽 cuimhne_VALUE 공간(KiB): "); SMS_tèirmineal.수쓰기(기억공간.UPPER_cuimhne_atharraich_am_meud());
            SMS_tèirmineal.sgrìobh("\n배열 동적 cuimhne_VALUE 공간(baidht_VALUE): "); SMS_tèirmineal.수쓰기(uidheam_VALUE.배열사용량());
            SMS_tèirmineal.sgrìobh(" / 262144\n작업 공간 earrann_VALUE: "); SMS_tèirmineal.수쓰기(기억공간.사용개수());
            SMS_tèirmineal.sgrìobh(" / 8 (각 4096바이트)\n");
        } else if (àithne("alloc")) {
            int INDEX = 기억공간.sònraich_stòras();
            SMS_tèirmineal.sgrìobh("earrann_VALUE INDEX: "); SMS_tèirmineal.수쓰기(INDEX); SMS_tèirmineal.sgrìobh("\n");
        } else if (àithne("free")) {
            if (faid_VALUE == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_tèirmineal.sgrìobh(기억공간.return_tomhas(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 earrann_VALUE\n");
            } else SMS_tèirmineal.sgrìobh("사용법: free 0..7\n");
        } else if (àithne("echo")) {
            for (int INDEX = 5; INDEX < faid_VALUE; INDEX++) SMS_tèirmineal.문자(입력[INDEX]);
            SMS_tèirmineal.문자(10);
        } else if (àithne("clear")) SMS_tèirmineal.지우기();
        else if (àithne("test")) eitean.시험();
        else if (àithne("halt")) {
            SMS_tèirmineal.sgrìobh("HALTED\n");
            uidheam_VALUE.정지();
        } else SMS_tèirmineal.sgrìobh("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void gabh_ris_AND_sgrìobh(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_tèirmineal.문자(10);
            if (cuimhne_siostam_fhaidhlichean.편집중) cuimhne_siostam_fhaidhlichean.편집줄(입력, faid_VALUE, loidhne_taomadh);
            else Pròiseas_VALUE_cur_a_steach();
            faid_VALUE = 0;
            loidhne_taomadh = false;
            SMS_tèirmineal.sgrìobh(cuimhne_siostam_fhaidhlichean.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (faid_VALUE > 0) {
                faid_VALUE--;
                SMS_tèirmineal.직렬바이트(8); SMS_tèirmineal.직렬바이트(32); SMS_tèirmineal.직렬바이트(8);
                SMS_tèirmineal.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && faid_VALUE < 입력.length) {
            입력[faid_VALUE++] = VALUE;
            SMS_tèirmineal.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) loidhne_taomadh = true;
    }

    static void ruith() {
        show_cuideachadh();
        SMS_tèirmineal.sgrìobh("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_tèirmineal.직렬읽기();
            if (VALUE < 0) VALUE = meur_chlàr.읽기();
            if (VALUE >= 0) gabh_ris_AND_sgrìobh(VALUE);
            else { lìonra_stac.dearbh(); uidheam_VALUE.잠시양보(); }
        }
    }
}
