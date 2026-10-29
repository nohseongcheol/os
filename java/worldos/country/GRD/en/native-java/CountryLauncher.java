// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** Host Java tool for checking and restoring dependencies, building and running an independent country edition. */
public final class CountryLauncher {
    static final class DataParser {
        final String source; int position;
        DataParser(String text) { source = text; }
        void skipWhitespace() { while (position < source.length() && Character.isWhitespace(source.charAt(position))) position++; }
        Object read() {
            skipWhitespace(); char characterValue = source.charAt(position++);
            if (characterValue == '{') {
                Map<String,Object> result = new LinkedHashMap<>(); skipWhitespace();
                if (source.charAt(position) == '}') { position++; return result; }
                while (true) {
                    String name = (String)read(); skipWhitespace(); if (source.charAt(position++) != ':') throw new IllegalArgumentException("data delimiterValue error");
                    result.put(name, read()); skipWhitespace(); char delimiterValue = source.charAt(position++);
                    if (delimiterValue == '}') return result; if (delimiterValue != ',') throw new IllegalArgumentException("data delimiterValue error");
                }
            }
            if (characterValue == '[') {
                List<Object> result = new ArrayList<>(); skipWhitespace();
                if (source.charAt(position) == ']') { position++; return result; }
                while (true) {
                    result.add(read()); skipWhitespace(); char delimiterValue = source.charAt(position++);
                    if (delimiterValue == ']') return result; if (delimiterValue != ',') throw new IllegalArgumentException("data delimiterValue error");
                }
            }
            if (characterValue == '"') {
                StringBuilder result = new StringBuilder();
                while (true) {
                    char nextItem = source.charAt(position++); if (nextItem == '"') return result.toString();
                    if (nextItem == '\\') {
                        nextItem = source.charAt(position++);
                        if (nextItem == 'u') { result.append((char)Integer.parseInt(source.substring(position, position + 4),16)); position += 4; continue; }
                        if (nextItem == 'n') nextItem = '\n'; else if (nextItem == 'r') nextItem = '\r'; else if (nextItem == 't') nextItem = '\t';
                        else if (nextItem == 'b') nextItem = '\b'; else if (nextItem == 'f') nextItem = '\f';
                        else if (nextItem != '"' && nextItem != '\\' && nextItem != '/') throw new IllegalArgumentException("Characters 이스케이프 error");
                    }
                    result.append(nextItem);
                }
            }
            int run = position - 1;
            while (position < source.length() && ",]} \t\r\n".indexOf(source.charAt(position)) < 0) position++;
            String value = source.substring(run, position);
            if (value.equals("true")) return Boolean.TRUE; if (value.equals("false")) return Boolean.FALSE; if (value.equals("null")) return null;
            return Double.valueOf(value);
        }
    }
    static String hashFile(Path path) throws Exception {
        MessageDigest calculation = MessageDigest.getInstance("SHA-256"); byte[] data = new byte[1024 * 1024];
        try (InputStream inputValue = Files.newInputStream(path)) { for (int lengthValue; (lengthValue = inputValue.read(data)) >= 0;) calculation.update(data,0,lengthValue); }
        return hashText(calculation.digest());
    }
    static String hashText(byte[] data) {
        StringBuilder text = new StringBuilder(); for (byte value : data) text.append(String.format(Locale.ROOT,"%02x",value & 255)); return text.toString();
    }
    static Path internalPath(Path projectRoot, String name) {
        Path result = projectRoot.resolve(name).normalize();
        if (name.isEmpty() || Paths.get(name).isAbsolute() || !result.startsWith(projectRoot) || name.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 path: " + name);
        for (Path subpartValue : Paths.get(name)) if (subpartValue.toString().equals("..")) throw new IllegalArgumentException("상위 path prohibitedValue: " + name);
        for (Path currentItem = result; currentItem != null && currentItem.startsWith(projectRoot); currentItem = currentItem.getParent())
            if (Files.isSymbolicLink(currentItem)) throw new IllegalArgumentException("dependencies 경로의 링크 prohibitedValue: " + name);
        return result;
    }
    static String commandOutput(List<String> command) throws Exception {
        Process processValue = new ProcessBuilder(command).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String result = new String(processValue.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (processValue.waitFor() != 0) throw new IOException("command failureValue: " + command.get(0)); return result;
    }
    static void extract(Path archiveValue, Path destinationValue) throws Exception {
        for (String name : commandOutput(Arrays.asList("tar","-tzf",archiveValue.toString())).split("\n")) internalPath(destinationValue, name);
        for (String line : commandOutput(Arrays.asList("tar","-tvzf",archiveValue.toString())).split("\n"))
            if (!line.isEmpty() && line.charAt(0) != '-' && line.charAt(0) != 'd') throw new IOException("externalValue 링크 또는 specialValue 파일을 포함한 dependencies");
        Files.createDirectories(destinationValue);
        int stateValue = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",archiveValue.toString(),"-C",destinationValue.toString()).inheritIO().start().waitFor();
        if (stateValue != 0) throw new IOException("dependencies archiveValue releaseStorage failureValue");
    }
    static void invoke(Path workingPath, Path tools, List<String> arguments, Map<String,String> environment) throws Exception {
        List<String> command = new ArrayList<>(Arrays.asList("python3", tools.toString())); command.addAll(arguments);
        ProcessBuilder executeCommand = new ProcessBuilder(command).directory(workingPath.toFile()).inheritIO(); executeCommand.environment().putAll(environment);
        int stateValue = executeCommand.start().waitFor(); if (stateValue != 0) throw new IOException("tools failureValue: " + tools + " (" + stateValue + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] arguments) throws Exception {
        if (arguments.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String action = arguments[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(action)) throw new IllegalArgumentException("알 number 없는 action");
        Path projectRoot = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> settings = (Map<String,Object>)new DataParser(Files.readString(projectRoot.resolve("native.json"),StandardCharsets.UTF_8)).read();
        Path sourceTree = internalPath(projectRoot,(String)settings.get("source")), kernelValue = internalPath(sourceTree,(String)settings.get("native"));
        List<String> ownedFiles = (List<String>)(List<?>)settings.get("owned_files");
        for (String name : ownedFiles) if (!Files.isRegularFile(internalPath(sourceTree,name))) throw new IOException("sourceTree missingMethod: " + name);
        if (action.equals("check")) { System.out.println(settings.get("country") + " " + settings.get("language") + " 독립 sourceTree verify isComplete"); return; }
        String resourceRelativePath = (String)settings.getOrDefault("resource_root", ".");
        if (!resourceRelativePath.equals(".") && !resourceRelativePath.equals("..")) throw new IllegalArgumentException("dependencies projectRoot path error");
        Path resourceValue = projectRoot.resolve(resourceRelativePath).normalize(); Path archiveValue = resourceValue.resolve("native-vendor.tar.gz");
        String expectedHash = (String)settings.get("vendor_sha256");
        if (!hashFile(archiveValue).equals(expectedHash)) throw new IOException("dependencies SHA-256 불일치");
        Path markerValue = sourceTree.resolve(".vendor-sha256");
        if (!Files.isRegularFile(markerValue) || !Files.readString(markerValue).trim().equals(expectedHash)) { extract(archiveValue, sourceTree); Files.writeString(markerValue,expectedHash + "\n"); }
        Map<String,String> environment = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (environment.containsKey("IP_CONFIG")) ipConfig = Paths.get(environment.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = projectRoot; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = sourceTree.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        environment.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(action) && !environment.containsKey("QEMU_AARCH64")) {
            Path ProgramLauncher = resourceValue.resolve("host/qemu"), launcherMarker = resourceValue.resolve("host/.qemu-sha256");
            String launcherHash = (String)settings.get("qemu_sha256");
            if (!Files.isRegularFile(ProgramLauncher) || !Files.isRegularFile(launcherMarker) || !Files.readString(launcherMarker).trim().equals(launcherHash)) {
                Path launcherArchive = resourceValue.resolve("qemu-host.tar.gz"); if (!hashFile(launcherArchive).equals(launcherHash)) throw new IOException("QEMU SHA-256 불일치");
                extract(launcherArchive,resourceValue.resolve("host")); Files.writeString(launcherMarker,launcherHash + "\n");
            }
            environment.put("QEMU_AARCH64",ProgramLauncher.toString());
        }
        MessageDigest calculation = MessageDigest.getInstance("SHA-256"); Collections.sort(ownedFiles);
        for (String name : ownedFiles) { calculation.update(name.getBytes(StandardCharsets.UTF_8)); calculation.update(Files.readAllBytes(internalPath(sourceTree,name))); }
        calculation.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); calculation.update(Files.readAllBytes(ipConfig));
        String sourceHash = hashText(calculation.digest()); Path buildMarker = kernelValue.resolve("build/worldos-source.sha256");
        if (action.equals("build") || !Files.isRegularFile(buildMarker) || !Files.readString(buildMarker).trim().equals(sourceHash)) {
            invoke(kernelValue,internalPath(kernelValue,(String)settings.get("builder")),Collections.emptyList(),environment);
            Files.writeString(buildMarker,sourceHash + "\n");
        }
        List<String> launcherArguments = new ArrayList<>(Arrays.asList(arguments).subList(1,arguments.length));
        if (action.equals("run") || action.equals("desktop")) {
            if (action.equals("desktop")) launcherArguments.add(0,"--desktop");
            invoke(kernelValue,internalPath(kernelValue,(String)settings.get("runner")),launcherArguments,environment);
        } else if (action.equals("image")) invoke(kernelValue,internalPath(kernelValue,(String)settings.get("image_builder")),launcherArguments,environment);
        else if (action.equals("test-system")) {
            launcherArguments.add(0,projectRoot.toString()); launcherArguments.add(0,"--edition");
            invoke(kernelValue,internalPath(kernelValue,(String)settings.get("system_tester")),launcherArguments,environment);
        }
    }
}
