// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Тоҷикистон.JTjkOS.системаи_файлӣ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian иҷро_кардан_фармон 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class қисмат_қимат {
        private final int 종류;
        private final int байрақ_қимат;
        private final int суроға;
        private final int 파일위치;
        private final int андоза_кардан;

        қисмат_қимат(int 종류, int байрақ_қимат, int суроға, int 파일위치, int андоза_кардан) {
            this.종류 = 종류;
            this.байрақ_қимат = байрақ_қимат;
            this.суроға = суроға;
            this.파일위치 = 파일위치;
            this.андоза_кардан = андоза_кардан;
        }

        public int 종류() {
            return 종류;
        }

        public int байрақ_қимат() {
            return байрақ_қимат;
        }

        public int суроға() {
            return суроға;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int андоза_кардан() {
            return андоза_кардан;
        }
    }

    public static final class расм {
        private final int Оғоз_суроға;
        private final List<қисмат_қимат> 구역들;

        расм(int Оғоз_суроға, List<қисмат_қимат> 구역들) {
            this.Оғоз_суроға = Оғоз_суроға;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Оғоз_суроға() {
            return Оғоз_суроға;
        }

        public List<қисмат_қимат> 구역들() {
            return 구역들;
        }
    }

    public расм 검사(byte[] иттилоот) {
        if (иттилоот == null || иттилоот.length < 52
                || иттилоот[0] != 0x7f || иттилоот[1] != 'E' || иттилоот[2] != 'L' || иттилоот[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (иттилоот[4] != 1 || иттилоот[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Оғоз_суроға = 정수읽기(иттилоот, 24);
        int 구역표위치 = 정수읽기(иттилоот, 32);
        int қисмат_ворида_андоза_кардан = 짧은정수읽기(иттилоот, 46);
        int 구역수 = 짧은정수읽기(иттилоот, 48);
        if (қисмат_ворида_андоза_кардан < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) қисмат_ворида_андоза_кардан * 구역수 > иттилоот.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<қисмат_қимат> 구역들 = new ArrayList<қисмат_қимат>();
        for (int индекс = 0; индекс < 구역수; индекс++) {
            int 위치 = 구역표위치 + индекс * қисмат_ворида_андоза_кардан;
            int 종류 = 정수읽기(иттилоот, 위치 + 4);
            int байрақ_қимат = 정수읽기(иттилоот, 위치 + 8);
            int суроға = 정수읽기(иттилоот, 위치 + 12);
            int 파일위치 = 정수읽기(иттилоот, 위치 + 16);
            int андоза_кардан = 정수읽기(иттилоот, 위치 + 20);
            if (андоза_кардан < 0 || (종류 != 8 && ((long) 파일위치 + андоза_кардан > иттилоот.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF қисмат_қимат иттилоот 범위가 올바르지 않습니다.");
            }
            구역들.add(new қисмат_қимат(종류, байрақ_қимат, суроға, 파일위치, андоза_кардан));
        }
        return new расм(Оғоз_суроға, 구역들);
    }

    private int 정수읽기(byte[] иттилоот, int 위치) {
        if (위치 < 0 || 위치 > иттилоот.length - 4) {
            throw new IllegalArgumentException("ELF адади_яклухт 범위를 벗어났습니다.");
        }
        return (иттилоот[위치] & 0xff)
                | ((иттилоот[위치 + 1] & 0xff) << 8)
                | ((иттилоот[위치 + 2] & 0xff) << 16)
                | ((иттилоот[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] иттилоот, int 위치) {
        if (위치 < 0 || 위치 > иттилоот.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 адади_яклухт 범위를 벗어났습니다.");
        }
        return (иттилоот[위치] & 0xff) | ((иттилоот[위치 + 1] & 0xff) << 8);
    }
}
