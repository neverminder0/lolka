#include "ClickEngine.h"
#include "Profile.h"
#include "MacroStep.h"
#include <QApplication>
#include <QScreen>
#include <QGuiApplication>
#include <QDebug>
#include <random>

#ifdef Q_OS_WIN
#include "../platform/windows/WindowsClickEngine.h"
#elif defined(Q_OS_MACOS)
#include "../platform/macos/MacOSClickEngine.h"
#elif defined(Q_OS_LINUX)
#include "../platform/linux/LinuxClickEngine.h"
#endif

ClickEngine::ClickEngine(QObject *parent)
    : QObject(parent)
    , m_executionTimer(new QTimer(this))
    , m_statusTimer(new QTimer(this))
{
    m_executionTimer->setSingleShot(true);
    connect(m_executionTimer, &QTimer::timeout, this, &ClickEngine::executeNextStep);
    
    m_statusTimer->setInterval(100); // Update status every 100ms
    connect(m_statusTimer, &QTimer::timeout, this, &ClickEngine::updateStatus);
}

std::unique_ptr<ClickEngine> ClickEngine::create(QObject *parent)
{
#ifdef Q_OS_WIN
    return std::make_unique<WindowsClickEngine>(parent);
#elif defined(Q_OS_MACOS)
    return std::make_unique<MacOSClickEngine>(parent);
#elif defined(Q_OS_LINUX)
    return std::make_unique<LinuxClickEngine>(parent);
#else
    qWarning() << "Unsupported platform for ClickEngine";
    return nullptr;
#endif
}

void ClickEngine::startClicking()
{
    if (!m_currentProfile || m_isRunning) {
        return;
    }
    
    if (m_currentProfile->steps().isEmpty()) {
        emit errorOccurred("No steps defined in profile");
        return;
    }
    
    m_isRunning = true;
    m_isPaused = false;
    m_failsafeTriggered = false;
    
    resetExecution();
    
    m_startTime = std::chrono::steady_clock::now();
    m_statusTimer->start();
    
    // Start with first step after initial delay
    calculateNextDelay();
    
    emit isRunningChanged();
    emit isPausedChanged();
    
    qDebug() << "Started clicking with profile:" << m_currentProfile->name();
}

void ClickEngine::stopClicking()
{
    if (!m_isRunning) {
        return;
    }
    
    m_isRunning = false;
    m_isPaused = false;
    
    m_executionTimer->stop();
    m_statusTimer->stop();
    
    resetExecution();
    
    emit isRunningChanged();
    emit isPausedChanged();
    
    qDebug() << "Stopped clicking";
}

void ClickEngine::pauseClicking()
{
    if (!m_isRunning || m_isPaused) {
        return;
    }
    
    m_isPaused = true;
    m_executionTimer->stop();
    
    emit isPausedChanged();
    
    qDebug() << "Paused clicking";
}

void ClickEngine::resumeClicking()
{
    if (!m_isRunning || !m_isPaused) {
        return;
    }
    
    m_isPaused = false;
    calculateNextDelay();
    
    emit isPausedChanged();
    
    qDebug() << "Resumed clicking";
}

void ClickEngine::emergencyStop()
{
    m_failsafeTriggered = true;
    stopClicking();
    emit errorOccurred("Emergency stop activated");
    qDebug() << "Emergency stop triggered";
}

void ClickEngine::setProfile(Profile* profile)
{
    if (m_isRunning) {
        stopClicking();
    }
    
    m_currentProfile = profile;
    resetExecution();
}

void ClickEngine::executeAction(const ClickAction& action)
{
    if (m_failsafeTriggered) {
        return;
    }
    
    try {
        performClick(action);
        m_clickCount++;
        m_lastClickTime = std::chrono::steady_clock::now();
        
        emit clickExecuted(action.position, action.type);
        emit clickCountChanged();
        
    } catch (const std::exception& e) {
        emit errorOccurred(QString("Click execution failed: %1").arg(e.what()));
    }
}

QPoint ClickEngine::getCurrentMousePosition()
{
    return getMousePosition();
}

