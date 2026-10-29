// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package França.JFraOS.파일체계;

public final class 파일정보 {
    private final int Talha;
    private final int 형태;

    public 파일정보(int Talha, int 형태) {
        this.Talha = Talha;
        this.형태 = 형태;
    }

    public int Talha() {
        return Talha;
    }

    public int 형태() {
        return 형태;
    }
}

