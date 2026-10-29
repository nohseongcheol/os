// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Россия.JRusOS.файл_системасы;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian үтәргә_команда 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class өлеш_VALUE {
        private final int 종류;
        private final int тамга_кую_VALUE;
        private final int адрес;
        private final int файл_урнаштыру;
        private final int үлчәмен_үзгәртү;

        өлеш_VALUE(int 종류, int тамга_кую_VALUE, int адрес, int файл_урнаштыру, int үлчәмен_үзгәртү) {
            this.종류 = 종류;
            this.тамга_кую_VALUE = тамга_кую_VALUE;
            this.адрес = адрес;
            this.файл_урнаштыру = файл_урнаштыру;
            this.үлчәмен_үзгәртү = үлчәмен_үзгәртү;
        }

        public int 종류() {
            return 종류;
        }

        public int тамга_кую_VALUE() {
            return тамга_кую_VALUE;
        }

        public int адрес() {
            return адрес;
        }

        public int файл_урнаштыру() {
            return файл_урнаштыру;
        }

        public int үлчәмен_үзгәртү() {
            return үлчәмен_үзгәртү;
        }
    }

    public static final class IMAGE {
        private final int Start_адрес;
        private final List<өлеш_VALUE> 구역들;

        IMAGE(int Start_адрес, List<өлеш_VALUE> 구역들) {
            this.Start_адрес = Start_адрес;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Start_адрес() {
            return Start_адрес;
        }

        public List<өлеш_VALUE> 구역들() {
            return 구역들;
        }
    }

    public IMAGE 검사(byte[] мәгълүмат) {
        if (мәгълүмат == null || мәгълүмат.length < 52
                || мәгълүмат[0] != 0x7f || мәгълүмат[1] != 'E' || мәгълүмат[2] != 'L' || мәгълүмат[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (мәгълүмат[4] != 1 || мәгълүмат[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Start_адрес = бүлү_бөтен_сан(мәгълүмат, 24);
        int өлеш_таблица_урнаштыру = бүлү_бөтен_сан(мәгълүмат, 32);
        int өлеш_кертү_үлчәмен_үзгәртү = 짧은정수읽기(мәгълүмат, 46);
        int өлеш_COUNT = 짧은정수읽기(мәгълүмат, 48);
        if (өлеш_кертү_үлчәмен_үзгәртү < 40 || өлеш_таблица_урнаштыру < 0
                || (long) өлеш_таблица_урнаштыру + (long) өлеш_кертү_үлчәмен_үзгәртү * өлеш_COUNT > мәгълүмат.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<өлеш_VALUE> 구역들 = new ArrayList<өлеш_VALUE>();
        for (int INDEX = 0; INDEX < өлеш_COUNT; INDEX++) {
            int урнаштыру = өлеш_таблица_урнаштыру + INDEX * өлеш_кертү_үлчәмен_үзгәртү;
            int 종류 = бүлү_бөтен_сан(мәгълүмат, урнаштыру + 4);
            int тамга_кую_VALUE = бүлү_бөтен_сан(мәгълүмат, урнаштыру + 8);
            int адрес = бүлү_бөтен_сан(мәгълүмат, урнаштыру + 12);
            int файл_урнаштыру = бүлү_бөтен_сан(мәгълүмат, урнаштыру + 16);
            int үлчәмен_үзгәртү = бүлү_бөтен_сан(мәгълүмат, урнаштыру + 20);
            if (үлчәмен_үзгәртү < 0 || (종류 != 8 && ((long) файл_урнаштыру + үлчәмен_үзгәртү > мәгълүмат.length || файл_урнаштыру < 0))) {
                throw new IllegalArgumentException("ELF өлеш_VALUE мәгълүмат 범위가 올바르지 않습니다.");
            }
            구역들.add(new өлеш_VALUE(종류, тамга_кую_VALUE, адрес, файл_урнаштыру, үлчәмен_үзгәртү));
        }
        return new IMAGE(Start_адрес, 구역들);
    }

    private int бүлү_бөтен_сан(byte[] мәгълүмат, int урнаштыру) {
        if (урнаштыру < 0 || урнаштыру > мәгълүмат.length - 4) {
            throw new IllegalArgumentException("ELF бөтен_сан 범위를 벗어났습니다.");
        }
        return (мәгълүмат[урнаштыру] & 0xff)
                | ((мәгълүмат[урнаштыру + 1] & 0xff) << 8)
                | ((мәгълүмат[урнаштыру + 2] & 0xff) << 16)
                | ((мәгълүмат[урнаштыру + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] мәгълүмат, int урнаштыру) {
        if (урнаштыру < 0 || урнаштыру > мәгълүмат.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 бөтен_сан 범위를 벗어났습니다.");
        }
        return (мәгълүмат[урнаштыру] & 0xff) | ((мәгълүмат[урнаштыру + 1] & 0xff) << 8);
    }
}
