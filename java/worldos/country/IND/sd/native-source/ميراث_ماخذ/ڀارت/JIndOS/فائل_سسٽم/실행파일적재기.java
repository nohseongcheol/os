// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ڀارت.JIndOS.فائل_سسٽم;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian تعميل_ڪرڻ_حڪم 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class سيڪشن_قدر {
        private final int 종류;
        private final int جهنڊو_قدر;
        private final int پتو;
        private final int 파일위치;
        private final int سائيز;

        سيڪشن_قدر(int 종류, int جهنڊو_قدر, int پتو, int 파일위치, int سائيز) {
            this.종류 = 종류;
            this.جهنڊو_قدر = جهنڊو_قدر;
            this.پتو = پتو;
            this.파일위치 = 파일위치;
            this.سائيز = سائيز;
        }

        public int 종류() {
            return 종류;
        }

        public int جهنڊو_قدر() {
            return جهنڊو_قدر;
        }

        public int پتو() {
            return پتو;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int سائيز() {
            return سائيز;
        }
    }

    public static final class نقش {
        private final int شروع_پتو;
        private final List<سيڪشن_قدر> 구역들;

        نقش(int شروع_پتو, List<سيڪشن_قدر> 구역들) {
            this.شروع_پتو = شروع_پتو;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int شروع_پتو() {
            return شروع_پتو;
        }

        public List<سيڪشن_قدر> 구역들() {
            return 구역들;
        }
    }

    public نقش 검사(byte[] ڪوائف) {
        if (ڪوائف == null || ڪوائف.length < 52
                || ڪوائف[0] != 0x7f || ڪوائف[1] != 'E' || ڪوائف[2] != 'L' || ڪوائف[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (ڪوائف[4] != 1 || ڪوائف[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int شروع_پتو = 정수읽기(ڪوائف, 24);
        int 구역표위치 = 정수읽기(ڪوائف, 32);
        int سيڪشن_داخلا_سائيز = 짧은정수읽기(ڪوائف, 46);
        int 구역수 = 짧은정수읽기(ڪوائف, 48);
        if (سيڪشن_داخلا_سائيز < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) سيڪشن_داخلا_سائيز * 구역수 > ڪوائف.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<سيڪشن_قدر> 구역들 = new ArrayList<سيڪشن_قدر>();
        for (int ابتدائي = 0; ابتدائي < 구역수; ابتدائي++) {
            int 위치 = 구역표위치 + ابتدائي * سيڪشن_داخلا_سائيز;
            int 종류 = 정수읽기(ڪوائف, 위치 + 4);
            int جهنڊو_قدر = 정수읽기(ڪوائف, 위치 + 8);
            int پتو = 정수읽기(ڪوائف, 위치 + 12);
            int 파일위치 = 정수읽기(ڪوائف, 위치 + 16);
            int سائيز = 정수읽기(ڪوائف, 위치 + 20);
            if (سائيز < 0 || (종류 != 8 && ((long) 파일위치 + سائيز > ڪوائف.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF سيڪشن_قدر ڪوائف 범위가 올바르지 않습니다.");
            }
            구역들.add(new سيڪشن_قدر(종류, جهنڊو_قدر, پتو, 파일위치, سائيز));
        }
        return new نقش(شروع_پتو, 구역들);
    }

    private int 정수읽기(byte[] ڪوائف, int 위치) {
        if (위치 < 0 || 위치 > ڪوائف.length - 4) {
            throw new IllegalArgumentException("ELF عدد_صحيح 범위를 벗어났습니다.");
        }
        return (ڪوائف[위치] & 0xff)
                | ((ڪوائف[위치 + 1] & 0xff) << 8)
                | ((ڪوائف[위치 + 2] & 0xff) << 16)
                | ((ڪوائف[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] ڪوائف, int 위치) {
        if (위치 < 0 || 위치 > ڪوائف.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 عدد_صحيح 범위를 벗어났습니다.");
        }
        return (ڪوائف[위치] & 0xff) | ((ڪوائف[위치 + 1] & 0xff) << 8);
    }
}
