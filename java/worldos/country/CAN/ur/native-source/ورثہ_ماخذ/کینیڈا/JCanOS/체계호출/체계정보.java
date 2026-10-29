// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package کینیڈا.JCanOS.체계호출;

public final class 체계정보 {
    private final String نظام_نام;
    private final String نوڈ_نام;
    private final String 배포판;
    private final String ورژن_قدر;
    private final String مشین;

    public 체계정보(String نظام_نام, String نوڈ_نام, String 배포판, String ورژن_قدر, String مشین) {
        this.نظام_نام = نظام_نام;
        this.نوڈ_نام = نوڈ_نام;
        this.배포판 = 배포판;
        this.ورژن_قدر = ورژن_قدر;
        this.مشین = مشین;
    }

    public String نظام_نام() { return نظام_نام; }
    public String نوڈ_نام() { return نوڈ_نام; }
    public String 배포판() { return 배포판; }
    public String ورژن_قدر() { return ورژن_قدر; }
    public String مشین() { return مشین; }
}
