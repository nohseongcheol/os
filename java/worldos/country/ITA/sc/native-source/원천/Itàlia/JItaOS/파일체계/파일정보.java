// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Itàlia.JItaOS.파일체계;

public final class 파일정보 {
    private final int Mannària;
    private final int 형태;

    public 파일정보(int Mannària, int 형태) {
        this.Mannària = Mannària;
        this.형태 = 형태;
    }

    public int Mannària() {
        return Mannària;
    }

    public int 형태() {
        return 형태;
    }
}

