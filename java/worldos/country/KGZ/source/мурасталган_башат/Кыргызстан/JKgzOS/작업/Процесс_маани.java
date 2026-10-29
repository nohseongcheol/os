// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Кыргызстан.JKgzOS.작업;

import Кыргызстан.JKgzOS.기억공간.бет_башкаруучу;
import Кыргызстан.JKgzOS.файл_тутуму.파일서술자표;

public final class Процесс_маани {
    private final int аныктагыч_маани;
    private final int 부모식별자;
    private final бет_башкаруучу.дарек_АРАЛЫК дарек_АРАЛЫК;
    private final 파일서술자표 파일서술자;
    private Процесс_абал абал_маани = Процесс_абал.Даярдоо;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Процесс_маани(int аныктагыч_маани, int 부모식별자, бет_башкаруучу.дарек_АРАЛЫК дарек_АРАЛЫК, 파일서술자표 파일서술자) {
        this.аныктагыч_маани = аныктагыч_маани;
        this.부모식별자 = 부모식별자;
        this.дарек_АРАЛЫК = дарек_АРАЛЫК;
        this.파일서술자 = 파일서술자;
    }

    public int аныктагыч_маани() {
        return аныктагыч_маани;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public бет_башкаруучу.дарек_АРАЛЫК дарек_АРАЛЫК() {
        return дарек_АРАЛЫК;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Процесс_абал абал_маани() {
        return абал_маани;
    }

    public void топ_абал(Процесс_абал 새상태) {
        абал_маани = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void Чыгуу_програм(int маани) {
        종료값 = маани & 0xff;
        абал_маани = Процесс_абал.Чыгуу_програм;
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

    public void 실행문맥설정(int Баштоо_дарек, String[] 인자, String[] 환경) {
        실행시작주소 = Баштоо_дарек;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
