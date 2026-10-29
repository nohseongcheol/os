// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nijar.JNerOS.작업;

import Nijar.JNerOS.기억공간.shafi_Manaja;
import Nijar.JNerOS.tsarin_fayil_a_kwamfuta.파일서술자표;

public final class haryar_aikin_na_ura_Daraja {
    private final int mai_ganewa_Daraja;
    private final int 부모식별자;
    private final shafi_Manaja.imel_wuri imel_wuri;
    private final 파일서술자표 파일서술자;
    private haryar_aikin_na_ura_Matsayi Matsayi_Daraja = haryar_aikin_na_ura_Matsayi.Shirya;
    private int Mafita_lambar_sirri;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    haryar_aikin_na_ura_Daraja(int mai_ganewa_Daraja, int 부모식별자, shafi_Manaja.imel_wuri imel_wuri, 파일서술자표 파일서술자) {
        this.mai_ganewa_Daraja = mai_ganewa_Daraja;
        this.부모식별자 = 부모식별자;
        this.imel_wuri = imel_wuri;
        this.파일서술자 = 파일서술자;
    }

    public int mai_ganewa_Daraja() {
        return mai_ganewa_Daraja;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public shafi_Manaja.imel_wuri imel_wuri() {
        return imel_wuri;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public haryar_aikin_na_ura_Matsayi Matsayi_Daraja() {
        return Matsayi_Daraja;
    }

    public void zubi_Matsayi(haryar_aikin_na_ura_Matsayi 새상태) {
        Matsayi_Daraja = 새상태;
    }

    public int Mafita_lambar_sirri() {
        return Mafita_lambar_sirri;
    }

    public void Mafita_Shiri(int Daraja) {
        Mafita_lambar_sirri = Daraja & 0xff;
        Matsayi_Daraja = haryar_aikin_na_ura_Matsayi.Mafita_Shiri;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("Shiri_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int Fara_imel, String[] maaunin_Tubalin_aiki, String[] 환경) {
        실행시작주소 = Fara_imel;
        실행인자 = maaunin_Tubalin_aiki.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
