// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاڪستان.JPakOS.체계호출;

public final class 체계정보 {
    private final String سسٽم_نالو;
    private final String نوڊ_نالو;
    private final String 배포판;
    private final String ورزين_قدر;
    private final String مشين;

    public 체계정보(String سسٽم_نالو, String نوڊ_نالو, String 배포판, String ورزين_قدر, String مشين) {
        this.سسٽم_نالو = سسٽم_نالو;
        this.نوڊ_نالو = نوڊ_نالو;
        this.배포판 = 배포판;
        this.ورزين_قدر = ورزين_قدر;
        this.مشين = مشين;
    }

    public String سسٽم_نالو() { return سسٽم_نالو; }
    public String نوڊ_نالو() { return نوڊ_نالو; }
    public String 배포판() { return 배포판; }
    public String ورزين_قدر() { return ورزين_قدر; }
    public String مشين() { return مشين; }
}
