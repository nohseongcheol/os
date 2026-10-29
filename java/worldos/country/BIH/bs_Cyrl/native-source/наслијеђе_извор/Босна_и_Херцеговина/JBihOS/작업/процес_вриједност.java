// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Босна_и_Херцеговина.JBihOS.작업;

import Босна_и_Херцеговина.JBihOS.기억공간.страница_менаџер;
import Босна_и_Херцеговина.JBihOS.фајл_систем.파일서술자표;

public final class процес_вриједност {
    private final int 식별자;
    private final int 부모식별자;
    private final страница_менаџер.адреса_простор адреса_простор;
    private final 파일서술자표 파일서술자;
    private процес_стање стање_вриједност = процес_стање.Припремити;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    процес_вриједност(int 식별자, int 부모식별자, страница_менаџер.адреса_простор адреса_простор, 파일서술자표 파일서술자) {
        this.식별자 = 식별자;
        this.부모식별자 = 부모식별자;
        this.адреса_простор = адреса_простор;
        this.파일서술자 = 파일서술자;
    }

    public int 식별자() {
        return 식별자;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public страница_менаџер.адреса_простор адреса_простор() {
        return адреса_простор;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public процес_стање стање_вриједност() {
        return стање_вриједност;
    }

    public void именовани_скуп_стање(процес_стање 새상태) {
        стање_вриједност = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void изаћи_програм(int вриједност) {
        종료값 = вриједност & 0xff;
        стање_вриједност = процес_стање.изаћи_програм;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("програм_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int почети_адреса, String[] 인자, String[] 환경) {
        실행시작주소 = почети_адреса;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
