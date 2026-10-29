// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 obszar_WARTOŚĆ_366e0bfa. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class urządzenie_magazynujące_połączenie {
    static boolean systemy_informacyjne_Aktywny_9e72441a = false;
    static int[] obszar_dane = new int[512];
    static void 잠깐기다리기() {
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) urządzenie_WARTOŚĆ.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Uruchom_2 = urządzenie_WARTOŚĆ.밀리초();
        while (urządzenie_WARTOŚĆ.밀리초() - Uruchom_2 < 500) {
            int Stan_WARTOŚĆ = urządzenie_WARTOŚĆ.입출력바이트읽기(0x1f7);
            if (Stan_WARTOŚĆ == 0 || Stan_WARTOŚĆ == 255) return -19;
            if ((Stan_WARTOŚĆ & 128) == 0) {
                if ((Stan_WARTOŚĆ & 33) != 0) return -5;
                if (!자료필요 || (Stan_WARTOŚĆ & 8) != 0) return 0;
            }
            urządzenie_WARTOŚĆ.잠시양보();
        }
        return -110;
    }
    static int żądanie(int obszar_WARTOŚĆ_366e0bfa, int polecenie) {
        if (obszar_WARTOŚĆ_366e0bfa < 0 || obszar_WARTOŚĆ_366e0bfa >= 2048) return -22;
        urządzenie_WARTOŚĆ.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ używać_WARTOŚĆ 안 함
        urządzenie_WARTOŚĆ.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int WYNIK = 준비기다리기(false);
        if (WYNIK < 0) return WYNIK;
        urządzenie_WARTOŚĆ.입출력바이트쓰기(0x1f2, 1);
        urządzenie_WARTOŚĆ.입출력바이트쓰기(0x1f3, obszar_WARTOŚĆ_366e0bfa & 255);
        urządzenie_WARTOŚĆ.입출력바이트쓰기(0x1f4, (obszar_WARTOŚĆ_366e0bfa >>> 8) & 255);
        urządzenie_WARTOŚĆ.입출력바이트쓰기(0x1f5, 0);
        urządzenie_WARTOŚĆ.입출력바이트쓰기(0x1f7, polecenie); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Odczyt(int obszar_WARTOŚĆ_366e0bfa) {
        int WYNIK = żądanie(obszar_WARTOŚĆ_366e0bfa, 0x20);
        if (WYNIK < 0) return WYNIK;
        for (int INDEKS = 0; INDEKS < 256; INDEKS++) {
            int WARTOŚĆ = urządzenie_WARTOŚĆ.입출력짧은수읽기(0x1f0);
            obszar_dane[INDEKS * 2] = WARTOŚĆ & 255; obszar_dane[INDEKS * 2 + 1] = WARTOŚĆ >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Zapis(int obszar_WARTOŚĆ_366e0bfa) {
        if (!systemy_informacyjne_Aktywny_9e72441a || obszar_WARTOŚĆ_366e0bfa < 1 || obszar_WARTOŚĆ_366e0bfa > 518) return -19;
        int WYNIK = żądanie(obszar_WARTOŚĆ_366e0bfa, 0x30);
        if (WYNIK < 0) return WYNIK;
        for (int INDEKS = 0; INDEKS < 256; INDEKS++)
            urządzenie_WARTOŚĆ.입출력짧은수쓰기(0x1f0, obszar_dane[INDEKS * 2] | obszar_dane[INDEKS * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int opróżnić_produkt_wyjściowy() {
        if (!systemy_informacyjne_Aktywny_9e72441a) return -19;
        urządzenie_WARTOŚĆ.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int analizować_liczba_całkowita(int pozycja) {
        return obszar_dane[pozycja] | obszar_dane[pozycja + 1] << 8 | obszar_dane[pozycja + 2] << 16 | obszar_dane[pozycja + 3] << 24;
    }
    static void zapis_liczba_całkowita_WARTOŚĆ(int pozycja, int WARTOŚĆ) {
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) obszar_dane[pozycja + INDEKS] = (WARTOŚĆ >>> (INDEKS * 8)) & 255;
    }
}
