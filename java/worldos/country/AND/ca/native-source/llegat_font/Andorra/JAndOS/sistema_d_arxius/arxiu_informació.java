// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Andorra.JAndOS.sistema_d_arxius;

public final class arxiu_informació {
    private final int Mida;
    private final int 형태;

    public arxiu_informació(int Mida, int 형태) {
        this.Mida = Mida;
        this.형태 = 형태;
    }

    public int Mida() {
        return Mida;
    }

    public int 형태() {
        return 형태;
    }
}

