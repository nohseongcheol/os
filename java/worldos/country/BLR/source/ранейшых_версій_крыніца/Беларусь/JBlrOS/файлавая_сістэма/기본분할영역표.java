// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Беларусь.JBlrOS.файлавая_сістэма;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 значэнне_па_змаўчанні 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class раздзел_значэнне {
        private final int 종류;
        private final long Пуск_секцыя;
        private final long 구역수;

        раздзел_значэнне(int 종류, long Пуск_секцыя, long 구역수) {
            this.종류 = 종류;
            this.Пуск_секцыя = Пуск_секцыя;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long Пуск_секцыя() { return Пуск_секцыя; }
        public long 구역수() { return 구역수; }
    }

    public List<раздзел_значэнне> Чытанне(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<раздзел_значэнне> 결과 = new ArrayList<раздзел_значэнне>();
        for (int індэкс = 0; індэкс < 4; індэкс++) {
            int Пазіцыя = 446 + індэкс * 16;
            int 종류 = 첫구역[Пазіцыя + 4] & 0xff;
            long Выканаць = 작은순서정수(첫구역, Пазіцыя + 8);
            long Памер = 작은순서정수(첫구역, Пазіцыя + 12);
            if (종류 != 0 && Памер != 0) {
                결과.add(new раздзел_значэнне(종류, Выканаць, Памер));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] дадзеныя, int Пазіцыя) {
        return (дадзеныя[Пазіцыя] & 0xffL)
                | ((дадзеныя[Пазіцыя + 1] & 0xffL) << 8)
                | ((дадзеныя[Пазіцыя + 2] & 0xffL) << 16)
                | ((дадзеныя[Пазіцыя + 3] & 0xffL) << 24);
    }
}

