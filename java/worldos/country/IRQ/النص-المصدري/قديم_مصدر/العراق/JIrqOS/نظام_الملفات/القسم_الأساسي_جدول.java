// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العراق.JIrqOS.نظام_الملفات;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 قيمة_افتراضية 분할 영역을 읽는다. */
public final class القسم_الأساسي_جدول {
    public static final class قسم_قيمة {
        private final int 종류;
        private final long بدء_قسم;
        private final long 구역수;

        قسم_قيمة(int 종류, long بدء_قسم, long 구역수) {
            this.종류 = 종류;
            this.بدء_قسم = بدء_قسم;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long بدء_قسم() { return بدء_قسم; }
        public long 구역수() { return 구역수; }
    }

    public List<قسم_قيمة> قراءة(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<قسم_قيمة> نتيجة = new ArrayList<قسم_قيمة>();
        for (int فهرس = 0; فهرس < 4; فهرس++) {
            int موضع = 446 + فهرس * 16;
            int 종류 = 첫구역[موضع + 4] & 0xff;
            long تشغيل = 작은순서정수(첫구역, موضع + 8);
            long حجم = 작은순서정수(첫구역, موضع + 12);
            if (종류 != 0 && حجم != 0) {
                نتيجة.add(new قسم_قيمة(종류, تشغيل, حجم));
            }
        }
        return Collections.unmodifiableList(نتيجة);
    }

    private long 작은순서정수(byte[] بيانات, int موضع) {
        return (بيانات[موضع] & 0xffL)
                | ((بيانات[موضع + 1] & 0xffL) << 8)
                | ((بيانات[موضع + 2] & 0xffL) << 16)
                | ((بيانات[موضع + 3] & 0xffL) << 24);
    }
}

