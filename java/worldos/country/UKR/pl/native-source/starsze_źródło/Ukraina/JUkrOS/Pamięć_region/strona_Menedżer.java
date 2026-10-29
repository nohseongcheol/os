// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ukraina.JUkrOS.Pamięć_region;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB strona_WARTOŚĆ 연결과 Zapis 시 복사를 제공한다. */
public final class strona_Menedżer {
    public static final int rozmiar_strony = 4096;

    private static final class strona_WARTOŚĆ {
        private byte[] dane = new byte[rozmiar_strony];
        private int odwołanie_ILE_LICZB = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class przestrzeń_adresowa {
        private final Map<Integer, strona_WARTOŚĆ> strona_tabela = new HashMap<Integer, strona_WARTOŚĆ>();
    }

    public przestrzeń_adresowa 새주소공간() {
        return new przestrzeń_adresowa();
    }

    public void MAP_strona(przestrzeń_adresowa ADRES_region, int adres_wirtualny, boolean 쓰기가능) {
        int INDEKS = strona_identyfikator(adres_wirtualny);
        strona_WARTOŚĆ 새쪽 = new strona_WARTOŚĆ();
        새쪽.쓰기가능 = 쓰기가능;
        ADRES_region.strona_tabela.put(Integer.valueOf(INDEKS), 새쪽);
    }

    public przestrzeń_adresowa 쓰기시복사복제(przestrzeń_adresowa 원본) {
        przestrzeń_adresowa 복제본 = new przestrzeń_adresowa();
        for (Map.Entry<Integer, strona_WARTOŚĆ> wpis_WARTOŚĆ : 원본.strona_tabela.entrySet()) {
            strona_WARTOŚĆ Współdzielona_strona = wpis_WARTOŚĆ.getValue();
            Współdzielona_strona.odwołanie_ILE_LICZB++;
            if (Współdzielona_strona.쓰기가능) {
                Współdzielona_strona.쓰기가능 = false;
                Współdzielona_strona.쓰기시복사 = true;
            }
            복제본.strona_tabela.put(wpis_WARTOŚĆ.getKey(), Współdzielona_strona);
        }
        return 복제본;
    }

    public byte 바이트읽기(przestrzeń_adresowa ADRES_region, int adres_wirtualny) {
        strona_WARTOŚĆ wartość_docelowa = ZNAJDŹ_strona(ADRES_region, adres_wirtualny);
        return wartość_docelowa.dane[Math.floorMod(adres_wirtualny, rozmiar_strony)];
    }

    public void zapis_bajt_WARTOŚĆ(przestrzeń_adresowa ADRES_region, int adres_wirtualny, byte WARTOŚĆ) {
        int INDEKS = strona_identyfikator(adres_wirtualny);
        strona_WARTOŚĆ wartość_docelowa = ZNAJDŹ_strona(ADRES_region, adres_wirtualny);
        if (!wartość_docelowa.쓰기가능) {
            if (!wartość_docelowa.쓰기시복사) {
                throw new IllegalStateException("Odczyt 전용 쪽입니다.");
            }
            wartość_docelowa = Twórca_Prywatne_strona(ADRES_region, INDEKS, wartość_docelowa);
        }
        wartość_docelowa.dane[Math.floorMod(adres_wirtualny, rozmiar_strony)] = WARTOŚĆ;
    }

    public void Prywatne_zakres_zapis(przestrzeń_adresowa ADRES_region, int START_ADRES, int Rozmiar) {
        if (Rozmiar < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int Koniec_ADRES = Math.addExact(START_ADRES, Rozmiar);
        for (int Adres = START_ADRES; Adres < Koniec_ADRES; Adres = (strona_identyfikator(Adres) + 1) * rozmiar_strony) {
            int INDEKS = strona_identyfikator(Adres);
            strona_WARTOŚĆ wartość_docelowa = ZNAJDŹ_strona(ADRES_region, Adres);
            if (wartość_docelowa.쓰기시복사) {
                Twórca_Prywatne_strona(ADRES_region, INDEKS, wartość_docelowa);
            } else {
                wartość_docelowa.쓰기가능 = true;
            }
        }
    }

    public void zakres_zapis(przestrzeń_adresowa ADRES_region, int START_ADRES, byte[] dane) {
        for (int INDEKS = 0; INDEKS < dane.length; INDEKS++) {
            zapis_bajt_WARTOŚĆ(ADRES_region, START_ADRES + INDEKS, dane[INDEKS]);
        }
    }

    private strona_WARTOŚĆ Twórca_Prywatne_strona(przestrzeń_adresowa ADRES_region, int INDEKS, strona_WARTOŚĆ Współdzielona_strona) {
        strona_WARTOŚĆ Prywatne_strona = new strona_WARTOŚĆ();
        Prywatne_strona.dane = Arrays.copyOf(Współdzielona_strona.dane, Współdzielona_strona.dane.length);
        Prywatne_strona.쓰기가능 = true;
        Prywatne_strona.쓰기시복사 = false;
        Współdzielona_strona.odwołanie_ILE_LICZB--;
        ADRES_region.strona_tabela.put(Integer.valueOf(INDEKS), Prywatne_strona);
        return Prywatne_strona;
    }

    private strona_WARTOŚĆ ZNAJDŹ_strona(przestrzeń_adresowa ADRES_region, int Adres) {
        strona_WARTOŚĆ wartość_docelowa = ADRES_region.strona_tabela.get(Integer.valueOf(strona_identyfikator(Adres)));
        if (wartość_docelowa == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return wartość_docelowa;
    }

    private int strona_identyfikator(int Adres) {
        if (Adres < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return Adres / rozmiar_strony;
    }
}

