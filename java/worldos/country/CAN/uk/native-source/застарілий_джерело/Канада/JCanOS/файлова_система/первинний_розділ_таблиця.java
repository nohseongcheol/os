// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Канада.JCanOS.файлова_система;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 стандартне_значення 분할 영역을 읽는다. */
public final class первинний_розділ_таблиця {
    public static final class розділ_значення {
        private final int 종류;
        private final long ПУСК_розділ;
        private final long 구역수;

        розділ_значення(int 종류, long ПУСК_розділ, long 구역수) {
            this.종류 = 종류;
            this.ПУСК_розділ = ПУСК_розділ;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long ПУСК_розділ() { return ПУСК_розділ; }
        public long 구역수() { return 구역수; }
    }

    public List<розділ_значення> Читання(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<розділ_значення> результат = new ArrayList<розділ_значення>();
        for (int індекс = 0; індекс < 4; індекс++) {
            int позиція = 446 + індекс * 16;
            int 종류 = 첫구역[позиція + 4] & 0xff;
            long запустити = з_прямим_порядком_байтів_ціле_число(첫구역, позиція + 8);
            long Розмір = з_прямим_порядком_байтів_ціле_число(첫구역, позиція + 12);
            if (종류 != 0 && Розмір != 0) {
                результат.add(new розділ_значення(종류, запустити, Розмір));
            }
        }
        return Collections.unmodifiableList(результат);
    }

    private long з_прямим_порядком_байтів_ціле_число(byte[] дані, int позиція) {
        return (дані[позиція] & 0xffL)
                | ((дані[позиція + 1] & 0xffL) << 8)
                | ((дані[позиція + 2] & 0xffL) << 16)
                | ((дані[позиція + 3] & 0xffL) << 24);
    }
}

