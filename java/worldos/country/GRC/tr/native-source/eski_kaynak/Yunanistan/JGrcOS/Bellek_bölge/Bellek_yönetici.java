// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Yunanistan.JGrcOS.Bellek_bölge;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 hizalamak_değer ayırmak_Depolama, sürüm_Depolama, 병합을 담당한다. */
public final class Bellek_yönetici {
    private final byte[] Bellek_bölge;
    private final TreeMap<Integer, Integer> boş_bölge = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Bellek_yönetici(int toplam_boyutlandırmak) {
        if (toplam_boyutlandırmak < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Bellek_bölge = new byte[toplam_boyutlandırmak];
        boş_bölge.put(Integer.valueOf(4096), Integer.valueOf(toplam_boyutlandırmak - 4096));
    }

    public synchronized int ayırmak_Depolama(int Boyut) {
        return 정렬할당(Boyut, 1);
    }

    public synchronized int 정렬할당(int Boyut, int hizalamak_değer) {
        if (Boyut <= 0 || hizalamak_değer <= 0 || (hizalamak_değer & (hizalamak_değer - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> girdi_değer : boş_bölge.entrySet()) {
            int çalıştır = girdi_değer.getKey().intValue();
            int bölge_boyutlandırmak = girdi_değer.getValue().intValue();
            int 정렬시작 = (çalıştır + hizalamak_değer - 1) & -hizalamak_değer;
            int ön_kamera_değer_boyutlandırmak = 정렬시작 - çalıştır;
            int 끝크기 = bölge_boyutlandırmak - ön_kamera_değer_boyutlandırmak - Boyut;
            if (끝크기 < 0) {
                continue;
            }
            boş_bölge.remove(Integer.valueOf(çalıştır));
            if (ön_kamera_değer_boyutlandırmak > 0) {
                boş_bölge.put(Integer.valueOf(çalıştır), Integer.valueOf(ön_kamera_değer_boyutlandırmak));
            }
            if (끝크기 > 0) {
                boş_bölge.put(Integer.valueOf(정렬시작 + Boyut), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Boyut));
            Arrays.fill(Bellek_bölge, 정렬시작, 정렬시작 + Boyut, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void sürüm_Depolama(int ADRES) {
        Integer boyutlandırmak_nesne = 사용영역.remove(Integer.valueOf(ADRES));
        if (boyutlandırmak_nesne == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int çalıştır = ADRES;
        int Boyut = boyutlandırmak_nesne.intValue();
        Map.Entry<Integer, Integer> ön_kamera_değer = boş_bölge.lowerEntry(Integer.valueOf(çalıştır));
        if (ön_kamera_değer != null && ön_kamera_değer.getKey().intValue() + ön_kamera_değer.getValue().intValue() == çalıştır) {
            çalıştır = ön_kamera_değer.getKey().intValue();
            Boyut += ön_kamera_değer.getValue().intValue();
            boş_bölge.remove(ön_kamera_değer.getKey());
        }
        Map.Entry<Integer, Integer> BACK_değer = boş_bölge.ceilingEntry(Integer.valueOf(çalıştır));
        if (BACK_değer != null && çalıştır + Boyut == BACK_değer.getKey().intValue()) {
            Boyut += BACK_değer.getValue().intValue();
            boş_bölge.remove(BACK_değer.getKey());
        }
        boş_bölge.put(Integer.valueOf(çalıştır), Integer.valueOf(Boyut));
    }

    public synchronized byte 바이트읽기(int ADRES) {
        çek_aralık(ADRES, 1);
        return Bellek_bölge[ADRES];
    }

    public synchronized void yazma_bayt_değer(int ADRES, byte değer) {
        çek_aralık(ADRES, 1);
        Bellek_bölge[ADRES] = değer;
    }

    public synchronized int toplam_boyutlandırmak() {
        return Bellek_bölge.length;
    }

    public synchronized int 사용크기() {
        int toplam_değer = 0;
        for (Integer Boyut : 사용영역.values()) {
            toplam_değer += Boyut.intValue();
        }
        return toplam_değer;
    }

    private void çek_aralık(int ADRES, int Boyut) {
        if (ADRES < 0 || Boyut < 0 || ADRES > Bellek_bölge.length - Boyut) {
            throw new IndexOutOfBoundsException("Bellek_bölge 범위를 벗어났습니다.");
        }
    }
}

