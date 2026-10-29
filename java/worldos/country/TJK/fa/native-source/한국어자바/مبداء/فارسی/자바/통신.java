// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP خطا 상태도 호출자가 판단할 수 있도록 پاسخ_دادن 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI آدرس, Duration محدوده_زمان_مجاز)
            throws IOException, InterruptedException {
        HttpClient اتصال = HttpClient.newBuilder().connectTimeout(محدوده_زمان_مجاز).build();
        return اتصال.send(HttpRequest.newBuilder(آدرس).timeout(محدوده_زمان_مجاز).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String آدرس, int 포트, int 제한밀리초) throws IOException {
        Socket اتصال = new Socket();
        try {
            اتصال.connect(new InetSocketAddress(آدرس, 포트), 제한밀리초);
            اتصال.setSoTimeout(제한밀리초);
            return اتصال;
        } catch (IOException خطا) { اتصال.close(); throw خطا; }
    }
}
