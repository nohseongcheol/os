// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package España.JEspOS.파일체계;

public final class 파일정보 {
    private final int Tamañu;
    private final int 형태;

    public 파일정보(int Tamañu, int 형태) {
        this.Tamañu = Tamañu;
        this.형태 = 형태;
    }

    public int Tamañu() {
        return Tamañu;
    }

    public int 형태() {
        return 형태;
    }
}

