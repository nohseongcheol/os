// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Yuganda.JUgaOS.파일체계;

public final class 파일정보 {
    private final int Bunene;
    private final int 형태;

    public 파일정보(int Bunene, int 형태) {
        this.Bunene = Bunene;
        this.형태 = 형태;
    }

    public int Bunene() {
        return Bunene;
    }

    public int 형태() {
        return 형태;
    }
}

