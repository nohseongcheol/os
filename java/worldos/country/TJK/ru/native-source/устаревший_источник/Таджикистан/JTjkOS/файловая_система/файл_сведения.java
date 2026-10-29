// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Таджикистан.JTjkOS.файловая_система;

public final class файл_сведения {
    private final int Размер;
    private final int фигура_Вид;

    public файл_сведения(int Размер, int фигура_Вид) {
        this.Размер = Размер;
        this.фигура_Вид = фигура_Вид;
    }

    public int Размер() {
        return Размер;
    }

    public int фигура_Вид() {
        return фигура_Вид;
    }
}

