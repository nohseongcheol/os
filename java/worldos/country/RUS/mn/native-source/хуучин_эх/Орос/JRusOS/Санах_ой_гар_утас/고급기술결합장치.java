// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Орос.JRusOS.Санах_ой_гар_утас;

import java.util.Arrays;

/** ATA 28비트 Тушаал 계층과 같은 512바이트 논리 хэсэг_утга 장치다. */
public final class 고급기술결합장치 {
    public static final int хэсэг_хэмжээ = 512;
    private final byte[] өгөгдөл;
    private final boolean зөвхөн_унших_утга;

    public 고급기술결합장치(int 구역수, boolean зөвхөн_унших_утга) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("хэсэг_утга 수가 올바르지 않습니다.");
        }
        өгөгдөл = new byte[Math.multiplyExact(구역수, хэсэг_хэмжээ)];
        this.зөвхөн_унших_утга = зөвхөн_унших_утга;
    }

    public int 구역수() {
        return өгөгдөл.length / хэсэг_хэмжээ;
    }

    public void Унших(int хэсэг_индекс, byte[] 받을곳) {
        범위확인(хэсэг_индекс, 받을곳);
        System.arraycopy(өгөгдөл, хэсэг_индекс * хэсэг_хэмжээ, 받을곳, 0, хэсэг_хэмжээ);
    }

    public void Бичих(int хэсэг_индекс, byte[] 쓸자료) {
        if (зөвхөн_унших_утга) {
            throw new IllegalStateException("Унших 전용 장치입니다.");
        }
        범위확인(хэсэг_индекс, 쓸자료);
        System.arraycopy(쓸자료, 0, өгөгдөл, хэсэг_индекс * хэсэг_хэмжээ, хэсэг_хэмжээ);
    }

    public void 지우기() {
        if (зөвхөн_унших_утга) {
            throw new IllegalStateException("Унших 전용 장치입니다.");
        }
        Arrays.fill(өгөгдөл, (byte) 0);
    }

    private void 범위확인(int хэсэг_индекс, byte[] 임시공간) {
        if (хэсэг_индекс < 0 || хэсэг_индекс >= 구역수() || 임시공간.length < хэсэг_хэмжээ) {
            throw new IllegalArgumentException("ATA хэсэг_утга 범위가 올바르지 않습니다.");
        }
    }
}

