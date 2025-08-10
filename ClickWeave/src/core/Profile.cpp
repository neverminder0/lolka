#include "Profile.h"
#include "MacroStep.h"
#include <QJsonDocument>
#include <QJsonArray>
#include <QFile>
#include <QFileInfo>
#include <QDir>
#include <QDebug>

Profile::Profile(QObject *parent)
    : QObject(parent)
    , m_createdAt(QDateTime::currentDateTime())
    , m_lastModified(QDateTime::currentDateTime())
{
}

Profile::Profile(const QString& name, QObject *parent)
    : QObject(parent)
    , m_name(name)
    , m_createdAt(QDateTime::currentDateTime())
    , m_lastModified(QDateTime::currentDateTime())
{
}

void Profile::setName(const QString& name)
{
    if (m_name != name) {
        m_name = name;
        updateLastModified();
        emit nameChanged();
    }
}

void Profile::setDescription(const QString& description)
{
    if (m_description != description) {
        m_description = description;
        updateLastModified();
        emit descriptionChanged();
    }
}

void Profile::setIntervalMs(int interval)
{
    if (m_intervalMs != interval && interval > 0) {
        m_intervalMs = interval;
        updateLastModified();
        emit intervalMsChanged();
    }
}

void Profile::setJitterPercent(int percent)
{
    if (m_jitterPercent != percent && percent >= 0 && percent <= 100) {
        m_jitterPercent = percent;
        updateLastModified();
        emit jitterPercentChanged();
    }
}

void Profile::setRepeatCount(int count)
{
    if (m_repeatCount != count && count >= 0) {
        m_repeatCount = count;
        updateLastModified();
        emit repeatCountChanged();
    }
}

void Profile::setMaxDurationMs(int duration)
{
    if (m_maxDurationMs != duration && duration >= 0) {
        m_maxDurationMs = duration;
        updateLastModified();
        emit maxDurationMsChanged();
    }
}

void Profile::setTargetWindowTitle(const QString& title)
{
    if (m_targetWindowTitle != title) {
        m_targetWindowTitle = title;
        updateLastModified();
        emit targetWindowTitleChanged();
    }
}

void Profile::setTargetProcessName(const QString& name)
{
    if (m_targetProcessName != name) {
        m_targetProcessName = name;
        updateLastModified();
        emit targetProcessNameChanged();
    }
}

void Profile::setEnabled(bool enabled)
{
    if (m_enabled != enabled) {
        m_enabled = enabled;
        updateLastModified();
        emit enabledChanged();
    }
}

void Profile::setScheduledStart(const QDateTime& start)
{
    if (m_scheduledStart != start) {
        m_scheduledStart = start;
        updateLastModified();
        emit scheduledStartChanged();
    }
}

void Profile::setCronExpression(const QString& expression)
{
    if (m_cronExpression != expression) {
        m_cronExpression = expression;
        updateLastModified();
        emit cronExpressionChanged();
    }
}

void Profile::addStep(MacroStep* step)
{
    if (step && !m_steps.contains(step)) {
        step->setParent(this);
        m_steps.append(step);
        updateLastModified();
        emit stepsChanged();
    }
}

void Profile::insertStep(int index, MacroStep* step)
{
    if (step && !m_steps.contains(step) && index >= 0 && index <= m_steps.size()) {
        step->setParent(this);
        m_steps.insert(index, step);
        updateLastModified();
        emit stepsChanged();
    }
}

void Profile::removeStep(int index)
{
    if (index >= 0 && index < m_steps.size()) {
        MacroStep* step = m_steps.takeAt(index);
        step->deleteLater();
        updateLastModified();
        emit stepsChanged();
    }
}

void Profile::removeStep(MacroStep* step)
{
    int index = m_steps.indexOf(step);
    if (index >= 0) {
        removeStep(index);
    }
}

void Profile::moveStep(int from, int to)
{
    if (from >= 0 && from < m_steps.size() && to >= 0 && to < m_steps.size() && from != to) {
        m_steps.move(from, to);
        updateLastModified();
        emit stepsChanged();
    }
}

void Profile::clearSteps()
{
    for (MacroStep* step : m_steps) {
        step->deleteLater();
    }
    m_steps.clear();
    updateLastModified();
    emit stepsChanged();
}

