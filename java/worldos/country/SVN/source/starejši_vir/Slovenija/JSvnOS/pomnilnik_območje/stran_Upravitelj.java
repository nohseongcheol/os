// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenija.JSvnOS.pomnilnik_območje;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB stran_VALUE 연결과 Pisanje 시 복사를 제공한다. */
public final class stran_Upravitelj {
    public static final int velikost_strani = 4096;

    private static final class stran_VALUE {
        private byte[] podatki = new byte[velikost_strani];
        private int Gradiva_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class naslov_Space {
        private final Map<Integer, stran_VALUE> stran_tabela = new HashMap<Integer, stran_VALUE>();
    }

    public naslov_Space 새주소공간() {
        return new naslov_Space();
    }

    public void MAP_stran(naslov_Space naslov_območje, int navidezni_naslov, boolean 쓰기가능) {
        int INDEX = 쪽번호(navidezni_naslov);
        stran_VALUE 새쪽 = new stran_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        naslov_območje.stran_tabela.put(Integer.valueOf(INDEX), 새쪽);
    }

    public naslov_Space 쓰기시복사복제(naslov_Space 원본) {
        naslov_Space 복제본 = new naslov_Space();
        for (Map.Entry<Integer, stran_VALUE> vnos_VALUE : 원본.stran_tabela.entrySet()) {
            stran_VALUE 공유쪽 = vnos_VALUE.getValue();
            공유쪽.Gradiva_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.stran_tabela.put(vnos_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(naslov_Space naslov_območje, int navidezni_naslov) {
        stran_VALUE tarča = FIND_stran(naslov_območje, navidezni_naslov);
        return tarča.podatki[Math.floorMod(navidezni_naslov, velikost_strani)];
    }

    public void pisati_bajt_VALUE(naslov_Space naslov_območje, int navidezni_naslov, byte VALUE) {
        int INDEX = 쪽번호(navidezni_naslov);
        stran_VALUE tarča = FIND_stran(naslov_območje, navidezni_naslov);
        if (!tarča.쓰기가능) {
            if (!tarča.쓰기시복사) {
                throw new IllegalStateException("Branje 전용 쪽입니다.");
            }
            tarča = Ustvari_zasebno_stran(naslov_območje, INDEX, tarča);
        }
        tarča.podatki[Math.floorMod(navidezni_naslov, velikost_strani)] = VALUE;
    }

    public void zasebno_obseg_pisati(naslov_Space naslov_območje, int Start_naslov, int Velikost) {
        if (Velikost < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int končati_klic_naslov = Math.addExact(Start_naslov, Velikost);
        for (int naslov = Start_naslov; naslov < končati_klic_naslov; naslov = (쪽번호(naslov) + 1) * velikost_strani) {
            int INDEX = 쪽번호(naslov);
            stran_VALUE tarča = FIND_stran(naslov_območje, naslov);
            if (tarča.쓰기시복사) {
                Ustvari_zasebno_stran(naslov_območje, INDEX, tarča);
            } else {
                tarča.쓰기가능 = true;
            }
        }
    }

    public void obseg_pisati(naslov_Space naslov_območje, int Start_naslov, byte[] podatki) {
        for (int INDEX = 0; INDEX < podatki.length; INDEX++) {
            pisati_bajt_VALUE(naslov_območje, Start_naslov + INDEX, podatki[INDEX]);
        }
    }

    private stran_VALUE Ustvari_zasebno_stran(naslov_Space naslov_območje, int INDEX, stran_VALUE 공유쪽) {
        stran_VALUE zasebno_stran = new stran_VALUE();
        zasebno_stran.podatki = Arrays.copyOf(공유쪽.podatki, 공유쪽.podatki.length);
        zasebno_stran.쓰기가능 = true;
        zasebno_stran.쓰기시복사 = false;
        공유쪽.Gradiva_COUNT--;
        naslov_območje.stran_tabela.put(Integer.valueOf(INDEX), zasebno_stran);
        return zasebno_stran;
    }

    private stran_VALUE FIND_stran(naslov_Space naslov_območje, int naslov) {
        stran_VALUE tarča = naslov_območje.stran_tabela.get(Integer.valueOf(쪽번호(naslov)));
        if (tarča == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return tarča;
    }

    private int 쪽번호(int naslov) {
        if (naslov < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return naslov / velikost_strani;
    }
}

