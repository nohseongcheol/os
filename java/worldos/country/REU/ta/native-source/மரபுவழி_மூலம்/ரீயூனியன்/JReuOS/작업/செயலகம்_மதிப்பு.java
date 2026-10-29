// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ரீயூனியன்.JReuOS.작업;

import ரீயூனியன்.JReuOS.기억공간.பக்கம்_மேலாளர்;
import ரீயூனியன்.JReuOS.கோப்பு_முறைமை.파일서술자표;

public final class செயலகம்_மதிப்பு {
    private final int அடையாளங்காட்டி_மதிப்பு;
    private final int 부모식별자;
    private final பக்கம்_மேலாளர்.முகவரி_தளம் முகவரி_தளம்;
    private final 파일서술자표 파일서술자;
    private செயலகம்_நிலை நிலை_மதிப்பு_e10195a1 = செயலகம்_நிலை.தயார்படுத்த;
    private int முடிவு_குறியீடு;
    private int நிரல்_இடைவேளை = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    செயலகம்_மதிப்பு(int அடையாளங்காட்டி_மதிப்பு, int 부모식별자, பக்கம்_மேலாளர்.முகவரி_தளம் முகவரி_தளம், 파일서술자표 파일서술자) {
        this.அடையாளங்காட்டி_மதிப்பு = அடையாளங்காட்டி_மதிப்பு;
        this.부모식별자 = 부모식별자;
        this.முகவரி_தளம் = முகவரி_தளம்;
        this.파일서술자 = 파일서술자;
    }

    public int அடையாளங்காட்டி_மதிப்பு() {
        return அடையாளங்காட்டி_மதிப்பு;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public பக்கம்_மேலாளர்.முகவரி_தளம் முகவரி_தளம்() {
        return முகவரி_தளம்;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public செயலகம்_நிலை நிலை_மதிப்பு_e10195a1() {
        return நிலை_மதிப்பு_e10195a1;
    }

    public void அமை_நிலை(செயலகம்_நிலை 새상태) {
        நிலை_மதிப்பு_e10195a1 = 새상태;
    }

    public int முடிவு_குறியீடு() {
        return முடிவு_குறியீடு;
    }

    public void முடிவு_நிரல்(int மதிப்பு) {
        முடிவு_குறியீடு = மதிப்பு & 0xff;
        நிலை_மதிப்பு_e10195a1 = செயலகம்_நிலை.முடிவு_நிரல்;
    }

    public int நிரல்_இடைவேளை() {
        return நிரல்_இடைவேளை;
    }

    public void அமை_நிரல்_இடைவேளை(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("நிரல்_f5044b9b 끝 범위를 벗어났습니다.");
        }
        நிரல்_இடைவேளை = 새끝;
    }

    public void 실행문맥설정(int தொடங்கு_முகவரி, String[] அளவுரு_மதிப்புரு, String[] 환경) {
        실행시작주소 = தொடங்கு_முகவரி;
        실행인자 = அளவுரு_மதிப்புரு.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
