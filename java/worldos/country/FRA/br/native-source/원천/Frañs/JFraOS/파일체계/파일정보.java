// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Frañs.JFraOS.파일체계;

public final class 파일정보 {
    private final int Ment;
    private final int 형태;

    public 파일정보(int Ment, int 형태) {
        this.Ment = Ment;
        this.형태 = 형태;
    }

    public int Ment() {
        return Ment;
    }

    public int 형태() {
        return 형태;
    }
}

