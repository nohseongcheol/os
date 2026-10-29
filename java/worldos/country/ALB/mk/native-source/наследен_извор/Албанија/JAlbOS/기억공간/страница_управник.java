// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Албанија.JAlbOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB страница_VALUE 연결과 Запиши 시 복사를 제공한다. */
public final class страница_управник {
    public static final int големина_на_страницата = 4096;

    private static final class страница_VALUE {
        private byte[] податоци = new byte[големина_на_страницата];
        private int Референци_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class адреса_простор {
        private final Map<Integer, страница_VALUE> страница_табела = new HashMap<Integer, страница_VALUE>();
    }

    public адреса_простор 새주소공간() {
        return new адреса_простор();
    }

    public void MAP_страница(адреса_простор 공간, int виртуелна_адреса, boolean 쓰기가능) {
        int INDEX = 쪽번호(виртуелна_адреса);
        страница_VALUE 새쪽 = new страница_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        공간.страница_табела.put(Integer.valueOf(INDEX), 새쪽);
    }

    public адреса_простор 쓰기시복사복제(адреса_простор 원본) {
        адреса_простор 복제본 = new адреса_простор();
        for (Map.Entry<Integer, страница_VALUE> внес_VALUE : 원본.страница_табела.entrySet()) {
            страница_VALUE 공유쪽 = внес_VALUE.getValue();
            공유쪽.Референци_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.страница_табела.put(внес_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(адреса_простор 공간, int виртуелна_адреса) {
        страница_VALUE цел = FIND_страница(공간, виртуелна_адреса);
        return цел.податоци[Math.floorMod(виртуелна_адреса, големина_на_страницата)];
    }

    public void запиши_бајт_VALUE(адреса_простор 공간, int виртуелна_адреса, byte VALUE) {
        int INDEX = 쪽번호(виртуелна_адреса);
        страница_VALUE цел = FIND_страница(공간, виртуелна_адреса);
        if (!цел.쓰기가능) {
            if (!цел.쓰기시복사) {
                throw new IllegalStateException("Читај 전용 쪽입니다.");
            }
            цел = Create_личен_страница(공간, INDEX, цел);
        }
        цел.податоци[Math.floorMod(виртуелна_адреса, големина_на_страницата)] = VALUE;
    }

    public void 범위개인쓰기(адреса_простор 공간, int почетна_адреса, int Големина) {
        if (Големина < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int крај_адреса = Math.addExact(почетна_адреса, Големина);
        for (int адреса = почетна_адреса; адреса < крај_адреса; адреса = (쪽번호(адреса) + 1) * големина_на_страницата) {
            int INDEX = 쪽번호(адреса);
            страница_VALUE цел = FIND_страница(공간, адреса);
            if (цел.쓰기시복사) {
                Create_личен_страница(공간, INDEX, цел);
            } else {
                цел.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(адреса_простор 공간, int почетна_адреса, byte[] податоци) {
        for (int INDEX = 0; INDEX < податоци.length; INDEX++) {
            запиши_бајт_VALUE(공간, почетна_адреса + INDEX, податоци[INDEX]);
        }
    }

    private страница_VALUE Create_личен_страница(адреса_простор 공간, int INDEX, страница_VALUE 공유쪽) {
        страница_VALUE личен_страница = new страница_VALUE();
        личен_страница.податоци = Arrays.copyOf(공유쪽.податоци, 공유쪽.податоци.length);
        личен_страница.쓰기가능 = true;
        личен_страница.쓰기시복사 = false;
        공유쪽.Референци_COUNT--;
        공간.страница_табела.put(Integer.valueOf(INDEX), личен_страница);
        return личен_страница;
    }

    private страница_VALUE FIND_страница(адреса_простор 공간, int адреса) {
        страница_VALUE цел = 공간.страница_табела.get(Integer.valueOf(쪽번호(адреса)));
        if (цел == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return цел;
    }

    private int 쪽번호(int адреса) {
        if (адреса < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return адреса / големина_на_страницата;
    }
}

