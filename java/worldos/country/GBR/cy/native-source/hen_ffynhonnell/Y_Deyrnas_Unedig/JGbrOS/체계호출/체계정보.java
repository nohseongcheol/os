// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Y_Deyrnas_Unedig.JGbrOS.체계호출;

public final class 체계정보 {
    private final String system_enw;
    private final String cwgn_enw;
    private final String 배포판;
    private final String fersiwn_VALUE;
    private final String peiriant;

    public 체계정보(String system_enw, String cwgn_enw, String 배포판, String fersiwn_VALUE, String peiriant) {
        this.system_enw = system_enw;
        this.cwgn_enw = cwgn_enw;
        this.배포판 = 배포판;
        this.fersiwn_VALUE = fersiwn_VALUE;
        this.peiriant = peiriant;
    }

    public String system_enw() { return system_enw; }
    public String cwgn_enw() { return cwgn_enw; }
    public String 배포판() { return 배포판; }
    public String fersiwn_VALUE() { return fersiwn_VALUE; }
    public String peiriant() { return peiriant; }
}
