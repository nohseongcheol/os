// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ísland.JIslOS.작업;

import Ísland.JIslOS.기억공간.síða_stjórnandi;
import Ísland.JIslOS.skrárkerfi.파일서술자표;

public final class Ferli_VALUE {
    private final int auðkenni_VALUE;
    private final int yfireining_auðkenni;
    private final síða_stjórnandi.slóð_svæði slóð_svæði;
    private final 파일서술자표 파일서술자;
    private Ferli_staða staða_VALUE_e10195a1 = Ferli_staða.Undirbúa;
    private int loka_CODE;
    private int forrit_hlé = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Ferli_VALUE(int auðkenni_VALUE, int yfireining_auðkenni, síða_stjórnandi.slóð_svæði slóð_svæði, 파일서술자표 파일서술자) {
        this.auðkenni_VALUE = auðkenni_VALUE;
        this.yfireining_auðkenni = yfireining_auðkenni;
        this.slóð_svæði = slóð_svæði;
        this.파일서술자 = 파일서술자;
    }

    public int auðkenni_VALUE() {
        return auðkenni_VALUE;
    }

    public int yfireining_auðkenni() {
        return yfireining_auðkenni;
    }

    public síða_stjórnandi.slóð_svæði slóð_svæði() {
        return slóð_svæði;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Ferli_staða staða_VALUE_e10195a1() {
        return staða_VALUE_e10195a1;
    }

    public void sett_staða(Ferli_staða 새상태) {
        staða_VALUE_e10195a1 = 새상태;
    }

    public int loka_CODE() {
        return loka_CODE;
    }

    public void loka_forrit(int VALUE) {
        loka_CODE = VALUE & 0xff;
        staða_VALUE_e10195a1 = Ferli_staða.loka_forrit;
    }

    public int forrit_hlé() {
        return forrit_hlé;
    }

    public void sett_forrit_hlé(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("forrit_f5044b9b 끝 범위를 벗어났습니다.");
        }
        forrit_hlé = 새끝;
    }

    public void 실행문맥설정(int Opna_slóð, String[] færibreyta_frumbreyta, String[] 환경) {
        실행시작주소 = Opna_slóð;
        실행인자 = færibreyta_frumbreyta.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
