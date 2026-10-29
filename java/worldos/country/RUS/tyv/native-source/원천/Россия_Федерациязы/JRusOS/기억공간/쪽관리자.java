// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Россия_Федерациязы.JRusOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB 쪽 연결과 쓰기 시 복사를 제공한다. */
public final class 쪽관리자 {
    public static final int 쪽크기 = 4096;

    private static final class 쪽 {
        private byte[] 자료 = new byte[쪽크기];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class 주소공간 {
        private final Map<Integer, 쪽> 쪽표 = new HashMap<Integer, 쪽>();
    }

    public 주소공간 새주소공간() {
        return new 주소공간();
    }

    public void 쪽연결(주소공간 공간, int 가상주소, boolean 쓰기가능) {
        int 번호 = 쪽번호(가상주소);
        쪽 새쪽 = new 쪽();
        새쪽.쓰기가능 = 쓰기가능;
        공간.쪽표.put(Integer.valueOf(번호), 새쪽);
    }

    public 주소공간 쓰기시복사복제(주소공간 원본) {
        주소공간 복제본 = new 주소공간();
        for (Map.Entry<Integer, 쪽> 항목 : 원본.쪽표.entrySet()) {
            쪽 공유쪽 = 항목.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.쪽표.put(항목.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(주소공간 공간, int 가상주소) {
        쪽 대상 = 쪽찾기(공간, 가상주소);
        return 대상.자료[Math.floorMod(가상주소, 쪽크기)];
    }

    public void 바이트쓰기(주소공간 공간, int 가상주소, byte 값) {
        int 번호 = 쪽번호(가상주소);
        쪽 대상 = 쪽찾기(공간, 가상주소);
        if (!대상.쓰기가능) {
            if (!대상.쓰기시복사) {
                throw new IllegalStateException("읽기 전용 쪽입니다.");
            }
            대상 = 개인쪽만들기(공간, 번호, 대상);
        }
        대상.자료[Math.floorMod(가상주소, 쪽크기)] = 값;
    }

    public void 범위개인쓰기(주소공간 공간, int 시작주소, int 크기) {
        if (크기 < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int 끝주소 = Math.addExact(시작주소, 크기);
        for (int 주소 = 시작주소; 주소 < 끝주소; 주소 = (쪽번호(주소) + 1) * 쪽크기) {
            int 번호 = 쪽번호(주소);
            쪽 대상 = 쪽찾기(공간, 주소);
            if (대상.쓰기시복사) {
                개인쪽만들기(공간, 번호, 대상);
            } else {
                대상.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(주소공간 공간, int 시작주소, byte[] 자료) {
        for (int 번호 = 0; 번호 < 자료.length; 번호++) {
            바이트쓰기(공간, 시작주소 + 번호, 자료[번호]);
        }
    }

    private 쪽 개인쪽만들기(주소공간 공간, int 번호, 쪽 공유쪽) {
        쪽 개인쪽 = new 쪽();
        개인쪽.자료 = Arrays.copyOf(공유쪽.자료, 공유쪽.자료.length);
        개인쪽.쓰기가능 = true;
        개인쪽.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.쪽표.put(Integer.valueOf(번호), 개인쪽);
        return 개인쪽;
    }

    private 쪽 쪽찾기(주소공간 공간, int 주소) {
        쪽 대상 = 공간.쪽표.get(Integer.valueOf(쪽번호(주소)));
        if (대상 == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return 대상;
    }

    private int 쪽번호(int 주소) {
        if (주소 < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return 주소 / 쪽크기;
    }
}

