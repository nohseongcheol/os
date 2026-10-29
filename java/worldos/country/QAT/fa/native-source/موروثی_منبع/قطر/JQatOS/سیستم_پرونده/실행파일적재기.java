// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package قطر.JQatOS.سیستم_پرونده;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian اجرا_فرمان 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class قسمت_مقدار {
        private final int 종류;
        private final int پرچم_مقدار;
        private final int آدرس;
        private final int فایل_مرتب_کردن;
        private final int اندازه;

        قسمت_مقدار(int 종류, int پرچم_مقدار, int آدرس, int فایل_مرتب_کردن, int اندازه) {
            this.종류 = 종류;
            this.پرچم_مقدار = پرچم_مقدار;
            this.آدرس = آدرس;
            this.فایل_مرتب_کردن = فایل_مرتب_کردن;
            this.اندازه = اندازه;
        }

        public int 종류() {
            return 종류;
        }

        public int پرچم_مقدار() {
            return پرچم_مقدار;
        }

        public int آدرس() {
            return آدرس;
        }

        public int فایل_مرتب_کردن() {
            return فایل_مرتب_کردن;
        }

        public int اندازه() {
            return اندازه;
        }
    }

    public static final class عکس {
        private final int شروع_آدرس;
        private final List<قسمت_مقدار> 구역들;

        عکس(int شروع_آدرس, List<قسمت_مقدار> 구역들) {
            this.شروع_آدرس = شروع_آدرس;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int شروع_آدرس() {
            return شروع_آدرس;
        }

        public List<قسمت_مقدار> 구역들() {
            return 구역들;
        }
    }

    public عکس 검사(byte[] داده_ها) {
        if (داده_ها == null || داده_ها.length < 52
                || داده_ها[0] != 0x7f || داده_ها[1] != 'E' || داده_ها[2] != 'L' || داده_ها[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (داده_ها[4] != 1 || داده_ها[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int شروع_آدرس = تفسیر_عدد_صحیح(داده_ها, 24);
        int قسمت_جدول_مرتب_کردن = تفسیر_عدد_صحیح(داده_ها, 32);
        int قسمت_ورودی_اندازه_کردن = 짧은정수읽기(داده_ها, 46);
        int 구역수 = 짧은정수읽기(داده_ها, 48);
        if (قسمت_ورودی_اندازه_کردن < 40 || قسمت_جدول_مرتب_کردن < 0
                || (long) قسمت_جدول_مرتب_کردن + (long) قسمت_ورودی_اندازه_کردن * 구역수 > داده_ها.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<قسمت_مقدار> 구역들 = new ArrayList<قسمت_مقدار>();
        for (int فهرست = 0; فهرست < 구역수; فهرست++) {
            int مرتب_کردن = قسمت_جدول_مرتب_کردن + فهرست * قسمت_ورودی_اندازه_کردن;
            int 종류 = تفسیر_عدد_صحیح(داده_ها, مرتب_کردن + 4);
            int پرچم_مقدار = تفسیر_عدد_صحیح(داده_ها, مرتب_کردن + 8);
            int آدرس = تفسیر_عدد_صحیح(داده_ها, مرتب_کردن + 12);
            int فایل_مرتب_کردن = تفسیر_عدد_صحیح(داده_ها, مرتب_کردن + 16);
            int اندازه = تفسیر_عدد_صحیح(داده_ها, مرتب_کردن + 20);
            if (اندازه < 0 || (종류 != 8 && ((long) فایل_مرتب_کردن + اندازه > داده_ها.length || فایل_مرتب_کردن < 0))) {
                throw new IllegalArgumentException("ELF قسمت_مقدار داده_ها 범위가 올바르지 않습니다.");
            }
            구역들.add(new قسمت_مقدار(종류, پرچم_مقدار, آدرس, فایل_مرتب_کردن, اندازه));
        }
        return new عکس(شروع_آدرس, 구역들);
    }

    private int تفسیر_عدد_صحیح(byte[] داده_ها, int مرتب_کردن) {
        if (مرتب_کردن < 0 || مرتب_کردن > داده_ها.length - 4) {
            throw new IllegalArgumentException("ELF عدد_صحیح 범위를 벗어났습니다.");
        }
        return (داده_ها[مرتب_کردن] & 0xff)
                | ((داده_ها[مرتب_کردن + 1] & 0xff) << 8)
                | ((داده_ها[مرتب_کردن + 2] & 0xff) << 16)
                | ((داده_ها[مرتب_کردن + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] داده_ها, int مرتب_کردن) {
        if (مرتب_کردن < 0 || مرتب_کردن > داده_ها.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 عدد_صحیح 범위를 벗어났습니다.");
        }
        return (داده_ها[مرتب_کردن] & 0xff) | ((داده_ها[مرتب_کردن + 1] & 0xff) << 8);
    }
}
