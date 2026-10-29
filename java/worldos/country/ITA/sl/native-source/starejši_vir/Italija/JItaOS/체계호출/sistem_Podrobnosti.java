// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italija.JItaOS.체계호출;

public final class sistem_Podrobnosti {
    private final String sistem_ime;
    private final String vozlišče_ime;
    private final String izdaja_VALUE;
    private final String različica_VALUE;
    private final String računalnik;

    public sistem_Podrobnosti(String sistem_ime, String vozlišče_ime, String izdaja_VALUE, String različica_VALUE, String računalnik) {
        this.sistem_ime = sistem_ime;
        this.vozlišče_ime = vozlišče_ime;
        this.izdaja_VALUE = izdaja_VALUE;
        this.različica_VALUE = različica_VALUE;
        this.računalnik = računalnik;
    }

    public String sistem_ime() { return sistem_ime; }
    public String vozlišče_ime() { return vozlišče_ime; }
    public String izdaja_VALUE() { return izdaja_VALUE; }
    public String različica_VALUE() { return različica_VALUE; }
    public String računalnik() { return računalnik; }
}
