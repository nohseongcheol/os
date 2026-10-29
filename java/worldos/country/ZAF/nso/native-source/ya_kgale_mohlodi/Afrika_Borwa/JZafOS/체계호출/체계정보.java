// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Afrika_Borwa.JZafOS.체계호출;

public final class 체계정보 {
    private final String lenaneo_leina;
    private final String noute_leina;
    private final String 배포판;
    private final String bešene_boleng;
    private final String motšhene;

    public 체계정보(String lenaneo_leina, String noute_leina, String 배포판, String bešene_boleng, String motšhene) {
        this.lenaneo_leina = lenaneo_leina;
        this.noute_leina = noute_leina;
        this.배포판 = 배포판;
        this.bešene_boleng = bešene_boleng;
        this.motšhene = motšhene;
    }

    public String lenaneo_leina() { return lenaneo_leina; }
    public String noute_leina() { return noute_leina; }
    public String 배포판() { return 배포판; }
    public String bešene_boleng() { return bešene_boleng; }
    public String motšhene() { return motšhene; }
}
