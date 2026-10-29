// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.sistem_de_fișiere;

public final class Fișier_info {
    private final int Mărime;
    private final int 형태;

    public Fișier_info(int Mărime, int 형태) {
        this.Mărime = Mărime;
        this.형태 = 형태;
    }

    public int Mărime() {
        return Mărime;
    }

    public int 형태() {
        return 형태;
    }
}

