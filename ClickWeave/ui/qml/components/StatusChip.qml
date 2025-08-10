import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: statusChip
    
    property string status: "Ready"
    property bool isRunning: false
    property bool isPaused: false
    property int clickCount: 0
    
    height: 32
    width: statusRow.width + 16
    radius: 16
    
    color: {
        if (isRunning && !isPaused) return Material.Green
        if (isPaused) return Material.Orange
        if (isRunning) return Material.Red
        return Material.color(Material.Grey, Material.Shade400)
    }
    
    RowLayout {
        id: statusRow
        anchors.centerIn: parent
        spacing: 8
        
        Rectangle {
            width: 8
            height: 8
            radius: 4
            color: "white"
            
            SequentialAnimation on opacity {
                running: isRunning && !isPaused
                loops: Animation.Infinite
                NumberAnimation { to: 0.3; duration: 800 }
                NumberAnimation { to: 1.0; duration: 800 }
            }
        }
        
        Label {
            text: {
                if (isRunning && !isPaused) return qsTr("Running")
                if (isPaused) return qsTr("Paused")
                return status
            }
            color: "white"
            font.pixelSize: 12
            font.bold: true
        }
        
        Label {
            text: clickCount > 0 ? "(" + clickCount + ")" : ""
            color: "white"
            font.pixelSize: 10
            visible: clickCount > 0
        }
    }
}