// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Tám tệp được giữ suốt phiên. Giữ tệp cũ khi sửa mã hay biên dịch thất bại. */
public final class HệTệpBộNhớ {
    static final int cỡTốiĐa = 16384;
    static int[] danhSáchCácTên = new int[8 * 64];
    static int[] danhSáchCỡ = new int[8];
    static int[] mởSốLượng = new int[8], cácQuyềnĐượcCấpQuyền = new int[8];
    static int[] tên = new int[64];
    static int[] giáTrịSửa = new int[cỡTốiĐa];
    static boolean làĐangSửa = false;
    static boolean giáTrịTràn = false;
    static int cỡSửa = 0;

    static boolean kiểmTraTên(int[] giáTrịKýTự, int độDài) {
        if (độDài < 1 || độDài > 63) return false;
        for (int trịSố = 0; trịSố < độDài; trịSố++) {
            int giáTrị = giáTrịKýTự[trịSố];
            if (!(giáTrị >= 'a' && giáTrị <= 'z') && !(giáTrị >= 'A' && giáTrị <= 'Z')
                && !(giáTrị >= '0' && giáTrị <= '9') && giáTrị != '_' && giáTrị != '-' && giáTrị != '.') return false;
        }
        return giáTrịKýTự[0] != '.';
    }

    static int tìmMục(int[] giáTrịKýTự, int độDài) {
        if (!kiểmTraTên(giáTrịKýTự, độDài)) return -22;
        for (int trịSố = 0; trịSố < 8; trịSố++) {
            boolean vănBảnBằng = danhSáchCácTên[trịSố * 64 + độDài] == 0;
            for (int mụcÔ = 0; mụcÔ < độDài; mụcÔ++) if (danhSáchCácTên[trịSố * 64 + mụcÔ] != giáTrịKýTự[mụcÔ]) vănBảnBằng = false;
            if (vănBảnBằng) return trịSố;
        }
        return -2;
    }

    static int giáTrịCất(int[] giáTrịKýTự, int độDài, int[] DữLiệu, int cỡ) {
        if (!kiểmTraTên(giáTrịKýTự, độDài) || cỡ < 0 || cỡ > DữLiệu.length) return -22;
        if (cỡ > cỡTốiĐa) return -90;
        int sốHiệu = tìmMục(giáTrịKýTự, độDài);
        if (sốHiệu == -2) {
            for (int trịSố = 0; trịSố < 8 && sốHiệu < 0; trịSố++) if (danhSáchCácTên[trịSố * 64] == 0 && mởSốLượng[trịSố] == 0) sốHiệu = trịSố;
            if (sốHiệu >= 0) cácQuyềnĐượcCấpQuyền[sốHiệu] = 438;
        }
        if (sốHiệu < 0) return -28;
        int địaChỉ = ThiếtBị.bộNhớTệp() + sốHiệu * cỡTốiĐa;
        for (int trịSố = 0; trịSố < cỡ; trịSố++) ThiếtBị.ghiBộNhớ(địaChỉ + trịSố, DữLiệu[trịSố]);
        for (int trịSố = 0; trịSố < 64; trịSố++) danhSáchCácTên[sốHiệu * 64 + trịSố] = trịSố < độDài ? giáTrịKýTự[trịSố] : 0;
        danhSáchCỡ[sốHiệu] = cỡ;
        return cỡ;
    }

    static void danhSáchMục() {
        for (int trịSố = 0; trịSố < 8; trịSố++) if (danhSáchCácTên[trịSố * 64] != 0) {
            for (int mụcÔ = 0; mụcÔ < 64 && danhSáchCácTên[trịSố * 64 + mụcÔ] != 0; mụcÔ++) ĐầuCuốiVănBản.KýTự(danhSáchCácTên[trịSố * 64 + mụcÔ]);
            ĐầuCuốiVănBản.ghi("  "); ĐầuCuốiVănBản.ghiSố(danhSáchCỡ[trịSố]); ĐầuCuốiVănBản.ghi("giáTrịByte\n");
        }
        ĐầuCuốiVănBản.ghi(KếtNốiLưuTrữ.làSẵnCó ? "Tệp 8칸, 파일당 16384바이트; sync로 giáTrịCất 장치에 보존\n"
            : "giáTrịTạm Tệp 8칸, 파일당 16384바이트; giáTrịThửLại 시작하면 사라짐\n");
    }

