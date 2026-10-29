// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Босна_и_Херцеговина.JBihOS.체계호출;

public final class 체계정보 {
    private final String систем_назив;
    private final String чвор_назив;
    private final String 배포판;
    private final String верзија_вриједност;
    private final String 기계;

    public 체계정보(String систем_назив, String чвор_назив, String 배포판, String верзија_вриједност, String 기계) {
        this.систем_назив = систем_назив;
        this.чвор_назив = чвор_назив;
        this.배포판 = 배포판;
        this.верзија_вриједност = верзија_вриједност;
        this.기계 = 기계;
    }

    public String систем_назив() { return систем_назив; }
    public String чвор_назив() { return чвор_назив; }
    public String 배포판() { return 배포판; }
    public String верзија_вриједност() { return верзија_вриједност; }
    public String 기계() { return 기계; }
}
