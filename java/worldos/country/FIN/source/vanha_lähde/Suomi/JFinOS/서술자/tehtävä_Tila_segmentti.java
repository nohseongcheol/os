// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Suomi.JFinOS.서술자;

/** x86 작업 MUUTA_tila 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class tehtävä_Tila_segmentti {
    private int Pino_nolla_Esto;
    private int Pino_nolla_OSOITE;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int OSOITE) {
        Pino_nolla_Esto = 조각;
        Pino_nolla_OSOITE = OSOITE;
    }

    public int Pino_nolla_Esto() { return Pino_nolla_Esto; }
    public int Pino_nolla_OSOITE() { return Pino_nolla_OSOITE; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

