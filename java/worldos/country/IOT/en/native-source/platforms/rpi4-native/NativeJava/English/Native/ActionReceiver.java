// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;
/** Receives and handles action notifications, such as button actions. */
public interface ActionReceiver {
    void receiveAction(ActionNotice notice);
}
