// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Éire.JIrlOS.체계호출;

public final class 체계정보 {
    private final String córas_ainm;
    private final String nód_ainm;
    private final String 배포판;
    private final String leagan_VALUE;
    private final String meaisín;

    public 체계정보(String córas_ainm, String nód_ainm, String 배포판, String leagan_VALUE, String meaisín) {
        this.córas_ainm = córas_ainm;
        this.nód_ainm = nód_ainm;
        this.배포판 = 배포판;
        this.leagan_VALUE = leagan_VALUE;
        this.meaisín = meaisín;
    }

    public String córas_ainm() { return córas_ainm; }
    public String nód_ainm() { return nód_ainm; }
    public String 배포판() { return 배포판; }
    public String leagan_VALUE() { return leagan_VALUE; }
    public String meaisín() { return meaisín; }
}
