#pragma once

#include <QObject>
#include <QPoint>
#include <QTimer>
#include <QColor>
#include <chrono>
#include <memory>

enum class ClickType {
    LeftClick,
    RightClick,
    MiddleClick,
    DoubleClick,
    MouseDown,
    MouseUp,
    Scroll,
    KeyPress
};

enum class ClickMode {
    Single,
    Double,
    Hold
};

struct ClickAction {
    ClickType type;
    ClickMode mode;
    QPoint position;
    int duration = 0; // For hold mode, in milliseconds
    QString keyCode; // For key presses
    int scrollDelta = 0; // For scroll actions
};

class Profile;
class MacroStep;

class ClickEngine : public QObject
{
    Q_OBJECT
    Q_PROPERTY(bool isRunning READ isRunning NOTIFY isRunningChanged)
    Q_PROPERTY(bool isPaused READ isPaused NOTIFY isPausedChanged)
    Q_PROPERTY(int clickCount READ clickCount NOTIFY clickCountChanged)
    Q_PROPERTY(QString status READ status NOTIFY statusChanged)

public:
    explicit ClickEngine(QObject *parent = nullptr);
    virtual ~ClickEngine() = default;

    bool isRunning() const { return m_isRunning; }
    bool isPaused() const { return m_isPaused; }
    int clickCount() const { return m_clickCount; }
    QString status() const { return m_status; }

    // Factory method for platform-specific engines
    static std::unique_ptr<ClickEngine> create(QObject *parent = nullptr);

public slots:
    void startClicking();
    void stopClicking();
    void pauseClicking();
    void resumeClicking();
    void emergencyStop();
    
    void setProfile(Profile* profile);
    void executeAction(const ClickAction& action);
    
    // Coordinate and pixel utilities
    QPoint getCurrentMousePosition();
    QColor getPixelColor(const QPoint& position);
    bool checkPixelTrigger(const QPoint& position, const QColor& targetColor, int tolerance = 0);

signals:
    void isRunningChanged();
    void isPausedChanged();
    void clickCountChanged();
    void statusChanged();
    void clickExecuted(const QPoint& position, ClickType type);
    void profileCompleted();
    void errorOccurred(const QString& error);

protected:
    // Platform-specific implementations
    virtual void performClick(const ClickAction& action) = 0;
    virtual void moveMouseTo(const QPoint& position) = 0;
    virtual QPoint getMousePosition() = 0;
    virtual QColor capturePixelColor(const QPoint& position) = 0;
    virtual void pressKey(const QString& keyCode) = 0;
    virtual void releaseKey(const QString& keyCode) = 0;

private slots:
    void executeNextStep();
    void updateStatus();

private:
    void resetExecution();
    void calculateNextDelay();
    int applyJitter(int baseInterval) const;

private:
    bool m_isRunning = false;
    bool m_isPaused = false;
    int m_clickCount = 0;
    QString m_status = "Ready";
    
    Profile* m_currentProfile = nullptr;
    QTimer* m_executionTimer;
    QTimer* m_statusTimer;
    
    int m_currentStepIndex = 0;
    int m_currentRepetition = 0;
    std::chrono::steady_clock::time_point m_startTime;
    std::chrono::steady_clock::time_point m_lastClickTime;
    
    // Safety features
    QPoint m_lastMousePosition;
    bool m_failsafeTriggered = false;
};