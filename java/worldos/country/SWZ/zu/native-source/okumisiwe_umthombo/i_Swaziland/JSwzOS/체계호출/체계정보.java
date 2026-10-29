// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package i_Swaziland.JSwzOS.체계호출;

public final class 체계정보 {
    private final String isistimu_igama;
    private final String iqupha_igama;
    private final String 배포판;
    private final String isibuyekezo_inani;
    private final String umshini;

    public 체계정보(String isistimu_igama, String iqupha_igama, String 배포판, String isibuyekezo_inani, String umshini) {
        this.isistimu_igama = isistimu_igama;
        this.iqupha_igama = iqupha_igama;
        this.배포판 = 배포판;
        this.isibuyekezo_inani = isibuyekezo_inani;
        this.umshini = umshini;
    }

    public String isistimu_igama() { return isistimu_igama; }
    public String iqupha_igama() { return iqupha_igama; }
    public String 배포판() { return 배포판; }
    public String isibuyekezo_inani() { return isibuyekezo_inani; }
    public String umshini() { return umshini; }
}
