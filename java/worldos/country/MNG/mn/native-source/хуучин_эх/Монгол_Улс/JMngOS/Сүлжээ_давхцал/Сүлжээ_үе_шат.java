// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Монгол_Улс.JMngOS.Сүлжээ_давхцал;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Сүлжээ_үе_шат {
    @FunctionalInterface
    public interface 자료처리기 {
        void үйл_явц_утга_оролт(byte[] өгөгдөл, int Ажиллуулах, int урт_утга);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void 상호통신망등록(int нөхцөл_байдал_утга, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(нөхцөл_байдал_утга & 0xff), 처리기);
    }

    public void 사용자자료단위등록(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] фрейм_индекс) {
        if (!Сүлжээ_Хэрэгслүүд.이더넷틀인가(фрейм_индекс)) {
            return false;
        }
        int 종류 = Сүлжээ_Хэрэгслүүд.이더넷상위규약(фрейм_индекс);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.үйл_явц_утга_оролт(фрейм_индекс, 14, фрейм_индекс.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(фрейм_индекс, 14);
    }

    private boolean 상호통신망받기(byte[] өгөгдөл, int Ажиллуулах) {
        if (!Сүлжээ_Хэрэгслүүд.상호통신망규약사판인가(өгөгдөл, Ажиллуулах)) {
            return false;
        }
        int Толгой_урт = (өгөгдөл[Ажиллуулах] & 0x0f) * 4;
        int 전체길이 = Сүлжээ_Хэрэгслүүд.큰순서짧은정수(өгөгдөл, Ажиллуулах + 2);
        if (전체길이 < Толгой_урт || Ажиллуулах + 전체길이 > өгөгдөл.length) {
            return false;
        }
        int нөхцөл_байдал_утга = өгөгдөл[Ажиллуулах + 9] & 0xff;
        int Агуулга_Эхлэл = Ажиллуулах + Толгой_урт;
        int Агуулга_урт = 전체길이 - Толгой_урт;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(нөхцөл_байдал_утга));
        if (직접처리기 != null) {
            직접처리기.үйл_явц_утга_оролт(өгөгдөл, Агуулга_Эхлэл, Агуулга_урт);
            return true;
        }
        if (Агуулга_урт < 4) {
            return false;
        }
        int 목적포트 = Сүлжээ_Хэрэгслүүд.큰순서짧은정수(өгөгдөл, Агуулга_Эхлэл + 2);
        Map<Integer, 자료처리기> порт_хүснэгт = нөхцөл_байдал_утга == 17 ? 사용자자료단위처리기 : нөхцөл_байдал_утга == 6 ? 전송제어처리기 : null;
        if (порт_хүснэгт == null) {
            return false;
        }
        자료처리기 포트처리기 = порт_хүснэгт.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.үйл_явц_утга_оролт(өгөгдөл, Агуулга_Эхлэл, Агуулга_урт);
        return true;
    }
}

