// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package নেপাল.JNplOS.체계호출;

public final class 체계정보 {
    private final String সিস্টেম_নাম;
    private final String নোড_নাম;
    private final String 배포판;
    private final String সংস্করণ_মান;
    private final String মেশিন;

    public 체계정보(String সিস্টেম_নাম, String নোড_নাম, String 배포판, String সংস্করণ_মান, String মেশিন) {
        this.সিস্টেম_নাম = সিস্টেম_নাম;
        this.নোড_নাম = নোড_নাম;
        this.배포판 = 배포판;
        this.সংস্করণ_মান = সংস্করণ_মান;
        this.মেশিন = মেশিন;
    }

    public String সিস্টেম_নাম() { return সিস্টেম_নাম; }
    public String নোড_নাম() { return নোড_নাম; }
    public String 배포판() { return 배포판; }
    public String সংস্করণ_মান() { return সংস্করণ_মান; }
    public String মেশিন() { return মেশিন; }
}
