// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Германия.JDeuOS.запоминающее_устройство;

import java.util.Arrays;

/** ATA 28비트 команда 계층과 같은 512바이트 논리 раздел_ЗНАЧЕН_366e0bfa 장치다. */
public final class 고급기술결합장치 {
    public static final int раздел_изменить_размер = 512;
    private final byte[] данные;
    private final boolean нередактируемый_ЗНАЧЕН;

    public 고급기술결합장치(int раздел_СЧЁТ, boolean нередактируемый_ЗНАЧЕН) {
        if (раздел_СЧЁТ <= 0) {
            throw new IllegalArgumentException("раздел_ЗНАЧЕН_366e0bfa 수가 올바르지 않습니다.");
        }
        данные = new byte[Math.multiplyExact(раздел_СЧЁТ, раздел_изменить_размер)];
        this.нередактируемый_ЗНАЧЕН = нередактируемый_ЗНАЧЕН;
    }

    public int раздел_СЧЁТ() {
        return данные.length / раздел_изменить_размер;
    }

    public void Чтение(int раздел_ИНДЕКС, byte[] получить_цель) {
        чек_диапазон(раздел_ИНДЕКС, получить_цель);
        System.arraycopy(данные, раздел_ИНДЕКС * раздел_изменить_размер, получить_цель, 0, раздел_изменить_размер);
    }

    public void Запись(int раздел_ИНДЕКС, byte[] 쓸자료) {
        if (нередактируемый_ЗНАЧЕН) {
            throw new IllegalStateException("Чтение 전용 장치입니다.");
        }
        чек_диапазон(раздел_ИНДЕКС, 쓸자료);
        System.arraycopy(쓸자료, 0, данные, раздел_ИНДЕКС * раздел_изменить_размер, раздел_изменить_размер);
    }

    public void удалить_ввод_c8dbc399() {
        if (нередактируемый_ЗНАЧЕН) {
            throw new IllegalStateException("Чтение 전용 장치입니다.");
        }
        Arrays.fill(данные, (byte) 0);
    }

    private void чек_диапазон(int раздел_ИНДЕКС, byte[] 임시공간) {
        if (раздел_ИНДЕКС < 0 || раздел_ИНДЕКС >= раздел_СЧЁТ() || 임시공간.length < раздел_изменить_размер) {
            throw new IllegalArgumentException("ATA раздел_ЗНАЧЕН_366e0bfa 범위가 올바르지 않습니다.");
        }
    }
}

