// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package భారతదేశం.JIndOS.체계호출;

public final class 체계정보 {
    private final String సిస్టం_పేరు;
    private final String నోడ్_పేరు;
    private final String 배포판;
    private final String సంస్కరణ_మూల్యం;
    private final String యంత్రం;

    public 체계정보(String సిస్టం_పేరు, String నోడ్_పేరు, String 배포판, String సంస్కరణ_మూల్యం, String యంత్రం) {
        this.సిస్టం_పేరు = సిస్టం_పేరు;
        this.నోడ్_పేరు = నోడ్_పేరు;
        this.배포판 = 배포판;
        this.సంస్కరణ_మూల్యం = సంస్కరణ_మూల్యం;
        this.యంత్రం = యంత్రం;
    }

    public String సిస్టం_పేరు() { return సిస్టం_పేరు; }
    public String నోడ్_పేరు() { return నోడ్_పేరు; }
    public String 배포판() { return 배포판; }
    public String సంస్కరణ_మూల్యం() { return సంస్కరణ_మూల్యం; }
    public String యంత్రం() { return యంత్రం; }
}
