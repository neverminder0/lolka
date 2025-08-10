#include "WindowsClickEngine.h"

#ifdef Q_OS_WIN

#include <windows.h>
#include <QApplication>
#include <QScreen>
#include <QDebug>

WindowsClickEngine::WindowsClickEngine(QObject *parent)
    : ClickEngine(parent)
{
}

void WindowsClickEngine::performClick(const ClickAction& action)
{
    if (action.position.isNull()) {
        return;
    }

    // Move mouse to position first if needed
    if (action.type != ClickType::KeyPress) {
        moveMouseTo(action.position);
        QThread::msleep(10); // Small delay for mouse movement
    }

    unsigned long downFlags = 0, upFlags = 0;
    unsigned long data = 0;

    switch (action.type) {
        case ClickType::LeftClick:
            downFlags = MOUSEEVENTF_LEFTDOWN;
            upFlags = MOUSEEVENTF_LEFTUP;
            break;
        case ClickType::RightClick:
            downFlags = MOUSEEVENTF_RIGHTDOWN;
            upFlags = MOUSEEVENTF_RIGHTUP;
            break;
        case ClickType::MiddleClick:
            downFlags = MOUSEEVENTF_MIDDLEDOWN;
            upFlags = MOUSEEVENTF_MIDDLEUP;
            break;
        case ClickType::MouseDown:
            downFlags = MOUSEEVENTF_LEFTDOWN;
            break;
        case ClickType::MouseUp:
            upFlags = MOUSEEVENTF_LEFTUP;
            break;
        case ClickType::Scroll:
            sendMouseInput(action.position.x(), action.position.y(), 
                          MOUSEEVENTF_WHEEL, action.scrollDelta * WHEEL_DELTA);
            return;
        case ClickType::KeyPress:
            pressKey(action.keyCode);
            if (action.mode != ClickMode::Hold) {
                QThread::msleep(action.duration);
                releaseKey(action.keyCode);
            }
            return;
        case ClickType::DoubleClick:
            // First click
            sendMouseInput(action.position.x(), action.position.y(), MOUSEEVENTF_LEFTDOWN);
            sendMouseInput(action.position.x(), action.position.y(), MOUSEEVENTF_LEFTUP);
            QThread::msleep(10);
            // Second click
            sendMouseInput(action.position.x(), action.position.y(), MOUSEEVENTF_LEFTDOWN);
            sendMouseInput(action.position.x(), action.position.y(), MOUSEEVENTF_LEFTUP);
            return;
    }

    // Perform mouse down
    if (downFlags != 0) {
        sendMouseInput(action.position.x(), action.position.y(), downFlags, data);
    }

    // Handle different click modes
    if (action.mode == ClickMode::Hold) {
        QThread::msleep(action.duration);
    } else if (action.mode == ClickMode::Double) {
        QThread::msleep(10);
        if (upFlags != 0) {
            sendMouseInput(action.position.x(), action.position.y(), upFlags, data);
        }
        QThread::msleep(10);
        if (downFlags != 0) {
            sendMouseInput(action.position.x(), action.position.y(), downFlags, data);
        }
    }

    // Perform mouse up
    if (upFlags != 0) {
        if (action.mode == ClickMode::Single || action.mode == ClickMode::Double) {
            QThread::msleep(10); // Small delay between down and up
        }
        sendMouseInput(action.position.x(), action.position.y(), upFlags, data);
    }
}

void WindowsClickEngine::moveMouseTo(const QPoint& position)
{
    sendMouseInput(position.x(), position.y(), MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE);
}

QPoint WindowsClickEngine::getMousePosition()
{
    POINT point;
    if (GetCursorPos(&point)) {
        return QPoint(point.x, point.y);
    }
    return QPoint();
}

QColor WindowsClickEngine::capturePixelColor(const QPoint& position)
{
    return getPixelColorFromScreen(position);
}

void WindowsClickEngine::pressKey(const QString& keyCode)
{
    unsigned short vk = stringToVirtualKey(keyCode);
    if (vk != 0) {
        sendKeyboardInput(vk, false);
    }
}

void WindowsClickEngine::releaseKey(const QString& keyCode)
{
    unsigned short vk = stringToVirtualKey(keyCode);
    if (vk != 0) {
        sendKeyboardInput(vk, true);
    }
}

void WindowsClickEngine::sendMouseInput(int x, int y, unsigned long flags, unsigned long data)
{
    INPUT input = {};
    input.type = INPUT_MOUSE;
    input.mi.dx = x;
    input.mi.dy = y;
    input.mi.dwFlags = flags;
    input.mi.mouseData = data;
    input.mi.time = 0;
    input.mi.dwExtraInfo = 0;

    // Convert to screen coordinates if needed
    if (flags & MOUSEEVENTF_ABSOLUTE) {
        QScreen* screen = QApplication::primaryScreen();
        QRect screenGeometry = screen->geometry();
        input.mi.dx = (x * 65535) / screenGeometry.width();
        input.mi.dy = (y * 65535) / screenGeometry.height();
    }

    SendInput(1, &input, sizeof(INPUT));
}

void WindowsClickEngine::sendKeyboardInput(unsigned short keyCode, bool keyUp)
{
    INPUT input = {};
    input.type = INPUT_KEYBOARD;
    input.ki.wVk = keyCode;
    input.ki.wScan = 0;
    input.ki.dwFlags = keyUp ? KEYEVENTF_KEYUP : 0;
    input.ki.time = 0;
    input.ki.dwExtraInfo = 0;

    SendInput(1, &input, sizeof(INPUT));
}

unsigned short WindowsClickEngine::stringToVirtualKey(const QString& keyString)
{
    QString key = keyString.toUpper();
    
    // Special keys
    if (key == "ESC" || key == "ESCAPE") return VK_ESCAPE;
    if (key == "ENTER" || key == "RETURN") return VK_RETURN;
    if (key == "SPACE") return VK_SPACE;
    if (key == "TAB") return VK_TAB;
    if (key == "SHIFT") return VK_SHIFT;
    if (key == "CTRL" || key == "CONTROL") return VK_CONTROL;
    if (key == "ALT") return VK_MENU;
    if (key == "WIN" || key == "WINDOWS") return VK_LWIN;
    
    // Arrow keys
    if (key == "UP") return VK_UP;
    if (key == "DOWN") return VK_DOWN;
    if (key == "LEFT") return VK_LEFT;
    if (key == "RIGHT") return VK_RIGHT;
    
    // Function keys
    if (key.startsWith("F") && key.length() <= 3) {
        bool ok;
        int fNum = key.mid(1).toInt(&ok);
        if (ok && fNum >= 1 && fNum <= 24) {
            return VK_F1 + fNum - 1;
        }
    }
    
    // Single character keys
    if (key.length() == 1) {
        QChar c = key[0];
        if (c.isLetter()) {
            return c.toUpper().toLatin1();
        } else if (c.isDigit()) {
            return c.toLatin1();
        }
    }
    
    return 0; // Unknown key
}

QColor WindowsClickEngine::getPixelColorFromScreen(const QPoint& position)
{
    HDC hdc = GetDC(NULL);
    if (!hdc) {
        return QColor();
    }
    
    COLORREF pixel = GetPixel(hdc, position.x(), position.y());
    ReleaseDC(NULL, hdc);
    
    if (pixel == CLR_INVALID) {
        return QColor();
    }
    
    return QColor(GetRValue(pixel), GetGValue(pixel), GetBValue(pixel));
}

#endif // Q_OS_WIN