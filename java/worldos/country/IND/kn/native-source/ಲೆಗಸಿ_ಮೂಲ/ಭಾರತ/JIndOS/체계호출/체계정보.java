// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಭಾರತ.JIndOS.체계호출;

public final class 체계정보 {
    private final String ಸಿಸ್ಟಂ_ಹೆಸರು;
    private final String ನೋಡ್_ಹೆಸರು;
    private final String 배포판;
    private final String ಆವೃತ್ತಿ_ಮೌಲ್ಯ;
    private final String ಯಂತ್ರ;

    public 체계정보(String ಸಿಸ್ಟಂ_ಹೆಸರು, String ನೋಡ್_ಹೆಸರು, String 배포판, String ಆವೃತ್ತಿ_ಮೌಲ್ಯ, String ಯಂತ್ರ) {
        this.ಸಿಸ್ಟಂ_ಹೆಸರು = ಸಿಸ್ಟಂ_ಹೆಸರು;
        this.ನೋಡ್_ಹೆಸರು = ನೋಡ್_ಹೆಸರು;
        this.배포판 = 배포판;
        this.ಆವೃತ್ತಿ_ಮೌಲ್ಯ = ಆವೃತ್ತಿ_ಮೌಲ್ಯ;
        this.ಯಂತ್ರ = ಯಂತ್ರ;
    }

    public String ಸಿಸ್ಟಂ_ಹೆಸರು() { return ಸಿಸ್ಟಂ_ಹೆಸರು; }
    public String ನೋಡ್_ಹೆಸರು() { return ನೋಡ್_ಹೆಸರು; }
    public String 배포판() { return 배포판; }
    public String ಆವೃತ್ತಿ_ಮೌಲ್ಯ() { return ಆವೃತ್ತಿ_ಮೌಲ್ಯ; }
    public String ಯಂತ್ರ() { return ಯಂತ್ರ; }
}
