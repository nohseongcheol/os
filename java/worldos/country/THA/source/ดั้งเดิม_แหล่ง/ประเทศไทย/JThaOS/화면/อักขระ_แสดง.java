// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ประเทศไทย.JThaOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class อักขระ_แสดง {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int แนวตั้ง_ตําแหน่ง;

    public อักขระ_แสดง() {
        ลบ_รายการ();
    }

    public void ข้อความออก(String เนื้อหา_ค่า) {
        for (int ดัชนี = 0; ดัชนี < เนื้อหา_ค่า.length(); ดัชนี++) {
            char 문자 = เนื้อหา_ค่า.charAt(ดัชนี);
            if (문자 == '\n') {
                가로 = 0;
                แนวตั้ง_ตําแหน่ง++;
            } else {
                พิมพ์_อักขระ(가로++, แนวตั้ง_ตําแหน่ง, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                แนวตั้ง_ตําแหน่ง++;
            }
            if (แนวตั้ง_ตําแหน่ง >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int แนวตั้ง_ตําแหน่ง) {
        ยืนยัน_ตําแหน่ง(가로, แนวตั้ง_ตําแหน่ง);
        return 문자들[แนวตั้ง_ตําแหน่ง * 너비 + 가로];
    }

    public void ลบ_รายการ() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        แนวตั้ง_ตําแหน่ง = 0;
    }

    private void พิมพ์_อักขระ(int 가로, int แนวตั้ง_ตําแหน่ง, char 문자) {
        ยืนยัน_ตําแหน่ง(가로, แนวตั้ง_ตําแหน่ง);
        문자들[แนวตั้ง_ตําแหน่ง * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        แนวตั้ง_ตําแหน่ง = 높이 - 1;
    }

    private void ยืนยัน_ตําแหน่ง(int 가로, int แนวตั้ง_ตําแหน่ง) {
        if (가로 < 0 || 가로 >= 너비 || แนวตั้ง_ตําแหน่ง < 0 || แนวตั้ง_ตําแหน่ง >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

