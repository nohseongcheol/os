// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Тоҷикистон.JTjkOS.Захирагоҳ_мобилӣ;

import java.util.Arrays;

/** ATA 28비트 фармон 계층과 같은 512바이트 논리 қисмат_қимат 장치다. */
public final class 고급기술결합장치 {
    public static final int қисмат_андоза_кардан = 512;
    private final byte[] иттилоот;
    private final boolean танҳо_барои_хондан_қимат;

    public 고급기술결합장치(int 구역수, boolean танҳо_барои_хондан_қимат) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("қисмат_қимат 수가 올바르지 않습니다.");
        }
        иттилоот = new byte[Math.multiplyExact(구역수, қисмат_андоза_кардан)];
        this.танҳо_барои_хондан_қимат = танҳо_барои_хондан_қимат;
    }

    public int 구역수() {
        return иттилоот.length / қисмат_андоза_кардан;
    }

    public void Хондан(int қисмат_индекс, byte[] 받을곳) {
        범위확인(қисмат_индекс, 받을곳);
        System.arraycopy(иттилоот, қисмат_индекс * қисмат_андоза_кардан, 받을곳, 0, қисмат_андоза_кардан);
    }

    public void Навиштан(int қисмат_индекс, byte[] 쓸자료) {
        if (танҳо_барои_хондан_қимат) {
            throw new IllegalStateException("Хондан 전용 장치입니다.");
        }
        범위확인(қисмат_индекс, 쓸자료);
        System.arraycopy(쓸자료, 0, иттилоот, қисмат_индекс * қисмат_андоза_кардан, қисмат_андоза_кардан);
    }

    public void 지우기() {
        if (танҳо_барои_хондан_қимат) {
            throw new IllegalStateException("Хондан 전용 장치입니다.");
        }
        Arrays.fill(иттилоот, (byte) 0);
    }

    private void 범위확인(int қисмат_индекс, byte[] 임시공간) {
        if (қисмат_индекс < 0 || қисмат_индекс >= 구역수() || 임시공간.length < қисмат_андоза_кардан) {
            throw new IllegalArgumentException("ATA қисмат_қимат 범위가 올바르지 않습니다.");
        }
    }
}

