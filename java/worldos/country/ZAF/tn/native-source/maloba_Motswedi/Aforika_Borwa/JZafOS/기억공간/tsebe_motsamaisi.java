// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aforika_Borwa.JZafOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB tsebe_Boleng 연결과 kwala 시 복사를 제공한다. */
public final class tsebe_motsamaisi {
    public static final int bogolo_jwa_tsebe = 4096;

    private static final class tsebe_Boleng {
        private byte[] tshedimosetso = new byte[bogolo_jwa_tsebe];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class aterese_sebaka {
        private final Map<Integer, tsebe_Boleng> tsebe_lenaneothalo = new HashMap<Integer, tsebe_Boleng>();
    }

    public aterese_sebaka 새주소공간() {
        return new aterese_sebaka();
    }

    public void mepa_tsebe(aterese_sebaka 공간, int aterese_ya_kamagano, boolean 쓰기가능) {
        int tshupane = 쪽번호(aterese_ya_kamagano);
        tsebe_Boleng 새쪽 = new tsebe_Boleng();
        새쪽.쓰기가능 = 쓰기가능;
        공간.tsebe_lenaneothalo.put(Integer.valueOf(tshupane), 새쪽);
    }

    public aterese_sebaka 쓰기시복사복제(aterese_sebaka 원본) {
        aterese_sebaka 복제본 = new aterese_sebaka();
        for (Map.Entry<Integer, tsebe_Boleng> tsenyo_Boleng : 원본.tsebe_lenaneothalo.entrySet()) {
            tsebe_Boleng 공유쪽 = tsenyo_Boleng.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.tsebe_lenaneothalo.put(tsenyo_Boleng.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(aterese_sebaka 공간, int aterese_ya_kamagano) {
        tsebe_Boleng setotwa = batla_tsebe(공간, aterese_ya_kamagano);
        return setotwa.tshedimosetso[Math.floorMod(aterese_ya_kamagano, bogolo_jwa_tsebe)];
    }

    public void kwala_baete_Boleng(aterese_sebaka 공간, int aterese_ya_kamagano, byte Boleng) {
        int tshupane = 쪽번호(aterese_ya_kamagano);
        tsebe_Boleng setotwa = batla_tsebe(공간, aterese_ya_kamagano);
        if (!setotwa.쓰기가능) {
            if (!setotwa.쓰기시복사) {
                throw new IllegalStateException("읽기 전용 쪽입니다.");
            }
            setotwa = tlhama_poraefete_tsebe(공간, tshupane, setotwa);
        }
        setotwa.tshedimosetso[Math.floorMod(aterese_ya_kamagano, bogolo_jwa_tsebe)] = Boleng;
    }

    public void 범위개인쓰기(aterese_sebaka 공간, int simolola_aterese, int lekanya) {
        if (lekanya < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int kgaola_aterese = Math.addExact(simolola_aterese, lekanya);
        for (int aterese = simolola_aterese; aterese < kgaola_aterese; aterese = (쪽번호(aterese) + 1) * bogolo_jwa_tsebe) {
            int tshupane = 쪽번호(aterese);
            tsebe_Boleng setotwa = batla_tsebe(공간, aterese);
            if (setotwa.쓰기시복사) {
                tlhama_poraefete_tsebe(공간, tshupane, setotwa);
            } else {
                setotwa.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(aterese_sebaka 공간, int simolola_aterese, byte[] tshedimosetso) {
        for (int tshupane = 0; tshupane < tshedimosetso.length; tshupane++) {
            kwala_baete_Boleng(공간, simolola_aterese + tshupane, tshedimosetso[tshupane]);
        }
    }

    private tsebe_Boleng tlhama_poraefete_tsebe(aterese_sebaka 공간, int tshupane, tsebe_Boleng 공유쪽) {
        tsebe_Boleng poraefete_tsebe = new tsebe_Boleng();
        poraefete_tsebe.tshedimosetso = Arrays.copyOf(공유쪽.tshedimosetso, 공유쪽.tshedimosetso.length);
        poraefete_tsebe.쓰기가능 = true;
        poraefete_tsebe.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.tsebe_lenaneothalo.put(Integer.valueOf(tshupane), poraefete_tsebe);
        return poraefete_tsebe;
    }

    private tsebe_Boleng batla_tsebe(aterese_sebaka 공간, int aterese) {
        tsebe_Boleng setotwa = 공간.tsebe_lenaneothalo.get(Integer.valueOf(쪽번호(aterese)));
        if (setotwa == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return setotwa;
    }

    private int 쪽번호(int aterese) {
        if (aterese < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return aterese / bogolo_jwa_tsebe;
    }
}

