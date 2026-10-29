// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Mooritani.JMrtOS.체계호출;

public final class 체계정보 {
    private final String kureel_tur;
    private final String lëkk_lëkk_tur;
    private final String 배포판;
    private final String taalif_xëyma;
    private final String masin;

    public 체계정보(String kureel_tur, String lëkk_lëkk_tur, String 배포판, String taalif_xëyma, String masin) {
        this.kureel_tur = kureel_tur;
        this.lëkk_lëkk_tur = lëkk_lëkk_tur;
        this.배포판 = 배포판;
        this.taalif_xëyma = taalif_xëyma;
        this.masin = masin;
    }

    public String kureel_tur() { return kureel_tur; }
    public String lëkk_lëkk_tur() { return lëkk_lëkk_tur; }
    public String 배포판() { return 배포판; }
    public String taalif_xëyma() { return taalif_xëyma; }
    public String masin() { return masin; }
}
