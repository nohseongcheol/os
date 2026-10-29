// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Jungtinė_Karalystė.JGbrOS.서술자;

/** x86 작업 SWITCH_MODE 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class užduotis_Būsena_segmentas {
    private int eilė_nulis_blokas;
    private int eilė_nulis_ADDRESS;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int ADDRESS) {
        eilė_nulis_blokas = 조각;
        eilė_nulis_ADDRESS = ADDRESS;
    }

    public int eilė_nulis_blokas() { return eilė_nulis_blokas; }
    public int eilė_nulis_ADDRESS() { return eilė_nulis_ADDRESS; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

