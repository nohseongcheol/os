// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Romanya.JRouOS.tanımlayıcı_girdi;

/** x86 작업 geçiş_mod 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class Görev_Durum_segment {
    private int Yığın_sıfır_blok;
    private int Yığın_sıfır_ADRES;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int parça_değer, int ADRES) {
        Yığın_sıfır_blok = parça_değer;
        Yığın_sıfır_ADRES = ADRES;
    }

    public int Yığın_sıfır_blok() { return Yığın_sıfır_blok; }
    public int Yığın_sıfır_ADRES() { return Yığın_sıfır_ADRES; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

