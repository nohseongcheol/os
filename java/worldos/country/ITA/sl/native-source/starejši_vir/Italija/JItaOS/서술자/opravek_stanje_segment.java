// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italija.JItaOS.서술자;

/** x86 작업 SWITCH_MODE 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class opravek_stanje_segment {
    private int Sklad_nič_blok;
    private int Sklad_nič_naslov;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int naslov) {
        Sklad_nič_blok = 조각;
        Sklad_nič_naslov = naslov;
    }

    public int Sklad_nič_blok() { return Sklad_nič_blok; }
    public int Sklad_nič_naslov() { return Sklad_nič_naslov; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

