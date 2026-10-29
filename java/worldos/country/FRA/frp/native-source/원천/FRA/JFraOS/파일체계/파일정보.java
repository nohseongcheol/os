// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package FRA.JFraOS.파일체계;

public final class 파일정보 {
    private final int Talyi;
    private final int 형태;

    public 파일정보(int Talyi, int 형태) {
        this.Talyi = Talyi;
        this.형태 = 형태;
    }

    public int Talyi() {
        return Talyi;
    }

    public int 형태() {
        return 형태;
    }
}

