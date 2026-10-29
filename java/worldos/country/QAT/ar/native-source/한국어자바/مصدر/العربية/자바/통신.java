// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP خطأ 상태도 호출자가 판단할 رقم 있도록 رد 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI عنوان, Duration الحد_الزمني)
            throws IOException, InterruptedException {
        HttpClient اتصال = HttpClient.newBuilder().connectTimeout(الحد_الزمني).build();
        return اتصال.send(HttpRequest.newBuilder(عنوان).timeout(الحد_الزمني).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket يتصل_المشارك(String عنوان, int أجهزة_منفذ, int 제한밀리초) throws IOException {
        Socket اتصال = new Socket();
        try {
            اتصال.connect(new InetSocketAddress(عنوان, أجهزة_منفذ), 제한밀리초);
            اتصال.setSoTimeout(제한밀리초);
            return اتصال;
        } catch (IOException خطأ) { اتصال.close(); throw خطأ; }
    }
}
