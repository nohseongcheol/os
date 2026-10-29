// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COD.JCodOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB paji_agaciro 연결과 kwandika 시 복사를 제공한다. */
public final class paji_Umugenzuzi {
    public static final int ingano_ya_paji = 4096;

    private static final class paji_agaciro {
        private byte[] amakurushingiro = new byte[ingano_ya_paji];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class aderesi_akanya {
        private final Map<Integer, paji_agaciro> paji_imbonerahamwe = new HashMap<Integer, paji_agaciro>();
    }

    public aderesi_akanya 새주소공간() {
        return new aderesi_akanya();
    }

    public void ikarita_paji(aderesi_akanya 공간, int aderesi_idafatika, boolean 쓰기가능) {
        int umugerekashakiro = 쪽번호(aderesi_idafatika);
        paji_agaciro 새쪽 = new paji_agaciro();
        새쪽.쓰기가능 = 쓰기가능;
        공간.paji_imbonerahamwe.put(Integer.valueOf(umugerekashakiro), 새쪽);
    }

    public aderesi_akanya 쓰기시복사복제(aderesi_akanya 원본) {
        aderesi_akanya 복제본 = new aderesi_akanya();
        for (Map.Entry<Integer, paji_agaciro> icyinjizwa_agaciro : 원본.paji_imbonerahamwe.entrySet()) {
            paji_agaciro 공유쪽 = icyinjizwa_agaciro.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.paji_imbonerahamwe.put(icyinjizwa_agaciro.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(aderesi_akanya 공간, int aderesi_idafatika) {
        paji_agaciro gusimbuza_igishya = gushaka_paji(공간, aderesi_idafatika);
        return gusimbuza_igishya.amakurushingiro[Math.floorMod(aderesi_idafatika, ingano_ya_paji)];
    }

    public void kwandika_bayiti_agaciro(aderesi_akanya 공간, int aderesi_idafatika, byte agaciro) {
        int umugerekashakiro = 쪽번호(aderesi_idafatika);
        paji_agaciro gusimbuza_igishya = gushaka_paji(공간, aderesi_idafatika);
        if (!gusimbuza_igishya.쓰기가능) {
            if (!gusimbuza_igishya.쓰기시복사) {
                throw new IllegalStateException("읽기 전용 쪽입니다.");
            }
            gusimbuza_igishya = kurema_bwite_paji(공간, umugerekashakiro, gusimbuza_igishya);
        }
        gusimbuza_igishya.amakurushingiro[Math.floorMod(aderesi_idafatika, ingano_ya_paji)] = agaciro;
    }

    public void 범위개인쓰기(aderesi_akanya 공간, int Itangira_aderesi, int Ingano) {
        if (Ingano < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int kurangiza_aderesi = Math.addExact(Itangira_aderesi, Ingano);
        for (int aderesi = Itangira_aderesi; aderesi < kurangiza_aderesi; aderesi = (쪽번호(aderesi) + 1) * ingano_ya_paji) {
            int umugerekashakiro = 쪽번호(aderesi);
            paji_agaciro gusimbuza_igishya = gushaka_paji(공간, aderesi);
            if (gusimbuza_igishya.쓰기시복사) {
                kurema_bwite_paji(공간, umugerekashakiro, gusimbuza_igishya);
            } else {
                gusimbuza_igishya.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(aderesi_akanya 공간, int Itangira_aderesi, byte[] amakurushingiro) {
        for (int umugerekashakiro = 0; umugerekashakiro < amakurushingiro.length; umugerekashakiro++) {
            kwandika_bayiti_agaciro(공간, Itangira_aderesi + umugerekashakiro, amakurushingiro[umugerekashakiro]);
        }
    }

    private paji_agaciro kurema_bwite_paji(aderesi_akanya 공간, int umugerekashakiro, paji_agaciro 공유쪽) {
        paji_agaciro bwite_paji = new paji_agaciro();
        bwite_paji.amakurushingiro = Arrays.copyOf(공유쪽.amakurushingiro, 공유쪽.amakurushingiro.length);
        bwite_paji.쓰기가능 = true;
        bwite_paji.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.paji_imbonerahamwe.put(Integer.valueOf(umugerekashakiro), bwite_paji);
        return bwite_paji;
    }

    private paji_agaciro gushaka_paji(aderesi_akanya 공간, int aderesi) {
        paji_agaciro gusimbuza_igishya = 공간.paji_imbonerahamwe.get(Integer.valueOf(쪽번호(aderesi)));
        if (gusimbuza_igishya == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return gusimbuza_igishya;
    }

    private int 쪽번호(int aderesi) {
        if (aderesi < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return aderesi / ingano_ya_paji;
    }
}

