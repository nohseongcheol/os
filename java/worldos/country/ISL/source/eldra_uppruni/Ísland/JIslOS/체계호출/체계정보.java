// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ísland.JIslOS.체계호출;

public final class 체계정보 {
    private final String kerfi_heiti;
    private final String hnútur_heiti;
    private final String 배포판;
    private final String útgáfa_VALUE;
    private final String vél;

    public 체계정보(String kerfi_heiti, String hnútur_heiti, String 배포판, String útgáfa_VALUE, String vél) {
        this.kerfi_heiti = kerfi_heiti;
        this.hnútur_heiti = hnútur_heiti;
        this.배포판 = 배포판;
        this.útgáfa_VALUE = útgáfa_VALUE;
        this.vél = vél;
    }

    public String kerfi_heiti() { return kerfi_heiti; }
    public String hnútur_heiti() { return hnútur_heiti; }
    public String 배포판() { return 배포판; }
    public String útgáfa_VALUE() { return útgáfa_VALUE; }
    public String vél() { return vél; }
}
