// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bẹ̀nẹ̀.JBenOS.ìlànà_ètò_fáìlì;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 àdáwọ̀ 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class abala_àwo_àká_ọ̀rọ̀_iye {
        private final int 종류;
        private final long bẹ̀rẹ̀_abala;
        private final long 구역수;

        abala_àwo_àká_ọ̀rọ̀_iye(int 종류, long bẹ̀rẹ̀_abala, long 구역수) {
            this.종류 = 종류;
            this.bẹ̀rẹ̀_abala = bẹ̀rẹ̀_abala;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long bẹ̀rẹ̀_abala() { return bẹ̀rẹ̀_abala; }
        public long 구역수() { return 구역수; }
    }

    public List<abala_àwo_àká_ọ̀rọ̀_iye> Kàá(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<abala_àwo_àká_ọ̀rọ̀_iye> 결과 = new ArrayList<abala_àwo_àká_ọ̀rọ̀_iye>();
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 4; wá_atọ̀ka_àkóónú++) {
            int 위치 = 446 + wá_atọ̀ka_àkóónú * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long Rọ́ọ̀nù = 작은순서정수(첫구역, 위치 + 8);
            long Ìwọ̀n = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && Ìwọ̀n != 0) {
                결과.add(new abala_àwo_àká_ọ̀rọ̀_iye(종류, Rọ́ọ̀nù, Ìwọ̀n));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] détà, int 위치) {
        return (détà[위치] & 0xffL)
                | ((détà[위치 + 1] & 0xffL) << 8)
                | ((détà[위치 + 2] & 0xffL) << 16)
                | ((détà[위치 + 3] & 0xffL) << 24);
    }
}