    static void lệnh(int[] giáTrịVào, int chạy, int độDài, int hànhĐộng) {
        while (chạy < độDài && giáTrịVào[chạy] == ' ') chạy++;
        int phầnKết = độDài;
        while (phầnKết > chạy && giáTrịVào[phầnKết - 1] == ' ') phầnKết--;
        int trịSố = phầnKết - chạy;
        if (trịSố < 1 || trịSố > 63) { ĐầuCuốiVănBản.ghi("올바르지 않은 Tệp tên\n"); return; }
        for (int mụcÔ = 0; mụcÔ < 64; mụcÔ++) tên[mụcÔ] = mụcÔ < trịSố ? giáTrịVào[chạy + mụcÔ] : 0;
        int sốHiệu = tìmMục(tên, trịSố);
        if (sốHiệu == -22) { ĐầuCuốiVănBản.ghi("올바르지 않은 Tệp tên\n"); return; }
        if (hànhĐộng == 0) {
            làĐangSửa = true; cỡSửa = 0; giáTrịTràn = false;
            ĐầuCuốiVănBản.ghi("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (sốHiệu < 0) ĐầuCuốiVănBản.ghi("파일을 찾을 trịSố 없습니다\n");
        else if (hànhĐộng == 1) {
            int địaChỉ = ThiếtBị.bộNhớTệp() + sốHiệu * cỡTốiĐa;
            for (int mụcÔ = 0; mụcÔ < danhSáchCỡ[sốHiệu]; mụcÔ++) ĐầuCuốiVănBản.KýTự(ThiếtBị.đọcBộNhớ(địaChỉ + mụcÔ));
            ĐầuCuốiVănBản.KýTự(10);
        } else { danhSáchCácTên[sốHiệu * 64] = 0; danhSáchCỡ[sốHiệu] = 0; ĐầuCuốiVănBản.ghi("파일을 지웠습니다\n"); }
    }

    static boolean làChínhXác(int[] giáTrịVào, int độDài, String giáTrịCụmTừ) {
        if (độDài != giáTrịCụmTừ.length()) return false;
        for (int mụcÔ = 0; mụcÔ < độDài; mụcÔ++) if (giáTrịVào[mụcÔ] != giáTrịCụmTừ.charAt(mụcÔ)) return false;
        return true;
    }

    static void dòngĐãSửa(int[] giáTrịVào, int độDài, boolean trànDòng) {
        if (làChínhXác(giáTrịVào, độDài, ".cancel")) {
            làĐangSửa = false; ĐầuCuốiVănBản.ghi("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (làChínhXác(giáTrịVào, độDài, ".save")) {
            làĐangSửa = false;
            if (giáTrịTràn) { ĐầuCuốiVănBản.ghi("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int trịSố = 0;
            while (trịSố < 64 && tên[trịSố] != 0) trịSố++;
            int kếtQuả = giáTrịCất(tên, trịSố, giáTrịSửa, cỡSửa);
            ĐầuCuốiVănBản.ghi(kếtQuả >= 0 ? "보존한 giáTrịByte trịSố: " : "보존 giáTrịSựThấtBại: ");
            ĐầuCuốiVănBản.ghiSố(kếtQuả); ĐầuCuốiVănBản.KýTự(10);
        } else if (trànDòng || độDài + 1 > cỡTốiĐa - cỡSửa) giáTrịTràn = true;
        else {
            for (int trịSố = 0; trịSố < độDài; trịSố++) giáTrịSửa[cỡSửa++] = giáTrịVào[trịSố];
            giáTrịSửa[cỡSửa++] = 10;
        }
    }

    static void VíDụ(String Tệp, String giáTrịNộiDung) {
        for (int trịSố = 0; trịSố < 64; trịSố++) tên[trịSố] = trịSố < Tệp.length() ? Tệp.charAt(trịSố) : 0;
        for (int trịSố = 0; trịSố < giáTrịNộiDung.length(); trịSố++) giáTrịSửa[trịSố] = giáTrịNộiDung.charAt(trịSố);
        giáTrịCất(tên, Tệp.length(), giáTrịSửa, giáTrịNộiDung.length());
    }

    static void chuẩnBị() {
        VíDụ("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int giáTrịNhóm = ThiếtBị.góiGộpTệpJava(), cỡ = ThiếtBị.cỡGóiGộpTệpJava();
        if (cỡ < 8 || QuảnLýThựcThi.trịSố(giáTrịNhóm) != 0x464a4b4a) { ĐầuCuốiVănBản.ghi("올바르지 않은 Java Tệp giáTrịNhóm\n"); return; }
        int sốLượngPhầnMục = QuảnLýThựcThi.trịSố(giáTrịNhóm + 4);
        if (sốLượngPhầnMục < 0 || sốLượngPhầnMục > 8 || sốLượngPhầnMục > (cỡ - 8) / 72) { ĐầuCuốiVănBản.ghi("올바르지 않은 Java Tệp danhSáchMục\n"); return; }
        for (int trịSố = 0; trịSố < sốLượngPhầnMục; trịSố++) {
            int giáTrịMục = giáTrịNhóm + 8 + trịSố * 72, độDài = 0;
            for (int mụcÔ = 0; mụcÔ < 64; mụcÔ++) tên[mụcÔ] = ThiếtBị.đọcBộNhớ(giáTrịMục + mụcÔ);
            while (độDài < 64 && tên[độDài] != 0) độDài++;
            int vịTrí = QuảnLýThựcThi.trịSố(giáTrịMục + 64), cỡTệp = QuảnLýThựcThi.trịSố(giáTrịMục + 68);
            if (!kiểmTraTên(tên, độDài) || cỡTệp < 0 || cỡTệp > cỡTốiĐa || vịTrí < 8 + sốLượngPhầnMục * 72 || vịTrí > cỡ - cỡTệp) {
                ĐầuCuốiVănBản.ghi("올바르지 않은 Java Tệp giáTrịMục\n"); return;
            }
            for (int mụcÔ = 0; mụcÔ < cỡTệp; mụcÔ++) giáTrịSửa[mụcÔ] = ThiếtBị.đọcBộNhớ(giáTrịNhóm + vịTrí + mụcÔ);
            if (giáTrịCất(tên, độDài, giáTrịSửa, cỡTệp) < 0) { ĐầuCuốiVănBản.ghi("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
