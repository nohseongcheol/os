// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.Java;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 通信 {
    private 通信() {}
    /** 返回完整响应，让调用者也能判断 HTTP 错误状态。 */
    public static HttpResponse<String> 取用值(URI 地址, Duration 时间限制)
            throws IOException, InterruptedException {
        HttpClient 连接 = HttpClient.newBuilder().connectTimeout(时间限制).build();
        return 连接.send(HttpRequest.newBuilder(地址).timeout(时间限制).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 连接端点(String 地址, int 硬件端口, int 限制毫秒) throws IOException {
        Socket 连接 = new Socket();
        try {
            连接.connect(new InetSocketAddress(地址, 硬件端口), 限制毫秒);
            连接.setSoTimeout(限制毫秒);
            return 连接;
        } catch (IOException 错误) { 连接.close(); throw 错误; }
    }
}
