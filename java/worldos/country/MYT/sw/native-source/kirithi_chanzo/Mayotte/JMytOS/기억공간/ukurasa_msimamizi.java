// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Mayotte.JMytOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB ukurasa_thamani 연결과 andika 시 복사를 제공한다. */
public final class ukurasa_msimamizi {
    public static final int ukubwa_wa_ukurasa = 4096;

    private static final class ukurasa_thamani {
        private byte[] data = new byte[ukubwa_wa_ukurasa];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class anwani_eneo {
        private final Map<Integer, ukurasa_thamani> ukurasa_jedwali = new HashMap<Integer, ukurasa_thamani>();
    }

    public anwani_eneo 새주소공간() {
        return new anwani_eneo();
    }

    public void ramani_ukurasa(anwani_eneo 공간, int anwani_sibayana, boolean 쓰기가능) {
        int kielezo = 쪽번호(anwani_sibayana);
        ukurasa_thamani 새쪽 = new ukurasa_thamani();
        새쪽.쓰기가능 = 쓰기가능;
        공간.ukurasa_jedwali.put(Integer.valueOf(kielezo), 새쪽);
    }

    public anwani_eneo 쓰기시복사복제(anwani_eneo 원본) {
        anwani_eneo 복제본 = new anwani_eneo();
        for (Map.Entry<Integer, ukurasa_thamani> ingizo_thamani : 원본.ukurasa_jedwali.entrySet()) {
            ukurasa_thamani 공유쪽 = ingizo_thamani.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.ukurasa_jedwali.put(ingizo_thamani.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(anwani_eneo 공간, int anwani_sibayana) {
        ukurasa_thamani lengo = gundua_ukurasa(공간, anwani_sibayana);
        return lengo.data[Math.floorMod(anwani_sibayana, ukubwa_wa_ukurasa)];
    }

    public void andika_baiti_thamani(anwani_eneo 공간, int anwani_sibayana, byte thamani) {
        int kielezo = 쪽번호(anwani_sibayana);
        ukurasa_thamani lengo = gundua_ukurasa(공간, anwani_sibayana);
        if (!lengo.쓰기가능) {
            if (!lengo.쓰기시복사) {
                throw new IllegalStateException("읽기 전용 쪽입니다.");
            }
            lengo = unda_Binafsi_ukurasa(공간, kielezo, lengo);
        }
        lengo.data[Math.floorMod(anwani_sibayana, ukubwa_wa_ukurasa)] = thamani;
    }

    public void 범위개인쓰기(anwani_eneo 공간, int Anza_anwani, int panga_ukubwa) {
        if (panga_ukubwa < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int tamatia_anwani = Math.addExact(Anza_anwani, panga_ukubwa);
        for (int anwani = Anza_anwani; anwani < tamatia_anwani; anwani = (쪽번호(anwani) + 1) * ukubwa_wa_ukurasa) {
            int kielezo = 쪽번호(anwani);
            ukurasa_thamani lengo = gundua_ukurasa(공간, anwani);
            if (lengo.쓰기시복사) {
                unda_Binafsi_ukurasa(공간, kielezo, lengo);
            } else {
                lengo.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(anwani_eneo 공간, int Anza_anwani, byte[] data) {
        for (int kielezo = 0; kielezo < data.length; kielezo++) {
            andika_baiti_thamani(공간, Anza_anwani + kielezo, data[kielezo]);
        }
    }

    private ukurasa_thamani unda_Binafsi_ukurasa(anwani_eneo 공간, int kielezo, ukurasa_thamani 공유쪽) {
        ukurasa_thamani Binafsi_ukurasa = new ukurasa_thamani();
        Binafsi_ukurasa.data = Arrays.copyOf(공유쪽.data, 공유쪽.data.length);
        Binafsi_ukurasa.쓰기가능 = true;
        Binafsi_ukurasa.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.ukurasa_jedwali.put(Integer.valueOf(kielezo), Binafsi_ukurasa);
        return Binafsi_ukurasa;
    }

    private ukurasa_thamani gundua_ukurasa(anwani_eneo 공간, int anwani) {
        ukurasa_thamani lengo = 공간.ukurasa_jedwali.get(Integer.valueOf(쪽번호(anwani)));
        if (lengo == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return lengo;
    }

    private int 쪽번호(int anwani) {
        if (anwani < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return anwani / ukubwa_wa_ukurasa;
    }
}

