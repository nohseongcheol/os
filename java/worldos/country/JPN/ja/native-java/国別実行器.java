// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 独立した国別版の依存関係の検査・復元、ビルド、実行を担うホスト Java 道具。 */
public final class 国別実行器 {
    static final class データ構文解析器 {
        final String ソース; int 位置;
        データ構文解析器(String 文) { ソース = 文; }
        void 空白読飛ばし() { while (位置 < ソース.length() && Character.isWhitespace(ソース.charAt(位置))) 位置++; }
        Object 読取() {
            空白読飛ばし(); char 文字値 = ソース.charAt(位置++);
            if (文字値 == '{') {
                Map<String,Object> 結果 = new LinkedHashMap<>(); 空白読飛ばし();
                if (ソース.charAt(位置) == '}') { 位置++; return 結果; }
                while (true) {
                    String 名前 = (String)読取(); 空白読飛ばし(); if (ソース.charAt(位置++) != ':') throw new IllegalArgumentException("データ 区切り記号値 エラー");
                    結果.put(名前, 読取()); 空白読飛ばし(); char 区切り記号値 = ソース.charAt(位置++);
                    if (区切り記号値 == '}') return 結果; if (区切り記号値 != ',') throw new IllegalArgumentException("データ 区切り記号値 エラー");
                }
            }
            if (文字値 == '[') {
                List<Object> 結果 = new ArrayList<>(); 空白読飛ばし();
                if (ソース.charAt(位置) == ']') { 位置++; return 結果; }
                while (true) {
                    結果.add(読取()); 空白読飛ばし(); char 区切り記号値 = ソース.charAt(位置++);
                    if (区切り記号値 == ']') return 結果; if (区切り記号値 != ',') throw new IllegalArgumentException("データ 区切り記号値 エラー");
                }
            }
            if (文字値 == '"') {
                StringBuilder 結果 = new StringBuilder();
                while (true) {
                    char 次回項目 = ソース.charAt(位置++); if (次回項目 == '"') return 結果.toString();
                    if (次回項目 == '\\') {
                        次回項目 = ソース.charAt(位置++);
                        if (次回項目 == 'u') { 結果.append((char)Integer.parseInt(ソース.substring(位置, 位置 + 4),16)); 位置 += 4; continue; }
                        if (次回項目 == 'n') 次回項目 = '\n'; else if (次回項目 == 'r') 次回項目 = '\r'; else if (次回項目 == 't') 次回項目 = '\t';
                        else if (次回項目 == 'b') 次回項目 = '\b'; else if (次回項目 == 'f') 次回項目 = '\f';
                        else if (次回項目 != '"' && 次回項目 != '\\' && 次回項目 != '/') throw new IllegalArgumentException("文字 이스케이프 エラー");
                    }
                    結果.append(次回項目);
                }
            }
            int 起動処理 = 位置 - 1;
            while (位置 < ソース.length() && ",]} \t\r\n".indexOf(ソース.charAt(位置)) < 0) 位置++;
            String 値 = ソース.substring(起動処理, 位置);
            if (値.equals("true")) return Boolean.TRUE; if (値.equals("false")) return Boolean.FALSE; if (値.equals("null")) return null;
            return Double.valueOf(値);
        }
    }
    static String ハッシュファイル(Path 経路) throws Exception {
        MessageDigest 計算結果 = MessageDigest.getInstance("SHA-256"); byte[] データ = new byte[1024 * 1024];
        try (InputStream 入力値 = Files.newInputStream(経路)) { for (int 長さ; (長さ = 入力値.read(データ)) >= 0;) 計算結果.update(データ,0,長さ); }
        return ハッシュ本文(計算結果.digest());
    }
    static String ハッシュ本文(byte[] データ) {
        StringBuilder 文 = new StringBuilder(); for (byte 値 : データ) 文.append(String.format(Locale.ROOT,"%02x",値 & 255)); return 文.toString();
    }
    static Path 内部経路(Path 計画根, String 名前) {
        Path 結果 = 計画根.resolve(名前).normalize();
        if (名前.isEmpty() || Paths.get(名前).isAbsolute() || !結果.startsWith(計画根) || 名前.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 経路: " + 名前);
        for (Path 部分要素値 : Paths.get(名前)) if (部分要素値.toString().equals("..")) throw new IllegalArgumentException("상위 経路 禁止対象値: " + 名前);
        for (Path 現在項目 = 結果; 現在項目 != null && 現在項目.startsWith(計画根); 現在項目 = 現在項目.getParent())
            if (Files.isSymbolicLink(現在項目)) throw new IllegalArgumentException("依存項目 경로의 링크 禁止対象値: " + 名前);
        return 結果;
    }
    static String 命令出力(List<String> 命令) throws Exception {
        Process プロセス値 = new ProcessBuilder(命令).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 結果 = new String(プロセス値.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (プロセス値.waitFor() != 0) throw new IOException("命令 失敗値: " + 命令.get(0)); return 結果;
    }
    static void 抽出(Path 書庫値, Path 宛先値) throws Exception {
        for (String 名前 : 命令出力(Arrays.asList("tar","-tzf",書庫値.toString())).split("\n")) 内部経路(宛先値, 名前);
        for (String 行 : 命令出力(Arrays.asList("tar","-tvzf",書庫値.toString())).split("\n"))
            if (!行.isEmpty() && 行.charAt(0) != '-' && 行.charAt(0) != 'd') throw new IOException("外部値 링크 또는 特殊値 파일을 포함한 依存項目");
        Files.createDirectories(宛先値);
        int 状況値 = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",書庫値.toString(),"-C",宛先値.toString()).inheritIO().start().waitFor();
        if (状況値 != 0) throw new IOException("依存項目 書庫値 記憶装置解放 失敗値");
    }
    static void 呼出(Path 作業中経路, Path 道具, List<String> 引数, Map<String,String> 環境) throws Exception {
        List<String> 命令 = new ArrayList<>(Arrays.asList("python3", 道具.toString())); 命令.addAll(引数);
        ProcessBuilder 命令実行 = new ProcessBuilder(命令).directory(作業中経路.toFile()).inheritIO(); 命令実行.environment().putAll(環境);
        int 状況値 = 命令実行.start().waitFor(); if (状況値 != 0) throw new IOException("道具 失敗値: " + 道具 + " (" + 状況値 + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 引数) throws Exception {
        if (引数.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String 動作 = 引数[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(動作)) throw new IllegalArgumentException("알 数 없는 動作");
        Path 計画根 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> 設定値 = (Map<String,Object>)new データ構文解析器(Files.readString(計画根.resolve("native.json"),StandardCharsets.UTF_8)).読取();
        Path ソース木 = 内部経路(計画根,(String)設定値.get("source")), 中核値 = 内部経路(ソース木,(String)設定値.get("native"));
        List<String> 所有対象ファイル群 = (List<String>)(List<?>)設定値.get("owned_files");
        for (String 名前 : 所有対象ファイル群) if (!Files.isRegularFile(内部経路(ソース木,名前))) throw new IOException("ソース木 未存在メソッド: " + 名前);
        if (動作.equals("check")) { System.out.println(設定値.get("country") + " " + 設定値.get("language") + " 독립 ソース木 検証 判定完了"); return; }
        String 資源相対経路 = (String)設定値.getOrDefault("resource_root", ".");
        if (!資源相対経路.equals(".") && !資源相対経路.equals("..")) throw new IllegalArgumentException("依存項目 計画根 経路 エラー");
        Path 資源値 = 計画根.resolve(資源相対経路).normalize(); Path 書庫値 = 資源値.resolve("native-vendor.tar.gz");
        String 期待ハッシュ = (String)設定値.get("vendor_sha256");
        if (!ハッシュファイル(書庫値).equals(期待ハッシュ)) throw new IOException("依存項目 SHA-256 불일치");
        Path 標識値 = ソース木.resolve(".vendor-sha256");
        if (!Files.isRegularFile(標識値) || !Files.readString(標識値).trim().equals(期待ハッシュ)) { 抽出(書庫値, ソース木); Files.writeString(標識値,期待ハッシュ + "\n"); }
        Map<String,String> 環境 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (環境.containsKey("IP_CONFIG")) ipConfig = Paths.get(環境.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 計画根; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = ソース木.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        環境.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(動作) && !環境.containsKey("QEMU_AARCH64")) {
            Path プログラム実行器 = 資源値.resolve("host/qemu"), 実行器標識 = 資源値.resolve("host/.qemu-sha256");
            String 実行器ハッシュ = (String)設定値.get("qemu_sha256");
            if (!Files.isRegularFile(プログラム実行器) || !Files.isRegularFile(実行器標識) || !Files.readString(実行器標識).trim().equals(実行器ハッシュ)) {
                Path 実行器書庫 = 資源値.resolve("qemu-host.tar.gz"); if (!ハッシュファイル(実行器書庫).equals(実行器ハッシュ)) throw new IOException("QEMU SHA-256 불일치");
                抽出(実行器書庫,資源値.resolve("host")); Files.writeString(実行器標識,実行器ハッシュ + "\n");
            }
            環境.put("QEMU_AARCH64",プログラム実行器.toString());
        }
        MessageDigest 計算結果 = MessageDigest.getInstance("SHA-256"); Collections.sort(所有対象ファイル群);
        for (String 名前 : 所有対象ファイル群) { 計算結果.update(名前.getBytes(StandardCharsets.UTF_8)); 計算結果.update(Files.readAllBytes(内部経路(ソース木,名前))); }
        計算結果.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 計算結果.update(Files.readAllBytes(ipConfig));
        String ソースハッシュ = ハッシュ本文(計算結果.digest()); Path 標識構築 = 中核値.resolve("build/worldos-source.sha256");
        if (動作.equals("build") || !Files.isRegularFile(標識構築) || !Files.readString(標識構築).trim().equals(ソースハッシュ)) {
            呼出(中核値,内部経路(中核値,(String)設定値.get("builder")),Collections.emptyList(),環境);
            Files.writeString(標識構築,ソースハッシュ + "\n");
        }
        List<String> 実行器引数列 = new ArrayList<>(Arrays.asList(引数).subList(1,引数.length));
        if (動作.equals("run") || 動作.equals("desktop")) {
            if (動作.equals("desktop")) 実行器引数列.add(0,"--desktop");
            呼出(中核値,内部経路(中核値,(String)設定値.get("runner")),実行器引数列,環境);
        } else if (動作.equals("image")) 呼出(中核値,内部経路(中核値,(String)設定値.get("image_builder")),実行器引数列,環境);
        else if (動作.equals("test-system")) {
            実行器引数列.add(0,計画根.toString()); 実行器引数列.add(0,"--edition");
            呼出(中核値,内部経路(中核値,(String)設定値.get("system_tester")),実行器引数列,環境);
        }
    }
}
