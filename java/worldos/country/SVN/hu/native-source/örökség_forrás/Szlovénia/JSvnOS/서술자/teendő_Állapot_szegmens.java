// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Szlovénia.JSvnOS.서술자;

/** x86 작업 vált_mód 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class teendő_Állapot_szegmens {
    private int Sor_nulla_blokk;
    private int Sor_nulla_CÍM;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int CÍM) {
        Sor_nulla_blokk = 조각;
        Sor_nulla_CÍM = CÍM;
    }

    public int Sor_nulla_blokk() { return Sor_nulla_blokk; }
    public int Sor_nulla_CÍM() { return Sor_nulla_CÍM; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

