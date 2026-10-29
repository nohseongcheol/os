// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;
/** Reçoit et traite les notifications d’action, notamment celles des boutons. */
public interface RécepteurAction {
    void recevoirAction(NotificationAction notification);
}
