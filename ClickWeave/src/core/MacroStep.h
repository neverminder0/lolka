#pragma once

#include <QObject>
#include <QPoint>
#include <QColor>
#include <QJsonObject>
#include "ClickEngine.h"

enum class StepType {
    Click,
    Move,
    Delay,
    KeyPress,
    Scroll,
    PixelTrigger
};

class MacroStep : public QObject
{
    Q_OBJECT
    Q_PROPERTY(StepType stepType READ stepType WRITE setStepType NOTIFY stepTypeChanged)
    Q_PROPERTY(ClickType clickType READ clickType WRITE setClickType NOTIFY clickTypeChanged)
    Q_PROPERTY(ClickMode clickMode READ clickMode WRITE setClickMode NOTIFY clickModeChanged)
    Q_PROPERTY(QPoint position READ position WRITE setPosition NOTIFY positionChanged)
    Q_PROPERTY(int delayMs READ delayMs WRITE setDelayMs NOTIFY delayMsChanged)
    Q_PROPERTY(int duration READ duration WRITE setDuration NOTIFY durationChanged)
    Q_PROPERTY(QString keyCode READ keyCode WRITE setKeyCode NOTIFY keyCodeChanged)
    Q_PROPERTY(int scrollDelta READ scrollDelta WRITE setScrollDelta NOTIFY scrollDeltaChanged)
    Q_PROPERTY(QString description READ description WRITE setDescription NOTIFY descriptionChanged)
    Q_PROPERTY(bool enabled READ enabled WRITE setEnabled NOTIFY enabledChanged)
    Q_PROPERTY(bool relativeToWindow READ relativeToWindow WRITE setRelativeToWindow NOTIFY relativeToWindowChanged)

public:
    explicit MacroStep(QObject *parent = nullptr);
    explicit MacroStep(StepType type, QObject *parent = nullptr);
    ~MacroStep() = default;

    // Basic properties
    StepType stepType() const { return m_stepType; }
    void setStepType(StepType type);

    ClickType clickType() const { return m_clickType; }
    void setClickType(ClickType type);

    ClickMode clickMode() const { return m_clickMode; }
    void setClickMode(ClickMode mode);

    QPoint position() const { return m_position; }
    void setPosition(const QPoint& position);

    int delayMs() const { return m_delayMs; }
    void setDelayMs(int delay);

    int duration() const { return m_duration; }
    void setDuration(int duration);

    QString keyCode() const { return m_keyCode; }
    void setKeyCode(const QString& key);

    int scrollDelta() const { return m_scrollDelta; }
    void setScrollDelta(int delta);

    QString description() const { return m_description; }
    void setDescription(const QString& description);

    bool enabled() const { return m_enabled; }
    void setEnabled(bool enabled);

    bool relativeToWindow() const { return m_relativeToWindow; }
    void setRelativeToWindow(bool relative);

    // Pixel trigger properties
    bool hasPixelTrigger() const { return m_hasPixelTrigger; }
    void setHasPixelTrigger(bool has);

    QPoint pixelPosition() const { return m_pixelPosition; }
    void setPixelPosition(const QPoint& position);

    QColor pixelColor() const { return m_pixelColor; }
    void setPixelColor(const QColor& color);

    int pixelTolerance() const { return m_pixelTolerance; }
    void setPixelTolerance(int tolerance);

    // Convenience methods
    bool isClick() const { return m_stepType == StepType::Click; }
    bool isMove() const { return m_stepType == StepType::Move; }
    bool isDelay() const { return m_stepType == StepType::Delay; }
    bool isKeyPress() const { return m_stepType == StepType::KeyPress; }
    bool isScroll() const { return m_stepType == StepType::Scroll; }
    bool isPixelTrigger() const { return m_stepType == StepType::PixelTrigger; }

    // Serialization
    QJsonObject toJson() const;
    static MacroStep* fromJson(const QJsonObject& json, QObject* parent = nullptr);

    // Validation
    bool isValid() const;
    QStringList validate() const;

    // Display helpers
    QString displayName() const;
    QString stepTypeString() const;
    QString clickTypeString() const;
    QString clickModeString() const;

public slots:
    // Factory methods for common step types
    static MacroStep* createClick(const QPoint& position, ClickType type = ClickType::LeftClick, QObject* parent = nullptr);
    static MacroStep* createMove(const QPoint& position, QObject* parent = nullptr);
    static MacroStep* createDelay(int delayMs, QObject* parent = nullptr);
    static MacroStep* createKeyPress(const QString& keyCode, QObject* parent = nullptr);
    static MacroStep* createScroll(const QPoint& position, int delta, QObject* parent = nullptr);
    static MacroStep* createPixelTrigger(const QPoint& position, const QColor& color, int tolerance = 0, QObject* parent = nullptr);

signals:
    void stepTypeChanged();
    void clickTypeChanged();
    void clickModeChanged();
    void positionChanged();
    void delayMsChanged();
    void durationChanged();
    void keyCodeChanged();
    void scrollDeltaChanged();
    void descriptionChanged();
    void enabledChanged();
    void relativeToWindowChanged();
    void pixelTriggerChanged();

private:
    StepType m_stepType = StepType::Click;
    ClickType m_clickType = ClickType::LeftClick;
    ClickMode m_clickMode = ClickMode::Single;
    QPoint m_position;
    int m_delayMs = 0;
    int m_duration = 100; // Default hold duration
    QString m_keyCode;
    int m_scrollDelta = 0;
    QString m_description;
    bool m_enabled = true;
    bool m_relativeToWindow = false;
    
    // Pixel trigger properties
    bool m_hasPixelTrigger = false;
    QPoint m_pixelPosition;
    QColor m_pixelColor;
    int m_pixelTolerance = 0;
};