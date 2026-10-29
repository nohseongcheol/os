// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Özbekistan.JUzbOS.dosya_sistemi;

public final class Dosya_bilgi {
    private final int Boyut;
    private final int şekil_Tip;

    public Dosya_bilgi(int Boyut, int şekil_Tip) {
        this.Boyut = Boyut;
        this.şekil_Tip = şekil_Tip;
    }

    public int Boyut() {
        return Boyut;
    }

    public int şekil_Tip() {
        return şekil_Tip;
    }
}

