// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Իրան.JIrnOS.체계호출;

public final class 체계정보 {
    private final String համակարգ_անուն;
    private final String հանգույց_անուն;
    private final String 배포판;
    private final String տարբերակ_արժեք;
    private final String մեքենա;

    public 체계정보(String համակարգ_անուն, String հանգույց_անուն, String 배포판, String տարբերակ_արժեք, String մեքենա) {
        this.համակարգ_անուն = համակարգ_անուն;
        this.հանգույց_անուն = հանգույց_անուն;
        this.배포판 = 배포판;
        this.տարբերակ_արժեք = տարբերակ_արժեք;
        this.մեքենա = մեքենա;
    }

    public String համակարգ_անուն() { return համակարգ_անուն; }
    public String հանգույց_անուն() { return հանգույց_անուն; }
    public String 배포판() { return 배포판; }
    public String տարբերակ_արժեք() { return տարբերակ_արժեք; }
    public String մեքենա() { return մեքենա; }
}
