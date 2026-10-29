// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Portugal.JPrtOS.sistema_de_ficheiros;

public final class Ficheiro_información {
    private final int Tamaño;
    private final int 형태;

    public Ficheiro_información(int Tamaño, int 형태) {
        this.Tamaño = Tamaño;
        this.형태 = 형태;
    }

    public int Tamaño() {
        return Tamaño;
    }

    public int 형태() {
        return 형태;
    }
}

