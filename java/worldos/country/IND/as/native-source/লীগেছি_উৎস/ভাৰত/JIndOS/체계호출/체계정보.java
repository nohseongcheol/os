// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ভাৰত.JIndOS.체계호출;

public final class 체계정보 {
    private final String ছিষ্টেম_নাম;
    private final String নোড_নাম;
    private final String 배포판;
    private final String সংস্কৰণ_মান;
    private final String মেচিন;

    public 체계정보(String ছিষ্টেম_নাম, String নোড_নাম, String 배포판, String সংস্কৰণ_মান, String মেচিন) {
        this.ছিষ্টেম_নাম = ছিষ্টেম_নাম;
        this.নোড_নাম = নোড_নাম;
        this.배포판 = 배포판;
        this.সংস্কৰণ_মান = সংস্কৰণ_মান;
        this.মেচিন = মেচিন;
    }

    public String ছিষ্টেম_নাম() { return ছিষ্টেম_নাম; }
    public String নোড_নাম() { return নোড_নাম; }
    public String 배포판() { return 배포판; }
    public String সংস্কৰণ_মান() { return সংস্কৰণ_মান; }
    public String মেচিন() { return মেচিন; }
}
