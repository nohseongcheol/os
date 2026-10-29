// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espainia.JEspOS.fitxategi_sistema;

public final class fitxategi_info {
    private final int Tamaina;
    private final int 형태;

    public fitxategi_info(int Tamaina, int 형태) {
        this.Tamaina = Tamaina;
        this.형태 = 형태;
    }

    public int Tamaina() {
        return Tamaina;
    }

    public int 형태() {
        return 형태;
    }
}

