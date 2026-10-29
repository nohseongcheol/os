// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Россия.JRusOS.Челтәр_Стәк;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Челтәр_дәрәҗә {
    @FunctionalInterface
    public interface 자료처리기 {
        void Процесс_VALUE_кертү(byte[] мәгълүмат, int эшләтү, int озынлык_VALUE);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void теркәлү_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void теркәлү_IP_протоколы(int бирем_VALUE_102996da, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(бирем_VALUE_102996da & 0xff), 처리기);
    }

    public void теркәлү_кулланучы_мәгълүмат_дәрес(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void теркәлү_тапшыру_идарә(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] кадр_INDEX) {
        if (!Челтәр_Кораллар.이더넷틀인가(кадр_INDEX)) {
            return false;
        }
        int 종류 = Челтәр_Кораллар.Ethernet_UPPER_протокол(кадр_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Процесс_VALUE_кертү(кадр_INDEX, 14, кадр_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(кадр_INDEX, 14);
    }

    private boolean 상호통신망받기(byte[] мәгълүмат, int эшләтү) {
        if (!Челтәр_Кораллар.상호통신망규약사판인가(мәгълүмат, эшләтү)) {
            return false;
        }
        int Башлама_озынлык = (мәгълүмат[эшләтү] & 0x0f) * 4;
        int 전체길이 = Челтәр_Кораллар.큰순서짧은정수(мәгълүмат, эшләтү + 2);
        if (전체길이 < Башлама_озынлык || эшләтү + 전체길이 > мәгълүмат.length) {
            return false;
        }
        int бирем_VALUE_102996da = мәгълүмат[эшләтү + 9] & 0xff;
        int Эчтәлек_Start = эшләтү + Башлама_озынлык;
        int Эчтәлек_озынлык = 전체길이 - Башлама_озынлык;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(бирем_VALUE_102996da));
        if (직접처리기 != null) {
            직접처리기.Процесс_VALUE_кертү(мәгълүмат, Эчтәлек_Start, Эчтәлек_озынлык);
            return true;
        }
        if (Эчтәлек_озынлык < 4) {
            return false;
        }
        int 목적포트 = Челтәр_Кораллар.큰순서짧은정수(мәгълүмат, Эчтәлек_Start + 2);
        Map<Integer, 자료처리기> порт_таблица = бирем_VALUE_102996da == 17 ? 사용자자료단위처리기 : бирем_VALUE_102996da == 6 ? 전송제어처리기 : null;
        if (порт_таблица == null) {
            return false;
        }
        자료처리기 포트처리기 = порт_таблица.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Процесс_VALUE_кертү(мәгълүмат, Эчтәлек_Start, Эчтәлек_озынлык);
        return true;
    }
}

