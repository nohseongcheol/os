// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Soome.JFinOS.Mälu_regioon;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB leht_VALUE 연결과 Kirjutamine 시 복사를 제공한다. */
public final class 쪽관리자 {
    public static final int lehekülje_suurus = 4096;

    private static final class leht_VALUE {
        private byte[] andmed = new byte[lehekülje_suurus];
        private int viide_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ADDRESS_ruum {
        private final Map<Integer, leht_VALUE> leht_tabel = new HashMap<Integer, leht_VALUE>();
    }

    public ADDRESS_ruum 새주소공간() {
        return new ADDRESS_ruum();
    }

    public void MAP_leht(ADDRESS_ruum ADDRESS_regioon, int virtuaalaadress, boolean 쓰기가능) {
        int INDEX = leht_number(virtuaalaadress);
        leht_VALUE 새쪽 = new leht_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        ADDRESS_regioon.leht_tabel.put(Integer.valueOf(INDEX), 새쪽);
    }

    public ADDRESS_ruum 쓰기시복사복제(ADDRESS_ruum 원본) {
        ADDRESS_ruum 복제본 = new ADDRESS_ruum();
        for (Map.Entry<Integer, leht_VALUE> kirje_VALUE : 원본.leht_tabel.entrySet()) {
            leht_VALUE 공유쪽 = kirje_VALUE.getValue();
            공유쪽.viide_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.leht_tabel.put(kirje_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(ADDRESS_ruum ADDRESS_regioon, int virtuaalaadress) {
        leht_VALUE siht = FIND_leht(ADDRESS_regioon, virtuaalaadress);
        return siht.andmed[Math.floorMod(virtuaalaadress, lehekülje_suurus)];
    }

    public void kirjutamine_bait_VALUE(ADDRESS_ruum ADDRESS_regioon, int virtuaalaadress, byte VALUE) {
        int INDEX = leht_number(virtuaalaadress);
        leht_VALUE siht = FIND_leht(ADDRESS_regioon, virtuaalaadress);
        if (!siht.쓰기가능) {
            if (!siht.쓰기시복사) {
                throw new IllegalStateException("Lugemine 전용 쪽입니다.");
            }
            siht = avama_era_leht(ADDRESS_regioon, INDEX, siht);
        }
        siht.andmed[Math.floorMod(virtuaalaadress, lehekülje_suurus)] = VALUE;
    }

    public void era_vahemik_kirjutamine(ADDRESS_ruum ADDRESS_regioon, int START_ADDRESS, int Suurus) {
        if (Suurus < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int lõpeta_kõne_ADDRESS = Math.addExact(START_ADDRESS, Suurus);
        for (int ADDRESS = START_ADDRESS; ADDRESS < lõpeta_kõne_ADDRESS; ADDRESS = (leht_number(ADDRESS) + 1) * lehekülje_suurus) {
            int INDEX = leht_number(ADDRESS);
            leht_VALUE siht = FIND_leht(ADDRESS_regioon, ADDRESS);
            if (siht.쓰기시복사) {
                avama_era_leht(ADDRESS_regioon, INDEX, siht);
            } else {
                siht.쓰기가능 = true;
            }
        }
    }

    public void vahemik_kirjutamine(ADDRESS_ruum ADDRESS_regioon, int START_ADDRESS, byte[] andmed) {
        for (int INDEX = 0; INDEX < andmed.length; INDEX++) {
            kirjutamine_bait_VALUE(ADDRESS_regioon, START_ADDRESS + INDEX, andmed[INDEX]);
        }
    }

    private leht_VALUE avama_era_leht(ADDRESS_ruum ADDRESS_regioon, int INDEX, leht_VALUE 공유쪽) {
        leht_VALUE era_leht = new leht_VALUE();
        era_leht.andmed = Arrays.copyOf(공유쪽.andmed, 공유쪽.andmed.length);
        era_leht.쓰기가능 = true;
        era_leht.쓰기시복사 = false;
        공유쪽.viide_COUNT--;
        ADDRESS_regioon.leht_tabel.put(Integer.valueOf(INDEX), era_leht);
        return era_leht;
    }

    private leht_VALUE FIND_leht(ADDRESS_ruum ADDRESS_regioon, int ADDRESS) {
        leht_VALUE siht = ADDRESS_regioon.leht_tabel.get(Integer.valueOf(leht_number(ADDRESS)));
        if (siht == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return siht;
    }

    private int leht_number(int ADDRESS) {
        if (ADDRESS < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ADDRESS / lehekülje_suurus;
    }
}

