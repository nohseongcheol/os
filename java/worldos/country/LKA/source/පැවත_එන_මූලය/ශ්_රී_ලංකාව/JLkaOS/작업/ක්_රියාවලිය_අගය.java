// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ශ්_රී_ලංකාව.JLkaOS.작업;

import ශ්_රී_ලංකාව.JLkaOS.기억공간.පිටුව_කළමනාකරු;
import ශ්_රී_ලංකාව.JLkaOS.ගොනු_පද්ධතිය.파일서술자표;

public final class ක්_රියාවලිය_අගය {
    private final int හඳුන්වනය_අගය;
    private final int 부모식별자;
    private final පිටුව_කළමනාකරු.යොමුව_ස්ථානය යොමුව_ස්ථානය;
    private final 파일서술자표 파일서술자;
    private ක්_රියාවලිය_තත්වය තත්වය_අගය = ක්_රියාවලිය_තත්වය.පිළියෙල_කරන්න;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    ක්_රියාවලිය_අගය(int හඳුන්වනය_අගය, int 부모식별자, පිටුව_කළමනාකරු.යොමුව_ස්ථානය යොමුව_ස්ථානය, 파일서술자표 파일서술자) {
        this.හඳුන්වනය_අගය = හඳුන්වනය_අගය;
        this.부모식별자 = 부모식별자;
        this.යොමුව_ස්ථානය = යොමුව_ස්ථානය;
        this.파일서술자 = 파일서술자;
    }

    public int හඳුන්වනය_අගය() {
        return හඳුන්වනය_අගය;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public පිටුව_කළමනාකරු.යොමුව_ස්ථානය යොමුව_ස්ථානය() {
        return යොමුව_ස්ථානය;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public ක්_රියාවලිය_තත්වය තත්වය_අගය() {
        return තත්වය_අගය;
    }

    public void කට්ටලය_තත්වය(ක්_රියාවලිය_තත්වය 새상태) {
        තත්වය_අගය = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void පිටවීම_යෙදු(int අගය) {
        종료값 = අගය & 0xff;
        තත්වය_අගය = ක්_රියාවලිය_තත්වය.පිටවීම_යෙදු;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("යෙදු_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int ඇරඹුම_යොමුව, String[] 인자, String[] 환경) {
        실행시작주소 = ඇරඹුම_යොමුව;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
