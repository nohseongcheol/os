// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espainia.JEspOS.gailu_balio;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI gailu_balio 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class osagarri_bus_kudeatzaile {
    public static final class gailu_balio {
        private final int saltzaile_identifikatzaile;
        private final int gailu_identifikatzaile;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public gailu_balio(int saltzaile_identifikatzaile, int gailu_identifikatzaile, int 입출력바탕, int 개입중단번호) {
            this.saltzaile_identifikatzaile = saltzaile_identifikatzaile;
            this.gailu_identifikatzaile = gailu_identifikatzaile;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int saltzaile_identifikatzaile() { return saltzaile_identifikatzaile; }
        public int gailu_identifikatzaile() { return gailu_identifikatzaile; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<gailu_balio> Gailuak_Zerrenda = new ArrayList<gailu_balio>();

    public void 발견(gailu_balio gailu_balio) {
        Gailuak_Zerrenda.add(gailu_balio);
    }

    public List<gailu_balio> Gailuak_Zerrenda() {
        return Collections.unmodifiableList(Gailuak_Zerrenda);
    }

    public gailu_balio Bilatu_sarrera(int saltzaile_identifikatzaile, int gailu_identifikatzaile) {
        for (gailu_balio 후보 : Gailuak_Zerrenda) {
            if (후보.saltzaile_identifikatzaile == saltzaile_identifikatzaile && 후보.gailu_identifikatzaile == gailu_identifikatzaile) {
                return 후보;
            }
        }
        return null;
    }
}

