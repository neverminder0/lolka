import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

Rectangle {
    id: card
    
    color: Material.cardColor
    radius: 8
    
    // Material elevation shadow effect
    layer.enabled: true
    layer.effect: DropShadow {
        horizontalOffset: 0
        verticalOffset: 2
        radius: 8
        color: "#40000000"
        samples: 16
    }
    
    // Hover effect
    property bool hoverEnabled: false
    property bool hovered: false
    
    states: [
        State {
            name: "hovered"
            when: hoverEnabled && hovered
            PropertyChanges {
                target: card
                layer.effect.radius: 12
                layer.effect.verticalOffset: 4
            }
        }
    ]
    
    transitions: [
        Transition {
            NumberAnimation {
                properties: "radius,verticalOffset"
                duration: 150
                easing.type: Easing.OutCubic
            }
        }
    ]
    
    MouseArea {
        anchors.fill: parent
        hoverEnabled: card.hoverEnabled
        onEntered: card.hovered = true
        onExited: card.hovered = false
        propagateComposedEvents: true
    }
}