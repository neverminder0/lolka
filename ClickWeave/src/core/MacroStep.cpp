#include "MacroStep.h"
#include <QJsonObject>
#include <QDebug>

MacroStep::MacroStep(QObject *parent)
    : QObject(parent)
{
}

MacroStep::MacroStep(StepType type, QObject *parent)
    : QObject(parent)
    , m_stepType(type)
{
}

void MacroStep::setStepType(StepType type)
{
    if (m_stepType != type) {
        m_stepType = type;
        emit stepTypeChanged();
    }
}

void MacroStep::setClickType(ClickType type)
{
    if (m_clickType != type) {
        m_clickType = type;
        emit clickTypeChanged();
    }
}

void MacroStep::setClickMode(ClickMode mode)
{
    if (m_clickMode != mode) {
        m_clickMode = mode;
        emit clickModeChanged();
    }
}

void MacroStep::setPosition(const QPoint& position)
{
    if (m_position != position) {
        m_position = position;
        emit positionChanged();
    }
}

void MacroStep::setDelayMs(int delay)
{
    if (m_delayMs != delay && delay >= 0) {
        m_delayMs = delay;
        emit delayMsChanged();
    }
}

void MacroStep::setDuration(int duration)
{
    if (m_duration != duration && duration >= 0) {
        m_duration = duration;
        emit durationChanged();
    }
}

void MacroStep::setKeyCode(const QString& key)
{
    if (m_keyCode != key) {
        m_keyCode = key;
        emit keyCodeChanged();
    }
}

void MacroStep::setScrollDelta(int delta)
{
    if (m_scrollDelta != delta) {
        m_scrollDelta = delta;
        emit scrollDeltaChanged();
    }
}

void MacroStep::setDescription(const QString& description)
{
    if (m_description != description) {
        m_description = description;
        emit descriptionChanged();
    }
}

void MacroStep::setEnabled(bool enabled)
{
    if (m_enabled != enabled) {
        m_enabled = enabled;
        emit enabledChanged();
    }
}

void MacroStep::setRelativeToWindow(bool relative)
{
    if (m_relativeToWindow != relative) {
        m_relativeToWindow = relative;
        emit relativeToWindowChanged();
    }
}

void MacroStep::setHasPixelTrigger(bool has)
{
    if (m_hasPixelTrigger != has) {
        m_hasPixelTrigger = has;
        emit pixelTriggerChanged();
    }
}

void MacroStep::setPixelPosition(const QPoint& position)
{
    if (m_pixelPosition != position) {
        m_pixelPosition = position;
        emit pixelTriggerChanged();
    }
}

void MacroStep::setPixelColor(const QColor& color)
{
    if (m_pixelColor != color) {
        m_pixelColor = color;
        emit pixelTriggerChanged();
    }
}

void MacroStep::setPixelTolerance(int tolerance)
{
    if (m_pixelTolerance != tolerance && tolerance >= 0) {
        m_pixelTolerance = tolerance;
        emit pixelTriggerChanged();
    }
}

QJsonObject MacroStep::toJson() const
{
    QJsonObject json;
    json["stepType"] = static_cast<int>(m_stepType);
    json["clickType"] = static_cast<int>(m_clickType);
    json["clickMode"] = static_cast<int>(m_clickMode);
    json["positionX"] = m_position.x();
    json["positionY"] = m_position.y();
    json["delayMs"] = m_delayMs;
    json["duration"] = m_duration;
    json["keyCode"] = m_keyCode;
    json["scrollDelta"] = m_scrollDelta;
    json["description"] = m_description;
    json["enabled"] = m_enabled;
    json["relativeToWindow"] = m_relativeToWindow;
    json["hasPixelTrigger"] = m_hasPixelTrigger;
    json["pixelPositionX"] = m_pixelPosition.x();
    json["pixelPositionY"] = m_pixelPosition.y();
    json["pixelColorRed"] = m_pixelColor.red();
    json["pixelColorGreen"] = m_pixelColor.green();
    json["pixelColorBlue"] = m_pixelColor.blue();
    json["pixelTolerance"] = m_pixelTolerance;
    
    return json;
}

MacroStep* MacroStep::fromJson(const QJsonObject& json, QObject* parent)
{
    MacroStep* step = new MacroStep(parent);
    
    step->m_stepType = static_cast<StepType>(json["stepType"].toInt());
    step->m_clickType = static_cast<ClickType>(json["clickType"].toInt());
    step->m_clickMode = static_cast<ClickMode>(json["clickMode"].toInt());
    step->m_position = QPoint(json["positionX"].toInt(), json["positionY"].toInt());
    step->m_delayMs = json["delayMs"].toInt(0);
    step->m_duration = json["duration"].toInt(100);
    step->m_keyCode = json["keyCode"].toString();
    step->m_scrollDelta = json["scrollDelta"].toInt(0);
    step->m_description = json["description"].toString();
    step->m_enabled = json["enabled"].toBool(true);
    step->m_relativeToWindow = json["relativeToWindow"].toBool(false);
    step->m_hasPixelTrigger = json["hasPixelTrigger"].toBool(false);
    step->m_pixelPosition = QPoint(json["pixelPositionX"].toInt(), json["pixelPositionY"].toInt());
    step->m_pixelColor = QColor(json["pixelColorRed"].toInt(),
                               json["pixelColorGreen"].toInt(),
                               json["pixelColorBlue"].toInt());
    step->m_pixelTolerance = json["pixelTolerance"].toInt(0);
    
    return step;
}

