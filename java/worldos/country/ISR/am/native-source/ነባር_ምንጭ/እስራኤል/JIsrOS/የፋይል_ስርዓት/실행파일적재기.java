// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package እስራኤል.JIsrOS.የፋይል_ስርዓት;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian ፈጽም_ትእዛዝ 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class ክፍል_እሴት {
        private final int 종류;
        private final int ጠቁም_እሴት;
        private final int አድራሻ;
        private final int ፋይል_በቦታ_አስቀመጠ;
        private final int መጠን;

        ክፍል_እሴት(int 종류, int ጠቁም_እሴት, int አድራሻ, int ፋይል_በቦታ_አስቀመጠ, int መጠን) {
            this.종류 = 종류;
            this.ጠቁም_እሴት = ጠቁም_እሴት;
            this.አድራሻ = አድራሻ;
            this.ፋይል_በቦታ_አስቀመጠ = ፋይል_በቦታ_አስቀመጠ;
            this.መጠን = መጠን;
        }

        public int 종류() {
            return 종류;
        }

        public int ጠቁም_እሴት() {
            return ጠቁም_እሴት;
        }

        public int አድራሻ() {
            return አድራሻ;
        }

        public int ፋይል_በቦታ_አስቀመጠ() {
            return ፋይል_በቦታ_አስቀመጠ;
        }

        public int መጠን() {
            return መጠን;
        }
    }

    public static final class ምስል {
        private final int ጀምር_አድራሻ;
        private final List<ክፍል_እሴት> 구역들;

        ምስል(int ጀምር_አድራሻ, List<ክፍል_እሴት> 구역들) {
            this.ጀምር_አድራሻ = ጀምር_አድራሻ;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int ጀምር_አድራሻ() {
            return ጀምር_አድራሻ;
        }

        public List<ክፍል_እሴት> 구역들() {
            return 구역들;
        }
    }

    public ምስል 검사(byte[] ውሂብ) {
        if (ውሂብ == null || ውሂብ.length < 52
                || ውሂብ[0] != 0x7f || ውሂብ[1] != 'E' || ውሂብ[2] != 'L' || ውሂብ[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (ውሂብ[4] != 1 || ውሂብ[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int ጀምር_አድራሻ = ተንትን_ኢንተጀር(ውሂብ, 24);
        int ክፍል_ሰንጠረዥ_በቦታ_አስቀመጠ = ተንትን_ኢንተጀር(ውሂብ, 32);
        int ክፍል_ምዝግብ_መጠን_ቀይር = 짧은정수읽기(ውሂብ, 46);
        int 구역수 = 짧은정수읽기(ውሂብ, 48);
        if (ክፍል_ምዝግብ_መጠን_ቀይር < 40 || ክፍል_ሰንጠረዥ_በቦታ_አስቀመጠ < 0
                || (long) ክፍል_ሰንጠረዥ_በቦታ_አስቀመጠ + (long) ክፍል_ምዝግብ_መጠን_ቀይር * 구역수 > ውሂብ.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<ክፍል_እሴት> 구역들 = new ArrayList<ክፍል_እሴት>();
        for (int መረጃ_ጠቆመ = 0; መረጃ_ጠቆመ < 구역수; መረጃ_ጠቆመ++) {
            int አካባቢ = ክፍል_ሰንጠረዥ_በቦታ_አስቀመጠ + መረጃ_ጠቆመ * ክፍል_ምዝግብ_መጠን_ቀይር;
            int 종류 = ተንትን_ኢንተጀር(ውሂብ, አካባቢ + 4);
            int ጠቁም_እሴት = ተንትን_ኢንተጀር(ውሂብ, አካባቢ + 8);
            int አድራሻ = ተንትን_ኢንተጀር(ውሂብ, አካባቢ + 12);
            int ፋይል_በቦታ_አስቀመጠ = ተንትን_ኢንተጀር(ውሂብ, አካባቢ + 16);
            int መጠን = ተንትን_ኢንተጀር(ውሂብ, አካባቢ + 20);
            if (መጠን < 0 || (종류 != 8 && ((long) ፋይል_በቦታ_አስቀመጠ + መጠን > ውሂብ.length || ፋይል_በቦታ_አስቀመጠ < 0))) {
                throw new IllegalArgumentException("ELF ክፍል_እሴት ውሂብ 범위가 올바르지 않습니다.");
            }
            구역들.add(new ክፍል_እሴት(종류, ጠቁም_እሴት, አድራሻ, ፋይል_በቦታ_አስቀመጠ, መጠን));
        }
        return new ምስል(ጀምር_አድራሻ, 구역들);
    }

    private int ተንትን_ኢንተጀር(byte[] ውሂብ, int አካባቢ) {
        if (አካባቢ < 0 || አካባቢ > ውሂብ.length - 4) {
            throw new IllegalArgumentException("ELF ኢንተጀር 범위를 벗어났습니다.");
        }
        return (ውሂብ[አካባቢ] & 0xff)
                | ((ውሂብ[አካባቢ + 1] & 0xff) << 8)
                | ((ውሂብ[አካባቢ + 2] & 0xff) << 16)
                | ((ውሂብ[አካባቢ + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] ውሂብ, int አካባቢ) {
        if (አካባቢ < 0 || አካባቢ > ውሂብ.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 ኢንተጀር 범위를 벗어났습니다.");
        }
        return (ውሂብ[አካባቢ] & 0xff) | ((ውሂብ[አካባቢ + 1] & 0xff) << 8);
    }
}
