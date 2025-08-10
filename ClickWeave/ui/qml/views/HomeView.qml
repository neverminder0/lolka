import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts 1.15
import "../components"

Page {
    id: homeView
    
    signal profileSelected(var profile)
    signal newProfile()
    
    title: qsTr("ClickWeave")
    
    ScrollView {
        anchors.fill: parent
        anchors.margins: 20
        
        ColumnLayout {
            width: homeView.width - 40
            spacing: 24
            
            // Welcome section
            Card {
                Layout.fillWidth: true
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 24
                    spacing: 16
                    
                    RowLayout {
                        Layout.fillWidth: true
                        
                        Image {
                            source: "qrc:/icons/app-icon.png"
                            sourceSize.width: 64
                            sourceSize.height: 64
                        }
                        
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 4
                            
                            Label {
                                text: qsTr("Welcome to ClickWeave")
                                font.pixelSize: 28
                                font.bold: true
                                color: Material.accent
                            }
                            
                            Label {
                                text: qsTr("Productivity-focused auto-clicker for UI testing and automation")
                                font.pixelSize: 14
                                color: Material.hintTextColor
                            }
                        }
                        
                        Item { Layout.fillWidth: true }
                        
                        Button {
                            text: qsTr("New Profile")
                            Material.background: Material.accent
                            icon.source: "qrc:/icons/plus.svg"
                            onClicked: homeView.newProfile()
                        }
                    }
                }
            }
            
            // Quick stats
            RowLayout {
                Layout.fillWidth: true
                spacing: 16
                
                Card {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 100
                    
                    ColumnLayout {
                        anchors.centerIn: parent
                        spacing: 8
                        
                        Label {
                            text: applicationController.profileCount.toString()
                            font.pixelSize: 32
                            font.bold: true
                            color: Material.accent
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Label {
                            text: qsTr("Profiles")
                            font.pixelSize: 14
                            color: Material.hintTextColor
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }
                }
                
                Card {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 100
                    
                    ColumnLayout {
                        anchors.centerIn: parent
                        spacing: 8
                        
                        Label {
                            text: applicationController.totalClicks.toString()
                            font.pixelSize: 32
                            font.bold: true
                            color: Material.Green
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Label {
                            text: qsTr("Total Clicks")
                            font.pixelSize: 14
                            color: Material.hintTextColor
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }
                }
                
                Card {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 100
                    
                    ColumnLayout {
                        anchors.centerIn: parent
                        spacing: 8
                        
                        Label {
                            text: applicationController.hoursUsed.toFixed(1)
                            font.pixelSize: 32
                            font.bold: true
                            color: Material.Orange
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Label {
                            text: qsTr("Hours Used")
                            font.pixelSize: 14
                            color: Material.hintTextColor
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }
                }
            }
            
            // Recent profiles section
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 16
                
                RowLayout {
                    Layout.fillWidth: true
                    
                    Label {
                        text: qsTr("Click Profiles")
                        font.pixelSize: 20
                        font.bold: true
                    }
                    
                    Item { Layout.fillWidth: true }
                    
                    TextField {
                        id: searchField
                        placeholderText: qsTr("Search profiles...")
                        Layout.preferredWidth: 250
                        
                        onTextChanged: applicationController.filterProfiles(text)
                    }
                }
                
                GridLayout {
                    Layout.fillWidth: true
                    columns: Math.max(1, Math.floor(homeView.width / 320))
                    columnSpacing: 16
                    rowSpacing: 16
                    
                    Repeater {
                        model: applicationController.profileListModel
                        
                        ProfileCard {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 200
                            
                            profile: model.profile
                            
                            onClicked: homeView.profileSelected(model.profile)
                            onDeleteRequested: applicationController.deleteProfile(model.profile)
                            onDuplicateRequested: applicationController.duplicateProfile(model.profile)
                        }
                    }
                }
                
                // Empty state
                Card {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 200
                    visible: applicationController.profileListModel.rowCount() === 0
                    
                    ColumnLayout {
                        anchors.centerIn: parent
                        spacing: 16
                        
                        Image {
                            source: "qrc:/icons/profile.svg"
                            sourceSize.width: 64
                            sourceSize.height: 64
                            opacity: 0.5
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Label {
                            text: qsTr("No profiles yet")
                            font.pixelSize: 18
                            color: Material.hintTextColor
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Label {
                            text: qsTr("Create your first profile to get started")
                            font.pixelSize: 14
                            color: Material.hintTextColor
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Button {
                            text: qsTr("Create Profile")
                            Material.background: Material.accent
                            onClicked: homeView.newProfile()
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }
                }
            }
            
            // Tips section
            Card {
                Layout.fillWidth: true
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 24
                    spacing: 16
                    
                    Label {
                        text: qsTr("Tips & Shortcuts")
                        font.pixelSize: 18
                        font.bold: true
                    }
                    
                    GridLayout {
                        Layout.fillWidth: true
                        columns: 2
                        columnSpacing: 24
                        rowSpacing: 12
                        
                        Label {
                            text: qsTr("F8")
                            font.bold: true
                            color: Material.accent
                        }
                        Label {
                            text: qsTr("Start/Stop clicking")
                            Layout.fillWidth: true
                        }
                        
                        Label {
                            text: qsTr("F7")
                            font.bold: true
                            color: Material.accent
                        }
                        Label {
                            text: qsTr("Pause/Resume clicking")
                            Layout.fillWidth: true
                        }
                        
                        Label {
                            text: qsTr("Esc")
                            font.bold: true
                            color: Material.Red
                        }
                        Label {
                            text: qsTr("Emergency stop (works anywhere)")
                            Layout.fillWidth: true
                        }
                        
                        Label {
                            text: qsTr("Tip")
                            font.bold: true
                            color: Material.Green
                        }
                        Label {
                            text: qsTr("Move mouse to screen corner for failsafe stop")
                            Layout.fillWidth: true
                        }
                    }
                }
            }
        }
    }
}