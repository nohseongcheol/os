// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package عمان.JOmnOS.سیستم_پرونده;

public final class فایل_اطلاعات {
    private final int اندازه;
    private final int 형태;

    public فایل_اطلاعات(int اندازه, int 형태) {
        this.اندازه = اندازه;
        this.형태 = 형태;
    }

    public int اندازه() {
        return اندازه;
    }

    public int 형태() {
        return 형태;
    }
}

