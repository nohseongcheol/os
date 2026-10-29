// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Oʻzbekiston.JUzbOS.fayllar_tizimi;

public final class fayl_ma_lumot {
    private final int Hajmi;
    private final int 형태;

    public fayl_ma_lumot(int Hajmi, int 형태) {
        this.Hajmi = Hajmi;
        this.형태 = 형태;
    }

    public int Hajmi() {
        return Hajmi;
    }

    public int 형태() {
        return 형태;
    }
}

