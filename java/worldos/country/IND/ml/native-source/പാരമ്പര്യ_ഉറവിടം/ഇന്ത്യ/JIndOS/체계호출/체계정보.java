// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ഇന്ത്യ.JIndOS.체계호출;

public final class 체계정보 {
    private final String సిస్టమ్_നാ_മം;
    private final String നോഡ്_നാ_മം;
    private final String 배포판;
    private final String പതിപ്പ്_മൂല്യം;
    private final String മെഷീൻ;

    public 체계정보(String సిస్టమ్_നാ_മം, String നോഡ്_നാ_മം, String 배포판, String പതിപ്പ്_മൂല്യം, String മെഷീൻ) {
        this.సిస్టమ్_നാ_മം = సిస్టమ్_നാ_മം;
        this.നോഡ്_നാ_മം = നോഡ്_നാ_മം;
        this.배포판 = 배포판;
        this.പതിപ്പ്_മൂല്യം = പതിപ്പ്_മൂല്യം;
        this.മെഷീൻ = മെഷീൻ;
    }

    public String సిస్టమ్_നാ_മം() { return సిస్టమ్_നാ_മം; }
    public String നോഡ്_നാ_മം() { return നോഡ്_നാ_മം; }
    public String 배포판() { return 배포판; }
    public String പതിപ്പ്_മൂല്യം() { return പതിപ്പ്_മൂല്യം; }
    public String മെഷീൻ() { return മെഷീൻ; }
}
