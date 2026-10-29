// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Россия.JRusOS.작업;

import Россия.JRusOS.기억공간.бит_идарәче;
import Россия.JRusOS.файл_системасы.파일서술자표;

public final class Процесс_VALUE {
    private final int күрсәткеч_VALUE;
    private final int 부모식별자;
    private final бит_идарәче.адрес_өлкә адрес_өлкә;
    private final 파일서술자표 파일서술자;
    private Процесс_халәт халәт_VALUE = Процесс_халәт.Әзерләү;
    private int Чыгу_CODE;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Процесс_VALUE(int күрсәткеч_VALUE, int 부모식별자, бит_идарәче.адрес_өлкә адрес_өлкә, 파일서술자표 파일서술자) {
        this.күрсәткеч_VALUE = күрсәткеч_VALUE;
        this.부모식별자 = 부모식별자;
        this.адрес_өлкә = адрес_өлкә;
        this.파일서술자 = 파일서술자;
    }

    public int күрсәткеч_VALUE() {
        return күрсәткеч_VALUE;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public бит_идарәче.адрес_өлкә адрес_өлкә() {
        return адрес_өлкә;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Процесс_халәт халәт_VALUE() {
        return халәт_VALUE;
    }

    public void җыелма_халәт(Процесс_халәт 새상태) {
        халәт_VALUE = 새상태;
    }

    public int Чыгу_CODE() {
        return Чыгу_CODE;
    }

    public void Чыгу_кушымта(int VALUE) {
        Чыгу_CODE = VALUE & 0xff;
        халәт_VALUE = Процесс_халәт.Чыгу_кушымта;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("кушымта_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int Start_адрес, String[] 인자, String[] 환경) {
        실행시작주소 = Start_адрес;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
