#pragma once

#include <QObject>
#include <QString>
#include <QQmlEngine>
#include <memory>

class ClickEngine;
class Profile;
class ProfileListModel;
class MacroStepListModel;
class HotkeyManager;
class WindowBinder;
class Logger;
class SettingsStore;

class ApplicationController : public QObject
{
    Q_OBJECT
    QML_ELEMENT
    
    Q_PROPERTY(ClickEngine* clickEngine READ clickEngine CONSTANT)
    Q_PROPERTY(ProfileListModel* profileListModel READ profileListModel CONSTANT)
    Q_PROPERTY(Profile* currentProfile READ currentProfile NOTIFY currentProfileChanged)
    Q_PROPERTY(bool darkMode READ darkMode WRITE setDarkMode NOTIFY darkModeChanged)
    Q_PROPERTY(QString language READ language WRITE setLanguage NOTIFY languageChanged)
    Q_PROPERTY(int profileCount READ profileCount NOTIFY profileCountChanged)
    Q_PROPERTY(int totalClicks READ totalClicks NOTIFY totalClicksChanged)
    Q_PROPERTY(double hoursUsed READ hoursUsed NOTIFY hoursUsedChanged)

public:
    explicit ApplicationController(QObject *parent = nullptr);
    ~ApplicationController() override;

    // Property getters
    ClickEngine* clickEngine() const { return m_clickEngine.get(); }
    ProfileListModel* profileListModel() const { return m_profileListModel; }
    Profile* currentProfile() const { return m_currentProfile; }
    bool darkMode() const { return m_darkMode; }
    QString language() const { return m_language; }
    int profileCount() const;
    int totalClicks() const;
    double hoursUsed() const;

    // Property setters
    void setDarkMode(bool dark);
    void setLanguage(const QString& language);

public slots:
    // Profile management
    void createNewProfile(const QString& name = QString());
    void loadProfile(Profile* profile);
    void saveCurrentProfile();
    void deleteProfile(Profile* profile);
    void duplicateProfile(Profile* profile);
    void exportProfile(Profile* profile, const QString& filePath);
    void importProfile(const QString& filePath);
    void filterProfiles(const QString& filter);

    // Click control
    void startClicking();
    void stopClicking();
    void pauseClicking();
    void resumeClicking();
    void toggleClicking();
    void emergencyStop();

    // Hotkey management
    void setupDefaultHotkeys();
    void registerHotkey(const QString& action, const QString& keySequence);
    void unregisterHotkey(const QString& action);

    // Window management
    void bindToWindow(const QString& windowTitle = QString(), const QString& processName = QString());
    void unbindWindow();

    // Coordinate picker
    void startCoordinatePicker();
    void stopCoordinatePicker();

    // Application lifecycle
    void saveSettings();
    void loadSettings();
    void resetSettings();

signals:
    void currentProfileChanged();
    void darkModeChanged();
    void languageChanged();
    void profileCountChanged();
    void totalClicksChanged();
    void hoursUsedChanged();
    
    void profileCreated(Profile* profile);
    void profileDeleted(Profile* profile);
    void profileLoaded(Profile* profile);
    
    void coordinatesPicked(int x, int y);
    void windowBound(const QString& windowTitle);
    void windowUnbound();
    
    void errorOccurred(const QString& error);
    void messageReceived(const QString& message);

private slots:
    void onHotkeyTriggered(int action);
    void onProfileCompleted();
    void onClickExecuted();

private:
    void initializeComponents();
    void connectSignals();
    void loadProfiles();
    void updateStatistics();

private:
    std::unique_ptr<ClickEngine> m_clickEngine;
    std::unique_ptr<HotkeyManager> m_hotkeyManager;
    std::unique_ptr<WindowBinder> m_windowBinder;
    std::unique_ptr<Logger> m_logger;
    std::unique_ptr<SettingsStore> m_settingsStore;
    
    ProfileListModel* m_profileListModel;
    Profile* m_currentProfile = nullptr;
    
    bool m_darkMode = false;
    QString m_language = "en";
    bool m_coordinatePickerActive = false;
    
    // Statistics
    int m_totalClicks = 0;
    double m_hoursUsed = 0.0;
};