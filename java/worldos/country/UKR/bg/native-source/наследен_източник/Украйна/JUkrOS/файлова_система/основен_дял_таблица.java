// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Украйна.JUkrOS.файлова_система;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 стойност_по_подразбиране 분할 영역을 읽는다. */
public final class основен_дял_таблица {
    public static final class дял_стойност {
        private final int 종류;
        private final long Старт_раздел;
        private final long 구역수;

        дял_стойност(int 종류, long Старт_раздел, long 구역수) {
            this.종류 = 종류;
            this.Старт_раздел = Старт_раздел;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long Старт_раздел() { return Старт_раздел; }
        public long 구역수() { return 구역수; }
    }

    public List<дял_стойност> Четене(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<дял_стойност> РЕЗУЛТАТ = new ArrayList<дял_стойност>();
        for (int индекс = 0; индекс < 4; индекс++) {
            int Позиция = 446 + индекс * 16;
            int 종류 = 첫구역[Позиция + 4] & 0xff;
            long Стартиране = първо_младшия_бит_с_водещ_младши_бит_цяло_число(첫구역, Позиция + 8);
            long Размер = първо_младшия_бит_с_водещ_младши_бит_цяло_число(첫구역, Позиция + 12);
            if (종류 != 0 && Размер != 0) {
                РЕЗУЛТАТ.add(new дял_стойност(종류, Стартиране, Размер));
            }
        }
        return Collections.unmodifiableList(РЕЗУЛТАТ);
    }

    private long първо_младшия_бит_с_водещ_младши_бит_цяло_число(byte[] данни, int Позиция) {
        return (данни[Позиция] & 0xffL)
                | ((данни[Позиция + 1] & 0xffL) << 8)
                | ((данни[Позиция + 2] & 0xffL) << 16)
                | ((данни[Позиция + 3] & 0xffL) << 24);
    }
}

