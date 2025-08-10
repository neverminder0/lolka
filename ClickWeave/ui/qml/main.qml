import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts 1.15
import QtQuick.Window 2.15
import ClickWeave 1.0

ApplicationWindow {
    id: mainWindow
    
    width: 1200
    height: 800
    minimumWidth: 800
    minimumHeight: 600
    
    title: qsTr("ClickWeave - Auto Clicker")
    
    Material.theme: applicationController.darkMode ? Material.Dark : Material.Light
    Material.accent: Material.Blue
    Material.primary: Material.Blue
    
    property bool isRunning: applicationController.clickEngine.isRunning
    property bool isPaused: applicationController.clickEngine.isPaused
    
    // Global shortcuts overlay
    Item {
        anchors.fill: parent
        focus: true
        
        Keys.onPressed: (event) => {
            if (event.key === Qt.Key_F8) {
                applicationController.toggleClicking()
                event.accepted = true
            } else if (event.key === Qt.Key_F7) {
                applicationController.pauseClicking()
                event.accepted = true
            } else if (event.key === Qt.Key_Escape) {
                applicationController.emergencyStop()
                event.accepted = true
            }
        }
    }
    
    header: ToolBar {
        Material.theme: Material.Dark
        
        RowLayout {
            anchors.fill: parent
            anchors.margins: 8
            
            Label {
                text: qsTr("ClickWeave")
                font.pixelSize: 20
                font.bold: true
                color: Material.accent
            }
            
            Item { Layout.fillWidth: true }
            
            StatusChip {
                id: statusChip
                status: applicationController.clickEngine.status
                isRunning: mainWindow.isRunning
                isPaused: mainWindow.isPaused
                clickCount: applicationController.clickEngine.clickCount
            }
            
            Item { width: 16 }
            
            ToolButton {
                icon.source: applicationController.darkMode ? "qrc:/icons/sun.svg" : "qrc:/icons/moon.svg"
                onClicked: applicationController.darkMode = !applicationController.darkMode
                ToolTip.text: qsTr("Toggle theme")
            }
            
            ToolButton {
                icon.source: "qrc:/icons/settings.svg"
                onClicked: stackView.push(settingsComponent)
                ToolTip.text: qsTr("Settings")
            }
        }
    }
    
    StackView {
        id: stackView
        anchors.fill: parent
        
        initialItem: HomeView {
            onProfileSelected: (profile) => {
                stackView.push(profileComponent, {"profile": profile})
            }
            
            onNewProfile: {
                stackView.push(profileComponent, {"profile": null})
            }
        }
    }
    
    // Global action buttons overlay
    Rectangle {
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.margins: 20
        
        width: actionColumn.width + 20
        height: actionColumn.height + 20
        
        color: Material.dialogColor
        radius: 12
        
        Material.elevation: 8
        
        Column {
            id: actionColumn
            anchors.centerIn: parent
            spacing: 8
            
            Button {
                id: startStopButton
                
                width: 120
                height: 48
                
                text: {
                    if (isRunning && !isPaused) return qsTr("Stop (F8)")
                    if (isPaused) return qsTr("Resume (F8)")
                    return qsTr("Start (F8)")
                }
                
                Material.background: {
                    if (isRunning && !isPaused) return Material.Red
                    if (isPaused) return Material.Orange
                    return Material.Green
                }
                
                icon.source: {
                    if (isRunning && !isPaused) return "qrc:/icons/stop.svg"
                    if (isPaused) return "qrc:/icons/play.svg"
                    return "qrc:/icons/play.svg"
                }
                
                enabled: applicationController.currentProfile !== null
                
                onClicked: applicationController.toggleClicking()
            }
            
            Button {
                width: 120
                height: 36
                
                text: qsTr("Pause (F7)")
                Material.background: Material.Orange
                icon.source: "qrc:/icons/pause.svg"
                
                enabled: isRunning && !isPaused
                visible: isRunning
                
                onClicked: applicationController.pauseClicking()
            }
            
            Button {
                width: 120
                height: 36
                
                text: qsTr("Emergency (Esc)")
                Material.background: Material.Red
                icon.source: "qrc:/icons/stop.svg"
                
                enabled: isRunning
                visible: isRunning
                
                onClicked: applicationController.emergencyStop()
            }
        }
    }
    
    // Profile view component
    Component {
        id: profileComponent
        ProfileView {
            onBack: stackView.pop()
        }
    }
    
    // Settings view component
    Component {
        id: settingsComponent
        SettingsView {
            onBack: stackView.pop()
        }
    }
    
    // Error dialog
    Dialog {
        id: errorDialog
        anchors.centerIn: parent
        
        title: qsTr("Error")
        modal: true
        
        property string errorMessage: ""
        
        Label {
            text: errorDialog.errorMessage
            wrapMode: Text.Wrap
        }
        
        standardButtons: Dialog.Ok
    }
    
    // Connect to application controller signals
    Connections {
        target: applicationController.clickEngine
        
        function onErrorOccurred(error) {
            errorDialog.errorMessage = error
            errorDialog.open()
        }
    }
    
    Component.onCompleted: {
        // Set up default hotkeys
        applicationController.setupDefaultHotkeys()
    }
}