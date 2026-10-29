// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turska.JTurOS.sistem_datoteka;

public final class Datoteka_informacije {
    private final int promeniti_veličinu;
    private final int 형태;

    public Datoteka_informacije(int promeniti_veličinu, int 형태) {
        this.promeniti_veličinu = promeniti_veličinu;
        this.형태 = 형태;
    }

    public int promeniti_veličinu() {
        return promeniti_veličinu;
    }

    public int 형태() {
        return 형태;
    }
}

