// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package کینیڈا.JCanOS.فائل_نظام;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian نفاذ_کریں_حکم 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class صیغہ_قدر {
        private final int 종류;
        private final int پرچم_قدر;
        private final int پتہ;
        private final int فائل_پوزیشن_ٹھیک_کریں;
        private final int حجم;

        صیغہ_قدر(int 종류, int پرچم_قدر, int پتہ, int فائل_پوزیشن_ٹھیک_کریں, int حجم) {
            this.종류 = 종류;
            this.پرچم_قدر = پرچم_قدر;
            this.پتہ = پتہ;
            this.فائل_پوزیشن_ٹھیک_کریں = فائل_پوزیشن_ٹھیک_کریں;
            this.حجم = حجم;
        }

        public int 종류() {
            return 종류;
        }

        public int پرچم_قدر() {
            return پرچم_قدر;
        }

        public int پتہ() {
            return پتہ;
        }

        public int فائل_پوزیشن_ٹھیک_کریں() {
            return فائل_پوزیشن_ٹھیک_کریں;
        }

        public int حجم() {
            return حجم;
        }
    }

    public static final class نقش {
        private final int ابتدا_پتہ;
        private final List<صیغہ_قدر> 구역들;

        نقش(int ابتدا_پتہ, List<صیغہ_قدر> 구역들) {
            this.ابتدا_پتہ = ابتدا_پتہ;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int ابتدا_پتہ() {
            return ابتدا_پتہ;
        }

        public List<صیغہ_قدر> 구역들() {
            return 구역들;
        }
    }

    public نقش 검사(byte[] کوائف) {
        if (کوائف == null || کوائف.length < 52
                || کوائف[0] != 0x7f || کوائف[1] != 'E' || کوائف[2] != 'L' || کوائف[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (کوائف[4] != 1 || کوائف[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int ابتدا_پتہ = پارس_سالم_عدد(کوائف, 24);
        int صیغہ_جدول_پوزیشن_ٹھیک_کریں = پارس_سالم_عدد(کوائف, 32);
        int صیغہ_اندراج_سائز_دیں = 짧은정수읽기(کوائف, 46);
        int 구역수 = 짧은정수읽기(کوائف, 48);
        if (صیغہ_اندراج_سائز_دیں < 40 || صیغہ_جدول_پوزیشن_ٹھیک_کریں < 0
                || (long) صیغہ_جدول_پوزیشن_ٹھیک_کریں + (long) صیغہ_اندراج_سائز_دیں * 구역수 > کوائف.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<صیغہ_قدر> 구역들 = new ArrayList<صیغہ_قدر>();
        for (int اشاریہ = 0; اشاریہ < 구역수; اشاریہ++) {
            int مقام = صیغہ_جدول_پوزیشن_ٹھیک_کریں + اشاریہ * صیغہ_اندراج_سائز_دیں;
            int 종류 = پارس_سالم_عدد(کوائف, مقام + 4);
            int پرچم_قدر = پارس_سالم_عدد(کوائف, مقام + 8);
            int پتہ = پارس_سالم_عدد(کوائف, مقام + 12);
            int فائل_پوزیشن_ٹھیک_کریں = پارس_سالم_عدد(کوائف, مقام + 16);
            int حجم = پارس_سالم_عدد(کوائف, مقام + 20);
            if (حجم < 0 || (종류 != 8 && ((long) فائل_پوزیشن_ٹھیک_کریں + حجم > کوائف.length || فائل_پوزیشن_ٹھیک_کریں < 0))) {
                throw new IllegalArgumentException("ELF صیغہ_قدر کوائف 범위가 올바르지 않습니다.");
            }
            구역들.add(new صیغہ_قدر(종류, پرچم_قدر, پتہ, فائل_پوزیشن_ٹھیک_کریں, حجم));
        }
        return new نقش(ابتدا_پتہ, 구역들);
    }

    private int پارس_سالم_عدد(byte[] کوائف, int مقام) {
        if (مقام < 0 || مقام > کوائف.length - 4) {
            throw new IllegalArgumentException("ELF سالم_عدد 범위를 벗어났습니다.");
        }
        return (کوائف[مقام] & 0xff)
                | ((کوائف[مقام + 1] & 0xff) << 8)
                | ((کوائف[مقام + 2] & 0xff) << 16)
                | ((کوائف[مقام + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] کوائف, int مقام) {
        if (مقام < 0 || مقام > کوائف.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 سالم_عدد 범위를 벗어났습니다.");
        }
        return (کوائف[مقام] & 0xff) | ((کوائف[مقام + 1] & 0xff) << 8);
    }
}
