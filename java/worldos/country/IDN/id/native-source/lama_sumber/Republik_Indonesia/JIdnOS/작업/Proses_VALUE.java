// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Republik_Indonesia.JIdnOS.작업;

import Republik_Indonesia.JIdnOS.Memori_wilayah.halaman_Manajer;
import Republik_Indonesia.JIdnOS.sistem_berkas.파일서술자표;

public final class Proses_VALUE {
    private final int pengidentifikasi_VALUE;
    private final int induk_pengidentifikasi;
    private final halaman_Manajer.surel_SPACE surel_SPACE;
    private final 파일서술자표 파일서술자;
    private Proses_Status Status_VALUE = Proses_Status.Siapkan;
    private int Keluar_CODE;
    private int apl_putus = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] lingkungan_VALUE = new String[0];

    Proses_VALUE(int pengidentifikasi_VALUE, int induk_pengidentifikasi, halaman_Manajer.surel_SPACE surel_SPACE, 파일서술자표 파일서술자) {
        this.pengidentifikasi_VALUE = pengidentifikasi_VALUE;
        this.induk_pengidentifikasi = induk_pengidentifikasi;
        this.surel_SPACE = surel_SPACE;
        this.파일서술자 = 파일서술자;
    }

    public int pengidentifikasi_VALUE() {
        return pengidentifikasi_VALUE;
    }

    public int induk_pengidentifikasi() {
        return induk_pengidentifikasi;
    }

    public halaman_Manajer.surel_SPACE surel_SPACE() {
        return surel_SPACE;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Proses_Status Status_VALUE() {
        return Status_VALUE;
    }

    public void set_Status(Proses_Status 새상태) {
        Status_VALUE = 새상태;
    }

    public int Keluar_CODE() {
        return Keluar_CODE;
    }

    public void Keluar_apl(int VALUE) {
        Keluar_CODE = VALUE & 0xff;
        Status_VALUE = Proses_Status.Keluar_apl;
    }

    public int apl_putus() {
        return apl_putus;
    }

    public void set_apl_putus(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("apl_f5044b9b 끝 범위를 벗어났습니다.");
        }
        apl_putus = 새끝;
    }

    public void 실행문맥설정(int alamat_permulaan, String[] parameter_argumen, String[] lingkungan) {
        실행시작주소 = alamat_permulaan;
        실행인자 = parameter_argumen.clone();
        lingkungan_VALUE = lingkungan.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] lingkungan_VALUE() { return lingkungan_VALUE.clone(); }
}
