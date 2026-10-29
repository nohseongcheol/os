// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ermenistan.JArmOS.통신망;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class 통신망계층 {
    @FunctionalInterface
    public interface 자료처리기 {
        void 처리(byte[] 자료, int 시작, int 길이);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void 상호통신망등록(int 규약, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(규약 & 0xff), 처리기);
    }

    public void 사용자자료단위등록(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] 틀) {
        if (!통신망도구.이더넷틀인가(틀)) {
            return false;
        }
        int 종류 = 통신망도구.이더넷상위규약(틀);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.처리(틀, 14, 틀.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(틀, 14);
    }

    private boolean 상호통신망받기(byte[] 자료, int 시작) {
        if (!통신망도구.상호통신망규약사판인가(자료, 시작)) {
            return false;
        }
        int 머리길이 = (자료[시작] & 0x0f) * 4;
        int 전체길이 = 통신망도구.큰순서짧은정수(자료, 시작 + 2);
        if (전체길이 < 머리길이 || 시작 + 전체길이 > 자료.length) {
            return false;
        }
        int 규약 = 자료[시작 + 9] & 0xff;
        int 내용시작 = 시작 + 머리길이;
        int 내용길이 = 전체길이 - 머리길이;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(규약));
        if (직접처리기 != null) {
            직접처리기.처리(자료, 내용시작, 내용길이);
            return true;
        }
        if (내용길이 < 4) {
            return false;
        }
        int 목적포트 = 통신망도구.큰순서짧은정수(자료, 내용시작 + 2);
        Map<Integer, 자료처리기> 포트표 = 규약 == 17 ? 사용자자료단위처리기 : 규약 == 6 ? 전송제어처리기 : null;
        if (포트표 == null) {
            return false;
        }
        자료처리기 포트처리기 = 포트표.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.처리(자료, 내용시작, 내용길이);
        return true;
    }
}

