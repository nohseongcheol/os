// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Польща.JPolOS.Пам_ять_область;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 вирівняти_значення виділяти_місце, випуск_місце, 병합을 담당한다. */
public final class 기억공간관리자 {
    private final byte[] Пам_ять_область;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public 기억공간관리자(int усього_змінювати_розмір) {
        if (усього_змінювати_розмір < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Пам_ять_область = new byte[усього_змінювати_розмір];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(усього_змінювати_розмір - 4096));
    }

    public synchronized int виділяти_місце(int Розмір) {
        return 정렬할당(Розмір, 1);
    }

    public synchronized int 정렬할당(int Розмір, int вирівняти_значення) {
        if (Розмір <= 0 || вирівняти_значення <= 0 || (вирівняти_значення & (вирівняти_значення - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> запис_значення_962f286b : 빈영역.entrySet()) {
            int запустити = запис_значення_962f286b.getKey().intValue();
            int область_змінювати_розмір = запис_значення_962f286b.getValue().intValue();
            int 정렬시작 = (запустити + вирівняти_значення - 1) & -вирівняти_значення;
            int фронтальна_камера_значення_змінювати_розмір = 정렬시작 - запустити;
            int 끝크기 = область_змінювати_розмір - фронтальна_камера_значення_змінювати_розмір - Розмір;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(запустити));
            if (фронтальна_камера_значення_змінювати_розмір > 0) {
                빈영역.put(Integer.valueOf(запустити), Integer.valueOf(фронтальна_камера_значення_змінювати_розмір));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Розмір), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Розмір));
            Arrays.fill(Пам_ять_область, 정렬시작, 정렬시작 + Розмір, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void випуск_місце(int Адреса) {
        Integer змінювати_розмір_об_єкт = 사용영역.remove(Integer.valueOf(Адреса));
        if (змінювати_розмір_об_єкт == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int запустити = Адреса;
        int Розмір = змінювати_розмір_об_єкт.intValue();
        Map.Entry<Integer, Integer> фронтальна_камера_значення = 빈영역.lowerEntry(Integer.valueOf(запустити));
        if (фронтальна_камера_значення != null && фронтальна_камера_значення.getKey().intValue() + фронтальна_камера_значення.getValue().intValue() == запустити) {
            запустити = фронтальна_камера_значення.getKey().intValue();
            Розмір += фронтальна_камера_значення.getValue().intValue();
            빈영역.remove(фронтальна_камера_значення.getKey());
        }
        Map.Entry<Integer, Integer> НАЗАД_значення = 빈영역.ceilingEntry(Integer.valueOf(запустити));
        if (НАЗАД_значення != null && запустити + Розмір == НАЗАД_значення.getKey().intValue()) {
            Розмір += НАЗАД_значення.getValue().intValue();
            빈영역.remove(НАЗАД_значення.getKey());
        }
        빈영역.put(Integer.valueOf(запустити), Integer.valueOf(Розмір));
    }

    public synchronized byte 바이트읽기(int Адреса) {
        перевіряти_діапазон(Адреса, 1);
        return Пам_ять_область[Адреса];
    }

    public synchronized void записування_байт_значення(int Адреса, byte значення) {
        перевіряти_діапазон(Адреса, 1);
        Пам_ять_область[Адреса] = значення;
    }

    public synchronized int усього_змінювати_розмір() {
        return Пам_ять_область.length;
    }

    public synchronized int 사용크기() {
        int усього_значення = 0;
        for (Integer Розмір : 사용영역.values()) {
            усього_значення += Розмір.intValue();
        }
        return усього_значення;
    }

    private void перевіряти_діапазон(int Адреса, int Розмір) {
        if (Адреса < 0 || Розмір < 0 || Адреса > Пам_ять_область.length - Розмір) {
            throw new IndexOutOfBoundsException("Пам_ять_область 범위를 벗어났습니다.");
        }
    }
}

