// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lëtzebuerg.JLuxOS.Fichierssystem;

public final class Fichier_Info {
    private final int d_Gréisst_veränneren;
    private final int 형태;

    public Fichier_Info(int d_Gréisst_veränneren, int 형태) {
        this.d_Gréisst_veränneren = d_Gréisst_veränneren;
        this.형태 = 형태;
    }

    public int d_Gréisst_veränneren() {
        return d_Gréisst_veränneren;
    }

    public int 형태() {
        return 형태;
    }
}

