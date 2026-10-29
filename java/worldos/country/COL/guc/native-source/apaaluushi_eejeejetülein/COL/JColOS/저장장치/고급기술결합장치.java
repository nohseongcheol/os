// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COL.JColOS.저장장치;

import java.util.Arrays;

/** ATA 28비트 aluwataaya 계층과 같은 512바이트 논리 alüjalee_ajutuu 장치다. */
public final class 고급기술결합장치 {
    public static final int 구역크기 = 512;
    private final byte[] atijaaya;
    private final boolean 읽기전용;

    public 고급기술결합장치(int 구역수, boolean 읽기전용) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("alüjalee_ajutuu 수가 올바르지 않습니다.");
        }
        atijaaya = new byte[Math.multiplyExact(구역수, 구역크기)];
        this.읽기전용 = 읽기전용;
    }

    public int 구역수() {
        return atijaaya.length / 구역크기;
    }

    public void 읽기(int alüjalee_ee_iyatialujuna, byte[] 받을곳) {
        범위확인(alüjalee_ee_iyatialujuna, 받을곳);
        System.arraycopy(atijaaya, alüjalee_ee_iyatialujuna * 구역크기, 받을곳, 0, 구역크기);
    }

    public void ashajaa(int alüjalee_ee_iyatialujuna, byte[] 쓸자료) {
        if (읽기전용) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(alüjalee_ee_iyatialujuna, 쓸자료);
        System.arraycopy(쓸자료, 0, atijaaya, alüjalee_ee_iyatialujuna * 구역크기, 구역크기);
    }

    public void 지우기() {
        if (읽기전용) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(atijaaya, (byte) 0);
    }

    private void 범위확인(int alüjalee_ee_iyatialujuna, byte[] 임시공간) {
        if (alüjalee_ee_iyatialujuna < 0 || alüjalee_ee_iyatialujuna >= 구역수() || 임시공간.length < 구역크기) {
            throw new IllegalArgumentException("ATA alüjalee_ajutuu 범위가 올바르지 않습니다.");
        }
    }
}

