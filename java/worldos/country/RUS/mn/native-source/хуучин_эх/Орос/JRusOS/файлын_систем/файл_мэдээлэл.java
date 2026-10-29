// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Орос.JRusOS.файлын_систем;

public final class файл_мэдээлэл {
    private final int Хэмжээ;
    private final int 형태;

    public файл_мэдээлэл(int Хэмжээ, int 형태) {
        this.Хэмжээ = Хэмжээ;
        this.형태 = 형태;
    }

    public int Хэмжээ() {
        return Хэмжээ;
    }

    public int 형태() {
        return 형태;
    }
}

