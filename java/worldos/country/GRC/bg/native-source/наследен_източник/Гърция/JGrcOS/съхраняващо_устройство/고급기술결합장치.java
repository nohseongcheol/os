// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Гърция.JGrcOS.съхраняващо_устройство;

import java.util.Arrays;

/** ATA 28비트 Команда 계층과 같은 512바이트 논리 раздел_стойност 장치다. */
public final class 고급기술결합장치 {
    public static final int раздел_размер = 512;
    private final byte[] данни;
    private final boolean само_за_четене_стойност;

    public 고급기술결합장치(int 구역수, boolean само_за_четене_стойност) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("раздел_стойност 수가 올바르지 않습니다.");
        }
        данни = new byte[Math.multiplyExact(구역수, раздел_размер)];
        this.само_за_четене_стойност = само_за_четене_стойност;
    }

    public int 구역수() {
        return данни.length / раздел_размер;
    }

    public void Четене(int раздел_индекс, byte[] получавам_местоназначение) {
        проверявам_обхват(раздел_индекс, получавам_местоназначение);
        System.arraycopy(данни, раздел_индекс * раздел_размер, получавам_местоназначение, 0, раздел_размер);
    }

    public void Писане(int раздел_индекс, byte[] 쓸자료) {
        if (само_за_четене_стойност) {
            throw new IllegalStateException("Четене 전용 장치입니다.");
        }
        проверявам_обхват(раздел_индекс, 쓸자료);
        System.arraycopy(쓸자료, 0, данни, раздел_индекс * раздел_размер, раздел_размер);
    }

    public void изтривам_запис() {
        if (само_за_четене_стойност) {
            throw new IllegalStateException("Четене 전용 장치입니다.");
        }
        Arrays.fill(данни, (byte) 0);
    }

    private void проверявам_обхват(int раздел_индекс, byte[] 임시공간) {
        if (раздел_индекс < 0 || раздел_индекс >= 구역수() || 임시공간.length < раздел_размер) {
            throw new IllegalArgumentException("ATA раздел_стойност 범위가 올바르지 않습니다.");
        }
    }
}

