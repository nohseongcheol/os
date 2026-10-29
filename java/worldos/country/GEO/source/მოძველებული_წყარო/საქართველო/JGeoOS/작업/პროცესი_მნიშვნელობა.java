// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package საქართველო.JGeoOS.작업;

import საქართველო.JGeoOS.기억공간.გვერდი_მმართველი;
import საქართველო.JGeoOS.ფაილური_სისტემა.파일서술자표;

public final class პროცესი_მნიშვნელობა {
    private final int იდენტიფიკატორი_მნიშვნელობა;
    private final int 부모식별자;
    private final გვერდი_მმართველი.მისამართი_სივრცე მისამართი_სივრცე;
    private final 파일서술자표 파일서술자;
    private პროცესი_სტატუსი სტატუსი_მნიშვნელობა = პროცესი_სტატუსი.მომზადება;
    private int გასვლა_კოდექსი;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    პროცესი_მნიშვნელობა(int იდენტიფიკატორი_მნიშვნელობა, int 부모식별자, გვერდი_მმართველი.მისამართი_სივრცე მისამართი_სივრცე, 파일서술자표 파일서술자) {
        this.იდენტიფიკატორი_მნიშვნელობა = იდენტიფიკატორი_მნიშვნელობა;
        this.부모식별자 = 부모식별자;
        this.მისამართი_სივრცე = მისამართი_სივრცე;
        this.파일서술자 = 파일서술자;
    }

    public int იდენტიფიკატორი_მნიშვნელობა() {
        return იდენტიფიკატორი_მნიშვნელობა;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public გვერდი_მმართველი.მისამართი_სივრცე მისამართი_სივრცე() {
        return მისამართი_სივრცე;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public პროცესი_სტატუსი სტატუსი_მნიშვნელობა() {
        return სტატუსი_მნიშვნელობა;
    }

    public void ნაკრები_სტატუსი(პროცესი_სტატუსი 새상태) {
        სტატუსი_მნიშვნელობა = 새상태;
    }

    public int გასვლა_კოდექსი() {
        return გასვლა_კოდექსი;
    }

    public void გასვლა_აპი(int მნიშვნელობა) {
        გასვლა_კოდექსი = მნიშვნელობა & 0xff;
        სტატუსი_მნიშვნელობა = პროცესი_სტატუსი.გასვლა_აპი;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("აპი_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int დაწყება_მისამართი, String[] 인자, String[] 환경) {
        실행시작주소 = დაწყება_მისამართი;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
