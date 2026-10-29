// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Монгол_Улс.JMngOS.файлын_систем;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 өгөгдмөл_утга 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class тасалгаа_утга {
        private final int 종류;
        private final long Эхлэл_хэсэг;
        private final long 구역수;

        тасалгаа_утга(int 종류, long Эхлэл_хэсэг, long 구역수) {
            this.종류 = 종류;
            this.Эхлэл_хэсэг = Эхлэл_хэсэг;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long Эхлэл_хэсэг() { return Эхлэл_хэсэг; }
        public long 구역수() { return 구역수; }
    }

    public List<тасалгаа_утга> Унших(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<тасалгаа_утга> 결과 = new ArrayList<тасалгаа_утга>();
        for (int индекс = 0; индекс < 4; индекс++) {
            int 위치 = 446 + индекс * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long Ажиллуулах = 작은순서정수(첫구역, 위치 + 8);
            long Хэмжээ = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && Хэмжээ != 0) {
                결과.add(new тасалгаа_утга(종류, Ажиллуулах, Хэмжээ));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] өгөгдөл, int 위치) {
        return (өгөгдөл[위치] & 0xffL)
                | ((өгөгдөл[위치 + 1] & 0xffL) << 8)
                | ((өгөгдөл[위치 + 2] & 0xffL) << 16)
                | ((өгөгдөл[위치 + 3] & 0xffL) << 24);
    }
}

