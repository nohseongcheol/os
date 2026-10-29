// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Zápis 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] vstup_VALUE = new int[128];
    static int dĺžka_VALUE = 0;
    static boolean 앞줄복귀 = false;
    static boolean linka_pretečenie = false;

    static boolean Príkaz(String Názov) {
        if (dĺžka_VALUE < Názov.length()) return false;
        for (int INDEX = 0; INDEX < Názov.length(); INDEX++)
            if (vstup_VALUE[INDEX] != Názov.charAt(INDEX)) return false;
        return dĺžka_VALUE == Názov.length() || vstup_VALUE[Názov.length()] == ' ';
    }

    static void zobraziť_Pomocník() {
        SMS_Terminál.Zápis("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminál.Zápis("apps | run NAME [ARGS] | net\n");
        SMS_Terminál.Zápis("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminál.Zápis("sync (연결된 JKSTORE1 Store_VALUE 장치에 Súbor 보존)\n");
    }

    static void Proces_VALUE_položka() {
        if (dĺžka_VALUE == 0) return;
        if (Príkaz("help")) zobraziť_Pomocník();
        else if (Príkaz("sync")) {
            int KR = 파일보존.synchronizovať();
            SMS_Terminál.Zápis("Sync: "); SMS_Terminál.수쓰기(KR); SMS_Terminál.문자(10);
        }
        else if (Príkaz("ls")) Pamäť_systém_súborov.položka_Zoznam();
        else if (Príkaz("edit")) Pamäť_systém_súborov.Príkaz(vstup_VALUE, 4, dĺžka_VALUE, 0);
        else if (Príkaz("cat")) Pamäť_systém_súborov.Príkaz(vstup_VALUE, 3, dĺžka_VALUE, 1);
        else if (Príkaz("rm")) Pamäť_systém_súborov.Príkaz(vstup_VALUE, 2, dĺžka_VALUE, 2);
        else if (Príkaz("java") || Príkaz("javac")) {
            int KR = 실행관리.Vykonať_príkaz(vstup_VALUE, 0, dĺžka_VALUE);
            SMS_Terminál.Zápis("Exit: "); SMS_Terminál.수쓰기(KR); SMS_Terminál.문자(10);
        }
        else if (Príkaz("apps")) 실행관리.položka_Zoznam();
        else if (Príkaz("net")) sieť_Vrstvy.Stav_VALUE();
        else if (Príkaz("run")) {
            int KR = 실행관리.Vykonať_príkaz(vstup_VALUE, 3, dĺžka_VALUE);
            SMS_Terminál.Zápis("Exit: "); SMS_Terminál.수쓰기(KR); SMS_Terminál.Zápis("\n");
        } else if (Príkaz("info")) {
            SMS_Terminál.Zápis("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Príkaz("mem")) {
            SMS_Terminál.Zápis("위쪽 Pamäť_VALUE adresa_oblasť(KiB): "); SMS_Terminál.수쓰기(Pamäť_oblasť.UPPER_Pamäť_zmeniť_veľkosť());
            SMS_Terminál.Zápis("\n배열 동적 Pamäť_VALUE adresa_oblasť(Byte_VALUE): "); SMS_Terminál.수쓰기(telefón_VALUE.pole_použitie());
            SMS_Terminál.Zápis(" / 262144\n작업 adresa_oblasť sekcia_VALUE: "); SMS_Terminál.수쓰기(Pamäť_oblasť.사용개수());
            SMS_Terminál.Zápis(" / 8 (각 4096바이트)\n");
        } else if (Príkaz("alloc")) {
            int INDEX = Pamäť_oblasť.vyhradiť_Úložisko();
            SMS_Terminál.Zápis("sekcia_VALUE INDEX: "); SMS_Terminál.수쓰기(INDEX); SMS_Terminál.Zápis("\n");
        } else if (Príkaz("free")) {
            if (dĺžka_VALUE == 6 && vstup_VALUE[4] == ' ' && vstup_VALUE[5] >= '0' && vstup_VALUE[5] <= '7') {
                SMS_Terminál.Zápis(Pamäť_oblasť.vrátiť_KR(vstup_VALUE[5] - '0') ? "반환됨\n" : "할당되지 않은 sekcia_VALUE\n");
            } else SMS_Terminál.Zápis("사용법: free 0..7\n");
        } else if (Príkaz("echo")) {
            for (int INDEX = 5; INDEX < dĺžka_VALUE; INDEX++) SMS_Terminál.문자(vstup_VALUE[INDEX]);
            SMS_Terminál.문자(10);
        } else if (Príkaz("clear")) SMS_Terminál.vymazať_položka();
        else if (Príkaz("test")) jadro.시험();
        else if (Príkaz("halt")) {
            SMS_Terminál.Zápis("HALTED\n");
            telefón_VALUE.정지();
        } else SMS_Terminál.Zápis("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void prijať_AND_zapísať(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_Terminál.문자(10);
            if (Pamäť_systém_súborov.편집중) Pamäť_systém_súborov.Upravené_linka(vstup_VALUE, dĺžka_VALUE, linka_pretečenie);
            else Proces_VALUE_položka();
            dĺžka_VALUE = 0;
            linka_pretečenie = false;
            SMS_Terminál.Zápis(Pamäť_systém_súborov.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (dĺžka_VALUE > 0) {
                dĺžka_VALUE--;
                SMS_Terminál.직렬바이트(8); SMS_Terminál.직렬바이트(32); SMS_Terminál.직렬바이트(8);
                SMS_Terminál.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && dĺžka_VALUE < vstup_VALUE.length) {
            vstup_VALUE[dĺžka_VALUE++] = VALUE;
            SMS_Terminál.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) linka_pretečenie = true;
    }

    static void Spustiť_2() {
        zobraziť_Pomocník();
        SMS_Terminál.Zápis("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_Terminál.직렬읽기();
            if (VALUE < 0) VALUE = klávesnica.Čítanie();
            if (VALUE >= 0) prijať_AND_zapísať(VALUE);
            else { sieť_Vrstvy.overiť(); telefón_VALUE.잠시양보(); }
        }
    }
}
