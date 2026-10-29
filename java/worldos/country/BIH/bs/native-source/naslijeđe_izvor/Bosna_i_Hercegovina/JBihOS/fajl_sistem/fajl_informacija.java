// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.fajl_sistem;

public final class fajl_informacija {
    private final int Veličina;
    private final int 형태;

    public fajl_informacija(int Veličina, int 형태) {
        this.Veličina = Veličina;
        this.형태 = 형태;
    }

    public int Veličina() {
        return Veličina;
    }

    public int 형태() {
        return 형태;
    }
}

