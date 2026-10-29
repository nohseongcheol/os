// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nijar.JNerOS.체계호출;

public final class 체계정보 {
    private final String na_ura_Suna;
    private final String Gwafa_Suna;
    private final String 배포판;
    private final String siga_Daraja;
    private final String na_ura_mai_kwakwalwa;

    public 체계정보(String na_ura_Suna, String Gwafa_Suna, String 배포판, String siga_Daraja, String na_ura_mai_kwakwalwa) {
        this.na_ura_Suna = na_ura_Suna;
        this.Gwafa_Suna = Gwafa_Suna;
        this.배포판 = 배포판;
        this.siga_Daraja = siga_Daraja;
        this.na_ura_mai_kwakwalwa = na_ura_mai_kwakwalwa;
    }

    public String na_ura_Suna() { return na_ura_Suna; }
    public String Gwafa_Suna() { return Gwafa_Suna; }
    public String 배포판() { return 배포판; }
    public String siga_Daraja() { return siga_Daraja; }
    public String na_ura_mai_kwakwalwa() { return na_ura_mai_kwakwalwa; }
}
