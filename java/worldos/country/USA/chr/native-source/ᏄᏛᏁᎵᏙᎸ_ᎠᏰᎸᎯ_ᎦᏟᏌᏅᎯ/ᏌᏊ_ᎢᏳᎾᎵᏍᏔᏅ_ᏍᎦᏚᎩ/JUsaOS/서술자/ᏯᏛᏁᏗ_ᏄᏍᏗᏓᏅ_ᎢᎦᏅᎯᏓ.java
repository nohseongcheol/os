// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.서술자;

/** x86 작업 ᎦᏁᏟᏴᏍᏗ_ᎬᏙᏗ 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class ᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅ_ᎢᎦᏅᎯᏓ {
    private int 영번쌓임조각;
    private int 영번쌓임주소;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int ᎪᏪᎵ_ᏫᏗᎦᏅᏗ) {
        영번쌓임조각 = 조각;
        영번쌓임주소 = ᎪᏪᎵ_ᏫᏗᎦᏅᏗ;
    }

    public int 영번쌓임조각() { return 영번쌓임조각; }
    public int 영번쌓임주소() { return 영번쌓임주소; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

