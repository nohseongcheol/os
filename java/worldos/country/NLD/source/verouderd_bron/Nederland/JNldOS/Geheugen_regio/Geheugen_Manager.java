// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederland.JNldOS.Geheugen_regio;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 uitlijnen_WAARDE toewijzen_Opslag, versie_Opslag, 병합을 담당한다. */
public final class Geheugen_Manager {
    private final byte[] Geheugen_regio;
    private final TreeMap<Integer, Integer> leeg_regio = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Geheugen_Manager(int totaal_formaat_wijzigen) {
        if (totaal_formaat_wijzigen < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Geheugen_regio = new byte[totaal_formaat_wijzigen];
        leeg_regio.put(Integer.valueOf(4096), Integer.valueOf(totaal_formaat_wijzigen - 4096));
    }

    public synchronized int toewijzen_Opslag(int Grootte) {
        return 정렬할당(Grootte, 1);
    }

    public synchronized int 정렬할당(int Grootte, int uitlijnen_WAARDE) {
        if (Grootte <= 0 || uitlijnen_WAARDE <= 0 || (uitlijnen_WAARDE & (uitlijnen_WAARDE - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> invoer_WAARDE_962f286b : leeg_regio.entrySet()) {
            int starten = invoer_WAARDE_962f286b.getKey().intValue();
            int regio_formaat_wijzigen = invoer_WAARDE_962f286b.getValue().intValue();
            int 정렬시작 = (starten + uitlijnen_WAARDE - 1) & -uitlijnen_WAARDE;
            int voorkant_WAARDE_formaat_wijzigen = 정렬시작 - starten;
            int 끝크기 = regio_formaat_wijzigen - voorkant_WAARDE_formaat_wijzigen - Grootte;
            if (끝크기 < 0) {
                continue;
            }
            leeg_regio.remove(Integer.valueOf(starten));
            if (voorkant_WAARDE_formaat_wijzigen > 0) {
                leeg_regio.put(Integer.valueOf(starten), Integer.valueOf(voorkant_WAARDE_formaat_wijzigen));
            }
            if (끝크기 > 0) {
                leeg_regio.put(Integer.valueOf(정렬시작 + Grootte), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Grootte));
            Arrays.fill(Geheugen_regio, 정렬시작, 정렬시작 + Grootte, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void versie_Opslag(int ADRES) {
        Integer formaat_wijzigen_object = 사용영역.remove(Integer.valueOf(ADRES));
        if (formaat_wijzigen_object == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int starten = ADRES;
        int Grootte = formaat_wijzigen_object.intValue();
        Map.Entry<Integer, Integer> voorkant_WAARDE = leeg_regio.lowerEntry(Integer.valueOf(starten));
        if (voorkant_WAARDE != null && voorkant_WAARDE.getKey().intValue() + voorkant_WAARDE.getValue().intValue() == starten) {
            starten = voorkant_WAARDE.getKey().intValue();
            Grootte += voorkant_WAARDE.getValue().intValue();
            leeg_regio.remove(voorkant_WAARDE.getKey());
        }
        Map.Entry<Integer, Integer> BACK_WAARDE = leeg_regio.ceilingEntry(Integer.valueOf(starten));
        if (BACK_WAARDE != null && starten + Grootte == BACK_WAARDE.getKey().intValue()) {
            Grootte += BACK_WAARDE.getValue().intValue();
            leeg_regio.remove(BACK_WAARDE.getKey());
        }
        leeg_regio.put(Integer.valueOf(starten), Integer.valueOf(Grootte));
    }

    public synchronized byte 바이트읽기(int ADRES) {
        cheque_bereik(ADRES, 1);
        return Geheugen_regio[ADRES];
    }

    public synchronized void schrijven_byte_WAARDE(int ADRES, byte WAARDE) {
        cheque_bereik(ADRES, 1);
        Geheugen_regio[ADRES] = WAARDE;
    }

    public synchronized int totaal_formaat_wijzigen() {
        return Geheugen_regio.length;
    }

    public synchronized int 사용크기() {
        int totaal_WAARDE = 0;
        for (Integer Grootte : 사용영역.values()) {
            totaal_WAARDE += Grootte.intValue();
        }
        return totaal_WAARDE;
    }

    private void cheque_bereik(int ADRES, int Grootte) {
        if (ADRES < 0 || Grootte < 0 || ADRES > Geheugen_regio.length - Grootte) {
            throw new IndexOutOfBoundsException("Geheugen_regio 범위를 벗어났습니다.");
        }
    }
}

