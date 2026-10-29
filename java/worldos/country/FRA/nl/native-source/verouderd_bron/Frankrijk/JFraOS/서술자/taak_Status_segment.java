// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Frankrijk.JFraOS.서술자;

/** x86 작업 switch_MODUS 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class taak_Status_segment {
    private int stack_nul_blok;
    private int stack_nul_ADRES;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int ADRES) {
        stack_nul_blok = 조각;
        stack_nul_ADRES = ADRES;
    }

    public int stack_nul_blok() { return stack_nul_blok; }
    public int stack_nul_ADRES() { return stack_nul_ADRES; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

