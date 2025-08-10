#pragma once

#include <QObject>
#include <QString>
#include <QMap>
#include <functional>

enum class HotkeyAction {
    StartStop,
    Pause,
    EmergencyStop
};

class HotkeyManager : public QObject
{
    Q_OBJECT

public:
    explicit HotkeyManager(QObject *parent = nullptr);
    virtual ~HotkeyManager() = default;

    // Factory method for platform-specific implementations
    static HotkeyManager* create(QObject *parent = nullptr);

    // Register/unregister hotkeys
    virtual bool registerHotkey(HotkeyAction action, const QString& keySequence) = 0;
    virtual bool unregisterHotkey(HotkeyAction action) = 0;
    virtual void unregisterAllHotkeys() = 0;

    // Check if hotkey is registered
    virtual bool isHotkeyRegistered(HotkeyAction action) const = 0;
    
    // Get current key sequence for action
    QString getKeySequence(HotkeyAction action) const;
    
    // Enable/disable hotkey processing
    virtual void setEnabled(bool enabled) = 0;
    virtual bool isEnabled() const = 0;

signals:
    void hotkeyTriggered(HotkeyAction action);
    void hotkeyRegistered(HotkeyAction action, const QString& keySequence);
    void hotkeyUnregistered(HotkeyAction action);
    void errorOccurred(const QString& error);

protected:
    // Helper methods
    QString actionToString(HotkeyAction action) const;
    HotkeyAction stringToAction(const QString& actionStr) const;

protected:
    QMap<HotkeyAction, QString> m_registeredHotkeys;
    bool m_enabled = true;
};