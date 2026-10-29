// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Албанија.JAlbOS.Мрежа_Купче;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Мрежа_слој {
    @FunctionalInterface
    public interface 자료처리기 {
        void Процес_VALUE_внес(byte[] податоци, int Изврши_2, int должина_VALUE);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void регистрирај_Етернет(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void регистрирај_ИП(int задача_VALUE_102996da, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(задача_VALUE_102996da & 0xff), 처리기);
    }

    public void регистрирај_корисник_податоци_единици(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void регистрирај_пренос_контрола(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] врами_INDEX) {
        if (!Мрежа_Алатки.информатичка_технологија_Етернет_врами(врами_INDEX)) {
            return false;
        }
        int 종류 = Мрежа_Алатки.Етернет_UPPER_протокол(врами_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Процес_VALUE_внес(врами_INDEX, 14, врами_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(врами_INDEX, 14);
    }

    private boolean 상호통신망받기(byte[] податоци, int Изврши_2) {
        if (!Мрежа_Алатки.상호통신망규약사판인가(податоци, Изврши_2)) {
            return false;
        }
        int Заглавие_должина = (податоци[Изврши_2] & 0x0f) * 4;
        int 전체길이 = Мрежа_Алатки.큰순서짧은정수(податоци, Изврши_2 + 2);
        if (전체길이 < Заглавие_должина || Изврши_2 + 전체길이 > податоци.length) {
            return false;
        }
        int задача_VALUE_102996da = податоци[Изврши_2 + 9] & 0xff;
        int Содржина_Start = Изврши_2 + Заглавие_должина;
        int Содржина_должина = 전체길이 - Заглавие_должина;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(задача_VALUE_102996da));
        if (직접처리기 != null) {
            직접처리기.Процес_VALUE_внес(податоци, Содржина_Start, Содржина_должина);
            return true;
        }
        if (Содржина_должина < 4) {
            return false;
        }
        int одредиште_број_на_порта = Мрежа_Алатки.큰순서짧은정수(податоци, Содржина_Start + 2);
        Map<Integer, 자료처리기> порта_табела = задача_VALUE_102996da == 17 ? 사용자자료단위처리기 : задача_VALUE_102996da == 6 ? 전송제어처리기 : null;
        if (порта_табела == null) {
            return false;
        }
        자료처리기 포트처리기 = порта_табела.get(Integer.valueOf(одредиште_број_на_порта));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Процес_VALUE_внес(податоци, Содржина_Start, Содржина_должина);
        return true;
    }
}

