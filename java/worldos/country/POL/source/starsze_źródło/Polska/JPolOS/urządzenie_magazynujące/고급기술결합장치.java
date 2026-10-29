// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Polska.JPolOS.urządzenie_magazynujące;

import java.util.Arrays;

/** ATA 28비트 polecenie 계층과 같은 512바이트 논리 obszar_WARTOŚĆ_366e0bfa 장치다. */
public final class 고급기술결합장치 {
    public static final int obszar_zmienić_rozmiar = 512;
    private final byte[] dane;
    private final boolean tylko_do_odczytu_WARTOŚĆ;

    public 고급기술결합장치(int obszar_ILE_LICZB, boolean tylko_do_odczytu_WARTOŚĆ) {
        if (obszar_ILE_LICZB <= 0) {
            throw new IllegalArgumentException("obszar_WARTOŚĆ_366e0bfa 수가 올바르지 않습니다.");
        }
        dane = new byte[Math.multiplyExact(obszar_ILE_LICZB, obszar_zmienić_rozmiar)];
        this.tylko_do_odczytu_WARTOŚĆ = tylko_do_odczytu_WARTOŚĆ;
    }

    public int obszar_ILE_LICZB() {
        return dane.length / obszar_zmienić_rozmiar;
    }

    public void Odczyt(int obszar_INDEKS, byte[] odbierać_cel) {
        czek_zakres(obszar_INDEKS, odbierać_cel);
        System.arraycopy(dane, obszar_INDEKS * obszar_zmienić_rozmiar, odbierać_cel, 0, obszar_zmienić_rozmiar);
    }

    public void Zapis(int obszar_INDEKS, byte[] 쓸자료) {
        if (tylko_do_odczytu_WARTOŚĆ) {
            throw new IllegalStateException("Odczyt 전용 장치입니다.");
        }
        czek_zakres(obszar_INDEKS, 쓸자료);
        System.arraycopy(쓸자료, 0, dane, obszar_INDEKS * obszar_zmienić_rozmiar, obszar_zmienić_rozmiar);
    }

    public void usunąć_wpis() {
        if (tylko_do_odczytu_WARTOŚĆ) {
            throw new IllegalStateException("Odczyt 전용 장치입니다.");
        }
        Arrays.fill(dane, (byte) 0);
    }

    private void czek_zakres(int obszar_INDEKS, byte[] 임시공간) {
        if (obszar_INDEKS < 0 || obszar_INDEKS >= obszar_ILE_LICZB() || 임시공간.length < obszar_zmienić_rozmiar) {
            throw new IllegalArgumentException("ATA obszar_WARTOŚĆ_366e0bfa 범위가 올바르지 않습니다.");
        }
    }
}

