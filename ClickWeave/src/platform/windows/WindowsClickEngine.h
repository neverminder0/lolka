#pragma once

#include "../core/ClickEngine.h"

#ifdef Q_OS_WIN

class WindowsClickEngine : public ClickEngine
{
    Q_OBJECT

public:
    explicit WindowsClickEngine(QObject *parent = nullptr);
    ~WindowsClickEngine() override = default;

protected:
    void performClick(const ClickAction& action) override;
    void moveMouseTo(const QPoint& position) override;
    QPoint getMousePosition() override;
    QColor capturePixelColor(const QPoint& position) override;
    void pressKey(const QString& keyCode) override;
    void releaseKey(const QString& keyCode) override;

private:
    // Windows-specific helper methods
    void sendMouseInput(int x, int y, unsigned long flags, unsigned long data = 0);
    void sendKeyboardInput(unsigned short keyCode, bool keyUp = false);
    unsigned short stringToVirtualKey(const QString& keyString);
    QColor getPixelColorFromScreen(const QPoint& position);
};

#endif // Q_OS_WIN