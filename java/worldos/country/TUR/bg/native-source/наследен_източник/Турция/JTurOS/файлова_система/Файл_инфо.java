// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Турция.JTurOS.файлова_система;

public final class Файл_инфо {
    private final int Размер;
    private final int 형태;

    public Файл_инфо(int Размер, int 형태) {
        this.Размер = Размер;
        this.형태 = 형태;
    }

    public int Размер() {
        return Размер;
    }

    public int 형태() {
        return 형태;
    }
}

