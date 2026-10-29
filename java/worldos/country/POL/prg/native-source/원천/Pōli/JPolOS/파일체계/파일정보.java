// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Pōli.JPolOS.파일체계;

public final class 파일정보 {
    private final int 크기;
    private final int 형태;

    public 파일정보(int 크기, int 형태) {
        this.크기 = 크기;
        this.형태 = 형태;
    }

    public int 크기() {
        return 크기;
    }

    public int 형태() {
        return 형태;
    }
}

