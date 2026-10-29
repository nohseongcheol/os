// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Noreg.JNorOS.filsystem;

public final class fil_informasjon {
    private final int Storleik;
    private final int 형태;

    public fil_informasjon(int Storleik, int 형태) {
        this.Storleik = Storleik;
        this.형태 = 형태;
    }

    public int Storleik() {
        return Storleik;
    }

    public int 형태() {
        return 형태;
    }
}

