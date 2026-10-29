// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Grønland.JGrlOS.체계호출;

public final class System_Detaljer {
    private final String System_navn;
    private final String node_navn;
    private final String 배포판;
    private final String version_VÆRDI;
    private final String maskine;

    public System_Detaljer(String System_navn, String node_navn, String 배포판, String version_VÆRDI, String maskine) {
        this.System_navn = System_navn;
        this.node_navn = node_navn;
        this.배포판 = 배포판;
        this.version_VÆRDI = version_VÆRDI;
        this.maskine = maskine;
    }

    public String System_navn() { return System_navn; }
    public String node_navn() { return node_navn; }
    public String 배포판() { return 배포판; }
    public String version_VÆRDI() { return version_VÆRDI; }
    public String maskine() { return maskine; }
}
