// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Россия.JRusOS.Память_регион;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 выровнять_ЗНАЧЕН выделить_Память, выпуск_Память_293182ec, 병합을 담당한다. */
public final class Память_менеджер {
    private final byte[] Память_регион;
    private final TreeMap<Integer, Integer> пустой_регион = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public Память_менеджер(int итог_изменить_размер) {
        if (итог_изменить_размер < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        Память_регион = new byte[итог_изменить_размер];
        пустой_регион.put(Integer.valueOf(4096), Integer.valueOf(итог_изменить_размер - 4096));
    }

    public synchronized int выделить_Память(int Размер) {
        return 정렬할당(Размер, 1);
    }

    public synchronized int 정렬할당(int Размер, int выровнять_ЗНАЧЕН) {
        if (Размер <= 0 || выровнять_ЗНАЧЕН <= 0 || (выровнять_ЗНАЧЕН & (выровнять_ЗНАЧЕН - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> ввод_ЗНАЧЕН : пустой_регион.entrySet()) {
            int запустить = ввод_ЗНАЧЕН.getKey().intValue();
            int регион_изменить_размер = ввод_ЗНАЧЕН.getValue().intValue();
            int 정렬시작 = (запустить + выровнять_ЗНАЧЕН - 1) & -выровнять_ЗНАЧЕН;
            int лицевая_камера_ЗНАЧЕН_изменить_размер = 정렬시작 - запустить;
            int 끝크기 = регион_изменить_размер - лицевая_камера_ЗНАЧЕН_изменить_размер - Размер;
            if (끝크기 < 0) {
                continue;
            }
            пустой_регион.remove(Integer.valueOf(запустить));
            if (лицевая_камера_ЗНАЧЕН_изменить_размер > 0) {
                пустой_регион.put(Integer.valueOf(запустить), Integer.valueOf(лицевая_камера_ЗНАЧЕН_изменить_размер));
            }
            if (끝크기 > 0) {
                пустой_регион.put(Integer.valueOf(정렬시작 + Размер), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Размер));
            Arrays.fill(Память_регион, 정렬시작, 정렬시작 + Размер, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void выпуск_Память_293182ec(int АДРЕС) {
        Integer изменить_размер_объект = 사용영역.remove(Integer.valueOf(АДРЕС));
        if (изменить_размер_объект == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int запустить = АДРЕС;
        int Размер = изменить_размер_объект.intValue();
        Map.Entry<Integer, Integer> лицевая_камера_ЗНАЧЕН = пустой_регион.lowerEntry(Integer.valueOf(запустить));
        if (лицевая_камера_ЗНАЧЕН != null && лицевая_камера_ЗНАЧЕН.getKey().intValue() + лицевая_камера_ЗНАЧЕН.getValue().intValue() == запустить) {
            запустить = лицевая_камера_ЗНАЧЕН.getKey().intValue();
            Размер += лицевая_камера_ЗНАЧЕН.getValue().intValue();
            пустой_регион.remove(лицевая_камера_ЗНАЧЕН.getKey());
        }
        Map.Entry<Integer, Integer> BACK_ЗНАЧЕН = пустой_регион.ceilingEntry(Integer.valueOf(запустить));
        if (BACK_ЗНАЧЕН != null && запустить + Размер == BACK_ЗНАЧЕН.getKey().intValue()) {
            Размер += BACK_ЗНАЧЕН.getValue().intValue();
            пустой_регион.remove(BACK_ЗНАЧЕН.getKey());
        }
        пустой_регион.put(Integer.valueOf(запустить), Integer.valueOf(Размер));
    }

    public synchronized byte чтение_байт_ЗНАЧЕН(int АДРЕС) {
        чек_диапазон(АДРЕС, 1);
        return Память_регион[АДРЕС];
    }

    public synchronized void запись_байт_ЗНАЧЕН(int АДРЕС, byte ЗНАЧЕН) {
        чек_диапазон(АДРЕС, 1);
        Память_регион[АДРЕС] = ЗНАЧЕН;
    }

    public synchronized int итог_изменить_размер() {
        return Память_регион.length;
    }

    public synchronized int 사용크기() {
        int итог_ЗНАЧЕН = 0;
        for (Integer Размер : 사용영역.values()) {
            итог_ЗНАЧЕН += Размер.intValue();
        }
        return итог_ЗНАЧЕН;
    }

    private void чек_диапазон(int АДРЕС, int Размер) {
        if (АДРЕС < 0 || Размер < 0 || АДРЕС > Память_регион.length - Размер) {
            throw new IndexOutOfBoundsException("Память_регион 범위를 벗어났습니다.");
        }
    }
}

