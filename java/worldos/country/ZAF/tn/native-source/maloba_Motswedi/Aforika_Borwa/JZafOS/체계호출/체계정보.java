// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aforika_Borwa.JZafOS.체계호출;

public final class 체계정보 {
    private final String tsamaiso_leina;
    private final String sekopanyamafaratlhatlha_leina;
    private final String 배포판;
    private final String kgaolo_Boleng;
    private final String motšhine;

    public 체계정보(String tsamaiso_leina, String sekopanyamafaratlhatlha_leina, String 배포판, String kgaolo_Boleng, String motšhine) {
        this.tsamaiso_leina = tsamaiso_leina;
        this.sekopanyamafaratlhatlha_leina = sekopanyamafaratlhatlha_leina;
        this.배포판 = 배포판;
        this.kgaolo_Boleng = kgaolo_Boleng;
        this.motšhine = motšhine;
    }

    public String tsamaiso_leina() { return tsamaiso_leina; }
    public String sekopanyamafaratlhatlha_leina() { return sekopanyamafaratlhatlha_leina; }
    public String 배포판() { return 배포판; }
    public String kgaolo_Boleng() { return kgaolo_Boleng; }
    public String motšhine() { return motšhine; }
}
