// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Norge.JNorOS.Minne_område;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 justere_VERDI tildele_lager, frigi_lager, 병합을 담당한다. */
public final class Minne_overordnet {
    private final byte[] Minne_område;
    private final TreeMap<Integer, Integer> tom_område = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Minne_overordnet(int total_skalere) {
        if (total_skalere < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Minne_område = new byte[total_skalere];
        tom_område.put(Integer.valueOf(4096), Integer.valueOf(total_skalere - 4096));
    }

    public synchronized int tildele_lager(int Størrelse) {
        return 정렬할당(Størrelse, 1);
    }

    public synchronized int 정렬할당(int Størrelse, int justere_VERDI) {
        if (Størrelse <= 0 || justere_VERDI <= 0 || (justere_VERDI & (justere_VERDI - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> oppføring_VERDI : tom_område.entrySet()) {
            int Kjør_2 = oppføring_VERDI.getKey().intValue();
            int område_skalere = oppføring_VERDI.getValue().intValue();
            int 정렬시작 = (Kjør_2 + justere_VERDI - 1) & -justere_VERDI;
            int frontkamera_VERDI_skalere = 정렬시작 - Kjør_2;
            int 끝크기 = område_skalere - frontkamera_VERDI_skalere - Størrelse;
            if (끝크기 < 0) {
                continue;
            }
            tom_område.remove(Integer.valueOf(Kjør_2));
            if (frontkamera_VERDI_skalere > 0) {
                tom_område.put(Integer.valueOf(Kjør_2), Integer.valueOf(frontkamera_VERDI_skalere));
            }
            if (끝크기 > 0) {
                tom_område.put(Integer.valueOf(정렬시작 + Størrelse), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Størrelse));
            Arrays.fill(Minne_område, 정렬시작, 정렬시작 + Størrelse, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void frigi_lager(int e_post) {
        Integer skalere_objekt = 사용영역.remove(Integer.valueOf(e_post));
        if (skalere_objekt == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Kjør_2 = e_post;
        int Størrelse = skalere_objekt.intValue();
        Map.Entry<Integer, Integer> frontkamera_VERDI = tom_område.lowerEntry(Integer.valueOf(Kjør_2));
        if (frontkamera_VERDI != null && frontkamera_VERDI.getKey().intValue() + frontkamera_VERDI.getValue().intValue() == Kjør_2) {
            Kjør_2 = frontkamera_VERDI.getKey().intValue();
            Størrelse += frontkamera_VERDI.getValue().intValue();
            tom_område.remove(frontkamera_VERDI.getKey());
        }
        Map.Entry<Integer, Integer> TILBAKE_VERDI = tom_område.ceilingEntry(Integer.valueOf(Kjør_2));
        if (TILBAKE_VERDI != null && Kjør_2 + Størrelse == TILBAKE_VERDI.getKey().intValue()) {
            Størrelse += TILBAKE_VERDI.getValue().intValue();
            tom_område.remove(TILBAKE_VERDI.getKey());
        }
        tom_område.put(Integer.valueOf(Kjør_2), Integer.valueOf(Størrelse));
    }

    public synchronized byte 바이트읽기(int e_post) {
        sjekk_område(e_post, 1);
        return Minne_område[e_post];
    }

    public synchronized void skrive_byte_VERDI(int e_post, byte VERDI) {
        sjekk_område(e_post, 1);
        Minne_område[e_post] = VERDI;
    }

    public synchronized int total_skalere() {
        return Minne_område.length;
    }

    public synchronized int 사용크기() {
        int total_VERDI = 0;
        for (Integer Størrelse : 사용영역.values()) {
            total_VERDI += Størrelse.intValue();
        }
        return total_VERDI;
    }

    private void sjekk_område(int e_post, int Størrelse) {
        if (e_post < 0 || Størrelse < 0 || e_post > Minne_område.length - Størrelse) {
            throw new IndexOutOfBoundsException("Minne_område 범위를 벗어났습니다.");
        }
    }
}

