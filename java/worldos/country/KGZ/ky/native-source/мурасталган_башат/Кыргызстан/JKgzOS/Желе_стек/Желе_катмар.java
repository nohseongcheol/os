// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Кыргызстан.JKgzOS.Желе_стек;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Желе_катмар {
    @FunctionalInterface
    public interface 자료처리기 {
        void Процесс_маани_киргизме_жазуу(byte[] берилмелер, int Жүргүзүү, int узундук_маани);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void 상호통신망등록(int иш_маани, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(иш_маани & 0xff), 처리기);
    }

    public void 사용자자료단위등록(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] кадр_индекс) {
        if (!Желе_Куралдар.이더넷틀인가(кадр_индекс)) {
            return false;
        }
        int 종류 = Желе_Куралдар.이더넷상위규약(кадр_индекс);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Процесс_маани_киргизме_жазуу(кадр_индекс, 14, кадр_индекс.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(кадр_индекс, 14);
    }

    private boolean 상호통신망받기(byte[] берилмелер, int Жүргүзүү) {
        if (!Желе_Куралдар.상호통신망규약사판인가(берилмелер, Жүргүзүү)) {
            return false;
        }
        int баш_аты_узундук = (берилмелер[Жүргүзүү] & 0x0f) * 4;
        int 전체길이 = Желе_Куралдар.큰순서짧은정수(берилмелер, Жүргүзүү + 2);
        if (전체길이 < баш_аты_узундук || Жүргүзүү + 전체길이 > берилмелер.length) {
            return false;
        }
        int иш_маани = берилмелер[Жүргүзүү + 9] & 0xff;
        int Мазмун_Баштоо = Жүргүзүү + баш_аты_узундук;
        int Мазмун_узундук = 전체길이 - баш_аты_узундук;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(иш_маани));
        if (직접처리기 != null) {
            직접처리기.Процесс_маани_киргизме_жазуу(берилмелер, Мазмун_Баштоо, Мазмун_узундук);
            return true;
        }
        if (Мазмун_узундук < 4) {
            return false;
        }
        int 목적포트 = Желе_Куралдар.큰순서짧은정수(берилмелер, Мазмун_Баштоо + 2);
        Map<Integer, 자료처리기> порт_жадыбал = иш_маани == 17 ? 사용자자료단위처리기 : иш_маани == 6 ? 전송제어처리기 : null;
        if (порт_жадыбал == null) {
            return false;
        }
        자료처리기 포트처리기 = порт_жадыбал.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Процесс_маани_киргизме_жазуу(берилмелер, Мазмун_Баштоо, Мазмун_узундук);
        return true;
    }
}

