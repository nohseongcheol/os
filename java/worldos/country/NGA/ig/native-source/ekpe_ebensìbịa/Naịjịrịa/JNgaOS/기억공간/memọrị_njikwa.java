// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Naịjịrịa.JNgaOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 hàkọma_valuu kepụta_Nchekwa, bupute_Nchekwa, 병합을 담당한다. */
public final class memọrị_njikwa {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public memọrị_njikwa(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int kepụta_Nchekwa(int Ụhara) {
        return 정렬할당(Ụhara, 1);
    }

    public synchronized int 정렬할당(int Ụhara, int hàkọma_valuu) {
        if (Ụhara <= 0 || hàkọma_valuu <= 0 || (hàkọma_valuu & (hàkọma_valuu - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> ndebà_valuu : 빈영역.entrySet()) {
            int Bido = ndebà_valuu.getKey().intValue();
            int 영역크기 = ndebà_valuu.getValue().intValue();
            int 정렬시작 = (Bido + hàkọma_valuu - 1) & -hàkọma_valuu;
            int 앞크기 = 정렬시작 - Bido;
            int 끝크기 = 영역크기 - 앞크기 - Ụhara;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Bido));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(Bido), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Ụhara), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Ụhara));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Ụhara, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void bupute_Nchekwa(int àdreèsì) {
        Integer ụha_ihe = 사용영역.remove(Integer.valueOf(àdreèsì));
        if (ụha_ihe == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Bido = àdreèsì;
        int Ụhara = ụha_ihe.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(Bido));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == Bido) {
            Bido = 앞.getKey().intValue();
            Ụhara += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> Àzụ_valuu = 빈영역.ceilingEntry(Integer.valueOf(Bido));
        if (Àzụ_valuu != null && Bido + Ụhara == Àzụ_valuu.getKey().intValue()) {
            Ụhara += Àzụ_valuu.getValue().intValue();
            빈영역.remove(Àzụ_valuu.getKey());
        }
        빈영역.put(Integer.valueOf(Bido), Integer.valueOf(Ụhara));
    }

    public synchronized byte 바이트읽기(int àdreèsì) {
        범위확인(àdreèsì, 1);
        return 기억공간[àdreèsì];
    }

    public synchronized void dee_baịtị_valuu(int àdreèsì, byte valuu) {
        범위확인(àdreèsì, 1);
        기억공간[àdreèsì] = valuu;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Ụhara : 사용영역.values()) {
            합계 += Ụhara.intValue();
        }
        return 합계;
    }

    private void 범위확인(int àdreèsì, int Ụhara) {
        if (àdreèsì < 0 || Ụhara < 0 || àdreèsì > 기억공간.length - Ụhara) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

