// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Україна.JUkrOS.мережа_Стіс;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP отримувати_значення_cef4d8ab 분배를 한곳에서 관리한다. */
public final class мережевий_рівень {
    @FunctionalInterface
    public interface 자료처리기 {
        void процес_значення_запис(byte[] дані, int запустити, int 길이);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void реєстр_протокол_Інтернету(int контракт_значення, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(контракт_значення & 0xff), 처리기);
    }

    public void реєстр_користувач_дані_урок(int обладнання_порт, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(обладнання_порт & 0xffff), 처리기);
    }

    public void 전송제어등록(int обладнання_порт, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(обладнання_порт & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] кадр_індекс) {
        if (!мережа_Інструменти.이더넷틀인가(кадр_індекс)) {
            return false;
        }
        int 종류 = мережа_Інструменти.이더넷상위규약(кадр_індекс);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.процес_значення_запис(кадр_індекс, 14, кадр_індекс.length - 14);
            return true;
        }
        return 종류 == 0x0800 && отримувати_хмара_пакет(кадр_індекс, 14);
    }

    private boolean отримувати_хмара_пакет(byte[] дані, int запустити) {
        if (!мережа_Інструменти.상호통신망규약사판인가(дані, запустити)) {
            return false;
        }
        int 머리길이 = (дані[запустити] & 0x0f) * 4;
        int 전체길이 = мережа_Інструменти.큰순서짧은정수(дані, запустити + 2);
        if (전체길이 < 머리길이 || запустити + 전체길이 > дані.length) {
            return false;
        }
        int контракт_значення = дані[запустити + 9] & 0xff;
        int Вміст_ПУСК = запустити + 머리길이;
        int 내용길이 = 전체길이 - 머리길이;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(контракт_значення));
        if (직접처리기 != null) {
            직접처리기.процес_значення_запис(дані, Вміст_ПУСК, 내용길이);
            return true;
        }
        if (내용길이 < 4) {
            return false;
        }
        int місце_номер_порту = мережа_Інструменти.큰순서짧은정수(дані, Вміст_ПУСК + 2);
        Map<Integer, 자료처리기> порт_таблиця = контракт_значення == 17 ? 사용자자료단위처리기 : контракт_значення == 6 ? 전송제어처리기 : null;
        if (порт_таблиця == null) {
            return false;
        }
        자료처리기 포트처리기 = порт_таблиця.get(Integer.valueOf(місце_номер_порту));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.процес_значення_запис(дані, Вміст_ПУСК, 내용길이);
        return true;
    }
}

