// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.Java;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class ဆက်သွယ်မှု {
    private ဆက်သွယ်မှု() {}
    /** ခေါ်ဆိုသူက HTTP အမှားအခြေအနေကိုလည်း ဆုံးဖြတ်နိုင်ရန် တုံ့ပြန်ချက်တစ်ခုလုံး ပြန်ပေးသည်။ */
    public static HttpResponse<String> တန်ဖိုးယူ(URI လိပ်စာ, Duration အချိန်ကန့်သတ်ချက်)
            throws IOException, InterruptedException {
        HttpClient ချိတ်ဆက် = HttpClient.newBuilder().connectTimeout(အချိန်ကန့်သတ်ချက်).build();
        return ချိတ်ဆက်.send(HttpRequest.newBuilder(လိပ်စာ).timeout(အချိန်ကန့်သတ်ချက်).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket အဆုံးမှတ်ချိတ်ဆက်(String လိပ်စာ, int စက်ပစ္စည်းဆက်သွယ်ပေါက်, int အများဆုံးမီလီစက္ကန့်) throws IOException {
        Socket ချိတ်ဆက် = new Socket();
        try {
            ချိတ်ဆက်.connect(new InetSocketAddress(လိပ်စာ, စက်ပစ္စည်းဆက်သွယ်ပေါက်), အများဆုံးမီလီစက္ကန့်);
            ချိတ်ဆက်.setSoTimeout(အများဆုံးမီလီစက္ကန့်);
            return ချိတ်ဆက်;
        } catch (IOException အမှား) { ချိတ်ဆက်.close(); throw အမှား; }
    }
}
