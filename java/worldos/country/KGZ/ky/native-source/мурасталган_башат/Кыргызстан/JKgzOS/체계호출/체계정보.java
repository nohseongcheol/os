// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Кыргызстан.JKgzOS.체계호출;

public final class 체계정보 {
    private final String тутум_аты;
    private final String түйүн_аты;
    private final String 배포판;
    private final String нуска_маани;
    private final String машина;

    public 체계정보(String тутум_аты, String түйүн_аты, String 배포판, String нуска_маани, String машина) {
        this.тутум_аты = тутум_аты;
        this.түйүн_аты = түйүн_аты;
        this.배포판 = 배포판;
        this.нуска_маани = нуска_маани;
        this.машина = машина;
    }

    public String тутум_аты() { return тутум_аты; }
    public String түйүн_аты() { return түйүн_аты; }
    public String 배포판() { return 배포판; }
    public String нуска_маани() { return нуска_маани; }
    public String машина() { return машина; }
}
