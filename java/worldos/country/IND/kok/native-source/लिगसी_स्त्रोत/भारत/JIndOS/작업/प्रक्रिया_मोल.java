// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.작업;

import भारत.JIndOS.기억공간.पान_वेवस्थापक;
import भारत.JIndOS.फायल_प्रणाली.파일서술자표;

public final class प्रक्रिया_मोल {
    private final int वळखुपी_मोल;
    private final int 부모식별자;
    private final पान_वेवस्थापक.नामो_SPACE नामो_SPACE;
    private final 파일서술자표 파일서술자;
    private प्रक्रिया_स्थिती स्थिती_मोल_e10195a1 = प्रक्रिया_स्थिती.तयार_करचें_9ce364fc;
    private int प्रस्थान_करचें_CODE;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    प्रक्रिया_मोल(int वळखुपी_मोल, int 부모식별자, पान_वेवस्थापक.नामो_SPACE नामो_SPACE, 파일서술자표 파일서술자) {
        this.वळखुपी_मोल = वळखुपी_मोल;
        this.부모식별자 = 부모식별자;
        this.नामो_SPACE = नामो_SPACE;
        this.파일서술자 = 파일서술자;
    }

    public int वळखुपी_मोल() {
        return वळखुपी_मोल;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public पान_वेवस्थापक.नामो_SPACE नामो_SPACE() {
        return नामो_SPACE;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public प्रक्रिया_स्थिती स्थिती_मोल_e10195a1() {
        return स्थिती_मोल_e10195a1;
    }

    public void संच_स्थिती(प्रक्रिया_स्थिती 새상태) {
        स्थिती_मोल_e10195a1 = 새상태;
    }

    public int प्रस्थान_करचें_CODE() {
        return प्रस्थान_करचें_CODE;
    }

    public void प्रस्थान_करचें_एप्लिकेशन(int मोल) {
        प्रस्थान_करचें_CODE = मोल & 0xff;
        स्थिती_मोल_e10195a1 = प्रक्रिया_स्थिती.प्रस्थान_करचें_एप्लिकेशन;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("एप्लिकेशन_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int Start_नामो, String[] 인자, String[] 환경) {
        실행시작주소 = Start_नामो;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
