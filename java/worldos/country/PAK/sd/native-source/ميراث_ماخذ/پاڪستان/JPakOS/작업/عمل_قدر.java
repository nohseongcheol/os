// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاڪستان.JPakOS.작업;

import پاڪستان.JPakOS.기억공간.صفحو_مئنيجر;
import پاڪستان.JPakOS.فائل_سسٽم.파일서술자표;

public final class عمل_قدر {
    private final int سڃاڻپ_ڪندڙ_قدر;
    private final int 부모식별자;
    private final صفحو_مئنيجر.پتو_جڳهه پتو_جڳهه;
    private final 파일서술자표 파일서술자;
    private عمل_حالت حالت_قدر = عمل_حالت.تياري_ڪريو;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    عمل_قدر(int سڃاڻپ_ڪندڙ_قدر, int 부모식별자, صفحو_مئنيجر.پتو_جڳهه پتو_جڳهه, 파일서술자표 파일서술자) {
        this.سڃاڻپ_ڪندڙ_قدر = سڃاڻپ_ڪندڙ_قدر;
        this.부모식별자 = 부모식별자;
        this.پتو_جڳهه = پتو_جڳهه;
        this.파일서술자 = 파일서술자;
    }

    public int سڃاڻپ_ڪندڙ_قدر() {
        return سڃاڻپ_ڪندڙ_قدر;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public صفحو_مئنيجر.پتو_جڳهه پتو_جڳهه() {
        return پتو_جڳهه;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public عمل_حالت حالت_قدر() {
        return حالت_قدر;
    }

    public void سيٽ_حالت(عمل_حالت 새상태) {
        حالت_قدر = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void خارج_ڪريو_ائپ(int قدر) {
        종료값 = قدر & 0xff;
        حالت_قدر = عمل_حالت.خارج_ڪريو_ائپ;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("ائپ_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int شروع_پتو, String[] 인자, String[] 환경) {
        실행시작주소 = شروع_پتو;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
