// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package EMzantsi_Afrika.JZafOS.체계호출;

public final class 체계정보 {
    private final String inkqubo_igama;
    private final String inowudi_igama;
    private final String 배포판;
    private final String inguqulelo_ixabiso;
    private final String umatshini;

    public 체계정보(String inkqubo_igama, String inowudi_igama, String 배포판, String inguqulelo_ixabiso, String umatshini) {
        this.inkqubo_igama = inkqubo_igama;
        this.inowudi_igama = inowudi_igama;
        this.배포판 = 배포판;
        this.inguqulelo_ixabiso = inguqulelo_ixabiso;
        this.umatshini = umatshini;
    }

    public String inkqubo_igama() { return inkqubo_igama; }
    public String inowudi_igama() { return inowudi_igama; }
    public String 배포판() { return 배포판; }
    public String inguqulelo_ixabiso() { return inguqulelo_ixabiso; }
    public String umatshini() { return umatshini; }
}
