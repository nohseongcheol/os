// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bẹ̀nẹ̀.JBenOS.ìlànà_ètò_fáìlì;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian ṣiṣẹ́_àṣẹ 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class abala_iye {
        private final int 종류;
        private final int ipe_àkíyèsí_sí_iye;
        private final int àdírẹ́ẹ̀sì;
        private final int 파일위치;
        private final int Ìwọ̀n;

        abala_iye(int 종류, int ipe_àkíyèsí_sí_iye, int àdírẹ́ẹ̀sì, int 파일위치, int Ìwọ̀n) {
            this.종류 = 종류;
            this.ipe_àkíyèsí_sí_iye = ipe_àkíyèsí_sí_iye;
            this.àdírẹ́ẹ̀sì = àdírẹ́ẹ̀sì;
            this.파일위치 = 파일위치;
            this.Ìwọ̀n = Ìwọ̀n;
        }

        public int 종류() {
            return 종류;
        }

        public int ipe_àkíyèsí_sí_iye() {
            return ipe_àkíyèsí_sí_iye;
        }

        public int àdírẹ́ẹ̀sì() {
            return àdírẹ́ẹ̀sì;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int Ìwọ̀n() {
            return Ìwọ̀n;
        }
    }

    public static final class àwòrán {
        private final int bẹ̀rẹ̀_àdírẹ́ẹ̀sì;
        private final List<abala_iye> 구역들;

        àwòrán(int bẹ̀rẹ̀_àdírẹ́ẹ̀sì, List<abala_iye> 구역들) {
            this.bẹ̀rẹ̀_àdírẹ́ẹ̀sì = bẹ̀rẹ̀_àdírẹ́ẹ̀sì;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int bẹ̀rẹ̀_àdírẹ́ẹ̀sì() {
            return bẹ̀rẹ̀_àdírẹ́ẹ̀sì;
        }

        public List<abala_iye> 구역들() {
            return 구역들;
        }
    }

    public àwòrán 검사(byte[] détà) {
        if (détà == null || détà.length < 52
                || détà[0] != 0x7f || détà[1] != 'E' || détà[2] != 'L' || détà[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (détà[4] != 1 || détà[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int bẹ̀rẹ̀_àdírẹ́ẹ̀sì = ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(détà, 24);
        int 구역표위치 = ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(détà, 32);
        int abala_ìgbéwọlé_ìwọn = 짧은정수읽기(détà, 46);
        int 구역수 = 짧은정수읽기(détà, 48);
        if (abala_ìgbéwọlé_ìwọn < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) abala_ìgbéwọlé_ìwọn * 구역수 > détà.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<abala_iye> 구역들 = new ArrayList<abala_iye>();
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 구역수; wá_atọ̀ka_àkóónú++) {
            int 위치 = 구역표위치 + wá_atọ̀ka_àkóónú * abala_ìgbéwọlé_ìwọn;
            int 종류 = ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(détà, 위치 + 4);
            int ipe_àkíyèsí_sí_iye = ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(détà, 위치 + 8);
            int àdírẹ́ẹ̀sì = ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(détà, 위치 + 12);
            int 파일위치 = ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(détà, 위치 + 16);
            int Ìwọ̀n = ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(détà, 위치 + 20);
            if (Ìwọ̀n < 0 || (종류 != 8 && ((long) 파일위치 + Ìwọ̀n > détà.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF abala_iye détà 범위가 올바르지 않습니다.");
            }
            구역들.add(new abala_iye(종류, ipe_àkíyèsí_sí_iye, àdírẹ́ẹ̀sì, 파일위치, Ìwọ̀n));
        }
        return new àwòrán(bẹ̀rẹ̀_àdírẹ́ẹ̀sì, 구역들);
    }

    private int ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(byte[] détà, int 위치) {
        if (위치 < 0 || 위치 > détà.length - 4) {
            throw new IllegalArgumentException("ELF nọ́ńbà_odindi 범위를 벗어났습니다.");
        }
        return (détà[위치] & 0xff)
                | ((détà[위치 + 1] & 0xff) << 8)
                | ((détà[위치 + 2] & 0xff) << 16)
                | ((détà[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] détà, int 위치) {
        if (위치 < 0 || 위치 > détà.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 nọ́ńbà_odindi 범위를 벗어났습니다.");
        }
        return (détà[위치] & 0xff) | ((détà[위치 + 1] & 0xff) << 8);
    }
}
