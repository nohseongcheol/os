// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Afrika_Borwa.JZafOS.작업;

import Afrika_Borwa.JZafOS.기억공간.letlakala_molaodi;
import Afrika_Borwa.JZafOS.tshepedišo_ya_difaele.파일서술자표;

public final class tiragalo_boleng {
    private final int sešupi_boleng;
    private final int 부모식별자;
    private final letlakala_molaodi.atrese_sekgoba atrese_sekgoba;
    private final 파일서술자표 파일서술자;
    private tiragalo_boemo boemo_boleng = tiragalo_boemo.Lokišetša;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    tiragalo_boleng(int sešupi_boleng, int 부모식별자, letlakala_molaodi.atrese_sekgoba atrese_sekgoba, 파일서술자표 파일서술자) {
        this.sešupi_boleng = sešupi_boleng;
        this.부모식별자 = 부모식별자;
        this.atrese_sekgoba = atrese_sekgoba;
        this.파일서술자 = 파일서술자;
    }

    public int sešupi_boleng() {
        return sešupi_boleng;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public letlakala_molaodi.atrese_sekgoba atrese_sekgoba() {
        return atrese_sekgoba;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public tiragalo_boemo boemo_boleng() {
        return boemo_boleng;
    }

    public void sehlopha_boemo(tiragalo_boemo 새상태) {
        boemo_boleng = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void Etšwa_tirišo(int boleng) {
        종료값 = boleng & 0xff;
        boemo_boleng = tiragalo_boemo.Etšwa_tirišo;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("tirišo_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int Thomišo_atrese, String[] 인자, String[] 환경) {
        실행시작주소 = Thomišo_atrese;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
