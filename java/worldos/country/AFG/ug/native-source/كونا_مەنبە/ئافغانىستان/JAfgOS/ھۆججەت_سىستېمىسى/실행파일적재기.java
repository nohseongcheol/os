// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ئافغانىستان.JAfgOS.ھۆججەت_سىستېمىسى;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian ئىجرا_قىلىش_بۇيرۇق 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class بۆلۈم_قىممىتى {
        private final int 종류;
        private final int بەلگە_قىممىتى_58846146;
        private final int ئادرېس;
        private final int ھۆججەت_ئورۇنلاشتۇرۇش;
        private final int چوڭلۇقى;

        بۆلۈم_قىممىتى(int 종류, int بەلگە_قىممىتى_58846146, int ئادرېس, int ھۆججەت_ئورۇنلاشتۇرۇش, int چوڭلۇقى) {
            this.종류 = 종류;
            this.بەلگە_قىممىتى_58846146 = بەلگە_قىممىتى_58846146;
            this.ئادرېس = ئادرېس;
            this.ھۆججەت_ئورۇنلاشتۇرۇش = ھۆججەت_ئورۇنلاشتۇرۇش;
            this.چوڭلۇقى = چوڭلۇقى;
        }

        public int 종류() {
            return 종류;
        }

        public int بەلگە_قىممىتى_58846146() {
            return بەلگە_قىممىتى_58846146;
        }

        public int ئادرېس() {
            return ئادرېس;
        }

        public int ھۆججەت_ئورۇنلاشتۇرۇش() {
            return ھۆججەت_ئورۇنلاشتۇرۇش;
        }

        public int چوڭلۇقى() {
            return چوڭلۇقى;
        }
    }

    public static final class رەسىم {
        private final int باشلاش_ئادرېس;
        private final List<بۆلۈم_قىممىتى> 구역들;

        رەسىم(int باشلاش_ئادرېس, List<بۆلۈم_قىممىتى> 구역들) {
            this.باشلاش_ئادرېس = باشلاش_ئادرېس;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int باشلاش_ئادرېس() {
            return باشلاش_ئادرېس;
        }

        public List<بۆلۈم_قىممىتى> 구역들() {
            return 구역들;
        }
    }

    public رەسىم 검사(byte[] مەلۇمات) {
        if (مەلۇمات == null || مەلۇمات.length < 52
                || مەلۇمات[0] != 0x7f || مەلۇمات[1] != 'E' || مەلۇمات[2] != 'L' || مەلۇمات[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (مەلۇمات[4] != 1 || مەلۇمات[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int باشلاش_ئادرېس = 정수읽기(مەلۇمات, 24);
        int بۆلۈم_جەدۋەل_ئورۇنلاشتۇرۇش = 정수읽기(مەلۇمات, 32);
        int بۆلۈم_كىرگۈزۈش_ئۆزگەرتمەك = 짧은정수읽기(مەلۇمات, 46);
        int 구역수 = 짧은정수읽기(مەلۇمات, 48);
        if (بۆلۈم_كىرگۈزۈش_ئۆزگەرتمەك < 40 || بۆلۈم_جەدۋەل_ئورۇنلاشتۇرۇش < 0
                || (long) بۆلۈم_جەدۋەل_ئورۇنلاشتۇرۇش + (long) بۆلۈم_كىرگۈزۈش_ئۆزگەرتمەك * 구역수 > مەلۇمات.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<بۆلۈم_قىممىتى> 구역들 = new ArrayList<بۆلۈم_قىممىتى>();
        for (int ئىندېكس = 0; ئىندېكس < 구역수; ئىندېكس++) {
            int ئورۇن = بۆلۈم_جەدۋەل_ئورۇنلاشتۇرۇش + ئىندېكس * بۆلۈم_كىرگۈزۈش_ئۆزگەرتمەك;
            int 종류 = 정수읽기(مەلۇمات, ئورۇن + 4);
            int بەلگە_قىممىتى_58846146 = 정수읽기(مەلۇمات, ئورۇن + 8);
            int ئادرېس = 정수읽기(مەلۇمات, ئورۇن + 12);
            int ھۆججەت_ئورۇنلاشتۇرۇش = 정수읽기(مەلۇمات, ئورۇن + 16);
            int چوڭلۇقى = 정수읽기(مەلۇمات, ئورۇن + 20);
            if (چوڭلۇقى < 0 || (종류 != 8 && ((long) ھۆججەت_ئورۇنلاشتۇرۇش + چوڭلۇقى > مەلۇمات.length || ھۆججەت_ئورۇنلاشتۇرۇش < 0))) {
                throw new IllegalArgumentException("ELF بۆلۈم_قىممىتى مەلۇمات 범위가 올바르지 않습니다.");
            }
            구역들.add(new بۆلۈم_قىممىتى(종류, بەلگە_قىممىتى_58846146, ئادرېس, ھۆججەت_ئورۇنلاشتۇرۇش, چوڭلۇقى));
        }
        return new رەسىم(باشلاش_ئادرېس, 구역들);
    }

    private int 정수읽기(byte[] مەلۇمات, int ئورۇن) {
        if (ئورۇن < 0 || ئورۇن > مەلۇمات.length - 4) {
            throw new IllegalArgumentException("ELF پۈتۈن_سان 범위를 벗어났습니다.");
        }
        return (مەلۇمات[ئورۇن] & 0xff)
                | ((مەلۇمات[ئورۇن + 1] & 0xff) << 8)
                | ((مەلۇمات[ئورۇن + 2] & 0xff) << 16)
                | ((مەلۇمات[ئورۇن + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] مەلۇمات, int ئورۇن) {
        if (ئورۇن < 0 || ئورۇن > مەلۇمات.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 پۈتۈن_سان 범위를 벗어났습니다.");
        }
        return (مەلۇمات[ئورۇن] & 0xff) | ((مەلۇمات[ئورۇن + 1] & 0xff) << 8);
    }
}
