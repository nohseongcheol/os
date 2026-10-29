// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 澳洲.JAusOS.檔案系統;

public final class 檔案信息 {
    private final int 大小;
    private final int 形狀種類;

    public 檔案信息(int 大小, int 形狀種類) {
        this.大小 = 大小;
        this.形狀種類 = 形狀種類;
    }

    public int 大小() {
        return 大小;
    }

    public int 形狀種類() {
        return 形狀種類;
    }
}

