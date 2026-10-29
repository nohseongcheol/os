// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Украіна.JUkrOS.작업;

import Украіна.JUkrOS.기억공간.старонка_менеджар;
import Украіна.JUkrOS.файлавая_сістэма.파일서술자표;

public final class Працэс_значэнне {
    private final int ідэнтыфікатар_значэнне;
    private final int 부모식별자;
    private final старонка_менеджар.адрас_ПРАБЕЛ адрас_ПРАБЕЛ;
    private final 파일서술자표 파일서술자;
    private Працэс_стан стан_значэнне = Працэс_стан.Падрыхтаваць;
    private int Выхад_код;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Працэс_значэнне(int ідэнтыфікатар_значэнне, int 부모식별자, старонка_менеджар.адрас_ПРАБЕЛ адрас_ПРАБЕЛ, 파일서술자표 파일서술자) {
        this.ідэнтыфікатар_значэнне = ідэнтыфікатар_значэнне;
        this.부모식별자 = 부모식별자;
        this.адрас_ПРАБЕЛ = адрас_ПРАБЕЛ;
        this.파일서술자 = 파일서술자;
    }

    public int ідэнтыфікатар_значэнне() {
        return ідэнтыфікатар_значэнне;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public старонка_менеджар.адрас_ПРАБЕЛ адрас_ПРАБЕЛ() {
        return адрас_ПРАБЕЛ;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Працэс_стан стан_значэнне() {
        return стан_значэнне;
    }

    public void набор_стан(Працэс_стан 새상태) {
        стан_значэнне = 새상태;
    }

    public int Выхад_код() {
        return Выхад_код;
    }

    public void Выхад_праграма(int значэнне) {
        Выхад_код = значэнне & 0xff;
        стан_значэнне = Працэс_стан.Выхад_праграма;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("праграма_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int Пуск_адрас, String[] параметр_аргумент, String[] 환경) {
        실행시작주소 = Пуск_адрас;
        실행인자 = параметр_аргумент.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
