#pragma once

#include "../HotkeyManager.h"

#ifdef Q_OS_WIN

#include <QAbstractNativeEventFilter>
#include <QMap>

class WindowsHotkeyManager : public HotkeyManager, public QAbstractNativeEventFilter
{
    Q_OBJECT

public:
    explicit WindowsHotkeyManager(QObject *parent = nullptr);
    ~WindowsHotkeyManager() override;

    bool registerHotkey(HotkeyAction action, const QString& keySequence) override;
    bool unregisterHotkey(HotkeyAction action) override;
    void unregisterAllHotkeys() override;
    bool isHotkeyRegistered(HotkeyAction action) const override;
    void setEnabled(bool enabled) override;
    bool isEnabled() const override;

protected:
    bool nativeEventFilter(const QByteArray &eventType, void *message, long *result) override;

private:
    struct HotkeyData {
        int id;
        unsigned int modifiers;
        unsigned int virtualKey;
    };

    bool parseKeySequence(const QString& keySequence, unsigned int& modifiers, unsigned int& virtualKey);
    unsigned int stringToVirtualKey(const QString& key);
    unsigned int stringToModifier(const QString& modifier);
    int getNextHotkeyId();

private:
    QMap<HotkeyAction, HotkeyData> m_hotkeyData;
    int m_nextHotkeyId = 1;
    static const int HOTKEY_BASE_ID = 0x8000;
};

#endif // Q_OS_WIN