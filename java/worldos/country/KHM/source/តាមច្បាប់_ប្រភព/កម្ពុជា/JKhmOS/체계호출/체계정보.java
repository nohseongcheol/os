// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package កម្ពុជា.JKhmOS.체계호출;

public final class 체계정보 {
    private final String ប្រព័ន្ធ_ឈ្មោះ;
    private final String ណូត_ឈ្មោះ;
    private final String 배포판;
    private final String កំណែ_តំលៃ;
    private final String ម៉ាស៊ីន;

    public 체계정보(String ប្រព័ន្ធ_ឈ្មោះ, String ណូត_ឈ្មោះ, String 배포판, String កំណែ_តំលៃ, String ម៉ាស៊ីន) {
        this.ប្រព័ន្ធ_ឈ្មោះ = ប្រព័ន្ធ_ឈ្មោះ;
        this.ណូត_ឈ្មោះ = ណូត_ឈ្មោះ;
        this.배포판 = 배포판;
        this.កំណែ_តំលៃ = កំណែ_តំលៃ;
        this.ម៉ាស៊ីន = ម៉ាស៊ីន;
    }

    public String ប្រព័ន្ធ_ឈ្មោះ() { return ប្រព័ន្ធ_ឈ្មោះ; }
    public String ណូត_ឈ្មោះ() { return ណូត_ឈ្មោះ; }
    public String 배포판() { return 배포판; }
    public String កំណែ_តំលៃ() { return កំណែ_តំលៃ; }
    public String ម៉ាស៊ីន() { return ម៉ាស៊ីន; }
}
