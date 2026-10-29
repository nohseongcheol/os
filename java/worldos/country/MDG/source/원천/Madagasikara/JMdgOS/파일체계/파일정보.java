// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Madagasikara.JMdgOS.파일체계;

public final class 파일정보 {
    private final int Habe;
    private final int 형태;

    public 파일정보(int Habe, int 형태) {
        this.Habe = Habe;
        this.형태 = 형태;
    }

    public int Habe() {
        return Habe;
    }

    public int 형태() {
        return 형태;
    }
}

