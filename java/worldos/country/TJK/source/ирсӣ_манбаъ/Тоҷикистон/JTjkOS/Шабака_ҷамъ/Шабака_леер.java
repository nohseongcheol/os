// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Тоҷикистон.JTjkOS.Шабака_ҷамъ;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Шабака_леер {
    @FunctionalInterface
    public interface 자료처리기 {
        void Раванд_қимат_ворида(byte[] иттилоот, int порча, int дарозӣ_қимат);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void қайд_кардан_Итранет(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void қайд_кардан_Протоколи_интернет(int кор_қимат, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(кор_қимат & 0xff), 처리기);
    }

    public void қайд_кардан_корбар_иттилоот_дарс(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] чорчӯба_индекс) {
        if (!Шабака_Абзорҳо.이더넷틀인가(чорчӯба_индекс)) {
            return false;
        }
        int 종류 = Шабака_Абзорҳо.이더넷상위규약(чорчӯба_индекс);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Раванд_қимат_ворида(чорчӯба_индекс, 14, чорчӯба_индекс.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(чорчӯба_индекс, 14);
    }

    private boolean 상호통신망받기(byte[] иттилоот, int порча) {
        if (!Шабака_Абзорҳо.상호통신망규약사판인가(иттилоот, порча)) {
            return false;
        }
        int Сарнавор_дарозӣ = (иттилоот[порча] & 0x0f) * 4;
        int 전체길이 = Шабака_Абзорҳо.큰순서짧은정수(иттилоот, порча + 2);
        if (전체길이 < Сарнавор_дарозӣ || порча + 전체길이 > иттилоот.length) {
            return false;
        }
        int кор_қимат = иттилоот[порча + 9] & 0xff;
        int Мӯҳтаво_Оғоз = порча + Сарнавор_дарозӣ;
        int Мӯҳтаво_дарозӣ = 전체길이 - Сарнавор_дарозӣ;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(кор_қимат));
        if (직접처리기 != null) {
            직접처리기.Раванд_қимат_ворида(иттилоот, Мӯҳтаво_Оғоз, Мӯҳтаво_дарозӣ);
            return true;
        }
        if (Мӯҳтаво_дарозӣ < 4) {
            return false;
        }
        int 목적포트 = Шабака_Абзорҳо.큰순서짧은정수(иттилоот, Мӯҳтаво_Оғоз + 2);
        Map<Integer, 자료처리기> порт_ҷадвал = кор_қимат == 17 ? 사용자자료단위처리기 : кор_қимат == 6 ? 전송제어처리기 : null;
        if (порт_ҷадвал == null) {
            return false;
        }
        자료처리기 포트처리기 = порт_ҷадвал.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Раванд_қимат_ворида(иттилоот, Мӯҳтаво_Оғоз, Мӯҳтаво_дарозӣ);
        return true;
    }
}

