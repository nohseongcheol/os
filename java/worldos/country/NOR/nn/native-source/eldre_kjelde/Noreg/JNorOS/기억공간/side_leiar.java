// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Noreg.JNorOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB side_VALUE 연결과 Skriv 시 복사를 제공한다. */
public final class side_leiar {
    public static final int sidestorleik = 4096;

    private static final class side_VALUE {
        private byte[] data = new byte[sidestorleik];
        private int Oppslagsverk_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ADDRESS_område {
        private final Map<Integer, side_VALUE> side_tabell = new HashMap<Integer, side_VALUE>();
    }

    public ADDRESS_område 새주소공간() {
        return new ADDRESS_område();
    }

    public void MAP_side(ADDRESS_område 공간, int virtuell_adresse, boolean 쓰기가능) {
        int INDEX = 쪽번호(virtuell_adresse);
        side_VALUE 새쪽 = new side_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        공간.side_tabell.put(Integer.valueOf(INDEX), 새쪽);
    }

    public ADDRESS_område 쓰기시복사복제(ADDRESS_område 원본) {
        ADDRESS_område 복제본 = new ADDRESS_område();
        for (Map.Entry<Integer, side_VALUE> oppføring_VALUE : 원본.side_tabell.entrySet()) {
            side_VALUE 공유쪽 = oppføring_VALUE.getValue();
            공유쪽.Oppslagsverk_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.side_tabell.put(oppføring_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(ADDRESS_område 공간, int virtuell_adresse) {
        side_VALUE mål = Søk_side(공간, virtuell_adresse);
        return mål.data[Math.floorMod(virtuell_adresse, sidestorleik)];
    }

    public void skrive_byte_VALUE(ADDRESS_område 공간, int virtuell_adresse, byte VALUE) {
        int INDEX = 쪽번호(virtuell_adresse);
        side_VALUE mål = Søk_side(공간, virtuell_adresse);
        if (!mål.쓰기가능) {
            if (!mål.쓰기시복사) {
                throw new IllegalStateException("Les 전용 쪽입니다.");
            }
            mål = Opprett_privat_side(공간, INDEX, mål);
        }
        mål.data[Math.floorMod(virtuell_adresse, sidestorleik)] = VALUE;
    }

    public void 범위개인쓰기(ADDRESS_område 공간, int START_ADDRESS, int Storleik) {
        if (Storleik < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int avslutte_ADDRESS = Math.addExact(START_ADDRESS, Storleik);
        for (int ADDRESS = START_ADDRESS; ADDRESS < avslutte_ADDRESS; ADDRESS = (쪽번호(ADDRESS) + 1) * sidestorleik) {
            int INDEX = 쪽번호(ADDRESS);
            side_VALUE mål = Søk_side(공간, ADDRESS);
            if (mål.쓰기시복사) {
                Opprett_privat_side(공간, INDEX, mål);
            } else {
                mål.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(ADDRESS_område 공간, int START_ADDRESS, byte[] data) {
        for (int INDEX = 0; INDEX < data.length; INDEX++) {
            skrive_byte_VALUE(공간, START_ADDRESS + INDEX, data[INDEX]);
        }
    }

    private side_VALUE Opprett_privat_side(ADDRESS_område 공간, int INDEX, side_VALUE 공유쪽) {
        side_VALUE privat_side = new side_VALUE();
        privat_side.data = Arrays.copyOf(공유쪽.data, 공유쪽.data.length);
        privat_side.쓰기가능 = true;
        privat_side.쓰기시복사 = false;
        공유쪽.Oppslagsverk_COUNT--;
        공간.side_tabell.put(Integer.valueOf(INDEX), privat_side);
        return privat_side;
    }

    private side_VALUE Søk_side(ADDRESS_område 공간, int ADDRESS) {
        side_VALUE mål = 공간.side_tabell.get(Integer.valueOf(쪽번호(ADDRESS)));
        if (mål == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return mål;
    }

    private int 쪽번호(int ADDRESS) {
        if (ADDRESS < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ADDRESS / sidestorleik;
    }
}

