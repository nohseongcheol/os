// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မျၢၼ်ႇမႃႇ_မိူင်းမၢၼ်ႈ.JMmrOS.파일체계;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian 실행 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class 구역 {
        private final int 종류;
        private final int 깃발;
        private final int 주소;
        private final int 파일위치;
        private final int 크기;

        구역(int 종류, int 깃발, int 주소, int 파일위치, int 크기) {
            this.종류 = 종류;
            this.깃발 = 깃발;
            this.주소 = 주소;
            this.파일위치 = 파일위치;
            this.크기 = 크기;
        }

        public int 종류() {
            return 종류;
        }

        public int 깃발() {
            return 깃발;
        }

        public int 주소() {
            return 주소;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int 크기() {
            return 크기;
        }
    }

    public static final class 실행영상 {
        private final int 시작주소;
        private final List<구역> 구역들;

        실행영상(int 시작주소, List<구역> 구역들) {
            this.시작주소 = 시작주소;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int 시작주소() {
            return 시작주소;
        }

        public List<구역> 구역들() {
            return 구역들;
        }
    }

    public 실행영상 검사(byte[] 자료) {
        if (자료 == null || 자료.length < 52
                || 자료[0] != 0x7f || 자료[1] != 'E' || 자료[2] != 'L' || 자료[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (자료[4] != 1 || 자료[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int 시작주소 = 정수읽기(자료, 24);
        int 구역표위치 = 정수읽기(자료, 32);
        int 구역항목크기 = 짧은정수읽기(자료, 46);
        int 구역수 = 짧은정수읽기(자료, 48);
        if (구역항목크기 < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) 구역항목크기 * 구역수 > 자료.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<구역> 구역들 = new ArrayList<구역>();
        for (int 번호 = 0; 번호 < 구역수; 번호++) {
            int 위치 = 구역표위치 + 번호 * 구역항목크기;
            int 종류 = 정수읽기(자료, 위치 + 4);
            int 깃발 = 정수읽기(자료, 위치 + 8);
            int 주소 = 정수읽기(자료, 위치 + 12);
            int 파일위치 = 정수읽기(자료, 위치 + 16);
            int 크기 = 정수읽기(자료, 위치 + 20);
            if (크기 < 0 || (종류 != 8 && ((long) 파일위치 + 크기 > 자료.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF 구역 자료 범위가 올바르지 않습니다.");
            }
            구역들.add(new 구역(종류, 깃발, 주소, 파일위치, 크기));
        }
        return new 실행영상(시작주소, 구역들);
    }

    private int 정수읽기(byte[] 자료, int 위치) {
        if (위치 < 0 || 위치 > 자료.length - 4) {
            throw new IllegalArgumentException("ELF 정수 범위를 벗어났습니다.");
        }
        return (자료[위치] & 0xff)
                | ((자료[위치 + 1] & 0xff) << 8)
                | ((자료[위치 + 2] & 0xff) << 16)
                | ((자료[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] 자료, int 위치) {
        if (위치 < 0 || 위치 > 자료.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 정수 범위를 벗어났습니다.");
        }
        return (자료[위치] & 0xff) | ((자료[위치 + 1] & 0xff) << 8);
    }
}
