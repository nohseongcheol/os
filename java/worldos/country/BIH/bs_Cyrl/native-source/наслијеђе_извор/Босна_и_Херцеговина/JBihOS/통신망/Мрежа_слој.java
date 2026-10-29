// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Босна_и_Херцеговина.JBihOS.통신망;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Мрежа_слој {
    @FunctionalInterface
    public interface 자료처리기 {
        void процес_вриједност_унос(byte[] подаци, int 시작, int дужина_вриједност);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void 상호통신망등록(int Уговор_вриједност, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(Уговор_вриједност & 0xff), 처리기);
    }

    public void 사용자자료단위등록(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] оквир_индекс) {
        if (!통신망도구.이더넷틀인가(оквир_индекс)) {
            return false;
        }
        int 종류 = 통신망도구.이더넷상위규약(оквир_индекс);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.процес_вриједност_унос(оквир_индекс, 14, оквир_индекс.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(оквир_индекс, 14);
    }

    private boolean 상호통신망받기(byte[] подаци, int 시작) {
        if (!통신망도구.상호통신망규약사판인가(подаци, 시작)) {
            return false;
        }
        int заглавље_дужина = (подаци[시작] & 0x0f) * 4;
        int 전체길이 = 통신망도구.큰순서짧은정수(подаци, 시작 + 2);
        if (전체길이 < заглавље_дужина || 시작 + 전체길이 > подаци.length) {
            return false;
        }
        int Уговор_вриједност = подаци[시작 + 9] & 0xff;
        int Садржај_почети = 시작 + заглавље_дужина;
        int Садржај_дужина = 전체길이 - заглавље_дужина;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(Уговор_вриједност));
        if (직접처리기 != null) {
            직접처리기.процес_вриједност_унос(подаци, Садржај_почети, Садржај_дужина);
            return true;
        }
        if (Садржај_дужина < 4) {
            return false;
        }
        int 목적포트 = 통신망도구.큰순서짧은정수(подаци, Садржај_почети + 2);
        Map<Integer, 자료처리기> порт_табела = Уговор_вриједност == 17 ? 사용자자료단위처리기 : Уговор_вриједност == 6 ? 전송제어처리기 : null;
        if (порт_табела == null) {
            return false;
        }
        자료처리기 포트처리기 = порт_табела.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.процес_вриједност_унос(подаци, Садржај_почети, Садржај_дужина);
        return true;
    }
}

