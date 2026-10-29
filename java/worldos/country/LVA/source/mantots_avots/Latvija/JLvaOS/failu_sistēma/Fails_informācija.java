// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.failu_sistēma;

public final class Fails_informācija {
    private final int Izmērs;
    private final int 형태;

    public Fails_informācija(int Izmērs, int 형태) {
        this.Izmērs = Izmērs;
        this.형태 = 형태;
    }

    public int Izmērs() {
        return Izmērs;
    }

    public int 형태() {
        return 형태;
    }
}

