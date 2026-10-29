// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.Java;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** စံ Path နှင့် IOException ကို တိုက်ရိုက် သုံးသော UTF-8 ဖိုင်အကူ။ */
public final class ဖိုင် {
    private ဖိုင်() {}
    public static Path လမ်း(String အမည်) { return Path.of(အမည်); }
    public static String ဖတ်(Path လမ်း) throws IOException {
        return Files.readString(လမ်း, StandardCharsets.UTF_8);
    }
    public static Path ရေး(Path လမ်း, String အကြောင်းအရာတန်ဖိုး) throws IOException {
        return Files.writeString(လမ်း, အကြောင်းအရာတန်ဖိုး, StandardCharsets.UTF_8);
    }
    public static byte[] ဘိုက်တန်ဖိုးဖတ်(Path လမ်း) throws IOException { return Files.readAllBytes(လမ်း); }
    public static Path ဘိုက်တန်ဖိုးရေး(Path လမ်း, byte[] အကြောင်းအရာတန်ဖိုး) throws IOException { return Files.write(လမ်း, အကြောင်းအရာတန်ဖိုး); }
    public static Path ဖိုင်တွဲဖန်တီး(Path လမ်း) throws IOException { return Files.createDirectories(လမ်း); }
    public static boolean ရှိသလား(Path လမ်း) { return Files.exists(လမ်း); }
    public static boolean အချက်ဖျက်(Path လမ်း) throws IOException { return Files.deleteIfExists(လမ်း); }
    public static List<Path> အချက်စာရင်း(Path လမ်း) throws IOException {
        try (Stream<Path> အချက်တန်ဖိုး = Files.list(လမ်း)) { return အချက်တန်ဖိုး.sorted().collect(Collectors.toList()); }
    }
}
