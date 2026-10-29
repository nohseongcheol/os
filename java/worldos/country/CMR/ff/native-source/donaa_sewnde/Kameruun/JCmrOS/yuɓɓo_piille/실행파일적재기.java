// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Kameruun.JCmrOS.yuɓɓo_piille;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian 실행 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class taƴre_njaru {
        private final int 종류;
        private final int maantaade_njaru;
        private final int ñiiɓirde;
        private final int 파일위치;
        private final int waylude_etannde;

        taƴre_njaru(int 종류, int maantaade_njaru, int ñiiɓirde, int 파일위치, int waylude_etannde) {
            this.종류 = 종류;
            this.maantaade_njaru = maantaade_njaru;
            this.ñiiɓirde = ñiiɓirde;
            this.파일위치 = 파일위치;
            this.waylude_etannde = waylude_etannde;
        }

        public int 종류() {
            return 종류;
        }

        public int maantaade_njaru() {
            return maantaade_njaru;
        }

        public int ñiiɓirde() {
            return ñiiɓirde;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int waylude_etannde() {
            return waylude_etannde;
        }
    }

    public static final class natal {
        private final int huɓɓude_ñiiɓirde;
        private final List<taƴre_njaru> 구역들;

        natal(int huɓɓude_ñiiɓirde, List<taƴre_njaru> 구역들) {
            this.huɓɓude_ñiiɓirde = huɓɓude_ñiiɓirde;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int huɓɓude_ñiiɓirde() {
            return huɓɓude_ñiiɓirde;
        }

        public List<taƴre_njaru> 구역들() {
            return 구역들;
        }
    }

    public natal 검사(byte[] keɓe) {
        if (keɓe == null || keɓe.length < 52
                || keɓe[0] != 0x7f || keɓe[1] != 'E' || keɓe[2] != 'L' || keɓe[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (keɓe[4] != 1 || keɓe[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int huɓɓude_ñiiɓirde = 정수읽기(keɓe, 24);
        int 구역표위치 = 정수읽기(keɓe, 32);
        int taƴre_naatnugol_waylude_etannde = 짧은정수읽기(keɓe, 46);
        int 구역수 = 짧은정수읽기(keɓe, 48);
        if (taƴre_naatnugol_waylude_etannde < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) taƴre_naatnugol_waylude_etannde * 구역수 > keɓe.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<taƴre_njaru> 구역들 = new ArrayList<taƴre_njaru>();
        for (int joopirdu = 0; joopirdu < 구역수; joopirdu++) {
            int 위치 = 구역표위치 + joopirdu * taƴre_naatnugol_waylude_etannde;
            int 종류 = 정수읽기(keɓe, 위치 + 4);
            int maantaade_njaru = 정수읽기(keɓe, 위치 + 8);
            int ñiiɓirde = 정수읽기(keɓe, 위치 + 12);
            int 파일위치 = 정수읽기(keɓe, 위치 + 16);
            int waylude_etannde = 정수읽기(keɓe, 위치 + 20);
            if (waylude_etannde < 0 || (종류 != 8 && ((long) 파일위치 + waylude_etannde > keɓe.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF taƴre_njaru keɓe 범위가 올바르지 않습니다.");
            }
            구역들.add(new taƴre_njaru(종류, maantaade_njaru, ñiiɓirde, 파일위치, waylude_etannde));
        }
        return new natal(huɓɓude_ñiiɓirde, 구역들);
    }

    private int 정수읽기(byte[] keɓe, int 위치) {
        if (위치 < 0 || 위치 > keɓe.length - 4) {
            throw new IllegalArgumentException("ELF 정수 범위를 벗어났습니다.");
        }
        return (keɓe[위치] & 0xff)
                | ((keɓe[위치 + 1] & 0xff) << 8)
                | ((keɓe[위치 + 2] & 0xff) << 16)
                | ((keɓe[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] keɓe, int 위치) {
        if (위치 < 0 || 위치 > keɓe.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 정수 범위를 벗어났습니다.");
        }
        return (keɓe[위치] & 0xff) | ((keɓe[위치 + 1] & 0xff) << 8);
    }
}
