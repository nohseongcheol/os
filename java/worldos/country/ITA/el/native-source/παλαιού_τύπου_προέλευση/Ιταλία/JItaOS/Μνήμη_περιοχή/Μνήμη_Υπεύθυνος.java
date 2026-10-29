// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ιταλία.JItaOS.Μνήμη_περιοχή;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 στοιχίζω_τιμή εκχωρώ_Χώρος_αποθήκευσης, έκδοση_Χώρος_αποθήκευσης, 병합을 담당한다. */
public final class Μνήμη_Υπεύθυνος {
    private final byte[] Μνήμη_περιοχή;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Μνήμη_Υπεύθυνος(int σύνολο_αλλάζω_μέγεθος) {
        if (σύνολο_αλλάζω_μέγεθος < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Μνήμη_περιοχή = new byte[σύνολο_αλλάζω_μέγεθος];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(σύνολο_αλλάζω_μέγεθος - 4096));
    }

    public synchronized int εκχωρώ_Χώρος_αποθήκευσης(int Μέγεθος) {
        return 정렬할당(Μέγεθος, 1);
    }

    public synchronized int 정렬할당(int Μέγεθος, int στοιχίζω_τιμή) {
        if (Μέγεθος <= 0 || στοιχίζω_τιμή <= 0 || (στοιχίζω_τιμή & (στοιχίζω_τιμή - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> καταχώρηση_τιμή : 빈영역.entrySet()) {
            int Εκτέλεση_2 = καταχώρηση_τιμή.getKey().intValue();
            int περιοχή_αλλάζω_μέγεθος = καταχώρηση_τιμή.getValue().intValue();
            int 정렬시작 = (Εκτέλεση_2 + στοιχίζω_τιμή - 1) & -στοιχίζω_τιμή;
            int μπροστινή_τιμή_αλλάζω_μέγεθος = 정렬시작 - Εκτέλεση_2;
            int 끝크기 = περιοχή_αλλάζω_μέγεθος - μπροστινή_τιμή_αλλάζω_μέγεθος - Μέγεθος;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Εκτέλεση_2));
            if (μπροστινή_τιμή_αλλάζω_μέγεθος > 0) {
                빈영역.put(Integer.valueOf(Εκτέλεση_2), Integer.valueOf(μπροστινή_τιμή_αλλάζω_μέγεθος));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Μέγεθος), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Μέγεθος));
            Arrays.fill(Μνήμη_περιοχή, 정렬시작, 정렬시작 + Μέγεθος, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void έκδοση_Χώρος_αποθήκευσης(int διεύθυνση) {
        Integer αλλάζω_μέγεθος_αντικείμενο = 사용영역.remove(Integer.valueOf(διεύθυνση));
        if (αλλάζω_μέγεθος_αντικείμενο == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Εκτέλεση_2 = διεύθυνση;
        int Μέγεθος = αλλάζω_μέγεθος_αντικείμενο.intValue();
        Map.Entry<Integer, Integer> μπροστινή_τιμή = 빈영역.lowerEntry(Integer.valueOf(Εκτέλεση_2));
        if (μπροστινή_τιμή != null && μπροστινή_τιμή.getKey().intValue() + μπροστινή_τιμή.getValue().intValue() == Εκτέλεση_2) {
            Εκτέλεση_2 = μπροστινή_τιμή.getKey().intValue();
            Μέγεθος += μπροστινή_τιμή.getValue().intValue();
            빈영역.remove(μπροστινή_τιμή.getKey());
        }
        Map.Entry<Integer, Integer> Πίσω_τιμή = 빈영역.ceilingEntry(Integer.valueOf(Εκτέλεση_2));
        if (Πίσω_τιμή != null && Εκτέλεση_2 + Μέγεθος == Πίσω_τιμή.getKey().intValue()) {
            Μέγεθος += Πίσω_τιμή.getValue().intValue();
            빈영역.remove(Πίσω_τιμή.getKey());
        }
        빈영역.put(Integer.valueOf(Εκτέλεση_2), Integer.valueOf(Μέγεθος));
    }

    public synchronized byte 바이트읽기(int διεύθυνση) {
        ελέγχω_εύρος(διεύθυνση, 1);
        return Μνήμη_περιοχή[διεύθυνση];
    }

    public synchronized void 바이트쓰기(int διεύθυνση, byte τιμή) {
        ελέγχω_εύρος(διεύθυνση, 1);
        Μνήμη_περιοχή[διεύθυνση] = τιμή;
    }

    public synchronized int σύνολο_αλλάζω_μέγεθος() {
        return Μνήμη_περιοχή.length;
    }

    public synchronized int 사용크기() {
        int σύνολο_τιμή = 0;
        for (Integer Μέγεθος : 사용영역.values()) {
            σύνολο_τιμή += Μέγεθος.intValue();
        }
        return σύνολο_τιμή;
    }

    private void ελέγχω_εύρος(int διεύθυνση, int Μέγεθος) {
        if (διεύθυνση < 0 || Μέγεθος < 0 || διεύθυνση > Μνήμη_περιοχή.length - Μέγεθος) {
            throw new IndexOutOfBoundsException("Μνήμη_περιοχή 범위를 벗어났습니다.");
        }
    }
}

