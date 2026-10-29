// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Словаччина.JSvkOS.хост;

import Словаччина.JSvkOS.Ядро.Ядро;

public final class хост_завантаження {
    private хост_завантаження() {
    }

    public static void main(String[] параметр_аргумент) {
        Ядро ядро_значення = new Ядро(new хост_обладнання());
        ядро_значення.запустити();
        ядро_значення.Виконати_крок();
    }
}

