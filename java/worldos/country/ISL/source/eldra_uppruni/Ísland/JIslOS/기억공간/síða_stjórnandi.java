// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ísland.JIslOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB síða_VALUE 연결과 Skrift 시 복사를 제공한다. */
public final class síða_stjórnandi {
    public static final int síðustærð = 4096;

    private static final class síða_VALUE {
        private byte[] gögn = new byte[síðustærð];
        private int tilvísun_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class slóð_svæði {
        private final Map<Integer, síða_VALUE> síða_tafla = new HashMap<Integer, síða_VALUE>();
    }

    public slóð_svæði 새주소공간() {
        return new slóð_svæði();
    }

    public void MAP_síða(slóð_svæði 공간, int sýndarvistfang, boolean 쓰기가능) {
        int INDEX = síða_númer(sýndarvistfang);
        síða_VALUE 새쪽 = new síða_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        공간.síða_tafla.put(Integer.valueOf(INDEX), 새쪽);
    }

    public slóð_svæði 쓰기시복사복제(slóð_svæði 원본) {
        slóð_svæði 복제본 = new slóð_svæði();
        for (Map.Entry<Integer, síða_VALUE> færsla_VALUE : 원본.síða_tafla.entrySet()) {
            síða_VALUE 공유쪽 = færsla_VALUE.getValue();
            공유쪽.tilvísun_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.síða_tafla.put(færsla_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(slóð_svæði 공간, int sýndarvistfang) {
        síða_VALUE markmið = FIND_síða(공간, sýndarvistfang);
        return markmið.gögn[Math.floorMod(sýndarvistfang, síðustærð)];
    }

    public void skrifa_bæti_VALUE(slóð_svæði 공간, int sýndarvistfang, byte VALUE) {
        int INDEX = síða_númer(sýndarvistfang);
        síða_VALUE markmið = FIND_síða(공간, sýndarvistfang);
        if (!markmið.쓰기가능) {
            if (!markmið.쓰기시복사) {
                throw new IllegalStateException("Lestur 전용 쪽입니다.");
            }
            markmið = stofna_einka_síða(공간, INDEX, markmið);
        }
        markmið.gögn[Math.floorMod(sýndarvistfang, síðustærð)] = VALUE;
    }

    public void 범위개인쓰기(slóð_svæði 공간, int Opna_slóð, int Stærð) {
        if (Stærð < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int ljúka_slóð = Math.addExact(Opna_slóð, Stærð);
        for (int slóð = Opna_slóð; slóð < ljúka_slóð; slóð = (síða_númer(slóð) + 1) * síðustærð) {
            int INDEX = síða_númer(slóð);
            síða_VALUE markmið = FIND_síða(공간, slóð);
            if (markmið.쓰기시복사) {
                stofna_einka_síða(공간, INDEX, markmið);
            } else {
                markmið.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(slóð_svæði 공간, int Opna_slóð, byte[] gögn) {
        for (int INDEX = 0; INDEX < gögn.length; INDEX++) {
            skrifa_bæti_VALUE(공간, Opna_slóð + INDEX, gögn[INDEX]);
        }
    }

    private síða_VALUE stofna_einka_síða(slóð_svæði 공간, int INDEX, síða_VALUE 공유쪽) {
        síða_VALUE einka_síða = new síða_VALUE();
        einka_síða.gögn = Arrays.copyOf(공유쪽.gögn, 공유쪽.gögn.length);
        einka_síða.쓰기가능 = true;
        einka_síða.쓰기시복사 = false;
        공유쪽.tilvísun_COUNT--;
        공간.síða_tafla.put(Integer.valueOf(INDEX), einka_síða);
        return einka_síða;
    }

    private síða_VALUE FIND_síða(slóð_svæði 공간, int slóð) {
        síða_VALUE markmið = 공간.síða_tafla.get(Integer.valueOf(síða_númer(slóð)));
        if (markmið == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return markmið;
    }

    private int síða_númer(int slóð) {
        if (slóð < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return slóð / síðustærð;
    }
}

