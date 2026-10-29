// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Кыргызстан.JKgzOS.сактагыч_түзмөк;

import java.util.Arrays;

/** ATA 28비트 Команда 계층과 같은 512바이트 논리 бөлүк_маани_366e0bfa 장치다. */
public final class 고급기술결합장치 {
    public static final int бөлүк_көлөм = 512;
    private final byte[] берилмелер;
    private final boolean окуу_үчүн_гана_маани;

    public 고급기술결합장치(int 구역수, boolean окуу_үчүн_гана_маани) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("бөлүк_маани_366e0bfa 수가 올바르지 않습니다.");
        }
        берилмелер = new byte[Math.multiplyExact(구역수, бөлүк_көлөм)];
        this.окуу_үчүн_гана_маани = окуу_үчүн_гана_маани;
    }

    public int 구역수() {
        return берилмелер.length / бөлүк_көлөм;
    }

    public void Окуу(int бөлүк_индекс, byte[] 받을곳) {
        범위확인(бөлүк_индекс, 받을곳);
        System.arraycopy(берилмелер, бөлүк_индекс * бөлүк_көлөм, 받을곳, 0, бөлүк_көлөм);
    }

    public void Жазуу(int бөлүк_индекс, byte[] 쓸자료) {
        if (окуу_үчүн_гана_маани) {
            throw new IllegalStateException("Окуу 전용 장치입니다.");
        }
        범위확인(бөлүк_индекс, 쓸자료);
        System.arraycopy(쓸자료, 0, берилмелер, бөлүк_индекс * бөлүк_көлөм, бөлүк_көлөм);
    }

    public void 지우기() {
        if (окуу_үчүн_гана_маани) {
            throw new IllegalStateException("Окуу 전용 장치입니다.");
        }
        Arrays.fill(берилмелер, (byte) 0);
    }

    private void 범위확인(int бөлүк_индекс, byte[] 임시공간) {
        if (бөлүк_индекс < 0 || бөлүк_индекс >= 구역수() || 임시공간.length < бөлүк_көлөм) {
            throw new IllegalArgumentException("ATA бөлүк_маани_366e0bfa 범위가 올바르지 않습니다.");
        }
    }
}

