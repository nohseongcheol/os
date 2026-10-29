// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ประเทศไทย.JThaOS.ระบบแฟ้ม;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 แฟ้ม 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final ระบบแฟ้ม.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(ระบบแฟ้ม.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final ระบบแฟ้ม ระบบแฟ้ม;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(ระบบแฟ้ม ระบบแฟ้ม) {
        this.ระบบแฟ้ม = ระบบแฟ้ม;
    }

    public int เปิด(String ชื่อ) {
        ระบบแฟ้ม.열린파일 열린파일 = ระบบแฟ้ม.เปิด(ชื่อ);
        if (열린파일 == null) {
            return -2;
        }
        int ดัชนี = 빈번호(3);
        if (ดัชนี < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(ดัชนี), new 서술자(열린파일));
        return ดัชนี;
    }

    public int อ่าน(int ดัชนี, byte[] รับ_ปลายทาง, int ขนาด) {
        서술자 รายการ_ค่า = 서술자들.get(Integer.valueOf(ดัชนี));
        if (รายการ_ค่า == null) {
            return -9;
        }
        if (ขนาด < 0 || ขนาด > รับ_ปลายทาง.length) {
            return -22;
        }
        int 남음 = รายการ_ค่า.열린파일.ข้อมูล.length - รายการ_ค่า.열린파일.ตําแหน่ง;
        int 읽을크기 = Math.min(ขนาด, Math.max(남음, 0));
        System.arraycopy(รายการ_ค่า.열린파일.ข้อมูล, รายการ_ค่า.열린파일.ตําแหน่ง, รับ_ปลายทาง, 0, 읽을크기);
        รายการ_ค่า.열린파일.ตําแหน่ง += 읽을크기;
        return 읽을크기;
    }

    public int ขยับ_ตําแหน่ง(int ดัชนี, int 거리, int แสดง_ราก) {
        서술자 รายการ_ค่า = 서술자들.get(Integer.valueOf(ดัชนี));
        if (รายการ_ค่า == null) {
            return -9;
        }
        int พื้นหลัง_ค่า;
        if (แสดง_ราก == 0) {
            พื้นหลัง_ค่า = 0;
        } else if (แสดง_ราก == 1) {
            พื้นหลัง_ค่า = รายการ_ค่า.열린파일.ตําแหน่ง;
        } else if (แสดง_ราก == 2) {
            พื้นหลัง_ค่า = รายการ_ค่า.열린파일.ข้อมูล.length;
        } else {
            return -22;
        }
        int 새위치 = พื้นหลัง_ค่า + 거리;
        if (새위치 < 0) {
            return -22;
        }
        รายการ_ค่า.열린파일.ตําแหน่ง = 새위치;
        return 새위치;
    }

    public int ปิด(int ดัชนี) {
        서술자 รายการ_ค่า = 서술자들.remove(Integer.valueOf(ดัชนี));
        if (รายการ_ค่า == null) {
            return -9;
        }
        รายการ_ค่า.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int ดัชนี, int 최소번호) {
        서술자 รายการ_ค่า = 서술자들.get(Integer.valueOf(ดัชนี));
        if (รายการ_ค่า == null) {
            return -9;
        }
        int หมายเลขใหม่ = 빈번호(최소번호);
        if (หมายเลขใหม่ < 0) {
            return -24;
        }
        รายการ_ค่า.열린파일.참조수++;
        서술자들.put(Integer.valueOf(หมายเลขใหม่), new 서술자(รายการ_ค่า.열린파일));
        return หมายเลขใหม่;
    }

    public int 지정복제(int ดัชนี, int หมายเลขใหม่) {
        if (ดัชนี == หมายเลขใหม่) {
            return 서술자들.containsKey(Integer.valueOf(ดัชนี)) ? ดัชนี : -9;
        }
        if (หมายเลขใหม่ < 0 || หมายเลขใหม่ >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(ดัชนี));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(หมายเลขใหม่))) {
            ปิด(หมายเลขใหม่);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(หมายเลขใหม่), new 서술자(원본.열린파일));
        return หมายเลขใหม่;
    }

    public int 실행시닫기설정(int ดัชนี, boolean ค่า) {
        서술자 รายการ_ค่า = 서술자들.get(Integer.valueOf(ดัชนี));
        if (รายการ_ค่า == null) {
            return -9;
        }
        รายการ_ค่า.실행시닫기 = ค่า;
        return 0;
    }

    public int 실행시닫기값(int ดัชนี) {
        서술자 รายการ_ค่า = 서술자들.get(Integer.valueOf(ดัชนี));
        if (รายการ_ค่า == null) {
            return -9;
        }
        return รายการ_ค่า.실행시닫기 ? 1 : 0;
    }

    public แฟ้ม_ข้อมูล ข้อมูลระบบ(int ดัชนี) {
        if (ดัชนี >= 0 && ดัชนี <= 2) {
            return new แฟ้ม_ข้อมูล(0, 0020666);
        }
        서술자 รายการ_ค่า = 서술자들.get(Integer.valueOf(ดัชนี));
        if (รายการ_ค่า == null) {
            return null;
        }
        return new แฟ้ม_ข้อมูล(รายการ_ค่า.열린파일.ข้อมูล.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] หมายเลข_รายการ = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer ดัชนี : หมายเลข_รายการ) {
            서술자 รายการ_ค่า = 서술자들.get(ดัชนี);
            if (รายการ_ค่า != null && รายการ_ค่า.실행시닫기) {
                ปิด(ดัชนี.intValue());
            }
        }
    }

    public boolean เทคโนโลยีสารสนเทศ_เปิด(int ดัชนี) {
        return 서술자들.containsKey(Integer.valueOf(ดัชนี));
    }

    public 파일서술자표 ลอกแบบ_ค่า() {
        파일서술자표 ผลลัพธ์ = new 파일서술자표(ระบบแฟ้ม);
        for (Map.Entry<Integer, 서술자> รายการ_ค่า : 서술자들.entrySet()) {
            รายการ_ค่า.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(รายการ_ค่า.getValue().열린파일);
            새서술자.실행시닫기 = รายการ_ค่า.getValue().실행시닫기;
            ผลลัพธ์.서술자들.put(รายการ_ค่า.getKey(), 새서술자);
        }
        return ผลลัพธ์;
    }

    private int 빈번호(int 최소번호) {
        for (int ดัชนี = Math.max(0, 최소번호); ดัชนี < 최대서술자; ดัชนี++) {
            if (!서술자들.containsKey(Integer.valueOf(ดัชนี))) {
                return ดัชนี;
            }
        }
        return -1;
    }
}
