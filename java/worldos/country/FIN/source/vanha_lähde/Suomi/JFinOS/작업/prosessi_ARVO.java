// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Suomi.JFinOS.작업;

import Suomi.JFinOS.Muisti_alue.page_Valvoja;
import Suomi.JFinOS.tiedostojärjestelmä.파일서술자표;

public final class prosessi_ARVO {
    private final int tunniste_ARVO;
    private final int pää_tunniste;
    private final page_Valvoja.osoiteavaruus osoiteavaruus;
    private final 파일서술자표 파일서술자;
    private prosessi_Tila Tila_ARVO = prosessi_Tila.Valmistele;
    private int lopetuskoodi;
    private int ohjelma_tauko = 0x06000000;
    private int suoritus_alku_OSOITE;
    private String[] suoritus_argumentti = new String[0];
    private String[] ympäristö_ARVO = new String[0];

    prosessi_ARVO(int tunniste_ARVO, int pää_tunniste, page_Valvoja.osoiteavaruus osoiteavaruus, 파일서술자표 파일서술자) {
        this.tunniste_ARVO = tunniste_ARVO;
        this.pää_tunniste = pää_tunniste;
        this.osoiteavaruus = osoiteavaruus;
        this.파일서술자 = 파일서술자;
    }

    public int tunniste_ARVO() {
        return tunniste_ARVO;
    }

    public int pää_tunniste() {
        return pää_tunniste;
    }

    public page_Valvoja.osoiteavaruus osoiteavaruus() {
        return osoiteavaruus;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public prosessi_Tila Tila_ARVO() {
        return Tila_ARVO;
    }

    public void ryhmä_Tila(prosessi_Tila 새상태) {
        Tila_ARVO = 새상태;
    }

    public int lopetuskoodi() {
        return lopetuskoodi;
    }

    public void Lopeta_ohjelma(int ARVO) {
        lopetuskoodi = ARVO & 0xff;
        Tila_ARVO = prosessi_Tila.Lopeta_ohjelma;
    }

    public int ohjelma_tauko() {
        return ohjelma_tauko;
    }

    public void ryhmä_ohjelma_tauko(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("ohjelma_f5044b9b 끝 범위를 벗어났습니다.");
        }
        ohjelma_tauko = 새끝;
    }

    public void ryhmä_suoritus_konteksti(int alku_OSOITE, String[] parametri_argumentti, String[] ympäristö) {
        suoritus_alku_OSOITE = alku_OSOITE;
        suoritus_argumentti = parametri_argumentti.clone();
        ympäristö_ARVO = ympäristö.clone();
    }

    public int suoritus_alku_OSOITE() { return suoritus_alku_OSOITE; }
    public String[] suoritus_argumentti() { return suoritus_argumentti.clone(); }
    public String[] ympäristö_ARVO() { return ympäristö_ARVO.clone(); }
}
