// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turqi.JTurOS.작업;

import Turqi.JTurOS.기억공간.faqe_menaxher;
import Turqi.JTurOS.sistemi_i_skedarëve.파일서술자표;

public final class Proces_VALUE {
    private final int identifikues_VALUE;
    private final int 부모식별자;
    private final faqe_menaxher.email_HAPËSIRË email_HAPËSIRË;
    private final 파일서술자표 파일서술자;
    private Proces_status status_VALUE = Proces_status.Përgatit;
    private int dal_kod;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Proces_VALUE(int identifikues_VALUE, int 부모식별자, faqe_menaxher.email_HAPËSIRË email_HAPËSIRË, 파일서술자표 파일서술자) {
        this.identifikues_VALUE = identifikues_VALUE;
        this.부모식별자 = 부모식별자;
        this.email_HAPËSIRË = email_HAPËSIRË;
        this.파일서술자 = 파일서술자;
    }

    public int identifikues_VALUE() {
        return identifikues_VALUE;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public faqe_menaxher.email_HAPËSIRË email_HAPËSIRË() {
        return email_HAPËSIRË;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Proces_status status_VALUE() {
        return status_VALUE;
    }

    public void bashkësi_status(Proces_status 새상태) {
        status_VALUE = 새상태;
    }

    public int dal_kod() {
        return dal_kod;
    }

    public void dal_program(int VALUE) {
        dal_kod = VALUE & 0xff;
        status_VALUE = Proces_status.dal_program;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("program_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int nis_email, String[] parametër_argument, String[] 환경) {
        실행시작주소 = nis_email;
        실행인자 = parametër_argument.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
