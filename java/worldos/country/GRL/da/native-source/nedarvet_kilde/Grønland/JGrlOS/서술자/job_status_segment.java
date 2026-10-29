// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Grønland.JGrlOS.서술자;

/** x86 작업 SKIFT_HYPPIGST 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class job_status_segment {
    private int Stak_nul_blok;
    private int Stak_nul_mail;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int mail) {
        Stak_nul_blok = 조각;
        Stak_nul_mail = mail;
    }

    public int Stak_nul_blok() { return Stak_nul_blok; }
    public int Stak_nul_mail() { return Stak_nul_mail; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

