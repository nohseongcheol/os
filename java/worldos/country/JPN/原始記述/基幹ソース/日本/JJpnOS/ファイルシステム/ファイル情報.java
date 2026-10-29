// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本.JJpnOS.ファイルシステム;

public final class ファイル情報 {
    private final int 容量;
    private final int 形状種別;

    public ファイル情報(int 容量, int 形状種別) {
        this.容量 = 容量;
        this.形状種別 = 形状種別;
    }

    public int 容量() {
        return 容量;
    }

    public int 形状種別() {
        return 形状種別;
    }
}

