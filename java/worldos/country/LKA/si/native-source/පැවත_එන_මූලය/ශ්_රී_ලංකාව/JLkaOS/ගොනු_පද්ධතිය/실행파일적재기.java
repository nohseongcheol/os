// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ශ්_රී_ලංකාව.JLkaOS.ගොනු_පද්ධතිය;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian ක්_රියාත්මක_කරන්න_විධානය 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class අංශය_අගය {
        private final int 종류;
        private final int සලකුණ_අගය;
        private final int යොමුව;
        private final int 파일위치;
        private final int ප්_රමාණය;

        අංශය_අගය(int 종류, int සලකුණ_අගය, int යොමුව, int 파일위치, int ප්_රමාණය) {
            this.종류 = 종류;
            this.සලකුණ_අගය = සලකුණ_අගය;
            this.යොමුව = යොමුව;
            this.파일위치 = 파일위치;
            this.ප්_රමාණය = ප්_රමාණය;
        }

        public int 종류() {
            return 종류;
        }

        public int සලකුණ_අගය() {
            return සලකුණ_අගය;
        }

        public int යොමුව() {
            return යොමුව;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int ප්_රමාණය() {
            return ප්_රමාණය;
        }
    }

    public static final class අනුරුව {
        private final int ඇරඹුම_යොමුව;
        private final List<අංශය_අගය> 구역들;

        අනුරුව(int ඇරඹුම_යොමුව, List<අංශය_අගය> 구역들) {
            this.ඇරඹුම_යොමුව = ඇරඹුම_යොමුව;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int ඇරඹුම_යොමුව() {
            return ඇරඹුම_යොමුව;
        }

        public List<අංශය_අගය> 구역들() {
            return 구역들;
        }
    }

    public අනුරුව 검사(byte[] දත්ත) {
        if (දත්ත == null || දත්ත.length < 52
                || දත්ත[0] != 0x7f || දත්ත[1] != 'E' || දත්ත[2] != 'L' || දත්ත[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (දත්ත[4] != 1 || දත්ත[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int ඇරඹුම_යොමුව = විශ්ලේෂණය_කරන්න_පූර්ණාංකය(දත්ත, 24);
        int 구역표위치 = විශ්ලේෂණය_කරන්න_පූර්ණාංකය(දත්ත, 32);
        int අංශය_පිවිසුම_ප්_රමාණනය = 짧은정수읽기(දත්ත, 46);
        int 구역수 = 짧은정수읽기(දත්ත, 48);
        if (අංශය_පිවිසුම_ප්_රමාණනය < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) අංශය_පිවිසුම_ප්_රමාණනය * 구역수 > දත්ත.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<අංශය_අගය> 구역들 = new ArrayList<අංශය_අගය>();
        for (int සූචිය = 0; සූචිය < 구역수; සූචිය++) {
            int පිහිටීම = 구역표위치 + සූචිය * අංශය_පිවිසුම_ප්_රමාණනය;
            int 종류 = විශ්ලේෂණය_කරන්න_පූර්ණාංකය(දත්ත, පිහිටීම + 4);
            int සලකුණ_අගය = විශ්ලේෂණය_කරන්න_පූර්ණාංකය(දත්ත, පිහිටීම + 8);
            int යොමුව = විශ්ලේෂණය_කරන්න_පූර්ණාංකය(දත්ත, පිහිටීම + 12);
            int 파일위치 = විශ්ලේෂණය_කරන්න_පූර්ණාංකය(දත්ත, පිහිටීම + 16);
            int ප්_රමාණය = විශ්ලේෂණය_කරන්න_පූර්ණාංකය(දත්ත, පිහිටීම + 20);
            if (ප්_රමාණය < 0 || (종류 != 8 && ((long) 파일위치 + ප්_රමාණය > දත්ත.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF අංශය_අගය දත්ත 범위가 올바르지 않습니다.");
            }
            구역들.add(new අංශය_අගය(종류, සලකුණ_අගය, යොමුව, 파일위치, ප්_රමාණය));
        }
        return new අනුරුව(ඇරඹුම_යොමුව, 구역들);
    }

    private int විශ්ලේෂණය_කරන්න_පූර්ණාංකය(byte[] දත්ත, int පිහිටීම) {
        if (පිහිටීම < 0 || පිහිටීම > දත්ත.length - 4) {
            throw new IllegalArgumentException("ELF පූර්ණාංකය 범위를 벗어났습니다.");
        }
        return (දත්ත[පිහිටීම] & 0xff)
                | ((දත්ත[පිහිටීම + 1] & 0xff) << 8)
                | ((දත්ත[පිහිටීම + 2] & 0xff) << 16)
                | ((දත්ත[පිහිටීම + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] දත්ත, int පිහිටීම) {
        if (පිහිටීම < 0 || පිහිටීම > දත්ත.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 පූර්ණාංකය 범위를 벗어났습니다.");
        }
        return (දත්ත[පිහිටීම] & 0xff) | ((දත්ත[පිහිටීම + 1] & 0xff) << 8);
    }
}
