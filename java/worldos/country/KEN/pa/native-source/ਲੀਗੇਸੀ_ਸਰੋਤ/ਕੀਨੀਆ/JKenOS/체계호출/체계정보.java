// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਕੀਨੀਆ.JKenOS.체계호출;

public final class 체계정보 {
    private final String ਪਰਬੰਧ_ਨਾਮ;
    private final String ਨੋਡ_ਨਾਮ;
    private final String 배포판;
    private final String ਵਰਜ਼ਨ_ਕੀਮਤ;
    private final String ਮਸ਼ੀਨ;

    public 체계정보(String ਪਰਬੰਧ_ਨਾਮ, String ਨੋਡ_ਨਾਮ, String 배포판, String ਵਰਜ਼ਨ_ਕੀਮਤ, String ਮਸ਼ੀਨ) {
        this.ਪਰਬੰਧ_ਨਾਮ = ਪਰਬੰਧ_ਨਾਮ;
        this.ਨੋਡ_ਨਾਮ = ਨੋਡ_ਨਾਮ;
        this.배포판 = 배포판;
        this.ਵਰਜ਼ਨ_ਕੀਮਤ = ਵਰਜ਼ਨ_ਕੀਮਤ;
        this.ਮਸ਼ੀਨ = ਮਸ਼ੀਨ;
    }

    public String ਪਰਬੰਧ_ਨਾਮ() { return ਪਰਬੰਧ_ਨਾਮ; }
    public String ਨੋਡ_ਨਾਮ() { return ਨੋਡ_ਨਾਮ; }
    public String 배포판() { return 배포판; }
    public String ਵਰਜ਼ਨ_ਕੀਮਤ() { return ਵਰਜ਼ਨ_ਕੀਮਤ; }
    public String ਮਸ਼ੀਨ() { return ਮਸ਼ੀਨ; }
}
