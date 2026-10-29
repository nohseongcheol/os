// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package NLD.JNldOS.파일체계;

public final class 파일정보 {
    private final int Gruutde;
    private final int 형태;

    public 파일정보(int Gruutde, int 형태) {
        this.Gruutde = Gruutde;
        this.형태 = 형태;
    }

    public int Gruutde() {
        return Gruutde;
    }

    public int 형태() {
        return 형태;
    }
}

