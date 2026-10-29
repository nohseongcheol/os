// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Sinh mã C cho nhân ARM64 độc lập từ tệp lớp Java. Chạy trên JDK của máy chủ. */
public final class BiênDịchTrước {
    static final class LỗiBảnDịch extends RuntimeException {
        LỗiBảnDịch(String môTả) { super(môTả); }
    }
    static final class BộĐọcDữLiệu {
        final byte[] DữLiệu;
        int vịTrí;
        BộĐọcDữLiệu(byte[] dữLiệuĐầuVào) { DữLiệu = dữLiệuĐầuVào; }
        byte[] đọc(int độDài) {
            if (độDài < 0 || độDài > DữLiệu.length - vịTrí) throw new LỗiBảnDịch("giáTrịĐãCắtXén giáTrịLớp 또는 lệnh DữLiệu");
            byte[] kếtQuả = Arrays.copyOfRange(DữLiệu, vịTrí, vịTrí + độDài); vịTrí += độDài; return kếtQuả;
        }
        int đọcByte() { if (vịTrí >= DữLiệu.length) throw new LỗiBảnDịch("giáTrịĐãCắtXén lệnh DữLiệu"); return DữLiệu[vịTrí++] & 255; }
        int đọcNgắnKiểu() { return (đọcByte() << 8) | đọcByte(); }
        int đọcSốNguyênGọn() { return (đọcNgắnKiểu() << 16) | đọcNgắnKiểu(); }
        int đọcByteCóDấu() { return (byte) đọcByte(); }
        int đọcNgắnKiểuCóDấu() { return (short) đọcNgắnKiểu(); }
    }
    static final class DữLiệuThànhViên {
        final int mụcTruyCập;
        final String tên, giáTrịMôTả;
        final Map<String, byte[]> giáTrịThuộcTính;
        DữLiệuThànhViên(int giáTrịTruyCập, String giáTrịTên, String dữLiệuBộMôTả, Map<String, byte[]> dữLiệuThuộcTính) {
            mụcTruyCập = giáTrịTruyCập; tên = giáTrịTên; giáTrịMôTả = dữLiệuBộMôTả; giáTrịThuộcTính = dữLiệuThuộcTính;
        }
    }
    static final class ThamChiếuPhươngThức implements Comparable<ThamChiếuPhươngThức> {
        final String giáTrịChủSởHữu, tên, giáTrịMôTả;
        ThamChiếuPhươngThức(String giáTrịThuộcDựÁn, String giáTrịTên, String dữLiệuBộMôTả) { giáTrịChủSởHữu = giáTrịThuộcDựÁn; tên = giáTrịTên; giáTrịMôTả = dữLiệuBộMôTả; }
        String[] cácPhần() { return new String[]{giáTrịChủSởHữu, tên, giáTrịMôTả}; }
        public int compareTo(ThamChiếuPhươngThức giáTrịĐốiTác) {
            int giáTrịPhépSoSánh = giáTrịChủSởHữu.compareTo(giáTrịĐốiTác.giáTrịChủSởHữu);
            if (giáTrịPhépSoSánh == 0) giáTrịPhépSoSánh = tên.compareTo(giáTrịĐốiTác.tên);
            return giáTrịPhépSoSánh == 0 ? giáTrịMôTả.compareTo(giáTrịĐốiTác.giáTrịMôTả) : giáTrịPhépSoSánh;
        }
        public boolean equals(Object giáTrịĐốiTác) { return giáTrịĐốiTác instanceof ThamChiếuPhươngThức && compareTo((ThamChiếuPhươngThức) giáTrịĐốiTác) == 0; }
        public int hashCode() { return Objects.hash(giáTrịChủSởHữu, tên, giáTrịMôTả); }
    }
    static final class DữLiệuLớp {
        final int[] loạiHằng;
        final Object[] dữLiệuHằng;
        final String tên;
        final List<DữLiệuThànhViên> giáTrịTrường, Hàm;
        DữLiệuLớp(Path đườngDẫn) throws IOException {
            BộĐọcDữLiệu giáTrịBộĐọc = new BộĐọcDữLiệu(Files.readAllBytes(đườngDẫn));
            if (giáTrịBộĐọc.đọcSốNguyênGọn() != 0xcafebabe) throw new LỗiBảnDịch("Java giáTrịLớp 표식이 아님");
            giáTrịBộĐọc.đọc(4);
            int sốLượngPhầnMục = giáTrịBộĐọc.đọcNgắnKiểu(); loạiHằng = new int[sốLượngPhầnMục]; dữLiệuHằng = new Object[sốLượngPhầnMục];
            for (int chỉSốThứBậc = 1; chỉSốThứBậc < sốLượngPhầnMục; chỉSốThứBậc++) {
                int giáTrịLoại = giáTrịBộĐọc.đọcByte(); loạiHằng[chỉSốThứBậc] = giáTrịLoại;
                switch (giáTrịLoại) {
                    case 1:
                        int độDài = giáTrịBộĐọc.đọcNgắnKiểu();
                        byte[] bộĐệmKýTự = giáTrịBộĐọc.đọc(độDài), dữLiệuCóTiềnTốĐộDài = new byte[độDài + 2];
                        dữLiệuCóTiềnTốĐộDài[0] = (byte)(độDài >> 8); dữLiệuCóTiềnTốĐộDài[1] = (byte)độDài;
                        System.arraycopy(bộĐệmKýTự, 0, dữLiệuCóTiềnTốĐộDài, 2, độDài);
                        dữLiệuHằng[chỉSốThứBậc] = new DataInputStream(new ByteArrayInputStream(dữLiệuCóTiềnTốĐộDài)).readUTF(); break;
                    case 3: dữLiệuHằng[chỉSốThứBậc] = giáTrịBộĐọc.đọcSốNguyênGọn(); break;
                    case 4: giáTrịBộĐọc.đọc(4); break;
                    case 5: case 6: giáTrịBộĐọc.đọc(8); chỉSốThứBậc++; break;
                    case 7: case 8: case 16: dữLiệuHằng[chỉSốThứBậc] = giáTrịBộĐọc.đọcNgắnKiểu(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        dữLiệuHằng[chỉSốThứBậc] = new int[]{giáTrịBộĐọc.đọcNgắnKiểu(), giáTrịBộĐọc.đọcNgắnKiểu()}; break;
                    case 15: dữLiệuHằng[chỉSốThứBậc] = new int[]{giáTrịBộĐọc.đọcByte(), giáTrịBộĐọc.đọcNgắnKiểu()}; break;
                    default: throw new LỗiBảnDịch("지원하지 않는 giáTrịHằng giáTrịLoại: " + giáTrịLoại);
                }
            }
            giáTrịBộĐọc.đọcNgắnKiểu(); tên = tênLớp(giáTrịBộĐọc.đọcNgắnKiểu());
            if (!tênLớp(giáTrịBộĐọc.đọcNgắnKiểu()).equals("java/lang/Object") || giáTrịBộĐọc.đọcNgắnKiểu() != 0)
                throw new LỗiBảnDịch(tên + ": 상속 및 인터페이스 làKhôngHỗTrợ");
            giáTrịTrường = đọcCácThànhViên(giáTrịBộĐọc); Hàm = đọcCácThànhViên(giáTrịBộĐọc); đọcCácThuộcTính(giáTrịBộĐọc);
            if (giáTrịBộĐọc.vịTrí != giáTrịBộĐọc.DữLiệu.length) throw new LỗiBảnDịch("giáTrịLớp 뒤에 남은 DữLiệu");
        }
        String KýTự(int sốHiệu) {
            if (sốHiệu < 1 || sốHiệu >= loạiHằng.length || loạiHằng[sốHiệu] != 1) throw new LỗiBảnDịch("KýTự giáTrịHằng sốHiệu lỗi");
            return (String) dữLiệuHằng[sốHiệu];
        }
        String tênLớp(int sốHiệu) {
            if (sốHiệu < 1 || sốHiệu >= loạiHằng.length || loạiHằng[sốHiệu] != 7) throw new LỗiBảnDịch("giáTrịLớp thamChiếu lỗi");
            return KýTự((Integer)dữLiệuHằng[sốHiệu]);
        }
        ThamChiếuPhươngThức thamChiếu(int sốHiệu) {
            if (sốHiệu < 1 || sốHiệu >= loạiHằng.length || loạiHằng[sốHiệu] < 9 || loạiHằng[sốHiệu] > 11) throw new LỗiBảnDịch("멤버 thamChiếu lỗi");
            int[] giáTrịCặp = (int[])dữLiệuHằng[sốHiệu], cặpTên = (int[])dữLiệuHằng[giáTrịCặp[1]];
            return new ThamChiếuPhươngThức(tênLớp(giáTrịCặp[0]), KýTự(cặpTên[0]), KýTự(cặpTên[1]));
        }
        Map<String, byte[]> đọcCácThuộcTính(BộĐọcDữLiệu giáTrịBộĐọc) {
            Map<String, byte[]> kếtQuả = new LinkedHashMap<>();
            int sốLượngPhầnMục = giáTrịBộĐọc.đọcNgắnKiểu();
            for (int chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngPhầnMục; chỉSốThứBậc++) {
                String tênThuộcTính = KýTự(giáTrịBộĐọc.đọcNgắnKiểu()); byte[] giáTrị = giáTrịBộĐọc.đọc(giáTrịBộĐọc.đọcSốNguyênGọn());
                if (kếtQuả.put(tênThuộcTính, giáTrị) != null) throw new LỗiBảnDịch("겹친 giáTrịThuộcTính: " + tênThuộcTính);
            }
            return kếtQuả;
        }
        List<DữLiệuThànhViên> đọcCácThànhViên(BộĐọcDữLiệu giáTrịBộĐọc) {
            List<DữLiệuThànhViên> kếtQuả = new ArrayList<>(); int sốLượngPhầnMục = giáTrịBộĐọc.đọcNgắnKiểu();
            for (int chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngPhầnMục; chỉSốThứBậc++) {
                int mụcTruyCập = giáTrịBộĐọc.đọcNgắnKiểu(); String tênMụcPhươngThức = KýTự(giáTrịBộĐọc.đọcNgắnKiểu()), giáTrịMôTả = KýTự(giáTrịBộĐọc.đọcNgắnKiểu());
                kếtQuả.add(new DữLiệuThànhViên(mụcTruyCập, tênMụcPhươngThức, giáTrịMôTả, đọcCácThuộcTính(giáTrịBộĐọc)));
            }
            return kếtQuả;
        }
    }
    static final class BộMôTảPhươngThức {
        final List<String> cácĐốiSố = new ArrayList<>();
        final String kếtQuảTrảVề;
        BộMôTảPhươngThức(String giáTrịMôTả) {
            if (!giáTrịMôTả.startsWith("(")) throw new LỗiBảnDịch("Hàm giáTrịMôTả lỗi: " + giáTrịMôTả);
            int phầnKết = giáTrịMôTả.indexOf(')'); if (phầnKết < 0) throw new LỗiBảnDịch("Hàm giáTrịMôTả lỗi: " + giáTrịMôTả);
            cácĐốiSố.addAll(phânTíchCúPhápCácKiểu(giáTrịMôTả.substring(1, phầnKết)));
            List<String> cácGiáTrịĐãTrảVề = phânTíchCúPhápCácKiểu(giáTrịMôTả.substring(phầnKết + 1));
            if (cácĐốiSố.contains("V") || cácGiáTrịĐãTrảVề.size() != 1) throw new LỗiBảnDịch("Hàm giáTrịMôTả lỗi: " + giáTrịMôTả);
            kếtQuảTrảVề = cácGiáTrịĐãTrảVề.get(0);
        }
    }
    static List<String> phânTíchCúPhápCácKiểu(String giáTrịMôTả) {
        List<String> kếtQuả = new ArrayList<>();
        String[] địnhDạngĐượcPhép = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int vịTrí = 0; vịTrí < giáTrịMôTả.length();) {
            String giáTrịViệcChọn = null;
            for (String giáTrịĐịnhDạng : địnhDạngĐượcPhép) if (giáTrịMôTả.startsWith(giáTrịĐịnhDạng, vịTrí)) { giáTrịViệcChọn = giáTrịĐịnhDạng; break; }
            if (giáTrịViệcChọn == null) throw new LỗiBảnDịch("지원하지 않는 kiểuDữLiệu: " + giáTrịMôTả);
            kếtQuả.add(giáTrịViệcChọn); vịTrí += giáTrịViệcChọn.length();
        }
        return kếtQuả;
    }
    static String kýHiệu(String giáTrịLoại, String... cácPhần) {
        try {
            byte[] tệpMãBăm = MessageDigest.getInstance("SHA-256").digest(String.join("\0", cácPhần).getBytes(StandardCharsets.UTF_8));
            StringBuilder vănBản = new StringBuilder("j_" + giáTrịLoại + "_");
            for (int chỉSốThứBậc = 0; chỉSốThứBậc < 12; chỉSốThứBậc++) vănBản.append(String.format(Locale.ROOT, "%02x", tệpMãBăm[chỉSốThứBậc] & 255));
            return vănBản.toString();
        } catch (Exception lỗi) { throw new LỗiBảnDịch(lỗi.toString()); }
    }
    final Map<String, DữLiệuLớp> danhSáchCácLớp = new TreeMap<>();
    final Map<ThamChiếuPhươngThức, DữLiệuThànhViên> danhSáchCácPhươngThức = new TreeMap<>(), danhSáchCácTrường = new TreeMap<>();
    final Map<String, String> cácGiáTrịChuỗi = new LinkedHashMap<>(), cácHàmMáy = new LinkedHashMap<>();
    final String đốiĐíchViệcThựcThi, lớpMáy;
    final int sốLượngTừVùngNhớĐộng;
    final Path đườngDẫnTàiNguyên;
    BiênDịchTrước(List<Path> danhSáchĐườngDẫn, String giáTrịĐốiĐích, int sốLượngTừTừVựng, Path giáTrịTàiNguyên) throws IOException {
        if ((!giáTrịĐốiĐích.equals("kernel") && !giáTrịĐốiĐích.equals("user")) || sốLượngTừTừVựng < 1024 || sốLượngTừTừVựng > 1048576) throw new LỗiBảnDịch("thựcThiLệnh giáTrịĐốiĐích 또는 BộNhớ miềnĐịaChỉ cỡ lỗi");
        đốiĐíchViệcThựcThi = giáTrịĐốiĐích; sốLượngTừVùngNhớĐộng = sốLượngTừTừVựng; đườngDẫnTàiNguyên = giáTrịTàiNguyên;
        // Tên này cũng được dịch khi sinh mã nguồn cho từng quốc gia.
        lớpMáy = giáTrịĐốiĐích.equals("kernel") ? "BoMạch" : "NgườiDùng";
        for (String dòng : Files.readAllLines(giáTrịTàiNguyên.resolve("CácHàmMáy.tsv"), StandardCharsets.UTF_8)) {
            String[] cácPhần = dòng.split("\t", -1);
            if (cácPhần.length != 4) throw new LỗiBảnDịch("máy Hàm DữLiệu lỗi");
            if (cácPhần[0].equals(giáTrịĐốiĐích)) cácHàmMáy.put(cácPhần[1] + cácPhần[2], cácPhần[3]);
        }
        for (Path đườngDẫn : danhSáchĐườngDẫn) {
            DữLiệuLớp DữLiệu = new DữLiệuLớp(đườngDẫn);
            if (danhSáchCácLớp.put(DữLiệu.tên, DữLiệu) != null) throw new LỗiBảnDịch("중복 giáTrịLớp: " + DữLiệu.tên);
            for (DữLiệuThànhViên giáTrịTrường : DữLiệu.giáTrịTrường) {
                if ((giáTrịTrường.mụcTruyCập & 8) == 0 || phânTíchCúPhápCácKiểu(giáTrịTrường.giáTrịMôTả).equals(Collections.singletonList("V"))) throw new LỗiBảnDịch("giáTrịTĩnh 필드만 giáTrịHỗTrợ");
                if (danhSáchCácTrường.put(new ThamChiếuPhươngThức(DữLiệu.tên, giáTrịTrường.tên, giáTrịTrường.giáTrịMôTả), giáTrịTrường) != null) throw new LỗiBảnDịch("중복 giáTrịTrường");
            }
            for (DữLiệuThànhViên Hàm : DữLiệu.Hàm) {
                if (Hàm.tên.equals("<init>")) continue;
                if ((Hàm.mụcTruyCập & 8) == 0 || (Hàm.mụcTruyCập & (0x20 | 0x400)) != 0) throw new LỗiBảnDịch("giáTrịTĩnh 비동기화 함수만 giáTrịHỗTrợ");
                new BộMôTảPhươngThức(Hàm.giáTrịMôTả);
                if (danhSáchCácPhươngThức.put(new ThamChiếuPhươngThức(DữLiệu.tên, Hàm.tên, Hàm.giáTrịMôTả), Hàm) != null) throw new LỗiBảnDịch("중복 Hàm");
            }
        }
    }
    String kýHiệuChuỗi(String vănBản) { return cácGiáTrịChuỗi.computeIfAbsent(vănBản, giáTrị -> "j_text_" + cácGiáTrịChuỗi.size()); }
    String biểuThứcHằng(DữLiệuLớp DữLiệu, int sốHiệu) {
        if (sốHiệu < 1 || sốHiệu >= DữLiệu.loạiHằng.length) throw new LỗiBảnDịch("giáTrịHằng sốHiệu cắtXén lỗi");
        if (DữLiệu.loạiHằng[sốHiệu] == 3) return "(word)(uint32_t)(" + DữLiệu.dữLiệuHằng[sốHiệu] + ")";
        if (DữLiệu.loạiHằng[sốHiệu] == 8) return "(word)" + kýHiệuChuỗi(DữLiệu.KýTự((Integer)DữLiệu.dữLiệuHằng[sốHiệu]));
        throw new LỗiBảnDịch("정수와 ChuỗiKýTự 상수만 giáTrịHỗTrợ");
    }
    String nguyênMẫuPhươngThức(ThamChiếuPhươngThức thamChiếu) {
        List<String> danhSáchCácĐốiSố = new ArrayList<>(); int sốLượngPhầnMục = new BộMôTảPhươngThức(thamChiếu.giáTrịMôTả).cácĐốiSố.size();
        for (int chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngPhầnMục; chỉSốThứBậc++) danhSáchCácĐốiSố.add("word a" + chỉSốThứBậc);
        return "static word " + kýHiệu("method", thamChiếu.cácPhần()) + "(" + (sốLượngPhầnMục == 0 ? "void" : String.join(", ", danhSáchCácĐốiSố)) + ")";
    }
    void kiểmTraCụcBộ(int sốHiệu, int sốLượngBiếnCụcBộ) { if (sốHiệu < 0 || sốHiệu >= sốLượngBiếnCụcBộ) throw new LỗiBảnDịch("phạmViCụcBộ giáTrịBiến sốHiệu cắtXén lỗi"); }
    void phátNhánh(List<String> ĐầuRa, Set<Integer> danhSáchNhánh, int vịTrí, int lượngChuyểnĐộng, String điềuKiện) {
        int giáTrịĐích = vịTrí + lượngChuyểnĐộng; danhSáchNhánh.add(giáTrịĐích);
        ĐầuRa.add((điềuKiện == null ? "" : "if (" + điềuKiện + ") ") + "goto b" + giáTrịĐích + ";");
    }
    String thânPhươngThức(ThamChiếuPhươngThức Hàm, DữLiệuThànhViên DữLiệu) {
        byte[] dữLiệuThân = DữLiệu.giáTrịThuộcTính.get("Code"); if (dữLiệuThân == null) throw new LỗiBảnDịch("Hàm 몸체가 phươngThứcThiếu: " + Hàm.tên);
        BộĐọcDữLiệu giáTrịBộĐọc = new BộĐọcDữLiệu(dữLiệuThân); int độSâuNgănXếp = giáTrịBộĐọc.đọcNgắnKiểu(), sốLượngBiếnCụcBộ = giáTrịBộĐọc.đọcNgắnKiểu();
        BộĐọcDữLiệu dữLiệuLệnh = new BộĐọcDữLiệu(giáTrịBộĐọc.đọc(giáTrịBộĐọc.đọcSốNguyênGọn()));
        if (giáTrịBộĐọc.đọcNgắnKiểu() != 0) throw new LỗiBảnDịch("try/catch/finally làKhôngHỗTrợ");
        BộMôTảPhươngThức giáTrịĐịnhDạng = new BộMôTảPhươngThức(Hàm.giáTrịMôTả); if (sốLượngBiếnCụcBộ < giáTrịĐịnhDạng.cácĐốiSố.size()) throw new LỗiBảnDịch("매개변수보다 적은 phạmViCụcBộ giáTrịBiến");
        DữLiệuLớp giáTrịLớp = danhSáchCácLớp.get(Hàm.giáTrịChủSởHữu);
        List<String> ĐầuRa = new ArrayList<>(); ĐầuRa.add(nguyênMẫuPhươngThức(Hàm) + " {");
        ĐầuRa.add("word s[" + Math.max(độSâuNgănXếp, 1) + "], l[" + Math.max(sốLượngBiếnCụcBộ, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int chỉSốThứBậc = 0; chỉSốThứBậc < giáTrịĐịnhDạng.cácĐốiSố.size(); chỉSốThứBậc++) ĐầuRa.add("l[" + chỉSốThứBậc + "] = a" + chỉSốThứBậc + ";");
        Set<Integer> danhSáchCácRanhGiới = new HashSet<>(), danhSáchNhánh = new HashSet<>();
        String[] danhSáchCácPhépSoSánh = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (dữLiệuLệnh.vịTrí < dữLiệuLệnh.DữLiệu.length) {
            int vịTrí = dữLiệuLệnh.vịTrí, lệnh = dữLiệuLệnh.đọcByte(); danhSáchCácRanhGiới.add(vịTrí); ĐầuRa.add("b" + vịTrí + ":;");
            if (lệnh == 0) continue;
            if (lệnh == 1) ĐầuRa.add("PUSH(0);");
            else if (lệnh >= 2 && lệnh <= 8) ĐầuRa.add("PUSH((uint32_t)(" + (lệnh - 3) + "));");
            else if (lệnh == 16 || lệnh == 17) ĐầuRa.add("PUSH((uint32_t)(" + (lệnh == 16 ? dữLiệuLệnh.đọcByteCóDấu() : dữLiệuLệnh.đọcNgắnKiểuCóDấu()) + "));");
            else if (lệnh == 18 || lệnh == 19) ĐầuRa.add("PUSH(" + biểuThứcHằng(giáTrịLớp, lệnh == 18 ? dữLiệuLệnh.đọcByte() : dữLiệuLệnh.đọcNgắnKiểu()) + ");");
            else if (lệnh == 21 || lệnh == 25 || (lệnh >= 26 && lệnh <= 29) || (lệnh >= 42 && lệnh <= 45)) {
                int sốHiệu = lệnh == 21 || lệnh == 25 ? dữLiệuLệnh.đọcByte() : lệnh - (lệnh <= 29 ? 26 : 42);
                kiểmTraCụcBộ(sốHiệu, sốLượngBiếnCụcBộ); ĐầuRa.add("PUSH(l[" + sốHiệu + "]);");
            } else if (lệnh == 54 || lệnh == 58 || (lệnh >= 59 && lệnh <= 62) || (lệnh >= 75 && lệnh <= 78)) {
                int sốHiệu = lệnh == 54 || lệnh == 58 ? dữLiệuLệnh.đọcByte() : lệnh - (lệnh <= 62 ? 59 : 75);
                kiểmTraCụcBộ(sốHiệu, sốLượngBiếnCụcBộ); ĐầuRa.add("l[" + sốHiệu + "] = POP();");
            } else if (lệnh == 46) ĐầuRa.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (lệnh == 79) ĐầuRa.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (lệnh == 87 || lệnh == 88) ĐầuRa.add(lệnh == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (lệnh >= 89 && lệnh <= 95) {
                int[] cácSốLượngPhầnMục = {1,2,3,2,3,4,2}; String[] danhSáchThứTự = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int chỉSốThứBậc = 0; chỉSốThứBậc < cácSốLượngPhầnMục[lệnh - 89]; chỉSốThứBậc++) ĐầuRa.add("abcd".charAt(chỉSốThứBậc) + " = POP();");
                for (char giáTrị : danhSáchThứTự[lệnh - 89].toCharArray()) ĐầuRa.add("PUSH(" + giáTrị + ");");
            } else if (lệnh == 96 || lệnh == 100 || lệnh == 104 || lệnh == 126 || lệnh == 128 || lệnh == 130) {
                String giáTrịThaoTác = lệnh == 96 ? "+" : lệnh == 100 ? "-" : lệnh == 104 ? "*" : lệnh == 126 ? "&" : lệnh == 128 ? "|" : "^";
                ĐầuRa.add("b = POP(); a = POP(); PUSH((uint32_t)a " + giáTrịThaoTác + " (uint32_t)b);");
            } else if (lệnh == 108 || lệnh == 112) ĐầuRa.add("b = POP(); a = POP(); PUSH(divide(a,b," + (lệnh == 112 ? 1 : 0) + "));");
            else if (lệnh == 116) ĐầuRa.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (lệnh == 120 || lệnh == 122 || lệnh == 124) {
                ĐầuRa.add("b = POP(); a = POP();"); ĐầuRa.add("PUSH(" + (lệnh == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (lệnh == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (lệnh == 132) {
                int sốHiệu = dữLiệuLệnh.đọcByte(), lượngBướcTăng = dữLiệuLệnh.đọcByteCóDấu(); kiểmTraCụcBộ(sốHiệu, sốLượngBiếnCụcBộ);
                ĐầuRa.add("l[" + sốHiệu + "] = (uint32_t)l[" + sốHiệu + "] + (uint32_t)(" + lượngBướcTăng + ");");
            } else if (lệnh >= 145 && lệnh <= 147) ĐầuRa.add("a = POP(); PUSH((uint32_t)(" + (lệnh == 145 ? "int8_t" : lệnh == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (lệnh >= 153 && lệnh <= 158) {
                ĐầuRa.add("a = POP();"); phátNhánh(ĐầuRa, danhSáchNhánh, vịTrí, dữLiệuLệnh.đọcNgắnKiểuCóDấu(), "(int32_t)a " + danhSáchCácPhépSoSánh[lệnh - 153] + " 0");
            } else if (lệnh >= 159 && lệnh <= 166) {
                ĐầuRa.add("b = POP(); a = POP();"); phátNhánh(ĐầuRa, danhSáchNhánh, vịTrí, dữLiệuLệnh.đọcNgắnKiểuCóDấu(), lệnh >= 165 ? "a " + danhSáchCácPhépSoSánh[lệnh - 159] + " b" : "(int32_t)a " + danhSáchCácPhépSoSánh[lệnh - 159] + " (int32_t)b");
            } else if (lệnh == 167 || lệnh == 200) phátNhánh(ĐầuRa, danhSáchNhánh, vịTrí, lệnh == 167 ? dữLiệuLệnh.đọcNgắnKiểuCóDấu() : dữLiệuLệnh.đọcSốNguyênGọn(), null);
            else if (lệnh == 170 || lệnh == 171) {
                while (dữLiệuLệnh.vịTrí % 4 != 0) dữLiệuLệnh.đọcByte();
                int giáTrịMặcĐịnh = dữLiệuLệnh.đọcSốNguyênGọn(); ĐầuRa.add("a = POP();");
                if (lệnh == 170) {
                    int giáTrịĐáy = dữLiệuLệnh.đọcSốNguyênGọn(), giáTrịĐỉnh = dữLiệuLệnh.đọcSốNguyênGọn(); long sốLượngPhầnMục = (long)giáTrịĐỉnh - giáTrịĐáy + 1;
                    if (sốLượngPhầnMục < 1 || sốLượngPhầnMục > (dữLiệuLệnh.DữLiệu.length - dữLiệuLệnh.vịTrí) / 4) throw new LỗiBảnDịch("switch cắtXén lỗi");
                    for (long giáTrị = giáTrịĐáy; giáTrị <= giáTrịĐỉnh; giáTrị++) phátNhánh(ĐầuRa, danhSáchNhánh, vịTrí, dữLiệuLệnh.đọcSốNguyênGọn(), "(int32_t)a == (" + giáTrị + ")");
                } else {
                    int sốLượngPhầnMục = dữLiệuLệnh.đọcSốNguyênGọn(), dữLiệuPhíaTrước = 0;
                    if (sốLượngPhầnMục < 0 || sốLượngPhầnMục > (dữLiệuLệnh.DữLiệu.length - dữLiệuLệnh.vịTrí) / 8) throw new LỗiBảnDịch("switch cỡ lỗi");
                    for (int chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngPhầnMục; chỉSốThứBậc++) {
                        int giáTrị = dữLiệuLệnh.đọcSốNguyênGọn(); if (chỉSốThứBậc > 0 && giáTrị <= dữLiệuPhíaTrước) throw new LỗiBảnDịch("switch giáTrịThứTự lỗi"); dữLiệuPhíaTrước = giáTrị;
                        phátNhánh(ĐầuRa, danhSáchNhánh, vịTrí, dữLiệuLệnh.đọcSốNguyênGọn(), "(int32_t)a == (" + giáTrị + ")");
                    }
                }
                phátNhánh(ĐầuRa, danhSáchNhánh, vịTrí, giáTrịMặcĐịnh, null);
            } else if (lệnh == 172 || lệnh == 176 || lệnh == 177) ĐầuRa.add("return " + (lệnh == 177 ? "0" : "POP()") + ";");
            else if (lệnh == 178 || lệnh == 179) {
                ThamChiếuPhươngThức thamChiếu = giáTrịLớp.thamChiếu(dữLiệuLệnh.đọcNgắnKiểu()); if (!danhSáchCácTrường.containsKey(thamChiếu)) throw new LỗiBảnDịch("알 trịSố 없는 giáTrịTrường");
                ĐầuRa.add(kýHiệu("init", thamChiếu.giáTrịChủSởHữu) + "();"); String giáTrịTrường = kýHiệu("field", thamChiếu.cácPhần());
                ĐầuRa.add(lệnh == 178 ? "PUSH(" + giáTrịTrường + ");" : giáTrịTrường + " = POP();");
            } else if (lệnh == 184) {
                ThamChiếuPhươngThức thamChiếu = giáTrịLớp.thamChiếu(dữLiệuLệnh.đọcNgắnKiểu()); if (!danhSáchCácPhươngThức.containsKey(thamChiếu)) throw new LỗiBảnDịch("알 trịSố 없는 Hàm");
                BộMôTảPhươngThức kiểuLờiGọi = new BộMôTảPhươngThức(thamChiếu.giáTrịMôTả); int sốLượngPhầnMục = kiểuLờiGọi.cácĐốiSố.size();
                ĐầuRa.add(kýHiệu("init", thamChiếu.giáTrịChủSởHữu) + "();"); ĐầuRa.add("if(sp < " + sốLượngPhầnMục + ") kernel_panic(\"call stack underflow\"); sp -= " + sốLượngPhầnMục + ";");
                List<String> cácĐốiSốLờiGọi = new ArrayList<>(); for (int chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngPhầnMục; chỉSốThứBậc++) cácĐốiSốLờiGọi.add("s[sp + " + chỉSốThứBậc + "]");
                ĐầuRa.add("a = " + kýHiệu("method", thamChiếu.cácPhần()) + "(" + String.join(",", cácĐốiSốLờiGọi) + ");");
                if (!kiểuLờiGọi.kếtQuảTrảVề.equals("V")) ĐầuRa.add("PUSH(a);");
            } else if (lệnh == 182) {
                ThamChiếuPhươngThức thamChiếu = giáTrịLớp.thamChiếu(dữLiệuLệnh.đọcNgắnKiểu());
                if (thamChiếu.equals(new ThamChiếuPhươngThức("java/lang/String", "length", "()I"))) ĐầuRa.add("a = POP(); PUSH(length(a));");
                else if (thamChiếu.equals(new ThamChiếuPhươngThức("java/lang/String", "charAt", "(I)C"))) ĐầuRa.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new LỗiBảnDịch("가상 Hàm gọiThựcHiện làKhôngHỗTrợ");
            } else if (lệnh == 188) {
                if (dữLiệuLệnh.đọcByte() != 10) throw new LỗiBảnDịch("new int[]만 giáTrịHỗTrợ"); ĐầuRa.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (lệnh == 190) ĐầuRa.add("a = POP(); PUSH(length(a));");
            else if (lệnh == 196) {
                int giáTrịPhầnMởRộng = dữLiệuLệnh.đọcByte(), sốHiệu = dữLiệuLệnh.đọcNgắnKiểu(); kiểmTraCụcBộ(sốHiệu, sốLượngBiếnCụcBộ);
                if (giáTrịPhầnMởRộng == 21 || giáTrịPhầnMởRộng == 25) ĐầuRa.add("PUSH(l[" + sốHiệu + "]);");
                else if (giáTrịPhầnMởRộng == 54 || giáTrịPhầnMởRộng == 58) ĐầuRa.add("l[" + sốHiệu + "] = POP();");
                else if (giáTrịPhầnMởRộng == 132) ĐầuRa.add("l[" + sốHiệu + "] = (uint32_t)l[" + sốHiệu + "] + (uint32_t)(" + dữLiệuLệnh.đọcNgắnKiểuCóDấu() + ");");
                else throw new LỗiBảnDịch("làKhôngHỗTrợ wide lệnh");
            } else if (lệnh == 198 || lệnh == 199) {
                ĐầuRa.add("a = POP();"); phátNhánh(ĐầuRa, danhSáchNhánh, vịTrí, dữLiệuLệnh.đọcNgắnKiểuCóDấu(), "a " + (lệnh == 198 ? "==" : "!=") + " 0");
            } else throw new LỗiBảnDịch(Hàm.giáTrịChủSởHữu + "." + Hàm.tên + ", giáTrịByte " + vịTrí + ": làKhôngHỗTrợ lệnh " + lệnh);
        }
        if (!danhSáchCácRanhGiới.containsAll(danhSáchNhánh)) throw new LỗiBảnDịch("lệnh 경계가 아닌 곳으로 nhánh");
        ĐầuRa.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", ĐầuRa);
    }
    String phươngThứcXuất(String kýHiệuLiênKết, String giáTrịĐốiĐích, boolean cóĐiểmMục) {
        int chỉSốVịTrí = giáTrịĐốiĐích.lastIndexOf('.'); if (chỉSốVịTrí < 0 || !kýHiệuLiênKết.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new LỗiBảnDịch("phátGiáTrị giáTrịGán lỗi");
        String giáTrịChủSởHữu = giáTrịĐốiĐích.substring(0, chỉSốVịTrí).replace('.', '/'), tên = giáTrịĐốiĐích.substring(chỉSốVịTrí + 1); ThamChiếuPhươngThức giáTrịViệcChọn = null;
        for (ThamChiếuPhươngThức thamChiếu : danhSáchCácPhươngThức.keySet()) if (thamChiếu.giáTrịChủSởHữu.equals(giáTrịChủSởHữu) && thamChiếu.tên.equals(tên)) {
            if (giáTrịViệcChọn != null) throw new LỗiBảnDịch("겹친 phátGiáTrị giáTrịĐốiĐích"); giáTrịViệcChọn = thamChiếu;
        }
        if (giáTrịViệcChọn == null || (danhSáchCácPhươngThức.get(giáTrịViệcChọn).mụcTruyCập & 0x100) != 0) throw new LỗiBảnDịch("내보낼 함수가 phươngThứcThiếu 또는 native Hàm");
        BộMôTảPhươngThức giáTrịĐịnhDạng = new BộMôTảPhươngThức(giáTrịViệcChọn.giáTrịMôTả);
        if ((cóĐiểmMục && !giáTrịĐịnhDạng.cácĐốiSố.isEmpty()) || !Arrays.asList("V", "I").contains(giáTrịĐịnhDạng.kếtQuảTrảVề)) throw new LỗiBảnDịch("giáTrịĐiểmMục 또는 C giáTrịRanhGiới giáTrịĐịnhDạng lỗi");
        List<String> danhSáchCácĐốiSố = new ArrayList<>(), cácĐốiSốLờiGọi = new ArrayList<>();
        for (int chỉSốThứBậc = 0; chỉSốThứBậc < giáTrịĐịnhDạng.cácĐốiSố.size(); chỉSốThứBậc++) {
            if (!giáTrịĐịnhDạng.cácĐốiSố.get(chỉSốThứBậc).equals("I")) throw new LỗiBảnDịch("C 경계는 int 인수만 giáTrịHỗTrợ");
            danhSáchCácĐốiSố.add("int32_t a" + chỉSốThứBậc); cácĐốiSốLờiGọi.add("(uint32_t)a" + chỉSốThứBậc);
        }
        return (giáTrịĐịnhDạng.kếtQuảTrảVề.equals("V") ? "void " : "int32_t ") + kýHiệuLiênKết + "(" + (danhSáchCácĐốiSố.isEmpty() ? "void" : String.join(",", danhSáchCácĐốiSố)) + ") { " + kýHiệu("init", giáTrịViệcChọn.giáTrịChủSởHữu) + "(); " + (giáTrịĐịnhDạng.kếtQuảTrảVề.equals("V") ? "" : "return (int32_t)") + kýHiệu("method", giáTrịViệcChọn.cácPhần()) + "(" + String.join(",", cácĐốiSốLờiGọi) + "); }";
    }
    String sinh(String điểmMục, List<String> cácMụcXuất, boolean cáchKýHiệuPhổQuát) throws IOException {
        List<String> danhSáchCácKhaiBáo = new ArrayList<>(), danhSáchCácThân = new ArrayList<>(), cácKhaiBáoTrường = new ArrayList<>();
        for (Map.Entry<ThamChiếuPhươngThức, DữLiệuThànhViên> giáTrịMục : danhSáchCácPhươngThức.entrySet()) {
            ThamChiếuPhươngThức thamChiếu = giáTrịMục.getKey(); DữLiệuThànhViên DữLiệu = giáTrịMục.getValue(); danhSáchCácKhaiBáo.add(nguyênMẫuPhươngThức(thamChiếu) + ";");
            if ((DữLiệu.mụcTruyCập & 0x100) != 0) {
                String nốiKết = cácHàmMáy.get(thamChiếu.tên + thamChiếu.giáTrịMôTả);
                if (!thamChiếu.giáTrịChủSởHữu.equals(lớpMáy) || nốiKết == null) throw new LỗiBảnDịch("허용되지 않은 native Hàm: " + thamChiếu.tên);
                int sốLượngPhầnMục = new BộMôTảPhươngThức(thamChiếu.giáTrịMôTả).cácĐốiSố.size(); List<String> danhSáchCácĐốiSố = new ArrayList<>();
                for (int chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngPhầnMục; chỉSốThứBậc++) danhSáchCácĐốiSố.add("a" + chỉSốThứBậc);
                danhSáchCácKhaiBáo.add("extern word " + nốiKết + "(" + (sốLượngPhầnMục == 0 ? "void" : String.join(",", Collections.nCopies(sốLượngPhầnMục, "word"))) + ");");
                danhSáchCácThân.add(nguyênMẫuPhươngThức(thamChiếu) + " { return " + nốiKết + "(" + String.join(",", danhSáchCácĐốiSố) + "); }");
            } else danhSáchCácThân.add(thânPhươngThức(thamChiếu, DữLiệu));
        }
        for (Map.Entry<ThamChiếuPhươngThức, DữLiệuThànhViên> giáTrịMục : danhSáchCácTrường.entrySet()) {
            ThamChiếuPhươngThức thamChiếu = giáTrịMục.getKey(); byte[] giáTrịHằng = giáTrịMục.getValue().giáTrịThuộcTính.get("ConstantValue");
            String giáTrị = giáTrịHằng == null ? "0" : biểuThứcHằng(danhSáchCácLớp.get(thamChiếu.giáTrịChủSởHữu), new BộĐọcDữLiệu(giáTrịHằng).đọcNgắnKiểu());
            cácKhaiBáoTrường.add("static word " + kýHiệu("field", thamChiếu.cácPhần()) + " = " + giáTrị + ";");
        }
        for (String tên : danhSáchCácLớp.keySet()) {
            String khởiTạo = kýHiệu("init", tên), giáTrịTrạngThái = kýHiệu("state", tên);
            danhSáchCácKhaiBáo.add("static void " + khởiTạo + "(void);"); cácKhaiBáoTrường.add("static unsigned " + giáTrịTrạngThái + ";");
            ThamChiếuPhươngThức thamChiếu = new ThamChiếuPhươngThức(tên, "<clinit>", "()V");
            danhSáchCácThân.add("static void " + khởiTạo + "(void) { if(" + giáTrịTrạngThái + ") return; " + giáTrịTrạngThái + " = 1; " + (danhSáchCácPhươngThức.containsKey(thamChiếu) ? kýHiệu("method", thamChiếu.cácPhần()) + "(); " : "") + giáTrịTrạngThái + " = 2; }");
        }
        danhSáchCácThân.add(phươngThứcXuất("java_entry", điểmMục, true)); Set<String> tênĐãXuất = new HashSet<>();
        for (String giáTrịGán : cácMụcXuất) {
            int chỉSốVịTrí = giáTrịGán.indexOf('='); if (chỉSốVịTrí < 1) throw new LỗiBảnDịch("phátGiáTrị giáTrịGán lỗi");
            String tên = giáTrịGán.substring(0, chỉSốVịTrí); tênĐãXuất.add(tên); danhSáchCácThân.add(phươngThứcXuất(tên, giáTrịGán.substring(chỉSốVịTrí + 1), false));
        }
        List<String> cácKhaiBáoChuỗi = new ArrayList<>();
        for (Map.Entry<String, String> giáTrịMục : cácGiáTrịChuỗi.entrySet()) {
            String vănBản = giáTrịMục.getKey(); StringBuilder giáTrịMảng = new StringBuilder("static const word " + giáTrịMục.getValue() + "[] = {" + vănBản.length());
            for (int chỉSốThứBậc = 0; chỉSốThứBậc < vănBản.length(); chỉSốThứBậc++) giáTrịMảng.append(", ").append((int)vănBản.charAt(chỉSốThứBậc));
            cácKhaiBáoChuỗi.add(giáTrịMảng.append("};").toString());
        }
        String giáTrịHỗTrợ = Files.readString(đườngDẫnTàiNguyên.resolve("HỗTrợMôiTrườngChạy.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(sốLượngTừVùngNhớĐộng));
        return bảnĐịaHóaNguồnĐãSinh(giáTrịHỗTrợ + String.join("\n", cácKhaiBáoChuỗi) + "\n" + String.join("\n", danhSáchCácKhaiBáo) + "\n" + String.join("\n", cácKhaiBáoTrường) + "\n" + String.join("\n", danhSáchCácThân) + "\n", tênĐãXuất, cáchKýHiệuPhổQuát);
    }
    String bảnĐịaHóaNguồnĐãSinh(String mãNguồn, Set<String> tênĐãXuất, boolean cáchKýHiệuPhổQuát) throws IOException {
        Map<String, String> bảngTraTên = new HashMap<>();
        for (String dòng : Files.readAllLines(đườngDẫnTàiNguyên.resolve("CácTênĐãSinh.tsv"), StandardCharsets.UTF_8)) {
            String[] giáTrịCặp = dòng.split("\t"); bảngTraTên.put(giáTrịCặp[0], giáTrịCặp[1]);
        }
        Pattern biểuThứcMảnh = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher giáTrịBộTìm = biểuThứcMảnh.matcher(mãNguồn); StringBuffer kếtQuả = new StringBuffer();
        while (giáTrịBộTìm.find()) {
            String tên = giáTrịBộTìm.group(), tênMới = tên;
            if (!tên.startsWith("//") && !tên.startsWith("/*") && !tên.startsWith("\"") && !tên.startsWith("'") && !tênĐãXuất.contains(tên)) {
                tênMới = bảngTraTên.getOrDefault(tên, tên);
                if (tên.matches("a[0-9]+")) tênMới = "cácĐốiSố" + tên.substring(1);
                if (tên.matches("b[0-9]+")) tênMới = "nhánh" + tên.substring(1);
                if (cáchKýHiệuPhổQuát) {
                    StringBuilder giáTrịCáchKýHiệu = new StringBuilder();
                    for (char giáTrịKýTự : tênMới.toCharArray()) giáTrịCáchKýHiệu.append(giáTrịKýTự < 128 ? Character.toString(giáTrịKýTự) : String.format(Locale.ROOT, "\\u%04x", (int)giáTrịKýTự));
                    tênMới = giáTrịCáchKýHiệu.toString();
                }
            }
            giáTrịBộTìm.appendReplacement(kếtQuả, Matcher.quoteReplacement(tênMới));
        }
        giáTrịBộTìm.appendTail(kếtQuả); return kếtQuả.toString();
    }
    String thânHàmX86(ThamChiếuPhươngThức Hàm, DữLiệuThànhViên DữLiệu, Map<String,String> bảngTraMáy, String giáTrịĐốiĐích) {
        String giáTrịDấuMốc = kýHiệu("method", Hàm.cácPhần());
        List<String> dòng = new ArrayList<>();
        if ((DữLiệu.mụcTruyCập & 0x100) != 0) {
            String nốiKết = bảngTraMáy.get(Hàm.tên + Hàm.giáTrịMôTả);
            if (!Hàm.giáTrịChủSởHữu.equals(giáTrịĐốiĐích.equals("kernel") ? "ThiếtBị" : "NgườiDùng") || nốiKết == null) throw new LỗiBảnDịch("허용되지 않은 native Hàm");
            return ".text\n" + giáTrịDấuMốc + ":\njmp " + nốiKết;
        }
        byte[] vănBảnThân = DữLiệu.giáTrịThuộcTính.get("Code"); if (vănBảnThân == null) throw new LỗiBảnDịch("Hàm 몸체가 phươngThứcThiếu");
        BộĐọcDữLiệu giáTrịBộĐọc = new BộĐọcDữLiệu(vănBảnThân); giáTrịBộĐọc.đọcNgắnKiểu(); int sốLượngCụcBộ = giáTrịBộĐọc.đọcNgắnKiểu();
        BộĐọcDữLiệu dữLiệuLệnh = new BộĐọcDữLiệu(giáTrịBộĐọc.đọc(giáTrịBộĐọc.đọcSốNguyênGọn()));
        if (giáTrịBộĐọc.đọcNgắnKiểu() != 0) throw new LỗiBảnDịch("try/catch/finally làKhôngHỗTrợ");
        BộMôTảPhươngThức giáTrịĐịnhDạng = new BộMôTảPhươngThức(Hàm.giáTrịMôTả); if (sốLượngCụcBộ < giáTrịĐịnhDạng.cácĐốiSố.size()) throw new LỗiBảnDịch("매개변수보다 적은 phạmViCụcBộ giáTrịBiến");
        Collections.addAll(dòng,".text",".globl " + giáTrịDấuMốc,".type " + giáTrịDấuMốc + ", @function",giáTrịDấuMốc + ":","pushl %ebp","movl %esp, %ebp","subl $" + sốLượngCụcBộ * 4 + ", %esp");
        for (int chỉSốThứBậc = 0; chỉSốThứBậc < giáTrịĐịnhDạng.cácĐốiSố.size(); chỉSốThứBậc++) Collections.addAll(dòng,"movl " + (8 + 4 * (giáTrịĐịnhDạng.cácĐốiSố.size() - chỉSốThứBậc - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (chỉSốThứBậc + 1)) + "(%ebp)");
        DữLiệuLớp giáTrịLớp = danhSáchCácLớp.get(Hàm.giáTrịChủSởHữu); Set<Integer> danhSáchCácRanhGiới = new HashSet<>(), danhSáchNhánh = new HashSet<>();
        String[] danhSáchCácPhépSoSánh = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (dữLiệuLệnh.vịTrí < dữLiệuLệnh.DữLiệu.length) {
            int vịTrí = dữLiệuLệnh.vịTrí, lệnh = dữLiệuLệnh.đọcByte(); String chỉSốVịTrí = giáTrịDấuMốc + "_b" + vịTrí;
            dòng.add(chỉSốVịTrí + ":"); danhSáchCácRanhGiới.add(vịTrí);
            if (lệnh == 0) dòng.add("nop");
            else if (lệnh == 1) dòng.add("pushl $0");
            else if (lệnh >= 2 && lệnh <= 8) dòng.add("pushl $" + (lệnh - 3));
            else if (lệnh == 16 || lệnh == 17) dòng.add("pushl $" + (lệnh == 16 ? dữLiệuLệnh.đọcByteCóDấu() : dữLiệuLệnh.đọcNgắnKiểuCóDấu()));
            else if (lệnh == 18 || lệnh == 19) {
                int sốHiệu = lệnh == 18 ? dữLiệuLệnh.đọcByte() : dữLiệuLệnh.đọcNgắnKiểu();
                dòng.add("pushl $" + hằngX86(giáTrịLớp,sốHiệu));
            } else if (lệnh == 21 || lệnh == 25 || (lệnh >= 26 && lệnh <= 29) || (lệnh >= 42 && lệnh <= 45) || lệnh == 54 || lệnh == 58 || (lệnh >= 59 && lệnh <= 62) || (lệnh >= 75 && lệnh <= 78)) {
                boolean đọcKếtQuả = lệnh < 54; int sốHiệu = lệnh == 21 || lệnh == 25 || lệnh == 54 || lệnh == 58 ? dữLiệuLệnh.đọcByte() : lệnh - (lệnh <= 29 ? 26 : lệnh <= 45 ? 42 : lệnh <= 62 ? 59 : 75);
                kiểmTraCụcBộ(sốHiệu,sốLượngCụcBộ); dòng.add((đọcKếtQuả ? "pushl " : "popl ") + "-" + (4 * (sốHiệu + 1)) + "(%ebp)");
            } else if (lệnh == 46) Collections.addAll(dòng,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (lệnh == 79) Collections.addAll(dòng,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (lệnh == 87 || lệnh == 88) dòng.add("addl $" + (lệnh == 87 ? 4 : 8) + ", %esp");
            else if (lệnh >= 89 && lệnh <= 95) {
                int[] cácSốLượngPhầnMục = {1,2,3,2,3,4,2}; int[][] danhSáchThứTự = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] thanhGhiCácGiáTrị = {"%eax","%ecx","%edx","%ebx"};
                for (int chỉSốThứBậc = 0; chỉSốThứBậc < cácSốLượngPhầnMục[lệnh - 89]; chỉSốThứBậc++) dòng.add("popl " + thanhGhiCácGiáTrị[chỉSốThứBậc]);
                for (int chỉSốThứBậc : danhSáchThứTự[lệnh - 89]) dòng.add("pushl " + thanhGhiCácGiáTrị[chỉSốThứBậc]);
            } else if (lệnh == 96 || lệnh == 100 || lệnh == 104 || lệnh == 126 || lệnh == 128 || lệnh == 130) {
                String giáTrịThaoTác = lệnh == 96 ? "addl" : lệnh == 100 ? "subl" : lệnh == 104 ? "imull" : lệnh == 126 ? "andl" : lệnh == 128 ? "orl" : "xorl";
                Collections.addAll(dòng,"popl %ecx","popl %eax",giáTrịThaoTác + " %ecx, %eax","pushl %eax");
            } else if (lệnh == 108 || lệnh == 112) Collections.addAll(dòng,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + chỉSốVịTrí + "_divide","cmpl $0x80000000, %eax","jne " + chỉSốVịTrí + "_divide","xorl %edx, %edx","jmp " + chỉSốVịTrí + "_done",chỉSốVịTrí + "_divide:","cltd","idivl %ecx",chỉSốVịTrí + "_done:","pushl " + (lệnh == 108 ? "%eax" : "%edx"));
            else if (lệnh == 116) dòng.add("negl (%esp)");
            else if (lệnh == 120 || lệnh == 122 || lệnh == 124) Collections.addAll(dòng,"popl %ecx","popl %eax",(lệnh == 120 ? "sall" : lệnh == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (lệnh == 132) {
                int sốHiệu = dữLiệuLệnh.đọcByte(), giáTrịBướcTăng = dữLiệuLệnh.đọcByteCóDấu(); kiểmTraCụcBộ(sốHiệu,sốLượngCụcBộ); dòng.add("addl $" + giáTrịBướcTăng + ", -" + (4 * (sốHiệu + 1)) + "(%ebp)");
            } else if (lệnh >= 145 && lệnh <= 147) Collections.addAll(dòng,"popl %eax",lệnh == 145 ? "movsbl %al, %eax" : lệnh == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (lệnh >= 153 && lệnh <= 166) {
                if (lệnh <= 158) Collections.addAll(dòng,"popl %eax","testl %eax, %eax");
                else Collections.addAll(dòng,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int giáTrịĐích = vịTrí + dữLiệuLệnh.đọcNgắnKiểuCóDấu(); danhSáchNhánh.add(giáTrịĐích); dòng.add(danhSáchCácPhépSoSánh[lệnh - (lệnh <= 158 ? 153 : 159)] + " " + giáTrịDấuMốc + "_b" + giáTrịĐích);
            } else if (lệnh == 167 || lệnh == 200) {
                int giáTrịĐích = vịTrí + (lệnh == 167 ? dữLiệuLệnh.đọcNgắnKiểuCóDấu() : dữLiệuLệnh.đọcSốNguyênGọn()); danhSáchNhánh.add(giáTrịĐích); dòng.add("jmp " + giáTrịDấuMốc + "_b" + giáTrịĐích);
            } else if (lệnh == 170 || lệnh == 171) {
                while (dữLiệuLệnh.vịTrí % 4 != 0) dữLiệuLệnh.đọcByte();
                int giáTrịMặcĐịnh = vịTrí + dữLiệuLệnh.đọcSốNguyênGọn(); danhSáchNhánh.add(giáTrịMặcĐịnh); dòng.add("popl %eax");
                int sốLượngPhầnMục, giáTrịĐáy = 0;
                if (lệnh == 170) { giáTrịĐáy = dữLiệuLệnh.đọcSốNguyênGọn(); int giáTrịĐỉnh = dữLiệuLệnh.đọcSốNguyênGọn(); long độDài = (long)giáTrịĐỉnh - giáTrịĐáy + 1; if (độDài < 1 || độDài > (dữLiệuLệnh.DữLiệu.length - dữLiệuLệnh.vịTrí) / 4) throw new LỗiBảnDịch("switch cắtXén lỗi"); sốLượngPhầnMục = (int)độDài; }
                else { sốLượngPhầnMục = dữLiệuLệnh.đọcSốNguyênGọn(); if (sốLượngPhầnMục < 0 || sốLượngPhầnMục > (dữLiệuLệnh.DữLiệu.length - dữLiệuLệnh.vịTrí) / 8) throw new LỗiBảnDịch("switch cỡ lỗi"); }
                for (int chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngPhầnMục; chỉSốThứBậc++) {
                    int giáTrị = lệnh == 170 ? giáTrịĐáy + chỉSốThứBậc : dữLiệuLệnh.đọcSốNguyênGọn(), giáTrịĐích = vịTrí + dữLiệuLệnh.đọcSốNguyênGọn(); danhSáchNhánh.add(giáTrịĐích);
                    Collections.addAll(dòng,"cmpl $" + giáTrị + ", %eax","je " + giáTrịDấuMốc + "_b" + giáTrịĐích);
                }
                dòng.add("jmp " + giáTrịDấuMốc + "_b" + giáTrịMặcĐịnh);
            } else if (lệnh == 172 || lệnh == 176 || lệnh == 177) {
                if (lệnh != 177) dòng.add("popl %eax"); Collections.addAll(dòng,"leave","ret");
            } else if (lệnh == 178 || lệnh == 179) {
                ThamChiếuPhươngThức thamChiếu = giáTrịLớp.thamChiếu(dữLiệuLệnh.đọcNgắnKiểu()); if (!danhSáchCácTrường.containsKey(thamChiếu)) throw new LỗiBảnDịch("알 trịSố 없는 giáTrịTrường");
                Collections.addAll(dòng,"call " + kýHiệu("init",thamChiếu.giáTrịChủSởHữu),(lệnh == 178 ? "pushl " : "popl ") + kýHiệu("field",thamChiếu.cácPhần()));
            } else if (lệnh == 184) {
                ThamChiếuPhươngThức thamChiếu = giáTrịLớp.thamChiếu(dữLiệuLệnh.đọcNgắnKiểu()); if (!danhSáchCácPhươngThức.containsKey(thamChiếu)) throw new LỗiBảnDịch("알 trịSố 없는 Hàm");
                BộMôTảPhươngThức kiểuLờiGọi = new BộMôTảPhươngThức(thamChiếu.giáTrịMôTả); Collections.addAll(dòng,"call " + kýHiệu("init",thamChiếu.giáTrịChủSởHữu),"call " + kýHiệu("method",thamChiếu.cácPhần()));
                if (!kiểuLờiGọi.cácĐốiSố.isEmpty()) dòng.add("addl $" + kiểuLờiGọi.cácĐốiSố.size() * 4 + ", %esp");
                if (!kiểuLờiGọi.kếtQuảTrảVề.equals("V")) dòng.add("pushl %eax");
            } else if (lệnh == 182) {
                ThamChiếuPhươngThức thamChiếu = giáTrịLớp.thamChiếu(dữLiệuLệnh.đọcNgắnKiểu());
                if (thamChiếu.equals(new ThamChiếuPhươngThức("java/lang/String","length","()I"))) Collections.addAll(dòng,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (thamChiếu.equals(new ThamChiếuPhươngThức("java/lang/String","charAt","(I)C"))) Collections.addAll(dòng,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new LỗiBảnDịch("가상 Hàm gọiThựcHiện làKhôngHỗTrợ");
            } else if (lệnh == 188) {
                if (dữLiệuLệnh.đọcByte() != 10) throw new LỗiBảnDịch("new int[]만 giáTrịHỗTrợ"); Collections.addAll(dòng,"popl %eax","call rt_new_array","pushl %eax");
            } else if (lệnh == 190) Collections.addAll(dòng,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (lệnh == 196) {
                int giáTrịPhầnMởRộng = dữLiệuLệnh.đọcByte(), sốHiệu = dữLiệuLệnh.đọcNgắnKiểu(); kiểmTraCụcBộ(sốHiệu,sốLượngCụcBộ);
                if (giáTrịPhầnMởRộng == 21 || giáTrịPhầnMởRộng == 25 || giáTrịPhầnMởRộng == 54 || giáTrịPhầnMởRộng == 58) dòng.add((giáTrịPhầnMởRộng <= 25 ? "pushl " : "popl ") + "-" + 4 * (sốHiệu + 1) + "(%ebp)");
                else if (giáTrịPhầnMởRộng == 132) dòng.add("addl $" + dữLiệuLệnh.đọcNgắnKiểuCóDấu() + ", -" + 4 * (sốHiệu + 1) + "(%ebp)");
                else throw new LỗiBảnDịch("wide lệnh làKhôngHỗTrợ");
            } else if (lệnh == 198 || lệnh == 199) {
                int giáTrịĐích = vịTrí + dữLiệuLệnh.đọcNgắnKiểuCóDấu(); danhSáchNhánh.add(giáTrịĐích); Collections.addAll(dòng,"popl %eax","testl %eax, %eax",(lệnh == 198 ? "je " : "jne ") + giáTrịDấuMốc + "_b" + giáTrịĐích);
            } else throw new LỗiBảnDịch("làKhôngHỗTrợ lệnh: " + lệnh);
        }
        if (!danhSáchCácRanhGiới.containsAll(danhSáchNhánh)) throw new LỗiBảnDịch("lệnh 경계가 아닌 곳으로 nhánh");
        dòng.add(".size " + giáTrịDấuMốc + ", .-" + giáTrịDấuMốc); return String.join("\n",dòng);
    }
    String hằngX86(DữLiệuLớp DữLiệu, int sốHiệu) {
        if (DữLiệu.loạiHằng[sốHiệu] == 3) return DữLiệu.dữLiệuHằng[sốHiệu].toString();
        if (DữLiệu.loạiHằng[sốHiệu] == 8) return kýHiệuChuỗi(DữLiệu.KýTự((Integer)DữLiệu.dữLiệuHằng[sốHiệu]));
        throw new LỗiBảnDịch("정수와 ChuỗiKýTự 상수만 giáTrịHỗTrợ");
    }
    String hợpNgữX86(String điểmMục, List<String> giáTrịĐãXuất, String giáTrịĐốiĐích) throws IOException {
        Map<String,String> bảngTraMáy = new HashMap<>();
        for (String dòng : Files.readAllLines(đườngDẫnTàiNguyên.resolve("HàmMáyX86.tsv"))) { String[] giáTrịCặp = dòng.split("\t"); if (giáTrịCặp[0].equals(giáTrịĐốiĐích)) bảngTraMáy.put(giáTrịCặp[1] + giáTrịCặp[2],giáTrịCặp[3]); }
        int chỉSốVịTrí = điểmMục.lastIndexOf('.'); if (chỉSốVịTrí < 0) throw new LỗiBảnDịch("điểmMục giáTrịGán lỗi");
        String giáTrịChủSởHữu = điểmMục.substring(0,chỉSốVịTrí).replace('.','/'), tênMụcPhươngThức = điểmMục.substring(chỉSốVịTrí + 1); ThamChiếuPhươngThức giáTrịĐiểmMục = null;
        for (String giáTrịMôTả : Arrays.asList("()I","()V")) { ThamChiếuPhươngThức thamChiếu = new ThamChiếuPhươngThức(giáTrịChủSởHữu,tênMụcPhươngThức,giáTrịMôTả); if (danhSáchCácPhươngThức.containsKey(thamChiếu)) { if (giáTrịĐiểmMục != null) throw new LỗiBảnDịch("겹친 điểmMục"); giáTrịĐiểmMục = thamChiếu; } }
        if (giáTrịĐiểmMục == null || (danhSáchCácPhươngThức.get(giáTrịĐiểmMục).mụcTruyCập & 0x100) != 0) throw new LỗiBảnDịch("giáTrịĐiểmMục Hàm giáTrịĐịnhDạng lỗi");
        List<String> dòng = new ArrayList<>(); dòng.add(".code32");
        for (DữLiệuLớp DữLiệu : danhSáchCácLớp.values()) {
            String giáTrịTrạngThái = kýHiệu("state",DữLiệu.tên), khởiTạo = kýHiệu("init",DữLiệu.tên);
            Collections.addAll(dòng,".bss",".balign 4",giáTrịTrạngThái + ": .long 0",".text",khởiTạo + ":","cmpl $0, " + giáTrịTrạngThái,"jne " + khởiTạo + "_done","movl $1, " + giáTrịTrạngThái);
            ThamChiếuPhươngThức thamChiếuBộKhởiTạo = new ThamChiếuPhươngThức(DữLiệu.tên,"<clinit>","()V"); if (danhSáchCácPhươngThức.containsKey(thamChiếuBộKhởiTạo)) dòng.add("call " + kýHiệu("method",thamChiếuBộKhởiTạo.cácPhần()));
            Collections.addAll(dòng,"movl $2, " + giáTrịTrạngThái,khởiTạo + "_done:","ret");
            for (DữLiệuThànhViên giáTrịTrường : DữLiệu.giáTrịTrường) {
                byte[] giáTrịHằng = giáTrịTrường.giáTrịThuộcTính.get("ConstantValue"); String giáTrị = giáTrịHằng == null ? "0" : hằngX86(DữLiệu,new BộĐọcDữLiệu(giáTrịHằng).đọcNgắnKiểu());
                Collections.addAll(dòng,".data",".balign 4",kýHiệu("field",DữLiệu.tên,giáTrịTrường.tên,giáTrịTrường.giáTrịMôTả) + ": .long " + giáTrị);
            }
            for (DữLiệuThànhViên Hàm : DữLiệu.Hàm) if (!Hàm.tên.equals("<init>")) dòng.add(thânHàmX86(new ThamChiếuPhươngThức(DữLiệu.tên,Hàm.tên,Hàm.giáTrịMôTả),Hàm,bảngTraMáy,giáTrịĐốiĐích));
        }
        Collections.addAll(dòng,".text",".globl java_entry","java_entry:","call " + kýHiệu("init",giáTrịĐiểmMục.giáTrịChủSởHữu),"call " + kýHiệu("method",giáTrịĐiểmMục.cácPhần()));
        if (giáTrịĐiểmMục.giáTrịMôTả.equals("()V")) dòng.add("xorl %eax, %eax"); dòng.add("ret");
        for (String giáTrịGán : giáTrịĐãXuất) {
            int giáTrịDấuPhânCách = giáTrịGán.indexOf('='); if (giáTrịDấuPhânCách < 1) throw new LỗiBảnDịch("phátGiáTrị giáTrịGán lỗi");
            String giáTrịBênNgoài = giáTrịGán.substring(0,giáTrịDấuPhânCách), Hàm = giáTrịGán.substring(giáTrịDấuPhânCách + 1); int kếtQuảPhépChia = Hàm.lastIndexOf('.');
            if (kếtQuảPhépChia < 0 || !giáTrịBênNgoài.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new LỗiBảnDịch("phátGiáTrị kýHiệu lỗi");
            String giáTrịLớp = Hàm.substring(0,kếtQuảPhépChia).replace('.','/'), tên = Hàm.substring(kếtQuảPhépChia + 1); ThamChiếuPhươngThức giáTrịViệcChọn = null;
            for (ThamChiếuPhươngThức thamChiếu : danhSáchCácPhươngThức.keySet()) if (thamChiếu.giáTrịChủSởHữu.equals(giáTrịLớp) && thamChiếu.tên.equals(tên)) { if (giáTrịViệcChọn != null) throw new LỗiBảnDịch("겹친 phátGiáTrị giáTrịĐốiĐích"); giáTrịViệcChọn = thamChiếu; }
            if (giáTrịViệcChọn == null) throw new LỗiBảnDịch("내보낼 함수가 phươngThứcThiếu");
            Collections.addAll(dòng,".text",".globl " + giáTrịBênNgoài,giáTrịBênNgoài + ":","call " + kýHiệu("init",giáTrịViệcChọn.giáTrịChủSởHữu),"jmp " + kýHiệu("method",giáTrịViệcChọn.cácPhần()));
        }
        dòng.add(".section .rodata");
        for (Map.Entry<String,String> giáTrịMục : cácGiáTrịChuỗi.entrySet()) {
            Collections.addAll(dòng,".balign 4",giáTrịMục.getValue() + ":",".long " + giáTrịMục.getKey().length());
            List<String> danhSáchCácĐơnVị = new ArrayList<>(); for (char giáTrịĐơnVị : giáTrịMục.getKey().toCharArray()) danhSáchCácĐơnVị.add(Integer.toString(giáTrịĐơnVị)); if (!danhSáchCácĐơnVị.isEmpty()) dòng.add(".long " + String.join(",",danhSáchCácĐơnVị));
        }
        dòng.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",dòng) + "\n";
    }
    static void thựcThiCôngCụ(List<String> lệnh) throws Exception {
        if (new ProcessBuilder(lệnh).inheritIO().start().waitFor() != 0) throw new LỗiBảnDịch("biênDịchNguồn lỗi: " + lệnh.get(0));
    }
    static String chuỗiDữLiệu(String vănBản) { return "\"" + vănBản.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void bảnBiênDịchX86(List<Path> danhSáchĐầuVào, String giáTrịĐốiĐích, String điểmMục, List<String> giáTrịĐãXuất, Path ĐầuRa, Path giáTrịTàiNguyên) throws Exception {
        Path giáTrịTạm = Files.createTempDirectory("jkoros-java-x86-"), đườngDẫnLớp = giáTrịTạm.resolve("classes"); Files.createDirectory(đườngDẫnLớp);
        try {
            List<String> lệnhJava = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",đườngDẫnLớp.toString(),"-sourcepath",đườngDẫnLớp.toString(),"-d",đườngDẫnLớp.toString()));
            List<Path> mãByte = new ArrayList<>(); int sốLượngNguồn = 0;
            for (Path giáTrịVào : danhSáchĐầuVào) {
                if (ĐầuRa.toAbsolutePath().normalize().equals(giáTrịVào.toAbsolutePath().normalize())) throw new LỗiBảnDịch("ĐầuRa 파일과 입력이 vănBảnBằng");
                if (giáTrịVào.toString().endsWith(".java")) { lệnhJava.add(giáTrịVào.toString()); sốLượngNguồn++; }
                else if (giáTrịVào.toString().endsWith(".class")) mãByte.add(giáTrịVào);
                else throw new LỗiBảnDịch(".java 또는 .class만 giáTrịHỗTrợ");
            }
            if (sốLượngNguồn > 0) thựcThiCôngCụ(lệnhJava);
            try (java.util.stream.Stream<Path> danhSáchĐườngDẫn = Files.walk(đườngDẫnLớp)) { danhSáchĐườngDẫn.filter(đườngDẫn -> đườngDẫn.toString().endsWith(".class")).sorted().forEach(mãByte::add); }
            BiênDịchTrước chuyểnĐổiGiáTrị = new BiênDịchTrước(mãByte,giáTrịĐốiĐích.equals("user") ? "user" : "kernel",262144,giáTrịTàiNguyên);
            String hợpDịchGiáTrị = chuyểnĐổiGiáTrị.hợpNgữX86(điểmMục,giáTrịĐãXuất,giáTrịĐốiĐích); Files.writeString(giáTrịTạm.resolve("program.s"),hợpDịchGiáTrị,StandardCharsets.UTF_8);
            Path vịTríCôngCụ = giáTrịTàiNguyên.getParent();
            thựcThiCôngCụ(Arrays.asList("as","--32","-o",giáTrịTạm.resolve("program.o").toString(),giáTrịTạm.resolve("program.s").toString()));
            thựcThiCôngCụ(Arrays.asList("as","--32","-o",giáTrịTạm.resolve("runtime.o").toString(),vịTríCôngCụ.resolve("HỗTrợMôiTrườngChạy.s").toString()));
            List<String> nốiKết = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (giáTrịĐốiĐích.equals("kernel")) nốiKết.add("-r");
            else {
                thựcThiCôngCụ(Arrays.asList("as","--32","-o",giáTrịTạm.resolve("start.o").toString(),vịTríCôngCụ.resolve(giáTrịĐốiĐích.equals("user") ? "bắtChạyChươngTrìnhNgườiDùng.s" : "lúcKhởiChạyLinux.s").toString()));
                Collections.addAll(nốiKết,"-e","_start",giáTrịTạm.resolve("start.o").toString());
                if (giáTrịĐốiĐích.equals("user")) Collections.addAll(nốiKết,"-T",vịTríCôngCụ.resolve("bốTríLiênKếtNgườiDùng.ld").toString());
            }
            Collections.addAll(nốiKết,"-o",giáTrịTạm.resolve("result").toString(),giáTrịTạm.resolve("program.o").toString(),giáTrịTạm.resolve("runtime.o").toString()); thựcThiCôngCụ(nốiKết);
            ĐầuRa = ĐầuRa.toAbsolutePath(); Files.createDirectories(ĐầuRa.getParent()); Path giáTrịCôngBố = Files.createTempFile(ĐầuRa.getParent(),".elf-",".tmp");
            try { Files.copy(giáTrịTạm.resolve("result"),giáTrịCôngBố,StandardCopyOption.REPLACE_EXISTING); Files.move(giáTrịCôngBố,ĐầuRa,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(giáTrịCôngBố); }
            Files.setPosixFilePermissions(ĐầuRa,java.nio.file.attribute.PosixFilePermissions.fromString(giáTrịĐốiĐích.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(ĐầuRa + ".s"),hợpDịchGiáTrị,StandardCharsets.UTF_8);
            List<String> dữLiệuKýHiệu = new ArrayList<>(), dữLiệuNguồn = new ArrayList<>();
            for (ThamChiếuPhươngThức thamChiếu : chuyểnĐổiGiáTrị.danhSáchCácPhươngThức.keySet()) dữLiệuKýHiệu.add(chuỗiDữLiệu(kýHiệu("method",thamChiếu.cácPhần())) + ":" + chuỗiDữLiệu(thamChiếu.giáTrịChủSởHữu + "." + thamChiếu.tên + thamChiếu.giáTrịMôTả));
            for (Path giáTrịVào : danhSáchĐầuVào) {
                byte[] tệpMãBăm = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(giáTrịVào)); StringBuilder vănBản = new StringBuilder(); for (byte giáTrị : tệpMãBăm) vănBản.append(String.format(Locale.ROOT,"%02x",giáTrị & 255));
                dữLiệuNguồn.add(chuỗiDữLiệu(giáTrịVào.toAbsolutePath().toString()) + ":" + chuỗiDữLiệu(vănBản.toString()));
            }
            Files.writeString(Paths.get(ĐầuRa + ".json"),"{\"target\":" + chuỗiDữLiệu(giáTrịĐốiĐích) + ",\"entry\":" + chuỗiDữLiệu(điểmMục) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",dữLiệuKýHiệu) + "},\"sources\":{" + String.join(",",dữLiệuNguồn) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> danhSáchĐườngDẫn = Files.walk(giáTrịTạm)) { for (Path đườngDẫn : (Iterable<Path>)danhSáchĐườngDẫn.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(đườngDẫn); }
        }
    }
    public static void main(String[] cácĐốiSố) {
        try {
            String điểmMục = null, giáTrịĐốiĐích = "kernel", đíchX86 = null; Path đườngDẫnĐầuRa = null; int sốLượngTừTừVựng = 262144; boolean cáchKýHiệuPhổQuát = false;
            List<String> giáTrịĐãXuất = new ArrayList<>(); List<Path> danhSáchĐườngDẫn = new ArrayList<>();
            for (int chỉSốThứBậc = 0; chỉSốThứBậc < cácĐốiSố.length; chỉSốThứBậc++) {
                String giáTrị = cácĐốiSố[chỉSốThứBậc];
                switch (giáTrị) {
                    case "--target": đíchX86 = cácĐốiSố[++chỉSốThứBậc]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry giáTrịLớp.Hàm -o ĐầuRa [--target linux|kernel|user] [--profile kernel|user] [--export kýHiệu=giáTrịLớp.Hàm] 클래스파일 또는 Java원문"); return;
                    case "--entry": điểmMục = cácĐốiSố[++chỉSốThứBậc]; break;
                    case "--profile": giáTrịĐốiĐích = cácĐốiSố[++chỉSốThứBậc]; break;
                    case "--heap-words": sốLượngTừTừVựng = Integer.parseInt(cácĐốiSố[++chỉSốThứBậc]); break;
                    case "--export": giáTrịĐãXuất.add(cácĐốiSố[++chỉSốThứBậc]); break;
                    case "-o": đườngDẫnĐầuRa = Paths.get(cácĐốiSố[++chỉSốThứBậc]); break;
                    case "--ucn": cáchKýHiệuPhổQuát = true; break;
                    default: if (giáTrị.startsWith("-")) throw new LỗiBảnDịch("알 trịSố 없는 옵션: " + giáTrị); danhSáchĐườngDẫn.add(Paths.get(giáTrị));
                }
            }
            if (điểmMục == null || đườngDẫnĐầuRa == null || danhSáchĐườngDẫn.isEmpty()) throw new LỗiBảnDịch("--entry, -o, giáTrịLớp 파일이 필요합니다");
            Path giáTrịTàiNguyên = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (đíchX86 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(đíchX86)) throw new LỗiBảnDịch("알 trịSố 없는 thựcThiLệnh giáTrịĐốiĐích");
                bảnBiênDịchX86(danhSáchĐườngDẫn,đíchX86,điểmMục,giáTrịĐãXuất,đườngDẫnĐầuRa,giáTrịTàiNguyên); return;
            }
            String mãNguồn = new BiênDịchTrước(danhSáchĐườngDẫn, giáTrịĐốiĐích, sốLượngTừTừVựng, giáTrịTàiNguyên).sinh(điểmMục, giáTrịĐãXuất, cáchKýHiệuPhổQuát);
            đườngDẫnĐầuRa = đườngDẫnĐầuRa.toAbsolutePath(); Files.createDirectories(đườngDẫnĐầuRa.getParent());
            Path giáTrịTạm = Files.createTempFile(đườngDẫnĐầuRa.getParent(), ".aot-", ".tmp");
            try { Files.writeString(giáTrịTạm, mãNguồn, StandardCharsets.UTF_8); Files.move(giáTrịTạm, đườngDẫnĐầuRa, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(giáTrịTạm); }
        } catch (Exception lỗi) { System.err.println("biênDịchNguồn lỗi: " + lỗi.getMessage()); System.exit(1); }
    }
}
