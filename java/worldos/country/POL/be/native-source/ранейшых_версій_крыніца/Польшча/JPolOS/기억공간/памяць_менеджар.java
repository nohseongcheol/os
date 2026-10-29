// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Польшча.JPolOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 выраўнаваць_значэнне вылучыць_Сховішча, выпуск_Сховішча, 병합을 담당한다. */
public final class памяць_менеджар {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public памяць_менеджар(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int вылучыць_Сховішча(int Памер) {
        return 정렬할당(Памер, 1);
    }

    public synchronized int 정렬할당(int Памер, int выраўнаваць_значэнне) {
        if (Памер <= 0 || выраўнаваць_значэнне <= 0 || (выраўнаваць_значэнне & (выраўнаваць_значэнне - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> увядзенне_значэнне : 빈영역.entrySet()) {
            int Выканаць = увядзенне_значэнне.getKey().intValue();
            int 영역크기 = увядзенне_значэнне.getValue().intValue();
            int 정렬시작 = (Выканаць + выраўнаваць_значэнне - 1) & -выраўнаваць_значэнне;
            int пярэдняя_камера_значэнне_памер = 정렬시작 - Выканаць;
            int 끝크기 = 영역크기 - пярэдняя_камера_значэнне_памер - Памер;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Выканаць));
            if (пярэдняя_камера_значэнне_памер > 0) {
                빈영역.put(Integer.valueOf(Выканаць), Integer.valueOf(пярэдняя_камера_значэнне_памер));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Памер), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Памер));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Памер, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void выпуск_Сховішча(int адрас) {
        Integer памер_аб_ект = 사용영역.remove(Integer.valueOf(адрас));
        if (памер_аб_ект == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Выканаць = адрас;
        int Памер = памер_аб_ект.intValue();
        Map.Entry<Integer, Integer> пярэдняя_камера_значэнне = 빈영역.lowerEntry(Integer.valueOf(Выканаць));
        if (пярэдняя_камера_значэнне != null && пярэдняя_камера_значэнне.getKey().intValue() + пярэдняя_камера_значэнне.getValue().intValue() == Выканаць) {
            Выканаць = пярэдняя_камера_значэнне.getKey().intValue();
            Памер += пярэдняя_камера_значэнне.getValue().intValue();
            빈영역.remove(пярэдняя_камера_значэнне.getKey());
        }
        Map.Entry<Integer, Integer> Назад_значэнне = 빈영역.ceilingEntry(Integer.valueOf(Выканаць));
        if (Назад_значэнне != null && Выканаць + Памер == Назад_значэнне.getKey().intValue()) {
            Памер += Назад_значэнне.getValue().intValue();
            빈영역.remove(Назад_значэнне.getKey());
        }
        빈영역.put(Integer.valueOf(Выканаць), Integer.valueOf(Памер));
    }

    public synchronized byte 바이트읽기(int адрас) {
        범위확인(адрас, 1);
        return 기억공간[адрас];
    }

    public synchronized void напісаць_байт_значэнне(int адрас, byte значэнне) {
        범위확인(адрас, 1);
        기억공간[адрас] = значэнне;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Памер : 사용영역.values()) {
            합계 += Памер.intValue();
        }
        return 합계;
    }

    private void 범위확인(int адрас, int Памер) {
        if (адрас < 0 || Памер < 0 || адрас > 기억공간.length - Памер) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

