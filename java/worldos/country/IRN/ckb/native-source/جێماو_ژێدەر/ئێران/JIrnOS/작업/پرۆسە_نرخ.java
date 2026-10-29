// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ئێران.JIrnOS.작업;

import ئێران.JIrnOS.기억공간.لاپەڕە_بەڕێوەبەر;
import ئێران.JIrnOS.سیستمی_فایل.파일서술자표;

public final class پرۆسە_نرخ {
    private final int ناسێنەر_نرخ;
    private final int 부모식별자;
    private final لاپەڕە_بەڕێوەبەر.ناونیشان_مەودا ناونیشان_مەودا;
    private final 파일서술자표 파일서술자;
    private پرۆسە_دۆخ_4346e67f دۆخ_نرخ = پرۆسە_دۆخ_4346e67f.ئامادە_کردن_9ce364fc;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    پرۆسە_نرخ(int ناسێنەر_نرخ, int 부모식별자, لاپەڕە_بەڕێوەبەر.ناونیشان_مەودا ناونیشان_مەودا, 파일서술자표 파일서술자) {
        this.ناسێنەر_نرخ = ناسێنەر_نرخ;
        this.부모식별자 = 부모식별자;
        this.ناونیشان_مەودا = ناونیشان_مەودا;
        this.파일서술자 = 파일서술자;
    }

    public int ناسێنەر_نرخ() {
        return ناسێنەر_نرخ;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public لاپەڕە_بەڕێوەبەر.ناونیشان_مەودا ناونیشان_مەودا() {
        return ناونیشان_مەودا;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public پرۆسە_دۆخ_4346e67f دۆخ_نرخ() {
        return دۆخ_نرخ;
    }

    public void سێت_دۆخ(پرۆسە_دۆخ_4346e67f 새상태) {
        دۆخ_نرخ = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void بزربوون_بەرنامە(int نرخ) {
        종료값 = نرخ & 0xff;
        دۆخ_نرخ = پرۆسە_دۆخ_4346e67f.بزربوون_بەرنامە;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("بەرنامە_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int دەستپێك_ناونیشان, String[] 인자, String[] 환경) {
        실행시작주소 = دەستپێك_ناونیشان;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
