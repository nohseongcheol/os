// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኢትዮጵያ.JEthOS.작업;

import ኢትዮጵያ.JEthOS.기억공간.ገጽ_አስተዳዳሪ;
import ኢትዮጵያ.JEthOS.የፋይል_ስርዓት.파일서술자표;

public final class ሂደት_እሴት {
    private final int መለያ_እሴት_5b7b8b77;
    private final int 부모식별자;
    private final ገጽ_አስተዳዳሪ.አድራሻ_ቦታ አድራሻ_ቦታ;
    private final 파일서술자표 파일서술자;
    private ሂደት_ዞን ዞን_እሴት = ሂደት_ዞን.አዘጋጅ_9ce364fc;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    ሂደት_እሴት(int መለያ_እሴት_5b7b8b77, int 부모식별자, ገጽ_አስተዳዳሪ.አድራሻ_ቦታ አድራሻ_ቦታ, 파일서술자표 파일서술자) {
        this.መለያ_እሴት_5b7b8b77 = መለያ_እሴት_5b7b8b77;
        this.부모식별자 = 부모식별자;
        this.አድራሻ_ቦታ = አድራሻ_ቦታ;
        this.파일서술자 = 파일서술자;
    }

    public int መለያ_እሴት_5b7b8b77() {
        return መለያ_እሴት_5b7b8b77;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public ገጽ_አስተዳዳሪ.አድራሻ_ቦታ አድራሻ_ቦታ() {
        return አድራሻ_ቦታ;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public ሂደት_ዞን ዞን_እሴት() {
        return ዞን_እሴት;
    }

    public void ስብስብ_ዞን(ሂደት_ዞን 새상태) {
        ዞን_እሴት = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void ውጣ_ፕሮግራም(int እሴት) {
        종료값 = እሴት & 0xff;
        ዞን_እሴት = ሂደት_ዞን.ውጣ_ፕሮግራም;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("ፕሮግራም_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int ጀምር_አድራሻ, String[] ግቤት_ነጋሪ_እሴት, String[] 환경) {
        실행시작주소 = ጀምር_አድራሻ;
        실행인자 = ግቤት_ነጋሪ_እሴት.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
