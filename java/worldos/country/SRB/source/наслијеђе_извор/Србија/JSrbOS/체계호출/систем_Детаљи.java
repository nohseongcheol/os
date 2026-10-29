// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Србија.JSrbOS.체계호출;

public final class систем_Детаљи {
    private final String систем_име;
    private final String чвор_име;
    private final String 배포판;
    private final String верзија_вриједност;
    private final String рачунар;

    public систем_Детаљи(String систем_име, String чвор_име, String 배포판, String верзија_вриједност, String рачунар) {
        this.систем_име = систем_име;
        this.чвор_име = чвор_име;
        this.배포판 = 배포판;
        this.верзија_вриједност = верзија_вриједност;
        this.рачунар = рачунар;
    }

    public String систем_име() { return систем_име; }
    public String чвор_име() { return чвор_име; }
    public String 배포판() { return 배포판; }
    public String верзија_вриједност() { return верзија_вриједност; }
    public String рачунар() { return рачунар; }
}
