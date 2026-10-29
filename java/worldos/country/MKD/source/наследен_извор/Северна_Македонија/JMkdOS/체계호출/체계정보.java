// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Северна_Македонија.JMkdOS.체계호출;

public final class 체계정보 {
    private final String систем_име;
    private final String јазол_име;
    private final String 배포판;
    private final String верзија_VALUE;
    private final String машина;

    public 체계정보(String систем_име, String јазол_име, String 배포판, String верзија_VALUE, String машина) {
        this.систем_име = систем_име;
        this.јазол_име = јазол_име;
        this.배포판 = 배포판;
        this.верзија_VALUE = верзија_VALUE;
        this.машина = машина;
    }

    public String систем_име() { return систем_име; }
    public String јазол_име() { return јазол_име; }
    public String 배포판() { return 배포판; }
    public String верзија_VALUE() { return верзија_VALUE; }
    public String машина() { return машина; }
}
