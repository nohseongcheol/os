// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hrvatska.JHrvOS.Memorija_regije;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB dojaviti_VALUE 연결과 Zapisuj 시 복사를 제공한다. */
public final class dojaviti_Upravitelj {
    public static final int veličina_stranice = 4096;

    private static final class dojaviti_VALUE {
        private byte[] podaci = new byte[veličina_stranice];
        private int Reference_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class adresa_Space {
        private final Map<Integer, dojaviti_VALUE> dojaviti_tablica = new HashMap<Integer, dojaviti_VALUE>();
    }

    public adresa_Space 새주소공간() {
        return new adresa_Space();
    }

    public void MAP_dojaviti(adresa_Space adresa_regije, int virtualna_adresa, boolean 쓰기가능) {
        int INDEX = 쪽번호(virtualna_adresa);
        dojaviti_VALUE 새쪽 = new dojaviti_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        adresa_regije.dojaviti_tablica.put(Integer.valueOf(INDEX), 새쪽);
    }

    public adresa_Space 쓰기시복사복제(adresa_Space 원본) {
        adresa_Space 복제본 = new adresa_Space();
        for (Map.Entry<Integer, dojaviti_VALUE> unos_VALUE : 원본.dojaviti_tablica.entrySet()) {
            dojaviti_VALUE 공유쪽 = unos_VALUE.getValue();
            공유쪽.Reference_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.dojaviti_tablica.put(unos_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(adresa_Space adresa_regije, int virtualna_adresa) {
        dojaviti_VALUE cilj = FIND_dojaviti(adresa_regije, virtualna_adresa);
        return cilj.podaci[Math.floorMod(virtualna_adresa, veličina_stranice)];
    }

    public void zapisivanje_bajt_VALUE(adresa_Space adresa_regije, int virtualna_adresa, byte VALUE) {
        int INDEX = 쪽번호(virtualna_adresa);
        dojaviti_VALUE cilj = FIND_dojaviti(adresa_regije, virtualna_adresa);
        if (!cilj.쓰기가능) {
            if (!cilj.쓰기시복사) {
                throw new IllegalStateException("Čitaj 전용 쪽입니다.");
            }
            cilj = Create_privatan_dojaviti(adresa_regije, INDEX, cilj);
        }
        cilj.podaci[Math.floorMod(virtualna_adresa, veličina_stranice)] = VALUE;
    }

    public void privatan_raspon_zapisivanje(adresa_Space adresa_regije, int START_adresa, int Veličina) {
        if (Veličina < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int završiti_razgovor_adresa = Math.addExact(START_adresa, Veličina);
        for (int adresa = START_adresa; adresa < završiti_razgovor_adresa; adresa = (쪽번호(adresa) + 1) * veličina_stranice) {
            int INDEX = 쪽번호(adresa);
            dojaviti_VALUE cilj = FIND_dojaviti(adresa_regije, adresa);
            if (cilj.쓰기시복사) {
                Create_privatan_dojaviti(adresa_regije, INDEX, cilj);
            } else {
                cilj.쓰기가능 = true;
            }
        }
    }

    public void raspon_zapisivanje(adresa_Space adresa_regije, int START_adresa, byte[] podaci) {
        for (int INDEX = 0; INDEX < podaci.length; INDEX++) {
            zapisivanje_bajt_VALUE(adresa_regije, START_adresa + INDEX, podaci[INDEX]);
        }
    }

    private dojaviti_VALUE Create_privatan_dojaviti(adresa_Space adresa_regije, int INDEX, dojaviti_VALUE 공유쪽) {
        dojaviti_VALUE privatan_dojaviti = new dojaviti_VALUE();
        privatan_dojaviti.podaci = Arrays.copyOf(공유쪽.podaci, 공유쪽.podaci.length);
        privatan_dojaviti.쓰기가능 = true;
        privatan_dojaviti.쓰기시복사 = false;
        공유쪽.Reference_COUNT--;
        adresa_regije.dojaviti_tablica.put(Integer.valueOf(INDEX), privatan_dojaviti);
        return privatan_dojaviti;
    }

    private dojaviti_VALUE FIND_dojaviti(adresa_Space adresa_regije, int adresa) {
        dojaviti_VALUE cilj = adresa_regije.dojaviti_tablica.get(Integer.valueOf(쪽번호(adresa)));
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

