// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Србија.JSrbOS.похрана_уређај;

import java.util.Arrays;

/** ATA 28비트 Наредба 계층과 같은 512바이트 논리 одељак_вриједност 장치다. */
public final class 고급기술결합장치 {
    public static final int одељак_подесити_величину = 512;
    private final byte[] подаци;
    private final boolean само_за_читање_вриједност;

    public 고급기술결합장치(int 구역수, boolean само_за_читање_вриједност) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("одељак_вриједност 수가 올바르지 않습니다.");
        }
        подаци = new byte[Math.multiplyExact(구역수, одељак_подесити_величину)];
        this.само_за_читање_вриједност = само_за_читање_вриједност;
    }

    public int 구역수() {
        return подаци.length / одељак_подесити_величину;
    }

    public void Чита(int одељак_индекс, byte[] 받을곳) {
        чек_опсег(одељак_индекс, 받을곳);
        System.arraycopy(подаци, одељак_индекс * одељак_подесити_величину, 받을곳, 0, одељак_подесити_величину);
    }

    public void Пише(int одељак_индекс, byte[] 쓸자료) {
        if (само_за_читање_вриједност) {
            throw new IllegalStateException("Чита 전용 장치입니다.");
        }
        чек_опсег(одељак_индекс, 쓸자료);
        System.arraycopy(쓸자료, 0, подаци, одељак_индекс * одељак_подесити_величину, одељак_подесити_величину);
    }

    public void 지우기() {
        if (само_за_читање_вриједност) {
            throw new IllegalStateException("Чита 전용 장치입니다.");
        }
        Arrays.fill(подаци, (byte) 0);
    }

    private void чек_опсег(int одељак_индекс, byte[] 임시공간) {
        if (одељак_индекс < 0 || одељак_индекс >= 구역수() || 임시공간.length < одељак_подесити_величину) {
            throw new IllegalArgumentException("ATA одељак_вриједност 범위가 올바르지 않습니다.");
        }
    }
}

