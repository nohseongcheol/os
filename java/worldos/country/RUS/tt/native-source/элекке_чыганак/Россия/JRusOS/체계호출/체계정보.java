// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Россия.JRusOS.체계호출;

public final class 체계정보 {
    private final String система_исем;
    private final String төен_исем;
    private final String 배포판;
    private final String версия_VALUE;
    private final String машина;

    public 체계정보(String система_исем, String төен_исем, String 배포판, String версия_VALUE, String машина) {
        this.система_исем = система_исем;
        this.төен_исем = төен_исем;
        this.배포판 = 배포판;
        this.версия_VALUE = версия_VALUE;
        this.машина = машина;
    }

    public String система_исем() { return система_исем; }
    public String төен_исем() { return төен_исем; }
    public String 배포판() { return 배포판; }
    public String версия_VALUE() { return версия_VALUE; }
    public String машина() { return машина; }
}
