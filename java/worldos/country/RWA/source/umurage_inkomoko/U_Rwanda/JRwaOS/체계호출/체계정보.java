// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package U_Rwanda.JRwaOS.체계호출;

public final class 체계정보 {
    private final String sisitemu_izina;
    private final String ipfundo_izina;
    private final String 배포판;
    private final String verisiyo_agaciro;
    private final String imashini;

    public 체계정보(String sisitemu_izina, String ipfundo_izina, String 배포판, String verisiyo_agaciro, String imashini) {
        this.sisitemu_izina = sisitemu_izina;
        this.ipfundo_izina = ipfundo_izina;
        this.배포판 = 배포판;
        this.verisiyo_agaciro = verisiyo_agaciro;
        this.imashini = imashini;
    }

    public String sisitemu_izina() { return sisitemu_izina; }
    public String ipfundo_izina() { return ipfundo_izina; }
    public String 배포판() { return 배포판; }
    public String verisiyo_agaciro() { return verisiyo_agaciro; }
    public String imashini() { return imashini; }
}
