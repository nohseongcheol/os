// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाल.JNplOS.체계호출;

public final class 체계정보 {
    private final String प्रणाली_नाम;
    private final String नोड_नाम;
    private final String 배포판;
    private final String संस्करण_मान;
    private final String मेशिन;

    public 체계정보(String प्रणाली_नाम, String नोड_नाम, String 배포판, String संस्करण_मान, String मेशिन) {
        this.प्रणाली_नाम = प्रणाली_नाम;
        this.नोड_नाम = नोड_नाम;
        this.배포판 = 배포판;
        this.संस्करण_मान = संस्करण_मान;
        this.मेशिन = मेशिन;
    }

    public String प्रणाली_नाम() { return प्रणाली_नाम; }
    public String नोड_नाम() { return नोड_नाम; }
    public String 배포판() { return 배포판; }
    public String संस्करण_मान() { return संस्करण_मान; }
    public String मेशिन() { return मेशिन; }
}
