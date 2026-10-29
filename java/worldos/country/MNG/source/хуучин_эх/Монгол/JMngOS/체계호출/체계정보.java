// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Монгол.JMngOS.체계호출;

public final class 체계정보 {
    private final String систем_нэр;
    private final String зангилаа_нэр;
    private final String 배포판;
    private final String хувилбар_утга;
    private final String компьютер;

    public 체계정보(String систем_нэр, String зангилаа_нэр, String 배포판, String хувилбар_утга, String компьютер) {
        this.систем_нэр = систем_нэр;
        this.зангилаа_нэр = зангилаа_нэр;
        this.배포판 = 배포판;
        this.хувилбар_утга = хувилбар_утга;
        this.компьютер = компьютер;
    }

    public String систем_нэр() { return систем_нэр; }
    public String зангилаа_нэр() { return зангилаа_нэр; }
    public String 배포판() { return 배포판; }
    public String хувилбар_утга() { return хувилбар_утга; }
    public String компьютер() { return компьютер; }
}
