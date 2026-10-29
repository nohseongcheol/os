// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Viro.JEstOS.Muisti_alue;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB page_ARVO 연결과 Kirjoitus 시 복사를 제공한다. */
public final class page_Valvoja {
    public static final int sivukoko = 4096;

    private static final class page_ARVO {
        private byte[] data = new byte[sivukoko];
        private int viite_LASKE = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class osoiteavaruus {
        private final Map<Integer, page_ARVO> page_taulukko = new HashMap<Integer, page_ARVO>();
    }

    public osoiteavaruus 새주소공간() {
        return new osoiteavaruus();
    }

    public void MAP_page(osoiteavaruus OSOITE_alue, int näennäisosoite, boolean 쓰기가능) {
        int INDEKSI = page_numero(näennäisosoite);
        page_ARVO 새쪽 = new page_ARVO();
        새쪽.쓰기가능 = 쓰기가능;
        OSOITE_alue.page_taulukko.put(Integer.valueOf(INDEKSI), 새쪽);
    }

    public osoiteavaruus 쓰기시복사복제(osoiteavaruus 원본) {
        osoiteavaruus 복제본 = new osoiteavaruus();
        for (Map.Entry<Integer, page_ARVO> merkintä_ARVO_962f286b : 원본.page_taulukko.entrySet()) {
            page_ARVO 공유쪽 = merkintä_ARVO_962f286b.getValue();
            공유쪽.viite_LASKE++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.page_taulukko.put(merkintä_ARVO_962f286b.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte lukea_tavu_ARVO(osoiteavaruus OSOITE_alue, int näennäisosoite) {
        page_ARVO tavoite = ETSI_page(OSOITE_alue, näennäisosoite);
        return tavoite.data[Math.floorMod(näennäisosoite, sivukoko)];
    }

    public void kirjoitus_tavu_ARVO(osoiteavaruus OSOITE_alue, int näennäisosoite, byte ARVO) {
        int INDEKSI = page_numero(näennäisosoite);
        page_ARVO tavoite = ETSI_page(OSOITE_alue, näennäisosoite);
        if (!tavoite.쓰기가능) {
            if (!tavoite.쓰기시복사) {
                throw new IllegalStateException("Luku 전용 쪽입니다.");
            }
            tavoite = Luo_Yksityinen_page(OSOITE_alue, INDEKSI, tavoite);
        }
        tavoite.data[Math.floorMod(näennäisosoite, sivukoko)] = ARVO;
    }

    public void Yksityinen_alue_kirjoitus(osoiteavaruus OSOITE_alue, int alku_OSOITE, int Koko) {
        if (Koko < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int lopettaa_puhelu_OSOITE = Math.addExact(alku_OSOITE, Koko);
        for (int OSOITE = alku_OSOITE; OSOITE < lopettaa_puhelu_OSOITE; OSOITE = (page_numero(OSOITE) + 1) * sivukoko) {
            int INDEKSI = page_numero(OSOITE);
            page_ARVO tavoite = ETSI_page(OSOITE_alue, OSOITE);
            if (tavoite.쓰기시복사) {
                Luo_Yksityinen_page(OSOITE_alue, INDEKSI, tavoite);
            } else {
                tavoite.쓰기가능 = true;
            }
        }
    }

    public void alue_kirjoitus(osoiteavaruus OSOITE_alue, int alku_OSOITE, byte[] data) {
        for (int INDEKSI = 0; INDEKSI < data.length; INDEKSI++) {
            kirjoitus_tavu_ARVO(OSOITE_alue, alku_OSOITE + INDEKSI, data[INDEKSI]);
        }
    }

    private page_ARVO Luo_Yksityinen_page(osoiteavaruus OSOITE_alue, int INDEKSI, page_ARVO 공유쪽) {
        page_ARVO Yksityinen_page = new page_ARVO();
        Yksityinen_page.data = Arrays.copyOf(공유쪽.data, 공유쪽.data.length);
        Yksityinen_page.쓰기가능 = true;
        Yksityinen_page.쓰기시복사 = false;
        공유쪽.viite_LASKE--;
        OSOITE_alue.page_taulukko.put(Integer.valueOf(INDEKSI), Yksityinen_page);
        return Yksityinen_page;
    }

    private page_ARVO ETSI_page(osoiteavaruus OSOITE_alue, int OSOITE) {
        page_ARVO tavoite = OSOITE_alue.page_taulukko.get(Integer.valueOf(page_numero(OSOITE)));
        if (tavoite == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return tavoite;
    }

    private int page_numero(int OSOITE) {
        if (OSOITE < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return OSOITE / sivukoko;
    }
}

