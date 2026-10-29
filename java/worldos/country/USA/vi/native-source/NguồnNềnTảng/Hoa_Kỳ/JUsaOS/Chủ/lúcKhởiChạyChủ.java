// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hoa_Kỳ.JUsaOS.Chủ;

import Hoa_Kỳ.JUsaOS.Nhân.Nhân;

public final class lúcKhởiChạyChủ {
    private lúcKhởiChạyChủ() {
    }

    public static void main(String[] đốiSốThamSố) {
        Nhân giáTrịNhân = new Nhân(new PhầnCứngChủ());
        giáTrịNhân.chạy();
        giáTrịNhân.thựcThiBước();
    }
}

