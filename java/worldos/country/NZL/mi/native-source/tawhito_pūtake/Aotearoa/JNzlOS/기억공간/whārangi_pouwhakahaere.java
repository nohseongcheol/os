// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aotearoa.JNzlOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB whārangi_uara 연결과 Tuhia 시 복사를 제공한다. */
public final class whārangi_pouwhakahaere {
    public static final int rahinga_whārangi = 4096;

    private static final class whārangi_uara {
        private byte[] raraunga = new byte[rahinga_whārangi];
        private int Pūranga_kōrero_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ADDRESS_wāhi {
        private final Map<Integer, whārangi_uara> whārangi_ripanga = new HashMap<Integer, whārangi_uara>();
    }

    public ADDRESS_wāhi 새주소공간() {
        return new ADDRESS_wāhi();
    }

    public void MAPI_whārangi(ADDRESS_wāhi 공간, int wāhitau_mariko, boolean 쓰기가능) {
        int INDEX = 쪽번호(wāhitau_mariko);
        whārangi_uara 새쪽 = new whārangi_uara();
        새쪽.쓰기가능 = 쓰기가능;
        공간.whārangi_ripanga.put(Integer.valueOf(INDEX), 새쪽);
    }

    public ADDRESS_wāhi 쓰기시복사복제(ADDRESS_wāhi 원본) {
        ADDRESS_wāhi 복제본 = new ADDRESS_wāhi();
        for (Map.Entry<Integer, whārangi_uara> tāurunga_uara : 원본.whārangi_ripanga.entrySet()) {
            whārangi_uara 공유쪽 = tāurunga_uara.getValue();
            공유쪽.Pūranga_kōrero_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.whārangi_ripanga.put(tāurunga_uara.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(ADDRESS_wāhi 공간, int wāhitau_mariko) {
        whārangi_uara ūnga = FIND_whārangi(공간, wāhitau_mariko);
        return ūnga.raraunga[Math.floorMod(wāhitau_mariko, rahinga_whārangi)];
    }

    public void tuhi_paita_uara(ADDRESS_wāhi 공간, int wāhitau_mariko, byte uara) {
        int INDEX = 쪽번호(wāhitau_mariko);
        whārangi_uara ūnga = FIND_whārangi(공간, wāhitau_mariko);
        if (!ūnga.쓰기가능) {
            if (!ūnga.쓰기시복사) {
                throw new IllegalStateException("Pānuitia 전용 쪽입니다.");
            }
            ūnga = Waihanga_tūmataiti_whārangi(공간, INDEX, ūnga);
        }
        ūnga.raraunga[Math.floorMod(wāhitau_mariko, rahinga_whārangi)] = uara;
    }

    public void 범위개인쓰기(ADDRESS_wāhi 공간, int Start_ADDRESS, int rahi) {
        if (rahi < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int mutu_ADDRESS = Math.addExact(Start_ADDRESS, rahi);
        for (int ADDRESS = Start_ADDRESS; ADDRESS < mutu_ADDRESS; ADDRESS = (쪽번호(ADDRESS) + 1) * rahinga_whārangi) {
            int INDEX = 쪽번호(ADDRESS);
            whārangi_uara ūnga = FIND_whārangi(공간, ADDRESS);
            if (ūnga.쓰기시복사) {
                Waihanga_tūmataiti_whārangi(공간, INDEX, ūnga);
            } else {
                ūnga.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(ADDRESS_wāhi 공간, int Start_ADDRESS, byte[] raraunga) {
        for (int INDEX = 0; INDEX < raraunga.length; INDEX++) {
            tuhi_paita_uara(공간, Start_ADDRESS + INDEX, raraunga[INDEX]);
        }
    }

    private whārangi_uara Waihanga_tūmataiti_whārangi(ADDRESS_wāhi 공간, int INDEX, whārangi_uara 공유쪽) {
        whārangi_uara tūmataiti_whārangi = new whārangi_uara();
        tūmataiti_whārangi.raraunga = Arrays.copyOf(공유쪽.raraunga, 공유쪽.raraunga.length);
        tūmataiti_whārangi.쓰기가능 = true;
        tūmataiti_whārangi.쓰기시복사 = false;
        공유쪽.Pūranga_kōrero_COUNT--;
        공간.whārangi_ripanga.put(Integer.valueOf(INDEX), tūmataiti_whārangi);
        return tūmataiti_whārangi;
    }

    private whārangi_uara FIND_whārangi(ADDRESS_wāhi 공간, int ADDRESS) {
        whārangi_uara ūnga = 공간.whārangi_ripanga.get(Integer.valueOf(쪽번호(ADDRESS)));
        if (ūnga == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return ūnga;
    }

    private int 쪽번호(int ADDRESS) {
        if (ADDRESS < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ADDRESS / rahinga_whārangi;
    }
}

