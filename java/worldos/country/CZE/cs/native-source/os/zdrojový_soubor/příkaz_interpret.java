// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Zápis 없이 동작하는 작은 직렬/PS2 příkaz_interpret. */
public final class příkaz_interpret {
    static int[] vstup_HODNOTA = new int[128];
    static int délka_HODNOTA = 0;
    static boolean 앞줄복귀 = false;
    static boolean čára_přetečení = false;

    static boolean příkaz(String Název) {
        if (délka_HODNOTA < Název.length()) return false;
        for (int INDEX = 0; INDEX < Název.length(); INDEX++)
            if (vstup_HODNOTA[INDEX] != Název.charAt(INDEX)) return false;
        return délka_HODNOTA == Název.length() || vstup_HODNOTA[Název.length()] == ' ';
    }

    static void zobrazit_nápovědu() {
        SMS_Terminál.Zápis("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminál.Zápis("apps | run NAME [ARGS] | net\n");
        SMS_Terminál.Zápis("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminál.Zápis("sync (연결된 JKSTORE1 Store_HODNOTA 장치에 název_souboru 보존)\n");
    }

    static void Proces_HODNOTA_položka() {
        if (délka_HODNOTA == 0) return;
        if (příkaz("help")) zobrazit_nápovědu();
        else if (příkaz("sync")) {
            int VÝSLEDEK = 파일보존.synchronizovat();
            SMS_Terminál.Zápis("Sync: "); SMS_Terminál.zápis_číslo(VÝSLEDEK); SMS_Terminál.문자(10);
        }
        else if (příkaz("ls")) Paměť_systém_souborů.položka_Seznam();
        else if (příkaz("edit")) Paměť_systém_souborů.příkaz(vstup_HODNOTA, 4, délka_HODNOTA, 0);
        else if (příkaz("cat")) Paměť_systém_souborů.příkaz(vstup_HODNOTA, 3, délka_HODNOTA, 1);
        else if (příkaz("rm")) Paměť_systém_souborů.příkaz(vstup_HODNOTA, 2, délka_HODNOTA, 2);
        else if (příkaz("java") || příkaz("javac")) {
            int VÝSLEDEK = spuštění_Správce.Provést_příkaz(vstup_HODNOTA, 0, délka_HODNOTA);
            SMS_Terminál.Zápis("Exit: "); SMS_Terminál.zápis_číslo(VÝSLEDEK); SMS_Terminál.문자(10);
        }
        else if (příkaz("apps")) spuštění_Správce.položka_Seznam();
        else if (příkaz("net")) síť_Štos.Stav_HODNOTA();
        else if (příkaz("run")) {
            int VÝSLEDEK = spuštění_Správce.Provést_příkaz(vstup_HODNOTA, 3, délka_HODNOTA);
            SMS_Terminál.Zápis("Exit: "); SMS_Terminál.zápis_číslo(VÝSLEDEK); SMS_Terminál.Zápis("\n");
        } else if (příkaz("info")) {
            SMS_Terminál.Zápis("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (příkaz("mem")) {
            SMS_Terminál.Zápis("위쪽 Paměť_HODNOTA ODKAZ_oblast(KiB): "); SMS_Terminál.zápis_číslo(Paměť_oblast.VELKÁ_Paměť_změnit_velikost());
            SMS_Terminál.Zápis("\n배열 동적 Paměť_HODNOTA ODKAZ_oblast(bajt_HODNOTA): "); SMS_Terminál.zápis_číslo(mobilní_HODNOTA.pole_využití());
            SMS_Terminál.Zápis(" / 262144\n작업 ODKAZ_oblast oddíl_HODNOTA_366e0bfa: "); SMS_Terminál.zápis_číslo(Paměť_oblast.사용개수());
            SMS_Terminál.Zápis(" / 8 (각 4096바이트)\n");
        } else if (příkaz("alloc")) {
            int INDEX = Paměť_oblast.přidělit_Storage();
            SMS_Terminál.Zápis("oddíl_HODNOTA_366e0bfa INDEX: "); SMS_Terminál.zápis_číslo(INDEX); SMS_Terminál.Zápis("\n");
        } else if (příkaz("free")) {
            if (délka_HODNOTA == 6 && vstup_HODNOTA[4] == ' ' && vstup_HODNOTA[5] >= '0' && vstup_HODNOTA[5] <= '7') {
                SMS_Terminál.Zápis(Paměť_oblast.Vratka_KV(vstup_HODNOTA[5] - '0') ? "반환됨\n" : "할당되지 않은 oddíl_HODNOTA_366e0bfa\n");
            } else SMS_Terminál.Zápis("사용법: free 0..7\n");
        } else if (příkaz("echo")) {
            for (int INDEX = 5; INDEX < délka_HODNOTA; INDEX++) SMS_Terminál.문자(vstup_HODNOTA[INDEX]);
            SMS_Terminál.문자(10);
        } else if (příkaz("clear")) SMS_Terminál.vymazat_položka();
        else if (příkaz("test")) jádro.zkoušky();
        else if (příkaz("halt")) {
            SMS_Terminál.Zápis("HALTED\n");
            mobilní_HODNOTA.정지();
        } else SMS_Terminál.Zápis("알 číslo 없는 명령입니다. help를 입력하세요.\n");
    }

    static void přijmout_A_zápis(int HODNOTA) {
        if (HODNOTA == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = HODNOTA == 13;
        if (HODNOTA == 10 || HODNOTA == 13) {
            SMS_Terminál.문자(10);
            if (Paměť_systém_souborů.편집중) Paměť_systém_souborů.Upraveno_čára(vstup_HODNOTA, délka_HODNOTA, čára_přetečení);
            else Proces_HODNOTA_položka();
            délka_HODNOTA = 0;
            čára_přetečení = false;
            SMS_Terminál.Zápis(Paměť_systém_souborů.편집중 ? "...> " : "jkoros> ");
        } else if (HODNOTA == 8 || HODNOTA == 127) {
            if (délka_HODNOTA > 0) {
                délka_HODNOTA--;
                SMS_Terminál.직렬바이트(8); SMS_Terminál.직렬바이트(32); SMS_Terminál.직렬바이트(8);
                SMS_Terminál.화면문자(8);
            }
        } else if (HODNOTA >= 32 && HODNOTA < 127 && délka_HODNOTA < vstup_HODNOTA.length) {
            vstup_HODNOTA[délka_HODNOTA++] = HODNOTA;
            SMS_Terminál.문자(HODNOTA);
        } else if (HODNOTA >= 32 && HODNOTA < 127) čára_přetečení = true;
    }

    static void Spustit_2() {
        zobrazit_nápovědu();
        SMS_Terminál.Zápis("READY\njkoros> ");
        while (true) {
            int HODNOTA = SMS_Terminál.직렬읽기();
            if (HODNOTA < 0) HODNOTA = klávesnice.Čtení();
            if (HODNOTA >= 0) přijmout_A_zápis(HODNOTA);
            else { síť_Štos.ověřit(); mobilní_HODNOTA.잠시양보(); }
        }
    }
}
