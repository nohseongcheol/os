// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package iMalawi.JMwiOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB ikhasi_inani 연결과 Bhala 시 복사를 제공한다. */
public final class ikhasi_imeneja {
    public static final int ubungako_bekhasi = 4096;

    private static final class ikhasi_inani {
        private byte[] imininingwane = new byte[ubungako_bekhasi];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ikheli_indawo {
        private final Map<Integer, ikhasi_inani> ikhasi_ithebula = new HashMap<Integer, ikhasi_inani>();
    }

    public ikheli_indawo 새주소공간() {
        return new ikheli_indawo();
    }

    public void faka_kumephu_ikhasi(ikheli_indawo 공간, int ikheli_talagu, boolean 쓰기가능) {
        int thola_inkomba = 쪽번호(ikheli_talagu);
        ikhasi_inani 새쪽 = new ikhasi_inani();
        새쪽.쓰기가능 = 쓰기가능;
        공간.ikhasi_ithebula.put(Integer.valueOf(thola_inkomba), 새쪽);
    }

    public ikheli_indawo 쓰기시복사복제(ikheli_indawo 원본) {
        ikheli_indawo 복제본 = new ikheli_indawo();
        for (Map.Entry<Integer, ikhasi_inani> okufakwayo_inani : 원본.ikhasi_ithebula.entrySet()) {
            ikhasi_inani 공유쪽 = okufakwayo_inani.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.ikhasi_ithebula.put(okufakwayo_inani.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(ikheli_indawo 공간, int ikheli_talagu) {
        ikhasi_inani impokophelo = thola_ikhasi(공간, ikheli_talagu);
        return impokophelo.imininingwane[Math.floorMod(ikheli_talagu, ubungako_bekhasi)];
    }

    public void bhala_ibhayithi_inani(ikheli_indawo 공간, int ikheli_talagu, byte inani) {
        int thola_inkomba = 쪽번호(ikheli_talagu);
        ikhasi_inani impokophelo = thola_ikhasi(공간, ikheli_talagu);
        if (!impokophelo.쓰기가능) {
            if (!impokophelo.쓰기시복사) {
                throw new IllegalStateException("Funda 전용 쪽입니다.");
            }
            impokophelo = yakha_okomnikazi_kuphela_ikhasi(공간, thola_inkomba, impokophelo);
        }
        impokophelo.imininingwane[Math.floorMod(ikheli_talagu, ubungako_bekhasi)] = inani;
    }

    public void 범위개인쓰기(ikheli_indawo 공간, int qala_ikheli, int Ubungako) {
        if (Ubungako < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int yekisa_ikheli = Math.addExact(qala_ikheli, Ubungako);
        for (int ikheli = qala_ikheli; ikheli < yekisa_ikheli; ikheli = (쪽번호(ikheli) + 1) * ubungako_bekhasi) {
            int thola_inkomba = 쪽번호(ikheli);
            ikhasi_inani impokophelo = thola_ikhasi(공간, ikheli);
            if (impokophelo.쓰기시복사) {
                yakha_okomnikazi_kuphela_ikhasi(공간, thola_inkomba, impokophelo);
            } else {
                impokophelo.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(ikheli_indawo 공간, int qala_ikheli, byte[] imininingwane) {
        for (int thola_inkomba = 0; thola_inkomba < imininingwane.length; thola_inkomba++) {
            bhala_ibhayithi_inani(공간, qala_ikheli + thola_inkomba, imininingwane[thola_inkomba]);
        }
    }

    private ikhasi_inani yakha_okomnikazi_kuphela_ikhasi(ikheli_indawo 공간, int thola_inkomba, ikhasi_inani 공유쪽) {
        ikhasi_inani okomnikazi_kuphela_ikhasi = new ikhasi_inani();
        okomnikazi_kuphela_ikhasi.imininingwane = Arrays.copyOf(공유쪽.imininingwane, 공유쪽.imininingwane.length);
        okomnikazi_kuphela_ikhasi.쓰기가능 = true;
        okomnikazi_kuphela_ikhasi.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.ikhasi_ithebula.put(Integer.valueOf(thola_inkomba), okomnikazi_kuphela_ikhasi);
        return okomnikazi_kuphela_ikhasi;
    }

    private ikhasi_inani thola_ikhasi(ikheli_indawo 공간, int ikheli) {
        ikhasi_inani impokophelo = 공간.ikhasi_ithebula.get(Integer.valueOf(쪽번호(ikheli)));
        if (impokophelo == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return impokophelo;
    }

    private int 쪽번호(int ikheli) {
        if (ikheli < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ikheli / ubungako_bekhasi;
    }
}

