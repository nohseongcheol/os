// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Россия.JRusOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB бит_VALUE 연결과 язу 시 복사를 제공한다. */
public final class бит_идарәче {
    public static final int бит_зурлыгы = 4096;

    private static final class бит_VALUE {
        private byte[] мәгълүмат = new byte[бит_зурлыгы];
        private int Белешмәлекләр_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class адрес_өлкә {
        private final Map<Integer, бит_VALUE> бит_таблица = new HashMap<Integer, бит_VALUE>();
    }

    public адрес_өлкә 새주소공간() {
        return new адрес_өлкә();
    }

    public void MAP_бит(адрес_өлкә 공간, int виртуаль_адрес, boolean 쓰기가능) {
        int INDEX = 쪽번호(виртуаль_адрес);
        бит_VALUE 새쪽 = new бит_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        공간.бит_таблица.put(Integer.valueOf(INDEX), 새쪽);
    }

    public адрес_өлкә 쓰기시복사복제(адрес_өлкә 원본) {
        адрес_өлкә 복제본 = new адрес_өлкә();
        for (Map.Entry<Integer, бит_VALUE> кертү_VALUE : 원본.бит_таблица.entrySet()) {
            бит_VALUE 공유쪽 = кертү_VALUE.getValue();
            공유쪽.Белешмәлекләр_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.бит_таблица.put(кертү_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(адрес_өлкә 공간, int виртуаль_адрес) {
        бит_VALUE максат_кыйммәт = FIND_бит(공간, виртуаль_адрес);
        return максат_кыйммәт.мәгълүмат[Math.floorMod(виртуаль_адрес, бит_зурлыгы)];
    }

    public void язу_байт_VALUE(адрес_өлкә 공간, int виртуаль_адрес, byte VALUE) {
        int INDEX = 쪽번호(виртуаль_адрес);
        бит_VALUE максат_кыйммәт = FIND_бит(공간, виртуаль_адрес);
        if (!максат_кыйммәт.쓰기가능) {
            if (!максат_кыйммәт.쓰기시복사) {
                throw new IllegalStateException("읽기 전용 쪽입니다.");
            }
            максат_кыйммәт = Төзү_хосусый_бит(공간, INDEX, максат_кыйммәт);
        }
        максат_кыйммәт.мәгълүмат[Math.floorMod(виртуаль_адрес, бит_зурлыгы)] = VALUE;
    }

    public void 범위개인쓰기(адрес_өлкә 공간, int Start_адрес, int үлчәмен_үзгәртү) {
        if (үлчәмен_үзгәртү < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int тәмамлау_адрес = Math.addExact(Start_адрес, үлчәмен_үзгәртү);
        for (int адрес = Start_адрес; адрес < тәмамлау_адрес; адрес = (쪽번호(адрес) + 1) * бит_зурлыгы) {
            int INDEX = 쪽번호(адрес);
            бит_VALUE максат_кыйммәт = FIND_бит(공간, адрес);
            if (максат_кыйммәт.쓰기시복사) {
                Төзү_хосусый_бит(공간, INDEX, максат_кыйммәт);
            } else {
                максат_кыйммәт.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(адрес_өлкә 공간, int Start_адрес, byte[] мәгълүмат) {
        for (int INDEX = 0; INDEX < мәгълүмат.length; INDEX++) {
            язу_байт_VALUE(공간, Start_адрес + INDEX, мәгълүмат[INDEX]);
        }
    }

    private бит_VALUE Төзү_хосусый_бит(адрес_өлкә 공간, int INDEX, бит_VALUE 공유쪽) {
        бит_VALUE хосусый_бит = new бит_VALUE();
        хосусый_бит.мәгълүмат = Arrays.copyOf(공유쪽.мәгълүмат, 공유쪽.мәгълүмат.length);
        хосусый_бит.쓰기가능 = true;
        хосусый_бит.쓰기시복사 = false;
        공유쪽.Белешмәлекләр_COUNT--;
        공간.бит_таблица.put(Integer.valueOf(INDEX), хосусый_бит);
        return хосусый_бит;
    }

    private бит_VALUE FIND_бит(адрес_өлкә 공간, int адрес) {
        бит_VALUE максат_кыйммәт = 공간.бит_таблица.get(Integer.valueOf(쪽번호(адрес)));
        if (максат_кыйммәт == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return максат_кыйммәт;
    }

    private int 쪽번호(int адрес) {
        if (адрес < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return адрес / бит_зурлыгы;
    }
}

