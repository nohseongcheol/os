// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ermənistan.JArmOS.작업;

import Ermənistan.JArmOS.기억공간.səhifə_menecer;
import Ermənistan.JArmOS.fayl_sistemi.파일서술자표;

public final class Proses_VALUE {
    private final int identifikator_VALUE;
    private final int 부모식별자;
    private final səhifə_menecer.ünvan_məkan ünvan_məkan;
    private final 파일서술자표 파일서술자;
    private Proses_vəziyyət vəziyyət_VALUE = Proses_vəziyyət.Hazırla;
    private int Çıxış_kod;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Proses_VALUE(int identifikator_VALUE, int 부모식별자, səhifə_menecer.ünvan_məkan ünvan_məkan, 파일서술자표 파일서술자) {
        this.identifikator_VALUE = identifikator_VALUE;
        this.부모식별자 = 부모식별자;
        this.ünvan_məkan = ünvan_məkan;
        this.파일서술자 = 파일서술자;
    }

    public int identifikator_VALUE() {
        return identifikator_VALUE;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public səhifə_menecer.ünvan_məkan ünvan_məkan() {
        return ünvan_məkan;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Proses_vəziyyət vəziyyət_VALUE() {
        return vəziyyət_VALUE;
    }

    public void Dəst_vəziyyət(Proses_vəziyyət 새상태) {
        vəziyyət_VALUE = 새상태;
    }

    public int Çıxış_kod() {
        return Çıxış_kod;
    }

    public void Çıxış_proqram(int VALUE) {
        Çıxış_kod = VALUE & 0xff;
        vəziyyət_VALUE = Proses_vəziyyət.Çıxış_proqram;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("proqram_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int başlama_ünvanı, String[] 인자, String[] 환경) {
        실행시작주소 = başlama_ünvanı;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
