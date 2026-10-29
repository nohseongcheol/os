// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** स्वतंत्र देशीय आवृत्तीच्या अवलंबित्वांची तपासणी व पुनर्स्थापना, बांधणी आणि कार्यान्वयन करणारे यजमान Java साधन. */
public final class देश_चालक {
    static final class डेटा_व्याकरणविश्लेषक {
        final String स्रोत; int जागा;
        डेटा_व्याकरणविश्लेषक(String पाठ्य) { स्रोत = पाठ्य; }
        void वगळा_रिक्तवर्ण() { while (जागा < स्रोत.length() && Character.isWhitespace(स्रोत.charAt(जागा))) जागा++; }
        Object वाचन() {
            वगळा_रिक्तवर्ण(); char वर्ण_मूल्य = स्रोत.charAt(जागा++);
            if (वर्ण_मूल्य == '{') {
                Map<String,Object> मोजमाप = new LinkedHashMap<>(); वगळा_रिक्तवर्ण();
                if (स्रोत.charAt(जागा) == '}') { जागा++; return मोजमाप; }
                while (true) {
                    String नाव = (String)वाचन(); वगळा_रिक्तवर्ण(); if (स्रोत.charAt(जागा++) != ':') throw new IllegalArgumentException("डेटा डीलिमीटर_मूल्य त्रुटी");
                    मोजमाप.put(नाव, वाचन()); वगळा_रिक्तवर्ण(); char डीलिमीटर_मूल्य = स्रोत.charAt(जागा++);
                    if (डीलिमीटर_मूल्य == '}') return मोजमाप; if (डीलिमीटर_मूल्य != ',') throw new IllegalArgumentException("डेटा डीलिमीटर_मूल्य त्रुटी");
                }
            }
            if (वर्ण_मूल्य == '[') {
                List<Object> मोजमाप = new ArrayList<>(); वगळा_रिक्तवर्ण();
                if (स्रोत.charAt(जागा) == ']') { जागा++; return मोजमाप; }
                while (true) {
                    मोजमाप.add(वाचन()); वगळा_रिक्तवर्ण(); char डीलिमीटर_मूल्य = स्रोत.charAt(जागा++);
                    if (डीलिमीटर_मूल्य == ']') return मोजमाप; if (डीलिमीटर_मूल्य != ',') throw new IllegalArgumentException("डेटा डीलिमीटर_मूल्य त्रुटी");
                }
            }
            if (वर्ण_मूल्य == '"') {
                StringBuilder मोजमाप = new StringBuilder();
                while (true) {
                    char पुढील_आयटम = स्रोत.charAt(जागा++); if (पुढील_आयटम == '"') return मोजमाप.toString();
                    if (पुढील_आयटम == '\\') {
                        पुढील_आयटम = स्रोत.charAt(जागा++);
                        if (पुढील_आयटम == 'u') { मोजमाप.append((char)Integer.parseInt(स्रोत.substring(जागा, जागा + 4),16)); जागा += 4; continue; }
                        if (पुढील_आयटम == 'n') पुढील_आयटम = '\n'; else if (पुढील_आयटम == 'r') पुढील_आयटम = '\r'; else if (पुढील_आयटम == 't') पुढील_आयटम = '\t';
                        else if (पुढील_आयटम == 'b') पुढील_आयटम = '\b'; else if (पुढील_आयटम == 'f') पुढील_आयटम = '\f';
                        else if (पुढील_आयटम != '"' && पुढील_आयटम != '\\' && पुढील_आयटम != '/') throw new IllegalArgumentException("वर्ण 이스케이프 त्रुटी");
                    }
                    मोजमाप.append(पुढील_आयटम);
                }
            }
            int सुरू_करा = जागा - 1;
            while (जागा < स्रोत.length() && ",]} \t\r\n".indexOf(स्रोत.charAt(जागा)) < 0) जागा++;
            String मूल्य = स्रोत.substring(सुरू_करा, जागा);
            if (मूल्य.equals("true")) return Boolean.TRUE; if (मूल्य.equals("false")) return Boolean.FALSE; if (मूल्य.equals("null")) return null;
            return Double.valueOf(मूल्य);
        }
    }
    static String हॅश_संचिका(Path मार्ग) throws Exception {
        MessageDigest गणना = MessageDigest.getInstance("SHA-256"); byte[] डेटा = new byte[1024 * 1024];
        try (InputStream आदान_मूल्य = Files.newInputStream(मार्ग)) { for (int लांबी_मूल्य; (लांबी_मूल्य = आदान_मूल्य.read(डेटा)) >= 0;) गणना.update(डेटा,0,लांबी_मूल्य); }
        return हॅश_मजकूर(गणना.digest());
    }
    static String हॅश_मजकूर(byte[] डेटा) {
        StringBuilder पाठ्य = new StringBuilder(); for (byte मूल्य : डेटा) पाठ्य.append(String.format(Locale.ROOT,"%02x",मूल्य & 255)); return पाठ्य.toString();
    }
    static Path अंतर्गत_पथ(Path प्रोजेक्ट_मूळ, String नाव) {
        Path मोजमाप = प्रोजेक्ट_मूळ.resolve(नाव).normalize();
        if (नाव.isEmpty() || Paths.get(नाव).isAbsolute() || !मोजमाप.startsWith(प्रोजेक्ट_मूळ) || नाव.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 मार्ग: " + नाव);
        for (Path उपभाग_मूल्य : Paths.get(नाव)) if (उपभाग_मूल्य.toString().equals("..")) throw new IllegalArgumentException("상위 मार्ग निषिद्ध_मूल्य: " + नाव);
        for (Path सध्याचे_आयटम = मोजमाप; सध्याचे_आयटम != null && सध्याचे_आयटम.startsWith(प्रोजेक्ट_मूळ); सध्याचे_आयटम = सध्याचे_आयटम.getParent())
            if (Files.isSymbolicLink(सध्याचे_आयटम)) throw new IllegalArgumentException("अवलंबने 경로의 링크 निषिद्ध_मूल्य: " + नाव);
        return मोजमाप;
    }
    static String आज्ञा_प्रदान(List<String> आदेश) throws Exception {
        Process प्रक्रिया_मूल्य = new ProcessBuilder(आदेश).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String मोजमाप = new String(प्रक्रिया_मूल्य.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (प्रक्रिया_मूल्य.waitFor() != 0) throw new IOException("आदेश बिघाड_मूल्य: " + आदेश.get(0)); return मोजमाप;
    }
    static void बाहेर_काढा(Path संग्रह_मूल्य, Path गंतव्यस्थान_मूल्य) throws Exception {
        for (String नाव : आज्ञा_प्रदान(Arrays.asList("tar","-tzf",संग्रह_मूल्य.toString())).split("\n")) अंतर्गत_पथ(गंतव्यस्थान_मूल्य, नाव);
        for (String ओळ : आज्ञा_प्रदान(Arrays.asList("tar","-tvzf",संग्रह_मूल्य.toString())).split("\n"))
            if (!ओळ.isEmpty() && ओळ.charAt(0) != '-' && ओळ.charAt(0) != 'd') throw new IOException("बाह्य_मूल्य 링크 또는 विशेष_मूल्य 파일을 포함한 अवलंबने");
        Files.createDirectories(गंतव्यस्थान_मूल्य);
        int राज्य_मूल्य = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",संग्रह_मूल्य.toString(),"-C",गंतव्यस्थान_मूल्य.toString()).inheritIO().start().waitFor();
        if (राज्य_मूल्य != 0) throw new IOException("अवलंबने संग्रह_मूल्य संग्रह_रिलीज बिघाड_मूल्य");
    }
    static void आवाहन(Path कार्यरत_पथ, Path साधने, List<String> बाबी, Map<String,String> पर्यावरण) throws Exception {
        List<String> आदेश = new ArrayList<>(Arrays.asList("python3", साधने.toString())); आदेश.addAll(बाबी);
        ProcessBuilder आज्ञा_कार्यवाही_करा = new ProcessBuilder(आदेश).directory(कार्यरत_पथ.toFile()).inheritIO(); आज्ञा_कार्यवाही_करा.environment().putAll(पर्यावरण);
        int राज्य_मूल्य = आज्ञा_कार्यवाही_करा.start().waitFor(); if (राज्य_मूल्य != 0) throw new IOException("साधने बिघाड_मूल्य: " + साधने + " (" + राज्य_मूल्य + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] बाबी) throws Exception {
        if (बाबी.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String कृती = बाबी[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(कृती)) throw new IllegalArgumentException("알 संख्या 없는 कृती");
        Path प्रोजेक्ट_मूळ = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> संयोजना = (Map<String,Object>)new डेटा_व्याकरणविश्लेषक(Files.readString(प्रोजेक्ट_मूळ.resolve("native.json"),StandardCharsets.UTF_8)).वाचन();
        Path स्रोत_ट्री = अंतर्गत_पथ(प्रोजेक्ट_मूळ,(String)संयोजना.get("source")), गाभा_मूल्य = अंतर्गत_पथ(स्रोत_ट्री,(String)संयोजना.get("native"));
        List<String> स्वमालकीचे_संचिका = (List<String>)(List<?>)संयोजना.get("owned_files");
        for (String नाव : स्वमालकीचे_संचिका) if (!Files.isRegularFile(अंतर्गत_पथ(स्रोत_ट्री,नाव))) throw new IOException("स्रोत_ट्री अनुपस्थित_पद्धत: " + नाव);
        if (कृती.equals("check")) { System.out.println(संयोजना.get("country") + " " + संयोजना.get("language") + " 독립 स्रोत_ट्री पडताळा आहे_पूर्ण"); return; }
        String संसाधन_सापेक्ष_पथ = (String)संयोजना.getOrDefault("resource_root", ".");
        if (!संसाधन_सापेक्ष_पथ.equals(".") && !संसाधन_सापेक्ष_पथ.equals("..")) throw new IllegalArgumentException("अवलंबने प्रोजेक्ट_मूळ मार्ग त्रुटी");
        Path संसाधन_मूल्य = प्रोजेक्ट_मूळ.resolve(संसाधन_सापेक्ष_पथ).normalize(); Path संग्रह_मूल्य = संसाधन_मूल्य.resolve("native-vendor.tar.gz");
        String अपेक्षित_हॅश = (String)संयोजना.get("vendor_sha256");
        if (!हॅश_संचिका(संग्रह_मूल्य).equals(अपेक्षित_हॅश)) throw new IOException("अवलंबने SHA-256 불일치");
        Path खूण_मूल्य = स्रोत_ट्री.resolve(".vendor-sha256");
        if (!Files.isRegularFile(खूण_मूल्य) || !Files.readString(खूण_मूल्य).trim().equals(अपेक्षित_हॅश)) { बाहेर_काढा(संग्रह_मूल्य, स्रोत_ट्री); Files.writeString(खूण_मूल्य,अपेक्षित_हॅश + "\n"); }
        Map<String,String> पर्यावरण = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (पर्यावरण.containsKey("IP_CONFIG")) ipConfig = Paths.get(पर्यावरण.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = प्रोजेक्ट_मूळ; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = स्रोत_ट्री.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        पर्यावरण.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(कृती) && !पर्यावरण.containsKey("QEMU_AARCH64")) {
            Path अनुप्रयोग_चालक = संसाधन_मूल्य.resolve("host/qemu"), चालक_खूण = संसाधन_मूल्य.resolve("host/.qemu-sha256");
            String चालक_हॅश = (String)संयोजना.get("qemu_sha256");
            if (!Files.isRegularFile(अनुप्रयोग_चालक) || !Files.isRegularFile(चालक_खूण) || !Files.readString(चालक_खूण).trim().equals(चालक_हॅश)) {
                Path चालक_संग्रह = संसाधन_मूल्य.resolve("qemu-host.tar.gz"); if (!हॅश_संचिका(चालक_संग्रह).equals(चालक_हॅश)) throw new IOException("QEMU SHA-256 불일치");
                बाहेर_काढा(चालक_संग्रह,संसाधन_मूल्य.resolve("host")); Files.writeString(चालक_खूण,चालक_हॅश + "\n");
            }
            पर्यावरण.put("QEMU_AARCH64",अनुप्रयोग_चालक.toString());
        }
        MessageDigest गणना = MessageDigest.getInstance("SHA-256"); Collections.sort(स्वमालकीचे_संचिका);
        for (String नाव : स्वमालकीचे_संचिका) { गणना.update(नाव.getBytes(StandardCharsets.UTF_8)); गणना.update(Files.readAllBytes(अंतर्गत_पथ(स्रोत_ट्री,नाव))); }
        गणना.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); गणना.update(Files.readAllBytes(ipConfig));
        String स्रोत_हॅश = हॅश_मजकूर(गणना.digest()); Path खूण_बांधणी = गाभा_मूल्य.resolve("build/worldos-source.sha256");
        if (कृती.equals("build") || !Files.isRegularFile(खूण_बांधणी) || !Files.readString(खूण_बांधणी).trim().equals(स्रोत_हॅश)) {
            आवाहन(गाभा_मूल्य,अंतर्गत_पथ(गाभा_मूल्य,(String)संयोजना.get("builder")),Collections.emptyList(),पर्यावरण);
            Files.writeString(खूण_बांधणी,स्रोत_हॅश + "\n");
        }
        List<String> चालक_वितर्क = new ArrayList<>(Arrays.asList(बाबी).subList(1,बाबी.length));
        if (कृती.equals("run") || कृती.equals("desktop")) {
            if (कृती.equals("desktop")) चालक_वितर्क.add(0,"--desktop");
            आवाहन(गाभा_मूल्य,अंतर्गत_पथ(गाभा_मूल्य,(String)संयोजना.get("runner")),चालक_वितर्क,पर्यावरण);
        } else if (कृती.equals("image")) आवाहन(गाभा_मूल्य,अंतर्गत_पथ(गाभा_मूल्य,(String)संयोजना.get("image_builder")),चालक_वितर्क,पर्यावरण);
        else if (कृती.equals("test-system")) {
            चालक_वितर्क.add(0,प्रोजेक्ट_मूळ.toString()); चालक_वितर्क.add(0,"--edition");
            आवाहन(गाभा_मूल्य,अंतर्गत_पथ(गाभा_मूल्य,(String)संयोजना.get("system_tester")),चालक_वितर्क,पर्यावरण);
        }
    }
}
