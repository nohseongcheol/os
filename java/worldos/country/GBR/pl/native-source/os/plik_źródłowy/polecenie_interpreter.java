// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Zapis 없이 동작하는 작은 직렬/PS2 polecenie_interpreter. */
public final class polecenie_interpreter {
    static int[] wejście_WARTOŚĆ = new int[128];
    static int długość_WARTOŚĆ = 0;
    static boolean 앞줄복귀 = false;
    static boolean linia_przepełnienie = false;

    static boolean polecenie(String Nazwa) {
        if (długość_WARTOŚĆ < Nazwa.length()) return false;
        for (int INDEKS = 0; INDEKS < Nazwa.length(); INDEKS++)
            if (wejście_WARTOŚĆ[INDEKS] != Nazwa.charAt(INDEKS)) return false;
        return długość_WARTOŚĆ == Nazwa.length() || wejście_WARTOŚĆ[Nazwa.length()] == ' ';
    }

    static void pokaż_pomoc() {
        SMS_Terminal.Zapis("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminal.Zapis("apps | run NAME [ARGS] | net\n");
        SMS_Terminal.Zapis("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminal.Zapis("sync (연결된 JKSTORE1 Store_WARTOŚĆ 장치에 nazwa_pliku 보존)\n");
    }

    static void Proces_WARTOŚĆ_wpis() {
        if (długość_WARTOŚĆ == 0) return;
        if (polecenie("help")) pokaż_pomoc();
        else if (polecenie("sync")) {
            int WYNIK = 파일보존.synchronizować();
            SMS_Terminal.Zapis("Sync: "); SMS_Terminal.zapis_identyfikator(WYNIK); SMS_Terminal.문자(10);
        }
        else if (polecenie("ls")) Pamięć_system_plików.wpis_Lista();
        else if (polecenie("edit")) Pamięć_system_plików.polecenie(wejście_WARTOŚĆ, 4, długość_WARTOŚĆ, 0);
        else if (polecenie("cat")) Pamięć_system_plików.polecenie(wejście_WARTOŚĆ, 3, długość_WARTOŚĆ, 1);
        else if (polecenie("rm")) Pamięć_system_plików.polecenie(wejście_WARTOŚĆ, 2, długość_WARTOŚĆ, 2);
        else if (polecenie("java") || polecenie("javac")) {
            int WYNIK = wykonanie_Menedżer.Wykonaj_polecenie(wejście_WARTOŚĆ, 0, długość_WARTOŚĆ);
            SMS_Terminal.Zapis("Exit: "); SMS_Terminal.zapis_identyfikator(WYNIK); SMS_Terminal.문자(10);
        }
        else if (polecenie("apps")) wykonanie_Menedżer.wpis_Lista();
        else if (polecenie("net")) sieć_Stos.Stan_WARTOŚĆ();
        else if (polecenie("run")) {
            int WYNIK = wykonanie_Menedżer.Wykonaj_polecenie(wejście_WARTOŚĆ, 3, długość_WARTOŚĆ);
            SMS_Terminal.Zapis("Exit: "); SMS_Terminal.zapis_identyfikator(WYNIK); SMS_Terminal.Zapis("\n");
        } else if (polecenie("info")) {
            SMS_Terminal.Zapis("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (polecenie("mem")) {
            SMS_Terminal.Zapis("위쪽 Pamięć_WARTOŚĆ ADRES_region(KiB): "); SMS_Terminal.zapis_identyfikator(Pamięć_region.LITERY_WIELKIE_Pamięć_zmienić_rozmiar());
            SMS_Terminal.Zapis("\n배열 동적 Pamięć_WARTOŚĆ ADRES_region(bajt_WARTOŚĆ): "); SMS_Terminal.zapis_identyfikator(urządzenie_WARTOŚĆ.TABLICA_użycie());
            SMS_Terminal.Zapis(" / 262144\n작업 ADRES_region obszar_WARTOŚĆ_366e0bfa: "); SMS_Terminal.zapis_identyfikator(Pamięć_region.사용개수());
            SMS_Terminal.Zapis(" / 8 (각 4096바이트)\n");
        } else if (polecenie("alloc")) {
            int INDEKS = Pamięć_region.przydzielić_Pamięć();
            SMS_Terminal.Zapis("obszar_WARTOŚĆ_366e0bfa INDEKS: "); SMS_Terminal.zapis_identyfikator(INDEKS); SMS_Terminal.Zapis("\n");
        } else if (polecenie("free")) {
            if (długość_WARTOŚĆ == 6 && wejście_WARTOŚĆ[4] == ' ' && wejście_WARTOŚĆ[5] >= '0' && wejście_WARTOŚĆ[5] <= '7') {
                SMS_Terminal.Zapis(Pamięć_region.Zwrot_KR(wejście_WARTOŚĆ[5] - '0') ? "반환됨\n" : "할당되지 않은 obszar_WARTOŚĆ_366e0bfa\n");
            } else SMS_Terminal.Zapis("사용법: free 0..7\n");
        } else if (polecenie("echo")) {
            for (int INDEKS = 5; INDEKS < długość_WARTOŚĆ; INDEKS++) SMS_Terminal.문자(wejście_WARTOŚĆ[INDEKS]);
            SMS_Terminal.문자(10);
        } else if (polecenie("clear")) SMS_Terminal.usunąć_wpis();
        else if (polecenie("test")) jądro.testy();
        else if (polecenie("halt")) {
            SMS_Terminal.Zapis("HALTED\n");
            urządzenie_WARTOŚĆ.정지();
        } else SMS_Terminal.Zapis("알 identyfikator 없는 명령입니다. help를 입력하세요.\n");
    }

    static void akceptować_ORAZ_zapis(int WARTOŚĆ) {
        if (WARTOŚĆ == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = WARTOŚĆ == 13;
        if (WARTOŚĆ == 10 || WARTOŚĆ == 13) {
            SMS_Terminal.문자(10);
            if (Pamięć_system_plików.편집중) Pamięć_system_plików.Edytowane_linia(wejście_WARTOŚĆ, długość_WARTOŚĆ, linia_przepełnienie);
            else Proces_WARTOŚĆ_wpis();
            długość_WARTOŚĆ = 0;
            linia_przepełnienie = false;
            SMS_Terminal.Zapis(Pamięć_system_plików.편집중 ? "...> " : "jkoros> ");
        } else if (WARTOŚĆ == 8 || WARTOŚĆ == 127) {
            if (długość_WARTOŚĆ > 0) {
                długość_WARTOŚĆ--;
                SMS_Terminal.직렬바이트(8); SMS_Terminal.직렬바이트(32); SMS_Terminal.직렬바이트(8);
                SMS_Terminal.화면문자(8);
            }
        } else if (WARTOŚĆ >= 32 && WARTOŚĆ < 127 && długość_WARTOŚĆ < wejście_WARTOŚĆ.length) {
            wejście_WARTOŚĆ[długość_WARTOŚĆ++] = WARTOŚĆ;
            SMS_Terminal.문자(WARTOŚĆ);
        } else if (WARTOŚĆ >= 32 && WARTOŚĆ < 127) linia_przepełnienie = true;
    }

    static void Uruchom_2() {
        pokaż_pomoc();
        SMS_Terminal.Zapis("READY\njkoros> ");
        while (true) {
            int WARTOŚĆ = SMS_Terminal.직렬읽기();
            if (WARTOŚĆ < 0) WARTOŚĆ = klawiatura.Odczyt();
            if (WARTOŚĆ >= 0) akceptować_ORAZ_zapis(WARTOŚĆ);
            else { sieć_Stos.확인(); urządzenie_WARTOŚĆ.잠시양보(); }
        }
    }
}
