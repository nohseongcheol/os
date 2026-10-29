// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkmenistan.JTkmOS.체계호출;

public final class 체계정보 {
    private final String ulgam_at;
    private final String düwün_at;
    private final String 배포판;
    private final String wersiýa_baha;
    private final String kompýuter;

    public 체계정보(String ulgam_at, String düwün_at, String 배포판, String wersiýa_baha, String kompýuter) {
        this.ulgam_at = ulgam_at;
        this.düwün_at = düwün_at;
        this.배포판 = 배포판;
        this.wersiýa_baha = wersiýa_baha;
        this.kompýuter = kompýuter;
    }

    public String ulgam_at() { return ulgam_at; }
    public String düwün_at() { return düwün_at; }
    public String 배포판() { return 배포판; }
    public String wersiýa_baha() { return wersiýa_baha; }
    public String kompýuter() { return kompýuter; }
}
