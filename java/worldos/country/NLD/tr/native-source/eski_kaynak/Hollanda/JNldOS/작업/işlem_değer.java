// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hollanda.JNldOS.작업;

import Hollanda.JNldOS.Bellek_bölge.sayfa_yönetici;
import Hollanda.JNldOS.dosya_sistemi.Dosya_tanımlayıcı_tablo;

public final class işlem_değer {
    private final int tanımlayıcı_değer;
    private final int ana_tanımlayıcı;
    private final sayfa_yönetici.adres_alanı adres_alanı;
    private final Dosya_tanımlayıcı_tablo Dosya_tanımlayıcı;
    private işlem_Durum Durum_değer = işlem_Durum.Hazırlan;
    private int çıkış_kodu;
    private int program_mola = 0x06000000;
    private int yürütme_Start_ADRES;
    private String[] yürütme_bağımsız_değişken = new String[0];
    private String[] ortam_değer = new String[0];

    işlem_değer(int tanımlayıcı_değer, int ana_tanımlayıcı, sayfa_yönetici.adres_alanı adres_alanı, Dosya_tanımlayıcı_tablo Dosya_tanımlayıcı) {
        this.tanımlayıcı_değer = tanımlayıcı_değer;
        this.ana_tanımlayıcı = ana_tanımlayıcı;
        this.adres_alanı = adres_alanı;
        this.Dosya_tanımlayıcı = Dosya_tanımlayıcı;
    }

    public int tanımlayıcı_değer() {
        return tanımlayıcı_değer;
    }

    public int ana_tanımlayıcı() {
        return ana_tanımlayıcı;
    }

    public sayfa_yönetici.adres_alanı adres_alanı() {
        return adres_alanı;
    }

    public Dosya_tanımlayıcı_tablo Dosya_tanımlayıcı() {
        return Dosya_tanımlayıcı;
    }

    public işlem_Durum Durum_değer() {
        return Durum_değer;
    }

    public void küme_Durum(işlem_Durum 새상태) {
        Durum_değer = 새상태;
    }

    public int çıkış_kodu() {
        return çıkış_kodu;
    }

    public void Çıkış_program(int değer) {
        çıkış_kodu = değer & 0xff;
        Durum_değer = işlem_Durum.Çıkış_program;
    }

    public int program_mola() {
        return program_mola;
    }

    public void küme_program_mola(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("program_f5044b9b 끝 범위를 벗어났습니다.");
        }
        program_mola = 새끝;
    }

    public void küme_bağlam(int Start_ADRES, String[] parametre_bağımsız_değişken, String[] ortam) {
        yürütme_Start_ADRES = Start_ADRES;
        yürütme_bağımsız_değişken = parametre_bağımsız_değişken.clone();
        ortam_değer = ortam.clone();
    }

    public int yürütme_Start_ADRES() { return yürütme_Start_ADRES; }
    public String[] yürütme_bağımsız_değişken() { return yürütme_bağımsız_değişken.clone(); }
    public String[] ortam_değer() { return ortam_değer.clone(); }
}
