// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 负责独立国家版依赖检查、恢复、构建和运行的宿主 Java 工具。 */
public final class 国家执行器 {
    static final class 数据解析器 {
        final String 源代码; int 位置;
        数据解析器(String 文本) { 源代码 = 文本; }
        void 跳过空白() { while (位置 < 源代码.length() && Character.isWhitespace(源代码.charAt(位置))) 位置++; }
        Object 读取() {
            跳过空白(); char 字符值 = 源代码.charAt(位置++);
            if (字符值 == '{') {
                Map<String,Object> 结果 = new LinkedHashMap<>(); 跳过空白();
                if (源代码.charAt(位置) == '}') { 位置++; return 结果; }
                while (true) {
                    String 名称 = (String)读取(); 跳过空白(); if (源代码.charAt(位置++) != ':') throw new IllegalArgumentException("数据 分隔符值 错误");
                    结果.put(名称, 读取()); 跳过空白(); char 分隔符值 = 源代码.charAt(位置++);
                    if (分隔符值 == '}') return 结果; if (分隔符值 != ',') throw new IllegalArgumentException("数据 分隔符值 错误");
                }
            }
            if (字符值 == '[') {
                List<Object> 结果 = new ArrayList<>(); 跳过空白();
                if (源代码.charAt(位置) == ']') { 位置++; return 结果; }
                while (true) {
                    结果.add(读取()); 跳过空白(); char 分隔符值 = 源代码.charAt(位置++);
                    if (分隔符值 == ']') return 结果; if (分隔符值 != ',') throw new IllegalArgumentException("数据 分隔符值 错误");
                }
            }
            if (字符值 == '"') {
                StringBuilder 结果 = new StringBuilder();
                while (true) {
                    char 下一项目 = 源代码.charAt(位置++); if (下一项目 == '"') return 结果.toString();
                    if (下一项目 == '\\') {
                        下一项目 = 源代码.charAt(位置++);
                        if (下一项目 == 'u') { 结果.append((char)Integer.parseInt(源代码.substring(位置, 位置 + 4),16)); 位置 += 4; continue; }
                        if (下一项目 == 'n') 下一项目 = '\n'; else if (下一项目 == 'r') 下一项目 = '\r'; else if (下一项目 == 't') 下一项目 = '\t';
                        else if (下一项目 == 'b') 下一项目 = '\b'; else if (下一项目 == 'f') 下一项目 = '\f';
                        else if (下一项目 != '"' && 下一项目 != '\\' && 下一项目 != '/') throw new IllegalArgumentException("字符 이스케이프 错误");
                    }
                    结果.append(下一项目);
                }
            }
            int 运行 = 位置 - 1;
            while (位置 < 源代码.length() && ",]} \t\r\n".indexOf(源代码.charAt(位置)) < 0) 位置++;
            String 值 = 源代码.substring(运行, 位置);
            if (值.equals("true")) return Boolean.TRUE; if (值.equals("false")) return Boolean.FALSE; if (值.equals("null")) return null;
            return Double.valueOf(值);
        }
    }
    static String 哈希文件(Path 路径) throws Exception {
        MessageDigest 计算结果 = MessageDigest.getInstance("SHA-256"); byte[] 数据 = new byte[1024 * 1024];
        try (InputStream 输入值 = Files.newInputStream(路径)) { for (int 长度; (长度 = 输入值.read(数据)) >= 0;) 计算结果.update(数据,0,长度); }
        return 哈希文本(计算结果.digest());
    }
    static String 哈希文本(byte[] 数据) {
        StringBuilder 文本 = new StringBuilder(); for (byte 值 : 数据) 文本.append(String.format(Locale.ROOT,"%02x",值 & 255)); return 文本.toString();
    }
    static Path 内部路径(Path 项目根, String 名称) {
        Path 结果 = 项目根.resolve(名称).normalize();
        if (名称.isEmpty() || Paths.get(名称).isAbsolute() || !结果.startsWith(项目根) || 名称.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 路径: " + 名称);
        for (Path 子部分值 : Paths.get(名称)) if (子部分值.toString().equals("..")) throw new IllegalArgumentException("상위 路径 禁用值: " + 名称);
        for (Path 当前项目 = 结果; 当前项目 != null && 当前项目.startsWith(项目根); 当前项目 = 当前项目.getParent())
            if (Files.isSymbolicLink(当前项目)) throw new IllegalArgumentException("依赖项列 경로의 링크 禁用值: " + 名称);
        return 结果;
    }
    static String 命令输出(List<String> 命令) throws Exception {
        Process 进程值 = new ProcessBuilder(命令).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String 结果 = new String(进程值.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (进程值.waitFor() != 0) throw new IOException("命令 失败值: " + 命令.get(0)); return 结果;
    }
    static void 提取(Path 存档值, Path 目的地址值) throws Exception {
        for (String 名称 : 命令输出(Arrays.asList("tar","-tzf",存档值.toString())).split("\n")) 内部路径(目的地址值, 名称);
        for (String 行 : 命令输出(Arrays.asList("tar","-tvzf",存档值.toString())).split("\n"))
            if (!行.isEmpty() && 行.charAt(0) != '-' && 行.charAt(0) != 'd') throw new IOException("外部值 링크 또는 特殊值 파일을 포함한 依赖项列");
        Files.createDirectories(目的地址值);
        int 状态值 = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",存档值.toString(),"-C",目的地址值.toString()).inheritIO().start().waitFor();
        if (状态值 != 0) throw new IOException("依赖项列 存档值 释放存储装置 失败值");
    }
    static void 调用(Path 工作中路径, Path 工具集, List<String> 实参, Map<String,String> 环境) throws Exception {
        List<String> 命令 = new ArrayList<>(Arrays.asList("python3", 工具集.toString())); 命令.addAll(实参);
        ProcessBuilder 执行命令 = new ProcessBuilder(命令).directory(工作中路径.toFile()).inheritIO(); 执行命令.environment().putAll(环境);
        int 状态值 = 执行命令.start().waitFor(); if (状态值 != 0) throw new IOException("工具集 失败值: " + 工具集 + " (" + 状态值 + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] 实参) throws Exception {
        if (实参.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String 动作 = 实参[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(动作)) throw new IllegalArgumentException("알 数 없는 动作");
        Path 项目根 = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> 设置 = (Map<String,Object>)new 数据解析器(Files.readString(项目根.resolve("native.json"),StandardCharsets.UTF_8)).读取();
        Path 源代码树 = 内部路径(项目根,(String)设置.get("source")), 内核值 = 内部路径(源代码树,(String)设置.get("native"));
        List<String> 自有文件集 = (List<String>)(List<?>)设置.get("owned_files");
        for (String 名称 : 自有文件集) if (!Files.isRegularFile(内部路径(源代码树,名称))) throw new IOException("源代码树 缺失方法: " + 名称);
        if (动作.equals("check")) { System.out.println(设置.get("country") + " " + 设置.get("language") + " 독립 源代码树 验证 是否完成"); return; }
        String 资源相对路径 = (String)设置.getOrDefault("resource_root", ".");
        if (!资源相对路径.equals(".") && !资源相对路径.equals("..")) throw new IllegalArgumentException("依赖项列 项目根 路径 错误");
        Path 资源值 = 项目根.resolve(资源相对路径).normalize(); Path 存档值 = 资源值.resolve("native-vendor.tar.gz");
        String 预期哈希 = (String)设置.get("vendor_sha256");
        if (!哈希文件(存档值).equals(预期哈希)) throw new IOException("依赖项列 SHA-256 불일치");
        Path 标记值 = 源代码树.resolve(".vendor-sha256");
        if (!Files.isRegularFile(标记值) || !Files.readString(标记值).trim().equals(预期哈希)) { 提取(存档值, 源代码树); Files.writeString(标记值,预期哈希 + "\n"); }
        Map<String,String> 环境 = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (环境.containsKey("IP_CONFIG")) ipConfig = Paths.get(环境.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = 项目根; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = 源代码树.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        环境.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(动作) && !环境.containsKey("QEMU_AARCH64")) {
            Path 运行器 = 资源值.resolve("host/qemu"), 启动器标记 = 资源值.resolve("host/.qemu-sha256");
            String 启动器哈希 = (String)设置.get("qemu_sha256");
            if (!Files.isRegularFile(运行器) || !Files.isRegularFile(启动器标记) || !Files.readString(启动器标记).trim().equals(启动器哈希)) {
                Path 启动器存档 = 资源值.resolve("qemu-host.tar.gz"); if (!哈希文件(启动器存档).equals(启动器哈希)) throw new IOException("QEMU SHA-256 불일치");
                提取(启动器存档,资源值.resolve("host")); Files.writeString(启动器标记,启动器哈希 + "\n");
            }
            环境.put("QEMU_AARCH64",运行器.toString());
        }
        MessageDigest 计算结果 = MessageDigest.getInstance("SHA-256"); Collections.sort(自有文件集);
        for (String 名称 : 自有文件集) { 计算结果.update(名称.getBytes(StandardCharsets.UTF_8)); 计算结果.update(Files.readAllBytes(内部路径(源代码树,名称))); }
        计算结果.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 计算结果.update(Files.readAllBytes(ipConfig));
        String 源代码哈希 = 哈希文本(计算结果.digest()); Path 构建标记 = 内核值.resolve("build/worldos-source.sha256");
        if (动作.equals("build") || !Files.isRegularFile(构建标记) || !Files.readString(构建标记).trim().equals(源代码哈希)) {
            调用(内核值,内部路径(内核值,(String)设置.get("builder")),Collections.emptyList(),环境);
            Files.writeString(构建标记,源代码哈希 + "\n");
        }
        List<String> 启动器参数列 = new ArrayList<>(Arrays.asList(实参).subList(1,实参.length));
        if (动作.equals("run") || 动作.equals("desktop")) {
            if (动作.equals("desktop")) 启动器参数列.add(0,"--desktop");
            调用(内核值,内部路径(内核值,(String)设置.get("runner")),启动器参数列,环境);
        } else if (动作.equals("image")) 调用(内核值,内部路径(内核值,(String)设置.get("image_builder")),启动器参数列,环境);
        else if (动作.equals("test-system")) {
            启动器参数列.add(0,项目根.toString()); 启动器参数列.add(0,"--edition");
            调用(内核值,内部路径(内核值,(String)设置.get("system_tester")),启动器参数列,环境);
        }
    }
}
