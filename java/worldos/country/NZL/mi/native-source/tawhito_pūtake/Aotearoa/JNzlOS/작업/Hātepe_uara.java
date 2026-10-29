// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aotearoa.JNzlOS.작업;

import Aotearoa.JNzlOS.기억공간.whārangi_pouwhakahaere;
import Aotearoa.JNzlOS.pūnaha_kōnae.파일서술자표;

public final class Hātepe_uara {
    private final int pūtāutu_uara;
    private final int 부모식별자;
    private final whārangi_pouwhakahaere.ADDRESS_wāhi ADDRESS_wāhi;
    private final 파일서술자표 파일서술자;
    private Hātepe_tūnga tūnga_uara = Hātepe_tūnga.Whakarite;
    private int Putaatu_CODE;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Hātepe_uara(int pūtāutu_uara, int 부모식별자, whārangi_pouwhakahaere.ADDRESS_wāhi ADDRESS_wāhi, 파일서술자표 파일서술자) {
        this.pūtāutu_uara = pūtāutu_uara;
        this.부모식별자 = 부모식별자;
        this.ADDRESS_wāhi = ADDRESS_wāhi;
        this.파일서술자 = 파일서술자;
    }

    public int pūtāutu_uara() {
        return pūtāutu_uara;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public whārangi_pouwhakahaere.ADDRESS_wāhi ADDRESS_wāhi() {
        return ADDRESS_wāhi;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Hātepe_tūnga tūnga_uara() {
        return tūnga_uara;
    }

    public void huinga_tūnga(Hātepe_tūnga 새상태) {
        tūnga_uara = 새상태;
    }

    public int Putaatu_CODE() {
        return Putaatu_CODE;
    }

    public void Putaatu_kaupapa(int uara) {
        Putaatu_CODE = uara & 0xff;
        tūnga_uara = Hātepe_tūnga.Putaatu_kaupapa;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("kaupapa_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int Start_ADDRESS, String[] 인자, String[] 환경) {
        실행시작주소 = Start_ADDRESS;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
