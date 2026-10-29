// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Venäjä.JRusOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Venäjä.JRusOS.Muisti_alue.page_Valvoja;
import Venäjä.JRusOS.tiedostojärjestelmä.파일서술자표;

/** prosessi_ARVO 식별자와 라운드로빈 Valmistele 대기열을 관리한다. */
public final class Aikataulutus {
    private final page_Valvoja 쪽관리;
    private final Map<Integer, prosessi_ARVO> prosessiluettelo = new HashMap<Integer, prosessi_ARVO>();
    private final Queue<prosessi_ARVO> 준비대기열 = new ArrayDeque<prosessi_ARVO>();
    private int Seuraava_tunniste = 1;

    public Aikataulutus(page_Valvoja 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public prosessi_ARVO 첫과정(파일서술자표 파일서술자) {
        prosessi_ARVO 새과정 = new prosessi_ARVO(jakaa_tunniste(), 0, 쪽관리.새주소공간(), 파일서술자);
        prosessiluettelo.put(Integer.valueOf(새과정.tunniste_ARVO()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public prosessi_ARVO klooni_ARVO(prosessi_ARVO pää_ARVO) {
        prosessi_ARVO ali_ARVO = new prosessi_ARVO(
                jakaa_tunniste(),
                pää_ARVO.tunniste_ARVO(),
                쪽관리.쓰기시복사복제(pää_ARVO.osoiteavaruus()),
                pää_ARVO.파일서술자().klooni_ARVO());
        ali_ARVO.ryhmä_ohjelma_tauko(pää_ARVO.ohjelma_tauko());
        prosessiluettelo.put(Integer.valueOf(ali_ARVO.tunniste_ARVO()), ali_ARVO);
        준비대기열.offer(ali_ARVO);
        return ali_ARVO;
    }

    public prosessi_ARVO Seuraava_prosessi() {
        int sekki_LASKE = 준비대기열.size();
        for (int INDEKSI = 0; INDEKSI < sekki_LASKE; INDEKSI++) {
            prosessi_ARVO Seuraava_kohde = 준비대기열.poll();
            if (Seuraava_kohde != null && (Seuraava_kohde.Tila_ARVO() == prosessi_Tila.Valmistele || Seuraava_kohde.Tila_ARVO() == prosessi_Tila.Suorita_komento)) {
                Seuraava_kohde.ryhmä_Tila(prosessi_Tila.Suorita_komento);
                준비대기열.offer(Seuraava_kohde);
                return Seuraava_kohde;
            }
        }
        return null;
    }

    public int 자식기다리기(prosessi_ARVO pää_ARVO, int ali_tunniste, boolean 기다리지않음) {
        for (prosessi_ARVO 후보 : prosessiluettelo.values()) {
            if (후보.pää_tunniste() != pää_ARVO.tunniste_ARVO()) {
                continue;
            }
            if (ali_tunniste > 0 && 후보.tunniste_ARVO() != ali_tunniste) {
                continue;
            }
            if (후보.Tila_ARVO() == prosessi_Tila.Lopeta_ohjelma) {
                int TULOS = (후보.lopetuskoodi() & 0xff) << 8;
                prosessiluettelo.remove(Integer.valueOf(후보.tunniste_ARVO()));
                return TULOS;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public prosessi_ARVO ETSI_prosessi(int tunniste_ARVO) {
        return prosessiluettelo.get(Integer.valueOf(tunniste_ARVO));
    }

    private int jakaa_tunniste() {
        return Seuraava_tunniste++;
    }
}
