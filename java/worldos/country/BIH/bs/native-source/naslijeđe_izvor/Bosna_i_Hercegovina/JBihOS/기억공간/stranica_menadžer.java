// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB stranica_VALUE 연결과 Piši 시 복사를 제공한다. */
public final class stranica_menadžer {
    public static final int veličina_stranice = 4096;

    private static final class stranica_VALUE {
        private byte[] podaci = new byte[veličina_stranice];
        private int Reference_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class adresa_prostor {
        private final Map<Integer, stranica_VALUE> stranica_tabela = new HashMap<Integer, stranica_VALUE>();
    }

    public adresa_prostor 새주소공간() {
        return new adresa_prostor();
    }

    public void MAP_stranica(adresa_prostor 공간, int virtualno_adresa, boolean 쓰기가능) {
        int INDEX = 쪽번호(virtualno_adresa);
        stranica_VALUE 새쪽 = new stranica_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        공간.stranica_tabela.put(Integer.valueOf(INDEX), 새쪽);
    }

    public adresa_prostor 쓰기시복사복제(adresa_prostor 원본) {
        adresa_prostor 복제본 = new adresa_prostor();
        for (Map.Entry<Integer, stranica_VALUE> unos_VALUE : 원본.stranica_tabela.entrySet()) {
            stranica_VALUE 공유쪽 = unos_VALUE.getValue();
            공유쪽.Reference_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.stranica_tabela.put(unos_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(adresa_prostor 공간, int virtualno_adresa) {
        stranica_VALUE cilj = FIND_stranica(공간, virtualno_adresa);
        return cilj.podaci[Math.floorMod(virtualno_adresa, veličina_stranice)];
    }

    public void pisati_bajt_VALUE(adresa_prostor 공간, int virtualno_adresa, byte VALUE) {
        int INDEX = 쪽번호(virtualno_adresa);
        stranica_VALUE cilj = FIND_stranica(공간, virtualno_adresa);
        if (!cilj.쓰기가능) {
            if (!cilj.쓰기시복사) {
                throw new IllegalStateException("Čitaj 전용 쪽입니다.");
            }
            cilj = Create_privatni_stranica(공간, INDEX, cilj);
        }
        cilj.podaci[Math.floorMod(virtualno_adresa, veličina_stranice)] = VALUE;
    }

    public void 범위개인쓰기(adresa_prostor 공간, int početna_adresa, int Veličina) {
        if (Veličina < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int završiti_adresa = Math.addExact(početna_adresa, Veličina);
        for (int adresa = početna_adresa; adresa < završiti_adresa; adresa = (쪽번호(adresa) + 1) * veličina_stranice) {
            int INDEX = 쪽번호(adresa);
            stranica_VALUE cilj = FIND_stranica(공간, adresa);
            if (cilj.쓰기시복사) {
                Create_privatni_stranica(공간, INDEX, cilj);
            } else {
                cilj.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(adresa_prostor 공간, int početna_adresa, byte[] podaci) {
        for (int INDEX = 0; INDEX < podaci.length; INDEX++) {
            pisati_bajt_VALUE(공간, početna_adresa + INDEX, podaci[INDEX]);
        }
    }

    private stranica_VALUE Create_privatni_stranica(adresa_prostor 공간, int INDEX, stranica_VALUE 공유쪽) {
        stranica_VALUE privatni_stranica = new stranica_VALUE();
        privatni_stranica.podaci = Arrays.copyOf(공유쪽.podaci, 공유쪽.podaci.length);
        privatni_stranica.쓰기가능 = true;
        privatni_stranica.쓰기시복사 = false;
        공유쪽.Reference_COUNT--;
        공간.stranica_tabela.put(Integer.valueOf(INDEX), privatni_stranica);
        return privatni_stranica;
    }

    private stranica_VALUE FIND_stranica(adresa_prostor 공간, int adresa) {
        stranica_VALUE cilj = 공간.stranica_tabela.get(Integer.valueOf(쪽번호(adresa)));
        if (cilj == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return cilj;
    }

    private int 쪽번호(int adresa) {
        if (adresa < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return adresa / veličina_stranice;
    }
}

