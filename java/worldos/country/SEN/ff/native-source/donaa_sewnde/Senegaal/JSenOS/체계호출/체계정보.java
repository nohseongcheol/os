// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Senegaal.JSenOS.체계호출;

public final class 체계정보 {
    private final String yuɓɓo_innde;
    private final String piɓol_innde;
    private final String 배포판;
    private final String yamre_njaru;
    private final String 기계;

    public 체계정보(String yuɓɓo_innde, String piɓol_innde, String 배포판, String yamre_njaru, String 기계) {
        this.yuɓɓo_innde = yuɓɓo_innde;
        this.piɓol_innde = piɓol_innde;
        this.배포판 = 배포판;
        this.yamre_njaru = yamre_njaru;
        this.기계 = 기계;
    }

    public String yuɓɓo_innde() { return yuɓɓo_innde; }
    public String piɓol_innde() { return piɓol_innde; }
    public String 배포판() { return 배포판; }
    public String yamre_njaru() { return yamre_njaru; }
    public String 기계() { return 기계; }
}
