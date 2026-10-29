// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package BEL.JBelOS.파일체계;

public final class 파일정보 {
    private final int Grandeu;
    private final int 형태;

    public 파일정보(int Grandeu, int 형태) {
        this.Grandeu = Grandeu;
        this.형태 = 형태;
    }

    public int Grandeu() {
        return Grandeu;
    }

    public int 형태() {
        return 형태;
    }
}

