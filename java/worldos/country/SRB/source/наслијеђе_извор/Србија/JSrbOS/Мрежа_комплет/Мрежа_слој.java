// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Србија.JSrbOS.Мрежа_комплет;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Мрежа_слој {
    @FunctionalInterface
    public interface 자료처리기 {
        void Процес_вриједност_унос(byte[] подаци, int Покрени, int дужина_вриједност);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void регистровати_интернетски_протокол(int случај_вриједност, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(случај_вриједност & 0xff), 처리기);
    }

    public void регистровати_корисник_подаци_лекција(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void регистровати_пренос_контрола(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] кадар_индекс) {
        if (!Мрежа_Алатке.이더넷틀인가(кадар_индекс)) {
            return false;
        }
        int 종류 = Мрежа_Алатке.이더넷상위규약(кадар_индекс);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Процес_вриједност_унос(кадар_индекс, 14, кадар_индекс.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(кадар_индекс, 14);
    }

    private boolean 상호통신망받기(byte[] подаци, int Покрени) {
        if (!Мрежа_Алатке.상호통신망규약사판인가(подаци, Покрени)) {
            return false;
        }
        int Заглавље_дужина = (подаци[Покрени] & 0x0f) * 4;
        int 전체길이 = Мрежа_Алатке.큰순서짧은정수(подаци, Покрени + 2);
        if (전체길이 < Заглавље_дужина || Покрени + 전체길이 > подаци.length) {
            return false;
        }
        int случај_вриједност = подаци[Покрени + 9] & 0xff;
        int Садржај_Старт = Покрени + Заглавље_дужина;
        int Садржај_дужина = 전체길이 - Заглавље_дужина;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(случај_вриједност));
        if (직접처리기 != null) {
            직접처리기.Процес_вриједност_унос(подаци, Садржај_Старт, Садржај_дужина);
            return true;
        }
        if (Садржај_дужина < 4) {
            return false;
        }
        int одредиште_број_порта = Мрежа_Алатке.큰순서짧은정수(подаци, Садржај_Старт + 2);
        Map<Integer, 자료처리기> порт_табела = случај_вриједност == 17 ? 사용자자료단위처리기 : случај_вриједност == 6 ? 전송제어처리기 : null;
        if (порт_табела == null) {
            return false;
        }
        자료처리기 포트처리기 = порт_табела.get(Integer.valueOf(одредиште_број_порта));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Процес_вриједност_унос(подаци, Садржај_Старт, Садржај_дужина);
        return true;
    }
}

