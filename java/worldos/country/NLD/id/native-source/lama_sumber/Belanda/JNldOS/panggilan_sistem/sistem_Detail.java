// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Belanda.JNldOS.panggilan_sistem;

public final class sistem_Detail {
    private final String sistem_nama;
    private final String node_nama;
    private final String 배포판;
    private final String versi_VALUE;
    private final String mesin;

    public sistem_Detail(String sistem_nama, String node_nama, String 배포판, String versi_VALUE, String mesin) {
        this.sistem_nama = sistem_nama;
        this.node_nama = node_nama;
        this.배포판 = 배포판;
        this.versi_VALUE = versi_VALUE;
        this.mesin = mesin;
    }

    public String sistem_nama() { return sistem_nama; }
    public String node_nama() { return node_nama; }
    public String 배포판() { return 배포판; }
    public String versi_VALUE() { return versi_VALUE; }
    public String mesin() { return mesin; }
}
