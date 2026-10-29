// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Suid_Afrika.JZafOS.체계호출;

public final class 체계정보 {
    private final String stelsel_naam;
    private final String nodus_naam;
    private final String uitgawe_VALUE;
    private final String weergawe_VALUE;
    private final String masjien;

    public 체계정보(String stelsel_naam, String nodus_naam, String uitgawe_VALUE, String weergawe_VALUE, String masjien) {
        this.stelsel_naam = stelsel_naam;
        this.nodus_naam = nodus_naam;
        this.uitgawe_VALUE = uitgawe_VALUE;
        this.weergawe_VALUE = weergawe_VALUE;
        this.masjien = masjien;
    }

    public String stelsel_naam() { return stelsel_naam; }
    public String nodus_naam() { return nodus_naam; }
    public String uitgawe_VALUE() { return uitgawe_VALUE; }
    public String weergawe_VALUE() { return weergawe_VALUE; }
    public String masjien() { return masjien; }
}
