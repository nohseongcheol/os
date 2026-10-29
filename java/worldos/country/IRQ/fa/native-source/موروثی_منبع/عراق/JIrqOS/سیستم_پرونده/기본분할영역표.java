// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package عراق.JIrqOS.سیستم_پرونده;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 مقدار_پیش_فرض 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class پارتیشن_مقدار {
        private final int 종류;
        private final long شروع_قسمت;
        private final long 구역수;

        پارتیشن_مقدار(int 종류, long شروع_قسمت, long 구역수) {
            this.종류 = 종류;
            this.شروع_قسمت = شروع_قسمت;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long شروع_قسمت() { return شروع_قسمت; }
        public long 구역수() { return 구역수; }
    }

    public List<پارتیشن_مقدار> خواندن(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<پارتیشن_مقدار> سنجش = new ArrayList<پارتیشن_مقدار>();
        for (int فهرست = 0; فهرست < 4; فهرست++) {
            int مرتب_کردن = 446 + فهرست * 16;
            int 종류 = 첫구역[مرتب_کردن + 4] & 0xff;
            long اجرا_2 = 작은순서정수(첫구역, مرتب_کردن + 8);
            long اندازه = 작은순서정수(첫구역, مرتب_کردن + 12);
            if (종류 != 0 && اندازه != 0) {
                سنجش.add(new پارتیشن_مقدار(종류, اجرا_2, اندازه));
            }
        }
        return Collections.unmodifiableList(سنجش);
    }

    private long 작은순서정수(byte[] داده_ها, int مرتب_کردن) {
        return (داده_ها[مرتب_کردن] & 0xffL)
                | ((داده_ها[مرتب_کردن + 1] & 0xffL) << 8)
                | ((داده_ها[مرتب_کردن + 2] & 0xffL) << 16)
                | ((داده_ها[مرتب_کردن + 3] & 0xffL) << 24);
    }
}

