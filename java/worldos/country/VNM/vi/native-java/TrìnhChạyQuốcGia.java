// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** Công cụ Java trên máy chủ kiểm tra, khôi phục phụ thuộc, biên dịch và chạy bản quốc gia độc lập. */
public final class TrìnhChạyQuốcGia {
    static final class BộPhânTíchDữLiệu {
        final String mãNguồn; int vịTrí;
        BộPhânTíchDữLiệu(String vănBản) { mãNguồn = vănBản; }
        void bỏKhoảngTrắng() { while (vịTrí < mãNguồn.length() && Character.isWhitespace(mãNguồn.charAt(vịTrí))) vịTrí++; }
        Object đọc() {
            bỏKhoảngTrắng(); char giáTrịKýTự = mãNguồn.charAt(vịTrí++);
            if (giáTrịKýTự == '{') {
                Map<String,Object> kếtQuả = new LinkedHashMap<>(); bỏKhoảngTrắng();
                if (mãNguồn.charAt(vịTrí) == '}') { vịTrí++; return kếtQuả; }
                while (true) {
                    String tên = (String)đọc(); bỏKhoảngTrắng(); if (mãNguồn.charAt(vịTrí++) != ':') throw new IllegalArgumentException("DữLiệu giáTrịDấuPhânCách lỗi");
                    kếtQuả.put(tên, đọc()); bỏKhoảngTrắng(); char giáTrịDấuPhânCách = mãNguồn.charAt(vịTrí++);
                    if (giáTrịDấuPhânCách == '}') return kếtQuả; if (giáTrịDấuPhânCách != ',') throw new IllegalArgumentException("DữLiệu giáTrịDấuPhânCách lỗi");
                }
            }
            if (giáTrịKýTự == '[') {
                List<Object> kếtQuả = new ArrayList<>(); bỏKhoảngTrắng();
                if (mãNguồn.charAt(vịTrí) == ']') { vịTrí++; return kếtQuả; }
                while (true) {
                    kếtQuả.add(đọc()); bỏKhoảngTrắng(); char giáTrịDấuPhânCách = mãNguồn.charAt(vịTrí++);
                    if (giáTrịDấuPhânCách == ']') return kếtQuả; if (giáTrịDấuPhânCách != ',') throw new IllegalArgumentException("DữLiệu giáTrịDấuPhânCách lỗi");
                }
            }
            if (giáTrịKýTự == '"') {
                StringBuilder kếtQuả = new StringBuilder();
                while (true) {
                    char phầnMụcKếTiếp = mãNguồn.charAt(vịTrí++); if (phầnMụcKếTiếp == '"') return kếtQuả.toString();
                    if (phầnMụcKếTiếp == '\\') {
                        phầnMụcKếTiếp = mãNguồn.charAt(vịTrí++);
                        if (phầnMụcKếTiếp == 'u') { kếtQuả.append((char)Integer.parseInt(mãNguồn.substring(vịTrí, vịTrí + 4),16)); vịTrí += 4; continue; }
                        if (phầnMụcKếTiếp == 'n') phầnMụcKếTiếp = '\n'; else if (phầnMụcKếTiếp == 'r') phầnMụcKếTiếp = '\r'; else if (phầnMụcKếTiếp == 't') phầnMụcKếTiếp = '\t';
                        else if (phầnMụcKếTiếp == 'b') phầnMụcKếTiếp = '\b'; else if (phầnMụcKếTiếp == 'f') phầnMụcKếTiếp = '\f';
                        else if (phầnMụcKếTiếp != '"' && phầnMụcKếTiếp != '\\' && phầnMụcKếTiếp != '/') throw new IllegalArgumentException("KýTự 이스케이프 lỗi");
                    }
                    kếtQuả.append(phầnMụcKếTiếp);
                }
            }
            int chạy = vịTrí - 1;
            while (vịTrí < mãNguồn.length() && ",]} \t\r\n".indexOf(mãNguồn.charAt(vịTrí)) < 0) vịTrí++;
            String giáTrị = mãNguồn.substring(chạy, vịTrí);
            if (giáTrị.equals("true")) return Boolean.TRUE; if (giáTrị.equals("false")) return Boolean.FALSE; if (giáTrị.equals("null")) return null;
            return Double.valueOf(giáTrị);
        }
    }
    static String tệpMãBăm(Path đườngDẫn) throws Exception {
        MessageDigest phépTính = MessageDigest.getInstance("SHA-256"); byte[] DữLiệu = new byte[1024 * 1024];
        try (InputStream giáTrịVào = Files.newInputStream(đườngDẫn)) { for (int độDài; (độDài = giáTrịVào.read(DữLiệu)) >= 0;) phépTính.update(DữLiệu,0,độDài); }
        return vănBảnMãBăm(phépTính.digest());
    }
    static String vănBảnMãBăm(byte[] DữLiệu) {
        StringBuilder vănBản = new StringBuilder(); for (byte giáTrị : DữLiệu) vănBản.append(String.format(Locale.ROOT,"%02x",giáTrị & 255)); return vănBản.toString();
    }
    static Path đườngDẫnNộiBộ(Path gốcCâyDựÁn, String tên) {
        Path kếtQuả = gốcCâyDựÁn.resolve(tên).normalize();
        if (tên.isEmpty() || Paths.get(tên).isAbsolute() || !kếtQuả.startsWith(gốcCâyDựÁn) || tên.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 đườngDẫn: " + tên);
        for (Path giáTrịPhầnCon : Paths.get(tên)) if (giáTrịPhầnCon.toString().equals("..")) throw new IllegalArgumentException("상위 đườngDẫn giáTrịCấm: " + tên);
        for (Path phầnMụcHiệnTại = kếtQuả; phầnMụcHiệnTại != null && phầnMụcHiệnTại.startsWith(gốcCâyDựÁn); phầnMụcHiệnTại = phầnMụcHiệnTại.getParent())
            if (Files.isSymbolicLink(phầnMụcHiệnTại)) throw new IllegalArgumentException("cácPhụThuộc 경로의 링크 giáTrịCấm: " + tên);
        return kếtQuả;
    }
    static String đầuRaLệnh(List<String> lệnh) throws Exception {
        Process giáTrịTiếnTrình = new ProcessBuilder(lệnh).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String kếtQuả = new String(giáTrịTiếnTrình.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (giáTrịTiếnTrình.waitFor() != 0) throw new IOException("lệnh giáTrịSựThấtBại: " + lệnh.get(0)); return kếtQuả;
    }
    static void tríchXuất(Path giáTrịKhoLưuTrữ, Path giáTrịĐích) throws Exception {
        for (String tên : đầuRaLệnh(Arrays.asList("tar","-tzf",giáTrịKhoLưuTrữ.toString())).split("\n")) đườngDẫnNộiBộ(giáTrịĐích, tên);
        for (String dòng : đầuRaLệnh(Arrays.asList("tar","-tvzf",giáTrịKhoLưuTrữ.toString())).split("\n"))
            if (!dòng.isEmpty() && dòng.charAt(0) != '-' && dòng.charAt(0) != 'd') throw new IOException("giáTrịBênNgoài 링크 또는 giáTrịĐặcBiệt 파일을 포함한 cácPhụThuộc");
        Files.createDirectories(giáTrịĐích);
        int giáTrịTrạngThái = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",giáTrịKhoLưuTrữ.toString(),"-C",giáTrịĐích.toString()).inheritIO().start().waitFor();
        if (giáTrịTrạngThái != 0) throw new IOException("cácPhụThuộc giáTrịKhoLưuTrữ giảiPhóngLưuTrữ giáTrịSựThấtBại");
    }
    static void gọiThựcHiện(Path đườngDẫnĐangLàmViệc, Path CôngCụ, List<String> cácĐốiSố, Map<String,String> môiTrường) throws Exception {
        List<String> lệnh = new ArrayList<>(Arrays.asList("python3", CôngCụ.toString())); lệnh.addAll(cácĐốiSố);
        ProcessBuilder thựcThiLệnh = new ProcessBuilder(lệnh).directory(đườngDẫnĐangLàmViệc.toFile()).inheritIO(); thựcThiLệnh.environment().putAll(môiTrường);
        int giáTrịTrạngThái = thựcThiLệnh.start().waitFor(); if (giáTrịTrạngThái != 0) throw new IOException("CôngCụ giáTrịSựThấtBại: " + CôngCụ + " (" + giáTrịTrạngThái + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] cácĐốiSố) throws Exception {
        if (cácĐốiSố.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String hànhĐộng = cácĐốiSố[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(hànhĐộng)) throw new IllegalArgumentException("알 trịSố 없는 hànhĐộng");
        Path gốcCâyDựÁn = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> cácThiếtLập = (Map<String,Object>)new BộPhânTíchDữLiệu(Files.readString(gốcCâyDựÁn.resolve("native.json"),StandardCharsets.UTF_8)).đọc();
        Path câyNguồn = đườngDẫnNộiBộ(gốcCâyDựÁn,(String)cácThiếtLập.get("source")), giáTrịNhân = đườngDẫnNộiBộ(câyNguồn,(String)cácThiếtLập.get("native"));
        List<String> cácTệpThuộcDựÁn = (List<String>)(List<?>)cácThiếtLập.get("owned_files");
        for (String tên : cácTệpThuộcDựÁn) if (!Files.isRegularFile(đườngDẫnNộiBộ(câyNguồn,tên))) throw new IOException("câyNguồn phươngThứcThiếu: " + tên);
        if (hànhĐộng.equals("check")) { System.out.println(cácThiếtLập.get("country") + " " + cácThiếtLập.get("language") + " 독립 câyNguồn xácMinh làĐầyĐủ"); return; }
        String đườngDẫnTươngĐốiTàiNguyên = (String)cácThiếtLập.getOrDefault("resource_root", ".");
        if (!đườngDẫnTươngĐốiTàiNguyên.equals(".") && !đườngDẫnTươngĐốiTàiNguyên.equals("..")) throw new IllegalArgumentException("cácPhụThuộc gốcCâyDựÁn đườngDẫn lỗi");
        Path giáTrịTàiNguyên = gốcCâyDựÁn.resolve(đườngDẫnTươngĐốiTàiNguyên).normalize(); Path giáTrịKhoLưuTrữ = giáTrịTàiNguyên.resolve("native-vendor.tar.gz");
        String mãBămDựKiến = (String)cácThiếtLập.get("vendor_sha256");
        if (!tệpMãBăm(giáTrịKhoLưuTrữ).equals(mãBămDựKiến)) throw new IOException("cácPhụThuộc SHA-256 불일치");
        Path giáTrịDấuMốc = câyNguồn.resolve(".vendor-sha256");
        if (!Files.isRegularFile(giáTrịDấuMốc) || !Files.readString(giáTrịDấuMốc).trim().equals(mãBămDựKiến)) { tríchXuất(giáTrịKhoLưuTrữ, câyNguồn); Files.writeString(giáTrịDấuMốc,mãBămDựKiến + "\n"); }
        Map<String,String> môiTrường = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (môiTrường.containsKey("IP_CONFIG")) ipConfig = Paths.get(môiTrường.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = gốcCâyDựÁn; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = câyNguồn.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        môiTrường.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(hànhĐộng) && !môiTrường.containsKey("QEMU_AARCH64")) {
            Path TrìnhKhởiChạyChươngTrình = giáTrịTàiNguyên.resolve("host/qemu"), dấuMốcTrìnhKhởiChạy = giáTrịTàiNguyên.resolve("host/.qemu-sha256");
            String mãBămTrìnhKhởiChạy = (String)cácThiếtLập.get("qemu_sha256");
            if (!Files.isRegularFile(TrìnhKhởiChạyChươngTrình) || !Files.isRegularFile(dấuMốcTrìnhKhởiChạy) || !Files.readString(dấuMốcTrìnhKhởiChạy).trim().equals(mãBămTrìnhKhởiChạy)) {
                Path khoLưuTrữTrìnhKhởiChạy = giáTrịTàiNguyên.resolve("qemu-host.tar.gz"); if (!tệpMãBăm(khoLưuTrữTrìnhKhởiChạy).equals(mãBămTrìnhKhởiChạy)) throw new IOException("QEMU SHA-256 불일치");
                tríchXuất(khoLưuTrữTrìnhKhởiChạy,giáTrịTàiNguyên.resolve("host")); Files.writeString(dấuMốcTrìnhKhởiChạy,mãBămTrìnhKhởiChạy + "\n");
            }
            môiTrường.put("QEMU_AARCH64",TrìnhKhởiChạyChươngTrình.toString());
        }
        MessageDigest phépTính = MessageDigest.getInstance("SHA-256"); Collections.sort(cácTệpThuộcDựÁn);
        for (String tên : cácTệpThuộcDựÁn) { phépTính.update(tên.getBytes(StandardCharsets.UTF_8)); phépTính.update(Files.readAllBytes(đườngDẫnNộiBộ(câyNguồn,tên))); }
        phépTính.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); phépTính.update(Files.readAllBytes(ipConfig));
        String mãBămNguồn = vănBảnMãBăm(phépTính.digest()); Path xâyDựngDấuMốc = giáTrịNhân.resolve("build/worldos-source.sha256");
        if (hànhĐộng.equals("build") || !Files.isRegularFile(xâyDựngDấuMốc) || !Files.readString(xâyDựngDấuMốc).trim().equals(mãBămNguồn)) {
            gọiThựcHiện(giáTrịNhân,đườngDẫnNộiBộ(giáTrịNhân,(String)cácThiếtLập.get("builder")),Collections.emptyList(),môiTrường);
            Files.writeString(xâyDựngDấuMốc,mãBămNguồn + "\n");
        }
        List<String> cácĐốiSốTrìnhKhởiChạy = new ArrayList<>(Arrays.asList(cácĐốiSố).subList(1,cácĐốiSố.length));
        if (hànhĐộng.equals("run") || hànhĐộng.equals("desktop")) {
            if (hànhĐộng.equals("desktop")) cácĐốiSốTrìnhKhởiChạy.add(0,"--desktop");
            gọiThựcHiện(giáTrịNhân,đườngDẫnNộiBộ(giáTrịNhân,(String)cácThiếtLập.get("runner")),cácĐốiSốTrìnhKhởiChạy,môiTrường);
        } else if (hànhĐộng.equals("image")) gọiThựcHiện(giáTrịNhân,đườngDẫnNộiBộ(giáTrịNhân,(String)cácThiếtLập.get("image_builder")),cácĐốiSốTrìnhKhởiChạy,môiTrường);
        else if (hànhĐộng.equals("test-system")) {
            cácĐốiSốTrìnhKhởiChạy.add(0,gốcCâyDựÁn.toString()); cácĐốiSốTrìnhKhởiChạy.add(0,"--edition");
            gọiThựcHiện(giáTrịNhân,đườngDẫnNộiBộ(giáTrịNhân,(String)cácThiếtLập.get("system_tester")),cácĐốiSốTrìnhKhởiChạy,môiTrường);
        }
    }
}
