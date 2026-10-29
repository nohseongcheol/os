// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hoa_Kỳ.JUsaOS.giáTrịVào;

public final class sựKiệnĐầuVào {
    public enum giáTrịLoại {
        xuốngPhím,
        lênPhím,
        chuyểnĐộngChuột,
        đãNhấnNútChuột,
        đãGiảiPhóngNútChuột
    }

    private final giáTrịLoại loạiSựKiện;
    private final int giáTrịĐầuTiên;
    private final int giáTrịThứHai;

    public sựKiệnĐầuVào(giáTrịLoại loạiSựKiện, int giáTrịĐầuTiên, int giáTrịThứHai) {
        this.loạiSựKiện = loạiSựKiện;
        this.giáTrịĐầuTiên = giáTrịĐầuTiên;
        this.giáTrịThứHai = giáTrịThứHai;
    }

    public giáTrịLoại loạiSựKiện() {
        return loạiSựKiện;
    }

    public int giáTrịĐầuTiên() {
        return giáTrịĐầuTiên;
    }

    public int giáTrịThứHai() {
        return giáTrịThứHai;
    }
}

