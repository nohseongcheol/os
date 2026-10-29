// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.체계호출;

public final class sistem_Detalji {
    private final String sistem_naziv;
    private final String čvor_naziv;
    private final String 배포판;
    private final String verzija_VALUE;
    private final String mašina;

    public sistem_Detalji(String sistem_naziv, String čvor_naziv, String 배포판, String verzija_VALUE, String mašina) {
        this.sistem_naziv = sistem_naziv;
        this.čvor_naziv = čvor_naziv;
        this.배포판 = 배포판;
        this.verzija_VALUE = verzija_VALUE;
        this.mašina = mašina;
    }

    public String sistem_naziv() { return sistem_naziv; }
    public String čvor_naziv() { return čvor_naziv; }
    public String 배포판() { return 배포판; }
    public String verzija_VALUE() { return verzija_VALUE; }
    public String mašina() { return mašina; }
}
