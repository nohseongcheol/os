// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Кыргызстан.JKgzOS.файл_тутуму;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 жарыяланбаган_маани 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class бөлүк_маани {
        private final int 종류;
        private final long Баштоо_бөлүк;
        private final long 구역수;

        бөлүк_маани(int 종류, long Баштоо_бөлүк, long 구역수) {
            this.종류 = 종류;
            this.Баштоо_бөлүк = Баштоо_бөлүк;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long Баштоо_бөлүк() { return Баштоо_бөлүк; }
        public long 구역수() { return 구역수; }
    }

    public List<бөлүк_маани> Окуу(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<бөлүк_маани> 결과 = new ArrayList<бөлүк_маани>();
        for (int индекс = 0; индекс < 4; индекс++) {
            int Турган_жери = 446 + индекс * 16;
            int 종류 = 첫구역[Турган_жери + 4] & 0xff;
            long Жүргүзүү = 작은순서정수(첫구역, Турган_жери + 8);
            long Өлчөмү = 작은순서정수(첫구역, Турган_жери + 12);
            if (종류 != 0 && Өлчөмү != 0) {
                결과.add(new бөлүк_маани(종류, Жүргүзүү, Өлчөмү));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] берилмелер, int Турган_жери) {
        return (берилмелер[Турган_жери] & 0xffL)
                | ((берилмелер[Турган_жери + 1] & 0xffL) << 8)
                | ((берилмелер[Турган_жери + 2] & 0xffL) << 16)
                | ((берилмелер[Турган_жери + 3] & 0xffL) << 24);
    }
}

