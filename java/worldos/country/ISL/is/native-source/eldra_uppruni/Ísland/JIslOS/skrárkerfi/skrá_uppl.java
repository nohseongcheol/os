// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ísland.JIslOS.skrárkerfi;

public final class skrá_uppl {
    private final int Stærð;
    private final int 형태;

    public skrá_uppl(int Stærð, int 형태) {
        this.Stærð = Stærð;
        this.형태 = 형태;
    }

    public int Stærð() {
        return Stærð;
    }

    public int 형태() {
        return 형태;
    }
}

