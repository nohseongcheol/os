// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.Memorija_oblast;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB stranica_VALUE 연결과 쓰기 시 복사를 제공한다. */
public final class stranica_menadžer {
    public static final int veličina_stranice = 4096;

    private static final class stranica_VALUE {
        private byte[] podaci = new byte[veličina_stranice];
        private int referenca_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class adresa_prostor {
        private final Map<Integer, stranica_VALUE> stranica_tabela = new HashMap<Integer, stranica_VALUE>();
    }

    public adresa_prostor 새주소공간() {
        return new adresa_prostor();
    }

    public void MAP_stranica(adresa_prostor adresa_oblast, int virtuelna_adresa, boolean 쓰기가능) {
        int INDEX = 쪽번호(virtuelna_adresa);
        stranica_VALUE 새쪽 = new stranica_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        adresa_oblast.stranica_tabela.put(Integer.valueOf(INDEX), 새쪽);
    }

    public adresa_prostor 쓰기시복사복제(adresa_prostor 원본) {
        adresa_prostor 복제본 = new adresa_prostor();
        for (Map.Entry<Integer, stranica_VALUE> stavka_VALUE : 원본.stranica_tabela.entrySet()) {
            stranica_VALUE 공유쪽 = stavka_VALUE.getValue();
            공유쪽.referenca_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.stranica_tabela.put(stavka_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(adresa_prostor adresa_oblast, int virtuelna_adresa) {
        stranica_VALUE cilj = FIND_stranica(adresa_oblast, virtuelna_adresa);
        return cilj.podaci[Math.floorMod(virtuelna_adresa, veličina_stranice)];
    }

    public void 바이트쓰기(adresa_prostor adresa_oblast, int virtuelna_adresa, byte VALUE) {
        int INDEX = 쪽번호(virtuelna_adresa);
        stranica_VALUE cilj = FIND_stranica(adresa_oblast, virtuelna_adresa);
        if (!cilj.쓰기가능) {
            if (!cilj.쓰기시복사) {
                throw new IllegalStateException("읽기 전용 쪽입니다.");
            }
            cilj = Create_privatan_stranica(adresa_oblast, INDEX, cilj);
        }
        cilj.podaci[Math.floorMod(virtuelna_adresa, veličina_stranice)] = VALUE;
    }

    public void 범위개인쓰기(adresa_prostor adresa_oblast, int START_adresa, int promeniti_veličinu) {
        if (promeniti_veličinu < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int završiti_razgovor_adresa = Math.addExact(START_adresa, promeniti_veličinu);
        for (int adresa = START_adresa; adresa < završiti_razgovor_adresa; adresa = (쪽번호(adresa) + 1) * veličina_stranice) {
            int INDEX = 쪽번호(adresa);
            stranica_VALUE cilj = FIND_stranica(adresa_oblast, adresa);
            if (cilj.쓰기시복사) {
                Create_privatan_stranica(adresa_oblast, INDEX, cilj);
            } else {
                cilj.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(adresa_prostor adresa_oblast, int START_adresa, byte[] podaci) {
        for (int INDEX = 0; INDEX < podaci.length; INDEX++) {
            바이트쓰기(adresa_oblast, START_adresa + INDEX, podaci[INDEX]);
        }
    }

    private stranica_VALUE Create_privatan_stranica(adresa_prostor adresa_oblast, int INDEX, stranica_VALUE 공유쪽) {
        stranica_VALUE privatan_stranica = new stranica_VALUE();
        privatan_stranica.podaci = Arrays.copyOf(공유쪽.podaci, 공유쪽.podaci.length);
        privatan_stranica.쓰기가능 = true;
        privatan_stranica.쓰기시복사 = false;
        공유쪽.referenca_COUNT--;
        adresa_oblast.stranica_tabela.put(Integer.valueOf(INDEX), privatan_stranica);
        return privatan_stranica;
    }

    private stranica_VALUE FIND_stranica(adresa_prostor adresa_oblast, int adresa) {
        stranica_VALUE cilj = adresa_oblast.stranica_tabela.get(Integer.valueOf(쪽번호(adresa)));
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

