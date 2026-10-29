// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاکستان.JPakOS.작업;

import پاکستان.JPakOS.기억공간.صفحہ_مینیجر;
import پاکستان.JPakOS.فائل_سسٹم.파일서술자표;

public final class عمل_قدر {
    private final int شناخت_کرنڑ_آلا_قدر;
    private final int 부모식별자;
    private final صفحہ_مینیجر.پتا_جگہ پتا_جگہ;
    private final 파일서술자표 파일서술자;
    private عمل_حالت حالت_قدر = عمل_حالت.تیاری_کرو;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    عمل_قدر(int شناخت_کرنڑ_آلا_قدر, int 부모식별자, صفحہ_مینیجر.پتا_جگہ پتا_جگہ, 파일서술자표 파일서술자) {
        this.شناخت_کرنڑ_آلا_قدر = شناخت_کرنڑ_آلا_قدر;
        this.부모식별자 = 부모식별자;
        this.پتا_جگہ = پتا_جگہ;
        this.파일서술자 = 파일서술자;
    }

    public int شناخت_کرنڑ_آلا_قدر() {
        return شناخت_کرنڑ_آلا_قدر;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public صفحہ_مینیجر.پتا_جگہ پتا_جگہ() {
        return پتا_جگہ;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public عمل_حالت حالت_قدر() {
        return حالت_قدر;
    }

    public void سیٹ_حالت(عمل_حالت 새상태) {
        حالت_قدر = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void خارج_کرو_ایپ(int قدر) {
        종료값 = قدر & 0xff;
        حالت_قدر = عمل_حالت.خارج_کرو_ایپ;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("ایپ_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int مکھ_پتا, String[] 인자, String[] 환경) {
        실행시작주소 = مکھ_پتا;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
