// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenija.JSvnOS.체계호출;

public final class sustav_Pojedinosti {
    private final String sustav_naziv;
    private final String čvor_naziv;
    private final String izdanje_VALUE;
    private final String verzija_VALUE;
    private final String stroj;

    public sustav_Pojedinosti(String sustav_naziv, String čvor_naziv, String izdanje_VALUE, String verzija_VALUE, String stroj) {
        this.sustav_naziv = sustav_naziv;
        this.čvor_naziv = čvor_naziv;
        this.izdanje_VALUE = izdanje_VALUE;
        this.verzija_VALUE = verzija_VALUE;
        this.stroj = stroj;
    }

    public String sustav_naziv() { return sustav_naziv; }
    public String čvor_naziv() { return čvor_naziv; }
    public String izdanje_VALUE() { return izdanje_VALUE; }
    public String verzija_VALUE() { return verzija_VALUE; }
    public String stroj() { return stroj; }
}
