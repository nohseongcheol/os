// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nàìjíríà.JNgaOS.작업;

import Nàìjíríà.JNgaOS.기억공간.ojú_ìwé_alákòóso;
import Nàìjíríà.JNgaOS.ìlànà_ètò_fáìlì.파일서술자표;

public final class Ìlànà_iye {
    private final int Àfidámọ̀_iye;
    private final int 부모식별자;
    private final ojú_ìwé_alákòóso.àdírẹ́ẹ̀sì_àlàfo àdírẹ́ẹ̀sì_àlàfo;
    private final 파일서술자표 파일서술자;
    private Ìlànà_ipò ipò_iye = Ìlànà_ipò.gbaradì;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Ìlànà_iye(int Àfidámọ̀_iye, int 부모식별자, ojú_ìwé_alákòóso.àdírẹ́ẹ̀sì_àlàfo àdírẹ́ẹ̀sì_àlàfo, 파일서술자표 파일서술자) {
        this.Àfidámọ̀_iye = Àfidámọ̀_iye;
        this.부모식별자 = 부모식별자;
        this.àdírẹ́ẹ̀sì_àlàfo = àdírẹ́ẹ̀sì_àlàfo;
        this.파일서술자 = 파일서술자;
    }

    public int Àfidámọ̀_iye() {
        return Àfidámọ̀_iye;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public ojú_ìwé_alákòóso.àdírẹ́ẹ̀sì_àlàfo àdírẹ́ẹ̀sì_àlàfo() {
        return àdírẹ́ẹ̀sì_àlàfo;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Ìlànà_ipò ipò_iye() {
        return ipò_iye;
    }

    public void ọ̀wọ̀_ipò(Ìlànà_ipò 새상태) {
        ipò_iye = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void jáde_àtòjọ_ètò(int iye) {
        종료값 = iye & 0xff;
        ipò_iye = Ìlànà_ipò.jáde_àtòjọ_ètò;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("àtòjọ_ètò_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int bẹ̀rẹ̀_àdírẹ́ẹ̀sì, String[] 인자, String[] 환경) {
        실행시작주소 = bẹ̀rẹ̀_àdírẹ́ẹ̀sì;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
