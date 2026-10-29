// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Serbia.JSrbOS.서술자;

/** x86 작업 SWITCH_mod 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class sarcină_Stare_segment {
    private int Teanc_zero_bloc;
    private int Teanc_zero_adresa;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int adresa) {
        Teanc_zero_bloc = 조각;
        Teanc_zero_adresa = adresa;
    }

    public int Teanc_zero_bloc() { return Teanc_zero_bloc; }
    public int Teanc_zero_adresa() { return Teanc_zero_adresa; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

