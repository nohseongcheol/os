// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاکستان.JPakOS.체계호출;

public final class 체계정보 {
    private final String نظام_ناں;
    private final String نوڈ_ناں;
    private final String 배포판;
    private final String ورژن_قدر;
    private final String مشین;

    public 체계정보(String نظام_ناں, String نوڈ_ناں, String 배포판, String ورژن_قدر, String مشین) {
        this.نظام_ناں = نظام_ناں;
        this.نوڈ_ناں = نوڈ_ناں;
        this.배포판 = 배포판;
        this.ورژن_قدر = ورژن_قدر;
        this.مشین = مشین;
    }

    public String نظام_ناں() { return نظام_ناں; }
    public String نوڈ_ناں() { return نوڈ_ناں; }
    public String 배포판() { return 배포판; }
    public String ورژن_قدر() { return ورژن_قدر; }
    public String مشین() { return مشین; }
}
