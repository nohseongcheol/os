// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti_Vabariik.JEstOS.체계호출;

public final class süsteem_Üksikasjad {
    private final String süsteem_nimetus;
    private final String sõlm_nimetus;
    private final String väljaanne_VALUE;
    private final String versioon_VALUE;
    private final String arvuti;

    public süsteem_Üksikasjad(String süsteem_nimetus, String sõlm_nimetus, String väljaanne_VALUE, String versioon_VALUE, String arvuti) {
        this.süsteem_nimetus = süsteem_nimetus;
        this.sõlm_nimetus = sõlm_nimetus;
        this.väljaanne_VALUE = väljaanne_VALUE;
        this.versioon_VALUE = versioon_VALUE;
        this.arvuti = arvuti;
    }

    public String süsteem_nimetus() { return süsteem_nimetus; }
    public String sõlm_nimetus() { return sõlm_nimetus; }
    public String väljaanne_VALUE() { return väljaanne_VALUE; }
    public String versioon_VALUE() { return versioon_VALUE; }
    public String arvuti() { return arvuti; }
}
