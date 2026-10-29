// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package تاجیکستان.JTjkOS.체계호출;

public final class 체계정보 {
    private final String سیستم_نام;
    private final String گره_نام;
    private final String 배포판;
    private final String نسخه_مقدار;
    private final String دستگاه;

    public 체계정보(String سیستم_نام, String گره_نام, String 배포판, String نسخه_مقدار, String دستگاه) {
        this.سیستم_نام = سیستم_نام;
        this.گره_نام = گره_نام;
        this.배포판 = 배포판;
        this.نسخه_مقدار = نسخه_مقدار;
        this.دستگاه = دستگاه;
    }

    public String سیستم_نام() { return سیستم_نام; }
    public String گره_نام() { return گره_نام; }
    public String 배포판() { return 배포판; }
    public String نسخه_مقدار() { return نسخه_مقدار; }
    public String دستگاه() { return دستگاه; }
}
