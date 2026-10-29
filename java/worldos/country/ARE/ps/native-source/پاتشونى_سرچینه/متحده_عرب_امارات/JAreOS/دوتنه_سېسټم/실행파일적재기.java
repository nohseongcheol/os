// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package متحده_عرب_امارات.JAreOS.دوتنه_سېسټم;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian 실행 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class برخه_ارزښت {
        private final int 종류;
        private final int رپى_ارزښت;
        private final int پته;
        private final int 파일위치;
        private final int کچ;

        برخه_ارزښت(int 종류, int رپى_ارزښت, int پته, int 파일위치, int کچ) {
            this.종류 = 종류;
            this.رپى_ارزښت = رپى_ارزښت;
            this.پته = پته;
            this.파일위치 = 파일위치;
            this.کچ = کچ;
        }

        public int 종류() {
            return 종류;
        }

        public int رپى_ارزښت() {
            return رپى_ارزښت;
        }

        public int پته() {
            return پته;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int کچ() {
            return کچ;
        }
    }

    public static final class انځور {
        private final int پيل_پته;
        private final List<برخه_ارزښت> 구역들;

        انځور(int پيل_پته, List<برخه_ارزښت> 구역들) {
            this.پيل_پته = پيل_پته;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int پيل_پته() {
            return پيل_پته;
        }

        public List<برخه_ارزښت> 구역들() {
            return 구역들;
        }
    }

    public انځور 검사(byte[] اومتوک) {
        if (اومتوک == null || اومتوک.length < 52
                || اومتوک[0] != 0x7f || اومتوک[1] != 'E' || اومتوک[2] != 'L' || اومتوک[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (اومتوک[4] != 1 || اومتوک[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int پيل_پته = تجزیه_صحيح_عدد(اومتوک, 24);
        int 구역표위치 = تجزیه_صحيح_عدد(اومتوک, 32);
        int 구역항목크기 = 짧은정수읽기(اومتوک, 46);
        int 구역수 = 짧은정수읽기(اومتوک, 48);
        if (구역항목크기 < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) 구역항목크기 * 구역수 > اومتوک.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<برخه_ارزښت> 구역들 = new ArrayList<برخه_ارزښت>();
        for (int لړیال = 0; لړیال < 구역수; لړیال++) {
            int ځای = 구역표위치 + لړیال * 구역항목크기;
            int 종류 = تجزیه_صحيح_عدد(اومتوک, ځای + 4);
            int رپى_ارزښت = تجزیه_صحيح_عدد(اومتوک, ځای + 8);
            int پته = تجزیه_صحيح_عدد(اومتوک, ځای + 12);
            int 파일위치 = تجزیه_صحيح_عدد(اومتوک, ځای + 16);
            int کچ = تجزیه_صحيح_عدد(اومتوک, ځای + 20);
            if (کچ < 0 || (종류 != 8 && ((long) 파일위치 + کچ > اومتوک.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF برخه_ارزښت اومتوک 범위가 올바르지 않습니다.");
            }
            구역들.add(new برخه_ارزښت(종류, رپى_ارزښت, پته, 파일위치, کچ));
        }
        return new انځور(پيل_پته, 구역들);
    }

    private int تجزیه_صحيح_عدد(byte[] اومتوک, int ځای) {
        if (ځای < 0 || ځای > اومتوک.length - 4) {
            throw new IllegalArgumentException("ELF صحيح_عدد 범위를 벗어났습니다.");
        }
        return (اومتوک[ځای] & 0xff)
                | ((اومتوک[ځای + 1] & 0xff) << 8)
                | ((اومتوک[ځای + 2] & 0xff) << 16)
                | ((اومتوک[ځای + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] اومتوک, int ځای) {
        if (ځای < 0 || ځای > اومتوک.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 صحيح_عدد 범위를 벗어났습니다.");
        }
        return (اومتوک[ځای] & 0xff) | ((اومتوک[ځای + 1] & 0xff) << 8);
    }
}
