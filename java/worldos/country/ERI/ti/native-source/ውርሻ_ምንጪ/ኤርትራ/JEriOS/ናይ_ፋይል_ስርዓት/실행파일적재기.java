// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኤርትራ.JEriOS.ናይ_ፋይል_ስርዓት;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian ተግብር_ትእዛዝ 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class ክፋል_ዋጋ {
        private final int 종류;
        private final int ባንዴራ_ዋጋ;
        private final int ኣድራሻ;
        private final int 파일위치;
        private final int መጠን;

        ክፋል_ዋጋ(int 종류, int ባንዴራ_ዋጋ, int ኣድራሻ, int 파일위치, int መጠን) {
            this.종류 = 종류;
            this.ባንዴራ_ዋጋ = ባንዴራ_ዋጋ;
            this.ኣድራሻ = ኣድራሻ;
            this.파일위치 = 파일위치;
            this.መጠን = መጠን;
        }

        public int 종류() {
            return 종류;
        }

        public int ባንዴራ_ዋጋ() {
            return ባንዴራ_ዋጋ;
        }

        public int ኣድራሻ() {
            return ኣድራሻ;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int መጠን() {
            return መጠን;
        }
    }

    public static final class ምስሊ {
        private final int ጀምር_ኣድራሻ;
        private final List<ክፋል_ዋጋ> 구역들;

        ምስሊ(int ጀምር_ኣድራሻ, List<ክፋል_ዋጋ> 구역들) {
            this.ጀምር_ኣድራሻ = ጀምር_ኣድራሻ;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int ጀምር_ኣድራሻ() {
            return ጀምር_ኣድራሻ;
        }

        public List<ክፋል_ዋጋ> 구역들() {
            return 구역들;
        }
    }

    public ምስሊ 검사(byte[] ሓበሬታ) {
        if (ሓበሬታ == null || ሓበሬታ.length < 52
                || ሓበሬታ[0] != 0x7f || ሓበሬታ[1] != 'E' || ሓበሬታ[2] != 'L' || ሓበሬታ[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (ሓበሬታ[4] != 1 || ሓበሬታ[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int ጀምር_ኣድራሻ = 정수읽기(ሓበሬታ, 24);
        int 구역표위치 = 정수읽기(ሓበሬታ, 32);
        int ክፋል_ምእታው_መጠን = 짧은정수읽기(ሓበሬታ, 46);
        int 구역수 = 짧은정수읽기(ሓበሬታ, 48);
        if (ክፋል_ምእታው_መጠን < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) ክፋል_ምእታው_መጠን * 구역수 > ሓበሬታ.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<ክፋል_ዋጋ> 구역들 = new ArrayList<ክፋል_ዋጋ>();
        for (int መሐበሪ = 0; መሐበሪ < 구역수; መሐበሪ++) {
            int 위치 = 구역표위치 + መሐበሪ * ክፋል_ምእታው_መጠን;
            int 종류 = 정수읽기(ሓበሬታ, 위치 + 4);
            int ባንዴራ_ዋጋ = 정수읽기(ሓበሬታ, 위치 + 8);
            int ኣድራሻ = 정수읽기(ሓበሬታ, 위치 + 12);
            int 파일위치 = 정수읽기(ሓበሬታ, 위치 + 16);
            int መጠን = 정수읽기(ሓበሬታ, 위치 + 20);
            if (መጠን < 0 || (종류 != 8 && ((long) 파일위치 + መጠን > ሓበሬታ.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF ክፋል_ዋጋ ሓበሬታ 범위가 올바르지 않습니다.");
            }
            구역들.add(new ክፋል_ዋጋ(종류, ባንዴራ_ዋጋ, ኣድራሻ, 파일위치, መጠን));
        }
        return new ምስሊ(ጀምር_ኣድራሻ, 구역들);
    }

    private int 정수읽기(byte[] ሓበሬታ, int 위치) {
        if (위치 < 0 || 위치 > ሓበሬታ.length - 4) {
            throw new IllegalArgumentException("ELF ኢንቲጀር 범위를 벗어났습니다.");
        }
        return (ሓበሬታ[위치] & 0xff)
                | ((ሓበሬታ[위치 + 1] & 0xff) << 8)
                | ((ሓበሬታ[위치 + 2] & 0xff) << 16)
                | ((ሓበሬታ[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] ሓበሬታ, int 위치) {
        if (위치 < 0 || 위치 > ሓበሬታ.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 ኢንቲጀር 범위를 벗어났습니다.");
        }
        return (ሓበሬታ[위치] & 0xff) | ((ሓበሬታ[위치 + 1] & 0xff) << 8);
    }
}
