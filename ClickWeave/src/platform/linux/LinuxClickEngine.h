#pragma once

#include "../core/ClickEngine.h"

#ifdef Q_OS_LINUX

#include <X11/Xlib.h>
#include <X11/extensions/XTest.h>

class LinuxClickEngine : public ClickEngine
{
    Q_OBJECT

public:
    explicit LinuxClickEngine(QObject *parent = nullptr);
    ~LinuxClickEngine() override;

protected:
    void performClick(const ClickAction& action) override;
    void moveMouseTo(const QPoint& position) override;
    QPoint getMousePosition() override;
    QColor capturePixelColor(const QPoint& position) override;
    void pressKey(const QString& keyCode) override;
    void releaseKey(const QString& keyCode) override;

private:
    // X11-specific helper methods
    void sendMouseEvent(int x, int y, int button, bool press);
    void sendKeyEvent(KeySym keysym, bool press);
    KeySym stringToKeySym(const QString& keyString);
    QColor getPixelColorFromScreen(const QPoint& position);

private:
    Display* m_display;
    int m_screen;
};

#endif // Q_OS_LINUX