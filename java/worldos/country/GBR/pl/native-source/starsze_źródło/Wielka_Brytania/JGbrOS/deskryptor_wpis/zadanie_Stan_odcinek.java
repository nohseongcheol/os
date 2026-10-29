// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Wielka_Brytania.JGbrOS.deskryptor_wpis;

/** x86 작업 zmiana_tryb 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class zadanie_Stan_odcinek {
    private int Stos_zero_blok;
    private int Stos_zero_ADRES;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int fragment_WARTOŚĆ_652d4b53, int Adres) {
        Stos_zero_blok = fragment_WARTOŚĆ_652d4b53;
        Stos_zero_ADRES = Adres;
    }

    public int Stos_zero_blok() { return Stos_zero_blok; }
    public int Stos_zero_ADRES() { return Stos_zero_ADRES; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

