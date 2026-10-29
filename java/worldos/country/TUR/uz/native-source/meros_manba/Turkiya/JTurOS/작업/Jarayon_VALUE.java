// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turkiya.JTurOS.작업;

import Turkiya.JTurOS.기억공간.sahifa_menejer;
import Turkiya.JTurOS.fayllar_tizimi.파일서술자표;

public final class Jarayon_VALUE {
    private final int identifikator_VALUE;
    private final int 부모식별자;
    private final sahifa_menejer.manzil_joy manzil_joy;
    private final 파일서술자표 파일서술자;
    private Jarayon_holat holat_VALUE_e10195a1 = Jarayon_holat.Tayyorlamoq;
    private int Chiqish_kod;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Jarayon_VALUE(int identifikator_VALUE, int 부모식별자, sahifa_menejer.manzil_joy manzil_joy, 파일서술자표 파일서술자) {
        this.identifikator_VALUE = identifikator_VALUE;
        this.부모식별자 = 부모식별자;
        this.manzil_joy = manzil_joy;
        this.파일서술자 = 파일서술자;
    }

    public int identifikator_VALUE() {
        return identifikator_VALUE;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public sahifa_menejer.manzil_joy manzil_joy() {
        return manzil_joy;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Jarayon_holat holat_VALUE_e10195a1() {
        return holat_VALUE_e10195a1;
    }

    public void to_plam_holat(Jarayon_holat 새상태) {
        holat_VALUE_e10195a1 = 새상태;
    }

    public int Chiqish_kod() {
        return Chiqish_kod;
    }

    public void Chiqish_ilova(int VALUE) {
        Chiqish_kod = VALUE & 0xff;
        holat_VALUE_e10195a1 = Jarayon_holat.Chiqish_ilova;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("ilova_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int Start_manzil, String[] 인자, String[] 환경) {
        실행시작주소 = Start_manzil;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
