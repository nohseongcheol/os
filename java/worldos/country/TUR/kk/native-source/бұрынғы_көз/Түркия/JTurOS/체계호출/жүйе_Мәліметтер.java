// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Түркия.JTurOS.체계호출;

public final class жүйе_Мәліметтер {
    private final String жүйе_аты;
    private final String түйін_аты;
    private final String 배포판;
    private final String нұсқа_мән;
    private final String компьютер;

    public жүйе_Мәліметтер(String жүйе_аты, String түйін_аты, String 배포판, String нұсқа_мән, String компьютер) {
        this.жүйе_аты = жүйе_аты;
        this.түйін_аты = түйін_аты;
        this.배포판 = 배포판;
        this.нұсқа_мән = нұсқа_мән;
        this.компьютер = компьютер;
    }

    public String жүйе_аты() { return жүйе_аты; }
    public String түйін_аты() { return түйін_аты; }
    public String 배포판() { return 배포판; }
    public String нұсқа_мән() { return нұсқа_мән; }
    public String компьютер() { return компьютер; }
}
