// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Албанија.JAlbOS.작업;

import Албанија.JAlbOS.기억공간.страница_управник;
import Албанија.JAlbOS.систем_на_датотеки.파일서술자표;

public final class Процес_VALUE {
    private final int идентификатор_VALUE;
    private final int 부모식별자;
    private final страница_управник.адреса_простор адреса_простор;
    private final 파일서술자표 파일서술자;
    private Процес_статус статус_VALUE = Процес_статус.Подготви;
    private int Излез_CODE;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Процес_VALUE(int идентификатор_VALUE, int 부모식별자, страница_управник.адреса_простор адреса_простор, 파일서술자표 파일서술자) {
        this.идентификатор_VALUE = идентификатор_VALUE;
        this.부모식별자 = 부모식별자;
        this.адреса_простор = адреса_простор;
        this.파일서술자 = 파일서술자;
    }

    public int идентификатор_VALUE() {
        return идентификатор_VALUE;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public страница_управник.адреса_простор адреса_простор() {
        return адреса_простор;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Процес_статус статус_VALUE() {
        return статус_VALUE;
    }

    public void збир_статус(Процес_статус 새상태) {
        статус_VALUE = 새상태;
    }

    public int Излез_CODE() {
        return Излез_CODE;
    }

    public void Излез_програма(int VALUE) {
        Излез_CODE = VALUE & 0xff;
        статус_VALUE = Процес_статус.Излез_програма;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("програма_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int почетна_адреса, String[] параметар_аргумент, String[] 환경) {
        실행시작주소 = почетна_адреса;
        실행인자 = параметар_аргумент.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
