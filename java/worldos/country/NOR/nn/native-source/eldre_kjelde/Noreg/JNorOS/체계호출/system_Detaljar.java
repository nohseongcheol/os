// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Noreg.JNorOS.체계호출;

public final class system_Detaljar {
    private final String system_namn;
    private final String node_namn;
    private final String 배포판;
    private final String versjon_VALUE;
    private final String maskin;

    public system_Detaljar(String system_namn, String node_namn, String 배포판, String versjon_VALUE, String maskin) {
        this.system_namn = system_namn;
        this.node_namn = node_namn;
        this.배포판 = 배포판;
        this.versjon_VALUE = versjon_VALUE;
        this.maskin = maskin;
    }

    public String system_namn() { return system_namn; }
    public String node_namn() { return node_namn; }
    public String 배포판() { return 배포판; }
    public String versjon_VALUE() { return versjon_VALUE; }
    public String maskin() { return maskin; }
}
