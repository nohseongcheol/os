// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hoa_Kỳ.JUsaOS.NgănXếpMạng;

/** Công cụ thứ tự byte và tổng kiểm dùng chung cho các lớp Ethernet/ARP/IPv4/ICMP/UDP. */
public final class CácCôngCụMạng {
    private CácCôngCụMạng() {
    }

    public static int ngắnKiểuThứTựByteLớn(byte[] DữLiệu, int vịTrí) {
        kiểmTraKhoảng(DữLiệu, vịTrí, 2);
        return ((DữLiệu[vịTrí] & 0xff) << 8) | (DữLiệu[vịTrí + 1] & 0xff);
    }

    public static long sốNguyênThứTựByteLớn(byte[] DữLiệu, int vịTrí) {
        kiểmTraKhoảng(DữLiệu, vịTrí, 4);
        return ((long) (DữLiệu[vịTrí] & 0xff) << 24)
                | ((long) (DữLiệu[vịTrí + 1] & 0xff) << 16)
                | ((long) (DữLiệu[vịTrí + 2] & 0xff) << 8)
                | (DữLiệu[vịTrí + 3] & 0xffL);
    }

    public static int tổngKiểmLiênMạng(byte[] DữLiệu, int chạy, int độDài) {
        kiểmTraKhoảng(DữLiệu, chạy, độDài);
        long giáTrịTổng = 0;
        int phầnKết = chạy + độDài;
        int vịTrí = chạy;
        while (vịTrí + 1 < phầnKết) {
            giáTrịTổng += ngắnKiểuThứTựByteLớn(DữLiệu, vịTrí);
            vịTrí += 2;
        }
        if (vịTrí < phầnKết) {
            giáTrịTổng += (DữLiệu[vịTrí] & 0xff) << 8;
        }
        while ((giáTrịTổng >>> 16) != 0) {
            giáTrịTổng = (giáTrịTổng & 0xffff) + (giáTrịTổng >>> 16);
        }
        return (int) (~giáTrịTổng) & 0xffff;
    }

    public static boolean làKhungEthernet(byte[] DữLiệu) {
        return DữLiệu != null && DữLiệu.length >= 14;
    }

    public static int giaoThứcThượngEthernet(byte[] DữLiệu) {
        if (!làKhungEthernet(DữLiệu)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return ngắnKiểuThứTựByteLớn(DữLiệu, 12);
    }

    public static boolean làGiaoThức4PhiênBảnIP(byte[] DữLiệu, int vịTrí) {
        if (DữLiệu == null || vịTrí < 0 || DữLiệu.length - vịTrí < 20) {
            return false;
        }
        int giáTrịPhiênBản = (DữLiệu[vịTrí] >>> 4) & 0xf;
        int độDàiĐầuMục = (DữLiệu[vịTrí] & 0xf) * 4;
        return giáTrịPhiênBản == 4 && độDàiĐầuMục >= 20 && DữLiệu.length - vịTrí >= độDàiĐầuMục;
    }

    private static void kiểmTraKhoảng(byte[] DữLiệu, int chạy, int độDài) {
        if (DữLiệu == null || chạy < 0 || độDài < 0 || chạy > DữLiệu.length - độDài) {
            throw new IllegalArgumentException("NgănXếpMạng DữLiệu 범위를 벗어났습니다.");
        }
    }
}

