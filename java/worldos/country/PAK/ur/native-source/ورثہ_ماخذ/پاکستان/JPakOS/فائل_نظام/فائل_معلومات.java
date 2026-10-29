// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاکستان.JPakOS.فائل_نظام;

public final class فائل_معلومات {
    private final int حجم;
    private final int 형태;

    public فائل_معلومات(int حجم, int 형태) {
        this.حجم = حجم;
        this.형태 = 형태;
    }

    public int حجم() {
        return حجم;
    }

    public int 형태() {
        return 형태;
    }
}

