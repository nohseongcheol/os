// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlân.JNldOS.파일체계;

public final class 파일정보 {
    private final int Grutte;
    private final int 형태;

    public 파일정보(int Grutte, int 형태) {
        this.Grutte = Grutte;
        this.형태 = 형태;
    }

    public int Grutte() {
        return Grutte;
    }

    public int 형태() {
        return 형태;
    }
}

