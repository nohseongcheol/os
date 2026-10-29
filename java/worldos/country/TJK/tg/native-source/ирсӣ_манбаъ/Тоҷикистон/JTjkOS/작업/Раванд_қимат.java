// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Тоҷикистон.JTjkOS.작업;

import Тоҷикистон.JTjkOS.기억공간.саҳифа_мудир;
import Тоҷикистон.JTjkOS.системаи_файлӣ.파일서술자표;

public final class Раванд_қимат {
    private final int идентификатор_қимат;
    private final int 부모식별자;
    private final саҳифа_мудир.суроға_фазо суроға_фазо;
    private final 파일서술자표 파일서술자;
    private Раванд_вазъият вазъият_қимат = Раванд_вазъият.Омода_кардан;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Раванд_қимат(int идентификатор_қимат, int 부모식별자, саҳифа_мудир.суроға_фазо суроға_фазо, 파일서술자표 파일서술자) {
        this.идентификатор_қимат = идентификатор_қимат;
        this.부모식별자 = 부모식별자;
        this.суроға_фазо = суроға_фазо;
        this.파일서술자 = 파일서술자;
    }

    public int идентификатор_қимат() {
        return идентификатор_қимат;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public саҳифа_мудир.суроға_фазо суроға_фазо() {
        return суроға_фазо;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Раванд_вазъият вазъият_қимат() {
        return вазъият_қимат;
    }

    public void маҷмуъ_вазъият(Раванд_вазъият 새상태) {
        вазъият_қимат = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void Баромад_барнома(int қимат) {
        종료값 = қимат & 0xff;
        вазъият_қимат = Раванд_вазъият.Баромад_барнома;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("барнома_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int Оғоз_суроға, String[] 인자, String[] 환경) {
        실행시작주소 = Оғоз_суроға;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
