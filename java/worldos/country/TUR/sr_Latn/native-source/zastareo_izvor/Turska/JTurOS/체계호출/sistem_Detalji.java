// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turska.JTurOS.체계호출;

public final class sistem_Detalji {
    private final String sistem_ime;
    private final String čvor_ime;
    private final String izdanje_VALUE;
    private final String verzija_VALUE;
    private final String računar;

    public sistem_Detalji(String sistem_ime, String čvor_ime, String izdanje_VALUE, String verzija_VALUE, String računar) {
        this.sistem_ime = sistem_ime;
        this.čvor_ime = čvor_ime;
        this.izdanje_VALUE = izdanje_VALUE;
        this.verzija_VALUE = verzija_VALUE;
        this.računar = računar;
    }

    public String sistem_ime() { return sistem_ime; }
    public String čvor_ime() { return čvor_ime; }
    public String izdanje_VALUE() { return izdanje_VALUE; }
    public String verzija_VALUE() { return verzija_VALUE; }
    public String računar() { return računar; }
}
