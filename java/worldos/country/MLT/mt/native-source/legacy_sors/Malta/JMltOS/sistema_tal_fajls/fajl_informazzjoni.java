// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malta.JMltOS.sistema_tal_fajls;

public final class fajl_informazzjoni {
    private final int daqqas;
    private final int 형태;

    public fajl_informazzjoni(int daqqas, int 형태) {
        this.daqqas = daqqas;
        this.형태 = 형태;
    }

    public int daqqas() {
        return daqqas;
    }

    public int 형태() {
        return 형태;
    }
}

