// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package சிங்கப்பூர்.JSgpOS.சேமிப்பகம்_சாதனம்;

import java.util.Arrays;

/** ATA 28비트 கட்டளை 계층과 같은 512바이트 논리 பிரிவு_மதிப்பு 장치다. */
public final class 고급기술결합장치 {
    public static final int பிரிவு_அளவு = 512;
    private final byte[] தரவு;
    private final boolean படிக்க_மட்டும்_மதிப்பு;

    public 고급기술결합장치(int 구역수, boolean படிக்க_மட்டும்_மதிப்பு) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("பிரிவு_மதிப்பு 수가 올바르지 않습니다.");
        }
        தரவு = new byte[Math.multiplyExact(구역수, பிரிவு_அளவு)];
        this.படிக்க_மட்டும்_மதிப்பு = படிக்க_மட்டும்_மதிப்பு;
    }

    public int 구역수() {
        return தரவு.length / பிரிவு_அளவு;
    }

    public void படி(int பிரிவு_அடைவு, byte[] 받을곳) {
        범위확인(பிரிவு_அடைவு, 받을곳);
        System.arraycopy(தரவு, பிரிவு_அடைவு * பிரிவு_அளவு, 받을곳, 0, பிரிவு_அளவு);
    }

    public void எழுது(int பிரிவு_அடைவு, byte[] 쓸자료) {
        if (படிக்க_மட்டும்_மதிப்பு) {
            throw new IllegalStateException("படி 전용 장치입니다.");
        }
        범위확인(பிரிவு_அடைவு, 쓸자료);
        System.arraycopy(쓸자료, 0, தரவு, பிரிவு_அடைவு * பிரிவு_அளவு, பிரிவு_அளவு);
    }

    public void அழி_உள்ளீடு() {
        if (படிக்க_மட்டும்_மதிப்பு) {
            throw new IllegalStateException("படி 전용 장치입니다.");
        }
        Arrays.fill(தரவு, (byte) 0);
    }

    private void 범위확인(int பிரிவு_அடைவு, byte[] 임시공간) {
        if (பிரிவு_அடைவு < 0 || பிரிவு_அடைவு >= 구역수() || 임시공간.length < பிரிவு_அளவு) {
            throw new IllegalArgumentException("ATA பிரிவு_மதிப்பு 범위가 올바르지 않습니다.");
        }
    }
}

