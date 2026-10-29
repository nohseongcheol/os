// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lëtzebuerg.JLuxOS.체계호출;

public final class 체계정보 {
    private final String System_Numm;
    private final String Knuet_Numm;
    private final String 배포판;
    private final String Versioun_VALUE;
    private final String Computer;

    public 체계정보(String System_Numm, String Knuet_Numm, String 배포판, String Versioun_VALUE, String Computer) {
        this.System_Numm = System_Numm;
        this.Knuet_Numm = Knuet_Numm;
        this.배포판 = 배포판;
        this.Versioun_VALUE = Versioun_VALUE;
        this.Computer = Computer;
    }

    public String System_Numm() { return System_Numm; }
    public String Knuet_Numm() { return Knuet_Numm; }
    public String 배포판() { return 배포판; }
    public String Versioun_VALUE() { return Versioun_VALUE; }
    public String Computer() { return Computer; }
}
