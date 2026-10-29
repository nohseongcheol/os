// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package KIR.JKirOS.체계호출;

public final class 체계정보 {
    private final String 체계이름;
    private final String 마디이름;
    private final String 배포판;
    private final String 판;
    private final String 기계;

    public 체계정보(String 체계이름, String 마디이름, String 배포판, String 판, String 기계) {
        this.체계이름 = 체계이름;
        this.마디이름 = 마디이름;
        this.배포판 = 배포판;
        this.판 = 판;
        this.기계 = 기계;
    }

    public String 체계이름() { return 체계이름; }
    public String 마디이름() { return 마디이름; }
    public String 배포판() { return 배포판; }
    public String 판() { return 판; }
    public String 기계() { return 기계; }
}
