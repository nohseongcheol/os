// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.भण्डारण_मोबाइल;

import java.util.Arrays;

/** ATA 28비트 आदेश 계층과 같은 512바이트 논리 सेक्सन_मान 장치다. */
public final class 고급기술결합장치 {
    public static final int सेक्सन_साइज = 512;
    private final byte[] लगत;
    private final boolean पढ्न_मात्र_मान;

    public 고급기술결합장치(int 구역수, boolean पढ्न_मात्र_मान) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("सेक्सन_मान 수가 올바르지 않습니다.");
        }
        लगत = new byte[Math.multiplyExact(구역수, सेक्सन_साइज)];
        this.पढ्न_मात्र_मान = पढ्न_मात्र_मान;
    }

    public int 구역수() {
        return लगत.length / सेक्सन_साइज;
    }

    public void पढनुहोस्(int सेक्सन_अनुक्रमणिका, byte[] 받을곳) {
        범위확인(सेक्सन_अनुक्रमणिका, 받을곳);
        System.arraycopy(लगत, सेक्सन_अनुक्रमणिका * सेक्सन_साइज, 받을곳, 0, सेक्सन_साइज);
    }

    public void लेख्नुहोस्(int सेक्सन_अनुक्रमणिका, byte[] 쓸자료) {
        if (पढ्न_मात्र_मान) {
            throw new IllegalStateException("पढनुहोस् 전용 장치입니다.");
        }
        범위확인(सेक्सन_अनुक्रमणिका, 쓸자료);
        System.arraycopy(쓸자료, 0, लगत, सेक्सन_अनुक्रमणिका * सेक्सन_साइज, सेक्सन_साइज);
    }

    public void 지우기() {
        if (पढ्न_मात्र_मान) {
            throw new IllegalStateException("पढनुहोस् 전용 장치입니다.");
        }
        Arrays.fill(लगत, (byte) 0);
    }

    private void 범위확인(int सेक्सन_अनुक्रमणिका, byte[] 임시공간) {
        if (सेक्सन_अनुक्रमणिका < 0 || सेक्सन_अनुक्रमणिका >= 구역수() || 임시공간.length < सेक्सन_साइज) {
            throw new IllegalArgumentException("ATA सेक्सन_मान 범위가 올바르지 않습니다.");
        }
    }
}

