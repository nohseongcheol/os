// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Kirjutamine 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int 길이 = 0;
    static boolean 앞줄복귀 = false;
    static boolean liin_ületäide = false;

    static boolean Käsk(String Nimi_2) {
        if (길이 < Nimi_2.length()) return false;
        for (int INDEX = 0; INDEX < Nimi_2.length(); INDEX++)
            if (입력[INDEX] != Nimi_2.charAt(INDEX)) return false;
        return 길이 == Nimi_2.length() || 입력[Nimi_2.length()] == ' ';
    }

    static void saade_spikker() {
        SMS_terminal.Kirjutamine("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_terminal.Kirjutamine("apps | run NAME [ARGS] | net\n");
        SMS_terminal.Kirjutamine("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_terminal.Kirjutamine("sync (연결된 JKSTORE1 salv_VALUE 장치에 Fail 보존)\n");
    }

    static void Joonis_VALUE_kirje() {
        if (길이 == 0) return;
        if (Käsk("help")) saade_spikker();
        else if (Käsk("sync")) {
            int TULEMUS = 파일보존.sünkroonima();
            SMS_terminal.Kirjutamine("Sync: "); SMS_terminal.kirjutamine_number(TULEMUS); SMS_terminal.문자(10);
        }
        else if (Käsk("ls")) Mälu_failisüsteem.kirje_Loend();
        else if (Käsk("edit")) Mälu_failisüsteem.Käsk(입력, 4, 길이, 0);
        else if (Käsk("cat")) Mälu_failisüsteem.Käsk(입력, 3, 길이, 1);
        else if (Käsk("rm")) Mälu_failisüsteem.Käsk(입력, 2, 길이, 2);
        else if (Käsk("java") || Käsk("javac")) {
            int TULEMUS = 실행관리.Täida_käsk(입력, 0, 길이);
            SMS_terminal.Kirjutamine("Exit: "); SMS_terminal.kirjutamine_number(TULEMUS); SMS_terminal.문자(10);
        }
        else if (Käsk("apps")) 실행관리.kirje_Loend();
        else if (Käsk("net")) võrk_Virn.Olek_VALUE();
        else if (Käsk("run")) {
            int TULEMUS = 실행관리.Täida_käsk(입력, 3, 길이);
            SMS_terminal.Kirjutamine("Exit: "); SMS_terminal.kirjutamine_number(TULEMUS); SMS_terminal.Kirjutamine("\n");
        } else if (Käsk("info")) {
            SMS_terminal.Kirjutamine("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Käsk("mem")) {
            SMS_terminal.Kirjutamine("위쪽 Mälu_VALUE ADDRESS_regioon(KiB): "); SMS_terminal.kirjutamine_number(Mälu_regioon.UPPER_Mälu_suurust_muutma());
            SMS_terminal.Kirjutamine("\n배열 동적 Mälu_VALUE ADDRESS_regioon(bait_VALUE): "); SMS_terminal.kirjutamine_number(seade_VALUE.ARRAY_kasutus());
            SMS_terminal.Kirjutamine(" / 262144\n작업 ADDRESS_regioon jaotis_VALUE: "); SMS_terminal.kirjutamine_number(Mälu_regioon.사용개수());
            SMS_terminal.Kirjutamine(" / 8 (각 4096바이트)\n");
        } else if (Käsk("alloc")) {
            int INDEX = Mälu_regioon.lisama_salvesti();
            SMS_terminal.Kirjutamine("jaotis_VALUE INDEX: "); SMS_terminal.kirjutamine_number(INDEX); SMS_terminal.Kirjutamine("\n");
        } else if (Käsk("free")) {
            if (길이 == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_terminal.Kirjutamine(Mälu_regioon.tagasi_saatma_näitaja(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 jaotis_VALUE\n");
            } else SMS_terminal.Kirjutamine("사용법: free 0..7\n");
        } else if (Käsk("echo")) {
            for (int INDEX = 5; INDEX < 길이; INDEX++) SMS_terminal.문자(입력[INDEX]);
            SMS_terminal.문자(10);
        } else if (Käsk("clear")) SMS_terminal.kustutama_kirje();
        else if (Käsk("test")) tuum.시험();
        else if (Käsk("halt")) {
            SMS_terminal.Kirjutamine("HALTED\n");
            seade_VALUE.정지();
        } else SMS_terminal.Kirjutamine("알 number 없는 명령입니다. help를 입력하세요.\n");
    }

    static void aktsepteerima_AND_kirjutamine(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_terminal.문자(10);
            if (Mälu_failisüsteem.편집중) Mälu_failisüsteem.Redigeeritud_liin(입력, 길이, liin_ületäide);
            else Joonis_VALUE_kirje();
            길이 = 0;
            liin_ületäide = false;
            SMS_terminal.Kirjutamine(Mälu_failisüsteem.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (길이 > 0) {
                길이--;
                SMS_terminal.직렬바이트(8); SMS_terminal.직렬바이트(32); SMS_terminal.직렬바이트(8);
                SMS_terminal.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && 길이 < 입력.length) {
            입력[길이++] = VALUE;
            SMS_terminal.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) liin_ületäide = true;
    }

    static void Käivita_2() {
        saade_spikker();
        SMS_terminal.Kirjutamine("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_terminal.직렬읽기();
            if (VALUE < 0) VALUE = klaviatuur.Lugemine();
            if (VALUE >= 0) aktsepteerima_AND_kirjutamine(VALUE);
            else { võrk_Virn.kinnitama(); seade_VALUE.잠시양보(); }
        }
    }
}
