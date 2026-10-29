// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاکستان.JPakOS.فائل_سسٹم;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian نفاذ_کرو_حکم 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class سیکشن_قدر {
        private final int 종류;
        private final int جھنڈا_قدر;
        private final int پتا;
        private final int 파일위치;
        private final int سائز;

        سیکشن_قدر(int 종류, int جھنڈا_قدر, int پتا, int 파일위치, int سائز) {
            this.종류 = 종류;
            this.جھنڈا_قدر = جھنڈا_قدر;
            this.پتا = پتا;
            this.파일위치 = 파일위치;
            this.سائز = سائز;
        }

        public int 종류() {
            return 종류;
        }

        public int جھنڈا_قدر() {
            return جھنڈا_قدر;
        }

        public int پتا() {
            return پتا;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int سائز() {
            return سائز;
        }
    }

    public static final class نقش {
        private final int مکھ_پتا;
        private final List<سیکشن_قدر> 구역들;

        نقش(int مکھ_پتا, List<سیکشن_قدر> 구역들) {
            this.مکھ_پتا = مکھ_پتا;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int مکھ_پتا() {
            return مکھ_پتا;
        }

        public List<سیکشن_قدر> 구역들() {
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
        int مکھ_پتا = 정수읽기(کوائف, 24);
        int 구역표위치 = 정수읽기(کوائف, 32);
        int سیکشن_داخلہ_سائز = 짧은정수읽기(کوائف, 46);
        int 구역수 = 짧은정수읽기(کوائف, 48);
        if (سیکشن_داخلہ_سائز < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) سیکشن_داخلہ_سائز * 구역수 > کوائف.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<سیکشن_قدر> 구역들 = new ArrayList<سیکشن_قدر>();
        for (int اشاریہ = 0; اشاریہ < 구역수; اشاریہ++) {
            int 위치 = 구역표위치 + اشاریہ * سیکشن_داخلہ_سائز;
            int 종류 = 정수읽기(کوائف, 위치 + 4);
            int جھنڈا_قدر = 정수읽기(کوائف, 위치 + 8);
            int پتا = 정수읽기(کوائف, 위치 + 12);
            int 파일위치 = 정수읽기(کوائف, 위치 + 16);
            int سائز = 정수읽기(کوائف, 위치 + 20);
            if (سائز < 0 || (종류 != 8 && ((long) 파일위치 + سائز > کوائف.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF سیکشن_قدر کوائف 범위가 올바르지 않습니다.");
            }
            구역들.add(new سیکشن_قدر(종류, جھنڈا_قدر, پتا, 파일위치, سائز));
        }
        return new نقش(مکھ_پتا, 구역들);
    }

    private int 정수읽기(byte[] کوائف, int 위치) {
        if (위치 < 0 || 위치 > کوائف.length - 4) {
            throw new IllegalArgumentException("ELF عدد 범위를 벗어났습니다.");
        }
        return (کوائف[위치] & 0xff)
                | ((کوائف[위치 + 1] & 0xff) << 8)
                | ((کوائف[위치 + 2] & 0xff) << 16)
                | ((کوائف[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] کوائف, int 위치) {
        if (위치 < 0 || 위치 > کوائف.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 عدد 범위를 벗어났습니다.");
        }
        return (کوائف[위치] & 0xff) | ((کوائف[위치 + 1] & 0xff) << 8);
    }
}
