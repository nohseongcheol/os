// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malta.JMltOS.작업;

import Malta.JMltOS.기억공간.paġna_maniġer;
import Malta.JMltOS.sistema_tal_fajls.파일서술자표;

public final class Proċess_VALUE {
    private final int identifikatur_VALUE;
    private final int 부모식별자;
    private final paġna_maniġer.ADDRESS_SPACE ADDRESS_SPACE;
    private final 파일서술자표 파일서술자;
    private Proċess_stat stat_VALUE = Proċess_stat.Ħejji;
    private int Ħruġ_CODE;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Proċess_VALUE(int identifikatur_VALUE, int 부모식별자, paġna_maniġer.ADDRESS_SPACE ADDRESS_SPACE, 파일서술자표 파일서술자) {
        this.identifikatur_VALUE = identifikatur_VALUE;
        this.부모식별자 = 부모식별자;
        this.ADDRESS_SPACE = ADDRESS_SPACE;
        this.파일서술자 = 파일서술자;
    }

    public int identifikatur_VALUE() {
        return identifikatur_VALUE;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public paġna_maniġer.ADDRESS_SPACE ADDRESS_SPACE() {
        return ADDRESS_SPACE;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Proċess_stat stat_VALUE() {
        return stat_VALUE;
    }

    public void sett_stat(Proċess_stat 새상태) {
        stat_VALUE = 새상태;
    }

    public int Ħruġ_CODE() {
        return Ħruġ_CODE;
    }

    public void Ħruġ_programm(int VALUE) {
        Ħruġ_CODE = VALUE & 0xff;
        stat_VALUE = Proċess_stat.Ħruġ_programm;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("programm_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int Bidu_ADDRESS, String[] 인자, String[] 환경) {
        실행시작주소 = Bidu_ADDRESS;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
