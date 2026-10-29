// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Молдова.JMdaOS.файловая_система;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian 실행 파일의 머리부와 적재 구역을 검증한다. */
public final class исполняемый_загрузчик {
    public static final class раздел_ЗНАЧЕН_366e0bfa {
        private final int Вид_ЗНАЧЕН;
        private final int флаг_ЗНАЧЕН;
        private final int АДРЕС;
        private final int файл_позиция;
        private final int Размер;

        раздел_ЗНАЧЕН_366e0bfa(int Вид_ЗНАЧЕН, int флаг_ЗНАЧЕН, int АДРЕС, int файл_позиция, int Размер) {
            this.Вид_ЗНАЧЕН = Вид_ЗНАЧЕН;
            this.флаг_ЗНАЧЕН = флаг_ЗНАЧЕН;
            this.АДРЕС = АДРЕС;
            this.файл_позиция = файл_позиция;
            this.Размер = Размер;
        }

        public int Вид_ЗНАЧЕН() {
            return Вид_ЗНАЧЕН;
        }

        public int флаг_ЗНАЧЕН() {
            return флаг_ЗНАЧЕН;
        }

        public int АДРЕС() {
            return АДРЕС;
        }

        public int файл_позиция() {
            return файл_позиция;
        }

        public int Размер() {
            return Размер;
        }
    }

    public static final class фото {
        private final int Пуск_АДРЕС;
        private final List<раздел_ЗНАЧЕН_366e0bfa> 구역들;

        фото(int Пуск_АДРЕС, List<раздел_ЗНАЧЕН_366e0bfa> 구역들) {
            this.Пуск_АДРЕС = Пуск_АДРЕС;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Пуск_АДРЕС() {
            return Пуск_АДРЕС;
        }

        public List<раздел_ЗНАЧЕН_366e0bfa> 구역들() {
            return 구역들;
        }
    }

    public фото 검사(byte[] данные) {
        if (данные == null || данные.length < 52
                || данные[0] != 0x7f || данные[1] != 'E' || данные[2] != 'L' || данные[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (данные[4] != 1 || данные[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Пуск_АДРЕС = анализировать_целое_число(данные, 24);
        int раздел_таблица_позиция = анализировать_целое_число(данные, 32);
        int раздел_ввод_изменить_размер = 짧은정수읽기(данные, 46);
        int раздел_СЧЁТ = 짧은정수읽기(данные, 48);
        if (раздел_ввод_изменить_размер < 40 || раздел_таблица_позиция < 0
                || (long) раздел_таблица_позиция + (long) раздел_ввод_изменить_размер * раздел_СЧЁТ > данные.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<раздел_ЗНАЧЕН_366e0bfa> 구역들 = new ArrayList<раздел_ЗНАЧЕН_366e0bfa>();
        for (int ИНДЕКС = 0; ИНДЕКС < раздел_СЧЁТ; ИНДЕКС++) {
            int позиция = раздел_таблица_позиция + ИНДЕКС * раздел_ввод_изменить_размер;
            int Вид_ЗНАЧЕН = анализировать_целое_число(данные, позиция + 4);
            int флаг_ЗНАЧЕН = анализировать_целое_число(данные, позиция + 8);
            int АДРЕС = анализировать_целое_число(данные, позиция + 12);
            int файл_позиция = анализировать_целое_число(данные, позиция + 16);
            int Размер = анализировать_целое_число(данные, позиция + 20);
            if (Размер < 0 || (Вид_ЗНАЧЕН != 8 && ((long) файл_позиция + Размер > данные.length || файл_позиция < 0))) {
                throw new IllegalArgumentException("ELF раздел_ЗНАЧЕН_366e0bfa данные 범위가 올바르지 않습니다.");
            }
            구역들.add(new раздел_ЗНАЧЕН_366e0bfa(Вид_ЗНАЧЕН, флаг_ЗНАЧЕН, АДРЕС, файл_позиция, Размер));
        }
        return new фото(Пуск_АДРЕС, 구역들);
    }

    private int анализировать_целое_число(byte[] данные, int позиция) {
        if (позиция < 0 || позиция > данные.length - 4) {
            throw new IllegalArgumentException("ELF целое_число 범위를 벗어났습니다.");
        }
        return (данные[позиция] & 0xff)
                | ((данные[позиция + 1] & 0xff) << 8)
                | ((данные[позиция + 2] & 0xff) << 16)
                | ((данные[позиция + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] данные, int позиция) {
        if (позиция < 0 || позиция > данные.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 целое_число 범위를 벗어났습니다.");
        }
        return (данные[позиция] & 0xff) | ((данные[позиция + 1] & 0xff) << 8);
    }
}
