// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package An_Rìoghachd_Aonaichte.JGbrOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB duilleag_VALUE 연결과 sgrìobh 시 복사를 제공한다. */
public final class duilleag_manaidsear {
    public static final int meud_na_duilleige = 4096;

    private static final class duilleag_VALUE {
        private byte[] dàta = new byte[meud_na_duilleige];
        private int fiosrachadh_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ADDRESS_spàs {
        private final Map<Integer, duilleag_VALUE> duilleag_clàr = new HashMap<Integer, duilleag_VALUE>();
    }

    public ADDRESS_spàs 새주소공간() {
        return new ADDRESS_spàs();
    }

    public void MAP_duilleag(ADDRESS_spàs 공간, int mas_fhìor_ADDRESS, boolean 쓰기가능) {
        int INDEX = 쪽번호(mas_fhìor_ADDRESS);
        duilleag_VALUE 새쪽 = new duilleag_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        공간.duilleag_clàr.put(Integer.valueOf(INDEX), 새쪽);
    }

    public ADDRESS_spàs 쓰기시복사복제(ADDRESS_spàs 원본) {
        ADDRESS_spàs 복제본 = new ADDRESS_spàs();
        for (Map.Entry<Integer, duilleag_VALUE> cur_a_steach_VALUE : 원본.duilleag_clàr.entrySet()) {
            duilleag_VALUE 공유쪽 = cur_a_steach_VALUE.getValue();
            공유쪽.fiosrachadh_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.duilleag_clàr.put(cur_a_steach_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(ADDRESS_spàs 공간, int mas_fhìor_ADDRESS) {
        duilleag_VALUE targaid = FIND_duilleag(공간, mas_fhìor_ADDRESS);
        return targaid.dàta[Math.floorMod(mas_fhìor_ADDRESS, meud_na_duilleige)];
    }

    public void sgrìobh_baidht_VALUE(ADDRESS_spàs 공간, int mas_fhìor_ADDRESS, byte VALUE) {
        int INDEX = 쪽번호(mas_fhìor_ADDRESS);
        duilleag_VALUE targaid = FIND_duilleag(공간, mas_fhìor_ADDRESS);
        if (!targaid.쓰기가능) {
            if (!targaid.쓰기시복사) {
                throw new IllegalStateException("읽기 전용 쪽입니다.");
            }
            targaid = Create_prìobhaideach_duilleag(공간, INDEX, targaid);
        }
        targaid.dàta[Math.floorMod(mas_fhìor_ADDRESS, meud_na_duilleige)] = VALUE;
    }

    public void 범위개인쓰기(ADDRESS_spàs 공간, int Start_ADDRESS, int atharraich_am_meud) {
        if (atharraich_am_meud < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int crìochnaich_ADDRESS = Math.addExact(Start_ADDRESS, atharraich_am_meud);
        for (int ADDRESS = Start_ADDRESS; ADDRESS < crìochnaich_ADDRESS; ADDRESS = (쪽번호(ADDRESS) + 1) * meud_na_duilleige) {
            int INDEX = 쪽번호(ADDRESS);
            duilleag_VALUE targaid = FIND_duilleag(공간, ADDRESS);
            if (targaid.쓰기시복사) {
                Create_prìobhaideach_duilleag(공간, INDEX, targaid);
            } else {
                targaid.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(ADDRESS_spàs 공간, int Start_ADDRESS, byte[] dàta) {
        for (int INDEX = 0; INDEX < dàta.length; INDEX++) {
            sgrìobh_baidht_VALUE(공간, Start_ADDRESS + INDEX, dàta[INDEX]);
        }
    }

    private duilleag_VALUE Create_prìobhaideach_duilleag(ADDRESS_spàs 공간, int INDEX, duilleag_VALUE 공유쪽) {
        duilleag_VALUE prìobhaideach_duilleag = new duilleag_VALUE();
        prìobhaideach_duilleag.dàta = Arrays.copyOf(공유쪽.dàta, 공유쪽.dàta.length);
        prìobhaideach_duilleag.쓰기가능 = true;
        prìobhaideach_duilleag.쓰기시복사 = false;
        공유쪽.fiosrachadh_COUNT--;
        공간.duilleag_clàr.put(Integer.valueOf(INDEX), prìobhaideach_duilleag);
        return prìobhaideach_duilleag;
    }

    private duilleag_VALUE FIND_duilleag(ADDRESS_spàs 공간, int ADDRESS) {
        duilleag_VALUE targaid = 공간.duilleag_clàr.get(Integer.valueOf(쪽번호(ADDRESS)));
        if (targaid == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return targaid;
    }

    private int 쪽번호(int ADDRESS) {
        if (ADDRESS < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ADDRESS / meud_na_duilleige;
    }
}

