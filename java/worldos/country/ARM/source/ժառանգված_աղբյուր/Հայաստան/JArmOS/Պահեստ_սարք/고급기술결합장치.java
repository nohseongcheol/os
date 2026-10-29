// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Հայաստան.JArmOS.Պահեստ_սարք;

import java.util.Arrays;

/** ATA 28비트 Հրահանգ 계층과 같은 512바이트 논리 խումբ_արժեք_366e0bfa 장치다. */
public final class 고급기술결합장치 {
    public static final int խումբ_չափափոխել_3a492be9 = 512;
    private final byte[] տվյալ;
    private final boolean միայն_կարդալու_արժեք;

    public 고급기술결합장치(int 구역수, boolean միայն_կարդալու_արժեք) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("խումբ_արժեք_366e0bfa 수가 올바르지 않습니다.");
        }
        տվյալ = new byte[Math.multiplyExact(구역수, խումբ_չափափոխել_3a492be9)];
        this.միայն_կարդալու_արժեք = միայն_կարդալու_արժեք;
    }

    public int 구역수() {
        return տվյալ.length / խումբ_չափափոխել_3a492be9;
    }

    public void Ընթերցում(int խումբ_դասիչ, byte[] 받을곳) {
        범위확인(խումբ_դասիչ, 받을곳);
        System.arraycopy(տվյալ, խումբ_դասիչ * խումբ_չափափոխել_3a492be9, 받을곳, 0, խումբ_չափափոխել_3a492be9);
    }

    public void Գրել(int խումբ_դասիչ, byte[] 쓸자료) {
        if (միայն_կարդալու_արժեք) {
            throw new IllegalStateException("Ընթերցում 전용 장치입니다.");
        }
        범위확인(խումբ_դասիչ, 쓸자료);
        System.arraycopy(쓸자료, 0, տվյալ, խումբ_դասիչ * խումբ_չափափոխել_3a492be9, խումբ_չափափոխել_3a492be9);
    }

    public void 지우기() {
        if (միայն_կարդալու_արժեք) {
            throw new IllegalStateException("Ընթերցում 전용 장치입니다.");
        }
        Arrays.fill(տվյալ, (byte) 0);
    }

    private void 범위확인(int խումբ_դասիչ, byte[] 임시공간) {
        if (խումբ_դասիչ < 0 || խումբ_դասիչ >= 구역수() || 임시공간.length < խումբ_չափափոխել_3a492be9) {
            throw new IllegalArgumentException("ATA խումբ_արժեք_366e0bfa 범위가 올바르지 않습니다.");
        }
    }
}

