// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ukraina.JUkrOS.system_plików;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 wartość_domyślna 분할 영역을 읽는다. */
public final class partycja_podstawowa_tabela {
    public static final class partycja_WARTOŚĆ {
        private final int Rodzaj_WARTOŚĆ;
        private final long START_obszar;
        private final long obszar_ILE_LICZB;

        partycja_WARTOŚĆ(int Rodzaj_WARTOŚĆ, long START_obszar, long obszar_ILE_LICZB) {
            this.Rodzaj_WARTOŚĆ = Rodzaj_WARTOŚĆ;
            this.START_obszar = START_obszar;
            this.obszar_ILE_LICZB = obszar_ILE_LICZB;
        }

        public int Rodzaj_WARTOŚĆ() { return Rodzaj_WARTOŚĆ; }
        public long START_obszar() { return START_obszar; }
        public long obszar_ILE_LICZB() { return obszar_ILE_LICZB; }
    }

    public List<partycja_WARTOŚĆ> Odczyt(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<partycja_WARTOŚĆ> WYNIK = new ArrayList<partycja_WARTOŚĆ>();
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) {
            int pozycja = 446 + INDEKS * 16;
            int Rodzaj_WARTOŚĆ = 첫구역[pozycja + 4] & 0xff;
            long Uruchom_2 = little_endian_liczba_całkowita(첫구역, pozycja + 8);
            long Rozmiar = little_endian_liczba_całkowita(첫구역, pozycja + 12);
            if (Rodzaj_WARTOŚĆ != 0 && Rozmiar != 0) {
                WYNIK.add(new partycja_WARTOŚĆ(Rodzaj_WARTOŚĆ, Uruchom_2, Rozmiar));
            }
        }
        return Collections.unmodifiableList(WYNIK);
    }

    private long little_endian_liczba_całkowita(byte[] dane, int pozycja) {
        return (dane[pozycja] & 0xffL)
                | ((dane[pozycja + 1] & 0xffL) << 8)
                | ((dane[pozycja + 2] & 0xffL) << 16)
                | ((dane[pozycja + 3] & 0xffL) << 24);
    }
}

