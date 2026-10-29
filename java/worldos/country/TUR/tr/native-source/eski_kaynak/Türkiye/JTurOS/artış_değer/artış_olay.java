// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkiye.JTurOS.artış_değer;

public final class artış_olay {
    public enum Tip_değer {
        tuş_kapalı,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final Tip_değer olay_türü;
    private final int 첫째값;
    private final int SANİYE_değer;

    public artış_olay(Tip_değer olay_türü, int 첫째값, int SANİYE_değer) {
        this.olay_türü = olay_türü;
        this.첫째값 = 첫째값;
        this.SANİYE_değer = SANİYE_değer;
    }

    public Tip_değer olay_türü() {
        return olay_türü;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int SANİYE_değer() {
        return SANİYE_değer;
    }
}

