// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ايران.JIrnOS.저장장치;

import java.util.Arrays;

/** ATA 28비트 بولۍ 계층과 같은 512바이트 논리 برخه_ارزښت 장치다. */
public final class 고급기술결합장치 {
    public static final int 구역크기 = 512;
    private final byte[] اومتوک;
    private final boolean 읽기전용;

    public 고급기술결합장치(int 구역수, boolean 읽기전용) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("برخه_ارزښت 수가 올바르지 않습니다.");
        }
        اومتوک = new byte[Math.multiplyExact(구역수, 구역크기)];
        this.읽기전용 = 읽기전용;
    }

    public int 구역수() {
        return اومتوک.length / 구역크기;
    }

    public void لوستل(int برخه_لړیال, byte[] 받을곳) {
        범위확인(برخه_لړیال, 받을곳);
        System.arraycopy(اومتوک, برخه_لړیال * 구역크기, 받을곳, 0, 구역크기);
    }

    public void لوستل_2(int برخه_لړیال, byte[] 쓸자료) {
        if (읽기전용) {
            throw new IllegalStateException("لوستل 전용 장치입니다.");
        }
        범위확인(برخه_لړیال, 쓸자료);
        System.arraycopy(쓸자료, 0, اومتوک, برخه_لړیال * 구역크기, 구역크기);
    }

    public void 지우기() {
        if (읽기전용) {
            throw new IllegalStateException("لوستل 전용 장치입니다.");
        }
        Arrays.fill(اومتوک, (byte) 0);
    }

    private void 범위확인(int برخه_لړیال, byte[] 임시공간) {
        if (برخه_لړیال < 0 || برخه_لړیال >= 구역수() || 임시공간.length < 구역크기) {
            throw new IllegalArgumentException("ATA برخه_ارزښت 범위가 올바르지 않습니다.");
        }
    }
}

