// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package An_Rìoghachd_Aonaichte.JGbrOS.체계호출;

public final class 체계정보 {
    private final String siostam_ainm;
    private final String nòd_ainm;
    private final String 배포판;
    private final String tionndadh_VALUE;
    private final String inneal;

    public 체계정보(String siostam_ainm, String nòd_ainm, String 배포판, String tionndadh_VALUE, String inneal) {
        this.siostam_ainm = siostam_ainm;
        this.nòd_ainm = nòd_ainm;
        this.배포판 = 배포판;
        this.tionndadh_VALUE = tionndadh_VALUE;
        this.inneal = inneal;
    }

    public String siostam_ainm() { return siostam_ainm; }
    public String nòd_ainm() { return nòd_ainm; }
    public String 배포판() { return 배포판; }
    public String tionndadh_VALUE() { return tionndadh_VALUE; }
    public String inneal() { return inneal; }
}
