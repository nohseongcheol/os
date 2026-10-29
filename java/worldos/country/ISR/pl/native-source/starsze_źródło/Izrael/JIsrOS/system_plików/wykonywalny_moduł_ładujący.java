// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Izrael.JIsrOS.system_plików;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Wykonaj_polecenie 파일의 머리부와 적재 구역을 검증한다. */
public final class wykonywalny_moduł_ładujący {
    public static final class obszar_WARTOŚĆ_366e0bfa {
        private final int Rodzaj_WARTOŚĆ;
        private final int flaga_WARTOŚĆ;
        private final int Adres;
        private final int Plik_stanowisko;
        private final int Rozmiar;

        obszar_WARTOŚĆ_366e0bfa(int Rodzaj_WARTOŚĆ, int flaga_WARTOŚĆ, int Adres, int Plik_stanowisko, int Rozmiar) {
            this.Rodzaj_WARTOŚĆ = Rodzaj_WARTOŚĆ;
            this.flaga_WARTOŚĆ = flaga_WARTOŚĆ;
            this.Adres = Adres;
            this.Plik_stanowisko = Plik_stanowisko;
            this.Rozmiar = Rozmiar;
        }

        public int Rodzaj_WARTOŚĆ() {
            return Rodzaj_WARTOŚĆ;
        }

        public int flaga_WARTOŚĆ() {
            return flaga_WARTOŚĆ;
        }

        public int Adres() {
            return Adres;
        }

        public int Plik_stanowisko() {
            return Plik_stanowisko;
        }

        public int Rozmiar() {
            return Rozmiar;
        }
    }

    public static final class OBRAZ {
        private final int START_ADRES;
        private final List<obszar_WARTOŚĆ_366e0bfa> 구역들;

        OBRAZ(int START_ADRES, List<obszar_WARTOŚĆ_366e0bfa> 구역들) {
            this.START_ADRES = START_ADRES;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int START_ADRES() {
            return START_ADRES;
        }

        public List<obszar_WARTOŚĆ_366e0bfa> 구역들() {
            return 구역들;
        }
    }

    public OBRAZ 검사(byte[] dane) {
        if (dane == null || dane.length < 52
                || dane[0] != 0x7f || dane[1] != 'E' || dane[2] != 'L' || dane[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (dane[4] != 1 || dane[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int START_ADRES = analizować_liczba_całkowita(dane, 24);
        int obszar_tabela_stanowisko = analizować_liczba_całkowita(dane, 32);
        int obszar_wpis_zmienić_rozmiar = 짧은정수읽기(dane, 46);
        int obszar_ILE_LICZB = 짧은정수읽기(dane, 48);
        if (obszar_wpis_zmienić_rozmiar < 40 || obszar_tabela_stanowisko < 0
                || (long) obszar_tabela_stanowisko + (long) obszar_wpis_zmienić_rozmiar * obszar_ILE_LICZB > dane.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<obszar_WARTOŚĆ_366e0bfa> 구역들 = new ArrayList<obszar_WARTOŚĆ_366e0bfa>();
        for (int INDEKS = 0; INDEKS < obszar_ILE_LICZB; INDEKS++) {
            int pozycja = obszar_tabela_stanowisko + INDEKS * obszar_wpis_zmienić_rozmiar;
            int Rodzaj_WARTOŚĆ = analizować_liczba_całkowita(dane, pozycja + 4);
            int flaga_WARTOŚĆ = analizować_liczba_całkowita(dane, pozycja + 8);
            int Adres = analizować_liczba_całkowita(dane, pozycja + 12);
            int Plik_stanowisko = analizować_liczba_całkowita(dane, pozycja + 16);
            int Rozmiar = analizować_liczba_całkowita(dane, pozycja + 20);
            if (Rozmiar < 0 || (Rodzaj_WARTOŚĆ != 8 && ((long) Plik_stanowisko + Rozmiar > dane.length || Plik_stanowisko < 0))) {
                throw new IllegalArgumentException("ELF obszar_WARTOŚĆ_366e0bfa dane 범위가 올바르지 않습니다.");
            }
            구역들.add(new obszar_WARTOŚĆ_366e0bfa(Rodzaj_WARTOŚĆ, flaga_WARTOŚĆ, Adres, Plik_stanowisko, Rozmiar));
        }
        return new OBRAZ(START_ADRES, 구역들);
    }

    private int analizować_liczba_całkowita(byte[] dane, int pozycja) {
        if (pozycja < 0 || pozycja > dane.length - 4) {
            throw new IllegalArgumentException("ELF liczba_całkowita 범위를 벗어났습니다.");
        }
        return (dane[pozycja] & 0xff)
                | ((dane[pozycja + 1] & 0xff) << 8)
                | ((dane[pozycja + 2] & 0xff) << 16)
                | ((dane[pozycja + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] dane, int pozycja) {
        if (pozycja < 0 || pozycja > dane.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 liczba_całkowita 범위를 벗어났습니다.");
        }
        return (dane[pozycja] & 0xff) | ((dane[pozycja + 1] & 0xff) << 8);
    }
}
