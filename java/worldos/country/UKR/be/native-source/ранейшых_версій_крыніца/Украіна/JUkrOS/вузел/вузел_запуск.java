// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Украіна.JUkrOS.вузел;

import Украіна.JUkrOS.ядро.ядро;

public final class вузел_запуск {
    private вузел_запуск() {
    }

    public static void main(String[] параметр_аргумент) {
        ядро ядро_значэнне = new ядро(new 호스트하드웨어());
        ядро_значэнне.Выканаць();
        ядро_значэнне.한단계실행();
    }
}

