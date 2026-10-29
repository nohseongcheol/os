// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Naịjịrịa.JNgaOS.체계호출;

public final class 체계정보 {
    private final String sistèm_akara_ahà;
    private final String akpụ_akara_ahà;
    private final String 배포판;
    private final String ụdị_valuu;
    private final String ngwa_komputa;

    public 체계정보(String sistèm_akara_ahà, String akpụ_akara_ahà, String 배포판, String ụdị_valuu, String ngwa_komputa) {
        this.sistèm_akara_ahà = sistèm_akara_ahà;
        this.akpụ_akara_ahà = akpụ_akara_ahà;
        this.배포판 = 배포판;
        this.ụdị_valuu = ụdị_valuu;
        this.ngwa_komputa = ngwa_komputa;
    }

    public String sistèm_akara_ahà() { return sistèm_akara_ahà; }
    public String akpụ_akara_ahà() { return akpụ_akara_ahà; }
    public String 배포판() { return 배포판; }
    public String ụdị_valuu() { return ụdị_valuu; }
    public String ngwa_komputa() { return ngwa_komputa; }
}
