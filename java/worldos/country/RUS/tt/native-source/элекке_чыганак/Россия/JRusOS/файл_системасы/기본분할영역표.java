// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Россия.JRusOS.файл_системасы;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 килешенгәнчә_кыйммәт 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class бүлем_VALUE {
        private final int 종류;
        private final long Start_өлеш;
        private final long өлеш_COUNT;

        бүлем_VALUE(int 종류, long Start_өлеш, long өлеш_COUNT) {
            this.종류 = 종류;
            this.Start_өлеш = Start_өлеш;
            this.өлеш_COUNT = өлеш_COUNT;
        }

        public int 종류() { return 종류; }
        public long Start_өлеш() { return Start_өлеш; }
        public long өлеш_COUNT() { return өлеш_COUNT; }
    }

    public List<бүлем_VALUE> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<бүлем_VALUE> үлчәм = new ArrayList<бүлем_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int урнаштыру = 446 + INDEX * 16;
            int 종류 = 첫구역[урнаштыру + 4] & 0xff;
            long эшләтү = 작은순서정수(첫구역, урнаштыру + 8);
            long үлчәмен_үзгәртү = 작은순서정수(첫구역, урнаштыру + 12);
            if (종류 != 0 && үлчәмен_үзгәртү != 0) {
                үлчәм.add(new бүлем_VALUE(종류, эшләтү, үлчәмен_үзгәртү));
            }
        }
        return Collections.unmodifiableList(үлчәм);
    }

    private long 작은순서정수(byte[] мәгълүмат, int урнаштыру) {
        return (мәгълүмат[урнаштыру] & 0xffL)
                | ((мәгълүмат[урнаштыру + 1] & 0xffL) << 8)
                | ((мәгълүмат[урнаштыру + 2] & 0xffL) << 16)
                | ((мәгълүмат[урнаштыру + 3] & 0xffL) << 24);
    }
}

