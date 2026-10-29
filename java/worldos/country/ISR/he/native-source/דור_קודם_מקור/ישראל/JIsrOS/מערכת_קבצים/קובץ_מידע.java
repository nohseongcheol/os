// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ישראל.JIsrOS.מערכת_קבצים;

public final class קובץ_מידע {
    private final int גודל;
    private final int 형태;

    public קובץ_מידע(int גודל, int 형태) {
        this.גודל = גודל;
        this.형태 = 형태;
    }

    public int גודל() {
        return גודל;
    }

    public int 형태() {
        return 형태;
    }
}

