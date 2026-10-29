// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.Java;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 通信 {
    private 通信() {}
    /** HTTP エラー状態も呼出し元が判断できるよう、応答全体を返す。 */
    public static HttpResponse<String> 取得処理値(URI 番地, Duration 時間上限)
            throws IOException, InterruptedException {
        HttpClient 接続 = HttpClient.newBuilder().connectTimeout(時間上限).build();
        return 接続.send(HttpRequest.newBuilder(番地).timeout(時間上限).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 通信端点接続(String 番地, int 機器ポート, int 上限ミリ秒) throws IOException {
        Socket 接続 = new Socket();
        try {
            接続.connect(new InetSocketAddress(番地, 機器ポート), 上限ミリ秒);
            接続.setSoTimeout(上限ミリ秒);
            return 接続;
        } catch (IOException エラー) { 接続.close(); throw エラー; }
    }
}
