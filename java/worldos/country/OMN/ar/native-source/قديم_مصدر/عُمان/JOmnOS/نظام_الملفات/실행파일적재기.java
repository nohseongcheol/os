// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package عُمان.JOmnOS.نظام_الملفات;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian ينفذ_أمر 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class قسم_قيمة_366e0bfa {
        private final int 종류;
        private final int إشارة_قيمة;
        private final int عنوان;
        private final int ملف_منصب;
        private final int حجم;

        قسم_قيمة_366e0bfa(int 종류, int إشارة_قيمة, int عنوان, int ملف_منصب, int حجم) {
            this.종류 = 종류;
            this.إشارة_قيمة = إشارة_قيمة;
            this.عنوان = عنوان;
            this.ملف_منصب = ملف_منصب;
            this.حجم = حجم;
        }

        public int 종류() {
            return 종류;
        }

        public int إشارة_قيمة() {
            return إشارة_قيمة;
        }

        public int عنوان() {
            return عنوان;
        }

        public int ملف_منصب() {
            return ملف_منصب;
        }

        public int حجم() {
            return حجم;
        }
    }

    public static final class صورة {
        private final int بدء_عنوان;
        private final List<قسم_قيمة_366e0bfa> 구역들;

        صورة(int بدء_عنوان, List<قسم_قيمة_366e0bfa> 구역들) {
            this.بدء_عنوان = بدء_عنوان;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int بدء_عنوان() {
            return بدء_عنوان;
        }

        public List<قسم_قيمة_366e0bfa> 구역들() {
            return 구역들;
        }
    }

    public صورة 검사(byte[] بيانات) {
        if (بيانات == null || بيانات.length < 52
                || بيانات[0] != 0x7f || بيانات[1] != 'E' || بيانات[2] != 'L' || بيانات[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (بيانات[4] != 1 || بيانات[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int بدء_عنوان = يوزّع_عدد_صحيح(بيانات, 24);
        int قسم_جدول_منصب = يوزّع_عدد_صحيح(بيانات, 32);
        int قسم_إدخال_يغير_الحجم = 짧은정수읽기(بيانات, 46);
        int 구역수 = 짧은정수읽기(بيانات, 48);
        if (قسم_إدخال_يغير_الحجم < 40 || قسم_جدول_منصب < 0
                || (long) قسم_جدول_منصب + (long) قسم_إدخال_يغير_الحجم * 구역수 > بيانات.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<قسم_قيمة_366e0bfa> 구역들 = new ArrayList<قسم_قيمة_366e0bfa>();
        for (int فهرس = 0; فهرس < 구역수; فهرس++) {
            int موضع = قسم_جدول_منصب + فهرس * قسم_إدخال_يغير_الحجم;
            int 종류 = يوزّع_عدد_صحيح(بيانات, موضع + 4);
            int إشارة_قيمة = يوزّع_عدد_صحيح(بيانات, موضع + 8);
            int عنوان = يوزّع_عدد_صحيح(بيانات, موضع + 12);
            int ملف_منصب = يوزّع_عدد_صحيح(بيانات, موضع + 16);
            int حجم = يوزّع_عدد_صحيح(بيانات, موضع + 20);
            if (حجم < 0 || (종류 != 8 && ((long) ملف_منصب + حجم > بيانات.length || ملف_منصب < 0))) {
                throw new IllegalArgumentException("ELF قسم_قيمة_366e0bfa بيانات 범위가 올바르지 않습니다.");
            }
            구역들.add(new قسم_قيمة_366e0bfa(종류, إشارة_قيمة, عنوان, ملف_منصب, حجم));
        }
        return new صورة(بدء_عنوان, 구역들);
    }

    private int يوزّع_عدد_صحيح(byte[] بيانات, int موضع) {
        if (موضع < 0 || موضع > بيانات.length - 4) {
            throw new IllegalArgumentException("ELF عدد_صحيح 범위를 벗어났습니다.");
        }
        return (بيانات[موضع] & 0xff)
                | ((بيانات[موضع + 1] & 0xff) << 8)
                | ((بيانات[موضع + 2] & 0xff) << 16)
                | ((بيانات[موضع + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] بيانات, int موضع) {
        if (موضع < 0 || موضع > بيانات.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 عدد_صحيح 범위를 벗어났습니다.");
        }
        return (بيانات[موضع] & 0xff) | ((بيانات[موضع + 1] & 0xff) << 8);
    }
}