QColor ClickEngine::getPixelColor(const QPoint& position)
{
    return capturePixelColor(position);
}

bool ClickEngine::checkPixelTrigger(const QPoint& position, const QColor& targetColor, int tolerance)
{
    QColor currentColor = getPixelColor(position);
    
    if (tolerance == 0) {
        return currentColor == targetColor;
    }
    
    // Check color difference within tolerance
    int rDiff = abs(currentColor.red() - targetColor.red());
    int gDiff = abs(currentColor.green() - targetColor.green());
    int bDiff = abs(currentColor.blue() - targetColor.blue());
    
    return (rDiff <= tolerance && gDiff <= tolerance && bDiff <= tolerance);
}

void ClickEngine::executeNextStep()
{
    if (!m_isRunning || m_isPaused || !m_currentProfile) {
        return;
    }
    
    const auto& steps = m_currentProfile->steps();
    if (m_currentStepIndex >= steps.size()) {
        // Check if we should repeat
        if (m_currentProfile->repeatCount() > 0 && 
            m_currentRepetition < m_currentProfile->repeatCount() - 1) {
            m_currentRepetition++;
            m_currentStepIndex = 0;
        } else if (m_currentProfile->repeatCount() == 0) { // Infinite repeat
            m_currentStepIndex = 0;
        } else {
            // Profile completed
            stopClicking();
            emit profileCompleted();
            return;
        }
    }
    
    if (m_currentStepIndex < steps.size()) {
        const MacroStep* step = steps[m_currentStepIndex];
        
        // Check if this step has pixel trigger conditions
        if (step->hasPixelTrigger()) {
            if (!checkPixelTrigger(step->pixelPosition(), step->pixelColor(), step->pixelTolerance())) {
                // Pixel condition not met, skip this step
                m_currentStepIndex++;
                calculateNextDelay();
                return;
            }
        }
        
        // Execute the step
        ClickAction action;
        action.type = step->clickType();
        action.mode = step->clickMode();
        action.position = step->position();
        action.duration = step->duration();
        action.keyCode = step->keyCode();
        action.scrollDelta = step->scrollDelta();
        
        executeAction(action);
        
        m_currentStepIndex++;
    }
    
    // Schedule next step
    calculateNextDelay();
}

void ClickEngine::updateStatus()
{
    if (!m_isRunning) {
        m_status = "Ready";
    } else if (m_isPaused) {
        m_status = "Paused";
    } else {
        auto now = std::chrono::steady_clock::now();
        auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(now - m_startTime).count();
        m_status = QString("Running (%1s, %2 clicks)").arg(elapsed).arg(m_clickCount);
    }
    
    emit statusChanged();
}

void ClickEngine::resetExecution()
{
    m_currentStepIndex = 0;
    m_currentRepetition = 0;
    m_clickCount = 0;
    m_status = "Ready";
    
    emit clickCountChanged();
    emit statusChanged();
}

void ClickEngine::calculateNextDelay()
{
    if (!m_currentProfile || m_currentStepIndex >= m_currentProfile->steps().size()) {
        return;
    }
    
    int baseInterval = m_currentProfile->intervalMs();
    if (m_currentStepIndex < m_currentProfile->steps().size()) {
        const MacroStep* step = m_currentProfile->steps()[m_currentStepIndex];
        if (step->delayMs() > 0) {
            baseInterval = step->delayMs();
        }
    }
    
    int actualInterval = applyJitter(baseInterval);
    m_executionTimer->start(actualInterval);
}

int ClickEngine::applyJitter(int baseInterval) const
{
    if (!m_currentProfile || m_currentProfile->jitterPercent() == 0) {
        return baseInterval;
    }
    
    static std::random_device rd;
    static std::mt19937 gen(rd());
    
    double jitterRange = baseInterval * (m_currentProfile->jitterPercent() / 100.0);
    std::uniform_real_distribution<> dis(-jitterRange, jitterRange);
    
    int jitter = static_cast<int>(dis(gen));
    return std::max(1, baseInterval + jitter); // Ensure minimum 1ms interval
}