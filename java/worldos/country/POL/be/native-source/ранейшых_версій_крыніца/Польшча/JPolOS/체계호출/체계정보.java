// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Польшча.JPolOS.체계호출;

public final class 체계정보 {
    private final String сістэма_імя;
    private final String вузел_імя;
    private final String 배포판;
    private final String версія_значэнне;
    private final String камп_ютар;

    public 체계정보(String сістэма_імя, String вузел_імя, String 배포판, String версія_значэнне, String камп_ютар) {
        this.сістэма_імя = сістэма_імя;
        this.вузел_імя = вузел_імя;
        this.배포판 = 배포판;
        this.версія_значэнне = версія_значэнне;
        this.камп_ютар = камп_ютар;
    }

    public String сістэма_імя() { return сістэма_імя; }
    public String вузел_імя() { return вузел_імя; }
    public String 배포판() { return 배포판; }
    public String версія_значэнне() { return версія_значэнне; }
    public String камп_ютар() { return камп_ютар; }
}
