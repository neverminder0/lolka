#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQuickStyle>
#include <QDir>
#include <QStandardPaths>
#include <QTranslator>
#include <QLocale>
#include <QQmlContext>

#include "ui/ApplicationController.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    
    // Set application properties
    app.setApplicationName("ClickWeave");
    app.setApplicationVersion(APP_VERSION);
    app.setOrganizationName("ClickWeave");
    app.setOrganizationDomain("clickweave.app");
    
    // Set up data directory
    QString dataDir = QStandardPaths::writableLocation(QStandardPaths::AppDataLocation);
    QDir().mkpath(dataDir);
    
    // Set Quick Controls style
    QQuickStyle::setStyle("Material");
    
    // Set up translations
    QTranslator translator;
    const QStringList uiLanguages = QLocale::system().uiLanguages();
    for (const QString &locale : uiLanguages) {
        const QString baseName = "clickweave_" + QLocale(locale).name();
        if (translator.load(":/translations/" + baseName)) {
            app.installTranslator(&translator);
            break;
        }
    }
    
    // Create application controller
    ApplicationController controller;
    
    // Set up QML engine
    QQmlApplicationEngine engine;
    engine.rootContext()->setContextProperty("applicationController", &controller);
    
    // Load main QML file
    const QUrl url(QStringLiteral("qrc:/ClickWeave/ui/qml/main.qml"));
    QObject::connect(&engine, &QQmlApplicationEngine::objectCreated,
                     &app, [url](QObject *obj, const QUrl &objUrl) {
        if (!obj && url == objUrl)
            QCoreApplication::exit(-1);
    }, Qt::QueuedConnection);
    
    engine.load(url);
    
    return app.exec();
}