// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package फ़िजी.JFjiOS.संग्रहण_उपकरण;

import java.util.Arrays;

/** ATA 28비트 आदेश 계층과 같은 512바이트 논리 खंड_मान 장치다. */
public final class 고급기술결합장치 {
    public static final int खंड_आकार = 512;
    private final byte[] आँकड़े;
    private final boolean केवल_पढ़ने_के_लिए_मान;

    public 고급기술결합장치(int 구역수, boolean केवल_पढ़ने_के_लिए_मान) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("खंड_मान 수가 올바르지 않습니다.");
        }
        आँकड़े = new byte[Math.multiplyExact(구역수, खंड_आकार)];
        this.केवल_पढ़ने_के_लिए_मान = केवल_पढ़ने_के_लिए_मान;
    }

    public int 구역수() {
        return आँकड़े.length / खंड_आकार;
    }

    public void पढ़ें(int खंड_इंडेक्स, byte[] 받을곳) {
        जाँचें_श्रेणी(खंड_इंडेक्स, 받을곳);
        System.arraycopy(आँकड़े, खंड_इंडेक्स * खंड_आकार, 받을곳, 0, खंड_आकार);
    }

    public void लिखें(int खंड_इंडेक्स, byte[] 쓸자료) {
        if (केवल_पढ़ने_के_लिए_मान) {
            throw new IllegalStateException("पढ़ें 전용 장치입니다.");
        }
        जाँचें_श्रेणी(खंड_इंडेक्स, 쓸자료);
        System.arraycopy(쓸자료, 0, आँकड़े, खंड_इंडेक्स * खंड_आकार, खंड_आकार);
    }

    public void मिटाएँ_एन्ट्री() {
        if (केवल_पढ़ने_के_लिए_मान) {
            throw new IllegalStateException("पढ़ें 전용 장치입니다.");
        }
        Arrays.fill(आँकड़े, (byte) 0);
    }

    private void जाँचें_श्रेणी(int खंड_इंडेक्स, byte[] 임시공간) {
        if (खंड_इंडेक्स < 0 || खंड_इंडेक्स >= 구역수() || 임시공간.length < खंड_आकार) {
            throw new IllegalArgumentException("ATA खंड_मान 범위가 올바르지 않습니다.");
        }
    }
}

