// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bẹ̀nẹ̀.JBenOS.Ibi_ìpamọ́_ohun_èlò;

import java.util.Arrays;

/** ATA 28비트 Àṣẹ 계층과 같은 512바이트 논리 abala_iye 장치다. */
public final class 고급기술결합장치 {
    public static final int abala_ìwọn = 512;
    private final byte[] détà;
    private final boolean kàn_kàá_iye;

    public 고급기술결합장치(int 구역수, boolean kàn_kàá_iye) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("abala_iye 수가 올바르지 않습니다.");
        }
        détà = new byte[Math.multiplyExact(구역수, abala_ìwọn)];
        this.kàn_kàá_iye = kàn_kàá_iye;
    }

    public int 구역수() {
        return détà.length / abala_ìwọn;
    }

    public void Kàá(int abala_wá_atọ̀ka_àkóónú, byte[] 받을곳) {
        범위확인(abala_wá_atọ̀ka_àkóónú, 받을곳);
        System.arraycopy(détà, abala_wá_atọ̀ka_àkóónú * abala_ìwọn, 받을곳, 0, abala_ìwọn);
    }

    public void Kọ(int abala_wá_atọ̀ka_àkóónú, byte[] 쓸자료) {
        if (kàn_kàá_iye) {
            throw new IllegalStateException("Kàá 전용 장치입니다.");
        }
        범위확인(abala_wá_atọ̀ka_àkóónú, 쓸자료);
        System.arraycopy(쓸자료, 0, détà, abala_wá_atọ̀ka_àkóónú * abala_ìwọn, abala_ìwọn);
    }

    public void 지우기() {
        if (kàn_kàá_iye) {
            throw new IllegalStateException("Kàá 전용 장치입니다.");
        }
        Arrays.fill(détà, (byte) 0);
    }

    private void 범위확인(int abala_wá_atọ̀ka_àkóónú, byte[] 임시공간) {
        if (abala_wá_atọ̀ka_àkóónú < 0 || abala_wá_atọ̀ka_àkóónú >= 구역수() || 임시공간.length < abala_ìwọn) {
            throw new IllegalArgumentException("ATA abala_iye 범위가 올바르지 않습니다.");
        }
    }
}

