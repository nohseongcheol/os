// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Беларусь.JBlrOS.файловая_система;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 значение_по_умолчанию 분할 영역을 읽는다. */
public final class основной_раздел_таблица {
    public static final class раздел_ЗНАЧЕН {
        private final int Вид_ЗНАЧЕН;
        private final long Пуск_раздел;
        private final long раздел_СЧЁТ;

        раздел_ЗНАЧЕН(int Вид_ЗНАЧЕН, long Пуск_раздел, long раздел_СЧЁТ) {
            this.Вид_ЗНАЧЕН = Вид_ЗНАЧЕН;
            this.Пуск_раздел = Пуск_раздел;
            this.раздел_СЧЁТ = раздел_СЧЁТ;
        }

        public int Вид_ЗНАЧЕН() { return Вид_ЗНАЧЕН; }
        public long Пуск_раздел() { return Пуск_раздел; }
        public long раздел_СЧЁТ() { return раздел_СЧЁТ; }
    }

    public List<раздел_ЗНАЧЕН> Чтение(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<раздел_ЗНАЧЕН> результат = new ArrayList<раздел_ЗНАЧЕН>();
        for (int ИНДЕКС = 0; ИНДЕКС < 4; ИНДЕКС++) {
            int позиция = 446 + ИНДЕКС * 16;
            int Вид_ЗНАЧЕН = 첫구역[позиция + 4] & 0xff;
            long запустить = прямой_порядок_байтов_целое_число(첫구역, позиция + 8);
            long Размер = прямой_порядок_байтов_целое_число(첫구역, позиция + 12);
            if (Вид_ЗНАЧЕН != 0 && Размер != 0) {
                результат.add(new раздел_ЗНАЧЕН(Вид_ЗНАЧЕН, запустить, Размер));
            }
        }
        return Collections.unmodifiableList(результат);
    }

    private long прямой_порядок_байтов_целое_число(byte[] данные, int позиция) {
        return (данные[позиция] & 0xffL)
                | ((данные[позиция + 1] & 0xffL) << 8)
                | ((данные[позиция + 2] & 0xffL) << 16)
                | ((данные[позиция + 3] & 0xffL) << 24);
    }
}

