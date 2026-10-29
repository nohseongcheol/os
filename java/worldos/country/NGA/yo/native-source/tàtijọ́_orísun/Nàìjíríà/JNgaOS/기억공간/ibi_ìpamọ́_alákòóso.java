// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nàìjíríà.JNgaOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 mu_dọ́gba_iye pín_Ibi_ìpamọ́, dápadà_Ibi_ìpamọ́, 병합을 담당한다. */
public final class ibi_ìpamọ́_alákòóso {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public ibi_ìpamọ́_alákòóso(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int pín_Ibi_ìpamọ́(int Ìwọ̀n) {
        return 정렬할당(Ìwọ̀n, 1);
    }

    public synchronized int 정렬할당(int Ìwọ̀n, int mu_dọ́gba_iye) {
        if (Ìwọ̀n <= 0 || mu_dọ́gba_iye <= 0 || (mu_dọ́gba_iye & (mu_dọ́gba_iye - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> ìgbéwọlé_iye : 빈영역.entrySet()) {
            int Rọ́ọ̀nù = ìgbéwọlé_iye.getKey().intValue();
            int 영역크기 = ìgbéwọlé_iye.getValue().intValue();
            int 정렬시작 = (Rọ́ọ̀nù + mu_dọ́gba_iye - 1) & -mu_dọ́gba_iye;
            int 앞크기 = 정렬시작 - Rọ́ọ̀nù;
            int 끝크기 = 영역크기 - 앞크기 - Ìwọ̀n;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Rọ́ọ̀nù));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(Rọ́ọ̀nù), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Ìwọ̀n), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Ìwọ̀n));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Ìwọ̀n, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void dápadà_Ibi_ìpamọ́(int àdírẹ́ẹ̀sì) {
        Integer ìwọn_nǹkan = 사용영역.remove(Integer.valueOf(àdírẹ́ẹ̀sì));
        if (ìwọn_nǹkan == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Rọ́ọ̀nù = àdírẹ́ẹ̀sì;
        int Ìwọ̀n = ìwọn_nǹkan.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(Rọ́ọ̀nù));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == Rọ́ọ̀nù) {
            Rọ́ọ̀nù = 앞.getKey().intValue();
            Ìwọ̀n += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> Padà_sẹ́yìn_iye = 빈영역.ceilingEntry(Integer.valueOf(Rọ́ọ̀nù));
        if (Padà_sẹ́yìn_iye != null && Rọ́ọ̀nù + Ìwọ̀n == Padà_sẹ́yìn_iye.getKey().intValue()) {
            Ìwọ̀n += Padà_sẹ́yìn_iye.getValue().intValue();
            빈영역.remove(Padà_sẹ́yìn_iye.getKey());
        }
        빈영역.put(Integer.valueOf(Rọ́ọ̀nù), Integer.valueOf(Ìwọ̀n));
    }

    public synchronized byte 바이트읽기(int àdírẹ́ẹ̀sì) {
        범위확인(àdírẹ́ẹ̀sì, 1);
        return 기억공간[àdírẹ́ẹ̀sì];
    }

    public synchronized void kọ_báìtì_iye(int àdírẹ́ẹ̀sì, byte iye) {
        범위확인(àdírẹ́ẹ̀sì, 1);
        기억공간[àdírẹ́ẹ̀sì] = iye;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Ìwọ̀n : 사용영역.values()) {
            합계 += Ìwọ̀n.intValue();
        }
        return 합계;
    }

    private void 범위확인(int àdírẹ́ẹ̀sì, int Ìwọ̀n) {
        if (àdírẹ́ẹ̀sì < 0 || Ìwọ̀n < 0 || àdírẹ́ẹ̀sì > 기억공간.length - Ìwọ̀n) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

