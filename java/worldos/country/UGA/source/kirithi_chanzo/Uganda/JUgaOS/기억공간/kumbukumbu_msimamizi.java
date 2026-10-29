// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Uganda.JUgaOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 pangilia_thamani tengea_Hifadhi, toleo_Hifadhi, 병합을 담당한다. */
public final class kumbukumbu_msimamizi {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public kumbukumbu_msimamizi(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int tengea_Hifadhi(int panga_ukubwa) {
        return 정렬할당(panga_ukubwa, 1);
    }

    public synchronized int 정렬할당(int panga_ukubwa, int pangilia_thamani) {
        if (panga_ukubwa <= 0 || pangilia_thamani <= 0 || (pangilia_thamani & (pangilia_thamani - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> ingizo_thamani : 빈영역.entrySet()) {
            int endesha = ingizo_thamani.getKey().intValue();
            int 영역크기 = ingizo_thamani.getValue().intValue();
            int 정렬시작 = (endesha + pangilia_thamani - 1) & -pangilia_thamani;
            int mbele_thamani_panga_ukubwa = 정렬시작 - endesha;
            int 끝크기 = 영역크기 - mbele_thamani_panga_ukubwa - panga_ukubwa;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(endesha));
            if (mbele_thamani_panga_ukubwa > 0) {
                빈영역.put(Integer.valueOf(endesha), Integer.valueOf(mbele_thamani_panga_ukubwa));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + panga_ukubwa), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(panga_ukubwa));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + panga_ukubwa, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void toleo_Hifadhi(int anwani) {
        Integer panga_ukubwa_kipengee = 사용영역.remove(Integer.valueOf(anwani));
        if (panga_ukubwa_kipengee == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int endesha = anwani;
        int panga_ukubwa = panga_ukubwa_kipengee.intValue();
        Map.Entry<Integer, Integer> mbele_thamani = 빈영역.lowerEntry(Integer.valueOf(endesha));
        if (mbele_thamani != null && mbele_thamani.getKey().intValue() + mbele_thamani.getValue().intValue() == endesha) {
            endesha = mbele_thamani.getKey().intValue();
            panga_ukubwa += mbele_thamani.getValue().intValue();
            빈영역.remove(mbele_thamani.getKey());
        }
        Map.Entry<Integer, Integer> Nyuma_thamani = 빈영역.ceilingEntry(Integer.valueOf(endesha));
        if (Nyuma_thamani != null && endesha + panga_ukubwa == Nyuma_thamani.getKey().intValue()) {
            panga_ukubwa += Nyuma_thamani.getValue().intValue();
            빈영역.remove(Nyuma_thamani.getKey());
        }
        빈영역.put(Integer.valueOf(endesha), Integer.valueOf(panga_ukubwa));
    }

    public synchronized byte 바이트읽기(int anwani) {
        범위확인(anwani, 1);
        return 기억공간[anwani];
    }

    public synchronized void andika_baiti_thamani(int anwani, byte thamani) {
        범위확인(anwani, 1);
        기억공간[anwani] = thamani;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer panga_ukubwa : 사용영역.values()) {
            합계 += panga_ukubwa.intValue();
        }
        return 합계;
    }

    private void 범위확인(int anwani, int panga_ukubwa) {
        if (anwani < 0 || panga_ukubwa < 0 || anwani > 기억공간.length - panga_ukubwa) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

