// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·δομή_Σύστημα·실행을 맡는 φιλοξενώ Java Εργαλεία. */
public final class Κάντρυ_εκκίνηση {
    static final class δεδομένα_ανάλυση {
        final String ΠΗΓΗ; int Θέση;
        δεδομένα_ανάλυση(String Κείμενο) { ΠΗΓΗ = Κείμενο; }
        void 빈칸() { while (Θέση < ΠΗΓΗ.length() && Character.isWhitespace(ΠΗΓΗ.charAt(Θέση))) Θέση++; }
        Object Ανάγνωση() {
            빈칸(); char χαρακτήρας_τιμή = ΠΗΓΗ.charAt(Θέση++);
            if (χαρακτήρας_τιμή == '{') {
                Map<String,Object> μέτρηση = new LinkedHashMap<>(); 빈칸();
                if (ΠΗΓΗ.charAt(Θέση) == '}') { Θέση++; return μέτρηση; }
                while (true) {
                    String Όνομα = (String)Ανάγνωση(); 빈칸(); if (ΠΗΓΗ.charAt(Θέση++) != ':') throw new IllegalArgumentException("δεδομένα οριοθέτης_τιμή ΣΦΑΛΜΑ");
                    μέτρηση.put(Όνομα, Ανάγνωση()); 빈칸(); char οριοθέτης_τιμή = ΠΗΓΗ.charAt(Θέση++);
                    if (οριοθέτης_τιμή == '}') return μέτρηση; if (οριοθέτης_τιμή != ',') throw new IllegalArgumentException("δεδομένα οριοθέτης_τιμή ΣΦΑΛΜΑ");
                }
            }
            if (χαρακτήρας_τιμή == '[') {
                List<Object> μέτρηση = new ArrayList<>(); 빈칸();
                if (ΠΗΓΗ.charAt(Θέση) == ']') { Θέση++; return μέτρηση; }
                while (true) {
                    μέτρηση.add(Ανάγνωση()); 빈칸(); char οριοθέτης_τιμή = ΠΗΓΗ.charAt(Θέση++);
                    if (οριοθέτης_τιμή == ']') return μέτρηση; if (οριοθέτης_τιμή != ',') throw new IllegalArgumentException("δεδομένα οριοθέτης_τιμή ΣΦΑΛΜΑ");
                }
            }
            if (χαρακτήρας_τιμή == '"') {
                StringBuilder μέτρηση = new StringBuilder();
                while (true) {
                    char Επόμενο_στοιχείο = ΠΗΓΗ.charAt(Θέση++); if (Επόμενο_στοιχείο == '"') return μέτρηση.toString();
                    if (Επόμενο_στοιχείο == '\\') {
                        Επόμενο_στοιχείο = ΠΗΓΗ.charAt(Θέση++);
                        if (Επόμενο_στοιχείο == 'u') { μέτρηση.append((char)Integer.parseInt(ΠΗΓΗ.substring(Θέση, Θέση + 4),16)); Θέση += 4; continue; }
                        if (Επόμενο_στοιχείο == 'n') Επόμενο_στοιχείο = '\n'; else if (Επόμενο_στοιχείο == 'r') Επόμενο_στοιχείο = '\r'; else if (Επόμενο_στοιχείο == 't') Επόμενο_στοιχείο = '\t';
                        else if (Επόμενο_στοιχείο == 'b') Επόμενο_στοιχείο = '\b'; else if (Επόμενο_στοιχείο == 'f') Επόμενο_στοιχείο = '\f';
                        else if (Επόμενο_στοιχείο != '"' && Επόμενο_στοιχείο != '\\' && Επόμενο_στοιχείο != '/') throw new IllegalArgumentException("문자 이스케이프 ΣΦΑΛΜΑ");
                    }
                    μέτρηση.append(Επόμενο_στοιχείο);
                }
            }
            int Εκτέλεση_2 = Θέση - 1;
            while (Θέση < ΠΗΓΗ.length() && ",]} \t\r\n".indexOf(ΠΗΓΗ.charAt(Θέση)) < 0) Θέση++;
            String τιμή = ΠΗΓΗ.substring(Εκτέλεση_2, Θέση);
            if (τιμή.equals("true")) return Boolean.TRUE; if (τιμή.equals("false")) return Boolean.FALSE; if (τιμή.equals("null")) return null;
            return Double.valueOf(τιμή);
        }
    }
    static String κατακερματισμός_Αρχείο(Path ΔΙΑΔΡΟΜΗ) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] δεδομένα = new byte[1024 * 1024];
        try (InputStream είσοδος_τιμή = Files.newInputStream(ΔΙΑΔΡΟΜΗ)) { for (int διάρκεια_τιμή; (διάρκεια_τιμή = είσοδος_τιμή.read(δεδομένα)) >= 0;) 계산.update(δεδομένα,0,διάρκεια_τιμή); }
        return κατακερματισμός_μήνυμα(계산.digest());
    }
    static String κατακερματισμός_μήνυμα(byte[] δεδομένα) {
        StringBuilder Κείμενο = new StringBuilder(); for (byte τιμή : δεδομένα) Κείμενο.append(String.format(Locale.ROOT,"%02x",τιμή & 255)); return Κείμενο.toString();
    }
    static Path εσωτερικός_διαδρομή(Path έργο_ρίζα, String Όνομα) {
        Path μέτρηση = έργο_ρίζα.resolve(Όνομα).normalize();
        if (Όνομα.isEmpty() || Paths.get(Όνομα).isAbsolute() || !μέτρηση.startsWith(έργο_ρίζα) || Όνομα.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 ΔΙΑΔΡΟΜΗ: " + Όνομα);
        for (Path 부분 : Paths.get(Όνομα)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 ΔΙΑΔΡΟΜΗ 금지: " + Όνομα);
        for (Path τρέχων_στοιχείο = μέτρηση; τρέχων_στοιχείο != null && τρέχων_στοιχείο.startsWith(έργο_ρίζα); τρέχων_στοιχείο = τρέχων_στοιχείο.getParent())
            if (Files.isSymbolicLink(τρέχων_στοιχείο)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Όνομα);
        return μέτρηση;
    }
    static String 명령출력(List<String> Εντολή) throws Exception {
        Process διεργασία_τιμή = new ProcessBuilder(Εντολή).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String μέτρηση = new String(διεργασία_τιμή.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (διεργασία_τιμή.waitFor() != 0) throw new IOException("Εντολή αποτυχία_τιμή: " + Εντολή.get(0)); return μέτρηση;
    }
    static void εξάγω(Path Αρχειοθήκη_τιμή, Path προορισμός_τιμή) throws Exception {
        for (String Όνομα : 명령출력(Arrays.asList("tar","-tzf",Αρχειοθήκη_τιμή.toString())).split("\n")) εσωτερικός_διαδρομή(προορισμός_τιμή, Όνομα);
        for (String Γραμμή : 명령출력(Arrays.asList("tar","-tvzf",Αρχειοθήκη_τιμή.toString())).split("\n"))
            if (!Γραμμή.isEmpty() && Γραμμή.charAt(0) != '-' && Γραμμή.charAt(0) != 'd') throw new IOException("εξωτερικός_τιμή 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(προορισμός_τιμή);
        int Κατάσταση_τιμή = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Αρχειοθήκη_τιμή.toString(),"-C",προορισμός_τιμή.toString()).inheritIO().start().waitFor();
        if (Κατάσταση_τιμή != 0) throw new IOException("의존성 Αρχειοθήκη_τιμή έκδοση_Χώρος_αποθήκευσης αποτυχία_τιμή");
    }
    static void 호출(Path 작업경로, Path Εργαλεία, List<String> Παράμετροι, Map<String,String> περιβάλλον_5d36e09c) throws Exception {
        List<String> Εντολή = new ArrayList<>(Arrays.asList("python3", Εργαλεία.toString())); Εντολή.addAll(Παράμετροι);
        ProcessBuilder εκτελώ_εντολή = new ProcessBuilder(Εντολή).directory(작업경로.toFile()).inheritIO(); εκτελώ_εντολή.environment().putAll(περιβάλλον_5d36e09c);
        int Κατάσταση_τιμή = εκτελώ_εντολή.start().waitFor(); if (Κατάσταση_τιμή != 0) throw new IOException("Εργαλεία αποτυχία_τιμή: " + Εργαλεία + " (" + Κατάσταση_τιμή + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] Παράμετροι) throws Exception {
        if (Παράμετροι.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Ενέργεια = Παράμετροι[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Ενέργεια)) throw new IllegalArgumentException("알 수 없는 Ενέργεια");
        Path έργο_ρίζα = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Ρυθμίσεις = (Map<String,Object>)new δεδομένα_ανάλυση(Files.readString(έργο_ρίζα.resolve("native.json"),StandardCharsets.UTF_8)).Ανάγνωση();
        Path προέλευση_δέντρο = εσωτερικός_διαδρομή(έργο_ρίζα,(String)Ρυθμίσεις.get("source")), πυρήνας_τιμή = εσωτερικός_διαδρομή(προέλευση_δέντρο,(String)Ρυθμίσεις.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Ρυθμίσεις.get("owned_files");
        for (String Όνομα : 소유파일들) if (!Files.isRegularFile(εσωτερικός_διαδρομή(προέλευση_δέντρο,Όνομα))) throw new IOException("προέλευση_δέντρο 없음: " + Όνομα);
        if (Ενέργεια.equals("check")) { System.out.println(Ρυθμίσεις.get("country") + " " + Ρυθμίσεις.get("language") + " 독립 προέλευση_δέντρο επαληθεύω 완료"); return; }
        String πόρος_σχετική_διαδρομή = (String)Ρυθμίσεις.getOrDefault("resource_root", ".");
        if (!πόρος_σχετική_διαδρομή.equals(".") && !πόρος_σχετική_διαδρομή.equals("..")) throw new IllegalArgumentException("의존성 έργο_ρίζα ΔΙΑΔΡΟΜΗ ΣΦΑΛΜΑ");
        Path πόρος_τιμή = έργο_ρίζα.resolve(πόρος_σχετική_διαδρομή).normalize(); Path Αρχειοθήκη_τιμή = πόρος_τιμή.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Ρυθμίσεις.get("vendor_sha256");
        if (!κατακερματισμός_Αρχείο(Αρχειοθήκη_τιμή).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path δείκτης_τιμή_7e8f90bd = προέλευση_δέντρο.resolve(".vendor-sha256");
        if (!Files.isRegularFile(δείκτης_τιμή_7e8f90bd) || !Files.readString(δείκτης_τιμή_7e8f90bd).trim().equals(기대해시)) { εξάγω(Αρχειοθήκη_τιμή, προέλευση_δέντρο); Files.writeString(δείκτης_τιμή_7e8f90bd,기대해시 + "\n"); }
        Map<String,String> περιβάλλον_5d36e09c = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (περιβάλλον_5d36e09c.containsKey("IP_CONFIG")) ipConfig = Paths.get(περιβάλλον_5d36e09c.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = έργο_ρίζα; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = προέλευση_δέντρο.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        περιβάλλον_5d36e09c.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Ενέργεια) && !περιβάλλον_5d36e09c.containsKey("QEMU_AARCH64")) {
            Path εφαρμογή_εκκίνηση = πόρος_τιμή.resolve("host/qemu"), εκκίνηση_δείκτης = πόρος_τιμή.resolve("host/.qemu-sha256");
            String εκκίνηση_κατακερματισμός = (String)Ρυθμίσεις.get("qemu_sha256");
            if (!Files.isRegularFile(εφαρμογή_εκκίνηση) || !Files.isRegularFile(εκκίνηση_δείκτης) || !Files.readString(εκκίνηση_δείκτης).trim().equals(εκκίνηση_κατακερματισμός)) {
                Path εκκίνηση_Αρχειοθήκη = πόρος_τιμή.resolve("qemu-host.tar.gz"); if (!κατακερματισμός_Αρχείο(εκκίνηση_Αρχειοθήκη).equals(εκκίνηση_κατακερματισμός)) throw new IOException("QEMU SHA-256 불일치");
                εξάγω(εκκίνηση_Αρχειοθήκη,πόρος_τιμή.resolve("host")); Files.writeString(εκκίνηση_δείκτης,εκκίνηση_κατακερματισμός + "\n");
            }
            περιβάλλον_5d36e09c.put("QEMU_AARCH64",εφαρμογή_εκκίνηση.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Όνομα : 소유파일들) { 계산.update(Όνομα.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(εσωτερικός_διαδρομή(προέλευση_δέντρο,Όνομα))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String προέλευση_κατακερματισμός = κατακερματισμός_μήνυμα(계산.digest()); Path δομή_δείκτης = πυρήνας_τιμή.resolve("build/worldos-source.sha256");
        if (Ενέργεια.equals("build") || !Files.isRegularFile(δομή_δείκτης) || !Files.readString(δομή_δείκτης).trim().equals(προέλευση_κατακερματισμός)) {
            호출(πυρήνας_τιμή,εσωτερικός_διαδρομή(πυρήνας_τιμή,(String)Ρυθμίσεις.get("builder")),Collections.emptyList(),περιβάλλον_5d36e09c);
            Files.writeString(δομή_δείκτης,προέλευση_κατακερματισμός + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(Παράμετροι).subList(1,Παράμετροι.length));
        if (Ενέργεια.equals("run") || Ενέργεια.equals("desktop")) {
            if (Ενέργεια.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(πυρήνας_τιμή,εσωτερικός_διαδρομή(πυρήνας_τιμή,(String)Ρυθμίσεις.get("runner")),추가인수,περιβάλλον_5d36e09c);
        } else if (Ενέργεια.equals("image")) 호출(πυρήνας_τιμή,εσωτερικός_διαδρομή(πυρήνας_τιμή,(String)Ρυθμίσεις.get("image_builder")),추가인수,περιβάλλον_5d36e09c);
        else if (Ενέργεια.equals("test-system")) {
            추가인수.add(0,έργο_ρίζα.toString()); 추가인수.add(0,"--edition");
            호출(πυρήνας_τιμή,εσωτερικός_διαδρομή(πυρήνας_τιμή,(String)Ρυθμίσεις.get("system_tester")),추가인수,περιβάλλον_5d36e09c);
        }
    }
}
