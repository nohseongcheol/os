// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Danmark.JDnkOS.Hukommelse_område;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 justere_VÆRDI tildel_Lager, udgive_Lager, 병합을 담당한다. */
public final class Hukommelse_Leder {
    private final byte[] Hukommelse_område;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Hukommelse_Leder(int i_alt_tilpasse_størrelse) {
        if (i_alt_tilpasse_størrelse < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Hukommelse_område = new byte[i_alt_tilpasse_størrelse];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(i_alt_tilpasse_størrelse - 4096));
    }

    public synchronized int tildel_Lager(int Størrelse) {
        return 정렬할당(Størrelse, 1);
    }

    public synchronized int 정렬할당(int Størrelse, int justere_VÆRDI) {
        if (Størrelse <= 0 || justere_VÆRDI <= 0 || (justere_VÆRDI & (justere_VÆRDI - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> post_VÆRDI_962f286b : 빈영역.entrySet()) {
            int Kør_2 = post_VÆRDI_962f286b.getKey().intValue();
            int område_tilpasse_størrelse = post_VÆRDI_962f286b.getValue().intValue();
            int 정렬시작 = (Kør_2 + justere_VÆRDI - 1) & -justere_VÆRDI;
            int frontvendt_VÆRDI_tilpasse_størrelse = 정렬시작 - Kør_2;
            int 끝크기 = område_tilpasse_størrelse - frontvendt_VÆRDI_tilpasse_størrelse - Størrelse;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Kør_2));
            if (frontvendt_VÆRDI_tilpasse_størrelse > 0) {
                빈영역.put(Integer.valueOf(Kør_2), Integer.valueOf(frontvendt_VÆRDI_tilpasse_størrelse));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Størrelse), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Størrelse));
            Arrays.fill(Hukommelse_område, 정렬시작, 정렬시작 + Størrelse, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void udgive_Lager(int mail) {
        Integer tilpasse_størrelse_objekt = 사용영역.remove(Integer.valueOf(mail));
        if (tilpasse_størrelse_objekt == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Kør_2 = mail;
        int Størrelse = tilpasse_størrelse_objekt.intValue();
        Map.Entry<Integer, Integer> frontvendt_VÆRDI = 빈영역.lowerEntry(Integer.valueOf(Kør_2));
        if (frontvendt_VÆRDI != null && frontvendt_VÆRDI.getKey().intValue() + frontvendt_VÆRDI.getValue().intValue() == Kør_2) {
            Kør_2 = frontvendt_VÆRDI.getKey().intValue();
            Størrelse += frontvendt_VÆRDI.getValue().intValue();
            빈영역.remove(frontvendt_VÆRDI.getKey());
        }
        Map.Entry<Integer, Integer> BACK_VÆRDI = 빈영역.ceilingEntry(Integer.valueOf(Kør_2));
        if (BACK_VÆRDI != null && Kør_2 + Størrelse == BACK_VÆRDI.getKey().intValue()) {
            Størrelse += BACK_VÆRDI.getValue().intValue();
            빈영역.remove(BACK_VÆRDI.getKey());
        }
        빈영역.put(Integer.valueOf(Kør_2), Integer.valueOf(Størrelse));
    }

    public synchronized byte 바이트읽기(int mail) {
        check_område(mail, 1);
        return Hukommelse_område[mail];
    }

    public synchronized void skrive_byte_VÆRDI(int mail, byte VÆRDI) {
        check_område(mail, 1);
        Hukommelse_område[mail] = VÆRDI;
    }

    public synchronized int i_alt_tilpasse_størrelse() {
        return Hukommelse_område.length;
    }

    public synchronized int 사용크기() {
        int i_alt_VÆRDI = 0;
        for (Integer Størrelse : 사용영역.values()) {
            i_alt_VÆRDI += Størrelse.intValue();
        }
        return i_alt_VÆRDI;
    }

    private void check_område(int mail, int Størrelse) {
        if (mail < 0 || Størrelse < 0 || mail > Hukommelse_område.length - Størrelse) {
            throw new IndexOutOfBoundsException("Hukommelse_område 범위를 벗어났습니다.");
        }
    }
}

