// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lenkija.JPolOS.atmintis_sritis;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB puslapis_VALUE 연결과 Rašymas 시 복사를 제공한다. */
public final class 쪽관리자 {
    public static final int puslapio_formatas = 4096;

    private static final class puslapis_VALUE {
        private byte[] duomenys = new byte[puslapio_formatas];
        private int nuoroda_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ADDRESS_erdvė {
        private final Map<Integer, puslapis_VALUE> puslapis_lentelė = new HashMap<Integer, puslapis_VALUE>();
    }

    public ADDRESS_erdvė 새주소공간() {
        return new ADDRESS_erdvė();
    }

    public void MAP_puslapis(ADDRESS_erdvė ADDRESS_sritis, int virtualusis_adresas, boolean 쓰기가능) {
        int INDEX = puslapis_numeris(virtualusis_adresas);
        puslapis_VALUE 새쪽 = new puslapis_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        ADDRESS_sritis.puslapis_lentelė.put(Integer.valueOf(INDEX), 새쪽);
    }

    public ADDRESS_erdvė 쓰기시복사복제(ADDRESS_erdvė 원본) {
        ADDRESS_erdvė 복제본 = new ADDRESS_erdvė();
        for (Map.Entry<Integer, puslapis_VALUE> įrašas_VALUE : 원본.puslapis_lentelė.entrySet()) {
            puslapis_VALUE 공유쪽 = įrašas_VALUE.getValue();
            공유쪽.nuoroda_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.puslapis_lentelė.put(įrašas_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(ADDRESS_erdvė ADDRESS_sritis, int virtualusis_adresas) {
        puslapis_VALUE tikslas = FIND_puslapis(ADDRESS_sritis, virtualusis_adresas);
        return tikslas.duomenys[Math.floorMod(virtualusis_adresas, puslapio_formatas)];
    }

    public void rašymas_baitas_VALUE(ADDRESS_erdvė ADDRESS_sritis, int virtualusis_adresas, byte VALUE) {
        int INDEX = puslapis_numeris(virtualusis_adresas);
        puslapis_VALUE tikslas = FIND_puslapis(ADDRESS_sritis, virtualusis_adresas);
        if (!tikslas.쓰기가능) {
            if (!tikslas.쓰기시복사) {
                throw new IllegalStateException("Skaitymas 전용 쪽입니다.");
            }
            tikslas = kurti_privatus_puslapis(ADDRESS_sritis, INDEX, tikslas);
        }
        tikslas.duomenys[Math.floorMod(virtualusis_adresas, puslapio_formatas)] = VALUE;
    }

    public void privatus_diapazonas_rašymas(ADDRESS_erdvė ADDRESS_sritis, int Start_ADDRESS, int Dydis) {
        if (Dydis < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int baigti_pokalbį_ADDRESS = Math.addExact(Start_ADDRESS, Dydis);
        for (int ADDRESS = Start_ADDRESS; ADDRESS < baigti_pokalbį_ADDRESS; ADDRESS = (puslapis_numeris(ADDRESS) + 1) * puslapio_formatas) {
            int INDEX = puslapis_numeris(ADDRESS);
            puslapis_VALUE tikslas = FIND_puslapis(ADDRESS_sritis, ADDRESS);
            if (tikslas.쓰기시복사) {
                kurti_privatus_puslapis(ADDRESS_sritis, INDEX, tikslas);
            } else {
                tikslas.쓰기가능 = true;
            }
        }
    }

    public void diapazonas_rašymas(ADDRESS_erdvė ADDRESS_sritis, int Start_ADDRESS, byte[] duomenys) {
        for (int INDEX = 0; INDEX < duomenys.length; INDEX++) {
            rašymas_baitas_VALUE(ADDRESS_sritis, Start_ADDRESS + INDEX, duomenys[INDEX]);
        }
    }

    private puslapis_VALUE kurti_privatus_puslapis(ADDRESS_erdvė ADDRESS_sritis, int INDEX, puslapis_VALUE 공유쪽) {
        puslapis_VALUE privatus_puslapis = new puslapis_VALUE();
        privatus_puslapis.duomenys = Arrays.copyOf(공유쪽.duomenys, 공유쪽.duomenys.length);
        privatus_puslapis.쓰기가능 = true;
        privatus_puslapis.쓰기시복사 = false;
        공유쪽.nuoroda_COUNT--;
        ADDRESS_sritis.puslapis_lentelė.put(Integer.valueOf(INDEX), privatus_puslapis);
        return privatus_puslapis;
    }

    private puslapis_VALUE FIND_puslapis(ADDRESS_erdvė ADDRESS_sritis, int ADDRESS) {
        puslapis_VALUE tikslas = ADDRESS_sritis.puslapis_lentelė.get(Integer.valueOf(puslapis_numeris(ADDRESS)));
        if (tikslas == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return tikslas;
    }

    private int puslapis_numeris(int ADDRESS) {
        if (ADDRESS < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ADDRESS / puslapio_formatas;
    }
}

