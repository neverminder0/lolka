#pragma once

#include <QObject>
#include <QString>
#include <QPoint>
#include <QRect>
#include <QList>

struct WindowInfo {
    QString title;
    QString processName;
    qint64 processId;
    void* handle; // Platform-specific window handle
    QRect geometry;
    bool isVisible;
    bool isMinimized;
};

class WindowBinder : public QObject
{
    Q_OBJECT

public:
    explicit WindowBinder(QObject *parent = nullptr);
    virtual ~WindowBinder() = default;

    // Factory method for platform-specific implementations
    static WindowBinder* create(QObject *parent = nullptr);

    // Window enumeration
    virtual QList<WindowInfo> getAllWindows() = 0;
    virtual QList<WindowInfo> getWindowsByTitle(const QString& title) = 0;
    virtual QList<WindowInfo> getWindowsByProcess(const QString& processName) = 0;
    
    // Window targeting
    virtual WindowInfo getActiveWindow() = 0;
    virtual WindowInfo getWindowAtPoint(const QPoint& point) = 0;
    virtual bool setActiveWindow(const WindowInfo& window) = 0;
    
    // Coordinate conversion
    virtual QPoint windowToScreen(const WindowInfo& window, const QPoint& windowPoint) = 0;
    virtual QPoint screenToWindow(const WindowInfo& window, const QPoint& screenPoint) = 0;
    
    // Window state
    virtual bool isWindowValid(const WindowInfo& window) = 0;
    virtual WindowInfo refreshWindowInfo(const WindowInfo& window) = 0;
    
    // Bound window management
    void bindToWindow(const WindowInfo& window);
    void bindToWindowByTitle(const QString& title);
    void bindToWindowByProcess(const QString& processName);
    void unbindWindow();
    
    bool isBound() const { return m_boundWindow.handle != nullptr; }
    WindowInfo boundWindow() const { return m_boundWindow; }
    
    // Convert coordinates if bound to a window
    QPoint convertCoordinate(const QPoint& point, bool relativeToWindow = false);

signals:
    void windowBound(const WindowInfo& window);
    void windowUnbound();
    void windowUpdated(const WindowInfo& window);
    void windowLost(); // Bound window is no longer valid
    void errorOccurred(const QString& error);

private slots:
    void checkBoundWindow();

protected:
    WindowInfo m_boundWindow;
    QTimer* m_windowCheckTimer;
    bool m_relativeCoordinates = false;
};