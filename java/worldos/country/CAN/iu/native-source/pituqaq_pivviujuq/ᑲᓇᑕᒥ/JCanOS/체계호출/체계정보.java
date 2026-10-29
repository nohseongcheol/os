// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᑲᓇᑕᒥ.JCanOS.체계호출;

public final class 체계정보 {
    private final String qarasaujaq_atiq;
    private final String attavigijaq_atiq;
    private final String 배포판;
    private final String imaittuuninga_atuutilik;
    private final String 기계;

    public 체계정보(String qarasaujaq_atiq, String attavigijaq_atiq, String 배포판, String imaittuuninga_atuutilik, String 기계) {
        this.qarasaujaq_atiq = qarasaujaq_atiq;
        this.attavigijaq_atiq = attavigijaq_atiq;
        this.배포판 = 배포판;
        this.imaittuuninga_atuutilik = imaittuuninga_atuutilik;
        this.기계 = 기계;
    }

    public String qarasaujaq_atiq() { return qarasaujaq_atiq; }
    public String attavigijaq_atiq() { return attavigijaq_atiq; }
    public String 배포판() { return 배포판; }
    public String imaittuuninga_atuutilik() { return imaittuuninga_atuutilik; }
    public String 기계() { return 기계; }
}
