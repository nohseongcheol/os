// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.서술자;

/** x86 작업 SWITCH_MODE 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class uzdevums_Statuss_segments {
    private int kopa_nulle_bloks;
    private int kopa_nulle_adrese;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int adrese) {
        kopa_nulle_bloks = 조각;
        kopa_nulle_adrese = adrese;
    }

    public int kopa_nulle_bloks() { return kopa_nulle_bloks; }
    public int kopa_nulle_adrese() { return kopa_nulle_adrese; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

