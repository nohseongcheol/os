// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkiyə.JTurOS.체계호출;

public final class 체계정보 {
    private final String sistem_ad;
    private final String qovşaq_ad;
    private final String 배포판;
    private final String versiya_VALUE;
    private final String maşın;

    public 체계정보(String sistem_ad, String qovşaq_ad, String 배포판, String versiya_VALUE, String maşın) {
        this.sistem_ad = sistem_ad;
        this.qovşaq_ad = qovşaq_ad;
        this.배포판 = 배포판;
        this.versiya_VALUE = versiya_VALUE;
        this.maşın = maşın;
    }

    public String sistem_ad() { return sistem_ad; }
    public String qovşaq_ad() { return qovşaq_ad; }
    public String 배포판() { return 배포판; }
    public String versiya_VALUE() { return versiya_VALUE; }
    public String maşın() { return maşın; }
}
