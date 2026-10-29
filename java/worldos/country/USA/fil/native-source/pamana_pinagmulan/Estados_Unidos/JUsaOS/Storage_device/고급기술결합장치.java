// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Estados_Unidos.JUsaOS.Storage_device;

import java.util.Arrays;

/** ATA 28비트 utos 계층과 같은 512바이트 논리 seksiyon_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int seksiyon_sukat = 512;
    private final byte[] data;
    private final boolean mababasa_lamang_VALUE;

    public 고급기술결합장치(int seksiyon_COUNT, boolean mababasa_lamang_VALUE) {
        if (seksiyon_COUNT <= 0) {
            throw new IllegalArgumentException("seksiyon_VALUE 수가 올바르지 않습니다.");
        }
        data = new byte[Math.multiplyExact(seksiyon_COUNT, seksiyon_sukat)];
        this.mababasa_lamang_VALUE = mababasa_lamang_VALUE;
    }

    public int seksiyon_COUNT() {
        return data.length / seksiyon_sukat;
    }

    public void 읽기(int seksiyon_INDEX, byte[] 받을곳) {
        범위확인(seksiyon_INDEX, 받을곳);
        System.arraycopy(data, seksiyon_INDEX * seksiyon_sukat, 받을곳, 0, seksiyon_sukat);
    }

    public void sumulat(int seksiyon_INDEX, byte[] 쓸자료) {
        if (mababasa_lamang_VALUE) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(seksiyon_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, data, seksiyon_INDEX * seksiyon_sukat, seksiyon_sukat);
    }

    public void burahin_pagpasok() {
        if (mababasa_lamang_VALUE) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(data, (byte) 0);
    }

    private void 범위확인(int seksiyon_INDEX, byte[] 임시공간) {
        if (seksiyon_INDEX < 0 || seksiyon_INDEX >= seksiyon_COUNT() || 임시공간.length < seksiyon_sukat) {
            throw new IllegalArgumentException("ATA seksiyon_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

