// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bulgaristan.JBgrOS.sistem_çağrısı;

public final class Sistem_Ayrıntılar {
    private final String Sistem_ad;
    private final String düğüm_ad;
    private final String sürüm_değer_237a4c94;
    private final String sürüm_değer;
    private final String makine;

    public Sistem_Ayrıntılar(String Sistem_ad, String düğüm_ad, String sürüm_değer_237a4c94, String sürüm_değer, String makine) {
        this.Sistem_ad = Sistem_ad;
        this.düğüm_ad = düğüm_ad;
        this.sürüm_değer_237a4c94 = sürüm_değer_237a4c94;
        this.sürüm_değer = sürüm_değer;
        this.makine = makine;
    }

    public String Sistem_ad() { return Sistem_ad; }
    public String düğüm_ad() { return düğüm_ad; }
    public String sürüm_değer_237a4c94() { return sürüm_değer_237a4c94; }
    public String sürüm_değer() { return sürüm_değer; }
    public String makine() { return makine; }
}
