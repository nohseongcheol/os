// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package TUN.JTunOS.저장장치;

import java.util.Arrays;

/** ATA 28비트 명령 계층과 같은 512바이트 논리 구역 장치다. */
public final class 고급기술결합장치 {
    public static final int 구역크기 = 512;
    private final byte[] 자료;
    private final boolean 읽기전용;

    public 고급기술결합장치(int 구역수, boolean 읽기전용) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("구역 수가 올바르지 않습니다.");
        }
        자료 = new byte[Math.multiplyExact(구역수, 구역크기)];
        this.읽기전용 = 읽기전용;
    }

    public int 구역수() {
        return 자료.length / 구역크기;
    }

    public void 읽기(int 구역번호, byte[] 받을곳) {
        범위확인(구역번호, 받을곳);
        System.arraycopy(자료, 구역번호 * 구역크기, 받을곳, 0, 구역크기);
    }

    public void 쓰기(int 구역번호, byte[] 쓸자료) {
        if (읽기전용) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(구역번호, 쓸자료);
        System.arraycopy(쓸자료, 0, 자료, 구역번호 * 구역크기, 구역크기);
    }

    public void 지우기() {
        if (읽기전용) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(자료, (byte) 0);
    }

    private void 범위확인(int 구역번호, byte[] 임시공간) {
        if (구역번호 < 0 || 구역번호 >= 구역수() || 임시공간.length < 구역크기) {
            throw new IllegalArgumentException("ATA 구역 범위가 올바르지 않습니다.");
        }
    }
}

