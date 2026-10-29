// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Shqipëri.JAlbOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 drejtvendos_VALUE caktoj_hapësira_ruajtëse, liroj_hapësira_ruajtëse, 병합을 담당한다. */
public final class Memorie_menaxher {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Memorie_menaxher(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int caktoj_hapësira_ruajtëse(int Madhësi) {
        return 정렬할당(Madhësi, 1);
    }

    public synchronized int 정렬할당(int Madhësi, int drejtvendos_VALUE) {
        if (Madhësi <= 0 || drejtvendos_VALUE <= 0 || (drejtvendos_VALUE & (drejtvendos_VALUE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> futje_VALUE : 빈영역.entrySet()) {
            int Ekzekuto = futje_VALUE.getKey().intValue();
            int 영역크기 = futje_VALUE.getValue().intValue();
            int 정렬시작 = (Ekzekuto + drejtvendos_VALUE - 1) & -drejtvendos_VALUE;
            int e_përparme_VALUE_ndryshoj_përmasat = 정렬시작 - Ekzekuto;
            int 끝크기 = 영역크기 - e_përparme_VALUE_ndryshoj_përmasat - Madhësi;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Ekzekuto));
            if (e_përparme_VALUE_ndryshoj_përmasat > 0) {
                빈영역.put(Integer.valueOf(Ekzekuto), Integer.valueOf(e_përparme_VALUE_ndryshoj_përmasat));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Madhësi), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Madhësi));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Madhësi, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void liroj_hapësira_ruajtëse(int email) {
        Integer ndryshoj_përmasat_objekt = 사용영역.remove(Integer.valueOf(email));
        if (ndryshoj_përmasat_objekt == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Ekzekuto = email;
        int Madhësi = ndryshoj_përmasat_objekt.intValue();
        Map.Entry<Integer, Integer> e_përparme_VALUE = 빈영역.lowerEntry(Integer.valueOf(Ekzekuto));
        if (e_përparme_VALUE != null && e_përparme_VALUE.getKey().intValue() + e_përparme_VALUE.getValue().intValue() == Ekzekuto) {
            Ekzekuto = e_përparme_VALUE.getKey().intValue();
            Madhësi += e_përparme_VALUE.getValue().intValue();
            빈영역.remove(e_përparme_VALUE.getKey());
        }
        Map.Entry<Integer, Integer> PAS_VALUE = 빈영역.ceilingEntry(Integer.valueOf(Ekzekuto));
        if (PAS_VALUE != null && Ekzekuto + Madhësi == PAS_VALUE.getKey().intValue()) {
            Madhësi += PAS_VALUE.getValue().intValue();
            빈영역.remove(PAS_VALUE.getKey());
        }
        빈영역.put(Integer.valueOf(Ekzekuto), Integer.valueOf(Madhësi));
    }

    public synchronized byte 바이트읽기(int email) {
        범위확인(email, 1);
        return 기억공간[email];
    }

    public synchronized void shkruaj_bajt_VALUE(int email, byte VALUE) {
        범위확인(email, 1);
        기억공간[email] = VALUE;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Madhësi : 사용영역.values()) {
            합계 += Madhësi.intValue();
        }
        return 합계;
    }

    private void 범위확인(int email, int Madhësi) {
        if (email < 0 || Madhësi < 0 || email > 기억공간.length - Madhësi) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

