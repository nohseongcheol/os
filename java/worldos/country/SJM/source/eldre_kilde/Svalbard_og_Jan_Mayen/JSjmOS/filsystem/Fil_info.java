// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svalbard_og_Jan_Mayen.JSjmOS.filsystem;

public final class Fil_info {
    private final int Størrelse;
    private final int 형태;

    public Fil_info(int Størrelse, int 형태) {
        this.Størrelse = Størrelse;
        this.형태 = 형태;
    }

    public int Størrelse() {
        return Størrelse;
    }

    public int 형태() {
        return 형태;
    }
}

