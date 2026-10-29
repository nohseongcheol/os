// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package عێراق.JIrqOS.체계호출;

public final class 체계정보 {
    private final String سیستم_ناو;
    private final String گرێ_ناو;
    private final String 배포판;
    private final String وەشان_نرخ;
    private final String مەکینه;

    public 체계정보(String سیستم_ناو, String گرێ_ناو, String 배포판, String وەشان_نرخ, String مەکینه) {
        this.سیستم_ناو = سیستم_ناو;
        this.گرێ_ناو = گرێ_ناو;
        this.배포판 = 배포판;
        this.وەشان_نرخ = وەشان_نرخ;
        this.مەکینه = مەکینه;
    }

    public String سیستم_ناو() { return سیستم_ناو; }
    public String گرێ_ناو() { return گرێ_ناو; }
    public String 배포판() { return 배포판; }
    public String وەشان_نرخ() { return وەشان_نرخ; }
    public String مەکینه() { return مەکینه; }
}
