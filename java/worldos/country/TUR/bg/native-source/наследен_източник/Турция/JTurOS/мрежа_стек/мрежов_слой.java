// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Турция.JTurOS.мрежа_стек;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP получавам_стойност_cef4d8ab 분배를 한곳에서 관리한다. */
public final class мрежов_слой {
    @FunctionalInterface
    public interface 자료처리기 {
        void Процес_стойност_запис(byte[] данни, int Стартиране, int 길이);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void регистър_Интернет_протокол(int случай_стойност, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(случай_стойност & 0xff), 처리기);
    }

    public void регистър_потребител_данни_урок(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] каре_индекс) {
        if (!мрежа_Инструменти.이더넷틀인가(каре_индекс)) {
            return false;
        }
        int 종류 = мрежа_Инструменти.이더넷상위규약(каре_индекс);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Процес_стойност_запис(каре_индекс, 14, каре_индекс.length - 14);
            return true;
        }
        return 종류 == 0x0800 && получавам_облак_пакет(каре_индекс, 14);
    }

    private boolean получавам_облак_пакет(byte[] данни, int Стартиране) {
        if (!мрежа_Инструменти.상호통신망규약사판인가(данни, Стартиране)) {
            return false;
        }
        int 머리길이 = (данни[Стартиране] & 0x0f) * 4;
        int 전체길이 = мрежа_Инструменти.큰순서짧은정수(данни, Стартиране + 2);
        if (전체길이 < 머리길이 || Стартиране + 전체길이 > данни.length) {
            return false;
        }
        int случай_стойност = данни[Стартиране + 9] & 0xff;
        int Съдържание_Старт = Стартиране + 머리길이;
        int 내용길이 = 전체길이 - 머리길이;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(случай_стойност));
        if (직접처리기 != null) {
            직접처리기.Процес_стойност_запис(данни, Съдържание_Старт, 내용길이);
            return true;
        }
        if (내용길이 < 4) {
            return false;
        }
        int местоназначение_номер_на_порт = мрежа_Инструменти.큰순서짧은정수(данни, Съдържание_Старт + 2);
        Map<Integer, 자료처리기> порт_таблица = случай_стойност == 17 ? 사용자자료단위처리기 : случай_стойност == 6 ? 전송제어처리기 : null;
        if (порт_таблица == null) {
            return false;
        }
        자료처리기 포트처리기 = порт_таблица.get(Integer.valueOf(местоназначение_номер_на_порт));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Процес_стойност_запис(данни, Съдържание_Старт, 내용길이);
        return true;
    }
}

