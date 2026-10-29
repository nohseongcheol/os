// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package மொரிசியஸ்.JMusOS.체계호출;

public final class 체계정보 {
    private final String முறைமை_பெயர்;
    private final String கணு_பெயர்;
    private final String 배포판;
    private final String பதிப்பு_மதிப்பு;
    private final String இயந்திரம்;

    public 체계정보(String முறைமை_பெயர், String கணு_பெயர், String 배포판, String பதிப்பு_மதிப்பு, String இயந்திரம்) {
        this.முறைமை_பெயர் = முறைமை_பெயர்;
        this.கணு_பெயர் = கணு_பெயர்;
        this.배포판 = 배포판;
        this.பதிப்பு_மதிப்பு = பதிப்பு_மதிப்பு;
        this.இயந்திரம் = இயந்திரம்;
    }

    public String முறைமை_பெயர்() { return முறைமை_பெயர்; }
    public String கணு_பெயர்() { return கணு_பெயர்; }
    public String 배포판() { return 배포판; }
    public String பதிப்பு_மதிப்பு() { return பதிப்பு_மதிப்பு; }
    public String இயந்திரம்() { return இயந்திரம்; }
}
