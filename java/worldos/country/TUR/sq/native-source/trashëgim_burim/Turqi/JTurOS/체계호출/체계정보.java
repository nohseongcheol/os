// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turqi.JTurOS.체계호출;

public final class 체계정보 {
    private final String sistem_emër;
    private final String nyjë_emër;
    private final String 배포판;
    private final String version_VALUE;
    private final String makinë;

    public 체계정보(String sistem_emër, String nyjë_emër, String 배포판, String version_VALUE, String makinë) {
        this.sistem_emër = sistem_emër;
        this.nyjë_emër = nyjë_emër;
        this.배포판 = 배포판;
        this.version_VALUE = version_VALUE;
        this.makinë = makinë;
    }

    public String sistem_emër() { return sistem_emër; }
    public String nyjë_emër() { return nyjë_emër; }
    public String 배포판() { return 배포판; }
    public String version_VALUE() { return version_VALUE; }
    public String makinë() { return makinë; }
}
