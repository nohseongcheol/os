// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkmenistan.JTkmOS.작업;

import Türkmenistan.JTkmOS.기억공간.sahypa_iş_dolandyryjy;
import Türkmenistan.JTkmOS.faýl_ulgamy.파일서술자표;

public final class Proses_baha {
    private final int tanaýjy_baha;
    private final int 부모식별자;
    private final sahypa_iş_dolandyryjy.salgy_ýer salgy_ýer;
    private final 파일서술자표 파일서술자;
    private Proses_ýagdaý ýagdaý_baha = Proses_ýagdaý.Taýýarla;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Proses_baha(int tanaýjy_baha, int 부모식별자, sahypa_iş_dolandyryjy.salgy_ýer salgy_ýer, 파일서술자표 파일서술자) {
        this.tanaýjy_baha = tanaýjy_baha;
        this.부모식별자 = 부모식별자;
        this.salgy_ýer = salgy_ýer;
        this.파일서술자 = 파일서술자;
    }

    public int tanaýjy_baha() {
        return tanaýjy_baha;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public sahypa_iş_dolandyryjy.salgy_ýer salgy_ýer() {
        return salgy_ýer;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Proses_ýagdaý ýagdaý_baha() {
        return ýagdaý_baha;
    }

    public void köplük_ýagdaý(Proses_ýagdaý 새상태) {
        ýagdaý_baha = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void çyk_programma(int baha) {
        종료값 = baha & 0xff;
        ýagdaý_baha = Proses_ýagdaý.çyk_programma;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("programma_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int başlat_salgy, String[] 인자, String[] 환경) {
        실행시작주소 = başlat_salgy;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
