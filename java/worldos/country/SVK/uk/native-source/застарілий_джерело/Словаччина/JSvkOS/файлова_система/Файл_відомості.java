// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Словаччина.JSvkOS.файлова_система;

public final class Файл_відомості {
    private final int Розмір;
    private final int 형태;

    public Файл_відомості(int Розмір, int 형태) {
        this.Розмір = Розмір;
        this.형태 = 형태;
    }

    public int Розмір() {
        return Розмір;
    }

    public int 형태() {
        return 형태;
    }
}

