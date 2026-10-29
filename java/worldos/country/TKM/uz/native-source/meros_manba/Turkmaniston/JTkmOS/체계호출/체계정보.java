// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turkmaniston.JTkmOS.체계호출;

public final class 체계정보 {
    private final String tizim_nom;
    private final String bog_lama_nom;
    private final String 배포판;
    private final String versiya_VALUE;
    private final String 기계;

    public 체계정보(String tizim_nom, String bog_lama_nom, String 배포판, String versiya_VALUE, String 기계) {
        this.tizim_nom = tizim_nom;
        this.bog_lama_nom = bog_lama_nom;
        this.배포판 = 배포판;
        this.versiya_VALUE = versiya_VALUE;
        this.기계 = 기계;
    }

    public String tizim_nom() { return tizim_nom; }
    public String bog_lama_nom() { return bog_lama_nom; }
    public String 배포판() { return 배포판; }
    public String versiya_VALUE() { return versiya_VALUE; }
    public String 기계() { return 기계; }
}
