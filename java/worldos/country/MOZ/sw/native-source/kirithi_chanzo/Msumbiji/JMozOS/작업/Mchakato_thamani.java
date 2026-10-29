// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Msumbiji.JMozOS.작업;

import Msumbiji.JMozOS.기억공간.ukurasa_msimamizi;
import Msumbiji.JMozOS.mfumo_ya_mafaili.파일서술자표;

public final class Mchakato_thamani {
    private final int kitambulishi_thamani;
    private final int 부모식별자;
    private final ukurasa_msimamizi.anwani_eneo anwani_eneo;
    private final 파일서술자표 파일서술자;
    private Mchakato_hali hali_thamani = Mchakato_hali.Andaa;
    private int toka_msimbo;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Mchakato_thamani(int kitambulishi_thamani, int 부모식별자, ukurasa_msimamizi.anwani_eneo anwani_eneo, 파일서술자표 파일서술자) {
        this.kitambulishi_thamani = kitambulishi_thamani;
        this.부모식별자 = 부모식별자;
        this.anwani_eneo = anwani_eneo;
        this.파일서술자 = 파일서술자;
    }

    public int kitambulishi_thamani() {
        return kitambulishi_thamani;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public ukurasa_msimamizi.anwani_eneo anwani_eneo() {
        return anwani_eneo;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Mchakato_hali hali_thamani() {
        return hali_thamani;
    }

    public void seti_hali(Mchakato_hali 새상태) {
        hali_thamani = 새상태;
    }

    public int toka_msimbo() {
        return toka_msimbo;
    }

    public void toka_programu(int thamani) {
        toka_msimbo = thamani & 0xff;
        hali_thamani = Mchakato_hali.toka_programu;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("programu_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int Anza_anwani, String[] parameta_hoja, String[] 환경) {
        실행시작주소 = Anza_anwani;
        실행인자 = parameta_hoja.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
