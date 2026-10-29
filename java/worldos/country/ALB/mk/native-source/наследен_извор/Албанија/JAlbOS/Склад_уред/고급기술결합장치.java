// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Албанија.JAlbOS.Склад_уред;

import java.util.Arrays;

/** ATA 28비트 Команда 계층과 같은 512바이트 논리 секција_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int секција_големина = 512;
    private final byte[] податоци;
    private final boolean само_за_читање_VALUE;

    public 고급기술결합장치(int секција_COUNT, boolean само_за_читање_VALUE) {
        if (секција_COUNT <= 0) {
            throw new IllegalArgumentException("секција_VALUE 수가 올바르지 않습니다.");
        }
        податоци = new byte[Math.multiplyExact(секција_COUNT, секција_големина)];
        this.само_за_читање_VALUE = само_за_читање_VALUE;
    }

    public int секција_COUNT() {
        return податоци.length / секција_големина;
    }

    public void Читај(int секција_INDEX, byte[] 받을곳) {
        범위확인(секција_INDEX, 받을곳);
        System.arraycopy(податоци, секција_INDEX * секција_големина, 받을곳, 0, секција_големина);
    }

    public void Запиши(int секција_INDEX, byte[] 쓸자료) {
        if (само_за_читање_VALUE) {
            throw new IllegalStateException("Читај 전용 장치입니다.");
        }
        범위확인(секција_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, податоци, секција_INDEX * секција_големина, секција_големина);
    }

    public void избриши_внес() {
        if (само_за_читање_VALUE) {
            throw new IllegalStateException("Читај 전용 장치입니다.");
        }
        Arrays.fill(податоци, (byte) 0);
    }

    private void 범위확인(int секција_INDEX, byte[] 임시공간) {
        if (секција_INDEX < 0 || секција_INDEX >= секција_COUNT() || 임시공간.length < секција_големина) {
            throw new IllegalArgumentException("ATA секција_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

