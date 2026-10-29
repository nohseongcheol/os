// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/** 독립 국가판의 의존성 검사·복원·збирання·실행을 맡는 хост Java інструменти. */
public final class Кантрі_запускач {
    static final class дані_аналізатор {
        final String вихіднийКод; int позиція;
        дані_аналізатор(String текст) { вихіднийКод = текст; }
        void 빈칸() { while (позиція < вихіднийКод.length() && Character.isWhitespace(вихіднийКод.charAt(позиція))) позиція++; }
        Object Читання() {
            빈칸(); char символ_значення_068c2631 = вихіднийКод.charAt(позиція++);
            if (символ_значення_068c2631 == '{') {
                Map<String,Object> результат = new LinkedHashMap<>(); 빈칸();
                if (вихіднийКод.charAt(позиція) == '}') { позиція++; return результат; }
                while (true) {
                    String Назва = (String)Читання(); 빈칸(); if (вихіднийКод.charAt(позиція++) != ':') throw new IllegalArgumentException("дані роздільник_значення ПОМИЛКА");
                    результат.put(Назва, Читання()); 빈칸(); char роздільник_значення = вихіднийКод.charAt(позиція++);
                    if (роздільник_значення == '}') return результат; if (роздільник_значення != ',') throw new IllegalArgumentException("дані роздільник_значення ПОМИЛКА");
                }
            }
            if (символ_значення_068c2631 == '[') {
                List<Object> результат = new ArrayList<>(); 빈칸();
                if (вихіднийКод.charAt(позиція) == ']') { позиція++; return результат; }
                while (true) {
                    результат.add(Читання()); 빈칸(); char роздільник_значення = вихіднийКод.charAt(позиція++);
                    if (роздільник_значення == ']') return результат; if (роздільник_значення != ',') throw new IllegalArgumentException("дані роздільник_значення ПОМИЛКА");
                }
            }
            if (символ_значення_068c2631 == '"') {
                StringBuilder результат = new StringBuilder();
                while (true) {
                    char Далі_елемент = вихіднийКод.charAt(позиція++); if (Далі_елемент == '"') return результат.toString();
                    if (Далі_елемент == '\\') {
                        Далі_елемент = вихіднийКод.charAt(позиція++);
                        if (Далі_елемент == 'u') { результат.append((char)Integer.parseInt(вихіднийКод.substring(позиція, позиція + 4),16)); позиція += 4; continue; }
                        if (Далі_елемент == 'n') Далі_елемент = '\n'; else if (Далі_елемент == 'r') Далі_елемент = '\r'; else if (Далі_елемент == 't') Далі_елемент = '\t';
                        else if (Далі_елемент == 'b') Далі_елемент = '\b'; else if (Далі_елемент == 'f') Далі_елемент = '\f';
                        else if (Далі_елемент != '"' && Далі_елемент != '\\' && Далі_елемент != '/') throw new IllegalArgumentException("문자 이스케이프 ПОМИЛКА");
                    }
                    результат.append(Далі_елемент);
                }
            }
            int запустити = позиція - 1;
            while (позиція < вихіднийКод.length() && ",]} \t\r\n".indexOf(вихіднийКод.charAt(позиція)) < 0) позиція++;
            String значення = вихіднийКод.substring(запустити, позиція);
            if (значення.equals("true")) return Boolean.TRUE; if (значення.equals("false")) return Boolean.FALSE; if (значення.equals("null")) return null;
            return Double.valueOf(значення);
        }
    }
    static String геш_код_Файл(Path шлях) throws Exception {
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); byte[] дані = new byte[1024 * 1024];
        try (InputStream 입력 = Files.newInputStream(шлях)) { for (int 길이; (길이 = 입력.read(дані)) >= 0;) 계산.update(дані,0,길이); }
        return геш_код_Текст(계산.digest());
    }
    static String геш_код_Текст(byte[] дані) {
        StringBuilder текст = new StringBuilder(); for (byte значення : дані) текст.append(String.format(Locale.ROOT,"%02x",значення & 255)); return текст.toString();
    }
    static Path внутрішній_шлях(Path Дії_корінь, String Назва) {
        Path результат = Дії_корінь.resolve(Назва).normalize();
        if (Назва.isEmpty() || Paths.get(Назва).isAbsolute() || !результат.startsWith(Дії_корінь) || Назва.indexOf('\\') >= 0)
            throw new IllegalArgumentException("범위를 벗어난 шлях: " + Назва);
        for (Path 부분 : Paths.get(Назва)) if (부분.toString().equals("..")) throw new IllegalArgumentException("상위 шлях 금지: " + Назва);
        for (Path чинний_елемент = результат; чинний_елемент != null && чинний_елемент.startsWith(Дії_корінь); чинний_елемент = чинний_елемент.getParent())
            if (Files.isSymbolicLink(чинний_елемент)) throw new IllegalArgumentException("의존성 경로의 링크 금지: " + Назва);
        return результат;
    }
    static String 명령출력(List<String> команда) throws Exception {
        Process процес_значення = new ProcessBuilder(команда).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        String результат = new String(процес_значення.getInputStream().readAllBytes(),StandardCharsets.UTF_8);
        if (процес_значення.waitFor() != 0) throw new IOException("команда неполадка_значення: " + команда.get(0)); return результат;
    }
    static void видобувати(Path Архів_значення, Path місце_значення) throws Exception {
        for (String Назва : 명령출력(Arrays.asList("tar","-tzf",Архів_значення.toString())).split("\n")) внутрішній_шлях(місце_значення, Назва);
        for (String рядок_введення : 명령출력(Arrays.asList("tar","-tvzf",Архів_значення.toString())).split("\n"))
            if (!рядок_введення.isEmpty() && рядок_введення.charAt(0) != '-' && рядок_введення.charAt(0) != 'd') throw new IOException("зовнішній_значення 링크 또는 특수 파일을 포함한 의존성");
        Files.createDirectories(місце_значення);
        int Стан_значення = new ProcessBuilder("tar","--no-same-owner","--no-same-permissions","-xzf",Архів_значення.toString(),"-C",місце_значення.toString()).inheritIO().start().waitFor();
        if (Стан_значення != 0) throw new IOException("의존성 Архів_значення випуск_місце неполадка_значення");
    }
    static void 호출(Path 작업경로, Path інструменти, List<String> аргументи, Map<String,String> середовище) throws Exception {
        List<String> команда = new ArrayList<>(Arrays.asList("python3", інструменти.toString())); команда.addAll(аргументи);
        ProcessBuilder Виконати_команда = new ProcessBuilder(команда).directory(작업경로.toFile()).inheritIO(); Виконати_команда.environment().putAll(середовище);
        int Стан_значення = Виконати_команда.start().waitFor(); if (Стан_значення != 0) throw new IOException("інструменти неполадка_значення: " + інструменти + " (" + Стан_значення + ")");
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] аргументи) throws Exception {
        if (аргументи.length < 1) throw new IllegalArgumentException("build, run, desktop, image, check, test-system 중 동작을 지정하세요");
        String Дія = аргументи[0];
        if (!Arrays.asList("build","run","desktop","image","check","test-system").contains(Дія)) throw new IllegalArgumentException("알 수 없는 Дія");
        Path Дії_корінь = Paths.get(System.getProperty("worldos.edition.root")).toAbsolutePath().normalize();
        Map<String,Object> Налаштування = (Map<String,Object>)new дані_аналізатор(Files.readString(Дії_корінь.resolve("native.json"),StandardCharsets.UTF_8)).Читання();
        Path джерело_дерево = внутрішній_шлях(Дії_корінь,(String)Налаштування.get("source")), ядро_значення = внутрішній_шлях(джерело_дерево,(String)Налаштування.get("native"));
        List<String> 소유파일들 = (List<String>)(List<?>)Налаштування.get("owned_files");
        for (String Назва : 소유파일들) if (!Files.isRegularFile(внутрішній_шлях(джерело_дерево,Назва))) throw new IOException("джерело_дерево 없음: " + Назва);
        if (Дія.equals("check")) { System.out.println(Налаштування.get("country") + " " + Налаштування.get("language") + " 독립 джерело_дерево перевіряти 완료"); return; }
        String ресурс_відносний_шлях = (String)Налаштування.getOrDefault("resource_root", ".");
        if (!ресурс_відносний_шлях.equals(".") && !ресурс_відносний_шлях.equals("..")) throw new IllegalArgumentException("의존성 Дії_корінь шлях ПОМИЛКА");
        Path ресурс_значення = Дії_корінь.resolve(ресурс_відносний_шлях).normalize(); Path Архів_значення = ресурс_значення.resolve("native-vendor.tar.gz");
        String 기대해시 = (String)Налаштування.get("vendor_sha256");
        if (!геш_код_Файл(Архів_значення).equals(기대해시)) throw new IOException("의존성 SHA-256 불일치");
        Path маркер_значення_7e8f90bd = джерело_дерево.resolve(".vendor-sha256");
        if (!Files.isRegularFile(маркер_значення_7e8f90bd) || !Files.readString(маркер_значення_7e8f90bd).trim().equals(기대해시)) { видобувати(Архів_значення, джерело_дерево); Files.writeString(маркер_значення_7e8f90bd,기대해시 + "\n"); }
        Map<String,String> середовище = new HashMap<>(System.getenv());
        Path ipConfig = null;
        if (середовище.containsKey("IP_CONFIG")) ipConfig = Paths.get(середовище.get("IP_CONFIG")).toAbsolutePath().normalize();
        else for (Path parent = Дії_корінь; parent != null; parent = parent.getParent()) {
            if (Files.isRegularFile(parent.resolve("ip.conf"))) { ipConfig = parent.resolve("ip.conf"); break; }
        }
        if (ipConfig == null) ipConfig = джерело_дерево.resolve("ip.conf");
        if (!Files.isRegularFile(ipConfig)) throw new IOException("Missing ip.conf: " + ipConfig);
        середовище.put("IP_CONFIG", ipConfig.toString());
        if (Arrays.asList("run","desktop","test-system").contains(Дія) && !середовище.containsKey("QEMU_AARCH64")) {
            Path програма_запускач = ресурс_значення.resolve("host/qemu"), запускач_маркер = ресурс_значення.resolve("host/.qemu-sha256");
            String запускач_геш_код = (String)Налаштування.get("qemu_sha256");
            if (!Files.isRegularFile(програма_запускач) || !Files.isRegularFile(запускач_маркер) || !Files.readString(запускач_маркер).trim().equals(запускач_геш_код)) {
                Path запускач_Архів = ресурс_значення.resolve("qemu-host.tar.gz"); if (!геш_код_Файл(запускач_Архів).equals(запускач_геш_код)) throw new IOException("QEMU SHA-256 불일치");
                видобувати(запускач_Архів,ресурс_значення.resolve("host")); Files.writeString(запускач_маркер,запускач_геш_код + "\n");
            }
            середовище.put("QEMU_AARCH64",програма_запускач.toString());
        }
        MessageDigest 계산 = MessageDigest.getInstance("SHA-256"); Collections.sort(소유파일들);
        for (String Назва : 소유파일들) { 계산.update(Назва.getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(внутрішній_шлях(джерело_дерево,Назва))); }
        계산.update("ip.conf\0".getBytes(StandardCharsets.UTF_8)); 계산.update(Files.readAllBytes(ipConfig));
        String джерело_геш_код = геш_код_Текст(계산.digest()); Path збірка_маркер = ядро_значення.resolve("build/worldos-source.sha256");
        if (Дія.equals("build") || !Files.isRegularFile(збірка_маркер) || !Files.readString(збірка_маркер).trim().equals(джерело_геш_код)) {
            호출(ядро_значення,внутрішній_шлях(ядро_значення,(String)Налаштування.get("builder")),Collections.emptyList(),середовище);
            Files.writeString(збірка_маркер,джерело_геш_код + "\n");
        }
        List<String> 추가인수 = new ArrayList<>(Arrays.asList(аргументи).subList(1,аргументи.length));
        if (Дія.equals("run") || Дія.equals("desktop")) {
            if (Дія.equals("desktop")) 추가인수.add(0,"--desktop");
            호출(ядро_значення,внутрішній_шлях(ядро_значення,(String)Налаштування.get("runner")),추가인수,середовище);
        } else if (Дія.equals("image")) 호출(ядро_значення,внутрішній_шлях(ядро_значення,(String)Налаштування.get("image_builder")),추가인수,середовище);
        else if (Дія.equals("test-system")) {
            추가인수.add(0,Дії_корінь.toString()); 추가인수.add(0,"--edition");
            호출(ядро_значення,внутрішній_шлях(ядро_значення,(String)Налаштування.get("system_tester")),추가인수,середовище);
        }
    }
}
