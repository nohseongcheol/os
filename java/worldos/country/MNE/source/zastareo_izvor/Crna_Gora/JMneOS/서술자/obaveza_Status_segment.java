// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Crna_Gora.JMneOS.서술자;

/** x86 작업 SWITCH_MODE 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class obaveza_Status_segment {
    private int stek_nula_blok;
    private int stek_nula_adresa;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int adresa) {
        stek_nula_blok = 조각;
        stek_nula_adresa = adresa;
    }

    public int stek_nula_blok() { return stek_nula_blok; }
    public int stek_nula_adresa() { return stek_nula_adresa; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

