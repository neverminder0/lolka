#pragma once

#include <QObject>
#include <QString>
#include <QDateTime>
#include <QJsonObject>
#include <QJsonArray>
#include <QList>
#include <memory>

class MacroStep;

class Profile : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString name READ name WRITE setName NOTIFY nameChanged)
    Q_PROPERTY(QString description READ description WRITE setDescription NOTIFY descriptionChanged)
    Q_PROPERTY(int intervalMs READ intervalMs WRITE setIntervalMs NOTIFY intervalMsChanged)
    Q_PROPERTY(int jitterPercent READ jitterPercent WRITE setJitterPercent NOTIFY jitterPercentChanged)
    Q_PROPERTY(int repeatCount READ repeatCount WRITE setRepeatCount NOTIFY repeatCountChanged)
    Q_PROPERTY(int maxDurationMs READ maxDurationMs WRITE setMaxDurationMs NOTIFY maxDurationMsChanged)
    Q_PROPERTY(QString targetWindowTitle READ targetWindowTitle WRITE setTargetWindowTitle NOTIFY targetWindowTitleChanged)
    Q_PROPERTY(QString targetProcessName READ targetProcessName WRITE setTargetProcessName NOTIFY targetProcessNameChanged)
    Q_PROPERTY(bool enabled READ enabled WRITE setEnabled NOTIFY enabledChanged)
    Q_PROPERTY(QDateTime scheduledStart READ scheduledStart WRITE setScheduledStart NOTIFY scheduledStartChanged)
    Q_PROPERTY(QString cronExpression READ cronExpression WRITE setCronExpression NOTIFY cronExpressionChanged)

public:
    explicit Profile(QObject *parent = nullptr);
    explicit Profile(const QString& name, QObject *parent = nullptr);
    ~Profile() = default;

    // Basic properties
    QString name() const { return m_name; }
    void setName(const QString& name);

    QString description() const { return m_description; }
    void setDescription(const QString& description);

    // Timing properties
    int intervalMs() const { return m_intervalMs; }
    void setIntervalMs(int interval);

    int jitterPercent() const { return m_jitterPercent; }
    void setJitterPercent(int percent);

    int repeatCount() const { return m_repeatCount; }
    void setRepeatCount(int count);

    int maxDurationMs() const { return m_maxDurationMs; }
    void setMaxDurationMs(int duration);

    // Targeting properties
    QString targetWindowTitle() const { return m_targetWindowTitle; }
    void setTargetWindowTitle(const QString& title);

    QString targetProcessName() const { return m_targetProcessName; }
    void setTargetProcessName(const QString& name);

    // State properties
    bool enabled() const { return m_enabled; }
    void setEnabled(bool enabled);

    // Scheduling properties
    QDateTime scheduledStart() const { return m_scheduledStart; }
    void setScheduledStart(const QDateTime& start);

    QString cronExpression() const { return m_cronExpression; }
    void setCronExpression(const QString& expression);

    // Step management
    QList<MacroStep*> steps() const { return m_steps; }
    void addStep(MacroStep* step);
    void insertStep(int index, MacroStep* step);
    void removeStep(int index);
    void removeStep(MacroStep* step);
    void moveStep(int from, int to);
    void clearSteps();
    int stepCount() const { return m_steps.size(); }

    // Serialization
    QJsonObject toJson() const;
    static Profile* fromJson(const QJsonObject& json, QObject* parent = nullptr);
    bool saveToFile(const QString& filePath) const;
    static Profile* loadFromFile(const QString& filePath, QObject* parent = nullptr);

    // Validation
    bool isValid() const;
    QStringList validate() const;

    // Statistics
    QDateTime createdAt() const { return m_createdAt; }
    QDateTime lastModified() const { return m_lastModified; }
    QDateTime lastRun() const { return m_lastRun; }
    int totalRuns() const { return m_totalRuns; }
    int totalClicks() const { return m_totalClicks; }

public slots:
    void recordRun(int clickCount);
    void resetStatistics();

signals:
    void nameChanged();
    void descriptionChanged();
    void intervalMsChanged();
    void jitterPercentChanged();
    void repeatCountChanged();
    void maxDurationMsChanged();
    void targetWindowTitleChanged();
    void targetProcessNameChanged();
    void enabledChanged();
    void scheduledStartChanged();
    void cronExpressionChanged();
    void stepsChanged();
    void statisticsChanged();

private:
    void updateLastModified();

private:
    QString m_name;
    QString m_description;
    int m_intervalMs = 1000; // Default 1 second
    int m_jitterPercent = 0; // No jitter by default
    int m_repeatCount = 1; // Run once by default (0 = infinite)
    int m_maxDurationMs = 0; // No duration limit by default
    QString m_targetWindowTitle;
    QString m_targetProcessName;
    bool m_enabled = true;
    QDateTime m_scheduledStart;
    QString m_cronExpression;
    
    QList<MacroStep*> m_steps;
    
    // Metadata
    QDateTime m_createdAt;
    QDateTime m_lastModified;
    QDateTime m_lastRun;
    int m_totalRuns = 0;
    int m_totalClicks = 0;
};