QJsonObject Profile::toJson() const
{
    QJsonObject json;
    json["name"] = m_name;
    json["description"] = m_description;
    json["intervalMs"] = m_intervalMs;
    json["jitterPercent"] = m_jitterPercent;
    json["repeatCount"] = m_repeatCount;
    json["maxDurationMs"] = m_maxDurationMs;
    json["targetWindowTitle"] = m_targetWindowTitle;
    json["targetProcessName"] = m_targetProcessName;
    json["enabled"] = m_enabled;
    json["scheduledStart"] = m_scheduledStart.toString(Qt::ISODate);
    json["cronExpression"] = m_cronExpression;
    json["createdAt"] = m_createdAt.toString(Qt::ISODate);
    json["lastModified"] = m_lastModified.toString(Qt::ISODate);
    json["lastRun"] = m_lastRun.toString(Qt::ISODate);
    json["totalRuns"] = m_totalRuns;
    json["totalClicks"] = m_totalClicks;
    
    QJsonArray stepsArray;
    for (const MacroStep* step : m_steps) {
        stepsArray.append(step->toJson());
    }
    json["steps"] = stepsArray;
    
    return json;
}

Profile* Profile::fromJson(const QJsonObject& json, QObject* parent)
{
    Profile* profile = new Profile(parent);
    
    profile->m_name = json["name"].toString();
    profile->m_description = json["description"].toString();
    profile->m_intervalMs = json["intervalMs"].toInt(1000);
    profile->m_jitterPercent = json["jitterPercent"].toInt(0);
    profile->m_repeatCount = json["repeatCount"].toInt(1);
    profile->m_maxDurationMs = json["maxDurationMs"].toInt(0);
    profile->m_targetWindowTitle = json["targetWindowTitle"].toString();
    profile->m_targetProcessName = json["targetProcessName"].toString();
    profile->m_enabled = json["enabled"].toBool(true);
    profile->m_scheduledStart = QDateTime::fromString(json["scheduledStart"].toString(), Qt::ISODate);
    profile->m_cronExpression = json["cronExpression"].toString();
    profile->m_createdAt = QDateTime::fromString(json["createdAt"].toString(), Qt::ISODate);
    profile->m_lastModified = QDateTime::fromString(json["lastModified"].toString(), Qt::ISODate);
    profile->m_lastRun = QDateTime::fromString(json["lastRun"].toString(), Qt::ISODate);
    profile->m_totalRuns = json["totalRuns"].toInt(0);
    profile->m_totalClicks = json["totalClicks"].toInt(0);
    
    // Load steps
    QJsonArray stepsArray = json["steps"].toArray();
    for (const QJsonValue& stepValue : stepsArray) {
        MacroStep* step = MacroStep::fromJson(stepValue.toObject(), profile);
        if (step) {
            profile->m_steps.append(step);
        }
    }
    
    return profile;
}

bool Profile::saveToFile(const QString& filePath) const
{
    QFileInfo fileInfo(filePath);
    QDir().mkpath(fileInfo.absolutePath());
    
    QFile file(filePath);
    if (!file.open(QIODevice::WriteOnly)) {
        qWarning() << "Failed to open file for writing:" << filePath;
        return false;
    }
    
    QJsonDocument doc(toJson());
    file.write(doc.toJson());
    return true;
}

Profile* Profile::loadFromFile(const QString& filePath, QObject* parent)
{
    QFile file(filePath);
    if (!file.open(QIODevice::ReadOnly)) {
        qWarning() << "Failed to open file for reading:" << filePath;
        return nullptr;
    }
    
    QJsonParseError error;
    QJsonDocument doc = QJsonDocument::fromJson(file.readAll(), &error);
    if (error.error != QJsonParseError::NoError) {
        qWarning() << "JSON parse error:" << error.errorString();
        return nullptr;
    }
    
    return fromJson(doc.object(), parent);
}

bool Profile::isValid() const
{
    return !m_name.isEmpty() && m_intervalMs > 0;
}

QStringList Profile::validate() const
{
    QStringList errors;
    
    if (m_name.isEmpty()) {
        errors << "Profile name cannot be empty";
    }
    
    if (m_intervalMs <= 0) {
        errors << "Interval must be greater than 0";
    }
    
    if (m_jitterPercent < 0 || m_jitterPercent > 100) {
        errors << "Jitter percent must be between 0 and 100";
    }
    
    if (m_repeatCount < 0) {
        errors << "Repeat count cannot be negative";
    }
    
    if (m_maxDurationMs < 0) {
        errors << "Max duration cannot be negative";
    }
    
    return errors;
}

void Profile::recordRun(int clickCount)
{
    m_lastRun = QDateTime::currentDateTime();
    m_totalRuns++;
    m_totalClicks += clickCount;
    emit statisticsChanged();
}

void Profile::resetStatistics()
{
    m_totalRuns = 0;
    m_totalClicks = 0;
    m_lastRun = QDateTime();
    emit statisticsChanged();
}

void Profile::updateLastModified()
{
    m_lastModified = QDateTime::currentDateTime();
}