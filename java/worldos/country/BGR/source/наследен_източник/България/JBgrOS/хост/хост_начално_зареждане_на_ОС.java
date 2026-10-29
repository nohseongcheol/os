// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package България.JBgrOS.хост;

import България.JBgrOS.ядро.ядро;

public final class хост_начално_зареждане_на_ОС {
    private хост_начално_зареждане_на_ОС() {
    }

    public static void main(String[] параметър_аргумент) {
        ядро ядро_стойност = new ядро(new 호스트하드웨어());
        ядро_стойност.Стартиране();
        ядро_стойност.изпълнявам_стъпка();
    }
}

