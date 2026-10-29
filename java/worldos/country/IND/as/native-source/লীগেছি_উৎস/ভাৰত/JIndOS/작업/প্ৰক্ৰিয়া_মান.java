// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ভাৰত.JIndOS.작업;

import ভাৰত.JIndOS.기억공간.পৃষ্ঠা_মেনেজাৰ;
import ভাৰত.JIndOS.ফাইল_ছিষ্টেম.파일서술자표;

public final class প্ৰক্ৰিয়া_মান {
    private final int চিনাক্তকাৰী_মান;
    private final int 부모식별자;
    private final পৃষ্ঠা_মেনেজাৰ.ঠিকনা_স্থান ঠিকনা_স্থান;
    private final 파일서술자표 파일서술자;
    private প্ৰক্ৰিয়া_অৱস্থা অৱস্থা_মান = প্ৰক্ৰিয়া_অৱস্থা.প্ৰস্তুত_কৰক;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    প্ৰক্ৰিয়া_মান(int চিনাক্তকাৰী_মান, int 부모식별자, পৃষ্ঠা_মেনেজাৰ.ঠিকনা_স্থান ঠিকনা_স্থান, 파일서술자표 파일서술자) {
        this.চিনাক্তকাৰী_মান = চিনাক্তকাৰী_মান;
        this.부모식별자 = 부모식별자;
        this.ঠিকনা_স্থান = ঠিকনা_স্থান;
        this.파일서술자 = 파일서술자;
    }

    public int চিনাক্তকাৰী_মান() {
        return চিনাক্তকাৰী_মান;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public পৃষ্ঠা_মেনেজাৰ.ঠিকনা_স্থান ঠিকনা_স্থান() {
        return ঠিকনা_স্থান;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public প্ৰক্ৰিয়া_অৱস্থা অৱস্থা_মান() {
        return অৱস্থা_মান;
    }

    public void ছেট_অৱস্থা(প্ৰক্ৰিয়া_অৱস্থা 새상태) {
        অৱস্থা_মান = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void প্ৰস্থান_এপ্প্(int মান) {
        종료값 = মান & 0xff;
        অৱস্থা_মান = প্ৰক্ৰিয়া_অৱস্থা.প্ৰস্থান_এপ্প্;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("এপ্প্_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int আৰম্ভ_ঠিকনা, String[] 인자, String[] 환경) {
        실행시작주소 = আৰম্ভ_ঠিকনা;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
