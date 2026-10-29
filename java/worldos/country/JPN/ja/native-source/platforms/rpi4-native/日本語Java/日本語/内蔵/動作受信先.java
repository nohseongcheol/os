// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;
/** ボタンなどの動作通知を受け取って処理する役割。 */
public interface 動作受信先 {
    void 動作受取(動作通知 通知);
}
