// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Mooritani.JMrtOS.Dencukaay_toftal;

import java.util.Arrays;

/** ATA 28비트 ndigel 계층과 같은 512바이트 논리 dog_xëyma 장치다. */
public final class 고급기술결합장치 {
    public static final int dog_tolluwaay = 512;
    private final byte[] mbir;
    private final boolean ngir_jaŋarek_la_xëyma;

    public 고급기술결합장치(int 구역수, boolean ngir_jaŋarek_la_xëyma) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("dog_xëyma 수가 올바르지 않습니다.");
        }
        mbir = new byte[Math.multiplyExact(구역수, dog_tolluwaay)];
        this.ngir_jaŋarek_la_xëyma = ngir_jaŋarek_la_xëyma;
    }

    public int 구역수() {
        return mbir.length / dog_tolluwaay;
    }

    public void 읽기(int dog_àlluwa_tur, byte[] 받을곳) {
        범위확인(dog_àlluwa_tur, 받을곳);
        System.arraycopy(mbir, dog_àlluwa_tur * dog_tolluwaay, 받을곳, 0, dog_tolluwaay);
    }

    public void biir(int dog_àlluwa_tur, byte[] 쓸자료) {
        if (ngir_jaŋarek_la_xëyma) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(dog_àlluwa_tur, 쓸자료);
        System.arraycopy(쓸자료, 0, mbir, dog_àlluwa_tur * dog_tolluwaay, dog_tolluwaay);
    }

    public void 지우기() {
        if (ngir_jaŋarek_la_xëyma) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(mbir, (byte) 0);
    }

    private void 범위확인(int dog_àlluwa_tur, byte[] 임시공간) {
        if (dog_àlluwa_tur < 0 || dog_àlluwa_tur >= 구역수() || 임시공간.length < dog_tolluwaay) {
            throw new IllegalArgumentException("ATA dog_xëyma 범위가 올바르지 않습니다.");
        }
    }
}

