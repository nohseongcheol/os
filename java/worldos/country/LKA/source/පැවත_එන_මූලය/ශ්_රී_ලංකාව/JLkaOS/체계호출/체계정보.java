// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ශ්_රී_ලංකාව.JLkaOS.체계호출;

public final class 체계정보 {
    private final String පද්ධතිය_නම;
    private final String මංසල_නම;
    private final String 배포판;
    private final String අනුවාදය_අගය;
    private final String යන්ත්_රය;

    public 체계정보(String පද්ධතිය_නම, String මංසල_නම, String 배포판, String අනුවාදය_අගය, String යන්ත්_රය) {
        this.පද්ධතිය_නම = පද්ධතිය_නම;
        this.මංසල_නම = මංසල_නම;
        this.배포판 = 배포판;
        this.අනුවාදය_අගය = අනුවාදය_අගය;
        this.යන්ත්_රය = යන්ත්_රය;
    }

    public String පද්ධතිය_නම() { return පද්ධතිය_නම; }
    public String මංසල_නම() { return මංසල_නම; }
    public String 배포판() { return 배포판; }
    public String අනුවාදය_අගය() { return අනුවාදය_අගය; }
    public String යන්ත්_රය() { return යන්ත්_රය; }
}
