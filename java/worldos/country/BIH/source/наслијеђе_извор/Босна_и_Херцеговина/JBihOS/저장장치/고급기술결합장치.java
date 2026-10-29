// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Босна_и_Херцеговина.JBihOS.저장장치;

import java.util.Arrays;

/** ATA 28비트 команда 계층과 같은 512바이트 논리 секција_вриједност 장치다. */
public final class 고급기술결합장치 {
    public static final int секција_подесити_величину = 512;
    private final byte[] подаци;
    private final boolean само_за_читање_вриједност;

    public 고급기술결합장치(int 구역수, boolean само_за_читање_вриједност) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("секција_вриједност 수가 올바르지 않습니다.");
        }
        подаци = new byte[Math.multiplyExact(구역수, секција_подесити_величину)];
        this.само_за_читање_вриједност = само_за_читање_вриједност;
    }

    public int 구역수() {
        return подаци.length / секција_подесити_величину;
    }

    public void 읽기(int секција_индекс, byte[] 받을곳) {
        범위확인(секција_индекс, 받을곳);
        System.arraycopy(подаци, секција_индекс * секција_подесити_величину, 받을곳, 0, секција_подесити_величину);
    }

    public void писати(int секција_индекс, byte[] 쓸자료) {
        if (само_за_читање_вриједност) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(секција_индекс, 쓸자료);
        System.arraycopy(쓸자료, 0, подаци, секција_индекс * секција_подесити_величину, секција_подесити_величину);
    }

    public void 지우기() {
        if (само_за_читање_вриједност) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(подаци, (byte) 0);
    }

    private void 범위확인(int секција_индекс, byte[] 임시공간) {
        if (секција_индекс < 0 || секција_индекс >= 구역수() || 임시공간.length < секција_подесити_величину) {
            throw new IllegalArgumentException("ATA секција_вриједност 범위가 올바르지 않습니다.");
        }
    }
}

