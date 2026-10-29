// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Молдова.JMdaOS.файлова_система;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Виконати_команда 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class розділ_значення_366e0bfa {
        private final int 종류;
        private final int позначка_значення;
        private final int Адреса;
        private final int Файл_посада;
        private final int Розмір;

        розділ_значення_366e0bfa(int 종류, int позначка_значення, int Адреса, int Файл_посада, int Розмір) {
            this.종류 = 종류;
            this.позначка_значення = позначка_значення;
            this.Адреса = Адреса;
            this.Файл_посада = Файл_посада;
            this.Розмір = Розмір;
        }

        public int 종류() {
            return 종류;
        }

        public int позначка_значення() {
            return позначка_значення;
        }

        public int Адреса() {
            return Адреса;
        }

        public int Файл_посада() {
            return Файл_посада;
        }

        public int Розмір() {
            return Розмір;
        }
    }

    public static final class фото {
        private final int ПУСК_адреса;
        private final List<розділ_значення_366e0bfa> 구역들;

        фото(int ПУСК_адреса, List<розділ_значення_366e0bfa> 구역들) {
            this.ПУСК_адреса = ПУСК_адреса;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int ПУСК_адреса() {
            return ПУСК_адреса;
        }

        public List<розділ_значення_366e0bfa> 구역들() {
            return 구역들;
        }
    }

    public фото 검사(byte[] дані) {
        if (дані == null || дані.length < 52
                || дані[0] != 0x7f || дані[1] != 'E' || дані[2] != 'L' || дані[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (дані[4] != 1 || дані[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int ПУСК_адреса = аналізувати_ціле_число(дані, 24);
        int розділ_таблиця_посада = аналізувати_ціле_число(дані, 32);
        int розділ_запис_змінювати_розмір = 짧은정수읽기(дані, 46);
        int 구역수 = 짧은정수읽기(дані, 48);
        if (розділ_запис_змінювати_розмір < 40 || розділ_таблиця_посада < 0
                || (long) розділ_таблиця_посада + (long) розділ_запис_змінювати_розмір * 구역수 > дані.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<розділ_значення_366e0bfa> 구역들 = new ArrayList<розділ_значення_366e0bfa>();
        for (int індекс = 0; індекс < 구역수; індекс++) {
            int позиція = розділ_таблиця_посада + індекс * розділ_запис_змінювати_розмір;
            int 종류 = аналізувати_ціле_число(дані, позиція + 4);
            int позначка_значення = аналізувати_ціле_число(дані, позиція + 8);
            int Адреса = аналізувати_ціле_число(дані, позиція + 12);
            int Файл_посада = аналізувати_ціле_число(дані, позиція + 16);
            int Розмір = аналізувати_ціле_число(дані, позиція + 20);
            if (Розмір < 0 || (종류 != 8 && ((long) Файл_посада + Розмір > дані.length || Файл_посада < 0))) {
                throw new IllegalArgumentException("ELF розділ_значення_366e0bfa дані 범위가 올바르지 않습니다.");
            }
            구역들.add(new розділ_значення_366e0bfa(종류, позначка_значення, Адреса, Файл_посада, Розмір));
        }
        return new фото(ПУСК_адреса, 구역들);
    }

    private int аналізувати_ціле_число(byte[] дані, int позиція) {
        if (позиція < 0 || позиція > дані.length - 4) {
            throw new IllegalArgumentException("ELF ціле_число 범위를 벗어났습니다.");
        }
        return (дані[позиція] & 0xff)
                | ((дані[позиція + 1] & 0xff) << 8)
                | ((дані[позиція + 2] & 0xff) << 16)
                | ((дані[позиція + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] дані, int позиція) {
        if (позиція < 0 || позиція > дані.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 ціле_число 범위를 벗어났습니다.");
        }
        return (дані[позиція] & 0xff) | ((дані[позиція + 1] & 0xff) << 8);
    }
}