bool MacroStep::isValid() const
{
    switch (m_stepType) {
        case StepType::Click:
        case StepType::Move:
        case StepType::Scroll:
            return !m_position.isNull();
        case StepType::Delay:
            return m_delayMs > 0;
        case StepType::KeyPress:
            return !m_keyCode.isEmpty();
        case StepType::PixelTrigger:
            return !m_pixelPosition.isNull() && m_pixelColor.isValid();
    }
    return false;
}

QStringList MacroStep::validate() const
{
    QStringList errors;
    
    switch (m_stepType) {
        case StepType::Click:
        case StepType::Move:
        case StepType::Scroll:
            if (m_position.isNull()) {
                errors << "Position is required for this step type";
            }
            break;
        case StepType::Delay:
            if (m_delayMs <= 0) {
                errors << "Delay must be greater than 0";
            }
            break;
        case StepType::KeyPress:
            if (m_keyCode.isEmpty()) {
                errors << "Key code is required for key press";
            }
            break;
        case StepType::PixelTrigger:
            if (m_pixelPosition.isNull()) {
                errors << "Pixel position is required for pixel trigger";
            }
            if (!m_pixelColor.isValid()) {
                errors << "Valid pixel color is required for pixel trigger";
            }
            break;
    }
    
    if (m_duration < 0) {
        errors << "Duration cannot be negative";
    }
    
    if (m_delayMs < 0) {
        errors << "Delay cannot be negative";
    }
    
    if (m_pixelTolerance < 0) {
        errors << "Pixel tolerance cannot be negative";
    }
    
    return errors;
}

QString MacroStep::displayName() const
{
    if (!m_description.isEmpty()) {
        return m_description;
    }
    
    QString name = stepTypeString();
    
    switch (m_stepType) {
        case StepType::Click:
            name += QString(" %1 at (%2, %3)").arg(clickTypeString()).arg(m_position.x()).arg(m_position.y());
            break;
        case StepType::Move:
            name += QString(" to (%1, %2)").arg(m_position.x()).arg(m_position.y());
            break;
        case StepType::Delay:
            name += QString(" %1ms").arg(m_delayMs);
            break;
        case StepType::KeyPress:
            name += QString(" '%1'").arg(m_keyCode);
            break;
        case StepType::Scroll:
            name += QString(" %1 at (%2, %3)").arg(m_scrollDelta).arg(m_position.x()).arg(m_position.y());
            break;
        case StepType::PixelTrigger:
            name += QString(" at (%1, %2)").arg(m_pixelPosition.x()).arg(m_pixelPosition.y());
            break;
    }
    
    return name;
}

QString MacroStep::stepTypeString() const
{
    switch (m_stepType) {
        case StepType::Click: return "Click";
        case StepType::Move: return "Move";
        case StepType::Delay: return "Delay";
        case StepType::KeyPress: return "Key Press";
        case StepType::Scroll: return "Scroll";
        case StepType::PixelTrigger: return "Pixel Trigger";
    }
    return "Unknown";
}

QString MacroStep::clickTypeString() const
{
    switch (m_clickType) {
        case ClickType::LeftClick: return "Left";
        case ClickType::RightClick: return "Right";
        case ClickType::MiddleClick: return "Middle";
        case ClickType::DoubleClick: return "Double";
        case ClickType::MouseDown: return "Down";
        case ClickType::MouseUp: return "Up";
        case ClickType::Scroll: return "Scroll";
        case ClickType::KeyPress: return "Key";
    }
    return "Unknown";
}

QString MacroStep::clickModeString() const
{
    switch (m_clickMode) {
        case ClickMode::Single: return "Single";
        case ClickMode::Double: return "Double";
        case ClickMode::Hold: return "Hold";
    }
    return "Unknown";
}

// Factory methods
MacroStep* MacroStep::createClick(const QPoint& position, ClickType type, QObject* parent)
{
    MacroStep* step = new MacroStep(StepType::Click, parent);
    step->setPosition(position);
    step->setClickType(type);
    return step;
}

MacroStep* MacroStep::createMove(const QPoint& position, QObject* parent)
{
    MacroStep* step = new MacroStep(StepType::Move, parent);
    step->setPosition(position);
    return step;
}

MacroStep* MacroStep::createDelay(int delayMs, QObject* parent)
{
    MacroStep* step = new MacroStep(StepType::Delay, parent);
    step->setDelayMs(delayMs);
    return step;
}

MacroStep* MacroStep::createKeyPress(const QString& keyCode, QObject* parent)
{
    MacroStep* step = new MacroStep(StepType::KeyPress, parent);
    step->setKeyCode(keyCode);
    return step;
}

MacroStep* MacroStep::createScroll(const QPoint& position, int delta, QObject* parent)
{
    MacroStep* step = new MacroStep(StepType::Scroll, parent);
    step->setPosition(position);
    step->setScrollDelta(delta);
    return step;
}

MacroStep* MacroStep::createPixelTrigger(const QPoint& position, const QColor& color, int tolerance, QObject* parent)
{
    MacroStep* step = new MacroStep(StepType::PixelTrigger, parent);
    step->setPixelPosition(position);
    step->setPixelColor(color);
    step->setPixelTolerance(tolerance);
    step->setHasPixelTrigger(true);
    return step;
}