// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলাদেশ.JBgdOS.স্টোরেজ_ডিভাইস;

import java.util.Arrays;

/** ATA 28비트 আদেশ 계층과 같은 512바이트 논리 শাখা_মান_366e0bfa 장치다. */
public final class 고급기술결합장치 {
    public static final int শাখা_আয়তন = 512;
    private final byte[] ডাটা;
    private final boolean কেবল_পাঠযোগ্য_মান;

    public 고급기술결합장치(int 구역수, boolean কেবল_পাঠযোগ্য_মান) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("শাখা_মান_366e0bfa 수가 올바르지 않습니다.");
        }
        ডাটা = new byte[Math.multiplyExact(구역수, শাখা_আয়তন)];
        this.কেবল_পাঠযোগ্য_মান = কেবল_পাঠযোগ্য_মান;
    }

    public int 구역수() {
        return ডাটা.length / শাখা_আয়তন;
    }

    public void পড়া(int শাখা_সূচি, byte[] 받을곳) {
        범위확인(শাখা_সূচি, 받을곳);
        System.arraycopy(ডাটা, শাখা_সূচি * শাখা_আয়তন, 받을곳, 0, শাখা_আয়তন);
    }

    public void লেখা(int শাখা_সূচি, byte[] 쓸자료) {
        if (কেবল_পাঠযোগ্য_মান) {
            throw new IllegalStateException("পড়া 전용 장치입니다.");
        }
        범위확인(শাখা_সূচি, 쓸자료);
        System.arraycopy(쓸자료, 0, ডাটা, শাখা_সূচি * শাখা_আয়তন, শাখা_আয়তন);
    }

    public void মুছুন_ভুক্তি() {
        if (কেবল_পাঠযোগ্য_মান) {
            throw new IllegalStateException("পড়া 전용 장치입니다.");
        }
        Arrays.fill(ডাটা, (byte) 0);
    }

    private void 범위확인(int শাখা_সূচি, byte[] 임시공간) {
        if (শাখা_সূচি < 0 || শাখা_সূচি >= 구역수() || 임시공간.length < শাখা_আয়তন) {
            throw new IllegalArgumentException("ATA শাখা_মান_366e0bfa 범위가 올바르지 않습니다.");
        }
    }
}

