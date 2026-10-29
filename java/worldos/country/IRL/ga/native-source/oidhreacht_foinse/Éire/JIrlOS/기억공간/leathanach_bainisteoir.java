// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Éire.JIrlOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB leathanach_VALUE 연결과 Scríobh 시 복사를 제공한다. */
public final class leathanach_bainisteoir {
    public static final int méid_leathanaigh = 4096;

    private static final class leathanach_VALUE {
        private byte[] sonraí = new byte[méid_leathanaigh];
        private int Leabhair_thagartha_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ADDRESS_spás {
        private final Map<Integer, leathanach_VALUE> leathanach_tábla = new HashMap<Integer, leathanach_VALUE>();
    }

    public ADDRESS_spás 새주소공간() {
        return new ADDRESS_spás();
    }

    public void MAPÁIL_leathanach(ADDRESS_spás 공간, int seoladh_fíorúil, boolean 쓰기가능) {
        int INDEX = 쪽번호(seoladh_fíorúil);
        leathanach_VALUE 새쪽 = new leathanach_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        공간.leathanach_tábla.put(Integer.valueOf(INDEX), 새쪽);
    }

    public ADDRESS_spás 쓰기시복사복제(ADDRESS_spás 원본) {
        ADDRESS_spás 복제본 = new ADDRESS_spás();
        for (Map.Entry<Integer, leathanach_VALUE> iontráil_VALUE : 원본.leathanach_tábla.entrySet()) {
            leathanach_VALUE 공유쪽 = iontráil_VALUE.getValue();
            공유쪽.Leabhair_thagartha_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.leathanach_tábla.put(iontráil_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(ADDRESS_spás 공간, int seoladh_fíorúil) {
        leathanach_VALUE sprioc = FIND_leathanach(공간, seoladh_fíorúil);
        return sprioc.sonraí[Math.floorMod(seoladh_fíorúil, méid_leathanaigh)];
    }

    public void scríobh_beart_VALUE(ADDRESS_spás 공간, int seoladh_fíorúil, byte VALUE) {
        int INDEX = 쪽번호(seoladh_fíorúil);
        leathanach_VALUE sprioc = FIND_leathanach(공간, seoladh_fíorúil);
        if (!sprioc.쓰기가능) {
            if (!sprioc.쓰기시복사) {
                throw new IllegalStateException("Léigh 전용 쪽입니다.");
            }
            sprioc = Create_príobháideach_leathanach(공간, INDEX, sprioc);
        }
        sprioc.sonraí[Math.floorMod(seoladh_fíorúil, méid_leathanaigh)] = VALUE;
    }

    public void 범위개인쓰기(ADDRESS_spás 공간, int seoladh_tosaithe, int Méid) {
        if (Méid < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int cuir_deireadh_le_ADDRESS = Math.addExact(seoladh_tosaithe, Méid);
        for (int ADDRESS = seoladh_tosaithe; ADDRESS < cuir_deireadh_le_ADDRESS; ADDRESS = (쪽번호(ADDRESS) + 1) * méid_leathanaigh) {
            int INDEX = 쪽번호(ADDRESS);
            leathanach_VALUE sprioc = FIND_leathanach(공간, ADDRESS);
            if (sprioc.쓰기시복사) {
                Create_príobháideach_leathanach(공간, INDEX, sprioc);
            } else {
                sprioc.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(ADDRESS_spás 공간, int seoladh_tosaithe, byte[] sonraí) {
        for (int INDEX = 0; INDEX < sonraí.length; INDEX++) {
            scríobh_beart_VALUE(공간, seoladh_tosaithe + INDEX, sonraí[INDEX]);
        }
    }

    private leathanach_VALUE Create_príobháideach_leathanach(ADDRESS_spás 공간, int INDEX, leathanach_VALUE 공유쪽) {
        leathanach_VALUE príobháideach_leathanach = new leathanach_VALUE();
        príobháideach_leathanach.sonraí = Arrays.copyOf(공유쪽.sonraí, 공유쪽.sonraí.length);
        príobháideach_leathanach.쓰기가능 = true;
        príobháideach_leathanach.쓰기시복사 = false;
        공유쪽.Leabhair_thagartha_COUNT--;
        공간.leathanach_tábla.put(Integer.valueOf(INDEX), príobháideach_leathanach);
        return príobháideach_leathanach;
    }

    private leathanach_VALUE FIND_leathanach(ADDRESS_spás 공간, int ADDRESS) {
        leathanach_VALUE sprioc = 공간.leathanach_tábla.get(Integer.valueOf(쪽번호(ADDRESS)));
        if (sprioc == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return sprioc;
    }

    private int 쪽번호(int ADDRESS) {
        if (ADDRESS < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ADDRESS / méid_leathanaigh;
    }
}

