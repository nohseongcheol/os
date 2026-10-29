// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Việt_Nam.JVnmOS.Chủ;

import Việt_Nam.JVnmOS.Nhân.Nhân;

public final class lúcKhởiChạyChủ {
    private lúcKhởiChạyChủ() {
    }

    public static void main(String[] đốiSốThamSố) {
        Nhân giáTrịNhân = new Nhân(new PhầnCứngChủ());
        giáTrịNhân.chạy();
        giáTrịNhân.thựcThiBước();
    }
}

