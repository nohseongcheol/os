// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 負責獨立國家版相依性檢查、還原、建置與執行的主機 Java 工具。 */
public final class 國家執行器 {
    static final class 資料解析器 {
        final String 原始碼; int 位置;
        資料解析器(String 文本) { 原始碼 = 文本; }
        void 跳過空白() { while (位置 < 原始碼.length() && Character.isWhitespace(原始碼.charAt(位置))) 位置++; }
        Object 讀取() {
            跳過空白(); char 字元值 = 原始碼.charAt(位置++);
            if (字元值 == '{') {
                Map<String,Object> 結果 = new LinkedHashMap<>(); 跳過空白();
                if (原始碼.charAt(位置) == '}') { 位置++; return 結果; }
                while (true) {
                    String 名稱 = (String)讀取(); 跳過空白(); if (原始碼.charAt(位置++) != ':') throw new IllegalArgumentException("資料 分隔符值 錯誤");
                    結果.put(名稱, 讀取()); 跳過空白(); char 分隔符值 = 原始碼.charAt(位置++);
                    if (分隔符值 == '}') return 結果; if (分隔符值 != ',') throw new IllegalArgumentException("資料 分隔符值 錯誤");
                }
            }
            if (字元值 == '[') {
                List<Object> 結果 = new ArrayList<>(); 跳過空白();
                if (原始碼.charAt(位置) == ']') { 位置++; return 結果; }
                while (true) {
                    結果.add(讀取()); 跳過空白(); char 分隔符值 = 原始碼.charAt(位置++);
                    if (分隔符值 == ']') return 結果; if (分隔符值 != ',') throw new IllegalArgumentException("資料 分隔符值 錯誤");
                }
            }
            if (字元值 == '"') {
                StringBuilder 結果 = new StringBuilder();
                while (true) {
                    char 下一項目 = 原始碼.charAt(位置++); if (下一項目 == '"') return 結果.toString();
                    if (下一項目 == '\\') {
                        下一項目 = 原始碼.charAt(位置++);
                        if (下一項目 == 'u') { 結果.append((char)Integer.parseInt(原始碼.substring(位置, 位置 + 4),16)); 位置 += 4; continue; }
                        if (下一項目 == 'n') 下一項目 = '\n'; else if (下一項目 == 'r') 下一項目 = '\r'; else if (下一項目 == 't') 下一項目 = '\t';
                        else if (下一項目 == 'b') 下一項目 = '\b'; else if (下一項目 == 'f') 下一項目 = '\f';
                        else if (下一項目 != '"' && 下一項目 != '\\' && 下一項目 != '/') throw new IllegalArgumentException("字元 이스케이프 錯誤");
                    }
                    結果.append(下一項目);
                }
            }
            int 運行 = 位置 - 1;
            while (位置 < 原始碼.length() && ",]} \t\r\n".indexOf(原始碼.charAt(位置)) < 0) 位置++;
            String 值 = 原始碼.substring(運行, 位置);
            if (值.equals("true")) return Boolean.TRUE; if (值.equals("false")) return Boolean.FALSE; if (值.equals("null")) return null;
            return Double.valueOf(值);
        }
    }
    static String 哈希檔案(Path 路徑) throws Exception {
        MessageDigest 計算結果 = MessageDigest.getInstance("SHA-256"); byte[] 資料 = new byte[1024 * 1024];
        try (InputStream 輸入值 = Files.newInputStream(路徑)) { for (int 長度; (長度 = 輸入值.read(資料)) >= 0;) 計算結果.update(資料,0,長度); }
        return 哈希文本(計算結果.digest());
    }
    static String 哈希文本(byte[] 資料) {
        StringBuilder 文本 = new StringBuilder(); for (byte 值 : 資料) 文本.append(String.format(Locale.ROOT,"%02x",值 & 255)); return 文本.toString();
    }
    static Path 內部路徑(Path 項目根, String 名稱) {
        Path 結果 = 項目根.resolve(名稱).normalize();
        if (名稱.isEmpty() || Paths.get(名稱).isAbsolute() || !結果.startsWith(項目根) || 名稱.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 路徑: " + 名稱);
        for (Path 子部分值 : Paths.get(名稱)) if (子部分值.toString().equals("..")) throw new IllegalArgumentException("상위 路徑 禁用值: " + 名稱);
        for (Path 當前項目 = 結果; 當前項目 != null && 當前項目.startsWith(項目根); 當前項目 = 當前項目.getParent())
            if (Files.isSymbolicLink(當前項目)) throw new IllegalArgumentException("依賴項列 경로의 링크 禁用值: " + 名稱);
        return 結果;
    }
    static String 命令輸出(List<String> 命令) throws Exception {
        Process 程序值 = new ProcessBuilder(命令).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 結果 = new String(程序值.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (程序值.waitFor() != 0) throw new IOException("命令 失敗值: " + 命令.get(0)); return 結果;
    }
    static void 提取(Path 存檔值, Path 目的地址值) throws Exception {
        for (String 名稱 : 命令輸出(Arrays.asList("tar","-tzf",存檔值.toString())).split("\n")) 內部路徑(目的地址值, 名稱);
        for (String 行 : 命令輸出(Arrays.asList("tar","-tvzf",存檔值.toString())).split("\n"))
            if (!行.isEmpty() && 行.charAt(0) != '-' && 行.charAt(0) != 'd') throw new IOException("外部值 링크 또는 特殊值 파일을 포함한 依賴項列");
        Files.createDirectories(目的地址值);
        int 狀態值 = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",存檔值.toString(),"-C",目的地址值.toString()).inheritIO().start().waitFor();
        if (狀態值 != 0) throw new IOException("依賴項列 存檔值 釋放存儲裝置 失敗值");
    }
    static void 調用(Path 工作中路徑, Path 工具集, List<String> 實參, Map<String,String> 環境) throws Exception {
        List<String> 命令 = new ArrayList<>(Arrays.asList("python3", 工具集.toString())); 命令.addAll(實參);
        ProcessBuilder 執行命令 = new ProcessBuilder(命令).directory(工作中路徑.toFile()).inheritIO(); 執行命令.environment().putAll(環境);
        int 狀態值 = 執行命令.start().waitFor(); if (狀態值 != 0) throw new IOException("工具集 失敗值: " + 工具集 + " (" + 狀態值 + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 實參) throws Exception {
        if (實參.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String 動作 = 實參[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(動作)) throw new IllegalArgumentException("알 數 없는 動作");
        Path 項目根 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> 設置 = (Map<String,Object>)new 資料解析器(Files.readString(項目根.resolve("native.json"),StandardCharsets.UTF_8)).讀取();
        Path 原始碼樹 = 內部路徑(項目根,(String)設置.get("source")), 內核值 = 內部路徑(原始碼樹,(String)設置.get("native"));
        List<String> 自有檔案集 = (List<String>)(List<?>)設置.get("owned_files");
        for (String 名稱 : 自有檔案集) if (!Files.isRegularFile(內部路徑(原始碼樹,名稱))) throw new IOException("原始碼樹 缺失方法: " + 名稱);
        if (動作.equals("check")) { System.out.println(設置.get("country") + " " + 設置.get("language") + " 독립 原始碼樹 驗證 是否完成"); return; }
        String 資源相對路徑 = (String)設置.getOrDefault("resource_root", ".");
        if (!資源相對路徑.equals(".") && !資源相對路徑.equals("..")) throw new IllegalArgumentException("依賴項列 項目根 路徑 錯誤");
        Path 資源值 = 項目根.resolve(資源相對路徑).normalize(); Path 存檔值 = 資源值.resolve("native-vendor.tar.gz");
        String 預期哈希 = (String)設置.get("vendor_sha256");
        if (!哈希檔案(存檔值).equals(預期哈希)) throw new IOException("依賴項列 SHA-256 불일치");
        Path 標記值 = 原始碼樹.resolve(".vendor-sha256");
        if (!Files.isRegularFile(標記值) || !Files.readString(標記值).trim().equals(預期哈希)) { 提取(存檔值, 原始碼樹); Files.writeString(標記值,預期哈希 + "\n"); }
        Map<String,String> 環境 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (環境.containsKey("IP_CONFIG")) ipConfig = Paths.get(環境.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 項目根; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = 原始碼樹.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        環境.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(動作) && !環境.containsKey("QEMU_AARCH64")) {
            Path 運行器 = 資源值.resolve("host/qemu"), 啓動器標記 = 資源值.resolve("host/.qemu-sha256");
            String 啓動器哈希 = (String)設置.get("qemu_sha256");
            if (!Files.isRegularFile(運行器) || !Files.isRegularFile(啓動器標記) || !Files.readString(啓動器標記).trim().equals(啓動器哈希)) {
                Path 啓動器存檔 = 資源值.resolve("qemu-host.tar.gz"); if (!哈希檔案(啓動器存檔).equals(啓動器哈希)) throw new IOException("QEMU SHA-256 불일치");
                提取(啓動器存檔,資源值.resolve("host")); Files.writeString(啓動器標記,啓動器哈希 + "\n");
            }
            環境.put("QEMU_AARCH64",運行器.toString());
        }
        MessageDigest 計算結果 = MessageDigest.getInstance("SHA-256"); Collections.sort(自有檔案集);
        for (String 名稱 : 自有檔案集) { 計算結果.update(名稱.getBytes(StandardCharsets.UTF_8)); 計算結果.update(Files.readAllBytes(內部路徑(原始碼樹,名稱))); }
        計算結果.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 計算結果.update(Files.readAllBytes(ipConfig));
        String 原始碼哈希 = 哈希文本(計算結果.digest()); Path 構建標記 = 內核值.resolve("build/worldos-source.sha256");
        if (動作.equals("build") || !Files.isRegularFile(構建標記) || !Files.readString(構建標記).trim().equals(原始碼哈希)) {
            調用(內核值,內部路徑(內核值,(String)設置.get("builder")),Collections.emptyList(),環境);
            Files.writeString(構建標記,原始碼哈希 + "\n");
        }
        List<String> 啓動器參數列 = new ArrayList<>(Arrays.asList(實參).subList(1,實參.length));
        if (動作.equals("run") || 動作.equals("desktop")) {
            if (動作.equals("desktop")) 啓動器參數列.add(0,"--desktop");
            調用(內核值,內部路徑(內核值,(String)設置.get("runner")),啓動器參數列,環境);
        } else if (動作.equals("image")) 調用(內核值,內部路徑(內核值,(String)設置.get("image_builder")),啓動器參數列,環境);
        else if (動作.equals("test-system")) {
            啓動器參數列.add(0,項目根.toString()); 啓動器參數列.add(0,"--edition");
            調用(內核值,內部路徑(內核值,(String)設置.get("system_tester")),啓動器參數列,環境);
        }
    }
}
