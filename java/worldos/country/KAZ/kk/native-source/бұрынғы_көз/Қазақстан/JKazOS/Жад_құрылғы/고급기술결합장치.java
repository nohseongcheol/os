// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Қазақстан.JKazOS.Жад_құрылғы;

import java.util.Arrays;

/** ATA 28비트 Команда 계층과 같은 512바이트 논리 бөлім_мән_366e0bfa 장치다. */
public final class 고급기술결합장치 {
    public static final int бөлім_өлшемді_өзгерту = 512;
    private final byte[] деректер;
    private final boolean тек_оқу_үшін_мән;

    public 고급기술결합장치(int 구역수, boolean тек_оқу_үшін_мән) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("бөлім_мән_366e0bfa 수가 올바르지 않습니다.");
        }
        деректер = new byte[Math.multiplyExact(구역수, бөлім_өлшемді_өзгерту)];
        this.тек_оқу_үшін_мән = тек_оқу_үшін_мән;
    }

    public int 구역수() {
        return деректер.length / бөлім_өлшемді_өзгерту;
    }

    public void Оқу(int бөлім_индекс, byte[] 받을곳) {
        чек_ауқым(бөлім_индекс, 받을곳);
        System.arraycopy(деректер, бөлім_индекс * бөлім_өлшемді_өзгерту, 받을곳, 0, бөлім_өлшемді_өзгерту);
    }

    public void Жазу(int бөлім_индекс, byte[] 쓸자료) {
        if (тек_оқу_үшін_мән) {
            throw new IllegalStateException("Оқу 전용 장치입니다.");
        }
        чек_ауқым(бөлім_индекс, 쓸자료);
        System.arraycopy(쓸자료, 0, деректер, бөлім_индекс * бөлім_өлшемді_өзгерту, бөлім_өлшемді_өзгерту);
    }

    public void өшіру_енгізу() {
        if (тек_оқу_үшін_мән) {
            throw new IllegalStateException("Оқу 전용 장치입니다.");
        }
        Arrays.fill(деректер, (byte) 0);
    }

    private void чек_ауқым(int бөлім_индекс, byte[] 임시공간) {
        if (бөлім_индекс < 0 || бөлім_индекс >= 구역수() || 임시공간.length < бөлім_өлшемді_өзгерту) {
            throw new IllegalArgumentException("ATA бөлім_мән_366e0bfa 범위가 올바르지 않습니다.");
        }
    }
}

