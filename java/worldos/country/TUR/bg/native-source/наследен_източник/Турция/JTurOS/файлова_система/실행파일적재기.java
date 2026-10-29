// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Турция.JTurOS.файлова_система;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian изпълнявам_команда 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class раздел_стойност {
        private final int 종류;
        private final int флаг_стойност;
        private final int адрес;
        private final int Файл_позиция;
        private final int Размер;

        раздел_стойност(int 종류, int флаг_стойност, int адрес, int Файл_позиция, int Размер) {
            this.종류 = 종류;
            this.флаг_стойност = флаг_стойност;
            this.адрес = адрес;
            this.Файл_позиция = Файл_позиция;
            this.Размер = Размер;
        }

        public int 종류() {
            return 종류;
        }

        public int флаг_стойност() {
            return флаг_стойност;
        }

        public int адрес() {
            return адрес;
        }

        public int Файл_позиция() {
            return Файл_позиция;
        }

        public int Размер() {
            return Размер;
        }
    }

    public static final class снимка {
        private final int Старт_адрес;
        private final List<раздел_стойност> 구역들;

        снимка(int Старт_адрес, List<раздел_стойност> 구역들) {
            this.Старт_адрес = Старт_адрес;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Старт_адрес() {
            return Старт_адрес;
        }

        public List<раздел_стойност> 구역들() {
            return 구역들;
        }
    }

    public снимка 검사(byte[] данни) {
        if (данни == null || данни.length < 52
                || данни[0] != 0x7f || данни[1] != 'E' || данни[2] != 'L' || данни[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (данни[4] != 1 || данни[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Старт_адрес = анализирам_цяло_число(данни, 24);
        int раздел_таблица_позиция = анализирам_цяло_число(данни, 32);
        int раздел_запис_размер = 짧은정수읽기(данни, 46);
        int 구역수 = 짧은정수읽기(данни, 48);
        if (раздел_запис_размер < 40 || раздел_таблица_позиция < 0
                || (long) раздел_таблица_позиция + (long) раздел_запис_размер * 구역수 > данни.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<раздел_стойност> 구역들 = new ArrayList<раздел_стойност>();
        for (int индекс = 0; индекс < 구역수; индекс++) {
            int Позиция = раздел_таблица_позиция + индекс * раздел_запис_размер;
            int 종류 = анализирам_цяло_число(данни, Позиция + 4);
            int флаг_стойност = анализирам_цяло_число(данни, Позиция + 8);
            int адрес = анализирам_цяло_число(данни, Позиция + 12);
            int Файл_позиция = анализирам_цяло_число(данни, Позиция + 16);
            int Размер = анализирам_цяло_число(данни, Позиция + 20);
            if (Размер < 0 || (종류 != 8 && ((long) Файл_позиция + Размер > данни.length || Файл_позиция < 0))) {
                throw new IllegalArgumentException("ELF раздел_стойност данни 범위가 올바르지 않습니다.");
            }
            구역들.add(new раздел_стойност(종류, флаг_стойност, адрес, Файл_позиция, Размер));
        }
        return new снимка(Старт_адрес, 구역들);
    }

    private int анализирам_цяло_число(byte[] данни, int Позиция) {
        if (Позиция < 0 || Позиция > данни.length - 4) {
            throw new IllegalArgumentException("ELF цяло_число 범위를 벗어났습니다.");
        }
        return (данни[Позиция] & 0xff)
                | ((данни[Позиция + 1] & 0xff) << 8)
                | ((данни[Позиция + 2] & 0xff) << 16)
                | ((данни[Позиция + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] данни, int Позиция) {
        if (Позиция < 0 || Позиция > данни.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 цяло_число 범위를 벗어났습니다.");
        }
        return (данни[Позиция] & 0xff) | ((данни[Позиция + 1] & 0xff) << 8);
    }
}
