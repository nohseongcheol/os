// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Kanada.JCanOS.Memória_régió;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 igazít_ÉRTÉK kioszt_tár, kiad_tár, 병합을 담당한다. */
public final class Memória_kezelő {
    private final byte[] Memória_régió;
    private final TreeMap<Integer, Integer> üres_régió = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Memória_kezelő(int összesen_méretez) {
        if (összesen_méretez < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Memória_régió = new byte[összesen_méretez];
        üres_régió.put(Integer.valueOf(4096), Integer.valueOf(összesen_méretez - 4096));
    }

    public synchronized int kioszt_tár(int Méret) {
        return 정렬할당(Méret, 1);
    }

    public synchronized int 정렬할당(int Méret, int igazít_ÉRTÉK) {
        if (Méret <= 0 || igazít_ÉRTÉK <= 0 || (igazít_ÉRTÉK & (igazít_ÉRTÉK - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> bejegyzés_ÉRTÉK : üres_régió.entrySet()) {
            int Futtatás = bejegyzés_ÉRTÉK.getKey().intValue();
            int régió_méretez = bejegyzés_ÉRTÉK.getValue().intValue();
            int 정렬시작 = (Futtatás + igazít_ÉRTÉK - 1) & -igazít_ÉRTÉK;
            int elülső_kamera_ÉRTÉK_méretez = 정렬시작 - Futtatás;
            int 끝크기 = régió_méretez - elülső_kamera_ÉRTÉK_méretez - Méret;
            if (끝크기 < 0) {
                continue;
            }
            üres_régió.remove(Integer.valueOf(Futtatás));
            if (elülső_kamera_ÉRTÉK_méretez > 0) {
                üres_régió.put(Integer.valueOf(Futtatás), Integer.valueOf(elülső_kamera_ÉRTÉK_méretez));
            }
            if (끝크기 > 0) {
                üres_régió.put(Integer.valueOf(정렬시작 + Méret), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Méret));
            Arrays.fill(Memória_régió, 정렬시작, 정렬시작 + Méret, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void kiad_tár(int CÍM) {
        Integer méretez_objektum = 사용영역.remove(Integer.valueOf(CÍM));
        if (méretez_objektum == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Futtatás = CÍM;
        int Méret = méretez_objektum.intValue();
        Map.Entry<Integer, Integer> elülső_kamera_ÉRTÉK = üres_régió.lowerEntry(Integer.valueOf(Futtatás));
        if (elülső_kamera_ÉRTÉK != null && elülső_kamera_ÉRTÉK.getKey().intValue() + elülső_kamera_ÉRTÉK.getValue().intValue() == Futtatás) {
            Futtatás = elülső_kamera_ÉRTÉK.getKey().intValue();
            Méret += elülső_kamera_ÉRTÉK.getValue().intValue();
            üres_régió.remove(elülső_kamera_ÉRTÉK.getKey());
        }
        Map.Entry<Integer, Integer> BACK_ÉRTÉK = üres_régió.ceilingEntry(Integer.valueOf(Futtatás));
        if (BACK_ÉRTÉK != null && Futtatás + Méret == BACK_ÉRTÉK.getKey().intValue()) {
            Méret += BACK_ÉRTÉK.getValue().intValue();
            üres_régió.remove(BACK_ÉRTÉK.getKey());
        }
        üres_régió.put(Integer.valueOf(Futtatás), Integer.valueOf(Méret));
    }

    public synchronized byte 바이트읽기(int CÍM) {
        csekk_tartomány(CÍM, 1);
        return Memória_régió[CÍM];
    }

    public synchronized void ír_bájt_ÉRTÉK(int CÍM, byte ÉRTÉK) {
        csekk_tartomány(CÍM, 1);
        Memória_régió[CÍM] = ÉRTÉK;
    }

    public synchronized int összesen_méretez() {
        return Memória_régió.length;
    }

    public synchronized int 사용크기() {
        int összesen_ÉRTÉK = 0;
        for (Integer Méret : 사용영역.values()) {
            összesen_ÉRTÉK += Méret.intValue();
        }
        return összesen_ÉRTÉK;
    }

    private void csekk_tartomány(int CÍM, int Méret) {
        if (CÍM < 0 || Méret < 0 || CÍM > Memória_régió.length - Méret) {
            throw new IndexOutOfBoundsException("Memória_régió 범위를 벗어났습니다.");
        }
    }
}

