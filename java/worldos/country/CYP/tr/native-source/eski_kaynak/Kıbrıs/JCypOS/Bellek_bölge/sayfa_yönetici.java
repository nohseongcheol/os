// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Kıbrıs.JCypOS.Bellek_bölge;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB sayfa_değer 연결과 Yazma 시 복사를 제공한다. */
public final class sayfa_yönetici {
    public static final int sayfa_boyutu = 4096;

    private static final class sayfa_değer {
        private byte[] veri = new byte[sayfa_boyutu];
        private int Başvuru_BAĞ_DEĞ_SAY = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class adres_alanı {
        private final Map<Integer, sayfa_değer> sayfa_tablo = new HashMap<Integer, sayfa_değer>();
    }

    public adres_alanı 새주소공간() {
        return new adres_alanı();
    }

    public void MAP_sayfa(adres_alanı ADRES_bölge, int sanal_adres, boolean 쓰기가능) {
        int Dizin = 쪽번호(sanal_adres);
        sayfa_değer 새쪽 = new sayfa_değer();
        새쪽.쓰기가능 = 쓰기가능;
        ADRES_bölge.sayfa_tablo.put(Integer.valueOf(Dizin), 새쪽);
    }

    public adres_alanı 쓰기시복사복제(adres_alanı 원본) {
        adres_alanı 복제본 = new adres_alanı();
        for (Map.Entry<Integer, sayfa_değer> girdi_değer : 원본.sayfa_tablo.entrySet()) {
            sayfa_değer Paylaşılan_sayfa = girdi_değer.getValue();
            Paylaşılan_sayfa.Başvuru_BAĞ_DEĞ_SAY++;
            if (Paylaşılan_sayfa.쓰기가능) {
                Paylaşılan_sayfa.쓰기가능 = false;
                Paylaşılan_sayfa.쓰기시복사 = true;
            }
            복제본.sayfa_tablo.put(girdi_değer.getKey(), Paylaşılan_sayfa);
        }
        return 복제본;
    }

    public byte 바이트읽기(adres_alanı ADRES_bölge, int sanal_adres) {
        sayfa_değer hedef = BUL_sayfa(ADRES_bölge, sanal_adres);
        return hedef.veri[Math.floorMod(sanal_adres, sayfa_boyutu)];
    }

    public void yazma_bayt_değer(adres_alanı ADRES_bölge, int sanal_adres, byte değer) {
        int Dizin = 쪽번호(sanal_adres);
        sayfa_değer hedef = BUL_sayfa(ADRES_bölge, sanal_adres);
        if (!hedef.쓰기가능) {
            if (!hedef.쓰기시복사) {
                throw new IllegalStateException("Okuma 전용 쪽입니다.");
            }
            hedef = açmak_Özel_sayfa(ADRES_bölge, Dizin, hedef);
        }
        hedef.veri[Math.floorMod(sanal_adres, sayfa_boyutu)] = değer;
    }

    public void Özel_aralık_yazma(adres_alanı ADRES_bölge, int Start_ADRES, int Boyut) {
        if (Boyut < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int Bitiş_ADRES = Math.addExact(Start_ADRES, Boyut);
        for (int ADRES = Start_ADRES; ADRES < Bitiş_ADRES; ADRES = (쪽번호(ADRES) + 1) * sayfa_boyutu) {
            int Dizin = 쪽번호(ADRES);
            sayfa_değer hedef = BUL_sayfa(ADRES_bölge, ADRES);
            if (hedef.쓰기시복사) {
                açmak_Özel_sayfa(ADRES_bölge, Dizin, hedef);
            } else {
                hedef.쓰기가능 = true;
            }
        }
    }

    public void aralık_yazma(adres_alanı ADRES_bölge, int Start_ADRES, byte[] veri) {
        for (int Dizin = 0; Dizin < veri.length; Dizin++) {
            yazma_bayt_değer(ADRES_bölge, Start_ADRES + Dizin, veri[Dizin]);
        }
    }

    private sayfa_değer açmak_Özel_sayfa(adres_alanı ADRES_bölge, int Dizin, sayfa_değer Paylaşılan_sayfa) {
        sayfa_değer Özel_sayfa = new sayfa_değer();
        Özel_sayfa.veri = Arrays.copyOf(Paylaşılan_sayfa.veri, Paylaşılan_sayfa.veri.length);
        Özel_sayfa.쓰기가능 = true;
        Özel_sayfa.쓰기시복사 = false;
        Paylaşılan_sayfa.Başvuru_BAĞ_DEĞ_SAY--;
        ADRES_bölge.sayfa_tablo.put(Integer.valueOf(Dizin), Özel_sayfa);
        return Özel_sayfa;
    }

    private sayfa_değer BUL_sayfa(adres_alanı ADRES_bölge, int ADRES) {
        sayfa_değer hedef = ADRES_bölge.sayfa_tablo.get(Integer.valueOf(쪽번호(ADRES)));
        if (hedef == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return hedef;
    }

    private int 쪽번호(int ADRES) {
        if (ADRES < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ADRES / sayfa_boyutu;
    }
}

