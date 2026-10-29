// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Украіна.JUkrOS.Сетка_Стэк;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Сетка_слой {
    @FunctionalInterface
    public interface 자료처리기 {
        void Працэс_значэнне_увядзенне(byte[] дадзеныя, int Выканаць, int даўжыня_значэнне);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void рэгістраваць_пратакол_IP(int зварот_значэнне, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(зварот_значэнне & 0xff), 처리기);
    }

    public void рэгістраваць_карыстальнік_дадзеныя_урок(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] кадр_індэкс) {
        if (!Сетка_Інструменты.이더넷틀인가(кадр_індэкс)) {
            return false;
        }
        int 종류 = Сетка_Інструменты.이더넷상위규약(кадр_індэкс);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Працэс_значэнне_увядзенне(кадр_індэкс, 14, кадр_індэкс.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(кадр_індэкс, 14);
    }

    private boolean 상호통신망받기(byte[] дадзеныя, int Выканаць) {
        if (!Сетка_Інструменты.상호통신망규약사판인가(дадзеныя, Выканаць)) {
            return false;
        }
        int Загаловак_даўжыня = (дадзеныя[Выканаць] & 0x0f) * 4;
        int 전체길이 = Сетка_Інструменты.큰순서짧은정수(дадзеныя, Выканаць + 2);
        if (전체길이 < Загаловак_даўжыня || Выканаць + 전체길이 > дадзеныя.length) {
            return false;
        }
        int зварот_значэнне = дадзеныя[Выканаць + 9] & 0xff;
        int кантэнт_Пуск = Выканаць + Загаловак_даўжыня;
        int кантэнт_даўжыня = 전체길이 - Загаловак_даўжыня;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(зварот_значэнне));
        if (직접처리기 != null) {
            직접처리기.Працэс_значэнне_увядзенне(дадзеныя, кантэнт_Пуск, кантэнт_даўжыня);
            return true;
        }
        if (кантэнт_даўжыня < 4) {
            return false;
        }
        int прызначэнне_нумар_порта = Сетка_Інструменты.큰순서짧은정수(дадзеныя, кантэнт_Пуск + 2);
        Map<Integer, 자료처리기> порт_табліца = зварот_значэнне == 17 ? 사용자자료단위처리기 : зварот_значэнне == 6 ? 전송제어처리기 : null;
        if (порт_табліца == null) {
            return false;
        }
        자료처리기 포트처리기 = порт_табліца.get(Integer.valueOf(прызначэнне_нумар_порта));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Працэс_значэнне_увядзенне(дадзеныя, кантэнт_Пуск, кантэнт_даўжыня);
        return true;
    }
}

