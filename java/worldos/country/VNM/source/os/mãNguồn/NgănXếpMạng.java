// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** IPv4/ARP/UDP tĩnh. Giữ tối đa bốn cổng truyền thông, mỗi cổng một thông điệp. */
public final class NgănXếpMạng {
    static final int địaChỉTựCó = 0xc0a80064; /* ip.conf:IP */
    static final int mặtNạMạng = 0xffffff00; /* ip.conf:NETMASK */
    static final int giáTrịCổngNối = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] khungĐầuVào = new int[1536], khungĐầuRa = new int[1536];
    static int[] cácCổng = new int[4], độDàiĐãNhận = new int[4], địaChỉĐãNhận = new int[4], sốCổngĐãNhận = new int[4];
    static int[] dữLiệuĐãNhận = new int[4096], thiếtBịĐãTìmThấy = new int[6];
    static int tìmĐếnĐịaChỉ = 0, địaChỉĐãTìmThấy = 0, giáTrịĐịnhDanh = 0, sốLượngĐãLoạiBỏ = 0;

    static int nguyên16(int[] chỉSốKhung, int vịTrí) { return (chỉSốKhung[vịTrí] << 8) | chỉSốKhung[vịTrí + 1]; }
    static int nguyên32(int[] chỉSốKhung, int vịTrí) { return (nguyên16(chỉSốKhung, vịTrí) << 16) | nguyên16(chỉSốKhung, vịTrí + 2); }
    static void đặt16Bit(int[] chỉSốKhung, int vịTrí, int giáTrị) { chỉSốKhung[vịTrí] = (giáTrị >>> 8) & 255; chỉSốKhung[vịTrí + 1] = giáTrị & 255; }
    static void đặt32Bit(int[] chỉSốKhung, int vịTrí, int giáTrị) { đặt16Bit(chỉSốKhung, vịTrí, giáTrị >>> 16); đặt16Bit(chỉSốKhung, vịTrí + 2, giáTrị); }
    static int giáTrịTổng(int[] chỉSốKhung, int chạy, int độDài, int giáTrị) {
        for (int sốHiệu = 0; sốHiệu < độDài; sốHiệu += 2)
            giáTrị += (chỉSốKhung[chạy + sốHiệu] << 8) | (sốHiệu + 1 < độDài ? chỉSốKhung[chạy + sốHiệu + 1] : 0);
        while ((giáTrị >>> 16) != 0) giáTrị = (giáTrị & 65535) + (giáTrị >>> 16);
        return giáTrị;
    }
    static int tổngKiểmĐầuMụcMôPhỏng(int giáTrịRờiĐi, int giáTrịĐến, int độDài) {
        return (giáTrịRờiĐi >>> 16) + (giáTrịRờiĐi & 65535) + (giáTrịĐến >>> 16) + (giáTrịĐến & 65535) + 17 + độDài;
    }

    static void tiếnTrìnhSạch() {
        for (int sốHiệu = 0; sốHiệu < 4; sốHiệu++) {
            cácCổng[sốHiệu] = 0; độDàiĐãNhận[sốHiệu] = -1; địaChỉĐãNhận[sốHiệu] = 0; sốCổngĐãNhận[sốHiệu] = 0;
        }
        for (int sốHiệu = 0; sốHiệu < 64; sốHiệu++) if (TrìnhĐiềuKhiểnMạng.nhận(khungĐầuVào) == 0) break;
    }
    static int sốHiệu(int giáTrịThẻXửLý) { return giáTrịThẻXửLý >= 3 && giáTrịThẻXửLý < 7 && cácCổng[giáTrịThẻXửLý - 3] != 0 ? giáTrịThẻXửLý - 3 : -1; }
    static int mở(int sốCổng) {
        if (TrìnhĐiềuKhiểnMạng.địaChỉCơSởVàoRa == 0) return -19;
        if (sốCổng < 0 || sốCổng > 65535) return -22;
        if (sốCổng != 0) for (int sốHiệu = 0; sốHiệu < 4; sốHiệu++) if (cácCổng[sốHiệu] == sốCổng) return -98;
        for (int sốHiệu = 0; sốHiệu < 4; sốHiệu++) if (cácCổng[sốHiệu] == 0) {
            if (sốCổng == 0) {
                sốCổng = 49152;
                boolean cácChồngLấn = true;
                while (cácChồngLấn) {
                    cácChồngLấn = false;
                    for (int giáTrịPhíaTrước = 0; giáTrịPhíaTrước < 4; giáTrịPhíaTrước++) if (cácCổng[giáTrịPhíaTrước] == sốCổng) cácChồngLấn = true;
                    if (cácChồngLấn) sốCổng++;
                }
            }
            cácCổng[sốHiệu] = sốCổng; độDàiĐãNhận[sốHiệu] = -1;
            return sốHiệu + 3;
        }
        return -24;
    }
    static int đóng(int giáTrịThẻXửLý) {
        int mụcÔ = sốHiệu(giáTrịThẻXửLý);
        if (mụcÔ < 0) return -9;
        cácCổng[mụcÔ] = 0; độDàiĐãNhận[mụcÔ] = -1;
        return 0;
    }
    static int địaChỉĐốiTác(int giáTrịThẻXửLý) { int mụcÔ = sốHiệu(giáTrịThẻXửLý); return mụcÔ < 0 ? -9 : địaChỉĐãNhận[mụcÔ]; }
    static int sốCổngĐốiTác(int giáTrịThẻXửLý) { int mụcÔ = sốHiệu(giáTrịThẻXửLý); return mụcÔ < 0 ? -9 : sốCổngĐãNhận[mụcÔ]; }

    static void đầuMụcPhíaNgoài(int giáTrịLoại, boolean giáTrịPhátQuảngBá) {
        for (int sốHiệu = 0; sốHiệu < 6; sốHiệu++) {
            khungĐầuRa[sốHiệu] = giáTrịPhátQuảngBá ? 255 : thiếtBịĐãTìmThấy[sốHiệu];
            khungĐầuRa[6 + sốHiệu] = TrìnhĐiềuKhiểnMạng.địaChỉThiếtBị[sốHiệu];
        }
        đặt16Bit(khungĐầuRa, 12, giáTrịLoại);
    }
    static void địaChỉYêuCầu(int giáTrịĐích) {
        đầuMụcPhíaNgoài(0x0806, true);
        đặt16Bit(khungĐầuRa, 14, 1); đặt16Bit(khungĐầuRa, 16, 0x0800);
        khungĐầuRa[18] = 6; khungĐầuRa[19] = 4; đặt16Bit(khungĐầuRa, 20, 1);
        for (int sốHiệu = 0; sốHiệu < 6; sốHiệu++) {
            khungĐầuRa[22 + sốHiệu] = TrìnhĐiềuKhiểnMạng.địaChỉThiếtBị[sốHiệu]; khungĐầuRa[32 + sốHiệu] = 0;
        }
        đặt32Bit(khungĐầuRa, 28, địaChỉTựCó); đặt32Bit(khungĐầuRa, 38, giáTrịĐích);
        TrìnhĐiềuKhiểnMạng.gửi(khungĐầuRa, 42);
    }
    static void địaChỉTiếnTrình(int độDài) {
        if (độDài < 42 || nguyên16(khungĐầuVào, 14) != 1 || nguyên16(khungĐầuVào, 16) != 0x0800
            || khungĐầuVào[18] != 6 || khungĐầuVào[19] != 4 || nguyên32(khungĐầuVào, 38) != địaChỉTựCó) { sốLượngĐãLoạiBỏ++; return; }
        int giáTrịLoại = nguyên16(khungĐầuVào, 20), giáTrịĐốiTác = nguyên32(khungĐầuVào, 28);
        if (giáTrịLoại == 2 && giáTrịĐốiTác == tìmĐếnĐịaChỉ) {
            for (int sốHiệu = 0; sốHiệu < 6; sốHiệu++) {
                if (khungĐầuVào[6 + sốHiệu] != khungĐầuVào[22 + sốHiệu] || khungĐầuVào[32 + sốHiệu] != TrìnhĐiềuKhiểnMạng.địaChỉThiếtBị[sốHiệu]) return;
            }
            for (int sốHiệu = 0; sốHiệu < 6; sốHiệu++) thiếtBịĐãTìmThấy[sốHiệu] = khungĐầuVào[22 + sốHiệu];
            địaChỉĐãTìmThấy = giáTrịĐốiTác;
        } else if (giáTrịLoại == 1) {
            đầuMụcPhíaNgoài(0x0806, false);
            đặt16Bit(khungĐầuRa, 14, 1); đặt16Bit(khungĐầuRa, 16, 0x0800);
            khungĐầuRa[18] = 6; khungĐầuRa[19] = 4; đặt16Bit(khungĐầuRa, 20, 2);
            for (int sốHiệu = 0; sốHiệu < 6; sốHiệu++) {
                khungĐầuRa[sốHiệu] = khungĐầuVào[22 + sốHiệu]; khungĐầuRa[32 + sốHiệu] = khungĐầuVào[22 + sốHiệu];
                khungĐầuRa[22 + sốHiệu] = TrìnhĐiềuKhiểnMạng.địaChỉThiếtBị[sốHiệu];
            }
            đặt32Bit(khungĐầuRa, 28, địaChỉTựCó); đặt32Bit(khungĐầuRa, 38, giáTrịĐốiTác);
            TrìnhĐiềuKhiểnMạng.gửi(khungĐầuRa, 42);
        }
    }

    static void khungTiếnTrình(int độDài) {
        if (độDài < 14 || độDài > khungĐầuVào.length) { sốLượngĐãLoạiBỏ++; return; }
        boolean thamChiếuBảnThân = true, giáTrịPhátQuảngBá = true;
        for (int sốHiệu = 0; sốHiệu < 6; sốHiệu++) {
            if (khungĐầuVào[sốHiệu] != TrìnhĐiềuKhiểnMạng.địaChỉThiếtBị[sốHiệu]) thamChiếuBảnThân = false;
            if (khungĐầuVào[sốHiệu] != 255) giáTrịPhátQuảngBá = false;
        }
        if (!thamChiếuBảnThân && !giáTrịPhátQuảngBá) return;
        if (nguyên16(khungĐầuVào, 12) == 0x0806) { địaChỉTiếnTrình(độDài); return; }
        if (nguyên16(khungĐầuVào, 12) != 0x0800) return;
        if (độDài < 34 || (khungĐầuVào[14] >>> 4) != 4) { sốLượngĐãLoạiBỏ++; return; }
        int độDàiĐầuMục = (khungĐầuVào[14] & 15) * 4, độDàiTổngCộng = nguyên16(khungĐầuVào, 16);
        if (độDàiĐầuMục < 20 || độDàiĐầuMục > 60 || độDàiTổngCộng < độDàiĐầuMục + 8 || độDàiTổngCộng > độDài - 14
            || (nguyên16(khungĐầuVào, 20) & 0x3fff) != 0 || khungĐầuVào[23] != 17
            || nguyên32(khungĐầuVào, 30) != địaChỉTựCó || giáTrịTổng(khungĐầuVào, 14, độDàiĐầuMục, 0) != 65535) { sốLượngĐãLoạiBỏ++; return; }
        int chạy = 14 + độDàiĐầuMục, độDàiDữLiệu = nguyên16(khungĐầuVào, chạy + 4);
        if (độDàiDữLiệu < 8 || độDàiDữLiệu != độDàiTổngCộng - độDàiĐầuMục || độDàiDữLiệu > 1032) { sốLượngĐãLoạiBỏ++; return; }
        int giáTrịRờiĐi = nguyên32(khungĐầuVào, 26);
        if (nguyên16(khungĐầuVào, chạy + 6) != 0 && giáTrịTổng(khungĐầuVào, chạy, độDàiDữLiệu, tổngKiểmĐầuMụcMôPhỏng(giáTrịRờiĐi, địaChỉTựCó, độDàiDữLiệu)) != 65535) {
            sốLượngĐãLoạiBỏ++; return;
        }
        int giáTrịĐích = nguyên16(khungĐầuVào, chạy + 2);
        for (int mụcÔ = 0; mụcÔ < 4; mụcÔ++) if (cácCổng[mụcÔ] != 0 && cácCổng[mụcÔ] == giáTrịĐích) {
            if (độDàiĐãNhận[mụcÔ] >= 0) { sốLượngĐãLoạiBỏ++; return; }
            độDàiĐãNhận[mụcÔ] = độDàiDữLiệu - 8; địaChỉĐãNhận[mụcÔ] = giáTrịRờiĐi; sốCổngĐãNhận[mụcÔ] = nguyên16(khungĐầuVào, chạy);
            for (int sốHiệu = 0; sốHiệu < độDàiDữLiệu - 8; sốHiệu++) dữLiệuĐãNhận[mụcÔ * 1024 + sốHiệu] = khungĐầuVào[chạy + 8 + sốHiệu];
            return;
        }
    }

    static void xácMinh() {
        for (int sốHiệu = 0; sốHiệu < 16; sốHiệu++) {
            int độDài = TrìnhĐiềuKhiểnMạng.nhận(khungĐầuVào);
            if (độDài == 0) return;
            khungTiếnTrình(độDài);
        }
    }
    static int tìmĐịaChỉ(int địaChỉ) {
        if (địaChỉ == 0 || địaChỉ == -1 || (địaChỉ >>> 28) >= 14 || (địaChỉ >>> 24) == 127 || địaChỉ == địaChỉTựCó) return -101;
        int phầnMụcKếTiếp = (địaChỉ & mặtNạMạng) == (địaChỉTựCó & mặtNạMạng) ? địaChỉ : giáTrịCổngNối;
        if (phầnMụcKếTiếp == địaChỉĐãTìmThấy) return 0;
        tìmĐếnĐịaChỉ = phầnMụcKếTiếp;
        int chạy = ThiếtBị.miliGiây(), yêuCầuKếTiếp = chạy;
        while (ThiếtBị.miliGiây() - chạy < 1000) {
            if (ThiếtBị.miliGiây() - yêuCầuKếTiếp >= 0) { địaChỉYêuCầu(phầnMụcKếTiếp); yêuCầuKếTiếp += 300; }
            xácMinh();
            if (địaChỉĐãTìmThấy == phầnMụcKếTiếp) return 0;
            ThiếtBị.nhườngNgắn();
        }
        return -110;
    }
    static int gửi(int giáTrịThẻXửLý, int địaChỉ, int sốCổng, int[] DữLiệu, int độDài) {
        int mụcÔ = sốHiệu(giáTrịThẻXửLý);
        if (mụcÔ < 0) return -9;
        if (TrìnhĐiềuKhiểnMạng.địaChỉCơSởVàoRa == 0) return -19;
        if (sốCổng < 1 || sốCổng > 65535 || độDài < 0 || độDài > 1024) return -22;
        int kếtQuả = tìmĐịaChỉ(địaChỉ);
        if (kếtQuả < 0) return kếtQuả;
        đầuMụcPhíaNgoài(0x0800, false);
        khungĐầuRa[14] = 0x45; khungĐầuRa[15] = 0; đặt16Bit(khungĐầuRa, 16, 28 + độDài);
        đặt16Bit(khungĐầuRa, 18, giáTrịĐịnhDanh++); đặt16Bit(khungĐầuRa, 20, 0x4000);
        khungĐầuRa[22] = 64; khungĐầuRa[23] = 17; đặt16Bit(khungĐầuRa, 24, 0);
        đặt32Bit(khungĐầuRa, 26, địaChỉTựCó); đặt32Bit(khungĐầuRa, 30, địaChỉ);
        đặt16Bit(khungĐầuRa, 24, ~giáTrịTổng(khungĐầuRa, 14, 20, 0));
        đặt16Bit(khungĐầuRa, 34, cácCổng[mụcÔ]); đặt16Bit(khungĐầuRa, 36, sốCổng);
        đặt16Bit(khungĐầuRa, 38, độDài + 8); đặt16Bit(khungĐầuRa, 40, 0);
        for (int sốHiệu = 0; sốHiệu < độDài; sốHiệu++) khungĐầuRa[42 + sốHiệu] = DữLiệu[sốHiệu] & 255;
        int tổngKiểm = (~giáTrịTổng(khungĐầuRa, 34, độDài + 8, tổngKiểmĐầuMụcMôPhỏng(địaChỉTựCó, địaChỉ, độDài + 8))) & 65535;
        đặt16Bit(khungĐầuRa, 40, tổngKiểm == 0 ? 65535 : tổngKiểm);
        kếtQuả = TrìnhĐiềuKhiểnMạng.gửi(khungĐầuRa, độDài + 42);
        return kếtQuả < 0 ? kếtQuả : độDài;
    }
    static int nhận(int giáTrịThẻXửLý, int[] DữLiệu, int giáTrịSứcChứa, int giáTrịGiớiHạn) {
        int mụcÔ = sốHiệu(giáTrịThẻXửLý);
        if (mụcÔ < 0) return -9;
        int chạy = ThiếtBị.miliGiây();
        while (true) {
            xácMinh();
            int độDài = độDàiĐãNhận[mụcÔ];
            if (độDài >= 0) {
                độDàiĐãNhận[mụcÔ] = -1;
                if (độDài > giáTrịSứcChứa) return -90;
                for (int sốHiệu = 0; sốHiệu < độDài; sốHiệu++) DữLiệu[sốHiệu] = dữLiệuĐãNhận[mụcÔ * 1024 + sốHiệu];
                return độDài;
            }
            if (giáTrịGiớiHạn == 0) return -11;
            if (ThiếtBị.miliGiây() - chạy >= giáTrịGiớiHạn) return -110;
            ThiếtBị.nhườngNgắn();
        }
    }
    static void giáTrịTrạngThái() {
        ĐầuCuốiVănBản.ghi(TrìnhĐiềuKhiểnMạng.địaChỉCơSởVàoRa == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        ĐầuCuốiVănBản.ghi("TX: "); ĐầuCuốiVănBản.ghiSố(TrìnhĐiềuKhiểnMạng.sốLượngTruyền);
        ĐầuCuốiVănBản.ghi(" RX: "); ĐầuCuốiVănBản.ghiSố(TrìnhĐiềuKhiểnMạng.nhậnSốLượng);
        ĐầuCuốiVănBản.ghi(" DROP: "); ĐầuCuốiVănBản.ghiSố(sốLượngĐãLoạiBỏ);
        ĐầuCuốiVănBản.ghi("\n");
    }
}
