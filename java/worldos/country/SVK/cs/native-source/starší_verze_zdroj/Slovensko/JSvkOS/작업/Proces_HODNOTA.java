// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovensko.JSvkOS.작업;

import Slovensko.JSvkOS.Paměť_oblast.stránka_Správce;
import Slovensko.JSvkOS.systém_souborů.Soubor_popisovač_tabulka;

public final class Proces_HODNOTA {
    private final int identifikátor_HODNOTA;
    private final int nadřazený_identifikátor;
    private final stránka_Správce.adresní_prostor adresní_prostor;
    private final Soubor_popisovač_tabulka Soubor_popisovač;
    private Proces_Stav Stav_HODNOTA = Proces_Stav.Připravit;
    private int ukončovací_kód;
    private int program_přerušení = 0x06000000;
    private int spuštění_START_ODKAZ;
    private String[] spuštění_argument = new String[0];
    private String[] prostředí_HODNOTA = new String[0];

    Proces_HODNOTA(int identifikátor_HODNOTA, int nadřazený_identifikátor, stránka_Správce.adresní_prostor adresní_prostor, Soubor_popisovač_tabulka Soubor_popisovač) {
        this.identifikátor_HODNOTA = identifikátor_HODNOTA;
        this.nadřazený_identifikátor = nadřazený_identifikátor;
        this.adresní_prostor = adresní_prostor;
        this.Soubor_popisovač = Soubor_popisovač;
    }

    public int identifikátor_HODNOTA() {
        return identifikátor_HODNOTA;
    }

    public int nadřazený_identifikátor() {
        return nadřazený_identifikátor;
    }

    public stránka_Správce.adresní_prostor adresní_prostor() {
        return adresní_prostor;
    }

    public Soubor_popisovač_tabulka Soubor_popisovač() {
        return Soubor_popisovač;
    }

    public Proces_Stav Stav_HODNOTA() {
        return Stav_HODNOTA;
    }

    public void sada_Stav(Proces_Stav 새상태) {
        Stav_HODNOTA = 새상태;
    }

    public int ukončovací_kód() {
        return ukončovací_kód;
    }

    public void Konec_program(int HODNOTA) {
        ukončovací_kód = HODNOTA & 0xff;
        Stav_HODNOTA = Proces_Stav.Konec_program;
    }

    public int program_přerušení() {
        return program_přerušení;
    }

    public void sada_program_přerušení(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("program_f5044b9b 끝 범위를 벗어났습니다.");
        }
        program_přerušení = 새끝;
    }

    public void sada_kontext(int START_ODKAZ, String[] parametr_argument, String[] prostředí_5d36e09c) {
        spuštění_START_ODKAZ = START_ODKAZ;
        spuštění_argument = parametr_argument.clone();
        prostředí_HODNOTA = prostředí_5d36e09c.clone();
    }

    public int spuštění_START_ODKAZ() { return spuštění_START_ODKAZ; }
    public String[] spuštění_argument() { return spuštění_argument.clone(); }
    public String[] prostředí_HODNOTA() { return prostředí_HODNOTA.clone(); }
}
