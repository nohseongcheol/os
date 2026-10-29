// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malaysia.JMysOS.panggilan_sistem;

public final class sistem_Butiran {
    private final String sistem_nama;
    private final String nod_nama;
    private final String 배포판;
    private final String versi_VALUE;
    private final String mesin;

    public sistem_Butiran(String sistem_nama, String nod_nama, String 배포판, String versi_VALUE, String mesin) {
        this.sistem_nama = sistem_nama;
        this.nod_nama = nod_nama;
        this.배포판 = 배포판;
        this.versi_VALUE = versi_VALUE;
        this.mesin = mesin;
    }

    public String sistem_nama() { return sistem_nama; }
    public String nod_nama() { return nod_nama; }
    public String 배포판() { return 배포판; }
    public String versi_VALUE() { return versi_VALUE; }
    public String mesin() { return mesin; }
}
