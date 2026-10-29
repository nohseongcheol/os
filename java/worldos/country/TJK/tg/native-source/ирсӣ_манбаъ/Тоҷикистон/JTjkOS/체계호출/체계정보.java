// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Тоҷикистон.JTjkOS.체계호출;

public final class 체계정보 {
    private final String система_ном;
    private final String гиреҳ_ном;
    private final String 배포판;
    private final String версия_қимат;
    private final String компютер;

    public 체계정보(String система_ном, String гиреҳ_ном, String 배포판, String версия_қимат, String компютер) {
        this.система_ном = система_ном;
        this.гиреҳ_ном = гиреҳ_ном;
        this.배포판 = 배포판;
        this.версия_қимат = версия_қимат;
        this.компютер = компютер;
    }

    public String система_ном() { return система_ном; }
    public String гиреҳ_ном() { return гиреҳ_ном; }
    public String 배포판() { return 배포판; }
    public String версия_қимат() { return версия_қимат; }
    public String компютер() { return компютер; }
}
