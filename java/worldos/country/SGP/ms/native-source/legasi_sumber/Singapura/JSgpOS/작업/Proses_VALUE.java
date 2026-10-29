// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Singapura.JSgpOS.작업;

import Singapura.JSgpOS.Memori_rantau.halaman_pengurus;
import Singapura.JSgpOS.sistem_fail.파일서술자표;

public final class Proses_VALUE {
    private final int 식별자;
    private final int 부모식별자;
    private final halaman_pengurus.e_mel_SPACE e_mel_SPACE;
    private final 파일서술자표 파일서술자;
    private Proses_status status_VALUE = Proses_status.Sediakan;
    private int Keluar_kod;
    private int aplikasi_putus = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] persekitaran_VALUE = new String[0];

    Proses_VALUE(int 식별자, int 부모식별자, halaman_pengurus.e_mel_SPACE e_mel_SPACE, 파일서술자표 파일서술자) {
        this.식별자 = 식별자;
        this.부모식별자 = 부모식별자;
        this.e_mel_SPACE = e_mel_SPACE;
        this.파일서술자 = 파일서술자;
    }

    public int 식별자() {
        return 식별자;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public halaman_pengurus.e_mel_SPACE e_mel_SPACE() {
        return e_mel_SPACE;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Proses_status status_VALUE() {
        return status_VALUE;
    }

    public void set_status(Proses_status 새상태) {
        status_VALUE = 새상태;
    }

    public int Keluar_kod() {
        return Keluar_kod;
    }

    public void Keluar_aplikasi(int VALUE) {
        Keluar_kod = VALUE & 0xff;
        status_VALUE = Proses_status.Keluar_aplikasi;
    }

    public int aplikasi_putus() {
        return aplikasi_putus;
    }

    public void set_aplikasi_putus(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("aplikasi_f5044b9b 끝 범위를 벗어났습니다.");
        }
        aplikasi_putus = 새끝;
    }

    public void 실행문맥설정(int alamat_mula, String[] parameter_argumen, String[] persekitaran) {
        실행시작주소 = alamat_mula;
        실행인자 = parameter_argumen.clone();
        persekitaran_VALUE = persekitaran.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] persekitaran_VALUE() { return persekitaran_VALUE.clone(); }
}
