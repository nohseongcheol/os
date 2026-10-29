// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkiyə.JTurOS.fayl_sistemi;

public final class fayl_məlumat {
    private final int Böyüklük;
    private final int 형태;

    public fayl_məlumat(int Böyüklük, int 형태) {
        this.Böyüklük = Böyüklük;
        this.형태 = 형태;
    }

    public int Böyüklük() {
        return Böyüklük;
    }

    public int 형태() {
        return 형태;
    }
}

