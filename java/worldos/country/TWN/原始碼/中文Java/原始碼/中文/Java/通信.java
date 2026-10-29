// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.Java;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 通信 {
    private 通信() {}
    /** 回傳完整回應，讓呼叫者也能判斷 HTTP 錯誤狀態。 */
    public static HttpResponse<String> 取用值(URI 地址, Duration 時間限制)
            throws IOException, InterruptedException {
        HttpClient 連接 = HttpClient.newBuilder().connectTimeout(時間限制).build();
        return 連接.send(HttpRequest.newBuilder(地址).timeout(時間限制).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 連接端點(String 地址, int 硬件埠, int 限制毫秒) throws IOException {
        Socket 連接 = new Socket();
        try {
            連接.connect(new InetSocketAddress(地址, 硬件埠), 限制毫秒);
            連接.setSoTimeout(限制毫秒);
            return 連接;
        } catch (IOException 錯誤) { 連接.close(); throw 錯誤; }
    }
}
