// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Польша.JPolOS.узел;

import Польша.JPolOS.Ядро.Ядро;

public final class узел_запуск {
    private узел_запуск() {
    }

    public static void main(String[] параметр_аргумент) {
        Ядро ядро_ЗНАЧЕН = new Ядро(new узел_аппаратный());
        ядро_ЗНАЧЕН.запустить();
        ядро_ЗНАЧЕН.Выполнить_шаг();
    }
}

