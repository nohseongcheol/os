// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espainia.JEspOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB orri_balio 연결과 Idatzi 시 복사를 제공한다. */
public final class orri_kudeatzaile {
    public static final int orrialdearen_tamaina = 4096;

    private static final class orri_balio {
        private byte[] datuak = new byte[orrialdearen_tamaina];
        private int Erreferentzia_materiala_ZENBATU = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class helbide_gune {
        private final Map<Integer, orri_balio> orri_taula = new HashMap<Integer, orri_balio>();
    }

    public helbide_gune 새주소공간() {
        return new helbide_gune();
    }

    public void MAP_orri(helbide_gune 공간, int helbide_birtual, boolean 쓰기가능) {
        int INDIZE = 쪽번호(helbide_birtual);
        orri_balio 새쪽 = new orri_balio();
        새쪽.쓰기가능 = 쓰기가능;
        공간.orri_taula.put(Integer.valueOf(INDIZE), 새쪽);
    }

    public helbide_gune 쓰기시복사복제(helbide_gune 원본) {
        helbide_gune 복제본 = new helbide_gune();
        for (Map.Entry<Integer, orri_balio> sarrera_balio : 원본.orri_taula.entrySet()) {
            orri_balio 공유쪽 = sarrera_balio.getValue();
            공유쪽.Erreferentzia_materiala_ZENBATU++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.orri_taula.put(sarrera_balio.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(helbide_gune 공간, int helbide_birtual) {
        orri_balio helburu_balio = Bilatu_orri(공간, helbide_birtual);
        return helburu_balio.datuak[Math.floorMod(helbide_birtual, orrialdearen_tamaina)];
    }

    public void idatzi_byte_balio(helbide_gune 공간, int helbide_birtual, byte balio) {
        int INDIZE = 쪽번호(helbide_birtual);
        orri_balio helburu_balio = Bilatu_orri(공간, helbide_birtual);
        if (!helburu_balio.쓰기가능) {
            if (!helburu_balio.쓰기시복사) {
                throw new IllegalStateException("Irakurri 전용 쪽입니다.");
            }
            helburu_balio = sortu_Pribatu_orri(공간, INDIZE, helburu_balio);
        }
        helburu_balio.datuak[Math.floorMod(helbide_birtual, orrialdearen_tamaina)] = balio;
    }

    public void Pribatu_barruti_idatzi(helbide_gune 공간, int HASI_helbide, int Tamaina) {
        if (Tamaina < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int amaitu_helbide = Math.addExact(HASI_helbide, Tamaina);
        for (int helbide = HASI_helbide; helbide < amaitu_helbide; helbide = (쪽번호(helbide) + 1) * orrialdearen_tamaina) {
            int INDIZE = 쪽번호(helbide);
            orri_balio helburu_balio = Bilatu_orri(공간, helbide);
            if (helburu_balio.쓰기시복사) {
                sortu_Pribatu_orri(공간, INDIZE, helburu_balio);
            } else {
                helburu_balio.쓰기가능 = true;
            }
        }
    }

    public void barruti_idatzi(helbide_gune 공간, int HASI_helbide, byte[] datuak) {
        for (int INDIZE = 0; INDIZE < datuak.length; INDIZE++) {
            idatzi_byte_balio(공간, HASI_helbide + INDIZE, datuak[INDIZE]);
        }
    }

    private orri_balio sortu_Pribatu_orri(helbide_gune 공간, int INDIZE, orri_balio 공유쪽) {
        orri_balio Pribatu_orri = new orri_balio();
        Pribatu_orri.datuak = Arrays.copyOf(공유쪽.datuak, 공유쪽.datuak.length);
        Pribatu_orri.쓰기가능 = true;
        Pribatu_orri.쓰기시복사 = false;
        공유쪽.Erreferentzia_materiala_ZENBATU--;
        공간.orri_taula.put(Integer.valueOf(INDIZE), Pribatu_orri);
        return Pribatu_orri;
    }

    private orri_balio Bilatu_orri(helbide_gune 공간, int helbide) {
        orri_balio helburu_balio = 공간.orri_taula.get(Integer.valueOf(쪽번호(helbide)));
        if (helburu_balio == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return helburu_balio;
    }

    private int 쪽번호(int helbide) {
        if (helbide < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return helbide / orrialdearen_tamaina;
    }
}

