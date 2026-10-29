// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] wejście_dane = new int[16384], produkt_wyjściowy_dane = new int[16384];
    static int wejście_długość, wejście_stanowisko, produkt_wyjściowy_długość, plik_wejściowy = -1, plik_wyjściowy = -1;
    static boolean potok_wejście, potok_produkt_wyjściowy;
    static int awaria_WARTOŚĆ;
    static boolean Zezwalaj_interakcyjny = true;
    public static int systemy_informacyjne_interakcyjny() { return Zezwalaj_interakcyjny && plik_wejściowy < 3 && plik_wyjściowy < 3 && !potok_wejście && !potok_produkt_wyjściowy ? 1 : 0; }
    public static int pozycja_wyjścia(int Kanał_WARTOŚĆ, int WARTOŚĆ) {
        if (Kanał_WARTOŚĆ != 1) return 0;
        if (plik_wyjściowy >= 3) { int 처리값 = Pamięć_Files.Zapis(plik_wyjściowy, WARTOŚĆ); if (처리값 < 0) awaria_WARTOŚĆ = 처리값; return 1; }
        if (!potok_produkt_wyjściowy) return 0;
        if (produkt_wyjściowy_długość == produkt_wyjściowy_dane.length) awaria_WARTOŚĆ = -28;
        else produkt_wyjściowy_dane[produkt_wyjściowy_długość++] = WARTOŚĆ;
        return 1;
    }
    public static int wejście_WARTOŚĆ() {
        if (plik_wejściowy >= 3) { int 처리값 = Pamięć_Files.Odczyt(plik_wejściowy); return 처리값 == 256 ? -2 : 처리값; }
        if (potok_wejście) return wejście_stanowisko < wejście_długość ? wejście_dane[wejście_stanowisko++] : -2;
        return -3; // UART로 Dalej_WARTOŚĆ
    }
    static void Uruchom_2(boolean interlinia_potok, boolean 뒤파이프) {
        potok_wejście = interlinia_potok; potok_produkt_wyjściowy = 뒤파이프;
        wejście_stanowisko = 0; produkt_wyjściowy_długość = 0; plik_wejściowy = -1; plik_wyjściowy = -1; awaria_WARTOŚĆ = 0;
    }
    static void 끝() {
        Tablica.입출력전환(0);
        if (plik_wejściowy >= 3) Pamięć_Files.Zamknięte(plik_wejściowy);
        if (plik_wyjściowy >= 3) Pamięć_Files.Zamknięte(plik_wyjściowy);
        if (potok_produkt_wyjściowy) { wejście_długość = produkt_wyjściowy_długość; for (int Loop_INDEKS = 0; Loop_INDEKS < produkt_wyjściowy_długość; Loop_INDEKS++) wejście_dane[Loop_INDEKS] = produkt_wyjściowy_dane[Loop_INDEKS]; }
        plik_wejściowy = -1; plik_wyjściowy = -1; potok_wejście = false; potok_produkt_wyjściowy = false;
    }
}
