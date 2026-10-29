// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti_Vabariik.JEstOS.서술자;

/** x86 작업 SWITCH_MODE 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class tööüksus_Olek_segment {
    private int Virn_null_plokk;
    private int Virn_null_ADDRESS;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int ADDRESS) {
        Virn_null_plokk = 조각;
        Virn_null_ADDRESS = ADDRESS;
    }

    public int Virn_null_plokk() { return Virn_null_plokk; }
    public int Virn_null_ADDRESS() { return Virn_null_ADDRESS; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

