// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Słowacja.JSvkOS.system_plików;

public final class Plik_informacje {
    private final int Rozmiar;
    private final int kształt_Rodzaj;

    public Plik_informacje(int Rozmiar, int kształt_Rodzaj) {
        this.Rozmiar = Rozmiar;
        this.kształt_Rodzaj = kształt_Rodzaj;
    }

    public int Rozmiar() {
        return Rozmiar;
    }

    public int kształt_Rodzaj() {
        return kształt_Rodzaj;
    }
}

