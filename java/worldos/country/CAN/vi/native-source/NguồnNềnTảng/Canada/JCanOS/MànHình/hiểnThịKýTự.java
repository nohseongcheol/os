// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.MànHình;

import java.util.Arrays;

/** Mô hình màn hình 80x25 ký tự như chế độ văn bản VGA. */
public final class hiểnThịKýTự {
    public static final int giáTrịRộng = 80;
    public static final int giáTrịCao = 25;
    private final char[] cácGiáTrịKýTự = new char[giáTrịRộng * giáTrịCao];
    private int vịTríNgang;
    private int vịTríDọc;

    public hiểnThịKýTự() {
        xóaMục();
    }

    public void ĐầuRa(String giáTrịNộiDung) {
        for (int sốHiệu = 0; sốHiệu < giáTrịNộiDung.length(); sốHiệu++) {
            char KýTự = giáTrịNộiDung.charAt(sốHiệu);
            if (KýTự == '\n') {
                vịTríNgang = 0;
                vịTríDọc++;
            } else {
                inKýTự(vịTríNgang++, vịTríDọc, KýTự);
            }
            if (vịTríNgang >= giáTrịRộng) {
                vịTríNgang = 0;
                vịTríDọc++;
            }
            if (vịTríDọc >= giáTrịCao) {
                lênCuộn();
            }
        }
    }

    public char KýTự(int vịTríNgang, int vịTríDọc) {
        xácMinhVịTrí(vịTríNgang, vịTríDọc);
        return cácGiáTrịKýTự[vịTríDọc * giáTrịRộng + vịTríNgang];
    }

    public void xóaMục() {
        Arrays.fill(cácGiáTrịKýTự, ' ');
        vịTríNgang = 0;
        vịTríDọc = 0;
    }

    private void inKýTự(int vịTríNgang, int vịTríDọc, char KýTự) {
        xácMinhVịTrí(vịTríNgang, vịTríDọc);
        cácGiáTrịKýTự[vịTríDọc * giáTrịRộng + vịTríNgang] = KýTự;
    }

    private void lênCuộn() {
        System.arraycopy(cácGiáTrịKýTự, giáTrịRộng, cácGiáTrịKýTự, 0, giáTrịRộng * (giáTrịCao - 1));
        Arrays.fill(cácGiáTrịKýTự, giáTrịRộng * (giáTrịCao - 1), cácGiáTrịKýTự.length, ' ');
        vịTríDọc = giáTrịCao - 1;
    }

    private void xácMinhVịTrí(int vịTríNgang, int vịTríDọc) {
        if (vịTríNgang < 0 || vịTríNgang >= giáTrịRộng || vịTríDọc < 0 || vịTríDọc >= giáTrịCao) {
            throw new IllegalArgumentException("MànHình 위치가 올바르지 않습니다.");
        }
    }
}

