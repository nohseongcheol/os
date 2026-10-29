// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.popisovač_položka;

/** x86 작업 SWITCH_MODE 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class úkol_Stav_segment {
    private int Štos_nula_blok;
    private int Štos_nula_ODKAZ;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int Adresa) {
        Štos_nula_blok = 조각;
        Štos_nula_ODKAZ = Adresa;
    }

    public int Štos_nula_blok() { return Štos_nula_blok; }
    public int Štos_nula_ODKAZ() { return Štos_nula_ODKAZ; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

