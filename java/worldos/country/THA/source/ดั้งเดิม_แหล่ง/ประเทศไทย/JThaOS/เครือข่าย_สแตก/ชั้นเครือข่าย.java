// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ประเทศไทย.JThaOS.เครือข่าย_สแตก;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP รับ_ค่า 분배를 한곳에서 관리한다. */
public final class ชั้นเครือข่าย {
    @FunctionalInterface
    public interface 자료처리기 {
        void กระบวนการ_ค่า_รายการ(byte[] ข้อมูล, int เรียกใช้งาน, int 길이);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void ทะเบียน_อีเทอร์เน็ต(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void ทะเบียน_อินเทอร์เน็ตโปรโตคอล(int มูลค่าตามสัญญา, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(มูลค่าตามสัญญา & 0xff), 처리기);
    }

    public void ทะเบียน_ผู้ใช้_ข้อมูล_หน่วย(int ฮาร์ดแวร์_แปลง, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(ฮาร์ดแวร์_แปลง & 0xffff), 처리기);
    }

    public void 전송제어등록(int ฮาร์ดแวร์_แปลง, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(ฮาร์ดแวร์_แปลง & 0xffff), 처리기);
    }

    public boolean รับ_อีเทอร์เน็ต(byte[] กรอบ_ดัชนี) {
        if (!เครือข่าย_เครื่องมือ.เทคโนโลยีสารสนเทศ_อีเทอร์เน็ต_กรอบ(กรอบ_ดัชนี)) {
            return false;
        }
        int 종류 = เครือข่าย_เครื่องมือ.이더넷상위규약(กรอบ_ดัชนี);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.กระบวนการ_ค่า_รายการ(กรอบ_ดัชนี, 14, กรอบ_ดัชนี.length - 14);
            return true;
        }
        return 종류 == 0x0800 && รับ_คลาวด์_แพคเก็ต(กรอบ_ดัชนี, 14);
    }

    private boolean รับ_คลาวด์_แพคเก็ต(byte[] ข้อมูล, int เรียกใช้งาน) {
        if (!เครือข่าย_เครื่องมือ.เทคโนโลยีสารสนเทศ_วัคซีนป้องกันโปลิโอ_4_โพรโทคอล(ข้อมูล, เรียกใช้งาน)) {
            return false;
        }
        int 머리길이 = (ข้อมูล[เรียกใช้งาน] & 0x0f) * 4;
        int 전체길이 = เครือข่าย_เครื่องมือ.큰순서짧은정수(ข้อมูล, เรียกใช้งาน + 2);
        if (전체길이 < 머리길이 || เรียกใช้งาน + 전체길이 > ข้อมูล.length) {
            return false;
        }
        int มูลค่าตามสัญญา = ข้อมูล[เรียกใช้งาน + 9] & 0xff;
        int เนื้อหา_เริ่ม = เรียกใช้งาน + 머리길이;
        int 내용길이 = 전체길이 - 머리길이;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(มูลค่าตามสัญญา));
        if (직접처리기 != null) {
            직접처리기.กระบวนการ_ค่า_รายการ(ข้อมูล, เนื้อหา_เริ่ม, 내용길이);
            return true;
        }
        if (내용길이 < 4) {
            return false;
        }
        int ปลายทาง_หมายเลขพอร์ต = เครือข่าย_เครื่องมือ.큰순서짧은정수(ข้อมูล, เนื้อหา_เริ่ม + 2);
        Map<Integer, 자료처리기> แปลง_ตาราง = มูลค่าตามสัญญา == 17 ? 사용자자료단위처리기 : มูลค่าตามสัญญา == 6 ? 전송제어처리기 : null;
        if (แปลง_ตาราง == null) {
            return false;
        }
        자료처리기 포트처리기 = แปลง_ตาราง.get(Integer.valueOf(ปลายทาง_หมายเลขพอร์ต));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.กระบวนการ_ค่า_รายการ(ข้อมูล, เนื้อหา_เริ่ม, 내용길이);
        return true;
    }
}

