// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.체계호출;

public final class 체계정보 {
    private final String प्रणाली_नांव;
    private final String नोड_नांव;
    private final String 배포판;
    private final String वर्जन_मोल;
    private final String यंत्र;

    public 체계정보(String प्रणाली_नांव, String नोड_नांव, String 배포판, String वर्जन_मोल, String यंत्र) {
        this.प्रणाली_नांव = प्रणाली_नांव;
        this.नोड_नांव = नोड_नांव;
        this.배포판 = 배포판;
        this.वर्जन_मोल = वर्जन_मोल;
        this.यंत्र = यंत्र;
    }

    public String प्रणाली_नांव() { return प्रणाली_नांव; }
    public String नोड_नांव() { return नोड_नांव; }
    public String 배포판() { return 배포판; }
    public String वर्जन_मोल() { return वर्जन_मोल; }
    public String यंत्र() { return यंत्र; }
}
