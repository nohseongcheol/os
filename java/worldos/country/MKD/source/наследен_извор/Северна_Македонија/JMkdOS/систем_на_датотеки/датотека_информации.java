// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Северна_Македонија.JMkdOS.систем_на_датотеки;

public final class датотека_информации {
    private final int Големина;
    private final int 형태;

    public датотека_информации(int Големина, int 형태) {
        this.Големина = Големина;
        this.형태 = 형태;
    }

    public int Големина() {
        return Големина;
    }

    public int 형태() {
        return 형태;
    }
}

