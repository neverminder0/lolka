#include "LinuxClickEngine.h"

#ifdef Q_OS_LINUX

#include <X11/keysym.h>
#include <X11/XKBlib.h>
#include <QApplication>
#include <QScreen>
#include <QThread>
#include <QDebug>

LinuxClickEngine::LinuxClickEngine(QObject *parent)
    : ClickEngine(parent)
    , m_display(nullptr)
    , m_screen(0)
{
    m_display = XOpenDisplay(nullptr);
    if (!m_display) {
        qWarning() << "Failed to open X11 display";
        return;
    }
    
    m_screen = DefaultScreen(m_display);
    
    // Check for XTest extension
    int event_base, error_base, major, minor;
    if (!XTestQueryExtension(m_display, &event_base, &error_base, &major, &minor)) {
        qWarning() << "XTest extension not available";
    }
}

LinuxClickEngine::~LinuxClickEngine()
{
    if (m_display) {
        XCloseDisplay(m_display);
    }
}

void LinuxClickEngine::performClick(const ClickAction& action)
{
    if (!m_display) {
        return;
    }

    if (action.type == ClickType::KeyPress) {
        pressKey(action.keyCode);
        if (action.mode != ClickMode::Hold) {
            QThread::msleep(action.duration);
            releaseKey(action.keyCode);
        }
        return;
    }

    if (action.position.isNull()) {
        return;
    }

    // Move mouse to position
    moveMouseTo(action.position);
    QThread::msleep(10);

    int button = 0;
    switch (action.type) {
        case ClickType::LeftClick:
        case ClickType::DoubleClick:
            button = Button1;
            break;
        case ClickType::RightClick:
            button = Button3;
            break;
        case ClickType::MiddleClick:
            button = Button2;
            break;
        case ClickType::Scroll:
            button = (action.scrollDelta > 0) ? Button4 : Button5;
            for (int i = 0; i < abs(action.scrollDelta); ++i) {
                sendMouseEvent(action.position.x(), action.position.y(), button, true);
                sendMouseEvent(action.position.x(), action.position.y(), button, false);
                QThread::msleep(10);
            }
            return;
        case ClickType::MouseDown:
            sendMouseEvent(action.position.x(), action.position.y(), Button1, true);
            return;
        case ClickType::MouseUp:
            sendMouseEvent(action.position.x(), action.position.y(), Button1, false);
            return;
        default:
            return;
    }

    if (action.type == ClickType::DoubleClick) {
        // First click
        sendMouseEvent(action.position.x(), action.position.y(), button, true);
        sendMouseEvent(action.position.x(), action.position.y(), button, false);
        QThread::msleep(50);
        // Second click
        sendMouseEvent(action.position.x(), action.position.y(), button, true);
        sendMouseEvent(action.position.x(), action.position.y(), button, false);
    } else {
        sendMouseEvent(action.position.x(), action.position.y(), button, true);
        
        if (action.mode == ClickMode::Hold) {
            QThread::msleep(action.duration);
        } else {
            QThread::msleep(10);
        }
        
        sendMouseEvent(action.position.x(), action.position.y(), button, false);
    }
}

void LinuxClickEngine::moveMouseTo(const QPoint& position)
{
    if (!m_display) {
        return;
    }
    
    XTestFakeMotionEvent(m_display, m_screen, position.x(), position.y(), CurrentTime);
    XFlush(m_display);
}

QPoint LinuxClickEngine::getMousePosition()
{
    if (!m_display) {
        return QPoint();
    }
    
    Window root, child;
    int root_x, root_y, win_x, win_y;
    unsigned int mask;
    
    if (XQueryPointer(m_display, DefaultRootWindow(m_display),
                      &root, &child, &root_x, &root_y, &win_x, &win_y, &mask)) {
        return QPoint(root_x, root_y);
    }
    
    return QPoint();
}

QColor LinuxClickEngine::capturePixelColor(const QPoint& position)
{
    return getPixelColorFromScreen(position);
}

void LinuxClickEngine::pressKey(const QString& keyCode)
{
    KeySym keysym = stringToKeySym(keyCode);
    if (keysym != NoSymbol) {
        sendKeyEvent(keysym, true);
    }
}

void LinuxClickEngine::releaseKey(const QString& keyCode)
{
    KeySym keysym = stringToKeySym(keyCode);
    if (keysym != NoSymbol) {
        sendKeyEvent(keysym, false);
    }
}

void LinuxClickEngine::sendMouseEvent(int x, int y, int button, bool press)
{
    if (!m_display) {
        return;
    }
    
    XTestFakeButtonEvent(m_display, button, press ? True : False, CurrentTime);
    XFlush(m_display);
}

void LinuxClickEngine::sendKeyEvent(KeySym keysym, bool press)
{
    if (!m_display) {
        return;
    }
    
    KeyCode keycode = XKeysymToKeycode(m_display, keysym);
    if (keycode != 0) {
        XTestFakeKeyEvent(m_display, keycode, press ? True : False, CurrentTime);
        XFlush(m_display);
    }
}

KeySym LinuxClickEngine::stringToKeySym(const QString& keyString)
{
    QString key = keyString.toLower();
    
    // Special keys
    if (key == "esc" || key == "escape") return XK_Escape;
    if (key == "enter" || key == "return") return XK_Return;
    if (key == "space") return XK_space;
    if (key == "tab") return XK_Tab;
    if (key == "shift") return XK_Shift_L;
    if (key == "ctrl" || key == "control") return XK_Control_L;
    if (key == "alt") return XK_Alt_L;
    if (key == "super" || key == "win") return XK_Super_L;
    
    // Arrow keys
    if (key == "up") return XK_Up;
    if (key == "down") return XK_Down;
    if (key == "left") return XK_Left;
    if (key == "right") return XK_Right;
    
    // Function keys
    if (key.startsWith("f") && key.length() <= 3) {
        bool ok;
        int fNum = key.mid(1).toInt(&ok);
        if (ok && fNum >= 1 && fNum <= 24) {
            return XK_F1 + fNum - 1;
        }
    }
    
    // Convert string to KeySym
    return XStringToKeysym(keyString.toLatin1().data());
}

QColor LinuxClickEngine::getPixelColorFromScreen(const QPoint& position)
{
    if (!m_display) {
        return QColor();
    }
    
    Window root = DefaultRootWindow(m_display);
    XImage* image = XGetImage(m_display, root, position.x(), position.y(), 1, 1, AllPlanes, ZPixmap);
    
    if (!image) {
        return QColor();
    }
    
    unsigned long pixel = XGetPixel(image, 0, 0);
    XDestroyImage(image);
    
    // Extract RGB values (assuming 24-bit color)
    int r = (pixel >> 16) & 0xFF;
    int g = (pixel >> 8) & 0xFF;
    int b = pixel & 0xFF;
    
    return QColor(r, g, b);
}

#endif // Q_OS_LINUX