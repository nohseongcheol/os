// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nàìjíríà.JNgaOS.체계호출;

public final class 체계정보 {
    private final String ètò_orúkọ;
    private final String apẹka_orúkọ;
    private final String 배포판;
    private final String ẹ̀yà_iye;
    private final String maṣíìnì;

    public 체계정보(String ètò_orúkọ, String apẹka_orúkọ, String 배포판, String ẹ̀yà_iye, String maṣíìnì) {
        this.ètò_orúkọ = ètò_orúkọ;
        this.apẹka_orúkọ = apẹka_orúkọ;
        this.배포판 = 배포판;
        this.ẹ̀yà_iye = ẹ̀yà_iye;
        this.maṣíìnì = maṣíìnì;
    }

    public String ètò_orúkọ() { return ètò_orúkọ; }
    public String apẹka_orúkọ() { return apẹka_orúkọ; }
    public String 배포판() { return 배포판; }
    public String ẹ̀yà_iye() { return ẹ̀yà_iye; }
    public String maṣíìnì() { return maṣíìnì; }
}
