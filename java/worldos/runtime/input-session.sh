#!/bin/sh
export XMODIFIERS=@im=fcitx
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XDG_RUNTIME_DIR=/run/user/1000
fcitx5 -d --disable=wayland,waylandim >/tmp/fcitx.log 2>&1
attempt=0
while [ "$attempt" -lt 120 ]; do
    if dbus-send --session --print-reply --dest=org.freedesktop.DBus \
        /org/freedesktop/DBus org.freedesktop.DBus.NameHasOwner \
        string:org.fcitx.Fcitx5 2>/dev/null | grep -q 'boolean true'; then
        break
    fi
    sleep 0.5
    attempt=$((attempt + 1))
done
