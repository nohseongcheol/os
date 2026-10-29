// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ukrajna.JUkrOS.체계호출;

public final class Rendszer_Részletek {
    private final String Rendszer_név;
    private final String csomópont_név;
    private final String kiadás_ÉRTÉK;
    private final String verzió_ÉRTÉK;
    private final String gép;

    public Rendszer_Részletek(String Rendszer_név, String csomópont_név, String kiadás_ÉRTÉK, String verzió_ÉRTÉK, String gép) {
        this.Rendszer_név = Rendszer_név;
        this.csomópont_név = csomópont_név;
        this.kiadás_ÉRTÉK = kiadás_ÉRTÉK;
        this.verzió_ÉRTÉK = verzió_ÉRTÉK;
        this.gép = gép;
    }

    public String Rendszer_név() { return Rendszer_név; }
    public String csomópont_név() { return csomópont_név; }
    public String kiadás_ÉRTÉK() { return kiadás_ÉRTÉK; }
    public String verzió_ÉRTÉK() { return verzió_ÉRTÉK; }
    public String gép() { return gép; }
}
