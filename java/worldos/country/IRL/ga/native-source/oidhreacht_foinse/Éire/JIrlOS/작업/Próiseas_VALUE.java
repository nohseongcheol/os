// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Éire.JIrlOS.작업;

import Éire.JIrlOS.기억공간.leathanach_bainisteoir;
import Éire.JIrlOS.córas_comhad.파일서술자표;

public final class Próiseas_VALUE {
    private final int aitheantóir_VALUE;
    private final int 부모식별자;
    private final leathanach_bainisteoir.ADDRESS_spás ADDRESS_spás;
    private final 파일서술자표 파일서술자;
    private Próiseas_staid staid_VALUE = Próiseas_staid.Ullmhaigh;
    private int scoir_CODE;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Próiseas_VALUE(int aitheantóir_VALUE, int 부모식별자, leathanach_bainisteoir.ADDRESS_spás ADDRESS_spás, 파일서술자표 파일서술자) {
        this.aitheantóir_VALUE = aitheantóir_VALUE;
        this.부모식별자 = 부모식별자;
        this.ADDRESS_spás = ADDRESS_spás;
        this.파일서술자 = 파일서술자;
    }

    public int aitheantóir_VALUE() {
        return aitheantóir_VALUE;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public leathanach_bainisteoir.ADDRESS_spás ADDRESS_spás() {
        return ADDRESS_spás;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Próiseas_staid staid_VALUE() {
        return staid_VALUE;
    }

    public void tacar_staid(Próiseas_staid 새상태) {
        staid_VALUE = 새상태;
    }

    public int scoir_CODE() {
        return scoir_CODE;
    }

    public void scoir_clár(int VALUE) {
        scoir_CODE = VALUE & 0xff;
        staid_VALUE = Próiseas_staid.scoir_clár;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("clár_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int seoladh_tosaithe, String[] paraiméadar_argóint, String[] 환경) {
        실행시작주소 = seoladh_tosaithe;
        실행인자 = paraiméadar_argóint.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
