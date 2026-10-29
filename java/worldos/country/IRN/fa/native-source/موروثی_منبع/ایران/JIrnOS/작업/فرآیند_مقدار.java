// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ایران.JIrnOS.작업;

import ایران.JIrnOS.기억공간.صفحه_مدیر;
import ایران.JIrnOS.سیستم_پرونده.파일서술자표;

public final class فرآیند_مقدار {
    private final int شناسه_مقدار;
    private final int 부모식별자;
    private final صفحه_مدیر.آدرس_فضا آدرس_فضا;
    private final 파일서술자표 파일서술자;
    private فرآیند_وضعیت وضعیت_مقدار = فرآیند_وضعیت.آماده_کردن;
    private int خروج_کد;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    فرآیند_مقدار(int شناسه_مقدار, int 부모식별자, صفحه_مدیر.آدرس_فضا آدرس_فضا, 파일서술자표 파일서술자) {
        this.شناسه_مقدار = شناسه_مقدار;
        this.부모식별자 = 부모식별자;
        this.آدرس_فضا = آدرس_فضا;
        this.파일서술자 = 파일서술자;
    }

    public int شناسه_مقدار() {
        return شناسه_مقدار;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public صفحه_مدیر.آدرس_فضا آدرس_فضا() {
        return آدرس_فضا;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public فرآیند_وضعیت وضعیت_مقدار() {
        return وضعیت_مقدار;
    }

    public void مجموعه_وضعیت(فرآیند_وضعیت 새상태) {
        وضعیت_مقدار = 새상태;
    }

    public int خروج_کد() {
        return خروج_کد;
    }

    public void خروج_برنامه(int مقدار) {
        خروج_کد = مقدار & 0xff;
        وضعیت_مقدار = فرآیند_وضعیت.خروج_برنامه;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("برنامه_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int شروع_آدرس, String[] پارامتر_آرگومان, String[] 환경) {
        실행시작주소 = شروع_آدرس;
        실행인자 = پارامتر_آرگومان.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
