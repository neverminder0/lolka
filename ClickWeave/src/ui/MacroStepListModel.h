#pragma once

#include <QAbstractListModel>
#include <QList>

class MacroStep;
class Profile;

class MacroStepListModel : public QAbstractListModel
{
    Q_OBJECT

public:
    enum StepRoles {
        StepRole = Qt::UserRole + 1,
        IndexRole,
        StepTypeRole,
        ClickTypeRole,
        ClickModeRole,
        PositionRole,
        DelayMsRole,
        DurationRole,
        KeyCodeRole,
        DescriptionRole,
        EnabledRole,
        DisplayNameRole
    };

    explicit MacroStepListModel(QObject *parent = nullptr);

    // QAbstractListModel interface
    int rowCount(const QModelIndex &parent = QModelIndex()) const override;
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;
    QHash<int, QByteArray> roleNames() const override;

    // Drag and drop support
    Qt::ItemFlags flags(const QModelIndex &index) const override;
    Qt::DropActions supportedDropActions() const override;
    QStringList mimeTypes() const override;
    QMimeData* mimeData(const QModelIndexList &indexes) const override;
    bool dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) override;

    // Custom methods
    void setProfile(Profile* profile);
    Profile* profile() const { return m_profile; }
    
    void addStep(MacroStep* step);
    void insertStep(int index, MacroStep* step);
    void removeStep(int index);
    void moveStep(int from, int to);
    void clear();
    
    MacroStep* stepAt(int index) const;
    int indexOf(MacroStep* step) const;
    
    void refreshStep(MacroStep* step);

private slots:
    void onStepChanged();
    void onProfileStepsChanged();

private:
    Profile* m_profile = nullptr;
};