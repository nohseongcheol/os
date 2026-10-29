// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti_Vabariik.JEstOS.failisüsteem;

public final class Fail_teave {
    private final int Suurus;
    private final int 형태;

    public Fail_teave(int Suurus, int 형태) {
        this.Suurus = Suurus;
        this.형태 = 형태;
    }

    public int Suurus() {
        return Suurus;
    }

    public int 형태() {
        return 형태;
    }
}

